"""Parameter attrs live in Il2CppType: out is not an unprovable ref guess."""
from types import SimpleNamespace as NS

import pytest

from il2cpp import Expr
from il2cpp.emitter import Emitter
from test_stack_args import make_call_lifter

INT = (0, 0x08 << 16)
REF_INT = (0, (0x08 << 16) | (1 << 29))
OUT_INT = (0, REF_INT[1] | 2)


def emitter_for(ty):
    e = Emitter.__new__(Emitter)
    e.il = NS(types=[ty], type_name=lambda _: 'int')
    e.meta = NS(method_params=lambda _: [NS(type=0, name='value')])
    e._param_default_suffix = lambda *a: ('', False)
    return e


@pytest.mark.parametrize('attrs,expected', [(0, 'ref '), (1, 'ref '),
                                            (2, 'out '), (3, 'ref ')])
def test_parameter_declaration_distinguishes_out_only(attrs, expected):
    ty = (0, REF_INT[1] | attrs)
    assert emitter_for(ty).render_params(None) == expected + 'int value'


def test_non_byref_out_attribute_does_not_create_out_parameter():
    assert emitter_for((0, INT[1] | 2)).render_params(None) == 'int value'


@pytest.mark.parametrize('ty,expected', [(REF_INT, 'ref value'),
                                       (OUT_INT, 'out value')])
def test_address_argument_uses_declared_parameter_modifier(ty, expected):
    e = Expr('&value', None, 'ptr')
    lift, _ = make_call_lifter([ty], {'RCX': e})
    args = ['&value']
    lift._hint_arg_types(args, [e], 0, None)
    assert args == [expected]


@pytest.mark.parametrize('ty,expected', [(REF_INT, 'ref value'),
                                       (OUT_INT, 'out value')])
def test_forwarded_byref_parameter_preserves_address_without_ampersand(ty, expected):
    # Entry seeds byref params with their plain C# name; it is still an address.
    e = Expr('value', REF_INT, 'int')
    lift, _ = make_call_lifter([ty], {'RCX': e})
    lift._entry_byrefs = {'value': REF_INT}
    args = ['value']
    lift._hint_arg_types(args, [e], 0, None)
    assert args == [expected]


@pytest.mark.parametrize('ty,kind', [(None, 'int'), (INT, 'int')])
def test_unproved_plain_argument_does_not_gain_byref_modifier(ty, kind):
    e = Expr('value', ty, kind)
    lift, _ = make_call_lifter([OUT_INT], {'RCX': e})
    args = ['value']
    lift._hint_arg_types(args, [e], 0, None)
    assert args == ['value']


def test_interface_method_signature_uses_out_attr():
    from test_review113_type_decls import make_emitter, td_base, P, I_BOOL
    e = make_emitter()
    e.il.types = [(0, 0x01 << 16), (0, 0x02 << 16), OUT_INT]
    e.il.type_name = lambda t: 'bool' if t[1] >> 16 & 0xff == 2 else 'int'
    td = td_base(name='IFoo', flags=0x20 | 0x80)
    m = NS(name='TryGet', is_static=False, return_type=I_BOOL,
           flags=0x400, declaring=10, generic_container=-1,
           parameter_start=0, ps=[P(2, 'value')])
    assert e.method_sig(m, td) == 'bool TryGet(out int value)'


def test_delegate_signature_uses_same_modifier_as_methods():
    from test_review113_type_decls import make_emitter, td_base, P
    inv = NS(name='Invoke', is_static=False, return_type=0, declaring=30,
             generic_container=-1, parameter_start=0, ps=[P(1, 'value')])
    td = td_base(index=30, name='TryValue', methods=[inv])
    td.mis = [0]
    e = make_emitter(methods=[inv], typedefs=[None] * 31)
    e.il.types = [(0, 0x02 << 16), OUT_INT]
    e.meta.typedefs[30] = td
    e.il.type_name = lambda t: 'bool' if t[1] >> 16 & 0xff == 2 else 'int'
    out = []
    assert e.emit_delegate(td, out, '')
    assert out[1] == 'internal delegate bool TryValue(out int value);'


def test_generic_return_abi_does_not_confidently_rewrite_forwarded_address():
    e = Expr('value', REF_INT, 'int')
    lift, _ = make_call_lifter([OUT_INT], {'RCX': e})
    args = ['value']
    lift._hint_arg_types(args, [e], 0, (0, 0x15 << 16))
    assert args == ['value']


def test_byref_typed_synthetic_local_does_not_gain_entry_alias_forwarding():
    e = Expr('type3', REF_INT, 'int')
    lift, _ = make_call_lifter([OUT_INT], {'RCX': e})
    lift._entry_byrefs = {'value': REF_INT}
    args = ['type3']
    lift._hint_arg_types(args, [e], 0, None)
    assert args == ['type3']
