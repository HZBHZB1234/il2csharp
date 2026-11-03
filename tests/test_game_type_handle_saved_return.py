"""Prove the extra return-save shape without weakening metadata/CFG identity."""
import re

import pytest
from iced_x86 import MemorySizeExt, Mnemonic, OpKind, Register

from game_support import find_method, lift_text
from il2cpp.lifter import calls

pytestmark = pytest.mark.game('unitask')


def test_saved_previous_return_allows_only_same_block_type_handle_setup(
        raw_game_decompiler, monkeypatch):
    il, dec = raw_game_decompiler
    mi, method, _ = find_method(il, 'Cysharp.Threading.Tasks.PlayerLoopHelper',
                               'Initialize', 2)
    insns, _ = dec._decode(method)
    original = calls.recover_type_handle_call
    hits = {}

    def observe(runtime, call, callee, value, block=None):
        before = None if value is None else (value.text, value.ty, value.kind,
                                             value._type_handle, value._unk)
        result = original(runtime, call, callee, value, block=block)
        if result is not None:
            start, slot, ty, text = value._type_handle
            # Independent actual-method decoding, not the production re-decode.
            native = [ins for ins in insns if start <= ins.ip <= call.ip]
            if len(native) == 4:
                load, zero, save, consumer = native
                assert consumer.ip == call.ip
                assert all(a.next_ip == b.ip for a, b in zip(native, native[1:]))
                assert [x.ip for x in block.insns if start <= x.ip <= call.ip] == [
                    x.ip for x in native]
                assert load.mnemonic == Mnemonic.MOV
                assert load.op0_kind == OpKind.REGISTER
                assert load.op0_register == Register.RCX
                assert load.op1_kind == OpKind.MEMORY
                assert load.memory_base == Register.RIP
                assert load.memory_index == load.segment_prefix == Register.NONE
                assert MemorySizeExt.size(load.memory_size) == 8
                assert load.ip_rel_memory_address == slot
                assert zero.mnemonic == Mnemonic.XOR
                assert zero.op0_register == zero.op1_register == Register.EDX
                assert save.mnemonic == Mnemonic.MOV
                assert save.op0_kind == save.op1_kind == OpKind.REGISTER
                assert save.op1_register == Register.RAX
                assert save.op0_register in (Register.RBX, Register.RBP, Register.RSI,
                                             Register.RDI, Register.R12, Register.R13,
                                             Register.R14, Register.R15)
                assert save.segment_prefix == Register.NONE
                assert consumer.mnemonic == Mnemonic.CALL
                assert consumer.op0_kind == OpKind.NEAR_BRANCH64
                target = consumer.near_branch_target
                assert tuple(il.addr_candidates[target]) == (('method', callee),)
                callee_method = il.meta.methods[callee]
                assert callee_method.addr == target
                assert callee_method.is_static
                assert callee_method.name == 'GetTypeFromHandle'
                assert il.meta.images[callee_method.image].name == 'mscorlib.dll'
                usage = il.decode_slot(slot)
                assert usage['kind'] == 2 and usage['type'] == ty
                assert usage['text'] == text == result
                hits[call.ip] = result
        assert before == (None if value is None else (
            value.text, value.ty, value.kind, value._type_handle, value._unk))
        return result

    monkeypatch.setattr(calls, 'recover_type_handle_call', observe)
    candidate = lift_text(il, dec, mi)
    assert len(hits) == len(set(hits.values())) == 32

    def previous(runtime, call, callee, value, block=None):
        if call.ip in hits:
            return None
        return original(runtime, call, callee, value, block=block)

    monkeypatch.setattr(calls, 'recover_type_handle_call', previous)
    baseline = lift_text(il, dec, mi)
    expected = baseline
    renames = {}
    for text in hits.values():
        old_rhs = 'System.Type.GetTypeFromHandle(' + text + ')'
        assert expected.count(old_rhs) == 1
        old_var = re.search(r'(\w+) = ' + re.escape(old_rhs) + ';', baseline).group(1)
        new_var = re.search(r'(\w+) = ' + re.escape(text) + ';', candidate).group(1)
        assert renames.setdefault(new_var, old_var) == old_var
        expected = expected.replace(old_rhs, text)
    assert len(renames) == len(set(renames.values())) == 2
    restored = candidate
    for new, old in renames.items():
        definitions = re.findall(r'\b' + re.escape(new) + r' = ([^;]+);', candidate)
        assert len(definitions) == 16
        assert all(rhs in hits.values() for rhs in definitions)
        restored, count = re.subn(r'\bSystem\.Type ' + re.escape(new) + r' =',
                                  'object ' + new + ' =', restored)
        assert count == 1
        restored = re.sub(r'\b' + re.escape(new) + r'\b', old, restored)
    # Only 32 proven wrappers plus two exact home retypes/renames may change.
    # This also checks all remaining statements and their order byte-for-byte.
    assert restored == expected
    assert candidate.count('System.Type.GetTypeFromHandle(') == baseline.count(
        'System.Type.GetTypeFromHandle(') - 32
    # A separately executed, cross-block handle consumer must stay unrecovered.
    assert 'System.Type.GetTypeFromHandle(typeof(' in candidate
