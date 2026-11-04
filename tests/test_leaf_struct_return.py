"""Authored Win64 leaf/ctor shapes: wrappers need both metadata and native proof."""
import struct
from types import SimpleNamespace as NS

import pytest
from iced_x86 import Decoder

from il2cpp import Lifter, Decompiler
from il2cpp.binary import PE
from il2cpp.expr import Expr
from il2cpp.lifter import leafreturns
from il2cpp.lifter.leafreturns import recover_leaf_struct_return

START = 0x180001000
CTOR = START + 0x80
VOID = (0, 1 << 16)


def setup(width=4, source=None, ctor=None):
    scalar = (0, (8 if width == 4 else 0x0a) << 16 | 1)
    owner_ty, target_ty = (0, 0x11 << 16), (1, 0x11 << 16)
    types = [VOID, scalar, owner_ty, target_ty]
    method = NS(index=0, name='Copy', addr=START, generic_container=-1,
                declaring=0, return_type=3, is_static=False, param_count=0, image=0)
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
    source = source if source is not None else (b'\x48' if width == 8 else b'') + b'\x8b\x01\xc3'
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
          type_name=lambda ty:'Example.Wrapper')
    insns=list(Decoder(64,source,ip=START))
    lift=NS(il=il,meta=meta,_current_method=method,_cur_ip=insns[-1].ip,
            out=NS(block=NS(bid=0,preds=[],insns=insns)),
            regs={'RAX':Expr('this.input',scalar,'int')})
    lift._td_of=lambda ty:ty[0] if il._type_enum(ty)==0x11 else None
    lift._piece_layout_proven=lambda ty,seen=frozenset():Lifter._piece_layout_proven(lift,ty,seen)
    return lift,'this.input',target_ty


@pytest.mark.parametrize('width',[4,8])
def test_exact_owned_copy_constructor_not_initializer(width):
    assert recover_leaf_struct_return(*setup(width))=='new Example.Wrapper(this.input)'


