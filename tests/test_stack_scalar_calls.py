"""Direct native scalar homes, not speculative signature hints."""
from types import SimpleNamespace as NS
import struct
import pytest
from iced_x86 import Decoder
from il2cpp.expr import Expr
from il2cpp.binary import PE
from il2cpp.lifter.stackscalars import recover_stack_scalars

VOID=(0,1<<16); INT=(0,8<<16); BOOL=(0,2<<16); ENUM=(1,0x11<<16)
START=0x180001000; TARGET=0x180010000

def setup(value=1, enum=False, before=b'', after=b'', store=None, instance=False):
    width=4 if enum else 1
    if store is None:
        store=(b'\xc7\x44\x24\x20'+struct.pack('<I',value&0xffffffff)) if enum else b'\xc6\x44\x24\x20'+bytes([value&0xff])
    prefix=before+store+after
    raw=prefix+b'\xe8'+struct.pack('<i',TARGET-(START+len(prefix)+5))
    insns=list(Decoder(64,raw,ip=START));call=insns[-1]
    owner=NS(generic_container=-1,declaring=-1,is_valuetype=False)
    etd=NS(is_enum=True,is_valuetype=True,generic_container=-1,declaring=-1,element=-1)
    method=NS(index=0,addr=TARGET,generic_container=-1,declaring=0,return_type=0,is_static=not instance,param_count=4 if instance else 5)
    types=[VOID,INT,BOOL,ENUM];params=[NS(type=1) for _ in range(method.param_count-1)]+[NS(type=3 if enum else 2)]
    meta=NS(typedefs=[owner,etd],methods=[method],method_params=lambda m:params,fields=[NS(name='value__',type=1)],type_fields=lambda td:[0])
    il=NS(meta=meta,types=types,addr_candidates={TARGET:[('method',0)]},_type_enum=lambda t:(t[1]>>16)&255,_closed_type_key=lambda t:t,enum_members=lambda td:{-1:'MinusOne',0:'Zero',1:'One',127:'Largest'},type_name=lambda t:'Example.Mode')
    binary = PE.__new__(PE)
    image = bytearray(0x80)
    struct.pack_into('<I', image, 0x3c, 0x40)
    image[0x40:0x46] = b'PE\x00\x00\x64\x86'
    binary.d = bytes(image)
    binary.is64 = True
    il.bin = binary
    lift=NS(il=il,out=NS(block=NS(insns=insns)),_cur_ip=call.ip,rsp_delta=-128,stack_map={-96:'s_20'},stack_values={'s_20':Expr(str(value),None,'int')})
    args=['a','b','c','d',str(value)]
    return lift,method,VOID,args

def recover(state):return recover_stack_scalars(*state)

@pytest.mark.parametrize('enum,value,text',[(False,0,'false'),(False,1,'true'),(True,-1,'Example.Mode.MinusOne'),(True,0,'Example.Mode.Zero'),(True,1,'Example.Mode.One'),(True,127,'Example.Mode.Largest')])
@pytest.mark.parametrize('instance',[False,True])
def test_exact_immediate_home(enum,value,text,instance):
    state=setup(value,enum,instance=instance);old=list(state[3]);out=recover(state)
    assert out==old[:4]+[text] and state[3]==old
    assert state[0].stack_values['s_20'].text==str(value)

@pytest.mark.parametrize('after',[b'\x48\x89\xf1',b'\x4c\x8d\x4c\x24\x40',b'\xc7\x44\x24\x28\x02\x00\x00\x00',b'\x48\x8b\x05\x00\x00\x00\x00'])
def test_harmless_register_setup_and_disjoint_home_writes(after):
    assert recover(setup(after=after))[-1]=='true'

@pytest.mark.parametrize('after',[b'\x90',b'\x48\x83\xc4\x00',b'\x89\xc4',b'\x66\x89\xc4',b'\x40\x88\xc4',b'\xe8\x00\x00\x00\x00',b'\xeb\x00',b'\x89\x00',b'\xc6\x44\x24\x20\x00',b'\x88\x44\x24\x20',b'\x66\xc7\x44\x24\x1f\x00\x00',b'\x64\x48\x8b\x00',b'\x50',b'\x0f\x0b'])
def test_alias_call_branch_partial_or_unknown_barriers_decline(after):
    state=setup(after=after);assert recover(state) is state[3]

@pytest.mark.parametrize('store',[b'\x88\x44\x24\x20',b'\xc7\x44\x24\x20\x01\x00\x00\x00',b'\xc6\x44\x24\x21\x01',b'\xc6\x44\x25\x20\x01',b'\x64\xc6\x44\x24\x20\x01',b'\x67\xc6\x44\x24\x20\x01'])
def test_only_exact_width_rsp_immediate_store_proves_bool(store):
    state=setup(store=store);assert recover(state) is state[3]

