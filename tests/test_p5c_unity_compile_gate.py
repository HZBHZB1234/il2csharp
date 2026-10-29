"""Roadmap P5 slice C: the game-vs-engine compile gate.

The gate always ran with NO reference closure, so every external name was
a binding error and the number was dominated by unresolved externals.
`--unity` references an installed Editor's own `Data/Managed/UnityEngine`
assemblies -- the TRUE names and signatures -- so the binding tier
measures the decompiler instead.

Measured on the game-only `Assembly-CSharp` (2026-10-28, Editor
2022.3.61f1c1, 87 engine dlls): syntax 75 / binding 12 with refs=87 and
syntax 75 / binding 12 with refs=0. The closure does NOT move the count:
the 12 are 12 `CS8641 "else" without a matching if` sites, i.e. real
decompiler defects (fix 165 family F), not unresolved engine names.
That is the finding these pins protect -- if a future change makes the
refs matter, this number moves and the test says so.
"""
import os
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "tools"))

from compile_gate import unity_refs, unity_framework_refs, run_gate


def _fake_editor(root):
    """A minimal Editor-shaped tree: Data/Managed/UnityEngine/*.dll."""
    eng = root / "Data" / "Managed" / "UnityEngine"
    eng.mkdir(parents=True)
    for n in ("UnityEngine.dll", "UnityEngine.CoreModule.dll", "notadll.txt"):
        (eng / n).write_bytes(b"x")
    return root


def test_unity_refs_from_editor_root(tmp_path):
    root = _fake_editor(tmp_path / "Editor")
    refs = unity_refs(str(root))
    assert len(refs) == 2
    assert all(r.endswith(".dll") for r in refs)
    assert sorted(os.path.basename(r) for r in refs) == [
        "UnityEngine.CoreModule.dll", "UnityEngine.dll"]


def test_unity_refs_from_managed_dir_directly(tmp_path):
    root = _fake_editor(tmp_path / "Editor")
    refs = unity_refs(str(root / "Data" / "Managed" / "UnityEngine"))
    assert len(refs) == 2


def test_unity_refs_prefers_managed_dir_over_install_root(tmp_path):
    """An install root holds native helpers (Calc.dll, FreeImage.dll) and
    no managed engine assemblies; the resolver must descend, not take the
    first directory that exists."""
    root = _fake_editor(tmp_path / "Editor")
    (root / "Calc.dll").write_bytes(b"native")
    refs = unity_refs(str(root))
    assert len(refs) == 2
    assert not any(r.endswith("Calc.dll") for r in refs)


def test_unity_refs_absent_path_is_empty():
    assert unity_refs(None) == []
    assert unity_refs("C:/definitely/not/here") == []


def test_run_gate_reports_ref_count(tmp_path, monkeypatch):
    (tmp_path / "A.cs").write_text("class A{}", encoding="utf-8")

    class P:
        stdout = "A.cs(1,1): error CS1002: ; expected\n"
        stderr = ""
        returncode = 1

    import compile_gate
    monkeypatch.setattr(compile_gate, "find_csc", lambda explicit=None: "csc")
    monkeypatch.setattr(compile_gate.subprocess, "run", lambda *a, **k: P())
    rep = run_gate(str(tmp_path), refs=["a.dll", "b.dll"])
    assert rep["refs"] == 2
    assert rep["syntax"] == 1


def test_run_gate_refs_default_zero(tmp_path, monkeypatch):
    (tmp_path / "A.cs").write_text("class A{}", encoding="utf-8")

    class P:
        stdout = ""
        stderr = ""
        returncode = 0

    import compile_gate
    monkeypatch.setattr(compile_gate, "find_csc", lambda explicit=None: "csc")
    monkeypatch.setattr(compile_gate.subprocess, "run", lambda *a, **k: P())
    rep = run_gate(str(tmp_path))
    assert rep["refs"] == 0


def test_run_gate_writes_refs_into_the_response_file(tmp_path, monkeypatch):
    """The references must reach csc; a silent drop would make the
    game-vs-engine mode a no-op that still reports a ref count."""
    (tmp_path / "A.cs").write_text("class A{}", encoding="utf-8")
    seen = {}

    class P:
        stdout = ""
        stderr = ""
        returncode = 0

    import compile_gate

    def fake_run(cmd, **kw):
        rsp = [c for c in cmd if c.startswith("@")]
        assert rsp, cmd
        seen["rsp"] = open(rsp[0][1:], encoding="utf-8").read()
        return P()

    monkeypatch.setattr(compile_gate, "find_csc", lambda explicit=None: "csc")
    monkeypatch.setattr(compile_gate.subprocess, "run", fake_run)
    run_gate(str(tmp_path), refs=["/x/UnityEngine.dll"])
    assert '/r:"/x/UnityEngine.dll"' in seen["rsp"], seen["rsp"]


# -- 2026-10-29: <root>/Editor/Data layout + the BCL resolver --------------

def _editor_root(root):
    """A Unity-6000-shaped Editor: <root>/Editor/Data/..."""
    ed = root / "Editor"
    eng = ed / "Data" / "Managed" / "UnityEngine"
    eng.mkdir(parents=True)
    for n in ("UnityEngine.dll", "UnityEngine.CoreModule.dll"):
        (eng / n).write_bytes(b"x")
    ns = ed / "Data" / "NetStandard"
    ref = ns / "ref" / "2.1.0"
    ref.mkdir(parents=True)
    (ref / "netstandard.dll").write_bytes(b"x")
    netfx = ns / "compat" / "2.1.0" / "shims" / "netfx"
    netfx.mkdir(parents=True)
    (netfx / "mscorlib.dll").write_bytes(b"x")
    std = ns / "compat" / "2.1.0" / "shims" / "netstandard"
    std.mkdir(parents=True)
    (std / "System.Runtime.dll").write_bytes(b"x")
    return root


def test_unity_refs_handles_the_root_editor_data_layout(tmp_path):
    """A Unity 6000 install has Editor/Data/Managed/UnityEngine, not
    Data/Managed/UnityEngine at the root -- the resolver must accept the
    Editor dir too (this is the layout the user pointed at)."""
    root = _editor_root(tmp_path / "unity_editor_6000")
    refs = unity_refs(str(root))
    assert len(refs) == 2
    assert any(r.endswith("UnityEngine.CoreModule.dll") for r in refs)


def test_unity_refs_accepts_the_editor_subdir(tmp_path):
    root = _editor_root(tmp_path / "unity_editor_6000")
    refs = unity_refs(str(root / "Editor"))
    assert len(refs) == 2


def test_unity_framework_refs_collects_the_bcl_shims(tmp_path):
    root = _editor_root(tmp_path / "unity_editor_6000")
    fw = unity_framework_refs(str(root))
    names = sorted(os.path.basename(x) for x in fw)
    assert names == ["System.Runtime.dll", "mscorlib.dll", "netstandard.dll"], names


def test_unity_framework_refs_empty_without_editor(tmp_path):
    assert unity_framework_refs(None) == []
    assert unity_framework_refs(str(tmp_path)) == []
