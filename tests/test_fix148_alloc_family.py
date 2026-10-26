"""fix 148: the object-alloc helper family, not just its first member.

IL2CPP's allocator has more than one entry point in this fixture: the
plain `il2cpp_object_new` (0x1807933d0, 5,764 klass sites) and a
class-init wrapper around the same allocator (0x1807e3d20, 1,226 klass
sites). The classifier kept only whichever sorted first, so the second
rendered as `sub_1807e3d20(typeof(T))` -- an untyped `object` that
blocked every downstream fold: 5,845 delegate-construction sites kept
`sub_1811cce50(obj, target, handler)` instead of
`new Action(target, handler)`, and inlined `List<T>.Add` fast paths
kept raw pointer arithmetic instead of `_size`/`_items`.

`rt_allocs` is the complete klass-argument family; `rt_alloc` keeps the
first-seen address for the consumers that only need one.
"""
import struct
from types import SimpleNamespace as NS

from iced_x86 import Decoder

from il2cpp import Expr, Lifter, MethodDef

KLASS = (7, (0x12 << 16))
FIRST = 0x1000
SECOND = 0x2000


def make_lifter():
    lift = Lifter.__new__(Lifter)
    lift.meta = NS(
        methods=[MethodDef(0, 'm', 0, 0, 0, -1, 0, 0, 0, 0, 0)],
        typedefs=[NS(name='Action', namespace='System', is_valuetype=False)],
    )
    lift.il = NS(
        types=[KLASS],
        type_name=lambda ty: 'System.Action',
        addr_candidates={},
        addr_to_method={},
        function_extent=lambda va: (va, va + 16),
        _type_enum=lambda ty: ((ty[1] >> 16) & 0xFF) if ty else None,
        returns_sret=lambda ty: False,
        candidate_return_type=lambda c: None,
        bin=NS(exports={}, valid_va=lambda va: False),
    )
    lift.bin = NS(exports={}, is_exec_va=lambda va: True,
                  read=lambda va, n: b'\xcc' * n)
    lift.rt_alloc = FIRST
    lift.rt_allocs = {FIRST, SECOND}
    lift.rt_arrnew = set()
    lift.rt_wbarrier = set()
    lift.rt_iface = {}
    lift.rt_isinst = set()
    lift.rt_interlocked = set()
    lift.rt_sqrt = None
    lift.rt_names = {}
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
    lift.regs = {'RCX': Expr('typeof(System.Action)', KLASS, 'klass')}
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


def call_insn(target, ip=0x900):
    return Decoder(64, b'\xe8' + struct.pack('<i', target - (ip + 5)),
                   ip=ip).decode()


def test_first_alloc_member_folds_to_new():
    lift = make_lifter()
    ins = call_insn(FIRST)
    lift._insn(ins, [ins], 0, None, ins.next_ip)
    assert lift.regs['RAX'].text == 'new System.Action()'


def test_second_family_member_folds_the_same_way():
    """The class-init wrapper allocates too: it must not stay `sub_`."""
    lift = make_lifter()
    ins = call_insn(SECOND)
    lift._insn(ins, [ins], 0, None, ins.next_ip)
    assert lift.regs['RAX'].text == 'new System.Action()'


def test_non_family_helper_keeps_the_honest_fallback():
    lift = make_lifter()
    ins = call_insn(0x3000)
    lift._insn(ins, [ins], 0, None, ins.next_ip)
    assert 'new System.Action' not in (lift.regs['RAX'].text or '')
