"""Fix 165: five independent parse-error families in the game-only build.

The game-only milestone build (commit 9ae22f5) reported 298 ERROR /
MISSING nodes in 28 files. Every one of them traced to a text or
structure pass producing output no C# grammar accepts; each family
below is a separate root cause, proven by a minimal repro first.

  A. `_unsafify`'s fixed 16-iteration cap -- the paren-matched arm
     peels ONE `*(EXPR)` per iteration, so a line with more than 16
     derefs kept the remainder raw. `*(A.B + 0x2a)` is not C#.
  B. `_NCONST_RX`'s `(?<!\\w\\s)` lookbehind, which exists to keep a
     multiplication (`a * 16`) untouched, also blocked the deref after
     an expression-OPENING keyword (`return *16 == 3;`).
  C. A 4-byte constant-pool float whose bits satisfy the usage-slot tag
     test decoded as a MethodRef and rendered `GenericMethod#N` as a
     float operand (`-3.1415927f` == 0xC0490FDB).
  D. `_strip_dangling_default` treated `==` as an assignment, clearing
     the live-`?` context so a ternary's `: default` false arm was
     stripped (`c == t ? (a ? 1 : 0) : default` -> `c == t ? (a ? 1 : 0) ;`).
  E. `_fix_cond_line`'s double-negation arm stripped `!(!` whenever the
     condition merely STARTED with it, mangling `!(!a ? 1 : 0) | flag`.
  F. `_null_conditional` folded `if (x != null) { x.M(); }` to
     `x?.M();` without noticing a following `else`, orphaning the else.
"""
import re

import pytest

from il2cpp.dec.textpass import _TextPassMixin


def _tp():
    return _TextPassMixin()


# -- A: the iteration bound -------------------------------------------------

def test_unsafify_is_not_capped_at_sixteen_derefs():
    """Twenty `*(...)` on one line (the real shape: a 20-deep ternary
    chain in UnitInformationSummaryTabContent.InitContents) must all
    convert; the old `for _ in range(16)` left four raw."""
    line = 'num1 = ' + ' : '.join(
        '*(*(A + 0x20) + 0x%x) == %d ? &d%d' % (i, i, i)
        for i in range(1, 21)) + ';'
    assert line.count('*(') == 40
    out = _tp()._unsafify(line)
    assert '*(' not in out


def test_unsafify_still_converts_a_single_deref():
    out = _tp()._unsafify('x = *(obj1 + 0x10);')
    assert out == 'x = ((byte*)obj1 + 0x10)[0];'


def test_unsafify_leaves_a_multiplication_alone():
    """The bound change must not weaken the multiplication guard."""
    for src in ('a * 16 == 3;', 'b = a * 3;', 'return a * 16 == 3;',
                'return (byte*)a * 2;', 'f(a * 2, b);'):
        assert _tp()._unsafify(src) == src, src


# -- B: the keyword-opened constant deref ----------------------------------

@pytest.mark.parametrize('src, want', [
    ('return *16 == 3;', 'return ((byte*)16)[0] == 3;'),
    ('return *48 == 9;', 'return ((byte*)48)[0] == 9;'),
    ('return *24 > null;', 'return ((byte*)24)[0] > null;'),
    ('return *24 == 0;', 'return ((byte*)24)[0] == 0;'),
    ('return *36 != 1;', 'return ((byte*)36)[0] != 1;'),
    ('return *20 == 2;', 'return ((byte*)20)[0] == 2;'),
    ('return *96 ^ (float2)(-0.0f, -0.0f);',
     'return ((byte*)96)[0] ^ (float2)(-0.0f, -0.0f);'),
])
def test_constant_deref_after_opening_keyword_converts(src, want):
    assert _tp()._unsafify(src) == want


def test_constant_deref_after_assignment_already_worked():
    """The pre-existing arm; the new one must not disturb it."""
    assert _tp()._unsafify('x = *16 == 3;') == 'x = ((byte*)16)[0] == 3;'


# -- C: the usage-slot / float-constant collision --------------------------

def test_float_bits_can_satisfy_the_usage_slot_tag():
    """Documents WHY the width gate is needed: the pool constant
    -3.1415927f is 0xC0490FDB -- odd, high dword 0 -- exactly the tag
    test `decode_slot` applies."""
    import struct
    q = struct.unpack('<Q', struct.pack('<f', -3.1415927) + b'\0\0\0\0')[0]
    assert q == 0xC0490FDB
    assert (q & 1) and (q >> 32) == 0


# -- D: `==` is not an assignment in the dangling-default strip ------------

@pytest.mark.parametrize('src', [
    'SORT_ORDER o = newSortType == this._t ? (this._c == 0 ? 1 : 0) : default;',
    'asyncService1 = obj14 == null ? ((typeof(I) == data_1) ? 0 : 0) : default;',
    'x = a <= b ? 1 : 2;',
    'x = a != b ? 1 : 2;',
    'x = a >= b ? 1 : 2;',
])
def test_ternary_with_a_comparison_condition_keeps_its_false_arm(src):
    out = _tp()._render([src])[0]
    assert 'default' in out or ' : ' in out, out
    assert not out.rstrip().endswith(') ;'), out


def test_a_genuine_dangling_default_is_still_stripped():
    out = _tp()._render(['Foo(a, b) : default;'])[0]
    assert 'default' not in out, out


# -- E: the double-negation head -------------------------------------------

def test_double_negation_head_must_span_the_whole_condition():
    """`!(!a ? 1 : 0) | flag` is not a whole-condition negation; the
    old arm stripped the outer `!(` anyway and produced
    `a ? 1 : 0) | flag` (stray `)`, unparseable)."""
    dec = _dec()
    out = dec._render(['if (!(!flag5 ? 1 : 0) | flag1)'])[0]
    assert out == 'if (!(!flag5 ? 1 : 0) | flag1)', out


def test_a_real_double_negation_still_folds():
    dec = _dec()
    assert dec._render(['if (!(!flag5))'])[0] == 'if (flag5)'
    assert dec._render(['while (!(!a))'])[0] == 'while (a)'


def test_single_negation_conditions_still_simplify():
    dec = _dec()
    assert dec._render(['if (!(a == b))'])[0] == 'if (a != b)'
    assert dec._render(['if (!(a != b))'])[0] == 'if (a == b)'


# -- F: the null-conditional fold must not orphan an else ------------------

def test_null_conditional_declines_when_an_else_follows():
    dec = _dec()
    src = ['if (mail1 != null)', '{', '    mail1.UpdateData(obj2);', '}',
           'else', '{', '    x();', '}']
    out = dec._null_conditional(list(src))
    assert out == src, out


def test_null_conditional_still_folds_without_an_else():
    dec = _dec()
    out = dec._null_conditional(
        ['if (mail1 != null)', '{', '    mail1.UpdateData(obj2);', '}'])
    assert out == ['mail1?.UpdateData(obj2);'], out


def test_null_conditional_folds_at_end_of_list():
    dec = _dec()
    out = dec._null_conditional(
        ['if (a != null)', '{', '    a.M();', '}', ''])
    assert out == ['a?.M();', ''], out


# -- the shared helper -----------------------------------------------------

_DEC = None


def _dec():
    """A real Decompiler: `_fix_cond_line` needs `_simplify_cond`'s NEG
    table, which only the composed mixin has."""
    global _DEC
    if _DEC is None:
        from il2cpp.dec import Decompiler
        _DEC = Decompiler.__new__(Decompiler)
    return _DEC
