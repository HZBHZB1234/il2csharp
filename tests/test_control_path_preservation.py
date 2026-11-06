"""Sequential guards are not an else-if chain without a terminating arm."""
import itertools
import re

import pytest
from il2cpp import Decompiler


def chain(first):
    return ['if (a)', '{', 'X();', '}', 'else', '{',
            'if (b)', '{', *first, '}', 'if (c)', '{', 'Z();', '}', '}']


def execute(lines, flags):
    """Small authored-control interpreter; no native/game snippets."""
    tokens = [s.strip() for s in lines if s.strip()]
    effects = []
    halted = False

    def statement(i, live):
        nonlocal halted
        text = tokens[i]
        m = re.fullmatch(r'(?:else )?if \(([abc])\)', text)
        if m:
            assert tokens[i + 1] == '{'
            choose = flags[m[1]]
            j = block(i + 1, live and choose)
            if j < len(tokens) and tokens[j] == 'else':
                j = block(j + 1, live and not choose)
            elif j < len(tokens) and tokens[j].startswith('else if ('):
                j = statement(j, live and not choose)
            return j
        assert text.endswith(';'), text
        if live and not halted:
            effects.append(text)
            if re.match(r'^(?:return|throw|goto)\b', text):
                halted = True
        return i + 1

    def block(i, live):
        assert tokens[i] == '{'
        i += 1
        while tokens[i] != '}':
            i = statement(i, live)
        return i + 1

    i = 0
    while i < len(tokens):
        i = statement(i, True)
    return effects


@pytest.mark.parametrize('values', list(itertools.product([False, True], repeat=3)))
@pytest.mark.parametrize('first', [[], ['Y();'], ['Y();', 'Y2();']])
def test_fallthrough_checks_preserve_all_paths(first, values):
    lines = chain(first)
    dec = Decompiler.__new__(Decompiler)
    output = dec._elseif_flatten_multi(lines)
    flags = dict(zip('abc', values))
    assert execute(output, flags) == execute(lines, flags)
    assert output == lines


@pytest.mark.parametrize('tail', ['return;', 'return value;', 'throw error;',
                                  'goto L_dead;', 'break;', 'continue;'])
def test_only_proved_top_level_terminal_arms_can_be_lifted(tail):
    lines = chain(['Y();', tail])
    out = Decompiler.__new__(Decompiler)._elseif_flatten_multi(lines)
    assert 'else if (b)' in out and 'else if (c)' in out


@pytest.mark.parametrize('body', [
    ['if (c)', '{', 'return;', '}'],
    ['Log("; return;");'],
    ['// return;'],
    ['/* return; */'],
    ['returning();'],
    ['L_dead:', 'return;'],
    ['goto L_dead;', 'L_dead:', 'Y();'],
])
def test_nested_conditional_fake_transfer_and_local_targets_decline(body):
    lines = chain(body)
    assert Decompiler.__new__(Decompiler)._elseif_flatten_multi(lines) == lines


def test_every_nonfinal_chunk_must_terminate_not_just_the_first():
    lines = chain(['return;'])
    lines[-1:-1] = ['if (b)', '{', 'Y();', '}']
    assert Decompiler.__new__(Decompiler)._elseif_flatten_multi(lines) == lines


@pytest.mark.parametrize('text', ['Log("{");', 'Log("}");',
                                 'Log("} return; {");', '// } return; {',
                                 '/* } return; { */'])
def test_literal_and_comment_braces_cannot_change_chunk_ownership(text):
    lines = chain([text])
    assert Decompiler.__new__(Decompiler)._elseif_flatten_multi(lines) == lines
