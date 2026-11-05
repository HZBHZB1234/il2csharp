"""Exact immutable tuple memoization must preserve admission and graph aliases."""
import bisect
import copy

import pytest

from il2cpp import metadata
from il2cpp.dec import entrycapture as arena_module
from il2cpp.dec.entrycapture import ArenaDeclined, _mutable_graph, isolated_clone
from test_entry_int32_capture import model

ATOMS = (None, False, True, 0, 19, -27, 1.5, float('nan'), float('inf'),
         -0.0, 3j, 'name', b'bytes', range(5))


def admitted(roots):
    memo = {id(bisect): bisect}
    graph = _mutable_graph(roots, immutable_memo=memo)
    return graph, memo


@pytest.mark.parametrize('atom', ATOMS)
@pytest.mark.parametrize('repeat', [1, 3, 17])
def test_exact_scalar_tuple_sharing_is_already_the_deepcopy_result(atom, repeat):
    value = tuple([atom] * repeat)
    assert copy.deepcopy(value) is value
    graph, memo = admitted((value,))
    assert graph == {} and memo[id(value)] is value
    assert copy.deepcopy(value, memo) is value


def test_empty_tuple_is_admitted_and_memoized():
    graph, memo = admitted(((),))
    assert graph == {} and memo[id(())] is ()


def test_no_memo_preserves_the_admission_api_and_mutable_node_set():
    leaf = tuple(ATOMS)
    container = {'values': [leaf, leaf, (leaf,)]}
    plain = _mutable_graph((container,))
    seeded, memo = admitted((container,))
    assert plain.keys() == seeded.keys()
    assert all(plain[key] is seeded[key] for key in plain)
    assert memo[id(leaf)] is leaf
    assert all(key not in memo for key in plain)


@pytest.mark.parametrize('place', ['list', 'dict-key', 'dict-value', 'set', 'frozenset'])
def test_tuple_key_value_and_repeated_reference_keep_identity(place):
    dec, method, owner = model()
    value = tuple(['unique-name', 23, range(4)])
    choices = {'list': [value, value], 'dict-key': {value: value},
               'dict-value': {'tuple': value}, 'set': {value},
               'frozenset': frozenset({value})}
    dec.extra = choices[place]
    dec.saved_tuple = value
    arena, _, _ = isolated_clone(dec, method, owner)
    assert arena.saved_tuple is value
    assert arena.extra is not dec.extra or place == 'frozenset'
    if place == 'list':
        assert arena.extra[0] is arena.extra[1] is value
    elif place == 'dict-key':
        assert next(iter(arena.extra)) is arena.extra[value] is value
    elif place == 'dict-value':
        assert arena.extra['tuple'] is value
    else:
        assert next(iter(arena.extra)) is value


@pytest.mark.parametrize('payload', [[], {}, set(), ([],)])
def test_mutable_tuple_contents_are_not_seeded_and_remain_private(payload):
    dec, method, owner = model()
    value = (payload,)
    dec.extra = [value, value, payload]
    graph, memo = admitted((dec, method, owner))
    assert id(value) not in memo and all(key not in memo for key in graph)
    arena, _, _ = isolated_clone(dec, method, owner)
    assert arena.extra[0] is arena.extra[1]
    assert arena.extra[0] is not value
    assert arena.extra[0][0] is arena.extra[2] is not payload
    assert _mutable_graph((arena,)).keys().isdisjoint(graph)


def test_tuple_list_cycle_preserves_all_edges_without_sharing_mutable_nodes():
    dec, method, owner = model()
    chain = []
    value = (chain,)
    chain.extend([value, chain])
    dec.extra = [value, chain]
    graph, memo = admitted((dec, method, owner))
    assert id(value) not in memo
    arena, _, _ = isolated_clone(dec, method, owner)
    other, copied_chain = arena.extra
    assert other is not value and copied_chain is not chain
    assert other[0] is copied_chain
    assert copied_chain[0] is other and copied_chain[1] is copied_chain
    assert _mutable_graph((arena,)).keys().isdisjoint(graph)


@pytest.mark.parametrize('ty', [int, float, complex, str, bytes, tuple])
def test_atom_and_tuple_subclasses_with_state_are_never_shared(ty, monkeypatch):
    name = 'ArenaTupleMemo' + ty.__name__
    derived = type(name, (ty,), {'__module__': metadata.__name__})
    monkeypatch.setattr(metadata, name, derived, raising=False)
    value = derived()  # subclasses can have mutable state despite immutable payloads
    value.payload = []
    dec, method, owner = model()
    dec.extra = (value,)
    graph, memo = admitted((dec, method, owner))
    assert id(dec.extra) not in memo and id(value) in graph and id(value) not in memo
    arena, _, _ = isolated_clone(dec, method, owner)
    assert arena.extra[0] is not value and arena.extra[0].payload is not value.payload
    assert _mutable_graph((arena,)).keys().isdisjoint(graph)
    value.payload.append(lambda: None)
    with pytest.raises(ArenaDeclined):
        isolated_clone(dec, method, owner)


@pytest.mark.parametrize('wrap', [lambda x: (x,), lambda x: ((x,),),
                                lambda x: ([x],), lambda x: ({'x': x},),
                                lambda x: frozenset({(x,)})])
def test_callback_in_or_beyond_a_tuple_still_declines(wrap):
    dec, method, owner = model()
    dec.extra = wrap(lambda: dec)
    with pytest.raises(ArenaDeclined):
        isolated_clone(dec, method, owner)


def test_metadata_tuple_attribute_uses_full_copy_and_keeps_external_state_alias():
    dec, method, owner = model()
    obj = dec.L.meta.params[0]
    obj.extra = tuple(ATOMS)
    dec.saved_state = vars(obj)
    arena, _, _ = isolated_clone(dec, method, owner)
    clone = arena.L.meta.params[0]
    assert clone is not obj and arena.saved_state is vars(clone) is not vars(obj)
    assert clone.extra is obj.extra
    clone.name = 'private'
    assert obj.name != clone.name


def test_isolated_clone_passes_admitted_tuple_memo_to_deepcopy(monkeypatch):
    dec, method, owner = model()
    scalar = tuple(ATOMS)
    nested = (scalar,)
    dec.extra = [scalar, nested]
    original = copy.deepcopy
    calls = []

    def observed(roots, memo):
        assert memo[id(scalar)] is scalar
        assert id(nested) not in memo
        assert id(dec.extra) not in memo
        calls.append(True)
        return original(roots, memo)

    monkeypatch.setattr(arena_module.copy, 'deepcopy', observed)
    arena, _, _ = isolated_clone(dec, method, owner)
    assert calls == [True] and arena.extra[0] is scalar
    assert arena.extra[1][0] is scalar
