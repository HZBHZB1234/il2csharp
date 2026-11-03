"""Run every tree-level gate for one fixture label, in one command.

    python tools/gate_all.py <fixture> <label> [--no-compile] [--no-compare]

Order matters: brace, then the per-image tree-sitter gate (the single-process
form can die with an access violation), then the whole-tree Roslyn compile
against the fixture's exact managed closure, then the source comparison when the
fixture ships sources. Prints a one-screen summary and writes one report per
grep in validation_reports/<fixture>/.
"""
import argparse
import json
import os
import subprocess
import sys

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TOOLS = os.path.join(REPO, 'tools')
EXCLUDE_DIRS = ('mscorlib', 'System', 'System.Core', 'System.Xml',
                'System.Data', 'System.Runtime.Serialization')


def _run(cmd, **kw):
    return subprocess.run([sys.executable] + cmd, cwd=REPO,
                          capture_output=True, text=True, **kw)


def main(argv):
    ap = argparse.ArgumentParser()
    ap.add_argument('fixture')
    ap.add_argument('label')
    ap.add_argument('--no-compile', action='store_true')
    ap.add_argument('--no-compare', action='store_true')
    args = ap.parse_args(argv)

    tree = os.path.join(REPO, 'out', args.fixture, args.label)
    if not os.path.isdir(tree):
        raise SystemExit('no tree at %s' % tree)
    reports = os.path.join(REPO, 'validation_reports', args.fixture)
    os.makedirs(reports, exist_ok=True)
    env = dict(os.environ, PYTHONHASHSEED='0',
               PYTHONPATH=os.pathsep.join([REPO, TOOLS]))
    summary = {'fixture': args.fixture, 'label': args.label, 'tree': tree}

    # 1. brace
    rep = os.path.join(reports, args.label + '.brace.json')
    p = _run([os.path.join(TOOLS, 'gate.py'), '--fixture', args.fixture,
              '--label', args.label, '--report', rep, 'brace'], env=env)
    print(p.stdout.strip() or p.stderr.strip()[-400:])
    try:
        with open(rep, encoding='utf-8') as fh:
            d = json.load(fh)
        summary['brace'] = {k: d.get(k) for k in ('files', 'unbalanced')}
    except Exception:
        summary['brace'] = None

    # 2. tree-sitter, per image (the single-process gate can crash)
    rep = os.path.join(reports, args.label + '.parse.json')
    p = _run([os.path.join(TOOLS, 'parse_per_image.py'), tree, rep], env=env)
    print(p.stdout.strip().splitlines()[-2:] if p.stdout.strip() else p.stderr)
    try:
        with open(rep, encoding='utf-8') as fh:
            d = json.load(fh)
        summary['parse'] = {k: d.get(k) for k in
                            ('files', 'bad_files', 'errors', 'missing',
                             'recovery_nodes')}
        summary['parse_crashed'] = [c['image'] for c in
                                    (d.get('crashed_images') or [])]
    except Exception:
        summary['parse'] = None

    # 3. whole-tree Roslyn compile against the fixture's exact closure
    if not args.no_compile:
        rep = os.path.join(reports, args.label + '.whole.compile.json')
        cmd = [os.path.join(TOOLS, 'compile_corpus.py'), tree, '--report', rep,
               '--managed-refs', os.path.join(REPO, 'fixtures', args.fixture,
                                              'build')]
        for d in EXCLUDE_DIRS:
            cmd += ['--exclude-dirs', d]
        p = _run(cmd, env=env, timeout=7200)
        print((p.stdout or p.stderr)[-1200:])
        try:
            with open(rep, encoding='utf-8') as fh:
                d = json.load(fh)
            summary['compile'] = {k: d.get(k) for k in
                                  ('source_files', 'files_with_errors',
                                   'errors', 'errors_by_code',
                                   'binding_masked')}
        except Exception:
            summary['compile'] = None

    # 4. source comparison
    if not args.no_compare:
        p = _run([os.path.join(TOOLS, 'source_compare.py'), '--fixture',
                  args.fixture, '--label', args.label], env=env, timeout=7200)
        print((p.stdout or p.stderr)[-600:])
        qr = os.path.join(tree, 'quality_report.json')
        try:
            with open(qr, encoding='utf-8') as fh:
                d = json.load(fh)
            summary['fidelity'] = d.get('averages')
            summary['unmatched'] = d.get('unmatched')
        except Exception:
            summary['fidelity'] = None

    print()
    print(json.dumps(summary, indent=1, ensure_ascii=False))
    out = os.path.join(reports, args.label + '.gate_all.json')
    with open(out, 'w', encoding='utf-8') as fh:
        json.dump(summary, fh, indent=1)
    print('summary ->', out)
    return 0


if __name__ == '__main__':
    raise SystemExit(main(sys.argv[1:]))
