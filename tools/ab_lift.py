"""Fast A/B body-diff: lift N methods from the CURRENT source and diff them
against a reference snapshot taken from another revision.

This is the per-slice validation path that replaces a 60-100 minute full
rebuild (user call 2026-10-29: the full build is a milestone tool, not a
per-slice one). It is the same instrument the fix-168 slice used to prove
+14/-14 symmetry in ~40 s.

Usage:
    # 1. snapshot from the reference revision (do this once, before editing)
    git stash && python tools/ab_lift.py snap --out /tmp/ref.json
    git stash pop
    # 2. after the edit, diff against it
    python tools/ab_lift.py diff --ref /tmp/ref.json

`--sample N` picks N methods spread across the image; `--mi` overrides with
explicit MethodDef rows. `--image` selects the image (default
Assembly-CSharp.dll).

The diff reports opcode-level counts (equal / replace / delete / insert) and
the changed lines. A `--strict` run exits nonzero when any changed method
differs in LINE COUNT (an insert/delete with no counterpart), which is the
shape a real structural regression takes -- a pure spelling/name change
always shows as a balanced replace.
"""
import argparse
import json
import os
import sys

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, REPO)
sys.path.insert(0, os.path.join(REPO, 'tools'))

from corpus_common import load  # noqa: E402
from fixtures import resolve  # noqa: E402


def _lift(il, dec, mi):
    from il2cpp import Decompiler  # noqa: F401  (documents the type)
    m = il.meta.methods[mi]
    td = il.meta.typedefs[m.declaring]
    try:
        return '\n'.join(dec.lift_method(m, td))
    except Exception as e:
        return 'ERR %r' % (e,)


def collect(args):
    from il2cpp import Decompiler, Lifter
    fx = resolve(args.fixture)
    il = load(REPO, fx.metadata, fx.binary)
    il.assign_images()
    dec = Decompiler(Lifter(il))
    if args.mi:
        picks = args.mi
    else:
        img = next((i for i in il.meta.images if i.name == args.image), None)
        if img is None:
            raise SystemExit('no image %r' % (args.image,))
        picks = []
        step = max(1, img.type_count // max(1, args.sample))
        for k in range(0, img.type_count, step):
            td = il.meta.typedefs[img.type_start + k]
            for mi in range(td.method_start, td.method_start + td.method_count):
                if il.meta.methods[mi].addr:
                    picks.append(mi)
                    break
            if len(picks) >= args.sample:
                break
    return {str(mi): _lift(il, dec, mi) for mi in picks}


def cmd_snap(args):
    res = collect(args)
    with open(args.out, 'w', encoding='utf-8') as f:
        json.dump(res, f, indent=0)
    print('snapshot: %d methods -> %s' % (len(res), args.out))
    return 0


def cmd_diff(args):
    import collections
    import difflib
    with open(args.ref, encoding='utf-8') as f:
        ref = json.load(f)
    cur = collect(args)
    common = sorted(set(ref) & set(cur), key=int)
    missing = sorted(set(ref) - set(cur), key=int)
    tags = collections.Counter()
    changed = []
    plus = minus = 0
    unbalanced = []
    for mi in common:
        if ref[mi] == cur[mi]:
            continue
        la = ref[mi].splitlines()
        lb = cur[mi].splitlines()
        dl = []
        for tag, i1, i2, j1, j2 in difflib.SequenceMatcher(
                None, la, lb, autojunk=False).get_opcodes():
            tags[tag] += 1
            if tag == 'replace':
                plus += j2 - j1
                minus += i2 - i1
                dl.extend(['-' + l for l in la[i1:i2]])
                dl.extend(['+' + l for l in lb[j1:j2]])
            elif tag == 'delete':
                minus += i2 - i1
                dl.extend(['-' + l for l in la[i1:i2]])
            elif tag == 'insert':
                plus += j2 - j1
                dl.extend(['+' + l for l in lb[j1:j2]])
        if len(la) != len(lb):
            unbalanced.append((mi, len(la), len(lb)))
        changed.append((mi, dl))
    print('compared=%d changed=%d missing=%d  +%d/-%d lines'
          % (len(common), len(changed), len(missing), plus, minus))
    print('opcodes: %s' % dict(tags))
    if missing:
        print('MISSING (in ref, not now): %s' % missing[:10])
    if unbalanced:
        print('LINE-COUNT CHANGES: %d methods (inspect each)'
              % len(unbalanced))
        for mi, a, b in unbalanced[:10]:
            print('  mi %s: %d -> %d lines' % (mi, a, b))
    shown = 0
    for mi, dl in changed:
        if shown >= args.show:
            break
        print('\n=== mi %s' % mi)
        for l in dl[:12]:
            print('   ' + l[:170])
        shown += 1
    if args.strict and unbalanced:
        return 1
    return 0


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('--fixture', default='limbus')
    ap.add_argument('--image', default='Assembly-CSharp.dll')
    ap.add_argument('--sample', type=int, default=60)
    ap.add_argument('--mi', type=int, nargs='*')
    ap.add_argument('--show', type=int, default=6)
    ap.add_argument('--strict', action='store_true')
    sub = ap.add_subparsers(dest='cmd', required=True)
    s = sub.add_parser('snap', help='write a reference snapshot')
    s.add_argument('--out', required=True)
    d = sub.add_parser('diff', help='diff the current source against a snapshot')
    d.add_argument('--ref', required=True)
    args = ap.parse_args()
    return cmd_snap(args) if args.cmd == 'snap' else cmd_diff(args)


if __name__ == '__main__':
    raise SystemExit(main())
