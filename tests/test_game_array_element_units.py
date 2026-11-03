"""Real native struct-array reads use field widths, not hardware byte scale."""
import re

import pytest


@pytest.mark.game('survivors-roguelike-kit')
def test_tmp_character_enum_and_char_reads(raw_game_decompiler):
    il, dec = raw_game_decompiler
    method = il.meta.methods[69643]
    td = il.meta.typedefs[method.declaring]
    assert td.name == 'TMP_TextEventHandler' and method.name == 'LateUpdate'
    text = '\n'.join(dec.lift_method(method, td))
    assert re.search(r'characterInfo\[num\d+\]\.elementType', text)
    assert re.search(r'characterInfo\[num\d+\]\.character', text)
    assert 'characterInfo[num1 * 376]' not in text


@pytest.mark.game('unitask')
def test_player_loop_type_read_is_one_element_not_five(raw_game_decompiler):
    il, dec = raw_game_decompiler
    td = next(td for td in il.meta.typedefs if td.name == 'PlayerLoopHelper')
    method = next(m for m in il.meta.methods[td.method_start:td.method_start+td.method_count]
                  if m.name == 'FindLoopSystemIndex')
    text = '\n'.join(dec.lift_method(method, td))
    assert re.search(r'playerLoopList\[num\d+\]\.type', text)
    assert not re.search(r'playerLoopList\[num\d+ \* 5\]', text)


@pytest.mark.game('survivors-roguelike-kit')
def test_shared_tail_clones_preserve_character_array_type(raw_game_decompiler):
    il, dec = raw_game_decompiler
    method = il.meta.methods[69863]
    td = il.meta.typedefs[method.declaring]
    assert method.name == 'MoveNext' and 'AnimateVertexColors' in td.name
    text = '\n'.join(dec.lift_method(method, td))
    assert len(re.findall(r'TMPro\.TMP_CharacterInfo\[\] \w+ = .*\.characterInfo;', text)) >= 3
    assert not re.search(r'object obj\d+ = .*\.characterInfo;', text)


@pytest.mark.game('unitask')
def test_nested_awaiter_declarations_are_repaired_after_tail_typing(raw_game_decompiler):
    il, dec = raw_game_decompiler
    method = il.meta.methods[22089]
    td = il.meta.typedefs[method.declaring]
    assert method.name == 'MoveNext' and td.name == '<BindToCore>d__2'
    text = '\n'.join(dec.lift_method(method, td))
    # Bare declarations preserve definite-assignment diagnostics; no defaults
    # are synthesized to make a state-machine join appear initialized.
    assert len(re.findall(r'UniTask<bool>\.Awaiter \w+;', text)) >= 10
    assert re.search(r'<BindToCore>d__2 \w+;', text)
