"""Block-local whole values, separate from scalar display and raw byte facts.

A materialized sret temp is a semantic snapshot, not evidence that padding is
initialized. At a typed by-value call consumer, replay a bounded original-native
copy window using byte *identities* (never byte values). Every byte must still
come from the same offset of that snapshot. No Expr, tile, hint or CFG fact is
re-rooted; unsupported effects, aliases and cross-block lifetimes decline.
"""
from dataclasses import dataclass

from il2cpp.prelude import *  # noqa: F401,F403
from il2cpp.lifter.abi import is_win64_pe
from il2cpp.text import reg_name, sdisp
from il2cpp.x64 import _reg_size


_GPRS = frozenset(('RAX', 'RCX', 'RDX', 'RBX', 'RSP', 'RBP', 'RSI', 'RDI')
                  + tuple('R%d' % n for n in range(8, 16)))


def _gpr(reg, width):
    return _reg_size(reg) == width and reg_name(reg) in _GPRS


@dataclass(frozen=True)
class _Snapshot:
    scope: object
    ip: int
    home: int
    rsp: int
    ty: tuple
    text: str
    size: int


def _plain(ins):
    return not (ins.segment_prefix != IReg.NONE or ins.has_rep_prefix
                or ins.has_repne_prefix or ins.has_lock_prefix)


def _method(il, ins):
    if (ins.mnemonic != Mnemonic.CALL or ins.op0_kind != OpKind.NEAR_BRANCH64
            or ins.op_count != 1 or not _plain(ins)):
        return None
    candidates = il.addr_candidates.get(ins.near_branch_target, ())
    if len(candidates) != 1 or candidates[0][0] != 'method':
        return None
    index = candidates[0][1]
    if not 0 <= index < len(il.meta.methods):
        return None
    method = il.meta.methods[index]
    if (method.index != index or method.addr != ins.near_branch_target
            or method.generic_container != -1):
        return None
    # A MethodDef under an open generic owner is not a closed call signature.
    td = method.declaring
    seen = set()
    while 0 <= td < len(il.meta.typedefs) and td not in seen and len(seen) < 16:
        seen.add(td)
        owner = il.meta.typedefs[td]
        if owner.generic_container != -1:
            return None
        if owner.declaring == -1:
            return method
        if not 0 <= owner.declaring < len(il.types):
            return None
        outer = il.types[owner.declaring]
        if il._type_enum(outer) not in (0x11, 0x12) or outer[1] & (1 << 29):
            return None
        td = outer[0]
    return None


def record_materialized_sret(lift, ins, home, ty, text):
    """Called only after the existing sret fold emits its assignment.

    Scope is the execution sink, NOT its Block: dry/real execution, a new
    method, and even a single-predecessor CFG edge all get distinct lifetimes.
    The latest producer suffices; an intervening call rejects an older one.
    """
    try:
        if (not HAVE_ICED or home is None or not is_win64_pe(lift.il.bin)
                or not isinstance(ty, tuple) or lift.il._type_enum(ty) != 0x11
                or ty[1] & (1 << 29) or not lift.il.returns_sret(ty)
                or not text.startswith('t') or not text[1:].isdigit()):
            return
        scope = lift.out
        if ins not in scope.block.insns:
            return
        method = _method(lift.il, ins)
        if method is None or not 0 <= method.return_type < len(lift.il.types):
            return
        key = lift.il._closed_type_key
        if key(ty) is None or key(lift.il.types[method.return_type]) != key(ty):
            return
        size = lift.il._sf_field_size(ty, 0)
        if size is None or not 8 < size <= 64:
            return
        if (lift._var_types.get(text) != ty or lift.slot_types.get(text) != ty
                or not lift._piece_layout_proven(ty)):
            return
        lift._materialized_sret = _Snapshot(scope, ins.ip, home, lift.rsp_delta,
                                            ty, text, size)
    except (AttributeError, IndexError, KeyError, TypeError, ValueError):
        return


