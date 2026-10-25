"""Fix 146: the Type.GetType(string) native helper is named and its
sites render as the managed call.

Ground truth: 0x18078cf40 (limbus v39, 213 tree-wide sites, no
metadata candidates, not exported). Sites called it as
``sub_x(name, stale, MethodRef)`` -- RCX the assembly-qualified type
name, RDX a dead slot the body overwrites before reading, R8 the
caller's MethodInfo context -- and the result needed a user cast.
The 51-byte head template (two wildcards: the RIP displacement and
the call rel32) is unique in the fixture's whole .text, proven by a
programmatic scan, never hand-transcribed.
"""
from types import SimpleNamespace as NS

from il2cpp import Lifter

# programmatically derived from the fixture's 0x18078cf40; the two
# 4-byte groups at [18:22] and [29:33] are the wildcarded RIP
# displacement and call rel32 (values here are the real ones)
TYPE_GETTYPE_HEAD = bytes.fromhex(
    '48895c24084889542410574883ec20488b3d1a3d9408498bd0488bd9e8'
    'affcffff4c8d4c243848c7442438000000004c8d4424')

TARGET = 0x5000


def gettype_lifter(body):
    lift = Lifter.__new__(Lifter)
    lift.il = NS(addr_candidates={}, types=[])
    lift.meta = NS(typedefs=[])
    lift.bin = NS(
        read=lambda va, n: body[:n] if va == TARGET else None,
        is_exec_va=lambda va: va == TARGET,
        exports={},
    )
    return lift


def test_type_gettype_template_recognized():
    lift = gettype_lifter(TYPE_GETTYPE_HEAD)
    assert lift._is_type_gettype_helper(TARGET)


def test_type_gettype_template_wildcards_the_displacement():
    body = bytearray(TYPE_GETTYPE_HEAD)
    body[18:22] = b'\xde\xad\xbe\xef'      # RIP displacement varies
    lift = gettype_lifter(bytes(body))
    assert lift._is_type_gettype_helper(TARGET)


def test_type_gettype_template_wildcards_the_call_rel32():
    body = bytearray(TYPE_GETTYPE_HEAD)
    body[29:33] = b'\x11\x22\x33\x44'      # call target varies
    lift = gettype_lifter(bytes(body))
    assert lift._is_type_gettype_helper(TARGET)


def test_type_gettype_template_rejects_mutations():
    for where, desc in ((0, 'prologue'), (24, 'mov rdx,r8'),
                        (34, 'lea r9 exception slot'), (42, 'zero-store')):
        body = bytearray(TYPE_GETTYPE_HEAD)
        body[where] ^= 0xFF
        lift = gettype_lifter(bytes(body))
        assert not lift._is_type_gettype_helper(TARGET), desc


def test_type_gettype_template_declines_registered_bodies():
    # a body with metadata owners or an export name is not this helper
    lift = gettype_lifter(TYPE_GETTYPE_HEAD)
    lift.il = NS(addr_candidates={TARGET: [('method', 0)]}, types=[])
    assert not lift._is_type_gettype_helper(TARGET)
    lift2 = gettype_lifter(TYPE_GETTYPE_HEAD)
    lift2.bin = NS(
        read=lambda va, n: TYPE_GETTYPE_HEAD[:n],
        is_exec_va=lambda va: va == TARGET,
        exports={TARGET: 'il2cpp_something'},
    )
    assert not lift2._is_type_gettype_helper(TARGET)
