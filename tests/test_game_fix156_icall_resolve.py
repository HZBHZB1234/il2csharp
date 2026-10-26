"""Fix 156: the icall resolver is found on the v39 fixture again.

`scan_icall_cache` pinned the fill tail to the bare
`lea/call/mov [cell],rax` layout; the v39 fixture always interleaves
the null guard (`test rax,rax; je +N`) between the call and the cached
store, so `rt_icall_resolve` stayed unset and every eager resolve site
rendered as an unannotated `sub_1807a5bf0(&"sig", ...)` with the
invoke's arguments merged in. With the guarded tail walked, the helper
is 0x1807a5bf0 (29,126 signature-valid fills, 4,197 cache cells), the
resolve renders nothing (the early arm reads its RCX argument
uncounted), and the guarded invoke renders the managed icall call:

    UnityEngine.Transform.SetPositionAndRotation_Injected(num1,
        ref vector32, ref quaternion2);
"""
import pytest

from game_support import find_method, lift_text

pytestmark = pytest.mark.game("limbus")


def test_resolver_detected(baseline_game_decompiler):
    il, _ = baseline_game_decompiler
    assert getattr(il, 'rt_icall_resolve', None) == 0x1807a5bf0
    cells = getattr(il, 'icall_cells', {}) or {}
    assert len(cells) >= 4000
    # every mapped signature names a real managed method
    assert all('::' in s for s in cells.values())


def test_resolve_site_renders_the_managed_call(baseline_game_decompiler):
    il, dec = baseline_game_decompiler
    mi, _, _ = find_method(
        il, 'AbilityEffect_NoirNailAlly', 'LateUpdate', 0)
    body = lift_text(il, dec, mi)
    assert 'sub_1807a5bf0' not in body
    assert ('UnityEngine.Transform.SetPositionAndRotation_Injected'
            in body)


def test_detour_site_has_no_leaked_sig_operand(baseline_game_decompiler):
    """The jmp-detour fill shape (the store sits behind interleaved
    code) must not leak the fill's `lea` as an `objN = &"sig"`
    statement -- that operand is CS0214 (address of a managed string)."""
    il, dec = baseline_game_decompiler
    mi, _, _ = find_method(
        il, 'UnityEngine.UI.InputField', 'LineDownCharacterPosition', 2)
    body = lift_text(il, dec, mi)
    assert '= &"' not in body
    assert 'sub_1807a5bf0' not in body
