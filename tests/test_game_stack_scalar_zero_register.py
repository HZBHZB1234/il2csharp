"""Independent native/ABI proof and exact text delta for false byte homes."""
import difflib

import pytest
from iced_x86 import MemorySizeExt, Mnemonic, OpKind, Register as R, RegisterExt

from game_support import lift_text
from il2cpp.lifter import stackscalars, values


PRESERVED = (R.RBX, R.RBP, R.RSI, R.RDI, R.R12, R.R13, R.R14, R.R15)


def _forward_homes(il, native, consumer):
    # Independent forward dataflow, not the production backward search.
    zeros, homes = {}, {}
    following = None
    for ins in native:
        if ins.ip == consumer.ip:
            return homes
        if following is not None and ins.ip != following:
            zeros.clear(); homes.clear()
        following = ins.next_ip
        if ins.segment_prefix != R.NONE:
            zeros.clear(); homes.clear(); continue
        if ins.mnemonic == Mnemonic.CALL:
            homes.clear()
            candidates = (il.addr_candidates.get(ins.near_branch_target, ())
                          if ins.op0_kind == OpKind.NEAR_BRANCH64 else ())
            if len(candidates) != 1 or candidates[0][0] != 'method':
                zeros.clear(); continue
            mi = candidates[0][1]
            assert 0 <= mi < len(il.meta.methods)
            method = il.meta.methods[mi]
            assert method.index == mi and method.addr == ins.near_branch_target
            assert method.generic_container == -1
            owner = il.meta.typedefs[method.declaring]
            assert owner.generic_container == owner.declaring == -1
            assert not owner.is_valuetype
            zeros = {reg: at for reg, at in zeros.items() if reg in PRESERVED}
            continue
        if ins.mnemonic == Mnemonic.XOR and ins.op_count == 2 \
                and ins.op0_kind == ins.op1_kind == OpKind.REGISTER \
                and ins.op0_register == ins.op1_register \
                and RegisterExt.is_gpr(ins.op0_register):
            reg = RegisterExt.full_register(ins.op0_register)
            if reg == R.RSP:
                zeros.clear(); homes.clear(); continue
            zeros.pop(reg, None)
            if RegisterExt.size(ins.op0_register) in (4, 8):
                zeros[reg] = ins.ip
            continue
        if ins.mnemonic in (Mnemonic.MOV, Mnemonic.LEA) and ins.op_count == 2 \
                and ins.op0_kind == OpKind.REGISTER and RegisterExt.is_gpr(ins.op0_register):
            reg = RegisterExt.full_register(ins.op0_register)
            if reg == R.RSP:
                zeros.clear(); homes.clear(); continue
            zeros.pop(reg, None)
            continue
        if ins.mnemonic == Mnemonic.MOV and ins.op_count == 2 \
                and ins.op0_kind == OpKind.MEMORY \
                and ins.memory_base == R.RSP and ins.memory_index == R.NONE:
            offset = ins.memory_displacement
            width = MemorySizeExt.size(ins.memory_size)
            homes = {off: proof for off, proof in homes.items()
                     if not offset < off + 1 or not off < offset + width}
            if width == 1 and ins.op1_kind == OpKind.REGISTER \
                    and RegisterExt.is_gpr(ins.op1_register) \
                    and RegisterExt.full_register(ins.op1_register) in zeros:
                assert RegisterExt.size(ins.op1_register) == 1
                homes[offset] = (zeros[RegisterExt.full_register(ins.op1_register)], ins.ip)
            continue
        zeros.clear(); homes.clear()
    return {}


@pytest.mark.parametrize('fixture_id,method_rows,expected', [
    pytest.param('unitask', [20033], 8, marks=pytest.mark.game('unitask')),
    pytest.param('survivors-roguelike-kit', [70818, 70976], 2,
                 marks=pytest.mark.game('survivors-roguelike-kit')),
])
def test_zero_register_false_arguments_have_native_and_exact_source_evidence(
        fixture_id, method_rows, expected, raw_game_decompiler, monkeypatch):
    il, dec = raw_game_decompiler
    original = values.recover_stack_scalars
    hits = {}
    current = None
    decoded = {}
    for mi in method_rows:
        decoded[mi], _ = dec._decode(il.meta.methods[mi])

    def observe(lift, method, rty, args):
        previous = list(args)
        hints, slots, types = dict(lift._type_hints), dict(lift.slot_types), dict(lift._var_types)
        exprs = {name: (expr.text, expr.ty, expr.kind, expr._unk)
                 for name, expr in lift.stack_values.items()}
        result = original(lift, method, rty, args)
        with monkeypatch.context() as patch:
            patch.setattr(stackscalars, '_zero_register_bool_home', lambda *a: False)
            old = original(lift, method, rty, args)
        assert args == previous and hints == lift._type_hints
        assert slots == lift.slot_types and types == lift._var_types
        assert exprs == {name: (expr.text, expr.ty, expr.kind, expr._unk)
                         for name, expr in lift.stack_values.items()}
        if not lift.dry:
            block = lift.out.block
            call = next(ins for ins in block.insns if ins.ip == lift._cur_ip)
            native = [ins for ins in decoded[current]
                      if block.insns[0].ip <= ins.ip <= call.ip]
            assert [ins.ip for ins in native] == [ins.ip for ins in block.insns
                                                if ins.ip <= call.ip]
            for pos, (before, after) in enumerate(zip(old, result)):
                if before == after:
                    continue
                assert before == '0' and after == 'false' and pos >= 4
                assert call.mnemonic == Mnemonic.CALL and call.op0_kind == OpKind.NEAR_BRANCH64
                assert method.addr == call.near_branch_target
                assert il.addr_candidates[method.addr] == [('method', method.index)]
                param = il.meta.method_params(method)[pos - (0 if method.is_static else 1)]
                assert il._type_enum(il.types[param.type]) == 0x02
                assert not il.types[param.type][1] & (1 << 29)
                zero, store = _forward_homes(il, native, call)[0x20 + 8 * (pos - 4)]
                assert zero < store < call.ip
                hits[current, call.ip, pos] = zero, store
        return result

    monkeypatch.setattr(values, 'recover_stack_scalars', observe)
    candidates = {}
    for current in method_rows:
        candidates[current] = lift_text(il, dec, current)
    assert len(hits) == expected
    monkeypatch.setattr(values, 'recover_stack_scalars', original)
    monkeypatch.setattr(stackscalars, '_zero_register_bool_home', lambda *a: False)
    changed = 0
    for current in method_rows:
        baseline = lift_text(il, dec, current)
        before, after = baseline.splitlines(), candidates[current].splitlines()
        assert len(before) == len(after)
        for a, b in zip(before, after):
            if a == b:
                continue
            edits = [op for op in difflib.SequenceMatcher(None, a, b, autojunk=False).get_opcodes()
                     if op[0] != 'equal']
            assert len(edits) == 1
            _, i, j, k, n = edits[0]
            assert a[i:j] == '0' and b[k:n] == 'false'
            changed += 1
    assert changed == expected
