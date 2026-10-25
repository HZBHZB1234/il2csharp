"""Fix 146 game ground truth: Type.GetType helper sites render managed.

AcquiredEgoGift..ctor (mi 98337) resolves ability types by name:
``sub_18078cf40(text2, obj53, AcquiredEgoGift.ctor)`` becomes
``System.Type.GetType(text2)`` with the local declared ``System.Type``.
DemoCamera.EnablePostProcessingForURP (mi 314868) names the
assembly-qualified string literally.
"""
import pytest

from game_support import find_method, lift_text

pytestmark = pytest.mark.game("limbus")


def test_acquired_ego_gift_resolves_ability_type(baseline_game_decompiler):
    il, dec = baseline_game_decompiler
    mi, _, _ = find_method(il, 'AcquiredEgoGift', '.ctor', 5)
    body = lift_text(il, dec, mi)
    assert 'sub_18078cf40' not in body
    assert 'System.Type type1 = System.Type.GetType(text2);' in body
    assert 'System.Type.GetType("EGOGiftAbility_Normal")' in body


def test_demo_camera_names_the_qualified_type(baseline_game_decompiler):
    il, dec = baseline_game_decompiler
    mi, _, _ = find_method(
        il, 'AllIn1SpriteShader.DemoCamera', 'EnablePostProcessingForURP', 0)
    body = lift_text(il, dec, mi)
    assert 'sub_18078cf40' not in body
    assert 'System.Type.GetType("UnityEngine.Rendering.Universal.' in body