@pytest.mark.parametrize('width',[4,8])
@pytest.mark.parametrize('shape',[
    'static','generic','parameter','wrong-index','wrong-row','no-address',
    'bad-return-index','wrong-return-type','owner-class','owner-enum',
    'owner-generic','owner-open-outer','owner-cycle','owner-byval',
    'target-class','target-enum','target-generic','target-open-outer',
    'target-cycle','target-explicit','owner-explicit','target-packed',
    'owner-packed','target-fields','target-field-start','target-field-type',
    'target-chain-offset','target-chain-type','target-chain-extra',
    'source-chain-missing','source-chain-type','entry','predecessor','ip',
    'missing-value','unknown-value','value-type','value-text','input-text',
    'byref','generic-type','no-type','return-type-disagrees','width',
    'field-width','field-float','field-byref','target-cctor-flag',
    'ctor-private','ctor-generic','ctor-static','ctor-parameters',
    'ctor-owner','ctor-index','ctor-address','ctor-pinvoke','ctor-abstract',
    'ctor-runtime','ctor-synchronized','ctor-unmanaged','ctor-security','ctor-special-flags','ctor-other-image','ctor-return','ctor-return-byref','ctor-param-start',
    'ctor-param-type','ctor-byref','ctor-candidate','ctor-range','ctor-count',
    'abi-unknown','abi-elf','abi-pe32','abi-arm64','abi-bad-header',
    'no-disassembler',
])
def test_every_unproved_metadata_context_or_abi_declines(width,shape,monkeypatch):
    lift,text,ty=setup(width);il=lift.il;meta=il.meta
    m,c=meta.methods;owner,target=meta.typedefs;b=lift.out.block
    if shape=='static':m.is_static=True
    elif shape=='generic':m.generic_container=0
    elif shape=='parameter':m.param_count=1
    elif shape=='wrong-index':m.index=-1
    elif shape=='wrong-row':m.index=1
    elif shape=='no-address':m.addr=0
    elif shape=='bad-return-index':m.return_type=-1
    elif shape=='wrong-return-type':m.return_type=1
    elif shape=='owner-class':owner.is_valuetype=False
    elif shape=='owner-enum':owner.is_enum=True
    elif shape=='owner-generic':owner.generic_container=0
    elif shape=='owner-open-outer':owner.declaring=3;target.generic_container=0
    elif shape=='owner-cycle':owner.declaring=2
    elif shape=='owner-byval':owner.byval=3
    elif shape=='target-class':target.is_valuetype=False
    elif shape=='target-enum':target.is_enum=True
    elif shape=='target-generic':target.generic_container=0
    elif shape=='target-open-outer':target.declaring=2;owner.generic_container=0
    elif shape=='target-cycle':target.declaring=3
    elif shape=='target-explicit':target.flags=0x10
    elif shape=='owner-explicit':owner.flags=0x10
    elif shape=='target-packed':target.bitfield=1
    elif shape=='owner-packed':owner.bitfield=1
    elif shape=='target-fields':target.field_count=2
    elif shape=='target-field-start':target.field_start=-1
    elif shape=='target-field-type':meta.fields[1].type=-1
    elif shape=='target-chain-offset':il.chains[1]={0x14:('payload',1)}
    elif shape=='target-chain-type':il.chains[1]={0x10:('payload',2)}
    elif shape=='target-chain-extra':il.chains[1][0x14]=('extra',1)
    elif shape=='source-chain-missing':il.chains[0]={}
    elif shape=='source-chain-type':il.chains[0]={0x10:('input',2)}
    elif shape=='entry':b.bid=1
    elif shape=='predecessor':b.preds=[1]
    elif shape=='ip':lift._cur_ip+=1
    elif shape=='missing-value':lift.regs={}
    elif shape=='unknown-value':lift.regs['RAX']._unk=True
    elif shape=='value-type':lift.regs['RAX'].ty=ty
    elif shape=='value-text':lift.regs['RAX'].text='other'
    elif shape=='input-text':text='other'
    elif shape=='byref':ty=(ty[0],ty[1]|(1<<29))
    elif shape=='generic-type':ty=(ty[0],0x15<<16)
    elif shape=='no-type':ty=None
    elif shape=='return-type-disagrees':ty=(0,ty[1])
    elif shape=='width':il._sf_field_size=lambda ty,d:16
    elif shape=='field-width':il._sf_field_size=lambda t,d:width if t==ty else 2
    elif shape=='field-float':
        il.types[1]=(0,0x0c<<16|1);lift.regs['RAX'].ty=il.types[1]
    elif shape=='field-byref':il.types[1]=(0,il.types[1][1]|(1<<29))
    elif shape=='target-cctor-flag':target.has_cctor=True
    elif shape=='ctor-private':c.flags=(c.flags&~7)|1
    elif shape=='ctor-generic':c.generic_container=0
    elif shape=='ctor-static':c.is_static=True
    elif shape=='ctor-parameters':c.param_count=2
    elif shape=='ctor-owner':c.declaring=0
    elif shape=='ctor-index':c.index=-1
    elif shape=='ctor-address':c.addr=0
    elif shape=='ctor-pinvoke':c.flags|=0x2000
    elif shape=='ctor-abstract':c.flags|=0x400
    elif shape=='ctor-runtime':c.iflags|=0x1000
    elif shape=='ctor-synchronized':c.iflags|=0x20
    elif shape=='ctor-unmanaged':c.iflags|=0x4
    elif shape=='ctor-security':c.flags|=0x4000
    elif shape=='ctor-special-flags':c.flags&=~0x1000
    elif shape=='ctor-other-image':c.image=1
    elif shape=='ctor-return':c.return_type=1
    elif shape=='ctor-return-byref':il.types[0]=(0,VOID[1]|(1<<29))
    elif shape=='ctor-param-start':c.parameter_start=-1
    elif shape=='ctor-param-type':meta.params[0].type=-1
    elif shape=='ctor-byref':il.types.append((0,il.types[1][1]|(1<<29)));meta.params[0].type=4
    elif shape=='ctor-candidate':il.addr_candidates[CTOR]=[]
    elif shape=='ctor-range':target.method_start=-1
    elif shape=='ctor-count':target.method_count=2
    elif shape=='abi-unknown':il.bin=NS(is64=True,d=il.bin.d)
    elif shape=='abi-elf':
        from il2cpp.binary import ELF
        il.bin=ELF.__new__(ELF);il.bin.is64=True
    elif shape=='abi-pe32':il.bin.is64=False
    elif shape=='abi-arm64':il.bin.d=il.bin.d[:0x44]+b'\x64\xaa'+il.bin.d[0x46:]
    elif shape=='abi-bad-header':il.bin.d=b''
    elif shape=='no-disassembler':monkeypatch.setattr(leafreturns,'HAVE_ICED',False)
    else:raise AssertionError(shape)
    assert recover_leaf_struct_return(lift,text,ty) is None,shape


