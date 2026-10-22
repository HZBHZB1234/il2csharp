"""Confirm the CodeRegistration start address definitively.

Layout seen at Limbus, from X=0x1876d07d0 (the codeGenModules pointer)
backwards:

  X- 1*8 = 162          codeGenModulesCount      (matches 162 images)
  X- 2*8 = 0            interopData?  / unused
  X- 3*8 = 0            ...
  X- 4*8 = 0x188d34380  a pointer (2069 next)
  X- 5*8 = 2069         a count
  X- 6*8 = 0x187775dfc0 unresolvedStaticCallPointers
  X- 7*8 = 0x187735e00 unresolvedInstanceCallPointers
  X- 8*8 = 0x187749ee0 unresolvedVirtualCallPointers
  X- 9*8 = 10267        unresolvedVirtualCallCount
  X-10*8 = 0x1876d07f0 invokerPointers
  X-11*8 = 51798        invokerPointersCount
  X-12*8 = 0x1878b22a0 genericAdjustorThunks
  X-13*8 = 0x187e0e0c0 genericMethodPointers
  X-14*8 = 299705       genericMethodPointersCount
  X-15*8 = 0x187735aa0 reversePInvokeWrappers
  X-16*8 = 108          reversePInvokeWrapperCount   <-- struct start
  X-17*8 = 0
  X-18*8 = 0x0000001000000010 (looks like a preceding struct tail)

So the struct is 17 qwords: X-16*8 .. X-1*8 inclusive.
The code logs X-18*8 = X-144, which is 16 bytes (2 qwords) too low.
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
import sys

from il2cpp import Metadata, load_binary, Il2Cpp

GAME = str(_game_dir())
m = Metadata(GAME + r'\BepInEx\decrypted-metadata.dat')
b = load_binary(GAME + r'\GameAssembly.dll')
il = Il2Cpp(m, b)
il.find_registrations()

X = il.code_gen_modules_field
start = X - 16 * 8
print('real CodeRegistration start  = %#x  (X - 16*8)' % start)
print('currently logged            = %#x  (X - 18*8)' % il.code_reg_va)
print('difference                  = %#x bytes' % (start - il.code_reg_va))

# Sanity: qwords at start..start+15 must look like (count, ptr) pairs.
names = ['reversePInvokeWrapperCount', 'reversePInvokeWrappers',
         'genericAdjustorThunks', 'genericMethodPointersCount',
         'genericMethodPointers', 'invokerPointersCount', 'invokerPointers',
         'unresolvedVirtualCallCount', 'unresolvedVirtualCallPointers',
         'unresolvedInstanceCallPointers', 'unresolvedStaticCallPointers',
         '?1', '?2', 'codeGenModulesCount', 'codeGenModules']
print('--- 17 qwords from the real start ---')
for i in range(17):
    v = b.qword(start + i * 8)
    lbl = names[i] if i < len(names) else '?'
    kind = 'PTR' if 0x18000000000 < v < 0x19000000000 else (
        'CNT' if 0 < v < 0x1000000 else '   ')
    print('  [%2d] %#018x  %-3s %s' % (i, v, kind, lbl))
