"""Decline-by-default recovery of exact leaf returns through copy constructors.

A scalar-looking field load is not a value of a different struct type. Nor
may an object initializer write private/readonly fields or invent constructor
side effects. Only a native-proved, accessible, single-field copy ctor can
supply the missing managed wrapper here.
"""
from il2cpp.prelude import *  # noqa: F401,F403

from il2cpp.csharp import FA_LITERAL, FA_STATIC, field_attrs
from il2cpp.lifter.abi import is_win64_pe


def _closed_owner(il, index):
    seen = set()
    while 0 <= index < len(il.meta.typedefs) and index not in seen and len(seen) < 16:
        seen.add(index)
        td = il.meta.typedefs[index]
        if td.generic_container != -1:
            return False
        if td.declaring == -1:
            return True
        if not 0 <= td.declaring < len(il.types):
            return False
        outer = il.types[td.declaring]
        if il._type_enum(outer) not in (0x11, 0x12) or outer[1] & (1 << 29):
            return False
        index = outer[0]
    return False


def _methods(il, td):
    start, count = td.method_start, td.method_count
    if start < 0 or count < 0 or start + count > len(il.meta.methods):
        return None
    return il.meta.methods[start:start + count]


def _copy_constructor(il, td_index, field_ty, width):
    td = il.meta.typedefs[td_index]
    methods = _methods(il, td)
    if methods is None or td.has_cctor or any(m.name == '.cctor' for m in methods):
        return None
    matches = []
    for method in methods:
        if method.name != '.ctor' or method.is_static or method.param_count != 1:
            continue
        if method.generic_container != -1 or method.declaring != td_index \
                or not 0 <= method.index < len(il.meta.methods) \
                or il.meta.methods[method.index] is not method \
                or not 0 <= method.parameter_start < len(il.meta.params):
            return None
        pi = il.meta.params[method.parameter_start].type
        if not 0 <= pi < len(il.types):
            return None
        if il._closed_type_key(il.types[pi]) == il._closed_type_key(field_ty):
            matches.append(method)
    if len(matches) != 1:
        return None
    method = matches[0]
    if method.flags & 7 != 6 or method.flags & 0x1800 != 0x1800 \
            or method.flags & (0x40 | 0x400 | 0x2000 | 0xc000) \
            or method.iflags & 0x1037 or not method.addr \
            or not 0 <= method.return_type < len(il.types):
        return None
    ret_ty = il.types[method.return_type]
    if il._type_enum(ret_ty) != 0x01 or ret_ty[1] & (1 << 29) \
            or ('method', method.index) not in il.addr_candidates.get(method.addr, ()):
        return None
    offset = il.bin.va2off(method.addr)
    if offset is None or not 0 <= offset < len(il.bin.d):
        return None
    instructions = iter(Decoder(64, il.bin.d[offset:offset + 16], ip=method.addr))
    store, ret = next(instructions), next(instructions)
    if store.mnemonic != Mnemonic.MOV or store.op_count != 2 \
            or store.op0_kind != OpKind.MEMORY or store.op1_kind != OpKind.REGISTER \
            or store.memory_base != IReg.RCX or store.memory_index != IReg.NONE \
            or store.memory_displacement != 0 or store.segment_prefix != IReg.NONE \
            or store.has_rep_prefix or store.has_repne_prefix \
            or MemorySizeExt.size(store.memory_size) != width \
            or store.op1_register != (IReg.EDX if width == 4 else IReg.RDX):
        return None
    if ret.mnemonic != Mnemonic.RET or ret.op_count != 0 \
            or ret.segment_prefix != IReg.NONE or ret.has_rep_prefix or ret.has_repne_prefix:
        return None
    # The target is the exact owned MethodDef, not a guessed callee picked
    # from its possibly shared address. Its two native instructions prove
    # the semantics independently of every other sharer.
    return method


