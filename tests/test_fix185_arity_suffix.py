"""fix 185: a metadata arity suffix in code is not C#.

A shared static body for an instance method on an open generic type renders as
`EqualityComparer`1.GetHashCode(comparer, value)` -- the metadata arity suffix,
which is CS1056 and the only parse error in the game's
`UnityEngine.TextCoreTextEngineModule` (RichTextTagParser, 4 sites; 134 sites
tree-wide but 130 of them sit inside string literals, which are untouched).

The fold: the call's first argument is the folded receiver, so a local declared
as the same generic type with closed arguments gives the spelling. Anything
else drops to the `unknown` marker, which the marker rules already turn into
compiling code.
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from il2cpp.dec.flow import _FlowMixin  # noqa: E402

BT = chr(96)


def _run(lines):
    return _FlowMixin.__new__(_FlowMixin)._arity_suffix_respell(list(lines))


def test_a_receiver_declaration_gives_the_closed_spelling():
    body = [
        'EqualityComparer<Vector4> equalityComparer7 = EqualityComparer<Vector4>.Default;',
        'int num2 = num1 + EqualityComparer%s1.GetHashCode(equalityComparer7, new Vector4());' % BT,
    ]
    out = _run(body)
    assert 'EqualityComparer<Vector4>.GetHashCode(equalityComparer7,' in out[1]


def test_an_unknown_receiver_becomes_the_marker():
    body = ['if (EqualityComparer%s1.Equals(comparerX, new Color()))' % BT]
    out = _run(body)
    assert out[0].strip() == 'if (unknown.Equals(comparerX, new Color()))'


def test_an_arity_mismatch_becomes_the_marker():
    body = [
        'EqualityComparer<Vector4> comparer7 = default;',
        'if (EqualityComparer%s2.Equals(comparer7, 1))' % BT,
    ]
    out = _run(body)
    assert 'unknown.Equals(' in out[1]


def test_a_literal_is_untouched():
    body = ['string s = "FSharpSet%s1";' % BT]
    assert _run(body) == body


def test_a_different_base_type_is_not_used():
    body = [
        'EqualityComparer<Vector4> comparer7 = default;',
        'int n = Other%s1.M(comparer7);' % BT,
    ]
    assert 'unknown.M(' in _run(body)[1]
