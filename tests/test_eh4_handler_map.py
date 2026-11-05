"""Authored EH4 data, not game bodies; handler entries are not continuations."""
import bisect
import struct
from types import SimpleNamespace

import pytest

from il2cpp.runtime.eh import _EhMixin


IB = 0x180000000
BG = 0x1000
END = 0x2000
MAP = 0x600


def _uint(value):
    for width in range(1, 5):
        bits = width * 7
        if value < 1 << bits:
            return ((value << width) | ((1 << (width - 1)) - 1)).to_bytes(width, 'little')
    return b'\x0f' + struct.pack('<I', value)


def _entry(flags, *, adjectives=0x81, descriptor=0x3500, catch=0x48,
           handler=0x3000, continuations=(0x200,)):
    out = bytearray([flags])
    if flags & 1:
        out += _uint(adjectives)
    if flags & 2:
        out += struct.pack('<i', descriptor)
    if flags & 4:
        out += _uint(catch)
    out += struct.pack('<i', handler)
    for value in continuations:
        out += struct.pack('<i', value) if flags & 8 else _uint(value)
    return bytes(out)


def _image(entries, *, declared_count=None):
    data = bytearray(0x4000)
    data[0x100] = 8  # UNW_FLAG_EHANDLER, no unwind codes
    struct.pack_into('<II', data, 0x104, 0x3800, 0x400)
    data[0x400] = 0x10  # TryBlockMap, no unwind map, non-separated
    struct.pack_into('<II', data, 0x401, 0x500, 0)
    trymap = _uint(1) + _uint(0) + _uint(1) + _uint(2) + struct.pack('<I', MAP)
    data[0x500:0x500 + len(trymap)] = trymap
    handlers = _uint(len(entries) if declared_count is None else declared_count) + b''.join(entries)
    data[MAP:MAP + len(handlers)] = handlers
    obj = _EhMixin()
    obj.bin = SimpleNamespace(d=data, image_base=IB,
                              va2off=lambda va: va - IB if IB <= va < IB + len(data) else None)
    obj._bisect = bisect
    obj._eh4_begins = [BG]
    obj._eh4_entries = [(BG, END, 0x100)]
    obj._eh4_handler = 0x3800
    obj._eh4_state = True
    obj._eh4_cache = {}
    return obj


@pytest.mark.parametrize('optional', range(8))
@pytest.mark.parametrize('rva_mode', [False, True])
@pytest.mark.parametrize('count', [0, 1, 2])
def test_handler_map_decodes_fields_independently(optional, rva_mode, count):
    values = (0x1200, 0x1400)[:count] if rva_mode else (0x200, 0x400)[:count]
    flags = optional | (8 if rva_mode else 0) | (count << 4)
    obj = _image([_entry(flags, continuations=values)])
    result = obj._eh4_handlers(MAP, BG)
    assert result == [dict(flags=flags, adjectives=0x81 if optional & 1 else 0,
                          type_descriptor=IB + 0x3500 if optional & 2 else None,
                          catch_object_offset=0x48 if optional & 4 else None,
                          handler=IB + 0x3000,
                          continuations=[IB + BG + v for v in (0x200, 0x400)[:count]])]


@pytest.mark.parametrize('rva_mode', [False, True])
def test_each_single_continuation_is_relative_to_function_not_previous_handler(rva_mode):
    flags = 0x17 | (8 if rva_mode else 0)
    values = [0x1200, 0x1400] if rva_mode else [0x200, 0x400]
    obj = _image([_entry(flags, continuations=(v,)) for v in values])
    result = obj._eh4_parse(BG)
    assert result['pads'] == [IB + 0x1200, IB + 0x1400]
    assert result['try_pads'] == [result['pads']]
    assert result['nhandlers'] == 2  # compatibility: admitted single-continuation pads


@pytest.mark.parametrize('rva_mode', [False, True])
def test_two_continuations_consume_both_but_do_not_guess_selected_pad(rva_mode):
    double = (0x1200, 0x1400) if rva_mode else (0x200, 0x400)
    single = (0x1600,) if rva_mode else (0x600,)
    obj = _image([_entry(0x27 | (8 if rva_mode else 0), continuations=double),
                  _entry(0x17 | (8 if rva_mode else 0), continuations=single)])
    result = obj._eh4_parse(BG)
    assert result['pads'] == [IB + 0x1600]
    assert result['handlers'][0]['continuations'] == [IB + 0x1200, IB + 0x1400]
    assert result['handlers'][1]['continuations'] == [IB + 0x1600]


