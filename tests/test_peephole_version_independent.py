"""Version-independent peephole behaviour, pinned on synthetic x86.

The class-init guard peephole (`_BuildMixin._guards`) and the EH-helper
noreturn screen (`_Decompiler._eh_helper_returns`) decide from x64
instruction bytes alone.  That makes them version-agnostic by
construction: the same MSVC prologue/guard/fence shapes appear in every
Windows x64 IL2CPP build from v24 through v39.  These tests pin the
shapes directly so a future edit cannot silently narrow them for one
Unity generation while another still needs them.

No game data is involved: each byte blob below is hand-assembled x86 the
way MSVC emits it, decoded with iced.
"""
import struct

import pytest

pytest.importorskip('iced_x86')

from iced_x86 import Decoder, DecoderOptions, Mnemonic, OpKind, Register as IReg

from il2cpp.dec import Decompiler

# A nearby fake helper address the synthetic `call rel32` instructions
# target.  Kept inside the low 2 GiB of a canonical-x64 image so the
# hand-computed rel32 is exact.
RT_INIT = 0x1807980C0
GUARD_SLOT = 0x189446C5F           # a .data byte cell, RIP-relative


def _insns(blob, ip=0x182BAB270):
    d = Decoder(64, bytes(blob), DecoderOptions.NONE)
    d.ip = ip
    return list(d)


def _rip_rel(at_ip, insn_len, target):
    """disp32 that turns `[rip+disp]` (rip = at_ip+insn_len) into target."""
    return target - (at_ip + insn_len)


def _bare_decompiler():
    """A Decompiler with only what `_guards` touches: `self.L`."""
    class _L:
        rt_init_meta = RT_INIT

    dec = Decompiler.__new__(Decompiler)
    dec.L = _L()
    return dec


def _guard_blob(brk='jne', moves=b'', n_types=1, barrier=True, releasestore=True):
    """Assemble one init-guard byte sequence and return (blob, ip_of_cmp).

    Layout (MSVC shape):
        cmp byte ptr [rip+GUARD_SLOT], 0
        <moves: register saves interleaved after the cmp>
        jne  skip
        per type:  lea rcx,[rip+T_i]; call RT_INIT [; lock or [rsp],0]
        [optional] mov byte ptr [rip+GUARD_SLOT], 1
    skip:
        nop
    """
    ip = 0x182BAB270
    b = bytearray()

    def emit(x):
        b.extend(x)

    # cmp byte ptr [rip+disp32], 0   -> 80 3D <disp32> 00
    cmp_ip = ip + len(b)
    emit(b'\x80\x3d')
    emit(struct.pack('<i', _rip_rel(cmp_ip, 7, GUARD_SLOT)))
    emit(b'\x00')

    if moves:
        emit(moves)

    # jcc rel8 placeholder -> patched to skip to the tail nop
    jcc_ip = ip + len(b)
    jcc_op = {'jne': b'\x75', 'je': b'\x74'}[brk]
    emit(jcc_op + b'\x00')          # 2-byte jcc rel8

    for i in range(n_types):
        # lea rcx,[rip+disp32] -> 48 8D 0D <disp32>
        lea_ip = ip + len(b)
        emit(b'\x48\x8d\x0d')
        emit(struct.pack('<i', _rip_rel(lea_ip, 7, 0x1890CA148 + i * 0x20)))
        # call rel32 -> E8 <disp32>
        call_ip = ip + len(b)
        emit(b'\xe8')
        emit(struct.pack('<i', RT_INIT - (call_ip + 5)))
        if barrier:
            # lock or dword ptr [rsp], 0 -> F0 83 0C 24 00
            # (0x0C = modrm /1 = OR; 0x04 would be /0 = ADD, a different
            #  mnemonic the peephole must NOT treat as a no-op fence)
            emit(b'\xf0\x83\x0c\x24\x00')

    if releasestore:
        # mov byte ptr [rip+disp32], 1 -> C6 05 <disp32> 01
        st_ip = ip + len(b)
        emit(b'\xc6\x05')
        emit(struct.pack('<i', _rip_rel(st_ip, 7, GUARD_SLOT)))
        emit(b'\x01')

    tail_ip = ip + len(b)
    emit(b'\x90')                   # nop at the branch target

    # patch the jcc rel8
    rel = tail_ip - (jcc_ip + 2)
    assert -128 <= rel <= 127, rel
    b[jcc_ip - ip + 1] = rel & 0xFF
    return bytes(b), cmp_ip


