"""Small call aggregates consume scalar snapshots, not guessed projections."""
import re

import pytest

from il2cpp import Lifter
from game_support import find_method, lift_text

pytestmark = pytest.mark.game('survivors-roguelike-kit')


@pytest.mark.parametrize('owner', ['CircleShotSateNode', 'SpreadShotStateNode'])
def test_bullet_call_consumes_both_captured_components(raw_game_decompiler, owner):
    il, dec = raw_game_decompiler
    mi, _, _ = find_method(il, owner, 'PerformShoot', 0)
    text = lift_text(il, dec, mi)
    assert re.search(r'\.CreateBullet\(new UnityEngine\.Vector2 \{ '
                     r'x = real\d+, y = real\d+ \}\)', text)
    assert '.CreateBullet(unknown)' not in text
    # This checks the call argument, not the existing loop reconstruction.


def test_size_delta_consumes_both_scalar_locals(raw_game_decompiler, monkeypatch):
    il, dec = raw_game_decompiler
    mi, _, _ = find_method(il, 'TMPro.Examples.TMP_ExampleScript_01', 'Awake', 0)
    text = lift_text(il, dec, mi)
    with monkeypatch.context() as patch:
        patch.setattr(Lifter, '_copied_scalar_struct_arg', lambda *args: None)
        before = lift_text(il, dec, mi)
    assert re.search(r'\.sizeDelta = new UnityEngine\.Vector2 \{ '
                     r'x = real\d+, y = real\d+ \};', text)
    # The existing upstream getter duplication is not repaired by this slice;
    # nor may the initializer introduce yet another evaluation of the getter.
    assert text.count('.GetPreferredValues(') == before.count('.GetPreferredValues(')


@pytest.mark.parametrize('owner, name', [
    ('DG.Tweening.DOTweenModulePhysics2D', 'DOJump'),
    ('DG.Tweening.DOTweenModuleUI', 'DOJumpAnchorPos'),
])
def test_jump_call_combines_exact_zero_and_float_parameter(raw_game_decompiler, owner, name):
    il, dec = raw_game_decompiler
    mi, _, _ = find_method(il, owner, name, 6)
    text = lift_text(il, dec, mi)
    assert 'new UnityEngine.Vector2 { x = 0.0f, y = jumpPower }' in text
    assert not re.search(r'new UnityEngine\.Vector2 \{[^}]*\.endValue', text)


@pytest.mark.parametrize('name', ['StartRush', '<StartRushSequence>b__13_0'])
def test_vector_arithmetic_keeps_existing_spelling(raw_game_decompiler, monkeypatch, name):
    il, dec = raw_game_decompiler
    mi, _, _ = find_method(il, 'RushStateNode', name, 0)
    text = lift_text(il, dec, mi)
    with monkeypatch.context() as patch:
        patch.setattr(Lifter, '_copied_scalar_struct_arg', lambda *args: None)
        before = lift_text(il, dec, mi)
    assert text == before
    assert '.rushSpeed.x' not in text
