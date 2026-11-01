"""Open-source fixture: a primitive instance call on a struct's first field.

`UnityEqualityComparer.Vector3EqualityComparer.Equals` is
`self.x.Equals(vector.x) && ...`.  IL2CPP passes the hidden `this` of
`Single.Equals` as a pointer to `self.x`; at offset 0 that pointer is textually
the whole `Vector3`, so the body used to read `self.Equals(vector.x)` -- a
method that does not exist on the struct.  The receiver is the first field
when the callee's owner is a value type and that field has exactly the owner's
type.
"""
import pytest

from game_support import find_method, lift_text


pytestmark = pytest.mark.game("unitask")


def test_offset_zero_primitive_receiver_keeps_its_field(raw_game_decompiler):
    il, dec = raw_game_decompiler
    mi, _m, _td = find_method(il, 'Vector3EqualityComparer', 'Equals')
    text = lift_text(il, dec, mi)
    assert 'self.x.Equals(vector.x)' in text
    assert 'self.y.Equals(vector.y)' in text
    assert 'self.z.Equals(vector.z)' in text
    assert 'self.Equals(vector.x)' not in text
