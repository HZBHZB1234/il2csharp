"""fix 168: an enum with NO recorded `td.element` still resolves its
underlying type, so both the member table and the `enum E : long`
declaration work.

The v39 Limbus metadata records `element == -1` for ALL 3,227 enum rows.
`enum_members` gated its per-member decode on `td.element` and so
`continue`d every member, returning None for every enum in the game --
which meant no enum cast, no member-name fold and no non-int base
declaration ever rendered (6,034 CS0266 + 287 CS1750, plus 7 more CS0266
from a `long` enum printing a bare `enum E`). The enum's own `value__`
instance field carries the same underlying type and is authoritative.

Il2CppType `bits` carry the type code in bits 16..23: `0x80080000` is
System.Int32 (te 0x08) and `0x800A0000` is System.Int64 (te 0x0a). Field
ATTRIBUTES live in the low 16 bits of the same word (`field_attrs`), so a
static-literal member is `0x00000050` (0x10 static | 0x40 literal) on top
of its type code.
"""
from types import SimpleNamespace as NS

from il2cpp.emitter import Emitter
from il2cpp.runtime.types import _TypesMixin

T_INT32 = (0, 0x80080000)
T_INT64 = (0, 0x800A0000)
T_VOID = (0, 0x00010000)
ATTR_STATIC_LITERAL = 0x0010 | 0x0040


def _td_enum(index=0, name="E", element=-1, fis=()):
    return NS(index=index, name=name, namespace="", flags=0x101,
              parent=-1, declaring=-1, is_enum=True, is_valuetype=True,
              element=element, generic_container=-1,
              field_start=0, field_count=len(fis), method_start=0,
              method_count=0, property_count=0, event_count=0,
              nested_count=0, interfaces_count=0, interfaces_start=0,
              fis=list(fis), mis=[])


def _make_il(element, underlying=T_INT32, members=("A",)):
    """A `_TypesMixin` wired to a synthetic enum whose ONLY interesting
    property is whether `element` is recorded."""
    value_f = NS(index=0, name="value__", type=1, flags=0x0)
    fields = [value_f]
    dv = {}
    for k, nm in enumerate(members, start=1):
        fields.append(NS(index=k, name=nm, type=1, flags=0x0))
        dv[k] = (1, 0)          # one blob row, at dv_off 0, value 0
    td = _td_enum(element=element, fis=fields)
    meta = NS(d=bytes(64), version=29, dv_off=0, typedefs=[td],
              fields=fields, field_default_values=dv,
              type_fields=lambda t: [f.index for f in t.fis])
    il = _TypesMixin.__new__(_TypesMixin)
    il.meta = meta
    # index 1 carries the underlying type code PLUS the static|literal
    # attributes field_attrs reads, so members are recognised as literals.
    il.types = [T_VOID, (underlying[0], underlying[1] | ATTR_STATIC_LITERAL)]
    return il, td, value_f


def test_enum_members_reads_the_underlying_type_from_value__():
    """The gate itself: with `element == -1`, `te_u` must still be known,
    so the member decodes instead of every row `continue`ing."""
    il, _, _ = _make_il(element=-1, underlying=T_INT32)
    assert il.enum_members(0) == {0: "A"}


def test_enum_members_keeps_using_a_recorded_element_when_present():
    """A metadata that DOES record `element` keeps that path; the fallback
    is only for the absent case."""
    il, _, _ = _make_il(element=1, underlying=T_INT32)   # element -> types[1]
    assert il.enum_members(0) == {0: "A"}


def test_enum_members_declines_when_the_underlying_is_unknowable():
    """`value__` missing and `element` absent -> no guess, still None."""
    il, td, value_f = _make_il(element=-1, underlying=T_INT32)
    value_f.name = "not_value__"
    il._enum_members_cache = {}
    assert il.enum_members(0) is None


def _emit_header(element, underlying):
    value_f = NS(index=0, name="value__", type=1, flags=0x0)
    td = _td_enum(name="Bits", element=element, fis=[value_f])
    meta = NS(type_fields=lambda t: [f.index for f in t.fis],
              fields=[value_f], typedefs=[td], methods=[], interfaces=[],
              field_default_values={}, type_methods=lambda t: [],
              getstr=lambda i: "P")
    il = NS(types=[T_VOID, underlying], type_name=lambda t: "int",
            base_chain_tds=lambda t: (t,),
            _type_enum=lambda t: (t[1] >> 16) & 0xFF if t else 0,
            _nested_owner=lambda i: None)
    e = Emitter.__new__(Emitter)
    e.il = il
    e.meta = meta
    il.meta = meta
    lines = []
    e.emit_type(td, lines)
    return [l.strip() for l in lines if l.strip().startswith("public enum")]


def test_enum_header_declares_long_when_element_is_absent():
    """`enum BattleEventBit : long` -- 64-bit members cannot convert in a
    bare `enum E` (CS0266)."""
    assert _emit_header(-1, T_INT64) == ["public enum Bits : long"]


def test_enum_header_stays_bare_int_when_underlying_is_int():
    """int is C#'s default, so an int enum must NOT grow a base clause."""
    assert _emit_header(-1, T_INT32) == ["public enum Bits"]


def test_enum_header_keeps_a_recorded_element():
    assert _emit_header(1, T_INT64) == ["public enum Bits : long"]
