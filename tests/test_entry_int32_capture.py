"""Authored entry captures, attempt isolation and atomic failure regressions."""
from dataclasses import fields
import bisect
from types import SimpleNamespace as NS

import pytest
from iced_x86 import Decoder, Mnemonic

from il2cpp import Decompiler, Expr, Il2Cpp, Lifter, Metadata, MethodDef, ParamDef, TypeDef
from il2cpp.cfg import Block, _Sink
from il2cpp.dec.entrycapture import (
    ArenaDeclined, _marker_reservations, _mutable_graph, isolated_clone,
    recover_entry_int32,
)
from il2cpp.expr import _RegState
from il2cpp.lifter.entrycapture import EntryCaptureDeclined, EntryInt32Captures
from il2cpp.runtime.types import _SYNTH_NEXT_VA
from test_entry_int32_origin import setup, MOVD, CVT
from test_native_unwind_boundary import BASE, image
from test_simd_field_conversion import seeded

INT = (0, 8 << 16)
FLOAT = (0, 12 << 16)
MARKER = '__il2cpp_capture_i32_0'
ALIAS = '__il2cpp_entry_i32_0'


def context(*, real=True, reserved=(), name='p0', body=MOVD + CVT + 'c3'):
    origin, lift, conversion = setup(body)
    lift.meta.method_params(origin.method)[0].name = name
    lift.dry = not real
    value = Expr(name, INT, 'int')
    lift.regs = {'RCX': value, 'XMM0': value}
    cap = EntryInt32Captures(lift.il, origin.method, origin.insns, reserved=reserved)
    cap.bind_entry(lift, origin.method, real=real)
    return cap, lift, conversion, value


def converted(**kwargs):
    cap, lift, ins, value = context(**kwargs)
    clone = cap.conversion_input(lift, ins, lift.out.block.insns, value)
    assert clone is not None
    return cap, lift, ins, value, clone


def finish(cap, lines):
    return cap.finalize(lines, Decompiler._mask_literals)


def test_conversion_clones_only_its_operand_without_register_uses():
    cap, lift, ins, value, clone = converted()
    assert clone is not value and clone.text == MARKER
    assert clone.ty == INT and clone.kind == 'int'
    assert lift.regs == {'RCX': value, 'XMM0': value}
    assert value.text == 'p0' and value.ty == INT and value.kind == 'int'
    assert value._uses is None and value._use_ip == -1
    assert getattr(value, '_parts', None) is None


@pytest.mark.parametrize('real', [False, True])
def test_binding_uses_explicit_phase_not_stale_dry_value(real):
    cap, lift, ins, old = context(real=not real)
    current = Expr('p0', INT, 'int')
    lift.regs = {'RCX': current, 'XMM0': current}
    # At _setup_entry, dry is still the *preceding* pass's value.
    cap.bind_entry(lift, cap.method, real=real)
    lift.dry = not real
    assert cap.conversion_input(lift, ins, lift.out.block.insns, current) is not None
    assert cap.conversion_input(lift, ins, lift.out.block.insns, old) is None
    if real:
        assert finish(cap, ['return (float)(' + MARKER + ');'])[1] == 1
    else:
        with pytest.raises(EntryCaptureDeclined):
            finish(cap, ['return (float)(' + MARKER + ');'])


def test_pass_rebinding_discards_dry_sites_and_requires_new_expr_identity():
    cap, lift, ins, old, _ = converted(real=False)
    current = Expr('p0', INT, 'int')
    lift.regs = {'RCX': current}
    cap.bind_entry(lift, cap.method, real=True)
    lift.dry = False
    assert cap._used == {}
    assert cap.conversion_input(lift, ins, lift.out.block.insns, old) is None
    assert finish(cap, ['return 1f;']) == (['return 1f;'], 0)
    assert cap.conversion_input(lift, ins, lift.out.block.insns, current) is not None


@pytest.mark.parametrize('change', ['method', 'lift', 'phase', 'block-copy',
                                    'missing-block', 'different-expr'])
def test_conversion_rejects_changed_execution_context(change):
    cap, lift, ins, value = context()
    block = lift.out.block.insns
    if change == 'method':
        lift._current_method = NS(index=0)
    elif change == 'lift':
        lift = NS(**vars(lift))
    elif change == 'phase':
        lift.dry = True
    elif change == 'block-copy':
        block = list(block)
    elif change == 'missing-block':
        lift.out.block = None
    elif change == 'different-expr':
        value = Expr('p0', INT, 'int')
    assert cap.conversion_input(lift, ins, block, value) is None


