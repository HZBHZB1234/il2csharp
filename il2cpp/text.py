from il2cpp.prelude import *  # noqa: F401,F403


# ---- literal/comment NUL mask (shared by textpass + highlevel) -----------
# One precompiled regex scans a rendered line left-to-right, exactly as the
# old char-by-char loop did: `//` to end-of-string, `/* ... */` (open on a
# line keeps the caller's block-comment state set), `@"..."` verbatim strings
# (`""` is an escaped quote), `"..."` regular strings (backslash escapes),
# and `'...'` char literals. Matched spans are NUL-blanked so the result is
# the same length as the input (token spans stay aligned). An unterminated
# literal/comment masks to end-of-string (the old loop's behaviour). A real
# rendered line never carries a raw newline, so `[\s\S]` == the old `.*`.
_MASK_RE = re.compile(
    r'(?P<line>//[\s\S]*)'
    r'|(?P<block>/\*[^*]*\*+(?:[^/*][^*]*\*+)*/)'
    r'|(?P<block_unterm>/\*[\s\S]*)'
    r'|(?P<vstr>@"(?:[^"]|"")*")'
    r'|(?P<vstr_unterm>@"[\s\S]*)'
    r'|(?P<str>"(?:\\.|[^"\\])*")'
    r'|(?P<str_unterm>"[\s\S]*)'
    r"|(?P<chr>'(?:\\.|[^'\\])*')"
    r"|(?P<chr_unterm>'[\s\S]*)"
)


def _mask_scan(line, i, n):
    """Mask literals/comments in `line[i:n]`; set the block flag if an
    unterminated `/*` opened one. Returns (masked, in_block_comment)."""
    out = []
    last = i
    inbc = False
    for m in _MASK_RE.finditer(line, i):
        s, e = m.span()
        if s > last:
            out.append(line[last:s])
        out.append('\x00' * (e - s))
        last = e
        if m.lastgroup == 'block_unterm':
            inbc = True
    if last < n:
        out.append(line[last:n])
    return ''.join(out), inbc


def mask_spans(line, in_block_comment):
    """Blank string/char literals and comments with NULs, same length.

    Byte-for-byte equivalent to the old char-by-char mask (verified on every
    line of the built tree): token spans stay aligned with the original line
    while the scanners only ever see code. `in_block_comment` carries a `/*`
    still open on the previous line."""
    n = len(line)
    if in_block_comment:
        j = line.find('*/')
        if j < 0:
            return '\x00' * n, True
        pre = j + 2
        rest, inbc = _mask_scan(line, pre, n)
        return '\x00' * pre + rest, inbc
    return _mask_scan(line, 0, n)

def _build_reg_canon() -> dict:
    canon = {}
    fams = ['RAX', 'RCX', 'RDX', 'RBX', 'RSP', 'RBP', 'RSI', 'RDI'] +            ['R%d' % i for i in range(8, 16)]
    variants = ['%s', 'E%s', '%s', '%sB', '%sW', '%sD']  # RAX/EAX/AX/AL-style handled below
    for fam in fams:
        base = fam[1:] if fam[0] == 'R' and fam[1:].isdigit() else fam
        names = []
        if fam[0] == 'R' and fam[1:].isdigit():
            n = fam[1:]
            names = [fam, 'R' + n + 'D', 'R' + n + 'W', 'R' + n + 'B', 'R' + n + 'L']
        else:
            b = base[1:] if base[0] in 'RE' else base  # e.g. AX from RAX
            if b in ('AX', 'CX', 'DX', 'BX'):
                names = [fam, 'E' + b, b, b[0] + 'L', b[0] + 'H']   # RAX,EAX,AX,AL,AH
            else:
                names = [fam, 'E' + b, b, b + 'L']                  # RSI,ESI,SI,SIL
        for nm in names:
            v = getattr(IReg, nm, None)
            if v is not None:
                canon[v] = fam
    for i in range(32):
        for nm in ('XMM%d' % i, 'YMM%d' % i):
            v = getattr(IReg, nm, None)
            if v is not None:
                canon[v] = 'XMM%d' % i
    return canon


