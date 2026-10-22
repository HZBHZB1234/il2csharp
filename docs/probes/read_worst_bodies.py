"""Print real bodies from the worst files so the defects can be read, not
just counted.  Pick by the audit's noise ranking and print full methods.
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
import re
import sys

ROOT = _tree()
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
