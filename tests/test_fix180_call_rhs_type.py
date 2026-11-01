"""fix 180: an `object` local takes the type metadata already knows.

A virtual/interface call resolved *textually* after lifting leaves its temp
untyped, so the declaration printed `object` although the callee's return
type (or the member's own type) is metadata:

    object obj9 = battleUnitModel1.IsDead();      // IsDead() : bool
    object obj2 = dateTime1.Hour;                 // Hour     : int

`_rhs_ref_type` resolves `recv.Method(args)` / `recv.Member` from the
receiver's own declaration spelling in the same body, walks the base chain by
name (and arity, for calls), and takes the static type. Decline-by-default: a
receiver that is not a declared local or `this`, an ambiguous name + arity, an
open generic without explicit call arguments, and user struct/enum types
(those could have been a box) all keep `object`.
"""
import os
import sys
from types import SimpleNamespace as NS

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from il2cpp.dec.highlevel import _HighLevelMixin  # noqa: E402

T_BOOL = (0, 0x02 << 16)
T_INT = (0, 0x08 << 16)
T_STRING = (0, 0x0e << 16)
T_FOO = (1, 0x12 << 16)          # class NS.Foo
T_STRUCT = (2, 0x11 << 16)       # struct NS.Struct
T_ENUM = (3, 0x11 << 16)         # enum NS.Mode
T_VAR = (0, 0x13 << 16)          # generic parameter
T_ARRAY = (4, 0x1d << 16)

TYPES = [T_BOOL, T_INT, T_STRING, T_FOO, T_STRUCT, T_ENUM, T_VAR, T_ARRAY]


def _method(name, params, ret, declaring=0):
    return NS(name=name, param_count=params, return_type=TYPES.index(ret),
              declaring=declaring)


def _meta(methods, typedefs=None, generic_params=None, fields=None,
          properties=None):
    typedefs = typedefs or [
        NS(index=0, name='Base', namespace='NS', flags=0, is_valuetype=False,
           is_enum=False, parent=-1, method_start=0, method_count=len(methods),
           field_start=0, field_count=0, property_start=0, property_count=0),
        NS(index=1, name='Foo', namespace='NS', flags=0, is_valuetype=False,
           is_enum=False, parent=-1, field_start=0, field_count=0,
           property_start=0, property_count=0),
        NS(index=2, name='Struct', namespace='NS', flags=0, is_valuetype=True,
           is_enum=False, parent=-1, field_start=0, field_count=0,
           property_start=0, property_count=0),
        NS(index=3, name='Mode', namespace='NS', flags=0, is_valuetype=True,
           is_enum=True, parent=-1, field_start=0, field_count=0,
           property_start=0, property_count=0),
    ]
    spans = {}
    for i, m in enumerate(methods):
        spans.setdefault(m.declaring, []).append(i)

    meta = NS(typedefs=typedefs, methods=list(methods),
              generic_parameters=list(generic_params or []),
              fields=list(fields or []), properties=list(properties or []),
              getstr=lambda s: s)
    meta.type_methods = lambda td: spans.get(td.index, [])
    meta.type_fields = lambda td: list(range(getattr(td, 'field_start', 0),
                                             getattr(td, 'field_start', 0)
                                             + getattr(td, 'field_count', 0)))
    meta.generic_parameter = lambda gi: (
        meta.generic_parameters[gi]
        if 0 <= gi < len(meta.generic_parameters) else None)
    return meta


def _decompiler(meta, types=None, chain=None):
    il = NS(types=list(types or TYPES), meta=meta,
            _type_enum=lambda t: (t[1] >> 16) & 0xFF,
            type_name=lambda t, depth=0: {
                T_BOOL: 'bool', T_INT: 'int', T_STRING: 'string',
                T_FOO: 'NS.Foo', T_STRUCT: 'NS.Struct', T_ENUM: 'NS.Mode',
                T_ARRAY: 'int[]',
            }.get((t[0], t[1]), '?'),
            base_chain_tds=lambda td: (chain(td) if chain else
                                       ((td,) if td == 0 else (td, 0))),
            typedef_full=lambda i: ('NS.' + meta.typedefs[i].name
                                    if 0 <= i < len(meta.typedefs) else ''))
    dec = _HighLevelMixin.__new__(_HighLevelMixin)
    dec.L = NS(meta=meta, il=il)
    dec._eq_typedef_map = lambda: {'NS.Foo': 1, 'NS.Base': 0}
    return dec


def _resolve(methods, rhs, decl, params=(), chain=None, self_td=0):
    m = _method('self', 0, T_INT, declaring=self_td)
    meta = _meta(methods, generic_params=params)
    return _decompiler(meta, chain=chain)._call_rhs_type(rhs, decl, m)


# -- calls ------------------------------------------------------------------

def test_a_primitive_return_types_the_local():
    methods = [_method('IsDead', 0, T_BOOL)]
    assert _resolve(methods, 'unit1.IsDead();',
                    {'unit1': ('NS.Foo', 0)}) == 'bool'


def test_a_generic_return_uses_the_call_arguments():
    methods = [NS(name='GetComponent', param_count=0,
                  return_type=TYPES.index(T_VAR), declaring=1)]
    assert _resolve(methods, 'go1.GetComponent<NS.Foo>();',
                    {'go1': ('NS.Foo', 0)},
                    params=[(0, 'T', 0, 0, 0, 0)]) == 'NS.Foo'


