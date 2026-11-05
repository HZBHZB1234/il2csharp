"""Authored cache lifecycle and arena tests, never licensed native data."""
import copy
import struct
from types import SimpleNamespace as NS

import pytest

from il2cpp.dec.entrycapture import (
    ArenaDeclined, _candidate, _mutable_graph, _unwind_cache, isolated_clone,
)
from il2cpp.lifter.entryorigin import EntryInt32Origin
from il2cpp.lifter.unwindproof import NativeUnwindBoundary, NativeUnwindCache
from test_entry_int32_capture import model
from test_entry_int32_origin import setup
from test_native_unwind_boundary import BASE, CHILD, ROOT, chain, image, instructions


def put(binary, offset, raw):
    data = bytearray(binary.d)
    data[offset:offset + len(raw)] = raw
    binary.d = bytes(data)


def mutate(binary, field):
    if field == 'handler':
        put(binary, 0x800, b'\x09')
    elif field == 'directory':
        put(binary, 0xe0, struct.pack('<II', 0, 0))
    elif field == 'text':
        put(binary, 0x200, b'\xc3')
    elif field == 'machine':
        put(binary, 0x44, struct.pack('<H', 0xaa64))
    elif field == 'is64':
        binary.is64 = False
    elif field == 'base':
        binary.image_base += 0x100000
    elif field == 'exec':
        binary.sections[0].chars = 0x40000040
    elif field == 'size':
        binary.sections[0].size = 0
    elif field == 'offset':
        binary.sections[0].offset = len(binary.d)
    elif field == 'rawsize':
        binary.sections[0].rawsize = 0
    elif field == 'address':
        binary.sections[0].addr = BASE + 0x2000
    elif field == 'alias':
        binary.sections.append(binary.sections[0])
    elif field == 'equal-bytes':
        binary.d = bytes(bytearray(binary.d))
    else:
        raise AssertionError(field)


MUTATIONS = ('handler', 'directory', 'text', 'machine', 'is64', 'base',
             'exec', 'size', 'offset', 'rawsize', 'address', 'alias', 'equal-bytes')


def query(cache, binary, seq):
    proof = cache.snapshot(binary)
    return None if proof is None else proof.covers(seq[0].ip, seq)


@pytest.mark.parametrize('chained', [False, True])
@pytest.mark.parametrize('field', MUTATIONS)
def test_mutation_and_restoration_match_fresh_snapshots(field, chained):
    binary = (image((ROOT, CHILD), unwind={0x3000: b'\x01\0\0\0', 0x3020: chain()})
              if chained else image())
    seq = instructions(binary, size=0x20 if chained else 1)
    cache = NativeUnwindCache()
    original = copy.deepcopy(binary)
    assert query(cache, binary, seq) == NativeUnwindBoundary(binary).covers(seq[0].ip, seq)
    previous = cache._proof
    assert cache.snapshot(binary) is previous
    mutate(binary, field)
    expected = NativeUnwindBoundary(binary).covers(seq[0].ip, seq)
    for _ in range(3):
        assert query(cache, binary, seq) == expected
    assert cache._proof is not previous
    binary.__dict__ = original.__dict__
    for _ in range(3):
        assert query(cache, binary, seq) == NativeUnwindBoundary(binary).covers(seq[0].ip, seq)


@pytest.mark.parametrize('field', ['handler', 'exec', 'base'])
def test_identity_only_cache_would_reuse_a_stale_proof(field):
    binary = image()
    seq = instructions(binary)
    cache = NativeUnwindCache()
    old = cache.snapshot(binary)
    assert old.covers(seq[0].ip, seq) == (ROOT,)
    mutate(binary, field)
    assert old.covers(seq[0].ip, seq) == (ROOT,)
    assert query(cache, binary, seq) is None


def test_single_strong_owner_and_immutable_data_identity_not_equality():
    binary = image()
    other = copy.deepcopy(binary)
    assert other is not binary and other.d is binary.d
    cache = NativeUnwindCache()
    first = cache.snapshot(binary)
    second = cache.snapshot(other)
    assert second is not first and cache._owner is other
    assert cache.snapshot(binary) is not first
    previous = cache._proof
    binary.d = bytes(bytearray(binary.d))
    assert cache.snapshot(binary) is not previous
    previous = cache._proof
    binary.sections = copy.deepcopy(binary.sections)
    binary.sections[0].name = 'not-a-proof-input'
    binary.sections[0].chars |= 0x40000000  # executable mapping unchanged
    assert cache.snapshot(binary) is previous


