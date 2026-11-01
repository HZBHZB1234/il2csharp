"""fix 179: a bare `x = 0;` under a struct/class declaration is CS0029.

IL2CPP renders stack-slot zeroing as `= 0` under whatever type the slot
carries. The DECLARATION path already respells that to `default`
(`_bare_rhs_needs_default`, fix 97b), so `UniTask.Awaiter awaiter1 = 0;`
became `= default` -- but a plain re-assignment of an already-declared local
was left alone, and `awaiter1 = 0;` under a struct is the same CS0029. Same
value (`default` is the zero every one of those types starts with), so the
rewrite is value-preserving.

`object` boxes and numerics convert, so both keep their faithful `= 0`; enums
convert too; generics/arrays/nullables/pointers decline because the spelling
alone cannot prove the conversion is illegal.
"""
import os
import sys
from types import SimpleNamespace as NS

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from il2cpp.dec.flow import _FlowMixin  # noqa: E402


class _Meta:
    def __init__(self):
        self.typedefs = [
            NS(name='Awaiter', namespace='Cysharp.Threading.Tasks', flags=0,
               is_valuetype=True, is_enum=False),
            NS(name='Holder', namespace='NS', flags=0,
               is_valuetype=False, is_enum=False),
            NS(name='Mode', namespace='NS', flags=0,
               is_valuetype=True, is_enum=True),
            NS(name='Vector3', namespace='UnityEngine', flags=0,
               is_valuetype=True, is_enum=False),
            NS(name='Object', namespace='System', flags=0,
               is_valuetype=False, is_enum=False),
        ]


def _decompiler():
    dec = _FlowMixin.__new__(_FlowMixin)
    meta = _Meta()
    dec.L = NS(meta=meta, il=NS(meta=meta))
    dec._eq_typedef_map = lambda: {
        'Cysharp.Threading.Tasks.Awaiter': 0,
        'NS.Holder': 1,
        'NS.Mode': 2,
        'UnityEngine.Vector3': 3,
        'System.Object': 4,
    }
    return dec


def _run(lines):
    return _decompiler()._zero_assign_default(list(lines))


def test_a_struct_local_zero_assign_becomes_default():
    # the declaration carries the FULL spelling at this stage: the file
    # boundary shortens it later, after this pass has run
    assert _run(['        Cysharp.Threading.Tasks.Awaiter awaiter1 = awaiter;',
                 '        awaiter1 = 0;']) == [
        '        Cysharp.Threading.Tasks.Awaiter awaiter1 = awaiter;',
        '        awaiter1 = default;']


def test_a_shortened_spelling_declines():
    """`UniTask.Awaiter` is not in the typedef map, so the pass cannot prove
    anything about it and keeps the faithful (if uncompilable) `= 0`."""
    assert _run(['        UniTask.Awaiter awaiter1 = awaiter;',
                 '        awaiter1 = 0;'])[-1] == '        awaiter1 = 0;'


def test_a_reference_local_zero_assign_becomes_default():
    assert _run(['        NS.Holder holder1 = null;',
                 '        holder1 = 0;']) == [
        '        NS.Holder holder1 = null;',
        '        holder1 = default;']


def test_primitives_and_enums_keep_their_zero():
    for decl in ('int num1 = 0;', 'bool flag1 = false;', 'NS.Mode mode1 = 0;'):
        name = decl.split()[1]
        assert _run(['        ' + decl, '        %s = 0;' % name]) == [
            '        ' + decl, '        %s = 0;' % name]


def test_object_keeps_its_zero():
    assert _run(['        object obj1 = x;', '        obj1 = 0;']) == [
        '        object obj1 = x;', '        obj1 = 0;']


def test_an_unknown_or_generic_spelling_declines():
    for decl in ('List<int> list1 = null;', 'NS.Unknown thing1 = null;',
                 'byte* ptr1 = null;'):
        out = _run(['        ' + decl, '        %s = 0;' %
                    decl.split()[1]])
        assert out[-1] == '        %s = 0;' % decl.split()[1]


def test_an_ambiguous_declaration_declines():
    assert _run(['        int num1 = 0;',
                 '        NS.Holder num1 = null;',
                 '        num1 = 0;'])[-1] == '        num1 = 0;'


def test_fields_members_and_compound_stores_never_match():
    for line in ('        this.F = 0;', '        a[0] = 0;',
                 '        obj1.field = 0;', '        num1 += 0;',
                 '        num1 = 0f;'):
        assert _run([line]) == [line]


def test_a_declaration_typed_zero_assign_is_untouched():
    """The declaration path owns that shape; this pass must not double up."""
    line = '        UniTask.Awaiter awaiter1 = 0;'
    assert _run([line]) == [line]
