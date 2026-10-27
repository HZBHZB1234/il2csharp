"""Fix 162 (C2): recursive inner-offset field resolution.

`instance_field_chain` merges a class's whole base chain but stops at
each field, so an offset INSIDE an embedded value type -- the
roadmap's `0x18` inside a field at `0x10` -> `.field.z` -- found no
entry and rendered `((byte*)recv + 0x18)[0]`. `nested_field_path`
walks it: the chain's nearest value-typed field at or below the
offset, then that struct's own chain for the remainder, recursively.

Guards: only a value type whose size covers the remainder is followed
(union-like or over-approximated layouts decline); a class-typed field
is never followed (its object is a pointer, not inline storage); the
depth is bounded. The offset convention mirrors the flat branch
exactly: a value-type receiver maps its read offset into the chain at
`disp + 0x10`, a class receiver at `disp`.
"""
from types import SimpleNamespace as NS

import pytest

from il2cpp import Il2Cpp

# type rows: (td_or_index, enum<<16)
VT = (1, 0x11 << 16)
CLS = (2, 0x12 << 16)
INT = (3, 0x08 << 16)
PTR = (4, 0x0f << 16)


def make_il(typedefs, fields, field_offsets, types, sizes):
    il = Il2Cpp.__new__(Il2Cpp)
    il.meta = NS(typedefs=typedefs, fields=fields,
                 type_fields=lambda td: range(td.field_start,
                                              td.field_start + td.field_count))
    il.types = types
    il.field_offsets = field_offsets
    il.value_type_size = lambda tdi: sizes.get(tdi)
    il.td_of_ty = lambda ty: ty[0] if ty else None
    il.instance_field_chain = lambda tdi: _chains.get(tdi)
    il._chain_cache = {}
    return il


def _td(index, is_valuetype, parent=-1, field_start=0, field_count=0):
    return NS(index=index, name='T%d' % index, namespace='',
              is_valuetype=is_valuetype, parent=parent,
              field_start=field_start, field_count=field_count)


_chains = {}


def _field(name, type_idx, attrs=0x1):
    return NS(name=name, type=type_idx, flags=attrs)


# ---------------------------------------------------------------- basics

def test_flat_field_resolves():
    outer = _td(0, False, field_start=0, field_count=2)
    fields = [_field('a', 3), _field('b', 3)]
    _chains.clear()
    _chains[0] = {0x10: ('a', 3), 0x18: ('b', 3)}
    il = make_il([outer], fields, [[0x10, 0x18]], [INT, VT, CLS, INT], {})
    assert il.nested_field_path(0, 0x18) == ('b', 3)


def test_inner_offset_of_a_value_type_field_resolves():
    """The roadmap's C2 case: `0x18` inside a field at `0x10`."""
    outer = _td(0, False)
    inner = _td(1, True)
    _chains.clear()
    _chains[0] = {0x10: ('vec', 1)}
    _chains[1] = {0x0: ('x', 3), 0x4: ('y', 3), 0x8: ('z', 3)}
    types = [None, (1, 0x11 << 16), (2, 0x12 << 16), INT, PTR]
    il = make_il([outer, inner], [], [], types, {1: 12})
    assert il.nested_field_path(0, 0x18) == ('vec.z', 3)
    assert il.nested_field_path(0, 0x14) == ('vec.y', 3)


def test_deeper_nesting_resolves():
    outer = _td(0, False)
    mid = _td(1, True)
    leaf = _td(2, True)
    _chains.clear()
    _chains[0] = {0x10: ('m', 1)}
    _chains[1] = {0x4: ('n', 2)}
    _chains[2] = {0x0: ('v', 3)}
    types = [None, (1, 0x11 << 16), (2, 0x11 << 16), INT, PTR]
    il = make_il([outer, mid, leaf], [], [], types, {1: 32, 2: 16})
    # the field itself, then a genuinely deeper inner offset
    assert il.nested_field_path(0, 0x10) == ('m', 1)
    assert il.nested_field_path(0, 0x14) == ('m.n', 2)
    assert il.nested_field_path(0, 0x14) == ('m.n', 2)


def test_class_typed_field_is_not_followed():
    """A class field holds a POINTER -- its members are not inline."""
    outer = _td(0, False)
    cls = _td(1, False)
    _chains.clear()
    _chains[0] = {0x10: ('obj', 1)}
    _chains[1] = {0x0: ('x', 3)}
    types = [None, (1, 0x12 << 16), CLS, INT, PTR]
    il = make_il([outer, cls], [], [], types, {1: 8})
    assert il.nested_field_path(0, 0x18) is None


def test_offset_past_the_value_type_declines():
    """The remainder must fall inside the struct's own size."""
    outer = _td(0, False)
    inner = _td(1, True)
    _chains.clear()
    _chains[0] = {0x10: ('v', 1)}
    _chains[1] = {0x0: ('x', 3)}
    types = [None, (1, 0x11 << 16), CLS, INT, PTR]
    il = make_il([outer, inner], [], [], types, {1: 4})
    assert il.nested_field_path(0, 0x18) is None   # 8 past the 4-byte struct


def test_unknown_size_declines():
    outer = _td(0, False)
    inner = _td(1, True)
    _chains.clear()
    _chains[0] = {0x10: ('v', 1)}
    _chains[1] = {0x0: ('x', 3)}
    types = [None, (1, 0x11 << 16), CLS, INT, PTR]
    il = make_il([outer, inner], [], [], types, {})
    assert il.nested_field_path(0, 0x14) is None


def test_depth_is_bounded():
    """A self-referential value type must not recurse forever."""
    a = _td(0, True)
    _chains.clear()
    _chains[0] = {0x0: ('self', 0)}
    types = [(0, 0x11 << 16), (1, 0x11 << 16), CLS, INT, PTR]
    il = make_il([a], [], [], types, {0: 64})
    assert il.nested_field_path(0, 0x8) is None


def test_no_chain_declines():
    il = make_il([_td(0, False)], [], [], [INT], {})
    _chains.clear()
    assert il.nested_field_path(0, 0x10) is None
