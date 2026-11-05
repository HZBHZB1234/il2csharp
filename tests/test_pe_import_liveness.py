"""Authored PE import records and conservative native argument proofs."""
import struct
from types import SimpleNamespace

import pytest

pytest.importorskip("iced_x86")

from il2cpp.binary import PE
from il2cpp.entrylive import entry_live_args
from il2cpp import Expr
from il2cpp.lifter.calls import _CallsMixin

BASE = 0x180000000
SLOT = BASE + 0x1120
NAME = b"?Baselib_Thread_GetCurrentThreadId@il2cpp_baselib@@YA_JXZ"


def image(module=b"baselib.dll", name=NAME):
    data = bytearray(0x1000)
    struct.pack_into("<I", data, 0x3c, 0x80)
    data[0x80:0x84] = b"PE\0\0"
    struct.pack_into("<H", data, 0x86, 2)
    struct.pack_into("<H", data, 0x94, 0xf0)
    opt = 0x98
    struct.pack_into("<H", data, opt, 0x20b)
    struct.pack_into("<Q", data, opt + 24, BASE)
    struct.pack_into("<I", data, opt + 108, 16)
    struct.pack_into("<II", data, opt + 120, 0x1000, 40)
    sections = ((0x188, 0x1000, 0x200, 0x600, 0x40000040),
                (0x1b0, 0x2000, 0x800, 0x200, 0x60000020))
    for offset, rva, raw, size, chars in sections:
        data[offset:offset + 8] = (b".rdata\0\0" if rva == 0x1000
                                   else b".text\0\0\0")
        struct.pack_into("<IIII", data, offset + 8, size, rva, size, raw)
        struct.pack_into("<I", data, offset + 36, chars)
    struct.pack_into("<IIIII", data, 0x200, 0x1100, 0, 0, 0x1140, 0x1120)
    struct.pack_into("<Q", data, 0x300, 0x1160)
    struct.pack_into("<Q", data, 0x320, 0x1160)
    data[0x340:0x340 + len(module) + 1] = module + b"\0"
    data[0x360:0x360 + len(name) + 3] = b"\0\0" + name + b"\0"
    code = b"\xff\x15" + struct.pack("<i", SLOT - (BASE + 0x2006)) + b"\xc3"
    data[0x800:0x800 + len(code)] = code
    return bytes(data)

ENTRY = BASE + 0x2000


def modified(offset, fmt, *values):
    data = bytearray(image())
    struct.pack_into(fmt, data, offset, *values)
    return bytes(data)


def native(data=None, code=None):
    data = bytearray(image() if data is None else data)
    if code is None:
        code = bytes(data[0x800:0x807])
    data[0x800:0x800 + len(code)] = code
    binary = PE(bytes(data))
    il = SimpleNamespace(bin=binary, function_extent=lambda va: (
        (ENTRY, ENTRY + len(code)) if va == ENTRY else (va, None)))
    return il


def indirect(prefix=b"", suffix=b"\xc3", slot=SLOT):
    ip = ENTRY + len(prefix)
    return prefix + b"\xff\x15" + struct.pack("<i", slot - (ip + 6)) + suffix


def test_named_iat_identity_is_exact_and_file_backed():
    binary = PE(image())
    assert binary.named_imports == {SLOT: ("baselib.dll", NAME.decode())}
    assert binary.qword(SLOT) == 0x1160  # do not resolve/load the DLL


@pytest.mark.parametrize("module", [b"baselib.dll", b"BASELIB.DLL"])
def test_nullary_import_reads_no_entry_arguments(module):
    il = native(image(module))
    assert entry_live_args(il, ENTRY) == ("", "", "", "")


@pytest.mark.parametrize("module,name", [
    (b"other.dll", NAME),
    (b"baselib.dll.evil", NAME),
    (b"some/baselib.dll", NAME),
    (b"baselib.dll", b"?Baselib_Thread_GetCurrentThreadId@il2cpp_baselib@@YA_JH@Z"),
    (b"baselib.dll", b"Baselib_Thread_GetCurrentThreadId"),
    (b"baselib.dll", NAME.lower()),
])
def test_similar_or_unsigned_import_keeps_conservative_reads(module, name):
    il = native(image(module, name))
    assert entry_live_args(il, ENTRY) == ("gx", "gx", "gx", "gx")


def test_missing_lookup_uses_only_an_unbound_file_iat():
    binary = PE(modified(0x200, "<I", 0))
    assert binary.named_imports == {SLOT: ("baselib.dll", NAME.decode())}
    assert not PE(modified(0x200, "<II", 0, 123)).named_imports