@pytest.mark.parametrize('backing', [bytearray, memoryview, type('BytesSubclass', (bytes,), {})])
def test_mutable_and_subclass_backing_clears_even_an_existing_hit(backing):
    binary = image()
    cache = NativeUnwindCache()
    previous = cache.snapshot(binary)
    saved = binary.d
    binary.d = backing(binary.d)
    assert cache.snapshot(binary) is None
    assert all(value is None for value in vars(cache).values())
    binary.d = saved
    assert cache.snapshot(binary) is not previous


@pytest.mark.parametrize('bad', [None, object(), NS(), NS(d=b'bad', image_base=BASE)])
def test_missing_or_unsupported_binary_context_clears(bad):
    cache = NativeUnwindCache()
    cache.snapshot(image())
    assert cache.snapshot(bad) is None
    assert all(value is None for value in vars(cache).values())


@pytest.mark.parametrize('attribute', ['d', 'image_base', 'sections', 'is64'])
def test_missing_context_attribute_cannot_leave_an_old_proof_usable(attribute):
    binary = image()
    cache = NativeUnwindCache()
    previous = cache.snapshot(binary)
    saved = getattr(binary, attribute)
    delattr(binary, attribute)
    # Binary.is64 is inherited as True, unlike the parsed instance flag. If
    # deletion exposes that exact value, there has been no ABI context change.
    if attribute == 'is64':
        assert cache.snapshot(binary) is previous
    else:
        assert cache.snapshot(binary) is None and cache._proof is None
    setattr(binary, attribute, saved)
    assert cache.snapshot(binary) is not None


@pytest.mark.parametrize('attribute', ['addr', 'size', 'offset', 'rawsize'])
@pytest.mark.parametrize('bad', [None, [], 1.0, True])
def test_non_scalar_section_keys_are_not_cached(attribute, bad):
    binary = image()
    cache = NativeUnwindCache()
    cache.snapshot(binary)
    setattr(binary.sections[0], attribute, bad)
    assert cache.snapshot(binary) is None and cache._proof is None


@pytest.mark.parametrize('bad', [None, [], 1.0, True])
def test_base_must_be_an_exact_immutable_integer(bad):
    binary = image()
    cache = NativeUnwindCache()
    cache.snapshot(binary)
    binary.image_base = bad
    assert cache.snapshot(binary) is None and cache._proof is None


def test_negative_parses_and_failed_roots_are_private_and_order_independent():
    binary = image((ROOT, CHILD), unwind={0x3000: b'\x01\0\0\0', 0x3020: b'\x09\0\0\0'})
    cache = NativeUnwindCache()
    seq = instructions(binary, size=0x20)
    assert query(cache, binary, seq) is None
    proof = cache._proof
    assert query(cache, binary, seq[:1]) == (ROOT,)
    assert cache._proof is proof
    put(binary, 0xe0, struct.pack('<II', 0, 0))
    assert query(cache, binary, seq) is None
    negative = cache._proof
    assert negative is not proof and not negative._valid
    assert cache.snapshot(binary) is negative


@pytest.mark.parametrize('field', MUTATIONS)
def test_old_origin_revalidates_live_binary_even_when_its_snapshot_still_exists(field):
    original, lift, conversion = setup()
    cache = NativeUnwindCache()
    plan = EntryInt32Origin(lift.il, original.method, original.insns, unwind_cache=cache)
    assert plan.parameter_at(lift, conversion, lift.out.block.insns) == 0
    mutate(lift.bin, field)
    assert plan.parameter_at(lift, conversion, lift.out.block.insns) is None
    fresh = EntryInt32Origin(lift.il, original.method, original.insns)
    renewed = EntryInt32Origin(lift.il, original.method, original.insns, unwind_cache=cache)
    assert renewed.parameter_at(lift, conversion, lift.out.block.insns) == fresh.parameter_at(
        lift, conversion, lift.out.block.insns)


@pytest.mark.parametrize('field', ['owner', 'shared', 'metadata', 'current', 'generic', 'address'])
def test_cache_hit_does_not_substitute_for_exact_current_method_evidence(field):
    original, lift, conversion = setup()
    cache = NativeUnwindCache()
    plan = EntryInt32Origin(lift.il, original.method, original.insns, unwind_cache=cache)
    proof = cache._proof
    assert plan.parameter_at(lift, conversion, lift.out.block.insns) == 0
    if field == 'owner':
        lift.il.meta.methods[0] = copy.copy(original.method)
    elif field == 'shared':
        lift.il.addr_candidates[original.method.addr].append(('method', 1))
    elif field == 'metadata':
        lift.il.meta = copy.copy(lift.il.meta)
    elif field == 'current':
        lift._current_method = copy.copy(original.method)
    elif field == 'generic':
        original.method.generic_container = 0
    else:
        original.method.addr += 1
    assert cache.snapshot(lift.bin) is proof
    assert plan.parameter_at(lift, conversion, lift.out.block.insns) is None


