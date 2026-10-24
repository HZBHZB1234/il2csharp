"""Focused Limbus v39 native-to-C# body checks.

Every method is looked up by type and name (and arity where overloaded).  The
fixture baseline makes the exact text meaningful; the lookups keep the test
readable and keep a future MethodDef-row move from silently changing targets.
"""
import pytest

from game_support import find_method, lift_text

pytestmark = pytest.mark.game("limbus")


def test_dungeon_progress_is_empty(baseline_game_decompiler):
    il, dec = baseline_game_decompiler
    mi, _, _ = find_method(il, 'Dungeon.DungeonProgress', 'IsEmpty', 0)
    assert lift_text(il, dec, mi) == 'return this.dungeonID == 0;'


def test_dungeon_progress_clone_copies_every_list(baseline_game_decompiler):
    il, dec = baseline_game_decompiler
    mi, _, _ = find_method(il, 'Dungeon.DungeonProgress', 'Clone', 0)
    body = lift_text(il, dec, mi)
    assert '__ret.units = null;' in body
    assert '__ret.AcquiredEgoGiftList = list11;' in body
    assert '__ret.passingRoute = list17;' in body
    assert '__ret.unlockedNodeIDList = list112;' in body
    assert '__ret.clearedNodeList = list117;' in body
    assert 'return __ret;' in body


def test_inventory_get_item_walks_the_backing_list(baseline_game_decompiler):
    il, dec = baseline_game_decompiler
    mi, _, _ = find_method(il, 'RPGSystem.RpgInventoryManager', 'GetItem', 1)
    body = lift_text(il, dec, mi)
    assert 'for (num1 = 0; num1 < list11._size; num1++)' in body
    assert '== itemId' in body
    assert 'list11._items[num1]' in body


def test_inventory_add_item_uses_stack_room(baseline_game_decompiler):
    il, dec = baseline_game_decompiler
    mi, _, _ = find_method(il, 'RPGSystem.RpgInventoryManager', 'AddItem', 3)
    body = lift_text(il, dec, mi)
    assert 'this.GetItemCount(data.itemId)' in body
    assert 'data.maxStack - num1' in body
    assert 'this.__field_OnItemAdded' in body
    assert 'return num19;' in body


def test_story_return_handle_disables_lobby_voice(baseline_game_decompiler):
    il, dec = baseline_game_decompiler
    mi, _, _ = find_method(
        il, 'LimbusCompany.Logics.ReturnFromStoryLibs.EnterStorySceneFromInventory',
        'Handle', 2)
    body = lift_text(il, dec, mi)
    assert 'GlobalGameManager._instance' in body
    assert '_canPlayLobbyPersonalityVoice = false;' in body
    assert 'UnityEngine.UI.SetPropertyUtility.SetStruct<float>' in body
