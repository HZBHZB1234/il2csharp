"""Unsigned SETcc/CMOVcc comparison conditions; not a partial-register proof."""
import pytest
from types import SimpleNamespace as NS
from il2cpp import Expr
from test_native_values import lifter,execute,INT

WIDTHS=[('3c09','byte'),('6683f809','ushort'),('83f809','uint')]
CONSUMERS=[('0f97c0','>'),('0f93c0','>='),('0f92c0','<'),('0f96c0','<='),
           ('0f47c2','>'),('0f43c2','>='),('0f42c2','<'),('0f46c2','<=')]
def seeded():
    return lifter({'RAX':Expr('value',INT,'int'),'RDX':Expr('other',INT,'int'),
                   'RCX':Expr('temp',INT,'int')})
def result(code):
    lift=seeded();execute(lift,code)
    return lift.regs['RAX'].text

@pytest.mark.parametrize('cmp,cast',WIDTHS)
@pytest.mark.parametrize('consumer,op',CONSUMERS)
def test_closed_unsigned_consumer_preserves_machine_width(cmp,cast,consumer,op):
    text=result(cmp+consumer)
    assert f'unchecked(({cast})(value)) {op} 9' in text

@pytest.mark.parametrize('cmp,cast',[('3ac2','byte'),('663bc2','ushort'),('3bc2','uint')])
@pytest.mark.parametrize('consumer,op',CONSUMERS)
def test_register_pair_consumers_normalize_both_operands(cmp,cast,consumer,op):
    assert f'unchecked(({cast})(value)) {op} unchecked(({cast})(other))' in result(cmp+consumer)

@pytest.mark.parametrize('cmp,cast',[('3cff','byte'),('6683f8ff','ushort'),('83f8ff','uint')])
@pytest.mark.parametrize('consumer,op',CONSUMERS)
def test_immediate_consumer_preserves_unsigned_all_ones(cmp,cast,consumer,op):
    text=result(cmp+consumer)
    rhs='255' if cast=='byte' else f'unchecked(({cast})(-1))'
    assert f'unchecked(({cast})(value)) {op} {rhs}' in text

@pytest.mark.parametrize('middle',['f8','f9','f5','9e','f7e1','83c101'])
@pytest.mark.parametrize('consumer,op',CONSUMERS)
def test_flag_clobbers_decline_consumer_recovery(middle,consumer,op):
    assert 'unchecked' not in result('83f809'+middle+consumer)

@pytest.mark.parametrize('middle',['90','4889c9','488d4901'])
@pytest.mark.parametrize('consumer,op',CONSUMERS)
def test_contiguous_flag_preserving_instructions_keep_proof(middle,consumer,op):
    assert f'unchecked((uint)(value)) {op} 9' in result('83f809'+middle+consumer)

@pytest.mark.parametrize('consumer,op',CONSUMERS)
def test_skipped_native_instruction_drops_consumer_proof(consumer,op):
    from iced_x86 import Decoder
    lift=seeded();insns=list(Decoder(64,bytes.fromhex('83f80990'+consumer),ip=0x1000))
    for idx in (0,2):lift._insn(insns[idx],insns,idx,None,insns[-1].next_ip)
    assert 'unchecked' not in lift.regs['RAX'].text

@pytest.mark.parametrize('consumer,op',CONSUMERS)
def test_replaced_flag_pair_cannot_assert_consumer_width(consumer,op):
    lift=seeded();execute(lift,'83f809');lift.flags=lift.flags;execute(lift,consumer)
    assert 'unchecked' not in lift.regs['RAX'].text

@pytest.mark.parametrize('call',['e800000000','ffd1'])
@pytest.mark.parametrize('consumer,op',CONSUMERS)
def test_call_invalidates_consumer_width(call,consumer,op):
    lift=seeded();lift._call=lambda *args:None;execute(lift,'83f809'+call+consumer)
    assert 'unchecked' not in lift.regs['RAX'].text

@pytest.mark.parametrize('cmp',['4883f809','833909','80fc09'])
@pytest.mark.parametrize('consumer,op',CONSUMERS)
def test_unsupported_cmp_shapes_keep_parent_spelling(cmp,consumer,op):
    assert 'unchecked' not in result(cmp+consumer)

@pytest.mark.parametrize('consumer',['0f9fc0','0f9dc0','0f9cc0','0f9ec0','0f94c0','0f95c0',
                                      '0f4fc2','0f4dc2','0f4cc2','0f4ec2','0f44c2','0f45c2'])
def test_signed_and_equality_consumers_are_unchanged(consumer):
    assert 'unchecked' not in result('83f809'+consumer)

@pytest.mark.parametrize('ty,kind,unk',[(None,'int',False),((0,2<<16),'int',False),
    ((0,0x11<<16),'int',False),((0,0xf<<16),'ptr',False),((0,8<<16|1<<29),'int',False),
    (INT,'int',True)])
@pytest.mark.parametrize('consumer',['0f96c0','0f46c2'])
def test_unclosed_operand_types_decline(ty,kind,unk,consumer):
    value=Expr('value',ty,kind);value._unk=unk
    lift=seeded();lift.regs['RAX']=value;execute(lift,'83f809'+consumer)
    assert 'unchecked' not in lift.regs['RAX'].text

@pytest.mark.parametrize('cmp,cast',WIDTHS)
@pytest.mark.parametrize('consumer,op',CONSUMERS)
def test_flat_fallback_does_not_gain_unproved_consumer_provenance(cmp,cast,consumer,op):
    lift=seeded();native=bytes.fromhex(cmp+consumer)
    lift.bin.read=lambda va,size:native
    lift.il.next_method_start=lambda va:va+len(native)
    lift._setup_entry=lambda m,td:lift.regs.update(RAX=Expr('value',INT,'int'),RDX=Expr('other',INT,'int'))
    lift._render=lambda:[lift.regs['RAX'].text]
    assert 'unchecked' not in '\n'.join(lift.lift(NS(addr=0x1000),NS()))