@pytest.mark.parametrize('mode', ['unknown', 'nobind', 'slice', 'parts', 'bytes',
                                  'stack', 'float', 'object', 'byref', 'text'])
def test_entry_clone_keeps_all_old_scalar_provenance_guards(mode):
    cap, lift, ins, value = context()
    if mode in ('unknown', 'nobind'):
        setattr(value, '_unk' if mode == 'unknown' else '_no_bind', True)
    elif mode in ('slice', 'parts', 'bytes'):
        setattr(value, '_' + mode, [])
    elif mode == 'stack':
        value._stack_offset = 0
    elif mode == 'float':
        value.ty = FLOAT
    elif mode == 'object':
        value.kind = 'obj'
    elif mode == 'byref':
        value.ty = (0, INT[1] | 1 << 29)
    elif mode == 'text':
        value.text = 'tmp1'
    assert cap.conversion_input(lift, ins, lift.out.block.insns, value) is None


@pytest.mark.parametrize('mode', ['other-method', 'other-il', 'other-meta', 'other-bin',
                                  'bad-phase', 'bad-name'])
def test_invalid_rebinding_clears_old_proof_and_used_sites(mode):
    cap, lift, ins, value, _ = converted()
    method, phase = cap.method, True
    if mode == 'other-method':
        method = NS(**vars(method))
    elif mode.startswith('other-'):
        setattr(lift, mode[6:], NS())
    elif mode == 'bad-phase':
        phase = 1
    elif mode == 'bad-name':
        lift.meta.method_params(method)[0].name = 'not.an.identifier'
    cap.bind_entry(lift, method, real=phase)
    assert cap._used == {} and cap._lift is None
    with pytest.raises(EntryCaptureDeclined):
        finish(cap, ['return (float)(' + MARKER + ');'])


@pytest.mark.parametrize('line', [
    'int M = 0;', 'M = 0;', 'M += 1;', 'M++;', '++M;', 'M--;', '--M;',
    'Use(ref M);', 'Use(out M);', 'Use(in M);', 'Use(M);', 'Use((M));',
    'Use(value: M);', 'fixed (int* p = &M) { }', 'return M;',
    'return (double)(M);', 'return (float)(obj.M);', 'return (float)(@M);',
    '// return (float)(M);', '/* return (float)(M); */',
    'return "(float)(M)";', 'return $"{(float)(M)}";',
    'return @"(float)(M)";', "return '(float)(M)';",
])
def test_every_surviving_marker_must_be_only_a_generated_float_operand(line):
    cap, *_ = converted()
    with pytest.raises(EntryCaptureDeclined):
        finish(cap, [line.replace('M', MARKER)])


def test_hidden_and_visible_marker_uses_cannot_silently_drop_a_declaration():
    cap, *_ = converted()
    with pytest.raises(EntryCaptureDeclined):
        finish(cap, ['return (float)(' + MARKER + ');', '// ' + MARKER])


def test_all_uses_and_multiple_occurrences_are_replaced_together():
    cap, *_ = converted()
    lines, count = finish(cap, ['float a = (float)(' + MARKER + ');',
                               'return (float)(' + MARKER + ') + a;'])
    assert count == 1 and lines[0] == 'int ' + ALIAS + ' = p0;'
    assert MARKER not in '\n'.join(lines)
    assert '\n'.join(lines).count(ALIAS) == 3


@pytest.mark.parametrize('collision', [
    'int A = 0;', 'A: ;', 'Use(obj.A);', 'Use(@A);', '// A', 'Use("A");',
])
def test_final_alias_avoids_all_symbol_and_literal_spellings(collision):
    cap, *_ = converted()
    lines, count = finish(cap, [collision.replace('A', ALIAS),
                               'return (float)(' + MARKER + ');'])
    assert count == 1 and lines[0] == 'int ' + ALIAS + '_ = p0;'
    assert lines[1] == collision.replace('A', ALIAS)
    assert lines[2] == 'return (float)(' + ALIAS + '_);'


def test_provisional_marker_avoids_parameters_and_pre_reserved_metadata_names():
    cap, lift, ins, value, clone = converted(reserved={MARKER, MARKER + '_'})
    assert clone.text == MARKER + '__'
    cap, lift, ins, value = context(name=MARKER)
    clone = cap.conversion_input(lift, ins, lift.out.block.insns, value)
    assert clone.text == MARKER + '_'


