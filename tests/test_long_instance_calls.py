"""Call text length must not invent static dispatch or duplicate a receiver.

Generic-method ABI closure and already materialized receiver expressions retain
existing boundaries. No game fixture or output snapshot is used here.
"""
import pytest
from il2cpp import Expr
from test_stack_args import make_call_lifter, INT, VOID


@pytest.mark.parametrize('receiver,kind', [('receiver', 'obj'), ('receiver', 'int'), ('items[index]', 'obj')])
@pytest.mark.parametrize('returns', [VOID, INT])
@pytest.mark.parametrize('length', [8, 65])
def test_resolved_instance_syntax_never_depends_on_total_argument_text_length(receiver, kind, returns, length):
    args = [f'argument{i}_' + 'x' * length for i in range(3)]
    lift, ins = make_call_lifter([INT] * 3, dict(zip(['RCX', 'RDX', 'R8', 'R9'], [Expr(receiver, None, kind), *args])), returns=returns, static=False)
    lift._insn(ins, [ins], 0, None, ins.next_ip)
    if returns == INT:
        lift._flush_pending_calls()
    text = '\n'.join((row[1] for row in lift.out))
    assert text.count(receiver + '.Target(') == 1, text
    assert 'Example.Target(' not in text
    for arg in args:
        assert text.count(arg) == 1


@pytest.mark.parametrize('length', [8, 65])
def test_static_metadata_stays_static_with_short_and_long_arguments(length):
    args = [f'argument{i}_' + 'x' * length for i in range(3)]
    lift, ins = make_call_lifter([INT] * 3, dict(zip(['RCX', 'RDX', 'R8'], args)))
    lift._insn(ins, [ins], 0, None, ins.next_ip)
    text = '\n'.join((row[1] for row in lift.out))
    assert text.count('Example.Target(') == 1
    for arg in args:
        assert text.count(arg) == 1


@pytest.mark.parametrize('receiver,expected', [('?', '?'), ('', 'default')])
@pytest.mark.parametrize('length', [8, 65])
def test_unproved_receiver_keeps_the_existing_conservative_form(receiver, expected, length):
    args = [f'argument{i}_' + 'x' * length for i in range(3)]
    lift, ins = make_call_lifter([INT] * 3, dict(zip(['RCX', 'RDX', 'R8', 'R9'], [Expr(receiver, None, 'int'), *args])), static=False)
    lift._insn(ins, [ins], 0, None, ins.next_ip)
    assert lift.out == [(ins.ip, 'Example.Target(' + ', '.join([expected, *args]) + ');', None)]


@pytest.mark.parametrize('length', [8, 65])
def test_constructor_rendering_is_not_broadened(length):
    args = [f'argument{i}_' + 'x' * length for i in range(3)]
    lift, ins = make_call_lifter([INT] * 3, dict(zip(['RCX', 'RDX', 'R8', 'R9'], [Expr('receiver', None, 'int'), *args])), static=False, name='.ctor')
    lift._insn(ins, [ins], 0, None, ins.next_ip)
    prefix = 'Example.ctor(receiver, '
    assert lift.out == [(ins.ip, prefix + ', '.join(args) + ');', None)]


@pytest.mark.parametrize('length', [8, 65])
def test_missing_metadata_does_not_gain_instance_semantics(length):
    args = [f'argument{i}_' + 'x' * length for i in range(3)]
    lift, ins = make_call_lifter([INT] * 3, dict(zip(['RCX', 'RDX', 'R8', 'R9'], [Expr('receiver', None, 'obj'), *args])), static=False)
    lift.il.addr_candidates = {}
    lift.il.addr_to_method = {}
    lift.il.bin = lift.bin
    lift.bin.exports = {}
    lift._twin_cache = {}
    lift._cls_init_export = None
    lift._thunk_cache = {8192: None}
    lift._insn(ins, [ins], 0, None, ins.next_ip)
    assert not any(('receiver.Target(' in row[1] for row in lift.out))
    assert any(('sub_2000(' in row[1] for row in lift.out))
    for arg in args:
        assert sum((row[1].count(arg) for row in lift.out)) == 1


