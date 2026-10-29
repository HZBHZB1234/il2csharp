"""Fix 133 (Limbus v39): open generic collection layouts and list bounds.

The first two checks are metadata-only.  The body checks moved from the
retired sample-game targets to current Limbus methods: ``AddItem`` walks its
``List<RpgItemStack>`` with the 4-byte ``_size`` field at 0x18, and ``GetItem``
specialises the element type through its receiver instead of leaking ``T``.
"""
import pytest

from game_support import find_method, lift_text

pytestmark = pytest.mark.game("limbus")


def _td(il, ns, name):
    hits = [i for i, t in enumerate(il.meta.typedefs)
            if t.namespace == ns and t.name == name]
    assert len(hits) == 1
    return hits[0]


def _names(il, td):
    return {off: v[0] for off, v in (il.instance_field_chain(td) or {}).items()}


def test_list_and_dictionary_layouts(baseline_game_decompiler):
    il, _ = baseline_game_decompiler
    lst = _names(il, _td(il, 'System.Collections.Generic', 'List`1'))
    assert lst == {0x10: '_items', 0x18: '_size', 0x1c: '_version', 0x20: '_syncRoot'}
    dic = _names(il, _td(il, 'System.Collections.Generic', 'Dictionary`2'))
    assert dic[0x10] == '_buckets' and dic[0x18] == '_entries' and dic[0x20] == '_count'
    assert 0 not in lst and 0 not in dic       # the object header is not a field


def test_list_count_reads_size(baseline_game_decompiler):
    il, dec = baseline_game_decompiler
    mi, m, td = find_method(il, 'RPGSystem.RpgInventoryManager', 'AddItem', 3)
    assert m.name == 'AddItem'
    body = lift_text(il, dec, mi)
    # fix 169 (C8): the arity strip also un-doubles the local's stem
    # (`List_1` used to lex as ['List','1'] -> stem `list1` -> `list12`).
    assert 'for (int num9 = 0; num9 < list2._size; num9++)' in body
    assert '__addr(list2) + 0x18' not in body
    assert '(list2 + 0x18)' not in body


def test_items_type_closes_through_the_receiver(baseline_game_decompiler):
    il, dec = baseline_game_decompiler
    mi, m, td = find_method(il, 'RPGSystem.RpgInventoryManager', 'GetItem', 1)
    body = lift_text(il, dec, mi)
    assert ('System.Collections.Generic.List<RPGSystem.RpgItemStack> '
            'list1 = this._items;') in body
    assert 'list1._items[num1]' in body
    assert 'T[] ' not in body
