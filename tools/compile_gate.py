"""Compile gate for emitted trees (decl-gate v2, last item).

Runs Roslyn over one emitted image directory and reports error
counts split into syntax (gated: must be zero) versus binding
(report only: game images have no reference closure here, and
mscorlib self-hosts, so unresolved externals are expected noise).
Called after diff_decls passes; never merged into decl grammar.

Usage: python compile_gate.py --tree <imgdir> [--assembly NAME]
         [--csc-dll PATH] [--timeout SEC]
Exit: 0 iff zero syntax errors, 1 on syntax errors, 2 on usage errors.
"""
import argparse
import glob
import os
import re
import subprocess
import sys
import tempfile

ERR_RX = re.compile(
    r"^(.*)\((\d+)(?:,(\d+))?\):\s+(error|warning)\s+(CS\d+)\s*:\s*(.*)$")


def find_csc(explicit=None):
    """Locate csc.dll (SDK Roslyn) or a csc executable, else None."""
    if explicit:
        return explicit if os.path.isfile(explicit) else None
    roots = []
    try:
        dr = os.environ.get("DOTNET_ROOT", r"C:\Program Files\dotnet")
        sdk = os.path.join(dr, "sdk")
        if os.path.isdir(sdk):
            for v in sorted(os.listdir(sdk), reverse=True):
                cand = os.path.join(sdk, v, "Roslyn", "bincore", "csc.dll")
                if os.path.isfile(cand):
                    return cand
    except Exception:
        pass
    try:
        import shutil
        for name in ("csc", "csc.exe", "dotnet"):
            hit = shutil.which(name)
            if hit:
                return hit
    except Exception:
        pass
    return None


def iter_sources(root):
    out = []
    for dp, _, fns in os.walk(root):
        for fn in fns:
            if fn.endswith(".cs"):
                out.append(os.path.join(dp, fn))
    return sorted(out)


def classify(output):
    """(syntax, binding, top) from csc output text.

    Syntax = CS1xxx (parse/declaration level); everything else with
    a CS code counts as binding. Lines that do not parse as csc
    diagnostics are ignored. top lists (code, count) most common.
    """
    syntax = 0
    binding = 0
    counts = {}
    for ln in (output or "").splitlines():
        m = ERR_RX.match(ln.strip())
        if not m or m.group(4) != "error":
            continue
        try:
            num = int(m.group(5)[2:])
        except Exception:
            continue
        counts[m.group(5)] = counts.get(m.group(5), 0) + 1
        if 1000 <= num < 2000:
            syntax += 1
        else:
            binding += 1
    top = sorted(counts.items(), key=lambda kv: (-kv[1], kv[0]))[:10]
    return syntax, binding, top


