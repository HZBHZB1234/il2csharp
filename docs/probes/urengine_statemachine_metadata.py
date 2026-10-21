"""The tree shows 0 `d__NNN` classes, but that regex may be wrong: the
emitter may sanitize `<>` out of identifiers.  Ask the METADATA directly
what the compiler-generated state machine types are called, then look for
them by their attributes instead of by name.

Ground truth: async/iterator methods carry
AsyncStateMachineAttribute / IteratorStateMachineAttribute, and their
state machine types are nested private classes whose name starts with '<'.
"""
import re
import sys

sys.path.insert(0, r'E:\desktop\work\LimbusDecompile\il2csharp')
from il2cpp import Metadata

GAME = r'C:\Program Files (x86)\Steam\steamapps\common\Limbus Company'
m = Metadata(GAME + r'\BepInEx\decrypted-metadata.dat')

# 1. Types whose name starts with '<' (compiler-generated nests)
odd = [t for t in m.typedefs if t.name.startswith('<')]
print('types whose name starts with "<":', len(odd))
from collections import Counter
pat = Counter()
for t in odd:
    pat[re.sub(r'\d+', 'N', t.name)[:40]] += 1
for k, v in pat.most_common(25):
    print('  %-42s %d' % (k, v))
print()

# 2. Names containing d__ or __state or MoveNext
for probe, label in ((r'd__\d+', 'name contains d__N'),
                     (r'__state', 'name contains __state'),
                     (r'MoveNext', 'name contains MoveNext'),
                     (r'SetStateMachine', 'name contains SetStateMachine')):
    hits = [t for t in m.typedefs if re.search(probe, t.name)]
    print('%-28s %d' % (label, len(hits)))
    for t in hits[:5]:
        print('     ', t.name, '|', t.namespace)
print()

# 3. Methods named MoveNext anywhere
mn = [x for x in m.methods if x.name == 'MoveNext']
print('methods named MoveNext:', len(mn))
for x in mn[:8]:
    td = m.typedefs[x.declaring] if 0 <= x.declaring < len(m.typedefs) else None
    print('   owner=%s  addr=%#x' % (td.name if td else '?', x.addr))
