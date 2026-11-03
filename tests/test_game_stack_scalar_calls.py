"""Real stack immediates recover scalars without typing reused frame homes."""
import collections

import pytest
from iced_x86 import MemorySizeExt, Mnemonic, OpKind, Register

from game_support import find_type, lift_text
from il2cpp.lifter import values
from il2cpp.runtime.meta import IMM_OPS

pytestmark = pytest.mark.game('unitask')


def test_playerloop_stack_immediates_have_exact_native_and_abi_evidence(
        raw_game_decompiler, monkeypatch):
    il, dec = raw_game_decompiler
    td = find_type(il, 'Cysharp.Threading.Tasks.PlayerLoopHelper')
    methods = [il.meta.methods[i]
               for i in range(td.method_start, td.method_start + td.method_count)
               if il.meta.methods[i].name == 'Initialize']
    assert len(methods) == 1
    hits = []
    declined = []
    original = values.recover_stack_scalars

    def observe(lift, method, rty, args):
        before_hints = dict(lift._type_hints)
        before_types = dict(lift.slot_types)
        result = original(lift, method, rty, args)
        assert lift._type_hints == before_hints and lift.slot_types == before_types
        if not lift.dry and method.name == 'InsertLoop':
            block = lift.out.block
            call = next(ins for ins in block.insns if ins.ip == lift._cur_ip)
            assert call.mnemonic == Mnemonic.CALL
            assert call.op0_kind == OpKind.NEAR_BRANCH64
            assert call.near_branch_target == method.addr
            assert il.addr_candidates[method.addr] == [('method', method.index)]
            for position in (5, 8):
                if result[position] == args[position]:
                    declined.append((position, args[position]))
                    continue
                offset = 0x20 + 8 * (position - 4)
                width = 1 if position == 5 else 4
                stores = [ins for ins in block.insns if ins.ip < call.ip
                          and ins.mnemonic == Mnemonic.MOV
                          and ins.op0_kind == OpKind.MEMORY
                          and ins.memory_base == Register.RSP
                          and ins.memory_index == Register.NONE
                          and ins.memory_displacement == offset
                          and MemorySizeExt.size(ins.memory_size) == width]
                assert stores
                store = stores[-1]
                assert store.op1_kind in IMM_OPS
                assert store.immediate(1) == int(args[position])
                assert all(ins.mnemonic in (Mnemonic.MOV, Mnemonic.LEA)
                           for ins in block.insns if store.ip < ins.ip < call.ip)
                param = il.meta.method_params(method)[position]
                pt = il.types[param.type]
                if position == 5:
                    assert il._type_enum(pt) == 0x02
                    assert result[position] == 'true'
                else:
                    assert il.meta.typedefs[pt[0]].is_enum
                    assert result[position] == il.type_name(pt) + '.' + il.enum_members(pt[0])[int(args[position])]
                hits.append((position, result[position]))
        return result

    monkeypatch.setattr(values, 'recover_stack_scalars', observe)
    body = lift_text(il, dec, methods[0].index)
    assert collections.Counter(pos for pos, _ in hits) == {5: 8, 8: 15}
    # Register-derived zeros are deliberately not blessed by this immediate-only proof.
    assert collections.Counter(declined) == {(5, '0'): 8, (8, '0'): 1}
    assert 'PlayerLoopTiming.LastInitialization' in body
    assert 'PlayerLoopTiming.LastTimeUpdate' in body
