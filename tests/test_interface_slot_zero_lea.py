"""Original synthetic instructions: exact slot-zero interface LEA scan proof.

No fixture machine-code bytes or lifted bodies are embedded here.
"""
from types import SimpleNamespace as NS

import pytest

from il2cpp.prelude import HAVE_ICED

pytestmark = pytest.mark.skipif(not HAVE_ICED, reason='iced_x86 required')


def fixture():
    from iced_x86 import Instruction as I, Code as C, Register as R, MemoryOperand as M
    rr = I.create_reg_reg
    rm = lambda c, r, base, idx=R.NONE, scale=1, disp=0: I.create_reg_mem(
        c, r, M(base, idx, scale, disp))
    branch = lambda c, b: I.create_branch(c, 0x1000 + b * 0x100)
    ins = [
        [rr(C.XOR_RM32_R32, R.EBP, R.EBP)],
        [rm(C.MOV_R64_RM64, R.R11, R.RDI),
         rr(C.MOVZX_R32_RM16, R.EDX, R.BP),
         rm(C.MOVZX_R32_RM16, R.R9D, R.R11, disp=0x12E),
         rr(C.CMP_RM16_R16, R.BP, R.R9W), branch(C.JAE_REL32_64, 5)],
        [rm(C.MOV_R64_RM64, R.R8, R.R11, disp=0xB0)],
        [rr(C.MOVZX_R32_RM16, R.ECX, R.DX),
         rr(C.ADD_RM64_R64, R.RCX, R.RCX),
         I.create_mem_reg(C.CMP_RM64_R64, M(R.R8, R.RCX, 8), R.R10),
         branch(C.JE_REL32_64, 6)],
        [I.create_reg(C.INC_RM16, R.DX),
         rr(C.CMP_RM16_R16, R.DX, R.R9W), branch(C.JB_REL32_64, 3)],
        [rr(C.XOR_RM32_R32, R.R8D, R.R8D),
         rr(C.MOV_R64_RM64, R.RDX, R.R10),
         rr(C.MOV_R64_RM64, R.RCX, R.RDI),
         I.create_branch(C.CALL_REL32_64, 0x9000)],
        [rr(C.MOVZX_R32_RM16, R.EAX, R.DX),
         rr(C.ADD_RM64_R64, R.RAX, R.RAX),
         rm(C.MOVSXD_R64_RM32, R.RCX, R.R8, R.RAX, 8, 8),
         rm(C.LEA_R64_M, R.RAX, R.R11, disp=0x138),
         I.create_reg_i32(C.SHL_RM64_IMM8, R.RCX, 4),
         rr(C.ADD_RM64_R64, R.RAX, R.RCX), branch(C.JMP_REL32_64, 7)],
        [I.create(C.RETNQ)],
    ]
    terms = [('fall', 1), ('jcc', 5, 2), ('fall', 3), ('jcc', 6, 4),
             ('jcc', 3, 5), ('fall', 7), ('jmp', 7), ('ret',)]
    blocks = [NS(bid=b, insns=xs, term=terms[b], succs=list(terms[b][1:]),
                 preds=[], cond=None) for b, xs in enumerate(ins)]
    for b in blocks:
        for n, i in enumerate(b.insns):
            i.ip = 0x1000 + b.bid * 0x100 + n * 10
        for s in b.succs:
            blocks[s].preds.append(b.bid)
    return blocks


def prune(blocks, skip=None):
    from il2cpp.dec.ifaceprune import iface_fast_path_prune
    return iface_fast_path_prune(blocks, {0x9000: 'il2cpp_interface_get_method'}, skip=skip)


def test_exact_zero_slot_scan_prunes_and_removes_dead_count():
    b = fixture()
    skip = set()
    assert prune(b, skip) == 1
    assert b[1].term == ('jmp', 5) and b[1].succs == [5]
    assert b[7].preds == [5]
    assert all(b[i].term == ('abort',) for i in [2, 3, 4, 6])
    assert skip == {0x1100 + 20, 0x1100 + 30}