@pytest.mark.parametrize('receiver,kind', [('receiver', 'obj'), ('receiver', 'int'), ('items[index]', 'obj')])
@pytest.mark.parametrize('returns', [VOID, INT])
@pytest.mark.parametrize('length', [8, 65])
def test_generic_method_argument_recovery_keeps_its_existing_boundary(receiver, kind, returns, length):
    args = [f'argument{i}_' + 'x' * length for i in range(3)]
    lift, ins = make_call_lifter([INT] * 3, dict(zip(['RCX', 'RDX', 'R8', 'R9'], [Expr(receiver, None, kind), *args])), returns=returns, static=False)
    lift.meta.methods[0].generic_container = 0
    lift._insn(ins, [ins], 0, None, ins.next_ip)
    if returns == INT:
        lift._flush_pending_calls()
    text = '\n'.join((row[1] for row in lift.out))
    expected = receiver + '.Target(' if length == 8 else 'Example.Target(' + receiver + ', '
    assert text.count(expected) == 1, text
    for arg in args:
        assert text.count(arg) == 1


@pytest.mark.parametrize('generic', [False, True])
@pytest.mark.parametrize('length', [8, 65])
def test_indexer_arguments_keep_the_receiver(generic, length):
    args = [f'argument{i}_' + 'x' * length for i in range(2)]
    lift, ins = make_call_lifter([INT] * 2, dict(zip(['RCX', 'RDX', 'R8'], [Expr('receiver', None, 'obj'), *args])), name='get_Item', returns=INT, static=False)
    if generic:
        lift.meta.methods[0].generic_container = 0
    lift._insn(ins, [ins], 0, None, ins.next_ip)
    lift._flush_pending_calls()
    text = '\n'.join([*(row[1] for row in lift.out), lift.regs['RAX'].text])
    prefix = 'Example.get_Item(receiver, ' if generic and length == 65 else 'receiver['
    assert text.count(prefix) == 1, text
    for arg in args:
        assert text.count(arg) == 1


@pytest.mark.parametrize('generic', [False, True])
@pytest.mark.parametrize('length', [8, 160])
def test_long_getter_receiver_keeps_member_syntax(generic, length):
    receiver = 'receiver_' + 'x' * length
    lift, ins = make_call_lifter([], {'RCX': Expr(receiver, None, 'obj')}, name='get_Value', returns=INT, static=False)
    if generic:
        lift.meta.methods[0].generic_container = 0
    lift._insn(ins, [ins], 0, None, ins.next_ip)
    lift._flush_pending_calls()
    text = '\n'.join([*(row[1] for row in lift.out), lift.regs['RAX'].text])
    expected = 't0.get_Value()' if length == 160 else receiver + '.Value'
    assert text.count(expected) == 1, text
    assert text.count(receiver) >= 1


@pytest.mark.parametrize('length', [0, 150])
@pytest.mark.parametrize('returns', [VOID, INT])
def test_effectful_receiver_is_evaluated_only_once(length, returns):
    receiver = 'Factory.GetReceiver(' + 'x' * length + ')'
    args = [f'argument{i}_' + 'x' * 65 for i in range(3)]
    lift, ins = make_call_lifter([INT] * 3, dict(zip(['RCX', 'RDX', 'R8', 'R9'], [Expr(receiver, None, 'obj'), *args])), returns=returns, static=False)
    lift._insn(ins, [ins], 0, None, ins.next_ip)
    if returns == INT:
        lift._flush_pending_calls()
    text = '\n'.join((row[1] for row in lift.out))
    assert text.count('Factory.GetReceiver(') == 1, text
    for arg in args:
        assert text.count(arg) == 1, text
