"""Explicit platform boundary for Windows x64 native recovery rules."""
import struct

from il2cpp.binary import PE


def is_win64_pe(binary):
    """Do not treat is64, x64 instruction bytes, or a filename as ABI proof."""
    try:
        if not isinstance(binary, PE) or not binary.is64:
            return False
        pe = struct.unpack_from('<I', binary.d, 0x3c)[0]
        return binary.d[pe:pe + 4] == b'PE\x00\x00' \
            and struct.unpack_from('<H', binary.d, pe + 4)[0] == 0x8664
    except (AttributeError, IndexError, TypeError, ValueError, OverflowError, struct.error):
        return False
