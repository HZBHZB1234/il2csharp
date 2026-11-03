"""A pending native call is an execution identity, not an equal RHS string."""
from types import SimpleNamespace as NS

import pytest
from iced_x86 import Decoder

from il2cpp import Decompiler, Expr
from il2cpp.cfg import Block
from test_stack_args import make_call_lifter, INT

CLASS = (0, 0x12 << 16)
FLAGS = '!flags'


def fixture(text='Example.Emit(i)', ty=CLASS):
    lift, call = make_call_lifter([], {}, returns=ty)
    block = Block(0, [call])
    successor = Block(1, [])
    successor.preds = [0]
    block.succs = [1]
    block.stmts = ['Before();', 'i = i + 1;']
    value = Expr(text, ty, 'call')
    value._defpos = (block, 1)
    block.end_state = {'RBX': value}
    lift._pending_calls = [(value, call.ip, 'call')]
    lift._pending_phi_anchors = {id(value): (value, block, 1, 0)}
    lift._aggregate_phi_types = {}
    dec = Decompiler.__new__(Decompiler)
    dec.L = lift
    dec._var_types = {}
    dec.phi_pre = {}
    return dec, [block, successor], {(1, 'RBX'): 'v40'}, value, call


def capture(dec, blocks, phi):
    dec._materialize_pending_phi_calls(blocks, phi, FLAGS)


def test_exact_pending_result_materializes_before_the_native_later_write():
    dec, bs, phi, e, _ = fixture()
    capture(dec, bs, phi)
    assert bs[0].stmts == ['Before();', 'var t0 = Example.Emit(i);', 'i = i + 1;']
    assert e.text == 't0' and e._uses == 1
    assert dec._var_types['t0'] == dec.L._var_types['t0'] == CLASS
    capture(dec, bs, phi)
    assert len(bs[0].stmts) == 3
    dec.L.out = []
    dec.L._flush_pending_calls()
    assert dec.L.out == []


def test_phi_construction_copies_the_captured_value_not_the_call():
    dec, bs, phi, e, _ = fixture()
    dec._build_phi_copies(bs, phi, FLAGS)
    assert dec.phi_copies == {(0, 1): ['v40 = t0;']}
    assert dec._drop_dead_copies(['while (true)', '{', *bs[0].stmts,
                                 *dec.phi_copies[(0, 1)], '}']) == [
        'while (true)', '{', *bs[0].stmts, '}']


def test_equal_text_from_a_different_expr_does_not_prove_pending_identity():
    dec, bs, phi, e, _ = fixture()
    bs[0].end_state['RBX'] = Expr(e.text, e.ty, e.kind)
    capture(dec, bs, phi)
    assert e.text == 'Example.Emit(i)' and len(bs[0].stmts) == 2


def test_two_distinct_equal_calls_keep_two_native_effects_and_values():
    dec, bs, phi, a, first = fixture()
    second = Decoder(64, b'\xe8\xf6\x0f\x00\x00', ip=0x1005).decode()
    bs[0].insns.append(second)
    b = Expr(a.text, CLASS, 'call'); b._defpos = (bs[0], 1)
    bs[0].end_state['RDI'] = b
    phi[(1, 'RDI')] = 'v41'
    dec.L._pending_calls.append((b, second.ip, 'call'))
    dec.L._pending_phi_anchors[id(b)] = (b, bs[0], b._defpos[1], 0)
    dec._build_phi_copies(bs, phi, FLAGS)
    assert bs[0].stmts[1:3] == ['var t1 = Example.Emit(i);', 'var t0 = Example.Emit(i);']
    assert (a.text, b.text) == ('t1', 't0')
    assert dec.phi_copies == {(0, 1): ['v40 = t1;', 'v41 = t0;']}


def test_descending_slots_preserve_definition_order():
    dec, bs, phi, a, first = fixture()
    second = Decoder(64, b'\xe8\xf6\x0f\x00\x00', ip=0x1005).decode()
    bs[0].insns.append(second)
    b = Expr('Example.Other(i)', CLASS, 'call');b._defpos = (bs[0], 2)
    bs[0].end_state['RDI'] = b;phi[(1, 'RDI')] = 'v41'
    dec.L._pending_calls.append((b, second.ip, 'call'))
    dec.L._pending_phi_anchors[id(b)] = (b, bs[0], b._defpos[1], 0)
    capture(dec, bs, phi)
    assert bs[0].stmts == ['Before();', 'var t1 = Example.Emit(i);',
                            'i = i + 1;', 'var t0 = Example.Other(i);']


