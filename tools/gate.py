"""One entry point for every validation gate, addressed by fixture.

Replaces the ad-hoc "run five scripts by hand and copy five numbers" ritual
the historical docs describe. Every subcommand resolves its inputs through
``tools/fixtures.py``, so no gate ever hard-codes a game or tree path::

    python tools/gate.py brace  --fixture limbus --label r11
    python tools/gate.py parse  --fixture limbus --label r11
    python tools/gate.py sweep  --fixture limbus --only Assembly-CSharp
    python tools/gate.py compile --fixture limbus --label r11 --only mscorlib
    python tools/gate.py decl   --fixture limbus --label r11 --only Unity.Burst.Unsafe
    python tools/gate.py all    --fixture limbus --label r11

Reports land in ``validation_reports/<fixture>/<label>.<gate>.json`` by
default; ``--report`` overrides. Exit status is 0 only when every requested
gate passes.
"""
import argparse
import json
import os
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO / 'tools'))
sys.path.insert(0, str(REPO))

from fixtures import FixtureError, out_tree, resolve, require_tree  # noqa: E402

REPORTS = REPO / 'validation_reports'


def _report_path(args, gate, suffix='.json'):
    if args.report:
        return args.report
    label = args.label or 'latest'
    return str(REPORTS / args.fixture / ('%s.%s%s' % (label, gate, suffix)))


def _tree_for(args):
    return str(require_tree(resolve(args.fixture), args.label))


# -- individual gates ----------------------------------------------------

def gate_brace(args):
    from gates.tree_brace_audit import audit_tree, write_report
    tree = Path(args.tree) if args.tree else require_tree(
        resolve(args.fixture), args.label)
    if not tree.is_dir():
        raise FixtureError('no such tree: %s' % tree)
    files, bad = audit_tree(tree)
    payload = {'kind': 'literal-aware brace audit',
               'tree': str(tree.resolve()), 'files': files,
               'unbalanced_files': len(bad), 'details': bad}
    write_report(_report_path(args, 'brace'), payload)
    print('brace : %d files, %d unbalanced -> %s' % (
        files, len(bad), _report_path(args, 'brace')))
    return 1 if bad else 0


def gate_parse(args):
    from validate_corpus import parse_tree
    tree = args.tree or _tree_for(args)
    class _A:
        pass
    a = _A()
    a.tree = tree
    a.report = _report_path(args, 'parse')
    rc = parse_tree(a)
    print('parse : %s -> %s (rc=%d)' % (tree, a.report, rc))
    return rc


def gate_sweep(args):
    if os.environ.get('PYTHONHASHSEED') != '0':
        print('note: PYTHONHASHSEED is not 0; body hashes will not be '
              'comparable across runs')
    from validate_corpus import sweep
    fx = resolve(args.fixture)
    class _A:
        pass
    a = _A()
    a.source = str(REPO)
    a.metadata = str(fx.metadata)
    a.binary = str(fx.binary)
    a.only = args.only
    a.report = _report_path(args, 'sweep')
    rc = sweep(a)
    print('sweep : %s (rc=%d)' % (a.report, rc))
    return rc


def gate_compile(args):
    from compile_gate import run_gate
    tree = args.tree or _tree_for(args)
    only = args.only
    if only and not args.tree:
        # scope to one image directory inside the tree
        base = Path(tree)
        cand = base / only
        if cand.is_dir():
            tree = str(cand)
        else:
            hits = [p for p in base.iterdir()
                    if p.is_dir() and only.casefold() in p.name.casefold()]
            if len(hits) == 1:
                tree = str(hits[0])
            else:
                raise FixtureError(
                    'image %r not found under %s (candidates: %s)'
                    % (only, base, ', '.join(p.name for p in hits[:8])))
    rep = run_gate(tree, timeout=args.timeout)
    payload = {'kind': 'roslyn compile gate', 'tree': str(Path(tree).resolve()),
               'assembly': only or Path(tree).name, **rep}
    path = Path(_report_path(args, 'compile'))
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2) + '\n', encoding='utf-8')
    print('compile: %s -> %s (files=%s syntax=%s binding=%s)' % (
        tree, path, rep.get('files'), rep.get('syntax'), rep.get('binding')))
    if rep.get('tool_error'):
        print('  tool error:', rep['tool_error'])
        return 2
    return 0 if rep['syntax'] == 0 else 1


