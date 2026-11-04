"""A GPR transports the field bits; conversion still rounds at CVTDQ2PS."""
import pytest
from iced_x86 import Decoder

from il2cpp import Expr
from il2cpp.cfg import Block, _Sink
from il2cpp.lifter.simdproof import movd_int32_field
from test_simd_field_conversion import seeded, step, INT, FLOAT

LOAD = '8b7110'     # mov esi,[rcx+10h]
MOVE = '660f6ece'   # movd xmm1,esi
CONVERT = '0f5bc9'  # cvtdq2ps xmm1,xmm1


def prove(code, *, text='this.value', value=None, lift=None):
    lift = seeded() if lift is None else lift
    insns = list(Decoder(64, bytes.fromhex(code), ip=0x1000))
    lift.out = _Sink(Block(0, insns))
    value = Expr(text, INT, 'int') if value is None else value
    return movd_int32_field(lift, insns[-1], insns, value)


@pytest.mark.parametrize('before,after', [('', ''), ('90', '90'),
                                         ('31d2', '31c0'),
                                         ('', '31f6'),
                                         ('', '66be0300'),
                                         ('', '400f95c6')])
@pytest.mark.parametrize('dry', [False, True])
def test_conversion_snapshots_the_captured_gpr_not_its_later_value(before, after, dry):
    lift = seeded()
    lift.dry = dry
    step(lift, LOAD + before + MOVE + after + CONVERT)
    value = dict.get(lift.regs, 'XMM1')
    assert value.kind == 'float' and value.ty == FLOAT
    assert lift._var_types[value.text] == FLOAT
    assert [lift._piece_value(value, i * 4, 4, FLOAT).text for i in range(4)] == [
        value.text, '0.0f', '0.0f', '0.0f']
    assert lift.out.block.stmts == ([] if dry else [
        'var ' + value.text + ' = (float)(this.value);'])


@pytest.mark.parametrize('load,move,convert,destination', [
    (LOAD, MOVE, CONVERT, 'XMM1'),
    ('448b4110', '66410f6ec8', CONVERT, 'XMM1'),
    (LOAD, MOVE, '0f5bc1', 'XMM0'),
    ('8b5110', '660f6ef2', '0f5bf6', 'XMM6'),
])
def test_full_dword_gprs_and_distinct_xmm_destinations(load, move, convert, destination):
    lift = seeded()
    step(lift, load + move + convert)
    assert dict.get(lift.regs, destination).ty == FLOAT
    assert lift.out.block.stmts == ['var t0 = (float)(this.value);']


@pytest.mark.parametrize('gap', ['31f6', '66be0300', '400f95c6',
                                 '89c6', '8d7601', '0f45f0', '48be0300000000000000'])
def test_any_gpr_last_writer_other_than_the_exact_field_load_declines(gap):
    assert not prove(LOAD + gap + MOVE + CONVERT)


@pytest.mark.parametrize('gap', ['31c9', '66b90300', '0f95c1',
                                 'c7411003000000', '8902', '660f7f02',
                                 'e800000000', 'eb00'])
@pytest.mark.parametrize('position', ['before_movd', 'after_movd'])
def test_receiver_alias_memory_and_control_barriers(gap, position):
    code = LOAD + (gap if position == 'before_movd' else '') + MOVE
    code += gap if position == 'after_movd' else ''
    assert not prove(code + CONVERT)


@pytest.mark.parametrize('load', [
    '0fb77110', '0fbe7110', '488b7110', '8b740110',
    '648b7110', '678b7110', '8b742410', '8b7510', '8b3510000000',
    'be03000000', '8bf0',
])
def test_load_width_address_and_nonfield_origins_decline(load):
    assert not prove(load + MOVE + CONVERT)


@pytest.mark.parametrize('gap', ['f30f10c8', '660f70c900', '660f6fc8',
                                 '0f57c9', 'c5f877'])
def test_xmm_alias_writes_after_movd_decline(gap):
    assert not prove(LOAD + MOVE + gap + CONVERT)


@pytest.mark.parametrize('text', ['obj1', 't0', '0', 'other.value',
                                  'this.other', '(this.value)', 'Get()'])
