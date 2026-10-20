from il2cpp.prelude import *  # noqa: F401,F403
from il2cpp.common import i32, u32

HEADER_TABLES = [
    # (name, struct_size or None)
    ('stringLiteral', 8), ('stringLiteralData', 1), ('string', 1),
    ('events', 24), ('properties', 20), ('methods', 32),
    ('parameterDefaultValues', 12), ('fieldDefaultValues', 12),
    ('fieldAndParameterDefaultValueData', 1), ('fieldMarshaledSizes', 8),
    ('parameters', 12), ('fields', 12), ('genericParameters', 12),
    ('genericParameterConstraints', 4),
    ('genericContainers', 16), ('nestedTypes', 4), ('interfaces', 4),
    ('vtableMethods', 4), ('interfaceOffsets', 8),
    ('typeDefinitions', None),  # version dependent
    ('images', 40), ('assemblies', None),
    ('fieldRefs', 8), ('referencedAssemblies', 4),
    ('attributeData', 1), ('attributeDataRange', 8),
    ('unresolvedVirtualCallParameterTypes', 4),
    ('unresolvedVirtualCallParameterRanges', 8),
    ('windowsRuntimeTypeNames', 8), ('windowsRuntimeStrings', 1),
    ('exportedTypeDefinitions', 4),
]
# tables present per metadata version (all >= 27.2 for our targets)
V_TABLES_MIN = {
    'genericParameterConstraints': 0,
    'fieldRefs': 19, 'referencedAssemblies': 20,
    'unresolvedVirtualCallParameterTypes': 22,
    'unresolvedVirtualCallParameterRanges': 22,
    'windowsRuntimeTypeNames': 23, 'windowsRuntimeStrings': 27,
    'exportedTypeDefinitions': 24,
    'attributeData': 29, 'attributeDataRange': 29,
}


@dataclass
class TypeDef:
    index: int
    name: str
    namespace: str
    byval: int
    declaring: int
    parent: int
    element: int
    generic_container: int
    flags: int
    field_start: int
    method_start: int
    event_start: int
    property_start: int
    nested_start: int
    interfaces_start: int
    vtable_start: int
    iface_offsets_start: int
    method_count: int
    property_count: int
    field_count: int
    event_count: int
    nested_count: int
    vtable_count: int
    interfaces_count: int
    iface_offsets_count: int
    bitfield: int
    token: int

    @property
    def is_valuetype(self): return bool(self.bitfield & 1)
    @property
    def is_enum(self): return bool(self.bitfield & 2)
    @property
    def has_cctor(self): return bool(self.bitfield & 8)


@dataclass
class MethodDef:
    index: int
    name: str
    declaring: int
    return_type: int
    parameter_start: int
    generic_container: int
    token: int
    flags: int
    iflags: int
    slot: int
    param_count: int
    image: int = -1
    addr: int = 0

    @property
    def is_static(self): return bool(self.flags & 0x10)
    @property
    def rid(self): return self.token & 0xFFFFFF


@dataclass
class FieldDef:
    name: str
    type: int
    token: int


@dataclass
class ParamDef:
    name: str
    token: int
    type: int


@dataclass
class ImageDef:
    name: str
    assembly_index: int
    type_start: int
    type_count: int
    entry_point: int
    token: int


