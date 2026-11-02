"""fix 192: a SET-ONLY property is not an auto-property.

C# requires a getter for auto-implementation (CS8051), so a property with only
a setter was written with an explicit body over a plain field. Treating that
field as a `<X>k__BackingField` respelled the lifted body to `X = value` --
infinite recursion, and the bodyless `{ set; }` shape does not compile either
(`UnityEngine.Bindings.IgnoreAttribute.DoesNotContributeToSize`).
"""
import os
import sys
from types import SimpleNamespace as NS

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from il2cpp.csharp import auto_property_field, auto_property_name  # noqa: E402


def _il(props, fields):
    """Fake Il2Cpp: one typedef with `props` rows and `fields` rows."""
    td = NS(index=0, property_start=0, property_count=len(props),
            field_start=0, field_count=len(fields))
    meta = NS(typedefs=[td],
              properties=props, fields=fields,
              getstr=lambda s: s,
              type_fields=lambda t: list(range(t.field_start,
                                               t.field_start + t.field_count)))
    return NS(meta=meta)


BACKING = NS(name='<Value>k__BackingField')


def test_a_getter_plus_setter_is_an_auto_property():
    il = _il([('Value', 0, 1, 0, 0)], [BACKING])
    assert auto_property_name(il, 0) == 'Value'
    assert auto_property_field(il, 0, 'Value') == 0


def test_a_get_only_property_is_an_auto_property():
    il = _il([('Value', 0, -1, 0, 0)], [BACKING])
    assert auto_property_name(il, 0) == 'Value'


def test_a_set_only_property_is_not():
    il = _il([('Value', -1, 1, 0, 0)], [BACKING])
    assert auto_property_name(il, 0) is None
    assert auto_property_field(il, 0, 'Value') is None
