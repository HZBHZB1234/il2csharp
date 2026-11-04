"""Exact native field copies need an owned, side-effect-free managed wrapper."""
import pytest
from iced_x86 import Mnemonic, OpKind, Register as R, MemorySizeExt

from game_support import lift_text
from il2cpp.dec import analyze

pytestmark = pytest.mark.game('unitask')


def test_small_struct_returns_match_native_load_and_owned_copy_ctor(
        raw_game_decompiler, monkeypatch):
    il,dec=raw_game_decompiler
    original=analyze.recover_leaf_struct_return
    hits={}

    def observe(lift,text,ty):
        values={k:tuple(getattr(v,s,None) for s in v.__slots__) if v else None
                for k,v in dict.items(lift.regs)}
        hints,slots,types=dict(lift._type_hints),dict(lift.slot_types),dict(lift._var_types)
        result=original(lift,text,ty)
        assert values=={k:tuple(getattr(v,s,None) for s in v.__slots__) if v else None
                        for k,v in dict.items(lift.regs)}
        assert hints==lift._type_hints and slots==lift.slot_types and types==lift._var_types
        if result is not None and not lift.dry:
            method=lift._current_method;td=il.meta.typedefs[ty[0]]
            assert method.index in (19861,21371)
            assert td.is_valuetype and not td.is_enum and not td.has_cctor
            native,_=dec._decode(method)
            load,ret=native[:2]
            width=il.type_sizes[ty[0]]
            assert width in (4,8)
            assert [load.ip,ret.ip]==[i.ip for i in lift.out.block.insns]
            assert load.mnemonic==Mnemonic.MOV and ret.mnemonic==Mnemonic.RET
            assert load.op0_register==(R.EAX if width==4 else R.RAX)
            assert load.op1_kind==OpKind.MEMORY and load.memory_base==R.RCX
            assert load.memory_index==R.NONE and MemorySizeExt.size(load.memory_size)==width
            field=il.meta.fields[td.field_start]
            field_ty=il.types[field.type]
            assert td.field_count==1 and il.field_offsets[ty[0]]==[0x10]
            assert field_ty[1]&7==1  # original private fields, not publicized output
            key=il._closed_type_key(field_ty)
            ctors=[c for c in il.meta.methods[td.method_start:td.method_start+td.method_count]
                   if c.name=='.ctor' and c.param_count==1
                   and il._closed_type_key(il.types[il.meta.params[c.parameter_start].type])==key]
            assert len(ctors)==1
            ctor=ctors[0]
            assert ctor.declaring==ty[0] and ctor.flags&7==6
            assert ctor.image==method.image and ctor.iflags&0x1037==0
            assert not any(c.name=='.cctor' for c in il.meta.methods[td.method_start:td.method_start+td.method_count])
            native_ctor,_=dec._decode(ctor)
            store,end=native_ctor[:2]
            assert store.mnemonic==Mnemonic.MOV and end.mnemonic==Mnemonic.RET
            assert store.op0_kind==OpKind.MEMORY and store.memory_base==R.RCX
            assert store.memory_index==R.NONE and store.memory_displacement==0
            assert store.op1_register==(R.EDX if width==4 else R.RDX)
            assert MemorySizeExt.size(store.memory_size)==width
            assert store.next_ip==end.ip and end.op_count==0
            assert result=='new '+il.type_name(ty)+'('+text+')'
            hits[method.index]=(text,result,ctor.index,field.name)
        return result

    monkeypatch.setattr(analyze,'recover_leaf_struct_return',observe)
    candidates={mi:lift_text(il,dec,mi) for mi in (19861,21371)}
    assert set(hits)=={19861,21371}
    monkeypatch.setattr(analyze,'recover_leaf_struct_return',lambda *a:None)
    for mi,body in candidates.items():
        old,new,ci,field=hits[mi]
        baseline=lift_text(il,dec,mi)
        assert baseline.count('return '+old+';')==1
        assert baseline.replace('return '+old+';','return '+new+';')==body
        # The generated constructor is also the exact copy, not an unresolved
        # shared-address stub. Derive names from metadata rather than pin bodies.
        ctor=il.meta.methods[ci]
        parameter=il.meta.params[ctor.parameter_start].name
        lines=[line.strip() for line in lift_text(il,dec,ci).splitlines()
               if line.strip() not in ('','unsafe','{','}','return;')]
        assert lines==['this.'+field+' = '+parameter+';']
