"""Bounded native Int32 entry provenance, independent of field recovery.

This module does not seed Exprs, recover SIMD lanes, render captures, or alter
lifting. A future caller must separately bind the exact per-execution entry
Expr, preserve conversion-time snapshots and validate final capture lifetime.
"""
from itertools import islice

from il2cpp.lifter.abi import is_win64_pe
from il2cpp.lifter.unwindproof import NativeUnwindBoundary


class EntryInt32Origin:
    """A finite, decoded, exact-method context; no cross-method/binary cache."""

    def __init__(self, il, method, insns):
        self.il = il
        self.method = method
        self.insns = ()
        self._valid = False
        try:
            self.bin = il.bin
            self.meta = il.meta
            self._data = self.bin.d
            # Identity is a live snapshot only for immutable native bytes.
            # Unwind indexing copies the image, so mutable backing could leave
            # that proof stale after an in-place write on the same object.
            if type(self._data) is not bytes:
                return
            self._base = self.bin.image_base
            self._sections = self._section_key()
            # Bound ingestion too: never materialize an arbitrary iterable.
            self.insns = tuple(ins.copy() for ins in islice(iter(insns), 513))
            if not self.insns or len(self.insns) > 512:
                return
            self._by_ip = {ins.ip: ins for ins in self.insns}
            if len(self._by_ip) != len(self.insns):
                return
            self._boundary = NativeUnwindBoundary(self.bin)
            self._valid = True
        except (AttributeError, IndexError, KeyError, TypeError, ValueError,
                OverflowError):
            pass

    def _section_key(self):
        return tuple((s.addr, s.size, s.offset, s.rawsize, s.is_exec)
                     for s in self.bin.sections)

    @staticmethod
    def _int32(ty):
        return (isinstance(ty, tuple) and len(ty) == 2
                and (ty[1] >> 16) & 255 == 8 and not ty[1] & (1 << 29))

    def parameter_at(self, lift, conversion, block_insns, window=512):
        """Return an entry parameter index only after all predecessors agree.

        The conversion must be in the actual execution block, with a legacy
        MOVD GPR32 last writer in that block. Every intervening instruction
        has exactly its native fallthrough predecessor. GPR reaching-defs
        accept only MOV32 copies; calls kill volatile registers. Cycles,
        conflicting origins and unsupported writes decline. Suffix steps
        and distinct reaching-definition states share a total 512 budget.
        No Expr, use counter or register map is read or mutated here.
        """
        try:
            return self._parameter_at(lift, conversion, block_insns, window)
        except (AttributeError, IndexError, KeyError, TypeError, ValueError,
                OverflowError):
            return None

    def _context(self, lift):
        from iced_x86 import Code, FlowControl, Mnemonic, OpKind, Register

        il, m = self.il, self.method
        if (not self._valid or lift.il is not il or lift.meta is not self.meta
                or lift.bin is not self.bin or il.bin is not self.bin
                or il.meta is not self.meta or not is_win64_pe(self.bin)
                or self.bin.d is not self._data or self.bin.image_base != self._base
                or self._section_key() != self._sections
                or getattr(lift, '_current_method', None) is not m
                or not 0 <= m.index < len(self.meta.methods)
                or self.meta.methods[m.index] is not m
                or self.insns[0].ip != m.addr
                or il.addr_candidates.get(m.addr) != [('method', m.index)]
                or m.name in ('.ctor', '.cctor') or m.generic_container != -1
                or not 0 <= m.declaring < len(self.meta.typedefs)
                or self.meta.typedefs[m.declaring].generic_container != -1):
            return None
        if self._boundary.covers(m.addr, self.insns) is None:
            return None
        if not 0 <= m.return_type < len(il.types):
            return None
        rt = il.types[m.return_type]
        if (il._closed_type_key(rt) is None
                or not il._return_abi_is_known(rt)):
            return None
        base = int(il.returns_sret(rt)) + int(not m.is_static)
        params = self.meta.method_params(m)
        if len(params) != m.param_count:
            return None
        seeds = {}
        args = (Register.RCX, Register.RDX, Register.R8, Register.R9)
        for i, p in enumerate(params):
            if not 0 <= p.type < len(il.types):
                return None
            ty = il.types[p.type]
            if (il._closed_type_key(ty) is None
                    or (ty[1] >> 16) & 255 in (0, 1, 0x16)):
                return None
            if base + i < 4 and self._int32(ty):
                seeds[args[base + i]] = i
        if not seeds:
            return None
        by = self._by_ip
        successors = {}
        for ins in self.insns:
            # InstructionInfo's ordinary register-write list is not a model
            # of restored processor state (FXRSTOR/XRSTOR omit XMM writes).
            # ENCLU can also resume a context without ordinary CFG edges.
            # Reject these whole contexts, including privileged instructions,
            # before trusting either GPR reaching-defs or the vector suffix.
            if (ins.is_save_restore_instruction or ins.is_privileged
                    or ins.mnemonic == Mnemonic.ENCLU):
                return None
            if ins.ip != m.addr and il.addr_candidates.get(ins.ip):
                return None
            fc = ins.flow_control
            if ins.code in (Code.INT3, Code.UD2):
                edges = ()
            elif fc in (FlowControl.NEXT, FlowControl.CALL):
                if (fc == FlowControl.CALL and
                        (ins.op0_kind != OpKind.NEAR_BRANCH64
                         or not self.bin.is_exec_va(ins.near_branch_target))):
                    return None
                edges = (ins.next_ip,)
            elif fc in (FlowControl.CONDITIONAL_BRANCH,
                        FlowControl.UNCONDITIONAL_BRANCH):
                if ins.op0_kind != OpKind.NEAR_BRANCH64:
                    return None
                edges = (ins.near_branch_target,)
                if fc == FlowControl.CONDITIONAL_BRANCH:
                    edges += (ins.next_ip,)
            elif fc == FlowControl.RETURN and ins.mnemonic == Mnemonic.RET:
                edges = ()
            else:
                return None
            if any(ip not in by for ip in edges):
                return None  # in particular, a truncated normal fallthrough
            successors[ins.ip] = edges
        reachable = set()
        pending = [m.addr]
        while pending:
            ip = pending.pop()
            if ip not in reachable:
                reachable.add(ip)
                pending.extend(successors[ip])
        predecessors = {ip: set() for ip in reachable}
        for ip in reachable:
            for after in successors[ip]:
                predecessors[after].add(ip)
        if predecessors[m.addr]:
            return None
        return predecessors, seeds

    def _parameter_at(self, lift, conversion, block_insns, window):
        from iced_x86 import (InstructionInfoFactory, OpAccess, RegisterExt,
                              Register, FlowControl, OpKind, Mnemonic)

        if not isinstance(window, int) or not 0 < window <= 512:
            return None
        context = self._context(lift)
        if context is None:
            return None
        predecessors, seeds = context
        by = self._by_ip
        if (conversion.mnemonic != Mnemonic.CVTDQ2PS
                or conversion.op0_kind != OpKind.REGISTER
                or conversion.op1_kind != OpKind.REGISTER
                or not RegisterExt.is_xmm(conversion.op0_register)
                or not RegisterExt.is_xmm(conversion.op1_register)
                or by.get(conversion.ip) != conversion
                or conversion.ip not in predecessors
                or getattr(getattr(lift.out, 'block', None), 'insns', None)
                is not block_insns):
            return None
        # Bound and verify the execution block independently of its container.
        block = tuple(islice(iter(block_insns), 513))
        if len(block) > 512 or any(by.get(ins.ip) != ins for ins in block):
            return None
        positions = [i for i, ins in enumerate(block) if ins == conversion]
        if len(positions) != 1:
            return None
        writes = (OpAccess.WRITE, OpAccess.COND_WRITE, OpAccess.READ_WRITE,
                  OpAccess.READ_COND_WRITE)
        factory = InstructionInfoFactory()
        written = {}

        def destinations(ins):
            if ins.ip not in written:
                written[ins.ip] = {RegisterExt.full_register(r.register)
                                  for r in factory.info(ins).used_registers()
                                  if r.access in writes}
            return written[ins.ip]

        source = RegisterExt.full_register(conversion.op1_register)
        expected = conversion.ip
        suffix = 0
        movd = None
        for ins in reversed(block[:positions[0]]):
            suffix += 1
            if (suffix >= window or ins.next_ip != expected
                    or ins.flow_control != FlowControl.NEXT
                    or predecessors.get(expected) != {ins.ip}):
                return None
            expected = ins.ip
            if source not in destinations(ins):
                continue
            if (ins.mnemonic != Mnemonic.MOVD or ins.op_count != 2
                    or ins.op0_kind != OpKind.REGISTER
                    or ins.op0_register != conversion.op1_register
                    or ins.op1_kind != OpKind.REGISTER
                    or not RegisterExt.is_gpr32(ins.op1_register)):
                return None
            movd = ins
            break
        if movd is None:
            return None
        nonvolatile = {Register.RBX, Register.RBP, Register.RSI, Register.RDI,
                       Register.R12, Register.R13, Register.R14, Register.R15}
        first = (movd.ip, RegisterExt.full_register(movd.op1_register))
        pending = [(first, False)]
        memo, dependencies = {}, {}
        active, visited = set(), set()
        # Iterative DFS avoids Python's recursion limit near the native budget.
        while pending:
            key, finish = pending.pop()
            if key in memo:
                continue
            ip, reg = key
            if finish:
                values = {memo[parent] for parent in dependencies[key]}
                if len(values) != 1:
                    return None
                memo[key] = values.pop()
                active.remove(key)
                continue
            if key in active or len(visited) + suffix >= window:
                return None
            visited.add(key)
            if ip == self.method.addr:
                if reg not in seeds:
                    return None
                memo[key] = seeds[reg]
                continue
            parents = predecessors.get(ip)
            if not parents:
                return None
            deps = []
            for before in sorted(parents):
                ins = by[before]
                previous = reg
                if ins.flow_control == FlowControl.CALL and reg not in nonvolatile:
                    return None
                if reg in destinations(ins):
                    if (ins.mnemonic != Mnemonic.MOV or ins.op_count != 2
                            or ins.op0_kind != OpKind.REGISTER
                            or ins.op1_kind != OpKind.REGISTER
                            or not RegisterExt.is_gpr32(ins.op0_register)
                            or not RegisterExt.is_gpr32(ins.op1_register)
                            or RegisterExt.full_register(ins.op0_register) != reg):
                        return None
                    previous = RegisterExt.full_register(ins.op1_register)
                deps.append((before, previous))
            active.add(key)
            dependencies[key] = deps
            pending.append((key, True))
            pending.extend((parent, False) for parent in reversed(deps))
        return memo[first]