def run_gate(tree, csc_dll=None, timeout=600, refs=None):
    """Compile every .cs under tree; return dict report. Never raises.

    `refs` is an optional list of assembly paths to reference (roadmap P5
    slice C, the game-vs-engine gate). Without it the compile has NO
    reference closure, so every external name is a binding error and the
    tier is dominated by unresolved externals. With a real UnityEngine
    (an installed Editor's `Data/Managed/UnityEngine/*.dll`) the binding
    count measures the decompiler's own defects instead.

    Measured on the game-only `Assembly-CSharp` (2026-10-28, Editor
    2022.3.61f1c1, 87 engine dlls): **syntax 75 / binding 12 both ways**.
    The reference closure does not move the number -- the 12 are not
    unresolved engine names, they are 12 `CS8641 "else" without a
    matching if` sites, i.e. decompiler defects (fix 165 family F).
    Wiring refs in is therefore about interpretability, not about
    reducing the count.
    """
    rep = {"files": 0, "syntax": 0, "binding": 0, "top": [],
           "tool_error": None, "refs": len(refs or [])}
    try:
        sources = iter_sources(tree)
    except Exception as e:
        rep["tool_error"] = "walk: %r" % (e,)
        return rep
    rep["files"] = len(sources)
    if not sources:
        rep["tool_error"] = "no .cs files"
        return rep
    csc = find_csc(csc_dll)
    if csc is None:
        rep["tool_error"] = "no compiler found"
        return rep
    rep["refs"] = len(refs or [])
    rsp = None
    out_dll = None
    try:
        fd, rsp = tempfile.mkstemp(prefix="gateresp_", suffix=".rsp")
        with os.fdopen(fd, "w", encoding="utf-8") as f:
            for r in (refs or []):
                f.write('/r:"%s"\n' % r)
            for s in sources:
                f.write('"%s"\n' % s)
        fd2, out_dll = tempfile.mkstemp(prefix="gateout_", suffix=".dll")
        os.close(fd2)
        if csc.lower().endswith("csc.dll"):
            cmd = ["dotnet", csc, "/t:library", "/nologo", "/unsafe",
                   "/langversion:latest", "/out:" + out_dll, "@" + rsp]
        else:
            cmd = [csc, "/t:library", "/nologo", "/unsafe",
                   "/langversion:latest", "/out:" + out_dll, "@" + rsp]
        # csc writes UTF-8; on a non-UTF-8 locale the default text=True
        # decoding (e.g. GBK) kills the reader thread and reports a bare
        # returncode with no diagnostics -- pin the encoding explicitly.
        pr = subprocess.run(cmd, capture_output=True, text=True,
                            encoding='utf-8', errors='replace',
                            timeout=timeout)
        text = (pr.stdout or "") + "\n" + (pr.stderr or "")
        s, b, top = classify(text)
        rep["syntax"], rep["binding"], rep["top"] = s, b, top
        rep["returncode"] = pr.returncode
    except subprocess.TimeoutExpired:
        rep["tool_error"] = "compiler timeout"
    except Exception as e:
        rep["tool_error"] = "run: %r" % (e,)
    finally:
        for p in (rsp, out_dll):
            try:
                if p and os.path.isfile(p):
                    os.remove(p)
            except Exception:
                pass
    return rep


def unity_refs(root=None):
    """Engine assemblies to reference, from an installed Unity Editor.

    `root` is the Editor's `Data/Managed/UnityEngine` directory (or an
    Editor install root, in which case that subdirectory is used). A
    Unity install's own copies of UnityEngine/UnityEditor are the TRUE
    names and signatures, so referencing them turns the binding tier
    into a measure of the decompiler rather than of unresolved
    externals. Returns [] when the path is absent -- the gate then runs
    exactly as before, and the report's `refs` count says which mode ran.
    """
    if not root:
        return []
    # an Editor install root must resolve to its MANAGED engine dir, not
    # the install dir itself (which holds native helpers like Calc.dll and
    # no managed engine assemblies at all)
    for cand in (os.path.join(root, 'Data', 'Managed', 'UnityEngine'), root):
        if os.path.isdir(cand):
            return [os.path.join(cand, f) for f in sorted(os.listdir(cand))
                    if f.lower().endswith('.dll')]
    return []


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--tree", required=True)
    ap.add_argument("--assembly", default="?")
    ap.add_argument("--csc-dll", default=None)
    ap.add_argument("--timeout", type=int, default=600)
    ap.add_argument("--unity", default=None,
                    help="Unity Editor install root or its "
                         "Data/Managed/UnityEngine dir; reference those "
                         "assemblies (game-vs-engine gate)")
    args = ap.parse_args()
    if not os.path.isdir(args.tree):
        print("no such tree: %s" % args.tree)
        return 2
    refs = unity_refs(args.unity)
    if args.unity and not refs:
        print("no engine assemblies under %s" % args.unity)
        return 2
    rep = run_gate(args.tree, args.csc_dll, args.timeout, refs)
    if rep.get("tool_error"):
        print("tool error: %s" % rep["tool_error"])
        return 2
    print("%s: %d files, syntax=%d binding=%d (refs=%d)" % (
        args.assembly, rep["files"], rep["syntax"], rep["binding"],
        rep["refs"]))
    for code, n in rep["top"]:
        print("  %s x%d" % (code, n))
    return 0 if rep["syntax"] == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