def gate_decl(args):
    """Declaration gate: metadata dump vs the same image in the tree."""
    import subprocess
    import tempfile
    fx = resolve(args.fixture)
    tree = Path(args.tree) if args.tree else require_tree(
        resolve(args.fixture), args.label)
    only = args.only
    if not only:
        raise FixtureError('decl gate needs --only <image name>')
    env = dict(os.environ, PYTHONPATH=str(REPO) + os.pathsep + str(REPO / 'tools'))
    with tempfile.TemporaryDirectory() as tmp:
        dump, ext = Path(tmp) / 'dump.txt', Path(tmp) / 'ext.txt'
        steps = [
            ['dump_decls.py', '--metadata', str(fx.metadata), '--binary',
             str(fx.binary), '--only', only, '--out', str(dump)],
            ['extract_decls.py', '--tree', str(tree / only), '--assembly',
             only + '.dll', '--out', str(ext)],
            ['diff_decls.py', '--dump', str(dump), '--extracted', str(ext)],
        ]
        for step in steps:
            r = subprocess.run([sys.executable, str(REPO / 'tools' / step[0])] + step[1:],
                               cwd=str(REPO), capture_output=True, text=True, encoding='utf-8', errors='replace',
                               env=env, timeout=args.timeout)
            if r.returncode != 0:
                print('  %s failed (rc=%d)' % (step[0], r.returncode))
                print((r.stdout + r.stderr)[-2000:])
                return r.returncode
    path = _report_path(args, 'decl')
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    Path(path).write_text(json.dumps(
        {'kind': 'declaration gate', 'fixture': fx.id, 'only': only,
         'passed': True}, indent=2) + '\n', encoding='utf-8')
    print('decl  : %s clean -> %s' % (only, path))
    return 0


def _normalize_argv(argv):
    """Return argv with the shared options moved ahead of the subcommand.

    argparse cannot reliably accept the same option both before and after a
    subcommand (the subparser re-applies its own defaults), so we hoist the
    shared options to the front ourselves. Both orders the docs use --
    ``brace --fixture X`` and ``--fixture X brace`` -- then work.
    """
    shared_flags = {'--fixture', '--label', '--tree', '--only',
                    '--timeout', '--report'}
    hoisted, rest = [], []
    i = 0
    while i < len(argv):
        tok = argv[i]
        key = tok.split('=', 1)[0]
        if key in shared_flags:
            hoisted.append(tok)
            if '=' not in tok and i + 1 < len(argv):
                hoisted.append(argv[i + 1])
                i += 2
                continue
        else:
            rest.append(tok)
        i += 1
    return hoisted + rest


def main(argv=None):
    argv = _normalize_argv(list(sys.argv[1:] if argv is None else argv))
    ap = argparse.ArgumentParser(
        prog='gate', description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('--fixture', help='fixture id (default: registry default)')
    ap.add_argument('--label', help='output label under out/<fixture>/')
    ap.add_argument('--tree', help='explicit tree, bypassing the fixture')
    ap.add_argument('--only', help='assembly/image filter')
    ap.add_argument('--timeout', type=int, default=900)
    ap.add_argument('--report', help='explicit report path')
    sub = ap.add_subparsers(dest='command', required=True)
    for name, fn, help_text in (
            ('brace', gate_brace, 'literal-aware brace audit'),
            ('parse', gate_parse, 'tree-sitter C# syntax gate'),
            ('sweep', gate_sweep, 'lift every native method in memory'),
            ('compile', gate_compile, 'Roslyn syntax gate over an image'),
            ('decl', gate_decl, 'metadata declarations vs the tree')):
        p = sub.add_parser(name, help=help_text, description=help_text)
        p.set_defaults(run=fn)
    args = ap.parse_args(argv)

    if args.command != 'sweep' and not args.tree and not args.fixture:
        ap.error('pass --fixture or --tree')
    try:
        return args.run(args)
    except FixtureError as ex:
        print('error:', ex)
        return 2
    except KeyboardInterrupt:
        return 130


if __name__ == '__main__':
    sys.exit(main())
