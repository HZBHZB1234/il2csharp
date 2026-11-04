"""Caller-owned return restoration retains opaque native helper semantics."""
import re

import pytest
from game_support import lift_text


@pytest.mark.game('survivors-roguelike-kit')
@pytest.mark.parametrize('mi', [70595, 70778])
def test_sqrt_domain_call_defines_the_joined_single(raw_game_decompiler, mi):
    il, dec = raw_game_decompiler
    text = lift_text(il, dec, mi)
    call = re.search(r'float (\w+) = \(float\)sub_[0-9a-f]+\([^;]+\);', text)
    # Other float helpers precede the domain call in 70778. Require the
    # assignment in the negative arm, followed by its joined float copy.
    arm = re.search(r'if \(0f > [^\n]+\)\s*\{\s*float (\w+) = '
                    r'\(float\)(sub_[0-9a-f]+\([^;]+\));\s*(\w+) = \1;', text)
    assert call is not None and arm is not None
    joined = arm[3]
    assert re.search(r'else\s*\{\s*' + joined +
                     r' = \(float\)global::System.Math.Sqrt\(', text)
    assert '(double)(' + joined + ')' in text
    assert text.count(arm[2]) == 1
    # No Math.Sqrt replacement on the negative arm, no invented input cast.
    assert 'System.Math.Sqrt' not in text[text.index('if (0f >'):text.index('else', text.index('if (0f >'))]
    assert lift_text(il, dec, mi) == text


@pytest.mark.game('limbus')
def test_two_domain_calls_both_keep_scalar_result_channels(raw_game_decompiler):
    il, dec = raw_game_decompiler
    text = lift_text(il, dec, 22321)
    calls = re.findall(r'float \w+ = \(float\)sub_[0-9a-f]+\([^;]+\);', text)
    assert len(calls) == 2
    assert lift_text(il, dec, 22321) == text
