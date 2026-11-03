"""fix 139: prune the inlined interface-dispatch fast path.

IL2CPP inlines an interface call as a scan of the receiver class's
interface table (`movzx n,word [k+0x12E]`, `mov t,[k+0xB0]`, a
`cmp [t+i*16],iface` loop) whose hit arm computes the VirtualInvokeData
pointer `k + 0x138 + 16*(offset+slot)`, and whose miss arm calls the
resolve helper (`il2cpp_interface_get_method(obj, typeof(I), slot)`).
Both arms join with the same entry in a register and `call [entry]`.

By the runtime contract the helper returns exactly the entry the scan
finds, so forcing the entry test onto the miss arm preserves meaning:
the scan blocks become unreachable and the join sees one definition --
the helper result -- which the lifter renders as a managed interface
call. The rewrite is gated structurally: the scan region is entered only
through the test, exits only to the miss arm or the join, holds the
`0x138` entry fold and a `[k+0xB0]` table load, performs no store /
call / non-GPR write, and every callee-saved register it writes is dead
at the join (volatile ones are undefined after the miss arm's call).
The slot-zero LEA alternative proves the complete four-block scan and
its receiver/class/table/count/offset def-use chain, exact helper arguments,
and a zero starting index. It does not broaden the legacy ADD matcher.
Anything else declines and keeps the honest scan rendering.
"""
from iced_x86 import (InstructionInfoFactory, OpAccess, RegisterExt, Mnemonic,
                      OpKind, FlowControl, MemorySizeExt, Register as IReg)

_VOL = {IReg.RAX, IReg.RCX, IReg.RDX, IReg.R8, IReg.R9, IReg.R10, IReg.R11}
_ARGR = {IReg.RCX, IReg.RDX, IReg.R8, IReg.R9}
_WR = {OpAccess.WRITE, OpAccess.READ_WRITE, OpAccess.COND_WRITE,
       OpAccess.READ_COND_WRITE}
_RD = {OpAccess.READ, OpAccess.READ_WRITE, OpAccess.COND_READ,
       OpAccess.READ_COND_WRITE}
_FAC = InstructionInfoFactory()


def _gpr_writes(ins):
    """Full GPRs written, or None when the instruction is not a pure
    register-only computation (memory store, call, stack, xmm, ...)."""
    if ins.flow_control in (FlowControl.CALL, FlowControl.INDIRECT_CALL,
                            FlowControl.RETURN, FlowControl.INTERRUPT,
                            FlowControl.EXCEPTION, FlowControl.INDIRECT_BRANCH):
        return None
    info = _FAC.info(ins)
    for um in info.used_memory():
        if um.access in _WR:
            return None
    out = set()
    for ur in info.used_registers():
        if ur.access in _WR:
            r = ur.register
            if not RegisterExt.is_gpr(r):
                return None
            f = RegisterExt.full_register(r)
            if f == IReg.RSP:
                return None
            out.add(f)
    return out


def _dead_at(blocks, start, regs, budget=400):
    """True when none of `regs` is read on any path from block `start`
    before being fully overwritten."""
    work = [(start, frozenset(regs))]
    seen = set()
    steps = 0
    while work:
        bid, live = work.pop()
        if (bid, live) in seen:
            continue
        seen.add((bid, live))
        steps += 1
        if steps > budget:
            return False
        b = blocks[bid]
        live = set(live)
        for ins in b.insns:
            if not live:
                break
            fc = ins.flow_control
            info = _FAC.info(ins)
            for ur in info.used_registers():
                if ur.access in _RD and RegisterExt.is_gpr(ur.register) \
                        and RegisterExt.full_register(ur.register) in live:
                    return False
            if fc in (FlowControl.CALL, FlowControl.INDIRECT_CALL):
                if live & _ARGR:
                    return False
                live -= _VOL
                continue
            if fc == FlowControl.RETURN:
                if IReg.RAX in live:
                    return False
                live = set()
                break
            for ur in info.used_registers():
                if ur.access == OpAccess.WRITE and RegisterExt.is_gpr(ur.register) \
                        and RegisterExt.size(ur.register) >= 4:
                    live.discard(RegisterExt.full_register(ur.register))
        if not live:
            continue
        t = b.term[0] if b.term else 'stop'
        if t in ('ret', 'abort'):
            if t == 'ret' and IReg.RAX in live:
                return False
            continue
        if t == 'stop' or not b.succs:
            return False
        for s in b.succs:
            work.append((s, frozenset(live)))
    return True


