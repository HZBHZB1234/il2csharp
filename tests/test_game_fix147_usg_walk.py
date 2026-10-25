"""Fix 147: shared-body calls resolve through the identity POINTER WALK
(limbus v39 ground truth).

A site that inlines the source method's core (ContainsKey/TryGetValue
inlining FindEntry, Add inlining its grow path) calls the shared helper
body and passes the identity MethodInfo* as a short pointer walk rooted
at a lazy MethodRef cell. Registered candidate names at those addresses
are mispaired in this fixture (pure-search FindEntry bodies carry
Remove specs at 0x183c23bc0/0x1857f89d0), so the walk root -- the
runtime's own identity, naming the SOURCE-level call -- is the only
trustworthy resolution evidence. `_read_mem_raw` propagates the root
onto every deref (`_usg_root`) and `_call` seats it at the site.

Ground truths: AbnormalityParts_8008.DestroyPart (mi 110185) renders
`this.parts_Breakable.ContainsKey(text1)` /
`this.parts_Breakable.TryGetValue(text1, _)`; AbilityBase.HasKeyword
(mi 1817) renders `this._keywordDic.TryGetValue(keyword, _)`;
ActionSlotDetail..ctor (mi 104984) renders its nine-element Add chain
`list11.Add(...)` where b21 printed nine
`sub_1842e7380/*shared body, 40 candidates*/(list11)` captures.
"""
import pytest

from game_support import find_method, lift_text

pytestmark = pytest.mark.game("limbus")


def test_destroy_part_resolves_containskey_and_trygetvalue(
        baseline_game_decompiler):
    il, dec = baseline_game_decompiler
    mi, _, _ = find_method(
        il, 'AbnormalityParts_8008', 'DestroyPart', 3)
    body = lift_text(il, dec, mi)
    assert 'sub_183c23bc0' not in body
    assert 'this.parts_Breakable.ContainsKey(' in body
    assert 'this.parts_Breakable.TryGetValue(text1, _)' in body


def test_has_keyword_resolves_trygetvalue(baseline_game_decompiler):
    il, dec = baseline_game_decompiler
    mi, _, _ = find_method(il, 'AbilityBase', 'HasKeyword', 1)
    body = lift_text(il, dec, mi)
    assert 'sub_18587c8b0' not in body
    assert 'this._keywordDic.TryGetValue(keyword, _)' in body


def test_action_slot_ctor_recovers_the_add_chain(baseline_game_decompiler):
    il, dec = baseline_game_decompiler
    mi, _, _ = find_method(il, 'ActionSlotDetail', '.ctor', 1)
    body = lift_text(il, dec, mi)
    assert 'sub_1842e7380' not in body
    assert body.count('list11.Add(') == 9
