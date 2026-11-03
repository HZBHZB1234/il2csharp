"""Resolved reference calls must retain one native call's object identity."""
import pytest

from test_stack_args import make_call_lifter, INT

CLASS = (0, 0x12 << 16)


def run_call(ty=CLASS, name="Create", dry=False, valuetype=False, resolved=True):
    lift, ins = make_call_lifter([], {}, returns=ty, name=name)
    lift.dry = dry
    lift._td_of = lambda _: 0 if resolved else None
    lift.meta.typedefs[0].is_valuetype = valuetype
    lift._insn(ins, [ins], 0, None, ins.next_ip)
    return lift


def statements(lift):
    return [s[1] for s in lift.out]


def test_reference_factory_is_bound_before_field_text_is_copied():
    lift = run_call()
    value = lift.regs["RAX"]
    # These consumers snapshot text, not the Expr itself. Later lazy _bind
    # cannot reliably rewrite their field/condition renderings across blocks.
    a, b = value.text + ".version", value.text + ".core.version"
    assert statements(lift) == ["var t0 = Example.Create();"]
    assert (a, b) == ("t0.version", "t0.core.version")
    assert not getattr(lift, "_pending_calls", None)


def test_ignored_reference_result_retains_its_call_once():
    lift = run_call()
    lift._flush_pending_calls()
    assert statements(lift) == ["var t0 = Example.Create();"]


def test_distinct_identical_calls_keep_distinct_native_identities():
    lift = run_call()
    first = lift.regs["RAX"]
    _, ins = make_call_lifter([], {})
    lift._insn(ins, [ins], 0, None, ins.next_ip)
    assert statements(lift) == ["var t0 = Example.Create();", "var t1 = Example.Create();"]
    assert first.text == "t0"
    assert lift.regs["RAX"].text == "t1"


@pytest.mark.parametrize("te", [0x0e, 0x1c, 0x1d, 0x14])
def test_non_class_reference_results_keep_existing_consumer_typing(te):
    assert not statements(run_call((0, te << 16)))


@pytest.mark.parametrize("ty,name,dry,valuetype,resolved", [
    (INT, "Create", False, False, True),
    ((0, 0x11 << 16), "Create", False, True, True),
    ((0, 0x15 << 16), "Create", False, True, True),
    ((0, 0x15 << 16), "Create", False, False, True),
    ((0, 0x15 << 16), "Create", False, False, False),
    ((0, 0x13 << 16), "Create", False, False, False),
    ((0, (0x12 << 16) | (1 << 29)), "Create", False, False, True),
    (CLASS, "Create", False, False, False),
    (CLASS, "get_Current", False, False, True),
    (CLASS, "Create", True, False, True),
])
def test_unproven_value_byref_getter_and_dry_returns_stay_lazy(ty, name, dry, valuetype, resolved):
    lift = run_call(ty, name, dry, valuetype, resolved)
    assert not statements(lift)
    assert lift.regs["RAX"].text == ("Example.Current" if name == "get_Current" else "Example.Create()")


def test_method_generic_substitution_is_not_frozen_as_object():
    lift, ins = make_call_lifter([], {}, returns=CLASS, name="GetOrAdd")
    lift.meta.methods[0].generic_container = 0
    lift._insn(ins, [ins], 0, None, ins.next_ip)
    assert not statements(lift)
    assert "(" in lift.regs["RAX"].text


@pytest.mark.parametrize("static,params,owner", [(False, [], 0),
                                               (True, [INT], 0),
                                               (True, [], 1)])
def test_only_static_nullary_own_class_factories_are_bound(static, params, owner):
    lift, ins = make_call_lifter(params, {}, returns=CLASS, static=static)
    lift._td_of = lambda _: owner
    lift._insn(ins, [ins], 0, None, ins.next_ip)
    assert not statements(lift)
