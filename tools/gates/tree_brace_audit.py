"""Literal-aware brace audit over an emitted C# tree.

Counts ``{`` and ``}`` outside string/char literals and ``/* */`` comments and
reports any file whose net depth is not zero. A naive ``line.count('{')``
reports false positives on literals like ``"BitVector32{"`` -- the whole
reason this tool exists.

Usage::

    python tools/gates/tree_brace_audit.py --tree <dir> [--report FILE]
    python tools/gates/tree_brace_audit.py --fixture ID [--label L]

Exit: 0 when every file balances, 1 otherwise, 2 on usage errors.
"""
import argparse
import json
import os
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from fixtures import FixtureError, out_tree, resolve, require_tree  # noqa: E402


def strip_literals(line, in_block):
    """Blank out string/char literals and comments, preserving length.

    Returns (masked_line, in_block_comment). Length is preserved so callers
    can keep byte/column offsets aligned with the original line.
    """
    out = []
    i = 0
    n = len(line)
    while i < n:
        c = line[i]
        if in_block:
            end = line.find('*/', i)
            if end < 0:
                out.append(' ' * (n - i))
                i = n
                continue
            out.append(' ' * (end + 2 - i))
            i = end + 2
            in_block = False
            continue
        if c == '"':
            if line.startswith('@"', i):
                j = i + 2
                while j < n:
                    if line[j] == '"':
                        if j + 1 < n and line[j + 1] == '"':
                            j += 2
                            continue
                        break
                    j += 1
                out.append(' ' * (min(j + 1, n) - i))
                i = j + 1
                continue
            j = i + 1
            while j < n and line[j] != '"':
                j += 2 if line[j] == '\\' else 1
            out.append(' ' * (min(j + 1, n) - i))
            i = j + 1
            continue
        if c == "'":
            j = i + 1
            while j < n and line[j] != "'":
                j += 2 if line[j] == '\\' else 1
            out.append(' ' * (min(j + 1, n) - i))
            i = j + 1
            continue
        if line.startswith('/*', i):
            end = line.find('*/', i + 2)
            if end < 0:
                out.append(' ' * (n - i))
                return ''.join(out), True
            out.append(' ' * (end + 2 - i))
            i = end + 2
            continue
        if line.startswith('//', i):
            out.append(' ' * (n - i))
            i = n
            continue
        out.append(c)
        i += 1
    return ''.join(out), in_block


def audit_tree(root):
    """{relpath: {'delta': int, 'line': int}} for every unbalanced file."""
    root = Path(root)
    bad = {}
    files = 0
    for path in sorted(root.rglob('*.cs')):
        files += 1
        try:
            data = path.read_bytes().decode('utf-8', 'replace')
        except OSError:
            continue
        depth = 0
        worst = None
        in_block = False
        for lineno, line in enumerate(data.split('\n'), 1):
            masked, in_block = strip_literals(line, in_block)
            for ch in masked:
                if ch == '{':
                    depth += 1
                elif ch == '}':
                    depth -= 1
            if depth < 0 and worst is None:
                worst = lineno
        if depth != 0:
            bad[path.relative_to(root).as_posix()] = {
                'delta': depth, 'line': worst or 0}
    return files, bad


def write_report(path, payload):
    path = Path(path)
    if path.parent:
        path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2) + '\n', encoding='utf-8')


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--tree', help='emitted tree to audit')
    ap.add_argument('--fixture', help='fixture id (uses --label, else newest)')
    ap.add_argument('--label', help='output label under out/<fixture>/')
    ap.add_argument('--report', help='write a JSON report here')
    args = ap.parse_args(argv)
    if not args.tree and not args.fixture:
        ap.error('pass --tree or --fixture')
    try:
        tree = Path(args.tree) if args.tree else require_tree(
            resolve(args.fixture), args.label)
    except FixtureError as ex:
        print('error:', ex)
        return 2
    if not tree.is_dir():
        print('error: no such tree:', tree)
        return 2
    files, bad = audit_tree(tree)
    payload = {
        'kind': 'literal-aware brace audit',
        'tree': str(Path(tree).resolve()),
        'files': files,
        'unbalanced_files': len(bad),
        'details': bad,
    }
    if args.report:
        write_report(args.report, payload)
    print('%s: %d files, %d unbalanced' % (tree, files, len(bad)))
    for name, info in sorted(bad.items())[:20]:
        print('  %s  delta=%d at line %d' % (name, info['delta'], info['line']))
    return 1 if bad else 0


if __name__ == '__main__':
    sys.exit(main())
