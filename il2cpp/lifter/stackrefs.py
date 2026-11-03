"""Consumer-only class-reference casts with an independent Win64 home proof."""
from il2cpp.prelude import *  # noqa: F401,F403
from il2cpp.lifter.abi import is_win64_pe
from il2cpp.runtime.meta import IMM_OPS


def _plain_method(il, call):
    if call.mnemonic != Mnemonic.CALL or call.op_count != 1 \
            or call.op0_kind != OpKind.NEAR_BRANCH64:
        return None
    target = call.near_branch_target
    candidates = tuple(il.addr_candidates.get(target, ()))
    if len(candidates) != 1 or candidates[0][0] != 'method':
        return None
    mi = candidates[0][1]
    if not 0 <= mi < len(il.meta.methods):
        return None
    method = il.meta.methods[mi]
    if method.index != mi or method.addr != target or method.generic_container != -1 \
            or not 0 <= method.declaring < len(il.meta.typedefs) \
            or not 0 <= method.return_type < len(il.types):
        return None
    td = il.meta.typedefs[method.declaring]
    if td.generic_container != -1 or td.declaring != -1 or td.is_valuetype:
        return None
    return method


def _reference_home_origin(il, block, call, offset, ty):
    """Prove a full-width store from an exact class-returning native CALL.

    After the store, no call/alias write may affect its home. Before the store,
    follow full-width GPR copies; only ordinary metadata calls may be crossed
    while the source lives in a Win64 preserved register. No statement, value
    identity or stack-local type is changed by this proof.
    """
    from iced_x86 import RegisterExt
    preserved = (IReg.RBX, IReg.RBP, IReg.RSI, IReg.RDI,
                 IReg.R12, IReg.R13, IReg.R14, IReg.R15)
    following = call.ip
    source = None
    for ins in reversed([x for x in block.insns if x.ip < call.ip][-128:]):
        if ins.next_ip != following or ins.segment_prefix != IReg.NONE:
            return False
        following = ins.ip
        if ins.mnemonic == Mnemonic.CALL:
            if source is None:
                return False  # a callee may write its incoming stack homes
            method = _plain_method(il, ins)
            if method is None:
                return False
            if source in preserved:
                continue
            return source == IReg.RAX and il.types[method.return_type] == ty
        if ins.mnemonic == Mnemonic.XOR and ins.op_count == 2 \
                and ins.op0_kind == ins.op1_kind == OpKind.REGISTER \
                and ins.op0_register == ins.op1_register \
                and RegisterExt.is_gpr(ins.op0_register):
            dest = RegisterExt.full_register(ins.op0_register)
            if dest == IReg.RSP or dest == source:
                return False
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
                if RegisterExt.size(dest) != 8 or ins.op1_kind != OpKind.REGISTER \
                        or RegisterExt.size(ins.op1_register) != 8:
                    return False
                source = RegisterExt.full_register(ins.op1_register)
            continue
        if ins.mnemonic != Mnemonic.MOV or ins.op0_kind != OpKind.MEMORY \
                or ins.memory_base != IReg.RSP or ins.memory_index != IReg.NONE:
            return False
        if ins.op1_kind == OpKind.REGISTER:
            if not RegisterExt.is_gpr(ins.op1_register):
                return False
        elif ins.op1_kind not in IMM_OPS:
            return False
        width = MemorySizeExt.size(ins.memory_size)
        if width not in (1, 2, 4, 8):
            return False
        disp = ins.memory_displacement
        if source is None and disp < offset + 8 and offset < disp + width:
            if disp != offset or width != 8 or ins.op1_kind != OpKind.REGISTER \
                    or RegisterExt.size(ins.op1_register) != 8:
                return False
            source = RegisterExt.full_register(ins.op1_register)
    return False


def recover_stack_references(lift, method, rty, args):
    """Cast only a bare outgoing home proved to contain the exact class type.

    This never repeats/captures a call, inserts statements, renames a home or
    changes slot types/type hints. Generics, byrefs, aggregates, tails, ambiguous
    methods, unsupported ABIs and unproved reaching definitions stay untouched.
    """
    if not HAVE_ICED or len(args) <= 4:
        return args
    try:
        il = lift.il
        if not is_win64_pe(il.bin):
            return args
        block = getattr(getattr(lift, 'out', None), 'block', None)
        if block is None:
            return args
        call = next((x for x in block.insns if x.ip == lift._cur_ip), None)
        if call is None or call.segment_prefix != IReg.NONE or _plain_method(il, call) is not method:
            return args
        if rty != il.types[method.return_type] or rty[1] & (1 << 29) \
                or il._type_enum(rty) not in tuple(range(1, 0x0f)) + (0x12, 0x1c, 0x1d):
            return args
        params = il.meta.method_params(method)
        if len(params) != method.param_count:
            return args
        out = args
        base = 0 if method.is_static else 1
        for pi, param in enumerate(params):
            pos = base + pi
            if pos < 4 or pos >= len(args) or not 0 <= param.type < len(il.types):
                continue
            pt = il.types[param.type]
            if il._type_enum(pt) != 0x12 or pt[1] & (1 << 29) \
                    or not 0 <= pt[0] < len(il.meta.typedefs) \
                    or il._closed_type_key(pt) is None:
                continue
            td = il.meta.typedefs[pt[0]]
            if td.generic_container != -1 or td.declaring != -1 or td.is_valuetype:
                continue
            offset = 0x20 + 8 * (pos - 4)
            name = lift.stack_map.get(lift.rsp_delta + offset)
            expr = lift.stack_values.get(name)
            if not name or not re.fullmatch(r's_[0-9a-f]+', name) or args[pos] != name \
                    or expr is None or expr._unk or expr.kind != 'obj' or expr.ty != pt:
                continue
            if _reference_home_origin(il, block, call, offset, pt):
                if out is args:
                    out = list(args)
                out[pos] = '((%s)%s)' % (il.type_name(pt), name)
        return out
    except (AttributeError, IndexError, KeyError, TypeError, ValueError, OverflowError, struct.error):
        return args