def test_bound_import_uses_lookup_names_not_loader_pointer():
    data = bytearray(image())
    struct.pack_into("<I", data, 0x204, 123)
    struct.pack_into("<Q", data, 0x320, 0x7ff800001000)
    assert PE(bytes(data)).named_imports == {
        SLOT: ("baselib.dll", NAME.decode())}


def test_ordinal_is_not_a_named_signature():
    il = native(modified(0x300, "<Q", (1 << 63) | 23))
    assert not il.bin.named_imports
    assert entry_live_args(il, ENTRY) == ("gx", "gx", "gx", "gx")


@pytest.mark.parametrize("offset,fmt,values", [
    (0x98, "<H", (0x10b,)),  # unsupported PE32
    (0x94, "<H", (127,)),  # no import directory in optional header
    (0x104, "<I", (1,)),  # NumberOfRvaAndSizes < 2
    (0x110, "<II", (0, 40)),
    (0x110, "<II", (0x1000, 20)),  # no room for null descriptor
    (0x110, "<II", (0x1000, 4096 * 20 + 1)),
    (0x110, "<II", (0x9999, 40)),
    (0x200, "<I", (0x9999,)),  # invalid lookup RVA
    (0x20c, "<I", (0,)),  # empty DLL RVA
    (0x20c, "<I", (0x9999,)),
    (0x210, "<I", (0,)),  # missing IAT
    (0x210, "<I", (0x15fc,)),  # IAT straddles raw section
    (0x210, "<I", (0x2000,)),  # executable IAT slot
    (0x300, "<Q", ((1 << 63) | (1 << 40) | 7,)),
    (0x300, "<Q", (0x100001160,)),  # non-RVA named thunk
    (0x300, "<Q", (0x9999,)),
    (0x308, "<Q", (0x9999,)),  # later bad thunk invalidates partial results
    (0x340, "<B", (0,)),
    (0x340, "<B", (0xff,)),  # invalid ASCII DLL name
    (0x362, "<B", (0,)),
    (0x362, "<B", (0xff,)),
    (0x1ac, "<I", (0x60000040,)),  # IAT section executable
])
def test_malformed_or_unsupported_import_table_declines(offset, fmt, values):
    assert not PE(modified(offset, fmt, *values)).named_imports


def test_missing_descriptor_terminator_declines_all_identities():
    data = bytearray(image())
    data[0x214:0x228] = data[0x200:0x214]
    assert not PE(bytes(data)).named_imports


@pytest.mark.parametrize("ordinal_first", [False, True])
def test_aliasing_descriptors_decline_even_for_ordinal_slots(ordinal_first):
    data = bytearray(image())
    struct.pack_into("<I", data, 0x114, 60)
    data[0x214:0x228] = data[0x200:0x214]
    struct.pack_into("<I", data, 0x214, 0x1180)
    struct.pack_into("<Q", data, 0x380, 0x1160)
    if ordinal_first:
        struct.pack_into("<Q", data, 0x300, (1 << 63) | 1)
    assert not PE(bytes(data)).named_imports


@pytest.mark.parametrize("field,limit", [(0x340, 256), (0x362, 1024)])
def test_unterminated_names_are_bounded(field, limit):
    data = bytearray(image())
    # Fill only the current section; never consume a following section/file.
    data[field:0x800] = b"A" * (0x800 - field)
    assert not PE(bytes(data)).named_imports


def test_imports_do_not_leak_between_binary_instances():
    known = PE(image())
    unknown = PE(image(b"other.dll"))
    assert known.named_imports[SLOT][0] == "baselib.dll"
    assert unknown.named_imports[SLOT][0] == "other.dll"


def test_non_pe_image_with_fabricated_import_identity_is_not_trusted():
    il = native()
    source = il.bin
    il.bin = SimpleNamespace(read=source.read, is_exec_va=source.is_exec_va,
                             named_imports=source.named_imports)
    assert entry_live_args(il, ENTRY) == ("gx", "gx", "gx", "gx")


def test_import_identity_must_match_the_exact_rip_relative_slot():
    il = native(code=indirect(slot=SLOT + 8))
    assert entry_live_args(il, ENTRY) == ("gx", "gx", "gx", "gx")


@pytest.mark.parametrize("prefix", [b"\x64", b"\x65"])
def test_segment_relative_call_is_not_a_flat_iat_slot(prefix):
    # FS/GS base changes the effective address even when RIP displacement matches.
    code = prefix + b"\xff\x15" + struct.pack(
        "<i", SLOT - (ENTRY + len(prefix) + 6)) + b"\xc3"
    assert entry_live_args(native(code=code), ENTRY) == ("gx", "gx", "gx", "gx")


