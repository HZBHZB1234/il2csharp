#!/usr/bin/env python3
"""Differential quality report: decompiled tree vs the original C# source.

A fixture with `source_url` also has its source checkout under
`fixtures/<id>/src` on this machine (local-only).  That is ground truth the
IL2CPP corpus does not otherwise have: for every source method that survives
compilation under the same name and arity, we can ask whether the lifted body
still *does the same thing* -- calls the same methods, touches the same
members, keeps the same statement shape.

The report is intentionally conservative.  It never claims equivalence; it
ranks the methods where the lifted body disagrees most with the source, so a
human can read a small list instead of 100k bodies.  Async/iterator methods,
lambdas/local functions and `[Conditional]` methods are excluded: the C#
compiler rewrites them into state machines/display classes, or removes the
body from the build, so the source body is not the body IL2CPP compiled.
Comments are stripped before sequences are counted, and an output body that
contains an inlined async/iterator state machine is excluded too (IL2CPP/MSVC
inlines small wrappers, so a sync source method can map to a rewritten body).

Usage:
    python tools/source_compare.py --fixture unitask --label src1
    python tools/source_compare.py --fixture survivors-roguelike-kit \
        --label src1 --show 20 --report /tmp/survivors-quality.json

`--source` may be repeated; the default is `fixtures/<id>/src`.  Directories
named Editor/Tests/Samples/Benchmarks and generated/object folders are
skipped.  The report is written next to the tree as
`quality_report.json` unless `--report` is given.
"""
import argparse
import collections
import difflib
import json
import os
import re
import sys

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, REPO)
sys.path.insert(0, os.path.join(REPO, 'tools'))

TYPE_NODES = {
    'class_declaration', 'struct_declaration', 'interface_declaration',
    'record_declaration', 'enum_declaration',
}
SKIP_DIRS = {
    'editor', 'tests', 'test', 'samples', 'samples~', 'benchmarks',
    'benchmark', 'obj', 'library', 'temp', 'logs', 'packages', '.git',
}


def _is_test_dir(name):
    """Project test folders (`NetCoreTests`, `Foo.Tests`) are not built."""
    n = name.casefold()
    return n.endswith(('test', 'tests', '_test', '_tests')) \
        or n.startswith(('test_', 'tests_'))
CALL_KEYWORDS = {
    'if', 'for', 'foreach', 'while', 'switch', 'catch', 'using', 'lock',
    'fixed', 'typeof', 'nameof', 'sizeof', 'default', 'checked',
    'unchecked', 'base', 'this', 'return', 'new', 'delegate', 'stackalloc',
    'when', 'in', 'out', 'ref',
}
OPERATOR_NAMES = {
    '+': 'op_Addition', '-': 'op_Subtraction', '*': 'op_Multiply',
    '/': 'op_Division', '%': 'op_Modulus', '&': 'op_BitwiseAnd',
    '|': 'op_BitwiseOr', '^': 'op_ExclusiveOr', '<<': 'op_LeftShift',
    '>>': 'op_RightShift', '==': 'op_Equality', '!=': 'op_Inequality',
    '<': 'op_LessThan', '>': 'op_GreaterThan', '<=': 'op_LessThanOrEqual',
    '>=': 'op_GreaterThanOrEqual', '!': 'op_LogicalNot',
    '~': 'op_OnesComplement', '++': 'op_Increment', '--': 'op_Decrement',
    'true': 'op_True', 'false': 'op_False',
}
# decompiler tells; each is a count, not a verdict
TELL_PATTERNS = {
    'unknown': re.compile(r'\bunknown\b'),
    'sub_call': re.compile(r'\bsub_[0-9A-Fa-f]+\b'),
    'data_name': re.compile(r'\bdata_[0-9A-Fa-f]+\b'),
    'byte_ptr': re.compile(r'\(byte\*\)'),
    'obj_temp': re.compile(r'\bobj\d+\b'),
    'ret_temp': re.compile(r'\b__ret\b'),
    'shared_stub': re.compile(r'__SharedBodyStubs|shared body'),
    'typeof_index': re.compile(r'\(\(byte\*\)typeof\('),
    'sret_store': re.compile(r'\(\(byte\*\)&'),
    'qword': re.compile(r'\bqword_'),
}
# An async/iterator state machine in the OUTPUT whose source method was not
# async: IL2CPP/MSVC inlined the async callee into a sync wrapper, so the
# outer method and the source body are no longer the same method.  The
# state-machine class name is the reliable tell.
INLINED_STATE_MACHINE_RX = re.compile(
    r'(?:<[A-Za-z_]\w*>|_[A-Za-z_]\w*_)d__\d+'
    r'|\bAsync(?:UniTask|Task|Void|ValueTask)MethodBuilder\b')


