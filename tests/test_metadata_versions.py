"""The metadata method-table parser across format versions.

Pre-v31 rows are 32 bytes / six int32 (no returnParameterToken); v31
rows are 36 bytes / seven int32.  The pre-v31 branch bound the return
type as `rt` while the shared MethodDef call read `rtok`, so every
real file with metadata < v31 (Megabonk ships v29) died with
UnboundLocalError before the binary was even loaded.  These tests pin
both layouts, including the return-type field and the token offset.
"""
import struct

import pytest

from il2cpp.metadata import HEADER_TABLES, V_TABLES_MIN, Metadata

SENTINEL_RT = 42
SENTINEL_RP = 0x1C000042
SENTINEL_TOKEN = 0x06000001


def _build(version, name=b'Foo', return_type=SENTINEL_RT,
           token=SENTINEL_TOKEN):
    """A minimal but real global-metadata.dat: header, one method row,
    one string.  Every other table is present (per version) with size 0,
    which is exactly what a v29 file's parser walks first."""
    strings = name + b'\x00'
    tables = []
    off = 8
    for tname, _struct_size in HEADER_TABLES:
        if version < V_TABLES_MIN.get(tname, 0):
            continue
        tables.append((tname, off))
        off += 8
    header_end = off

    mstride = 36 if version >= 31 else 32
    method_off = header_end
    if version >= 31:
        row = struct.pack('<7i', 0, 0, return_type, SENTINEL_RP, 0, -1, token) \
            + struct.pack('<4H', 0x10, 0, 3, 0)
    else:
        row = struct.pack('<6i', 0, 0, return_type, 0, -1, token) \
            + struct.pack('<4H', 0x10, 0, 3, 0)
    assert len(row) == mstride

    string_off = method_off + mstride
    buf = bytearray(string_off + len(strings))
    struct.pack_into('<I', buf, 0, 0xFAB11BAF)
    struct.pack_into('<i', buf, 4, version)
    for tname, toff in tables:
        offset, size = 0, 0
        if tname == 'methods':
            offset, size = method_off, mstride
        elif tname == 'string':
            offset, size = string_off, len(strings)
        struct.pack_into('<i', buf, toff, offset)
        struct.pack_into('<i', buf, toff + 4, size)
    buf[method_off:method_off + mstride] = row
    buf[string_off:string_off + len(strings)] = strings
    return bytes(buf)


@pytest.mark.parametrize('version', [24, 27, 29, 30, 31])
def test_method_table_return_type_parses(tmp_path, version):
    path = tmp_path / 'global-metadata.dat'
    path.write_bytes(_build(version))

    m = Metadata(str(path))

    assert len(m.methods) == 1
    md = m.methods[0]
    assert md.name == 'Foo'
    assert md.declaring == 0
    assert md.return_type == SENTINEL_RT
    assert md.parameter_start == 0
    assert md.generic_container == -1
    assert md.token == SENTINEL_TOKEN
    assert md.flags == 0x10 and md.is_static
    assert md.slot == 3
    assert md.param_count == 0


def test_v31_row_carries_return_parameter_token(tmp_path):
    """v31's extra int32 shifts the row to 36 bytes; the shared parser
    must read the same name/return-type/token fields there too."""
    path = tmp_path / 'global-metadata.dat'
    path.write_bytes(_build(31))

    m = Metadata(str(path))

    md = m.methods[0]
    assert (md.name, md.return_type, md.token) == (
        'Foo', SENTINEL_RT, SENTINEL_TOKEN)
    strided = _build(31)
    # 36-byte stride: the string table sits right after the row.
    assert len(strided) == 8 + 31 * 8 + 36 + len(b'Foo\x00')


# -- v39 (Unity 6000.3) --------------------------------------------------
# The triple header (offset, size, count per table) and the
# variable-width indexes are new in v38+; the typedef row is 82 bytes and
# the method row 32.  Limbus Company ships exactly this shape.  The
# synthetic file declares 256 typedefs and 256 generic containers so the
# derived widths match a real file (td_w = gc_w = 2, type_w = 4).

TD_W, GC_W = 2, 2
V39_N_TD = 256
V39_STRINGS = b'\x00Foo\x00Bar\x00Ns\x00asm.dll\x00'
V39_LITERAL_DATA = b'HiWorld'


