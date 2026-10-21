"""Honest quality audit of the exported tree.

Reads real files and measures the things that make output hard to read:
  1. how much of a body is honest markers vs real logic
  2. whether types resolve or collapse to object/unknown
  3. whether control flow structures or degrades to goto
  4. identifier quality (objN / sub_X / vN spam)
  5. per-file noise density

No cherry-picking: sample deterministically across the tree by size band.
"""
import io
import os
import re
import sys
from collections import Counter

ROOT = r'E:\desktop\work\LimbusDecompile\il2csharp\limbus_out1'
AC = os.path.join(ROOT, 'Assembly-CSharp')

files = []
for dp, _d, fs in os.walk(AC):
    for f in fs:
        if f.endswith('.cs'):
            files.append(os.path.join(dp, f))
files.sort()
print('files in Assembly-CSharp:', len(files))

# Deterministic sample across the whole tree.
STEP = max(1, len(files) // 40)
sample = files[::STEP][:40]
print('sampled %d files (every %d-th)' % (len(sample), STEP))
print('=' * 78)

PATTERNS = [
    ('sub_<va>',            re.compile(r'\bsub_[0-9a-f]{6,}\b')),
    ('object objN',         re.compile(r'\bobject\s+obj\d+\b')),
    ('objN use',            re.compile(r'\bobj\d+\b')),
    ('unknown',             re.compile(r'\bunknown\b')),
    ('/* nothing */',       re.compile(r'/\*\s*nothing\s*\*/')),
    ('shared body marker',  re.compile(r'shared body')),
    ('goto',                re.compile(r'\bgoto\b')),
    ('vN temp',             re.compile(r'\bv\d+\b')),
    ('numN temp',           re.compile(r'\bnum\d+\b')),
    ('realN temp',          re.compile(r'\breal\d+\b')),
    ('vectorN temp',        re.compile(r'\bvector\d+\b')),
    ('IntPtr',              re.compile(r'\bIntPtr\b')),
    ('(byte*) cast',        re.compile(r'\(byte\s*\*\)')),
    ('(T*) cast',           re.compile(r'\([A-Za-z_][\w.]*\*\)')),
    ('&address-of',         re.compile(r'&\w')),
]

tot_lines = 0
grand = Counter()
per_file = []

for p in sample:
    d = io.open(p, 'rb').read().decode('utf-8', 'replace')
    n = d.count('\n')
    tot_lines += n
    c = Counter()
    for label, rx in PATTERNS:
        c[label] = len(rx.findall(d))
    for k in c:
        grand[k] += c[k]
    per_file.append((os.path.basename(p), n, c))

print('total sampled lines: %d' % tot_lines)
print()
print('%-22s %8s %10s' % ('marker', 'count', 'per-100-line'))
for label, _rx in PATTERNS:
    print('%-22s %8d %10.2f' % (label, grand[label],
                                grand[label] * 100.0 / max(1, tot_lines)))

print()
print('=' * 78)
print('WORST FILES (marker density)')
print('=' * 78)
scored = []
for name, n, c in per_file:
    noise = (c['sub_<va>'] + c['object objN'] + c['objN use']
             + c['unknown'] + c['goto'] + c['vN temp'] + c['numN temp']
             + c['realN temp'] + c['IntPtr'] + c['/* nothing */'])
    scored.append((noise * 100.0 / max(1, n), name, n, noise))
scored.sort(reverse=True)
for dens, name, n, noise in scored[:12]:
    print('  %5.1f%%  %-46s %5d lines, %d markers' % (dens, name[:46], n, noise))

print()
print('BEST FILES')
for dens, name, n, noise in scored[-5:]:
    print('  %5.1f%%  %-46s %5d lines, %d markers' % (dens, name[:46], n, noise))
