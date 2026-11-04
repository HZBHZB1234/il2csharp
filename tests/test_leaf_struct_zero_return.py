"""Authored exact native zero leaves; literals alone never prove a struct."""
import struct
from types import SimpleNamespace as NS

import pytest
from iced_x86 import Decoder

from il2cpp import Lifter, Decompiler
from il2cpp.binary import PE
from il2cpp.expr import Expr
from il2cpp.lifter import leafreturns
from il2cpp.lifter.leafreturns import recover_leaf_struct_zero_return as recover

START = 0x180001000
CTOR = START + 0x80
VOID = (0, 1 << 16)


def setup(width=8, source=None, ctor=None):
    scalar = (0, {1: 5, 2: 6, 4: 8, 8: 0x0a}[width] << 16 | 1)
    owner_ty, target_ty = (0, 0x11 << 16), (1, 0x11 << 16)
    types = [VOID, scalar, owner_ty, target_ty]
    method = NS(index=0, name='Copy', addr=START, generic_container=-1,
                declaring=0, return_type=3, is_static=False, param_count=0, image=0, flags=6, iflags=0)
    constructor = NS(index=1, name='.ctor', addr=CTOR, generic_container=-1,
                     declaring=1, return_type=0, is_static=False, param_count=1,
                     parameter_start=0, flags=0x1886, iflags=0, image=0)
    owner = NS(index=0, byval=2, generic_container=-1, declaring=-1,
               is_valuetype=True, is_enum=False, has_cctor=False, flags=8,
               bitfield=0xc01, field_start=0, field_count=1,
               method_start=0, method_count=1)
    target = NS(**vars(owner)); target.index=1; target.byval=3
    target.field_start=1; target.method_start=1
    fields = [NS(name='input', type=1), NS(name='payload', type=1)]
    meta = NS(typedefs=[owner, target], methods=[method, constructor],
              fields=fields, params=[NS(type=1)])
    source = source if source is not None else b'\x33\xc0\xc3'
    ctor = ctor if ctor is not None else (b'\x48' if width == 8 else b'') + b'\x89\x11\xc3'
    data = bytearray(0x200); struct.pack_into('<I', data, 0x3c, 0x40)
    data[0x40:0x46] = b'PE\x00\x00\x64\x86'
    data[0x100:0x100+len(source)] = source
    data[0x180:0x180+len(ctor)] = ctor
    binary = PE.__new__(PE); binary.is64=True; binary.d=bytes(data)
    binary.va2off=lambda va:va-START+0x100 if START<=va<START+0x100 else None
    chains={0:{0x10:('input',1)},1:{0x10:('payload',1)}}
    il=NS(bin=binary,meta=meta,types=types,chains=chains,
          addr_candidates={START:[('method',0)],CTOR:[('method',1)]},
          _type_enum=lambda ty:(ty[1]>>16)&255,
          _closed_type_key=lambda ty:(ty[0],(ty[1]>>16)&255,(ty[1]>>29)&1),
          _sf_field_size=lambda ty,depth:width,
          _sf_subst=lambda ty,args:ty,
          instance_field_chain=lambda index:chains.get(index),
          type_name=lambda ty:'Example.Wrapper', returns_sret=lambda ty:False,
          enum_members=lambda td:None)
    insns=list(Decoder(64,source,ip=START))
    lift=NS(il=il,meta=meta,_current_method=method,_cur_ip=insns[-1].ip,
            out=NS(block=NS(bid=0,preds=[],insns=insns)),
            regs={'RAX':Expr('0',None,'int')})
    lift._td_of=lambda ty:ty[0] if il._type_enum(ty)==0x11 else None
    lift._piece_layout_proven=lambda ty,seen=frozenset():Lifter._piece_layout_proven(lift,ty,seen)
    return lift,'0',target_ty


@pytest.mark.parametrize('width', [1, 2, 4, 8])
@pytest.mark.parametrize('source', [bytes.fromhex('33c0c3'), bytes.fromhex('4833c0c3'),
                                    bytes.fromhex('31c0c3'), bytes.fromhex('4831c0c3')])
@pytest.mark.parametrize('static', [False, True])
def test_exact_zero_leaf_returns_default_without_constructor(width, source, static):
    lift, text, ty = setup(width, source=source, ctor=b'\xcc')
    lift._current_method.is_static = static
    assert recover(lift, text, ty) == 'default(Example.Wrapper)'
    assert Decompiler._return_literal_text(None, lift, text, ty) == 'default(Example.Wrapper)'