def _build_v39():
    hdr_end = 8 + 31 * 12
    tdo = hdr_end
    td_size = V39_N_TD * 82
    mo = tdo + td_size
    po = mo + 32
    gco = po + 12
    gc_size = 256 * 16
    io = gco + gc_size
    slo = io + 36
    sldo = slo + 3 * 4
    so = sldo + len(V39_LITERAL_DATA)
    buf = bytearray(so + len(V39_STRINGS))

    struct.pack_into('<I', buf, 0, 0xFAB11BAF)
    struct.pack_into('<i', buf, 4, 39)
    tables = {
        'stringLiteral': (slo, 3 * 4, 3),
        'stringLiteralData': (sldo, len(V39_LITERAL_DATA), len(V39_LITERAL_DATA)),
        'string': (so, len(V39_STRINGS), len(V39_STRINGS)),
        'methods': (mo, 32, 1),
        'parameters': (po, 12, 1),
        'genericContainers': (gco, gc_size, 256),
        'typeDefinitions': (tdo, td_size, V39_N_TD),
        'images': (io, 36, 1),
    }
    off = 8
    for tname, _ in HEADER_TABLES:
        if 39 < V_TABLES_MIN.get(tname, 0):
            raise AssertionError('table missing in v39: %s' % tname)
        toff, tsize, tcount = tables.get(tname, (0, 0, 0))
        struct.pack_into('<3i', buf, off, toff, tsize, tcount)
        off += 12
    assert off == hdr_end, off

    # typedef 0: Foo.Ns, one method, no fields
    td = bytearray(82)
    struct.pack_into('<2I', td, 0, 1, 9)          # name, namespace
    struct.pack_into('<3i', td, 8, 1, -1, 2)      # byval, declaring, parent
    struct.pack_into('<h', td, 20, -1)            # generic container
    struct.pack_into('<i', td, 22, 0x10)          # flags
    struct.pack_into('<8i', td, 26, *([0] * 8))   # starts
    struct.pack_into('<8H', td, 58, 1, 0, 0, 0, 0, 0, 0, 0)  # method_count
    struct.pack_into('<2I', td, 74, 0, 0x02000001)
    buf[tdo:tdo + 82] = td

    md = bytearray(32)
    struct.pack_into('<I', md, 0, 5)              # name
    struct.pack_into('<h', md, 4, 0)              # declaring (td_w)
    struct.pack_into('<i', md, 6, SENTINEL_RT)    # return type
    struct.pack_into('<i', md, 10, SENTINEL_RP)   # return parameter token
    md[14] = 0                                     # parameter_start (param_w = 1)
    struct.pack_into('<H', md, 15, 0xFFFF)        # generic container (gc_w = 2)
    struct.pack_into('<I', md, 17, SENTINEL_TOKEN)
    struct.pack_into('<4H', md, 21, 0x10, 0, 3, 1)
    buf[mo:mo + 32] = md

    pd = bytearray(12)
    struct.pack_into('<2I', pd, 0, 1, SENTINEL_RP)
    struct.pack_into('<i', pd, 8, SENTINEL_RT)
    buf[po:po + 12] = pd

    im = bytearray(36)
    struct.pack_into('<2i', im, 0, 12, 0)         # name, assembly index
    struct.pack_into('<H', im, 8, 0)              # type start (td_w)
    struct.pack_into('<I', im, 10, V39_N_TD)      # type count
    struct.pack_into('<H', im, 14, 0)             # exported type start
    struct.pack_into('<I', im, 16, 0)             # exported type count
    struct.pack_into('<2i', im, 20, -1, 0x02000001)
    buf[io:io + 36] = im

    struct.pack_into('<3I', buf, slo, 0, 2, 7)    # literal boundaries
    buf[sldo:sldo + len(V39_LITERAL_DATA)] = V39_LITERAL_DATA
    buf[so:so + len(V39_STRINGS)] = V39_STRINGS
    return bytes(buf)


def test_v39_tables_and_widths(tmp_path):
    path = tmp_path / 'global-metadata.dat'
    path.write_bytes(_build_v39())

    m = Metadata(str(path))

    assert (m.td_w, m.gc_w, m.param_w, m.type_w) == (TD_W, GC_W, 1, 4)
    assert len(m.typedefs) == V39_N_TD
    t = m.typedefs[0]
    assert (t.name, t.namespace, t.byval, t.declaring, t.parent) == (
        'Foo', 'Ns', 1, -1, 2)
    assert (t.generic_container, t.flags, t.method_count) == (-1, 0x10, 1)
    assert (t.field_count, t.property_count, t.token) == (0, 0, 0x02000001)

    md = m.methods[0]
    assert (md.name, md.declaring, md.return_type) == ('Bar', 0, SENTINEL_RT)
    assert (md.parameter_start, md.generic_container) == (0, -1)
    assert (md.token, md.rid) == (SENTINEL_TOKEN, 1)  # rid = token & 0xFFFFFF
    assert (md.flags, md.is_static, md.slot, md.param_count) == (0x10, True, 3, 1)

    assert (m.params[0].name, m.params[0].type) == ('Foo', SENTINEL_RT)
    img = m.images[0]
    assert (img.name, img.type_start, img.type_count, img.entry_point) == (
        'asm.dll', 0, V39_N_TD, -1)


def test_v39_string_literals_use_boundaries(tmp_path):
    """v35+ stores one boundary offset per literal plus a terminator, so
    the last boundary is the pool size and there is no per-row length."""
    path = tmp_path / 'global-metadata.dat'
    path.write_bytes(_build_v39())

    m = Metadata(str(path))

    assert m.string_literals == [(2, 0), (5, 2)]
    assert [m.string_literal(i) for i in range(2)] == ['Hi', 'World']


def _v39_typedef_stride_from_widths(type_w, gc_w):
    """The v38+ typedef row is packed, so its stride follows the
    variable index widths instead of being a fixed 82.

    4 name + 4 namespace + 3*type_w (byval, declaring, parent)
    + gc_w (generic container) + 4 flags + 32 (8 starts)
    + 16 (8 counts) + 4 bitfield + 4 token."""
    return 4 + 4 + 3 * type_w + gc_w + 4 + 32 + 16 + 4 + 4


def test_v39_typedef_stride_follows_the_variable_widths():
    """82 is the Limbus answer (type_w 4, gc_w 2), not a constant.

    A file with <=255 generic containers narrows gc_w to 1 and the row
    to 81 bytes; type_w 2 shortens the three Type indexes.  Pin the
    formula and both endpoints, not just the Limbus-specific number."""
    assert _v39_typedef_stride_from_widths(4, 2) == 82   # Limbus Company
    assert _v39_typedef_stride_from_widths(4, 1) == 81   # <=255 containers
    assert _v39_typedef_stride_from_widths(2, 2) == 76   # type_w 2
    assert _v39_typedef_stride_from_widths(4, 4) == 84   # >65535 containers

    # The fixture above declares 256 generic containers, so gc_w is 2 and
    # its 82-byte rows are exactly the derived stride.
    assert GC_W == 2