def _ts():
    from tree_sitter import Language, Parser
    import tree_sitter_c_sharp
    return Parser(Language(tree_sitter_c_sharp.language()))


def _text(node):
    return node.text.decode('utf-8', 'replace') if node is not None else ''


def _child(node, field):
    return node.child_by_field_name(field)


def _code_text(node):
    """Node text with comment nodes removed.

    The report compares call/member *sequences*.  A comment mentioning
    `Foo()` is not a call, and a method whose whole source body is
    commented out compiles to an empty body.  Dropping comments here keeps
    the source side honest without changing the output side's spelling.
    """
    if node is None:
        return ''
    data = node.text
    cuts = []
    stack = [node]
    while stack:
        cur = stack.pop()
        if cur.type in ('comment', 'documentation_comment'):
            cuts.append((cur.start_byte - node.start_byte,
                         cur.end_byte - node.start_byte))
        else:
            stack.extend(cur.named_children)
    if not cuts:
        return data.decode('utf-8', 'replace')
    cuts.sort()
    parts, pos = [], 0
    for start, end in cuts:
        if start > pos:
            parts.append(data[pos:start])
        pos = max(pos, end)
    if pos < len(data):
        parts.append(data[pos:])
    return b''.join(parts).decode('utf-8', 'replace')


def _normalize_type(name):
    return re.sub(r'`\d+', '', name.replace('/', '.'))


def _join(ns, name):
    if not name:
        return ns
    return (ns + '.' if ns else '') + name


def _body_has_code(text):
    """False for `{}`, `{ /* gone */ }`, whitespace and stray semicolons."""
    return bool(re.sub(r'[{}\s;]', '', text))


def _strip_expr(text):
    text = text.strip()
    if text.startswith('=>'):
        text = text[2:]
    return text


class Method:
    __slots__ = ('type_full', 'name', 'arity', 'params', 'body', 'file',
                 'line', 'transformed', 'kind')

    def __init__(self, type_full, name, params, body, file, line,
                 transformed=False, kind='method'):
        self.type_full = type_full
        self.name = name
        self.arity = len(params)
        self.params = params
        self.body = body
        self.file = file
        self.line = line
        self.transformed = transformed
        self.kind = kind


def _param_info(node):
    """(names, type texts) of a parameter list node."""
    names, types = [], []
    params = _child(node, 'parameters') if node.type != 'parameter_list' else node
    if params is None:
        for ch in node.children:
            if ch.type == 'parameter_list':
                params = ch
                break
    if params is None:
        return names, types
    for p in params.named_children:
        if p.type not in ('parameter', 'this_parameter'):
            continue
        n = _child(p, 'name')
        t = _child(p, 'type')
        names.append(_text(n))
        types.append(re.sub(r'\s+', ' ', _text(t)).strip())
    return names, types


def _is_async(node):
    stack = [node]
    while stack:
        cur = stack.pop()
        if cur.type == 'modifier' and _text(cur).strip() == 'async':
            return True
        stack.extend(cur.named_children)
    return False


