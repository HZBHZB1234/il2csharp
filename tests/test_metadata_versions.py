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


# -- v38+ packed rows follow type_w, not a constant ----------------------
# The type index inside a parameter/field/event/method row is type_w wide,
# so the row shrinks when a file's indexes are narrow.  Only Limbus's
# shape (type_w 4) happened to equal the old hard-coded widths (12/12/24/
# 32).  survivors-roguelike-kit is v39 with type_w 2: its real rows are
# 10/10/22/30, and reading them at the Limbus constants shifted every row
# after the first, fragmenting names and starving the method-address map
# (11,427 of 94,205 methods resolved, 12%, instead of 89%).

def _v39_method_stride(type_w, td_w, param_w, gc_w):
    """4 name + td_w declaring + type_w return + 4 return-param token
    + param_w parameter start + gc_w generic container + 4 token
    + 8 (4 tail ushorts)."""
    return 4 + td_w + type_w + 4 + param_w + gc_w + 4 + 8


def _v39_param_stride(type_w):
    """4 name + type_w type + 4 token."""
    return 4 + type_w + 4


def _v39_event_stride(type_w):
    """4 name + type_w type + 4 add + 4 remove + 4 raise + 4 token."""
    return 4 + type_w + 16


def test_v39_row_strides_follow_the_variable_widths():
    """Pin the packed-row formulas at both endpoints, not just Limbus."""
    assert _v39_method_stride(4, 2, 4, 2) == 32   # Limbus Company
    assert _v39_method_stride(2, 2, 4, 2) == 30   # survivors (type_w 2)
    assert _v39_param_stride(4) == 12             # Limbus params/fields
    assert _v39_param_stride(2) == 10             # survivors params/fields
    assert _v39_event_stride(4) == 24             # Limbus events
    assert _v39_event_stride(2) == 22             # survivors events


def _build_v39_narrow():
    """A v39 file whose widths force type_w = 2 (the survivors shape).

    parametersSize/parametersCount = 10 implies type_w 2, so every packed
    row is narrower than the Limbus constants: methods 30, parameters 10,
    fields 10, events 22.  Two methods pin the stride (the second row is
    only reachable when the first row advances by 30, not 32)."""
    td_w = gc_w = 2
    type_w = 2
    n_td = 256
    n_methods = 2
    # parametersCount must exceed 65535 so param_w is 4 (survivors shape),
    # while parametersSize/parametersCount = 10 pins type_w to 2.
    n_params = 70000
    n_fields = 1
    n_events = 1

    hdr_end = 8 + 31 * 12
    tdo = hdr_end
    td_size = n_td * _v39_typedef_stride_from_widths(type_w, gc_w)
    mo = tdo + td_size
    m_stride = _v39_method_stride(type_w, td_w, 4, gc_w)
    m_size = n_methods * m_stride
    po = mo + m_size
    p_stride = _v39_param_stride(type_w)
    p_size = n_params * p_stride
    fo = po + p_size
    f_size = n_fields * p_stride
    eo = fo + f_size
    e_size = n_events * _v39_event_stride(type_w)
    ifo = eo + e_size
    n_interfaces = 2
    i_size = n_interfaces * type_w
    fdvo = ifo + i_size
    dv_stride = 4 + type_w + 4
    fdv_size = 2 * dv_stride
    pdvo = fdvo + fdv_size
    pdv_size = 1 * dv_stride
    gco = pdvo + pdv_size
    gc_size = n_td * 16
    so = gco + gc_size
    strings = b'\x00Foo\x00Bar\x00Baz\x00Ns\x00asm.dll\x00'
    buf = bytearray(so + len(strings))

    struct.pack_into('<I', buf, 0, 0xFAB11BAF)
    struct.pack_into('<i', buf, 4, 39)
    tables = {
        'string': (so, len(strings), len(strings)),
        'methods': (mo, m_size, n_methods),
        'parameters': (po, p_size, n_params),
        'fields': (fo, f_size, n_fields),
        'events': (eo, e_size, n_events),
        'interfaces': (ifo, i_size, n_interfaces),
        'fieldDefaultValues': (fdvo, fdv_size, 2),
        'parameterDefaultValues': (pdvo, pdv_size, 1),
        'genericContainers': (gco, gc_size, n_td),
        'typeDefinitions': (tdo, td_size, n_td),
    }
    off = 8
    for tname, _ in HEADER_TABLES:
        if 39 < V_TABLES_MIN.get(tname, 0):
            raise AssertionError('table missing in v39: %s' % tname)
        toff, tsize, tcount = tables.get(tname, (0, 0, 0))
        struct.pack_into('<3i', buf, off, toff, tsize, tcount)
        off += 12
    assert off == hdr_end

    td = bytearray(td_size)
    struct.pack_into('<2I', td, 0, 1, 9)
    struct.pack_into('<H', td, 8, 1)              # byval (type_w)
    struct.pack_into('<H', td, 8 + type_w, 0xFFFF)  # declaring = -1
    struct.pack_into('<H', td, 8 + 2 * type_w, 0xFFFF)  # parent = -1
    gc_off = 8 + 3 * type_w
    struct.pack_into('<H', td, gc_off, 0xFFFF)    # generic container = -1
    flags_off = gc_off + gc_w
    struct.pack_into('<i', td, flags_off, 0x10)
    starts_off = flags_off + 4
    struct.pack_into('<8i', td, starts_off, 0, 0, 0, 0, 0, 0, 0, 0)
    counts_off = starts_off + 32
    struct.pack_into('<8H', td, counts_off, n_methods, n_fields, 0, 0, 0, 0, 0, 0)
    buf[tdo:tdo + td_size] = td

    # method 0 -> 'Bar', method 1 -> 'Baz'.  If the reader advances 32
    # instead of 30 the second name is garbage.
    for i, (name_idx, token) in enumerate(((5, SENTINEL_TOKEN), (9, 0x06000002))):
        md = bytearray(m_stride)
        b = mo + i * m_stride
        struct.pack_into('<I', buf, b, name_idx)
        p = b + 4
        struct.pack_into('<H', buf, p, 0)          # declaring (td_w)
        p += td_w
        struct.pack_into('<H', buf, p, SENTINEL_RT)  # return type (type_w)
        p += type_w
        struct.pack_into('<i', buf, p, SENTINEL_RP)
        p += 4
        struct.pack_into('<I', buf, p, i)          # parameter start (param_w)
        p += 4
        struct.pack_into('<H', buf, p, 0xFFFF)     # generic container
        p += gc_w
        struct.pack_into('<I', buf, p, token)
        p += 4
        struct.pack_into('<4H', buf, p, 0x10, 0, 3, 1)

    for i in range(n_params):
        b = po + i * p_stride
        struct.pack_into('<I', buf, b, 1)                  # 'Foo'
        struct.pack_into('<I', buf, b + 4, SENTINEL_RP)    # token
        struct.pack_into('<H', buf, b + 8, SENTINEL_RT)    # type (type_w)

    b = fo
    struct.pack_into('<I', buf, b, 13)             # 'Ns'
    struct.pack_into('<H', buf, b + 4, SENTINEL_RT)   # type (type_w)
    struct.pack_into('<I', buf, b + 4 + type_w, SENTINEL_TOKEN)

    b = eo
    struct.pack_into('<I', buf, b, 5)              # 'Bar'
    struct.pack_into('<H', buf, b + 4, SENTINEL_RT)
    struct.pack_into('<i', buf, b + 4 + type_w, 0)
    struct.pack_into('<i', buf, b + 8 + type_w, 0)
    struct.pack_into('<i', buf, b + 12 + type_w, 0)
    struct.pack_into('<I', buf, b + 16 + type_w, SENTINEL_TOKEN)

    # interfaces table: two TypeDef indices, each type_w wide.  A fixed
    # 4-byte read turns this into one bogus row (0x00090007).
    for i, type_index in enumerate((7, 9)):
        struct.pack_into('<H', buf, ifo + i * type_w, type_index)

    # field default row 0 (index 3, type, data 11) and row 1 (index 4, ...)
    for i, (idx, data) in enumerate(((3, 11), (4, 12))):
        b = fdvo + i * dv_stride
        struct.pack_into('<i', buf, b, idx)
        struct.pack_into('<H', buf, b + 4, SENTINEL_RT)
        struct.pack_into('<i', buf, b + 4 + type_w, data)
    # parameter default row 0 at its own offset
    b = pdvo
    struct.pack_into('<i', buf, b, 7)
    struct.pack_into('<H', buf, b + 4, SENTINEL_RT)
    struct.pack_into('<i', buf, b + 4 + type_w, 21)

    buf[so:so + len(strings)] = strings
    return bytes(buf)


