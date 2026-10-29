"""fix 169 (C8): the metadata arity backtick is stripped from TYPE
identifiers, so a generic spells the natural C# name.

Metadata spells `List`1`; C# spells `List`. fix 117 deliberately rendered
it as `List_1` so references matched our own re-emitted declarations -- a
self-consistent spelling that binds to nothing real. Against the real
Unity 6000 reference closure the `_N` form accounted for 28,361 CS0246
on the game's own Assembly-CSharp.

The strip is a PARAMETER, not a change to the default: `sanitize()` is
shared with member names (fields, methods, accessors) where a `_N` suffix
would be wrong for a different reason, so the type-only path goes
through `Emitter._type_ident`.

A second consequence, found by A/B: `_semantic_type_prefix` derives a
local's readable stem from its declared type text, so `List_1` produced
`words = ['List', '1']` -> stem `list1` -> the local `list11` (the arity
digit doubled into the counter). With the strip the stem is `list`, so
locals read `list1`. That is a naming improvement, and it moves every
such local's number.
"""
from types import SimpleNamespace as NS

from il2cpp.common import csharp_type_name
from il2cpp.emitter import Emitter
from test_review113_type_decls import make_emitter, td_base


def test_strip_arity_renders_the_natural_name():
    assert csharp_type_name("System.Collections.Generic.List`1",
                            strip_arity=True) == \
        "System.Collections.Generic.List"
    assert csharp_type_name("System.Collections.Generic.Dictionary`2",
                            strip_arity=True) == \
        "System.Collections.Generic.Dictionary"


def test_strip_arity_applies_inside_generic_arguments():
    assert csharp_type_name(
        "System.Collections.Generic.ICollection`1<System.Collections.Generic.KeyValuePair`2<TKey, TValue>>",
        strip_arity=True) == \
        ("System.Collections.Generic.ICollection<"
         "System.Collections.Generic.KeyValuePair<TKey, TValue>>")


def test_strip_arity_applies_to_nested_names():
    assert csharp_type_name("Outer+Inner`2", strip_arity=True) == "Outer.Inner"


def test_default_is_unchanged_for_non_type_callers():
    """The legacy `_N` form stays the default so nothing outside the
    type-identifier path moves by accident."""
    assert csharp_type_name("System.Collections.Generic.List`1") == \
        "System.Collections.Generic.List_1"


def test_keyword_mapping_survives_the_strip():
    assert csharp_type_name("System.Collections.Generic.List`1", strip_arity=True) \
        == "System.Collections.Generic.List"
    assert csharp_type_name("System.Int32", strip_arity=True) == "int"


def test_type_ident_matches_a_generic_declaration():
    """`class Box<T>` and every reference to it spell `Box`."""
    assert Emitter._type_ident("Box`1") == "Box"
    assert Emitter._type_ident("Pair`2") == "Pair"
    assert Emitter._type_ident("Plain") == "Plain"


def test_ctor_sig_uses_the_same_identifier_the_header_declares():
    from test_review114_method_flags import method
    e = make_emitter()
    td = td_base(name="Box`1")
    assert e.ctor_sig(method(6, ".ctor"), td) == "public Box()"
    assert e.ctor_sig(method(0x10, ".cctor"), td) == "static Box()"


def test_header_and_base_list_agree_on_the_stripped_identifier():
    """A generic declaring type and a generic base both lose the arity,
    so the emitted `class A<T> : B<T>` is self-consistent."""
    e = make_emitter()
    e.il.type_name = lambda t: "Base"
    td = td_base(name="Derived`1", parent=0)
    # `_type_generic_params` reads the generic container, so the mock needs
    # one to render `<T>`; without it the header is a bare non-generic class
    # and there is no arity to compare.
    e.meta.generic_containers = [(0, 1, 0, 0)]
    e.meta.generic_parameters = [(0, "T")]
    td.generic_container = 0
    lines = []
    e.emit_type(td, lines)
    hdr = [l for l in lines if "Derived" in l][0]
    assert "Derived<T>" in hdr, lines
    assert "Derived_1" not in hdr


def test_bare_typeof_of_a_generic_definition_keeps_the_arity():
    """A `typeof(<name>)` cell carries NO closed arguments, so stripping
    the arity would print `typeof(KeyValuePair)` -- invalid C#, since the
    type has no such closed form. That site keeps the metadata `_N`
    spelling (found as a real regression on test_game_bss_ties)."""
    assert Emitter._type_ident("KeyValuePair`2") == "KeyValuePair"
    # ...which is exactly why the typeof site cannot use `_type_ident`:
    # it must test generic_container first, and only then decide.
    from il2cpp.common import csharp_type_name
    assert csharp_type_name("System.Collections.Generic.KeyValuePair`2",
                            strip_arity=False) == \
        "System.Collections.Generic.KeyValuePair_2"
