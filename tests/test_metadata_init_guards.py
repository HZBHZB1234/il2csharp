"""Authored x64 metadata-init shapes: shared scanner and atomic declines."""
import struct
import pytest
pytest.importorskip('iced_x86')
from iced_x86 import Decoder, Mnemonic, Instruction, Code
from il2cpp.initguard import metadata_init_guards, is_init_barrier

BASE = 0x180010000
SLOT = 0x180200000
HELPER = 0x180003000


def guard(*, gap=b'', before=b'', after=b'', count=1, branch=0x85,
          close=True, flag=1, helper=HELPER, setup=True, between=b'',
          wide_compare=False, wide_store=False, prefix=b'', compare=None):
    b = bytearray(prefix)
    def rip(head, target, tail=b''):
        at=BASE+len(b);size=len(head)+4+len(tail)
        b.extend(head+struct.pack('<i',target-at-size)+tail)
    rip(compare or (b'\x83\x3d' if wide_compare else b'\x80\x3d'),
        SLOT, b'' if compare else b'\x00')
    b.extend(gap)
    j=len(b);b.extend(bytes((0x0f,branch))+b'\0'*4)
    b.extend(before)
    for i in range(count):
        if setup:rip(b'\x48\x8d\x0d',SLOT+16+i*8)
        b.extend(between)
        rip(b'\xe8',helper)
    b.extend(after)
    if close:rip(b'\xc7\x05' if wide_store else b'\xc6\x05',SLOT,
                 struct.pack('<I',flag) if wide_store else bytes((flag,)))
    target=BASE+len(b);b.extend(b'\x90\xc3')
    struct.pack_into('<i',b,j+2,target-(BASE+j+6))
    return list(Decoder(64,bytes(b),ip=BASE))


def scan(raw):return metadata_init_guards(raw,HELPER)


@pytest.mark.parametrize('count',[1,2,25,50,100])
def test_complete_body_is_target_bounded_not_sixty_four_instructions(count):
    raw=guard(count=count)
    result=scan(raw)
    assert raw[0].ip in result
    assert all(x.ip in result for x in raw if x.mnemonic in (Mnemonic.LEA,Mnemonic.CALL))
    assert raw[-2].ip not in result


@pytest.mark.parametrize('gap',[b'\x90',b'\xf3\x0f\x58\xc0',b'\x0f\xc6\xc0\x00',
                                b'\x0f\x29\x74\x24\x20',b'\x66\x48\x0f\x7e\xf7',
                                b'\x48\x63\xc0',b'\x48\x8b\xc1'])
def test_eflags_neutral_gap_runs_and_is_never_skipped(gap):
    raw=guard(gap=gap)
    skipped=scan(raw)
    assert raw[0].ip in skipped
    assert raw[1].ip not in skipped


@pytest.mark.parametrize('gap',[b'\x01\xc0',b'\x11\xc0',b'\x0f\x45\xc1',b'\x0f\x95\xc0',
                                b'\x9c',b'\x9d',b'\xeb\x00',b'\xcc',b'\xe8\0\0\0\0'])
def test_flag_consumers_writers_and_control_flow_decline(gap):
    assert scan(guard(gap=gap))==set()


@pytest.mark.parametrize('distance',[1,7,8,15,16,17])
def test_gap_runaway_bound(distance):
    raw=guard(gap=b'\x90'*(distance-1))
    assert bool(scan(raw))==(distance<=16)


@pytest.mark.parametrize('branch',[0x84,0x82,0x83,0x86,0x87,0x8c,0x8e])
def test_non_jne_branch_is_not_a_one_shot_guard(branch):
    assert scan(guard(branch=branch))==set()


@pytest.mark.parametrize('after',[b'\xf0\x83\x0c\x24\x00',b'\xf0\x48\x83\x0c\x24\x00'])
def test_barrier_is_elided_only_in_a_completed_guard(after):
    raw=guard(after=after)
    fences=[x for x in raw if is_init_barrier(x)]
    assert len(fences)==1 and fences[0].ip in scan(raw)
    assert scan(guard(after=after,close=False))==set()


@pytest.mark.parametrize('fence',[b'\x83\x0c\x24\x00',b'\xf0\x83\x4c\x24\x08\x00',
                                b'\xf0\x83\x0c\x24\x01',b'\xf0\x83\x0f\x00',
                                b'\xf0\x83\x04\x24\x00', b'\xf0\x80\x0c\x24\x00'])
def test_only_exact_zero_identity_release_fence_is_admitted(fence):
    assert not any(is_init_barrier(x) for x in guard(after=fence))
    assert scan(guard(after=fence))==set()


