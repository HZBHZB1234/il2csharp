"""The tree shows 0 `d__NNN` classes, but that regex may be wrong: the
emitter may sanitize `<>` out of identifiers.  Ask the METADATA directly
what the compiler-generated state machine types are called, then look for
them by their attributes instead of by name.

Ground truth: async/iterator methods carry
AsyncStateMachineAttribute / IteratorStateMachineAttribute, and their
state machine types are nested private classes whose name starts with '<'.
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
import re
import sys

from il2cpp import Metadata

GAME = str(_game_dir())
m = Metadata(GAME + r'\BepInEx\decrypted-metadata.dat')

# 1. Types whose name starts with '<' (compiler-generated nests)
odd = [t for t in m.typedefs if t.name.startswith('<')]
print('types whose name starts with "<":', len(odd))
from collections import Counter
pat = Counter()
for t in odd:
    pat[re.sub(r'\d+', 'N', t.name)[:40]] += 1
for k, v in pat.most_common(25):
    print('  %-42s %d' % (k, v))
print()

# 2. Names containing d__ or __state or MoveNext
for probe, label in ((r'd__\d+', 'name contains d__N'),
                     (r'__state', 'name contains __state'),
                     (r'MoveNext', 'name contains MoveNext'),
                     (r'SetStateMachine', 'name contains SetStateMachine')):
    hits = [t for t in m.typedefs if re.search(probe, t.name)]
    print('%-28s %d' % (label, len(hits)))
    for t in hits[:5]:
        print('     ', t.name, '|', t.namespace)
print()

# 3. Methods named MoveNext anywhere
mn = [x for x in m.methods if x.name == 'MoveNext']
print('methods named MoveNext:', len(mn))
for x in mn[:8]:
    td = m.typedefs[x.declaring] if 0 <= x.declaring < len(m.typedefs) else None
    print('   owner=%s  addr=%#x' % (td.name if td else '?', x.addr))
