"""Literal-aware brace audit for the v39 tree (work/lib/tree_brace_audit.py
is not present in this checkout).

Counts { and } outside string/char literals and /* */ comments, which is
what the project's own brace audit does -- a naive count reports false
positives on literals like "BitVector32{".
"""
# --- probe bootstrap (repo-relative; no host-absolute paths) ---------
import os as _os
import sys as _sys
from pathlib import Path as _Path
_REPO = _Path(__file__).resolve().parents[2]
_sys.path.insert(0, str(_REPO))
_sys.path.insert(0, str(_REPO / 'tools'))


def _tree():
    """The emitted tree to inspect: $IL2CSHARP_LABEL under the default
    fixture, else argv[1], else an explicit IL2CSHARP_TREE."""
    env = _os.environ.get('IL2CSHARP_TREE')
    if env:
        return _Path(env)
    if len(_sys.argv) > 1 and not _sys.argv[1].startswith('-'):
        return _Path(_sys.argv[1])
    try:
        import fixtures as _fx
        return _fx.require_tree(_fx.resolve())
    except Exception as _ex:
        raise SystemExit('probe needs a tree: pass one on argv, set '
                         'IL2CSHARP_TREE, or build a fixture tree (%s)' % _ex)


def _game_dir():
    """The game directory: $IL2CSHARP_GAME, else the default fixture."""
    env = _os.environ.get('IL2CSHARP_GAME')
    if env:
        return _Path(env)
    try:
        import fixtures as _fx
        return _fx.resolve().game_dir
    except Exception as _ex:
        raise SystemExit('probe needs a game: set IL2CSHARP_GAME or add a '
                         'fixture to fixtures/registry.json (%s)' % _ex)
# ---------------------------------------------------------------------
import io
import os
import sys

ROOT = _tree()


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
