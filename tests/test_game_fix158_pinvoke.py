"""Fix 158: the P/Invoke resolver folds to the managed DllImport call.

il2cpp strips DllImportAttribute from the runtime attribute blobs, so
the managed identity of a pinvoke site cannot come from the attribute
table. What survives: each `pinvokeimpl` method's codegen fnptr is the
resolver stub whose descriptor carries the same (module, entrypoint)
literals the inlined call sites build -- the module name UTF-16, the
entrypoint ASCII. scan_pinvoke_stubs maps 1,999 of the 2,032
pinvokeimpl methods to their (module, entrypoint); the inlined fill
sites' cache cells (2,018) map through the same pairs; and the
resolver call itself renders nothing, so the guarded invoke collapses
to the direct managed call:

    FMOD.Studio.EventInstance.FMOD_Studio_EventInstance_SetTimelinePosition(
        BattleSoundGenerator._currentInstance, millisec);
"""
import pytest

from game_support import find_method, lift_text

pytestmark = pytest.mark.game("limbus")


def test_pinvoke_map_and_resolver_detected(baseline_game_decompiler):
    il, _ = baseline_game_decompiler
    assert getattr(il, 'rt_pinvoke_resolve', None) == 0x18078d570
    pmap = getattr(il, 'pinvoke_map', {}) or {}
    assert len(pmap) >= 1900
    assert ('fmodstudio', 'FMOD5_System_Create') in pmap
    cells = getattr(il, 'pinvoke_cells', {}) or {}
    assert len(cells) >= 1800


def test_pinvoke_site_renders_the_managed_call(baseline_game_decompiler):
    il, dec = baseline_game_decompiler
    mi, _, _ = find_method(
        il, 'BattleSkillViewEGO_2010711', 'SetBgmStartPos', 1)
    body = lift_text(il, dec, mi)
    assert 'sub_18078d570' not in body
    assert ('FMOD.Studio.EventInstance.'
            'FMOD_Studio_EventInstance_SetTimelinePosition(') in body
    assert 'FMOD.Studio.EventInstance.FMOD_Studio_EventInstance_GetDescription(' \
        in body


def test_pinvoke_cell_reads_render_the_managed_name(baseline_game_decompiler):
    il, dec = baseline_game_decompiler
    mi, _, _ = find_method(
        il, 'BattleSkillViewEGO_2010711', 'SetBgmStartPos', 1)
    body = lift_text(il, dec, mi)
    # the cached-cell guard names the method, not data_NNN
    assert 'data_189452dc0' not in body