def _is_iterator(node):
    stack = [node]
    while stack:
        cur = stack.pop()
        if cur.type == 'yield_statement':
            return True
        stack.extend(cur.named_children)
    return False


def _has_attribute(decl, simple_name):
    """True when the declaration carries `[Conditional(...)]` (or `X.Y`)."""
    for ch in decl.named_children:
        if ch.type != 'attribute_list':
            continue
        stack = [ch]
        while stack:
            cur = stack.pop()
            if cur.type == 'attribute':
                name = _text(_child(cur, 'name'))
                if name.split('.')[-1] == simple_name:
                    return True
            stack.extend(cur.named_children)
    return False


def _has_lambda_or_local_function(node):
    """Compiler-rewritten bodies: closure classes / local functions.

    A lambda body becomes a method on a display class and a local function
    becomes its own MethodDef, so the outer source body and the lifted body
    are not the same method.  Excluding these is the same conservative rule
    already used for async/iterator methods.
    """
    stack = [node]
    while stack:
        cur = stack.pop()
        if cur.type in ('lambda_expression', 'anonymous_method_expression',
                        'local_function_statement'):
            return True
        stack.extend(cur.named_children)
    return False


def _add_method(idx, type_full, name, decl, node, file, kind='method'):
    body = _child(node, 'body')
    if body is None:
        return
    params, _types = _param_info(decl)
    body_text = _code_text(body)
    if node.type in ('property_declaration', 'indexer_declaration',
                     'event_declaration'):
        body_text = _strip_expr(body_text)
    transformed = (_is_async(node) or _is_iterator(node)
                   or _has_attribute(decl, 'Conditional')
                   or _has_lambda_or_local_function(body))
    idx.setdefault(type_full, {}).setdefault(
        (name, len(params)), []).append(
        Method(type_full, name, params, body_text, file,
               node.start_point[0] + 1, transformed, kind))


def _collect_accessors(idx, type_full, node, file):
    """Property/indexer/event accessors, named the metadata way."""
    name = _text(_child(node, 'name'))
    if node.type == 'indexer_declaration':
        name = 'Item'
    if not name:
        return
    params, _types = _param_info(node)
    acc = _child(node, 'accessors')
    if acc is None:
        acc = next((ch for ch in node.children
                    if ch.type == 'accessor_list'), None)
    if acc is not None:
        for a in acc.named_children:
            if a.type != 'accessor_declaration':
                continue
            head = _text(a).lstrip()
            hit = re.match(r'(get|set|add|remove)\b', head)
            if hit is None:
                continue
            prefix = hit.group(1) + '_'
            body = _child(a, 'body')
            if body is None:
                continue
            idx.setdefault(type_full, {}).setdefault(
                (prefix + name, len(params)), []).append(
                Method(type_full, prefix + name, params, _code_text(body), file,
                       a.start_point[0] + 1,
                       _has_lambda_or_local_function(body), hit.group(1)))
        return
    # expression-bodied property: the arrow is the getter
    body = _child(node, 'value')
    if body is not None and node.type == 'property_declaration':
        idx.setdefault(type_full, {}).setdefault(
            ('get_' + name, len(params)), []).append(
            Method(type_full, 'get_' + name, params,
                   _strip_expr(_code_text(body)), file,
                   node.start_point[0] + 1,
                   _has_lambda_or_local_function(body), 'get'))


