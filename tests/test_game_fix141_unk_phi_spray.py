"""Fix 141 ground truths, superseded by fix 158's pinvoke fold.

FMOD.Channel.setFrequency 0x18359AED0 and the ISteamMusicRemote interface
pointer body 0x183473B70 (shared with SteamAPI_SteamMusicRemote_v001) were
the fix-141 ground truths: a cached function pointer guard join whose
resolve arm calls sub_18078d570 clobbered the volatile registers, and the
join's argument builder printed undeclared trailing ``objN`` arguments
(CS0103 at Roslyn). Fix 141 made the all-unknown phi ``_unk`` and dropped
it; the carried obj17..obj19 on setFrequency stayed honest.

Fix 158 goes further: the resolver itself is recognized (the stub scan
maps (module, entrypoint) -> MethodDef), so the guard-join resolve and
the cached invoke collapse to the direct managed DllImport call -- there
is no indirect call left to spray at either site.
"""
import pytest

from game_support import find_method, lift_text

pytestmark = pytest.mark.game("limbus")


def test_fmod_set_frequency_renders_the_dllimport_call(baseline_game_decompiler):
    il, dec = baseline_game_decompiler
    mi, _, _ = find_method(il, 'FMOD.Channel', 'setFrequency', 1)
    body = lift_text(il, dec, mi)
    # FMOD_Channel_SetFrequency(handle, float): the fold erased the
    # resolver, the cached cell, and the join spray entirely.
    assert '/*indirect*/' not in body
    assert 'sub_18078d570' not in body
    assert 'obj17' not in body and 'obj22' not in body
    assert 'return FMOD.Channel.FMOD5_Channel_SetFrequency(this.handle, frequency);' \
        in body


def test_steam_interface_pointer_takes_no_arguments(baseline_game_decompiler):
    il, dec = baseline_game_decompiler
    mi, _, _ = find_method(
        il, 'Steamworks.ISteamMusicRemote', 'GetUserInterfacePointer', 0)
    body = lift_text(il, dec, mi)
    # The v001 entry point returns the interface pointer and takes nothing;
    # the fold renders the zero-argument managed call directly.
    assert '/*indirect*/' not in body
    assert ', obj12' not in body
    assert 'return Steamworks.ISteamMusicRemote.SteamAPI_SteamMusicRemote_v001();' \
        in body
