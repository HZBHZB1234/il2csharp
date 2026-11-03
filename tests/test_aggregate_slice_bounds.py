"""A partial native copy cannot prove bytes from its enclosing struct."""
import pytest

from il2cpp import Expr
from test_recovery_followup import struct_lifter, V3, F32


def sliced(text='snapshot', start=0, size=8):
    value = Expr(text, V3, 'local')
    value._slice = (Expr('owner.position', V3, 'obj'), start, size)
    return value


@pytest.mark.parametrize('start,size,offset,width', [
    (0, 8, 8, 4), (0, 8, 0, 12), (4, 4, 4, 4),
    (0, 8, -1, 4), (0, 8, 0, 0), (0, 8, 0, -1),
    (0, 8, 5, 4), (4, 4, 1, 4), (0, 0, 0, 4),
])
def test_cannot_project_an_uncopied_byte(start, size, offset, width):
    lift = struct_lifter()
    value = sliced(start=start, size=size)
    assert lift._piece_value(value, offset, width, F32) is None
    assert lift._piece_value(value, offset, width, V3) is None


@pytest.mark.parametrize('offset,field', [(0, 'x'), (4, 'y')])
def test_in_bounds_zero_slice_keeps_the_captured_snapshot_name(offset, field):
    lift = struct_lifter()
    value = sliced()
    got = lift._piece_value(value, offset, 4, F32)
    assert got.text == 'snapshot.' + field
    assert got.ty == F32
    assert lift._piece_value(value, offset, 4, None).text == got.text


def test_nested_zero_slice_does_not_extend_the_original_copy():
    lift = struct_lifter()
    inner = sliced()
    outer = lift._fragment(inner, 0, 12)
    assert lift._piece_value(outer, 8, 4, F32) is None
    assert lift._piece_value(outer, 0, 4, F32).text == 'snapshot.x'


def test_nested_nonzero_slice_cannot_hide_a_narrow_inner_bound():
    lift = struct_lifter()
    inner = sliced(size=4)
    outer = Expr('nested', V3, 'local')
    outer._slice = (inner, 4, 8)
    assert lift._piece_value(outer, 0, 4, F32) is None
    assert lift._scalar_parts(outer, 0, 4) == []


def test_bounds_precede_phi_type_and_literal_byte_evidence():
    lift = struct_lifter()
    value = sliced()
    value._bytes = bytes(12)
    lift._aggregate_phi_sources = {value.text: [Expr('other', V3, 'local')]}
    lift._aggregate_phi_types = {}
    before = dict(lift._type_hints)
    assert lift._piece_value(value, 8, 4, F32) is None
    assert lift._aggregate_phi_types == {}
    assert lift._type_hints == before


@pytest.mark.parametrize('offset,width,expected', [
    (0, 12, [(0, 'owner.position.x', 4), (4, 'owner.position.y', 4)]),
    (4, 8, [(0, 'owner.position.y', 4)]),
    (8, 4, []), (-1, 4, []), (0, 0, []), (0, -1, []),
])
def test_scalar_parts_clip_to_the_native_copy(offset, width, expected):
    lift = struct_lifter()
    parts = lift._scalar_parts(sliced(), offset, width)
    assert [(lo, value.text, count) for lo, value, _, count in parts] == expected


def test_partial_scalar_type_does_not_override_byte_bounds():
    lift = struct_lifter()
    value = Expr('partial', F32, 'float')
    value._slice = (Expr('whole', F32, 'float'), 0, 2)
    assert lift._piece_value(value, 0, 4, F32) is None
    assert sum(count for _, _, _, count in lift._scalar_parts(value, 0, 4)) <= 2


def test_cycles_and_overdeep_nested_fragments_decline():
    lift = struct_lifter()
    value = sliced()
    value._slice = (value, 0, 8)
    assert lift._piece_value(value, 0, 4, F32) is None
    assert lift._scalar_parts(value, 0, 4) == []


def test_reconstructed_stack_does_not_fill_a_missing_third_component():
    lift = struct_lifter()
    value = sliced()
    lift._stack_store(0x20, 12, value)
    assert lift._stack_struct(0x20, V3) is None


def test_nested_bounds_match_an_independent_byte_coverage_model():
    import random
    rng = random.Random(0xB017D)
    lift = struct_lifter()
    for _ in range(1000):
        value = Expr('root', V3, 'local')
        # Only slice coverage is tested here, not a struct's actual size.
        coverage = [True] * 1024
        count = rng.randrange(11)
        for level in range(count):
            start, size = rng.randrange(-1, 9), rng.randrange(25)
            outer = Expr('part' + str(level), V3, 'local')
            outer._slice = (value, start, size)
            coverage = [start >= 0 and i < size and coverage[i + start]
                        for i in range(128)]
            value = outer
        for offset in range(-1, 18):
            for width in (0, 1, 4, 8, 12, 16):
                expected = 0
                if count <= 8 and offset >= 0:
                    for i in range(offset, offset + width):
                        if not coverage[i]:
                            break
                        expected += 1
                assert lift._slice_width(value, offset, width, 0) == expected
