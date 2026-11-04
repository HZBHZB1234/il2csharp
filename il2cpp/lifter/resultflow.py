"""Caller-owned, all-path proof of an opaque call's scalar XMM0 result.

This does not identify the callee, replace its operation, prove its input
signature, or infer any high SIMD lane. In particular CRT error handling
stays in the original native call. Only an unambiguous scalar return
channel, already consumed by every bounded caller path, is recovered.
"""
from il2cpp.prelude import *  # noqa: F401,F403
from il2cpp.entrylive import _width_tables, _copy_tables
from il2cpp.lifter.abi import is_win64_pe


class ScalarResultFlow:
    """Per-method native context; never reused as evidence for another body."""

    def __init__(self, method, insns):
        self.method = method
        self.insns = tuple(insns)
        self._by_ip = None

    def width(self, lift, call, window=24):
        """Return 4/8 only if *all* forward paths first consume that width.

        At most the existing linear proof's 24 instruction states are
        visited in total, not per branch. Calls drop volatile aliases;
        only the low lanes of Win64 nonvolatile XMM6..15 survive. A path
        escaping the decoded method, touching RAX before a later call,
        losing every copy, mixing widths, looping or exceeding the budget
        declines atomically. A packed read is deliberately not scalar proof.
        """
        try:
            return self._width(lift, call, window)
        except (AttributeError, IndexError, KeyError, TypeError, ValueError,
                OverflowError):
            return None

    def _width(self, lift, call, window):
        from iced_x86 import InstructionInfoFactory, OpAccess, RegisterExt, Code

        m = self.method
        if (not HAVE_ICED or not is_win64_pe(lift.bin)
                or getattr(lift, '_current_method', None) is not m
                or not 0 <= m.index < len(lift.meta.methods)
                or lift.meta.methods[m.index] is not m
                or not self.insns or self.insns[0].ip != m.addr
                or call.mnemonic != Mnemonic.CALL
                or call.op0_kind != OpKind.NEAR_BRANCH64
                or call.flow_control != FlowControl.CALL
                or window <= 0):
            return None
        target = call.near_branch_target
        if (not lift.bin.is_exec_va(target)
                or lift.il.addr_candidates.get(target)
                or target in (getattr(lift.il, 'addr_to_method', None) or {})
                or target in lift.bin.exports):
            return None
        if self._by_ip is None:
            self._by_ip = {ins.ip: ins for ins in self.insns}
        by_ip = self._by_ip
        if len(by_ip) != len(self.insns) or by_ip.get(call.ip) != call:
            return None
        widths, rmw = _width_tables()
        copies, _, _ = _copy_tables()
        writes = (OpAccess.WRITE, OpAccess.COND_WRITE, OpAccess.READ_WRITE,
                  OpAccess.READ_COND_WRITE)
        factory = InstructionInfoFactory()
        pending = [(call.next_ip, frozenset({0}), True)]
        seen = set()
        result = None
        while pending:
            ip, held, rax_live = pending.pop()
            state = (ip, held, rax_live)
            if state in seen:
                continue  # identical rejoin, not an independent new proof
            if len(seen) >= window:
                return None
            seen.add(state)
            ins = by_ip.get(ip)
            if (ins is None or ins.code == Code.INVALID or ins.next_ip <= ip
                    or (ip != m.addr and lift.il.addr_candidates.get(ip))):
                return None
            used = factory.info(ins).used_registers()
            if rax_live and any(RegisterExt.is_gpr(u.register)
                                and RegisterExt.full_register(u.register) == IReg.RAX
                                for u in used):
                return None
            # No YMM/ZMM/high-lane argument is inferred by this rule.
            touched = {RegisterExt.number(u.register) for u in used
                       if RegisterExt.is_vector_register(u.register)}
            ops = [(j, ins.op_register(j)) for j in range(ins.op_count)
                   if ins.op_kind(j) == OpKind.REGISTER]
            mine = [(j, r) for j, r in ops
                    if RegisterExt.is_xmm(r) and RegisterExt.number(r) in held]
            explicit = {RegisterExt.number(r) for _, r in mine}
            if (touched & held) - explicit:
                return None
            # Exact legacy self-xor is a write, not a read of stale bits.
            zero = (ins.mnemonic in (Mnemonic.XORPS, Mnemonic.XORPD, Mnemonic.PXOR)
                    and ins.op_count == 2 and ins.op0_kind == OpKind.REGISTER
                    and ins.op1_kind == OpKind.REGISTER
                    and RegisterExt.is_xmm(ins.op0_register)
                    and ins.op0_register == ins.op1_register)
            src = [] if zero else [j for j, _ in mine if j >= 1]
            if not src and ins.mnemonic in rmw and ins.op_count == 2:
                src = [j for j, _ in mine if j == 0]
            if src:
                if (ins.mnemonic in copies and ins.op_count == 2
                        and ins.op0_kind == OpKind.REGISTER
                        and ins.op1_kind == OpKind.REGISTER
                        and RegisterExt.is_xmm(ins.op0_register)
                        and RegisterExt.is_xmm(ins.op1_register)):
                    held = held | {RegisterExt.number(ins.op0_register)}
                elif ins.mnemonic in widths:
                    width = widths[ins.mnemonic]
                    if result is not None and result != width:
                        return None
                    result = width
                    continue
                else:
                    return None
            else:
                # Even a partial/vector-alias write ends this low-lane fact.
                killed = {RegisterExt.number(u.register) for u in used
                          if RegisterExt.is_vector_register(u.register)
                          and u.access in writes}
                held = held - killed
                if not held:
                    return None
            fc = ins.flow_control
            if fc == FlowControl.NEXT:
                pending.append((ins.next_ip, frozenset(held), rax_live))
            elif fc == FlowControl.CALL and ins.op0_kind == OpKind.NEAR_BRANCH64:
                held = frozenset(n for n in held if 6 <= n <= 15)
                if not held:
                    return None
                pending.append((ins.next_ip, held, False))
            elif (fc in (FlowControl.CONDITIONAL_BRANCH,
                         FlowControl.UNCONDITIONAL_BRANCH)
                    and ins.op0_kind == OpKind.NEAR_BRANCH64):
                target = ins.near_branch_target
                if target <= ins.ip or target not in by_ip:
                    return None  # includes loops and out-of-method tail jumps
                pending.append((target, frozenset(held), rax_live))
                if fc == FlowControl.CONDITIONAL_BRANCH:
                    pending.append((ins.next_ip, frozenset(held), rax_live))
            else:
                return None
        return result
