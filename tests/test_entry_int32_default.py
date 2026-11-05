"""Default activation is bounded, transactional and lazy; no game snapshots."""
import builtins
import copy
from types import SimpleNamespace as NS

import pytest
from iced_x86 import Decoder

from il2cpp import Decompiler
from il2cpp.dec import entrycapture as recovery
from il2cpp.lifter.entrycapture import EntryCaptureDeclined, EntryInt32Captures
from il2cpp.runtime.types import _SYNTH_NEXT_VA
from test_entry_int32_capture import full_model, ALIAS

EXPECTED = ['int ' + ALIAS + ' = p0;',
            'float real1 = (float)(' + ALIAS + ');', 'return real1;']


def test_default_activation_uses_complete_pipeline_without_a_switch():
    dec, method, owner = full_model()
    assert not hasattr(dec, '_entry_int32_recovery')
    refs = dec.L, dec.L.il, dec.L.meta, dec.L.bin
    counter = _SYNTH_NEXT_VA[0]
    for _ in range(2):
        assert dec.lift_method(method, owner) == EXPECTED
        assert dec._entry_int32_status == 'accepted'
        assert (dec.L, dec.L.il, dec.L.meta, dec.L.bin) == refs
        assert dec.L._entry_int32_capture is None
        assert _SYNTH_NEXT_VA[0] == counter
    # The completed live state still belongs to the disabled baseline.
    dec._entry_int32_recovery = False
    assert dec.lift_method(method, owner) == ['return p0;']
    assert dec._entry_int32_status == 'disabled'
    del dec._entry_int32_recovery
    assert dec.lift_method(method, owner) == EXPECTED


@pytest.mark.parametrize('stage', ['preflight', 'clone', 'binding', 'cleanup'])
def test_default_failures_return_exact_baseline_and_do_not_poison_next_attempt(monkeypatch, stage):
    dec, method, owner = full_model()
    original = Decompiler._lift_method
    baselines = []

    def record(self, m, td):
        result = original(self, m, td)
        if self is dec:
            baselines.append(result)
        return result

    def reject(*args, **kwargs):
        raise EntryCaptureDeclined('authored failure')

    monkeypatch.setattr(Decompiler, '_lift_method', record)
    target, name = {
        'preflight': (recovery, '_candidate'),
        'clone': (recovery, 'isolated_clone'),
        'binding': (EntryInt32Captures, 'bind_entry'),
        'cleanup': (EntryInt32Captures, 'finalize'),
    }[stage]
    before = _SYNTH_NEXT_VA[0]
    with monkeypatch.context() as patch:
        patch.setattr(target, name, reject)
        assert dec.lift_method(method, owner) is baselines[-1]
        assert baselines[-1] == ['return p0;']
        assert dec.L._entry_int32_capture is None
        assert _SYNTH_NEXT_VA[0] == before
    assert dec.lift_method(method, owner) == EXPECTED


@pytest.mark.parametrize('shape', ['disabled', 'comments', 'eh', 'method',
                                  'empty', 'missing', 'cap', 'no-conversion'])
def test_non_candidate_filters_do_not_import_recovery_or_allocate_cache(monkeypatch, shape):
    dec, method, owner = full_model()
    dec._entry_int32_status = 'accepted'  # status from a previous method
    sentinel = ['authored baseline']
    dec._flat_insns = list(Decoder(64, bytes.fromhex('660f6ec10f5bc0c3'), ip=method.addr))
    dec.L._current_method = method
    if shape == 'disabled':
        dec._entry_int32_recovery = False
    elif shape == 'comments':
        dec.L.asm_comments = True
    elif shape == 'eh':
        dec.eh = [object()]
    elif shape == 'method':
        dec.L._current_method = copy.copy(method)
    elif shape == 'empty':
        dec._flat_insns = []
    elif shape == 'missing':
        del dec._flat_insns
    elif shape == 'cap':
        dec._flat_insns *= 172  # 516 > the unchanged 512 cap
    else:
        dec._flat_insns = list(Decoder(64, b'\xc3', ip=method.addr))
    monkeypatch.setattr(Decompiler, '_lift_method', lambda *args: sentinel)
    importer = builtins.__import__

    def no_recovery(name, *args, **kwargs):
        if name == 'il2cpp.dec.entrycapture':
            pytest.fail('cheap non-candidate imported recovery')
        return importer(name, *args, **kwargs)

    monkeypatch.setattr(builtins, '__import__', no_recovery)
    assert dec.lift_method(method, owner) is sentinel
    assert dec._entry_int32_status == ('disabled' if shape == 'disabled' else 'not-candidate')
    assert not hasattr(dec, '_entry_int32_unwind')


@pytest.mark.parametrize('change', ['owner', 'mutable-native', 'shared', 'generic',
                                   'missing-unwind', 'callback', 'metadata'])
def test_default_activation_does_not_bypass_old_native_or_arena_guards(change):
    dec, method, owner = full_model()
    if change == 'owner':
        dec.L.il.addr_candidates[method.addr] = [('method', method.index + 1)]
    elif change == 'mutable-native':
        dec.L.bin.d = bytearray(dec.L.bin.d)
    elif change == 'shared':
        dec.L.il.addr_candidates[method.addr].append(('method', method.index + 1))
    elif change == 'generic':
        method.generic_container = 0
    elif change == 'missing-unwind':
        data = bytearray(dec.L.bin.d)
        data[0xe0:0xe8] = b'\0' * 8
        dec.L.bin.d = bytes(data)
    elif change == 'callback':
        dec.extra = lambda: dec.L
    else:
        dec.L.meta.d = bytearray(dec.L.meta.d)
    dec._entry_int32_recovery = False
    baseline = dec.lift_method(method, owner)
    del dec._entry_int32_recovery
    assert dec.lift_method(method, owner) == baseline
    assert dec._entry_int32_status != 'accepted'
    assert dec.L._entry_int32_capture is None


def test_default_activation_leaves_simd_upper_lanes_and_entry_expr_unmodified():
    dec, method, owner = full_model()
    dec._entry_int32_recovery = False
    baseline = dec.lift_method(method, owner)
    # Use an independent disabled lift to describe the required live continuation.
    first_regs = {k: (v.text, v.ty, v.kind) for k, v in dict.items(dec.L.regs)}
    del dec._entry_int32_recovery
    assert dec.lift_method(method, owner) == EXPECTED
    assert {k: (v.text, v.ty, v.kind) for k, v in dict.items(dec.L.regs)} == first_regs
    dec._entry_int32_recovery = False
    assert dec.lift_method(method, owner) == baseline