REG_CANON = _build_reg_canon() if HAVE_ICED else {}


def reg_name(r) -> str:
    n = REG_CANON.get(r)
    if n:
        return n
    if r is None or r == 0:
        return '?'
    txt = str(r)
    if txt.endswith('.NONE') or txt == 'Register.NONE' or txt == '0':
        return '?'
    m = re.match(r'^(?:Register\.)?(R(?:AX|CX|DX|BX|SP|BP|SI|DI|1?[0-9]))[DWB]?$', txt)
    if m:
        f = m.group(1)
        return 'R' + f if not f[0].isdigit() else f
    m2 = re.match(r'^(?:Register\.)?(XMM\d+)', txt)
    if m2:
        return m2.group(1)
    return txt.split('.')[-1]


# identifier tokens that contain IL-only characters (`<>c`, `<Foo>d__13`,
# `<>9__0_0`, `<P>k__BackingField`); C# can express none of them, even as
# verbatim identifiers, so the file writer mangles `<`/`>` to `_`. The
# match requires a word boundary before the `<` and no trailing word char
# after the `>` run, so `a < b` comparisons and generics like
# `Foo<int>` are untouched.
#
# The third alternative covers a compiler-generated name whose OWN brackets
# carry a type-argument list --
# `<System_Collections_Generic_IEnumerable<T>_GetEnumerator>d__21`, an
# iterator state machine named after the interface it implements. The first
# alternative cannot span the inner `<T>` and the second needs a literal
# `<>`, so that one name reached the file with raw angle brackets and was
# the only parse error on a full 161-image declaration build. One nested
# bracket group is all the compiler emits; legal `List<Foo<int>>` source is
# excluded by the same lookbehind (its `<` follows a word character).
MANGLED_IDENT_RX = re.compile(
    r'(?<![\w`])<?<[\w.`]+(?:`\d+)?>[\w`]*(?:\|[\w`]+)*(?:>[\w`]+)?'
    r'|<>[\w`]*(?:\|[\w`]+)*'
    r'|(?<![\w`])<[\w.]*(?:<[\w.,\s]*>[\w.]*)*>[\w`]*(?:\|[\w`]+)*')


def mangle_generated_ident(text):
    """Replace the angle brackets of compiler-generated identifiers.

    Roslyn spells a state machine `<Method>d__3`, a closure `<>c`, a local
    function `<M>g__F|0_0`, the module's static array class
    `<PrivateImplementationDetails>` -- all of which no C# grammar accepts.
    The heuristic that finds them must not fire on an ordinary shift
    expression: `(section & value) << section >> 32` matched the nested
    angle-bracket alternative (`< section >`) and reached the file as
    `__ section __`, the only parse error on the game tree.

    Two positive proofs, and a skipped match is returned untouched:
    a double underscore (every generated *method*-shaped name carries one:
    `d__`, `c__`, `9__`, `g__`, `b__`, `f__`), or no WHITESPACE at all -- a
    generated name never contains one, while every false positive (a shift or
    comparison inside brackets) does. The second proof is what keeps
    `<PrivateImplementationDetails>` mangled; a `'__'`-only test left its raw
    brackets in every `PrivateImplementationDetails.cs` in the tree.
    """
    t = text or ''
    # A qualified alias path (`global::System.Collections...`) is not a
    # generated name; mangling one produced the undeclarable identifier
    # `global__System...` in five explicit-interface implementations.
    if '::' in t:
        return t
    if '__' not in t and not t.startswith('<>') and (' ' in t or '\t' in t):
        return t
    # ,/[/]/space reach here only inside a generic argument list
    # (<System_Collections_Generic_IEnumerable<A, B>>d__57): the brackets
    # become _, so leaving the separator would print Foo_A, B_, which is
    # not an identifier (four survivors-tree files, 25 parse errors).
    return (t.replace('<', '_').replace('>', '_')
             .replace('.', '_').replace('|', '_')
             .replace(',', '_').replace('[', '_').replace(']', '_')
             .replace(' ', '_').replace(chr(9), '_'))


