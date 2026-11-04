"""Exact native-zero leaf return, using original metadata and binary bytes."""
import pytest
from iced_x86 import Mnemonic, OpKind, Register as R

from game_support import lift_text
from il2cpp.dec import analyze

pytestmark = pytest.mark.game('unitask')


def test_small_struct_zero_is_default_not_scalar_or_constructor(
        raw_game_decompiler, monkeypatch):
    il, dec = raw_game_decompiler
    original = analyze.recover_leaf_struct_zero_return
    hits = []

    def observe(lift, text, ty):
        snapshot = {k: tuple(getattr(v, a, None) for a in v.__slots__) if v else None
                    for k, v in dict.items(lift.regs)}
        hints, slots, types = dict(lift._type_hints), dict(lift.slot_types), dict(lift._var_types)
        result = original(lift, text, ty)
        assert snapshot == {k: tuple(getattr(v, a, None) for a in v.__slots__) if v else None
                            for k, v in dict.items(lift.regs)}
        assert hints == lift._type_hints and slots == lift.slot_types and types == lift._var_types
        if result is not None and not lift.dry:
            method = lift._current_method; td = il.meta.typedefs[ty[0]]
            assert method.index == 23169 and method.is_static and method.param_count == 0
            assert td.is_valuetype and not td.is_enum and not td.has_cctor
            assert il.type_sizes[ty[0]] == 8 and td.field_count == 1
            assert il.field_offsets[ty[0]] == [0x10]
            field = il.meta.fields[td.field_start]
            assert il._type_enum(il.types[field.type]) == 0x12
            native, _ = dec._decode(method)
            zero, ret = native[:2]
            assert zero.mnemonic == Mnemonic.XOR and zero.op_count == 2
            assert zero.op0_kind == zero.op1_kind == OpKind.REGISTER
            assert zero.op0_register == zero.op1_register == R.EAX
            assert zero.ip == method.addr and zero.next_ip == ret.ip == lift._cur_ip
            assert ret.mnemonic == Mnemonic.RET and ret.op_count == 0 and ret.len == 1
            assert result == 'default(' + il.type_name(ty) + ')'
            hits.append(result)
        return result

    monkeypatch.setattr(analyze, 'recover_leaf_struct_zero_return', observe)
    candidate = lift_text(il, dec, 23169)
    assert len(hits) == 1
    monkeypatch.setattr(analyze, 'recover_leaf_struct_zero_return', lambda *a: None)
    baseline = lift_text(il, dec, 23169)
    assert baseline.count('return 0;') == 1
    assert baseline.replace('return 0;', 'return ' + hits[0] + ';') == candidate
