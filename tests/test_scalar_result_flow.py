"""Opaque call results over an authored, caller-owned forward native CFG."""
import struct
from types import SimpleNamespace as NS

import pytest
from iced_x86 import Decoder

from il2cpp.binary import PE
from il2cpp.entrylive import xmm0_result_width
from il2cpp.lifter.resultflow import ScalarResultFlow

BASE = 0x1000
CALL = 'e800000000'
SAVE = '0f28f0'  # movaps xmm6,xmm0
SINGLE = 'f30f5ace'  # cvtss2sd xmm1,xmm6: source is still Single
DOUBLE = 'f20f5ace'  # cvtsd2ss xmm1,xmm6: source is Double


def setup(body, *, prefix=''):
    raw = bytes.fromhex(prefix + CALL + body)
    insns = list(Decoder(64, raw, ip=BASE))
    method = NS(index=0, addr=BASE)
    binary = PE.__new__(PE)
    image = bytearray(0x80)
    struct.pack_into('<I', image, 0x3c, 0x40)
    image[0x40:0x46] = b'PE\x00\x00\x64\x86'
    binary.d, binary.is64 = bytes(image), True
    binary.exports = {}
    binary.is_exec_va = lambda ip: True
    binary.read = lambda ip, n: raw[ip - BASE:ip - BASE + n] if BASE <= ip < BASE + len(raw) else None
    meta = NS(methods=[method])
    il = NS(bin=binary, meta=meta, addr_candidates={BASE: [('method', 0)]})
    lift = NS(bin=binary, meta=meta, il=il, _current_method=method)
    call = next(ins for ins in insns if ins.ip == BASE + len(bytes.fromhex(prefix)))
    return ScalarResultFlow(method, insns), lift, call


def width(body, **kwargs):
    flow, lift, call = setup(body, **kwargs)
    return flow.width(lift, call)


@pytest.mark.parametrize('consume,expected', [(SINGLE, 4), (DOUBLE, 8)])
@pytest.mark.parametrize('with_call', [False, True])
def test_every_branch_path_reads_same_scalar_width(consume, expected, with_call):
    arm = CALL if with_call else '90' * 5
    flow, lift, call = setup(SAVE + '85db7405' + arm + consume + 'c3')
    assert xmm0_result_width(lift.bin, call.next_ip) is None
    assert flow.width(lift, call) == expected


def test_unconditional_forward_rejoin_is_inside_owned_native_body():
    assert width(SAVE + 'eb03' + '31c0cc' + SINGLE + 'c3') == 4


@pytest.mark.parametrize('consume', [SINGLE, DOUBLE])
def test_conflicting_width_on_one_arm_declines(consume):
    other = DOUBLE if consume == SINGLE else SINGLE
    assert width(SAVE + '85db7406' + consume + 'eb04' + other + 'c3') is None


@pytest.mark.parametrize('arm', ['c390909090', 'cc90909090', 'ffe3909090',
                                 '4889d89090', '0f57f69090'])
def test_one_bad_path_rejects_the_entire_proof(arm):
    assert len(bytes.fromhex(arm)) == 5
    assert width(SAVE + '85db7405' + arm + SINGLE + 'c3') is None


@pytest.mark.parametrize('regsave', ['0f28c8', '0f28e8', ''])
def test_only_volatile_copies_die_on_a_second_call(regsave):
    # The consume uses XMM6 but no copy there was proved.
    assert width(regsave + '85db7405' + CALL + SINGLE + 'c3') is None


@pytest.mark.parametrize('change', ['0f57f6', 'f30f10f1', '660f6ef1',
                                   'c5fc77', '0f28f1'])
def test_every_actual_or_vector_alias_low_lane_overwrite_ends_the_copy(change):
    assert width(SAVE + change + '85db7405' + CALL + SINGLE + 'c3') is None


@pytest.mark.parametrize('packed', ['0f58f1', '660f58f1', '0fc6f100',
                                    '0f16c6', '0f1133', '660f7ef0'])
def test_packed_high_lane_bitcast_and_memory_escape_are_not_scalar_proof(packed):
    assert width(SAVE + '85db7405' + CALL + packed + SINGLE + 'c3') is None


@pytest.mark.parametrize('branch', ['ebfe', 'e900000001', 'ffe3', '7401'])
def test_backward_external_indirect_and_mid_instruction_targets_decline(branch):
    assert width(SAVE + branch + SINGLE + 'c3') is None


@pytest.mark.parametrize('touch', ['31c0', '4885c0', '4889c3', '0f95c0'])
def test_rax_touch_before_any_later_call_is_ambiguous(touch):
    assert width(SAVE + touch + '85db7405' + CALL + SINGLE + 'c3') is None