@pytest.mark.parametrize('where', ['stmt', 'cond', 'ret', 'switch', 'other-block'])
def test_rendered_call_is_not_rewritten_by_text(where):
    dec, bs, phi, e, _ = fixture()
    text = 'Use(' + e.text + ');'
    if where == 'stmt':bs[0].stmts.append(text)
    elif where == 'other-block':bs[1].stmts.append(text)
    else:setattr(bs[0], {'cond':'cond', 'ret':'ret', 'switch':'switch_idx'}[where], text)
    capture(dec, bs, phi)
    assert e.text == 'Example.Emit(i)'


@pytest.mark.parametrize('ty', [None, INT, (0, 0x0c << 16), (0, 0x11 << 16),
                                (0, 0x15 << 16), (0, 0x1c << 16),
                                (0, (0x12 << 16) | (1 << 29))])
def test_unproven_return_lanes_keep_the_existing_path(ty):
    dec, bs, phi, e, _ = fixture(ty=ty)
    capture(dec, bs, phi)
    assert e.text == 'Example.Emit(i)'


@pytest.mark.parametrize('flag', ['_unk', '_uses', '_no_bind', '_sites'])
def test_used_or_unknown_values_do_not_capture(flag):
    dec, bs, phi, e, _ = fixture()
    setattr(e, flag, [(bs[0], 0)] if flag == '_sites' else True)
    capture(dec, bs, phi)
    assert e.text == 'Example.Emit(i)'


@pytest.mark.parametrize('text', ['Example.Emit<object>(i)', 'a < b', 't1000', 'unknown'])
def test_non_call_or_generic_spelling_declines(text):
    dec, bs, phi, e, _ = fixture(text=text)
    capture(dec, bs, phi)
    assert e.text == text


@pytest.mark.parametrize('bad', ['missing', 'foreign', 'negative', 'past-end', 'wrong-ip', 'not-call'])
def test_definition_requires_a_real_owned_native_call_anchor(bad):
    dec, bs, phi, e, call = fixture()
    if bad == 'missing':e._defpos = None
    elif bad == 'foreign':e._defpos = (Block(0, [call]), 1)
    elif bad == 'negative':e._defpos = (bs[0], -1)
    elif bad == 'past-end':e._defpos = (bs[0], 3)
    elif bad == 'wrong-ip':dec.L._pending_calls = [(e, call.ip + 1, 'call')]
    else:bs[0].insns = [Decoder(64, b'\x90', ip=call.ip).decode()]
    capture(dec, bs, phi)
    assert e.text == 'Example.Emit(i)'


def test_duplicate_pending_entry_does_not_materialize_twice():
    dec, bs, phi, e, _ = fixture()
    dec.L._pending_calls *= 2
    capture(dec, bs, phi)
    assert len(bs[0].stmts) == 3


@pytest.mark.parametrize('mode', ['dry', 'no-phi', 'flags-only', 'no-pending'])
def test_unrelated_work_has_no_effect(mode):
    dec, bs, phi, e, _ = fixture()
    if mode == 'dry':dec.L.dry = True
    elif mode == 'no-phi':phi = {}
    elif mode == 'flags-only':phi = {(1, FLAGS): 'v40'}
    else:dec.L._pending_calls = []
    capture(dec, bs, phi)
    assert e.text == 'Example.Emit(i)'


@pytest.mark.parametrize('where', [0, 1, 2])
def test_a_bind_insertion_after_recording_invalidates_the_integer_anchor(where):
    dec, bs, phi, e, _ = fixture()
    dec.L._insert_bound_statement(bs[0], where, 'var t99 = Earlier();')
    capture(dec, bs, phi)
    assert e.text == 'Example.Emit(i)'