@pytest.mark.parametrize('width', [1, 2, 4, 8])
@pytest.mark.parametrize('shape', [
    'parameter', 'generic', 'no-address', 'method-index', 'method-row',
    'return-index', 'return-mismatch', 'no-candidate', 'generic-candidate',
    'owner-generic', 'owner-open-outer', 'owner-cycle', 'owner-out-of-range',
    'target-generic', 'target-open-outer', 'target-cycle', 'target-class',
    'target-enum', 'target-cctor', 'target-cctor-row', 'target-method-start',
    'target-method-count', 'target-explicit', 'target-packed', 'target-field-start',
    'target-field-count', 'target-field-type', 'field-byref', 'field-explicit',
    'field-generic', 'size-unknown', 'size-three', 'size-large', 'sret',
    'type-key', 'byref', 'generic-return', 'class-return', 'bad-typedef',
    'entry', 'pred', 'ip', 'no-value', 'unknown-value', 'value-text', 'text',
    'native-different', 'native-truncated', 'offset-none', 'offset-negative',
    'offset-outside', 'abstract', 'pinvoke', 'runtime', 'synchronized',
    'unmanaged', 'native-iflag', 'abi-elf', 'abi-pe32', 'abi-arm64', 'abi-bad-header',
    'no-disassembler', 'no-context', 'chain-offset', 'chain-extra',
    'chain-type', 'field-width', 'field-enum', 'class-value-confusion',
])
def test_every_unproved_context_declines_without_inventing_default(width, shape, monkeypatch):
    lift, text, ty = setup(width)
    il = lift.il; method = lift._current_method
    owner, target = il.meta.typedefs; block = lift.out.block
    if shape == 'parameter': method.param_count = 1
    elif shape == 'generic': method.generic_container = 0
    elif shape == 'no-address': method.addr = 0
    elif shape == 'method-index': method.index = -1
    elif shape == 'method-row': il.meta.methods[0] = NS(**vars(method))
    elif shape == 'return-index': method.return_type = len(il.types)
    elif shape == 'return-mismatch': method.return_type = 2
    elif shape == 'no-candidate': il.addr_candidates.clear()
    elif shape == 'generic-candidate': il.addr_candidates[START] = [('generic', 0)]
    elif shape == 'owner-generic': owner.generic_container = 0
    elif shape == 'owner-open-outer': owner.declaring = 3; target.generic_container = 0
    elif shape == 'owner-cycle': owner.declaring = 2
    elif shape == 'owner-out-of-range': method.declaring = 999
    elif shape == 'target-generic': target.generic_container = 0
    elif shape == 'target-open-outer': target.declaring = 2; owner.generic_container = 0
    elif shape == 'target-cycle': target.declaring = 3
    elif shape == 'target-class': target.is_valuetype = False
    elif shape == 'target-enum': target.is_enum = True
    elif shape == 'target-cctor': target.has_cctor = True
    elif shape == 'target-cctor-row': il.meta.methods[1].name = '.cctor'
    elif shape == 'target-method-start': target.method_start = -1
    elif shape == 'target-method-count': target.method_count = 999
    elif shape == 'target-explicit': target.flags = 0x10
    elif shape == 'target-packed': target.bitfield = 1
    elif shape == 'target-field-start': target.field_start = -1
    elif shape == 'target-field-count': target.field_count = 999
    elif shape == 'target-field-type': il.meta.fields[1].type = 999
    elif shape == 'field-byref': il.types[1] = (0, (8 << 16) | (1 << 29))
    elif shape == 'field-explicit': il.types[1] = (0, 0x11 << 16); owner.flags = 0x10
    elif shape == 'field-generic': il.types[1] = (0, 0x13 << 16)
    elif shape == 'size-unknown': il._sf_field_size = lambda *a: None
    elif shape == 'size-three': il._sf_field_size = lambda *a: 3
    elif shape == 'size-large': il._sf_field_size = lambda *a: 16
    elif shape == 'sret': il.returns_sret = lambda ty: True
    elif shape == 'type-key': il._closed_type_key = lambda ty: None
    elif shape == 'byref': ty = (1, (0x11 << 16) | (1 << 29))
    elif shape == 'generic-return': ty = (1, 0x15 << 16)
    elif shape == 'class-return': ty = (1, 0x12 << 16)
    elif shape == 'bad-typedef': ty = (999, 0x11 << 16)
    elif shape == 'entry': block.bid = 1
    elif shape == 'pred': block.preds = [1]
    elif shape == 'ip': lift._cur_ip += 1
    elif shape == 'no-value': lift.regs.clear()
    elif shape == 'unknown-value': lift.regs['RAX']._unk = True
    elif shape == 'value-text': lift.regs['RAX'].text = 'other'
    elif shape == 'text': text = '1'
    elif shape == 'native-different':
        raw = bytearray(il.bin.d); raw[0x100:0x102] = b'\x33\xc9'; il.bin.d = bytes(raw)
    elif shape == 'native-truncated': il.bin.d = il.bin.d[:0x102]
    elif shape == 'offset-none': il.bin.va2off = lambda va: None
    elif shape == 'offset-negative': il.bin.va2off = lambda va: -1
    elif shape == 'offset-outside': il.bin.va2off = lambda va: len(il.bin.d)
    elif shape == 'abstract': method.flags |= 0x400
    elif shape == 'pinvoke': method.flags |= 0x2000
    elif shape == 'runtime': method.iflags |= 3
    elif shape == 'synchronized': method.iflags |= 0x20
    elif shape == 'unmanaged': method.iflags |= 4
    elif shape == 'native-iflag': method.iflags |= 1
    elif shape == 'abi-elf': il.bin = NS(d=b'\x7fELF', is64=True)
    elif shape == 'abi-pe32': il.bin.is64 = False
    elif shape == 'abi-arm64':
        raw = bytearray(il.bin.d); raw[0x44:0x46] = b'\x64\xaa'; il.bin.d = bytes(raw)
    elif shape == 'abi-bad-header': il.bin.d = b'invalid'
    elif shape == 'no-disassembler': monkeypatch.setattr(leafreturns, 'HAVE_ICED', False)
    elif shape == 'no-context': lift = None
    elif shape == 'chain-offset': il.chains[1] = {0x14: ('payload', 1)}
    elif shape == 'chain-extra': il.chains[1][0x18] = ('extra', 1)
    elif shape == 'chain-type': il.chains[1][0x10] = ('payload', 0)
    elif shape == 'field-width':
        il._sf_field_size = lambda ft, depth: width if ft == ty else width + 1
    elif shape == 'field-enum': il.types[1] = (0, 0x11 << 16); owner.is_enum = True
    elif shape == 'class-value-confusion': il.types[1] = (0, 0x12 << 16)
    else: raise AssertionError(shape)
    assert recover(lift, text, ty) is None


