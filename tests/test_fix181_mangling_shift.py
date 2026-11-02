"""fix 181: the generated-name mangler must not fire on a shift expression.

The file boundary replaces the angle brackets of compiler-generated
identifiers (`<Foo>d__13`, `<>c`, `<>9__0_0`, a nested
`<IEnumerable<T>_GetEnumerator>d__21`) because no C# grammar accepts them.
The nested-bracket alternative in `MANGLED_IDENT_RX` accepted spaces, so a
plain shift expression matched it: the game tree's only Assembly-CSharp parse
error was

    ulong num1 = ... | (section & value) __ section __ 32 & 63;

i.e. `<< section >>` mangled as if it were a generic name. Every Roslyn-
generated name carries a double underscore (`d__`, `c__`, `9__`, `g__`,
`b__`) or is one of the bare `<>`-prefixed closure names, so anything else is
returned untouched.
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from il2cpp.text import MANGLED_IDENT_RX, mangle_generated_ident  # noqa: E402


def _fix(text):
    return MANGLED_IDENT_RX.sub(
        lambda m: mangle_generated_ident(m.group(0)), text)


def test_a_shift_expression_is_untouched():
    for line in ('return (section << (section >> 32) & this.data) >> section >> 32 & 63;',
                 'ulong num1 = ~(section << (section >> 32)) & this.data | '
                 '(section & value) << section >> 32 & 63;',
                 'obj11 = (((byte*)(obj10 >> 8 >> 4 & 63) + byteArray + 0x0)[0]);',
                 'x = a << b >> c;'):
        assert _fix(line) == line, line


def test_comparisons_and_real_generics_are_untouched():
    for line in ('if (a < b) { }', 'bool flag1 = num1 < num2;',
                 'List<Foo> x;', 'Dictionary<int, List<Foo>> map1;'):
        assert _fix(line) == line, line


def test_generated_names_are_still_mangled():
    cases = {
        '<Foo>d__13 c;': '_Foo_d__13 c;',
        '<>c.<>9__0_0()': '__c.__9__0_0()',
        '<Main>g__Local|0_0()': '_Main_g__Local_0_0()',
        '<System_Collections_Generic_IEnumerable<T>_GetEnumerator>d__21 x;':
            '_System_Collections_Generic_IEnumerable_T__GetEnumerator_d__21 x;',
    }
    for src, want in cases.items():
        assert _fix(src) == want, (src, _fix(src))


def test_the_module_static_array_class_is_mangled():
    # `<PrivateImplementationDetails>` carries no `__` but never contains
    # whitespace, so it is still a generated name (fix 186).
    assert _fix('internal sealed partial class <PrivateImplementationDetails>') == \
        'internal sealed partial class _PrivateImplementationDetails_'


def test_the_helper_declines_a_match_without_a_generated_marker():
    assert mangle_generated_ident('< section >') == '< section >'
    assert mangle_generated_ident('') == ''
    assert mangle_generated_ident(None) == ''
