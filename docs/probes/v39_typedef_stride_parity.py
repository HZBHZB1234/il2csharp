"""Settle the TypeDef start/count field order empirically and prove the
stride patch is behaviour-neutral, using a full-tuple comparison that does
not depend on my remembering the dataclass order."""
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
import struct
import sys

from il2cpp.metadata import Metadata

GAME = str(_game_dir())
META = GAME + r'\BepInEx\decrypted-metadata.dat'

m = Metadata(META)
d = m.d
tdo = m.hdr['typeDefinitionsOffset']
n = m.hdr['typeDefinitionsCount']
assert m.type_w == 4 and m.gc_w == 2

# Reference parse with an explicit 82 stride, building a TypeDef-shaped
# tuple in the dataclass's own field order.
ref = []
for i in range(n):
    b = tdo + i * 82
    name = m.getstr(struct.unpack_from('<I', d, b)[0])
    ns = m.getstr(struct.unpack_from('<I', d, b + 4)[0])
    byval, decl, parent = struct.unpack_from('<3i', d, b + 8)
    gcv = struct.unpack_from('<H', d, b + 20)[0]
    gc = -1 if gcv == 0xFFFF else gcv
    flags = struct.unpack_from('<I', d, b + 22)[0]
    starts = struct.unpack_from('<8i', d, b + 26)
    counts = struct.unpack_from('<8H', d, b + 58)
    bitfield = struct.unpack_from('<I', d, b + 74)[0]
    token = struct.unpack_from('<I', d, b + 78)[0]
    ref.append((i, name, ns, byval, decl, parent, -1, gc, flags,
                starts[0], starts[1], starts[2], starts[3], starts[4],
                starts[5], starts[6], starts[7],
                counts[0], counts[1], counts[2], counts[3], counts[4],
                counts[5], counts[6], counts[7], bitfield, token))

# Compare against the parser by rebuilding the same tuple from its objects.
import dataclasses


def as_tuple(t):
    return tuple(getattr(t, f.name) for f in dataclasses.fields(t))


patched = [as_tuple(t) for t in m.typedefs]

print('rows compared:', len(patched))
diff = [i for i, (a, b) in enumerate(zip(patched, ref)) if a != b]
print('mismatched rows:', len(diff))
for i in diff[:3]:
    print(' row', i)
    print('  patched', patched[i])
    print('  ref    ', ref[i])
if not diff:
    print('IDENTICAL -- stride patch is behaviour-neutral on Limbus')

# Independently confirm which start is fields and which is methods, by
# checking that methods land inside the methods table and fields inside
# the fields table.
msize = m.hdr['methodsSize'] // 32
fsize = m.hdr['fieldsSize'] // 12
okm = okf = 0
for t in m.typedefs[:2000]:
    if 0 <= t.method_start and t.method_start + t.method_count <= msize:
        okm += 1
    if 0 <= t.field_start and t.field_start + t.field_count <= fsize:
        okf += 1
print('of first 2000 typedefs: method ranges valid=%d  field ranges valid=%d'
      % (okm, okf))
