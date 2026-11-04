"""Authored PE fixtures: no licensed image or captured native body data."""
import struct

import pytest
from iced_x86 import Decoder

from il2cpp.binary import PE
from il2cpp.lifter.unwindproof import NativeUnwindBoundary

BASE = 0x180000000
ROOT = (0x1000, 0x1010, 0x3000)
CHILD = (0x1010, 0x1020, 0x3020)


def image(rows=(ROOT,), *, unwind=None, text=None):
    data = bytearray(0x1000)
    data[:2] = b'MZ'
    struct.pack_into('<I', data, 0x3c, 0x40)
    data[0x40:0x44] = b'PE\x00\x00'
    struct.pack_into('<HH', data, 0x44, 0x8664, 3)
    struct.pack_into('<H', data, 0x54, 0xf0)
    struct.pack_into('<H', data, 0x58, 0x20b)
    struct.pack_into('<Q', data, 0x70, BASE)
    struct.pack_into('<I', data, 0xc4, 16)
    struct.pack_into('<II', data, 0xe0, 0x2000, len(rows) * 12)
    sections = [(b'.text', 0x1000, 0x400, 0x200, 0x60000020),
                (b'.pdata', 0x2000, 0x200, 0x600, 0x40000040),
                (b'.xdata', 0x3000, 0x800, 0x800, 0x40000040)]
    for i, (name, rva, size, offset, chars) in enumerate(sections):
        head = 0x148 + 40 * i
        data[head:head + 8] = name.ljust(8, b'\0')
        struct.pack_into('<IIII', data, head + 8, size, rva, size, offset)
        struct.pack_into('<I', data, head + 36, chars)
    data[0x200:0x600] = b'\x90' * 0x400
    if text:
        for rva, raw in text.items():
            data[0x200 + rva - 0x1000:0x200 + rva - 0x1000 + len(raw)] = raw
    for i, row in enumerate(rows):
        struct.pack_into('<III', data, 0x600 + i * 12, *row)
    unwind = unwind or {0x3000: b'\x01\0\0\0'}
    for rva, raw in unwind.items():
        data[0x800 + rva - 0x3000:0x800 + rva - 0x3000 + len(raw)] = raw
    return PE(bytes(data))


def instructions(binary, rva=0x1000, size=1):
    return list(Decoder(64, binary.read(BASE + rva, size), ip=BASE + rva))


def mutate(binary, offset, raw):
    data = bytearray(binary.d)
    data[offset:offset + len(raw)] = raw
    return PE(bytes(data))


def chain(row=ROOT, *, frame=0):
    return bytes([0x21, 0, 0, frame]) + struct.pack('<III', *row)


def test_plain_handler_free_primary_and_real_pe_parse():
    binary = image()
    assert NativeUnwindBoundary(binary).covers(BASE + 0x1000, instructions(binary)) == (ROOT,)


def test_recursive_chains_cover_one_family_not_the_first_pdata_extent():
    third = (0x1020, 0x1030, 0x3040)
    binary = image((ROOT, CHILD, third), unwind={0x3000: b'\x01\0\0\0',
                   0x3020: chain(), 0x3040: chain(CHILD)})
    seq = instructions(binary, size=0x30)
    assert NativeUnwindBoundary(binary).covers(BASE + 0x1000, seq) == (ROOT, CHILD, third)


def test_directory_not_section_name_selects_records():
    binary = image()
    binary.sections[1].name = 'renamed'
    assert NativeUnwindBoundary(binary).covers(BASE + 0x1000, instructions(binary)) == (ROOT,)


@pytest.mark.parametrize('flags', [1, 2, 3, 5, 6, 7, 8, 16, 31])
def test_all_handlers_reserved_flags_and_chain_handler_combinations_decline(flags):
    binary = image(unwind={0x3000: bytes([(flags << 3) | 1, 0, 0, 0])})
    assert NativeUnwindBoundary(binary).covers(BASE + 0x1000, instructions(binary)) is None


