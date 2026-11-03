"""Metadata string parameters survive generic GPR display categories.

Original synthetic expressions only; no licensed method bodies or bytes.
"""
from types import SimpleNamespace as NS

import pytest

from il2cpp import Expr, Lifter

STRING = (0, 0x0e << 16)
INT = (0, 0x08 << 16)


def lift():
    x = Lifter.__new__(Lifter)
    x.slot_types = {}
    x._type_hints = {}
    x._entry_strings = {'s': STRING, 'value1': STRING, 'string_': STRING}
    x._td_of = lambda ty: None
    x.il = NS(_type_enum=lambda ty: (ty[1] >> 16) & 255)
    x.meta = NS(typedefs=[])
    return x


@pytest.mark.parametrize('kind', ['?', 'int', 'obj', 'str'])
@pytest.mark.parametrize('text', ['s', 'value1', 'string_'])
def test_exact_string_dword_load_ignores_generic_merge_kind(kind, text):
    e = lift()._field_expr(Expr(text, STRING, kind), 0x10, 4, load=True)
    assert e.text == text + '.Length'
    assert (e.ty, e.kind) == (INT, 'int')


@pytest.mark.parametrize('kind', ['?', 'int', 'obj'])
@pytest.mark.parametrize('size', [1, 2, 8, 16])
def test_no_length_invention_at_other_access_widths(kind, size):
    e = lift()._field_expr(Expr('s', STRING, kind), 0x10, size, load=True)
    assert '.Length' not in e.text


@pytest.mark.parametrize('kind', ['?', 'int', 'obj'])
@pytest.mark.parametrize('disp', [0, 0x0c, 0x14, 0x18, 0x20])
def test_no_length_invention_at_other_offsets(kind, disp):
    e = lift()._field_expr(Expr('s', STRING, kind), disp, 4, load=True)
    assert '.Length' not in e.text


@pytest.mark.parametrize('kind', ['?', 'int', 'obj'])
def test_no_length_lvalue_from_type_fact(kind):
    e = lift()._field_expr(Expr('s', STRING, kind), 0x10, 4)
    assert '.Length' not in e.text


@pytest.mark.parametrize('kind', ['ptr', 'local', 'klass', 'kmember'])
def test_address_and_runtime_internal_categories_decline(kind):
    e = lift()._field_expr(Expr('s', STRING, kind), 0x10, 4, load=True)
    assert '.Length' not in e.text


@pytest.mark.parametrize('ty', [None, INT, (0, (0x0e << 16) | (1 << 29)),
                               (0, 0x0f << 16), (0, 0x10 << 16)])
def test_only_nonbyref_string_type_qualifies(ty):
    x = lift()
    x.il.type_from_ptr = lambda _: None
    e = x._field_expr(Expr('value1', ty, 'int'), 0x10, 4, load=True)
    assert '.Length' not in e.text


def test_text_and_hint_alone_do_not_establish_exact_base_type():
    x = lift()
    x._type_hints['s'] = STRING
    e = x._field_expr(Expr('s', None, 'int'), 0x10, 4, load=True)
    assert '.Length' not in e.text


def test_address_text_never_becomes_managed_receiver():
    e = lift()._field_expr(Expr('&s', STRING, 'int'), 0x10, 4, load=True)
    assert '.Length' not in e.text


@pytest.mark.parametrize('kind', ['?', 'int', 'obj'])
def test_original_synthetic_native_dword_read_uses_type_fact(kind):
    from iced_x86 import Instruction, Code, Register, MemoryOperand
    x = lift()
    x.regs = {'RCX': Expr('s', STRING, kind)}
    ins = Instruction.create_reg_mem(Code.MOV_R32_RM32, Register.EAX,
                                     MemoryOperand(Register.RCX, displ=0x10))
    e = x._read_mem_raw(ins, str(ins))
    assert (e.text, e.ty, e.kind) == ('s.Length', INT, 'int')



@pytest.mark.parametrize('text', ['(s + 1)', '~s', 'this.caption', 'GetCaption()',
                                  'phi1', '123', 's[0]'])
def test_string_tuple_without_metadata_parameter_identity_declines(text):
    e = lift()._field_expr(Expr(text, STRING, 'int'), 0x10, 4, load=True)
    assert '.Length' not in e.text


def test_unknown_metadata_parameter_value_declines():
    e = Expr('s', STRING, 'int')
    e._unk = True
    assert '.Length' not in lift()._field_expr(e, 0x10, 4, load=True).text


def test_missing_or_conflicting_parameter_identity_declines():
    for facts in ({}, {'s': INT}):
        x = lift()
        x._entry_strings = facts
        assert '.Length' not in x._field_expr(Expr('s', STRING, 'int'),
                                             0x10, 4, load=True).text


def test_real_entry_setup_records_strings_and_resets_on_each_method():
    x = lift()
    x.regs = {}
    x.il.types = [(0, 0x01 << 16), STRING, (0, (0x0e << 16) | (1 << 29)), INT]
    x.il.returns_sret = lambda _: False
    x.il._return_value_register = lambda _: 'RAX'
    params = [NS(name='s', type=1), NS(name='byref', type=2), NS(name='number', type=3),
              NS(name='string', type=1), NS(name='stacked', type=1)]
    x.meta.method_params = lambda _: params
    method = NS(return_type=0, is_static=True, generic_container=-1)
    owner = NS(index=0)
    x._setup_entry(method, owner)
    assert x._entry_strings == {'s': STRING, 'string_': STRING, 'stacked': STRING}
    assert 'byref' in x._entry_byrefs
    assert x._field_expr(x.regs['RCX'], 0x10, 4, load=True).text == 's.Length'
    assert x._field_expr(x.stack_values['stacked'], 0x10, 4,
                         load=True).text == 'stacked.Length'
    params.clear()
    x._setup_entry(method, owner)
    assert x._entry_strings == {}


@pytest.mark.parametrize('extra', [[], ['s = other;'], ['Visit(s[v1]);']])
def test_string_length_does_not_enter_array_only_foreach_rewrite(extra):
    from il2cpp import Decompiler
    d = Decompiler.__new__(Decompiler)
    d.L = lift()
    d._var_types = {}
    lines = ['for (int v1 = 0; v1 < s.Length; v1++)', '{',
             'Visit(s[v1]);'] + extra + ['}']
    assert d._foreach_sugar(list(lines)) == lines


def test_array_foreach_path_is_unchanged():
    from il2cpp import Decompiler
    d = Decompiler.__new__(Decompiler)
    d.L = lift()
    d._var_types = {}
    d._array_elem_type = lambda _: 'char'
    lines = ['for (int v1 = 0; v1 < arr.Length; v1++)', '{',
             'Visit(arr[v1]);', '}']
    result = d._foreach_sugar(list(lines))
    assert result[0].startswith('foreach (char ')
    assert result[0].endswith(' in arr)')