def _address(ins, regs):
    if ins.memory_index != IReg.NONE or not _gpr(ins.memory_base, 8):
        return None
    base = regs.get(reg_name(ins.memory_base))
    return base + sdisp(ins.memory_displacement) if isinstance(base, int) else None


def _bits(value, width):
    return (value + (None,) * width)[:width] if isinstance(value, tuple) else (None,) * width


def _copy(ins, regs, memory):
    """Finite native-copy interpreter. Unknown data is not a source byte.

    Unknown-address writes reject, rather than pretending not to alias the
    frame. Other unsupported instructions reject, even if a legacy lifter
    happens to retain its destination. Partial/upper-register merges are not
    inferred. The dictionary denotes source offsets, never concrete bytes.
    """
    if ins.flow_control != FlowControl.NEXT or not _plain(ins):
        return False
    mn = ins.mnemonic
    if mn == Mnemonic.NOP:
        return ins.op_count == 0
    if ins.op_count != 2:
        return False
    if mn == Mnemonic.LEA:
        if (ins.op0_kind != OpKind.REGISTER or not _gpr(ins.op0_register, 8)
                or ins.op1_kind != OpKind.MEMORY):
            return False
        regs[reg_name(ins.op0_register)] = _address(ins, regs)
        return True
    if mn in (Mnemonic.XOR, Mnemonic.XORPS, Mnemonic.XORPD, Mnemonic.PXOR):
        if (ins.op0_kind != OpKind.REGISTER or ins.op1_kind != OpKind.REGISTER
                or ins.op0_register != ins.op1_register):
            return False
        name = reg_name(ins.op0_register)
        if mn == Mnemonic.XOR and not any(_gpr(ins.op0_register, n) for n in (4, 8)):
            return False
        if mn != Mnemonic.XOR and not name.startswith('XMM'):
            return False
        regs[name] = None
        return True
    vector16 = (Mnemonic.MOVUPS, Mnemonic.MOVAPS, Mnemonic.MOVUPD,
                Mnemonic.MOVAPD, Mnemonic.MOVDQU, Mnemonic.MOVDQA)
    scalar = {Mnemonic.MOVSS: 4, Mnemonic.MOVSD: 8,
              Mnemonic.MOVD: 4, Mnemonic.MOVQ: 8}
    if mn not in (Mnemonic.MOV,) + vector16 + tuple(scalar):
        return False
    memory_operand = ins.op0_kind == OpKind.MEMORY or ins.op1_kind == OpKind.MEMORY
    if mn == Mnemonic.MOV:
        n = MemorySizeExt.size(ins.memory_size) if memory_operand else _reg_size(ins.op0_register)
        if n not in (4, 8):
            return False
        for k in range(2):
            if ins.op_kind(k) == OpKind.REGISTER and not _gpr(ins.op_register(k), n):
                return False
    else:
        n = 16 if mn in vector16 else scalar[mn]
        if memory_operand and MemorySizeExt.size(ins.memory_size) != n:
            return False
        # Scalar reg-reg SSE moves preserve lanes; do not model them as
        # whole-register copies. GPR/XMM MOVD/Q moves also decline here.
        if mn in scalar and not memory_operand:
            return False
        for k in range(2):
            if ins.op_kind(k) == OpKind.REGISTER and not reg_name(ins.op_register(k)).startswith('XMM'):
                return False
    if ins.op1_kind == OpKind.MEMORY:
        address = _address(ins, regs)
        value = tuple(memory.get(address + i) for i in range(n)) if address is not None else (None,) * n
    elif ins.op1_kind == OpKind.REGISTER:
        value = regs.get(reg_name(ins.op1_register))
    else:
        # Constants may overwrite copies, but cannot prove source-byte identity.
        from il2cpp.runtime.meta import IMM_OPS
        if ins.op1_kind not in IMM_OPS:
            return False
        value = None
    if ins.op0_kind == OpKind.MEMORY:
        address = _address(ins, regs)
        if address is None:
            return False
        for i, byte in enumerate(_bits(value, n)):
            memory[address + i] = byte
    elif ins.op0_kind == OpKind.REGISTER:
        name = reg_name(ins.op0_register)
        if mn == Mnemonic.MOV and n == 8 and isinstance(value, int):
            regs[name] = value
        else:
            width = 16 if name.startswith('XMM') else 8
            regs[name] = _bits(value, n) + (None,) * (width - n)
    else:
        return False
    return True


