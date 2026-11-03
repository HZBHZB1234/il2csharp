"""Exact native reference-home origins; never capture or globally type a home."""
from types import SimpleNamespace as NS
import struct

import pytest
from iced_x86 import Decoder
from il2cpp.binary import PE
from il2cpp.expr import Expr
from il2cpp.lifter.stackrefs import recover_stack_references

VOID = (0, 1 << 16)
INT = (0, 8 << 16)
REF = (1, 0x12 << 16)
START = 0x180001000
TARGET = 0x180010000
PRODUCER = 0x180020000
HELPER = 0x180030000


def call_at(ip, target):
    return b'\xe8' + struct.pack('<i', target - ip - 5)


def setup(*, position=4, instance=False, before=b'', after=b'', store=None,
          prefix=b''):
    offset = 0x20 + 8 * (position - 4)
    if store is None:
        store = b'\x48\x89\x44\x24' + bytes([offset])
    raw = prefix + call_at(START + len(prefix), PRODUCER) + before + store + after
    raw += call_at(START + len(raw), TARGET)
    insns = list(Decoder(64, raw, ip=START))
    owner = NS(generic_container=-1, declaring=-1, is_valuetype=False)
    ref = NS(generic_container=-1, declaring=-1, is_valuetype=False)
    method = NS(index=0, addr=TARGET, generic_container=-1, declaring=0,
                return_type=0, is_static=not instance,
                param_count=position + 1 - int(instance))
    producer = NS(index=1, addr=PRODUCER, generic_container=-1, declaring=0,
                  return_type=2, is_static=True, param_count=0)
    helper = NS(index=2, addr=HELPER, generic_container=-1, declaring=0,
                return_type=0, is_static=True, param_count=0)
    params = [NS(type=1) for _ in range(method.param_count - 1)] + [NS(type=2)]
    producer.declaring = 2
    helper.declaring = 3
    producer_owner = NS(**vars(owner))
    helper_owner = NS(**vars(owner))
    meta = NS(typedefs=[owner, ref, producer_owner, helper_owner],
              methods=[method, producer, helper],
              method_params=lambda m: params if m is method else [])
    binary = PE.__new__(PE)
    image = bytearray(0x80)
    struct.pack_into('<I', image, 0x3c, 0x40)
    image[0x40:0x46] = b'PE\x00\x00\x64\x86'
    binary.d = bytes(image)
    binary.is64 = True
    il = NS(meta=meta, bin=binary, types=[VOID, INT, REF],
            addr_candidates={TARGET: [('method', 0)], PRODUCER: [('method', 1)],
                             HELPER: [('method', 2)]},
            _type_enum=lambda t: (t[1] >> 16) & 255,
            _closed_type_key=lambda t: t, type_name=lambda t: 'Example.Value')
    name = 's_%x' % offset
    expr = Expr('Example.Make()', REF, 'obj')
    lift = NS(il=il, meta=meta, out=NS(block=NS(insns=insns, stmts=[])),
              _cur_ip=insns[-1].ip, rsp_delta=-128,
              stack_map={-128 + offset: name}, stack_values={name: expr},
              slot_types={}, _type_hints={}, _var_types={})
    return lift, method, VOID, ['arg%d' % i for i in range(position)] + [name]


def recover(state):
    return recover_stack_references(*state)


@pytest.mark.parametrize('position', range(4, 10))
@pytest.mark.parametrize('instance', [False, True])
def test_exact_reference_argument_positions_without_mutation(position, instance):
    state = setup(position=position, instance=instance)
    lift, _, _, args = state
    before = list(args)
    expr = next(iter(lift.stack_values.values()))
    snapshot = (expr.text, expr.ty, expr.kind, expr._uses, expr._sites, expr._defpos)
    out = recover(state)
    assert out == before[:-1] + ['((Example.Value)%s)' % before[-1]]
    assert args == before and out is not args
    assert snapshot == (expr.text, expr.ty, expr.kind, expr._uses, expr._sites, expr._defpos)
    assert not lift.out.block.stmts
    assert lift.slot_types == lift._type_hints == lift._var_types == {}