def test_far_call_is_not_an_ordinary_nullary_iat_call():
    code = b"\x48\xff\x1d" + struct.pack(
        "<i", SLOT - (ENTRY + 7)) + b"\xc3"
    assert entry_live_args(native(code=code), ENTRY) == ("gx", "gx", "gx", "gx")


def test_register_indirect_call_remains_conservative():
    il = native(code=b"\xff\xd0\xc3")  # call rax; ret
    assert entry_live_args(il, ENTRY) == ("gx", "gx", "gx", "gx")


def test_import_tail_branch_still_declines():
    code = b"\xff\x25" + struct.pack("<i", SLOT - (ENTRY + 6))
    assert entry_live_args(native(code=code), ENTRY) is None


def test_reads_before_nullary_call_still_contribute_arguments():
    # Save RCX and RDX, then the import executes but reads no argument slots.
    il = native(code=indirect(prefix=bytes.fromhex("4889cb4889d6")))
    assert entry_live_args(il, ENTRY) == ("g", "g", "", "")


def test_nullary_call_still_clobbers_volatile_entry_values():
    # A read after the call is not an incoming RCX/XMM0 read.
    code = indirect(suffix=bytes.fromhex("4889c8f30f58c1c3"))
    assert entry_live_args(native(code=code), ENTRY) == ("", "", "", "")


def test_stack_arguments_still_decline():
    code = indirect(prefix=bytes.fromhex("488b442428"))
    assert entry_live_args(native(code=code), ENTRY) is None


def test_conditional_unknown_arm_keeps_every_entry_argument():
    # jz skips known import and lands at an unknown register call.
    code = bytes.fromhex("7407") + indirect(suffix=b"\xc3\xff\xd0\xc3")
    assert entry_live_args(native(code=code), ENTRY) == ("gx", "gx", "gx", "gx")


def test_direct_caller_recursion_and_cache_order_remain_deterministic():
    # Wrapper reads RCX then calls the function containing the nullary import.
    def setup():
        il = native()
        original_read = il.bin.read
        other = ENTRY + 0x100
        code = b"\x48\x89\xcb\xe8" + struct.pack("<i", ENTRY - (other + 8)) + b"\xc3"
        il.bin.read = lambda va, n: code[:n] if va == other else original_read(va, n)
        il.function_extent = lambda va: ((other, other + len(code)) if va == other
                                        else (ENTRY, ENTRY + 7))
        return il, other
    il, other = setup()
    first = entry_live_args(il, other), entry_live_args(il, ENTRY)
    il, other = setup()
    second = entry_live_args(il, ENTRY), entry_live_args(il, other)
    assert first == (second[1], second[0]) == (("g", "", "", ""), ("", "", "", ""))


def test_raw_call_argument_consumer_keeps_the_helper_and_its_live_input():
    il = native(code=indirect(prefix=bytes.fromhex("4889cb")))
    il.addr_candidates = {}
    lift = _CallsMixin()
    lift.il, lift.bin = il, il.bin
    values = [Expr(n, None, "obj") for n in ("methodInfo", "stale1", "stale2", "stale3")]
    assert lift._entry_live_call_args(ENTRY, values, [v.text for v in values],
                                      [None] * 4) == ["methodInfo"]


@pytest.mark.parametrize("known", [True, False])
def test_complete_raw_call_is_kept_once_and_only_proved_arguments_are_trimmed(known):
    from iced_x86 import Decoder
    from test_stack_args import make_call_lifter

    il = native(image(b"baselib.dll" if known else b"other.dll"),
                code=indirect(prefix=bytes.fromhex("4889cb")))
    lift, _ = make_call_lifter([], {"RCX": "methodInfo", "RDX": "stale1",
                                   "R8": "stale2", "R9": "stale3"})
    lift.bin = lift.il.bin = il.bin
    lift.il.function_extent = il.function_extent
    lift.il.addr_candidates = {}
    lift.il.addr_to_method = {}
    lift._call_name = lambda target: "sub_180002000"
    ip = BASE + 0x1000
    ins = Decoder(64, b"\xe8" + struct.pack("<i", ENTRY - (ip + 5)), ip=ip).decode()
    lift._insn(ins, [ins], 0, None, ins.next_ip)
    text = "\n".join(row[1] for row in lift.out)
    expected = "methodInfo" if known else "methodInfo, stale1, stale2, stale3"
    assert text.count("sub_180002000(" + expected + ")") == 1
    assert "GetCurrentThreadId" not in text  # do not rename/elide the helper