def test_v39_narrow_rows_do_not_shift(tmp_path):
    """The narrow file must parse every table at its own stride.

    A hard 32/12/12/24 read parses one method, zero fields, one bogus
    parameter and a misaligned event, and the IndexError it plants only
    shows up much later in a lift."""
    path = tmp_path / 'global-metadata.dat'
    path.write_bytes(_build_v39_narrow())

    m = Metadata(str(path))

    assert m.type_w == 2
    assert len(m.methods) == 2
    assert [md.name for md in m.methods] == ['Bar', 'Baz']
    assert [md.rid for md in m.methods] == [1, 2]
    assert all(md.return_type == SENTINEL_RT for md in m.methods)
    assert m.methods[1].token == 0x06000002

    assert len(m.params) == 70000
    assert all(p.name == 'Foo' and p.type == SENTINEL_RT and p.token == SENTINEL_RP
               for p in m.params)
    assert len(m.fields) == 1
    assert (m.fields[0].name, m.fields[0].type) == ('Ns', SENTINEL_RT)
    assert len(m.events) == 1
    assert (m.events[0][0], m.events[0][5]) == (5, SENTINEL_TOKEN)

    # The interfaces table is also packed at type_w: a fixed 4-byte read
    # halves a narrow table and leaves the tail out of range (survivors'
    # header emission raised IndexError on 54 types).
    assert m.interfaces == [7, 9]

    # Default-value tables use the same packed row; a fixed 12 read drops
    # the tail of a narrow file (survivors parsed 8,450 of 12,629).
    assert len(m.field_default_values) == 2
    assert m.field_default_values[3] == (SENTINEL_RT, 11)
    assert m.field_default_values[4] == (SENTINEL_RT, 12)
    assert len(m.param_default_values) == 1
    assert m.param_default_values[7] == (SENTINEL_RT, 21)