@pytest.mark.parametrize('fault', [
    'lea_disp', 'lea_index', 'lea_base', 'lea_result', 'lea_width', 'lea_segment',
    'offset_base', 'offset_index', 'offset_scale', 'offset_disp', 'offset_width',
    'shift', 'add_source', 'hit_counter', 'loop_scale', 'loop_iface', 'loop_width',
    'loop_counter', 'loop_branch', 'step_counter', 'step_count', 'step_branch',
    'table_base', 'table_disp', 'table_width', 'count_base', 'count_disp', 'count_width',
    'entry_compare', 'entry_branch', 'slot_nonzero', 'miss_iface', 'miss_receiver',
    'klass_object', 'klass_store', 'klass_clobber', 'receiver_clobber',
    'unknown_seed', 'nonzero_seed', 'partial_zero', 'extra_hit_write', 'extra_store',
    'extra_miss_write', 'extra_entry', 'live_saved_write', 'malformed_loop',
])
def test_near_misses_preserve_original_scan(fault):
    from iced_x86 import Instruction as I, Code as C, Register as R, MemoryOperand as M
    b = fixture()
    h, loop, entry = b[6].insns, b[3].insns, b[1].insns
    if fault == 'lea_disp': h[3].memory_displacement = 0x140
    elif fault == 'lea_index': h[3].memory_index = R.RDX
    elif fault == 'lea_base': h[3].memory_base = R.R12
    elif fault == 'lea_result': h[3].op0_register = R.RDX
    elif fault == 'lea_width': h[3] = I.create_reg_mem(C.LEA_R32_M, R.EAX, M(R.R11, displ=0x138))
    elif fault == 'lea_segment': h[3].segment_prefix = R.FS
    elif fault == 'offset_base': h[2].memory_base = R.R12
    elif fault == 'offset_index': h[2].memory_index = R.RDX
    elif fault == 'offset_scale': h[2].memory_index_scale = 4
    elif fault == 'offset_disp': h[2].memory_displacement = 0
    elif fault == 'offset_width': h[2] = I.create_reg_mem(C.MOV_R64_RM64, R.RCX, M(R.R8, R.RAX, 8, 8))
    elif fault == 'shift': h[4].immediate8 = 3
    elif fault == 'add_source': h[5].op1_register = R.RDX
    elif fault == 'hit_counter': h[0].op1_register = R.BX
    elif fault == 'loop_scale': loop[2].memory_index_scale = 4
    elif fault == 'loop_iface': loop[2].op1_register = R.R12
    elif fault == 'loop_width': loop[2] = I.create_mem_reg(C.CMP_RM32_R32, M(R.R8, R.RCX, 8), R.R10D)
    elif fault == 'loop_counter': loop[0].op1_register = R.BX
    elif fault == 'loop_branch': loop[-1].code = C.JNE_REL32_64
    elif fault == 'step_counter': b[4].insns[0].op0_register = R.CX
    elif fault == 'step_count': b[4].insns[1].op1_register = R.R12W
    elif fault == 'step_branch': b[4].insns[-1].code = C.JBE_REL32_64
    elif fault == 'table_base': b[2].insns[0].memory_base = R.R12
    elif fault == 'table_disp': b[2].insns[0].memory_displacement = 0xB8
    elif fault == 'table_width': b[2].insns[0] = I.create_reg_mem(C.MOV_R32_RM32, R.R8D, M(R.R11, displ=0xB0))
    elif fault == 'count_base': entry[2].memory_base = R.R12
    elif fault == 'count_disp': entry[2].memory_displacement = 0x130
    elif fault == 'count_width': entry[2] = I.create_reg_mem(C.MOVZX_R32_RM8, R.R9D, M(R.R11, displ=0x12E))
    elif fault == 'entry_compare': entry[3].op0_register = R.BX
    elif fault == 'entry_branch': entry[-1].code = C.JA_REL32_64
    elif fault == 'slot_nonzero': b[5].insns[0] = I.create_reg_i32(C.MOV_R32_IMM32, R.R8D, 1)
    elif fault == 'miss_iface': b[5].insns[1].op1_register = R.R12
    elif fault == 'miss_receiver': b[5].insns[2].op1_register = R.RSI
    elif fault == 'klass_object': entry[0].memory_base = R.RSI
    elif fault == 'klass_store': entry[0] = I.create_mem_reg(C.MOV_RM64_R64, M(R.RDI), R.R11)
    elif fault == 'klass_clobber': entry.insert(1, I.create_reg_reg(C.XOR_RM32_R32, R.R11D, R.R11D))
    elif fault == 'receiver_clobber': entry.insert(1, I.create_reg_reg(C.XOR_RM32_R32, R.EDI, R.EDI))
    elif fault == 'unknown_seed': b[0].insns = []
    elif fault == 'nonzero_seed': b[0].insns[0] = I.create_reg_i32(C.MOV_R32_IMM32, R.EBP, 1)
    elif fault == 'partial_zero': b[0].insns[0] = I.create_reg_reg(C.XOR_RM16_R16, R.BP, R.BP)
    elif fault == 'extra_hit_write': h.insert(3, I.create_reg_reg(C.XOR_RM32_R32, R.R12D, R.R12D))
    elif fault == 'extra_store': b[2].insns.append(I.create_mem_reg(C.MOV_RM64_R64, M(R.RDI), R.RAX))
    elif fault == 'extra_miss_write': b[5].insns.insert(0, I.create_reg_reg(C.XOR_RM32_R32, R.R12D, R.R12D))
    elif fault == 'extra_entry': b[3].preds.append(0)
    elif fault == 'live_saved_write':
        h[2].op0_register = R.R12; h[4].op0_register = R.R12; h[5].op1_register = R.R12
        b[7].insns.insert(0, I.create_reg_reg(C.MOV_R64_RM64, R.RAX, R.R12))
    elif fault == 'malformed_loop': b[3].term = ('ret',)
    assert prune(b) == 0
    assert b[1].term == ('jcc', 5, 2)


def test_nops_in_scan_are_ignored():
    from iced_x86 import Instruction as I, Code as C
    b = fixture()
    b[2].insns.append(I.create(C.NOPD))
    assert prune(b) == 1


