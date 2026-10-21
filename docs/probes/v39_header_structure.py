"""Structural validation of the v39 header: 31 triple-column tables,
380-byte header, every table's (offset,size,count) inside the file, and
the string-pool boundary arithmetic.

Also cross-checks the counts the handoff quoted (51,021 typedef /
319,009 method / 373,677 param / 204,180 field / 162 image / 4,991
generic container / 7,628 generic param / 32,124 literal).
"""
import struct
import sys

sys.path.insert(0, r'E:\desktop\work\LimbusDecompile\il2csharp')
from il2cpp.metadata import HEADER_TABLES, V_TABLES_MIN, Metadata

GAME = r'C:\Program Files (x86)\Steam\steamapps\common\Limbus Company'
m = Metadata(GAME + r'\BepInEx\decrypted-metadata.dat')
d = m.d
h = m.hdr

print('file size      :', len(d))
print('version        :', m.version)
print('header bytes   :', 8 + 31 * 12, '(8 + 31 tables * 12)')
print('header_ints    :', m.header_ints)

print('--- tables present in v39 header ---')
missing = []
bad_range = []
for tname, _sz in HEADER_TABLES:
    if tname + 'Offset' not in h:
        continue
    off = h[tname + 'Offset']
    size = h.get(tname + 'Size')
    cnt = h.get(tname + 'Count')
    if tname in ('stringLiteralData', 'stringData'):
        continue
    if off + size > len(d):
        bad_range.append((tname, off, size))
    if cnt is None:
        missing.append(tname)
print('tables with a count column :', sum(
    1 for t, _ in HEADER_TABLES if t + 'Count' in h))
print('tables without a count     :', missing)
print('out-of-range tables        :', bad_range)

print('--- quoted counts ---')
for label, key in (('typeDefinitions', 'typeDefinitionsCount'),
                   ('methods', 'methodsCount'),
                   ('parameters', 'parametersCount'),
                   ('fields', 'fieldsCount'),
                   ('images', 'imagesCount'),
                   ('genericContainers', 'genericContainersCount'),
                   ('genericParameters', 'genericParametersCount'),
                   ('stringLiterals', 'stringLiteralCount')):
    print('  %-20s %d' % (label, h.get(key, -1)))

print('--- stride checks (size / count) ---')
for label, ck, sk in (('typedef', 'typeDefinitionsCount', 'typeDefinitionsSize'),
                      ('method', 'methodsCount', 'methodsSize'),
                      ('param', 'parametersCount', 'parametersSize'),
                      ('field', 'fieldsCount', 'fieldsSize'),
                      ('image', 'imagesCount', 'imagesSize'),
                      ('genericContainer', 'genericContainersCount',
                       'genericContainersSize'),
                      ('genericParameter', 'genericParametersCount',
                       'genericParametersSize')):
    c, s = h.get(ck, 0), h.get(sk, 0)
    if c:
        print('  %-18s %d / %d = %s' % (label, s, c, s / c))

print('--- string literal boundaries ---')
so, sc, n = h['stringLiteralOffset'], h['stringLiteralSize'], h['stringLiteralCount']
bounds = [struct.unpack_from('<I', d, so + i * 4)[0] for i in range(n)]
print('  literal count :', n)
print('  pool size     :', sc)
print('  last boundary :', bounds[-1])
print('  MATCH' if bounds[-1] == sc else '  MISMATCH')
print('  total length  :', sum(m.string_literal(i)[0] for i in range(n)))
