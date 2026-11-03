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

GLOBAL_ERR_RX = re.compile(
    r"^(?:(?:csc|CSC)(?:\.exe)?\s*:\s*)?(error|warning)\s+(CS\d+)\s*:\s*(.*)$")


def diagnostics(output):
    """Yield located and compiler-wide diagnostics in one stable shape."""
    for line in (output or '').splitlines():
        m = ERR_RX.match(line.strip())
        if m:
            yield m.group(4), m.group(5), m.group(1), int(m.group(2)), m.group(6)
            continue
        m = GLOBAL_ERR_RX.match(line.strip())
        if m:
            yield m.group(1), m.group(2), '<compiler>', 0, m.group(3)


def first_samples(output, limit=3):
    """One sample diagnostics line per code, for triage.

    A bare count says where the errors are not; the line text and the
    `file(line,col)` prefix say exactly which recovered statement uses a
    name the compiler cannot resolve. Kept small (three per code) so the
    report stays readable and the JSON stays diffable.
    """
    seen = {}
    for severity, code, file, line, message in diagnostics(output):
        if severity != 'error':
            continue
        bucket = seen.setdefault(code, [])
        if len(bucket) < limit:
            bucket.append({"file": file, "line": line, "message": message[:240]})
    return seen


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


def managed_refs(build_dir, exclude=()):
    """Reference assemblies from a Unity build's backup folder.

    An IL2CPP player build keeps the exact managed assemblies it was
    compiled from under
    `<build>/<Player>_BackUpThisFolder_ButDontShipItWithYourGame/Managed/`
    (Unity 2021.2+). Those files are the *true* reference closure for the
    build -- engine modules, BCL, and every package -- so compiling an
    emitted image against them measures the decompiler, not unresolved
    externals: `references=260`-style gaps (the game-vs-engine gate on a
    shipped game, whose `Managed/` folder IL2CPP builds delete) cannot
    appear.

    `exclude` drops the images the tree under test emits itself (pass the
    image's own `<Name>.dll`), because referencing the original would let
    the compiler resolve the very names that recovery failed to emit.

    Returns [] when the folder is absent -- the gate then runs exactly as
    before, and the report's `refs` count says which mode ran.
    """
    import glob as _glob
    hits = sorted(_glob.glob(os.path.join(
        build_dir, '*BackUpThisFolder_ButDontShipItWithYourGame', 'Managed')))
    if not hits:
        return []
    skip = {e.casefold() for e in exclude if e}
    out = []
    for name in sorted(os.listdir(hits[0])):
        if not name.lower().endswith('.dll'):
            continue
        if name.casefold() in skip:
            continue
        out.append(os.path.join(hits[0], name))
    return out


def _decode(raw):
    """Decode compiler output bytes as UTF-8, else the console code page.

    Roslyn honours `/utf8output` when asked, but a localized Windows
    install still writes diagnostic TEXT in the console code page, and a
    mis-decode is invisible in the counts (they key on `CSxxxx`) while
    making every sample line unreadable. Try strict UTF-8 first, then the
    ANSI code page, then a lossy UTF-8 pass.
    """
    if not raw:
        return ""
    if isinstance(raw, str):
        return raw
    try:
        return raw.decode("utf-8")
    except UnicodeDecodeError:
        pass
    enc = "mbcs" if os.name == "nt" else (sys.getdefaultencoding() or "utf-8")
    try:
        return raw.decode(enc, errors="replace")
    except Exception:
        return raw.decode("utf-8", errors="replace")


def classify(output):
    """(syntax, binding, top) from csc output text.

    Syntax = CS1xxx (parse/declaration level); everything else with a CS
    code counts as binding. Lines that do not parse as csc diagnostics are
    ignored. top lists (code, count) most common.

    The CS1xxx band is a HEURISTIC, not a truth: a handful of codes in it
    are genuine BINDING errors, and counting them as syntax makes a clean
    parse look broken. `CS1750` (a default parameter value that does not
    convert) and `CS1061`/`CS1501`/`CS1503`/`CS1620` (no such member /
    wrong arg count / wrong arg type) all live in that band and all
    describe a resolved-but-mismatched program, never a parse failure. The
    authoritative parse number is the tree-sitter gate; this tier must not
    contradict it. Measured 2026-10-30 on the fix-169 tree: 215 "syntax"
    errors in one image were ALL CS1061/CS1503/CS1501/CS1620, while
    tree-sitter reported 0/0/0/0 on the same tree.
    """
    BINDING_BAND = frozenset((
        "CS1061", "CS1501", "CS1503", "CS1620", "CS1750",
    ))
    syntax = 0
    binding = 0
    counts = {}
    for severity, code, _, _, _ in diagnostics(output):
        if severity != 'error':
            continue
        num = int(code[2:])
        counts[code] = counts.get(code, 0) + 1
        if 1000 <= num < 2000 and code not in BINDING_BAND:
            syntax += 1
        else:
            binding += 1
    top = sorted(counts.items(), key=lambda kv: (-kv[1], kv[0]))[:10]
    return syntax, binding, top


