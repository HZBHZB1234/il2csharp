"""Authored native CFGs; no fixture instructions or generated bodies."""
import struct
from types import SimpleNamespace as NS

import pytest
from iced_x86 import Decoder

from il2cpp.binary import PE
from il2cpp.dec.stackframe import prove_block_entry_rsp as prove

START = 0x180001000


def setup(hexbytes, reachable=None):
    body = bytes.fromhex(hexbytes)
    data = bytearray(0x100 + len(body))
    struct.pack_into('<I', data, 0x3c, 0x40)
    data[0x40:0x46] = b'PE\x00\x00\x64\x86'
    data[0x100:] = body
    binary = PE.__new__(PE)
    binary.is64, binary.d = True, bytes(data)
    binary.va2off = lambda va: 0x100 + va - START if START <= va < START + len(body) else None
    flat = list(Decoder(64, body, ip=START))
    blocks = [NS(bid=k, is_entry=k==0,
                 preds=[0] if k and (reachable is None or k in reachable) else [],
                 insns=[ins]) for k, ins in enumerate(flat)]
    return NS(bin=binary), NS(addr=START), flat, blocks


def test_diamond_restores_same_frame_on_both_epilogues():
    args = setup('4883ec284885c974054883c428c34883c428c3')
    assert list(prove(*args).values()) == [0,-40,-40,-40,0,-40,0]


def test_loop_has_a_fixed_point_and_calls_are_balanced():
    # sub rsp,40; dec ecx; jne dec; call rel; add rsp,40; ret
    args = setup('4883ec28ffc975fce8000000104883c428c3')
    assert list(prove(*args).values()) == [0,-40,-40,-40,-40,0]


@pytest.mark.parametrize('push,pop', [('50','58'),('55','5d'),('4154','415c')])
def test_plain_saved_register_frame(push,pop):
    assert list(prove(*setup(push+'4883ec284883c428'+pop+'c3')).values()) == [0,-8,-48,-8,0]


@pytest.mark.parametrize('sub,add,size', [
    ('4883ec28','4883c428',40),
    ('4881ec00020000','4881c400020000',512),
    ('4883c4d8','4883ecd8',40),
])
def test_signed_fixed_frame_adjustment(sub,add,size):
    assert list(prove(*setup(sub+'90'+add+'c3')).values()) == [0,-size,-size,0]


@pytest.mark.parametrize('body', [
    '4883ec28c3',                       # returning with an allocated frame
    '4883ec284885c974044883c428c3',       # unequal join: either 0 or -40
    '4883ec28ebfa',                     # loop grows frame each iteration
    '4883ec28e900000010',               # tail transfer before restoring frame
    '4885c9747fc3',                     # conditional edge outside native window
    'ebffc3',                           # branch into instruction interior
    '4883ec28',                         # fallthrough outside native window
    '54c3',                             # PUSH RSP special semantics
    '5cc3',                             # POP RSP
    '66506658c3',                       # PUSH/POP r16
    'ff342458c3',                       # PUSH memory
    '9c9dc3',                           # implicit RSP writes (flags)
    '4889ccc3',                         # MOV RSP,RCX
    '89ccc3',                           # partial ESP write
    '6689ccc3',                         # partial SP write
    '488d642420c3',                     # LEA RSP
    '4883e4f0c3',                       # stack alignment (not exact allocation)
    '4889ecc3',                         # MOV RSP,RBP quarantined
    'c9c3',                             # LEAVE
    'c21000',                           # RET imm
    'f3c3',                             # prefixed return
    'ffe0',                             # indirect JMP (unknown native edges)
    '0f05c3',                           # syscall
    'ccc3',                             # trap semantics not modeled
    'f04883ec284883c428c3',              # invalid/locked stack adjustment
])
def test_unsupported_or_inconsistent_native_cfg_declines(body):
    assert prove(*setup(body)) is None


def test_balanced_external_tail_is_accepted():
    assert prove(*setup('4883ec284883c428e900000010')) == {0:0,1:-40,2:0}


def test_ud2_path_does_not_require_frame_restore():
    assert prove(*setup('4883ec280f0b')) == {0:0,1:-40}


@pytest.mark.parametrize('call', ['e800000010','ffd0','ff542420'])
def test_near_calls_preserve_caller_frame(call):
    assert list(prove(*setup('4883ec28'+call+'4883c428c3')).values()) == [0,-40,-40,0]


@pytest.mark.parametrize('field,value', [('is64',False),('d',b'')])
def test_explicit_win64_header_is_required(field,value):
    il,m,flat,blocks=setup('c3')
    setattr(il.bin,field,value)
    assert prove(il,m,flat,blocks) is None


def test_is64_duck_type_does_not_prove_win64():
    il,m,flat,blocks=setup('c3')
    il.bin=NS(**il.bin.__dict__)
    assert prove(il,m,flat,blocks) is None


def test_arm64_pe_declines():
    il,m,flat,blocks=setup('c3')
    d=bytearray(il.bin.d);d[0x44:0x46]=bytes.fromhex('64aa');il.bin.d=bytes(d)
    assert prove(il,m,flat,blocks) is None


def test_eh_context_declines_even_with_a_balanced_normal_path():
    assert prove(*setup('c3'),eh={'pads':[START]}) is None


