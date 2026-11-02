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
