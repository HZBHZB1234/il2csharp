"""Fix 141: no stale-register spray on indirect calls (limbus v39 ground truth).

FMOD.Channel.setFrequency 0x18359AED0 and the ISteamMusicRemote interface
pointer body 0x183473B70 (shared with SteamAPI_SteamMusicRemote_v001): a
cached function pointer guard join whose resolve arm calls sub_18078d570
clobbers the volatile registers, so one arm of the join leaves them missing
and the other carries explicit ``_unk`` seeds. The join used to mint phis
that the argument builder printed as undeclared trailing ``objN`` arguments
(CS0103 at Roslyn). The merge now marks an all-unknown phi ``_unk`` and the
argument builder drops it; carried values that are not all-unknown (obj17..
obj19 on setFrequency) stay honest.
"""
import pytest

from game_support import find_method, lift_text

pytestmark = pytest.mark.game("limbus")


def _indirect_calls(body):
    return [ln.strip() for ln in body.splitlines() if '/*indirect*/' in ln]


def test_fmod_set_frequency_drops_the_unknown_tail(baseline_game_decompiler):
    il, dec = baseline_game_decompiler
    mi, _, _ = find_method(il, 'FMOD.Channel', 'setFrequency', 1)
    body = lift_text(il, dec, mi)
    calls = _indirect_calls(body)
    assert len(calls) == 1, calls
    # FMOD_Channel_SetFrequency(handle, float): the pre-fix spelling sprayed
    # obj20..obj22 (undeclared) around the real float argument.
    assert calls[0] == (
        'object obj16 = obj3() /*indirect*/'
        '(this.handle, obj17, obj18, obj19, frequency);')
    assert 'obj22' not in body


def test_steam_interface_pointer_takes_no_arguments(baseline_game_decompiler):
    il, dec = baseline_game_decompiler
    mi, _, _ = find_method(
        il, 'Steamworks.ISteamMusicRemote', 'GetUserInterfacePointer', 0)
    body = lift_text(il, dec, mi)
    calls = _indirect_calls(body)
    assert len(calls) == 1, calls
    # The v001 entry point returns the interface pointer and takes nothing;
    # the pre-fix spelling sprayed obj12..obj18 after `this`.
    assert calls[0] == 'object obj11 = obj1() /*indirect*/(this);'
    assert ', obj12' not in body