def _walk_members(idx, type_full, node, file):
    for ch in node.named_children:
        t = ch.type
        if t == 'method_declaration':
            _add_method(idx, type_full, _text(_child(ch, 'name')), ch, ch, file)
        elif t == 'constructor_declaration':
            _add_method(idx, type_full, '.ctor', ch, ch, file, 'ctor')
        elif t == 'destructor_declaration':
            _add_method(idx, type_full, 'Finalize', ch, ch, file, 'dtor')
        elif t in ('property_declaration', 'indexer_declaration',
                   'event_declaration'):
            _collect_accessors(idx, type_full, ch, file)
        elif t == 'operator_declaration':
            head = _text(ch).split('{', 1)[0]
            m = re.search(r'\boperator\s*(\S+)', head)
            if m:
                name = OPERATOR_NAMES.get(m.group(1))
                if name:
                    _add_method(idx, type_full, name, ch, ch, file, 'operator')
        elif t == 'conversion_operator_declaration':
            head = _text(ch).split('{', 1)[0]
            name = 'op_Implicit' if 'implicit' in head else 'op_Explicit'
            _add_method(idx, type_full, name, ch, ch, file, 'operator')
        elif t in ('preproc_if', 'preproc_else', 'preproc_elif'):
            _walk_members(idx, type_full, ch, file)


def _walk_types(idx, node, ns, outer, file):
    for ch in node.named_children:
        t = ch.type
        if t == 'namespace_declaration':
            ns2 = _join(ns, _text(_child(ch, 'name')))
            body = _child(ch, 'body')
            _walk_types(idx, body if body is not None else ch, ns2, '', file)
        elif t == 'file_scoped_namespace_declaration':
            ns2 = _join(ns, _text(_child(ch, 'name')))
            _walk_types(idx, ch, ns2, outer, file)
        elif t in TYPE_NODES:
            name = _text(_child(ch, 'name'))
            rel = _join(outer, name)
            full = _join(ns, rel)
            body = _child(ch, 'body')
            if body is not None:
                _walk_members(idx, full, body, file)
                _walk_types(idx, body, ns, rel, file)
        elif t in ('preproc_if', 'preproc_else', 'preproc_elif'):
            _walk_types(idx, ch, ns, outer, file)


def index_cs(root, files=None, skip_dirs=None):
    """full type name -> {(method, arity): [Method, ...]}"""
    skip = {s.casefold() for s in (skip_dirs or SKIP_DIRS)}
    parser = _ts()
    idx = {}
    if files is None:
        files = []
        for dp, dns, fns in os.walk(root):
            dns[:] = [d for d in dns
                      if d.casefold() not in skip and not _is_test_dir(d)]
            for fn in fns:
                if fn.endswith('.cs'):
                    files.append(os.path.join(dp, fn))
    for path in files:
        try:
            with open(path, 'rb') as f:
                data = f.read()
            if data.startswith(b'\xef\xbb\xbf'):
                data = data[3:]
            tree = parser.parse(data)
            _walk_types(idx, tree.root_node, '', '', path)
        except Exception as ex:  # keep the report running over one bad file
            print('warning: %s: %s' % (path, ex), file=sys.stderr)
    return idx


def index_tree(tree_dir, image_dirs):
    files = []
    for image in image_dirs:
        base = os.path.join(tree_dir, image)
        if not os.path.isdir(base):
            continue
        for dp, _dns, fns in os.walk(base):
            for fn in fns:
                if fn.endswith('.cs') and fn not in (
                        '__SharedBodyStubs.cs', '__Addr.cs'):
                    files.append(os.path.join(dp, fn))
    return index_cs(tree_dir, files, skip_dirs=set())


def call_sequence(body):
    seq = []
    for m in re.finditer(
            r'([A-Za-z_][\w]*)\s*(?:<[^<>{};]*>)?\s*\(', body):
        name = m.group(1)
        if name in CALL_KEYWORDS:
            continue
        seq.append(name)
    return seq


def member_sequence(body):
    seq = []
    for m in re.finditer(r'[?.]\s*([A-Za-z_]\w*)(?!\s*\()', body):
        name = m.group(1)
        if name in CALL_KEYWORDS or name.isdigit():
            continue
        seq.append(name)
    return seq


def _f1(src, out):
    if not src and not out:
        return 1.0, 1.0, 1.0
    if not src or not out:
        return 0.0, 0.0, 0.0
    a, b = collections.Counter(src), collections.Counter(out)
    inter = sum((a & b).values())
    prec = inter / len(out)
    rec = inter / len(src)
    f1 = 2 * prec * rec / (prec + rec) if prec + rec else 0.0
    return prec, rec, f1


