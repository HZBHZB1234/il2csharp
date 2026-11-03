"""A Type[] SSA merge retains native pointer-wide element reads."""
import re

import pytest
from iced_x86 import MemorySizeExt, Mnemonic

from game_support import find_method, lift_text
from il2cpp import Lifter

pytestmark = pytest.mark.game('unitask')


def test_cleanup_stack_trace_reads_a_reference_array_element(raw_game_decompiler, monkeypatch):
    il, dec = raw_game_decompiler
    mi, _, _ = find_method(il, 'DiagnosticsExtensions', 'CleanupAsyncStackTrace')
    sites = []
    original = Lifter._typed_phi_reference_array_load

    def observe(self, ins, base, index, size):
        out = original(self, ins, base, index, size)
        if out is not None and not self.dry:
            sites.append((ins.mnemonic, MemorySizeExt.size(ins.memory_size),
                          ins.memory_index_scale, ins.memory_displacement,
                          base.kind, self.il._type_enum(base.ty),
                          self.il._type_enum(out.ty)))
        return out

    with monkeypatch.context() as patch:
        patch.setattr(Lifter, '_typed_phi_reference_array_load', observe)
        after = lift_text(il, dec, mi)
    assert re.search(r'BeautifyType\(\w+\[\w+\], true\)', after)
    assert sites == [(Mnemonic.MOV, 8, 8, 0x20, 'obj', 0x1d, 0x12)]
    with monkeypatch.context() as patch:
        patch.setattr(Lifter, '_typed_phi_reference_array_load', lambda *args: None)
        before = lift_text(il, dec, mi)
    assert not re.search(r'BeautifyType\(\w+\[\w+\], true\)', before)
    # The probe compares the same MethodDef on both paths, not a stored body.
    assert len(before.splitlines()) == len(after.splitlines())
    assert sum(a != b for a, b in zip(before.splitlines(), after.splitlines())) == 1
