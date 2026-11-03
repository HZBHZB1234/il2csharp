"""Narrow Win64 stack scalar recovery with a same-block native write proof."""
from il2cpp.prelude import *  # noqa: F401,F403
from il2cpp.lifter.abi import is_win64_pe
from il2cpp.runtime.meta import IMM_OPS
from il2cpp.text import _int_lit


def _immediate_home_write(block, call, offset, width, value):
    """Last write must be an exact immediate store, with no alias/call barrier."""
    from iced_x86 import RegisterExt
    following = call.ip
    for ins in reversed([x for x in block.insns if x.ip < call.ip]):
        if ins.next_ip != following or ins.segment_prefix != IReg.NONE:
            return False
        following = ins.ip
        if ins.mnemonic == Mnemonic.MOV and ins.op_count == 2:
            if ins.op0_kind == OpKind.REGISTER:
                reg = ins.op0_register
                if not RegisterExt.is_gpr(reg) or RegisterExt.full_register(reg) == IReg.RSP:
                    return False
                if ins.op1_kind == OpKind.REGISTER:
                    if not RegisterExt.is_gpr(ins.op1_register):
                        return False
                elif ins.op1_kind != OpKind.MEMORY and ins.op1_kind not in IMM_OPS:
                    return False
                continue
            if ins.op0_kind != OpKind.MEMORY or ins.memory_base != IReg.RSP \
                    or ins.memory_index != IReg.NONE:
                return False
            size = MemorySizeExt.size(ins.memory_size)
            disp = ins.memory_displacement
            if size not in (1, 2, 4, 8):
                return False
            if disp < offset + width and offset < disp + size:
                return disp == offset and size == width and ins.op1_kind in IMM_OPS \
                    and ins.immediate(1) == (value & ((1 << (8 * width)) - 1))
            continue
        if ins.mnemonic == Mnemonic.LEA and ins.op_count == 2 \
                and ins.op0_kind == OpKind.REGISTER and ins.op1_kind == OpKind.MEMORY \
                and RegisterExt.is_gpr(ins.op0_register) \
                and RegisterExt.full_register(ins.op0_register) != IReg.RSP:
            continue
        return False
    return False



def _zero_register_bool_home(il, block, call, offset):
    """Prove one false byte home from a same-block full-register self-XOR.

    No copies, partial zeros or cross-block facts. Before the byte store only
    Win64 preserved registers may carry zero across canonical managed calls;
    after the store every call is a barrier (it can write incoming homes).
    """
    from iced_x86 import RegisterExt
    from il2cpp.lifter.stackrefs import _plain_method
    if call.segment_prefix != IReg.NONE:
        return False
    preserved = (IReg.RBX, IReg.RBP, IReg.RSI, IReg.RDI,
                 IReg.R12, IReg.R13, IReg.R14, IReg.R15)
    source = None
    following = call.ip
    for ins in reversed([x for x in block.insns if x.ip < call.ip][-512:]):
        if ins.next_ip != following or ins.segment_prefix != IReg.NONE:
            return False
        following = ins.ip
        if ins.mnemonic == Mnemonic.CALL:
            if source not in preserved or _plain_method(il, ins) is None:
                return False
            continue
        if ins.mnemonic == Mnemonic.XOR and ins.op_count == 2 \
                and ins.op0_kind == ins.op1_kind == OpKind.REGISTER \
                and ins.op0_register == ins.op1_register \
                and RegisterExt.is_gpr(ins.op0_register):
            dest = RegisterExt.full_register(ins.op0_register)
            if dest == IReg.RSP:
                return False
            if dest == source:
                return RegisterExt.size(ins.op0_register) in (4, 8)
            continue
        if ins.mnemonic not in (Mnemonic.MOV, Mnemonic.LEA) or ins.op_count != 2:
            return False
        if ins.op0_kind == OpKind.REGISTER:
            dest = ins.op0_register
            if not RegisterExt.is_gpr(dest) or RegisterExt.full_register(dest) == IReg.RSP:
                return False
            if ins.mnemonic == Mnemonic.LEA:
                if ins.op1_kind != OpKind.MEMORY or RegisterExt.full_register(dest) == source:
                    return False
                continue
            if ins.op1_kind == OpKind.REGISTER:
                if not RegisterExt.is_gpr(ins.op1_register):
                    return False
            elif ins.op1_kind != OpKind.MEMORY and ins.op1_kind not in IMM_OPS:
                return False
            if RegisterExt.full_register(dest) == source:
                return False
            continue
        if ins.mnemonic != Mnemonic.MOV or ins.op0_kind != OpKind.MEMORY \
                or ins.memory_base != IReg.RSP or ins.memory_index != IReg.NONE:
            return False
        size = MemorySizeExt.size(ins.memory_size)
        disp = ins.memory_displacement
        if size not in (1, 2, 4, 8):
            return False
        if ins.op1_kind == OpKind.REGISTER:
            if not RegisterExt.is_gpr(ins.op1_register):
                return False
        elif ins.op1_kind not in IMM_OPS:
            return False
        if source is None and disp < offset + 1 and offset < disp + size:
            if disp != offset or size != 1 or ins.op1_kind != OpKind.REGISTER \
                    or RegisterExt.size(ins.op1_register) != 1:
                return False
            source = RegisterExt.full_register(ins.op1_register)
    return False