@pytest.mark.parametrize('width',[4,8])
@pytest.mark.parametrize('raw',[
    b'\x8a\x01\xc3',b'\x66\x8b\x01\xc3',b'\x8b\x02\xc3',
    b'\x8b\x11\xc3',b'\x8b\x04\x11\xc3',b'\x64\x8b\x01\xc3',
    b'\x8b\x01\xc2\x08\x00',b'\x8b\x01\x90\xc3',b'\x8b\x01\xcc',
    b'\x33\xc0\xc3',b'\xf3\x8b\x01\xc3',b'\x8b\x01\xf3\xc3',
])
def test_native_return_must_be_exact_load_and_plain_ret(width,raw):
    assert recover_leaf_struct_return(*setup(width,source=raw)) is None


@pytest.mark.parametrize('width',[4,8])
@pytest.mark.parametrize('raw',[
    b'\x89\x01\xc3',b'\x89\x51\x04\xc3',b'\x88\x11\xc3',
    b'\x66\x89\x11\xc3',b'\x89\x14\x11\xc3',b'\x64\x89\x11\xc3',
    b'\x89\x11\xc2\x08\x00',b'\x89\x11\x33\xc0\xc3',b'\x89\x11\xcc',
    b'\xf3\x89\x11\xc3',b'\x89\x11\xf3\xc3',
])
def test_constructor_must_be_exact_copy_and_plain_ret(width,raw):
    if width==8:raw=b'\x48'+raw
    assert recover_leaf_struct_return(*setup(width,ctor=raw)) is None


@pytest.mark.parametrize('width',[4,8])
def test_no_counted_reads_or_state_mutation_and_literal_behavior(width):
    lift,text,ty=setup(width)
    class UncountedOnly(dict):
        def get(self,*a):raise AssertionError('counted get')
        def __getitem__(self,key):raise AssertionError('counted lookup')
    value=lift.regs['RAX'];lift.regs=UncountedOnly(lift.regs)
    before=tuple(getattr(value,name,None) for name in Expr.__slots__)
    assert recover_leaf_struct_return(lift,text,ty)=='new Example.Wrapper(this.input)'
    assert tuple(getattr(value,name,None) for name in Expr.__slots__)==before
    assert Decompiler._return_literal_text(None,lift,text,ty)=='new Example.Wrapper(this.input)'
    assert Decompiler._return_literal_text(None,lift,'0',(0,2<<16))=='false'
    assert Decompiler._return_literal_text(None,lift,'1',(0,2<<16))=='true'


@pytest.mark.parametrize('width',[4,8])
@pytest.mark.parametrize('shape',['nested-target','private-readonly','shared-address',
                                  'cctor-row','duplicate-ctor','zero-arg-ctor'])
def test_exact_owned_identity_not_publicized_fields_or_address_guess(width,shape):
    lift,text,ty=setup(width);il=lift.il;target=il.meta.typedefs[1]
    expected=True
    if shape=='nested-target':target.declaring=2
    elif shape=='private-readonly':
        il.types[1]=(0,il.types[1][1]|0x20);lift.regs['RAX'].ty=il.types[1]
    elif shape=='shared-address':il.addr_candidates[CTOR]+=[('method',0),('generic',123)]
    else:
        extra=NS(**vars(il.meta.methods[1]));extra.index=2
        il.meta.methods.append(extra);target.method_count+=1
        if shape=='cctor-row':extra.name='.cctor';extra.is_static=True;expected=False
        elif shape=='duplicate-ctor':expected=False
        else:extra.param_count=0
    assert (recover_leaf_struct_return(lift,text,ty) is not None)==expected


@pytest.mark.parametrize('width',[4,8])
def test_scalar_float_parameter_uses_xmm_not_a_gpr_even_at_same_size(width):
    lift,text,ty=setup(width)
    lift.il.types[1]=(0,(0x0c if width==4 else 0x0d)<<16|1)
    lift.regs['RAX'].ty=lift.il.types[1]
    assert recover_leaf_struct_return(lift,text,ty) is None


@pytest.mark.parametrize('return_ty',[None,(),(0,),('bad','bad'),(0,0x12<<16),
                                    (0,0x15<<16),(0,8<<16),[1,0x11<<16]])
def test_unsupported_return_metadata_declines_without_touching_lifter(return_ty):
    assert recover_leaf_struct_return(None,'anything',return_ty) is None