@pytest.mark.parametrize('version', [0, 2, 3, 4, 5, 6, 7])
def test_unsupported_unwind_versions_are_not_no_eh_evidence(version):
    binary = image(unwind={0x3000: bytes([version, 0, 0, 0])})
    assert NativeUnwindBoundary(binary).covers(BASE + 0x1000, instructions(binary)) is None


def test_missing_directory_and_uncovered_leaf_decline():
    binary = image(())
    assert NativeUnwindBoundary(binary).covers(BASE + 0x1000, instructions(binary)) is None
    binary = image(((0x1010, 0x1020, 0x3000),))
    assert NativeUnwindBoundary(binary).covers(BASE + 0x1000, instructions(binary)) is None


@pytest.mark.parametrize('offset,raw', [
    (0x44, b'\x64\xaa'), (0x54, b'\x80\0'), (0x58, b'\x0b\x01'),
    (0xc4, struct.pack('<I', 3)), (0xe0, struct.pack('<I', 0)),
    (0xe4, struct.pack('<I', 11)), (0xe4, struct.pack('<I', 0x204)),
    (0xe0, struct.pack('<I', 0x21f8)),
])
def test_bad_platform_optional_header_and_directory_decline(offset, raw):
    baseline = image()
    seq = instructions(baseline)
    binary = mutate(baseline, offset, raw)
    assert NativeUnwindBoundary(binary).covers(BASE + 0x1000, seq) is None


@pytest.mark.parametrize('rows', [
    (ROOT, ROOT), (CHILD, ROOT), (ROOT, (0x1008, 0x1020, 0x3020)),
    ((0x1000, 0x1000, 0x3000),), ((0x1000, 0x1010, 0),),
    ((0x1000, 0x1010, 0x3001),), ((0, 0x1010, 0x3000),),
])
def test_unsorted_overlapping_duplicate_invalid_runtime_records_decline(rows):
    binary = image(rows)
    assert NativeUnwindBoundary(binary).covers(BASE + 0x1000, instructions(binary)) is None


@pytest.mark.parametrize('target', [
    (0x1001, 0x1010, 0x3000), (0x1000, 0x100f, 0x3000),
    (0x1000, 0x1010, 0x3040), CHILD,
])
def test_chain_must_target_exact_indexed_record_and_not_cycle(target):
    binary = image((ROOT, CHILD), unwind={0x3000: b'\x01\0\0\0', 0x3020: chain(target)})
    assert NativeUnwindBoundary(binary).covers(BASE + 0x1000, instructions(binary, size=0x20)) is None


def test_primary_chain_cycle_declines_without_recursion():
    binary = image((ROOT, CHILD), unwind={0x3000: chain(CHILD), 0x3020: chain(ROOT)})
    assert NativeUnwindBoundary(binary).covers(BASE + 0x1000, instructions(binary)) is None


def test_adjacent_but_unrelated_primary_is_not_method_ownership():
    binary = image((ROOT, CHILD), unwind={0x3000: b'\x01\0\0\0', 0x3020: b'\x01\0\0\0'})
    assert NativeUnwindBoundary(binary).covers(BASE + 0x1000, instructions(binary, size=0x20)) is None


def test_handler_in_primary_or_child_rejects_whole_footprint():
    for first, second in [(b'\x09\0\0\0', chain()),
                          (b'\x01\0\0\0', b'\x09\0\0\0')]:
        binary = image((ROOT, CHILD), unwind={0x3000: first, 0x3020: second})
        assert NativeUnwindBoundary(binary).covers(BASE + 0x1000, instructions(binary, size=0x20)) is None


def test_mid_record_entry_and_secondary_entry_decline():
    binary = image((ROOT, CHILD), unwind={0x3000: b'\x01\0\0\0', 0x3020: chain()})
    proof = NativeUnwindBoundary(binary)
    for rva in (0x1001, 0x1010):
        assert proof.covers(BASE + rva, instructions(binary, rva)) is None


def test_instruction_must_not_cross_runtime_record_boundary():
    binary = image(((0x1000, 0x1001, 0x3000),), text={0x1000: b'\x66\x90'})
    assert NativeUnwindBoundary(binary).covers(BASE + 0x1000, instructions(binary, size=2)) is None


