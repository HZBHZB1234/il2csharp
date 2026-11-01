"""fix 173: generic parameter constraints are recovered, not dropped.

Every generic parameter row carries a CLI GenericParameterAttributes word
and a range into one flat `genericParameterConstraints` TypeIndex array.
Nothing in the emitted tree used either, so a recovered
`WithCancellation<T>(AsyncInstantiateOperation<T>)` lost the
`where T : UnityEngine.Object` the source wrote -- and the compiler then
rejects the emitted file (CS0314/CS0452/CS0453). The same word also holds
CLI variance (`out`/`in`), which every `IUniTaskAsyncEnumerable<out T>`
declaration was missing.

The constraint table is a TypeIndex array like every other type index, so
v38+ packs its rows at the metadata's own width: Limbus types are 4 bytes
(byte-identical to the old fixed read) while a narrow v39 file is 2. The
tests below pin both layouts, then the rendered C# shapes -- including the
shapes C# refuses to compile, which must decline rather than print.
"""
import struct

from types import SimpleNamespace as NS

from il2cpp.emitter import Emitter
from il2cpp.metadata import HEADER_TABLES, V_TABLES_MIN, Metadata

# -- synthetic metadata ----------------------------------------------------

GP_NAMES = b'\x00T\x00U\x00'
GP_ROWS = [
    # (owner, name_off, constraints_start, constraints_count, num, flags)
    (0, 1, 0, 1, 0, 0x04),      # T : class
    (0, 3, 1, 2, 1, 0x18),      # U : struct, IFoo
]


def _build_v31():
    """A v31 file whose only populated tables are the generic ones."""
    strings = GP_NAMES
    gpo, gpc = 0, len(GP_ROWS) * 16
    cco, ccc = 0, 3 * 4
    tables = [(t, 0) for t, _ in HEADER_TABLES if 31 >= V_TABLES_MIN.get(t, 0)]
    off = 8
    head = {}
    for tname, _ in HEADER_TABLES:
        if 31 < V_TABLES_MIN.get(tname, 0):
            continue
        head[tname] = off
        off += 8
    gpo = off
    cco = gpo + gpc
    so = cco + ccc
    buf = bytearray(so + len(strings))
    struct.pack_into('<I', buf, 0, 0xFAB11BAF)
    struct.pack_into('<i', buf, 4, 31)
    for tname, toff in head.items():
        offset, size = 0, 0
        if tname == 'genericParameters':
            offset, size = gpo, gpc
        elif tname == 'genericParameterConstraints':
            offset, size = cco, ccc
        elif tname == 'string':
            offset, size = so, len(strings)
        struct.pack_into('<2i', buf, toff, offset, size)
    for k, (owner, nm, cs, cc, num, flags) in enumerate(GP_ROWS):
        struct.pack_into('<iIhhhH', buf, gpo + k * 16, owner, nm, cs, cc, num, flags)
    struct.pack_into('<3i', buf, cco, 7, 8, 9)
    buf[so:so + len(strings)] = strings
    return bytes(buf)


