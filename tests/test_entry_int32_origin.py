"""Authored exact-owner/CFG/native-origin tests, with no captured game bodies."""
import struct
from types import SimpleNamespace as NS

import pytest
from iced_x86 import Decoder, Mnemonic

from il2cpp import Il2Cpp
from il2cpp.lifter.entryorigin import EntryInt32Origin
from test_native_unwind_boundary import BASE, image

MOVD = '660f6ec1'  # xmm0 <- ecx, clearing the other 96 bits
CVT = '0f5bc0'


def setup(body=MOVD + CVT + 'c3', *, parameters=(1,), static=True,
          return_type=0, size=24):
    raw = bytearray()
    for i, part in enumerate(body.split('CALL')):
        if i:
            raw.extend(b'\xe8' + struct.pack('<i', 0x300 - len(raw) - 5))
        raw.extend(bytes.fromhex(part))
    binary = image(((0x1000, 0x1400, 0x3000),),
                   text={0x1000: bytes(raw), 0x1300: b'\xc3'})
    m = NS(index=0, addr=BASE + 0x1000, name='Test', generic_container=-1,
           declaring=0, return_type=return_type, is_static=static,
           param_count=len(parameters))
    params = [NS(type=ty, name='p' + str(i)) for i, ty in enumerate(parameters)]
    il = Il2Cpp.__new__(Il2Cpp)
    il.bin = binary
    il.meta = NS(methods=[m], typedefs=[NS(index=0, generic_container=-1)],
                 method_params=lambda method: params)
    il.types = [(0, 1 << 16), (0, 8 << 16), (0, 12 << 16),
                (0, (8 << 16) | (1 << 29)), (0, 0x11 << 16),
                (0, 0x13 << 16), (0, 0x16 << 16)]
    il.type_sizes = [size]
    il.addr_candidates = {m.addr: [('method', 0)]}
    insns = tuple(Decoder(64, bytes(raw), ip=m.addr))
    lift = NS(il=il, meta=il.meta, bin=binary, _current_method=m,
              out=NS(block=NS(insns=insns)))
    conversion = next((i for i in insns if i.mnemonic == Mnemonic.CVTDQ2PS), None)
    return EntryInt32Origin(il, m, insns), lift, conversion


def result(body=MOVD + CVT + 'c3', **kwargs):
    plan, lift, conversion = setup(body, **kwargs)
    return plan.parameter_at(lift, conversion, lift.out.block.insns)


def test_direct_entry_and_different_simd_destination():
    assert result() == 0
    assert result(MOVD + '0f5bc8c3') == 0
    assert result('660f6ec9' + '0f5bc1c3') == 0


@pytest.mark.parametrize('parameters,static,sret,movd,expected', [
    ((1,), False, False, '660f6ec2', 0),
    ((1,), True, True, '660f6ec2', 0),
    ((1,), False, True, '66410f6ec0', 0),
    ((2, 1), True, False, '660f6ec2', 1),
    ((2, 1), False, False, '66410f6ec0', 1),
    ((1, 1, 1, 1), True, False, '66410f6ec1', 3),
    ((3, 1), True, False, '660f6ec2', 1),
])
def test_exact_positional_float_receiver_and_sret_slots(parameters, static, sret,
                                                       movd, expected):
    assert result(movd + CVT + 'c3', parameters=parameters, static=static,
                  return_type=4 if sret else 0) == expected


@pytest.mark.parametrize('size', [1, 2, 4, 8])
def test_exact_small_struct_return_does_not_spend_a_parameter_slot(size):
    assert result(return_type=4, size=size) == 0


@pytest.mark.parametrize('parameters', [(2,), (3,), (5,), (6,), (0,)])
def test_float_byref_open_typedreference_and_void_are_not_int32_entry(parameters):
    assert result(parameters=parameters) is None


@pytest.mark.parametrize('size', [None, 0, -1])
def test_unknown_or_invalid_struct_return_layout_declines(size):
    assert result(return_type=4, size=size) is None


def test_shared_total_budget_counts_suffix_and_distinct_native_states():
    plan, lift, conversion = setup('90' * 20 + MOVD + CVT + 'c3')
    assert plan.parameter_at(lift, conversion, lift.out.block.insns, window=22) == 0
    assert plan.parameter_at(lift, conversion, lift.out.block.insns, window=21) is None
    for budget in (0, -1, 513, None, '512'):
        assert plan.parameter_at(lift, conversion, lift.out.block.insns, budget) is None


@pytest.mark.parametrize('write', ['89d1', '31c9', '80c101', '66b90200',
                                    'b101', '4889d1', '0fb6c9', '0f44ca',
                                    '87ca', 'ffc1', '8d4901'])
def test_noncopy_partial_wide_or_conflicting_writers_decline(write):
    # A MOV32 from an unseeded RDX is not this method's parameter.
    assert result(write + MOVD + CVT + 'c3') is None


