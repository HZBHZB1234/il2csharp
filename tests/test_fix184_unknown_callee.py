"""fix 184: a call on an unresolved callee compiles as the unknown marker.

The lifter renders a call whose callee register was never resolved as
`?(args)`, which is not a C# expression:

    object obj1 = ?(pUnk);      // mscorlib Marshal.ReleaseInternal

Five sites tree-wide, but they broke the parse of three emitted images (and one
of them produced a tree whose free crashed tree-sitter). The call's value is
exactly an unresolved value, so `spell_unresolved_values` routes it through the
existing marker: value position `= /*unknown*/ default;`, statement position
`/*unknown call*/;`. A ternary (`b ? (c) : d`) and literals are untouched.
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from il2cpp.text import spell_unresolved_values  # noqa: E402


def test_a_value_call_becomes_a_typed_default():
    assert spell_unresolved_values('object obj1 = ?(pUnk);') == \
        'object obj1 = /*unknown*/ default;'


def test_a_statement_call_becomes_the_marker_statement():
    assert spell_unresolved_values('?(pUnk);') == '/*unknown call*/;'


def test_a_returned_call_becomes_a_typed_default():
    assert spell_unresolved_values('return ?(x);') == \
        'return /*unknown*/ default;'


def test_a_ternary_is_not_a_call():
    for line in ('int a = b ? (c) : d;', 'x = a == b ? c : d;',
                 'bool f = (a ? b : c);'):
        assert spell_unresolved_values(line) == line, line


def test_a_literal_is_untouched():
    for line in ('string s = "?(x)";', '// ?(x)'):
        assert spell_unresolved_values(line) == line, line


def test_a_member_call_keeps_its_receiver():
    """`x.M(...)` is a resolved call, never the `?` placeholder."""
    line = 'int n = obj1.M(2);'
    assert spell_unresolved_values(line) == line
