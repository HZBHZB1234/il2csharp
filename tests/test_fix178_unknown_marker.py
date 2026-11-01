"""fix 178: the unresolved-value marker compiles without hiding itself.

An unresolved native value renders the bare text `unknown` (from
`_rewrite_unknowns`). It is honest and it parses, but it does not compile:
CS0103, 10,940 sites on the licensed game tree — the largest single
compiler-error family there.

At the file boundary, where no type context is left to recover, the marker
moves into a comment and the expression becomes a target-typed `default`.
Only shapes whose target type is certain qualify:

* an assignment RHS (`x = unknown;`) — every recovered declaration spells
  its type, and the tree contains no `var`;
* a `return` (`return unknown;`) — the signature's return type is declared;
* a member access on an unresolved value (`unknown.nFileSizeLow`) — the
  member name is fabricated, so the whole expression becomes the marker.

`unknown` inside a larger expression (`unknown + 1`, `f(unknown, 2)`, an
operand of `==`) keeps the old text: `default` there would need a type the
tree does not have.
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from il2cpp.text import spell_unresolved_values  # noqa: E402


def test_an_assignment_rhs_becomes_a_marked_default():
    assert spell_unresolved_values('            x = unknown;') == \
        '            x = /*unknown*/ default;'
    assert spell_unresolved_values('this.m_Value = unknown;') == \
        'this.m_Value = /*unknown*/ default;'


def test_a_return_becomes_a_marked_default():
    assert spell_unresolved_values('return unknown;') == \
        'return /*unknown*/ default;'
    assert spell_unresolved_values('                    return unknown;') == \
        '                    return /*unknown*/ default;'


def test_a_member_access_on_an_unknown_value_is_the_marker():
    """The member name is fabricated: keep the marker, drop the access."""
    assert spell_unresolved_values(
        'InitializeArray(array1, unknown.nFileSizeLow);') == \
        'InitializeArray(array1, /*unknown*/ default);'


def test_a_larger_expression_keeps_todays_text():
    for line in ('if (unknown + 1 > 2) {', 'f(unknown, 2);',
                 'if (unknown == null) {', 'unknown[0] = 1;'):
        assert spell_unresolved_values(line) == line, line


def test_a_plain_unknown_statement_is_untouched():
    assert spell_unresolved_values('unknown;') == 'unknown;'


def test_strings_and_comments_are_untouched():
    for line in ('text = "x = unknown;";',
                 '// x = unknown; is the marker',
                 'log = "unknown.nFileSizeLow";'):
        assert spell_unresolved_values(line) == line, line


def test_a_block_comment_spanning_lines_is_untouched():
    text = '/*\nx = unknown;\n*/\ny = unknown;'
    assert spell_unresolved_values(text) == \
        '/*\nx = unknown;\n*/\ny = /*unknown*/ default;'


def test_a_conditional_condition_becomes_a_typed_default():
    """A condition must be `bool`, so the type IS known (178b)."""
    assert spell_unresolved_values('(unknown ? a : b)') == \
        '(/*unknown*/ default(bool) ? a : b)'
    assert spell_unresolved_values('if (unknown ? flag1 : flag2) {') == \
        'if (/*unknown*/ default(bool) ? flag1 : flag2) {'
    assert spell_unresolved_values('bool f = unknown ? a : b;') == \
        'bool f = /*unknown*/ default(bool) ? a : b;'


def test_a_nullable_type_marker_is_not_a_condition():
    """`unknown?` (no space) is a type spelling, never a ternary."""
    for line in ('int? num1 = unknown?;', 'unknown? x = null;'):
        assert spell_unresolved_values(line) == line, line


def test_a_conditional_inside_a_literal_or_comment_is_untouched():
    for line in ('string s = "unknown ? a : b";',
                 '// unknown ? a : b'):
        assert spell_unresolved_values(line) == line, line