def test_only_32_bit_register_copies_preserve_entry_identity():
    assert result('89cb' + '660f6ec3' + CVT + 'c3') == 0
    assert result('4889cb' + '660f6ec3' + CVT + 'c3') is None
    assert result('89cb89de' + '660f6ec6' + CVT + 'c3') == 0
    assert result('89d1' + MOVD + CVT + 'c3', parameters=(1, 1)) == 1


@pytest.mark.parametrize('save,movd', [('89cb', '660f6ec3'), ('89ce', '660f6ec6'),
                                       ('89cf', '660f6ec7'), ('4189cc', '66410f6ec4')])
def test_nonvolatile_gpr_copies_survive_real_direct_calls(save, movd):
    assert result(save + 'CALL' + movd + CVT + 'c3') == 0


@pytest.mark.parametrize('save,movd', [('', MOVD), ('89c8', '660f6ec0'),
                                       ('4189c8', '66410f6ec0')])
def test_volatile_gpr_entry_and_copies_are_killed_by_call(save, movd):
    assert result(save + 'CALL' + movd + CVT + 'c3') is None


def test_all_predecessors_must_agree_on_the_same_parameter():
    prefix = '85c0740489cbeb02'
    assert result(prefix + '89cb' + '660f6ec3' + CVT + 'c3') == 0
    assert result(prefix + '89d3' + '660f6ec3' + CVT + 'c3',
                  parameters=(1, 1)) is None
    assert result(prefix + '31db' + '660f6ec3' + CVT + 'c3') is None


def test_one_call_arm_cannot_resurrect_a_volatile_origin():
    # jz skips the five-byte call, reaching the same conversion block.
    assert result('85c07405CALL' + MOVD + CVT + 'c3') is None
    assert result('89cb85c07405CALL' + '660f6ec3' + CVT + 'c3') == 0


def test_prefix_cycle_declines_but_an_unrelated_suffix_loop_is_allowed():
    assert result('85c07402ebfa' + MOVD + CVT + 'c3') is None
    assert result(MOVD + CVT + 'ebfe') == 0


@pytest.mark.parametrize('prefix', ['ebfe', 'c3', 'cc', '0f0b'])
def test_unreachable_conversion_is_not_entry_proven(prefix):
    assert result(prefix + MOVD + CVT + 'c3') is None


@pytest.mark.parametrize('tail', ['', '90', 'CALL', '7401', 'eb7f', 'ffe0',
                                  'ff10', 'cd29', 'cb'])
def test_missing_normal_successor_external_indirect_interrupt_and_far_return_decline(tail):
    assert result(MOVD + CVT + tail) is None


def test_same_block_must_not_hide_a_second_predecessor_into_the_suffix():
    # Conditional jump bypasses MOVD, directly entering CVTDQ2PS.
    assert result('85c07404' + MOVD + CVT + 'c3') is None


@pytest.mark.parametrize('between', ['CALL', '0f57c0', '0f28c1', 'c5f877',
                                     '0f28c8eb00'])
def test_suffix_calls_vector_writers_and_branch_boundaries_decline(between):
    assert result(MOVD + between + CVT + 'c3') is None


@pytest.mark.parametrize('producer', ['660f6e01', 'f30f7ec1', 'c5f96ec1',
                                      '660f6fc1'])
def test_memory_wide_vex_or_other_packed_producers_decline(producer):
    assert result(producer + CVT + 'c3') is None


@pytest.mark.parametrize('candidates', [[], [('method', 1)], [('spec', 0)],
                                       [('method', 0), ('method', 0)]])
def test_exact_metadata_owner_not_candidate_count(candidates):
    plan, lift, conversion = setup()
    lift.il.addr_candidates[lift._current_method.addr] = candidates
    assert plan.parameter_at(lift, conversion, lift.out.block.insns) is None


@pytest.mark.parametrize('field,value', [('index', -1), ('index', 1),
                                        ('declaring', -1), ('return_type', -1),
                                        ('return_type', 100), ('generic_container', 0),
                                        ('name', '.ctor'), ('name', '.cctor'),
                                        ('param_count', 2)])
def test_invalid_or_unsupported_method_metadata_declines(field, value):
    plan, lift, conversion = setup()
    setattr(lift._current_method, field, value)
    assert plan.parameter_at(lift, conversion, lift.out.block.insns) is None


def test_generic_owner_registered_interior_and_swapped_current_method_decline():
    for change in ('generic', 'interior', 'method', 'meta', 'binary', 'il'):
        plan, lift, conversion = setup()
        if change == 'generic':
            lift.meta.typedefs[0].generic_container = 0
        elif change == 'interior':
            lift.il.addr_candidates[conversion.ip] = [('method', 1)]
        elif change == 'method':
            lift._current_method = NS(**lift._current_method.__dict__)
        elif change == 'meta':
            lift.meta = NS(**lift.meta.__dict__)
        elif change == 'binary':
            lift.bin = image()
        else:
            lift.il = NS(**lift.il.__dict__)
        assert plan.parameter_at(lift, conversion, lift.out.block.insns) is None