def test_handler_optional_fields_reset_between_entries():
    obj = _image([_entry(0x17), _entry(0x10, continuations=(0x400,))])
    first, second = obj._eh4_handlers(MAP, BG)
    assert first['catch_object_offset'] == 0x48
    assert second['catch_object_offset'] is None
    assert second['type_descriptor'] is None
    assert second['adjectives'] == 0


def test_signed_fixed_width_rvas_are_not_unsigned_or_function_relative():
    obj = _image([_entry(0x1a, descriptor=-0x80, handler=-0x40, continuations=(-0x20,))])
    result = obj._eh4_handlers(MAP, BG)[0]
    assert result['type_descriptor'] == IB - 0x80
    assert result['handler'] == IB - 0x40
    assert result['continuations'] == [IB - 0x20]


@pytest.mark.parametrize('value', [0, 0x7f, 0x80, 0x3fff, 0x4000,
                                 0x1fffff, 0x200000, 0xfffffff, 0x10000000])
def test_catch_object_offset_uses_all_compressed_unsigned_widths(value):
    obj = _image([_entry(0x14, catch=value)])
    assert obj._eh4_handlers(MAP, BG)[0]['catch_object_offset'] == value


@pytest.mark.parametrize('continuation', [0, 0xfff, 0x2000, 0x2800])
def test_only_in_parent_single_continuation_is_admitted(continuation):
    obj = _image([_entry(0x18, continuations=(continuation,))])
    result = obj._eh4_parse(BG)
    assert result is None


def test_handler_metadata_is_distinct_from_continuation_and_grouped_by_try():
    obj = _image([_entry(0x17)])
    result = obj._eh4_parse(BG)
    assert result['handlers'][0]['handler'] == IB + 0x3000
    assert result['pads'] == [IB + 0x1200]
    assert result['try_handlers'] == [result['handlers']]
    assert result['handlers'][0]['catch_object_offset'] == 0x48


@pytest.mark.parametrize('flags', [0x30, 0x40, 0x80, 0xff])
def test_unknown_handler_layout_declines_without_guess(flags):
    obj = _image([_entry(flags, continuations=())])
    assert obj.eh_regions(IB + BG) is None


def test_handler_count_over_bound_declines_instead_of_partial_map():
    obj = _image([_entry(0x17)] * 33)
    assert obj.eh_regions(IB + BG) is None


def test_no_handler_map_has_no_entries():
    assert _image([])._eh4_handlers(MAP, BG) == []


def test_truncated_handler_map_declines():
    obj = _image([_entry(0x1f, continuations=(0x1200,))])
    obj.bin.d = obj.bin.d[:MAP + 5]
    assert obj.eh_regions(IB + BG) is None


def test_each_try_retains_its_own_handler_metadata():
    obj = _image([_entry(0x17)])
    second_map = 0x800
    second = _uint(1) + _entry(0x10, continuations=(0x400,))
    obj.bin.d[second_map:second_map + len(second)] = second
    tries = (_uint(2) + _uint(0) + _uint(0) + _uint(1) + struct.pack('<I', MAP)
             + _uint(2) + _uint(2) + _uint(3) + struct.pack('<I', second_map))
    obj.bin.d[0x500:0x500 + len(tries)] = tries
    result = obj._eh4_parse(BG)
    assert result['ntry'] == 2
    assert result['try_pads'] == [[IB + 0x1200], [IB + 0x1400]]
    assert [len(group) for group in result['try_handlers']] == [1, 1]
    assert result['handlers'] == result['try_handlers'][0] + result['try_handlers'][1]
    assert result['try_handlers'][1][0]['catch_object_offset'] is None


def test_zero_catch_offset_is_present_not_missing():
    result = _image([_entry(0x14, catch=0)])._eh4_handlers(MAP, BG)[0]
    assert result['catch_object_offset'] == 0
    assert result['type_descriptor'] is None


def test_handler_count_at_supported_bound_decodes_all_entries():
    obj = _image([_entry(0x17)] * 32)
    assert len(obj._eh4_handlers(MAP, BG)) == 32
    assert len(obj._eh4_parse(BG)['handlers']) == 32
