"""Primitive instance calls on a struct's first field (fix 172).

The helper is metadata-driven; this test drives its proofs without a game
fixture: a value-type receiver, an object-relative field table whose first
field is at 0x10, and a callee owned by that field's primitive type.
"""
from types import SimpleNamespace as NS

from il2cpp.lifter.calls import _CallsMixin


def _fake_self(chain, first_type_name='float'):
    types = [(0, 0x000C0000), (1, 0x00110000)]   # float, struct
    typedefs = [
        NS(namespace='System', name='Single', is_valuetype=True),
        NS(namespace='UnityEngine', name='Vector3', is_valuetype=True),
    ]

    def td_of(ty):
        if ty is None:
            return None
        data, bits = ty
        return data if ((bits >> 16) & 0xFF) in (0x11, 0x12) else None

    il = NS(
        types=types,
        instance_field_chain=lambda td: chain,
        type_name=lambda ty: first_type_name,
    )
    return NS(il=il, meta=NS(typedefs=typedefs), _td_of=td_of)


def _recv():
    return NS(text='self', ty=(1, 0x00110000))


def test_first_value_type_field_is_the_receiver():
    self_ = _fake_self({16: ('x', 0), 20: ('y', 0), 24: ('z', 0)})
    m2 = NS(is_static=False, declaring=0, name='Equals')
    assert _CallsMixin._value_receiver_field(self_, _recv(), m2) == 'x'


def test_declines_when_first_field_is_a_different_type():
    self_ = _fake_self({16: ('other', 0), 20: ('y', 0)})
    self_.il.type_name = lambda ty: 'int'
    m2 = NS(is_static=False, declaring=0, name='Equals')
    assert _CallsMixin._value_receiver_field(self_, _recv(), m2) is None


def test_declines_when_offset_zero_is_padding():
    self_ = _fake_self({24: ('z', 0)})
    m2 = NS(is_static=False, declaring=0, name='Equals')
    assert _CallsMixin._value_receiver_field(self_, _recv(), m2) is None


def test_declines_for_static_calls_and_same_owner():
    self_ = _fake_self({16: ('x', 0)})
    assert _CallsMixin._value_receiver_field(
        self_, _recv(), NS(is_static=True, declaring=0, name='M')) is None
    assert _CallsMixin._value_receiver_field(
        self_, _recv(), NS(is_static=False, declaring=1, name='M')) is None
