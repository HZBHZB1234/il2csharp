"""A.3: the Boehm GC cardmark write barrier is dropped from output.

The compiler inlines a cardmarking write barrier after each reference
store; the lifter mis-models its `lock cmpxchg` retry loop as an empty
`while (<expr> >> 12 & 63 [!= 0])`.  PAGE_SHIFT is 12 on x86-64, so that
shift IS the card-table algorithm.  The loop condition is NOT
loop-invariant and can be non-zero, so a literal C# translation is an
infinite loop -- wrong in every case.  Because the body is empty and the
condition has no observable side effect, the empty loop is removed
ANYWHERE (always sound); then a `if (data_X != 0) { }` that this emptied
is removed too.  A loop with a NON-empty body is left alone.
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
    assert drop_gc_cardmark_barriers(_pure()) == []


def test_pure_guard_removed_between_neighbours():
    src = ['foo();'] + _pure() + ['bar();']
    assert drop_gc_cardmark_barriers(src) == ['foo();', 'bar();']


def test_hex_mask_form_removed():
    assert drop_gc_cardmark_barriers(_pure('addr >> 12 & 0x3F')) == []


def test_empty_while_dropped_from_a_larger_block():
    """A cardmark while nested among real statements: the loop is removed
    (it would be an infinite loop), the guard and real code are kept."""
    src = [
        'if (data_1894383ec != 0)',
        '{',
        '    object o1;',
        '    while (&this.m >> 12 & 63 != 0)',
        '    {',
        '    }',
        '    this.x = 1;',
        '}',
    ]
    out = drop_gc_cardmark_barriers(src)
    assert out == [
        'if (data_1894383ec != 0)',
        '{',
        '    object o1;',
        '    this.x = 1;',
        '}',
    ]


def test_nonempty_while_body_kept():
    """A cardmark-looking while with a REAL body is not a barrier: keep it."""
    src = [
        'while (a >> 12 & 63 != 0)',
        '{',
        '    tick();',
        '}',
    ]
    assert drop_gc_cardmark_barriers(src) == src


def test_equality_guard_kept_but_emptied_guard_dropped():
    """`== 0` guard is not the barrier guard, but its body (an empty
    cardmark while) is still removed; the now-empty guard is kept because
    only `!= 0` guards are dropped."""
    src = [
        'if (data_1894383ec == 0)',
        '{',
        '    while (a >> 12 & 63 != 0)',
        '    {',
        '    }',
        '}',
    ]
    # while removed; the `== 0` guard body becomes empty but is NOT dropped
    out = drop_gc_cardmark_barriers(src)
    assert out == ['if (data_1894383ec == 0)', '{', '}']


def test_other_shift_kept():
    src = _pure('a >> 5 & 7 != 0')
    assert drop_gc_cardmark_barriers(src) == src


def test_guard_with_else_keeps_else():
    """A `!= 0` guard whose emptied body would be dropped but has an else
    keeps the guard (its while is removed, else preserved)."""
    src = [
        'if (data_1894383ec != 0)',
        '{',
        '    while (a >> 12 & 63 != 0)',
        '    {',
        '    }',
        '}',
        'else',
        '{',
        '    restore();',
        '}',
    ]
    out = drop_gc_cardmark_barriers(src)
    # the while is gone; the guard is kept because of the else
    joined = '\n'.join(out)
    assert 'while' not in joined
    assert 'restore();' in joined
