"""Long expressions retain their entire value/effects, never a placeholder zero."""
import pytest
from il2cpp import Expr
from test_native_values import lifter, INT, FLOAT, OBJECT


@pytest.mark.parametrize('kind,ty', [('int', INT), ('float', FLOAT), ('obj', OBJECT), ('?', None)])
@pytest.mark.parametrize('cap', [8, 64, 240])
def test_oversized_expression_is_materialized_without_truncation(kind, ty, cap):
    lift = lifter()
    text = 'value' + ' + other' * (cap + 1)
    expr = lift._mk(text, ty, kind, cap)
    assert expr.text == 't0' and expr.ty == ty and expr.kind == kind
    assert lift.out == [(0, 'var t0 = ' + text + ';', None)]
    assert ' = 0; //' not in lift.out[0][1]


@pytest.mark.parametrize('dry', [False, True])
def test_expression_threshold_and_numbering_are_identical_in_dry_and_real_pass(dry):
    lift = lifter()
    lift.dry = dry
    text = 'x + y'
    inline = lift._mk(text, INT, 'int', len(text))
    assert inline.text == text and not lift.out and lift.var_n == 0
    first = lift._mk(text, INT, 'int', len(text) - 1)
    second = lift._mk(text, INT, 'int', len(text) - 1)
    assert [first.text, second.text] == ['t0', 't1']
    assert lift.var_n == 2
    assert lift.out == ([] if dry else [(0, 'var t0 = x + y;', None), (0, 'var t1 = x + y;', None)])


@pytest.mark.parametrize('text', [
    'Consume() + ' + 'input + ' * 40 + '0',
    'guard ? ' + 'Left() + ' * 40 + '0 : Right()',
    '(' + 'term + ' * 40 + 'tail) / denominator',
    'new Thing("' + 'x' * 300 + '")',
    '(__w_int)' + '(' + 'term + ' * 40 + 'tail)',
    '"' + 'literal // not a comment ' * 20 + '"',
])
def test_full_expression_and_literal_or_width_marker_remain_executable(text):
    lift = lifter()
    expr = lift._mk(text)
    assert expr.text == 't0'
    assert lift.out[0][1] == 'var t0 = ' + text + ';'


def test_repeated_composition_materializes_a_bounded_graph_without_zero_substitution():
    lift = lifter()
    expr = Expr('seed', INT, 'int')
    for i in range(100):
        expr = lift._mk('(' + expr.text + ') + (' + expr.text + ')', INT, 'int')
    assert lift.out
    assert all(' = 0; //' not in text for _, text, _ in lift.out)
    # Each node expands only the two bounded children, not the full history.
    assert max(len(text) for _, text, _ in lift.out) < 520
    assert lift.out[0][1].count('seed') > 0
