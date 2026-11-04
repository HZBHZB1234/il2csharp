"""Native dword unsigned branches preserve state/range/hash bit patterns."""
import pytest
from game_support import lift_text

@pytest.mark.game('unitask')
def test_async_state_dispatch_keeps_unsigned_dword(raw_game_decompiler):
    il,dec=raw_game_decompiler
    text=lift_text(il,dec,18693)
    assert 'unchecked((uint)(this.<>1__state)) <= 1' in text
    assert lift_text(il,dec,18693)==text

@pytest.mark.game('survivors-roguelike-kit')
@pytest.mark.parametrize('mi,condition', [
    (69630,'unchecked((uint)(num3)) <= 13'),
    (71057,'unchecked((uint)(character1)) <= 2112764879'),
])
def test_survivors_unsigned_dword_checks(raw_game_decompiler,mi,condition):
    il,dec=raw_game_decompiler
    text=lift_text(il,dec,mi)
    assert condition in text
    assert lift_text(il,dec,mi)==text
