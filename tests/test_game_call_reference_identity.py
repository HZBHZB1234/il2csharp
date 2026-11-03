"""Factory return identity survives copied field and condition expressions."""
import pytest
from iced_x86 import Decoder, Mnemonic, OpKind

pytestmark = pytest.mark.game('unitask')


@pytest.mark.parametrize('mi,name', [(21473, 'CreateFromCanceled'),
                                   (21474, 'CreateFromException'),
                                   (21475, 'CreateCompleted')])
def test_auto_reset_factory_call_is_evaluated_once(raw_game_decompiler, mi, name):
    il, dec = raw_game_decompiler
    method = il.meta.methods[mi]
    td = il.meta.typedefs[method.declaring]
    assert td.name == 'AutoResetUniTaskCompletionSource'
    assert method.name == name
    factory = il.meta.methods[21472]
    assert factory.name == 'Create' and factory.declaring == td.index
    start, end = il.function_extent(method.addr)
    native = Decoder(64, il.bin.read(start, end - start), ip=start)
    assert sum(i.mnemonic == Mnemonic.CALL and i.op0_kind == OpKind.NEAR_BRANCH64
               and i.near_branch_target == factory.addr for i in native) == 1
    text = '\n'.join(dec.lift_method(method, td))
    assert text.count('AutoResetUniTaskCompletionSource.Create()') == 1
    assert 'token = autoResetUniTaskCompletionSource1.core.version;' in text
    assert 'return autoResetUniTaskCompletionSource1;' in text
    if mi != 21475:
        assert 'autoResetUniTaskCompletionSource1.version == autoResetUniTaskCompletionSource1.core.version' in text