@pytest.mark.parametrize('change',[dict(count=0),dict(setup=False),dict(helper=HELPER+16),
                                  dict(close=False),dict(flag=0),dict(flag=2),
                                  dict(before=b'\xf0\x83\x0c\x24\x00')])
def test_missing_helper_or_unfinished_proof_never_publishes_a_partial_skip(change):
    assert scan(guard(**change))==set()


@pytest.mark.parametrize('after',[b'\x48\x89\x07',b'\x48\x8b\x07',b'\xc3',b'\x0f\x0b',
                                 b'\x75\x00',b'\xff\xd0'])
def test_non_plumbing_memory_or_control_effects_keep_native_guard(after):
    assert scan(guard(after=after))==set()


@pytest.mark.parametrize('after',[b'\x48\x89\x74\x24\x20',b'\xf3\x0f\x6f\x44\x24\x20',
                                 b'\xf3\x0f\x7f\x44\x24\x20',b'\xb8\x05\0\0\0',
                                 b'\x48\x89\xf0',b'\x48\x83\xec\x20'])
def test_unowned_body_effects_keep_their_native_condition(after):
    # With an already-set flag, native code skips these effects. Merely
    # retaining them while deleting JNE would change fast-path state.
    assert scan(guard(after=after))==set()


def test_non_contiguous_input_cannot_supply_a_missing_proof():
    raw=guard(gap=b'\x90')
    assert scan([raw[0]]+raw[2:])==set()


def test_declined_guard_does_not_poison_the_next_guard():
    first=guard(after=b'\xf0\x83\x0c\x24\x00',close=False)
    second=guard()
    result=scan(first)
    assert result==set() and scan(second)


@pytest.mark.parametrize('between',[b'\x48\x89\xc8',b'\x89\xf9',b'\x48\x8d\x0c\x24',
                                   b'\x51',b'\x48\x89\x0c\x24',b'\x48\x83\xe9\x01',
                                   b'\x66\x0f\x6e\xc1',b'\x48\x8d\x11'])
def test_metadata_arg_is_owned_by_its_exact_consumer(between):
    assert scan(guard(between=between))==set()


@pytest.mark.parametrize('index',[1,2,3,4,5])
def test_outside_branch_into_gap_or_body_declines(index):
    raw=guard(gap=b'\x90')
    jump=Instruction.create_branch(Code.JMP_REL32_64,raw[index].ip)
    jump.ip=raw[-1].ip
    raw[-1]=jump
    assert scan(raw)==set()


def test_branch_to_merge_point_is_not_an_interior_entry():
    raw=guard()
    jump=Instruction.create_branch(Code.JMP_REL32_64,raw[-2].ip)
    jump.ip=raw[-1].ip;raw[-1]=jump
    assert raw[0].ip in scan(raw)


@pytest.mark.parametrize('changes',[dict(wide_compare=True),dict(wide_store=True),
                                   dict(after=b'\x48\x89\x45\x20'),
                                   dict(after=b'\x48\x89\x04\x0c')])
def test_nonbyte_flags_and_unproved_frame_addresses_decline(changes):
    assert scan(guard(**changes))==set()


@pytest.mark.parametrize('count',[500,512])
def test_body_runaway_bound_is_a_decline_not_a_partial_skip(count):
    assert bool(scan(guard(count=count)))==(count==500)


def test_missing_runtime_helper_identity_keeps_raw_control_flow():
    assert metadata_init_guards(guard(),None)==set()
    assert metadata_init_guards([],HELPER)==set()


def test_unpaired_argument_after_last_call_keeps_its_value_and_guard():
    assert scan(guard(after=b'\x48\x8d\x0d\0\0\0\0'))==set()


@pytest.mark.parametrize('path',['structured','flat'])
@pytest.mark.parametrize('has_helper', [True, False])
def test_both_lifting_paths_delegate_to_the_shared_scanner(monkeypatch,path,has_helper):
    from types import SimpleNamespace
    from il2cpp import Decompiler,Lifter
    class ReachedScanner(Exception):
        pass
    def observed(insns,helper,entry_points=()):
        assert entry_points==()
        assert helper==(HELPER if has_helper else None) and insns
        assert insns[0].ip==BASE
        raise ReachedScanner()
    if path=='structured':
        monkeypatch.setattr('il2cpp.dec.build.metadata_init_guards',observed)
        dec=Decompiler.__new__(Decompiler)
        dec.L=SimpleNamespace(**(dict(rt_init_meta=HELPER) if has_helper else {}))
        with pytest.raises(ReachedScanner):dec._guards(guard())
    else:
        monkeypatch.setattr('il2cpp.lifter.state.metadata_init_guards',observed)
        lifter=Lifter.__new__(Lifter)
        lifter.bin=SimpleNamespace(read=lambda va,n:b'\xc3')
        lifter.il=SimpleNamespace(next_method_start=lambda va:va+1)
        lifter.asm_comments=False
        if has_helper:lifter.rt_init_meta=HELPER
        monkeypatch.setattr(lifter,'_new_regs',lambda:{})
        with pytest.raises(ReachedScanner):lifter.lift(SimpleNamespace(addr=BASE),None)