def run_gate(tree, csc_dll=None, timeout=600, refs=None, body_probe=False):
    """Compile every .cs under tree; return dict report. Never raises.

    `body_probe` injects an isolated missing-name method in a temporary file.
    Seeing its CS0103 proves that Roslyn reached method-body binding in this
    compilation, NOT that it bound every emitted method. An absent diagnostic
    warns that declaration errors (or an incomplete run) may mask body errors.
    The synthetic diagnostic is excluded from counts/samples; sources stay
    untouched and the probe is removed even on compiler failure.

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
    probe_path = None
    probe_name = None
    if body_probe:
        rep['body_probe_observed'] = None
    try:
        if body_probe:
            import uuid
            probe_name = '__il2csharp_missing_' + uuid.uuid4().hex
            fd, probe_path = tempfile.mkstemp(prefix='gateprobe_', suffix='.cs')
            source = ('internal static class Probe_%s { '
                      'static int Check() { return %s; } }' % (probe_name, probe_name))
            with os.fdopen(fd, 'wb') as probe:
                probe.write(source.encode('utf-8'))
            sources = sources + [probe_path]
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
                   "/langversion:latest", "/utf8output",
                   "/out:" + out_dll, "@" + rsp]
        else:
            cmd = [csc, "/t:library", "/nologo", "/unsafe",
                   "/langversion:latest", "/utf8output",
                   "/out:" + out_dll, "@" + rsp]
        # csc writes UTF-8; on a non-UTF-8 locale the default text=True
        # decoding (e.g. GBK) kills the reader thread and reports a bare
        # returncode with no diagnostics -- pin the encoding explicitly.
        # `/utf8output` alone does not localize: a non-English Windows
        # still emits diagnostic TEXT in the console code page, so also
        # force the compiler's message language (VSLANG 1033 = en-US).
        # The counts key on `CSxxxx`, which is locale-independent either
        # way; this only makes the report's sample lines readable.
        env = dict(os.environ, VSLANG="1033", DOTNET_CLI_UI_LANGUAGE="en")
        pr = subprocess.run(cmd, capture_output=True, timeout=timeout, env=env)
        text = _decode(pr.stdout) + "\n" + _decode(pr.stderr)
        if body_probe:
            # Match BOTH the private probe path and its unique identifier;
            # never hide a real program diagnostic with the same CS code.
            kept = []
            observed = False
            for line in text.splitlines():
                m = ERR_RX.match(line.strip())
                if m and m.group(4) == 'error' and m.group(5) == 'CS0103' \
                        and os.path.normcase(os.path.abspath(m.group(1))) == \
                        os.path.normcase(os.path.abspath(probe_path)) \
                        and probe_name in m.group(6):
                    observed = True
                else:
                    kept.append(line)
            rep['body_probe_observed'] = observed
            text = '\n'.join(kept)
        s, b, top = classify(text)
        rep["syntax"], rep["binding"], rep["top"] = s, b, top
        rep["samples"] = first_samples(text)
        rep["returncode"] = pr.returncode
    except subprocess.TimeoutExpired:
        rep["tool_error"] = "compiler timeout"
    except Exception as e:
        rep["tool_error"] = "run: %r" % (e,)
    finally:
        for p in (rsp, out_dll, probe_path):
            try:
                if p and os.path.isfile(p):
                    os.remove(p)
            except Exception:
                pass
    return rep


def unity_refs(root=None):
    """Engine assemblies to reference, from an installed Unity Editor.

    `root` may be:
      * an Editor install root            (`<root>/Editor/Data/Managed/UnityEngine`)
      * an install root's `Editor` dir    (`<root>/Data/Managed/UnityEngine`)
      * that `UnityEngine` dir directly

    A Unity install's own copies of UnityEngine/UnityEditor are the TRUE
    names and signatures, so referencing them turns the binding tier into
    a measure of the decompiler rather than of unresolved externals.
    Returns [] when the path is absent -- the gate then runs exactly as
    before, and the report's `refs` count says which mode ran.

    Measured on this box: `D:\\unity_editor_6000` (Unity 6000, the same
    generation as the fixture's `6000.3.12f1`) has 139 managed engine
    assemblies under `Editor/Data/Managed/UnityEngine`.
    """
    if not root:
        return []
    cands = (
        os.path.join(root, 'Editor', 'Data', 'Managed', 'UnityEngine'),
        os.path.join(root, 'Data', 'Managed', 'UnityEngine'),
        root,
    )
    for cand in cands:
        if os.path.isdir(cand):
            refs = [os.path.join(cand, f) for f in sorted(os.listdir(cand))
                    if f.lower().endswith('.dll')]
            if refs:
                return refs
    return []


def unity_framework_refs(root=None):
    """BCL reference assemblies from the same Unity Editor.

    The game code uses `System.*`, `mscorlib` and `netstandard` types that
    the engine modules do not define, so a gate that references ONLY
    UnityEngine still reports every BCL name as a binding error. These are
    the Editor's own shim sets:
      `Data/NetStandard/ref/2.1.0/netstandard.dll`
      `Data/NetStandard/compat/2.1.0/shims/netfx/*.dll`      (mscorlib, ...)
      `Data/NetStandard/compat/2.1.0/shims/netstandard/*.dll`
    Returns [] when the root is not an Editor install.
    """
    if not root:
        return []
    editors = [os.path.join(root, 'Editor'), root]
    editor = next((e for e in editors
                   if os.path.isdir(os.path.join(e, 'Data', 'NetStandard'))), None)
    if editor is None:
        return []
    ns = os.path.join(editor, 'Data', 'NetStandard')
    out = []
    for sub in (os.path.join(ns, 'ref', '2.1.0'),
                os.path.join(ns, 'compat', '2.1.0', 'shims', 'netfx'),
                os.path.join(ns, 'compat', '2.1.0', 'shims', 'netstandard')):
        if os.path.isdir(sub):
            out.extend(os.path.join(sub, f) for f in sorted(os.listdir(sub))
                       if f.lower().endswith('.dll'))
    return out


def merge_refs(*groups, exclude=()):
    """One DLL per case-insensitive basename; later groups override earlier.

    For a game-vs-Editor gate pass player packages, then Editor engine/BCL,
    then any explicit overrides. This prevents two netstandard/mscorlib or
    UnityEngine identities from silently entering the same invocation.
    It is filename precedence, NOT proof of binary/API compatibility.
    Exclusions apply after merging, including to Editor/explicit references.
    """
    def name(path):
        return os.fspath(path).replace('\\', '/').rsplit('/', 1)[-1].casefold()
    skipped = {name(p) for p in exclude}
    refs = {}
    for group in groups:
        for path in group:
            key = name(path)
            if key not in skipped:
                refs[key] = os.fspath(path)
    return [refs[key] for key in sorted(refs)]


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--tree", required=True)
    ap.add_argument("--assembly", default="?")
    ap.add_argument("--csc-dll", default=None)
    ap.add_argument("--timeout", type=int, default=600)
    ap.add_argument("--body-probe", action="store_true",
                    help="check that Roslyn reaches method-body binding; "
                         "exclude the synthetic error from counts")
    ap.add_argument("--unity", default=None,
                    help="Unity Editor install root or its "
                         "Data/Managed/UnityEngine dir; reference those "
                         "assemblies (game-vs-engine gate)")
    ap.add_argument("--no-framework", action="store_true",
                    help="with --unity, reference ONLY the engine modules "
                         "(skip the Editor's mscorlib/netstandard shims)")
    ap.add_argument("--refs-dir", action="append", metavar="DIR",
                    help="reference every .dll in DIR (repeatable)")
    ap.add_argument("--managed-refs", default=None, metavar="BUILD_DIR",
                    help="reference the exact closure of a Unity player "
                         "build: BUILD_DIR/*BackUpThisFolder*/Managed/*.dll")
    ap.add_argument("--exclude", action="append", metavar="DLL",
                    help="with --managed-refs, skip this dll name "
                         "(the image the tree emits itself)")
    args = ap.parse_args()
    if not os.path.isdir(args.tree):
        print("no such tree: %s" % args.tree)
        return 2
    refs = unity_refs(args.unity)
    if args.unity and not refs:
        print("no engine assemblies under %s" % args.unity)
        return 2
    fw = [] if args.no_framework else unity_framework_refs(args.unity)
    extra = []
    for d in (args.refs_dir or []):
        if not os.path.isdir(d):
            print("no such refs dir: %s" % d)
            return 2
        extra.extend(os.path.join(d, f) for f in sorted(os.listdir(d))
                    if f.lower().endswith('.dll'))
    got = []
    if args.managed_refs:
        got = managed_refs(args.managed_refs)
        if not got:
            print("no Managed backup folder under %s" % args.managed_refs)
            return 2
    refs = merge_refs(got, refs, fw, extra, exclude=args.exclude or ())
    rep = run_gate(args.tree, args.csc_dll, args.timeout, refs,
                   body_probe=args.body_probe)
    if rep.get("tool_error"):
        print("tool error: %s" % rep["tool_error"])
        return 2
    print("%s: %d files, syntax=%d binding=%d (refs=%d, merged)" % (
        args.assembly, rep["files"], rep["syntax"], rep["binding"], len(refs)))
    if args.body_probe:
        print("  method-body probe: " + (
            "observed (not proof of full coverage)" if rep['body_probe_observed']
            else "NOT observed; declaration errors may mask body diagnostics"))
    for code, n in rep["top"]:
        print("  %s x%d" % (code, n))
    for code, rows in sorted((rep.get("samples") or {}).items()):
        for row in rows[:1]:
            print("  %s: %s(%d): %s" % (code, row["file"].split('\\')[-1],
                                        row["line"], row["message"][:160]))
    return 0 if rep["syntax"] == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
