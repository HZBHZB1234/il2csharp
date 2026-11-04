"""Long call arguments retain one native call and its definition order."""
import re
import pytest
from game_support import lift_text


@pytest.mark.game('unitask')
def test_distinct_warning_branches_keep_one_concat_each(raw_game_decompiler):
    il, dec = raw_game_decompiler
    text = lift_text(il, dec, 19951)
    assert text.count('string.Concat(') == 2
    assert text.count('UnityEngine.Debug.LogWarning(') == 2
    assert lift_text(il, dec, 19951) == text


@pytest.mark.game('unitask')
def test_async_enumerable_pipeline_does_not_repeat_producers(raw_game_decompiler):
    il, dec = raw_game_decompiler
    text = lift_text(il, dec, 30539)
    for name in ('Range', 'Where', 'Select'):
        assert len(re.findall(r'\.' + name + r'(?:<[^>]+>)?\(', text)) == 1
    assert lift_text(il, dec, 30539) == text


@pytest.mark.game('survivors-roguelike-kit')
def test_pool_warning_has_one_concat(raw_game_decompiler):
    il, dec = raw_game_decompiler
    text = lift_text(il, dec, 71216)
    assert text.count('string.Concat(') == 2
    assert text.count("string.Concat(\"[PoolRuntimeSO] Pool with key '") == 1
    assert text.count('UnityEngine.Debug.LogWarning(') == 1
    assert lift_text(il, dec, 71216) == text


@pytest.mark.game('survivors-roguelike-kit')
@pytest.mark.parametrize('mi', [70065, 70069])
def test_rush_sequence_is_not_appended_twice(raw_game_decompiler, mi):
    il, dec = raw_game_decompiler
    text = lift_text(il, dec, mi)
    assert text.count('.AppendCallback(') == 1
    assert text.count('.AppendInterval(') == 1
    assert lift_text(il, dec, mi) == text


@pytest.mark.game('survivors-roguelike-kit')
def test_color_tween_creation_is_not_duplicated(raw_game_decompiler):
    il, dec = raw_game_decompiler
    text = lift_text(il, dec, 90891)
    assert text.count('DG.Tweening.DOTween.To(') == 1
    assert lift_text(il, dec, 90891) == text


@pytest.mark.game('survivors-roguelike-kit')
def test_circle_tween_reuses_the_created_value(raw_game_decompiler):
    il, dec = raw_game_decompiler
    text = lift_text(il, dec, 90945)
    assert text.count('DG.Tweening.Plugins.CirclePlugin.Get(') == 1
    assert 'tweenerCore2' not in text
    assert lift_text(il, dec, 90945) == text


@pytest.mark.game('survivors-roguelike-kit')
def test_long_tween_call_is_bound_before_the_next_native_call(raw_game_decompiler):
    il, dec = raw_game_decompiler
    text = lift_text(il, dec, 90933)
    assert text.count('.OnStart<') == 1
    assert text.index('.OnStart<') < text.rindex('sub_180421090')
    assert lift_text(il, dec, 90933) == text


@pytest.mark.game('survivors-roguelike-kit')
def test_rush_tween_creation_is_not_duplicated(raw_game_decompiler):
    il, dec = raw_game_decompiler
    text = lift_text(il, dec, 70062)
    assert text.count('DG.Tweening.ShortcutExtensions.DOScale(') == 1
    assert text.count('DG.Tweening.TweenSettingsExtensions.Append(') == 1
    assert lift_text(il, dec, 70062) == text