@pytest.mark.parametrize('before,store', [
    (b'\x48\x89\xc3', b'\x48\x89\x5c\x24\x20'),
    (b'\x48\x89\xc6', b'\x48\x89\x74\x24\x20'),
    (b'\x48\x89\xc7', b'\x48\x89\x7c\x24\x20'),
    (b'\x49\x89\xc4', b'\x4c\x89\x64\x24\x20'),
    (b'\x49\x89\xc7', b'\x4c\x89\x7c\x24\x20'),
    (b'\x48\x89\xc3\x49\x89\xdc', b'\x4c\x89\x64\x24\x20'),
    (b'\x48\x89\xc1', b'\x48\x89\x4c\x24\x20'),
])
def test_full_width_register_copy_chains(before, store):
    assert recover(setup(before=before, store=store))[-1] == '((Example.Value)s_20)'


@pytest.mark.parametrize('after', [
    b'\x48\x89\xf1', b'\x4c\x8d\x4c\x24\x40',
    b'\xc7\x44\x24\x28\x02\x00\x00\x00', b'\x48\x8b\x05\x00\x00\x00\x00',
    b'\x33\xd2', b'\x45\x33\xc9', b'\x48\x89\x44\x24\x20',
])
def test_harmless_setup_and_latest_exact_rewrite(after):
    assert recover(setup(after=after))[-1] == '((Example.Value)s_20)'


def preserved_call_setup(register='rbx'):
    move = b'\x48\x89\xc3' if register == 'rbx' else b'\x48\x89\xc1'
    crossing = call_at(START + 5 + len(move), HELPER)
    store = b'\x48\x89\x5c\x24\x20' if register == 'rbx' else b'\x48\x89\x4c\x24\x20'
    return setup(before=move + crossing, store=store)


def test_only_win64_preserved_register_may_cross_a_canonical_call():
    assert recover(preserved_call_setup())[-1] == '((Example.Value)s_20)'
    state = preserved_call_setup('rcx')
    assert recover(state) is state[3]


@pytest.mark.parametrize('after', [
    b'\x90', b'\x48\x83\xc4\x00', b'\x89\xc4', b'\x66\x89\xc4', b'\x40\x88\xc4',
    b'\xe8\x00\x00\x00\x00', b'\xeb\x00', b'\x89\x00',
    b'\xc6\x44\x24\x20\x00', b'\x66\xc7\x44\x24\x1f\x00\x00',
    b'\xc7\x44\x24\x24\x00\x00\x00\x00', b'\x64\x48\x8b\x00',
    b'\x50', b'\x0f\x0b', b'\xf3\x0f\x7f\x44\x24\x20',
])
def test_alias_partial_unknown_branch_or_call_after_store_declines(after):
    state = setup(after=after)
    assert recover(state) is state[3]


@pytest.mark.parametrize('before', [
    b'\x89\xc0', b'\x66\x89\xc0', b'\x88\xc0', b'\x48\x8b\x03',
    b'\x48\x8d\x43\x01', b'\x33\xc0', b'\x48\x83\xc0\x00',
    b'\x48\xc7\xc0\x00\x00\x00\x00', b'\x48\x89\xe0',
    b'\x48\x89\xc3\x33\xdb\x48\x89\xd8',
])
def test_source_truncation_redefinition_or_noncopy_declines(before):
    state = setup(before=before)
    assert recover(state) is state[3]


@pytest.mark.parametrize('store', [
    b'\x88\x44\x24\x20', b'\x89\x44\x24\x20', b'\x66\x89\x44\x24\x20',
    b'\x48\x89\x44\x24\x21', b'\x48\x89\x44\x25\x20',
    b'\x64\x48\x89\x44\x24\x20', b'\x67\x48\x89\x44\x24\x20',
    b'\x48\xc7\x44\x24\x20\x01\x00\x00\x00',
])
def test_only_exact_full_width_rsp_register_store_proves_a_reference(store):
    state = setup(store=store)
    assert recover(state) is state[3]