@pytest.mark.parametrize('prefix,compare', [
    (b'\x31\xc0', b'\x38\x05'),  # xor eax,eax; cmp [flag],al
    (b'\x48\x31\xc0', b'\x38\x05'),
    (b'\x30\xc0', b'\x38\x05'),
    (b'\x66\x31\xc0', b'\x38\x05'),
    (b'\x29\xc0', b'\x38\x05'),
    (b'\xb0\x00', b'\x38\x05'),
    (b'\xb8\x00\x00\x00\x00', b'\x38\x05'),
    (b'\x31\xff\x48\x89\x7c\x24\x20', b'\x40\x38\x3d'),
])
def test_register_compare_requires_a_proved_local_zero(prefix,compare):
    raw=guard(prefix=prefix,compare=compare)
    cmp=next(x for x in raw if x.mnemonic==Mnemonic.CMP)
    result=scan(raw)
    assert cmp.ip in result
    assert all(x.ip not in result for x in raw if x.ip<cmp.ip)


@pytest.mark.parametrize('prefix', [
    b'', b'\xb0\x01', b'\x31\xc0\xb0\x01', b'\x31\xc0\x0f\xa2',
    b'\x31\xc0\xf7\xe3', b'\x31\xc0\xe8\0\0\0\0',
    b'\x31\xc0\x0f\x45\xc3', b'\x31\xc0\x91',
    b'\xb4\x00', b'\x31\xc0'+b'\x90'*64,
])
def test_nonzero_clobbered_highbyte_or_unproved_register_declines(prefix):
    assert scan(guard(prefix=prefix,compare=b'\x38\x05'))==set()


@pytest.mark.parametrize('entry', ['compare','after-producer','producer'])
def test_zero_proof_cannot_cross_a_second_cfg_or_exception_entry(entry):
    raw=guard(prefix=b'\x31\xc0\x90',compare=b'\x38\x05')
    cmp=next(x for x in raw if x.mnemonic==Mnemonic.CMP)
    at={'compare':cmp.ip,'after-producer':raw[1].ip,'producer':raw[0].ip}[entry]
    result=metadata_init_guards(raw,HELPER,entry_points=[at])
    assert (cmp.ip in result)==(entry=='producer')


@pytest.mark.parametrize('index', [1,2,3,4])
def test_exception_entry_inside_guard_is_not_flattened(index):
    raw=guard(gap=b'\x90')
    assert metadata_init_guards(raw,HELPER,entry_points=[raw[index].ip])==set()


def test_direct_entry_after_zero_producer_declines():
    raw=guard(prefix=b'\x31\xc0',compare=b'\x38\x05')
    jump=Instruction.create_branch(Code.JMP_REL32_64,raw[1].ip)
    jump.ip=raw[-1].ip
    raw[-1]=jump
    assert scan(raw)==set()


def test_zero_fact_does_not_cross_a_decode_hole():
    raw=guard(prefix=b'\x31\xc0\x90',compare=b'\x38\x05')
    assert scan([raw[0]]+raw[2:])==set()


def test_conditional_return_register_effect_is_not_made_unconditional():
    # Authored counterexample: RAX=3, flag=1 -> native returns 3. Dropping
    # CMP/JNE but retaining body MOV EAX,5 would instead return 5.
    raw=guard(after=b'\xb8\x05\0\0\0')
    assert scan(raw)==set()


def test_structured_guard_scan_receives_exception_entry_points(monkeypatch):
    from types import SimpleNamespace
    from il2cpp import Decompiler
    raw=guard()
    dec=Decompiler.__new__(Decompiler)
    dec.L=SimpleNamespace(rt_init_meta=HELPER)
    dec.eh={'pads': [raw[2].ip]}
    class ReachedScanner(Exception):
        pass
    def observed(insns,helper,entry_points):
        assert insns is raw and helper==HELPER
        assert entry_points==dec.eh['pads']
        raise ReachedScanner()
    monkeypatch.setattr('il2cpp.dec.build.metadata_init_guards',observed)
    with pytest.raises(ReachedScanner):dec._guards(raw)


def test_high_byte_compare_is_not_proved_by_low_byte_zero():
    assert scan(guard(prefix=b'\x30\xc0',compare=b'\x38\x25'))==set()


def test_body_nop_is_retained_without_a_managed_effect():
    raw=guard(after=b'\x90')
    assert raw[0].ip in scan(raw) and raw[-4].ip not in scan(raw)
