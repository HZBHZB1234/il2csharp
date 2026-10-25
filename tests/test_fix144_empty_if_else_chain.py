"""Fix 144: the empty-then drop arm must not orphan an `else if` chain.

`_render`'s empty-block walk had two arms for an emptied `if (C) { }`:
a bare-`else` continuation inverts the test and keeps that branch
(fix 44b), and anything else drops the three head lines.  The drop arm
also fired when the continuation was an `else if ...` CHAIN head --
dropping `if (C) { }` left the chain's `else` heads orphaned inside
the enclosing block (`if (c) { else if (a) ... }`, CS8641/CS1002/
CS1003/CS1026/CS1525 -- 40 sites / 14 images in the v39b21 partial
tree, pre-existing but drowned in the fix-143 noise until then).
Ground truth: BattleMapSwitchUtility.ResolveMapId (mi 119627).
"""
from il2cpp import Decompiler


def render(lines):
    return Decompiler.__new__(Decompiler)._render(list(lines))


def test_else_if_chain_is_kept_intact():
    out = render([
        'if (a < b)',
        '{',
        '}',
        'else',
        '{',
        '    if (x != y)',
        '    {',
        '    }',
        '    else if (p == q)',
        '    {',
        '        G();',
        '    }',
        '}',
    ])
    assert out == [
        'if (a >= b)',
        '{',
        '    if (x != y)',
        '    {',
        '    }',
        '    else if (p == q)',
        '    {',
        '        G();',
        '    }',
        '}',
    ]


def test_longer_chain_survives_a_deeper_nest():
    out = render([
        'if (c1)',
        '{',
        '}',
        'else',
        '{',
        '    if (c2)',
        '    {',
        '    }',
        '    else if (c3)',
        '    {',
        '        A();',
        '    }',
        '    else if (c4)',
        '    {',
        '        B();',
        '    }',
        '}',
    ])
    assert not any(ln.strip().startswith('else') and i > 0
                   and out[i-1].rstrip().endswith('{')
                   for i, ln in enumerate(out))
    assert any('else if (c3)' in ln for ln in out)
    assert any('else if (c4)' in ln for ln in out)


def test_bare_else_still_inverts():
    out = render([
        'if (a < b)',
        '{',
        '}',
        'else',
        '{',
        '    G();',
        '}',
    ])
    # _fix_cond_line simplifies `!(a < b)` to `a >= b`
    assert out == [
        'if (a >= b)',
        '{',
        '    G();',
        '}',
    ]


def test_pure_empty_if_without_else_still_drops():
    out = render([
        'if (flag)',
        '{',
        '}',
        'G();',
    ])
    assert out == ['G();']


def test_impure_empty_if_without_else_is_kept():
    lines = [
        'if (Call())',
        '{',
        '}',
        'G();',
    ]
    assert render(lines) == lines