@pytest.mark.parametrize('width', [1, 2, 4, 8])
@pytest.mark.parametrize('raw', [
    '30c0c3', '6633c0c3', '33c9c3', '4833c9c3', '33c1c3',
    'b800000000c3', '4831c0c20800', '9033c0c3', '33c090c3',
    '33c0e800000000c3', '33c0eb00c3', '33c0cc', 'f333c0c3',
    'f233c0c3', '6433c0c3', '33c0f3c3', '33c0f2c3', '33c064c3',
    '33c0c20400', '4833c090c3', '33c066c3', '4833c0cb',
])
def test_native_shape_is_not_inferred_from_scalar_text(width, raw):
    assert recover(*setup(width, source=bytes.fromhex(raw))) is None


@pytest.mark.parametrize('width', [1, 2, 4, 8])
def test_no_counted_reads_or_mutation_and_no_constructor_guess(width):
    lift, text, ty = setup(width, ctor=b'\xcc')
    # Address sharing and constructor side effects do not change default(T).
    lift.il.addr_candidates[START] += [('method', 1), ('generic', 123)]
    lift.il.meta.methods[1].flags = 1  # private ctor, deliberately not invoked
    class UncountedOnly(dict):
        def get(self, *args): raise AssertionError('counted read')
        def __getitem__(self, key): raise AssertionError('counted read')
    value = dict.get(lift.regs, 'RAX')
    before = tuple(getattr(value, key, None) for key in Expr.__slots__)
    lift.regs = UncountedOnly(lift.regs)
    lift._type_hints = {}; lift.slot_types = {}; lift._var_types = {}
    assert recover(lift, text, ty) == 'default(Example.Wrapper)'
    assert before == tuple(getattr(value, key, None) for key in Expr.__slots__)
    assert not lift._type_hints and not lift.slot_types and not lift._var_types


@pytest.mark.parametrize('ty', [None, (), (0,), ('bad', 'bad'), [1, 0x11 << 16]])
def test_malformed_type_declines(ty):
    assert recover(None, '0', ty) is None


@pytest.mark.parametrize('width', [1, 2, 4, 8])
def test_existing_boolean_enum_and_nonleaf_spelling_is_unchanged(width):
    lift, _, ty = setup(width)
    assert Decompiler._return_literal_text(None, lift, '0', (0, 2 << 16)) == 'false'
    assert Decompiler._return_literal_text(None, lift, '1', (0, 2 << 16)) == 'true'
    lift.il.enum_members = lambda td: {0: 'Zero'}
    lift.il.meta.typedefs[1].is_enum = True
    lift.il.meta.typedefs[1].name = 'Status'
    assert Decompiler._return_literal_text(None, lift, '0', ty) == 'Status.Zero'
    lift.il.enum_members = lambda td: None
    lift.il.meta.typedefs[1].is_enum = False
    lift.out.block.insns = lift.out.block.insns + lift.out.block.insns
    assert Decompiler._return_literal_text(None, lift, '0', ty) == '0'


@pytest.mark.parametrize('width, te', [(1, 2), (1, 4), (1, 5), (2, 3), (2, 6),
                                     (2, 7), (4, 8), (4, 9), (4, 0x0c),
                                     (8, 0x0a), (8, 0x0b), (8, 0x0d),
                                     (8, 0x0e), (8, 0x12), (8, 0x18),
                                     (8, 0x19), (8, 0x1c)])
def test_zero_means_default_bits_for_exact_scalar_or_reference_field(width, te):
    lift, text, ty = setup(width)
    lift.il.types[1] = (0, (te << 16) | 0x21)  # private readonly payload
    if te == 0x12:
        lift.il.meta.typedefs[0].is_valuetype = False
    assert recover(lift, text, ty) == 'default(Example.Wrapper)'