def test_final_alias_is_fresh_even_for_an_unused_metadata_parameter():
    cap, *_ = converted(name=ALIAS)
    lines, _ = finish(cap, ['return (float)(' + MARKER + ');'])
    assert lines[0] == 'int ' + ALIAS + '_ = ' + ALIAS + ';'


def test_snapshot_is_inserted_inside_canonical_unsafe_envelope_after_cleanup():
    cap, *_ = converted()
    lines, _ = finish(cap, ['unsafe', '{', '    Use();',
                           '    return (float)(' + MARKER + ');', '}'])
    assert lines[:4] == ['unsafe', '{', 'int ' + ALIAS + ' = p0;', '    Use();']


@pytest.mark.parametrize('head', ['unsafe {', '    unsafe', 'unsafe /*x*/'])
def test_unknown_unsafe_envelope_discards_entire_attempt(head):
    cap, *_ = converted()
    with pytest.raises(EntryCaptureDeclined):
        finish(cap, [head, 'return (float)(' + MARKER + ');'])


def test_removed_conversion_does_not_add_unused_entry_captures():
    cap, *_ = converted()
    assert finish(cap, ['return 0f;']) == (['return 0f;'], 0)


def test_coordinate_changing_mask_discards_attempt():
    cap, *_ = converted()
    with pytest.raises(EntryCaptureDeclined):
        cap.finalize(['return (float)(' + MARKER + ');'], lambda s, b: ('', b))


def model():
    """A real model graph with authored metadata, not fixture data or callbacks."""
    binary = image(((0x1000, 0x1400, 0x3000),),
                   text={0x1000: bytes.fromhex(MOVD + CVT + 'c3')})
    method = MethodDef(0, 'Test', 0, 0, 0, -1, 1, 0x10, 0, 0, 1,
                       addr=BASE + 0x1000)
    kwargs = {f.name: 0 for f in fields(TypeDef)}
    kwargs.update(name='Owner', namespace='', generic_container=-1, parent=-1)
    owner = TypeDef(**kwargs)
    meta = Metadata.__new__(Metadata)
    meta.methods, meta.typedefs = [method], [owner]
    meta.params = [ParamDef('p0', 0, 1)]
    meta.d = b'Test\0Owner\0p0\0'
    meta.string_off, meta.string_size = 0, len(meta.d)
    il = Il2Cpp(meta, binary)
    il.types = [FLOAT, INT]
    il.type_sizes = [4]
    il.addr_candidates = {method.addr: [('method', 0)]}
    il._bisect = bisect
    lift = Lifter.__new__(Lifter)
    lift.il, lift.bin, lift.meta = il, binary, meta
    lift._current_method = method
    lift._cur_ip, lift._copying, lift.dry = 0, False, False
    lift._blocks = [Block(0, list(Decoder(64, binary.read(method.addr, 8), ip=method.addr)))]
    lift.regs = _RegState(lift, {'RCX': Expr('p0', INT, 'int')})
    lift.out = _Sink(lift._blocks[0])
    dec = Decompiler(lift)
    dec._flat_insns = lift._blocks[0].insns
    return dec, method, owner


def test_arena_is_disjoint_including_cycles_expr_registers_metadata_and_native_models():
    dec, m, td = model()
    arena, am, at = isolated_clone(dec, m, td)
    before = _mutable_graph((dec, m, td))
    after = _mutable_graph((arena, am, at))
    assert before.keys().isdisjoint(after)
    assert arena.L.regs.L is arena.L
    assert arena.L.il.meta is arena.L.meta and arena.L.il.bin is arena.L.bin
    assert am is arena.L.meta.methods[0] and at is arena.L.meta.typedefs[0]
    assert arena.L.bin.d is dec.L.bin.d  # exact immutable bytes may be shared
    arena.L.regs['RCX'].text = 'changed'
    arena.L.meta.params[0].name = 'changed'
    arena.L.il._chain_cache[0] = {'x': []}
    assert dec.L.regs['RCX'].text == 'p0' and dec.L.meta.params[0].name == 'p0'
    assert not dec.L.il._chain_cache


@pytest.mark.parametrize('resource', [lambda: None, NS(), iter([1]), bytearray(b'x')])
def test_unsupported_callbacks_or_resources_decline_before_attempt(resource):
    dec, m, td = model()
    dec.L.resource = resource
    with pytest.raises(ArenaDeclined):
        isolated_clone(dec, m, td)


