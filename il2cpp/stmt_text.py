from il2cpp.prelude import *  # noqa: F401,F403


class _LateDecompiler:
    """Late-bound stand-in for il2cpp.dec.Decompiler.

    This module is imported while il2cpp.dec is still initialising, so the
    class is looked up on first attribute use rather than at import time.
    """

    def __getattr__(self, name):
        from il2cpp.dec import Decompiler as _D
        return getattr(_D, name)

    def __setattr__(self, name, value):
        from il2cpp.dec import Decompiler as _D
        setattr(_D, name, value)


Decompiler = _LateDecompiler()

def _rsplit_op(text, op):
    depth = 0
    inq = None
    for i in range(len(text) - 1, -1, -1):
        ch = text[i]
        if inq:
            if ch == inq:
                inq = None
            continue
        if ch in ('"', "'"):
            inq = ch
            continue
        if ch in ')]':
            depth += 1
        elif ch in '((':
            depth -= 1
        elif depth == 0 and text.startswith(op, i) and i > 0 and text[i - 1] == ' ' \
                and i + len(op) < len(text) and text[i + len(op)] == ' ':
            return i
    return None


def _top_level_logic_op(text):
    """True when `text` carries a `&`/`|`/`^`/`&&`/`||` outside any
    paren group. Used by `_fix_cond_line`'s double-negation arm: an outer
    `!` distributes over exactly those operators (De Morgan), so unwrapping
    `!(!X op Y)` as `X op Y` would invert half the condition."""
    depth = 0
    i = 0
    n = len(text)
    while i < n:
        ch = text[i]
        if ch == '(':
            depth += 1
        elif ch == ')':
            depth = max(0, depth - 1)
        elif depth == 0:
            for op in ('&&', '||'):
                if text.startswith(op, i):
                    return True
            if ch in '&|^':
                # a bitwise op inside an identifier-ish run is not a
                # logical operator (there is none in C# text we emit)
                return True
        i += 1
    return False


def _fix_cond_line(line, dec):
    m = re.match(r'^(if|while) \((.*)\)(;?)$', line)
    # fix 165: the double-negation arm must see a condition that IS one
    # `!(!X)` group. `group(2)` is greedy, so a leading `!(!` also matched
    # when more of the expression followed -- `!(!flag5 ? 1 : 0) | flag1`
    # became `flag5 ? 1 : 0) | flag1` (stray `)`, unparseable).
    #
    # The whole-span test is necessary but NOT sufficient: `!(!(A) | (B))`
    # also starts with `!(!` and also has its outer `!` spanning the whole
    # condition, yet by De Morgan it is `(A) & !(B)`, not `(A) | (B)`.
    # Folding it silently INVERTS half the condition. The rule: peel the
    # outer `!(`...`)`, then the inner text must be a negation whose own
    # operand carries no top-level `&`/`|`/`&&`/`||` -- those are exactly
    # the operators the outer `!` distributes over. A ternary, a call or
    # an atom after the inner `!` is safe to unwrap.
    _c = m.group(2) if m else None
    if _c is not None and _c.startswith('!(') \
            and Decompiler._paren_wraps_whole(_c) \
            and _c[2:-1].startswith('!'):
        _operand = _c[3:]
        if not _top_level_logic_op(_operand[:-1] if _operand.endswith(')')
                                   else _operand):
            inner = _c[3:-1].strip()
            return '%s (%s)%s' % (m.group(1), inner, m.group(3))
    if m and m.group(2).startswith('!(') :
        return '%s (%s)%s' % (m.group(1), dec._simplify_cond(m.group(2)), m.group(3))
    if m:
        return '%s (%s)%s' % (m.group(1), m.group(2), m.group(3))
    m2 = re.match(r'^\} while \((.*)\);$', line)
    if m2:
        return '} while (%s);' % m2.group(2)
    return line


_CONDHEAD_RX = re.compile(r'^(if|while) \((.*)\)(;?)$')
_DOWHILE_RX = re.compile(r'^\} while \((.*)\);$')


def _cond_dewrap(ln):
    """Strip REDUNDANT fully-wrapping parens from an if/while condition
    head -- `if (((X != null)))` -> `if (X != null)`, `if (!((X)))` ->
    `if (!(X))`. The fold family stacks these late: op_Equality/
    op_Inequality replacements always paren-wrap, and they run in
    _final_text AFTER render's condition fixing, so the cleanup has to
    live after them (fix 44c). An outermost wrap is always redundant in
    a condition head; an operand of `!` keeps its one required pair.
    Literal-aware via _paren_wraps_whole; never touches a line that is
    not an exact head shape (indentation-aware -- _final_text sees the
    rendered, indented lines)."""
    stripped = ln.lstrip()
    indent = ln[:len(ln) - len(stripped)]
    m = _CONDHEAD_RX.match(stripped)
    if m:
        return indent + '%s (%s)%s' % (m.group(1),
                                       _dewrap_cond(m.group(2)), m.group(3))
    m = _DOWHILE_RX.match(stripped)
    if m:
        return indent + '} while (%s);' % _dewrap_cond(m.group(1))
    return ln


def _dewrap_cond(c):
    for _ in range(4):
        if c[:1] == '(' and c[-1:] == ')' \
                and Decompiler._paren_wraps_whole(c):
            c = c[1:-1]
        elif c.startswith('!(') and c.endswith(')') \
                and c[2:-1][:1] == '(' and c[2:-1][-1:] == ')' \
                and Decompiler._paren_wraps_whole(c[2:-1]):
            c = '!(%s)' % c[3:-2]
        else:
            break
    return c


def _split_top(text):
    parts = []
    depth = 0
    inq = None
    cur = []
    for ch in text:
        if inq:
            cur.append(ch)
            if ch == inq:
                inq = None
            continue
        if ch in ('"', "'"):
            inq = ch
            cur.append(ch)
            continue
        if ch in '([':
            depth += 1
        elif ch in ')]':
            depth -= 1
        if ch == ',' and depth == 0:
            parts.append(''.join(cur))
            cur = []
        else:
            cur.append(ch)
    parts.append(''.join(cur))
    return parts

