"""Closed native proof for a uint32 xor/multiply fold over string code units.

This is deliberately NOT a method-name or FNV-constant recognizer. Every
reachable instruction (including ABI saves/restores and every branch target)
must match the supported Win64 lowering. The seed and multiplier come from
instructions; unknown callees, extra effects, EH and other lowerings decline.
General machine-integer/phi provenance is still handled by the ordinary path.
"""
import re
import struct

from iced_x86 import Code, MemorySizeExt, Mnemonic, OpKind, Register, RegisterExt

from il2cpp.binary import PE
from il2cpp.names import ident_name
from il2cpp.text import imm_of


_NONVOLATILE = frozenset((Register.RBX, Register.RBP, Register.RSI, Register.RDI,
                          Register.R12, Register.R13, Register.R14, Register.R15))
_HOME_SLOTS = (8, 16, 24, 32)


def _primitive(ty, kind):
    return (isinstance(ty, tuple) and len(ty) == 2
            and (ty[1] >> 16) & 255 == kind and not (ty[1] >> 29) & 1)


def _rr(ins, mnemonic, dst, src):
    return (ins.mnemonic == mnemonic and ins.op_count == 2
            and ins.op0_kind == ins.op1_kind == OpKind.REGISTER
            and ins.op0_register == dst and ins.op1_register == src)


def _memory(ins, base, displacement, width):
    return (ins.memory_base == base and ins.memory_index == Register.NONE
            and ins.memory_displacement == displacement
            and ins.memory_index_scale == 1
            and MemorySizeExt.size(ins.memory_size) == width)


def _move_home(ins, reg, displacement, *, load=False):
    memory_op, reg_op = (1, 0) if load else (0, 1)
    return (ins.mnemonic == Mnemonic.MOV and ins.op_count == 2
            and ins.op_kind(memory_op) == OpKind.MEMORY
            and ins.op_kind(reg_op) == OpKind.REGISTER
            and ins.op_register(reg_op) == reg
            and _memory(ins, Register.RSP, displacement, 8))


def _branch(ins, mnemonic, target):
    return (ins.mnemonic == mnemonic and ins.op_count == 1
            and ins.op0_kind == OpKind.NEAR_BRANCH64
            and ins.near_branch_target == target)


def _getter_is_string_char(il, target, string_type):
    # A singleton ordinary MethodDef is required. An address consensus is
    # insufficient to prove the accessor's managed identity.
    candidates = il.addr_candidates.get(target)
    if not candidates or len(candidates) != 1:
        return False
    kind, mi = candidates[0]
    if kind != 'method' or mi < 0:
        return False
    method = il.meta.methods[mi]
    if not 0 <= method.declaring < len(il.meta.typedefs):
        return False
    owner = il.meta.typedefs[method.declaring]
    ps = il.meta.method_params(method)
    return (string_type[0] == method.declaring
            and method.addr == target and method.name == 'get_Chars'
            and not method.is_static and method.generic_container == -1
            and method.param_count == len(ps) == 1
            and owner.name == 'String' and owner.namespace == 'System'
            and owner.declaring == owner.generic_container == -1
            and 0 <= method.image < len(il.meta.images)
            and il.meta.images[method.image].name in
            ('mscorlib.dll', 'System.Private.CoreLib.dll')
            and _primitive(il.types[method.return_type], 0x03)
            and _primitive(il.types[ps[0].type], 0x08))


