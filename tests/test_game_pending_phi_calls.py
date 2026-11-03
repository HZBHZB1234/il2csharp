"""Native-origin captures retain shooting calls inside their loop."""
import pytest
from game_support import find_method, lift_text
from il2cpp import Decompiler

pytestmark = pytest.mark.game('survivors-roguelike-kit')


@pytest.mark.parametrize('owner', ['CircleShotSateNode', 'SpreadShotStateNode'])
def test_pending_bullet_call_stays_in_its_native_loop(raw_game_decompiler, monkeypatch, owner):
    il, dec = raw_game_decompiler
    mi, _, _ = find_method(il, owner, 'PerformShoot', 0)
    text = lift_text(il, dec, mi)
    assert text.count('.CreateBullet(') == 1
    lines = text.splitlines()
    call = next(i for i, line in enumerate(lines) if '.CreateBullet(' in line)
    # The single native call occurs before the per-iteration exit decision,
    # not merely once after the structured loop has finished.
    assert sum(line.strip() == '{' for line in lines[:call]) - sum(
        line.strip() == '}' for line in lines[:call]) >= 2
    assert any('break;' in line for line in lines[call:])
    with monkeypatch.context() as patch:
        patch.setattr(Decompiler, '_materialize_pending_phi_calls', lambda *args: None)
        before = lift_text(il, dec, mi)
    assert before.count('.CreateBullet(') == 1
    before_lines = before.splitlines()
    old = next(i for i, line in enumerate(before_lines) if '.CreateBullet(' in line)
    assert any('break;' in line for line in before_lines[:old])
    assert not any('break;' in line for line in before_lines[old:])
