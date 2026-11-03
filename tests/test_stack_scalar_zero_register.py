"""False byte homes need executed native zero/store evidence, not type hints."""
import struct
import pytest
from types import SimpleNamespace as NS
from iced_x86 import Decoder
from test_stack_scalar_calls import setup,START,TARGET
from il2cpp.lifter.stackscalars import recover_stack_scalars

def check(state):
 lift,method,rty,args=state
 return recover_stack_scalars(*state)[-1]=='false'
def zero(reg,width=4):
 low=reg&7;prefix=bytes([0x45 if reg>=8 else 0x40]) if reg>=8 else b''
 if width==8:prefix=bytes([0x4d if reg>=8 else 0x48])
 return prefix+b'\x33'+bytes([0xc0|(low<<3)|low])
def store(reg):
 prefix=b'\x44' if reg>=8 else b'\x40' if reg>=4 else b''
 return prefix+b'\x88'+bytes([0x44|((reg&7)<<3)])+b'\x24\x20'
def call_at(n):return b'\xe8'+struct.pack('<i',TARGET-(START+n+5))
@pytest.mark.parametrize('reg',[0,1,2,3,5,6,7,8,9,10,11,12,13,14,15])
@pytest.mark.parametrize('width',[4,8])
def test_exact_self_zero_before_low_byte_store(reg,width):
 assert check(setup(value=0,before=zero(reg,width),store=store(reg)))
@pytest.mark.parametrize('reg',[3,5,6,7,12,13,14,15])
@pytest.mark.parametrize('count',[1,3])
def test_only_preserved_registers_carry_zero_across_canonical_calls(reg,count):
 before=zero(reg)
 for _ in range(count):before+=call_at(len(before))
 assert check(setup(value=0,before=before,store=store(reg)))
@pytest.mark.parametrize('reg',[0,1,2,8,9,10,11])
def test_volatile_registers_cannot_carry_zero_across_call(reg):
 before=zero(reg);before+=call_at(len(before))
 assert not check(setup(value=0,before=before,store=store(reg)))
@pytest.mark.parametrize('part',[b'\x44\x8b\x3c\x24',b'\x41\xbf\x01\x00\x00\x00',b'\x41\x88\xc7',b'\x66\x45\x33\xff',b'\x45\x30\xff',b'\x50',b'\x90',b'\x48\x83\xc4\x00',b'\x89\x00',b'\xeb\x00'])
def test_clobbers_partial_zeros_unknowns_and_aliases_decline(part):
 assert not check(setup(value=0,before=zero(15)+part,store=store(15)))
@pytest.mark.parametrize('part',[b'\xe8\x00\x00\x00\x00',b'\xc6\x44\x24\x20\x01',b'\x89\x00',b'\xeb\x00',b'\x48\x83\xc4\x00',b'\x90'])
def test_post_store_call_write_and_control_flow_barriers(part):
 assert not check(setup(value=0,before=zero(15),store=store(15),after=part))
@pytest.mark.parametrize('shape',['missing-zero','partial-zero','wrong-source','wide-store','segment','unknown-call','shared-call','gap','no-block-start','too-far','nonzero-symbolic'])
def test_proof_boundaries_are_not_signature_guesses(shape):
 before=zero(15);st=store(15);value=0
 if shape=='missing-zero':before=b''
 elif shape=='partial-zero':before=bytes.fromhex('4530ff')
 elif shape=='wrong-source':st=store(14)
 elif shape=='wide-store':st=bytes.fromhex('44897c2420')
 elif shape=='segment':st=b'\x64'+st
 elif shape in ('unknown-call','shared-call'):before+=call_at(len(before))
 elif shape=='too-far':before+=bytes.fromhex('4889c9')*512
 elif shape=='nonzero-symbolic':value=1
 state=setup(value=value,before=before,store=st);lift=state[0]
 if shape=='unknown-call':lift.il.addr_candidates.clear()
 elif shape=='shared-call':lift.il.addr_candidates[TARGET].append(('method',0))
 elif shape in ('gap','no-block-start'):lift.out.block.insns=lift.out.block.insns[1:]
 assert not check(state)

@pytest.mark.parametrize('change', [
    'unknown', 'missing-value', 'wrong-value', 'complex-value', 'wrong-kind',
    'missing-home', 'rsp-delta', 'no-block', 'alternate-entry', 'no-call',
    'target', 'shared', 'generic-method', 'generic-owner', 'nested-owner',
    'value-owner', 'return-byref', 'return-generic', 'sret', 'bad-index',
    'not-canonical-method', 'incomplete-params', 'byref-param'])