_NAME_CHARS = set('abcdefghijklmnopqrstuvwxyz'
                  'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
                  '0123456789_.`[]| ,')


def mangle_generated_names(text):
    """Mangle every generated identifier that must be one in the given text.

    The regex form (`MANGLED_IDENT_RX`) cannot see a name whose generic
    arguments nest more than one level, and IL2CPP spells a state machine
    after its whole interface: `LocalizedString.<System_Collections_Generic_
    IEnumerable<System_Collections_Generic_KeyValuePair<System_String,
    UnityEngine.Localization...>>__>d__57` reached four files of the survivors
    tree verbatim (60 tree-sitter ERRORs plus 8 MISSING). This walks the
    brackets instead of matching them: a `<` at an identifier start opens a
    candidate, the candidate is kept only while every character is a
    name character (letters, digits, `_`, `.`, backtick, `[`, `]`, `|`, space)
    and the brackets balance, and `mangle_generated_ident` still applies its
    own two positive proofs to the result.

    A shift or comparison (`(section & value) << section >> 32`) contains
    `&`/`(`, so its candidate fails at once; a string literal is not scanned
    because the caller hands in source text whose literals may contain `<>`,
    which is why the candidate also refuses `"` and `'`.
    """
    if '<' not in text:
        return text
    out = []
    i = 0
    n = len(text)
    while i < n:
        ch = text[i]
        if ch == '<' and i and text[i:i + 2] == '<>' \
                and (text[i - 1].isalnum() or text[i - 1] in '_`'):
            # `CS$<>8__locals2` -> the `$` sanitize leaves `CS_<>8__locals2`,
            # where the empty angle pair sits INSIDE the identifier: mangle
            # from the identifier start, not from the `<`.
            start = i
            while start and (text[start - 1].isalnum() or text[start - 1] in '_`'):
                start -= 1
            k = i + 2
            while k < n and (text[k].isalnum() or text[k] in '_`'):
                k += 1
            # the identifier's own characters are already in `out`
            del out[len(out) - (i - start):]
            out.append(mangle_generated_ident(text[start:k]))
            i = k
            continue
        if ch != '<' or (i and (text[i - 1].isalnum() or text[i - 1] in '_`')):
            out.append(ch)
            i += 1
            continue
        depth = 0
        j = i
        ok = True
        while j < n:
            c = text[j]
            if c == '<':
                depth += 1
            elif c == '>':
                depth -= 1
                if depth == 0:
                    j += 1
                    break
            elif c not in _NAME_CHARS:
                ok = False
                break
            j += 1
        else:
            ok = False
        if not ok or depth != 0:
            out.append(ch)
            i += 1
            continue
        # trailing identifier part (`d__57`, `c`, `9__0_0`)
        k = j
        while k < n and (text[k].isalnum() or text[k] in '_`'):
            k += 1
        cand = text[i:k]
        out.append(mangle_generated_ident(cand))
        i = k
    return ''.join(out)

