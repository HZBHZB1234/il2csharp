"""Fix 149: element stores render as `array[index] = value`
(limbus v39 ground truth).

`0x180002950` is the bounds-checked reference store (15,453 sites):
OOB guard, `mov [rcx+rdx*8+0x20],r8`, GC write barrier, returning a
bitmap word that source never reads. Before, every site printed
`object objN = sub_180002950(new string[6], 0, "...")` -- re-allocating
the array per element and inventing a value.
"""
import pytest

from game_support import find_method, lift_text

pytestmark = pytest.mark.game("limbus")


def test_string_array_initializer_reads_as_element_stores(
        baseline_game_decompiler):
    il, dec = baseline_game_decompiler
    mi, _, _ = find_method(
        il, 'CodeStage.AntiCheat.Examples.Genuine.GenuineValidatorExample',
        'OnGotHash', 1)
    body = lift_text(il, dec, mi)
    assert 'sub_180002950' not in body
    # the six-string array is a collection initializer, not six stores
    assert 'new string[6] {' in body
    assert 'Summary hashes' in body
    assert 'Whitelisted hashes count' in body


def test_clone_body_has_no_store_helper(baseline_game_decompiler):
    il, dec = baseline_game_decompiler
    mi, _, _ = find_method(il, 'Dungeon.DungeonProgress', 'Clone', 0)
    body = lift_text(il, dec, mi)
    assert 'sub_180002950' not in body