@pytest.mark.parametrize('which', ['producer', 'consumer', 'crossed'])
@pytest.mark.parametrize('change', [
    'absent', 'shared', 'generic-candidate', 'negative-index', 'method-index',
    'address', 'generic-method', 'generic-owner', 'nested-owner', 'value-owner',
    'bad-return-index', 'bad-owner',
])
def test_every_native_call_requires_unique_canonical_plain_metadata(which, change):
    state = preserved_call_setup() if which == 'crossed' else setup()
    lift = state[0]
    il = lift.il
    index = {'consumer': 0, 'producer': 1, 'crossed': 2}[which]
    method = il.meta.methods[index]
    if change == 'absent':il.addr_candidates.pop(method.addr)
    elif change == 'shared':il.addr_candidates[method.addr].append(('method', index))
    elif change == 'generic-candidate':il.addr_candidates[method.addr] = [('generic', index)]
    elif change == 'negative-index':il.addr_candidates[method.addr] = [('method', -1)]
    elif change == 'method-index':method.index = -1
    elif change == 'address':method.addr += 1
    elif change == 'generic-method':method.generic_container = 0
    elif change == 'generic-owner':il.meta.typedefs[method.declaring].generic_container = 0
    elif change == 'nested-owner':il.meta.typedefs[method.declaring].declaring = 1
    elif change == 'value-owner':il.meta.typedefs[method.declaring].is_valuetype = True
    elif change == 'bad-return-index':method.return_type = -1
    elif change == 'bad-owner':method.declaring = -1
    assert recover(state) is state[3]


@pytest.mark.parametrize('change', [
    'unknown', 'missing-value', 'wrong-type', 'wrong-kind', 'missing-home',
    'wrong-argument', 'complex-argument', 'rsp-delta', 'no-block', 'alternate-entry',
    'no-call', 'incomplete-params', 'byref-param', 'generic-param', 'array-param',
    'struct-param', 'bad-param-index', 'bad-class-index', 'unclosed-param',
    'generic-class', 'nested-class', 'value-class', 'byref-return', 'sret-return',
    'different-return', 'noncanonical-home', 'producer-return', 'gap', 'tail',
])
def test_symbolic_type_abi_and_cfg_agreement_is_required(change):
    state = setup(before=b'\x48\x89\xd1')
    lift, method, _, args = state
    il = lift.il
    expr = lift.stack_values['s_20']
    if change == 'unknown':expr._unk = True
    elif change == 'missing-value':lift.stack_values.clear()
    elif change == 'wrong-type':expr.ty = INT
    elif change == 'wrong-kind':expr.kind = 'ptr'
    elif change == 'missing-home':lift.stack_map.clear()
    elif change == 'wrong-argument':args[-1] = 'other'
    elif change == 'complex-argument':args[-1] = 'f()'
    elif change == 'rsp-delta':lift.rsp_delta += 8
    elif change == 'no-block':lift.out.block = None
    elif change == 'alternate-entry':lift.out.block.insns = lift.out.block.insns[1:]
    elif change == 'no-call':lift._cur_ip += 1
    elif change == 'incomplete-params':il.meta.method_params = lambda m: []
    elif change == 'byref-param':il.types[2] = (1, REF[1] | 1 << 29)
    elif change == 'generic-param':il.types[2] = (1, 0x15 << 16)
    elif change == 'array-param':il.types[2] = (1, 0x1d << 16)
    elif change == 'struct-param':il.types[2] = (1, 0x11 << 16)
    elif change == 'bad-param-index':il.meta.method_params(method)[-1].type = -1
    elif change == 'bad-class-index':il.types[2] = (-1, REF[1])
    elif change == 'unclosed-param':il._closed_type_key = lambda ty: None
    elif change == 'generic-class':il.meta.typedefs[1].generic_container = 0
    elif change == 'nested-class':il.meta.typedefs[1].declaring = 0
    elif change == 'value-class':il.meta.typedefs[1].is_valuetype = True
    elif change == 'byref-return':il.types[0] = (0, VOID[1] | 1 << 29);state = lift, method, il.types[0], args
    elif change == 'sret-return':il.types[0] = (0, 0x11 << 16);state = lift, method, il.types[0], args
    elif change == 'different-return':state = lift, method, INT, args
    elif change == 'noncanonical-home':lift.stack_map[-96] = 'someName';lift.stack_values['someName'] = expr;args[-1] = 'someName'
    elif change == 'producer-return':il.meta.methods[1].return_type = 1
    elif change == 'gap':lift.out.block.insns.pop(1)
    elif change == 'tail':
        call = lift.out.block.insns[-1]
        lift.out.block.insns[-1] = Decoder(64, b'\xe9' + struct.pack('<i', TARGET - call.ip - 5), ip=call.ip).decode()
    assert recover(state) is state[3]


