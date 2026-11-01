"""Generic method table alignment.

`Il2CppGenericMethodFunctionsDefinitions` is NOT parallel to
`Il2CppCodeRegistration.genericMethodPointers`: the row carries its own
`methodPointerIndex` (the second int), and the two counts differ (the
pointer array omits null slots).  Pairing by table row index shifted every
generic target after the first gap -- the survivors tree rendered
`WrapperT<bool>.set_Value` as `WhereSelectEnumerableIterator.ctor` and
`Component.GetComponent<object>` as `Memmove<...>`.
"""
from il2cpp.runtime.core import Il2Cpp


def _addr(rows, ptrs):
    return list(Il2Cpp._generic_method_addresses(
        rows, ptrs, lambda p: p != 0))


def test_rows_index_the_pointer_array_by_their_own_method_index():
    ptrs = [0, 0xAAA, 0xBBB, 0xCCC]
    rows = [(100, 2, 0, 0), (101, 3, 0, 0), (102, 1, 0, 0)]
    assert _addr(rows, ptrs) == [(0xBBB, 100), (0xCCC, 101), (0xAAA, 102)]


def test_null_and_out_of_range_pointer_slots_decline():
    ptrs = [0, 0xAAA, 0xBBB]
    rows = [(1, 0, 0, 0),       # null executable slot
            (2, 1, 0, 0),       # valid
            (3, 9, 0, 0),       # out of range
            (4,),               # malformed row
            (5, 2, 0, 0)]
    assert _addr(rows, ptrs) == [(0xAAA, 2), (0xBBB, 5)]