def test_binding_in_a_different_block_does_not_shift_this_anchor():
    dec, bs, phi, e, _ = fixture()
    dec.L._insert_bound_statement(bs[1], 0, 'var t99 = Other();')
    capture(dec, bs, phi)
    assert e.text == 't0'


def test_missing_creation_epoch_declines():
    dec, bs, phi, e, _ = fixture()
    dec.L._pending_phi_anchors = {}
    capture(dec, bs, phi)
    assert e.text == 'Example.Emit(i)'



def test_real_call_registration_records_the_native_definition_epoch():
    from il2cpp.cfg import _Sink
    lift, call = make_call_lifter([], {'RCX': 'receiver'}, returns=CLASS, static=False)
    lift._td_of = lambda ty: 0
    block = Block(0, [call]);block.stmts = ['Before();']
    lift.out = _Sink(block)
    lift.regs = lift._new_regs(lift.regs)
    lift._insn(call, [call], 0, None, call.next_ip)
    value = dict.get(lift.regs, 'RAX')
    assert lift._pending_calls[0][0] is value
    assert lift._pending_phi_anchors[id(value)] == (value, block, 1, 0)
    assert block.stmts == ['Before();']
    lift._flush_pending_calls()
    assert lift._pending_phi_anchors == {}


@pytest.mark.parametrize('text', [
    'Example.Emit(Other(i))', 'Example.Emit(*(p + 8))',
    'Example.Emit(items[i])', 'Example.Emit(&value)',
    'items[i].Emit(i)', 'Example.Emit((int)i)',
    'Example.Emit(new Pair(i, i))',
])
def test_nested_or_raw_argument_spellings_decline(text):
    dec, bs, phi, e, _ = fixture(text=text)
    capture(dec, bs, phi)
    assert e.text == text and len(bs[0].stmts) == 2


@pytest.mark.parametrize('slot', [0, 1, 2])
@pytest.mark.parametrize('uses', [None, 1, 2])
def test_an_uncaptured_pending_call_in_the_same_block_declines(slot, uses):
    dec, bs, phi, e, call = fixture()
    other = Expr('Example.After(i)', CLASS, 'call')
    other._defpos = (bs[0], slot)
    other._uses = uses
    dec.L._pending_calls.append((other, call.ip + 5, 'call'))
    capture(dec, bs, phi)
    assert e.text == 'Example.Emit(i)' and len(bs[0].stmts) == 2


def test_a_pending_call_in_another_block_does_not_shift_this_definition():
    dec, bs, phi, e, call = fixture()
    other = Expr('Example.After(i)', CLASS, 'call')
    other._defpos = (bs[1], 0)
    dec.L._pending_calls.append((other, call.ip + 5, 'call'))
    capture(dec, bs, phi)
    assert e.text == 't0'


@pytest.mark.parametrize('text', ['Example.Compute(i)', 'this.longMemberPath.value',
                                'i + anotherLongVariable', '*(array + index * 8)'])
def test_a_complex_phi_source_cannot_bind_later_into_the_capture_block(text):
    dec, bs, phi, e, _ = fixture()
    other = Expr(text, INT, 'int')
    other._defpos = (bs[0], 1)
    other._uses = 1
    bs[0].end_state['RDI'] = other
    phi[(1, 'RDI')] = 'v41'
    capture(dec, bs, phi)
    assert e.text == 'Example.Emit(i)' and len(bs[0].stmts) == 2


@pytest.mark.parametrize('text', ['t42', 'v99', 'i', '0', 'null'])
def test_an_atomic_phi_source_needs_no_late_insertion(text):
    dec, bs, phi, e, _ = fixture()
    other = Expr(text, INT, 'int')
    other._defpos = (bs[0], 1)
    bs[0].end_state['RDI'] = other
    phi[(1, 'RDI')] = 'v41'
    capture(dec, bs, phi)
    assert e.text == 't0'


def test_a_complex_phi_defined_in_another_block_does_not_shift_this_definition():
    dec, bs, phi, e, _ = fixture()
    other = Expr('Example.Compute(i)', INT, 'int')
    other._defpos = (bs[1], 0)
    bs[0].end_state['RDI'] = other
    phi[(1, 'RDI')] = 'v41'
    capture(dec, bs, phi)
    assert e.text == 't0'
