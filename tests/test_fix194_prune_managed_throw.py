"""fix 194 test surface: the prune keeps a USER-level throw, drops a BCL guard.

The predicate is a property of the CALL TARGET, so it can be tested without a
binary: a call to a managed throw helper whose declaring type lives outside
`System.*` is source-level control flow (a restored throw arm); `System.
ThrowHelper.ThrowArgumentOutOfRange_IndexException` is the IL2CPP/BCL guard
noise the pruning exists to remove (keeping one restructured
RpgInventoryManager.AddItem and lost its event sugar).
"""
import os
import sys
from types import SimpleNamespace as NS

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from iced_x86 import Mnemonic  # noqa: E402

from il2cpp.dec.analyze import _AnalyzeMixin  # noqa: E402


class _Call:
    def __init__(self, target):
        self.mnemonic = Mnemonic.CALL
        self.near_branch_target = target


class _Block:
    def __init__(self, targets):
        self.insns = [_Call(t) for t in targets]


def _dec(ns_of_target):
    """A Decompiler stand-in whose one address maps to one managed method."""
    td = NS(namespace=ns_of_target, declaring=0)
    meta = NS(typedefs=[td, NS(namespace=ns_of_target, declaring=-1)],
              methods=[NS(declaring=0, name='ThrowX')])
    il = NS(meta=meta, addr_candidates={0x100: [('method', 0)]})
    return NS(il=il, L=NS(il=il))


def test_a_user_namespace_throw_helper_is_kept():
    dec = _dec('Cysharp.Threading.Tasks.Internal')
    assert _AnalyzeMixin._abort_carries_managed_throw(
        dec, _Block([0x100])) is True


def test_a_bcl_guard_helper_is_pruned():
    dec = _dec('System')
    assert _AnalyzeMixin._abort_carries_managed_throw(
        dec, _Block([0x100])) is False


def test_a_call_with_no_single_candidate_is_pruned():
    dec = _dec('Game.Foo')
    dec.il.addr_candidates = {0x100: [('method', 0), ('method', 0)]}
    assert _AnalyzeMixin._abort_carries_managed_throw(
        dec, _Block([0x100])) is False


def test_a_block_without_a_call_is_pruned():
    dec = _dec('Game.Foo')
    assert _AnalyzeMixin._abort_carries_managed_throw(dec, _Block([])) is False


def test_a_constructed_exception_arm_is_kept():
    # new T(args) + raise + int3: two calls, one of them unregistered. The arm
    # constructs its own exception, so it is source-level control flow even
    # though the raiser has no metadata owner.
    dec = _dec('System')
    dec.il.addr_candidates = {0x100: [], 0x200: []}
    assert _AnalyzeMixin._abort_carries_managed_throw(
        dec, _Block([0x100, 0x200])) is True
