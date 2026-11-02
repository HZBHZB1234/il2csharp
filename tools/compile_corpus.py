"""Compile a recovered tree as one diagnostic unit; never execute its output.

This deliberately bypasses per-assembly reference wiring. Duplicate generated
shared stubs are merged in a temporary file; recovered source is never edited.
A clean result would prove compilation only, not recovered behavior.

Reference closure
-----------------
By default the compile references the local .NET SDK's own runtime pack,
which is right for a tree that re-emits BCL images (`mscorlib`, `System`, ...)
and wrong for one that does not. Two modes wire the *real* closure instead:

  --managed-refs BUILD_DIR   the exact assemblies a Unity IL2CPP player build
                             was compiled from (its
                             `<Player>_BackUpThisFolder_ButDontShipItWithYourGame/
                             Managed/` folder). Every image directory present in
                             the tree is then excluded automatically, because
                             the tree emits those itself and referencing the
                             original would resolve the very names recovery
                             missed.
  --unity EDITOR_ROOT        an installed Unity Editor's engine modules plus its
                             netstandard shims (the game-vs-engine closure for a
                             tree that only emits the game's own images).

Both may be repeated/combined; `--no-dotnet-refs` drops the SDK pack when the
supplied closure already carries `System.Object`.
"""
import argparse
from collections import Counter
import gzip
import hashlib
import json
from pathlib import Path
import re
import shutil
import subprocess
import sys
import tempfile


def version_key(path):
    return tuple(int(n) for n in re.findall(r"\d+", str(path)))


def _closure_refs(tree_root, refs_dirs, unity_roots, managed_dirs,
                  exclude=(), exclude_images=True):
    """Assemblies to reference for a whole-tree compile, plus a note list."""
    import compile_gate as cg

    tree_images = set()
    if exclude_images:
        try:
            tree_images = {p.name.casefold() for p in Path(tree_root).iterdir()
                           if p.is_dir()}
        except OSError:
            tree_images = set()
    skip = {e.casefold() for e in exclude if e}
    if exclude_images:
        skip |= {name + '.dll' for name in tree_images}

    refs, notes = [], []
    for d in refs_dirs:
        got = [str(p) for p in sorted(Path(d).glob('*.dll'))
               if p.name.casefold() not in skip]
        refs.extend(got)
        notes.append('refs-dir %s: %d' % (d, len(got)))
    for root in unity_roots:
        engine = cg.unity_refs(root)
        fw = cg.unity_framework_refs(root)
        if not engine:
            raise SystemExit('no engine assemblies under %s' % root)
        got = [p for p in engine + fw if Path(p).name.casefold() not in skip]
        refs.extend(got)
        notes.append('unity %s: %d engine + %d bcl' % (root, len(engine), len(fw)))
    for d in managed_dirs:
        got = cg.managed_refs(d, sorted(skip))
        if not got:
            raise SystemExit('no Managed backup folder under %s' % d)
        refs.extend(got)
        notes.append('managed-refs %s: %d (excluded %d tree images)'
                     % (d, len(got), len(tree_images)))
    return refs, notes


def _stub_members(text):
    """Member blocks of a generated `__SharedBodyStubs` class, deduped by VA.

    Each stub is a real method with a body
    (`internal static object sub_<va>(params object[] args) { throw ... }`),
    so merging them means merging whole members, not signature lines: a
    signature-only merge produced 91 CS1002 in one temporary file. Blocks
    are returned in file order with their `0x<va>:` comments dropped, and two
    images that reference the same address contribute it once.
    """
    seen = {}
    out = []
    lines = text.splitlines()
    i = 0
    while i < len(lines):
        m = re.match(r'\s+internal static object (sub_[0-9a-fA-F]+)'
                     r'\(params object\[\] args\)\s*$', lines[i])
        if not m:
            i += 1
            continue
        va = m.group(1)
        block = [lines[i]]
        depth = 0
        opened = False
        i += 1
        while i < len(lines):
            line = lines[i]
            block.append(line)
            depth += line.count('{') - line.count('}')
            if '{' in line:
                opened = True
            if opened and depth <= 0:
                i += 1
                break
            i += 1
        if va in seen:
            continue
        seen[va] = True
        out.append((va, block))
    return out


