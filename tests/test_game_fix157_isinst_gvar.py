"""Fix 157: the isinst family's generic-variable build, lazily named.

`0x1807e3c60` (10,696 sites) is the isinst helper's second body: the
same prologue and System.Object short-circuit as the census-named
0x180479f80, plus the VAR/MVAR target handling. The hot-target sample
behind the census never reaches it, so the lazy prober is its only
shot. Sites whose klass argument renders as typeof(T) route through
the fix-151 `obj as T` fold; the common shared-body shape takes the
target klass from the rgctx ([klass+0x40]) and keeps the honest named
call -- the fold declines there, it never guesses.
"""
import pytest

pytestmark = pytest.mark.game("limbus")

GVAR_ISINST = 0x1807e3c60


def test_gvar_isinst_lazily_named(baseline_game_decompiler):
    il, dec = baseline_game_decompiler
    L = dec.L
    assert getattr(L, 'rt_names', {}).get(GVAR_ISINST) is None
    assert L._call_name(GVAR_ISINST) == 'il2cpp_object_isinst'
    assert GVAR_ISINST in L.rt_isinst
    # one structural proof, memoized per address
    assert L._call_name(GVAR_ISINST) == 'il2cpp_object_isinst'


def test_gvar_isinst_fold_declines_without_typeof(baseline_game_decompiler):
    """A shared-body site takes the target klass from the rgctx deref --
    no typeof() argument, no fold, the honest named call."""
    from game_support import find_method, lift_text
    il, dec = baseline_game_decompiler
    mi, _, _ = find_method(
        il, 'UnityEngine.UI.StencilMaterial', 'Add', 7)
    body = lift_text(il, dec, mi)
    if 'sub_1807e3c60' in body:
        raise AssertionError('lazy naming did not reach the site')
