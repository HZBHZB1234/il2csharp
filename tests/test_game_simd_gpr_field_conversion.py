"""GPR MOVD field input must round before the native SQRTSS path."""
import re

import pytest
from game_support import lift_text


@pytest.mark.game('survivors-roguelike-kit')
def test_prop_count_rounds_to_single_before_sqrt(raw_game_decompiler):
    il, dec = raw_game_decompiler
    text = lift_text(il, dec, 70595)
    match = re.search(r'float (\w+) = \(float\)\(_config\.PropCount\);', text)
    assert match is not None
    assert 'System.Math.Sqrt(' + match[1] + ')' in text
    assert 'System.Math.Sqrt(_config.PropCount)' not in text
    assert text.index('(float)(_config.PropCount)') < text.index('System.Math.Sqrt(')
    assert lift_text(il, dec, 70595) == text
