"""Live metadata/native proof, never a method-name based implementation shortcut."""
import pytest


@pytest.mark.parametrize('mi', [
    pytest.param(71258, marks=pytest.mark.game('survivors-roguelike-kit')),
    pytest.param(30307, marks=pytest.mark.game('unitask')),
])
def test_full_native_uint_string_fold(raw_game_decompiler, mi):
    from il2cpp.dec.stringfold import lift_u32_string_fold
    il, dec = raw_game_decompiler
    method = il.meta.methods[mi]
    td = il.meta.typedefs[method.declaring]
    assert method.name == 'ComputeStringHash'
    native, skip = dec._decode(method)
    proof = lift_u32_string_fold(il, method, td, native, skip,
                                 il.eh_regions(method.addr))
    assert proof is not None
    body = dec.lift_method(method, td)
    assert body == proof
    text = '\n'.join(body)
    assert 'uint hash = 2166136261u;' in text
    assert 'hash = unchecked((hash ^ s[index]) * 16777619u);' in text
    assert 'index < s.Length' in text and 'return 0u;' in text
    assert not any(s in text for s in ('char ', 'unsafe', 'sub_', 'default'))
    # An explicit failed proof returns to the ordinary symbolic path. Its
    # current phi typing is deliberately NOT hidden by casts or a default.
    import il2cpp.dec.stringfold as module
    original = module.lift_u32_string_fold
    try:
        module.lift_u32_string_fold = lambda *a, **k: None
        before = '\n'.join(dec.lift_method(method, td))
    finally:
        module.lift_u32_string_fold = original
    assert 'char ' in before
    assert dec.lift_method(method, td) == body