def _shape(body):
    return {
        'if': len(re.findall(r'\bif\s*\(', body)),
        'for': len(re.findall(r'\bfor\s*\(', body)),
        'while': len(re.findall(r'\bwhile\s*\(', body)),
        'switch': len(re.findall(r'\bswitch\s*\(', body)),
        'try': len(re.findall(r'\btry\b', body)),
        'return': len(re.findall(r'\breturn\b', body)),
        'goto': len(re.findall(r'\bgoto\b', body)),
        'new': len(re.findall(r'\bnew\s+', body)),
    }


def _shape_cos(a, b):
    keys = sorted(set(a) | set(b))
    dot = sum(a[k] * b[k] for k in keys)
    na = sum(v * v for v in a.values()) ** 0.5
    nb = sum(v * v for v in b.values()) ** 0.5
    return dot / (na * nb) if na and nb else (1.0 if not na and not nb else 0.0)


def _pair_overloads(slist, olist):
    """Greedy pair by parameter-type similarity (exact text wins)."""
    if len(slist) == 1 and len(olist) == 1:
        return [(slist[0], olist[0])]
    scores = []
    for i, s in enumerate(slist):
        for j, o in enumerate(olist):
            a = '|'.join(s.params)
            b = '|'.join(o.params)
            scores.append((difflib.SequenceMatcher(None, a, b).ratio(), i, j))
    scores.sort(reverse=True)
    used_s, used_o, pairs = set(), set(), []
    for _score, i, j in scores:
        if i in used_s or j in used_o:
            continue
        used_s.add(i)
        used_o.add(j)
        pairs.append((slist[i], olist[j]))
    return pairs


