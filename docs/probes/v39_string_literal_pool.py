"""The handoff says "32,124 literals total 930,512 bytes, exactly equal to
the pool size".  The probe disproves that: stringLiteralSize is 128,500,
not 930,512.  Work out what the two numbers really mean.

Hypotheses:
  (a) stringLiteralSize is a *container/alignment* size and the literal
      data pool is a separate region whose size equals bounds[-1].
  (b) The boundaries are not byte offsets into the data pool but something
      else (e.g. offsets scaled, or into a different table).

Test: the data offset for literal i should point at real literal bytes.
Check the handoff's own quoted strings ('KEY: ', 'Effects that animate...')
and see whether they sit at stringLiteralDataOffset + bounds[i].
"""
import struct
import sys

sys.path.insert(0, r'E:\desktop\work\LimbusDecompile\il2csharp')
from il2cpp.metadata import Metadata

GAME = r'C:\Program Files (x86)\Steam\steamapps\common\Limbus Company'
m = Metadata(GAME + r'\BepInEx\decrypted-metadata.dat')
d = m.d
h = m.hdr

so = h['stringLiteralOffset']
sc = h['stringLiteralSize']
sldo = h['stringLiteralDataOffset']
slds = h['stringLiteralDataSize']
n = h['stringLiteralCount']
bounds = [struct.unpack_from('<I', d, so + i * 4)[0] for i in range(n)]

print('stringLiteralOffset      : %#x' % so)
print('stringLiteralSize        : %d (%#x)' % (sc, sc))
print('stringLiteralDataOffset  : %#x' % sldo)
print('stringLiteralDataSize    : %d (%#x)' % (slds, slds))
print('boundary entries         :', n)
print('bounds[-1] (max)         :', bounds[-1])
print()
print('stringLiteralSize / 4    :', sc / 4, '(looks like the boundary array itself)')
print('stringLiteralDataSize    :', slds)
print('bounds[-1] == stringLiteralDataSize ?', bounds[-1] == slds)
print()
# Where does the boundary array actually live?
print('so + n*4 = %#x ; sldo = %#x ; delta = %d' % (so + n * 4, sldo,
                                                   sldo - (so + n * 4)))
print()
# Read literals directly from the data pool at sldo + bounds[i]
print('--- literals read from stringLiteralDataOffset + bounds[i] ---')
ok = 0
tested = 0
for i in (1, 1000, 16000, 32122):
    L = bounds[i + 1] - bounds[i]
    raw = d[sldo + bounds[i]: sldo + bounds[i] + L]
    tested += 1
    try:
        s = raw.decode('utf-8')
    except Exception as e:
        s = '<decode error %s>' % e
    print('  [%5d] len=%d  %r' % (i, L, s[:50]))
    if len(s) < 200:
        ok += 1
print()
print('--- handoff-quoted strings ---')
for probe in (b'KEY: ', b'Effects that animate'):
    pos = 0
    while True:
        j = d.find(probe, pos)
        if j < 0:
            break
        pos = j + 1
        rel = j - sldo
        if 0 <= rel <= bounds[-1]:
            print('  %r at data offset %d (in pool)' % (probe, rel))
        else:
            print('  %r at file offset %#x (outside the data pool)' % (probe, j))