# An unresolved native value renders the bare text `unknown` (from
# `_rewrite_unknowns` in dec/textpass.py). It is honest and it parses, but it
# does not COMPILE (CS0103) -- 10,940 occurrences on the licensed game tree,
# the largest single compiler-error family. At the file boundary, where the
# value has no type context left to recover, the marker moves into a comment
# and the expression becomes a target-typed `default`: the site now compiles,
# and the text still says the value was not recovered.
#
# Only shapes whose target type is certain qualify -- an assignment RHS and a
# `return` (every recovered declaration spells its type; the tree contains no
# `var`), plus a member access on an unknown value (the member is fabricated,
# so the whole expression becomes the marker). `unknown` inside a larger
# expression (`unknown + 1`, `f(unknown, 2)`, an operand of `==`) keeps the
# old text: `default` there would need a type the tree does not have.
_UNKNOWN_RHS_RX = re.compile(r'=\s*unknown\s*;')
_UNKNOWN_RETURN_RX = re.compile(r'\breturn\s+unknown\s*;')
# A member access on an unresolved value renders `unknown.Member`; the whole
# CHAIN and any call argument list must go with it. `unknown.GetEnumerator(0)`
# used to become `/*unknown*/ default(0)` (the arguments were left behind) and
# `unknown.a.b` became `/*unknown*/ default.b` -- both unparseable; the game
# tree's last two syntax-error files were exactly this shape. One level of
# nested parentheses is allowed because an argument can itself be a call
# (`AddComponent(list, new Provider<T>())`).
_UNKNOWN_CHAIN = r'unknown(?:\.[A-Za-z_]\w*)+(?:\((?:[^()]|\([^()]*\))*\))?'
_UNKNOWN_MEMBER_RX = re.compile(r'(?<![\w.])' + _UNKNOWN_CHAIN)
# The same chain as a whole STATEMENT: `default;` is not a C# expression
# statement, so the statement form becomes the marker alone (`/*unknown call*/;`).
_UNKNOWN_CHAIN_STMT_RX = re.compile(r'^(\s*)' + _UNKNOWN_CHAIN + r'\s*;$')
# A conditional expression's condition is required to be `bool`, so the
# target type IS known even though the value is not (658 sites on the game
# tree). `default` alone would have no type there (CS8716), so the spelling
# carries it. The literal space is load-bearing: `unknown?` is a nullable
# TYPE marker, never a condition.
_UNKNOWN_COND_RX = re.compile(r'(?<![\w.])unknown(\s+)\?')
# A call whose CALLEE was never resolved renders as `?(args)` (the lifter's
# placeholder register). That is not an expression: `object o = ?(pUnk);`
# broke the parse of three emitted images (mscorlib Marshal, Plugins, TMPro).
# The call's value is exactly an unresolved value, so it takes the marker and
# the rules above turn the surrounding shape into something that compiles.
_UNK_CALL_RX = re.compile(r'(?<![\w.\])])\?\(([^()]*)\)')
# The same call in STATEMENT position: a bare `unknown;` is not a C#
# expression statement either, so it becomes the marker alone.
_UNKNOWN_STMT_RX = re.compile(r'^(\s*)unknown\s*;$')


def _sub_unknown_calls(line, masked):
    """`?(args)` -> the `unknown` marker, literal-aware."""
    spans = [m.span() for m in _UNK_CALL_RX.finditer(masked)]
    if not spans:
        return line
    out, last = [], 0
    for a, b in spans:
        out.append(line[last:a])
        out.append('unknown')
        last = b
    out.append(line[last:])
    return ''.join(out)


