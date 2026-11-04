"""Native block-entry stack coordinates survive dry/real RPO execution."""
from collections import Counter
import re

import pytest

from game_support import lift_text
from il2cpp.dec import analyze


@pytest.mark.parametrize('mi,needles', [
    pytest.param(23044, ('.Equals(vector.y)',), marks=pytest.mark.game('unitask')),
    pytest.param(23068, ('= self.m_Y;', ', vector.m_Y);'), marks=pytest.mark.game('unitask')),
    pytest.param(23075, (', vector.length);',), marks=pytest.mark.game('unitask')),
    pytest.param(69628, (), marks=pytest.mark.game('survivors-roguelike-kit')),
])
def test_proved_entries_apply_once_per_block_in_both_passes(
        raw_game_decompiler, monkeypatch, mi, needles):
    il, dec = raw_game_decompiler
    original_prove, original_sink = analyze.prove_block_entry_rsp, analyze._Sink
    proofs, visits = [], Counter()

    def prove(*args, **kwargs):
        result = original_prove(*args, **kwargs)
        assert result is not None
        proofs.append(result)
        return result

    def sink(block):
        assert len(proofs) == 1
        assert dec.L.rsp_delta == proofs[0][block.bid]
        visits[block.bid] += 1
        return original_sink(block)

    monkeypatch.setattr(analyze, 'prove_block_entry_rsp', prove)
    monkeypatch.setattr(analyze, '_Sink', sink)
    candidate = lift_text(il, dec, mi)
    assert visits == Counter({bid:2 for bid in proofs[0]})
    for needle in needles:
        assert needle in candidate
    if mi == 69628:
        match = re.search(r'object (\w+) = ch;', candidate)
        assert match and '&' + match[1] + ', 0)' in candidate
    monkeypatch.setattr(analyze, '_Sink', original_sink)
    monkeypatch.setattr(analyze, 'prove_block_entry_rsp', lambda *a, **k: None)
    baseline = lift_text(il, dec, mi)
    assert baseline != candidate
    for needle in needles:
        assert needle not in baseline
    # Correct coordinates must not replay or duplicate an effectful call.
    calls = lambda text: Counter(re.findall(r'\b([A-Za-z_][\w.]*)\s*(?:/\*.*?\*/)?\(', text))
    assert calls(candidate) == calls(baseline)
    monkeypatch.setattr(analyze, 'prove_block_entry_rsp', original_prove)
    assert lift_text(il, dec, mi) == candidate
