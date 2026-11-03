"""Real kind-2 loads prove a Type token without guessing klass offsets."""
import re

import pytest
from iced_x86 import Mnemonic, Register

from game_support import find_method, lift_text
from il2cpp.lifter import calls

pytestmark = pytest.mark.game('survivors-roguelike-kit')


def test_type_registry_direct_type_handles_are_recovered(raw_game_decompiler, monkeypatch):
    il, dec = raw_game_decompiler
    mi, method, _ = find_method(il, 'RGame.ScriptableCoreKit.TypeRegistry',
                               'EnsureInitialized', 0)
    insns, _ = dec._decode(method)
    hits = []
    original = calls.recover_type_handle_call

    def observe(runtime, call, callee, value, block=None):
        result = original(runtime, call, callee, value, block=block)
        if result is not None:
            assert block.insns[0].ip <= value._type_handle[0] <= call.ip
            assert any(ins is call for ins in block.insns)
        if result is not None:
            hits.append((call.ip, callee, value._type_handle, result))
        return result

    monkeypatch.setattr(calls, 'recover_type_handle_call', observe)
    body = lift_text(il, dec, mi)
    assert hits
    wanted = 'typeof(UnityEngine.Vector2)'
    selected = [hit for hit in hits if hit[3] == wanted]
    assert selected
    for at, callee, (start, slot, ty, text), result in selected:
        m = il.meta.methods[callee]
        assert m.name == 'GetTypeFromHandle' and m.is_static
        assert il.meta.images[m.image].name == 'mscorlib.dll'
        native = [ins for ins in insns if start <= ins.ip <= at]
        assert native[0].mnemonic == Mnemonic.MOV
        assert native[0].op0_register == Register.RCX
        assert native[0].memory_base == Register.RIP
        assert native[0].ip_rel_memory_address == slot
        assert native[-1].mnemonic == Mnemonic.CALL
        assert native[-1].near_branch_target == m.addr
        assert all(ins.mnemonic == Mnemonic.XOR
                   and ins.op0_register == ins.op1_register == Register.EDX
                   for ins in native[1:-1])
        usage = il.decode_slot(slot)
        assert usage['kind'] == 2 and usage['type'] == ty
        assert usage['text'] == text == result == wanted
    assert re.search(r'(?:System\.)?Type \w+ = typeof\(UnityEngine.Vector2\);', body)
    assert 'GetTypeFromHandle(typeof(UnityEngine.Vector2))' not in body
    # A class pointer plus 0x20 is a separate, currently unproved path.
    assert 'GetTypeFromHandle((typeof(int) + 0x20))' in body