def spell_unresolved_values(text):
    """Make the `unknown` marker compile without hiding it.

    ``= unknown;`` and ``return unknown;`` become the marker plus a
    target-typed ``default``; ``unknown.Member`` (a member access on an
    unresolved value, whose name is fabricated) becomes the marker alone; a
    conditional's condition becomes ``default(bool)``, whose type the grammar
    guarantees; a call on an unresolved callee (``?(args)``) becomes the marker
    in value position and the bare marker in statement position. Literal-aware:
    the scans run on the NUL-masked line, so a string or comment that spells
    any of this is untouched.
    """
    out = []
    in_block = False
    for line in text.split('\n'):
        masked, in_block = mask_spans(line, in_block)
        if '?' in masked:
            line = _sub_unknown_calls(line, masked)
            masked, in_block = mask_spans(line, in_block)
        stmt = _UNKNOWN_STMT_RX.match(masked)
        if stmt is not None and masked.strip() == 'unknown;':
            out.append('%s/*unknown call*/;' % stmt.group(1))
            continue
        chain_stmt = _UNKNOWN_CHAIN_STMT_RX.match(masked)
        if chain_stmt is not None:
            out.append('%s/*unknown call*/;' % chain_stmt.group(1))
            continue
        if 'unknown' not in masked:
            out.append(line)
            continue
        pieces = []
        last = 0
        for rx, repl in ((_UNKNOWN_MEMBER_RX, '/*unknown*/ default'),
                         (_UNKNOWN_RHS_RX, '= /*unknown*/ default;'),
                         (_UNKNOWN_RETURN_RX, 'return /*unknown*/ default;'),
                         (_UNKNOWN_COND_RX, '/*unknown*/ default(bool) ?')):
            pos = 0
            while True:
                m = rx.search(masked, pos)
                if m is None:
                    break
                pieces.append((m.start(), m.end(), repl))
                pos = m.end()
        if not pieces:
            out.append(line)
            continue
        pieces.sort()
        rebuilt = []
        for start, end, repl in pieces:
            if start < last:
                continue          # overlapping match: the earlier one won
            rebuilt.append(line[last:start])
            rebuilt.append(repl)
            last = end
        rebuilt.append(line[last:])
        out.append(''.join(rebuilt))
    return '\n'.join(out)


def _brace_scan(line):
    """(leading_closers, opens, closes) for one line, skipping braces that
    live inside string/char literals or a `//` comment tail. `leading_closers`
    counts `}` that appear before any other non-space token, which is what
    makes `} else {` and `});` dedent to the level of their opener."""
    opens = closes = lead = 0
    seen_other = False
    i = 0
    n = len(line)
    while i < n:
        c = line[i]
        if c == '/' and i + 1 < n and line[i + 1] == '/':
            break
        if c in '"\'':
            q = c
            i += 1
            while i < n:
                if line[i] == '\\':
                    i += 2
                    continue
                if line[i] == q:
                    break
                i += 1
            seen_other = True
        elif c == '{':
            opens += 1
            seen_other = True
        elif c == '}':
            closes += 1
            if not seen_other:
                lead += 1
        elif not c.isspace():
            seen_other = True
        i += 1
    return lead, opens, closes


def reindent(content, unit='    '):
    """Re-lay every line at its true brace depth.

    Emitters that thread an `indent` string through nested calls drift by a
    level whenever one construct forgets to deepen it, and the result reads
    as a body sitting outside its own braces. Depth is a property of the
    text, so recompute it from the text and stop threading it.

    Idempotent on already-correct files. Bails out unchanged if the braces
    do not balance or a string literal spans a line break -- a formatter is
    never worth corrupting output for."""
    lines = content.split('\n')
    for l in lines:
        # an unterminated literal means the naive per-line scan is unsafe
        q = 0
        i = 0
        while i < len(l):
            if l[i] == '\\':
                i += 2
                continue
            if l[i] in '"\'':
                q += 1
            i += 1
        if q % 2:
            return content
    out = []
    depth = 0
    for raw in lines:
        s = raw.strip()
        if not s:
            out.append('')
            continue
        lead, opens, closes = _brace_scan(s)
        depth -= lead
        if depth < 0:
            return content
        out.append(unit * depth + s)
        depth += opens - (closes - lead)
        if depth < 0:
            return content
    if depth != 0:
        return content
    return '\n'.join(out)


def va_in(t, ip, end):
    return ip < t <= end


def sign_of(v, ins):
    return v


def rty_has_value(lifter, rty):
    if rty is None:
        return False
    return ((rty[1] >> 16) & 0xFF) != 0x01


def imm_of(ins, opnd=1) -> int:
    try:
        v = ins.immediate(opnd)
    except Exception:
        return 0
    if v > 0x7FFFFFFFFFFFFFFF:
        v -= 1 << 64
    return v


