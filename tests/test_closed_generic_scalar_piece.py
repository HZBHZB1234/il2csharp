"""Only exact scalar members of a proved closed generic layout name a slice."""
from types import SimpleNamespace as NS

import pytest

from il2cpp import Expr
from test_recovery_followup import lifter

SHORT = (0, 0x06 << 16)
INT = (0, 0x08 << 16)
CORE = (0x1000, 0x15 << 16)


def setup(*, closed=True, flags=0, bitfield=0xc01):
    il = NS(types=[], _type_enum=lambda t: (t[1] >> 16) & 0xff if t else 0,
            _generic_inst_args=lambda ty: (SHORT,),
            instance_field_chain=lambda td: {},
            _sf_field_size=lambda t, depth: 40 if t == CORE else 2 if t == SHORT else 4,
            _closed_type_key=lambda t: t if closed or t != CORE else None,
            _sf_field_path=lambda ty, key, depth, seen:
                ('version', SHORT) if ty == CORE and key == 0x20 else None)
    lift = lifter(il=il)
    lift.meta.typedefs = [NS(is_valuetype=True, flags=flags, bitfield=bitfield,
                             field_start=0, field_count=0)]
    lift._td_of = lambda ty: 0 if ty == CORE else None
    return lift


def test_exact_closed_generic_member_has_its_own_type_and_keeps_fragment_provenance():
    lift = setup()
    origin = Expr('source.core', CORE, 'obj')
    piece = lift._fragment(origin, 0x10, 2)
    assert piece.text == 'source.core.version'
    assert piece.ty == SHORT
    assert piece.kind == 'int'
    assert piece._slice == (origin, 0x10, 2)
    assert lift._piece_value(origin, 0x10, 2, SHORT).text == piece.text


@pytest.mark.parametrize('offset,width', [(0x10, 1), (0x10, 4), (0x11, 1),
                                         (0x12, 2), (40, 2), (-1, 2)])
def test_partial_spanning_padding_and_outside_accesses_do_not_name_the_member(offset, width):
    assert setup()._piece_value(Expr('core', CORE, 'obj'), offset, width, None) is None


@pytest.mark.parametrize('kwargs', [dict(closed=False), dict(flags=0x10),
                                     dict(bitfield=1), dict(bitfield=0x401)])
def test_unproved_or_custom_layout_declines(kwargs):
    assert setup(**kwargs)._piece_value(Expr('core', CORE, 'obj'), 0x10, 2, None) is None


def test_incompatible_expected_scalar_is_not_inferred_from_the_consumer():
    assert setup()._piece_value(Expr('core', CORE, 'obj'), 0x10, 2, INT) is None


def test_whole_tile_is_not_replaced_with_its_first_member():
    origin = Expr('core', CORE, 'obj')
    assert setup()._piece_value(origin, 0, 40, None) is origin


def test_unknown_value_does_not_gain_a_generic_member_name():
    origin = Expr('core', CORE, 'obj'); origin._unk = True
    assert setup()._piece_value(origin, 0x10, 2, None) is None


def test_nested_custom_layout_declines_even_when_outer_layout_is_default():
    lift = setup()
    nested = (1, 0x11 << 16)
    lift.meta.typedefs.append(NS(is_valuetype=True, flags=0x10, bitfield=0xc01,
                                field_start=1, field_count=0))
    lift.meta.typedefs[0].field_count = 1
    lift.meta.fields = [NS(type=0)]
    lift.il.types = [nested]
    lift.il._sf_subst = lambda ty, args: ty
    lift._td_of = lambda ty: 0 if ty == CORE else 1 if ty == nested else None
    assert not lift._piece_layout_proven(CORE)
    assert lift._piece_value(Expr('core', CORE, 'obj'), 0x10, 2, None) is None


def test_nested_pack_can_change_a_later_scalar_offset_so_it_also_declines():
    lift = setup()
    nested = (1, 0x11 << 16)
    lift.meta.typedefs.append(NS(is_valuetype=True, flags=0, bitfield=0x801,
                                field_start=1, field_count=0))
    lift.meta.typedefs[0].field_count = 1
    lift.meta.fields = [NS(type=0)]
    lift.il.types = [nested]
    lift.il._sf_subst = lambda ty, args: ty
    lift._td_of = lambda ty: 0 if ty == CORE else 1 if ty == nested else None
    assert lift._piece_value(Expr('core', CORE, 'obj'), 0x10, 2, None) is None


def test_default_nested_layout_is_allowed_but_recursive_value_layout_is_not():
    lift = setup()
    nested = (1, 0x11 << 16)
    lift.meta.typedefs.append(NS(is_valuetype=True, flags=0, bitfield=0xc01,
                                field_start=1, field_count=0))
    lift.meta.typedefs[0].field_count = 1
    lift.meta.fields = [NS(type=0), NS(type=1)]
    lift.il.types = [nested, CORE]
    lift.il._sf_subst = lambda ty, args: ty
    lift._td_of = lambda ty: 0 if ty == CORE else 1 if ty == nested else None
    assert lift._piece_layout_proven(CORE)
    lift.meta.typedefs[1].field_count = 1
    assert not lift._piece_layout_proven(CORE)


def test_native_sized_empty_leaf_has_alignment_one_without_default_size_flag():
    lift = setup()
    empty = (1, 0x11 << 16)
    lift.meta.typedefs.append(NS(is_valuetype=True, flags=8, bitfield=0x19,
                                field_start=1, field_count=0))
    lift.meta.typedefs[0].field_count = 1
    lift.meta.fields = [NS(type=0)]
    lift.il.types = [empty]
    lift.il.type_sizes = [None, 1]
    lift.il._sf_subst = lambda ty, args: ty
    lift._td_of = lambda ty: 0 if ty == CORE else 1 if ty == empty else None
    assert lift._piece_layout_proven(CORE)
    lift.il.type_sizes[1] = None
    assert not lift._piece_layout_proven(CORE)