def _int32_enum(il, ty):
    if il._type_enum(ty) != 0x11 or ty[1] & (1 << 29) \
            or not 0 <= ty[0] < len(il.meta.typedefs):
        return None
    td = il.meta.typedefs[ty[0]]
    if not td.is_enum or not td.is_valuetype or td.generic_container != -1 or td.declaring != -1 \
            or il._closed_type_key(ty) is None:
        return None
    fields = [il.meta.fields[i] for i in il.meta.type_fields(td)]
    underlying = [il.types[f.type] for f in fields if f.name == 'value__'
                  and 0 <= f.type < len(il.types)]
    if len(underlying) != 1 or il._type_enum(underlying[0]) != 0x08 \
            or underlying[0][1] & (1 << 29):
        return None
    if td.element != -1 and (not 0 <= td.element < len(il.types) \
            or il._type_enum(il.types[td.element]) != 0x08 \
            or il.types[td.element][1] & (1 << 29)):
        return None
    return il.enum_members(ty[0])


def recover_stack_scalars(lift, method, rty, args):
    """Render only literal bool/int32-enum homes proved at a unique direct call.

    This does not type a stack local or infer a value from the signature. Sret,
    generic targets, tails, unknown values and mixed/partial homes stay raw.
    Register stores need a separate exact false-byte origin proof; no true or
    enum value is inferred from a register or from the consumer signature.
    """
    if not HAVE_ICED or len(args) <= 4:
        return args
    try:
        il = lift.il
        if not is_win64_pe(il.bin):
            return args
        if method.generic_container != -1 or not 0 <= method.declaring < len(il.meta.typedefs):
            return args
        owner = il.meta.typedefs[method.declaring]
        if owner.generic_container != -1 or owner.declaring != -1 or owner.is_valuetype:
            return args
        if not 0 <= method.return_type < len(il.types) or rty != il.types[method.return_type] \
                or rty[1] & (1 << 29) or il._type_enum(rty) not in \
                tuple(range(1, 0x0f)) + (0x12, 0x1c, 0x1d):
            return args
        block = getattr(getattr(lift, 'out', None), 'block', None)
        if block is None:
            return args
        call = next((x for x in block.insns if x.ip == lift._cur_ip), None)
        if call is None or call.mnemonic != Mnemonic.CALL or call.op_count != 1 \
                or call.op0_kind != OpKind.NEAR_BRANCH64 or method.addr != call.near_branch_target \
                or tuple(il.addr_candidates.get(method.addr, ())) != (('method', method.index),) \
                or not 0 <= method.index < len(il.meta.methods) \
                or il.meta.methods[method.index] is not method:
            return args
        params = il.meta.method_params(method)
        if len(params) != method.param_count:
            return args
        base = 0 if method.is_static else 1
        out = args
        for pi, param in enumerate(params):
            pos = base + pi
            if pos < 4 or pos >= len(args) or not 0 <= param.type < len(il.types):
                continue
            pt = il.types[param.type]
            if pt[1] & (1 << 29):
                continue
            te = il._type_enum(pt)
            if te not in (0x02, 0x11):
                continue
            value = _int_lit(args[pos])
            if value is None:
                continue
            offset = 0x20 + 8 * (pos - 4)
            name = lift.stack_map.get(lift.rsp_delta + offset)
            expr = lift.stack_values.get(name)
            if expr is None or expr._unk or expr.kind != 'int' or expr.text != args[pos]:
                continue
            if te == 0x02:
                if value not in (0, 1):
                    continue
                width = 1
                text = 'true' if value else 'false'
            else:
                if not -(1 << 31) <= value < (1 << 31):
                    continue
                members = _int32_enum(il, pt)
                if not members or value not in members:
                    continue
                width = 4
                text = '%s.%s' % (il.type_name(pt), members[value])
            if _immediate_home_write(block, call, offset, width, value) or (
                    te == 0x02 and value == 0
                    and _zero_register_bool_home(il, block, call, offset)):
                if out is args:
                    out = list(args)
                out[pos] = text
        return out
    except (AttributeError, IndexError, KeyError, TypeError, ValueError, OverflowError, struct.error):
        return args
