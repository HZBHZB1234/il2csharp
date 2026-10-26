"""Fix 148: the second alloc helper folds delegate construction
(limbus v39 ground truth).

`0x1807e3d20` is the class-init wrapper around the same allocator as
`0x1807933d0` (1,226 klass-argument sites). The classifier's
single-slot rule kept only the first, so this one rendered as
`sub_1807e3d20(typeof(T))` and every delegate-construction site built
on it stayed an untyped `object`:

    object obj21 = sub_1807e3d20(typeof(Action));
    sub_1811cce50/*shared body, 30 candidates*/(obj21, this,
                                                Type.OnNotGenuine...);

With the family recognized, the allocation carries its type and the
existing delegate arm completes the ctor:

    System.Action action1 = new System.Action(this.OnNotGenuineDataDetected);

`sub_1811cce50` alone is 5,845 sites tree-wide -- the largest single
shared-body population.
"""
import pytest

from game_support import find_method, lift_text

pytestmark = pytest.mark.game("limbus")


def test_delegate_ctor_renders_as_new_action(baseline_game_decompiler):
    il, dec = baseline_game_decompiler
    mi, _, _ = find_method(
        il, 'CodeStage.AntiCheat.Examples.ObscuredFilePrefsExamples',
        'Start', 0)
    body = lift_text(il, dec, mi)
    assert 'sub_1811cce50' not in body
    assert 'sub_1807e3d20' not in body
    assert 'new System.Action(this.OnNotGenuineDataDetected)' in body
    assert 'new System.Action(this.OnDataFromAnotherDeviceDetected)' in body


def test_typed_allocation_unlocks_named_list_fields(baseline_game_decompiler):
    """A typed `new List<T>()` lets the inlined Add fast path read
    `_size`/`_items` instead of raw pointer arithmetic."""
    il, dec = baseline_game_decompiler
    mi, _, _ = find_method(
        il, 'Stores.Util.JsonProductDescriptionsDeserializer',
        'DeserializeProductDescriptions', 1)
    body = lift_text(il, dec, mi)
    assert 'new System.Collections.Generic.List_1<' in body
    assert 'list11._size' in body and 'list11._items' in body
