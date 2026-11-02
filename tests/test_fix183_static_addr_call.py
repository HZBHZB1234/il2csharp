"""fix 183: a generic callee's call parens survive the static-address fold.

`_fold_static_addrs` turns `typeof(T).__static_fields[+ N]` into
`typeof(T).field`. When the blob is a call's SOLE argument the fold must keep
the call's parentheses; it only drops a *grouping* pair. The distinguishing
test looked two characters back for an identifier character, so a GENERIC
callee (`EnsureInitializedCore<T>(blob)`) left `>` there and the fold glued
the callee to its argument:

    EnsureInitializedCore<object>typeof(Hashtable).s_serializationInfoTable

-- the one unparseable line in the game's mscorlib
(`Hashtable.get_SerializationInfoTable`). A rendered binary `>` is always
space-separated, so an identifier character just before the `>` proves a
generic callee; a call can also follow `]` or `)`.
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from il2cpp.dec.sugar import _SugarMixin  # noqa: E402


class _D(_SugarMixin):
    def _static_field_name(self, type_name, offset):
        if offset in (None, 0):
            return 's_field'
        return None


def _fold(text):
    return _D()._fold_static_addrs(text)


BLOB = 'typeof(System.Collections.Hashtable).__static_fields'


def test_a_generic_callee_keeps_its_call_parens():
    src = 'LazyInitializer.EnsureInitializedCore<object>(%s)' % BLOB
    assert _fold(src) == \
        'LazyInitializer.EnsureInitializedCore<object>(typeof(System.Collections.Hashtable).s_field)'


def test_an_identifier_callee_keeps_its_call_parens():
    assert _fold('Notify(%s)' % BLOB) == \
        'Notify(typeof(System.Collections.Hashtable).s_field)'


def test_a_grouping_pair_is_still_dropped():
    assert _fold('if ((%s) == 0)' % BLOB) == \
        'if (typeof(System.Collections.Hashtable).s_field == 0)'


def test_a_comparison_before_a_grouping_pair_is_not_a_callee():
    # `a > (blob)` -- the `>` is a space-separated binary operator
    assert _fold('bool b = num1 > (%s);' % BLOB) == \
        'bool b = num1 > typeof(System.Collections.Hashtable).s_field;'


def test_a_call_after_an_indexer_keeps_its_parens():
    assert _fold('arr[0](%s)' % BLOB) == \
        'arr[0](typeof(System.Collections.Hashtable).s_field)'


def test_an_offset_blob_still_names_its_field():
    assert _fold('f<T>(typeof(X).__static_fields + 0x10)') == \
        'f<T>(typeof(X).__static_fields + 0x10)'
