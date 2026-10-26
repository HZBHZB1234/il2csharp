"""fix 156: the icall resolver is found on this fixture again.

`scan_icall_cache` pinned the fill tail to the bare
`lea rcx,[sig]; call resolve; mov [cell],rax` layout. The v39 fixture
always interleaves the null guard (`test rax,rax; je +N`) between the
call and the cached store, and sometimes a spill (`mov r10,rax`) before
the guard, so the scan found nothing, `rt_icall_resolve` stayed unset,
and every eager resolve site (~12k tree-wide) rendered as an
unannotated `sub_1807a5bf0(&"sig", ...)` with the invoke's arguments
merged in. The scan now walks the tail (spill?, guard?, store) and the
helper vote counts signature-valid fills only, so same-shaped lazy
caches whose first argument is a bare name cannot win.

The resolve call itself renders nothing: `_call`'s early arm reads the
signature from RCX uncounted (the old post-argument arm use-bound the
feeding lea into a dead `objN = &"sig"` temp -- CS0214 at every detour
site) and seats the annotated fptr in RAX for the guarded invoke.
"""
import struct
from types import SimpleNamespace as NS

from iced_x86 import Decoder, OpKind

from il2cpp import Expr, Lifter, MethodDef

SEC = 0x4000
HELPER = 0x5000
SIGS = {0x6000: b'UnityEngine.Transform::get_position_Injected(\0'}
CELLS = {}


def _section(code):
    return [NS(addr=SEC, size=len(code), rawsize=len(code),
               is_exec=True, is_bss=False)]


def _bin(code):
    return NS(sections=_section(code),
              read=lambda va, n: code if va == SEC else None,
              cstr=lambda va, n: SIGS.get(va, CELLS.get(va, b'')).rstrip(b'\0').decode('latin-1'))


def _il():
    from il2cpp.runtime.fields import _FieldsMixin

    class _Host(_FieldsMixin):
        pass

    il = _Host()
    il.rt_icall_resolve = None
    il.icall_cells = {}
    il._icall_annotation = (
        lambda s: {'kind': 3, 'method': 7, 'icall': True, 'text': 'A.B.C'}
        if '::' in s else None)
    return il


def scan(code, sigs=SIGS, cells=CELLS):
    global SIGS, CELLS
    old_s, old_c = SIGS, CELLS
    SIGS, CELLS = sigs, cells
    try:
        il = _il()
        il.bin = _bin(code)
        il.scan_icall_cache()
        return il
    finally:
        SIGS, CELLS = old_s, old_c


def rel32(src_end, dst):
    return struct.pack('<i', dst - src_end)


# --------------------------------------------------------------- shapes

def test_guarded_fill_is_found():
    code = bytearray(b'\xcc' * 8)
    p = len(code)
    code += (b'\x48\x8d\x0d' + rel32(SEC + p + 7, 0x6000)        # lea rcx,[sig]
             + b'\xe8' + rel32(SEC + p + 12, HELPER)              # call resolve
             + b'\x48\x85\xc0'                              # test rax,rax
             + b'\x74\x02'                                  # je +2 (over store)
             + b'\x48\x89\x05' + rel32(SEC + p + 24, 0x7000)      # mov [cell],rax
             + b'\xcc' * 4)
    il = scan(bytes(code))
    assert il.rt_icall_resolve == HELPER
    assert il.icall_cells == {0x7000: 'UnityEngine.Transform::get_position_Injected('}


def test_tight_fill_still_maps():
    code = bytearray(b'\xcc' * 8)
    p = len(code)
    code += (b'\x48\x8d\x0d' + rel32(SEC + p + 7, 0x6000)
             + b'\xe8' + rel32(SEC + p + 12, HELPER)
             + b'\x48\x89\x05' + rel32(SEC + p + 19, 0x7001)
             + b'\xcc' * 8)
    il = scan(bytes(code))
    assert il.rt_icall_resolve == HELPER
    assert il.icall_cells == {0x7001: 'UnityEngine.Transform::get_position_Injected('}


def test_spill_and_rel32_guard_variant():
    code = bytearray(b'\xcc' * 8)
    p = len(code)
    # call, mov r10,rax, test rax,rax, je rel32 (+6 over the 7-byte store)
    code += (b'\x48\x8d\x0d' + rel32(SEC + p + 7, 0x6000)
             + b'\xe8' + rel32(SEC + p + 12, HELPER)
             + b'\x4c\x8b\xd0'
             + b'\x48\x85\xc0'
             + b'\x0f\x84' + rel32(SEC + p + 27, SEC + p + 27)
             + b'\x48\x89\x05' + rel32(SEC + p + 31, 0x7002)
             + b'\xcc' * 4)
    il = scan(bytes(code))
    assert il.rt_icall_resolve == HELPER
    assert il.icall_cells == {0x7002: 'UnityEngine.Transform::get_position_Injected('}


def test_vote_is_gated_on_signature_validity():
    """A same-shaped lazy cache whose first argument is a bare class name
    (no `::`) outnumbers the icall fills -- the raw-count vote of the old
    scan would have crowned it and poisoned every annotation."""
    sigs = {0x6000: b'UnityEngine.Transform::get_position_Injected(\0'}
    cells = {0x6100: b'MonoType\0'}
    code = bytearray(b'\xcc' * 8)
    p = len(code)
    code += (b'\x48\x8d\x0d' + rel32(SEC + p + 7, 0x6000)
             + b'\xe8' + rel32(SEC + p + 12, HELPER)
             + b'\x48\x85\xc0' + b'\x74\x02'
             + b'\x48\x89\x05' + rel32(SEC + p + 24, 0x7000)
             + b'\xcc' * 2)
    for _ in range(5):
        p2 = len(code)
        code += (b'\x48\x8d\x0d' + rel32(SEC + p2 + 7, 0x6100)
                 + b'\xe8' + rel32(SEC + p2 + 12, 0x9000)
                 + b'\x48\x85\xc0' + b'\x74\x02'
                 + b'\x48\x89\x05' + rel32(SEC + p2 + 24, 0x7100)
                 + b'\xcc' * 2)
    il = scan(bytes(code), sigs=sigs, cells=cells)
    assert il.rt_icall_resolve == HELPER
    assert il.icall_cells == {0x7000: 'UnityEngine.Transform::get_position_Injected('}


