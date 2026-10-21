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
    """typedefs: list of (name, [method_names]); type_methods returns the
    global indices of that typedef's methods."""
    methods = []
    idx_by_td = []
    for _name, mnames in typedefs:
        idxs = []
        for mn in mnames:
            idxs.append(len(methods))
            methods.append(SimpleNamespace(name=mn))
        idx_by_td.append(idxs)
    td_objs = []
    for (name, _m), idxs in zip(typedefs, idx_by_td):
        td_objs.append(SimpleNamespace(name=name, _mi=idxs))
    em = Emitter.__new__(Emitter)
    em.meta = SimpleNamespace(
        typedefs=td_objs,
        methods=methods,
        type_methods=lambda td: td._mi,
    )
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


def test_note_does_not_claim_async_or_iterator():
    """We cannot decode AsyncStateMachineAttribute cheaply, so the note
    must not assert the kind -- only that it is a MoveNext state machine."""
    em, tds = _em([('<Bar>d__9', ['MoveNext'])])
    note = em._state_machine_note(tds[0])
    assert note is not None
    assert 'async' not in note.lower()
    assert 'iterator' not in note.lower()
