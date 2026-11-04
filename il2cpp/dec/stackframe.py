"""Bounded, native-CFG proof of entry-relative RSP, independent of render order.

No RBP/value/name facts are inferred. Unsupported methods keep the old path.
"""
from collections import deque

from iced_x86 import (Code, CodeSize, Decoder, FlowControl, InstructionInfoFactory,
                      Mnemonic, OpAccess, OpKind, Register, RegisterExt)

from il2cpp.lifter.abi import is_win64_pe
from il2cpp.text import imm_of

_WRITES = (OpAccess.WRITE, OpAccess.COND_WRITE, OpAccess.READ_WRITE,
           OpAccess.READ_COND_WRITE)
_MAX_INSNS, _MAX_BYTES = 8192, 65536


def _plain(ins):
    return not (ins.has_lock_prefix or ins.has_rep_prefix
                or ins.has_repne_prefix or ins.segment_prefix != Register.NONE)


def _sp_effect(ins, factory):
    """None is an unmodelled write; zero is a proved SP-preserving operation."""
    if ins.mnemonic in (Mnemonic.PUSH, Mnemonic.POP):
        if (not _plain(ins) or ins.code not in (Code.PUSH_R64, Code.POP_R64)
                or ins.op0_register == Register.RSP):
            return None
        return -8 if ins.mnemonic == Mnemonic.PUSH else 8
    # Near calls return to the next instruction under the Win64 ABI. Their
    # implicit push is balanced by the callee, not a caller frame allocation.
    if ins.flow_control in (FlowControl.CALL, FlowControl.INDIRECT_CALL):
        return 0 if _plain(ins) and ins.code in (
            Code.CALL_REL32_64, Code.CALL_RM64) else None
    if ins.flow_control == FlowControl.RETURN:
        return 0 if _plain(ins) and ins.code == Code.RETNQ else None
    writes_sp = any(RegisterExt.full_register(u.register) == Register.RSP
                    and u.access in _WRITES
                    for u in factory.info(ins).used_registers())
    if not writes_sp:
        return 0
    if (_plain(ins) and ins.code in (Code.ADD_RM64_IMM8,
            Code.ADD_RM64_IMM32, Code.SUB_RM64_IMM8, Code.SUB_RM64_IMM32)
            and ins.op0_kind == OpKind.REGISTER
            and ins.op0_register == Register.RSP):
        value = imm_of(ins, 1)
        return value if ins.mnemonic == Mnemonic.ADD else -value
    return None


def prove_block_entry_rsp(il, method, flat, blocks, skip=(), eh=None):
    """Return {bid: entry_rsp} only for a complete, exact native-window proof.

    Production CFG edges/pruning cannot prove native reachability. They are
    consulted only after the independent instruction-CFG has been solved.
    """
    if eh or not is_win64_pe(getattr(il, 'bin', None)):
        return None
    if not flat or len(flat) > _MAX_INSNS or flat[0].ip != method.addr:
        return None
    lo, hi = flat[0].ip, flat[-1].next_ip
    if hi <= lo or hi - lo > _MAX_BYTES:
        return None
    if any(a.next_ip != b.ip for a, b in zip(flat, flat[1:])):
        return None
    binary = il.bin
    off = binary.va2off(lo)
    if (off is None or off < 0 or off + hi - lo > len(binary.d)
            or binary.va2off(hi - 1) != off + hi - lo - 1):
        return None
    native = list(Decoder(64, binary.d[off:off + hi - lo], ip=lo))
    if native != list(flat) or any(i.is_invalid or i.code_size != CodeSize.CODE64 for i in native):
        return None
    by_ip = {i.ip: i for i in native}
    factory = InstructionInfoFactory()
    effects = {i.ip: _sp_effect(i, factory) for i in native}
    # Skipped SP effects would make symbolic execution disagree with the proof.
    # Unknown effects decline even on an unreachable byte island.
    if any(v is None or (v and ip in skip) for ip, v in effects.items()):
        return None
    states, pending = {lo: 0}, deque([lo])
    while pending:
        ip = pending.popleft()
        ins = by_ip[ip]
        before = states[ip]
        after = before + effects[ip]
        if not -(1 << 31) <= after < (1 << 31):
            return None
        fc = ins.flow_control
        if fc in (FlowControl.NEXT, FlowControl.CALL, FlowControl.INDIRECT_CALL):
            successors = (ins.next_ip,)
        elif fc == FlowControl.CONDITIONAL_BRANCH:
            if not _plain(ins) or ins.op0_kind != OpKind.NEAR_BRANCH64:
                return None
            successors = (ins.near_branch_target, ins.next_ip)
        elif fc == FlowControl.UNCONDITIONAL_BRANCH:
            if not _plain(ins) or ins.op0_kind != OpKind.NEAR_BRANCH64:
                return None
            target = ins.near_branch_target
            if not lo <= target < hi:
                # A tail transfer may only expose the original caller's frame.
                if after != 0:
                    return None
                successors = ()
            else:
                successors = (target,)
        elif fc == FlowControl.RETURN:
            if before != 0:
                return None
            successors = ()
        elif fc == FlowControl.EXCEPTION and ins.mnemonic == Mnemonic.UD2:
            successors = ()
        else:
            return None
        for succ in successors:
            if succ not in by_ip:
                return None
            if succ in states:
                if states[succ] != after:
                    return None
            else:
                states[succ] = after
                pending.append(succ)
    entry_blocks = [b for b in blocks if b.is_entry]
    if (len(entry_blocks) != 1 or not entry_blocks[0].insns
            or entry_blocks[0].insns[0].ip != lo):
        return None
    entries = {}
    for b in blocks:
        # Match the analysis driver's execution predicate. Unreachable cycles
        # still have predecessors and must decline, never inherit an RPO state.
        if not b.is_entry and not b.preds:
            continue
        if not b.insns or b.insns[0].ip not in states:
            return None
        # Production may remove instructions, but must not synthesize/reorder
        # native instructions or put a different SP path inside one block.
        for a, nxt in zip(b.insns, b.insns[1:]):
            if a.next_ip != nxt.ip:
                return None
        rsp = states[b.insns[0].ip]
        for i in b.insns:
            if (i.ip not in by_ip or i != by_ip[i.ip]
                    or states.get(i.ip) != rsp):
                return None
            rsp += effects[i.ip]
        entries[b.bid] = states[b.insns[0].ip]
    return entries