def compile_tree(tree, report, refs_dirs=(), unity_roots=(), managed_dirs=(),
                 exclude=(), exclude_images=True, dotnet_refs=True,
                 timeout=1800, exclude_dirs=()):
    dotnet = shutil.which("dotnet")
    if not dotnet:
        raise RuntimeError("A .NET SDK is required")
    root = Path(dotnet).resolve().parent
    compilers = sorted((root / "sdk").glob("*/Roslyn/bincore/csc.dll"), key=version_key)
    packs = sorted((root / "packs/Microsoft.NETCore.App.Ref").glob("*/ref/net*"),
                   key=version_key)
    if not compilers:
        raise RuntimeError("Roslyn is required")
    if dotnet_refs and not packs:
        raise RuntimeError(".NET reference assemblies are required")
    closure, notes = _closure_refs(tree, refs_dirs, unity_roots, managed_dirs,
                                   exclude, exclude_images)
    files = []
    root_dir = Path(tree).resolve()
    skip_dirs = tuple(d for d in exclude_dirs if d)
    for p in sorted(root_dir.rglob("*.cs")):
        rel = p.relative_to(root_dir).as_posix()
        if skip_dirs and rel.split("/", 1)[0] in skip_dirs:
            continue
        files.append(p)
    if not files:
        raise ValueError("No C# source files found")
    sources, stub_members = [], []
    stub_order = {}
    inventory = hashlib.sha256()
    # Compiler scaffolding is emitted per ASSEMBLY, so a whole-tree compile as
    # ONE unit sees the same helper type declared by every image (CS0102 /
    # CS0111 -- 484 of the game tree's 857 errors). Those declarations are
    # byte-identical compiler artifacts, not game code: keep the first and
    # skip the rest.
    _SCAFFOLDING = {
        "PrivateImplementationDetails.cs", "EmbeddedAttribute.cs",
        "NullableAttribute.cs", "NullableContextAttribute.cs",
        "RefSafetyRulesAttribute.cs",
        "UnitySourceGeneratedAssemblyMonoScriptTypes_v1.cs",
    }
    seen_scaffolding = set()
    for path in files:
        inventory.update(path.relative_to(Path(tree).resolve()).as_posix().encode())
        inventory.update(hashlib.sha256(path.read_bytes()).digest())
        if path.name in _SCAFFOLDING:
            if path.name in seen_scaffolding:
                continue
            seen_scaffolding.add(path.name)
        if path.name == "__SharedBodyStubs.cs":
            text = path.read_text(encoding="utf-8-sig")
            for va, block in _stub_members(text):
                if va in stub_order:
                    continue
                stub_order[va] = True
                stub_members.extend(block)
        else:
            sources.append(path)
    # The scratch dir holds the merged stub file the compiler must open by
    # path. Create it beside the report, not in %TEMP%: a temp cleaner removed
    # the directory between the write and the compiler invocation, and csc then
    # reported `CS2001: source file not found __SharedBodyStubs.cs` -- which
    # reads like a decompiler failure and is not one.
    scratch_parent = Path(report).resolve().parent if report else Path.cwd()
    scratch_parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix="il2csharp_compile_",
                                     dir=str(scratch_parent)) as temporary:
        temp = Path(temporary)
        merged = temp / "__SharedBodyStubs.cs"
        merged.write_text("internal static class __SharedBodyStubs {\n" +
                          "\n".join(stub_members) + "\n}")
        response = temp / "compile.rsp"
        options = ["/nologo", "/target:library", "/unsafe+", "/langversion:latest",
                   "/utf8output",
                   '/out:"' + str(temp / "Recovered.dll") + '"']
        if dotnet_refs:
            options.extend('/reference:"%s"' % p for p in packs[-1].glob("*.dll"))
        options.extend('/reference:"%s"' % p for p in closure)
        options.extend('"' + str(p) + '"' for p in sources + [merged])
        response.write_text("\n".join(options), encoding="utf-8")
        result = subprocess.run([dotnet, str(compilers[-1]), "@" + str(response)],
                                capture_output=True, timeout=timeout)
    log = (result.stdout or b"").decode("utf-8", "replace") + \
        (result.stderr or b"").decode("utf-8", "replace")
    report = Path(report)
    report.parent.mkdir(parents=True, exist_ok=True)
    log_path = report.with_suffix(".log.gz")
    with gzip.open(log_path, "wt", encoding="utf-8") as stream:
        stream.write(log)
    error_files = set(re.findall(r"^(.+?)\(\d+,\d+\): error CS\d+:", log, re.MULTILINE))
    errors = Counter(re.findall(r"\berror (CS\d+):", log))
    first = {}
    for m in re.finditer(r"^(.+?)\((\d+),\d+\): error (CS\d+): (.*)$", log, re.MULTILINE):
        first.setdefault(m.group(3), {
            "file": m.group(1), "line": int(m.group(2)),
            "message": m.group(4)[:200]})
    summary = dict(tree=str(Path(tree).resolve()), source_files=len(sources),
                   merged_stubs=len(stub_order), compiler=str(compilers[-1]),
                   inventory_sha256=inventory.hexdigest(), log=str(log_path),
                   references=str(packs[-1]) if dotnet_refs else None,
                   reference_closure=notes, closure_refs=len(closure),
                   exit_code=result.returncode,
                   files_with_errors=len(error_files),
                   errors=sum(errors.values()), errors_by_code=dict(errors.most_common()),
                   first_error_by_code=first,
                   scope="Single diagnostic assembly; original project wiring is not tested")
    report.write_text(json.dumps(summary, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({k: summary[k] for k in
                      ("source_files", "closure_refs", "files_with_errors",
                       "errors", "errors_by_code")}, indent=2))
    return result.returncode


if __name__ == "__main__":
    sys.path.insert(0, str(Path(__file__).resolve().parent))
    parser = argparse.ArgumentParser(description=__doc__,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("tree")
    parser.add_argument("--report", required=True)
    parser.add_argument("--refs-dir", action="append", default=[],
                        help="reference every .dll in this directory (repeatable)")
    parser.add_argument("--unity", action="append", default=[],
                        help="Unity Editor install root: engine modules + shims")
    parser.add_argument("--managed-refs", action="append", default=[],
                        help="Unity player build dir: its Managed backup folder")
    parser.add_argument("--exclude", action="append", default=[],
                        help="dll names to skip (repeatable)")
    parser.add_argument("--exclude-dirs", action="append", default=[],
                        help="image directories whose sources are left out of "
                             "the diagnostic assembly (repeatable; e.g. "
                             "mscorlib / System / UnityEngine.CoreModule when "
                             "those types come from the reference closure)")
    parser.add_argument("--keep-emitted-refs", action="store_true",
                        help="do not auto-exclude the tree's own image dlls")
    parser.add_argument("--dotnet-refs", dest="dotnet_refs",
                        action="store_true", default=None,
                        help="force the SDK runtime pack into the reference set")
    parser.add_argument("--no-dotnet-refs", dest="dotnet_refs",
                        action="store_false",
                        help="drop the SDK runtime pack (implied whenever a "
                             "reference closure is supplied: Unity's Managed "
                             "set brings its own mscorlib, and mixing the two "
                             "leaves System.Object ambiguous -> 40k CS0518)")
    parser.add_argument("--timeout", type=int, default=1800)
    args = parser.parse_args()
    provided_closure = bool(args.refs_dir or args.unity or args.managed_refs)
    use_dotnet = (args.dotnet_refs if args.dotnet_refs is not None
                  else not provided_closure)
    raise SystemExit(compile_tree(
        args.tree, args.report, args.refs_dir, args.unity, args.managed_refs,
        args.exclude, not args.keep_emitted_refs, use_dotnet, args.timeout,
        args.exclude_dirs))
