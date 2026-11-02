"""fix 193: a type name declared in the file shadows the namespace type.

The using-strip shortens `UnityEngine.UIElements.UxmlTraits` to `UxmlTraits`
when one visible typedef answers to that head. Inside
`class VisualElement`, which declares its own NESTED `UxmlTraits`, the short
name resolves to the nested type, so the emitted base clause became
`class UxmlTraits : UxmlTraits` -- CS0146 circular base, which then cascaded
into 52 CS0311 constraint errors on `UxmlFactory<TCreatedType, TTraits>`.
`collision_heads(..., declared=...)` now keeps the prefix for a head the file
declares itself.
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from il2cpp.csharp import collision_heads, strip_namespaces  # noqa: E402

USES = {'UnityEngine.UIElements', 'System'}
SHORT = {'UxmlTraits': {'UnityEngine.UIElements'}, 'String': {'System'}}


def _strip(text, declared=()):
    dup = collision_heads(text, 'UnityEngine.UIElements.Test', USES, SHORT,
                          declared)
    return strip_namespaces([text], USES, 'UnityEngine.UIElements.Test', dup)


def test_a_declared_name_shadows_the_namespace_type():
    line = 'public partial class UxmlTraits : UnityEngine.UIElements.UxmlTraits'
    out = _strip(line, declared={'VisualElement', 'UxmlTraits'})
    assert out == [line], out


def test_an_undeclared_name_is_still_shortened():
    line = 'public partial class Foo : UnityEngine.UIElements.UxmlTraits'
    out = _strip(line, declared={'VisualElement', 'Foo'})
    assert out == ['public partial class Foo : UxmlTraits'], out


def test_no_declared_names_keeps_the_old_behaviour():
    line = 'public partial class Foo : UnityEngine.UIElements.UxmlTraits'
    assert _strip(line) == ['public partial class Foo : UxmlTraits']


def test_a_generic_nested_name_shadows_with_its_arity_stripped():
    # metadata names a generic type UxmlObjectTraits`1; the emitted short
    # spelling is UxmlObjectTraits, which is what the head comparison sees.
    line = ('internal partial class UxmlObjectTraits<T> : '
            'UnityEngine.UIElements.UxmlObjectTraits<T>')
    out = _strip(line, declared={'UxmlObjectTraits`1', 'UxmlObjectTraits'})
    assert out == [line], out



def test_a_doubled_closure_name_keeps_the_type_and_a_space():
    # IL2CPP spells a closure field that refers to another closure field
    # <>3__<>4__this; mangling it must not eat the space or the type's
    # tail (CS1519 x4 on the survivors tree).
    from il2cpp.text import mangle_generated_names
    line = 'public X.InputDeviceMatcher <>3__<>4__this;'
    out = mangle_generated_names(line)
    assert out == 'public X.InputDeviceMatcher __3____4__this;', out
    assert mangle_generated_names('x = (a & b) << c >> 32;') == \
        'x = (a & b) << c >> 32;'
