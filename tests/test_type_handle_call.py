"""A rendered typeof is not by itself evidence of RuntimeTypeHandle."""
import struct
from types import SimpleNamespace as NS

import pytest
from iced_x86 import Decoder, Register

from il2cpp import Lifter
from il2cpp.expr import Expr
from il2cpp.lifter.typehandles import recover_type_handle_call

START, SLOT, TARGET = 0x1000, 0x2000, 0x3000
INT = (0, 0x08 << 16)
TYPE = (0, 0x12 << 16)
HANDLE = (1, 0x11 << 16)


def setup(*, suffix=b'\x33\xd2', prefix=b'\x48\x8b\x0d', ty=INT, text='typeof(int)'):
    raw = prefix + struct.pack('<i', SLOT - START - len(prefix) - 4) + suffix
    at = START + len(raw)
    call = Decoder(64, b'\xe8' + struct.pack('<i', TARGET - at - 5), ip=at).decode()
    type_td = NS(name='Type', namespace='System', declaring=-1,
                 generic_container=-1, is_valuetype=False, is_enum=False)
    handle_td = NS(name='RuntimeTypeHandle', namespace='System', declaring=-1,
                   generic_container=-1, is_valuetype=True, is_enum=False)
    sample_td = NS(name='Sample', namespace='Example', declaring=-1,
                   generic_container=-1, is_valuetype=False, is_enum=False)
    method = NS(name='GetTypeFromHandle', addr=TARGET, declaring=0, image=0,
                is_static=True, generic_container=-1, return_type=0, param_count=1)
    params = [NS(type=1)]
    meta = NS(methods=[method], typedefs=[type_td, handle_td, sample_td],
              images=[NS(name='mscorlib.dll', type_start=0, type_count=3)],
              method_params=lambda m: params)
    usage = {'kind': 2, 'type': ty, 'text': text}
    binary = NS(read=lambda p, n: raw[p - START:p - START + n],
                qword=lambda p: None, va2off=lambda p: None)
    il = NS(meta=meta, types=[TYPE, HANDLE], addr_candidates={TARGET: [('method', 0)]},
            decode_slot=lambda p: usage if p == SLOT else None, bin=binary,
            _type_enum=lambda t: (t[1] >> 16) & 0xff,
            _closed_type_key=lambda t: (t[0], t[1] >> 16), type_name=lambda t: text[7:-1])
    il._proof_block = NS(insns=list(Decoder(64, raw, ip=START)) + [call])
    value = Expr(text, ty, 'klass');value._type_handle = (START, SLOT, ty, text)
    return il, call, value, usage, params


def recover(state):
    il, call, value, _, _ = state
    return recover_type_handle_call(il, call, 0, value, block=il._proof_block)


@pytest.mark.parametrize('suffix', [b'', b'\x33\xd2', b'\x31\xd2', b'\x40\x33\xd2'])
@pytest.mark.parametrize('corelib', ['mscorlib.dll', 'System.Private.CoreLib.dll'])
def test_adjacent_exact_type_usage_load_recovers(suffix, corelib):
    state = setup(suffix=suffix);state[0].meta.images[0].name = corelib
    assert recover(state) == 'typeof(int)'


@pytest.mark.parametrize('ty,text', [((0, n << 16), 'typeof(int)') for n in range(1, 15)] + [
    ((0, 0x1c << 16), 'typeof(object)'), ((2, 0x12 << 16), 'typeof(Example.Sample)'),
    ((2, 0x11 << 16), 'typeof(Example.Sample)')])
def test_closed_simple_types_are_not_reclassified(ty, text):
    state = setup(ty=ty, text=text);value = state[2]
    assert recover(state) == text
    assert (value.text, value.ty, value.kind) == (text, ty, 'klass')


@pytest.mark.parametrize('what', ['no-proof', 'unknown', 'text', 'kind', 'type',
                                  'slot', 'origin', 'proof-text', 'proof-type'])
def test_missing_stale_or_changed_symbolic_evidence_declines(what):
    state = setup();value = state[2]
    if what == 'no-proof':value._type_handle = None
    elif what == 'unknown':value._unk = True
    elif what == 'text':value.text = 'obj1'
    elif what == 'kind':value.kind = 'ptr'
    elif what == 'type':value.ty = TYPE
    else:
        origin, slot, ty, text = value._type_handle
        value._type_handle = (origin + (1 if what == 'origin' else 0),
                              slot + (8 if what == 'slot' else 0),
                              TYPE if what == 'proof-type' else ty,
                              'typeof(long)' if what == 'proof-text' else text)
    assert recover(state) is None


@pytest.mark.parametrize('kind', [1, 3, 4, 5, 6])
def test_class_pointer_or_other_usage_is_not_a_type_handle(kind):
    state = setup();state[3]['kind'] = kind
    assert recover(state) is None


@pytest.mark.parametrize('suffix', [b'\x89\xc9', b'\x48\x83\xc1\x20', b'\x90',
    b'\xeb\x00', b'\x33\xc9', b'\x33\xd0', b'\x48\x33\xd2', b'\x33\xc0',
    b'\x0f\x57\xc0', b'\xcc', b'\x48\x8b\xcb', b'\x48\x89\xcb'])
def test_intervening_unproved_or_truncating_instructions_decline(suffix):
    assert recover(setup(suffix=suffix)) is None


@pytest.mark.parametrize('prefix', [b'\x48\x8b\x1d', b'\x48\x8d\x0d', b'\x8b\x0d',
    b'\x66\x8b\x0d', b'\x64\x48\x8b\x0d', b'\xf2\x0f\x10\x0d'])