def test_forged_instruction_and_overlap_and_invalid_decode_decline():
    binary = image()
    proof = NativeUnwindBoundary(binary)
    forged = list(Decoder(64, b'\xc3', ip=BASE + 0x1000))
    actual = instructions(binary)
    assert proof.covers(BASE + 0x1000, forged) is None
    assert proof.covers(BASE + 0x1000, actual * 2) is None
    assert proof.covers(BASE + 0x1000, list(Decoder(64, b'\x0f', ip=BASE + 0x1000))) is None
    assert proof.covers(BASE + 0x1000, []) is None


def test_uncovered_tail_and_raw_backing_short_reads_decline():
    binary = image()
    assert NativeUnwindBoundary(binary).covers(BASE + 0x1000, instructions(binary, size=0x11)) is None
    for field, value in [('rawsize', 0), ('size', 0), ('offset', len(binary.d)), ('chars', 0x40000040)]:
        binary = image()
        setattr(binary.sections[0], field, value)
        assert NativeUnwindBoundary(binary).covers(BASE + 0x1000, list(Decoder(64, b'\x90', ip=BASE + 0x1000))) is None


def test_ambiguous_section_mapping_declines_instead_of_first_match_wins():
    binary = image()
    binary.sections.append(binary.sections[0])
    assert NativeUnwindBoundary(binary).covers(BASE + 0x1000, instructions(binary)) is None


def test_exact_512_instruction_limit():
    row = (0x1000, 0x1400, 0x3000)
    binary = image((row,))
    proof = NativeUnwindBoundary(binary)
    assert proof.covers(BASE + 0x1000, instructions(binary, size=512)) == (row,)
    assert proof.covers(BASE + 0x1000, instructions(binary, size=513)) is None


@pytest.mark.parametrize('header,codes', [
    (b'\x01\x01\x01\0', b'\x01\x30'),  # push rbx
    (b'\x01\x01\x01\0', b'\x01\xf2'),  # alloc_small
    (b'\x01\x01\x02\0', b'\x01\x01\x10\0'),
    (b'\x01\x01\x03\0', b'\x01\x11\x80\0\0\0'),
    (b'\x01\x01\x01\x05', b'\x01\x03'),  # set_fpreg rbp
    (b'\x01\x01\x02\0', b'\x01\x34\0\0'),
    (b'\x01\x01\x03\0', b'\x01\x35\0\0\0\0'),
    (b'\x01\x01\x02\0', b'\x01\x68\0\0'),
    (b'\x01\x01\x03\0', b'\x01\x69\0\0\0\0'),
    (b'\x01\x01\x01\0', b'\x01\x0a'),
])
def test_supported_v1_unwind_slot_grammar(header, codes):
    binary = image(unwind={0x3000: header + codes + b'\0' * ((-len(codes)) % 4)})
    assert NativeUnwindBoundary(binary).covers(BASE + 0x1000, instructions(binary)) == (ROOT,)


@pytest.mark.parametrize('header,codes', [
    (b'\x01\x01\x01\0', b'\x02\x30'),  # outside prolog
    (b'\x01\x01\x01\0', b'\x01\x00'),  # volatile register
    (b'\x01\x01\x01\0', b'\x01\x21'),  # reserved alloc_large
    (b'\x01\x01\x01\0', b'\x01\x01'),  # missing operand slot
    (b'\x01\x01\x01\0', b'\x01\x06'),
    (b'\x01\x01\x01\0', b'\x01\x07'),
    (b'\x01\x01\x01\0', b'\x01\x0b'),
    (b'\x01\x01\x01\0', b'\x01\x03'),  # no frame register
    (b'\x01\x01\x01\x05', b'\x01\x13'),
    (b'\x01\0\0\x10', b''),
    (b'\x01\0\0\x01', b''),
    (b'\x01\x02\x02\0', b'\x01\x30\x02\x30'),
    (b'\x01\x01\x02\0', b'\x01\x58\0\0'),
    (b'\x01\x01\x01\0', b'\x01\x2a'),
])
def test_unsupported_or_malformed_slot_grammar_declines(header, codes):
    binary = image(unwind={0x3000: header + codes + b'\0' * ((-len(codes)) % 4)})
    assert NativeUnwindBoundary(binary).covers(BASE + 0x1000, instructions(binary)) is None


