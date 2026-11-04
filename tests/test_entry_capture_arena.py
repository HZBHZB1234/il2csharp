"""Scalar-leaf cloning and authored arena graph-alias regressions."""
import bisect
import copy
from dataclasses import fields

import pytest

from il2cpp import metadata
from il2cpp.dec import entrycapture as arena_module
from il2cpp.dec.entrycapture import ArenaDeclined, _mutable_graph, isolated_clone
from il2cpp.metadata import FieldDef, ImageDef, MethodDef, ParamDef, TypeDef
from test_entry_int32_capture import model

RECORDS = (TypeDef, MethodDef, FieldDef, ParamDef, ImageDef)


def record(ty=ParamDef):
    return ty(**{field.name: 'value' if field.name in ('name', 'namespace') else 0
                 for field in fields(ty)})


def seed(roots):
    graph = _mutable_graph(roots)
    memo = {id(bisect): bisect}
    count = arena_module._seed_metadata_memo(graph, memo)
    return graph, memo, count


@pytest.mark.parametrize('place', ['metadata-leaf', 'metadata-root', 'decompiler', 'lifter'])
def test_external_state_dict_aliases_remain_the_object_state(place):
    dec, method, owner = model()
    obj = {'metadata-leaf': dec.L.meta.params[0], 'metadata-root': dec.L.meta,
           'decompiler': dec, 'lifter': dec.L}[place]
    dec.saved_state = vars(obj)
    dec.saved_object = obj
    arena, _, _ = isolated_clone(dec, method, owner)
    assert arena.saved_state is vars(arena.saved_object)
    arena.saved_state['arena_only'] = [1]
    assert arena.saved_object.arena_only == [1]
    assert 'arena_only' not in vars(obj)


def test_shared_record_state_and_dict_self_cycle_remain_shared_and_disjoint():
    dec, method, owner = model()
    a, b = record(), record()
    b.__dict__ = a.__dict__
    a.state = vars(a)  # mutable state is deliberately NOT a scalar leaf
    dec.extra = [a, b, vars(a)]
    arena, _, _ = isolated_clone(dec, method, owner)
    x, y, state = arena.extra
    assert vars(x) is vars(y) is state is x.state is y.state
    state['name'] = 'isolated'
    assert x.name == y.name == 'isolated' and a.name == b.name == 'value'
    assert state is not vars(a)


@pytest.mark.parametrize('ty', RECORDS)
@pytest.mark.parametrize('value', [None, False, 7, -2.5, 3j, 'text', b'bytes', range(3)])
def test_exact_scalar_records_are_seeded_as_fresh_object_and_fresh_state(ty, value):
    obj = record(ty)
    obj.extra = value
    graph, memo, count = seed((obj, vars(obj)))
    clone, state = copy.deepcopy((obj, vars(obj)), memo)
    assert count == 1 and clone is not obj and state is not vars(obj)
    assert vars(clone) is state is memo[id(vars(obj))]
    assert vars(clone) == vars(obj) and clone.extra is value
    assert all(key in memo and memo[key] is not source for key, source in graph.items())
    clone.name = 'private'
    assert obj.name == 'value'


@pytest.mark.parametrize('ty', RECORDS)
def test_seed_preserves_repeated_records_and_external_shared_state(ty):
    a, b = record(ty), record(ty)
    b.__dict__ = a.__dict__
    graph, memo, count = seed((a, b, a, vars(a)))
    x, y, again, state = copy.deepcopy((a, b, a, vars(a)), memo)
    assert count == 2 and x is again and x is not y
    assert vars(x) is vars(y) is state and state is not vars(a)
    assert all(key in memo and memo[key] is not source for key, source in graph.items())


@pytest.mark.parametrize('ty', RECORDS)
@pytest.mark.parametrize('payload', [[], {}, set(), ([],), frozenset({1})])
def test_nonscalar_attributes_fall_back_to_full_graph_copy(ty, payload):
    obj = record(ty)
    obj.payload = payload
    graph, memo, count = seed((obj,))
    clone = copy.deepcopy(obj, memo)
    assert count == 0 and clone is not obj
    assert all(key in memo and memo[key] is not source for key, source in graph.items())


@pytest.mark.parametrize('payload', [lambda: None, {'callback': lambda: None}, [lambda: None]])
def test_leaf_optimization_does_not_hide_callbacks(payload):
    dec, method, owner = model()
    dec.L.meta.params[0].payload = payload
    with pytest.raises(ArenaDeclined):
        isolated_clone(dec, method, owner)


def test_record_subclasses_are_not_seeded_and_their_slots_are_traversed(monkeypatch):
    ty = type('ArenaTestParam', (ParamDef,),
              {'__module__': metadata.__name__, '__slots__': ('payload',)})
    monkeypatch.setattr(metadata, ty.__name__, ty, raising=False)
    obj = ty('subtype', 0, 0)
    obj.payload = []
    graph, memo, count = seed((obj,))
    clone = copy.deepcopy(obj, memo)
    assert count == 0 and clone.payload is not obj.payload
    assert all(key in memo and memo[key] is not source for key, source in graph.items())
    obj.payload = lambda: None
    with pytest.raises(ArenaDeclined):
        _mutable_graph((obj,))


def test_nonstr_state_keys_do_not_take_scalar_record_shortcut():
    obj = record()
    vars(obj)[17] = 'not-an-attribute'
    _, _, count = seed((obj,))
    assert count == 0


def test_new_copy_hooks_do_not_take_scalar_record_shortcut(monkeypatch):
    obj = record()
    monkeypatch.setattr(ParamDef, '__deepcopy__', lambda self, memo: self, raising=False)
    _, memo, count = seed((obj,))
    assert count == 0 and id(obj) not in memo
    dec, method, owner = model()
    with pytest.raises(ArenaDeclined):
        isolated_clone(dec, method, owner)


def test_fast_admission_has_the_exact_same_mutable_nodes_as_full_admission(monkeypatch):
    dec, method, owner = model()
    a, b = record(), record()
    b.__dict__ = a.__dict__
    dec.extra = [a, b, vars(a), record(FieldDef), record(ImageDef)]
    fast = _mutable_graph((dec, method, owner))
    monkeypatch.setattr(arena_module, '_metadata_leaf_types', lambda: frozenset())
    standard = _mutable_graph((dec, method, owner))
    assert fast.keys() == standard.keys()
    assert all(fast[key] is standard[key] for key in fast)


def test_malformed_custom_copy_state_declines_instead_of_repairing_it(monkeypatch):
    dec, method, owner = model()
    original = copy.deepcopy
    def bad_copy(roots, memo):
        result = original(roots, memo)
        result[0]._sw_depth = 99
        return result
    monkeypatch.setattr(arena_module.copy, 'deepcopy', bad_copy)
    with pytest.raises(ArenaDeclined):
        isolated_clone(dec, method, owner)
