"""Recognize metadata initialization bookkeeping once for both lifting paths.

A candidate owns its skip set: nothing is published until its forward JNE,
helper arguments, closing flag store and release fences have all been checked.
Ordinary gap instructions are never elided; unowned body effects decline.
Unknown shapes keep native control flow instead of borrowing a proof from a
different initialization.
"""
from il2cpp.prelude import *  # noqa: F401,F403
from il2cpp.text import imm_of

GAP_MAX = 16
BODY_MAX = 1024


def is_init_barrier(ins):
    return (ins.mnemonic == Mnemonic.OR and ins.has_lock_prefix
            and ins.op0_kind == OpKind.MEMORY and ins.memory_base == IReg.RSP
            and ins.memory_index == IReg.NONE and ins.memory_displacement == 0
            and MemorySizeExt.size(ins.memory_size) in (4, 8)
            and ins.op1_kind in (OpKind.IMMEDIATE8, OpKind.IMMEDIATE8TO32,
                                 OpKind.IMMEDIATE8TO64, OpKind.IMMEDIATE32,
                                 OpKind.IMMEDIATE32TO64)
            and imm_of(ins, 1) == 0)


def _flag(ins, slot, value):
    return (ins.mnemonic == Mnemonic.MOV and ins.op0_kind == OpKind.MEMORY
            and ins.memory_base == IReg.RIP and ins.memory_size == 1
            and ins.ip_rel_memory_address == slot
            and ins.op1_kind == OpKind.IMMEDIATE8 and imm_of(ins, 1) == value)


if HAVE_ICED:
    from iced_x86 import InstructionInfoFactory, OpAccess, RegisterExt
    _WRITES = (OpAccess.WRITE, OpAccess.COND_WRITE, OpAccess.READ_WRITE,
               OpAccess.READ_COND_WRITE)
    _HIGH = (IReg.AH, IReg.CH, IReg.DH, IReg.BH)
    _ZERO_IMMS = (OpKind.IMMEDIATE8, OpKind.IMMEDIATE16, OpKind.IMMEDIATE32,
                  OpKind.IMMEDIATE64, OpKind.IMMEDIATE8TO16,
                  OpKind.IMMEDIATE8TO32, OpKind.IMMEDIATE8TO64,
                  OpKind.IMMEDIATE32TO64)


def _zero_byte_before(raw, i, reg, entries):
    """A local definition, not imm_of(register)'s zero-on-error fallback.

    Stop at every control/exception entry, call, decode hole or overlapping
    explicit/implicit register write. The zeroing producer stays executable.
    High-byte writes never establish a low-byte fact.
    """
    if reg in _HIGH or RegisterExt.size(reg) != 1:
        return False
    family = RegisterExt.full_register(reg)
    factory = InstructionInfoFactory()
    for k in range(i - 1, max(-1, i - 65), -1):
        w = raw[k]
        if (w.next_ip != raw[k + 1].ip or raw[k + 1].ip in entries
                or w.flow_control != FlowControl.NEXT):
            return False
        if not any(u.access in _WRITES
                   and RegisterExt.full_register(u.register) == family
                   for u in factory.info(w).used_registers()):
            continue
        if (w.op0_kind != OpKind.REGISTER or w.op0_register in _HIGH
                or RegisterExt.full_register(w.op0_register) != family):
            return False
        if (w.mnemonic in (Mnemonic.XOR, Mnemonic.SUB)
                and w.op1_kind == OpKind.REGISTER
                and w.op0_register == w.op1_register):
            return True
        return (w.mnemonic == Mnemonic.MOV and w.op1_kind in _ZERO_IMMS
                and imm_of(w, 1) == 0)
    return False


def metadata_init_guards(raw, init_meta, entry_points=()):
    """Return completely matched bookkeeping IPs, never a partial guard."""
    if not raw or not init_meta:
        return set()
    M = Mnemonic
    skip = set()
    n = len(raw)
    branch_targets = {w.near_branch_target for w in raw
                      if w.flow_control in (FlowControl.CONDITIONAL_BRANCH,
                                            FlowControl.UNCONDITIONAL_BRANCH)
                      and w.op0_kind == OpKind.NEAR_BRANCH64}
    branch_targets.update(entry_points)
    for i, ins in enumerate(raw):
        if not (ins.mnemonic == M.CMP and ins.op0_kind == OpKind.MEMORY
                and ins.memory_base == IReg.RIP and ins.memory_size == 1):
            continue
        if ins.op1_kind == OpKind.IMMEDIATE8:
            if imm_of(ins, 1) != 0:
                continue
        elif ins.op1_kind == OpKind.REGISTER:
            if not _zero_byte_before(raw, i, ins.op1_register, branch_targets):
                continue
        else:
            continue
        slot = ins.ip_rel_memory_address
        j = None
        for k in range(i + 1, min(i + GAP_MAX + 1, n)):
            w = raw[k]
            if raw[k - 1].next_ip != w.ip or w.ip in branch_targets:
                break
            if w.flow_control == FlowControl.CONDITIONAL_BRANCH:
                if w.mnemonic == M.JNE and w.op0_kind == OpKind.NEAR_BRANCH64:
                    j = k
                break
            # Retain these instructions. Only the flag dependency matters:
            # ADDSS and SHUFPS do not touch EFLAGS, but ADC/CMOV/SETcc do.
            if w.flow_control != FlowControl.NEXT or w.rflags_read or w.rflags_modified:
                break
        if j is None:
            continue
        target = raw[j].near_branch_target
        if target <= raw[j].next_ip:
            continue
        owned = {ins.ip, raw[j].ip}
        pending = None
        saw_init = False
        found = False
        for k in range(j + 1, min(j + BODY_MAX + 1, n)):
            w = raw[k]
            if (raw[k - 1].next_ip != w.ip or w.ip >= target
                    or w.ip in branch_targets):
                break
            if _flag(w, slot, 1):
                found = saw_init and pending is None and w.next_ip == target
                if found:
                    owned.add(w.ip)
                break
            if w.mnemonic == M.CALL:
                # No managed/user call may become unconditional when the
                # flag branch is removed. Each init owns its RIP-relative arg.
                if (w.op0_kind != OpKind.NEAR_BRANCH64
                        or w.near_branch_target != init_meta or pending is None):
                    break
                owned.update((pending, w.ip))
                pending = None
                saw_init = True
                continue
            if is_init_barrier(w):
                if not saw_init:
                    break
                owned.add(w.ip)
                continue
            if w.flow_control != FlowControl.NEXT:
                break
            if (w.mnemonic == M.LEA and w.op0_kind == OpKind.REGISTER
                    and w.op0_register == IReg.RCX and w.memory_base == IReg.RIP):
                if pending is not None:
                    break
                pending = w.ip
                continue
            # Retaining an instruction is not enough: removing its branch
            # would make a conditional source spill/register write unconditional.
            # Only owned bookkeeping and NOPs may inhabit a flattened body.
            # Prologue/SIMD movement in the pre-JNE gap is still retained.
            if w.mnemonic != M.NOP:
                break
        if found:
            skip.update(owned)
    return skip