def sdisp(d):
    """Sign-extend a memory displacement from its unsigned 64-bit encoding:
    stack offsets arrive as 0xffffffffffffffe8, meaning -0x18."""
    if d > 0x7FFFFFFFFFFFFFFF:
        d -= 1 << 64
    return d


def disp_add(d):
    """Render a displacement as `+ 0xNN` / `- 0xNN` for `*(base ...)` text."""
    d = sdisp(d)
    if d < 0:
        return '- %#x' % -d
    return '+ %#x' % d


# ---- arithmetic rendering: folding + precedence-aware parentheses --------
_BIN_PREC = {'|': 1, '^': 2, '&': 3, '<<': 4, '>>': 4,
             '+': 5, '-': 5, '*': 6, '/': 6, '%': 6}
_ATOM_PREC = 99


def _term_up(s, mul=False):
    """Guard a text substituted into a `X*N`-style address template
    (`*(%s + %s*%d ...)`): an operator that binds looser than `*`
    must be parenthesized or `v + 2*8` silently means `v + (2*8)`
    instead of `(v + 2)*8`. mul=True also guards `+`/`-`, the
    operators the *index* position sits next to. Atomic tokens and
    already-fully-parenthesized texts pass through untouched."""
    if not s:
        return s
    if _outer_parens(s):
        return s
    loose = '[|^&<>?:+-]' if mul else '[|^&<>?:]'
    if re.search(loose, s):
        return '(%s)' % s
    return s


def _int_lit(t):
    """Parse an integer literal text (hex/decimal, optional f/d suffix)."""
    if not t:
        return None
    # `d` and `f` are hex DIGITS, not a float suffix: stripping them from a
    # hex literal silently truncates it (`0x3d` -> 3 instead of 61, `0x7f`
    # -> 7 instead of 127, `0xf` -> unparseable). Only decimal-looking text
    # can carry a float suffix -- `0f`/`1d` are the forms _fold_bin's
    # identity rules depend on, so those must keep parsing -- fix 87
    body = t if t.lstrip('+-')[:2].lower() == '0x' else t.rstrip('fFdD')
    try:
        return int(body, 0)
    except ValueError:
        return None


def _paren_spans_all(s):
    """True when s starts with `(` and that paren closes on its LAST
    character -- i.e. the parens cover the whole expression, so a bare
    `*` prefix derefs all of it. `(a + b)` yes; `(a << 4) + c` no."""
    if not s.startswith('('):
        return False
    depth = 0
    for k, ch in enumerate(s):
        if ch == '(':
            depth += 1
        elif ch == ')':
            depth -= 1
            if depth == 0:
                return k == len(s) - 1
    return False


def _deref_spans_all(s):
    """True when s is already a deref of its WHOLE self: `*(...)` or
    `*(...)[i]`. Nesting-aware, unlike a `[^)]*` regex."""
    if not s.startswith('*'):
        return False
    rest = s[1:]
    if _paren_spans_all(rest):
        return True
    m = re.match(r'^(.*)(\[[^\[\]]*\])$', rest, re.S)
    return bool(m) and _paren_spans_all(m.group(1))


_WIDE_TWIN_CASTS = frozenset((
    'short', 'int', 'long', 'ushort', 'uint', 'ulong',
    'float', 'double', 'char', 'bool', 'byte', 'sbyte'))


