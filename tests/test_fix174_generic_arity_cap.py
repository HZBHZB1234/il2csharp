"""fix 174: a generic instantiation's argument list is not 8 long.

`_argv_names` rendered `min(argc, 8)` arguments. That cap is Win64 ABI
vocabulary (four integer + four float argument registers) applied to a
*metadata* list, and real arities exceed it: `CombineLatest`16` (15 sources
plus TResult), `WhenAllPromise`15`, the `CombineLatest` extension methods.

A truncated list is worse than a short one, because
`_distribute_nested_args` only distributes when a nested type's segment
arities sum EXACTLY to the argument count. With 8 of 12 arguments the proof
failed and the legacy single-list rendering took over, which attaches every
argument to the innermost segment: `UniTask.WhenAllPromise.<>c<T1..T8>`
(CS0308 -- the non-generic `WhenAllPromise` cannot take type arguments)
instead of `UniTask.WhenAllPromise<T1..T12>.__c`. The same shape produced
CS0305 `CombineLatest<T1,T2,TResult> requires 3 type arguments`.
"""
import struct
from types import SimpleNamespace as NS

from il2cpp.runtime.types import _TypesMixin

ARGV = 0x1000


def _il(nargs, argv=ARGV):
    buf = bytearray(nargs * 8)
    for k in range(nargs):
        struct.pack_into('<Q', buf, k * 8, 0x200 + k)
    il = _TypesMixin.__new__(_TypesMixin)
    il.bin = NS(qword=lambda va: struct.unpack_from('<Q', buf, va - ARGV)[0])
    il.type_from_ptr = lambda p: (p, (0x12 << 16))
    il.type_name = lambda t, depth=0: 'T%d' % (t[0] - 0x200)
    return il


def test_twelve_arguments_all_render():
    il = _il(12)
    assert il._argv_names(ARGV, 12, 0) == ['T%d' % k for k in range(12)]


def test_sixteen_arguments_all_render():
    """`CombineLatest`16` is the widest real closure in the fixtures."""
    il = _il(16)
    names = il._argv_names(ARGV, 16, 0)
    assert len(names) == 16
    assert names[-1] == 'T15'


def test_no_arguments_is_an_empty_list():
    il = _il(4)
    assert il._argv_names(ARGV, 0, 0) == []


def test_an_absurd_count_declines_instead_of_reading_garbage():
    il = _il(4)
    assert il._argv_names(ARGV, 65, 0) is None
    assert il._argv_names(ARGV, -1, 0) is None


def test_a_missing_argument_array_declines():
    il = _il(4)
    assert il._argv_names(0, 4, 0) is None


def _nested_fixture(outer_arity):
    """`NS.UniTask.WhenAllPromise`9.<>c` as three typedef rows.

    `UniTask` and `<>c` declare no parameters of their own; the arguments
    all belong to `WhenAllPromise`9` (the second segment), which is exactly
    the shape that used to mis-render.
    """
    il = _il(0)
    il.meta = NS(typedefs=[NS(index=0, name='<>c'),
                           NS(index=1, name='WhenAllPromise`%d' % outer_arity),
                           NS(index=2, name='UniTask')])
    il._nested_owner = lambda ti: {0: 1, 1: 2}.get(ti)
    il._typedef_arity = lambda td: {0: 0, 1: outer_arity, 2: 0}[td.index]
    return il


def test_a_nine_arity_nested_type_distributes_over_the_outer():
    """The end shape: arguments belong to the OUTER segment."""
    il = _nested_fixture(9)
    got = il._distribute_nested_args(
        0, 'NS.UniTask.WhenAllPromise.<>c', ['T%d' % k for k in range(9)])
    assert got == 'NS.UniTask.WhenAllPromise<T0, T1, T2, T3, T4, T5, T6, T7, T8>.<>c'


def test_a_mismatched_count_still_declines():
    """The distribution proof stays exact: 8 arguments, 9 parameters."""
    il = _nested_fixture(9)
    assert il._distribute_nested_args(
        0, 'NS.UniTask.WhenAllPromise.<>c', ['T%d' % k for k in range(8)]) is None
