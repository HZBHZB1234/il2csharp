"""Compare two emitted trees: file sets, per-file hashes, line deltas.

Merges the three historical one-shot comparers (``compare_content.py``,
``compare_outputs.py``, ``count_diffs.py``), all of which defaulted to trees
that no longer exist. This one requires both trees explicitly -- there is no
silent default to a missing directory.

Usage::

    python tools/gates/compare_trees.py A B [--scope Assembly-CSharp]
                                      [--report FILE] [--show N]

Exit: 0 when the trees are identical (or when --allow-differs is given),
1 otherwise.
"""
import argparse
import hashlib
import json
import sys
from pathlib import Path


def tree_files(root, scope=None):
    root = Path(root)
    base = root / scope if scope else root
    out = {}
    for path in sorted(base.rglob('*.cs')):
        out[path.relative_to(base).as_posix()] = path
    return out


def digest(path):
    h = hashlib.sha256()
    with open(path, 'rb') as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b''):
            h.update(chunk)
    return h.hexdigest()


def line_count(path):
    n = 0
    with open(path, 'rb') as fh:
        for _ in fh:
            n += 1
    return n


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('a')
    ap.add_argument('b')
    ap.add_argument('--scope', help='compare only this subdirectory (e.g. Assembly-CSharp)')
    ap.add_argument('--report', help='write a JSON report here')
    ap.add_argument('--show', type=int, default=0,
                    help='print up to N differing paths')
    ap.add_argument('--allow-differs', action='store_true',
                    help='exit 0 even when the trees differ')
    args = ap.parse_args(argv)

    for label, path in (('A', args.a), ('B', args.b)):
        if not Path(path).is_dir():
            print('error: %s tree does not exist: %s' % (label, path))
            print('  (these tools have no default trees; pass both explicitly)')
            return 2

    fa, fb = tree_files(args.a, args.scope), tree_files(args.b, args.scope)
    only_a = sorted(set(fa) - set(fb))
    only_b = sorted(set(fb) - set(fa))
    common = sorted(set(fa) & set(fb))
    changed, line_deltas = [], []
    for rel in common:
        ha, hb = digest(fa[rel]), digest(fb[rel])
        if ha != hb:
            la, lb = line_count(fa[rel]), line_count(fb[rel])
            changed.append(rel)
            line_deltas.append({'path': rel, 'a_lines': la, 'b_lines': lb,
                                'delta': lb - la})
    total_delta = sum(d['delta'] for d in line_deltas)
    payload = {
        'kind': 'tree comparison',
        'a': str(Path(args.a).resolve()),
        'b': str(Path(args.b).resolve()),
        'scope': args.scope,
        'files_a': len(fa), 'files_b': len(fb),
        'only_a': len(only_a), 'only_b': len(only_b),
        'identical': len(common),
        'changed': len(changed),
        'net_line_delta': total_delta,
        'line_deltas': line_deltas,
        'only_a_paths': only_a, 'only_b_paths': only_b,
    }
    if args.report:
        path = Path(args.report)
        if path.parent:
            path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(payload, indent=2) + '\n', encoding='utf-8')
    print('%s vs %s%s' % (args.a, args.b, ' [%s]' % args.scope if args.scope else ''))
    print('  files      : %d / %d' % (len(fa), len(fb)))
    print('  identical  : %d' % (len(common) - len(changed)))
    print('  changed    : %d  (net %+d lines)' % (len(changed), total_delta))
    print('  only in A  : %d' % len(only_a))
    print('  only in B  : %d' % len(only_b))
    for rel in changed[:args.show]:
        d = next(x for x in line_deltas if x['path'] == rel)
        print('    %s  %+d lines' % (rel, d['delta']))
    for rel in only_a[:args.show]:
        print('    -A %s' % rel)
    for rel in only_b[:args.show]:
        print('    +B %s' % rel)
    if args.report:
        print('  report     : %s' % args.report)
    differ = bool(changed or only_a or only_b)
    if differ and not args.allow_differs:
        return 1
    return 0


if __name__ == '__main__':
    sys.exit(main())
