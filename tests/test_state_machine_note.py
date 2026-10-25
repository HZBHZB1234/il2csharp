"""URE async/iterator state-machine identification (Stage 1).

A compiler-generated `<Method>d__N` type that owns a MoveNext is the state
machine for `Method`.  The emitter strips `<>`, so the class prints as
`_Method_d__N` with no hint of its origin; this note restores it.  The
test pins the two gates: name pattern AND a MoveNext method on the same
typedef.
"""
from types import SimpleNamespace

from il2cpp import Emitter


def _em(typedefs):
    """typedefs: list of (name, [method_names]) or (name, [method_names],
    [interface_names]); type_methods returns the global indices of that
    typedef's methods, and the interface list rides td.interfaces_start/
    interfaces_count over em.meta.interfaces -> em.il.types."""
    methods = []
    idx_by_td = []
    for t in typedefs:
        _name, mnames = t[0], t[1]
        idxs = []
        for mn in mnames:
            idxs.append(len(methods))
            methods.append(SimpleNamespace(name=mn))
        idx_by_td.append(idxs)
    ifaces = []
    for t in typedefs:
        ifaces.extend(t[2] if len(t) > 2 else [])
    td_objs = []
    base = 0
    for t, idxs in zip(typedefs, idx_by_td):
        inames = t[2] if len(t) > 2 else []
        td_objs.append(SimpleNamespace(
            name=t[0], _mi=idxs,
            interfaces_start=base, interfaces_count=len(inames)))
        base += len(inames)
    em = Emitter.__new__(Emitter)
    em.meta = SimpleNamespace(
        typedefs=td_objs,
        methods=methods,
        type_methods=lambda td: td._mi,
        interfaces=list(range(len(ifaces))),
    )
    em.il = SimpleNamespace(types=list(ifaces), type_name=lambda t: t)
    return em, td_objs


def test_state_machine_note_names_the_source_method():
    em, tds = _em([('<LoadSprite>d__1', ['MoveNext', '.ctor'])])
    note = em._state_machine_note(tds[0])
    assert note is not None
    assert 'state machine for LoadSprite' in note


def test_no_movenext_is_not_a_state_machine():
    em, tds = _em([('<Foo>d__2', ['Bar', '.ctor'])])
    assert em._state_machine_note(tds[0]) is None


def test_non_matching_name_is_none():
    em, tds = _em([('PlainClass', ['MoveNext'])])
    assert em._state_machine_note(tds[0]) is None


def test_note_neutral_when_no_kind_is_provable():
    """A machine proving neither kind keeps the neutral note."""
    em, tds = _em([('<Bar>d__9', ['MoveNext'])])
    note = em._state_machine_note(tds[0])
    assert note is not None
    assert 'async' not in note.lower()
    assert 'iterator' not in note.lower()


IASM = 'System.Runtime.CompilerServices.IAsyncStateMachine'


def test_note_claims_async_from_the_interface_list():
    em, tds = _em([('<Bar>d__9', ['MoveNext'], [IASM])])
    note = em._state_machine_note(tds[0])
    assert note is not None
    assert 'async state machine for Bar' in note


def test_note_claims_iterator_from_the_interface_list():
    em, tds = _em([('<Baz>d__3', ['MoveNext'],
                    ['System.Collections.Generic.IEnumerator_1<object>',
                     'System.Collections.IEnumerator'])])
    note = em._state_machine_note(tds[0])
    assert note is not None
    assert 'iterator state machine for Baz' in note


def test_async_wins_when_both_kinds_are_in_the_bases():
    em, tds = _em([('<Qux>d__1', ['MoveNext'],
                    ['System.Collections.IEnumerator', IASM])])
    note = em._state_machine_note(tds[0])
    assert note is not None
    assert 'async state machine for Qux' in note
