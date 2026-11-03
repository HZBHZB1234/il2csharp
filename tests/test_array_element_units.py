"""Native array byte offsets must not become byte-scaled C# indices."""
from types import SimpleNamespace as NS

import pytest

from il2cpp import Expr
from il2cpp.lifter.arrayindex import array_index_units
from test_recovery_followup import lifter, execute, INT


@pytest.mark.parametrize('text,scale,stride,expected', [
    ('i * 376', 1, 376, 'i'), ('i * 3 << 5', 1, 96, 'i'),
    ('i * 3', 8, 24, 'i'), ('i * 5', 8, 40, 'i'),
    ('(i + j) * 376', 1, 376, 'i + j'), ('i', 8, 8, 'i'),
    ('i', 8, 4, 'i * 2'), ('i * 6', 8, 24, 'i * 2'),
    ('(i + j) * 6', 8, 24, '(i + j) * 2'),
    ('(index * 0x178)', 1, 376, 'index'),
])
def test_exact_outer_byte_factors(text, scale, stride, expected):
    assert array_index_units(text, scale, stride) == expected


@pytest.mark.parametrize('text,scale,stride', [
    ('i + j * 376', 1, 376), ('i * n', 1, 376), ('376 * i', 1, 376),
    ('i * -376', 1, 376), ('i * 0', 1, 376), ('i', 1, 376),
    ('(int)i * 376', 1, 376), ('i << 32', 1, 4), ('i << 64', 1, 4),
    ('i << -1', 1, 4), ('i * 2147483648', 1, 4), ('i * True', 1, 4),
    ('i', 3, 3), ('i', 1, None), ('i', 1, 0), ('i', 1, -1),
    ('i', 1, 0x100000), ('?', 8, 8), ('i' * 513, 8, 8),
])
def test_unproved_factorization_declines(text, scale, stride):
    assert array_index_units(text, scale, stride) is None


def setup():
    element = (0, 0x11 << 16); array = (0x1234, 0x1d << 16)
    enum = (1, 0x11 << 16); char = (0, 0x03 << 16); string = (0, 0x0e << 16)
    sizes = {element: 376, enum: 4, char: 2, string: 8}
    fields = {0x10: ('elementType', enum), 0x14: ('character', char),
              0x18: ('label', string), 0x40: ('vertexIndex', INT)}
    def path(ty, key, depth, seen):
        assert ty == element  # never walk the array typedef as a struct
        return fields.get(key)
    il = NS(types=[], _type_enum=lambda t: (t[1] >> 16) & 0xff if t else 0,
            type_from_ptr=lambda p: element if p == array[0] else None,
            _sf_field_size=lambda ty, _: sizes.get(ty, 4),
            _sf_field_path=path, instance_field_chain=lambda _: {})
    lift = lifter(il=il)
    lift.meta.typedefs = [NS(is_valuetype=True), NS(is_valuetype=True)]
    return lift, Expr('characters', array, 'arr'), enum, char


@pytest.mark.parametrize('disp,size,member', [(0x20, 4, 'elementType'),
    (0x24, 2, 'character'), (0x28, 8, 'label'), (0x50, 4, 'vertexIndex')])
def test_exact_member_type_and_element_units(disp, size, member):
    lift, arr, enum, char = setup()
    got = lift._arr_elem_expr(arr, Expr('i * 376', INT, 'int'), 1, disp, size)
    assert got.text == 'characters[i].' + member
    if member == 'elementType':
        assert got.ty == enum
    elif member == 'character':
        assert got.ty == char
        assert got.kind == 'int'


def test_native_load_and_store_use_the_same_char_location():
    lift, arr, _, char = setup()
    lift.regs.update(RCX=arr, RDX=Expr('i', INT, 'int'))
    # imul rdx,rdx,376; movzx eax,word ptr [rcx+rdx+0x24]
    execute(lift, '48 69 d2 78 01 00 00 0f b7 44 11 24')
    assert lift.regs['RAX'].text == 'characters[i].character'
    assert lift.regs['RAX'].ty == char
    lift.regs['RAX'] = Expr('replacement', char, 'int')
    execute(lift, '66 89 44 11 24')
    assert any('characters[i].character = replacement;' in line for _, line, _ in lift.out)


@pytest.mark.parametrize('size', [None, 376])
def test_whole_element_and_address_are_normalized(size):
    lift, arr, _, _ = setup()
    got = lift._arr_elem_expr(arr, Expr('i * 376', INT, 'int'), 1, 0x20, size)
    assert got.text == 'characters[i]'
    assert got.ty == lift._elem_type(arr.ty)


def test_constant_bias_is_divided_by_real_stride_not_hardware_scale():
    lift, arr, _, char = setup()
    got = lift._arr_elem_expr(arr, Expr('i * 376', INT, 'int'), 1, 0x24 + 376, 2)
    assert got.text == 'characters[(i + 1)].character'
    assert got.ty == char


@pytest.mark.parametrize('disp,size', [(0x24, 1), (0x24, 4), (0x25, 1),
    (0x2f, 2), (0x20, 16)])
def test_partial_padding_and_simd_slices_do_not_gain_a_scalar_field(disp, size):
    lift, arr, _, _ = setup()
    got = lift._arr_elem_expr(arr, Expr('i * 376', INT, 'int'), 1, disp, size)
    assert got is None or not any('.' + f in got.text for f in ('elementType', 'character', 'label'))


def test_normalization_preserves_native_addresses_for_valid_small_indices():
    for text, scale, stride in [('i * 376', 1, 376), ('i * 3 << 5', 1, 96),
                                ('i * 3', 8, 24), ('i', 8, 4)]:
        normalized = array_index_units(text, scale, stride)
        for i in range(128):
            assert eval(text, {}, {'i': i}) * scale == eval(normalized, {}, {'i': i}) * stride