def _reads_before_write(insns, reg, call_args=_ARGR):
    """True when `reg` (full GPR) is read in `insns` before a full write.
    A call reads `call_args` (default: the Win64 argument registers)."""
    for ins in insns:
        info = _FAC.info(ins)
        for ur in info.used_registers():
            if ur.access in _RD and RegisterExt.is_gpr(ur.register) \
                    and RegisterExt.full_register(ur.register) == reg:
                return True
        if ins.flow_control in (FlowControl.CALL, FlowControl.INDIRECT_CALL):
            return reg in call_args
        for ur in info.used_registers():
            if ur.access == OpAccess.WRITE and RegisterExt.is_gpr(ur.register) \
                    and RegisterExt.size(ur.register) >= 4 \
                    and RegisterExt.full_register(ur.register) == reg:
                return False
    return False


def _dead_count_test(pb, miss_insns):
    """ips of the entry test's interface-count load and compare, once the
    test is forced: `movzx D,word [k+0x12E]` ... `cmp/test ..D..; jcc`,
    when nothing else in the test block after the load and nothing on
    the miss arm before the helper call reads D. Else ()."""
    ins = pb.insns
    if len(ins) < 3 or ins[-2].mnemonic not in (Mnemonic.CMP, Mnemonic.TEST):
        return ()
    cmp = ins[-2]
    for j in range(len(ins) - 3, -1, -1):
        x = ins[j]
        if x.mnemonic == Mnemonic.MOVZX and x.op0_kind == OpKind.REGISTER \
                and x.op1_kind == OpKind.MEMORY and x.memory_displacement == 0x12E:
            d = RegisterExt.full_register(x.op0_register)
            if d == IReg.RSP or d not in _VOL:
                return ()
            if _reads_before_write(ins[j + 1:-2], d):
                return ()
            if not any(ur.access in _RD and RegisterExt.is_gpr(ur.register)
                       and RegisterExt.full_register(ur.register) == d
                       for ur in _FAC.info(cmp).used_registers()):
                return ()
            # the resolve helper takes (obj, iface, slot) in RCX/RDX/R8
            # and never reads R9 (`_is_iface_resolve_helper`)
            if _reads_before_write(miss_insns, d,
                                   call_args={IReg.RCX, IReg.RDX, IReg.R8}):
                return ()
            return (x.ip, cmp.ip)
    return ()


def _is_rr_mov(ins):
    return ins.mnemonic == Mnemonic.MOV and ins.op0_kind == OpKind.REGISTER \
        and ins.op1_kind == OpKind.REGISTER and RegisterExt.is_gpr64(ins.op0_register) \
        and RegisterExt.is_gpr64(ins.op1_register)


def _known_zero_before(blocks, bid, end, reg):
    """All backward reaching definitions are full-width zero writes.

    A repeated node is a definition-free cycle, not evidence of zero. At
    least one zero definition is required and every entry/other write fails.
    Calls preserve only the Win64 nonvolatile registers. Bounded and read-only.
    """
    todo, seen, found, budget = [(bid, end)], set(), False, 4000
    while todo:
        bid, end = todo.pop()
        if (bid, end) in seen:
            continue
        seen.add((bid, end))
        block = blocks[bid]
        for ins in reversed(block.insns[:end]):
            budget -= 1
            if budget < 0:
                return False
            if ins.flow_control in (FlowControl.CALL, FlowControl.INDIRECT_CALL) \
                    and reg in _VOL:
                return False
            writes = any(ur.access in _WR and RegisterExt.is_gpr(ur.register)
                         and RegisterExt.full_register(ur.register) == reg
                         for ur in _FAC.info(ins).used_registers())
            if not writes:
                continue
            if ins.op0_kind != OpKind.REGISTER \
                    or not RegisterExt.is_gpr(ins.op0_register) \
                    or RegisterExt.size(ins.op0_register) < 4:
                return False
            zero = (ins.mnemonic == Mnemonic.XOR
                    and ins.op1_kind == OpKind.REGISTER
                    and ins.op0_register == ins.op1_register)
            if not zero:
                return False
            found = True
            break
        else:
            if not block.preds:
                return False
            todo.extend((p, len(blocks[p].insns)) for p in block.preds)
    return found