def _build_v39(narrow):
    """A v39 file with one counted generic parameter row.

    v38+ packs a TypeIndex row at the width its own table counts force,
    so `narrow` chooses the metadata's `type_w`: 2 (the survivors-roguelike
    fixture) or 4 (Limbus). The header's
    `genericParameterConstraintsCount` is what decides the constraint
    width, and it must win over the fallback.
    """
    type_w = 2 if narrow else 4
    hdr_end = 8 + 31 * 12
    # parameters: one row -> type_w follows the row size
    po = hdr_end
    psize = 8 + type_w
    # generic parameter row: owner(gc_w=1) + name(4) + cs/cc/num/flags(8)
    gpo = po + psize
    gp_row = 1 + 4 + 8
    gpc = 256                      # -> gc_w = 2 ... but one row: pc=1 -> gc_w 1
    gpo = po + psize
    gpc = gp_row
    cco = gpo + gpc
    n_cons = 3
    ccc = n_cons * type_w
    so = cco + ccc
    strings = b'\x00T\x00'
    buf = bytearray(so + len(strings))
    struct.pack_into('<I', buf, 0, 0xFAB11BAF)
    struct.pack_into('<i', buf, 4, 39)
    off = 8
    for tname, _ in HEADER_TABLES:
        if 39 < V_TABLES_MIN.get(tname, 0):
            raise AssertionError('table missing in v39: %s' % tname)
        offset, size, count = 0, 0, 0
        if tname == 'parameters':
            offset, size, count = po, psize, 1
        elif tname == 'genericParameters':
            offset, size, count = gpo, gpc, 1
        elif tname == 'genericParameterConstraints':
            offset, size, count = cco, ccc, n_cons
        elif tname == 'string':
            offset, size, count = so, len(strings), len(strings)
        struct.pack_into('<3i', buf, off, offset, size, count)
        off += 12
    assert off == hdr_end, off
    # one parameter row: name(4) + token(4) + type(type_w)
    struct.pack_into('<iI', buf, po, 1, 0x10000001)
    struct.pack_into('<H' if type_w == 2 else '<i', buf, po + 8, 5)
    # one generic parameter: owner(1) name(4) cs(2) cc(2) num(2) flags(2)
    struct.pack_into('<BIHhhH', buf, gpo, 0, 1, 0, n_cons, 0, 0x1C)
    for k, v in enumerate((11, 12, 13)):
        if type_w == 2:
            struct.pack_into('<H', buf, cco + k * type_w, v)
        else:
            struct.pack_into('<i', buf, cco + k * type_w, v)
    buf[so:so + len(strings)] = strings
    return bytes(buf)


def test_v31_constraint_table_parses(tmp_path):
    path = tmp_path / 'global-metadata.dat'
    path.write_bytes(_build_v31())

    m = Metadata(str(path))

    assert m.gp_constraints == [7, 8, 9]
    assert m.generic_param_constraints(0) == [7]
    assert m.generic_param_constraints(1) == [8, 9]
    assert m.generic_param_constraints(99) == []
    assert m.generic_param(0)[1] == 'T'
    assert m.generic_param(1)[5] == 0x18


def test_v39_narrow_constraints_are_packed_at_the_count_width(tmp_path):
    """A 4-byte read of the narrow table would land on the SECOND row's
    high half, giving every constraint a plausible-looking wrong index."""
    path = tmp_path / 'global-metadata.dat'
    path.write_bytes(_build_v39(narrow=True))

    m = Metadata(str(path))

    assert m.type_w == 2
    assert m.gp_constraints == [11, 12, 13]
    assert m.generic_param_constraints(0) == [11, 12, 13]


def test_v39_wide_constraints_keep_the_v31_shape(tmp_path):
    path = tmp_path / 'global-metadata.dat'
    path.write_bytes(_build_v39(narrow=False))

    m = Metadata(str(path))

    assert m.type_w == 4
    assert m.gp_constraints == [11, 12, 13]


# -- rendered C# -----------------------------------------------------------

T_CLASS = (0, (0x12 << 16))
T_VALUETYPE = (1, (0x12 << 16))
T_IFACE = (2, (0x12 << 16))
T_SEALED = (3, (0x12 << 16))
T_GENERIC_IFACE = (4, (0x15 << 16))
T_VAR = (5, (0x13 << 16))

NAMES = {
    0: 'System.Object',
    1: 'System.ValueType',
    2: 'NS.IFoo',
    3: 'System.String',
    4: 'System.IEquatable<T>',
    5: 'T',
}
# genericinst data is a POINTER to the Il2CppGenericClass; the fake
# `type_from_ptr` resolves it to the instantiated typedef's own tuple.
GENERICINST_TARGET = {4: T_IFACE}


def _td(flags):
    return NS(flags=flags, is_valuetype=False, is_enum=False, index=0,
              generic_container=-1)


