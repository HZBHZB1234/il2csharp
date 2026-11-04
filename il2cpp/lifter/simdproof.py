"""Same-block proof for legacy MOVD Int32-field -> CVTDQ2PS recovery."""
import re

from il2cpp.prelude import *  # noqa: F401,F403
from il2cpp.text import reg_name, sdisp


def _int32(ty):
    # Metadata data/attribute bits differ between fields and synthetic types.
    return (isinstance(ty, tuple) and len(ty) == 2
            and (ty[1] >> 16) & 0xff == 8 and not ty[1] & (1 << 29))


def movd_int32_field(lift, ins, insns, value):
    """Prove all 128 source bits without changing the MOVD Expr's identity.

    Only a plain Int32 reference-instance field, a contiguous same-block
    legacy MOVD last writer, and no intervening memory/base writes qualify.
    A GPR source also needs an exact four-byte field-load last writer and
    the unchanged receiver-field expression. Other register inputs, aliases,
    partial writes, calls and flat fallback decline. Text is never used to
    guess an unknown scalar type.
    """
    from iced_x86 import InstructionInfoFactory, OpAccess, RegisterExt

    if (value is None or not _int32(value.ty) or value.kind != 'int'
            or value._unk or value._no_bind
            or any(getattr(value, key, None) is not None
                   for key in ('_slice', '_parts', '_bytes', '_stack_offset'))):
        return False
    block = getattr(lift.out, 'block', None)
    if (block is None or insns is not block.insns
            or ins.mnemonic != Mnemonic.CVTDQ2PS
            or ins.op0_kind != OpKind.REGISTER or ins.op1_kind != OpKind.REGISTER
            or not RegisterExt.is_xmm(ins.op0_register)
            or not RegisterExt.is_xmm(ins.op1_register)):
        return False
    # Structured execution deliberately supplies idx=0 to _insn. Recover
    # the position from the block's actual instruction, never that hint.
    index = next((i for i, native in enumerate(insns)
                  if native.ip == ins.ip and native == ins), None)
    if index is None:
        return False
    source = RegisterExt.full_register(ins.op1_register)
    gpr = None
    expected = ins.ip
    written = set()
    factory = InstructionInfoFactory()
    writes = (OpAccess.WRITE, OpAccess.COND_WRITE, OpAccess.READ_WRITE,
              OpAccess.READ_COND_WRITE)
    # Bound work on large/malformed blocks; a missing proof keeps old output.
    for i in range(index - 1, max(-1, index - 513), -1):
        native = insns[i]
        if native.next_ip != expected or native.flow_control != FlowControl.NEXT:
            return False
        expected = native.ip
        info = factory.info(native)
        if any(memory.access in writes for memory in info.used_memory()):
            return False
        regs = {RegisterExt.full_register(reg.register)
                for reg in info.used_registers() if reg.access in writes}
        if gpr is None:
            if source not in regs:
                written.update(regs)
                continue
            if (native.mnemonic != Mnemonic.MOVD
                    or native.op0_kind != OpKind.REGISTER
                    or native.op0_register != ins.op1_register):
                return False
            if native.op1_kind == OpKind.REGISTER:
                if RegisterExt.size(native.op1_register) != 4:
                    return False
                # MOVD captured this GPR before any later writes. Find its
                # last native writer at that point, not the current GPR Expr.
                gpr = RegisterExt.full_register(native.op1_register)
                written.update(regs)
                continue
        else:
            if gpr not in regs:
                written.update(regs)
                continue
            if (native.mnemonic != Mnemonic.MOV
                    or native.op0_kind != OpKind.REGISTER
                    or RegisterExt.size(native.op0_register) != 4
                    or RegisterExt.full_register(native.op0_register) != gpr):
                return False
        if (native.op1_kind != OpKind.MEMORY
                or MemorySizeExt.size(native.memory_size) != 4
                or native.segment_prefix != IReg.NONE
                or native.memory_index != IReg.NONE
                or RegisterExt.size(native.memory_base) != 8
                or native.memory_base in (IReg.RSP, IReg.RBP, IReg.RIP)
                or RegisterExt.full_register(native.memory_base) in written):
            return False
        # Proof probes must not count uses or materialize receiver expressions.
        base = dict.get(lift.regs, reg_name(native.memory_base))
        if (base is None or base.kind != 'obj' or base._unk or base._no_bind
                or any(getattr(base, key, None) is not None
                       for key in ('_slice', '_parts', '_bytes', '_stack_offset'))
                or not isinstance(base.ty, tuple) or len(base.ty) != 2
                or (base.ty[1] >> 16) & 0xff != 0x12
                or base.ty[1] & (1 << 29)
                or re.fullmatch(r'@?[A-Za-z_]\w*', base.text or '') is None):
            return False
        td = lift._td_of(base.ty)
        if td is None or lift.meta.typedefs[td].is_valuetype:
            return False
        field = (lift.il.instance_field_chain(td) or {}).get(
            sdisp(native.memory_displacement))
        return (field is not None and 0 <= field[1] < len(lift.il.types)
                and _int32(lift.il.types[field[1]])
                # Do not cast an inferred/bound object token numerically.
                # The extra GPR path must still denote the proved field.
                and (gpr is None or value.text == base.text + '.' + field[0]))
    return False
