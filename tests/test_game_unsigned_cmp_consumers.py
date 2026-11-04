"""Unsigned queue growth cap conditions, not whole-method equivalence."""
import pytest
from game_support import lift_text

@pytest.mark.game('unitask')
@pytest.mark.parametrize('mi', [21729,22932])
def test_queue_growth_cmova_keeps_unsigned_relation(raw_game_decompiler,mi):
    il,dec=raw_game_decompiler
    text=lift_text(il,dec,mi)
    assert text.count('unchecked((uint)(')==2
    assert text.count('> 2146435071) ? 2146435071 :')==2
    assert lift_text(il,dec,mi)==text
