"""Resolved native interface slots can supply exact delegate method groups."""
import re

import pytest

pytestmark = pytest.mark.game('survivors-roguelike-kit')


@pytest.mark.parametrize('mi, owner, expected', [(27494, 'PlayerActions', 12),
                                               (27511, 'UIActions', 54)])
def test_interface_callback_delegate_construction(raw_game_decompiler, mi, owner, expected):
    il, dec = raw_game_decompiler
    method = il.meta.methods[mi]
    td = il.meta.typedefs[method.declaring]
    assert method.name == 'SetCallbacks' and td.name == owner
    text = '\n'.join(dec.lift_method(method, td))
    assert len(re.findall(r'new System\.Action<[^;\n]+>\(@?[A-Za-z_]\w*\.On\w+\)', text)) == expected
    # Six unresolved mixed-path constructions still have no exact proof.
    # Do not force those to method groups just to erase shared markers.
    assert text.count('sub_18070bf10') == 6
