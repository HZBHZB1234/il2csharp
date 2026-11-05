"""Per-execution entry binding and post-cleanup immutable Int32 captures.

Only an isolated decompiler arena installs this object. Native ownership and
all-path origin remain the independent EntryInt32Origin proof. A successful
conversion returns a fresh Expr, never rewrites the parameter or register map.
"""
import re

from il2cpp.expr import Expr
from il2cpp.lifter.entryorigin import EntryInt32Origin
from il2cpp.names import safe_ident
from il2cpp.x64 import ARG_REGS


class EntryCaptureDeclined(ValueError):
    """The entire speculative body must be discarded, not partly repaired."""


class EntryInt32Captures:
    def __init__(self, il, method, insns, *, reserved=(), unwind_cache=None):
        self._reserved = frozenset(reserved)
        self.origin = EntryInt32Origin(il, method, insns, unwind_cache=unwind_cache)
        self.method = method
        self._lift = None
        self._bindings = {}
        self._used = {}
        # Dry values can survive through phi/end-state caches into real output.
        # Keep the lifetime set separate from each execution's proved uses.
        self._generated = set()
        self._real = False

    def bind_entry(self, lift, method, *, real):
        # _setup_entry runs independently for the dry and the real pass.
        self._lift = None
        self._bindings = {}
        self._used = {}
        self._real = False
        if (type(real) is not bool or method is not self.method
                or lift.il is not self.origin.il
                or lift.meta is not self.origin.meta
                or lift.bin is not self.origin.bin
                or getattr(lift, '_current_method', None) is not method):
            return
        params = lift.meta.method_params(method)
        names = [safe_ident(p.name) for p in params]
        if (len({n.lstrip('@') for n in names}) != len(names)
                or any(re.fullmatch(r'@?[A-Za-z_]\w*', n) is None for n in names)):
            return
        base = int(lift.il.returns_sret(lift.il.types[method.return_type]))
        base += int(not method.is_static)
        reserved = set(self._reserved) | {n.lstrip('@') for n in names}
        for pi, param in enumerate(params):
            if base + pi >= 4:
                continue
            ty = lift.il.types[param.type]
            if not self.origin._int32(ty):
                continue
            # Side probes must not count/stamp a symbolic register use.
            value = dict.get(lift.regs, ARG_REGS[base + pi])
            if (value is None or value.text != names[pi] or value.ty != ty
                    or value.kind != 'int'):
                continue
            marker = '__il2cpp_capture_i32_' + str(pi)
            # Cleanup can expose suffixes (for example get_X -> X). Reserve
            # substrings too, not just whole metadata/baseline identifiers.
            while any(marker in name for name in reserved):
                marker += '_'
            reserved.add(marker)
            self._bindings[pi] = (value, marker, names[pi], ty)
        self._lift = lift
        self._real = real

    def conversion_input(self, lift, conversion, block_insns, value):
        if (lift is not self._lift
                or getattr(lift, '_current_method', None) is not self.method
                or self._real != (not lift.dry)
                or getattr(lift.out, 'block', None) is None
                or lift.out.block.insns is not block_insns
                or value is None or value.kind != 'int' or value._unk
                or value._no_bind or not self.origin._int32(value.ty)
                or any(getattr(value, k, None) is not None for k in
                       ('_slice', '_parts', '_bytes', '_stack_offset'))):
            return None
        pi = self.origin.parameter_at(lift, conversion, block_insns)
        record = self._bindings.get(pi)
        if record is None:
            return None
        original, marker, parameter, ty = record
        if original is not value or original.text != parameter or value.ty != ty:
            return None
        self._used[marker] = parameter
        self._generated.add(marker)
        return Expr(marker, ty, 'int')

    def finalize(self, lines, mask_literals):
        """Commit only exact generated cast operands after *all* cleanup.

        Raw/masked occurrence equality also rejects markers hidden in a string
        interpolation or comment; lexical masking alone cannot prove a marker
        was removed. Every final alias is fresh across all identifier spellings,
        including fields, labels, escaped names and parameters. An alias is only
        read as an Int32 value in a float cast, never passed by managed address.
        """
        if self._lift is None or not self._real:
            raise EntryCaptureDeclined('no matching real entry execution')
        source = '\n'.join(lines)
        masked, block_comment = [], False
        for line in lines:
            code, block_comment = mask_literals(line, block_comment)
            masked.append(code)
        code = '\n'.join(masked)
        if len(code) != len(source):
            raise EntryCaptureDeclined('literal mask changed source coordinates')
        reserved = set(re.findall(r'\w+', source))
        reserved.update(safe_ident(p.name).lstrip('@') for p in
                        self._lift.meta.method_params(self.method))
        # A dry-only marker must not escape just because another parameter has
        # a valid real-pass capture. Reject the whole attempt, never patch it
        # with an unproved declaration or silently leave it undeclared.
        for marker in self._generated - self._used.keys():
            if re.search(r'(?<!\w)' + re.escape(marker) + r'(?!\w)', source):
                raise EntryCaptureDeclined('surviving capture has no real-pass proof')
        replacements, declarations = [], []
        for marker, parameter in sorted(self._used.items()):
            token = re.compile(r'(?<!\w)' + re.escape(marker) + r'(?!\w)')
            raw_uses = {m.span() for m in token.finditer(source)}
            if not raw_uses:
                continue
            uses = {m.span() for m in token.finditer(code)}
            cast = re.compile(r'\(float\)\s*\(\s*(?P<value>'
                              + re.escape(marker) + r')\s*\)')
            operands = {m.span('value') for m in cast.finditer(code)}
            if raw_uses != uses or uses != operands:
                raise EntryCaptureDeclined('capture is not an exact float-cast operand')
            # A preceding . or @ would make this a member/escaped identifier,
            # not the generated local even though the cast text looks alike.
            if any(start and code[start - 1] in '.@' for start, _ in uses):
                raise EntryCaptureDeclined('capture identifier was qualified')
            alias = marker.replace('__il2cpp_capture_', '__il2cpp_entry_', 1)
            while alias in reserved:
                alias += '_'
            reserved.add(alias)
            declarations.append('int ' + alias + ' = ' + parameter + ';')
            replacements.extend((start, end, alias) for start, end in uses)
        if not declarations:
            return list(lines), 0
        for start, end, alias in sorted(replacements, reverse=True):
            source = source[:start] + alias + source[end:]
        if any(re.search(r'(?<!\w)' + re.escape(marker) + r'(?!\w)', source)
               for marker in self._generated):
            raise EntryCaptureDeclined('capture marker survived replacement')
        result = source.split('\n')
        # Only the canonical envelope emitted by _structure is supported.
        if result[:2] == ['unsafe', '{']:
            result[2:2] = declarations
        elif result and re.match(r'^\s*unsafe\b', result[0]):
            raise EntryCaptureDeclined('unsupported unsafe envelope')
        else:
            result[:0] = declarations
        return result, len(declarations)