def _slot_zero_lea_fold(blocks, pb, bm, call_index, region, hits, res):
    """Exact zero-slot LEA alternative, NOT an arbitrary klass+0x138 LEA.

    Prove the whole four-block scan, the same receiver klass/count/table,
    interface comparison and signed offset*16 def-use chain. Miss arguments
    must be exactly (that receiver, that interface, 0). Existing outer purity,
    entry/exit and callee-saved liveness gates still apply.
    """
    def body(block):
        return [i for i in block.insns if i.mnemonic != Mnemonic.NOP]

    def rr(i, mnemonic, a, b):
        return (i.mnemonic == mnemonic and i.op0_kind == OpKind.REGISTER
                and i.op1_kind == OpKind.REGISTER
                and i.op0_register == a and i.op1_register == b)

    def mem(i, base, index, scale, disp, size):
        return (i.memory_base == base and i.memory_index == index
                and i.memory_index_scale == scale
                and i.memory_displacement == disp
                and MemorySizeExt.size(i.memory_size) == size
                and i.segment_prefix == IReg.NONE)

    if len(region) != 4 or len(hits) != 1 or res != IReg.RAX:
        return False
    hit = blocks[hits[0]]
    h = body(hit)
    if len(h) != 7 or h[-1].mnemonic != Mnemonic.JMP:
        return False
    z, double, offset, lea, shift, add, _ = h
    if z.mnemonic != Mnemonic.MOVZX or z.op0_kind != OpKind.REGISTER \
            or z.op1_kind != OpKind.REGISTER \
            or not RegisterExt.is_gpr32(z.op0_register) \
            or not RegisterExt.is_gpr16(z.op1_register):
        return False
    result = RegisterExt.full_register(z.op0_register)
    counter = z.op1_register
    if result != res or not rr(double, Mnemonic.ADD, result, result) \
            or offset.mnemonic != Mnemonic.MOVSXD \
            or offset.op0_kind != OpKind.REGISTER \
            or not RegisterExt.is_gpr64(offset.op0_register) \
            or offset.op1_kind != OpKind.MEMORY \
            or lea.mnemonic != Mnemonic.LEA or lea.op0_register != result \
            or lea.op1_kind != OpKind.MEMORY:
        return False
    off, table, klass = offset.op0_register, offset.memory_base, lea.memory_base
    if not all(RegisterExt.is_gpr64(r) for r in (table, klass)) \
            or len({result, off, klass}) != 3 or result == table \
            or not mem(offset, table, result, 8, 8, 4) \
            or lea.memory_index != IReg.NONE or lea.memory_displacement != 0x138 \
            or lea.segment_prefix != IReg.NONE \
            or shift.mnemonic != Mnemonic.SHL or shift.op0_register != off \
            or shift.op1_kind != OpKind.IMMEDIATE8 or shift.immediate8 != 4 \
            or not rr(add, Mnemonic.ADD, result, off):
        return False
    if len(hit.preds) != 1:
        return False
    loop = blocks[hit.preds[0]]
    q = body(loop)
    if loop.bid not in region or len(q) != 4 or q[-1].mnemonic != Mnemonic.JE \
            or not loop.term or len(loop.term) != 3 \
            or loop.term[0:2] != ('jcc', hit.bid) \
            or loop.term[2] not in region:
        return False
    zx, dbl, cmp, _ = q
    if zx.mnemonic != Mnemonic.MOVZX or zx.op0_kind != OpKind.REGISTER \
            or not RegisterExt.is_gpr32(zx.op0_register) \
            or zx.op1_kind != OpKind.REGISTER or zx.op1_register != counter:
        return False
    index = RegisterExt.full_register(zx.op0_register)
    if not rr(dbl, Mnemonic.ADD, index, index) \
            or cmp.mnemonic != Mnemonic.CMP or cmp.op0_kind != OpKind.MEMORY \
            or cmp.op1_kind != OpKind.REGISTER \
            or not RegisterExt.is_gpr64(cmp.op1_register) \
            or not mem(cmp, table, index, 8, 0, 8):
        return False
    iface = cmp.op1_register
    step = blocks[loop.term[2]]
    s = body(step)
    if len(s) != 3 or s[0].mnemonic != Mnemonic.INC \
            or s[0].op0_kind != OpKind.REGISTER or s[0].op0_register != counter \
            or s[1].mnemonic != Mnemonic.CMP or s[1].op0_register != counter \
            or s[1].op1_kind != OpKind.REGISTER \
            or not RegisterExt.is_gpr16(s[1].op1_register) \
            or s[2].mnemonic != Mnemonic.JB \
            or step.term != ('jcc', loop.bid, bm.bid):
        return False
    count = RegisterExt.full_register(s[1].op1_register)
    loads = region - {hit.bid, loop.bid, step.bid}
    if len(loads) != 1:
        return False
    load = blocks[next(iter(loads))]
    t = body(load)
    if len(t) != 1 or t[0].mnemonic != Mnemonic.MOV \
            or t[0].op0_register != table or t[0].op1_kind != OpKind.MEMORY \
            or not mem(t[0], klass, IReg.NONE, 1, 0xB0, 8) \
            or load.term != ('fall', loop.bid) or load.preds != [pb.bid] \
            or set(loop.preds) != {load.bid, step.bid} \
            or step.preds != [loop.bid]:
        return False
    e = body(pb)
    if len(e) < 5 or e[-1].mnemonic != Mnemonic.JAE \
            or pb.term != ('jcc', bm.bid, load.bid):
        return False
    seed, cnt, cmp = e[-4:-1]
    if seed.mnemonic != Mnemonic.MOVZX or seed.op0_kind != OpKind.REGISTER \
            or not RegisterExt.is_gpr32(seed.op0_register) \
            or RegisterExt.full_register(seed.op0_register) != RegisterExt.full_register(counter) \
            or seed.op1_kind != OpKind.REGISTER \
            or not RegisterExt.is_gpr16(seed.op1_register) \
            or cnt.mnemonic != Mnemonic.MOVZX or cnt.op0_kind != OpKind.REGISTER \
            or not RegisterExt.is_gpr32(cnt.op0_register) \
            or RegisterExt.full_register(cnt.op0_register) != count \
            or cnt.op1_kind != OpKind.MEMORY \
            or not mem(cnt, klass, IReg.NONE, 1, 0x12E, 2) \
            or not rr(cmp, Mnemonic.CMP, seed.op1_register, s[1].op1_register):
        return False
    miss = body(bm)
    # No hidden preparations, reordered arguments, slot changes or copies.
    if len(miss) != 4 or bm.insns[call_index] != miss[-1] \
            or not rr(miss[0], Mnemonic.XOR, IReg.R8D, IReg.R8D) \
            or not rr(miss[1], Mnemonic.MOV, IReg.RDX, iface) \
            or not _is_rr_mov(miss[2]) or miss[2].op0_register != IReg.RCX:
        return False
    obj = miss[2].op1_register
    # Respect the actual setup order: zeroing slot R8 must not destroy the
    # interface/receiver, and MOV RDX,iface must not destroy the receiver.
    if iface == IReg.R8 or obj in (IReg.R8, IReg.RDX):
        return False
    stable = {obj, klass, iface, count, table, RegisterExt.full_register(counter)}
    if len(stable) != 6 or IReg.RSP in stable \
            or index in stable or result in {klass, table}:
        return False
    # klass is freshly loaded from precisely the helper receiver. No later
    # call/write may replace either before the test; table/count use that klass.
    prefix = e[:-4]
    for j in range(len(prefix) - 1, -1, -1):
        ins = prefix[j]
        writes = _gpr_writes(ins)
        if writes is None:
            return False
        if klass in writes:
            if ins.mnemonic != Mnemonic.MOV or ins.op0_register != klass \
                    or ins.op1_kind != OpKind.MEMORY \
                    or not mem(ins, obj, IReg.NONE, 1, 0, 8):
                return False
            break
        if obj in writes:
            return False
    else:
        return False
    source = RegisterExt.full_register(seed.op1_register)
    if source in stable or source == IReg.RSP:
        return False
    seed_index = next(i for i, ins in enumerate(pb.insns) if ins.ip == seed.ip)
    return _known_zero_before(blocks, pb.bid, seed_index, source)