@pytest.mark.parametrize('change',['unknown','missing-value','wrong-value','complex-value','wrong-kind','missing-home','rsp-delta','no-block','alternate-entry','no-call','target','shared','generic-method','generic-owner','nested-owner','value-owner','return-byref','return-generic','sret','bad-index','not-canonical-method','incomplete-params','byref-param'])
def test_missing_or_conflicting_value_abi_and_identity_evidence_declines(change):
    state=setup();lift,m,rty,args=state;il=lift.il
    if change=='unknown':lift.stack_values['s_20']._unk=True
    elif change=='missing-value':lift.stack_values.clear()
    elif change=='wrong-value':lift.stack_values['s_20'].text='0'
    elif change=='complex-value':args[-1]=lift.stack_values['s_20'].text='f()'
    elif change=='wrong-kind':lift.stack_values['s_20'].kind='ptr'
    elif change=='missing-home':lift.stack_map.clear()
    elif change=='rsp-delta':lift.rsp_delta+=8
    elif change=='no-block':lift.out.block=None
    elif change=='alternate-entry':lift.out.block.insns=lift.out.block.insns[1:]
    elif change=='no-call':lift._cur_ip+=1
    elif change=='target':m.addr+=1
    elif change=='shared':il.addr_candidates[m.addr].append(('method',1))
    elif change=='generic-method':m.generic_container=0
    elif change=='generic-owner':il.meta.typedefs[0].generic_container=0
    elif change=='nested-owner':il.meta.typedefs[0].declaring=1
    elif change=='value-owner':il.meta.typedefs[0].is_valuetype=True
    elif change=='return-byref':il.types[0]=(0,1<<16|1<<29);rty=il.types[0]
    elif change=='return-generic':il.types[0]=(0,0x15<<16);rty=il.types[0]
    elif change=='sret':il.types[0]=(1,0x11<<16);rty=il.types[0]
    elif change=='bad-index':m.index=-1
    elif change=='not-canonical-method':il.meta.methods[0]=NS()
    elif change=='incomplete-params':m.param_count+=1
    elif change=='byref-param':il.types[2]=(0,2<<16|1<<29)
    assert recover((lift,m,rty,args)) is args

@pytest.mark.parametrize('value',[2,3,255])
def test_noncanonical_bool_literals_decline(value):
    state=setup(value);assert recover(state) is state[3]

@pytest.mark.parametrize('change',['not-enum','not-value','generic','open','underlying64','byref-underlying','bad-underlying','missing-underlying','element64','element-bad','no-members','unmatched-member','wrong-width','partial-overwrite'])
def test_enum_requires_closed_int32_named_member_and_exact_store(change):
    state=setup(enum=True);lift,m,rty,args=state;il=lift.il;td=il.meta.typedefs[1]
    if change=='not-enum':td.is_enum=False
    elif change=='not-value':td.is_valuetype=False
    elif change=='generic':td.generic_container=0
    elif change=='open':il._closed_type_key=lambda t:None
    elif change=='underlying64':il.types[1]=(0,0x0a<<16)
    elif change=='byref-underlying':il.types[1]=(0,8<<16|1<<29)
    elif change=='bad-underlying':il.meta.fields[0].type=-1
    elif change=='missing-underlying':il.meta.fields.clear();il.meta.type_fields=lambda td:[]
    elif change=='element64':td.element=0;il.types[0]=(0,0x0a<<16)
    elif change=='element-bad':td.element=100
    elif change=='no-members':il.enum_members=lambda td:None
    elif change=='unmatched-member':il.enum_members=lambda td:{2:'Two'}
    elif change=='wrong-width':state=setup(enum=True,store=b'\xc6\x44\x24\x20\x01');args=state[3]
    elif change=='partial-overwrite':state=setup(enum=True,after=b'\xc6\x44\x24\x21\x00');args=state[3]
    assert recover(state) is args


@pytest.mark.parametrize('before', [b'\x90', b'\xe8\x00\x00\x00\x00',
                                    b'\x89\x00', b'\xc6\x44\x24\x20\x00'])
def test_earlier_effects_do_not_invalidate_a_later_full_immediate_definition(before):
    assert recover(setup(before=before))[-1] == 'true'


@pytest.mark.parametrize('position', [4, 5, 6, 7, 8, 9])
@pytest.mark.parametrize('instance', [False, True])
def test_exact_stack_position_is_not_an_integer_argument_ordinal(position, instance):
    offset = 0x20 + 8 * (position - 4)
    state = setup(instance=instance, store=b'\xc6\x44\x24' + bytes([offset, 1]))
    lift, method, rty, args = state
    method.param_count = position + (0 if instance else 1)
    params = [NS(type=1) for _ in range(method.param_count - 1)] + [NS(type=2)]
    lift.il.meta.method_params = lambda m: params
    lift.stack_map = {lift.rsp_delta + offset: 'home'}
    lift.stack_values = {'home': Expr('1', None, 'int')}
    args = ['arg'] * position + ['1']
    assert recover((lift, method, rty, args)) == args[:-1] + ['true']


