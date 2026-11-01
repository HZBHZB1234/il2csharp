"""Compile-gate scope repair: escaping locals hoist, empty class-init
guards drop (il2cpp/dec/build.py)."""
from types import SimpleNamespace as NS

from il2cpp.dec.build import (drop_duplicate_raw_stores,
                              drop_empty_init_guards, hoist_escaping_locals)
from il2cpp.emitter import Emitter


def test_hoists_arm_declared_local_used_after_join():
    body = [
        'if (flag1)',
        '{',
        '    object obj6 = a;',
        '}',
        'else',
        '{',
        '    object obj6 = b;',
        '}',
        'Use(obj6);',
    ]
    out, n = hoist_escaping_locals(body)
    assert n == 1
    assert out[0] == 'object obj6;'
    assert '    obj6 = a;' in out and '    obj6 = b;' in out
    assert not any(l.strip().startswith('object obj6 =') for l in out)


def test_leaves_well_scoped_locals_alone():
    body = ['int num1 = 3;', 'if (num1 > 2)', '{', '    int num2 = num1;',
            '    Use(num2);', '}']
    out, n = hoist_escaping_locals(body)
    assert n == 0 and out == body


def test_conflicting_types_decline():
    body = ['if (x)', '{', '    int num1 = 1;', '}', 'else', '{',
            '    float num1 = 2f;', '}', 'Use(num1);']
    out, n = hoist_escaping_locals(body)
    assert n == 0 and out == body


def test_never_hoists_into_switch_block():
    body = [
        'switch (k)',
        '{',
        '    case 0:',
        '    {',
        '        string text1 = "a";',
        '        break;',
        '    }',
        '    case 1:',
        '    {',
        '        string text1 = "b";',
        '        break;',
        '    }',
        '}',
    ]
    out, n = hoist_escaping_locals(body)
    assert n == 1
    assert out[0] == 'string text1;'      # above the switch, not inside


def test_parameters_and_pattern_vars_untouched():
    body = ['if (x)', '{', '    int a1 = 1;', '}', 'Use(a1);']
    out, n = hoist_escaping_locals(body, params={'a1'})
    assert n == 0


def test_empty_init_guard_dropped_only_when_empty():
    lines = [
        'if (typeof(UnityEngine.Object).initialized == 0)',
        '{',
        '}',
        'Foo();',
        'if (typeof(Bar).initialized == 0)',
        '{',
        '    Baz();',
        '}',
        'if (typeof(Q).initialized == 0)',
        '{',
        '}',
        'else',
        '{',
        '}',
    ]
    out = drop_empty_init_guards(lines)
    assert out[0] == 'Foo();'
    assert 'if (typeof(Bar).initialized == 0)' in out
    assert 'if (typeof(Q).initialized == 0)' in out


def test_raw_class_init_guard_dropped_after_fix134_spelling():
    """The same native guard, rendered as the post-fix-134 raw load.

    The old regex matched only `typeof(X).initialized`; the raw spelling
    left 1,336 empty `if`s in the UniTask tree."""
    lines = [
        'if (((byte*)typeof(UniTask) + 0xe0)[0] == 0)',
        '{',
        '}',
        'Foo();',
        'if (((byte*)typeof(UniTask) + 0xe0)[0] != 0)',
        '{',
        '    Bar();',
        '}',
        'if (((byte*)typeof(UniTask) + 0xe0)[0] == 0)',
        '{',
        '}',
        'else',
        '{',
        '}',
    ]
    out = drop_empty_init_guards(lines)
    assert out[0] == 'Foo();'
    assert 'if (((byte*)typeof(UniTask) + 0xe0)[0] != 0)' in out
    assert out.count('if (((byte*)typeof(UniTask) + 0xe0)[0] == 0)') == 1


def test_duplicate_raw_field_store_dropped_only_for_exact_twin():
    lines = [
        'Rigidbody2D rigidbody2D1 = this.transform.GetComponent();',
        '((byte*)&this.MyRigidbody + 0x0)[0] = rigidbody2D1;',
        'this.MyRigidbody = rigidbody2D1;',
        '((byte*)&this.MyAnimator + 0x0)[0] = animator1;',
        'this.MyAnimator = other;',
        '((byte*)&s_20 + 0x0)[0] = value1;',
        'return value1;',
    ]
    out = drop_duplicate_raw_stores(lines)
    assert '((byte*)&this.MyRigidbody + 0x0)[0] = rigidbody2D1;' not in out
    assert 'this.MyRigidbody = rigidbody2D1;' in out
    # a differing managed store and a non-store neighbour keep the raw line
    assert '((byte*)&this.MyAnimator + 0x0)[0] = animator1;' in out
    assert '((byte*)&s_20 + 0x0)[0] = value1;' in out


def test_duplicate_raw_store_accepts_inline_void_return_twin():
    lines = [
        '((byte*)&this.MyAnimator + 0x0)[0] = animator1;',
        'this.MyAnimator = animator1; return;',
    ]
    assert drop_duplicate_raw_stores(lines) == [
        'this.MyAnimator = animator1; return;']


def test_void_tail_strips_inline_return_only_after_a_statement():
    em = Emitter.__new__(Emitter)
    em.il = NS(types=[(0, 0x00010000)])       # void
    m = NS(return_type=0)
    assert em._void_tail_strip(['Foo(); return;'], m) == ['Foo();']
    assert em._void_tail_strip(['} return;'], m) == ['}']
    assert em._void_tail_strip(['if (x) return;'], m) == ['if (x) return;']