def test_private_synthetic_allocator_cannot_advance_the_process_allocator():
    dec, m, td = model()
    arena, _, _ = isolated_clone(dec, m, td)
    before = _SYNTH_NEXT_VA[0]
    result = arena.L.il._synthetic_inst((0, 0x12 << 16), [INT])
    assert result[0] == before and _SYNTH_NEXT_VA[0] == before
    assert not hasattr(dec.L.il, '_synthetic_insts')
    assert arena.L.il._synthetic_allocator[0] == before + 1


def test_metadata_reserves_even_hidden_sanitized_symbols():
    dec, _, _ = model()
    meta = dec.L.meta
    meta.d += (MARKER + '\0hidden-name\0').encode()
    meta.string_size = len(meta.d)
    reserved = _marker_reservations(meta, ['Use(other_name);'])
    assert {MARKER, 'hidden_name', 'other_name'} <= reserved


@pytest.mark.parametrize('spelling, expected_suffix', [
    ('get_' + MARKER, '_'),
    ('set_' + MARKER + '_', '__'),
    ('Owner.' + MARKER, '_'),
    ('public$' + MARKER, '_'),
])
def test_provisional_marker_avoids_derived_metadata_identifier_suffixes(
        spelling, expected_suffix):
    dec, _, _ = model()
    meta = dec.L.meta
    meta.d += (spelling + '\0').encode()
    meta.string_size = len(meta.d)
    reserved = _marker_reservations(meta, [])
    cap, lift, ins, value, clone = converted(reserved=reserved)
    assert clone.text == MARKER + expected_suffix
    assert all(clone.text not in name for name in reserved)
    lines, count = finish(cap, ['return (float)(' + clone.text + ');'])
    alias = ALIAS + expected_suffix
    assert count == 1 and lines == ['int ' + alias + ' = p0;',
                                  'return (float)(' + alias + ');']


@pytest.mark.parametrize('failure', ['clone', 'lift', 'finalize', 'no-survivor'])
def test_failure_returns_exact_baseline_without_mutating_live_runtime(monkeypatch, failure):
    import il2cpp.dec.entrycapture as module
    dec, m, td = model()
    baseline = ['return 99f;']
    before = _SYNTH_NEXT_VA[0]
    monkeypatch.setattr(module, '_candidate', lambda d, m: True)
    def rejected(*args, **kwargs):
        raise ValueError('injected failure')
    def speculative(self, method, owner):
        self.L.regs['RCX'].text = 'attempt-only'
        self.L.il._synthetic_inst((0, 0x12 << 16), [INT])
        self.L._entry_int32_capture._real = True
        if failure == 'lift':
            raise RuntimeError('injected lift failure')
        return ['attempt-only']
    monkeypatch.setattr(Decompiler, '_lift_method', speculative)
    if failure == 'clone':
        monkeypatch.setattr(module, 'isolated_clone', rejected)
    elif failure == 'finalize':
        monkeypatch.setattr(EntryInt32Captures, 'finalize', rejected)
    else:
        monkeypatch.setattr(EntryInt32Captures, 'finalize', lambda *a: (['unused'], 0))
    assert recover_entry_int32(dec, m, td, baseline) is baseline
    assert dec.L.regs['RCX'].text == 'p0'
    assert not hasattr(dec.L.il, '_synthetic_insts') and _SYNTH_NEXT_VA[0] == before
    assert getattr(dec.L, '_entry_int32_capture', None) is None


def test_success_commits_only_output_not_attempt_state(monkeypatch):
    import il2cpp.dec.entrycapture as module
    dec, m, td = model()
    monkeypatch.setattr(module, '_candidate', lambda *a: True)
    def speculative(self, method, owner):
        self.L.regs['RCX'].text = 'attempt-only'
        return ['temporary']
    monkeypatch.setattr(Decompiler, '_lift_method', speculative)
    monkeypatch.setattr(EntryInt32Captures, 'finalize', lambda *a: (['committed'], 1))
    assert recover_entry_int32(dec, m, td, ['baseline']) == ['committed']
    assert dec.L.regs['RCX'].text == 'p0' and dec._entry_int32_status == 'accepted'


