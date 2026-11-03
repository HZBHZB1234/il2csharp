"""Original synthetic Win64 loops; no game instructions or bodies stored here."""
import struct
from types import SimpleNamespace as NS

import pytest
from iced_x86 import (BlockEncoder, Code, Decoder, Instruction as I,
                      MemoryOperand as Mem, Register as R, RegisterExt)

from il2cpp.binary import PE
from il2cpp.dec.stringfold import lift_u32_string_fold

UINT, STRING, CHAR, INT = [(0, k << 16) for k in (9, 14, 3, 8)]
BASE, GETTER = 0x120000, 0x160000


def synthetic_loop(seed=0xdef01234, multiplier=0xf1234567,
                   index=R.R12, receiver=R.R14, accumulator=R.EBP,
                   frame=0x40, index_home=24, accum_entry_home=8, short_multiplier=False):
    """Assemble an independently parameterized code-unit fold from instructions."""
    idx = RegisterExt.full_register32(index)
    acc = RegisterExt.full_register(accumulator)
    home = frame + 8 + accum_entry_home
    rr = I.create_reg_reg
    stack = lambda d: Mem(R.RSP, displ=d)
    target = lambda pos: BASE + 16 * pos
    raw = [
        I.create_mem_reg(Code.MOV_RM64_R64, stack(index_home), index),
        I.create_reg(Code.PUSH_R64, receiver),
        I.create_reg_i32(Code.SUB_RM64_IMM32, R.RSP, frame),
        rr(Code.XOR_RM32_R32, idx, idx),
        rr(Code.MOV_RM64_R64, receiver, R.RCX),
        rr(Code.MOV_RM32_R32, R.EAX, idx),
        rr(Code.TEST_RM64_R64, R.RCX, R.RCX),
        I.create_branch(Code.JE_REL32_64, target(24)),
        I.create_mem_reg(Code.MOV_RM64_R64, stack(home), acc),
        I.create_reg_u32(Code.MOV_R32_IMM32, accumulator, seed),
        I.create_reg_mem(Code.CMP_R32_RM32, R.EAX, Mem(receiver, displ=0x10)),
        I.create_branch(Code.JGE_REL32_64, target(22)),
        rr(Code.XOR_RM32_R32, R.R8D, R.R8D),
        rr(Code.MOV_RM32_R32, R.EDX, idx),
        rr(Code.MOV_RM64_R64, R.RCX, receiver),
        I.create_branch(Code.CALL_REL32_64, GETTER),
        rr(Code.MOVZX_R32_RM16, R.EAX, R.AX),
        rr(Code.XOR_RM32_R32, R.EAX, accumulator),
        I.create_reg_reg_i32(Code.IMUL_R32_RM32_IMM8 if short_multiplier
                            else Code.IMUL_R32_RM32_IMM32, accumulator, R.EAX,
                            multiplier if multiplier < 0x80000000 else multiplier - (1 << 32)),
        I.create_reg(Code.INC_RM32, idx),
        rr(Code.MOV_RM32_R32, R.EAX, idx),
        I.create_branch(Code.JMP_REL32_64, target(10)),
        rr(Code.MOV_RM32_R32, R.EAX, accumulator),
        I.create_reg_mem(Code.MOV_R64_RM64, acc, stack(home)),
        I.create_reg_mem(Code.MOV_R64_RM64, index, stack(index_home + frame + 8)),
        I.create_reg_i32(Code.ADD_RM64_IMM32, R.RSP, frame),
        I.create_reg(Code.POP_R64, receiver),
        I.create(Code.RETNQ),
    ]
    for pos, ins in enumerate(raw):
        ins.ip = target(pos)
    enc = BlockEncoder(64)
    enc.add_many(raw)
    return list(Decoder(64, enc.encode(BASE), ip=BASE))


def fixture(**native):
    binary = PE.__new__(PE)
    header = bytearray(128)
    struct.pack_into('<I', header, 0x3c, 64)
    header[64:68] = b'PE\0\0'
    struct.pack_into('<H', header, 68, 0x8664)
    binary.d, binary.is64 = bytes(header), True
    getter = NS(name='get_Chars', addr=GETTER, declaring=0, return_type=2,
                is_static=False, generic_container=-1, param_count=1,
                image=0, params=[NS(name='index', type=3)])
    method = NS(name='UnrelatedName', addr=BASE, declaring=1, return_type=0,
                is_static=True, generic_container=-1, param_count=1,
                params=[NS(name='text', type=1)])
    owner = NS(name='String', namespace='System', declaring=-1,
               generic_container=-1)
    td = NS(name='UnrelatedOwner', generic_container=-1)
    meta = NS(methods=[getter, method], typedefs=[owner, td],
              images=[NS(name='mscorlib.dll')], method_params=lambda m: m.params)
    il = NS(bin=binary, types=[UINT, STRING, CHAR, INT], meta=meta,
            addr_candidates={GETTER: [('method', 0)]})
    return il, method, td, synthetic_loop(**native)