class Metadata:
    def __init__(self, path: str):
        self.path = path
        self.d = open(path, 'rb').read()
        self.version = i32(self.d, 4)
        if u32(self.d, 0) != 0xFAB11BAF:
            raise ValueError('not a global-metadata.dat file: %s' % path)
        if not (24 <= self.version <= 39):
            raise ValueError('unsupported metadata version %d' % self.version)
        self.v31 = self.version >= 31
        self.v35 = self.version >= 35
        self.v38 = self.version >= 38
        self._parse_header()
        self._parse_tables()

    # -- header -------------------------------------------------------------
    def _parse_header(self):
        d = self.d
        self.hdr = {}
        self.hdr['sanity'] = u32(d, 0)
        self.hdr['version'] = i32(d, 4)
        off = 8
        for name, _ in HEADER_TABLES:
            lo = V_TABLES_MIN.get(name, 0)
            if self.version < lo:
                continue
            self.hdr[name + 'Offset'] = i32(d, off)
            self.hdr[name + 'Size'] = i32(d, off + 4)
            if self.v38:
                self.hdr[name + 'Count'] = i32(d, off + 8)
                off += 12
            else:
                off += 8
        self.header_ints = off // 4

    def toff(self, table): return self.hdr[table + 'Offset']
    def tsize(self, table): return self.hdr[table + 'Size']

    @staticmethod
    def _vw(count: int) -> int:
        if count <= 0xFF:
            return 1
        if count <= 0xFFFF:
            return 2
        return 4

    def _read_vw(self, off: int, width: int) -> int:
        if width == 1:
            v = self.d[off]
            return -1 if v == 0xFF else v
        if width == 2:
            v = struct.unpack_from('<H', self.d, off)[0]
            return -1 if v == 0xFFFF else v
        return i32(self.d, off)

    # -- tables ---------------------------------------------------------------
    def _parse_tables(self):
        d, h = self.d, self.hdr
        self.string_off = h['stringOffset']
        self.string_size = h['stringSize']
        self._str_cache: Dict[int, str] = {}

        # v38+ variable-width index sizes. The widths are derived from the
        # table counts, exactly like the runtime's metadata reader.
        if self.v38:
            self.td_w = self._vw(h['typeDefinitionsCount'])
            self.gc_w = self._vw(h['genericContainersCount'])
            self.param_w = self._vw(h['parametersCount'])
            pc = h['parametersCount']
            self.type_w = (h['parametersSize'] // pc - 8) if pc else 4
            if self.type_w not in (1, 2, 4):
                self.type_w = 4

        # string literals: v35+ drops the per-row length and stores the
        # sorted string pool as a boundary array (count = strings + 1).
        so, sc = h['stringLiteralOffset'], h['stringLiteralSize']
        if self.v35:
            n = h.get('stringLiteralCount', sc // 4)
            bounds = [u32(d, so + i * 4) for i in range(n)]
            self.string_literals: List[Tuple[int, int]] = [
                (bounds[i + 1] - bounds[i], bounds[i])
                for i in range(max(0, n - 1))]
        else:
            self.string_literals: List[Tuple[int, int]] = [
                (u32(d, so + i * 8), u32(d, so + i * 8 + 4)) for i in range(sc // 8)]

        # images
        io, ic = h['imagesOffset'], h['imagesSize']
        self.images: List[ImageDef] = []
        if self.v38:
            for i in range(h['imagesCount']):
                b = io + i * 36
                p = b + 8
                type_start = self._read_vw(p, self.td_w); p += self.td_w
                type_count = u32(d, p); p += 4
                p += self.td_w + 4          # exportedTypeStart/Count
                entry_point = i32(d, p); p += 4
                token = u32(d, p)
                self.images.append(ImageDef(
                    self.getstr(u32(d, b)), i32(d, b + 4), type_start,
                    type_count, entry_point, token))
        else:
            for i in range(ic // 40):
                b = io + i * 40
                self.images.append(ImageDef(
                    self.getstr(u32(d, b)), i32(d, b + 4), i32(d, b + 8),
                    u32(d, b + 12), i32(d, b + 24), u32(d, b + 28)))

        # type definitions: v38+ uses variable-width indices and drops
        # byref/element; v31 row is 88 bytes (84 before 24.2).
        tdo = h['typeDefinitionsOffset']
        self.typedefs: List[TypeDef] = []
        if self.v38:
            n = h['typeDefinitionsCount']
            # The row is packed, so its stride follows the variable
            # widths: 4 name + 4 namespace + 3*type_w (byval, declaring,
            # parent) + gc_w (generic container) + 4 flags + 32 starts +
            # 16 counts + 4 bitfield + 4 token.  Limbus is 82
            # (type_w 4, gc_w 2); a <=255-container file is 81.
            td_stride = 4 + 4 + 3 * self.type_w + self.gc_w + 4 + 32 + 16 + 4 + 4
            for i in range(n):
                b = tdo + i * td_stride
                p = b + 8
                byval = self._read_vw(p, self.type_w); p += self.type_w
                decl = self._read_vw(p, self.type_w); p += self.type_w
                parent = self._read_vw(p, self.type_w); p += self.type_w
                generic = self._read_vw(p, self.gc_w); p += self.gc_w
                flags = u32(d, p); p += 4
                starts = struct.unpack_from('<8i', d, p); p += 32
                counts = struct.unpack_from('<8H', d, p); p += 16
                self.typedefs.append(TypeDef(
                    i, self.getstr(u32(d, b)), self.getstr(u32(d, b + 4)),
                    byval, decl, parent, -1, generic, flags,
                    starts[0], starts[1], starts[2], starts[3], starts[4],
                    starts[5], starts[6], starts[7],
                    counts[0], counts[1], counts[2], counts[3],
                    counts[4], counts[5], counts[6], counts[7],
                    u32(d, p), u32(d, p + 4)))
        else:
            stride = 88 if self.version >= 24.2 else 84
            n = h['typeDefinitionsSize'] // stride
            for i in range(n):
                b = tdo + i * stride
                f = struct.unpack_from('<16i', d, b)
                counts = struct.unpack_from('<8H', d, b + 64)
                self.typedefs.append(TypeDef(
                    i, self.getstr(f[0]), self.getstr(f[1]), f[2], f[3], f[4], f[5],
                    f[6], u32(d, b + 28), f[8], f[9], f[10], f[11], f[12], f[13],
                    f[14], f[15], counts[0], counts[1], counts[2], counts[3],
                    counts[4], counts[5], counts[6], counts[7],
                    u32(d, b + 80), u32(d, b + 84)))

        # methods: v31 adds returnParameterToken; v38+ uses variable-width
        # declaring/return/parameter indices and a 32-byte row.
        mo, mc = h['methodsOffset'], h['methodsSize']
        self.methods: List[MethodDef] = []
        if self.v38:
            nm = h['methodsCount']
            for i in range(nm):
                b = mo + i * 32
                p = b + 4
                decl = self._read_vw(p, self.td_w); p += self.td_w
                rtok = self._read_vw(p, self.type_w); p += self.type_w
                rptok = i32(d, p); p += 4
                pstart = self._read_vw(p, self.param_w); p += self.param_w
                gci = self._read_vw(p, self.gc_w); p += self.gc_w
                token = u32(d, p); p += 4
                tail = struct.unpack_from('<4H', d, p)
                self.methods.append(MethodDef(
                    i, self.getstr(u32(d, b)), decl, rtok, pstart, gci,
                    token, tail[0], tail[1], tail[2], tail[3]))
        else:
            mstride = 36 if self.v31 else 32
            nm = mc // mstride
            for i in range(nm):
                b = mo + i * mstride
                if self.v31:
                    nameI, decl, rtok, _rp, pstart, gci, token = struct.unpack_from('<7i', d, b)
                    tail = struct.unpack_from('<4H', d, b + 28)
                else:
                    nameI, decl, rtok, pstart, gci, token = struct.unpack_from('<6i', d, b)
                    tail = struct.unpack_from('<4H', d, b + 24)
                self.methods.append(MethodDef(
                    i, self.getstr(nameI), decl, rtok, pstart, gci,
                    u32(d, b + 24 if self.v31 else b + 20), tail[0], tail[1], tail[2], tail[3]))

        # parameters / fields / properties / events
        po, pc = h['parametersOffset'], h['parametersSize']
        self.params: List[ParamDef] = [
            ParamDef(self.getstr(u32(d, po + i * 12)), u32(d, po + i * 12 + 4), i32(d, po + i * 12 + 8))
            for i in range(pc // 12)]
        fo, fc = h['fieldsOffset'], h['fieldsSize']
        self.fields: List[FieldDef] = [
            FieldDef(self.getstr(u32(d, fo + i * 12)), i32(d, fo + i * 12 + 4), u32(d, fo + i * 12 + 8))
            for i in range(fc // 12)]
        pro, prc = h['propertiesOffset'], h['propertiesSize']
        self.properties = [struct.unpack_from('<5i', d, pro + i * 20) for i in range(prc // 20)]
        eo, ec = h['eventsOffset'], h['eventsSize']
        self.events = [struct.unpack_from('<6i', d, eo + i * 24) for i in range(ec // 24)]

        # generic containers / parameters
        gco, gcc = h['genericContainersOffset'], h['genericContainersSize']
        self.generic_containers = [struct.unpack_from('<4i', d, gco + i * 16) for i in range(gcc // 16)]
        gpo, gpc = h['genericParametersOffset'], h['genericParametersSize']
        self.generic_parameters = []
        if self.v38:
            for i in range(h['genericParametersCount']):
                b = gpo + i * 14
                owner = self._read_vw(b, self.gc_w)
                name = self.getstr(u32(d, b + self.gc_w))
                cs, cc, num, flags = struct.unpack_from('<hhHH', d, b + self.gc_w + 4)
                self.generic_parameters.append((owner, name, cs, cc, num, flags))
        else:
            gp_stride = 16 if self.version >= 24.2 else 12
            for i in range(gpc // gp_stride):
                b = gpo + i * gp_stride
                owner = i32(d, b)
                name = self.getstr(u32(d, b + 4))
                if gp_stride == 16:
                    cs, cc, num, flags = struct.unpack_from('<hhHH', d, b + 8)
                else:
                    cs, cc, num, flags = struct.unpack_from('<iiHH', d, b + 8)
                self.generic_parameters.append((owner, name, cs, cc, num, flags))

        # misc index tables
        nto, ntc = h['nestedTypesOffset'], h['nestedTypesSize']
        self.nested_types = [i32(d, nto + i * 4) for i in range(ntc // 4)]
        ifo, ifc = h['interfacesOffset'], h['interfacesSize']
        self.interfaces = [i32(d, ifo + i * 4) for i in range(ifc // 4)]
        vto, vtc = h['vtableMethodsOffset'], h['vtableMethodsSize']
        self.vtable_methods = [u32(d, vto + i * 4) for i in range(vtc // 4)]

        # default values
        fdvo, fdvc = h['fieldDefaultValuesOffset'], h['fieldDefaultValuesSize']
        self.field_default_values = {
            i32(d, fdvo + i * 12): (i32(d, fdvo + i * 12 + 4), i32(d, fdvo + i * 12 + 8))
            for i in range(fdvc // 12)}
        pdvo, pdvc = h['parameterDefaultValuesOffset'], h['parameterDefaultValuesSize']
        self.param_default_values = {
            i32(d, pdvo + i * 12): (i32(d, pdvo + i * 12 + 4), i32(d, pdvo + i * 12 + 8))
            for i in range(pdvc // 12)}
        self.dv_off = h['fieldAndParameterDefaultValueDataOffset']

        # per-type method/field lookup accelerators
        self.methods_by_type: Dict[int, List[int]] = {}
        for i, m in enumerate(self.methods):
            if m.declaring >= 0:
                self.methods_by_type.setdefault(m.declaring, []).append(i)

    def getstr(self, idx: int) -> str:
        if idx in self._str_cache:
            return self._str_cache[idx]
        if not (0 <= idx < self.string_size):
            return ''
        e = self.d.index(b'\x00', self.string_off + idx)
        s = self.d[self.string_off + idx:e].decode('utf-8', 'replace')
        self._str_cache[idx] = s
        return s

    def string_literal(self, idx: int) -> str:
        if not (0 <= idx < len(self.string_literals)):
            return ''
        ln, do = self.string_literals[idx]
        return self.d[self.hdr['stringLiteralDataOffset'] + do:
                      self.hdr['stringLiteralDataOffset'] + do + ln].decode('utf-8', 'replace')

    def method_params(self, m: MethodDef) -> List[ParamDef]:
        return self.params[m.parameter_start:m.parameter_start + m.param_count]

    def type_fields(self, t: TypeDef) -> List[int]:
        return list(range(t.field_start, t.field_start + t.field_count))

    def type_methods(self, t: TypeDef) -> List[int]:
        return list(range(t.method_start, t.method_start + t.method_count))


# ----------------------------------------------------------------------------
# executable binaries
# ----------------------------------------------------------------------------
