"""Open-source fixture: generic method table alignment and tail resolution.

`Il2CppGenericMethodFunctionsDefinitions.methodPointerIndex` (the second
int) indexes `genericMethodPointers`; the table row number does not.  Before
the fix the survivors tree paired row i with pointer i, so:
  * `BoolWrapper.Reset`'s tail to `WrapperT<bool>.set_Value` was named
    `WhereSelectEnumerableIterator<...>.ctor` (the body at that address
    after the shift), and
  * `PlayerAnim.Awake`'s `Component.GetComponent<Rigidbody2D>()` came out as
    `GetComponent()` (the owner was found, but the qualified generic
    argument's own dot defeated the method-name slice).
"""
import pytest

from game_support import find_method, lift_text


pytestmark = pytest.mark.game("survivors-roguelike-kit")


def test_generic_tail_uses_its_true_method_spec(raw_game_decompiler):
    il, dec = raw_game_decompiler
    mi, _m, _td = find_method(il, 'RGame.Framework.BoolWrapper', 'Reset')
    text = lift_text(il, dec, mi)
    assert 'WhereSelectEnumerableIterator' not in text
    assert 'WrapperT<bool>.set_Value' in text or 'this.Value = false' in text
    assert 'this.Value = false' in text


def test_reference_generic_call_keeps_its_closed_type(raw_game_decompiler):
    il, dec = raw_game_decompiler
    mi, _m, _td = find_method(il, 'RGame.RoguelikeKit.PlayerAnim', 'Awake')
    text = lift_text(il, dec, mi)
    assert 'GetComponent<UnityEngine.Rigidbody2D>' in text
    assert 'GetComponent<UnityEngine.Animator>' in text
    # the GC write barrier's raw twin is dropped next to the managed store
    assert '((byte*)&this.MyRigidbody + 0x0)[0]' not in text
