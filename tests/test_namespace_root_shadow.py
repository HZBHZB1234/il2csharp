"""A retained full namespace must not bind against a relative child."""
from il2cpp.csharp import strip_namespaces

NS = {'Game', 'Game.Kit', 'Game.Kit.Game', 'Game.Kit.Game.Kit'}


def rewrite(line, ns='Game.Kit', uses=None, dup=('Enemy',)):
    return strip_namespaces([line], uses or {'Game.Kit'}, ns, dup, NS)[0]


def test_preserved_namespace_is_rooted_when_a_child_shadows_its_head():
    assert rewrite('Game.Kit.Enemy owner;') == 'global::Game.Kit.Enemy owner;'


def test_parent_namespace_children_also_shadow_the_root():
    assert rewrite('Game.Kit.Enemy owner;', ns='Game.Kit.Sub') == \
        'global::Game.Kit.Enemy owner;'


def test_unambiguous_shortening_remains_short():
    assert rewrite('Game.Kit.Player player;') == 'Player player;'


def test_global_namespace_has_no_relative_child_shadow():
    assert rewrite('Game.Kit.Enemy owner;', ns='') == 'Game.Kit.Enemy owner;'


def test_existing_global_prefix_is_not_stripped_or_doubled():
    line = 'global::Game.Kit.Enemy owner;'
    assert rewrite(line) == line


def test_literals_comments_and_unproved_member_chains_stay_unchanged():
    line = 'Log("Game.Kit.Enemy"); item.Game.Kit.Enemy = 1; // Game.Kit.Enemy'
    assert rewrite(line) == line


def test_no_metadata_shadow_preserves_previous_spelling():
    line = 'Game.Kit.Enemy owner;'
    assert strip_namespaces([line], {'Game.Kit'}, 'Game.Kit', {'Enemy'},
                            {'Game', 'Game.Kit'}) == [line]


def test_namespace_type_self_shadow_is_rooted_too():
    line = 'HID.HID.HIDDeviceDescriptor field;'
    assert strip_namespaces([line], {'HID'}, 'Game.Kit', (),
                            NS | {'HID', 'Game.Kit.HID'}) == ['global::' + line]
