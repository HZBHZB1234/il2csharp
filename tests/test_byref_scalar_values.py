"""Managed byrefs are addresses natively but values in C# loads/stores."""
import pytest

from il2cpp import Expr
from test_native_values import lifter as native_lifter, execute, SHORT, INT, FLOAT, OBJECT, ARRAY


def lifter(regs=None):
    lift = native_lifter(regs)
    # Model the method's declared byref parameters, not inferred locals.
    lift._entry_byrefs = {e.text: e.ty for e in lift.regs.values()
                          if e.ty is not None and (e.ty[1] >> 29) & 1}
    return lift


def byref(ty, attrs=2):
    return (ty[0], ty[1] | (1 << 29) | attrs)


@pytest.mark.parametrize('ty,code,expected', [
    (SHORT, '66c7013412', 'value = 4660;'),
    (INT, 'c701ffffffff', 'value = -1;'),
    ((0, 2 << 16), 'c60101', 'value = true;'),
])
def test_exact_byref_immediate_store_assigns_the_parameter(ty, code, expected):
    lift = lifter({'RCX': Expr('value', byref(ty), 'int')})
    assert execute(lift, code) == [expected]
    assert lift._lv_ty == ty


@pytest.mark.parametrize('ty,kind,code', [
    (SHORT, 'int', '0fbf01'), (INT, 'int', '8b01'),
    (FLOAT, 'float', 'f30f1001'), (OBJECT, 'obj', '488b01'),
    (ARRAY, 'arr', '488b01'),
])
def test_exact_byref_load_removes_address_type_before_further_use(ty, kind, code):
    lift = lifter({'RCX': Expr('value', byref(ty), 'int')})
    execute(lift, code)
    result = lift.regs['XMM0' if kind == 'float' else 'RAX']
    assert result.text == 'value'
    assert result.ty == ty
    assert result.kind == kind


@pytest.mark.parametrize('ty,kind', [(SHORT, 'int'), (OBJECT, 'obj'), (ARRAY, 'arr')])
def test_byref_copies_keep_the_address_until_an_actual_memory_access(ty, kind):
    lift = lifter({'RCX': Expr('value', byref(ty), kind)})
    execute(lift, '488bd1')  # mov rdx, rcx -- pointer copy, NOT dereference
    assert lift.regs['RDX'].ty == byref(ty)


@pytest.mark.parametrize('ty,disp,size,text,unknown', [
    (byref(SHORT), 0, 4, 'value', False),   # overwrites more than one short
    (byref(INT), 0, 1, 'value', False),     # partial write
    (byref(INT), 4, 4, 'value', False),     # interior pointer
    (INT, 0, 4, 'value', False),            # not byref
    (byref((0, 0x11 << 16)), 0, 4, 'value', False),  # aggregate
    (byref((0, 0x15 << 16)), 0, 8, 'value', False),  # unknown generic layout
    (byref(INT), 0, 4, 'value + 4', False), # not a source variable
    (byref(INT), 0, 4, 'value', True),      # stale entry register
])
def test_unproved_byref_dereferences_decline(ty, disp, size, text, unknown):
    lift = lifter()
    value = Expr(text, ty, 'int'); value._unk = unknown
    assert lift._byref_value(value, disp, size) is None


def test_out_reference_store_does_not_write_the_referenced_objects_header():
    lift = lifter({'RCX': Expr('result', byref(OBJECT), 'obj'),
                   'RDX': Expr('item', OBJECT, 'obj')})
    assert execute(lift, '488911') == ['result = item;']


def test_indexed_memory_store_is_not_a_whole_byref_assignment():
    lift = lifter({'RCX': Expr('value', byref(INT), 'int'),
                   'RAX': Expr('index', INT, 'int')})
    out = execute(lift, 'c7048107000000')
    assert len(out) == 1 and out[0] != 'value = 7;'


def test_overwrite_freezes_loaded_value_but_not_its_byref_address():
    lift = lifter({'RCX': Expr('value', byref(INT, attrs=0), 'int')})
    out = execute(lift, '8b01c70107000000')  # eax = *p; *p = 7
    assert out == ['var t0 = value;', 'value = 7;']
    assert lift.regs['RCX'].text == 'value'
    assert lift.regs['RCX'].ty == byref(INT, attrs=0)
    assert lift.regs['RAX'].text == 't0'
    assert lift.regs['RAX'].ty == INT
    out = execute(lift, 'c70108000000')
    assert out[-1] == 'value = 8;'


def test_byref_typed_phi_is_not_an_emitted_ref_alias():
    lift = lifter({'RCX': Expr('value', byref(INT), 'int')})
    synthetic = Expr('type3', byref(INT), 'int')
    assert lift._byref_value(synthetic, 0, 4) is None
    frozen = lift._kill_one(synthetic, 'type3', {})
    assert frozen.text != 'type3'
    assert len(lift.out) == 1


def test_entry_name_with_mismatched_type_does_not_prove_an_alias():
    lift = lifter({'RCX': Expr('value', byref(INT), 'int')})
    assert lift._byref_value(Expr('value', byref(SHORT), 'int'), 0, 2) is None


def test_no_entry_metadata_means_no_managed_alias_even_with_byref_type():
    lift = native_lifter({'RCX': Expr('value', byref(INT), 'int')})
    assert lift._byref_value(lift.regs['RCX'], 0, 4) is None
