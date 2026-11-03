"""Only exact interface receiver, method and delegate signatures prove a ctor."""
from types import SimpleNamespace as NS

import pytest

from il2cpp import Expr, Lifter

VOID = (0, 1 << 16)
INT = (0, 8 << 16)
FLOAT = (0, 12 << 16)
DELEGATE = (0, 0x12 << 16)
IFACE = (2, 0x12 << 16)


def setup():
    lift = Lifter.__new__(Lifter)
    methods = [NS(name='.ctor', declaring=0, param_count=2, is_static=False,
                  generic_container=-1, return_type=0),
               NS(name='Invoke', declaring=0, param_count=1, is_static=False,
                  generic_container=-1, return_type=0),
               NS(name='OnEvent', declaring=2, param_count=1, is_static=False,
                  generic_container=-1, return_type=0)]
    lift.meta = NS(methods=methods,
        typedefs=[NS(name='Handler', namespace='', flags=0),
                  NS(name='MulticastDelegate', namespace='System', flags=0),
                  NS(name='IEvents', namespace='', flags=0x20)],
        method_params=lambda m: [NS(type=1)] * m.param_count)
    lift.il = NS(types=[VOID, INT], method_specs=[],
        base_chain_tds=lambda td: (0, 1) if td == 0 else (td,),
        _closed_type_key=lambda ty: ty if ty != FLOAT else None,
        _subst_closed=lambda ty, ca, ma: ty,
        _method_spec_type_args=lambda i: None)
    lift._generic_class_args = lambda ty: None
    lift._delegate_invoke_method = lambda ty: 1
    recv = Expr('handler1', DELEGATE, 'obj'); recv._alloc = 'new Handler()'
    target = Expr('instance', IFACE, 'obj')
    pointer = Expr('methodInfo', None, 'ptr')
    pointer._ifm = (2, None, 'IEvents.OnEvent', VOID, 'method')
    pointer._ifrecv = target
    args = [recv, target, pointer, Expr('0', None, 'int')]
    return lift, [('method', 0)], args


def test_exact_interface_method_constructs_delegate_once():
    lift, cands, args = setup()
    assert lift._interface_delegate_constructor(cands, args) == (
        ('method', 0), 'instance.OnEvent')


@pytest.mark.parametrize('fault', [
    'not_fresh', 'wrong_receiver', 'method_pointer', 'opaque', 'bad_slot',
    'not_interface', 'not_delegate', 'static', 'generic', 'wrong_signature',
    'open_signature', 'wrong_return', 'missing_candidate', 'extra_argument',
    'unknown_receiver', 'complex_receiver', 'malformed',
])
def test_unproven_shapes_decline(fault):
    lift, cands, args = setup()
    if fault == 'not_fresh': args[0]._alloc = None
    elif fault == 'wrong_receiver': args[1] = Expr('other', IFACE, 'obj')
    elif fault == 'method_pointer': args[2]._ifm = args[2]._ifm[:4] + ('methodPtr',)
    elif fault == 'opaque': args[2]._ifm = None
    elif fault == 'bad_slot': args[2]._ifm = (99, None, 'Bad', VOID, 'method')
    elif fault == 'not_interface': lift.meta.typedefs[2].flags = 0
    elif fault == 'not_delegate': lift.il.base_chain_tds = lambda td: (td,)
    elif fault == 'static': lift.meta.methods[2].is_static = True
    elif fault == 'generic': lift.meta.methods[2].generic_container = 1
    elif fault == 'wrong_signature': lift.meta.methods[2].param_count = 0
    elif fault == 'open_signature': lift.il.types[1] = FLOAT
    elif fault == 'wrong_return': lift.meta.methods[2].return_type = 1
    elif fault == 'missing_candidate': cands = []
    elif fault == 'extra_argument': args[3] = Expr('work()', None, 'obj')
    elif fault == 'unknown_receiver': args[1]._unk = True
    elif fault == 'complex_receiver': args[1].text = 'GetReceiver()'
    elif fault == 'malformed': args[2]._ifm = ('bad',)
    assert lift._interface_delegate_constructor(cands, args) is None


def test_same_spelling_does_not_prove_receiver_identity():
    lift, cands, args = setup()
    args[1] = Expr('instance', IFACE, 'obj')
    assert lift._interface_delegate_constructor(cands, args) is None


def test_receiver_provenance_survives_expression_copy():
    lift, cands, args = setup()
    copied = Lifter._copy_expr(args[2])
    assert copied._ifrecv is args[1]


@pytest.mark.parametrize('inst, expected', [(1, True), (2, False), (-1, False)])
def test_generic_ctor_requires_exact_closed_class_arguments(inst, expected):
    lift, _, args = setup()
    lift._generic_class_args = lambda ty: [INT] if ty == DELEGATE else None
    lift.il.method_specs = [(0, inst, -1)]
    lift.il._method_spec_type_args = lambda i: [INT] if i == 1 else [VOID] if i == 2 else None
    result = lift._interface_delegate_constructor([('generic', 0)], args)
    assert (result is not None) is expected


def test_duplicate_equivalent_owners_remain_ambiguous():
    lift, _, args = setup()
    lift._generic_class_args = lambda ty: [INT] if ty == DELEGATE else None
    lift.il.method_specs = [(0, 1, -1), (0, 1, -1)]
    lift.il._method_spec_type_args = lambda i: [INT]
    assert lift._interface_delegate_constructor([('generic', 0), ('generic', 1)], args) is None


def test_return_byref_difference_is_not_erased():
    lift, cands, args = setup()
    lift.il.types.append((VOID[0], VOID[1] | (1 << 29)))
    lift.meta.methods[2].return_type = 2
    assert lift._interface_delegate_constructor(cands, args) is None


def test_field_pointer_copies_receiver_proof_without_using_recv():
    lift, _, args = setup()
    base = Expr('resolved', None, 'ptr')
    base._ifm = args[2]._ifm[:4]
    base._ifrecv = args[1]
    value = lift._field_expr(base, 8, 8)
    assert value._ifrecv is args[1] and value.recv is None
    assert value._ifm[-1] == 'method'
