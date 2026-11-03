"""Consumer casts leave native call identities, stores and statement order alone."""
import collections
import re

import pytest
from iced_x86 import MemorySizeExt, Mnemonic, OpKind, Register, RegisterExt

from game_support import find_type, lift_text
from il2cpp.lifter import values

pytestmark = pytest.mark.game('unitask')


def _native_reference_homes(il, block, consumer):
    """Independent forward reaching-value check, not the production backward walk."""
    volatile = (Register.RAX, Register.RCX, Register.RDX, Register.R8,
                Register.R9, Register.R10, Register.R11)
    regs = {}
    homes = {}
    for ins in block.insns:
        if ins is consumer:
            return homes
        if ins.segment_prefix != Register.NONE:
            regs.clear()
            homes.clear()
            continue
        if ins.mnemonic == Mnemonic.CALL:
            for reg in volatile:
                regs.pop(reg, None)
            homes.clear()  # every call can write its own incoming home area
            if ins.op0_kind != OpKind.NEAR_BRANCH64:
                continue
            candidates = il.addr_candidates.get(ins.near_branch_target, ())
            if len(candidates) != 1 or candidates[0][0] != 'method':
                continue
            method = il.meta.methods[candidates[0][1]]
            ty = il.types[method.return_type]
            if method.addr == ins.near_branch_target and il._type_enum(ty) == 0x12 \
                    and not ty[1] & (1 << 29):
                regs[Register.RAX] = (ty, ins.ip)
            continue
        if ins.mnemonic in (Mnemonic.MOV, Mnemonic.LEA, Mnemonic.XOR) \
                and ins.op0_kind == OpKind.REGISTER \
                and RegisterExt.is_gpr(ins.op0_register):
            dst = RegisterExt.full_register(ins.op0_register)
            incoming = None
            if ins.mnemonic == Mnemonic.MOV and RegisterExt.size(ins.op0_register) == 8 \
                    and ins.op1_kind == OpKind.REGISTER \
                    and RegisterExt.is_gpr(ins.op1_register) \
                    and RegisterExt.size(ins.op1_register) == 8:
                incoming = regs.get(RegisterExt.full_register(ins.op1_register))
            regs.pop(dst, None)
            if incoming is not None:
                regs[dst] = incoming
            continue
        if ins.mnemonic == Mnemonic.MOV and ins.op0_kind == OpKind.MEMORY \
                and ins.memory_base == Register.RSP and ins.memory_index == Register.NONE:
            offset = ins.memory_displacement
            width = MemorySizeExt.size(ins.memory_size)
            for home in list(homes):
                if home < offset + width and offset < home + 8:
                    homes.pop(home)
            if width == 8 and ins.op1_kind == OpKind.REGISTER \
                    and RegisterExt.is_gpr(ins.op1_register) \
                    and RegisterExt.size(ins.op1_register) == 8:
                incoming = regs.get(RegisterExt.full_register(ins.op1_register))
                if incoming is not None:
                    homes[offset] = incoming
            continue
        regs.clear()
        homes.clear()
    raise AssertionError('consumer is not in this native CFG block')


def test_playerloop_reference_homes_have_exact_native_return_types_without_capture(
        raw_game_decompiler, monkeypatch):
    il, dec = raw_game_decompiler
    td = find_type(il, 'Cysharp.Threading.Tasks.PlayerLoopHelper')
    methods = [il.meta.methods[i]
               for i in range(td.method_start, td.method_start + td.method_count)
               if il.meta.methods[i].name == 'Initialize']
    assert len(methods) == 1
    original = values.recover_stack_references
    with monkeypatch.context() as patch:
        patch.setattr(values, 'recover_stack_references', lambda lift, method, rty, args: args)
        before = lift_text(il, dec, methods[0].index)
    hits = []

    def observe(lift, method, rty, args):
        before_args = list(args)
        hints = dict(lift._type_hints)
        types = dict(lift.slot_types)
        vars = dict(lift._var_types)
        block = getattr(lift.out, 'block', None)
        statements = tuple(block.stmts) if block is not None else ()
        result = original(lift, method, rty, args)
        assert args == before_args
        assert lift._type_hints == hints and lift.slot_types == types and lift._var_types == vars
        assert (tuple(block.stmts) if block is not None else ()) == statements
        if not lift.dry and result is not args:
            call = next(ins for ins in block.insns if ins.ip == lift._cur_ip)
            native = _native_reference_homes(il, block, call)
            assert method.name == 'InsertLoop'
            assert il.addr_candidates[call.near_branch_target] == [('method', method.index)]
            for pos, (old, new) in enumerate(zip(args, result)):
                if old == new:
                    continue
                assert pos in (6, 7)
                param = il.meta.method_params(method)[pos]
                pt = il.types[param.type]
                offset = 0x20 + 8 * (pos - 4)
                proven, origin = native[offset]
                assert proven == pt and origin < call.ip
                assert new == '((%s)%s)' % (il.type_name(pt), old)
                name = lift.stack_map[lift.rsp_delta + offset]
                assert old == name and lift.stack_values[name].ty == pt
                hits.append(pos)
        return result

    monkeypatch.setattr(values, 'recover_stack_references', observe)
    after = lift_text(il, dec, methods[0].index)
    assert collections.Counter(hits) == {6: 16, 7: 16}
    cast = re.compile(r'\(\(System\.Type\)([A-Za-z_]\w*)\)')
    assert len(cast.findall(after)) == 32
    assert cast.sub(r'\1', after) == before
    assert after.count('System.Type.GetTypeFromHandle(') == before.count('System.Type.GetTypeFromHandle(')