def test_instruction_and_binary_mutation_after_construction_cannot_supply_new_proof():
    for change in ('ip', 'bytes', 'section'):
        plan, lift, conversion = setup()
        if change == 'ip':
            conversion.ip += 1
        elif change == 'bytes':
            lift.bin.d = lift.bin.d + b'\0'
        else:
            lift.bin.sections[0].rawsize -= 1
        assert plan.parameter_at(lift, conversion, lift.out.block.insns) is None


def test_actual_execution_block_identity_and_unmutated_native_instructions():
    plan, lift, conversion = setup()
    assert plan.parameter_at(lift, conversion, list(lift.out.block.insns)) is None
    lift.out.block.insns = (conversion,)
    assert plan.parameter_at(lift, conversion, lift.out.block.insns) is None
    lift.out = NS()
    assert plan.parameter_at(lift, conversion, ()) is None


def test_missing_leaf_unwind_and_handler_records_are_not_no_eh_proof():
    for header, rows in [(b'\x09\0\0\0', ((0x1000, 0x1400, 0x3000),)),
                         (b'\x01\0\0\0', ())]:
        _, lift, conversion = setup()
        raw = bytes.fromhex(MOVD + CVT + 'c3')
        binary = image(rows, text={0x1000: raw}, unwind={0x3000: header})
        lift.il.bin = lift.bin = binary
        plan = EntryInt32Origin(lift.il, lift._current_method, lift.out.block.insns)
        assert plan.parameter_at(lift, conversion, lift.out.block.insns) is None


def test_bounded_ingestion_and_independent_instruction_count():
    _, lift, conversion = setup()
    first = lift.out.block.insns[0]
    count = 0

    def forever():
        nonlocal count
        while True:
            count += 1
            yield first

    plan = EntryInt32Origin(lift.il, lift._current_method, forever())
    assert count == 513
    assert plan.parameter_at(lift, conversion, lift.out.block.insns) is None
    assert result('90' * 509 + MOVD + CVT + 'c3') == 0  # exactly 512 instructions
    assert result('90' * 510 + MOVD + CVT + 'c3') is None


def test_reuse_and_query_order_do_not_leak_across_binary_method_or_execution():
    plan, lift, conversion = setup()
    other, foreign, foreign_conversion = setup('89d1' + MOVD + CVT + 'c3')
    assert plan.parameter_at(foreign, foreign_conversion, foreign.out.block.insns) is None
    assert other.parameter_at(foreign, foreign_conversion, foreign.out.block.insns) is None
    for dry in (True, False, True):
        lift.dry = dry
        assert plan.parameter_at(lift, conversion, lift.out.block.insns) == 0


def test_native_proof_does_not_read_counting_regs_or_mutate_entry_exprs():
    from il2cpp import Expr

    class NoRead(dict):
        def __getitem__(self, key):
            raise AssertionError('proof counted a register use')

        def get(self, key, default=None):
            raise AssertionError('proof read a symbolic register')

    plan, lift, conversion = setup()
    original = Expr('p0', (0, 8 << 16), 'int')
    lift.regs = NoRead(RCX=original, XMM0=original)
    assert plan.parameter_at(lift, conversion, lift.out.block.insns) == 0
    assert dict.get(lift.regs, 'RCX') is original
    assert original.text == 'p0' and original.kind == 'int'


def test_malformed_contexts_decline_without_exposing_partial_proof():
    for il in (None, object()):
        plan = EntryInt32Origin(il, object(), [])
        assert plan.parameter_at(None, None, None) is None


@pytest.mark.parametrize('hidden', [
    '0fae08', '480fae08',  # FXRSTOR / FXRSTOR64: no XMM writes in used_registers
    '0fae28', '480fae28',  # XRSTOR / XRSTOR64
    '0fc718', '480fc718',  # XRSTORS / XRSTORS64
    '0f01d7',             # ENCLU may resume an unmodelled execution context
    '0f37',               # GETSEC is a context save/restore instruction
    '0f20c0', '0f0118',   # privileged control/system-state instructions
])
@pytest.mark.parametrize('position', ['prefix', 'suffix'])
def test_hidden_context_restores_and_system_effects_are_not_register_write_proofs(hidden,
                                                                                 position):
    # Ordinary instruction-info register lists are not a complete model of
    # restored machine state. Neither provenance nor the MOVD-to-CVT suffix
    # may rely on the absence of an explicit GPR/XMM destination here.
    body = (hidden + MOVD if position == 'prefix' else MOVD + hidden)
    assert result(body + CVT + 'c3') is None


@pytest.mark.parametrize('view', [False, True])
def test_mutable_binary_backing_cannot_supply_a_live_native_snapshot(view):
    _, lift, conversion = setup()
    storage = bytearray(lift.bin.d)
    lift.bin.d = memoryview(storage) if view else storage
    plan = EntryInt32Origin(lift.il, lift._current_method, lift.out.block.insns)
    assert plan.parameter_at(lift, conversion, lift.out.block.insns) is None
    section = lift.bin.sections[0]
    offset = section.offset + lift._current_method.addr - section.addr + 3
    storage[offset] ^= 3  # MOVD ecx -> edx; same data identity.
    assert plan.parameter_at(lift, conversion, lift.out.block.insns) is None