def test_odd_slot_padding_places_chain_triple_at_four_byte_alignment():
    binary = image((ROOT, CHILD), unwind={0x3000: b'\x01\0\0\0',
                   0x3020: b'\x21\x01\x01\0\x01\x30\0\0' + struct.pack('<III', *ROOT)})
    assert NativeUnwindBoundary(binary).covers(BASE + 0x1000, instructions(binary, size=0x20)) == (ROOT, CHILD)


def test_short_header_slots_padding_or_chain_never_read_next_section():
    for rva, raw in [(0x37fe, b'\x01\0'),
                     (0x37fc, b'\x01\x01\x01\0'),
                     (0x37f8, b'\x21\0\0\0')]:
        row = (0x1000, 0x1010, rva)
        binary = image((row,), unwind={rva: raw})
        assert NativeUnwindBoundary(binary).covers(BASE + 0x1000, instructions(binary)) is None


def test_failed_child_query_cannot_poison_valid_ancestor_or_other_binary():
    binary = image((ROOT, CHILD), unwind={0x3000: b'\x01\0\0\0', 0x3020: chain(frame=5)})
    proof = NativeUnwindBoundary(binary)
    assert proof.covers(BASE + 0x1000, instructions(binary, size=0x20)) is None
    assert proof.covers(BASE + 0x1000, instructions(binary)) == (ROOT,)
    other = image(unwind={0x3000: b'\x09\0\0\0'})
    assert NativeUnwindBoundary(other).covers(BASE + 0x1000, instructions(other)) is None
    assert proof.covers(BASE + 0x1000, instructions(binary)) == (ROOT,)


def test_binary_and_section_mutation_after_construction_cannot_change_snapshot():
    binary = image()
    proof = NativeUnwindBoundary(binary)
    seq = instructions(binary)
    binary.d = b''
    binary.sections.clear()
    assert proof.covers(BASE + 0x1000, seq) == (ROOT,)


def test_non_pe_and_malformed_objects_decline():
    for binary in (None, object(), b'not a PE'):
        assert NativeUnwindBoundary(binary).covers(BASE + 0x1000, []) is None
    proof = NativeUnwindBoundary(image())
    assert proof.covers(None, [object()]) is None


def test_chain_bound_is_independent_conservative_and_order_stable():
    rows = tuple((0x1000 + 16 * i, 0x1010 + 16 * i, 0x3000 + 32 * i)
                 for i in range(33))
    unwind = {rows[0][2]: b'\x01\0\0\0'}
    unwind.update({row[2]: chain(rows[i - 1]) for i, row in enumerate(rows) if i})
    binary = image(rows, unwind=unwind)
    proof = NativeUnwindBoundary(binary)
    assert proof.covers(BASE + 0x1000, instructions(binary, size=32 * 16)) == rows[:32]
    assert proof.covers(BASE + 0x1000, instructions(binary, size=512) +
                        instructions(binary, rva=0x1200)) is None
    # Keep under the independent instruction count while touching depth 33.
    sparse = instructions(binary) + instructions(binary, rva=0x1200)
    assert proof.covers(BASE + 0x1000, sparse) is None
    assert proof.covers(BASE + 0x1000, instructions(binary)) == rows[:1]


def test_same_va_different_binary_context_and_failed_query_do_not_leak():
    first = image()
    second = image(text={0x1000: b'\xc3'})
    a, b = NativeUnwindBoundary(first), NativeUnwindBoundary(second)
    nop, ret = instructions(first), instructions(second)
    assert a.covers(BASE + 0x1000, ret) is None
    assert b.covers(BASE + 0x1000, nop) is None
    assert a.covers(BASE + 0x1000, nop) == (ROOT,)
    assert b.covers(BASE + 0x1000, ret) == (ROOT,)