def test_native_zero_requires_all_consumer_and_symbolic_guards(change):
    state = setup(value=0, before=zero(15), store=store(15))
    lift, method, rty, args = state
    il = lift.il
    assert check(state)
    if change == 'unknown': lift.stack_values['s_20']._unk = True
    elif change == 'missing-value': lift.stack_values.clear()
    elif change == 'wrong-value': lift.stack_values['s_20'].text = '1'
    elif change == 'complex-value': args[-1] = lift.stack_values['s_20'].text = 'f()'
    elif change == 'wrong-kind': lift.stack_values['s_20'].kind = 'ptr'
    elif change == 'missing-home': lift.stack_map.clear()
    elif change == 'rsp-delta': lift.rsp_delta += 8
    elif change == 'no-block': lift.out.block = None
    elif change == 'alternate-entry': lift.out.block.insns = lift.out.block.insns[1:]
    elif change == 'no-call': lift._cur_ip += 1
    elif change == 'target': method.addr += 1
    elif change == 'shared': il.addr_candidates[method.addr].append(('method', 1))
    elif change == 'generic-method': method.generic_container = 0
    elif change == 'generic-owner': il.meta.typedefs[0].generic_container = 0
    elif change == 'nested-owner': il.meta.typedefs[0].declaring = 1
    elif change == 'value-owner': il.meta.typedefs[0].is_valuetype = True
    elif change == 'return-byref': il.types[0] = rty = (0, 1 << 16 | 1 << 29)
    elif change == 'return-generic': il.types[0] = rty = (0, 0x15 << 16)
    elif change == 'sret': il.types[0] = rty = (1, 0x11 << 16)
    elif change == 'bad-index': method.index = -1
    elif change == 'not-canonical-method': il.meta.methods[0] = NS()
    elif change == 'incomplete-params': method.param_count += 1
    elif change == 'byref-param': il.types[2] = (0, 2 << 16 | 1 << 29)
    assert recover_stack_scalars(lift, method, rty, args) is args


@pytest.mark.parametrize('change', [
    'unknown', 'shared', 'bad-index', 'wrong-addr', 'generic-method',
    'generic-owner', 'nested-owner', 'value-owner', 'bad-return',
    'indirect', 'tail', 'segment'])
def test_only_canonical_ordinary_calls_can_preserve_the_zero(change):
    before = zero(15)
    before += call_at(len(before))
    state = setup(value=0, before=before, store=store(15))
    lift, method, rty, args = state
    il = lift.il
    assert check(state)
    # The producer has its own target so mutations do not invalidate consumer.
    producer = NS(**vars(method)); producer.index = 1
    il.meta.methods.append(producer)
    other_target = TARGET + 0x100
    producer.addr = other_target
    il.addr_candidates[other_target] = [('method', 1)]
    at = lift.out.block.insns[1].ip
    raw = b'\xe8' + struct.pack('<i', other_target - (at + 5))
    if change == 'unknown': il.addr_candidates.pop(other_target)
    elif change == 'shared': il.addr_candidates[other_target].append(('method', 0))
    elif change == 'bad-index': producer.index = 0
    elif change == 'wrong-addr': producer.addr += 1
    elif change == 'generic-method': producer.generic_container = 0
    elif change in ('generic-owner', 'nested-owner', 'value-owner'):
        owner = NS(**vars(il.meta.typedefs[0])); il.meta.typedefs.append(owner)
        producer.declaring = 2
        if change == 'generic-owner': owner.generic_container = 0
        elif change == 'nested-owner': owner.declaring = 0
        else: owner.is_valuetype = True
    elif change == 'bad-return': producer.return_type = -1
    elif change == 'indirect': raw = b'\xff\x10' + b'\x90' * 3
    elif change == 'tail': raw = b'\xe9' + raw[1:]
    elif change == 'segment': raw = b'\x64' + raw
    lift.out.block.insns[1] = Decoder(64, raw, ip=at).decode()
    assert recover_stack_scalars(*state) is args


@pytest.mark.parametrize('shape', ['unknown', 'pe32', 'arm64', 'bad-header',
                                  'truncated', 'bad-offset', 'elf64', 'x86',
                                  'truncated-machine', 'missing-data', 'truncated-offset'])
def test_new_register_path_keeps_win64_abi_boundaries(shape):
    from il2cpp.binary import ELF
    state = setup(value=0, before=zero(15), store=store(15))
    binary = state[0].il.bin
    assert check(state)
    if shape == 'unknown': state[0].il.bin = NS(is64=True, d=binary.d)
    elif shape == 'pe32': binary.is64 = False
    elif shape == 'arm64': binary.d = binary.d[:0x44] + b'\x64\xaa' + binary.d[0x46:]
    elif shape == 'bad-header': binary.d = b'\x00' * len(binary.d)
    elif shape == 'truncated': binary.d = b''
    elif shape == 'bad-offset':
        data = bytearray(binary.d); struct.pack_into('<I', data, 0x3c, len(data) - 2)
        binary.d = bytes(data)
    elif shape == 'elf64':
        other = ELF.__new__(ELF); other.is64 = True; other.d = b'\x7fELF' + bytes(124)
        state[0].il.bin = other
    elif shape == 'x86':
        data = bytearray(binary.d); struct.pack_into('<H', data, 0x44, 0x14c)
        binary.d = bytes(data)
    elif shape == 'truncated-machine': binary.d = binary.d[:0x45]
    elif shape == 'truncated-offset': binary.d = binary.d[:0x3e]
    else: del binary.d
    assert recover_stack_scalars(*state) is state[3]


