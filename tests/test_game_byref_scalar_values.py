"""Native UniTask token writes must assign the managed output parameter."""
import pytest

pytestmark = pytest.mark.game('unitask')


def test_create_completed_writes_out_token_instead_of_treating_it_as_an_address(raw_game_decompiler):
    il, dec = raw_game_decompiler
    method = il.meta.methods[21475]
    td = il.meta.typedefs[method.declaring]
    assert td.name == 'AutoResetUniTaskCompletionSource'
    assert method.name == 'CreateCompleted'
    text = '\n'.join(dec.lift_method(method, td))
    assert 'token = autoResetUniTaskCompletionSource1.core.version;' in text
    assert '*(token ' not in text
    assert '__addr(token)' not in text
    assert ' = token;' not in text


def test_byref_typed_phi_keeps_the_unresolved_indirect_write(raw_game_decompiler):
    # This ordinary Type local inherited a byref type during merging, but
    # is NOT emitted as a ref alias. Rewriting its store as an assignment
    # lets later cleanup erase the native side effect entirely.
    import re
    il, dec = raw_game_decompiler
    td = il.meta.typedefs[3638]
    assert td.name == 'DiagnosticsExtensions'
    method = next(m for m in il.meta.methods if m.declaring == td.index
                  and m.name == 'TryResolveStateMachineMethod')
    text = '\n'.join(dec.lift_method(method, td))
    assert re.search(r'\(\(byte\*\)type\d+ \+ 0x0\)\[0\] = ', text)
