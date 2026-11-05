"""Conservative PE x64 unwind boundaries for future entry-origin proofs.

This is not an EH decoder, a stack unwinder, or method-ownership evidence.
Only an exact file-backed instruction footprint in one handler-free unwind
family qualifies. Missing leaf records are unknown, not proof of no EH.
No lifting or rendering rule is enabled by this module alone.
"""
from bisect import bisect_right
import struct

from il2cpp.lifter.abi import is_win64_pe


class NativeUnwindBoundary:
    """One immutable binary snapshot; success/failure caches are per instance.

    The PE exception directory, not a section's conventional name, selects
    the RUNTIME_FUNCTION table. Only version-1 UNWIND_INFO with flags 0 or
    CHAININFO is supported. Chained triples must be real indexed records
    and terminate at the same primary record starting at the method entry.
    """

    def __init__(self, binary):
        self._rows = ()
        self._starts = ()
        self._roots = {}
        self._valid = False
        try:
            if not is_win64_pe(binary):
                return
            self._data = bytes(binary.d)
            self._base = binary.image_base
            self._sections = tuple((s.addr, s.size, s.offset, s.rawsize, s.is_exec)
                                   for s in binary.sections)
            pe = struct.unpack_from('<I', self._data, 0x3c)[0]
            opt = pe + 24
            size = struct.unpack_from('<H', self._data, pe + 20)[0]
            if (pe < 0x40 or size < 144 or opt + size > len(self._data)
                    or struct.unpack_from('<H', self._data, opt)[0] != 0x20b
                    or struct.unpack_from('<I', self._data, opt + 108)[0] < 4):
                return
            rva, length = struct.unpack_from('<II', self._data, opt + 136)
            if not rva or not length or length % 12:
                return
            raw = self._read(rva, length)
            if raw is None:
                return
            rows = tuple(struct.iter_unpack('<III', raw))
            previous = 0
            for begin, end, unwind in rows:
                if (not begin or end <= begin or begin < previous
                        or not unwind or unwind & 3):
                    return
                previous = end
            self._rows = rows
            self._starts = tuple(row[0] for row in rows)
            self._records = frozenset(rows)
            self._valid = True
        except (AttributeError, IndexError, TypeError, ValueError, OverflowError,
                struct.error):
            # A partial parse is never made usable by a later query.
            self._valid = False

    def _read(self, rva, length, executable=False):
        """Never let Binary.read silently cross a raw section/file boundary."""
        if not isinstance(rva, int) or not isinstance(length, int):
            return None
        if rva <= 0 or length <= 0 or rva + length > 0x100000000:
            return None
        va = self._base + rva
        touching = [s for s in self._sections
                    if s[0] < va + length and va < s[0] + max(s[1], s[3])]
        if len(touching) != 1:
            return None
        addr, size, offset, rawsize, is_exec = touching[0]
        delta = va - addr
        if (delta < 0 or delta + length > min(size, rawsize)
                or (executable and not is_exec) or offset < 0):
            return None
        start = offset + delta
        if start < 0 or start + length > len(self._data):
            return None
        return self._data[start:start + length]

    def _record(self, rva):
        i = bisect_right(self._starts, rva) - 1
        if i >= 0 and rva < self._rows[i][1]:
            return self._rows[i]
        return None

    @staticmethod
    def _codes_valid(header, codes):
        """Validate v1 slot grammar; do not interpret a restored register value."""
        frame = header[3] & 15
        nonvolatile = (3, 5, 6, 7, 12, 13, 14, 15)
        if frame not in (0,) + nonvolatile or (not frame and header[3] >> 4):
            return False
        i, previous = 0, header[1]
        while i < header[2]:
            offset, packed = codes[2 * i:2 * i + 2]
            op, info = packed & 15, packed >> 4
            if offset > previous:
                return False
            previous = offset
            if op in (0, 4, 5):
                if info not in nonvolatile:
                    return False
                extra = {0: 0, 4: 1, 5: 2}[op]
            elif op == 1:
                if info not in (0, 1):
                    return False
                extra = 1 if info == 0 else 2
            elif op == 2:
                extra = 0
            elif op == 3:
                if info or not frame:
                    return False
                extra = 0
            elif op in (8, 9):
                if not 6 <= info <= 15:
                    return False
                extra = 1 if op == 8 else 2
            elif op == 10:
                if info not in (0, 1):
                    return False
                extra = 0
            else:
                return False
            i += 1 + extra
            if i > header[2]:
                return False
        return True

    def _root(self, row):
        if row in self._roots:
            return self._roots[row]
        seen = set()
        current = row
        root = None
        frame = None
        # Independent conservative chain bound, not a lifting/CFG cap change.
        for _ in range(32):
            if current in seen or current not in self._records:
                break
            seen.add(current)
            begin, end, unwind = current
            if self._read(begin, end - begin, executable=True) is None:
                break
            header = self._read(unwind, 4)
            if header is None or header[0] & 7 != 1:
                break
            flags = header[0] >> 3
            if flags not in (0, 4):
                break  # includes all known/unknown handlers and reserved flags
            if frame is not None and header[3] != frame:
                break
            frame = header[3]
            count = header[2]
            padded = (2 * count + 3) & ~3
            # Include odd-slot padding and the complete chained triple.
            raw = self._read(unwind, 4 + padded + (12 if flags == 4 else 0))
            if raw is None or not self._codes_valid(header, raw[4:4 + 2 * count]):
                break
            if not flags:
                root = current
                break
            current = struct.unpack_from('<III', raw, 4 + padded)
        # Cache only after the chain terminates or the whole proof declines.
        # A failed descendant must not poison a valid ancestor's cache (or
        # make another method's answer depend on which query ran first).
        self._roots[row] = root
        return root

    def covers(self, entry, insns):
        """Return footprint records iff they share a handler-free primary root.

        Re-decode each actual file slice and compare instructions, not just
        caller-supplied address ranges. This proves neither CFG completeness
        nor metadata ownership; a caller must establish both independently.
        At most 512 instructions are accepted. Missing/malformed data declines.
        """
        try:
            return self._covers(entry, insns)
        except (AttributeError, IndexError, KeyError, TypeError, ValueError,
                OverflowError, struct.error):
            return None

    def _covers(self, entry, insns):
        from iced_x86 import Code, Decoder

        if not self._valid:
            return None
        insns = tuple(insns)
        if not insns or len(insns) > 512 or insns[0].ip != entry:
            return None
        primary = self._record(entry - self._base)
        if (primary is None or primary[0] + self._base != entry
                or self._root(primary) != primary):
            return None
        end = 0
        records = set()
        for ins in sorted(insns, key=lambda native: native.ip):
            size = ins.next_ip - ins.ip
            if ins.code == Code.INVALID or size < 1 or size > 15 or ins.ip < end:
                return None
            rva = ins.ip - self._base
            raw = self._read(rva, size, executable=True)
            if raw is None or Decoder(64, raw, ip=ins.ip).decode() != ins:
                return None
            row = self._record(rva)
            if row is None or rva + size > row[1] or self._root(row) != primary:
                return None
            end = ins.next_ip
            records.add(row)
        return tuple(sorted(records))


