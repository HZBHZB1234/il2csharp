"""Real MOVD fields preserve float conversion before native consumers."""
import re

import pytest
from game_support import lift_text


@pytest.mark.game('limbus')
@pytest.mark.parametrize('mi', [65142, 65143, 65145])
def test_coin_scale_division_uses_the_converted_float_denominator(raw_game_decompiler, mi):
    il, dec = raw_game_decompiler
    text = lift_text(il, dec, mi)
    match = re.search(r'float (\w+) = \(float\)\(this\._DEVIDE_BY_DIFF_SPEED\);', text)
    assert match is not None
    assert text.count('/ ' + match[1] + ')') == 2
    assert lift_text(il, dec, mi) == text


@pytest.mark.game('limbus')
@pytest.mark.parametrize('mi,field', [
    (40548, '_attackDmgMulPercentV3'), (153530, '_triggerChancePercent'),
])
def test_percentage_field_has_an_explicit_conversion_snapshot(raw_game_decompiler, mi, field):
    il, dec = raw_game_decompiler
    text = lift_text(il, dec, mi)
    assert re.search(r'float \w+ = \(float\)\(this\.' + field + r'\);', text)
    assert lift_text(il, dec, mi) == text


@pytest.mark.game('survivors-roguelike-kit')
@pytest.mark.parametrize('mi', [69717, 69747])
def test_frame_counter_is_converted_before_fps_division(raw_game_decompiler, mi):
    il, dec = raw_game_decompiler
    text = lift_text(il, dec, mi)
    match = re.search(r'float (\w+) = \(float\)\(this\.m_Frames\);', text)
    assert match is not None
    assert match[1] + ' / (' in text
    assert text.index('(float)(this.m_Frames)') < text.index('this.m_Frames = 0;')
    assert lift_text(il, dec, mi) == text


@pytest.mark.game('survivors-roguelike-kit')
def test_skill_percent_uses_the_int_field_snapshot(raw_game_decompiler):
    il, dec = raw_game_decompiler
    text = lift_text(il, dec, 70755)
    assert text.count('(float)(attackSkillAttributeMod1.IntValue)') == 2
    assert lift_text(il, dec, 70755) == text