def iface_fast_path_prune(blocks, names, stats=None, skip=None):
    """Rewrite every proved inline interface dispatch in `blocks` (see the
    module docstring); return the number of fast paths pruned. `names`
    maps helper VAs to runtime names. Rebuilds preds when it rewrites.
    When `skip` (the lifter's skip-ip set) is given, the forced test's
    now-dead interface-count load and compare join it, so no orphan
    `[k+0x12E]` read renders."""
    def note(k):
        if stats is not None:
            stats[k] = stats.get(k, 0) + 1
    n = 0
    for bm in blocks:
        if not bm.insns:
            continue
        k = None
        for j, ins in enumerate(bm.insns):
            if ins.mnemonic == Mnemonic.CALL and ins.op0_kind == OpKind.NEAR_BRANCH64 \
                    and names.get(ins.near_branch_target) == 'il2cpp_interface_get_method':
                k = j
        if k is None:
            continue
        note('sites')
        tail = list(bm.insns[k + 1:])
        if tail and tail[-1].mnemonic == Mnemonic.JMP:
            tail = tail[:-1]
            if not bm.term or bm.term[0] != 'jmp':
                note('d_tail')
                continue
        elif not bm.term or bm.term[0] != 'fall':
            note('d_tail')
            continue
        join = bm.term[1]
        # the resolved entry travels from RAX through register copies
        res = IReg.RAX
        ok = True
        for t in tail:
            if _is_rr_mov(t) and t.op1_register == res:
                res = t.op0_register
            else:
                ok = False
        if not ok:
            note('d_tail2')
            continue
        done = False
        for p in list(bm.preds):
            pb = blocks[p]
            if not pb.term or pb.term[0] != 'jcc':
                continue
            ti, fi = pb.term[1], pb.term[2]
            other = fi if ti == bm.bid else ti
            if other < 0 or other in (bm.bid, join) or {ti, fi} != {bm.bid, other}:
                continue
            region, stack, ok = set(), [other], True
            while stack and ok:
                x = stack.pop()
                if x in region:
                    continue
                if x == p or len(region) >= 12:
                    ok = False
                    break
                region.add(x)
                for s in blocks[x].succs:
                    if s not in (bm.bid, join):
                        stack.append(s)
            if not ok:
                continue
            allowed = region | {p}
            if any(q not in allowed for x in region for q in blocks[x].preds):
                note('d_entry')
                continue
            if any(q not in allowed for q in bm.preds):
                note('d_misspreds')
                continue
            if any(q not in region and q != bm.bid for q in blocks[join].preds):
                note('d_joinpreds')
                continue
            hits = [x for x in region if join in blocks[x].succs]
            add_fold = any(
                i.mnemonic == Mnemonic.ADD and i.op1_kind in (
                    OpKind.IMMEDIATE32TO64, OpKind.IMMEDIATE32)
                and i.immediate32 == 0x138
                for x in hits for i in blocks[x].insns)
            if not hits or (not add_fold and not _slot_zero_lea_fold(
                    blocks, pb, bm, k, region, hits, res)):
                note('d_hit')
                continue
            if not any(i.op1_kind == OpKind.MEMORY and i.memory_displacement == 0xB0
                       for x in region for i in blocks[x].insns):
                note('d_table')
                continue
            written = set()
            for x in region:
                for i in blocks[x].insns:
                    w = _gpr_writes(i)
                    if w is None:
                        written = None
                        break
                    written |= w
                if written is None:
                    break
            if written is None:
                note('d_impure')
                continue
            # volatile registers are undefined after the miss path's call
            # (only the resolved entry survives), so no JOIN code reads
            # them; a callee-saved register the scan wrote must be dead
            written -= _VOL
            if written and not _dead_at(blocks, join, written):
                note('d_live')
                continue
            # rewrite: the entry test always takes the miss path
            pb.term = ('jmp', bm.bid)
            pb.succs = [bm.bid]
            pb.cond = None
            if skip is not None:
                skip.update(_dead_count_test(pb, bm.insns[:k + 1]))
            for x in region:
                blocks[x].succs = []
                blocks[x].term = ('abort',)
            for b in blocks:
                b.preds = []
            for b in blocks:
                for s in b.succs:
                    if 0 <= s < len(blocks):
                        blocks[s].preds.append(b.bid)
            n += 1
            done = True
            note('pruned')
            break
        if not done:
            note('d_nopred')
    return n
