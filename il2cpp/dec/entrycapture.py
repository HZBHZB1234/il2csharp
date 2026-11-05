"""Transactional entry-Int32 recovery: baseline first, disjoint attempt second.

A failed attempt never reuses its lifter, runtime, caches or synthetic addresses.
The caller's baseline lifter/decompiler remain the authoritative continuation,
including Emitter.lifter's flat fallback. No candidate state is committed.
"""
import bisect
from collections import defaultdict, deque
import copy
import re
import sys
from types import ModuleType, SimpleNamespace

from il2cpp.lifter.entrycapture import EntryInt32Captures
from il2cpp.lifter.entryorigin import EntryInt32Origin
from il2cpp.lifter.unwindproof import NativeUnwindCache
from il2cpp.names import safe_ident
from il2cpp.metadata import TypeDef, MethodDef, FieldDef, ParamDef, ImageDef
from il2cpp.runtime.types import _SYNTH_NEXT_VA


class ArenaDeclined(ValueError):
    pass


_ATOMIC_TYPES = frozenset((str, bytes, int, float, bool, complex, type(None), range))
_METADATA_RECORDS = frozenset((TypeDef, MethodDef, FieldDef, ParamDef, ImageDef))
_COPY_HOOKS = ('__slots__', '__deepcopy__', '__getstate__', '__setstate__',
               '__reduce__', '__reduce_ex__', '__new__', '__getattribute__',
               '__getattr__', '__setattr__')


def _metadata_leaf_types():
    # Exact plain records only. Future inheritance, slots or copy hooks must
    # take the full graph path, not silently lose state or bypass a hook.
    return frozenset(ty for ty in _METADATA_RECORDS
                     if ty.__bases__ == (object,)
                     and getattr(sys.modules.get(ty.__module__), ty.__name__, None) is ty
                     and not any(name in ty.__dict__ for name in _COPY_HOOKS))


def _scalar_record_state(obj, leaf_types):
    if type(obj) not in leaf_types:
        return None
    state = vars(obj)
    if (type(state) is dict
            and all(type(key) is str and type(value) in _ATOMIC_TYPES
                    for key, value in state.items())):
        return state
    return None


def _seed_metadata_memo(mutable, memo):
    """Preallocate independent scalar records; never share a mutable leaf.

    Seed the record AND its state dict. This keeps repeated references and two
    records sharing one state dict attached to the same private copied state.
    Nested/mutable attributes and subclasses use ordinary deepcopy instead.
    """
    leaf_types = _metadata_leaf_types()
    count = 0
    for key, obj in mutable.items():
        state = _scalar_record_state(obj, leaf_types)
        if state is None:
            continue
        clone = object.__new__(type(obj))
        memo[key] = clone
        if id(state) not in memo:
            memo[id(state)] = state.copy()
        clone.__dict__ = memo[id(state)]
        count += 1
    return count


def _restore_state_aliases(mutable, memo):
    # deepcopy reconstructs Python objects with __dict__.update(state), which
    # detaches an externally held reference to that state dict. Restore the
    # canonical memo dict after checking it describes exactly the copied object.
    # Do not guess how custom state/copy hooks transformed an ordinary model.
    for key, obj in mutable.items():
        if type(obj) in (dict, list, set, defaultdict, deque):
            continue
        if not hasattr(obj, '__dict__'):
            continue
        copied_state = memo.get(id(vars(obj)))
        clone = memo[key]
        state = vars(clone)
        if state is copied_state:
            continue
        if (type(state) is not dict or type(copied_state) is not dict
                or len(state) != len(copied_state)
                or any(name not in state or state[name] is not value
                       for name, value in copied_state.items())):
            raise ArenaDeclined('nonstandard copied model state')
        object.__setattr__(clone, '__dict__', copied_state)