def _canon_wide_cast(s):
    """`((T*)inner)[0]` -> `*(inner)` for primitive pointer casts.

    Fix 102 renders raw native-width stores width-preserving while the
    write-barrier twin still renders raw, so the twin comparison meets
    on the raw spelling. Recursive: a width cast can wrap a byte-cast
    read (`((uint*)((byte*)b + 0x10)[0] + N)[0]`). Anything unparseable
    passes through unchanged; non-cast parens never match (the `*`
    before `)` is required).
    """
    out = []
    i, n = 0, len(s)
    while i < n:
        m = None
        if s.startswith('((', i):
            m = re.match(r'\(\(([A-Za-z_][\w$]*)\*\)', s[i:])
            if m is not None and m.group(1) not in _WIDE_TWIN_CASTS:
                m = None
        if m is not None:
            k = i + m.end()
            depth, j = 0, k
            while j < n:
                if s[j] == '(':
                    depth += 1
                elif s[j] == ')':
                    if depth == 0:
                        break
                    depth -= 1
                j += 1
            if j < n and s.startswith('[0]', j + 1):
                inner = s[k:j]
                # fix 124: the wide spelling byte-addresses its offset,
                # `((T*)((byte*)E + N))[0]`; the raw twin is `*(E + N)`.
                if inner.startswith('((byte*)') and _paren_spans_all(inner):
                    inner = inner[len('((byte*)'):-1]
                out.append('*(' + _canon_wide_cast(inner) + ')')
                i = j + 4
                continue
        out.append(s[i])
        i += 1
    return ''.join(out)

def _norm_twin(s):
    """Whitespace/radix-normalized statement text for plain-store vs
    write-barrier twin comparison: the same native write renders once as
    `*(v + i*8 + 0x20) = x;` (memory operand) and once as `*(v + i * 8 +
    32) = x;` (lea/add-chain address) -- same target, two spellings."""
    if not s:
        return s
    s = re.sub(r'\s+', '', s)
    s = _canon_wide_cast(s)

    def hexlit(m):
        s = m.group(0).lstrip('0') or '0'
        v = int(s, 0)
        return '%#x' % v if v > 9 else str(v)

    return re.sub(r'(?<![\w.])\d+(?![\w.])', hexlit, s)


def _outer_parens(t):
    """True when t's first '(' matches its last ')' -- the whole text is one
    parenthesised group (string literals respected, so casts and call
    arguments like `(int)(x)` / `Foo(a, b)` never qualify)."""
    if len(t) < 2 or t[0] != '(' or t[-1] != ')':
        return False
    depth = 0
    q = None
    for i, c in enumerate(t):
        if q is not None:
            if c == q:
                q = None
            continue
        if c in '"\'':
            q = c
        elif c == '(':
            depth += 1
        elif c == ')':
            depth -= 1
            if depth == 0 and i != len(t) - 1:
                return False
    return depth == 0


def _has_top_ternary(t):
    """True when t has a `?`/`:` ternary pair at bracket depth 0 (`?.`/`??`
    are member-access/null-coalesce, not this operator; strings are
    respected the same way `_outer_parens` respects them)."""
    depth = 0
    q = None
    seen_q = False
    n = len(t)
    i = 0
    while i < n:
        c = t[i]
        if q is not None:
            if c == q:
                q = None
            i += 1
            continue
        if c in '"\'':
            q = c
        elif c in '([{':
            depth += 1
        elif c in ')]}':
            depth -= 1
        elif depth == 0 and c == '?' and t[i + 1:i + 2] not in ('.', '?'):
            seen_q = True
        elif depth == 0 and c == ':' and seen_q:
            return True
        i += 1
    return False


def strip_outer(t):
    """Remove one redundant outermost paren layer (statement-level RHS).
    Never strips a layer that's protecting a top-level ternary: `?:` binds
    looser than everything else, so once this text is embedded as an
    OPERAND elsewhere (not every caller is statement-level -- the
    conditional-branch builder composes `lt OP rhs` from it), `(cond ? a :
    b) OP c` and `cond ? a : b OP c` are different expressions. Found
    live: a CMOV-derived ternary losing its parens there and reading as
    `if (cond ? a : b <= null)` -- parses as `cond ? a : (b <= null)`, not
    `(cond ? a : b) <= null` -- batch 27."""
    while _outer_parens(t) and not _has_top_ternary(t[1:-1]):
        t = t[1:-1].strip()
    return t