def test_instruction_hook_preserves_source_identity_and_all_four_lanes():
    cap, ctx, conversion, _, _ = converted()
    lift = seeded()
    lift.il, lift.meta, lift.bin = ctx.il, ctx.meta, ctx.bin
    lift._current_method = cap.method
    value = Expr('p0', INT, 'int')
    lift.regs = {'RCX': value}
    block = Block(0, ctx.out.block.insns)
    lift.out = _Sink(block)
    lift._entry_int32_capture = cap
    cap.bind_entry(lift, cap.method, real=True)
    for ins in block.insns[:-1]:
        lift._insn(ins, block.insns, 0, None, block.insns[-1].next_ip)
    packed = dict.get(lift.regs, 'XMM0')
    assert dict.get(lift.regs, 'RCX') is value
    assert value.text == 'p0' and value.kind == 'int' and value.ty == INT
    assert packed.kind == 'float' and packed.ty == FLOAT
    assert [lift._piece_value(packed, lo, 4, FLOAT).text for lo in (0, 4, 8, 12)] == [
        packed.text, '0.0f', '0.0f', '0.0f']
    assert block.stmts == ['var ' + packed.text + ' = (float)(' + MARKER + ');']


@pytest.mark.parametrize('hidden', [False, True])
def test_dry_only_orphan_cannot_escape_beside_a_real_survivor(hidden):
    cap, lift, ins, old, _ = converted(real=False)
    # The dry marker reaches final output through a cached predecessor value,
    # while a different generated spelling obtains a fresh real proof.
    cap._reserved = frozenset({MARKER})
    current = Expr('p0', INT, 'int')
    lift.regs = {'RCX': current}
    cap.bind_entry(lift, cap.method, real=True)
    lift.dry = False
    clone = cap.conversion_input(lift, ins, lift.out.block.insns, current)
    assert clone.text == MARKER + '_' and MARKER not in cap._used
    orphan = ('// ' + MARKER if hidden else 'var dry = (float)(' + MARKER + ');')
    with pytest.raises(EntryCaptureDeclined, match='no real-pass proof'):
        finish(cap, [orphan, 'return (float)(' + clone.text + ');'])


def test_removed_dry_only_marker_does_not_block_a_real_survivor():
    cap, lift, ins, _, _ = converted(real=False)
    cap._reserved = frozenset({MARKER})
    current = Expr('p0', INT, 'int')
    lift.regs = {'RCX': current}
    cap.bind_entry(lift, cap.method, real=True)
    lift.dry = False
    clone = cap.conversion_input(lift, ins, lift.out.block.insns, current)
    lines, count = finish(cap, ['return (float)(' + clone.text + ');'])
    assert count == 1 and lines == [
        'int ' + ALIAS + '_ = p0;', 'return (float)(' + ALIAS + '_);']


@pytest.mark.parametrize('offset,size', [
    (-1, 1), (0, -1), (100, 1), (1, 100), (True, 1), (0, False),
    (0.0, 1), (0, 1.0), (None, 1), (0, None), (10**100, 0),
])
def test_metadata_name_table_invalid_bounds_decline(offset, size):
    dec, _, _ = model()
    dec.L.meta.string_off, dec.L.meta.string_size = offset, size
    with pytest.raises(ArenaDeclined):
        _marker_reservations(dec.L.meta, [])


@pytest.mark.parametrize('backing', [bytearray(b'p0\0'), memoryview(b'p0\0')])
def test_metadata_name_table_mutable_or_view_backing_declines(backing):
    dec, _, _ = model()
    dec.L.meta.d, dec.L.meta.string_size = backing, len(backing)
    with pytest.raises(ArenaDeclined):
        _marker_reservations(dec.L.meta, [])


def test_metadata_name_table_truncated_identifier_declines():
    dec, _, _ = model()
    dec.L.meta.string_size -= 1
    with pytest.raises(ArenaDeclined, match='unterminated'):
        _marker_reservations(dec.L.meta, [])