def test_typed_but_unproved_text_is_not_an_int_field_cast(text):
    assert not prove(LOAD + MOVE + CONVERT, text=text)


@pytest.mark.parametrize('mode', ['unknown', 'nobind', 'parts', 'slice',
                                  'bytes', 'stack', 'float', 'object', 'byref'])
def test_scalar_type_and_provenance_guards_still_apply(mode):
    value = Expr('this.value', INT, 'int')
    if mode in ('unknown', 'nobind'):
        setattr(value, '_unk' if mode == 'unknown' else '_no_bind', True)
    if mode in ('parts', 'slice', 'bytes'):
        setattr(value, '_' + mode, [])
    if mode == 'stack':
        value._stack_offset = 0
    if mode == 'float':
        value.ty = FLOAT
    if mode == 'object':
        value.kind = 'obj'
    if mode == 'byref':
        value.ty = (0, INT[1] | 1 << 29)
    assert not prove(LOAD + MOVE + CONVERT, value=value)


@pytest.mark.parametrize('hint', [-1, 0, 999])
def test_native_block_position_does_not_use_the_structured_index_hint(hint):
    lift = seeded()
    insns = list(Decoder(64, bytes.fromhex(LOAD + MOVE + CONVERT), ip=0x1000))
    lift.out = _Sink(Block(0, insns))
    for ins in insns:
        lift._insn(ins, insns, hint, None, insns[-1].next_ip)
    assert lift.out.block.stmts == ['var t0 = (float)(this.value);']


def test_single_rounding_precedes_sqrt_and_later_field_mutation():
    lift = seeded()
    step(lift, LOAD + MOVE + CONVERT + 'c7411003000000f30f51c1')
    assert lift.out.block.stmts == [
        'var t0 = (float)(this.value);', 'var t1 = this.value;',
        'this.value = 3;']
    assert dict.get(lift.regs, 'RSI').text == 't1'
    assert lift.regs['XMM0'].text == '(float)global::System.Math.Sqrt(t0)'


def test_gpr_expression_identity_is_not_retyped_or_wrapped():
    lift = seeded()
    insns = list(Decoder(64, bytes.fromhex(LOAD + MOVE + CONVERT), ip=0x1000))
    lift.out = _Sink(Block(0, insns))
    for ins in insns[:2]:
        lift._insn(ins, insns, 0, None, insns[-1].next_ip)
    gpr = dict.get(lift.regs, 'RSI')
    assert dict.get(lift.regs, 'XMM1') is gpr
    lift._insn(insns[-1], insns, 0, None, insns[-1].next_ip)
    assert dict.get(lift.regs, 'RSI') is gpr
    assert gpr.ty == INT and gpr.kind == 'int' and gpr.text == 'this.value'
    assert getattr(gpr, '_parts', None) is None


def test_double_conversion_is_not_enabled_by_the_new_origin_proof():
    assert not prove(LOAD + MOVE + 'f30fe6c9')


def test_load_to_conversion_scan_budget_includes_both_native_transfers():
    assert not prove(LOAD + '90' * 511 + MOVE + CONVERT)


@pytest.mark.parametrize('padding,accepted', [(510, True), (511, False)])
def test_exact_total_backward_scan_bound(padding, accepted):
    assert prove(LOAD + '90' * padding + MOVE + CONVERT) is accepted


@pytest.mark.parametrize('mode', ['flat', 'split', 'copy', 'gap'])
def test_gpr_proof_requires_owned_contiguous_same_block(mode):
    lift = seeded()
    insns = list(Decoder(64, bytes.fromhex(LOAD + MOVE + CONVERT), ip=0x1000))
    lift.out = _Sink(Block(0, insns))
    if mode == 'flat':
        lift.out = []
    elif mode == 'split':
        lift.out = _Sink(Block(1, insns[1:]))
    elif mode == 'copy':
        lift.out = _Sink(Block(0, insns.copy()))
    else:
        insns[0].ip -= 1
    assert not movd_int32_field(lift, insns[-1], insns, Expr('this.value', INT, 'int'))


def test_receiver_overwritten_by_its_own_load_is_not_a_stable_object():
    lift = seeded()
    step(lift, '8b4910660f6ec90f5bc9')
    assert not any('= (float)(' in stmt for stmt in lift.out.block.stmts)
