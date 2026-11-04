"""Native field conversion, complete lanes and conversion-time lifetime."""
import pytest
from iced_x86 import Decoder

from il2cpp import Expr
from il2cpp.cfg import Block, _Sink
from il2cpp.lifter.simdproof import movd_int32_field, _int32
from test_native_values import lanes_lifter, INT, FLOAT, OBJECT

LOAD = '660f6e4910'  # movd xmm1,[rcx+10h]
CONVERT = '0f5bc9'   # cvtdq2ps xmm1,xmm1


def seeded():
    lift = lanes_lifter({'RCX': Expr('this', OBJECT, 'obj')})
    lift.il.instance_field_chain = lambda td: {0x10: ('value', 0)}
    lift.il._sf_field_size = lambda ty, depth: 4 if ty in (INT, FLOAT) else None
    lift._td_of = lambda ty: 0 if ty == OBJECT else None
    return lift


def step(lift, code):
    insns = list(Decoder(64, bytes.fromhex(code), ip=0x1000))
    block = Block(0, insns)
    lift.out = _Sink(block)
    for i, ins in enumerate(insns):
        lift._insn(ins, insns, i, None, insns[-1].next_ip)
    return insns, block


def prove(lift, insns, value=None, current=None):
    value = value if value is not None else Expr('this.value', INT, 'int')
    return movd_int32_field(lift, current or insns[-1], insns, value)


@pytest.mark.parametrize('gap', ['', '90', '31d2', '660f6ec2',
                                 '660f6ec231d20f5bc0'])
@pytest.mark.parametrize('dry', [False, True])
def test_full_field_conversion(gap, dry):
    lift = seeded()
    lift.dry = dry
    step(lift, LOAD + gap + CONVERT)
    value = lift.regs['XMM1']
    assert value.ty == FLOAT and value.kind == 'float'
    assert lift._var_types[value.text] == FLOAT
    assert lift.out.block.stmts == ([] if dry else [
        'var ' + value.text + ' = (float)(this.value);'])
    assert [lift._piece_value(value, i * 4, 4, FLOAT).text for i in range(4)] == [
        value.text, '0.0f', '0.0f', '0.0f']


@pytest.mark.parametrize('gap', [
    'f30f10c8', '660f70c900', '660f6fc8', '0f57c9', 'c5f877',
    'e800000000', 'eb00', 'c7411003000000', '31c9', '66b90300',
    '0f95c1', '8902', '0f94c1', '660f7f02',
])
def test_alias_partial_write_call_branch_memory_and_base_barriers(gap):
    lift = seeded()
    insns = list(Decoder(64, bytes.fromhex(LOAD + gap + CONVERT), ip=0x1000))
    lift.out = _Sink(Block(0, insns))
    assert not prove(lift, insns)


@pytest.mark.parametrize('mode', [
    'float', 'uint', 'missingfield', 'unknownbase', 'struct', 'stackbase',
    'rawbase', 'byrefbase', 'fieldwidth', 'index', 'flat', 'split', 'copy',
    'fakecurrent', 'fieldbyref', 'receivercall', 'receiverfield', 'receiverparts',
    'receiverslice', 'receiverbytes', 'nobindbase', 'segment', 'address32',
    'stack', 'rbp', 'rip', 'gprsource', 'differentdestination',
])
def test_type_and_cfg_boundaries(mode):
    lift = seeded()
    load, convert = LOAD, CONVERT
    if mode == 'float':
        lift.il.types[0] = FLOAT
    if mode == 'uint':
        lift.il.types[0] = (0, 9 << 16)
    if mode == 'fieldbyref':
        lift.il.types[0] = (0, INT[1] | 1 << 29)
    if mode == 'missingfield':
        lift.il.instance_field_chain = lambda td: {}
    if mode == 'unknownbase':
        lift.regs['RCX']._unk = True
    if mode == 'struct':
        lift.meta.typedefs[0].is_valuetype = True
    if mode == 'stackbase':
        lift.regs['RCX']._stack_offset = 0
    if mode == 'rawbase':
        lift.regs['RCX'].kind = 'ptr'
    if mode == 'byrefbase':
        lift.regs['RCX'].ty = (0, OBJECT[1] | 1 << 29)
    if mode in ('receivercall', 'receiverfield'):
        lift.regs['RCX'].text = 'Get()' if mode == 'receivercall' else 'this.next'
    if mode in ('receiverparts', 'receiverslice', 'receiverbytes'):
        key = {'receiverparts': '_parts', 'receiverslice': '_slice',
               'receiverbytes': '_bytes'}[mode]
        setattr(lift.regs['RCX'], key, [])
    if mode == 'nobindbase':
        lift.regs['RCX']._no_bind = True
    if mode == 'fieldwidth':
        load = 'f30f7e4910'
    if mode == 'index':
        load = '660f6e4c0110'
    if mode == 'segment':
        load = '64660f6e4910'
    if mode == 'address32':
        load = '67660f6e4910'
    if mode in ('stack', 'rbp', 'rip', 'gprsource'):
        load = {'stack': '660f6e4c2410', 'rbp': '660f6e4d10',
                'rip': '660f6e0d10000000', 'gprsource': '660f6eca'}[mode]
    if mode == 'differentdestination':
        convert = '0f5bc8'  # xmm0 was never written by MOVD
    insns = list(Decoder(64, bytes.fromhex(load + convert), ip=0x1000))
    lift.out = _Sink(Block(0, insns))
    if mode == 'flat':
        lift.out = []
    if mode == 'split':
        lift.out = _Sink(Block(1, insns[1:]))
    if mode == 'copy':
        lift.out = _Sink(Block(1, insns.copy()))
    current = insns[-1]
    if mode == 'fakecurrent':
        current = list(Decoder(64, bytes.fromhex('0f5bc0'), ip=current.ip))[0]
    assert not prove(lift, insns, current=current)