@pytest.mark.parametrize('orphan', [
    'var dry = (float)(' + MARKER + ');', '// ' + MARKER,
    'var text = "' + MARKER + '";',
])
def test_mixed_parameters_require_real_proof_for_each_surviving_marker(orphan):
    origin, lift, _ = setup(MOVD + CVT + '660f6eca0f5bc9c3', parameters=(1, 1))
    cap = EntryInt32Captures(lift.il, origin.method, origin.insns)
    conversions = [i for i in origin.insns if i.mnemonic == Mnemonic.CVTDQ2PS]
    p0, p1 = Expr('p0', INT, 'int'), Expr('p1', INT, 'int')
    lift.regs = {'RCX': p0, 'RDX': p1}
    cap.bind_entry(lift, origin.method, real=False)
    lift.dry = True
    assert cap.conversion_input(lift, conversions[0], lift.out.block.insns, p0)
    real0, real1 = Expr('p0', INT, 'int'), Expr('p1', INT, 'int')
    lift.regs = {'RCX': real0, 'RDX': real1}
    cap.bind_entry(lift, origin.method, real=True)
    lift.dry = False
    # A phi-held dry Expr is no longer the real entry seed.
    assert cap.conversion_input(lift, conversions[0], lift.out.block.insns, p0) is None
    second = cap.conversion_input(lift, conversions[1], lift.out.block.insns, real1)
    assert second.text == '__il2cpp_capture_i32_1'
    with pytest.raises(EntryCaptureDeclined, match='no real-pass proof'):
        finish(cap, [orphan, 'return (float)(' + second.text + ');'])


def full_model():
    dec, method, owner = model()
    dec.L.asm_comments = False
    dec.L.il._ms_bisect = bisect
    dec.L.il.method_starts = [method.addr, method.addr + 8]
    return dec, method, owner


def test_real_pipeline_dry_real_cleanup_capture_and_method_reuse():
    dec, method, owner = full_model()
    baseline = dec.lift_method(method, owner)
    assert baseline == ['return p0;']
    lift, runtime, native, metadata = dec.L, dec.L.il, dec.L.bin, dec.L.meta
    before = _SYNTH_NEXT_VA[0]
    dec._entry_int32_recovery = True
    for _ in range(2):
        result = dec.lift_method(method, owner)
        assert result == ['int ' + ALIAS + ' = p0;',
                          'float real1 = (float)(' + ALIAS + ');', 'return real1;']
        assert dec._entry_int32_status == 'accepted'
        assert (dec.L, dec.L.il, dec.L.bin, dec.L.meta) == (lift, runtime, native, metadata)
        assert getattr(lift, '_entry_int32_capture', None) is None
        assert _SYNTH_NEXT_VA[0] == before
    dec._entry_int32_recovery = False
    assert dec.lift_method(method, owner) == baseline


@pytest.mark.parametrize('failing_stage', ['binding', 'cleanup'])
def test_real_pipeline_failure_and_next_method_match_recovery_disabled(monkeypatch, failing_stage):
    dec, method, owner = full_model()
    baseline = dec.lift_method(method, owner)
    dec._entry_int32_recovery = True
    def rejected(*args, **kwargs):
        raise EntryCaptureDeclined('injected real pipeline failure')
    with monkeypatch.context() as patch:
        patch.setattr(EntryInt32Captures,
                      'bind_entry' if failing_stage == 'binding' else 'finalize', rejected)
        assert dec.lift_method(method, owner) == baseline
        assert dec._entry_int32_status == 'declined'
    assert dec.lift_method(method, owner)[0] == 'int ' + ALIAS + ' = p0;'
    dec._entry_int32_recovery = False
    assert dec.lift_method(method, owner) == baseline



def test_register_container_payload_is_part_of_the_admitted_model_graph():
    dec, method, owner = model()
    original = dict.get(dec.L.regs, 'RCX')
    graph = _mutable_graph((dec, method, owner))
    assert graph[id(original)] is original
    arena, _, _ = isolated_clone(dec, method, owner)
    copied = dict.get(arena.L.regs, 'RCX')
    assert copied is not original and copied.text == original.text


@pytest.mark.parametrize('location', ['direct', 'nested', 'key'])
def test_register_container_cannot_hide_a_shared_callback(location):
    dec, method, owner = model()
    callback = lambda: dec.L.il
    # The sentinel makes a shallow-shared function survive _RegState's stamp;
    # it must be rejected during graph admission, before deepcopy is invoked.
    callback._defpos = (None, 0)
    if location == 'direct':
        dict.__setitem__(dec.L.regs, 'HIDDEN_CALLBACK', callback)
    elif location == 'nested':
        dict.__setitem__(dec.L.regs, '!flags', {'hidden': [callback]})
    else:
        dict.__setitem__(dec.L.regs, callback, None)
    with pytest.raises(ArenaDeclined, match='unsupported object'):
        isolated_clone(dec, method, owner)
