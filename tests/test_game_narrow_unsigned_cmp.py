"""A saved char's range check keeps 16-bit unsigned underflow."""
import pytest
from game_support import lift_text

pytestmark=pytest.mark.game('survivors-roguelike-kit')

def test_digit_validator_preserves_unsigned_word_range(raw_game_decompiler, monkeypatch):
    il,dec=raw_game_decompiler
    from il2cpp.dec import analyze
    original_sink=analyze._Sink
    entries=[]
    def sink(block):
        assert dec.L._cmp_width is None
        entries.append(block.bid)
        return original_sink(block)
    monkeypatch.setattr(analyze,'_Sink',sink)
    text=lift_text(il,dec,69628)
    assert 'unchecked((ushort)(ch - 48)) <= 9' in text
    assert 'if (ch <= 57)' not in text
    assert lift_text(il,dec,69628)==text
    assert entries