def test_rax_after_a_later_call_is_that_calls_own_value():
    assert width(SAVE + CALL + '4889c3' + '85db7401' + '90' + SINGLE + 'c3') == 4


def test_two_different_nonvolatile_copies_survive_a_branch():
    # movaps xmm7,xmm0; one arm overwrites xmm6; consume xmm7 on both arms.
    assert width(SAVE + '0f28f8' + '85db7403' + '0f57f6' + 'f30f5acf' + 'c3') == 4


def test_copy_of_an_unrelated_register_does_not_retain_the_result():
    assert width(SAVE + '0f28f1' + '85db7401' + '90' + SINGLE + 'c3') is None


@pytest.mark.parametrize('nops,expected', [(22, 4), (23, None)])
def test_exact_existing_24_instruction_budget_is_not_increased(nops, expected):
    assert width(SAVE + '90' * nops + SINGLE + 'c3') == expected


def test_state_budget_is_shared_by_both_branch_arms():
    # Each arm alone fits 24; their union must not get 24 per arm.
    consume = SINGLE
    left = '90' * 12 + consume
    right = '90' * 12 + consume
    assert width(SAVE + '85db7412' + left + 'eb10' + right + 'c3') is None


@pytest.mark.parametrize('mode', ['missing_method', 'other_method', 'metadata',
                                  'entry', 'foreign_call', 'call_jump',
                                  'duplicate_ip', 'missing_target', 'registered_join',
                                  'elf', 'x86', 'arm64', 'bad_header'])
def test_native_owner_metadata_and_platform_boundaries(mode):
    flow, lift, call = setup(SAVE + '85db7405' + CALL + SINGLE + 'c3')
    if mode == 'missing_method':
        del lift._current_method
    elif mode == 'other_method':
        lift._current_method = NS(index=0, addr=BASE)
    elif mode == 'metadata':
        lift.meta.methods = [NS(index=0, addr=BASE)]
    elif mode == 'entry':
        flow.method.addr += 1
    elif mode == 'foreign_call':
        call = Decoder(64, bytes.fromhex(CALL), ip=BASE - 5).decode()
    elif mode == 'call_jump':
        call = Decoder(64, bytes.fromhex('e900000000'), ip=BASE).decode()
    elif mode == 'duplicate_ip':
        flow.insns += (flow.insns[0],)
    elif mode == 'missing_target':
        flow.insns = flow.insns[:-2]
    elif mode == 'registered_join':
        lift.il.addr_candidates[flow.insns[-2].ip] = [('method', 1)]
    elif mode == 'elf':
        lift.bin = NS(is64=True, d=lift.bin.d)
    elif mode == 'x86':
        lift.bin.is64 = False
    else:
        data = bytearray(lift.bin.d)
        if mode == 'arm64':
            data[0x44:0x46] = bytes.fromhex('64aa')
        else:
            data[0x40] = 0
        lift.bin.d = bytes(data)
    assert flow.width(lift, call) is None


def test_later_method_cannot_consume_the_previous_methods_context():
    flow, lift, call = setup(SAVE + '85db7401' + '90' + SINGLE + 'c3')
    assert flow.width(lift, call) == 4
    lift._current_method = NS(index=1, addr=BASE)
    assert flow.width(lift, call) is None
    lift._current_method = flow.method
    assert flow.width(lift, call) == 4


def test_proof_only_reads_native_context_not_symbolic_registers():
    flow, lift, call = setup(SAVE + '85db7405' + CALL + SINGLE + 'c3')
    class Unreadable:
        def __getattribute__(self, name):
            raise AssertionError('side probe touched a counted register')
    lift.regs = Unreadable()
    assert flow.width(lift, call) == 4


@pytest.mark.parametrize('zero', ['0f57c0', '660f57c0', '660fefc0'])
def test_zeroing_one_alias_does_not_invalidate_a_nonvolatile_saved_result(zero):
    assert width(SAVE + '85db7405' + CALL + zero + SINGLE + 'c3') == 4


def test_zeroing_the_last_held_copy_is_not_a_return_type():
    assert width('0f57c0' + 'f30f5ac8c3') is None


@pytest.mark.parametrize('shape', ['metadata', 'method', 'export', 'nonexec'])
def test_only_unregistered_executable_native_callees_are_newly_recovered(shape):
    flow, lift, call = setup(SAVE + '85db7401' + '90' + SINGLE + 'c3')
    target = call.near_branch_target
    if shape == 'metadata':
        lift.il.addr_candidates[target] = [('method', 1)]
    elif shape == 'method':
        lift.il.addr_to_method = {target: ('method', 1)}
    elif shape == 'export':
        lift.bin.exports[target] = 'Exported'
    else:
        lift.bin.is_exec_va = lambda ip: False
    assert flow.width(lift, call) is None
