"""Fix 145: a shared-body tail resolves through its hidden MethodInfo*
slot even when stale register spray follows it (limbus v39 ground
truth).

IL2CPP passes a shared generic body's callee identity -- the method's
own MethodInfo, loaded from a lazy MethodRef usage slot -- as a hidden
argument at a fixed ABI position: one GPR slot past the declared
argument slots. ``_tail_hidden_generic`` used to accept the identity
only when nothing written followed it, so every tail whose dead GPRs
outlived the identity kept the ``sub_x/*shared body, N candidates*/``
marker and sprayed those dead values as invented arguments.
``_methodinfo_slot`` computes the slot from the spec's declared
signature; an identity sitting exactly there is the callee.

PluginsManager.PurgeAll (mi 294568) tails ``Dictionary`2<Type,
ITweenPlugin>.Clear`` with two stale GPRs behind the MethodRef and now
renders ``PluginsManager._customPlugins.Clear(); return;``;
RenderPipelineChecker.GetTypesSafe (mi 314901) resolves the
``Enumerable.Where<Type>`` tail it used to spray.
"""
import pytest

from game_support import find_method, lift_text

pytestmark = pytest.mark.game("limbus")


def test_purge_all_clears_dictionary(baseline_game_decompiler):
    il, dec = baseline_game_decompiler
    mi, _, _ = find_method(
        il, 'DG.Tweening.Plugins.Core.PluginsManager', 'PurgeAll', 0)
    body = lift_text(il, dec, mi)
    assert 'sub_183c16050' not in body
    assert 'PluginsManager._customPlugins.Clear(); return;' in body


def test_get_types_safe_resolves_where_tail(baseline_game_decompiler):
    il, dec = baseline_game_decompiler
    mi, _, _ = find_method(
        il, 'AllIn1SpriteShader.RenderPipelineChecker', 'GetTypesSafe', 1)
    body = lift_text(il, dec, mi)
    assert 'sub_1838e3560' not in body
    assert 'return System.Linq.Enumerable.Where<System.Type>(' in body
