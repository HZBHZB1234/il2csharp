"""Fix 159: the interface dispatch twins admit at arity 1.

0x180013b50 / 0x180016f40 (2,778 call sites) are the shared-generic
interface dispatch thunks: (u16 methodSlot, interfaceTypeIndex, recv,
<first method arg>) with the stack args forwarded by the tail-jump.
The body is exactly the shape `_iface_dispatch_arity` already
recognizes -- and the landed `_param_interface_dispatch` fold handles
the rest (stack tiles, closed generics, ABI gates). The twins were
held at arity 0 by one register-name comparison: they extract the
forwarded argument as `movzx esi,r9w` / `mov esi,r9d`, and
`_r9_touch` compared iced operand registers against R9 directly, so a
sub-register read counted as no touch.

Sites fold to the interface's own method (slot = the interface's
method-row order):

    if (readOnlyList11[num2] == this._curSkillMotion)
    string text1 = staticDataJson.GetDataByIndex(num4);
    string text3 = retryHandler.GetTurnCountText(turnCount);
"""
import pytest

from game_support import find_method, lift_text

pytestmark = pytest.mark.game("limbus")

THUNK_A = 0x180013b50
THUNK_B = 0x180016f40


def test_both_thunk_builds_admit_at_arity_one(baseline_game_decompiler):
    il, dec = baseline_game_decompiler
    L = dec.L
    assert L._iface_dispatch_arity(THUNK_A) == 1
    assert L._iface_dispatch_arity(THUNK_B) == 1
    # the memoized choke answers identically
    assert L._iface_arity(THUNK_A) == 1
    assert L._iface_arity(THUNK_B) == 1


def test_closed_generic_indexer_site_folds(baseline_game_decompiler):
    """IReadOnlyList`1 slot 0 = get_Item: the fold renders the
    closed-generic indexer, not the thunk call."""
    il, dec = baseline_game_decompiler
    mi, _, _ = find_method(
        il, 'BattleSkillViewSkin_UseLastMotionOnLastCoin', 'BuildMotionOrder', 4)
    body = lift_text(il, dec, mi)
    assert 'sub_180016f40' not in body
    assert 'sub_180013b50' not in body
    assert '[num2]' in body or 'get_Item' in body


def test_stack_argument_recovered_site_folds(baseline_game_decompiler):
    """IStaticDataJson.GetDataByIndex(int): the argument travels in a
    stack tile; the landed recovery renders it."""
    il, dec = baseline_game_decompiler
    mi, _, _ = find_method(
        il, 'AttendanceRewardsByPartDataList', 'Init', 1)
    body = lift_text(il, dec, mi)
    assert 'sub_180016f40' not in body
    assert 'GetDataByIndex(' in body