def compare(source_idx, tree_idx, min_calls=1):
    rows = []
    unmatched = collections.Counter()
    samples = {}          # category -> a few (type, name, arity, file, line)

    def _note(cat, item):
        bucket = samples.setdefault(cat, [])
        if len(bucket) < 400:
            bucket.append(item)
    for type_full, smeths in source_idx.items():
        omeths = tree_idx.get(_normalize_type(type_full))
        if not omeths:
            unmatched['type'] += sum(len(v) for v in smeths.values())
            continue
        for (name, arity), slist in smeths.items():
            olist = omeths.get((name, arity))
            if not olist:
                # accessor/property spellings can differ by '.'/'_'; try the
                # exact name with the other arity as a last resort
                unmatched['method'] += len(slist)
                for s in slist[:2]:
                    _note('method', [type_full, name, arity, s.file, s.line])
                continue
            for s, o in _pair_overloads(slist, olist):
                if s.transformed:
                    unmatched['transformed'] += 1
                    continue
                if not _body_has_code(s.body) or not _body_has_code(o.body):
                    unmatched['empty'] += 1
                    which = ('src' if not _body_has_code(s.body) else '') + \
                            ('out' if not _body_has_code(o.body) else '')
                    # split the side: mpty_out (the source has a body and
                    # ours does not) is the only DEFECT of the three; both
                    # empty is pairing noise and src-only is a stripped or
                    # [Conditional] body in the player build
                    unmatched['empty_' + (which or 'both')] += 1
                    _note('empty', [type_full, name, arity, s.file, s.line,
                                    which])
                    continue
                if 'Method body was not recovered' in o.body:
                    unmatched['stub'] += 1
                    _note('stub', [type_full, name, arity, s.file, s.line])
                    continue
                if INLINED_STATE_MACHINE_RX.search(o.body):
                    # IL2CPP inlined the async implementation into this
                    # sync wrapper; the outer body is a compiler rewrite.
                    unmatched['inlined'] += 1
                    continue
                sc, oc = call_sequence(s.body), call_sequence(o.body)
                sm, om = member_sequence(s.body), member_sequence(o.body)
                cp, cr, cf1 = _f1(sc, oc)
                mp, mr, mf1 = _f1(sm, om)
                ss, os_ = _shape(s.body), _shape(o.body)
                rows.append({
                    'type': type_full,
                    'method': name,
                    'arity': arity,
                    'file': s.file,
                    'line': s.line,
                    'src_calls': len(sc),
                    'out_calls': len(oc),
                    'call_precision': round(cp, 4),
                    'call_recall': round(cr, 4),
                    'call_f1': round(cf1, 4),
                    'member_f1': round(mf1, 4),
                    'shape_cos': round(_shape_cos(ss, os_), 4),
                    'src_shape': ss,
                    'out_shape': os_,
                    'missing_calls': sorted(
                        (collections.Counter(sc) - collections.Counter(oc)).elements())[:30],
                    'extra_calls': sorted(
                        (collections.Counter(oc) - collections.Counter(sc)).elements())[:30],
                    'tells': {k: len(rx.findall(o.body))
                              for k, rx in TELL_PATTERNS.items()
                              if rx.search(o.body)},
                })
    # per-construct deltas over the whole matched population: shape_cos alone
    # says HOW different, this says WHAT runs long (an `if` spray and a `goto`
    # cascade are different defects with the same cosine).
    deltas = collections.Counter()
    worst_delta = []
    for r in rows:
        ss, os_ = r['src_shape'], r['out_shape']
        for k in ss:
            d = os_.get(k, 0) - ss[k]
            if d:
                deltas['%s%+d' % (k, d)] += 1
        mag = sum(abs(os_.get(k, 0) - ss[k]) for k in ss)
        if mag:
            worst_delta.append((mag, r['type'], r['method'], r['arity'],
                                r['src_shape'], r['out_shape']))
    worst_delta.sort(key=lambda x: x[0], reverse=True)
    return rows, unmatched, samples, {
        'deltas': dict(deltas.most_common(40)),
        'worst': [{'magnitude': m, 'type': t, 'method': n, 'arity': a,
                   'src_shape': s, 'out_shape': o}
                  for m, t, n, a, s, o in worst_delta[:25]],
    }


def census(tree_dir, image_dirs):
    total = collections.Counter()
    files = 0
    for image in image_dirs:
        base = os.path.join(tree_dir, image)
        if not os.path.isdir(base):
            continue
        for dp, _dns, fns in os.walk(base):
            for fn in fns:
                if not fn.endswith('.cs'):
                    continue
                files += 1
                with open(os.path.join(dp, fn), encoding='utf-8',
                          errors='replace') as f:
                    data = f.read()
                for k, rx in TELL_PATTERNS.items():
                    n = len(rx.findall(data))
                    if n:
                        total[k] += n
    return files, dict(total)


def _fmt_row(r):
    return ('%-46s %-34s n=%-2d calls=%d/%d rec=%.2f f1=%.2f '
            'mem=%.2f shape=%.2f' % (
                (r['type'] + '.' + r['method'])[:46], r['method'], r['arity'],
                r['src_calls'], r['out_calls'], r['call_recall'],
                r['call_f1'], r['member_f1'], r['shape_cos']))