def _mutable_graph(roots, immutable_memo=None):
    """Admit only the model's ordinary data graph, not callbacks/resources.

    In particular, deepcopy shares functions/closures silently. They are not
    allowed to smuggle a reference to the live runtime into an attempt. The
    only admitted module is bisect, stored by the runtime as a pure search API.
    """
    atomic = _ATOMIC_TYPES
    leaf_types = _metadata_leaf_types()
    containers = (list, dict, tuple, set, frozenset, defaultdict, deque)
    work = list(roots)
    seen, mutable = set(), {}
    while work:
        obj = work.pop()
        ty = type(obj)
        if ty in atomic:
            continue
        if ty is ModuleType:
            if obj is not bisect:
                raise ArenaDeclined('unsupported module in attempt state')
            continue
        key = id(obj)
        if key in seen:
            continue
        seen.add(key)
        if ty is tuple and all(type(value) in atomic for value in obj):
            # deepcopy already shares these exact immutable tuples, but still
            # revisits every element at every occurrence. Admit them once and
            # seed that same result; nested/mutable tuples and subclasses keep
            # the full graph path. Never seed an unproved mutable model node.
            if immutable_memo is not None:
                immutable_memo[key] = obj
            continue
        if ty in containers:
            if ty not in (tuple, frozenset):
                mutable[key] = obj
            if isinstance(obj, dict):
                work.extend(obj.keys())
                work.extend(obj.values())
                if ty is defaultdict and obj.default_factory is not None:
                    # Builtin factories are immutable, closure-free types.
                    if obj.default_factory not in (list, dict, set, int):
                        raise ArenaDeclined('unsupported cache factory')
            else:
                work.extend(obj)
            continue
        state = _scalar_record_state(obj, leaf_types)
        if state is not None:
            # All state edges are already proved immutable atoms. Still admit
            # both mutable nodes, including externally held/shared state dicts.
            mutable[key] = obj
            mutable[id(state)] = state
            seen.add(id(state))
            continue
        module = getattr(ty, '__module__', '')
        trusted = (module.startswith('il2cpp.') or module == 'iced_x86._iced_x86_py')
        if (not trusted or getattr(sys.modules.get(module), ty.__name__, None) is not ty):
            raise ArenaDeclined('unsupported object in attempt state: ' + module + '.' + ty.__name__)
        mutable[key] = obj
        # Trusted model containers (notably _RegState(dict)) own BOTH their
        # container payload and their attributes/slots. Traversing only slots
        # misses register Exprs and can let a deepcopy-shared callback escape.
        if isinstance(obj, dict):
            work.extend(obj.keys())
            work.extend(obj.values())
            if isinstance(obj, defaultdict) and obj.default_factory is not None:
                if obj.default_factory not in (list, dict, set, int):
                    raise ArenaDeclined('unsupported model cache factory')
        elif isinstance(obj, (list, tuple, set, frozenset, deque)):
            work.extend(obj)
        if hasattr(obj, '__dict__'):
            work.append(vars(obj))
        for cls in ty.__mro__:
            slots = cls.__dict__.get('__slots__', ())
            if isinstance(slots, str):
                slots = (slots,)
            for slot in slots:
                if slot not in ('__dict__', '__weakref__') and hasattr(obj, slot):
                    work.append(getattr(obj, slot))
    return mutable


def isolated_clone(decompiler, method, owner):
    """Copy the complete reachable model, proving no mutable model is shared."""
    memo = {id(bisect): bisect}
    mutable = _mutable_graph((decompiler, method, owner), immutable_memo=memo)
    _seed_metadata_memo(mutable, memo)
    arena, copied_method, copied_owner = copy.deepcopy((decompiler, method, owner), memo)
    if any(key not in memo or memo[key] is obj for key, obj in mutable.items()):
        raise ArenaDeclined('attempt retained mutable baseline state')
    _restore_state_aliases(mutable, memo)
    # The ordinary process-wide synthetic VA allocator is not in the object
    # graph. Do not reserve from it, restore it, or let speculative calls use it.
    arena.L.il._synthetic_allocator = [_SYNTH_NEXT_VA[0]]
    arena._entry_int32_recovery = False
    arena.L._entry_int32_capture = None
    if (arena.L.il is decompiler.L.il or arena.L is decompiler.L
            or arena.L.meta is decompiler.L.meta or arena.L.bin is decompiler.L.bin
            or arena.L.il.meta is not arena.L.meta
            or arena.L.il.bin is not arena.L.bin
            or arena.L.meta.methods[copied_method.index] is not copied_method
            or arena.L.meta.typedefs[copied_method.declaring] is not copied_owner):
        raise ArenaDeclined('inconsistent copied method context')
    return arena, copied_method, copied_owner


