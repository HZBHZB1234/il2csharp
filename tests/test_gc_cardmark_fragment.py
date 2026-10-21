"""GC cardmark-index fragment residue: dead split-assignment lines dropped.

When a write barrier is split into standalone assignments the lifter emits
`T name = (typeof(X)._F & 8589930496) >> 12 & 63;` (8589930496 =
0x200000000 is Boehm's card-table mask).  The RHS is pure static-field
arithmetic; when `name` is declared and never used again, the line is dead
code (and usually has the wrong declared type).  Only this exact shape is
touched; a used fragment or any other bit expression is kept.
"""
from il2cpp.dec.build import drop_dead_cardmark_fragments


def test_dead_fragment_dropped():
    src = [
        'BuffAbilityManager bm1 = (typeof(BuffAbilityManager)._a & 8589930496) >> 18;',
        'foo();',
    ]
    assert drop_dead_cardmark_fragments(src) == ['foo();']


def test_used_fragment_kept():
    src = [
        'int x = (typeof(T)._a & 8589930496) >> 12 & 63;',
        'bar(x);',
    ]
    assert drop_dead_cardmark_fragments(src) == src


def test_shift18_dead_dropped():
    src = ['T a = (typeof(X)._f & 8589930496) >> 18;']
    assert drop_dead_cardmark_fragments(src) == []


def test_other_bit_expression_kept():
    src = ['int y = (a & 255) >> 3;']
    assert drop_dead_cardmark_fragments(src) == src


def test_no_gc_mask_kept():
    src = ['int z = (a >> 12) & 63;']
    assert drop_dead_cardmark_fragments(src) == src


def test_name_in_different_context_kept():
    """If the name appears anywhere else (even a same-named token), keep."""
    src = [
        'int q = (typeof(T)._a & 8589930496) >> 18;',
        'q = 5;',
    ]
    assert drop_dead_cardmark_fragments(src) == src
