"""A.3: the pure Boehm GC cardmark write barrier is dropped.

The compiler inlines a cardmarking write barrier after each reference
store; the lifter mis-models its `lock cmpxchg` retry loop as an empty
`while (<expr> >> 12 & 63 != 0)`.  PAGE_SHIFT is 12 on x86-64, so that
shift is the card-table algorithm, not an application shift.  Only the
PURE shape (guard body is exactly one empty such while) is removed; a
body with any other statement is kept.
"""
from il2cpp.dec.build import drop_gc_cardmark_barriers


def _pure(expr='&this.X >> 12 & 63 != 0'):
    return [
        'if (data_1894383ec != 0)',
        '{',
        '    while (%s)' % expr,
        '    {',
        '    }',
        '}',
    ]


def test_pure_cardmark_guard_removed():
    src = _pure()
    assert drop_gc_cardmark_barriers(src) == []


def test_pure_guard_removed_between_neighbours():
    src = ['foo();'] + _pure() + ['bar();']
    out = drop_gc_cardmark_barriers(src)
    assert out == ['foo();', 'bar();']


def test_hex_mask_form_removed():
    assert drop_gc_cardmark_barriers(
        _pure('addr >> 12 & 0x3F')) == []


def test_body_with_extra_statement_kept():
    src = [
        'if (data_1894383ec != 0)',
        '{',
        '    while (a >> 12 & 63 != 0)',
        '    {',
        '    }',
        '    extra();',
        '}',
    ]
    assert drop_gc_cardmark_barriers(src) == src


def test_equality_guard_not_touched():
    src = [
        'if (data_1894383ec == 0)',
        '{',
        '    while (a >> 12 & 63 != 0)',
        '    {',
        '    }',
        '}',
    ]
    assert drop_gc_cardmark_barriers(src) == src


def test_other_shift_not_touched():
    assert drop_gc_cardmark_barriers(_pure('a >> 5 & 7 != 0')) == _pure('a >> 5 & 7 != 0')


def test_guard_with_else_kept():
    src = _pure() + ['else', '{', '    restore();', '}']
    assert drop_gc_cardmark_barriers(src) == src
