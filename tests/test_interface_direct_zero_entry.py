"""Authored instruction graphs for an exact local-zero interface-scan entry.

No game-native bytes or lifted bodies are stored here.
"""
import pytest
from iced_x86 import Instruction as I, Code as C, Register as R, MemoryOperand as M
from test_interface_slot_zero_lea import fixture as classic_fixture, prune


def fixture():
    b = classic_fixture()
    e = b[1].insns
    b[0].insns = []  # No reaching zero is available or needed.
    b[1].insns = [e[0], I.create_reg_reg(C.XOR_RM32_R32, R.EDX, R.EDX),
                  I.create_reg_mem(C.MOV_R64_RM64, R.R10, M(R.RIP, displ=0x5000)),
                  e[2], I.create_reg_reg(C.CMP_RM16_R16, R.DX, R.R9W), e[4]]
    for bid, block in enumerate(b):
        for n, ins in enumerate(block.insns):
            ins.ip = 0x1000 + bid * 0x100 + n * 10
    return b


def snapshot(blocks):
    return [(b.term, tuple(b.succs), tuple(b.preds), b.cond,
             tuple((i.ip, str(i), i.segment_prefix, i.has_rep_prefix, i.has_repne_prefix)
                   for i in b.insns)) for b in blocks]


def counter(b, r32, r16):
    b[1].insns[1] = I.create_reg_reg(C.XOR_RM32_R32, r32, r32)
    b[1].insns[4].op0_register = r16
    b[3].insns[0].op1_register = r16
    b[4].insns[0].op0_register = r16
    b[4].insns[1].op0_register = r16
    b[6].insns[0].op1_register = r16


def test_exact_direct_zero_entry():
    b = fixture()
    original_instructions = [tuple(str(i) for i in block.insns) for block in b]
    skip = {0xdead}
    assert prune(b, skip) == 1
    assert b[1].term == ('jmp', 5) and b[1].succs == [5]
    assert b[5].preds == [1] and b[7].preds == [5]
    assert all(b[x].term == ('abort',) and not b[x].succs for x in (2,3,4,6))
    assert skip == {0xdead, 0x111e, 0x1128}
    assert original_instructions == [tuple(str(i) for i in block.insns) for block in b]


@pytest.mark.parametrize('r32,r16', [(R.EAX,R.AX),(R.EDX,R.DX),(R.EBX,R.BX),
                                    (R.EBP,R.BP),(R.ESI,R.SI),(R.R12D,R.R12W),
                                    (R.R13D,R.R13W),(R.R14D,R.R14W),(R.R15D,R.R15W)])
def test_distinct_counter_registers(r32,r16):
    b=fixture();counter(b,r32,r16)
    assert prune(b)==1


@pytest.mark.parametrize('fault',[
    'zero16','zero64','zero8','different_zero_source','nonzero','seed_mov',
    'wrong_seed_register','wrong_entry_counter','wrong_count','wrong_cmp_width',
    'wrong_branch','missing_seed','extra_instruction','extra_store','extra_call',
    'reordered_setup','klass_clobber','receiver_clobber','iface_clobber',
    'iface_base','iface_index','iface_width','iface_destination','iface_store',
    'klass_receiver','klass_displacement','klass_index','klass_width',
    'count_base','count_displacement','count_index','count_width','count_signed',
    'table_base','table_displacement','table_width','table_store',
    'hit_offset_disp','hit_shift','hit_counter','loop_iface','loop_counter',
    'slot_nonzero','miss_iface','miss_receiver','call_other_helper',
    'extra_region_entry','extra_join_entry','live_preserved_scan_write'])