def lift_u32_string_fold(il, method, td, insns, skip=(), eh=None):
    """Return a complete body only after a closed instruction/metadata proof.

    The emitted uint arithmetic is explicitly unchecked: IMUL keeps the low
    32 bits regardless of signedness or the C# project's overflow setting.
    The index remains signed and the getter runs once per native iteration.
    """
    if len(insns) != 28 or skip or eh:
        return None
    # This grammar includes Win64 shadow/home slots, not the SysV ABI.
    binary = il.bin
    if not isinstance(binary, PE) or not binary.is64:
        return None
    try:
        pe = struct.unpack_from('<I', binary.d, 0x3c)[0]
        if (binary.d[pe:pe + 4] != b'PE\0\0'
                or struct.unpack_from('<H', binary.d, pe + 4)[0] != 0x8664):
            return None
        ps = il.meta.method_params(method)
        if (not method.is_static or method.generic_container != -1
                or td.generic_container != -1
                or method.param_count != 1 or len(ps) != 1
                or not _primitive(il.types[method.return_type], 0x09)
                or not _primitive(il.types[ps[0].type], 0x0e)):
            return None
        parameter = ident_name(ps[0].name)
        if not re.fullmatch(r'[A-Za-z_][A-Za-z_0-9]*', parameter):
            return None
        # Complete, contiguous, prefix-free instruction stream. No skipped
        # guards, cold islands, inserted stores or alternate entry are erased.
        if insns[0].ip != method.addr:
            return None
        for pos, ins in enumerate(insns):
            if (ins.has_lock_prefix or ins.has_rep_prefix or ins.has_repne_prefix
                    or ins.has_segment_prefix
                    or pos and insns[pos - 1].next_ip != ins.ip):
                return None
        i = insns
        index64, recv64, accum32 = (i[0].op1_register, i[1].op0_register,
                                    i[9].op0_register)
        accum64 = RegisterExt.full_register(accum32)
        if (index64 not in _NONVOLATILE or recv64 not in _NONVOLATILE
                or accum64 not in _NONVOLATILE
                or len({index64, recv64, accum64}) != 3
                or not RegisterExt.is_gpr32(accum32)):
            return None
        index32 = RegisterExt.full_register32(index64)
        frame, index_home, accum_home = (imm_of(i[2]),
                                        i[0].memory_displacement,
                                        i[8].memory_displacement)
        # One push aligns RSP for the call. Saved values must be separate
        # caller-owned homes, outside the nested call's shadow space.
        if (not 0x20 <= frame <= 0x100 or frame % 16
                or index_home not in _HOME_SLOTS
                or accum_home - frame - 8 not in _HOME_SLOTS
                or accum_home - frame - 8 == index_home):
            return None
        if not (_move_home(i[0], index64, index_home)
                and i[1].code == Code.PUSH_R64 and i[1].op0_register == recv64
                and i[2].code in (Code.SUB_RM64_IMM8, Code.SUB_RM64_IMM32)
                and i[2].op0_register == Register.RSP
                and _rr(i[3], Mnemonic.XOR, index32, index32)
                and _rr(i[4], Mnemonic.MOV, recv64, Register.RCX)
                and _rr(i[5], Mnemonic.MOV, Register.EAX, index32)
                and _rr(i[6], Mnemonic.TEST, Register.RCX, Register.RCX)
                and _branch(i[7], Mnemonic.JE, i[24].ip)
                and _move_home(i[8], accum64, accum_home)
                and i[9].code == Code.MOV_R32_IMM32
                and i[9].op0_register == accum32
                and i[10].code == Code.CMP_R32_RM32
                and i[10].op0_register == Register.EAX
                and i[10].op1_kind == OpKind.MEMORY
                and _memory(i[10], recv64, 0x10, 4)
                and _branch(i[11], Mnemonic.JGE, i[22].ip)
                and _rr(i[12], Mnemonic.XOR, Register.R8D, Register.R8D)
                and _rr(i[13], Mnemonic.MOV, Register.EDX, index32)
                and _rr(i[14], Mnemonic.MOV, Register.RCX, recv64)
                and i[15].code == Code.CALL_REL32_64
                and _getter_is_string_char(il, i[15].near_branch_target,
                                           il.types[ps[0].type])
                and _rr(i[16], Mnemonic.MOVZX, Register.EAX, Register.AX)
                and _rr(i[17], Mnemonic.XOR, Register.EAX, accum32)
                and i[18].code in (Code.IMUL_R32_RM32_IMM32,
                                   Code.IMUL_R32_RM32_IMM8)
                and i[18].op0_register == accum32
                and i[18].op1_kind == OpKind.REGISTER
                and i[18].op1_register == Register.EAX
                and i[19].code == Code.INC_RM32
                and i[19].op0_kind == OpKind.REGISTER
                and i[19].op0_register == index32
                and _rr(i[20], Mnemonic.MOV, Register.EAX, index32)
                and _branch(i[21], Mnemonic.JMP, i[10].ip)
                and _rr(i[22], Mnemonic.MOV, Register.EAX, accum32)
                and _move_home(i[23], accum64, accum_home, load=True)
                and _move_home(i[24], index64, index_home + frame + 8, load=True)
                and i[25].code in (Code.ADD_RM64_IMM8, Code.ADD_RM64_IMM32)
                and i[25].op0_register == Register.RSP and imm_of(i[25]) == frame
                and i[26].code == Code.POP_R64 and i[26].op0_register == recv64
                and i[27].code == Code.RETNQ):
            return None
        seed = imm_of(i[9]) & 0xffffffff
        multiplier = imm_of(i[18], 2) & 0xffffffff
    except (AttributeError, IndexError, KeyError, TypeError, ValueError, struct.error):
        # Incomplete metadata/native evidence stays on the ordinary path.
        return None

    used = {parameter}

    def fresh(base):
        name = base
        while name in used:
            name += '_'
        used.add(name)
        return name

    accumulator, index = fresh('hash'), fresh('index')
    return [f'if ({parameter} == null)', '{', '    return 0u;', '}',
            f'uint {accumulator} = {seed}u;',
            f'for (int {index} = 0; {index} < {parameter}.Length; {index}++)',
            '{', f'    {accumulator} = unchecked(({accumulator} ^ '
            f'{parameter}[{index}]) * {multiplier}u);', '}',
            f'return {accumulator};']
