"""Shared-tail duplication must preserve facts, never invent aliases/types."""
from types import SimpleNamespace as NS

import pytest

from il2cpp import Decompiler

ARRAY = (0x1234, 0x1d << 16)
OTHER = (0x5678, 0x12 << 16)


def make():
    lift = NS(_var_types={}, _type_hints={}, _gp_blocked=set(), slot_types={},
              il=NS(type_name=lambda ty: 'Element[]' if ty == ARRAY else 'Other'))
    dec = Decompiler(lift)
    # Force the documented duplication fallback: moving the tail would leak
    # onto a nonparticipant path, but each goto's unwind is already proved.
    dec._funnel_ok = lambda *a: False
    return dec


def body(token='t1'):
    return ['if (flag1)', '{', 'L_a:', 'var %s = source;' % token,
            'Consume(%s);' % token, '}', 'else', '{', 'goto L_a;', '}']


def clone(dec, lines=None):
    result = dec._hoist_shared_tails(body() if lines is None else lines)
    copies = [line.split()[1] for line in result if line.startswith('var ')]
    assert len(copies) == 2 and copies[0] != copies[1]
    return copies[1], result


@pytest.mark.parametrize('owner', ['dec', 'lifter', 'hint'])
def test_exact_facts_survive_tail_clone(owner):
    dec = make()
    facts = {'dec': dec._var_types, 'lifter': dec.L._var_types,
             'hint': dec.L._type_hints}[owner]
    facts['t1'] = ARRAY
    fresh, _ = clone(dec)
    assert facts[fresh] == ARRAY
    assert dec._decl_type_of(fresh) == 'Element[]'
    assert facts['t1'] == ARRAY


def test_precedence_and_conflicts_are_copied_without_reinterpretation():
    dec = make()
    dec._var_types['t1'] = ARRAY
    dec.L._var_types['t1'] = OTHER
    dec.L._type_hints['t1'] = OTHER
    fresh, _ = clone(dec)
    assert dec._var_types[fresh] == ARRAY
    assert dec.L._var_types[fresh] == OTHER
    assert dec.L._type_hints[fresh] == OTHER
    assert dec._decl_type_of(fresh) == dec._decl_type_of('t1')


def test_unknown_does_not_gain_type_or_entry_alias_identity():
    dec = make()
    dec.L._entry_byrefs = {'t1': ARRAY}
    dec.L._gp_blocked.add('t1')
    fresh, _ = clone(dec)
    assert dec._decl_type_of(fresh) == 'object'
    assert fresh in dec.L._gp_blocked
    assert fresh not in dec.L._entry_byrefs
    assert not dec._var_types and not dec.L._var_types and not dec.L._type_hints


@pytest.mark.parametrize('owner', ['dec', 'lifter', 'hint', 'blocked', 'param'])
def test_fresh_token_cannot_capture_map_only_or_unused_parameter(owner):
    dec = make()
    dec.L._var_types['t1'] = ARRAY
    maps = {'dec': dec._var_types, 'lifter': dec.L._var_types,
            'hint': dec.L._type_hints}
    if owner == 'blocked':
        dec.L._gp_blocked.add('t2')
    elif owner == 'param':
        dec.L._current_method = NS()
        dec.L.meta = NS(method_params=lambda m: [NS(name='t2')])
    else:
        maps[owner]['t2'] = OTHER
    fresh, result = clone(dec)
    assert fresh != 't2'
    assert dec._decl_type_of(fresh) == 'Element[]'
    if owner in maps:
        assert maps[owner]['t2'] == OTHER


def test_shared_outer_token_stays_shared():
    dec = make()
    dec.L._var_types['t1'] = ARRAY
    lines = ['var t1 = source;'] + body('t2')
    lines[5] = 'Consume(t2, t1);'
    result = dec._hoist_shared_tails(lines)
    assert result.count('var t1 = source;') == 1
    assert sum('t1);' in line for line in result) == 2
    assert all(ty == ARRAY for ty in dec.L._var_types.values())


def test_repeated_clones_do_not_share_types_with_other_fresh_values():
    dec = make()
    dec.L._var_types['t1'] = ARRAY
    lines = body()[:8] + ['if (flag2)', '{', 'goto L_a;', '}',
                          'else', '{', 'goto L_a;', '}', '}']
    result = dec._hoist_shared_tails(lines)
    copies = [line.split()[1] for line in result if line.startswith('var ')]
    assert len(copies) == 3 and len(set(copies)) == 3
    assert all(dec._decl_type_of(t) == 'Element[]' for t in copies)
    assert sum('Consume(' in line for line in result) == 3
