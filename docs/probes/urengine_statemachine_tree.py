"""Measure the real cost of NOT modelling async/coroutine state machines.

A C# async method or iterator compiles to a compiler-generated class
(AsyncStateMachineAttribute / IteratorStateMachineAttribute) named like
`<MethodName>d__123` holding a `<>1__state` field and a MoveNext method
whose body is a `switch (state)` dispatcher.

If il2csharp does not recognise these, the output shows the state machine
as a plain class with a big switch -- which is what the tree should be
full of.  Count:
  * how many `d__NNN` types exist in the tree,
  * how many have a `<>1__state` field,
  * how many have a MoveNext method,
  * how many of those MoveNext bodies contain a switch on the state field.
"""
import io
import os
import re
import sys
from collections import Counter

ROOT = (sys.argv[1] if len(sys.argv) > 1 else
        r'E:\desktop\work\LimbusDecompile\il2csharp\limbus_out1')

d_pat = re.compile(r'class\s+<([A-Za-z_]\w*)>d__(\d+)')
state_pat = re.compile(r'<>\d+__state')
move_pat = re.compile(r'MoveNext')

n_files = 0
n_sm = 0
n_state_field = 0
n_move = 0
n_switch_on_state = 0
examples = []

for dp, _dirs, fs in os.walk(ROOT):
    for f in fs:
        if not f.endswith('.cs'):
            continue
        p = os.path.join(dp, f)
        n_files += 1
        try:
            d = io.open(p, 'rb').read().decode('utf-8', 'replace')
        except Exception:
            continue
        if not d_pat.search(d):
            continue
        n_sm += 1
        has_state = bool(state_pat.search(d))
        if has_state:
            n_state_field += 1
        if move_pat.search(d):
            n_move += 1
            # a MoveNext whose body switches on the state field
            if re.search(r'switch\s*\([^)]*__state', d):
                n_switch_on_state += 1
                if len(examples) < 3:
                    examples.append((f, has_state))

print('files scanned            :', n_files)
print('state-machine classes    :', n_sm)
print('  with <>N__state field  :', n_state_field)
print('  with MoveNext          :', n_move)
print('  switch on state field  :', n_switch_on_state)
print('examples                 :', examples)
