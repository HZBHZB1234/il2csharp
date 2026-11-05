"""A MethodRef passed to a helper is not automatically its call identity."""
import pytest

from il2cpp import Expr
from test_stack_args import make_call_lifter, VOID, INT, FLOAT

NAME = "Example.Start<int>"
STRUCT = (0, 0x11 << 16)


def call_with_methodref(position, *, static=False, dry=False, returns=VOID,
                        params=(), registered=False, same_text=True):
    regs = {"RCX": Expr("receiver", None, "obj"),
            "RDX": Expr("argument", INT, "int")}
    value = Expr(NAME if same_text else "unrelated", None, "obj")
    value._usg_idx = 0
    regs[("RCX", "RDX", "R8", "R9")[position]] = value
    lift, ins = make_call_lifter(list(params), regs, static=static, returns=returns)
    lift.dry = dry
    lift.il.method_specs = [(0, -1, -1)]
    lift.il.generic_method_name = lambda si: NAME
    lift.il._method_spec_type_args = lambda index: None
    lift.il.candidate_return_type = lambda info: returns
    lift.il.addr_candidates = {0x2000: [("generic", 0)]} if registered else {}
    lift.il.addr_to_method = {}
    lift._call_name = lambda target: NAME if registered else "sub_2000"
    return lift, ins, value


def invoke(lift, ins):
    lift._insn(ins, [ins], 0, None, ins.next_ip)
    lift._flush_pending_calls()
    return "\n".join(row[1] for row in lift.out)


@pytest.mark.parametrize("dry", [False, True])
@pytest.mark.parametrize("returns", [VOID, INT, STRUCT])
def test_instance_methodref_in_first_gpr_keeps_raw_call(dry, returns):
    lift, ins, value = call_with_methodref(0, dry=dry, returns=returns)
    # Even an aggregate return needs an extra buffer, never fewer slots.
    lift.il.returns_sret = lambda ty: ty == STRUCT
    invoke(lift, ins)
    assert lift._call_class_args is None
    if not dry:
        text = "\n".join(row[1] for row in lift.out)
        assert text.count("sub_2000(") == 1
        assert NAME in text  # ordinary metadata argument is not silently erased
        assert ".Start<int>(" not in text
    assert value._usg_idx == 0 and value.text == NAME


@pytest.mark.parametrize("position", [1, 2, 3])
def test_instance_hidden_identity_after_receiver_still_recovers(position):
    lift, ins, _ = call_with_methodref(position)
    text = invoke(lift, ins)
    assert "receiver.Start<int>(" in text
    assert "sub_2000" not in text
    assert NAME not in text  # the trailing identity is not a source argument


@pytest.mark.parametrize("position", [0, 1, 2, 3])
def test_static_methodref_selection_is_unchanged(position):
    lift, ins, _ = call_with_methodref(position, static=True)
    text = invoke(lift, ins)
    assert NAME + "(" in text
    assert "sub_2000" not in text


def test_closed_sret_instance_identity_in_r8_still_recovers():
    lift, ins, _ = call_with_methodref(2, returns=STRUCT)
    lift.regs["RCX"] = Expr("&result", STRUCT, "ptr")
    lift.regs["RDX"] = Expr("builder", None, "obj")
    lift.il.returns_sret = lambda ty: ty == STRUCT
    text = invoke(lift, ins)
    assert "result = builder.Target();" == text
    assert "sub_2000" not in text


def test_float_parameter_does_not_invoke_legacy_exact_slot_calculator():
    lift, ins, _ = call_with_methodref(2, params=[FLOAT])
    lift.regs["XMM1"] = Expr("amount", FLOAT, "float")
    def forbidden(*args):
        raise AssertionError("negative receiver proof must not use exact slot guessing")
    lift._methodinfo_slot = forbidden
    assert "receiver.Start<int>(amount)" in invoke(lift, ins)


def test_registered_callee_identity_is_not_removed_by_negative_argument_proof():
    lift, ins, _ = call_with_methodref(0, registered=True)
    assert "sub_2000" not in invoke(lift, ins)


def test_no_text_match_preserves_existing_raw_behavior():
    lift, ins, _ = call_with_methodref(1, same_text=False)
    assert "sub_2000(receiver, unrelated)" in invoke(lift, ins)


def test_no_methodref_provenance_does_not_invent_identity():
    lift, ins, value = call_with_methodref(0)
    value._usg_idx = None
    assert "sub_2000(" in invoke(lift, ins)