@pytest.mark.parametrize('budget', [0, -1, 513, None, '512'])
def test_cache_hit_does_not_increase_the_total_native_origin_budget(budget):
    original, lift, conversion = setup()
    cache = NativeUnwindCache()
    for _ in range(2):
        plan = EntryInt32Origin(lift.il, original.method, original.insns, unwind_cache=cache)
        assert plan.parameter_at(lift, conversion, lift.out.block.insns, window=budget) is None


def test_complete_arena_copy_preserves_private_owner_proof_and_root_aliases():
    dec, method, owner = model()
    assert _candidate(dec, method)
    cache = dec._entry_int32_unwind
    proof = cache._proof
    arena, am, at = isolated_clone(dec, method, owner)
    cloned = arena._entry_int32_unwind
    assert cloned is not cache and cloned._owner is arena.L.bin
    assert cloned._data is cache._data is arena.L.bin.d
    assert cloned._proof is not proof and cloned._proof._roots is not proof._roots
    assert cloned.snapshot(arena.L.bin) is cloned._proof
    assert _mutable_graph((dec, method, owner)).keys().isdisjoint(
        _mutable_graph((arena, am, at)))
    cloned._proof._roots.clear()
    assert proof._roots
    put(arena.L.bin, 0x800, b'\x09')
    assert _candidate(arena, am) is False
    assert _candidate(dec, method) is True and cache._proof is proof


@pytest.mark.parametrize('bad', [object(), NativeUnwindBoundary(image()),
                                  type('CacheSubclass', (NativeUnwindCache,), {})()])
def test_arbitrary_proof_providers_or_cache_subclasses_are_not_admitted(bad):
    original, lift, conversion = setup()
    plan = EntryInt32Origin(lift.il, original.method, original.insns, unwind_cache=bad)
    assert plan.parameter_at(lift, conversion, lift.out.block.insns) is None
    dec, _, _ = model()
    dec._entry_int32_unwind = bad
    with pytest.raises(ArenaDeclined):
        _unwind_cache(dec)


@pytest.mark.parametrize('filter_name', ['comments', 'eh', 'different-method', 'no-conversion'])
def test_cheap_candidate_rejections_do_not_allocate_a_cache(filter_name):
    dec, method, _ = model()
    if filter_name == 'comments':
        dec.L.asm_comments = True
    elif filter_name == 'eh':
        dec.eh = object()
    elif filter_name == 'different-method':
        dec.L._current_method = copy.copy(method)
    else:
        dec._flat_insns = dec._flat_insns[:1]
    assert not _candidate(dec, method)
    assert not hasattr(dec, '_entry_int32_unwind')


def test_preflight_and_capture_reuse_one_index_without_lending_live_proof(monkeypatch):
    from il2cpp.dec.entrycapture import recover_entry_int32
    from il2cpp.lifter.entrycapture import EntryInt32Captures
    from il2cpp import Decompiler

    dec, method, owner = model()
    init = NativeUnwindBoundary.__init__
    builds, attempts = [], []
    def counted(self, binary):
        builds.append(binary)
        init(self, binary)
    def attempted(self, am, at):
        capture = self.L._entry_int32_capture
        assert capture.origin._boundary is self._entry_int32_unwind._proof
        assert capture.origin._boundary is not dec._entry_int32_unwind._proof
        assert capture.origin._boundary._roots is not dec._entry_int32_unwind._proof._roots
        assert self._entry_int32_unwind._owner is self.L.bin is not dec.L.bin
        attempts.append(self)
        return ['attempt']
    monkeypatch.setattr(NativeUnwindBoundary, '__init__', counted)
    monkeypatch.setattr(Decompiler, '_lift_method', attempted)
    monkeypatch.setattr(EntryInt32Captures, 'finalize', lambda *args: (['committed'], 1))
    assert recover_entry_int32(dec, method, owner, ['baseline']) == ['committed']
    assert recover_entry_int32(dec, method, owner, ['baseline']) == ['committed']
    assert builds == [dec.L.bin] and len(attempts) == 2
    assert attempts[0]._entry_int32_unwind is not attempts[1]._entry_int32_unwind