def main(argv=None):
    ap = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('--fixture', required=True)
    ap.add_argument('--label', default=None,
                    help='tree label under out/<fixture>/; default newest')
    ap.add_argument('--source', action='append', default=None,
                    help='source root (repeatable); default fixtures/<id>/src')
    ap.add_argument('--images', default=None,
                    help='comma-separated image dirs; default all dirs in tree')
    ap.add_argument('--report', default=None)
    ap.add_argument('--show', type=int, default=15)
    ap.add_argument('--min-calls', type=int, default=2,
                    help='ignore methods with fewer source calls in ranking')
    ap.add_argument('--json', action='store_true')
    args = ap.parse_args(argv)

    from fixtures import resolve
    fx = resolve(args.fixture)
    out_root = os.path.join(REPO, 'out', args.fixture)
    if args.label:
        tree = os.path.join(out_root, args.label)
    else:
        cands = [os.path.join(out_root, d) for d in os.listdir(out_root)] \
            if os.path.isdir(out_root) else []
        cands = [c for c in cands if os.path.isdir(c)]
        if not cands:
            raise SystemExit('no tree under %s' % out_root)
        tree = max(cands, key=os.path.getmtime)

    sources = args.source or [os.path.join(REPO, 'fixtures', args.fixture,
                                           'src')]
    sources = [s for s in sources if os.path.isdir(s)]
    if not sources:
        raise SystemExit('no source checkout (use --source)')

    if args.images:
        images = [x.strip() for x in args.images.split(',') if x.strip()]
    else:
        images = sorted(d for d in os.listdir(tree)
                        if os.path.isdir(os.path.join(tree, d))
                        and not d.startswith('_'))

    print('tree   : %s' % tree)
    print('source : %s' % ', '.join(sources))
    print('images : %s' % ', '.join(images))

    src_idx = {}
    for root in sources:
        part = index_cs(root)
        for k, v in part.items():
            dst = src_idx.setdefault(k, {})
            for key, methods in v.items():
                dst.setdefault(key, []).extend(methods)
    tree_idx = index_tree(tree, images)

    rows, unmatched, samples, shapedelta = compare(src_idx, tree_idx)
    files, tells = census(tree, images)

    def _avg(key):
        return round(sum(r[key] for r in rows) / len(rows), 4) if rows else 0.0

    ranked = sorted(
        (r for r in rows if r['src_calls'] >= args.min_calls),
        key=lambda r: (r['call_recall'], r['call_f1'], r['member_f1'],
                       r['shape_cos']))
    report = {
        'fixture': args.fixture,
        'tree': tree,
        'sources': sources,
        'images': images,
        'source_types': len(src_idx),
        'tree_types': len(tree_idx),
        'matched_methods': len(rows),
        'unmatched': dict(unmatched),
        'unmatched_samples': samples,
        'shape_deltas': shapedelta,
        'averages': {k: _avg(k) for k in (
            'call_precision', 'call_recall', 'call_f1', 'member_f1',
            'shape_cos')},
        'methods_with_full_call_recall': sum(
            1 for r in rows if r['call_recall'] >= 0.999),
        'methods_with_zero_call_recall': sum(
            1 for r in rows if r['call_recall'] <= 0.001),
        'files': files,
        'tells': tells,
        'worst': ranked[:200],
    }
    if args.report:
        path = args.report
    else:
        path = os.path.join(tree, 'quality_report.json')
    with open(path, 'w', encoding='utf-8', newline='\n') as f:
        json.dump(report, f, indent=1, ensure_ascii=False)

    if args.json:
        print(json.dumps({k: v for k, v in report.items() if k != 'worst'},
                         indent=1))
    else:
        print('types  : source=%d tree=%d' %
              (len(src_idx), len(tree_idx)))
        print('methods: matched=%d  unmatched=%s' %
              (len(rows), dict(unmatched)))
        print('averages: ' + '  '.join(
            '%s=%.3f' % (k, v) for k, v in report['averages'].items()))
        print('full call recall: %d/%d (%.1f%%)  zero: %d' % (
            report['methods_with_full_call_recall'], len(rows),
            100.0 * report['methods_with_full_call_recall'] / max(1, len(rows)),
            report['methods_with_zero_call_recall']))
        print('census : %d files  %s' % (files, tells))
        print('\nworst (source calls >= %d):' % args.min_calls)
        for r in ranked[:args.show]:
            print('  ' + _fmt_row(r))
            if r['missing_calls']:
                print('      missing: %s' % ', '.join(r['missing_calls']))
            if r['tells']:
                print('      tells  : %s' % r['tells'])
        print('\nreport: %s' % path)
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
