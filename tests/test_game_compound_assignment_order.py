"""The list's pre-increment size stays captured before the size update."""
import re

import pytest
from iced_x86 import Mnemonic, Register

from game_support import find_method, lift_text
from il2cpp import Decompiler

pytestmark = pytest.mark.game('survivors-roguelike-kit')


def test_registry_list_index_keeps_the_old_size(raw_game_decompiler, monkeypatch):
    il, dec = raw_game_decompiler
    mi, method, _ = find_method(il, 'RGame.ScriptableCoreKit.TypeRegistry',
                               'EnsureInitialized', 0)
    insns, _ = dec._decode(method)
    old_reads = [i for i, ins in enumerate(insns)
                 if ins.mnemonic == Mnemonic.MOVSXD
                 and ins.op0_register == Register.RDX
                 and ins.memory_base == Register.RDI
                 and ins.memory_displacement == 0x18]
    assert len(old_reads) == 1
    at = old_reads[0]
    # Compare native dataflow, not a stored method body or absolute address.
    updates = [i for i in range(at + 1, len(insns))
               if insns[i].mnemonic == Mnemonic.MOV
               and insns[i].memory_base == Register.RDI
               and insns[i].memory_displacement == 0x18
               and insns[i].op1_register == Register.EAX]
    assert updates
    update = updates[0]
    assert any(ins.mnemonic == Mnemonic.LEA and ins.op0_register == Register.EAX
               and ins.memory_base == Register.RDX and ins.memory_displacement == 1
               for ins in insns[at + 1:update])
    element_addresses = [i for i in range(update + 1, len(insns))
                         if insns[i].mnemonic == Mnemonic.LEA
                         and insns[i].op0_register == Register.RCX
                         and insns[i].memory_base == Register.RCX
                         and insns[i].memory_index == Register.RDX
                         and insns[i].memory_index_scale == 8]
    assert element_addresses
    address = element_addresses[0]
    assert insns[address + 1].mnemonic == Mnemonic.ADD
    assert insns[address + 1].op0_register == Register.RCX
    assert insns[address + 1].immediate(1) == 0x20
    assert insns[address + 2].mnemonic == Mnemonic.MOV
    assert insns[address + 2].memory_base == Register.RCX
    between = insns[update + 1:address]
    assert [ins.mnemonic for ins in between] == [Mnemonic.CMP, Mnemonic.JAE]
    assert between[0].op0_register == Register.EDX
    assert between[0].memory_base == Register.RCX
    assert between[0].memory_displacement == 0x18

    text = lift_text(il, dec, mi)
    snapshot = re.search(r'int (num\d+) = (\w+)\._size;', text)
    assert snapshot
    index, owner = snapshot.groups()
    write = re.search(r'(?m)^\s*' + re.escape(owner) + r'\._size = num\d+;', text)
    assert write and snapshot.end() < write.start()
    assert re.search(re.escape(owner) + r'\._items\[' + re.escape(index) + r'\] = ', text)
    assert not re.search(re.escape(owner) + r'\._size \+=', text)
    with monkeypatch.context() as patch:
        patch.setattr(Decompiler, '_compound_assign', lambda self, lines: lines)
        unfolded = lift_text(il, dec, mi)
    assert snapshot.group(0) in unfolded
