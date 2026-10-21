"""Literal-aware brace audit for the v39 tree (work/lib/tree_brace_audit.py
is not present in this checkout).

Counts { and } outside string/char literals and /* */ comments, which is
what the project's own brace audit does -- a naive count reports false
positives on literals like "BitVector32{".
"""
import io
import os
import sys

ROOT = (sys.argv[1] if len(sys.argv) > 1 else
        r'E:\desktop\work\LimbusDecompile\il2csharp\limbus_out1')


def strip_literals(line):
    """Blank out string/char literals and comments, preserving length."""
    out = []
    i = 0
    n = len(line)
    while i < n:
        c = line[i]
        if c == '"':
            if line.startswith('@"', i):
                j = i + 2
                while j < n:
                    if line[j] == '"':
                        if j + 1 < n and line[j + 1] == '"':
                            j += 2
                            continue
                        break
                    j += 1
                out.append(' ' * (min(j + 1, n) - i))
                i = j + 1
                continue
            j = i + 1
            while j < n and line[j] != '"':
                j += 2 if line[j] == '\\' else 1
            out.append(' ' * (min(j + 1, n) - i))
            i = j + 1
            continue
        if c == "'":
            j = i + 1
            while j < n and line[j] != "'":
                j += 2 if line[j] == '\\' else 1
            out.append(' ' * (min(j + 1, n) - i))
            i = j + 1
            continue
        if line.startswith('//', i):
            out.append(' ' * (n - i))
            break
        if line.startswith('/*', i):
            out.append(' ' * (n - i))
            break
        out.append(c)
        i += 1
    return ''.join(out)


def audit(path):
    d = io.open(path, 'rb').read().decode('utf-8', 'replace')
    depth = 0
    in_block = False
    for raw in d.split('\n'):
        line = raw
        if in_block:
            k = line.find('*/')
            if k < 0:
                continue
            line = ' ' * (k + 2) + line[k + 2:]
            in_block = False
        s = strip_literals(line)
        while True:
            k = s.find('/*')
            if k < 0:
                break
            e = s.find('*/', k + 2)
            if e < 0:
                in_block = True
                s = s[:k] + ' ' * (len(s) - k)
                break
            s = s[:k] + ' ' * (e + 2 - k) + s[e + 2:]
        depth += s.count('{') - s.count('}')
        if depth < 0:
            return depth
    return depth


bad = []
n = 0
total_lines = 0
for dirpath, _dirs, files in os.walk(ROOT):
    for f in files:
        if not f.endswith('.cs'):
            continue
        p = os.path.join(dirpath, f)
        n += 1
        try:
            d = audit(p)
        except Exception as e:
            bad.append((p, 'ERROR %s' % e))
            continue
        if d:
            bad.append((p, 'delta %d' % d))

print('files audited :', n)
print('unbalanced    :', len(bad))
for p, why in bad[:20]:
    print('  ', why, p)
print('RESULT:', 'PASS (0 unbalanced)' if not bad else 'FAIL')
