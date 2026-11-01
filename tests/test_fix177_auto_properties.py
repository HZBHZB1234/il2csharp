"""fix 177: an auto-property's backing field reads as the property.

`<X>k__BackingField` is emitted by the C# compiler for an auto-property and
for nothing else, so a field with that name plus a property named `X` on the
same type is a *compiler guarantee*, not a guess. Two consequences:

* the property is emitted in its source shape -- `{ get; set; }` / `{ get; }`
  -- instead of a lifted body that reads its own backing field
  (`return this.__field_Count;` would become a self-call if the access had
  been spelled as the property);
* every ACCESS reads as `X`. That is what the source wrote, and it is what
  binds across assemblies: the renamed `__field_X` storage has no counterpart
  in any other assembly, which is why `tween.__field_active` could not
  resolve against the original `DOTween.dll`.

The renamed field declaration stays (`__field_X`) so the field and the
property cannot collide (CS0102), and an address-take (`&o.X` is CS0206)
respells back to that storage.
"""
from types import SimpleNamespace as NS

from il2cpp.csharp import auto_property_field, auto_property_name
from il2cpp.lifter.values import _ValuesMixin
from il2cpp.runtime.fields import _storage_name


def _meta(typedefs, fields, props, events=()):
    meta = NS(typedefs=list(typedefs), fields=list(fields),
              properties=list(props), events=list(events),
              getstr=lambda i: i,
              type_fields=lambda td: list(range(td.field_start,
                                                td.field_start + td.field_count)),
              type_methods=lambda td: [])
    return meta


def _td(index, field_start, field_count, property_start, property_count,
        event_start=0, event_count=0):
    return NS(index=index, field_start=field_start, field_count=field_count,
              property_start=property_start, property_count=property_count,
              event_start=event_start, event_count=event_count,
              name='T', namespace='', flags=0, is_enum=False,
              generic_container=-1, declaring=-1)


def _il(meta):
    il = NS(meta=meta, types=[])
    return il


def test_an_auto_property_backing_field_reads_as_the_property():
    td = _td(0, 0, 1, 0, 1)
    meta = _meta([td], [NS(name='<Count>k__BackingField', type=0)],
                 [('Count', 0, -1)])
    il = _il(meta)

    assert auto_property_name(il, 0) == 'Count'
    assert auto_property_field(il, 0, 'Count') == 0
    assert _storage_name(il, 0) == 'Count'


def test_a_collision_only_field_keeps_the_marker_storage():
    """A real field named like a member is not an auto-property.

    It is renamed to `__field_X` (the collision rule) and its accesses keep
    that spelling: only a `<X>k__BackingField` row proves an auto-property.
    """
    td = _td(0, 0, 1, 0, 1)
    meta = _meta([td], [NS(name='Count', type=0)], [('Count', 0, -1)])
    il = _il(meta)

    assert auto_property_name(il, 0) is None
    assert _storage_name(il, 0) == '__field_Count'


def test_a_backing_field_without_a_property_is_not_auto():
    td = _td(0, 0, 1, 0, 0)
    meta = _meta([td], [NS(name='<Count>k__BackingField', type=0)], [])
    il = _il(meta)

    assert auto_property_name(il, 0) is None
    assert _storage_name(il, 0) == '<Count>k__BackingField'


def test_an_event_only_collision_is_not_auto():
    td = _td(0, 0, 1, 0, 0, 0, 1)
    meta = _meta([td], [NS(name='<Changed>k__BackingField', type=0)], [],
                 [('Changed', 0, -1, -1, -1)])
    il = _il(meta)

    assert auto_property_name(il, 0) is None


def test_the_address_take_respells_to_the_storage_field():
    td = _td(0, 0, 1, 0, 1)
    meta = _meta([td], [NS(name='<Count>k__BackingField', type=0)],
                 [('Count', 0, -1)])
    il = _il(meta)
    lifter = _ValuesMixin.__new__(_ValuesMixin)
    lifter.il = il
    fe = NS(text='obj1.Count')
    fe._aprop = (0, 'Count')

    assert lifter._addr_field_text(fe) == 'obj1.__field_Count'
    # and a plain member keeps its text
    plain = NS(text='obj1.other')
    assert lifter._addr_field_text(plain) == 'obj1.other'


def test_the_property_type_is_not_affected():
    """`auto_property_maps` is keyed by FieldDef identity, never by name."""
    td0 = _td(0, 0, 1, 0, 1)
    td1 = _td(1, 1, 1, 1, 1)
    meta = _meta([td0, td1],
                 [NS(name='<Count>k__BackingField', type=0),
                  NS(name='Other', type=0)],
                 [('Count', 0, -1), ('Other', 0, -1)])
    il = _il(meta)

    assert auto_property_name(il, 0) == 'Count'
    assert auto_property_name(il, 1) is None
    assert _storage_name(il, 1) == '__field_Other'