class NativeUnwindCache:
    """One owner's checked immutable snapshot, never a global/identity-only cache.

    Owning decompilers may reuse the index across preflights. A recovery arena
    must deepcopy this object with its binary: the owner and mutable root cache
    then belong to that arena. This is not MethodDef, CFG or ABI-slot evidence.
    """

    def __init__(self):
        self._clear()

    def _clear(self):
        self._owner = self._data = self._base = self._sections = self._proof = None

    def snapshot(self, binary):
        """Return a snapshot only while its entire live native context matches.

        A strong owner reference prevents recycled-id hits. Equal bytes from a
        different image are not identity evidence. Mutable backing is declined,
        even when its present contents happen to match an earlier snapshot.
        """
        try:
            data, base = binary.d, binary.image_base
            if type(data) is not bytes or type(base) is not int or not is_win64_pe(binary):
                self._clear()
                return None
            sections = tuple((s.addr, s.size, s.offset, s.rawsize, s.is_exec)
                             for s in binary.sections)
            if any(any(type(value) is not int for value in row[:4])
                   or type(row[4]) is not bool for row in sections):
                self._clear()
                return None
            if (self._owner is binary and self._data is data
                    and self._base == base and self._sections == sections):
                return self._proof
            # Publish the complete snapshot together, including negative parses.
            # No earlier proof remains available if construction fails.
            self._clear()
            proof = NativeUnwindBoundary(binary)
            self._owner, self._data, self._base = binary, data, base
            self._sections, self._proof = sections, proof
            return proof
        except (AttributeError, IndexError, KeyError, TypeError, ValueError,
                OverflowError, struct.error):
            self._clear()
            return None
