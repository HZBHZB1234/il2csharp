"""Only exact pointer-wide reference loads may use array-typed SSA values."""
from types import SimpleNamespace as NS

import pytest
from iced_x86 import Decoder, MemorySizeExt

from il2cpp import Expr
from test_recovery_followup import lifter, INT

ARRAY = (0x1234, 0x1d << 16)
CLASS = (0, 0x12 << 16)


def setup(element=CLASS, raw='4a8b44c120'):
    il = NS(types=[], _type_enum=lambda t: (t[1] >> 16) & 0xff if t else 0,
            type_from_ptr=lambda p: element if p == ARRAY[0] else None,
            instance_field_chain=lambda td: {})
    lift = lifter(il=il)
    base = Expr('v377', ARRAY, 'obj')
    index = Expr('v378', INT, '?')
    ins = Decoder(64, bytes.fromhex(raw), ip=0x1000).decode()
    lift.regs.update(RCX=base, R8=index)
    return lift, base, index, ins


def load(lift, base, index, ins):
    return lift._typed_phi_reference_array_load(ins, base, index, MemorySizeExt.size(ins.memory_size))


@pytest.mark.parametrize('te,kind', [(0x0e, 'str'), (0x12, 'obj'), (0x1c, 'obj'),
                                     (0x1d, 'arr'), (0x14, 'arr')])
@pytest.mark.parametrize('token', ['v377', 't42'])
def test_exact_reference_element_type_is_preserved(te, kind, token):
    element = (0, te << 16)
    lift, base, index, ins = setup(element)
    base.text = token
    out = load(lift, base, index, ins)
    assert (out.text, out.ty, out.kind) == (token + '[v378]', element, kind)
    assert base.kind == 'obj' and base.text == token and base.ty == ARRAY
    assert not getattr(base, '_newarr', False)
    assert lift._read_mem_raw(ins, None).text == token + '[v378]'


@pytest.mark.parametrize('te', [0x08, 0x09, 0x0a, 0x0b, 0x18, 0x19])
@pytest.mark.parametrize('kind', ['int', '?'])
def test_typed_integer_index_survives_phi_kind_loss(te, kind):
    lift, base, index, ins = setup()
    index.ty, index.kind = (0, te << 16), kind
    assert load(lift, base, index, ins).text == 'v377[v378]'


@pytest.mark.parametrize('raw', ['428a44c120', '428b44c120', '66428b44c120',
    'f24a0f1044c120', 'f34a0f7e44c120', '4a8d44c120', '4a3b44c120',
    '498b440820', '4a8b44c118', '4a8b44c128', '4a8b44c121',
    '674a8b44c120', '644a8b44c120', '654a8b44c120', '4a8944c120'])
def test_partial_simd_address_stride_or_displacement_is_not_a_reference_load(raw):
    lift, base, index, ins = setup(raw=raw)
    assert load(lift, base, index, ins) is None


@pytest.mark.parametrize('ty', [None, (0, 0x12 << 16), (0x1234, 0x14 << 16),
                                (0x1234, (0x1d << 16) | (1 << 29))])
def test_base_type_must_prove_a_non_byref_vector(ty):
    lift, base, index, ins = setup()
    base.ty = ty
    assert load(lift, base, index, ins) is None


@pytest.mark.parametrize('kind', ['?', 'klass', 'ptr', 'arr', 'int'])
def test_other_base_kinds_keep_the_existing_path(kind):
    lift, base, index, ins = setup()
    base.kind = kind
    assert load(lift, base, index, ins) is None


@pytest.mark.parametrize('text', ['items', 'unknown', 'null', '0', 'GetItems()',
                                'this.items', '(v377)', 'v377 + 1'])
def test_no_new_lifetime_or_expression_proof_is_invented(text):
    lift, base, index, ins = setup()
    base.text = text
    assert load(lift, base, index, ins) is None


@pytest.mark.parametrize('element', [None, INT, (0, 0x0c << 16), (0, 0x11 << 16),
    (0, 0x13 << 16), (0, 0x15 << 16), (0, 0x1e << 16),
    (0, (0x12 << 16) | (1 << 29))])
def test_scalar_generic_struct_and_byref_elements_decline(element):
    lift, base, index, ins = setup(element)
    assert load(lift, base, index, ins) is None


@pytest.mark.parametrize('ty', [None, (0, 0x0c << 16), CLASS,
                               (0, (0x08 << 16) | (1 << 29))])
def test_unproved_index_types_decline(ty):
    lift, base, index, ins = setup()
    index.ty = ty
    assert load(lift, base, index, ins) is None


@pytest.mark.parametrize('what', ['base', 'index', 'pointer-index', 'missing-index'])
def test_unknown_or_conflicting_index_evidence_declines(what):
    lift, base, index, ins = setup()
    if what == 'base':base._unk = True
    elif what == 'index':index._unk = True
    elif what == 'pointer-index':index.kind = 'ptr'
    else:index = None
    assert load(lift, base, index, ins) is None


@pytest.mark.parametrize('raw', ['428a44c120', '428b44c120', '66428b44c120',
                                 'f24a0f1044c120', '4a8d44c120', '4a3b44c120'])
def test_rejected_width_or_opcode_keeps_raw_consumer_spelling(raw):
    lift, base, index, ins = setup(raw=raw)
    out = lift._read_mem_raw(ins, None)
    assert out.text != 'v377[v378]'
    assert base.kind == 'obj' and base.ty == ARRAY


@pytest.mark.parametrize('size', [None, 0, 1, 2, 4, 16])
def test_caller_width_cannot_expand_a_copy(size):
    lift, base, index, ins = setup()
    assert lift._typed_phi_reference_array_load(ins, base, index, size) is None