def fold(case, **kw):
    return lift_u32_string_fold(*case, **kw)


def test_recovers_complete_loop_without_a_method_name_or_hash_constant():
    text = '\n'.join(fold(fixture()))
    assert 'if (text == null)' in text and 'return 0u;' in text
    assert 'uint hash = 3740275252u;' in text
    assert 'int index = 0; index < text.Length; index++' in text
    assert 'hash = unchecked((hash ^ text[index]) * 4045620583u);' in text
    assert text.endswith('return hash;')
    assert not any(x in text for x in ('char ', 'unsafe', 'sub_', 'default'))


@pytest.mark.parametrize('seed,multiplier', [(0, 0), (1, 1), (0xffffffff, 0xffffffff),
                                            (0x80000000, 0x80000000), (19, 167)])
def test_constants_are_extracted_as_uint32_not_algorithm_fingerprints(seed, multiplier):
    text = '\n'.join(fold(fixture(seed=seed, multiplier=multiplier)))
    assert f'uint hash = {seed}u;' in text
    assert f'* {multiplier}u)' in text


@pytest.mark.parametrize('index,receiver,accumulator', [
    (R.R13, R.R15, R.EBX), (R.RBP, R.RSI, R.R12D), (R.RDI, R.RBX, R.R14D)])
def test_distinct_nonvolatile_register_allocations(index, receiver, accumulator):
    assert fold(fixture(index=index, receiver=receiver, accumulator=accumulator))


@pytest.mark.parametrize('name', ['hash', 'index', 'class', 'text'])
def test_local_identifiers_cannot_shadow_the_metadata_parameter(name):
    case = fixture()
    case[1].params[0].name = name
    text = '\n'.join(fold(case))
    parameter = name + '_' if name == 'class' else name
    assert f'{parameter}.Length' in text
    assert f'uint {parameter} =' not in text
    assert f'int {parameter} =' not in text


@pytest.mark.parametrize('position', range(28))
def test_every_reachable_instruction_is_required(position):
    case = fixture()
    case[3][position].code = Code.NOPD
    assert fold(case) is None


@pytest.mark.parametrize('position', [7, 11, 21])
def test_every_cfg_target_is_required(position):
    case = fixture()
    case[3][position].near_branch64 += 1
    assert fold(case) is None


@pytest.mark.parametrize('position,code', [(7, Code.JNE_REL8_64),
                                        (11, Code.JAE_REL8_64)])
def test_null_arm_and_signed_loop_exit_must_not_change(position, code):
    case = fixture()
    case[3][position].code = code
    assert fold(case) is None


@pytest.mark.parametrize('position,register', [(5, R.R14D), (13, R.R14D),
                                             (14, R.R12), (17, R.R12D),
                                             (18, R.R12D), (20, R.R14D),
                                             (22, R.R12D), (26, R.R12)])
def test_register_dataflow_must_match(position, register):
    case = fixture()
    if position == 26:
        case[3][position].op0_register = register
    else:
        case[3][position].op1_register = register
    assert fold(case) is None


@pytest.mark.parametrize('position', [0, 8, 10, 23, 24])
def test_native_memory_offsets_are_not_ignored(position):
    case = fixture()
    case[3][position].memory_displacement += 8
    assert fold(case) is None


@pytest.mark.parametrize('position,code', [(10, Code.CMP_R64_RM64),
                                        (16, Code.MOVSX_R32_RM16),
                                        (18, Code.IMUL_R64_RM64_IMM32),
                                        (19, Code.INC_RM64), (27, Code.RETNQ_IMM16)])
def test_width_extension_and_return_adjustment_are_not_erased(position, code):
    case = fixture()
    case[3][position].code = code
    assert fold(case) is None


@pytest.mark.parametrize('prefix', ['has_lock_prefix', 'has_rep_prefix',
                                    'has_repne_prefix', 'segment_prefix'])
def test_prefixed_instructions_decline(prefix):
    case = fixture()
    setattr(case[3][10], prefix, R.FS if prefix == 'segment_prefix' else True)
    assert fold(case) is None


@pytest.mark.parametrize('kw', [{'skip': {BASE}}, {'eh': {'pads': [BASE]}}])
def test_elided_guards_or_eh_decline(kw):
    assert fold(fixture(), **kw) is None


@pytest.mark.parametrize('change', ['extra', 'missing', 'gap', 'entry', 'call'])
def test_unaccounted_native_control_flow_or_effects_decline(change):
    case = fixture()
    if change == 'extra':
        case[3].insert(18, I.create(Code.NOPD))
    elif change == 'missing':
        case[3].pop(18)
    elif change == 'gap':
        case[3][18].ip += 1
    elif change == 'entry':
        case[1].addr += 1
    else:
        case[3][15].near_branch64 += 16
    assert fold(case) is None


