"""Tree-level Roslyn census: the whole emitted tree in ONE csc run.

The per-image gate (tools/compile_gate.py) compiles each image
standalone, so cross-image references surface as CS0246/CS0656 noise
and -- without mscorlib -- every `object` use scores CS0518. The
emitted tree self-hosts its core types (mscorlib's emitted source
defines System.Object and friends), so one compilation over all .cs
files has full reference closure: the error population is the real
binding-tier population. Validated on the v39b20 tree: 36,603 files,
one csc run, 52 s, zero CS0518, zero CS0101 duplicate-type warnings
(no cross-image collisions at this scale).

Usage: python gate_tree.py --tree <tree> [--out report.json]
         [--csc-dll PATH] [--timeout SEC]
Exit: 0 iff zero syntax errors, 1 on syntax errors, 2 on tool errors.
"""
import argparse
import json
import os
import subprocess
import sys
import tempfile
import time

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from compile_gate import ERR_RX, find_csc, iter_sources


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--tree', required=True)
    ap.add_argument('--out', default=None, help='write the full JSON report')
    ap.add_argument('--csc-dll', default=None)
    ap.add_argument('--timeout', type=int, default=3600)
    args = ap.parse_args()
    if not os.path.isdir(args.tree):
        print('no such tree: %s' % args.tree)
        return 2
    csc = find_csc(args.csc_dll)
    if csc is None:
        print('no compiler found')
        return 2
    sources = iter_sources(args.tree)
    if not sources:
        print('no .cs files under %s' % args.tree)
        return 2
    rsp = None
    out_dll = None
    t0 = time.time()
    try:
        fd, rsp = tempfile.mkstemp(prefix='gatetree_', suffix='.rsp')
        with os.fdopen(fd, 'w', encoding='utf-8') as f:
            for s in sources:
                f.write('"%s"\n' % s)
        fd2, out_dll = tempfile.mkstemp(prefix='gatetreeout_', suffix='.dll')
        os.close(fd2)
        cmd = (['dotnet', csc] if csc.lower().endswith('csc.dll') else [csc]) + \
              ['/t:library', '/nologo', '/unsafe', '/langversion:latest',
               '/out:' + out_dll, '@' + rsp]
        pr = subprocess.run(cmd, capture_output=True, text=True,
                            encoding='utf-8', errors='replace',
                            timeout=args.timeout)
        text = (pr.stdout or '') + '\n' + (pr.stderr or '')
    except subprocess.TimeoutExpired:
        print('compiler timeout after %ds' % args.timeout)
        return 2
    finally:
        for p in (rsp, out_dll):
            try:
                if p and os.path.isfile(p):
                    os.remove(p)
            except Exception:
                pass
    codes = {}
    dupes = 0
    for ln in text.splitlines():
        m = ERR_RX.match(ln.strip())
        if not m or m.group(4) != 'error':
            if 'CS0101' in ln:
                dupes += 1
            continue
        codes[m.group(5)] = codes.get(m.group(5), 0) + 1
    total = sum(codes.values())
    syntax = sum(n for c, n in codes.items()
                 if 1000 <= int(c[2:]) < 2000)
    top = sorted(codes.items(), key=lambda kv: (-kv[1], kv[0]))[:30]
    print('%s: %d files, total=%d syntax=%d binding=%d dupes=%d in %.0fs'
          % (args.tree, len(sources), total, syntax, total - syntax,
             dupes, time.time() - t0))
    for c, n in top:
        print('  %s x%d' % (c, n))
    if args.out:
        with open(args.out, 'w', encoding='utf-8') as f:
            json.dump({'kind': 'tree-level roslyn census',
                       'tree': args.tree, 'files': len(sources),
                       'wall_s': round(time.time() - t0, 1),
                       'total': total, 'syntax': syntax,
                       'binding': total - syntax,
                       'dupes_CS0101': dupes, 'codes': codes}, f, indent=1)
    return 0 if syntax == 0 else 1


if __name__ == '__main__':
    sys.exit(main())
