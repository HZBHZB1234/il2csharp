"""Length-limited call arguments must retain their native execution identity."""
import pytest
from il2cpp import Expr
from test_pending_phi_calls import fixture, FLAGS, INT

LONG = 'Example.Calculate(' + ', '.join('argument%d' % n for n in range(20)) + ')'


def setup_call(text=LONG):
    dec, blocks, phi, value, call = fixture(text=text, ty=INT)
    value.kind = 'int'
    dec.L._cur_ip = call.next_ip
    dec.L.out = []
    return dec, blocks, phi, value, call


def test_length_materialization_then_phi_does_not_execute_call_twice():
    dec, bs, phi, value, call = setup_call()
    # A register read is counted before the call argument length limiter.
    dec.L._note_use(value)
    arg = dec.L._materialize(value, 110)
    dec.L.emit(call.next_ip, 'Consume(%s);' % arg, None)
    bs[0].stmts.extend(s[1] for s in dec.L.out)
    dec.L.out = []
    dec.L._cur_ip = -1
    dec._build_phi_copies(bs, phi, FLAGS)
    text = '\n'.join(bs[0].stmts + [s[1] for s in dec.L.out])
    assert text.count(LONG) == 1
    assert value.text == arg
    assert dec.phi_copies == {(0, 1): ['v40 = %s;' % arg]}


def test_long_argument_materialization_updates_exact_pending_value():
    dec, bs, _, value, call = setup_call()
    dec.L._note_use(value)
    arg = dec.L._materialize(value, 110)
    assert value.text == arg
    assert bs[0].stmts[1] == 'var %s = %s;' % (arg, LONG)
    dec.L._flush_pending_calls()
    assert dec.L.out == []


def test_two_equal_pending_calls_remain_two_executions():
    dec, bs, _, a, call = setup_call()
    b = Expr(a.text, a.ty, a.kind)
    b._defpos = (bs[0], 2)
    dec.L._pending_calls.append((b, call.next_ip, 'call'))
    dec.L._note_use(a)
    first = dec.L._materialize(a, 110)
    dec.L._cur_ip += 1
    dec.L._note_use(b)
    second = dec.L._materialize(b, 110)
    assert first != second
    assert (a.text, b.text) == (first, second)
    assert sum(s.count(LONG) for s in bs[0].stmts) == 2


@pytest.mark.parametrize('mode', ['dry', 'no-bind', 'no-anchor', 'not-pending',
                                  'equal-but-other-identity', 'short', 'unknown',
                                  'slice', 'parts', 'bytes', 'stack-offset'])
def test_unproved_or_ineligible_values_retain_snapshot_behavior(mode):
    dec, bs, _, value, call = setup_call()
    if mode == 'dry': dec.L.dry = True
    elif mode == 'no-bind': value._no_bind = True
    elif mode == 'no-anchor': value._defpos = None
    elif mode == 'not-pending': dec.L._pending_calls = []
    elif mode == 'equal-but-other-identity':
        dec.L._pending_calls = [(Expr(value.text, value.ty, value.kind), call.ip, 'call')]
    elif mode == 'short': value.text = 'Example.Small()'
    elif mode == 'unknown': value._unk = True
    else: setattr(value, {'slice': '_slice', 'parts': '_parts', 'bytes': '_bytes',
                         'stack-offset': '_stack_offset'}[mode], (0,))
    old = value.text
    dec.L._materialize(value, 110)
    assert value.text == old
    assert bs[0].stmts == ['Before();', 'i = i + 1;']


@pytest.mark.parametrize('kind', ['int', 'float', 'obj', 'call'])
def test_pending_call_identity_survives_supported_result_kinds(kind):
    dec, bs, _, value, _ = setup_call()
    value.kind = kind
    old = value.text
    arg = dec.L._materialize(value, 110)
    assert value.text == arg
    assert bs[0].stmts[1] == 'var %s = %s;' % (arg, old)


def test_repeated_length_materialization_reuses_the_first_temp():
    dec, bs, _, value, _ = setup_call()
    first = dec.L._materialize(value, 110)
    assert dec.L._materialize(value, 110) == first
    assert sum(s.count(LONG) for s in bs[0].stmts) == 1
    assert value._prec is None
