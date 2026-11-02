"""fix 182: a ternary arm that carries two statements is not an expression.

`_ternary_pass` folds `if (c) { x = a; } else { x = b; }` into
`x = c ? a : b;`. An arm line can carry more than its own statement -- a
joined inline return puts `X = v; return;` on one line -- and folding that
splices the second statement into the ternary:

    ((byte*)dstOffset + 0x20 + dst)[0] = num4 == dst ? srcOffset + 0x20 + num4; return : srcOffset + 0x20 + num4;

which was the one unparseable line on the game tree's mscorlib
(`System/Buffer.cs`, `Buffer.BlockCopy`). An arm whose RHS runs past its own
`;` now declines, keeping today's `if`/`else` (both arms are valid C#).
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from il2cpp.dec.highlevel import _HighLevelMixin  # noqa: E402


def _run(lines):
    dec = _HighLevelMixin.__new__(_HighLevelMixin)
    dec._var_types = {}
    return dec._ternary_pass(list(lines))


def test_a_two_statement_arm_declines():
    body = [
        'if (num4 == dst)',
        '{',
        '    *(dstOffset + 0x20 + dst) = srcOffset + 0x20 + num4; return;',
        '}',
        'else',
        '{',
        '    *(dstOffset + 0x20 + dst) = srcOffset + 0x20 + num4;',
        '}',
    ]
    assert _run(body) == body


def test_a_single_statement_pairs_still_fold():
    body = [
        'if (flag1)',
        '{',
        '    num1 = 1;',
        '}',
        'else',
        '{',
        '    num1 = 2;',
        '}',
    ]
    assert _run(body) == ['num1 = flag1 ? 1 : 2;']


def test_the_second_arm_alone_with_two_statements_also_declines():
    body = [
        'if (flag1)',
        '{',
        '    num1 = 1;',
        '}',
        'else',
        '{',
        '    num1 = 2; return;',
        '}',
    ]
    assert _run(body) == body
