"""Body-tier measurement, one image at a time (no cross-image duplicates).

`tools/body_tier.py` measures a whole tree, but a whole-tree compile carries
cross-image duplicate types (CS0101/CS0102/CS0111), which are declaration-tier
errors and therefore mask body binding again. This mode compiles each image
against the ORIGINAL closure (the image under test excluded, so its own types
come from its sources) and runs the stub loop per image.

Usage:
    python tools/body_tier_per_image.py <fixture> <label> <report.json> [rounds]
"""
import glob
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
from collections import Counter

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(REPO, 'tools'))
import compile_gate as cg  # noqa: E402

BCL_PREFIX = ('mscorlib', 'System', 'Mono.', 'netstandard')
DECL_CODES = ('CS0234', 'CS0246', 'CS0116')
NAMES_RX = [
    ('CS0246', re.compile(r"error CS0246: .*?'([A-Za-z_][\w.<>`]*)'")),
    ('CS0234', re.compile(r"error CS0234: .*?'([A-Za-z_][\w.]*)'")),
]


def compile_once(scratch, tag, files, refs):
    rsp = os.path.join(scratch, 'rsp_%s.txt' % tag)
    cmd = ['-nologo', '-target:library', '-unsafe', '-nowarn:1701,1702',
           '-utf8output', '-out:' + os.path.join(scratch, 'o_%s.dll' % tag)]
    cmd += ['-r:"%s"' % r for r in refs]
    cmd += ['"%s"' % f for f in files]
    with open(rsp, 'w', encoding='utf-8') as fh:
        fh.write('\n'.join(cmd) + '\n')
    proc = subprocess.run([shutil.which('dotnet') or 'dotnet', cg.find_csc(),
                           '-noconfig', '@' + rsp], capture_output=True)
    out = cg._decode(proc.stdout) + cg._decode(proc.stderr)
    return [l for l in out.splitlines() if ' error ' in l]


def main(argv):
    fixture, label, report = argv[1], argv[2], os.path.abspath(argv[3])
    rounds = int(argv[4]) if len(argv) > 4 else 3
    tree = os.path.join(REPO, 'out', fixture, label)
    mdir = glob.glob(os.path.join(REPO, 'fixtures', fixture, 'build',
                                  '*BackUpThisFolder*', 'Managed'))[0]
    all_refs = [os.path.join(mdir, f) for f in sorted(os.listdir(mdir))
                if f.endswith('.dll')]
    scratch = tempfile.mkdtemp(prefix='il2csharp_bodytier_img_')
    per_image = {}
    totals = Counter()
    for name in sorted(os.listdir(tree)):
        d = os.path.join(tree, name)
        if not os.path.isdir(d):
            continue
        files = sorted(glob.glob(os.path.join(d, '**', '*.cs'), recursive=True))
        if not files:
            continue
        if any(name == p or name.startswith(p) for p in BCL_PREFIX):
            continue
        refs = [r for r in all_refs
                if os.path.basename(r) != name + '.dll']
        stub_path = os.path.join(scratch, '__Stubs_%s.cs' % abs(hash(name)))
        stubs = ['// diagnostic stubs']
        with open(stub_path, 'w', encoding='utf-8', newline='\n') as fh:
            fh.write('\n'.join(stubs))
        srcs = files + [stub_path]
        best = None
        for r in range(rounds):
            rows = compile_once(scratch, '%s_%d' % (abs(hash(name)), r),
                               srcs, refs)
            codes = Counter(re.findall(r'error (CS\d+)', '\n'.join(rows)))
            decl = sum(v for k, v in codes.items() if k in DECL_CODES)
            best = (len(rows), codes, decl)
            if decl == 0:
                break
            seen = set()
            for row in rows:
                for code, rx in NAMES_RX:
                    if code not in row:
                        continue
                    m = rx.search(row)
                    if not m:
                        continue
                    nm = m.group(1).split('<')[0].strip('.')
                    if not nm or nm in seen:
                        continue
                    seen.add(nm)
                    ns, _, short = nm.rpartition('.')
                    stubs.append(('namespace %s { internal class %s { } }'
                                  % (ns, short)) if ns
                                 else ('internal class %s { }' % short))
            with open(stub_path, 'w', encoding='utf-8',
                      newline='\n') as fh:
                fh.write('\n'.join(stubs))
            if not seen:
                break
        total, codes, decl = best
        per_image[name] = {'errors': total, 'declaration': decl,
                           'codes': dict(codes.most_common(8)),
                           'files': len(files)}
        totals.update(codes)
        print('%-44s files=%-4d errors=%-5d decl=%-4d %s'
              % (name, len(files), total, decl, dict(codes.most_common(3))))
    out = {'fixture': fixture, 'label': label, 'per_image': per_image,
           'errors_total': sum(v['errors'] for v in per_image.values()),
           'declaration_total': sum(v['declaration'] for v in per_image.values()),
           'totals': dict(totals.most_common())}
    with open(report, 'w', encoding='utf-8') as fh:
        json.dump(out, fh, indent=1)
    print('TOTAL errors=%d declaration=%d' % (out['errors_total'],
                                              out['declaration_total']))
    print('top codes', totals.most_common(8))
    return 0


if __name__ == '__main__':
    raise SystemExit(main(sys.argv))
