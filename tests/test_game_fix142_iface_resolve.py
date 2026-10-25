"""Fix 142: the v39 interface-resolve helper is named, so the inlined
interface-table scans fold (limbus v39 ground truth).

On this runtime the slow-path resolve helper lives at 0x180789290 and
the 2022 byte template does not match it, so the helper stayed
``sub_180789290``, fix 139's ifaceprune never fired, and every inlined
interface dispatch printed the raw scan: a 1-byte ``[k+0x12E]`` count
read, a 1-byte ``[k+0xB0]`` table load, a 1-byte-indexed for head
comparing against ``typeof(I)`` (CS0019) and an indirect
``((byte*)E + 0x0)[0]()(args)`` call (CS0149). The v39 template names
the helper, which lights the arity trim, ifaceprune and the managed
``recv.I_Member`` fold: BuildHashes.PrintToConsole (mi 290837) renders
``enumerator12.MoveNext()`` / ``enumerator12.Current`` with the
``FileHash`` element type closed from ``IEnumerator_1<FileHash>``, and
AbilityBase.SetKeywords (mi 1816) renders GetEnumerator/MoveNext/
Dispose with no scan residue.
"""
import pytest

from game_support import find_method, lift_text

pytestmark = pytest.mark.game("limbus")


def _scan_residue(body):
    return [ln.strip() for ln in body.splitlines()
            if 'sub_180789290' in ln
            or 'il2cpp_interface_get_method(' in ln
            or ']*8 + 0x0)[0] != typeof(' in ln]


def test_print_to_console_dispatches_managed(baseline_game_decompiler):
    il, dec = baseline_game_decompiler
    mi, _, _ = find_method(
        il, 'CodeStage.AntiCheat.Genuine.CodeHash.BuildHashes',
        'PrintToConsole', 0)
    body = lift_text(il, dec, mi)
    residue = _scan_residue(body)
    assert not residue, residue[:4]
    assert 'enumerator12.MoveNext()' in body
    assert ('CodeStage.AntiCheat.Genuine.CodeHash.FileHash fileHash1 '
            '= enumerator12.Current;') in body


def test_set_keywords_has_no_scan_residue(baseline_game_decompiler):
    il, dec = baseline_game_decompiler
    mi, _, _ = find_method(il, 'AbilityBase', 'SetKeywords', 0)
    body = lift_text(il, dec, mi)
    residue = _scan_residue(body)
    assert not residue, residue[:4]
    assert 'enumerator2.MoveNext()' in body
    assert 'obj42?.Dispose();' in body
