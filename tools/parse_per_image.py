"""Parse-gate a tree one image directory at a time.

`tools/gate.py parse` runs tree-sitter over the whole tree in one process, and
that process can die with an access violation on a large tree (measured on the
survivors fixture: exit 0xC0000005 with no report written, although every file
parses fine on its own). This driver runs the same gate per image, so one
crash confines to one image and every other image still reports, then merges
the per-image reports into the tree-level one.

Usage:
    python tools/parse_per_image.py <tree> <report.json>
"""
import json
import os
import subprocess
import sys

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
KEYS = ('files', 'bad_files', 'errors', 'missing', 'recovery_nodes')


def main(argv):
    tree = os.path.abspath(argv[1])
    report = os.path.abspath(argv[2])
    totals = {k: 0 for k in KEYS}
    crashed = []
    details = {}
    per_image = {}
    for name in sorted(os.listdir(tree)):
        img = os.path.join(tree, name)
        if not os.path.isdir(img):
            continue
        if not any(f.endswith('.cs') for _, _, fs in os.walk(img) for f in fs):
            continue
        rep = report + '.' + name + '.json'
        proc = subprocess.run(
            [sys.executable, os.path.join(REPO, 'tools', 'gate.py'),
             '--tree', img, '--report', rep, 'parse'],
            cwd=REPO, capture_output=True, text=True,
            env=dict(os.environ, PYTHONHASHSEED='0',
                     PYTHONPATH=os.pathsep.join(
                         [REPO, os.path.join(REPO, 'tools')])))
        if proc.returncode != 0 or not os.path.exists(rep):
            crashed.append({'image': name, 'rc': proc.returncode,
                            'stderr': (proc.stderr or '')[-400:]})
            continue
        with open(rep, encoding='utf-8') as fh:
            d = json.load(fh)
        for k in KEYS:
            totals[k] += d.get(k, 0)
        per_image[name] = {k: d.get(k, 0) for k in KEYS}
        for f, nodes in (d.get('details') or {}).items():
            details[f] = nodes
        print('%-46s files=%-5d bad=%-3d err=%-3d missing=%-3d' % (
            name, d.get('files', 0), d.get('bad_files', 0),
            d.get('errors', 0), d.get('missing', 0)))
    out = dict(totals)
    out['images'] = per_image
    out['crashed_images'] = crashed
    out['details'] = details
    with open(report, 'w', encoding='utf-8') as fh:
        json.dump(out, fh, indent=1)
    print('TOTAL', {k: totals[k] for k in KEYS})
    if crashed:
        print('crashed images (parse them file by file):',
              [c['image'] for c in crashed])
    return 0 if not crashed else 1


if __name__ == '__main__':
    if len(sys.argv) != 3:
        raise SystemExit(__doc__)
    raise SystemExit(main(sys.argv))
