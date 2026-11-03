"""Small native/metadata proof for a constant RuntimeTypeHandle consumer."""
from il2cpp.prelude import *  # noqa: F401,F403


def recover_type_handle_call(il, call, mi, value, block=None):
    """Return typeof(T) only for the exact corelib call and adjacent kind-2 load.

    Il2CppClass* (usage kind 1), slot addresses, arithmetic, spills and phi
    merges do not prove RuntimeTypeHandle. Re-decode the bounded local setup
    independently of symbolic register spelling: stale values surviving an
    unmodelled/truncating instruction must not become stronger evidence.
    """
    proof = getattr(value, '_type_handle', None)
    if not HAVE_ICED or proof is None or value._unk:
        return None
    try:
        start, slot, ty, text = proof
        # Equal-text CFG joins may reuse one predecessor Expr, including its
        # tag. Adjacency in the binary alone does not prove that every path
        # executed the load: require both sites inside THIS executed block.
        window = [ins for ins in block.insns if start <= ins.ip <= call.ip]
        if not window or window[0].ip != start or window[-1] is not call:
            return None
        if value.kind != 'klass' or value.ty != ty or value.text != text:
            return None
        if call.mnemonic != Mnemonic.CALL or call.op_count != 1 \
                or call.op0_kind != OpKind.NEAR_BRANCH64:
            return None
        target = call.near_branch_target
        if mi is None or not 0 <= mi < len(il.meta.methods) \
                or tuple(il.addr_candidates.get(target, ())) != (('method', mi),):
            return None
        method = il.meta.methods[mi]
        if not 0 <= method.declaring < len(il.meta.typedefs):
            return None
        owner = il.meta.typedefs[method.declaring]
        image = il.meta.images[method.image] if method.image >= 0 else None
        if image is None or image.name not in ('mscorlib.dll', 'System.Private.CoreLib.dll') \
                or method.addr != target or method.name != 'GetTypeFromHandle' \
                or not method.is_static or method.generic_container != -1 \
                or owner.namespace != 'System' or owner.name != 'Type' \
                or owner.declaring != -1 or owner.generic_container != -1 \
                or owner.is_valuetype:
            return None
        first, end = image.type_start, image.type_start + image.type_count
        if not first <= method.declaring < end:
            return None
        if not 0 <= method.return_type < len(il.types):
            return None
        rt = il.types[method.return_type]
        params = il.meta.method_params(method)
        if method.param_count != 1 or len(params) != 1 \
                or rt[0] != method.declaring or (rt[1] >> 16) & 0xff != 0x12 \
                or rt[1] & (1 << 29):
            return None
        if not 0 <= params[0].type < len(il.types):
            return None
        pt = il.types[params[0].type]
        if (pt[1] >> 16) & 0xff != 0x11 or pt[1] & (1 << 29) \
                or not first <= pt[0] < end:
            return None
        handle = il.meta.typedefs[pt[0]]
        if handle.namespace != 'System' or handle.name != 'RuntimeTypeHandle' \
                or handle.declaring != -1 or handle.generic_container != -1 \
                or not handle.is_valuetype or handle.is_enum:
            return None
        te = il._type_enum(ty)
        if ty[1] & (1 << 29) or te not in tuple(range(1, 0x0f)) + (0x11, 0x12, 0x1c) \
                or il._closed_type_key(ty) is None:
            return None
        if te in (0x11, 0x12):
            if not 0 <= ty[0] < len(il.meta.typedefs):
                return None
            td = il.meta.typedefs[ty[0]]
            if td.generic_container != -1:
                return None
        usage = il.decode_slot(slot)
        if not usage or usage.get('kind') != 2 or usage.get('type') != ty \
                or usage.get('text') != text or text != 'typeof(%s)' % il.type_name(ty):
            return None
        size = call.ip - start
        if not 7 <= size <= 10:
            return None
        raw = il.bin.read(start, size)
        if raw is None or len(raw) != size:
            return None
        insns = list(Decoder(64, raw, ip=start))
        if len(insns) not in (1, 2) or insns[-1].next_ip != call.ip:
            return None
        load = insns[0]
        if load.mnemonic != Mnemonic.MOV or load.op_count != 2 \
                or load.op0_kind != OpKind.REGISTER or load.op0_register != IReg.RCX \
                or load.op1_kind != OpKind.MEMORY or load.memory_base != IReg.RIP \
                or load.memory_index != IReg.NONE or load.segment_prefix != IReg.NONE \
                or MemorySizeExt.size(load.memory_size) != 8 \
                or load.ip_rel_memory_address != slot:
            return None
        if len(insns) == 2:
            zero = insns[1]
            if zero.mnemonic != Mnemonic.XOR or zero.op_count != 2 \
                    or zero.op0_kind != OpKind.REGISTER or zero.op1_kind != OpKind.REGISTER \
                    or zero.op0_register != IReg.EDX or zero.op1_register != IReg.EDX:
                return None
        return text
    except (AttributeError, IndexError, KeyError, TypeError, ValueError, OverflowError):
        return None
