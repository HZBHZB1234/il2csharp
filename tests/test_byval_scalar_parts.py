"""Recompose small by-value call arguments only from exact scalar copies."""
from types import SimpleNamespace as NS

import pytest

from il2cpp import Expr
from test_recovery_followup import struct_lifter, F32

PAIR = (1, 0x11 << 16)
FIELD = (0, (0x0c << 16) | 6)


def fixture(width=8):
    lift = struct_lifter()
    fields = [NS(name=name, type=3) for name in ('first', 'second')[:width // 4]]
    lift.il.types += [FIELD, PAIR]
    lift.meta.fields = fields
    lift.meta.methods = []
    definition = NS(is_valuetype=True, field_start=0, field_count=len(fields),
                    flags=8, bitfield=0xc00, name='Pair', namespace='Proof',
                    method_start=0, method_count=0)
    lift.meta.typedefs.append(definition)
    lift.il._sf_field_size = lambda ty, _: (width if ty == PAIR else 4 if lift.il._type_enum(ty) == 0x0c else None)
    lift.il.instance_field_chain = lambda td: {0x10 + 4*i: (f.name, f.type) for i, f in enumerate(fields)}
    lift.il.type_name = lambda ty: 'Proof.Pair'
    lift.il._sf_subst = lambda ty, args: ty
    lift.il._closed_type_key = lambda ty: (ty[0], ty[1] & ~0xffff) if ty else None
    lift.il.returns_sret = lambda ty: False
    lift.meta.method_params = lambda m: [NS(type=4)]
    lift.il._generic_inst_args = lambda ty: None
    return lift


def packed(*values):
    e = Expr('low', None, 'bits')
    e._parts = [(4*i, v if isinstance(v, Expr) else Expr(v, F32, 'float'), 0, 4)
                for i, v in enumerate(values)]
    return e


def test_named_low_text_does_not_hide_the_other_argument_lane():
    lift = fixture()
    value = packed('left', 'right')
    before = (dict(lift.regs), dict(lift._type_hints), list(lift.out), value.text, value.ty)
    assert lift._copied_scalar_struct_arg(value, PAIR) == 'new Proof.Pair { first = left, second = right }'
    assert (lift.regs, lift._type_hints, lift.out, value.text, value.ty) == before


@pytest.mark.parametrize('width', [4, 8])
@pytest.mark.parametrize('static,sret', [(True, False), (False, False), (True, True), (False, True)])
def test_materialize_at_declared_abi_position_only(width, static, sret):
    lift = fixture(width)
    lift.il.returns_sret = lambda ty: sret
    base = int(not static) + int(sret)
    value = packed(*('left', 'right')[:width//4])
    args = ['receiver'] * base + [value.text]
    exprs = [Expr('receiver')] * base + [value]
    method = NS(is_static=static)
    actual = lift._materialize_float_lanes(args.copy(), exprs, method, None)
    expected = 'new Proof.Pair { first = left' + (', second = right' if width == 8 else '') + ' }'
    assert actual == ['receiver'] * base + [expected]


@pytest.mark.parametrize('change', ['gap', 'overlap', 'partial', 'container', 'int', 'double', 'unknown', 'call', 'address', 'missing', 'cycle'])
def test_incomplete_or_unproved_scalar_copy_declines(change):
    lift = fixture(); value = packed('left', 'right')
    if change == 'gap': value._parts.pop()
    elif change == 'overlap': value._parts.append(value._parts[0])
    elif change == 'partial': value._parts[1] = (4, value._parts[1][1], 0, 2)
    elif change == 'container': value._parts[0][1].ty = PAIR
    elif change == 'int': value._parts[0][1].ty = (0, 0x08 << 16)
    elif change == 'double': value._parts[0][1].ty = (0, 0x0d << 16)
    elif change == 'unknown': value._parts[0][1]._unk = True
    elif change == 'call': value._parts[0][1].text = 'Read()'
    elif change == 'address': value._parts[0][1].text = '&left'
    elif change == 'missing': value._parts[0][1].text = '?'
    elif change == 'cycle': value._parts[0] = (0, value, 0, 4)
    assert lift._copied_scalar_struct_arg(value, PAIR) is None


@pytest.mark.parametrize('text', ['Read()', 'owner.Read()', '((Callback)f)()', 'left++', '--left', 'left = right', 'new C()', 'await task', '?', '_', 'unknown', 'null', 'default', '&left', ''])
def test_call_or_unbound_placeholder_is_not_duplicated(text):
    lift = fixture()
    assert lift._copied_scalar_struct_arg(packed(text, 'right'), PAIR) is None


@pytest.mark.parametrize('change', ['byref', 'generic', 'class', 'enum', 'private', 'readonly', 'packed', 'explicit', 'extra', 'offset', 'fieldtype', 'whole_snapshot'])
def test_unsupported_target_and_existing_whole_snapshot_decline(change):
    lift = fixture(); ty = PAIR; value = packed('left', 'right')
    td = lift.meta.typedefs[1]
    if change == 'byref': ty = (PAIR[0], PAIR[1] | 1 << 29)
    elif change == 'generic': ty = (PAIR[0], 0x15 << 16)
    elif change == 'class': td.is_valuetype = False
    elif change == 'enum': td.bitfield |= 2; lift.il.instance_field_chain = lambda td: {0x10: ('value__', 3)}
    elif change == 'private': lift.il.types[3] = (0, (0x0c << 16) | 1)
    elif change == 'readonly': lift.il.types[3] = (0, (0x0c << 16) | 0x26)
    elif change == 'packed': td.bitfield = 0
    elif change == 'explicit': td.flags = 0x10
    elif change == 'extra': td.field_count = 1
    elif change == 'offset': lift.il.instance_field_chain = lambda td: {0x10: ('first', 3), 0x18: ('second', 3)}
    elif change == 'fieldtype': lift.il.types[3] = (0, (0x08 << 16) | 6)
    elif change == 'whole_snapshot': value.ty = PAIR; value.text = 'captured'
    assert lift._copied_scalar_struct_arg(value, ty) is None


def test_scalar_snapshot_name_wins_over_older_copy_arithmetic():
    lift = fixture()
    value = packed('source * scale', 'right')
    value.text, value.ty, value.kind = 'captured', F32, 'float'
    assert lift._copied_scalar_struct_arg(value, PAIR) == 'new Proof.Pair { first = captured, second = right }'


def test_nested_scalar_slice_keeps_captured_name_and_bounds():
    lift = fixture(); original = Expr('source', F32, 'float')
    captured = Expr('snapshot', F32, 'float'); captured._slice = (original, 0, 4)
    value = packed(captured, 'right')
    assert 'first = snapshot' in lift._copied_scalar_struct_arg(value, PAIR)
    captured._slice = (original, 0, 2)
    assert lift._copied_scalar_struct_arg(value, PAIR) is None


def test_mismatched_rendering_and_stack_argument_do_not_rewrite():
    lift = fixture(); value = packed('left', 'right'); method = NS(is_static=True)
    assert lift._materialize_float_lanes(['other'], [value], method, None) == ['other']
    lift.meta.method_params = lambda m: [NS(type=0)]*4 + [NS(type=4)]
    args = ['0']*4 + ['low']
    assert lift._materialize_float_lanes(args.copy(), [None]*4 + [value], method, None) == args


@pytest.mark.parametrize('text', [
    'owner.field', 'owner.field.x', 'vector * scale.x', 'left + right',
    'array[i]', '(float)number', 'float.NaN', '1.25', '1', '0x3f800000',
    'true', 'false', 'this', 'base',
])
def test_unbound_arithmetic_projection_and_nonfloat_literals_decline(text):
    assert fixture()._copied_scalar_struct_arg(packed(text, 'right'), PAIR) is None


@pytest.mark.parametrize('text', ['0.0f', '-0.0f', '1e-45f', '3.4028235E+38F', '.5f', '@value'])
def test_exact_float_literal_or_scalar_identifier_is_safe(text):
    result = fixture()._copied_scalar_struct_arg(packed(text, 'right'), PAIR)
    assert result == 'new Proof.Pair { first = ' + text + ', second = right }'


def test_parameterless_struct_constructor_effects_are_not_invented():
    lift = fixture()
    lift.meta.methods = [NS(name='.ctor', is_static=False, param_count=0)]
    lift.meta.typedefs[1].method_count = 1
    assert lift._copied_scalar_struct_arg(packed('left', 'right'), PAIR) is None
    lift.meta.methods[0].param_count = 2
    assert lift._copied_scalar_struct_arg(packed('left', 'right'), PAIR) is not None


@pytest.mark.parametrize('change', ['unknown', 'gap', 'int', 'byref', 'cycle'])
def test_scalar_snapshot_cannot_expand_or_retype_its_copy_evidence(change):
    lift = fixture(); value = packed('source * scale', 'right')
    value.text, value.ty, value.kind = 'captured', F32, 'float'
    leaf = value._parts[0][1]
    if change == 'unknown': leaf._unk = True
    elif change == 'gap': value._parts[0] = (0, leaf, 0, 2)
    elif change == 'int': leaf.ty = (0, 0x08 << 16)
    elif change == 'byref': leaf.ty = (0, (0x0c << 16) | (1 << 29))
    elif change == 'cycle': value._parts[0] = (0, value, 0, 4)
    assert lift._copied_scalar_struct_arg(value, PAIR) is None


@pytest.mark.parametrize('text', ['float', 'await', 'new', 'switch', 'return'])
def test_keyword_is_not_a_captured_local(text):
    assert fixture()._copied_scalar_struct_arg(packed(text, 'right'), PAIR) is None


def test_snapshot_slice_must_not_hide_unknown_origin():
    origin = Expr('unknown', F32, 'float'); origin._unk = True
    snapshot = Expr('captured', F32, 'float'); snapshot._slice = (origin, 0, 4)
    assert fixture()._copied_scalar_struct_arg(packed(snapshot, 'right'), PAIR) is None
