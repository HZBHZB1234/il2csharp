"""fix 197: `x - N == Enum.Member` folds to the member whose value is V + N.

MSVC lowers a switch into a dispatch that shifts the index before comparing, and
the lifter prints the shift inside the comparison. `enum - int` is not legal C#
(CS0019) and the shape also hides the flat `==` chain from `_switch_synth`, so
892 sites in one fixture read `expr - 1 == ComparisonType.LessThan`.
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from il2cpp.dec.highlevel import _HighLevelMixin  # noqa: E402


class _Il:
    def __init__(self, enums):
        # enums: {short name: {value: member}}
        self._enums = enums
        self.meta = type('M', (), {'typedefs': []})()

    def enum_members(self, idx):
        return self._enums.get(idx)


def _dec(enums, typedef_names=()):
    """A stand-in whose enum table is `{short name: {value: member}}`."""
    il = _Il({i: v for i, (n, v) in enumerate(enums.items())})
    il.meta.typedefs = [type('T', (), {'index': i, 'name': n,
                                       'is_valuetype': True})()
                        for i, n in enumerate(enums)]
    class D(_HighLevelMixin):
        pass
    d = D()
    d.il = il
    return d


ENUMS = {'ComparisonType': {0: 'LessThan', 1: 'Equal', 2: 'GreaterThan'},
         'FpsCounterAnchorPositions': {0: 'TopLeft', 1: 'BottomLeft',
                                       2: 'TopRight', 3: 'BottomRight'}}


def test_shifted_enum_comparison_names_the_right_member():
    d = _dec(ENUMS)
    out = d._enum_shift_fold(['if (this.comparisonType - 1 == '
                              'ComparisonType.LessThan)'])
    assert out == ['if (this.comparisonType == ComparisonType.Equal)'], out


def test_a_shift_that_names_no_member_is_kept():
    d = _dec(ENUMS)
    line = 'if (this.comparisonType - 7 == ComparisonType.LessThan)'
    assert d._enum_shift_fold([line]) == [line]


def test_an_unknown_enum_is_kept():
    d = _dec(ENUMS)
    line = 'if (x - 1 == OtherEnum.Thing)'
    assert d._enum_shift_fold([line]) == [line]


def test_the_numeric_rhs_shifts_arithmetically():
    d = _dec(ENUMS)
    out = d._enum_shift_fold(['if (anchor - 2 == 1)'])
    assert out == ['if (anchor == 3)'], out


def test_a_line_without_a_shift_is_untouched():
    d = _dec(ENUMS)
    line = 'if (this.comparisonType == ComparisonType.Equal)'
    assert d._enum_shift_fold([line]) == [line]