def test_other_target_cells_are_not_mapped():
    code = bytearray(b'\xcc' * 8)
    p = len(code)
    code += (b'\x48\x8d\x0d' + rel32(SEC + p + 7, 0x6000)
             + b'\xe8' + rel32(SEC + p + 12, 0x9000)       # NOT the winner
             + b'\x48\x85\xc0' + b'\x74\x02'
             + b'\x48\x89\x05' + rel32(SEC + p + 24, 0x7003)
             + b'\xcc' * 4)
    il = scan(bytes(code))
    # the winner is 0x9000 (the only sig-valid fills); HELPER fills none
    assert il.rt_icall_resolve == 0x9000
    assert il.icall_cells == {0x7003: 'UnityEngine.Transform::get_position_Injected('}


# ------------------------------------------------------------ early arm

def make_lifter():
    lift = Lifter.__new__(Lifter)
    lift.meta = NS(
        methods=[MethodDef(0, 'f', 0, 0, 0, -1, 0, 0, 0, 0, 0)],
        typedefs=[NS(name='X', namespace='', is_valuetype=False)],
        method_params=lambda m: [],
    )
    lift.il = NS(
        meta=lift.meta,
        types=[],
        addr_candidates={},
        addr_to_method={},
        rt_icall_resolve=HELPER,
        _icall_annotation=lambda s: {'kind': 3, 'method': 7, 'icall': True,
                                     'text': 'A.B.C'} if '::' in s else None,
        bin=NS(cstr=lambda va, n: 'A.B::C()', exports={}),
    )
    lift.bin = NS(cstr=lambda va, n: 'A.B::C()', exports={},
                  is_exec_va=lambda va: True, read=lambda va, n: b'\xcc' * n)
    for attr in ('rt_alloc', 'rt_value_box', 'rt_names'):
        setattr(lift, attr, None if attr != 'rt_names' else {})
    lift.rt_allocs = set()
    lift.rt_arrnew = set()
    lift.rt_wbarrier = set()
    lift.rt_iface = {}
    lift.rt_isinst = set()
    lift.rt_interlocked = set()
    lift.rt_sqrt = None
    lift.rt_init_meta = None
    lift.rt_await_funcs = {}
    lift.rethrow_va = None
    lift.raise_va = None
    lift.eh_helper_set = {}
    lift._thunk_cache = {}
    lift._twin_cache = {}
    lift._cast_narrow = None
    lift._cls_init_export = None
    lift._cls_init_cache = {}
    lift.regs = {
        'RCX': Expr('&"A.B::C()"', None, 'ptr'),
        'RDX': Expr('num2', (0, 0x08 << 16), 'int'),
    }
    lift.out = []
    lift.dry = False
    lift.asm_comments = False
    lift.cur_va = 0x900
    lift._current_method = NS(return_type=0)
    lift._type_hints = {}
    lift.slot_types = {}
    lift._call_class_args = None
    lift._xmm_pending = []
    lift.vt_recv_slot = None
    lift.vt_recv = None
    lift.flags = None
    lift._cur_ip = 0
    lift.var_n = 0
    lift.rsp_delta = 0
    lift._unk_n = 0
    return lift


def call_insn(target=HELPER, ip=0x900):
    return Decoder(64, b'\xe8' + struct.pack('<i', target - (ip + 5)),
                   ip=ip).decode()


def test_resolve_renders_nothing_and_seats_the_fptr():
    lift = make_lifter()
    ins = call_insn()
    lift._insn(ins, [ins], 0, None, ins.next_ip)
    assert lift.out == []
    rax = lift.regs['RAX']
    assert rax.text == 'A.B.C'
    assert rax.kind == 'fptr'
    assert rax._mi == 7
    # the resolve consumed its argument register: RCX is a clobbered
    # fresh unknown, not the signature pointer the invoke would re-read
    assert lift.regs['RCX']._unk is True


def test_resolve_keeps_an_already_annotated_rax():
    """The guard load put the cell's fptr in RAX; the resolve returns the
    same pointer, so the lift keeps the SAME Expr and the guarded invoke
    merges to one lane instead of a fresh phi value."""
    lift = make_lifter()
    held = Expr('A.B.C', None, 'fptr')
    held._mi = 7
    lift.regs['RAX'] = held
    ins = call_insn()
    lift._insn(ins, [ins], 0, None, ins.next_ip)
    assert lift.regs['RAX'] is held


def test_unresolved_signature_declines():
    lift = make_lifter()
    lift.il = NS(**dict(lift.il.__dict__))
    lift.il._icall_annotation = lambda s: None
    lift.il.returns_sret = lambda ty: False
    lift.il.candidate_return_type = lambda c: None
    ins = call_insn()
    lift._insn(ins, [ins], 0, None, ins.next_ip)
    # falls through to the ordinary call path (the honest sub_ render)
    assert any('sub_%x' % HELPER in (l[1] or '') for l in lift.out)
