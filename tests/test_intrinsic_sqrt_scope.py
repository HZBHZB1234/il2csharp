"""Only proven native square-root construction binds the framework owner."""
import pytest

from il2cpp import Decompiler, Expr
from il2cpp.csharp import UsingTracker, strip_namespaces
from csharp_smoke import DOUBLE, execute as call_execute, fixture
from test_native_values import execute, lifter


@pytest.mark.parametrize("argument", ["value", "Math.Sqrt(value)",
                                      "System.Math.Sqrt(value)"])
def test_intrinsic_qualifies_only_its_own_call_not_argument_text(argument):
    lift = lifter({"XMM1": Expr(argument, DOUBLE, "float")})
    execute(lift, "f20f51c1")
    assert lift.regs["XMM0"].text == "global::System.Math.Sqrt(" + argument + ")"


@pytest.mark.parametrize("unknown", [False, True])
def test_proven_helper_qualifies_owner_without_inventing_arguments(unknown):
    lift = fixture()
    lift.rt_sqrt = 0x2000
    value = Expr("value", DOUBLE, "float")
    value._unk = unknown
    lift.regs = {"RCX": Expr("stale", None, "int"), "XMM0": value}
    call_execute(lift, "e8fb0f0000")
    result = lift.regs["XMM0"]
    assert result.text == "global::System.Math.Sqrt(" + ("?" if unknown else "value") + ")"
    assert result.ty == DOUBLE
    assert "stale" not in result.text


@pytest.mark.parametrize("uses", [set(), {"System"}, {"System.Math"},
                                  {"System", "System.Math"}])
@pytest.mark.parametrize("namespace", ["", "Consumer", "System.Consumer"])
def test_explicit_global_intrinsic_survives_namespace_shortening(uses, namespace):
    lines = ["return global::System.Math.Sqrt(value);"]
    assert strip_namespaces(lines, uses, namespace) == lines


def test_final_render_does_not_rewrite_ordinary_math_calls_or_literals():
    lines = ["return Math.Sqrt(value);", "return System.Math.Sqrt(value);",
             'Log("Math.Sqrt(value)");', "// Math.Sqrt(value)",
             "/* Math.Sqrt(value) */", "return global::System.Math.Sqrt(value);"]
    assert Decompiler.__new__(Decompiler)._render(lines) == lines


@pytest.mark.parametrize("rooted", ["global::System.Math.Sqrt(value)",
                                   "alias::System.Math.Sqrt(value)"])
def test_rooted_intrinsic_does_not_import_a_namespace(rooted):
    tracker = UsingTracker()
    tracker.add_text("return " + rooted + ";")
    assert tracker.used == set()


def test_alias_root_keeps_unrooted_generic_arguments_visible():
    tracker = UsingTracker()
    tracker.add_text("global::Root.Box<Other.Element> value;")
    assert tracker.used == {"Other"}


def test_ordinary_qualified_call_still_imports_its_owner_namespace():
    tracker = UsingTracker()
    tracker.add_text("System.Math.Sqrt(value)")
    assert tracker.used == {"System.Math"}