def test_native_load_must_be_pointer_mov_into_rcx(prefix):
    assert recover(setup(prefix=prefix)) is None


@pytest.mark.parametrize('what', ['name', 'namespace', 'owner', 'image', 'static',
    'method-generic', 'owner-generic', 'nested-owner', 'value-owner', 'return',
    'return-byref', 'parameter', 'parameter-byref', 'parameter-count', 'parameter-list',
    'handle-name', 'handle-namespace', 'handle-generic', 'handle-nested', 'handle-class',
    'handle-enum', 'image-range', 'return-index', 'parameter-index', 'method-address',
    'negative-owner', 'candidate-generic', 'candidate-shared', 'candidate-absent'])
def test_exact_core_library_metadata_identity_is_required(what):
    state = setup();il, _, _, _, params = state
    m = il.meta.methods[0];owner, handle = il.meta.typedefs[:2]
    if what == 'name':m.name = 'GetTypeFromHandle2'
    elif what == 'namespace':owner.namespace = 'Application'
    elif what == 'owner':owner.name = 'TypeProxy'
    elif what == 'image':il.meta.images[0].name = 'Application.dll'
    elif what == 'static':m.is_static = False
    elif what == 'method-generic':m.generic_container = 0
    elif what == 'owner-generic':owner.generic_container = 0
    elif what == 'nested-owner':owner.declaring = 2
    elif what == 'value-owner':owner.is_valuetype = True
    elif what == 'return':il.types[0] = INT
    elif what == 'return-byref':il.types[0] = (0, TYPE[1] | 1 << 29)
    elif what == 'parameter':il.types[1] = TYPE
    elif what == 'parameter-byref':il.types[1] = (1, HANDLE[1] | 1 << 29)
    elif what == 'parameter-count':m.param_count = 2
    elif what == 'parameter-list':params.clear()
    elif what == 'handle-name':handle.name = 'RuntimeMethodHandle'
    elif what == 'handle-namespace':handle.namespace = 'Application'
    elif what == 'handle-generic':handle.generic_container = 0
    elif what == 'handle-nested':handle.declaring = 2
    elif what == 'handle-class':handle.is_valuetype = False
    elif what == 'handle-enum':handle.is_enum = True
    elif what == 'image-range':il.meta.images[0].type_start = 1
    elif what == 'return-index':m.return_type = -1
    elif what == 'parameter-index':params[0].type = -1
    elif what == 'method-address':m.addr += 1
    elif what == 'negative-owner':m.declaring = -1
    elif what == 'candidate-generic':il.addr_candidates[TARGET] = [('generic', 0)]
    elif what == 'candidate-shared':il.addr_candidates[TARGET].append(('method', 1))
    elif what == 'candidate-absent':il.addr_candidates.clear()
    assert recover(state) is None


@pytest.mark.parametrize('te', [0, 0x0f, 0x10, 0x13, 0x14, 0x15, 0x1d, 0x1e])
def test_open_pointer_and_aggregate_type_shapes_decline(te):
    assert recover(setup(ty=(0, te << 16))) is None


def test_open_type_definition_declines_even_if_a_fake_closed_key_exists():
    state = setup(ty=(2, 0x12 << 16), text='typeof(Example.Sample)')
    state[0].meta.typedefs[2].generic_container = 0
    assert recover(state) is None


def test_byref_and_unclosed_payload_decline():
    assert recover(setup(ty=(0, INT[1] | 1 << 29))) is None
    state = setup();state[0]._closed_type_key = lambda t: None
    assert recover(state) is None


@pytest.mark.parametrize('kind', [1, 2])
@pytest.mark.parametrize('prefix', [b'\x48\x8b\x0d', b'\x48\x8b\x1d', b'\x8b\x0d',
                                   b'\x66\x8b\x0d', b'\x64\x48\x8b\x0d',
                                   b'\xf3\x0f\x6f\x0d'])
def test_only_exact_full_width_kind_two_load_records_a_proof(kind, prefix):
    state = setup(prefix=prefix);il, _, _, usage, _ = state;usage['kind'] = kind
    lift = Lifter.__new__(Lifter);lift.il = il;lift.bin = il.bin
    ins = Decoder(64, il.bin.read(START, 7 + len(prefix)), ip=START).decode()
    out = lift._read_mem_raw(ins, None)
    expected = kind == 2 and prefix in (b'\x48\x8b\x0d', b'\x48\x8b\x1d')
    assert (out._type_handle is not None) == expected
    if expected:assert out._type_handle == (START, SLOT, INT, 'typeof(int)')


def test_generic_copy_and_phi_shaped_values_do_not_inherit_load_proof():
    state = setup();value = state[2]
    assert Lifter._copy_expr(value)._type_handle is None
    merged = Expr(value.text, value.ty, value.kind)
    assert merged._type_handle is None
    assert recover_type_handle_call(state[0], state[1], 0, merged) is None


@pytest.mark.parametrize('shape', ['missing', 'call-only', 'zero-call', 'other-call'])
def test_adjacent_bytes_without_same_executed_cfg_block_decline(shape):
    state = setup();il, call, value, _, _ = state
    block = il._proof_block
    if shape == 'missing':block = None
    elif shape == 'call-only':block = NS(insns=[call])
    elif shape == 'zero-call':block = NS(insns=block.insns[1:])
    else:block = NS(insns=block.insns[:-1])
    assert recover_type_handle_call(il, call, 0, value, block=block) is None


@pytest.mark.parametrize('index', [-1, 3, 1000000])
def test_out_of_range_represented_type_definition_declines(index):
    state = setup(ty=(index, 0x12 << 16), text='typeof(Example.Sample)')
    assert recover(state) is None