def test_near_misses_leave_entire_graph_unchanged(fault):
    b=fixture();e=b[1].insns
    if fault=='zero16': e[1]=I.create_reg_reg(C.XOR_RM16_R16,R.DX,R.DX)
    elif fault=='zero64': e[1]=I.create_reg_reg(C.XOR_RM64_R64,R.RDX,R.RDX)
    elif fault=='zero8': e[1]=I.create_reg_reg(C.XOR_RM8_R8,R.DL,R.DL)
    elif fault=='different_zero_source': e[1].op1_register=R.EAX
    elif fault=='nonzero': e[1]=I.create_reg_i32(C.MOV_R32_IMM32,R.EDX,1)
    elif fault=='seed_mov': e[1]=I.create_reg_i32(C.MOV_R32_IMM32,R.EDX,0)
    elif fault=='wrong_seed_register': e[1]=I.create_reg_reg(C.XOR_RM32_R32,R.EAX,R.EAX)
    elif fault=='wrong_entry_counter': e[4].op0_register=R.AX
    elif fault=='wrong_count': e[4].op1_register=R.R10W
    elif fault=='wrong_cmp_width': e[4]=I.create_reg_reg(C.CMP_RM32_R32,R.EDX,R.R9D)
    elif fault=='wrong_branch': e[-1].code=C.JA_REL32_64
    elif fault=='missing_seed': del e[1]
    elif fault=='extra_instruction': e.insert(3,I.create_reg_reg(C.MOV_R64_RM64,R.R12,R.R13))
    elif fault=='extra_store': e.insert(3,I.create_mem_reg(C.MOV_RM64_R64,M(R.RDI),R.RAX))
    elif fault=='extra_call': e.insert(3,I.create_branch(C.CALL_REL32_64,0x9000))
    elif fault=='reordered_setup': e[1],e[2]=e[2],e[1]
    elif fault=='klass_clobber': e[2]=I.create_reg_reg(C.XOR_RM32_R32,R.R11D,R.R11D)
    elif fault=='receiver_clobber': e[2]=I.create_reg_reg(C.XOR_RM32_R32,R.EDI,R.EDI)
    elif fault=='iface_clobber': e[2]=I.create_reg_reg(C.XOR_RM32_R32,R.R10D,R.R10D)
    elif fault=='iface_base': e[2].memory_base=R.RBX
    elif fault=='iface_index': e[2].memory_index=R.RAX
    elif fault=='iface_width': e[2]=I.create_reg_mem(C.MOV_R32_RM32,R.R10D,M(R.RIP,displ=0x5000))
    elif fault=='iface_destination': e[2].op0_register=R.R12
    elif fault=='iface_store': e[2]=I.create_mem_reg(C.MOV_RM64_R64,M(R.RIP,displ=0x5000),R.R10)
    elif fault=='klass_receiver': e[0].memory_base=R.RSI
    elif fault=='klass_displacement': e[0].memory_displacement=8
    elif fault=='klass_index': e[0].memory_index=R.RAX
    elif fault=='klass_width': e[0]=I.create_reg_mem(C.MOV_R32_RM32,R.R11D,M(R.RDI))
    elif fault=='count_base': e[3].memory_base=R.R12
    elif fault=='count_displacement': e[3].memory_displacement=0x130
    elif fault=='count_index': e[3].memory_index=R.RAX
    elif fault=='count_width': e[3]=I.create_reg_mem(C.MOVZX_R32_RM8,R.R9D,M(R.R11,displ=0x12e))
    elif fault=='count_signed': e[3]=I.create_reg_mem(C.MOVSX_R32_RM16,R.R9D,M(R.R11,displ=0x12e))
    elif fault=='table_base': b[2].insns[0].memory_base=R.R12
    elif fault=='table_displacement': b[2].insns[0].memory_displacement=0xb8
    elif fault=='table_width': b[2].insns[0]=I.create_reg_mem(C.MOV_R32_RM32,R.R8D,M(R.R11,displ=0xb0))
    elif fault=='table_store': b[2].insns[0]=I.create_mem_reg(C.MOV_RM64_R64,M(R.R11,displ=0xb0),R.R8)
    elif fault=='hit_offset_disp': b[6].insns[2].memory_displacement=0
    elif fault=='hit_shift': b[6].insns[4].immediate8=3
    elif fault=='hit_counter': b[6].insns[0].op1_register=R.AX
    elif fault=='loop_iface': b[3].insns[2].op1_register=R.R12
    elif fault=='loop_counter': b[3].insns[0].op1_register=R.AX
    elif fault=='slot_nonzero': b[5].insns[0]=I.create_reg_i32(C.MOV_R32_IMM32,R.R8D,1)
    elif fault=='miss_iface': b[5].insns[1].op1_register=R.R12
    elif fault=='miss_receiver': b[5].insns[2].op1_register=R.RSI
    elif fault=='call_other_helper': b[5].insns[-1].near_branch64=0x9001
    elif fault=='extra_region_entry': b[3].preds.append(0)
    elif fault=='extra_join_entry': b[7].preds.append(0)
    elif fault=='live_preserved_scan_write':
        b[6].insns[2].op0_register=R.R12;b[6].insns[4].op0_register=R.R12;b[6].insns[5].op1_register=R.R12
        b[7].insns.insert(0,I.create_reg_reg(C.MOV_R64_RM64,R.RAX,R.R12))
    before=snapshot(b);skip={0xdead}
    assert prune(b,skip)==0
    assert snapshot(b)==before and skip=={0xdead}


@pytest.mark.parametrize('slot',range(6))
@pytest.mark.parametrize('prefix',['segment','rep','repne'])
def test_unproved_entry_prefixes_decline(slot,prefix):
    b=fixture();ins=b[1].insns[slot]
    if prefix=='segment': ins.segment_prefix=R.FS
    elif prefix=='rep': ins.has_rep_prefix=True
    else: ins.has_repne_prefix=True
    before=snapshot(b)
    assert prune(b)==0 and snapshot(b)==before


@pytest.mark.parametrize('r32,r16',[(R.ESP,R.SP),(R.EDI,R.DI),(R.R11D,R.R11W),
                                   (R.R10D,R.R10W),(R.R9D,R.R9W),(R.R8D,R.R8W),
                                   (R.ECX,R.CX)])
def test_overlapping_counter_roles_decline(r32,r16):
    b=fixture();counter(b,r32,r16);before=snapshot(b)
    assert prune(b)==0 and snapshot(b)==before


def test_existing_copy_seed_with_in_block_zero_still_qualifies():
    b=classic_fixture()
    b[1].insns.insert(1,I.create_reg_reg(C.XOR_RM32_R32,R.EBP,R.EBP))
    b[0].insns=[]
    assert prune(b)==1