@pytest.mark.parametrize('mode', ['unknown', 'nobind', 'parts', 'slice', 'bytes',
                                  'stack', 'float', 'uint', 'byref', 'kind'])
def test_source_scalar_proof_cannot_be_inferred_from_text(mode):
    lift = seeded()
    insns = list(Decoder(64, bytes.fromhex(LOAD + CONVERT), ip=0x1000))
    lift.out = _Sink(Block(0, insns))
    value = Expr('this.value', INT, 'int')
    if mode in ('unknown', 'nobind'):
        setattr(value, '_unk' if mode == 'unknown' else '_no_bind', True)
    if mode in ('parts', 'slice', 'bytes'):
        setattr(value, '_' + mode, [])
    if mode == 'stack':
        value._stack_offset = 0
    if mode == 'float':
        value.ty = FLOAT
    if mode == 'uint':
        value.ty = (0, 9 << 16)
    if mode == 'byref':
        value.ty = (0, INT[1] | 1 << 29)
    if mode == 'kind':
        value.kind = 'obj'
    assert not prove(lift, insns, value)


def test_denominator_restores_float_division_without_mutating_movd_source():
    lift = seeded()
    source = Expr('n', INT, 'int')
    lift.regs['RAX'] = source
    step(lift, LOAD + '660f6ec031d20f5bc0' + CONVERT + 'f30f5ec1')
    assert lift.regs['XMM0'].text == 'n / t0'
    assert lift.regs['RAX'] is source
    assert source.ty == INT and source.kind == 'int' and getattr(source, '_parts', None) is None


@pytest.mark.parametrize('ty', [(0, 8 << 16), (33013, 0x80080001),
                                (987, 0x00080006)])
def test_metadata_int32_does_not_require_equal_raw_tuple(ty):
    lift = seeded()
    lift.il.types[0] = ty
    assert _int32(ty)
    step(lift, LOAD + CONVERT)
    assert lift.regs['XMM1'].ty == FLOAT
    assert 'float)(this.value)' in lift.out.block.stmts[0]


def test_later_field_write_cannot_change_any_snapshot_lane():
    lift = seeded()
    step(lift, LOAD + CONVERT + 'c7411003000000')
    value = lift.regs['XMM1']
    assert value.ty == FLOAT
    assert [lift._piece_value(value, i * 4, 4, FLOAT).text for i in range(4)] == [
        't0', '0.0f', '0.0f', '0.0f']
    assert lift.out.block.stmts == [
        'var t0 = (float)(this.value);', 'this.value = 3;']


def test_distinct_xmm_destination_keeps_the_scalar_source_identity():
    lift = seeded()
    insns, block = step(lift, LOAD + '0f5bc1')
    assert lift.regs['XMM1'].ty == INT
    assert lift.regs['XMM0'].ty == FLOAT
    assert block.stmts == ['var t0 = (float)(this.value);']


def test_noncontiguous_native_addresses_decline():
    lift = seeded()
    insns = list(Decoder(64, bytes.fromhex(LOAD + CONVERT), ip=0x1000))
    insns[-1].ip += 1
    lift.out = _Sink(Block(0, insns))
    assert not prove(lift, insns)


@pytest.mark.parametrize('hint', [-1, 0, 999])
def test_structured_execution_index_hint_is_not_a_native_position(hint):
    lift = seeded()
    insns = list(Decoder(64, bytes.fromhex(LOAD + CONVERT), ip=0x1000))
    lift.out = _Sink(Block(0, insns))
    for ins in insns:
        lift._insn(ins, insns, hint, None, insns[-1].next_ip)
    assert lift.out.block.stmts == ['var t0 = (float)(this.value);']
    assert lift.regs['XMM1'].ty == FLOAT


def test_native_scan_is_bounded():
    lift = seeded()
    insns = list(Decoder(64, bytes.fromhex(LOAD + '90' * 512 + CONVERT), ip=0x1000))
    lift.out = _Sink(Block(0, insns))
    assert not prove(lift, insns)
