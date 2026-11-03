"""Compound spelling is not permission to hoist a write across statements."""
import pytest

from il2cpp import Decompiler


def fold(lines):
    return Decompiler.__new__(Decompiler)._compound_assign(lines)


@pytest.mark.parametrize('target', ['this.count', 'box.Count', 'arr[index]'])
@pytest.mark.parametrize('middle', [
    'int num2 = TARGET;',
    'Observe(TARGET);',
    'Observe(alias);',
    'MayThrow();',
    'box = other;',
    'index = 2;',
    'alias.Count = 7;',
    'arr[otherIndex] = 7;',
    'TARGET += 3;',
    'if (ready)',
    'return;',
    '// Keep this statement boundary.',
    '{', '}', 'L_123:',
])
def test_hop_does_not_cross_an_unproven_statement(target, middle):
    middle = middle.replace('TARGET', target)
    lines = ['int num1 = %s + 1;' % target, middle,
             '%s = num1;' % target, 'Use(num2);']
    before = list(lines)
    assert fold(lines) == before
    assert lines == before


@pytest.mark.parametrize('target', ['this.count', 'box.Count', 'arr[index]'])
@pytest.mark.parametrize('op', ['+', '-'])
@pytest.mark.parametrize('decl', ['', 'int '])
def test_adjacent_hop_still_folds(target, op, decl):
    lines = ['    %snum1 = %s %s 1;' % (decl, target, op),
             '    %s = num1;' % target]
    assert fold(lines) == ['    %s %s= 1;' % (target, op)]


def test_blank_lines_do_not_observe_an_early_write():
    assert fold(['int num1 = box.Count + 1;', '', '  ',
                 'box.Count = num1;']) == ['box.Count += 1;', '', '  ']


def test_target_free_scalar_assignment_is_also_a_barrier():
    # Without typed effects, even a target-free expression may throw or read
    # an alias. Declining is intentional; no lexical independence guess.
    lines = ['int num1 = box.Count + 1;', 'int num2 = other.Value;',
             'box.Count = num1;']
    assert fold(lines) == lines


def test_hop_live_after_the_copy_is_not_removed():
    lines = ['int num1 = box.Count + 1;', 'box.Count = num1;', 'Use(num1);']
    assert fold(lines) == lines


def test_neighboring_hops_remain_in_their_original_order():
    assert fold(['int num1 = box.Count + 1;', 'box.Count = num1;',
                 'int num2 = other.Count - 1;', 'other.Count = num2;']) == [
                     'box.Count += 1;', 'other.Count -= 1;']


def test_direct_arithmetic_does_not_move_across_an_observer():
    assert fold(['Observe(box);', 'box.Count = box.Count + 1;']) == [
        'Observe(box);', 'box.Count += 1;']