@pytest.mark.parametrize('kind', ['absent', 'shared', 'generic', 'negative', 'bad_index'])
def test_exact_getter_identity_not_address_majority(kind):
    case = fixture()
    candidates = {'absent': [], 'shared': [('method', 0), ('method', 0)],
                  'generic': [('generic', 0)], 'negative': [('method', -1)],
                  'bad_index': [('method', 999)]}
    case[0].addr_candidates[GETTER] = candidates[kind]
    assert fold(case) is None


@pytest.mark.parametrize('which,attribute,value', [
    ('method', 'is_static', False), ('method', 'generic_container', 0),
    ('method', 'param_count', 2), ('method', 'return_type', 3),
    ('getter', 'name', 'ReadChar'), ('getter', 'addr', GETTER + 1),
    ('getter', 'is_static', True), ('getter', 'generic_container', 0),
    ('getter', 'param_count', 2), ('getter', 'return_type', 3),
    ('owner', 'namespace', 'User'), ('owner', 'name', 'StringLike'),
    ('owner', 'generic_container', 0), ('owner', 'declaring', 0),
    ('td', 'generic_container', 0), ('image', 'name', 'User.dll')])
def test_signature_and_core_library_owner_are_proven(which, attribute, value):
    case = fixture()
    il, method, td, _ = case
    obj = {'method': method, 'getter': il.meta.methods[0],
           'owner': il.meta.typedefs[0], 'td': td, 'image': il.meta.images[0]}[which]
    setattr(obj, attribute, value)
    assert fold(case) is None


@pytest.mark.parametrize('index,kind', [(0, 8), (1, 18), (2, 7), (3, 9)])
def test_primitive_type_codes_must_match(index, kind):
    case = fixture()
    case[0].types[index] = (0, kind << 16)
    assert fold(case) is None


@pytest.mark.parametrize('index', range(4))
def test_byref_inputs_results_and_getter_signature_decline(index):
    case = fixture()
    ty = case[0].types[index]
    case[0].types[index] = (ty[0], ty[1] | (1 << 29))
    assert fold(case) is None


@pytest.mark.parametrize('change', ['elf', 'x86', 'arm64', 'bad_header', 'truncated'])
def test_win64_lowering_cannot_be_used_with_other_abis(change):
    case = fixture()
    binary = case[0].bin
    if change == 'elf':
        case[0].bin = NS(is64=True, d=binary.d)
    elif change == 'x86':
        binary.is64 = False
    elif change == 'truncated':
        binary.d = b''
    else:
        header = bytearray(binary.d)
        if change == 'arm64':
            struct.pack_into('<H', header, 68, 0xaa64)
        else:
            header[64:68] = b'FAKE'
        binary.d = bytes(header)
    assert fold(case) is None


@pytest.mark.parametrize('native', [
    {'index': R.RAX}, {'receiver': R.RCX}, {'accumulator': R.EAX},
    {'index': R.RBP}, {'frame': 0x18}, {'frame': 0x21},
    {'index_home': 0}, {'index_home': 40}, {'accum_entry_home': 24},
    {'accum_entry_home': 0}, {'accum_entry_home': 40}])
def test_abi_save_restore_liveness_and_home_slots_are_closed(native):
    assert fold(fixture(**native)) is None


@pytest.mark.parametrize('multiplier', [-128, -1, 0, 127])
def test_sign_extended_imul_immediate_is_preserved_modulo_32_bits(multiplier):
    case = fixture(multiplier=multiplier & 0xffffffff, short_multiplier=True)
    text = '\n'.join(fold(case))
    assert f'* {multiplier & 0xffffffff}u)' in text


@pytest.mark.parametrize('position', [0, 8, 10, 23, 24])
def test_indexed_native_memory_access_is_not_a_save_or_length_read(position):
    case = fixture()
    case[3][position].memory_index = R.RAX
    assert fold(case) is None


def test_a_second_recovery_does_not_depend_on_the_previous_method():
    first = fixture(seed=19, multiplier=167)
    second = fixture(seed=37, multiplier=5)
    expected = fold(first)
    assert fold(second) != expected
    assert fold(first) == expected


def test_failed_proof_does_not_modify_instructions_or_metadata():
    case = fixture()
    case[0].addr_candidates[GETTER].append(('method', 0))
    native = [str(i) for i in case[3]]
    assert fold(case) is None
    assert [str(i) for i in case[3]] == native
    case[0].addr_candidates[GETTER].pop()
    assert fold(case) is not None


def test_builtin_string_type_must_identify_the_getter_declaring_type():
    case = fixture()
    case[0].types[1] = (999, STRING[1])
    assert fold(case) is None


@pytest.mark.parametrize('frame,index_home,accum_entry_home', [
    (0x20, 8, 16), (0x60, 32, 24), (0x100, 16, 32)])
def test_other_balanced_frames_and_disjoint_caller_homes(frame, index_home, accum_entry_home):
    assert fold(fixture(frame=frame, index_home=index_home,
                        accum_entry_home=accum_entry_home)) is not None