def _bin_txt(a_txt, ap, op, b_txt, bp):
    """Compose `a op b` with precedence-aware grouping: a left operand
    groups only below the operator's precedence (left associativity lets
    equal precedence shed), a right operand groups at or below it
    (`a - (b - c)` is not `a - b - c`). ap/bp are the operands' own
    operator precedences (_ATOM_PREC for anything not built here)."""
    p = _BIN_PREC[op]
    if ap < p:
        if not _outer_parens(a_txt):
            a_txt = '(' + a_txt + ')'
    elif _outer_parens(a_txt) and not _has_top_ternary(a_txt[1:-1]):
        a_txt = a_txt[1:-1].strip()
    if bp <= p:
        if not _outer_parens(b_txt):
            b_txt = '(' + b_txt + ')'
    elif _outer_parens(b_txt) and not _has_top_ternary(b_txt[1:-1]):
        b_txt = b_txt[1:-1].strip()
    return '%s %s %s' % (a_txt, op, b_txt)


def _fold_bin(a_txt, ap, op, b_txt, bp):
    """Fold what composition-time constant arithmetic allows: negative
    immediates normalise to a flipped operator (`x + -1` -> `x - 1`),
    literal-literal pairs evaluate, and the algebraic identities against
    0/1 drop out. Returns (text, prec) or None to keep the general path."""
    flipped = False
    if op in ('+', '-'):
        vb0 = _int_lit(b_txt)
        if vb0 is not None and vb0 < 0:
            op = '-' if op == '+' else '+'
            b_txt = str(-vb0)
            flipped = True
    va = _int_lit(a_txt)
    vb = _int_lit(b_txt)
    if va is not None and vb is not None:
        try:
            if op == '+':
                r = va + vb
            elif op == '-':
                r = va - vb
            elif op == '*':
                r = va * vb
            elif op == '&':
                r = va & vb
            elif op == '|':
                r = va | vb
            elif op == '^':
                r = va ^ vb
            elif op == '<<':
                r = (va << (vb & 63)) if 0 <= vb < 64 else None
            elif op == '>>':
                r = va >> vb if 0 <= vb < 64 else None
            elif op in ('/', '%'):
                r = None if vb == 0 else int(va / vb) if op == '/' else va - int(va / vb) * vb
            else:
                r = None
        except Exception:
            r = None
        if r is not None:
            if r > 0x7FFFFFFFFFFFFFFF:
                r -= 1 << 64
            return str(r), _ATOM_PREC
    # identities: x op 0 / x op 1 / x * 0 ...
    if a_txt != b_txt:
        if op in ('+', '-', '|') and b_txt in ('0', '0f', '0d'):
            return a_txt, ap
        if op in ('^', '<<', '>>') and b_txt == '0':
            return a_txt, ap
        if op == '&' and b_txt in ('0', '-1'):
            return ('0' if b_txt == '0' else a_txt), _ATOM_PREC
        if op == '*' and b_txt in ('1', '1f', '1d'):
            return a_txt, ap
        if op == '*' and b_txt in ('0', '0f', '0d'):
            return '0', _ATOM_PREC
        if op == '/' and b_txt in ('1', '1f', '1d'):
            return a_txt, ap
        if op in ('+', '|') and a_txt in ('0', '0f', '0d'):
            return b_txt, bp
        if op == '*' and a_txt in ('0', '0f', '0d'):
            return '0', _ATOM_PREC
        if op == '*' and a_txt in ('1', '1f', '1d'):
            return b_txt, bp
        if op == '-' and a_txt == '0' and vb is not None:
            return str(-vb), _ATOM_PREC
    if flipped:
        return _bin_txt(a_txt, ap, op, b_txt, bp), _BIN_PREC[op]
    return None


# ----------------------------------------------------------------------------
# C# emitter
# ----------------------------------------------------------------------------

# CLI member accessibility (MethodAttributes/FieldAttributes low 3 bits)