def recover_materialized_sret(lift, address, ty):
    """Recover a whole snapshot only at a canonical typed call consumer."""
    try:
        proof = getattr(lift, '_materialized_sret', None)
        if (not HAVE_ICED or proof is None or proof.scope is not lift.out or ty != proof.ty
                or not is_win64_pe(lift.il.bin)):
            return None
        il = lift.il
        block = lift.out.block
        insns = block.insns
        source = next(i for i, ins in enumerate(insns) if ins.ip == proof.ip)
        end = next(i for i, ins in enumerate(insns) if ins.ip == lift._cur_ip)
        if not source < end <= source + 96:
            return None
        producer, consumer = insns[source], insns[end]
        pm, cm = _method(il, producer), _method(il, consumer)
        if pm is None or cm is None or il.types[pm.return_type] != ty:
            return None
        # Independently prove the producer's hidden RCX buffer. A copied or
        # ambiguous setup declines; RSP must stay fixed after this exact LEA.
        seed = None
        for pos in range(source - 1, max(-1, source - 17), -1):
            ins = insns[pos]
            if ins.flow_control != FlowControl.NEXT or not _plain(ins):
                return None
            if ins.op0_kind == OpKind.REGISTER:
                name = reg_name(ins.op0_register)
                if name == 'RSP':
                    return None
                if name == 'RCX':
                    if (ins.mnemonic != Mnemonic.LEA or ins.op0_register != IReg.RCX
                            or ins.op1_kind != OpKind.MEMORY or ins.memory_base != IReg.RSP
                            or ins.memory_index != IReg.NONE
                            or proof.rsp + sdisp(ins.memory_displacement) != proof.home):
                        return None
                    seed = pos
                    break
            # Only the finite interpreter's explicit, nonimplicit effects are
            # admitted before the call as well. A dummy map is sufficient.
            if not _copy(ins, {}, {}):
                return None
        if seed is None:
            return None
        expected = insns[seed:end + 1]
        lo, hi = expected[0].ip, expected[-1].next_ip
        off = il.bin.va2off(lo)
        if off is None or off < 0 or hi - lo > 2048 or off + hi - lo > len(il.bin.d):
            return None
        native = list(Decoder(64, il.bin.d[off:off + hi - lo], ip=lo))
        if native != expected:
            return None
        regs = {'RSP': proof.rsp, 'RAX': proof.home}
        memory = {proof.home + i: i for i in range(proof.size)}
        identity = tuple(range(proof.size))
        for ins in insns[source + 1:end]:
            if not _copy(ins, regs, memory):
                return None
            # The existing managed temp is not a fresh SSA copy. A native
            # write to its home may also mutate that temp in the legacy lifter.
            # Even if a saved register later restores the source, decline as
            # soon as its identity changes; the temp must stay valid throughout.
            if tuple(memory.get(proof.home + i) for i in range(proof.size)) != identity:
                return None
        if regs.get('RSP') != lift.rsp_delta:
            return None
        if tuple(memory.get(address + i) for i in range(proof.size)) != identity:
            return None
        # A rendered &slot is not an ABI argument proof. Match its actual
        # pointer register to a by-value parameter of the exact closed type.
        if not 0 <= cm.return_type < len(il.types):
            return None
        params = il.meta.method_params(cm)
        if len(params) != cm.param_count:
            return None
        ret = il.types[cm.return_type]
        base = int(not cm.is_static) + int(il.returns_sret(ret))
        args = ('RCX', 'RDX', 'R8', 'R9')
        for pi, param in enumerate(params):
            if pi + base >= len(args):
                break
            if (0 <= param.type < len(il.types) and il.types[param.type] == ty
                    and regs.get(args[pi + base]) == address):
                return proof.text
    except (AttributeError, IndexError, KeyError, StopIteration, TypeError, ValueError, OverflowError):
        return None
    return None