def _unwind_cache(decompiler):
    # Created only by the opt-in path, after the cheap candidate filters. The
    # complete object is cloned with the arena; never lend it a live proof.
    cache = getattr(decompiler, '_entry_int32_unwind', None)
    if cache is None:
        cache = decompiler._entry_int32_unwind = NativeUnwindCache()
    if type(cache) is not NativeUnwindCache:
        raise ArenaDeclined('unsupported unwind cache')
    return cache


def _candidate(decompiler, method):
    from iced_x86 import Mnemonic

    lift = decompiler.L
    insns = getattr(decompiler, '_flat_insns', ())
    if (getattr(lift, 'asm_comments', False) or getattr(decompiler, 'eh', None)
            or getattr(lift, '_current_method', None) is not method
            or not insns or len(insns) > 512
            or not any(ins.mnemonic == Mnemonic.CVTDQ2PS for ins in insns)):
        return False
    origin = EntryInt32Origin(lift.il, method, insns,
                              unwind_cache=_unwind_cache(decompiler))
    # Do not replace the live sink or read symbolic registers for preflight.
    probe = SimpleNamespace(il=lift.il, bin=lift.bin, meta=lift.meta,
                            _current_method=method)
    for block in getattr(lift, '_blocks', ()):
        probe.out = SimpleNamespace(block=block)
        for ins in block.insns:
            if (ins.mnemonic == Mnemonic.CVTDQ2PS
                    and origin.parameter_at(probe, ins, block.insns) is not None):
                return True
    return False


def _marker_reservations(metadata, baseline):
    # All metadata spellings are included, even fields/types/properties hidden
    # in baseline output. A later cleanup may expose one of these symbols.
    backing, offset, size = metadata.d, metadata.string_off, metadata.string_size
    if type(backing) is not bytes:
        raise ArenaDeclined('mutable metadata name table')
    if (type(offset) is not int or type(size) is not int
            or offset < 0 or size < 0 or offset > len(backing)
            or size > len(backing) - offset):
        raise ArenaDeclined('invalid metadata name-table bounds')
    data = backing[offset:offset + size]
    if data and not data.endswith(b'\0'):
        raise ArenaDeclined('unterminated metadata name table')
    reserved = set(re.findall(r'\w+', '\n'.join(baseline)))
    for raw in data.split(b'\0'):
        name = safe_ident(raw.decode('utf-8', 'replace'))
        reserved.update(re.findall(r'\w+', name))
    return reserved


def recover_entry_int32(decompiler, method, owner, baseline):
    """Return baseline unchanged unless the *whole* arena attempt commits."""
    decompiler._entry_int32_status = 'not-candidate'
    try:
        if not _candidate(decompiler, method):
            return baseline
        decompiler._entry_int32_status = 'declined'
        arena, copied_method, copied_owner = isolated_clone(decompiler, method, owner)
        capture = EntryInt32Captures(arena.L.il, copied_method,
                                     arena._flat_insns,
                                     unwind_cache=_unwind_cache(arena),
                                     reserved=_marker_reservations(arena.L.meta, baseline))
        arena.L._entry_int32_capture = capture
        lines = arena._lift_method(copied_method, copied_owner)
        lines, count = capture.finalize(lines, arena._mask_literals)
        if not count:
            return baseline
        decompiler._entry_int32_status = 'accepted'
        return lines
    except Exception:
        # A partial body, a partially updated register file or a cache from the
        # attempt must never be used as a fallback. The baseline is already
        # complete; the entire arena becomes unreachable here.
        return baseline
