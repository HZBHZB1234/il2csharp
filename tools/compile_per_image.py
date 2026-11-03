"""Compile every image of a tree SEPARATELY against the original closure.

`compile_corpus` compiles the whole tree as one assembly, which manufactures
errors the real project never had: the same generated scaffolding emitted in
several images (CS0111), an `internal` type from a sibling image (CS0051/52/53),
and a namespace that only shadows the root when 75 assemblies become one
(CS0234). This driver answers a narrower question: is ONE image self-consistent
against the closure the original build used.

Caveat measured on the survivors fixture (2026-11-03): this model is NOT a
quality metric either. Each image is compiled against the ORIGINAL sibling
dlls, so every recovered type the siblings also declare is a second, distinct
type -- CS0030 (5,068) and CS1061 (3,803) are type-identity conflicts, not
decompiler defects -- and calls into a sibling's inlined internal member are
CS0122 (4,861). The whole-tree model is the number to quote; BCL images are
skipped because a corlib cannot be compiled against itself (CS0518 x41k).

Usage:
    python tools/compile_per_image.py <fixture> <label> <report.json>
"""
import json
import os
import re
import subprocess
import sys
from collections import Counter

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def main(argv):
    fixture, label, report = argv[1], argv[2], os.path.abspath(argv[3])
    tree = os.path.join(REPO, 'out', fixture, label)
    totals = Counter()
    per_image = {}
    skipped = []
    for name in sorted(os.listdir(tree)):
        img = os.path.join(tree, name)
        if not os.path.isdir(img):
            continue
        if not any(f.endswith('.cs') for _, _, fs in os.walk(img) for f in fs):
            continue
        if name.startswith(('mscorlib', 'System', 'Mono.')):
            # a corlib cannot be compiled against itself: without a corlib
            # reference every predefined type is CS0518 (41k on this fixture),
            # so these images are not part of this metric
            skipped.append({'image': name, 'rc': 'bcl'})
            continue
        rep = report + '.' + name + '.json'
        proc = subprocess.run(
            [sys.executable, os.path.join(REPO, 'tools', 'gate.py'),
             '--fixture', fixture, '--tree', img,
             '--managed-refs', '--report', rep, 'compile'],
            cwd=REPO, capture_output=True, text=True,
            env=dict(os.environ, PYTHONHASHSEED='0',
                     PYTHONPATH=os.pathsep.join(
                         [REPO, os.path.join(REPO, 'tools')])))
        if not os.path.exists(rep):
            skipped.append({'image': name, 'rc': proc.returncode,
                            'stderr': (proc.stderr or '')[-300:]})
            continue
        with open(rep, encoding='utf-8') as fh:
            d = json.load(fh)
        codes = Counter()
        for row in (d.get('top') or []):
            try:
                codes[row[0]] += int(row[1])
            except Exception:
                pass
        per_image[name] = {'syntax': d.get('syntax', 0),
                           'binding': d.get('binding', 0),
                           'codes': dict(codes), 'refs': d.get('refs')}
        totals.update(codes)
        print('%-46s syntax=%-3d binding=%-4d %s' % (
            name, d.get('syntax', 0), d.get('binding', 0),
            dict(codes.most_common(4))))
    out = {'fixture': fixture, 'label': label,
           'per_image': per_image,
           'totals': dict(totals.most_common()),
           'syntax_total': sum(v['syntax'] for v in per_image.values()),
           'binding_total': sum(v['binding'] for v in per_image.values()),
           'skipped': skipped}
    with open(report, 'w', encoding='utf-8') as fh:
        json.dump(out, fh, indent=1)
    print('TOTAL syntax=%d binding=%d' % (out['syntax_total'],
                                          out['binding_total']))
    print('top codes', totals.most_common(8))
    if skipped:
        print('skipped images:', [s['image'] for s in skipped])
    return 0


if __name__ == '__main__':
    if len(sys.argv) != 4:
        raise SystemExit(__doc__)
    raise SystemExit(main(sys.argv))