@pytest.mark.parametrize('te', [0x03, 0x04, 0x08, 0x0a, 0x0c, 0x0d, 0x0f,
                              0x10, 0x12, 0x13, 0x15, 0x1d, 0x1e])
def test_other_parameter_shapes_are_not_hinted_or_cast(te):
    state = setup()
    state[0].il.types[2] = (0, te << 16)
    assert recover(state) is state[3]


def test_symbolic_literal_must_equal_the_actual_native_immediate():
    state = setup(store=b'\xc6\x44\x24\x20\x00')
    assert recover(state) is state[3]


def test_nested_enum_and_conflicting_element_metadata_decline():
    state = setup(enum=True)
    state[0].il.meta.typedefs[1].declaring = 0
    assert recover(state) is state[3]
    state = setup(enum=True)
    state[0].il.types.append((0, 0x0a << 16))
    state[0].il.meta.typedefs[1].element = 4
    assert recover(state) is state[3]


def test_int32_element_metadata_can_agree_with_the_instance_field():
    state = setup(enum=True)
    state[0].il.meta.typedefs[1].element = 1
    assert recover(state)[-1] == 'Example.Mode.One'


@pytest.mark.parametrize('raw', [b'\xe9\x00\x00\x00\x00', b'\xff\x10'])
def test_tail_or_indirect_call_is_not_a_unique_direct_consumer(raw):
    state = setup()
    lift = state[0]
    instructions = lift.out.block.insns
    instructions[-1] = Decoder(64, raw, ip=lift._cur_ip).decode()
    assert recover(state) is state[3]


def test_missing_native_instruction_cannot_hide_a_crossed_effect():
    state = setup(after=b'\x90')
    state[0].out.block.insns.pop(1)
    assert recover(state) is state[3]


@pytest.mark.parametrize('enum', [False, True])
def test_positional_call_integration_preserves_float_slot_and_all_type_hints(enum):
    from il2cpp.lifter.values import _ValuesMixin
    state = setup(enum=enum)
    lift, method, rty, args = state
    lift.il.types.append((0, 0x0c << 16))
    params = lift.il.meta.method_params(method)
    params[0].type = 4
    lift.il.returns_sret = lambda t: False
    lift.meta = lift.il.meta
    lift._class_type_subst = lambda t: t
    lift._xmm_pending = [(0, Expr('1.25f', lift.il.types[4], 'float'))]
    lift._stack_arg_texts = lambda count: _ValuesMixin._stack_arg_texts(lift, count)
    lift.slot_types = {}
    lift._type_hints = {}
    result = _ValuesMixin._positional_args(lift, args[:4], method, rty)
    assert result == ['1.25f', 'b', 'c', 'd', 'Example.Mode.One' if enum else 'true']
    assert not lift.slot_types and not lift._type_hints
    assert lift.stack_values['s_20'].text == '1'


@pytest.mark.parametrize('shape', ['unknown', 'pe32', 'arm64', 'bad-header', 'truncated', 'bad-offset'])
def test_non_windows_x64_or_malformed_binary_does_not_assume_this_abi(shape):
    state = setup()
    binary = state[0].il.bin
    if shape == 'unknown':state[0].il.bin = NS(is64=True, d=binary.d)
    elif shape == 'pe32':binary.is64 = False
    elif shape == 'arm64':binary.d = binary.d[:0x44] + b'\x64\xaa' + binary.d[0x46:]
    elif shape == 'bad-header':binary.d = b'\x00' * len(binary.d)
    elif shape == 'truncated':binary.d = b''
    else:
        data = bytearray(binary.d)
        struct.pack_into('<I', data, 0x3c, len(data) - 2)
        binary.d = bytes(data)
    assert recover(state) is state[3]


@pytest.mark.parametrize('shape', ['elf64', 'x86', 'truncated-machine',
                                  'missing-data', 'truncated-offset'])
def test_stack_scalar_shared_abi_guard_keeps_unsupported_shapes_raw(shape):
    from il2cpp.binary import ELF
    state = setup()
    binary = state[0].il.bin
    assert recover(state)[-1] == 'true'
    if shape == 'elf64':
        other = ELF.__new__(ELF)
        other.is64 = True
        other.d = b'\x7fELF' + bytes(124)
        state[0].il.bin = other
    elif shape == 'x86':
        data = bytearray(binary.d)
        struct.pack_into('<H', data, 0x44, 0x14c)
        binary.d = bytes(data)
    elif shape == 'truncated-machine':binary.d = binary.d[:0x45]
    elif shape == 'truncated-offset':binary.d = binary.d[:0x3e]
    else:del binary.d
    assert recover(state) is state[3]