@pytest.mark.parametrize('te', [0x03, 0x04, 0x08, 0x0a, 0x0c, 0x0d, 0x0f,
                              0x10, 0x12, 0x13, 0x15, 0x1d, 0x1e])
def test_zero_register_is_not_a_general_typed_literal(te):
    state = setup(value=0, before=zero(15), store=store(15))
    state[0].il.types[2] = (0, te << 16)
    assert recover_stack_scalars(*state) is state[3]


@pytest.mark.parametrize('instance', [False, True])
@pytest.mark.parametrize('position', [4, 5, 6, 7, 8, 9])
def test_native_abi_position_and_input_state_unchanged(instance, position):
    from il2cpp.expr import Expr
    from il2cpp.lifter.values import _ValuesMixin
    offset = 0x20 + 8 * (position - 4)
    state = setup(value=0, before=zero(15), store=store(15)[:-1] + bytes([offset]), instance=instance)
    lift, method, rty, args = state
    method.param_count = position + (0 if instance else 1)
    params = [NS(type=1) for _ in range(method.param_count - 1)] + [NS(type=2)]
    lift.il.meta.method_params = lambda m: params
    lift.il.types.append((0, 0x0c << 16)); params[0].type = 4
    lift.il.returns_sret = lambda t: False
    lift.meta = lift.il.meta; lift._class_type_subst = lambda t: t
    lift._xmm_pending = [(1 if instance else 0, Expr('1.25f', lift.il.types[4], 'float'))]
    lift._stack_arg_texts = lambda count: _ValuesMixin._stack_arg_texts(lift, count)
    lift.slot_types = {}; lift._type_hints = {}; lift._var_types = {}
    lift.stack_map = {lift.rsp_delta + offset: 'home'}
    lift.stack_values = {'home': Expr('0', None, 'int')}
    for slot in range(4, position):
        name = 'earlier_%d' % slot
        lift.stack_map[lift.rsp_delta + 0x20 + 8 * (slot - 4)] = name
        lift.stack_values[name] = Expr('9', None, 'int')
    args = ['a'] * 4 + ['9'] * (position - 4) + ['0']; previous = list(args)
    assert recover_stack_scalars(lift, method, rty, args) == args[:-1] + ['false']
    result = _ValuesMixin._positional_args(lift, args[:4], method, rty)
    assert result[-1] == 'false' and result[1 if instance else 0] == '1.25f'
    assert args == previous and lift.stack_values['home'].text == '0'
    assert not lift.slot_types and not lift._type_hints and not lift._var_types


def test_zero_register_does_not_enable_even_named_zero_enum():
    state = setup(value=0, enum=True, before=zero(15), store=store(15))
    assert recover_stack_scalars(*state) is state[3]

@pytest.mark.parametrize('after', [b'\x41\xbf\x01\x00\x00\x00',
                                  b'\x45\x33\xff', b'\x4c\x8d\x7c\x24\x40',
                                  b'\xc6\x44\x24\x21\x01'])
def test_after_store_register_clobbers_and_disjoint_writes_leave_home_intact(after):
    assert check(setup(value=0, before=zero(15), store=store(15), after=after))


@pytest.mark.parametrize('reg', [0, 1, 2, 3])
def test_full_zero_proves_high_legacy_byte_too(reg):
    raw = b'\x88' + bytes([0x44 | ((reg + 4) << 3)]) + b'\x24\x20'
    assert check(setup(value=0, before=zero(reg), store=raw))


@pytest.mark.parametrize('before', [b'\x90', b'\xe8\x00\x00\x00\x00',
                                   b'\x89\x00', b'\x41\xbf\x01\x00\x00\x00'])
def test_only_effects_after_reaching_full_zero_need_to_be_proved(before):
    assert check(setup(value=0, before=before + zero(15), store=store(15)))


def test_general_zero_copy_is_deliberately_not_chased():
    assert not check(setup(value=0, before=zero(14) + b'\x4d\x89\xf7', store=store(15)))


def test_exact_bounded_search_includes_512_but_not_513_instructions():
    neutral = bytes.fromhex('4889c9')
    assert check(setup(value=0, before=zero(15) + neutral * 510, store=store(15)))
    assert not check(setup(value=0, before=zero(15) + neutral * 511, store=store(15)))