def test_barrier_guard_is_swallowed():
    """The `lock or [rsp],0` release fence must not stop the guard scan."""
    blob, cmp_ip = _guard_blob(n_types=2, barrier=True)
    raw = _insns(blob)
    dec = _bare_decompiler()
    skip = dec._guards(raw)

    assert cmp_ip in skip, 'guard cmp must be skipped'
    barriers = [x for x in raw if dec._is_init_barrier(x)]
    assert len(barriers) == 2
    assert all(x.ip in skip for x in barriers), 'every fence must be skipped'
    # the flag store and the init call are skipped too
    calls = [x for x in raw
             if x.mnemonic == Mnemonic.CALL and x.near_branch_target == RT_INIT]
    assert len(calls) == 2 and all(x.ip in skip for x in calls)


def test_guard_without_release_store_is_not_swallowed():
    """No `mov byte [slot],1` closing the guard -> decline (unchanged)."""
    blob, cmp_ip = _guard_blob(n_types=1, barrier=True, releasestore=False)
    raw = _insns(blob)
    dec = _bare_decompiler()
    skip = dec._guards(raw)
    assert cmp_ip not in skip


def test_jcc_behind_register_saves_is_found():
    """MSVC parks the jcc behind movq/movaps saves; window must reach it."""
    # movq rdi,xmm6 ; movaps xmm6,[rsp+0x1F0] (a pure move pair)
    moves = (b'\x66\x48\x0f\x7e\xf7'                  # movq rdi, xmm6
             b'\x0f\x29\xb4\x24\xf0\x01\x00\x00')     # movaps [rsp+0x1F0],xmm6
    blob, cmp_ip = _guard_blob(n_types=1, moves=moves, barrier=True)
    raw = _insns(blob)
    dec = _bare_decompiler()
    skip = dec._guards(raw)
    assert cmp_ip in skip, 'jcc sits 2 saves past the cmp; window must reach it'


def test_arithmetic_between_cmp_and_jcc_declines():
    """A real arithmetic op (addss) is NOT a pure move: keep declining."""
    # addss xmm0,xmm0 = F3 0F 58 C0
    moves = b'\xf3\x0f\x58\xc0'
    blob, cmp_ip = _guard_blob(n_types=1, moves=moves, barrier=True)
    raw = _insns(blob)
    dec = _bare_decompiler()
    skip = dec._guards(raw)
    assert cmp_ip not in skip, 'arithmetic must not be treated as a save'


# ------------------------------------------------------------------ P1-a
class _LforEh:
    pass


def _eh_decompiler(bin_bytes_by_va):
    """A Decompiler whose _eh_helper_returns can read fake code."""
    class _Bin:
        def __init__(self, m):
            self._m = m

        def is_exec_va(self, va):
            return va in self._m

        def read(self, va, n):
            return self._m[va][:n]

    class _Il:
        def __init__(self, m):
            self.bin = _Bin(m)

    class _L:
        def __init__(self, m):
            self.il = _Il(m)

    dec = Decompiler.__new__(Decompiler)
    dec.L = _LforEh()
    dec.L.il = _Il(bin_bytes_by_va)
    # _eh_helper_returns uses self.L.il.bin and HAVE_ICED
    return dec


def test_eh_helper_rejects_a_late_returner():
    """A routine whose first `ret` is far past the old 64-insn window
    must be rejected (it is not a throw helper)."""
    va = 0x1807E3DB0
    # 200 nops then a ret: nothing that looks noreturn, but it clearly returns.
    code = b'\x90' * 200 + b'\xc3'
    dec = _eh_decompiler({va: code})
    assert dec._eh_helper_returns(va) is True


def test_eh_helper_accepts_an_early_int3_noreturn():
    """A `sub rsp,X; call T; int3` stub is noreturn: no ret before int3."""
    va = 0x18078C580
    # sub rsp,0x28 ; call rel32 ; int3  (call target irrelevant for this test)
    code = bytearray(b'\x48\x83\xec\x28')
    call_ip = va + len(code)
    code += b'\xe8' + struct.pack('<i', 0x1807A3C10 - (call_ip + 5))
    code += b'\xcc'                       # int3
    code += b'\xc3'                       # a ret AFTER the int3 (padding)
    dec = _eh_decompiler({va: bytes(code)})
    assert dec._eh_helper_returns(va) is False