@pytest.mark.parametrize('shape', ['elf64', 'unknown', 'pe32', 'arm64', 'x86', 'truncated'])
def test_no_reference_recovery_without_explicit_windows_x64(shape):
    from il2cpp.binary import ELF
    state = setup()
    binary = state[0].il.bin
    if shape in ('elf64', 'unknown'):
        other = ELF.__new__(ELF) if shape == 'elf64' else NS()
        other.is64 = True
        other.d = binary.d
        state[0].il.bin = other
    elif shape == 'pe32':binary.is64 = False
    elif shape == 'truncated':binary.d = b''
    else:
        data = bytearray(binary.d)
        struct.pack_into('<H', data, 0x44, 0xaa64 if shape == 'arm64' else 0x14c)
        binary.d = bytes(data)
    assert recover(state) is state[3]


@pytest.mark.parametrize('position', range(4, 10))
@pytest.mark.parametrize('instance', [False, True])
def test_positional_argument_integration_keeps_float_and_receiver_positions(position, instance):
    from il2cpp import Lifter
    state = setup(position=position, instance=instance)
    original, method, rty, _ = state
    lift = Lifter.__new__(Lifter)
    lift.__dict__.update(original.__dict__)
    lift.il.returns_sret = lambda ty: False
    lift._class_type_subst = lambda ty: ty
    float_ty = (0, 0x0c << 16)
    lift.il.types.append(float_ty)
    lift.meta.method_params(method)[0].type = 3
    float_pos = int(instance)
    lift._xmm_pending = [(float_pos, Expr('0.5f', float_ty, 'float'))]
    for pos in range(4, position):
        offset = 0x20 + 8 * (pos - 4)
        name = 's_%x' % offset
        lift.stack_map[lift.rsp_delta + offset] = name
        lift.stack_values[name] = Expr('value%d' % pos, INT, 'int')
    args = ['rcx', 'rdx', 'r8', 'r9', 'stale-xmm-tail']
    out = lift._positional_args(args, method, rty)
    assert len(out) == position + 1
    assert out[float_pos] == '0.5f'
    assert out[-1] == '((Example.Value)s_%x)' % (0x20 + 8 * (position - 4))
    if instance:
        assert out[0] == 'rcx'
    assert args == ['rcx', 'rdx', 'r8', 'r9', 'stale-xmm-tail']


@pytest.mark.parametrize('count,proven', [(0, True), (1, True), (126, True),
                                         (127, False), (128, False), (256, False)])
def test_native_origin_walk_is_bounded(count, proven):
    state = setup(before=b'\x48\x89\xd1' * count)
    out = recover(state)
    assert (out is not state[3]) == proven


@pytest.mark.parametrize('which', ['producer', 'consumer', 'crossed'])
def test_indirect_calls_are_not_ordinary_metadata_proofs(which):
    state = preserved_call_setup() if which == 'crossed' else setup()
    insns = state[0].out.block.insns
    index = {'producer': 0, 'consumer': len(insns) - 1, 'crossed': 2}[which]
    old = insns[index]
    # Five bytes keep the next address contiguous while changing the call kind.
    insns[index] = Decoder(64, b'\x66\x66\x66\xff\xd0', ip=old.ip).decode()
    assert recover(state) is state[3]


def test_a_prior_partial_home_does_not_override_the_latest_full_width_store():
    state = setup(before=b'\xc6\x44\x24\x20\x00')
    assert recover(state)[-1] == '((Example.Value)s_20)'


def test_identical_call_texts_are_never_bound_or_rewritten():
    prefix = call_at(START, PRODUCER)
    state = setup(prefix=prefix)
    expr = state[0].stack_values['s_20']
    expr.text = 'Example.Make()'
    state[0].out.block.stmts[:] = ['object old = Example.Make();']
    out = recover(state)
    assert out[-1] == '((Example.Value)s_20)'
    assert expr.text == 'Example.Make()' and expr._uses is None
    assert state[0].out.block.stmts == ['object old = Example.Make();']



def test_a_noncanonical_consumer_object_keeps_the_original_arguments():
    lift, method, rty, args = setup()
    clone = NS(**vars(method))
    assert recover_stack_references(lift, clone, rty, args) is args