def test_native_bytes_must_match_every_flat_instruction():
    il,m,flat,blocks=setup('4883ec284883c428c3')
    d=bytearray(il.bin.d);d[0x103]=0x38;il.bin.d=bytes(d)
    assert prove(il,m,flat,blocks) is None


def test_noncontiguous_instruction_window_declines():
    il,m,flat,blocks=setup('9090c3')
    assert prove(il,m,[flat[0],flat[2]],[blocks[0],blocks[2]]) is None


def test_method_entry_must_be_native_window_entry():
    il,m,flat,blocks=setup('c3');m.addr-=1
    assert prove(il,m,flat,blocks) is None


@pytest.mark.parametrize('which',[0,1])
def test_a_skipped_stack_adjustment_declines(which):
    il,m,flat,blocks=setup('4883ec284883c428c3')
    assert prove(il,m,flat,blocks,skip={flat[which].ip}) is None


def test_skipped_non_stack_plumbing_is_allowed():
    il,m,flat,blocks=setup('4883ec28904883c428c3')
    assert prove(il,m,flat,blocks,skip={flat[1].ip}) is not None


def test_pruned_production_edge_cannot_hide_native_frame_conflict():
    il,m,flat,blocks=setup('4883ec284885c974044883c428c3')
    assert prove(il,m,flat,blocks[:1]) is None


def test_unknown_stack_write_on_unreachable_native_island_declines():
    # Native window still includes bytes a production prune has hidden.
    il,m,flat,blocks=setup('c34889cc')
    assert prove(il,m,flat,blocks[:1]) is None


def test_unreachable_production_cycle_cannot_inherit_rpo_state():
    assert prove(*setup('c3ebfe')) is None


def test_driver_skipped_unreachable_orphan_needs_no_entry_state():
    il,m,flat,blocks=setup('c390',reachable=set())
    assert prove(il,m,flat,blocks) == {0:0}


def test_no_extra_production_instruction_may_claim_a_proved_entry():
    il,m,flat,blocks=setup('90c3')
    blocks[0].insns.append(list(Decoder(64,bytes.fromhex('48ffc0'),ip=START+1))[0])
    assert prove(il,m,flat,blocks) is None


@pytest.mark.parametrize('change', ['first','last','negative','short'])
def test_native_window_file_mapping_must_be_exact_and_bounded(change):
    il,m,flat,blocks=setup('90c3')
    old=il.bin.va2off
    if change=='first': il.bin.va2off=lambda va: None
    if change=='last': il.bin.va2off=lambda va: old(va)+(1 if va==START+1 else 0)
    if change=='negative': il.bin.va2off=lambda va: -1
    if change=='short': il.bin.d=il.bin.d[:-1]
    assert prove(il,m,flat,blocks) is None


def test_instruction_bound_is_checked_before_native_read():
    il,m,flat,blocks=setup('c3')
    assert prove(il,m,flat*8193,blocks) is None


def test_no_shared_proof_cache_or_mutated_inputs():
    il,m,flat,blocks=setup('4883ec284883c428c3')
    first=prove(il,m,flat,blocks)
    first[1]=999
    assert prove(il,m,flat,blocks)[1] == -40
    assert not hasattr(il,'_frame_entries')
    assert not hasattr(m,'_frame_entries')
    assert il.bin.d[-9:]==bytes.fromhex('4883ec284883c428c3')


def test_frame_proof_is_independent_of_production_visit_order():
    il,m,flat,blocks=setup('4883ec284885c974054883c428c34883c428c3')
    expected=prove(il,m,flat,blocks)
    assert prove(il,m,flat,list(reversed(blocks))) == expected
    assert prove(il,m,flat,blocks[::2]+blocks[1::2]) == expected


def test_native_byte_bound_is_checked_before_decode():
    il,m,flat,blocks=setup('90c3')
    far=flat[-1].copy(); far.ip=START+65536
    assert prove(il,m,[flat[0],far],blocks) is None


def test_pruning_can_only_select_already_proved_entries():
    il,m,flat,blocks=setup('4883ec284885c974054883c428c34883c428c3')
    assert prove(il,m,flat,[blocks[k] for k in (0,2,5,6)]) == {0:0,2:-40,5:-40,6:0}


@pytest.mark.parametrize('write',['4887cc','4887642408','c8000000','660f7ec4'])
def test_other_implicit_or_full_stack_pointer_writes_decline(write):
    assert prove(*setup(write+'c3')) is None


def test_production_block_cannot_linearize_a_jump_over_unreachable_bytes():
    il,m,flat,blocks=setup('eb0190c3')
    blocks[0].insns=flat
    assert prove(il,m,flat,[blocks[0]]) is None


@pytest.mark.parametrize('entries',[0,2])
def test_exactly_one_native_entry_block_is_required(entries):
    il,m,flat,blocks=setup('90c3')
    blocks[0].is_entry=entries>0
    blocks[1].is_entry=entries>1
    assert prove(il,m,flat,blocks) is None


def test_entry_block_cannot_start_after_the_proved_native_entry():
    il,m,flat,blocks=setup('90c3')
    blocks[0].is_entry=False;blocks[1].is_entry=True
    assert prove(il,m,flat,blocks) is None