def test_zero_proof_requires_all_reaching_definitions():
    from iced_x86 import Instruction as I, Code as C, Register as R
    b = fixture()
    b.append(NS(bid=8, insns=[I.create_reg_i32(C.MOV_R32_IMM32, R.EBP, 1)],
                term=('jmp', 1), succs=[1], preds=[], cond=None))
    b[1].preds.append(8)
    assert prune(b) == 0


def test_definition_free_cycle_is_not_a_zero_proof():
    from il2cpp.dec.ifaceprune import _known_zero_before
    b = fixture()
    b[0].insns = []; b[0].preds = [0]
    from iced_x86 import Register as R
    assert not _known_zero_before(b, 1, 1, R.RBP)


def test_alternate_register_assignment_including_hit_counter_overwrite():
    from iced_x86 import Register as R
    b = fixture()
    e, q, s, h = b[1].insns, b[3].insns, b[4].insns, b[6].insns
    e[0].op0_register = R.R10
    e[1].op0_register = R.ECX
    e[2].op0_register = R.EDX; e[2].memory_base = R.R10
    e[3].op1_register = R.DX
    b[2].insns[0].memory_base = R.R10
    q[0].op0_register = R.EAX; q[0].op1_register = R.CX
    q[1].op0_register = R.RAX; q[1].op1_register = R.RAX
    q[2].memory_index = R.RAX; q[2].op1_register = R.R9
    s[0].op0_register = R.CX
    s[1].op0_register = R.CX; s[1].op1_register = R.DX
    b[5].insns[1].op1_register = R.R9
    h[0].op1_register = R.CX; h[3].memory_base = R.R10
    assert prune(b) == 1


def test_zero_proof_accepts_definition_free_cycle_with_zero_entry():
    from il2cpp.dec.ifaceprune import _known_zero_before
    from iced_x86 import Register as R
    b = fixture()
    b.append(NS(bid=8, insns=[], term=('jmp', 1), succs=[1], preds=[0, 8], cond=None))
    b[1].preds = [8]
    assert _known_zero_before(b, 1, 1, R.RBP)


def test_zero_proof_declines_unknown_alternative_entry_and_volatile_call():
    from il2cpp.dec.ifaceprune import _known_zero_before
    from iced_x86 import Instruction as I, Code as C, Register as R
    b = fixture()
    b.append(NS(bid=8, insns=[], term=('jmp', 1), succs=[1], preds=[], cond=None))
    b[1].preds.append(8)
    assert not _known_zero_before(b, 1, 1, R.RBP)
    b[0].insns = [I.create_reg_reg(C.XOR_RM32_R32, R.EAX, R.EAX),
                  I.create_branch(C.CALL_REL32_64, 0x9000)]
    assert not _known_zero_before(b, 0, 2, R.RAX)


@pytest.mark.parametrize('clobbered', ['receiver_rdx', 'receiver_r8', 'interface_r8'])
def test_miss_argument_setup_must_preserve_original_values(clobbered):
    from iced_x86 import Register as R
    b = fixture()
    if clobbered == 'receiver_rdx':
        # Move the counter away so the receiver/scan proof still matches.
        # MOV RDX,iface then destroys the receiver before MOV RCX,RDX.
        b[1].insns[0].memory_base = R.RDX
        b[1].insns[1].op0_register = R.EBX
        b[3].insns[0].op1_register = R.BX
        b[4].insns[0].op0_register = R.BX
        b[4].insns[1].op0_register = R.BX
        b[6].insns[0].op1_register = R.BX
        b[5].insns[2].op1_register = R.RDX
    elif clobbered == 'receiver_r8':
        b[1].insns[0].memory_base = R.R8
        b[2].insns[0].op0_register = R.R12
        b[3].insns[2].memory_base = R.R12
        b[6].insns[2].memory_base = R.R12
        b[5].insns[2].op1_register = R.R8
    else:
        # Move the table away so XOR R8D,R8D alone destroys the interface.
        b[2].insns[0].op0_register = R.R12
        b[3].insns[2].memory_base = R.R12
        b[3].insns[2].op1_register = R.R8
        b[6].insns[2].memory_base = R.R12
        b[5].insns[1].op1_register = R.R8
    skip = set()
    assert prune(b, skip) == 0
    assert b[1].term == ('jcc', 5, 2)
    assert not skip


def test_stack_pointer_cannot_prove_zero_counter():
    from iced_x86 import Instruction as I, Code as C, Register as R
    b = fixture()
    b[0].insns = [I.create_reg_reg(C.XOR_RM32_R32, R.ESP, R.ESP)]
    b[1].insns[1].op1_register = R.SP
    b[1].insns[3].op0_register = R.SP
    assert prune(b) == 0


def test_interface_may_already_occupy_its_destination_register():
    from iced_x86 import Register as R
    b = fixture()
    b[1].insns[1].op0_register = R.EBX
    b[3].insns[0].op1_register = R.BX
    b[4].insns[0].op0_register = R.BX
    b[4].insns[1].op0_register = R.BX
    b[6].insns[0].op1_register = R.BX
    b[3].insns[2].op1_register = R.RDX
    b[5].insns[1].op1_register = R.RDX
    assert prune(b) == 1