def recover_leaf_struct_return(lift, text, return_ty):
    """Name a 4/8-byte wrapper only at an exact two-instruction return.

    No register use is counted and no Expr, hint, statement or type is changed.
    All decline paths leave the existing return rendering intact.
    """
    if not HAVE_ICED:
        return None
    try:
        # Most return sites are scalars, references or larger method bodies.
        # Reject those before ABI, metadata traversal or native decoding.
        if not isinstance(return_ty, tuple) or len(return_ty) != 2 \
                or (return_ty[1] >> 16) & 0xff != 0x11 \
                or return_ty[1] & (1 << 29):
            return None
        il = lift.il
        block = lift.out.block
        if len(block.insns) != 2 or block.bid != 0 or block.preds:
            return None
        method = lift._current_method
        if not is_win64_pe(il.bin) or method.is_static or method.param_count != 0 \
                or method.generic_container != -1 or not method.addr \
                or not 0 <= method.index < len(il.meta.methods) \
                or il.meta.methods[method.index] is not method \
                or not 0 <= method.return_type < len(il.types) \
                or not _closed_owner(il, method.declaring):
            return None
        owner = il.meta.typedefs[method.declaring]
        if not owner.is_valuetype or owner.is_enum or not 0 <= owner.byval < len(il.types):
            return None
        owner_ty = il.types[owner.byval]
        if il._type_enum(owner_ty) != 0x11 or owner_ty[0] != method.declaring \
                or not lift._piece_layout_proven(owner_ty):
            return None
        if return_ty is None or il._type_enum(return_ty) != 0x11 \
                or return_ty[1] & (1 << 29) \
                or not 0 <= return_ty[0] < len(il.meta.typedefs) \
                or il._closed_type_key(return_ty) is None \
                or il._closed_type_key(return_ty) != il._closed_type_key(il.types[method.return_type]) \
                or not _closed_owner(il, return_ty[0]):
            return None
        td = il.meta.typedefs[return_ty[0]]
        if not td.is_valuetype or td.is_enum or not lift._piece_layout_proven(return_ty):
            return None
        if td.field_start < 0 or td.field_count < 0 \
                or td.field_start + td.field_count > len(il.meta.fields):
            return None
        fields = [f for f in il.meta.fields[td.field_start:td.field_start + td.field_count]
                  if not field_attrs(il, f) & (FA_STATIC | FA_LITERAL)]
        chain = il.instance_field_chain(return_ty[0]) or {}
        if len(fields) != 1 or len(chain) != 1 or 0x10 not in chain \
                or chain[0x10][1] != fields[0].type \
                or not 0 <= fields[0].type < len(il.types):
            return None
        field_ty = il.types[fields[0].type]
        width = il._sf_field_size(return_ty, 0)
        # A scalar float ctor argument is in XMM1, not RDX. Struct arguments
        # of the same width use a GPR, even if their fields include floats.
        if width not in (4, 8) or il._sf_field_size(field_ty, 0) != width \
                or il._type_enum(field_ty) not in (0x08, 0x09, 0x0a, 0x0b, 0x11) \
                or field_ty[1] & (1 << 29) or il._closed_type_key(field_ty) is None \
                or not lift._piece_layout_proven(field_ty):
            return None
        load, ret = block.insns
        if load.ip != method.addr or load.next_ip != ret.ip or ret.ip != lift._cur_ip \
                or ret.mnemonic != Mnemonic.RET or ret.op_count != 0 \
                or ret.segment_prefix != IReg.NONE or ret.has_rep_prefix or ret.has_repne_prefix:
            return None
        if load.mnemonic != Mnemonic.MOV or load.op_count != 2 \
                or load.op0_kind != OpKind.REGISTER or load.op1_kind != OpKind.MEMORY \
                or load.op0_register != (IReg.EAX if width == 4 else IReg.RAX) \
                or load.memory_base != IReg.RCX or load.memory_index != IReg.NONE \
                or load.segment_prefix != IReg.NONE or load.has_rep_prefix or load.has_repne_prefix \
                or MemorySizeExt.size(load.memory_size) != width:
            return None
        source = (il.instance_field_chain(method.declaring) or {}).get(
            0x10 + load.memory_displacement)
        if source is None or not 0 <= source[1] < len(il.types) \
                or il.types[source[1]] != field_ty or text != 'this.' + source[0]:
            return None
        value = dict.get(lift.regs, 'RAX')
        if value is None or value._unk or value.ty != field_ty or value.text != text:
            return None
        constructor = _copy_constructor(il, return_ty[0], field_ty, width)
        if constructor is None or constructor.image != method.image:
            return None
        return 'new ' + il.type_name(return_ty) + '(' + text + ')'
    except (AttributeError, IndexError, KeyError, TypeError, ValueError, OverflowError, StopIteration):
        return None