def test_a_reference_return_types_the_local():
    methods = [_method('GetFoo', 0, T_FOO)]
    assert _resolve(methods, 'unit1.GetFoo();',
                    {'unit1': ('NS.Foo', 0)}) == 'NS.Foo'


def test_a_user_struct_or_enum_return_declines():
    for ret in (T_STRUCT, T_ENUM):
        methods = [_method('Make', 0, ret)]
        assert _resolve(methods, 'unit1.Make();',
                        {'unit1': ('NS.Foo', 0)}) is None


def test_an_unknown_receiver_declines():
    methods = [_method('IsDead', 0, T_BOOL)]
    assert _resolve(methods, 'field1.IsDead();', {}) is None


def test_an_ambiguous_name_and_arity_declines():
    methods = [_method('Make', 0, T_BOOL), _method('Make', 0, T_INT)]
    assert _resolve(methods, 'unit1.Make();',
                    {'unit1': ('NS.Foo', 0)}) is None


def test_a_non_local_receiver_declines():
    methods = [_method('IsDead', 0, T_BOOL)]
    assert _resolve(methods, 'this.IsDead();', {}) is None


def test_an_array_return_types_the_local():
    methods = [_method('GetAll', 0, T_ARRAY)]
    assert _resolve(methods, 'unit1.GetAll();',
                    {'unit1': ('NS.Foo', 0)}) == 'int[]'


def test_a_member_chain_rhs_declines():
    methods = [_method('IsDead', 0, T_BOOL)]
    assert _resolve(methods, 'unit1.field.IsDead();',
                    {'unit1': ('NS.Foo', 0)}) is None


# -- plain member accesses --------------------------------------------------

def _member(meta, rhs, decl, self_td=0):
    m = _method('self', 0, T_INT, declaring=self_td)
    return _decompiler(meta)._member_rhs_type(rhs, decl, m)


def _field_meta(field_ty, prop=None):
    meta = _meta([], fields=[NS(name='Inner', type=TYPES.index(field_ty))],
                 properties=([prop] if prop else []))
    td0 = meta.typedefs[0]
    td0.field_start, td0.field_count = 0, 1
    td0.property_start, td0.property_count = (0, 1) if prop else (0, 0)
    return meta


def test_a_member_access_takes_the_field_type():
    meta = _field_meta(T_FOO)
    assert _member(meta, 'this.Inner', {}, self_td=0) == 'NS.Foo'


def test_a_member_access_through_a_local_takes_the_field_type():
    meta = _field_meta(T_STRING)
    assert _member(meta, 'unit1.Inner', {'unit1': ('NS.Base', 0)}) == 'string'


def test_a_property_member_uses_its_getter_return_type():
    getter = NS(name='get_Inner', param_count=0,
                return_type=TYPES.index(T_FOO), declaring=0)
    meta = _meta([getter], fields=[], properties=[('Inner', 0, -1)])
    td0 = meta.typedefs[0]
    td0.field_start, td0.field_count = 0, 0
    td0.property_start, td0.property_count = 0, 1
    assert _member(meta, 'this.Inner', {}, self_td=0) == 'NS.Foo'


def test_a_member_of_an_unknown_receiver_declines():
    meta = _field_meta(T_FOO)
    assert _member(meta, 'field1.Inner', {}) is None


def test_a_struct_member_return_declines():
    meta = _field_meta(T_STRUCT)
    assert _member(meta, 'this.Inner', {}, self_td=0) is None


def test_a_bare_identifier_member_rhs_declines():
    """`x = y;` is a copy, not a member access."""
    meta = _field_meta(T_FOO)
    assert _member(meta, 'Inner', {}) is None


# -- copies and allocations -------------------------------------------------

def _rhs(meta, rhs, decl, self_td=0):
    m = _method('self', 0, T_INT, declaring=self_td)
    return _decompiler(meta)._rhs_ref_type(rhs, decl, m)


def _typedef_with(name='Foo'):
    return NS(index=0, name=name, namespace='NS', flags=0, is_valuetype=False,
              is_enum=False, parent=-1, field_start=0, field_count=0,
              property_start=0, property_count=0, method_start=0,
              method_count=0)


def test_a_copy_of_a_reference_local_takes_its_type():
    meta = _meta([], typedefs=[_typedef_with()])
    assert _rhs(meta, 'source1;', {'source1': ('NS.Foo', 0)}) == 'NS.Foo'


def test_a_copy_of_a_primitive_local_declines():
    """`object o = num1;` may be a box; spelling `int` changes identity."""
    meta = _meta([], typedefs=[_typedef_with()])
    assert _rhs(meta, 'num1;', {'num1': ('int', 0)}) is None


def test_a_fresh_allocation_takes_its_type():
    meta = _meta([], typedefs=[_typedef_with()])
    assert _rhs(meta, 'new NS.Foo();', {}) == 'NS.Foo'


def test_an_allocation_of_a_value_type_declines():
    meta = _meta([], typedefs=[_typedef_with()])
    assert _rhs(meta, 'new NS.Struct();', {}) is None

