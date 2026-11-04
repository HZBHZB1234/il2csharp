"""Direct-zero interface scans need the same receiver and complete def-use proof."""
import pytest
from iced_x86 import Mnemonic, OpKind, Register as R, RegisterExt, MemorySizeExt

from game_support import lift_text
from il2cpp.dec import ifaceprune

pytestmark = pytest.mark.game('unitask')


@pytest.mark.parametrize('mi', [22264, 22780, 22781])
def test_exact_local_zero_scan_has_one_resolve_path(raw_game_decompiler, monkeypatch, mi):
    il, dec = raw_game_decompiler
    method = il.meta.methods[mi]
    assert method.name in ('AwakeAsync', 'OnWillRenderObjectAsync')
    original = ifaceprune._slot_zero_lea_fold
    proofs = []

    def observe(blocks, pb, bm, call_index, region, hits, result):
        answer = original(blocks, pb, bm, call_index, region, hits, result)
        e = [i for i in pb.insns if i.mnemonic != Mnemonic.NOP]
        if answer and len(e) == 6 and e[1].mnemonic == Mnemonic.XOR:
            # Independently read the original native entry, not lifted text.
            klass, zero, iface, count, compare, branch = e
            assert klass.mnemonic == Mnemonic.MOV and klass.op0_kind == OpKind.REGISTER
            assert klass.op1_kind == OpKind.MEMORY and klass.memory_index == R.NONE
            assert klass.memory_displacement == 0 and MemorySizeExt.size(klass.memory_size) == 8
            assert zero.op0_register == zero.op1_register
            assert RegisterExt.is_gpr32(zero.op0_register)
            assert iface.mnemonic == Mnemonic.MOV and iface.memory_base == R.RIP
            assert iface.memory_index == R.NONE and MemorySizeExt.size(iface.memory_size) == 8
            assert count.mnemonic == Mnemonic.MOVZX and count.memory_base == klass.op0_register
            assert count.memory_index == R.NONE and count.memory_displacement == 0x12e
            assert MemorySizeExt.size(count.memory_size) == 2
            assert compare.mnemonic == Mnemonic.CMP and branch.mnemonic == Mnemonic.JAE
            assert RegisterExt.full_register(compare.op0_register) == RegisterExt.full_register(zero.op0_register)
            assert RegisterExt.full_register(compare.op1_register) == RegisterExt.full_register(count.op0_register)
            miss = [i for i in bm.insns if i.mnemonic != Mnemonic.NOP]
            assert len(miss) == 4 and miss[-1] == bm.insns[call_index]
            assert miss[0].mnemonic == Mnemonic.XOR and miss[0].op0_register == miss[0].op1_register == R.R8D
            assert miss[1].op0_register == R.RDX and miss[1].op1_register == iface.op0_register
            assert miss[2].op0_register == R.RCX and miss[2].op1_register == klass.memory_base
            assert miss[3].mnemonic == Mnemonic.CALL and miss[3].op0_kind == OpKind.NEAR_BRANCH64
            assert len(region) == 4 and len(hits) == 1 and result == R.RAX
            proofs.append(pb.bid)
        return answer

    monkeypatch.setattr(ifaceprune, '_slot_zero_lea_fold', observe)
    candidate = lift_text(il, dec, mi)
    assert len(proofs) == 1
    assert candidate.count('il2cpp_interface_get_method(') == 1
    assert '+ 0x12e' not in candidate and '+ 0xb0' not in candidate
    assert '.vtable[' not in candidate and 'for (' not in candidate
    # sret interface invocation is a separate unresolved proof; keep it honest.
    assert candidate.count('/*indirect*/') == 1 and 'return __ret;' in candidate

    def classic_only(blocks, pb, *args):
        e = [i for i in pb.insns if i.mnemonic != Mnemonic.NOP]
        if len(e) == 6 and e[1].mnemonic == Mnemonic.XOR and e[2].mnemonic == Mnemonic.MOV:
            return False
        return original(blocks, pb, *args)

    monkeypatch.setattr(ifaceprune, '_slot_zero_lea_fold', classic_only)
    baseline = lift_text(il, dec, mi)
    assert '+ 0x12e' in baseline and '+ 0xb0' in baseline and '.vtable[' in baseline
    assert baseline.count('/*indirect*/') == candidate.count('/*indirect*/')
    assert baseline.count('new Cysharp.Threading.Tasks.Triggers.AsyncTriggerHandler<') == candidate.count('new Cysharp.Threading.Tasks.Triggers.AsyncTriggerHandler<') == 1
