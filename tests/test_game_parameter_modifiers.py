"""GameInput must implement the real InputSystem out-parameter contract."""
import pytest

from il2cpp import Emitter

pytestmark = pytest.mark.game('survivors-roguelike-kit')


@pytest.mark.parametrize('mi', [69561, 70304])
def test_find_binding_declaration_and_forwarding_match_input_system(raw_game_decompiler, mi):
    il, dec = raw_game_decompiler
    m = il.meta.methods[mi]
    td = il.meta.typedefs[m.declaring]
    assert m.name == 'FindBinding'
    action = il.meta.method_params(m)[1]
    assert il.types[action.type][1] & 3 == 2
    em = Emitter(il, '', with_bodies=False)
    assert 'out UnityEngine.InputSystem.InputAction action' in em.render_params(m)
    text = '\n'.join(dec.lift_method(m, td))
    assert ', out action)' in text
    assert ', ref action)' not in text
