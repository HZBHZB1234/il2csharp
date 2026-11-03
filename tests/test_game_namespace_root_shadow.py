"""Real repeated namespace segments must not hijack root type names."""
import pytest
from il2cpp import Emitter

pytestmark = pytest.mark.game('survivors-roguelike-kit')


def test_nested_state_machine_owner_uses_global_namespace_root(raw_game_decompiler, tmp_path):
    il, _ = raw_game_decompiler
    td = il.meta.typedefs[7889]
    assert td.name == 'BaseBulletShootState'
    assert td.namespace == 'RGame.RoguelikeKit'
    assert td.namespace + '.RGame' in il.all_namespaces
    emitter = Emitter(il, str(tmp_path), with_bodies=False)
    emitter._emit_one_top(td, 'Assembly-CSharp.dll', str(tmp_path), td.name)
    path = tmp_path / 'RGame/RoguelikeKit/BaseBulletShootState.cs'
    text = path.read_text(encoding='utf-8')
    assert 'global::RGame.RoguelikeKit.BaseBulletShootState __4__this;' in text