def _emitter(gp_rows, constraints, types=(), tds=None):
    """An Emitter wired to exactly what `_where_clause` reads.

    `types` is a sparse {type index: tuple} map; the fake table is padded so
    an out-of-range row is the only way to miss.
    """
    sparse = dict(types)
    top = max(sparse) if sparse else -1
    table = [sparse.get(i, (99, 0)) for i in range(top + 1)]
    meta = NS(generic_parameters=gp_rows, gp_constraints=list(constraints),
              typedefs=tds or [_td(0x12), _td(0x11), _td(0x20),
                               _td(0x12 | 0x100), _td(0x20), _td(0x12)])
    # borrow the real row/ranged accessors
    meta.generic_param = lambda gi: (
        meta.generic_parameters[gi] if 0 <= gi < len(meta.generic_parameters)
        else None)
    meta.generic_param_constraints = lambda gi: (
        meta.gp_constraints[meta.generic_parameters[gi][2]:
                            meta.generic_parameters[gi][2]
                            + meta.generic_parameters[gi][3]]
        if 0 <= gi < len(meta.generic_parameters) else [])
    il = NS(types=table,
            _type_enum=lambda t: (t[1] >> 16) & 0xFF,
            type_name=lambda t, depth=0: NAMES.get(t[0], '?'),
            type_from_ptr=lambda v: GENERICINST_TARGET.get(v),
            # an Il2CppGenericClass pointer at file offset 4 holds the
            # instantiated typedef's tuple pointer (the fake resolves 4)
            bin=NS(va2off=lambda va: va,
                    d=bytes(4) + struct.pack('<Q', 4)))
    em = Emitter.__new__(Emitter)
    em.meta = meta
    em.il = il
    return em


def _gp(name, cs, cc, num=0, flags=0):
    return (0, name, cs, cc, num, flags)


def test_where_clause_spells_class_and_new():
    em = _emitter([_gp('T', 0, 0, flags=0x04 | 0x10)], [])
    assert em._where_clause([0]) == ' where T : class, new()'


def test_where_clause_struct_drops_the_implied_value_type_row():
    em = _emitter([_gp('T', 0, 1, flags=0x18)], [1], {1: T_VALUETYPE})
    assert em._where_clause([0]) == ' where T : struct'


def test_where_clause_interface_and_generic_interface():
    em = _emitter([_gp('T', 0, 2, flags=0x04)], [2, 4],
                  {2: T_IFACE, 4: T_GENERIC_IFACE})
    assert em._where_clause([0]) == ' where T : class, NS.IFoo, System.IEquatable<T>'


def test_where_clause_orders_the_base_class_before_interfaces():
    """CS0401: the class constraint must come first, whatever the row order."""
    em = _emitter([_gp('T', 0, 2)], [2, 3], {2: T_IFACE, 3: (3, (0x12 << 16))},
                  tds=[_td(0x12), _td(0x11), _td(0x20), _td(0x12), _td(0x20),
                       _td(0x12)])
    assert em._where_clause([0]) == ' where T : System.String, NS.IFoo'


def test_where_clause_declines_a_sealed_class_constraint():
    em = _emitter([_gp('T', 0, 1)], [3], {3: T_SEALED})
    assert em._where_clause([0]) == ''


def test_where_clause_declines_two_class_constraints():
    em = _emitter([_gp('T', 0, 2)], [0, 3], {0: T_CLASS, 3: T_SEALED})
    assert em._where_clause([0]) == ''


def test_where_clause_declines_an_unreadable_index():
    em = _emitter([_gp('T', 0, 1)], [77], {0: T_CLASS})
    assert em._where_clause([0]) == ''


def test_where_clause_spells_a_parameter_constraint():
    em = _emitter([_gp('U', 0, 1)], [5], {5: T_VAR})
    assert em._where_clause([0]) == ' where U : T'


def test_where_clause_is_empty_without_constraints():
    em = _emitter([_gp('T', 0, 0)], [])
    assert em._where_clause([0]) == ''
