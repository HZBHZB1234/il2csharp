"""Narrow unsigned Jcc uses machine-width operands, not promoted C# ints."""
import pytest
from types import SimpleNamespace as NS
from il2cpp import Expr
from test_native_values import lifter, execute

CHAR = (0, 3 << 16)
BYTE = (0, 5 << 16)

@pytest.mark.parametrize('prefix,ty,cast', [('66', CHAR, 'ushort'), ('', BYTE, 'byte')])
@pytest.mark.parametrize('jcc,op', [('77','>'), ('73','>='), ('72','<'), ('76','<=')])
def test_unsigned_narrow_range_preserves_wrap(prefix, ty, cast, jcc, op):
    # SUB AX/AL,48; CMP AX/AL,9; unsigned Jcc.
    code = '6683e8306683f809' if prefix else '2c303c09'
    lift = lifter({'RAX': Expr('ch', ty, 'int')})
    out = execute(lift, code + jcc + '00')
    assert len(out)==1 and out[0].startswith(f'if (unchecked(({cast})(ch - 48)) {op} 9) goto L_')

@pytest.mark.parametrize('te', range(3, 12))
def test_closed_integer_metadata_preserves_low_word_bits(te):
    lift = lifter({'RAX': Expr('value', (0,te<<16), 'int')})
    assert 'unchecked((ushort)(value))' in execute(lift,'6683f8097600')[0]

@pytest.mark.parametrize('code', ['6683f8ff7600', '663bc17600'])
def test_both_operands_are_normalized(code):
    lift = lifter({'RAX': Expr('value',CHAR,'int'), 'RCX': Expr('other',CHAR,'int')})
    out = execute(lift,code)[0]
    rhs = '-1' if 'ff' in code else 'other'
    assert f'<= unchecked((ushort)({rhs}))' in out

@pytest.mark.parametrize('code', ['6683f8097e00', '6683f8097400', '83f8097600', '4883f8097600', '80fc097600', '668339097600'])
def test_other_comparisons_keep_the_existing_spelling(code):
    lift = lifter({'RAX': Expr('value',CHAR,'int'), 'RCX': Expr('other',CHAR,'int')})
    assert 'unchecked' not in '\n'.join(execute(lift,code))

@pytest.mark.parametrize('ty,kind,text,unk', [
    (None,'int','value',False), ((0,2<<16),'int','value',False),
    ((0,0xc<<16),'float','value',False), ((0,0x11<<16),'int','value',False),
    ((0,0xf<<16),'ptr','value',False), ((0,3<<16|1<<29),'int','value',False),
    (CHAR,'int','value',True), (CHAR,'int','?',False),
])
def test_unproved_operand_declines(ty,kind,text,unk):
    value=Expr(text,ty,kind); value._unk=unk
    lift=lifter({'RAX':value})
    assert 'unchecked' not in execute(lift,'6683f8097600')[0]

@pytest.mark.parametrize('middle', ['90', '4889c9', '488d4901'])
def test_flag_preserving_instruction_keeps_width(middle):
    lift=lifter({'RAX':Expr('value',CHAR,'int'), 'RCX':Expr('other',(0,8<<16),'int')})
    assert 'unchecked((ushort)(value))' in execute(lift,'6683f809'+middle+'7600')[0]

@pytest.mark.parametrize('middle', ['f8', 'f9', 'f5', '9e', 'f7e1', '83c101'])
def test_changed_or_undefined_unsigned_flags_drop_width(middle):
    lift=lifter({'RAX':Expr('value',CHAR,'int'), 'RCX':Expr('other',(0,8<<16),'int')})
    assert 'unchecked' not in '\n'.join(execute(lift,'6683f809'+middle+'7600'))


def test_flag_pair_assignment_cannot_keep_an_old_width():
    lift=lifter({'RAX':Expr('value',CHAR,'int')})
    execute(lift,'6683f809')
    lift.flags=lift.flags
    assert 'unchecked' not in execute(lift,'7600')[0]


def test_lifter_reuse_does_not_leak_width():
    lift=lifter({'RAX':Expr('value',CHAR,'int')})
    assert 'unchecked' in execute(lift,'6683f8097600')[0]
    lift.out=[]
    assert 'unchecked' not in execute(lift,'83f8097600')[0]


@pytest.mark.parametrize('call', ['e800000000', 'ffd1'])
def test_even_a_call_handler_that_preserves_the_pair_drops_width(call):
    lift=lifter({'RAX':Expr('value',CHAR,'int')})
    lift._call=lambda *args: None
    assert 'unchecked' not in execute(lift,'6683f809'+call+'7600')[0]


@pytest.mark.parametrize('omitted', ['90', 'f9', '83c101'])
def test_omitted_native_instruction_cannot_prove_live_cmp(omitted):
    from iced_x86 import Decoder
    lift=lifter({'RAX':Expr('value',CHAR,'int')})
    insns=list(Decoder(64,bytes.fromhex('6683f809'+omitted+'7600'),ip=0x1000))
    for index in (0,2):
        lift._insn(insns[index],insns,index,None,insns[-1].next_ip)
    assert 'unchecked' not in lift.out[0][1]


@pytest.mark.parametrize('code', ['83f809','4883f809','80fc09','663901','663b01','66833909'])
def test_width_proof_declines_wide_high_byte_and_memory_operands(code):
    from iced_x86 import Decoder
    from il2cpp.x64 import narrow_cmp_width
    assert narrow_cmp_width(next(iter(Decoder(64,bytes.fromhex(code))))) is None


@pytest.mark.parametrize('prefix', ['has_lock_prefix','has_rep_prefix','has_repne_prefix'])
def test_prefixed_cmp_is_not_an_ordinary_width_proof(prefix):
    from iced_x86 import Decoder
    from il2cpp.x64 import narrow_cmp_width
    ins=next(iter(Decoder(64,bytes.fromhex('6683f809'))))
    setattr(ins,prefix,True)
    assert narrow_cmp_width(ins) is None


def test_unknown_right_operand_does_not_gain_a_cast():
    lift=lifter({'RAX':Expr('value',CHAR,'int'), 'RCX':Expr('other',None,'int')})
    assert 'unchecked' not in execute(lift,'663bc17600')[0]


def test_final_enum_shift_sugar_cannot_remove_the_modulo_boundary():
    from il2cpp.dec.highlevel import _HighLevelMixin
    passes=_HighLevelMixin(); passes._enum_maps={'Example':[({'One':1},{1:'One'})]}
    lines=['if (unchecked((ushort)(ch - 48)) <= 9)']
    assert passes._enum_shift_fold(lines)==lines


@pytest.mark.parametrize('code', ['6683f8097600', '83f86476046683f8097600'])
def test_flat_lift_does_not_assert_unproved_block_flag_provenance(code):
    lift = lifter()
    native = bytes.fromhex(code)
    lift.bin.read = lambda va, size: native
    lift.il.next_method_start = lambda va: va + len(native)
    lift._setup_entry = lambda method, owner: lift.regs.update(
        RAX=Expr('value', (0, 8 << 16), 'int'))
    lift._render = lambda: [text for _, text, _ in lift.out]
    text = '\n'.join(lift.lift(NS(addr=0x1000), NS()))
    assert 'if (' in text
    assert 'unchecked' not in text
