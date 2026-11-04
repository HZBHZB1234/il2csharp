"""A dword CMP/Jcc compares UInt32 bit patterns, even for signed sources."""
import pytest
from il2cpp import Expr
from test_native_values import lifter, execute, INT

@pytest.mark.parametrize('jcc,op', [('77','>'),('73','>='),('72','<'),('76','<=')])
@pytest.mark.parametrize('cmp', ['83f809','3d09000000','3bc1'])
def test_unsigned_dword_operands_keep_all_32_bits(cmp,jcc,op):
    lift=lifter({'RAX':Expr('state',INT,'int'),'RCX':Expr('other',INT,'int')})
    rhs='unchecked((uint)(other))' if cmp=='3bc1' else '9'
    assert execute(lift,cmp+jcc+'00')[0].startswith(
        f'if (unchecked((uint)(state)) {op} {rhs}) goto L_')

@pytest.mark.parametrize('te',range(3,12))
def test_closed_integer_sources_allow_a_low_dword_view(te):
    lift=lifter({'RAX':Expr('value',(0,te<<16),'int')})
    assert 'unchecked((uint)(value)) <= 9' in execute(lift,'83f8097600')[0]

@pytest.mark.parametrize('code,rhs',[
    ('83f8ff','unchecked((uint)(-1))'),
    ('3dffffffff','4294967295'),
    ('3d00000080','2147483648'),
])
def test_dword_immediate_signedness_is_normalized(code,rhs):
    lift=lifter({'RAX':Expr('value',INT,'int')})
    assert f'<= {rhs}' in execute(lift,code+'7600')[0]

@pytest.mark.parametrize('middle',['90','4889c9','488d4901'])
def test_dword_flag_preserving_instructions_keep_width(middle):
    lift=lifter({'RAX':Expr('value',INT,'int'),'RCX':Expr('other',INT,'int')})
    assert 'unchecked((uint)(value))' in execute(lift,'83f809'+middle+'7600')[0]

@pytest.mark.parametrize('middle',['f8','f9','f5','9e','f7e1','83c101'])
def test_changed_or_undefined_dword_flags_decline(middle):
    lift=lifter({'RAX':Expr('value',INT,'int'),'RCX':Expr('other',INT,'int')})
    assert 'unchecked' not in '\n'.join(execute(lift,'83f809'+middle+'7600'))

@pytest.mark.parametrize('call',['e800000000','ffd1'])
def test_dword_width_does_not_survive_a_call(call):
    lift=lifter({'RAX':Expr('value',INT,'int')})
    lift._call=lambda *args:None
    assert 'unchecked' not in execute(lift,'83f809'+call+'7600')[0]

@pytest.mark.parametrize('omitted',['90','f9','83c101'])
def test_dword_width_does_not_survive_a_skipped_native_instruction(omitted):
    from iced_x86 import Decoder
    lift=lifter({'RAX':Expr('value',INT,'int')})
    insns=list(Decoder(64,bytes.fromhex('83f809'+omitted+'7600'),ip=0x1000))
    for idx in (0,2):lift._insn(insns[idx],insns,idx,None,insns[-1].next_ip)
    assert 'unchecked' not in lift.out[0][1]

@pytest.mark.parametrize('code',['83f8097e00','83f8097400','4883f8097600','8339097600','3b017600'])
def test_non_unsigned_dword_register_checks_stay_unchanged(code):
    lift=lifter({'RAX':Expr('value',INT,'int'),'RCX':Expr('other',INT,'int')})
    assert 'unchecked' not in '\n'.join(execute(lift,code))

@pytest.mark.parametrize('prefix',['has_lock_prefix','has_rep_prefix','has_repne_prefix'])
def test_prefixed_dword_cmp_does_not_prove_width(prefix):
    from iced_x86 import Decoder
    from il2cpp.x64 import narrow_cmp_width
    ins=next(iter(Decoder(64,bytes.fromhex('83f809'))));setattr(ins,prefix,True)
    assert narrow_cmp_width(ins) is None


def test_replaced_dword_flag_pair_has_no_width_proof():
    lift=lifter({'RAX':Expr('value',INT,'int')})
    execute(lift,'83f809');lift.flags=lift.flags
    assert 'unchecked' not in execute(lift,'7600')[0]


def test_algebra_sugar_cannot_remove_the_dword_modulo_boundary():
    from il2cpp.dec.highlevel import _HighLevelMixin
    passes=_HighLevelMixin();passes._enum_maps={'Example':[({'One':1},{1:'One'})]}
    lines=['if (unchecked((uint)(state - 48)) <= 9)']
    assert passes._enum_shift_fold(lines)==lines


def test_reuse_replaces_word_width_with_dword_width():
    lift=lifter({'RAX':Expr('value',INT,'int')})
    assert 'unchecked((ushort)(value))' in execute(lift,'6683f8097600')[0]
    lift.out=[]
    text=execute(lift,'83f8097600')[0]
    assert 'unchecked((uint)(value))' in text
    assert 'ushort' not in text


@pytest.mark.parametrize('ty,kind,text,unk', [
    (None,'int','value',False), ((0,2<<16),'int','value',False),
    ((0,0xc<<16),'float','value',False), ((0,0x11<<16),'int','value',False),
    ((0,0xf<<16),'ptr','value',False), ((0,8<<16|1<<29),'int','value',False),
    (INT,'int','value',True), (INT,'int','?',False),
])
def test_unproved_dword_operand_declines(ty,kind,text,unk):
    value=Expr(text,ty,kind);value._unk=unk
    assert 'unchecked' not in execute(lifter({'RAX':value}),'83f8097600')[0]


@pytest.mark.parametrize('code', ['83f8097600','6683f864760483f8097600'])
def test_flat_dword_lift_keeps_unproved_branch_provenance(code):
    from types import SimpleNamespace as NS
    lift=lifter();native=bytes.fromhex(code)
    lift.bin.read=lambda va,size:native
    lift.il.next_method_start=lambda va:va+len(native)
    lift._setup_entry=lambda method,owner:lift.regs.update(RAX=Expr('value',INT,'int'))
    lift._render=lambda:[text for _,text,_ in lift.out]
    text='\n'.join(lift.lift(NS(addr=0x1000),NS()))
    assert 'if (' in text
    assert 'unchecked' not in text
