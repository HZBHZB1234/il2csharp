"""Print real bodies from the worst files so the defects can be read, not
just counted.  Pick by the audit's noise ranking and print full methods.
"""
import io
import os
import re
import sys

ROOT = r'E:\desktop\work\LimbusDecompile\il2csharp\limbus_out1'
AC = os.path.join(ROOT, 'Assembly-CSharp')

TARGETS = [
    'PassiveAbility_1051402.cs',
    'StageScript_9564Base.cs',
    'CoinAbility_1041004_2.cs',
]


def find(name):
    for dp, _d, fs in os.walk(AC):
        if name in fs:
            return os.path.join(dp, name)
    return None


for t in TARGETS:
    p = find(t)
    print('#' * 78)
    print('#', t, '->', p)
    print('#' * 78)
    if not p:
        print('  NOT FOUND')
        continue
    d = io.open(p, 'rb').read().decode('utf-8', 'replace')
    lines = d.split('\n')
    print('total lines:', len(lines))
    # print the whole file if small, else the first 3 methods
    idx = [i for i, l in enumerate(lines) if '// RVA:' in l]
    if len(lines) <= 210:
        print(d)
    else:
        print('(%d methods; showing first 3)' % len(idx))
        for k in range(min(3, len(idx))):
            j = idx[k] - 1
            while j > 0 and not re.match(
                    r'\s*(public|private|internal|protected)', lines[j]):
                j -= 1
            end = idx[k + 1] - 1 if k + 1 < len(idx) else len(lines)
            print('---- method %d ----' % (k + 1))
            print('\n'.join(lines[j:min(end, j + 70)]))
    print()
