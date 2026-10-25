"""fix 147: shared-body identity read from a lazy-MethodRef pointer walk.

A call site that inlines the source method's core and calls the shared
helper body passes the identity MethodInfo* through a short pointer
walk rooted at a lazy MethodRef cell. Registered candidate names at
such addresses can be mispaired (FindEntry bodies under Remove specs),
so the walk's root cell -- the runtime's own identity -- outranks them.
"""
import struct
from types import SimpleNamespace as NS

from iced_x86 import Decoder

from il2cpp import Expr, Lifter, MethodDef, ParamDef

INT = (0, 0x08 << 16)
VOID = (0, 0x01 << 16)
TARGET = 0x2000
TGT_NAME = 'List_1<int>.Add'


def walk_meta_il():
    m = MethodDef(0, 'Add', 0, 0, 0, -1, 1, 0, 0, 0, 1)
    m2 = MethodDef(1, 'Bogus', 1, 0, 0, -1, 1, 0, 0, 0, 1)
    meta = NS(
        methods=[m, m2],
        typedefs=[NS(name='Dictionary_2',
                     namespace='System.Collections.Generic',
                     is_valuetype=False)],
        method_params=lambda mm: [ParamDef('key', 0, 1)],
    )
    il = NS(
        meta=meta,
        types=[VOID, INT],
        addr_candidates={TARGET: [('generic', 0), ('generic', 1)]},
        addr_to_method={},
        method_specs=[(0, 0, -1), (1, 0, -1)],
        generic_method_name=lambda si: TGT_NAME if si == 0 else 'Other.Bogus',
        candidate_return_type=lambda c: VOID,
        _method_spec_type_args=lambda ci: (INT,),
        returns_sret=lambda ty: False,
        _type_enum=lambda ty: ((ty[1] >> 16) & 0xFF) if ty else None,
        function_extent=lambda va: (va, va + 16),
        bin=NS(exports={}, valid_va=lambda va: False),
    )
    return meta, il


def make_lifter():
    meta, il = walk_meta_il()
    lift = Lifter.__new__(Lifter)
    lift.il, lift.meta = il, meta
    lift.bin = NS(is_exec_va=lambda va: va == TARGET, exports={},
                  read=lambda va, n: b'\xcc' * n)
    walk = Expr('*(*(metadata + 0xC0) + 0x70)', None, 'ptr')
    walk._usg_root = 0
    lift.regs = {
        'RCX': Expr('t8', None, 'obj'),
        'RDX': Expr('t9', None, 'int'),
        'R8': walk,
    }
    lift.out = []
    lift.dry = False
    lift.asm_comments = False
    lift.rt_names = {}
    lift.rt_init_meta = None
    lift.rt_alloc = None
    lift.rt_arrnew = set()
    lift.rt_wbarrier = set()
    lift.rt_iface = {}
    lift.rt_isinst = set()
    lift.rt_interlocked = set()
    lift.rt_sqrt = None
    lift.rt_await_funcs = {}
    lift.rethrow_va = None
    lift.raise_va = None
    lift.eh_helper_set = {}
    lift._thunk_cache = {}
    lift._twin_cache = {}
    lift._cast_narrow = None
    lift._cls_init_export = None
    lift._cls_init_cache = {}
    lift.cur_va = 0x1000
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


def call_insn(target=TARGET, ip=0x1000):
    return Decoder(64, b'\xe8' + struct.pack('<i', target - (ip + 5)),
                   ip=ip).decode()


def test_expr_usg_root_slot_defaults_to_none():
    e = Expr('x', None, 'obj')
    assert e._usg_root is None
    e._usg_root = 5
    assert e._usg_root == 5


def test_walk_identity_picks_the_single_root():
    lift = make_lifter()
    exprs = list(lift.regs.values())
    assert lift._usg_walk_identity(
        [('generic', 0), ('generic', 1)], exprs) == (2, 0)


def test_walk_identity_declines_two_distinct_roots():
    lift = make_lifter()
    second = Expr('*(*(m + 0x20) + 0x8)', None, 'ptr')
    second._usg_root = 1
    exprs = [lift.regs['RCX'], lift.regs['RDX'], lift.regs['R8'], second]
    assert lift._usg_walk_identity(
        [('generic', 0), ('generic', 1)], exprs) is None


def test_walk_identity_declines_without_a_root():
    lift = make_lifter()
    exprs = [lift.regs['RCX'], lift.regs['RDX'], Expr('x', None, 'ptr')]
    assert lift._usg_walk_identity(
        [('generic', 0), ('generic', 1)], exprs) is None
    assert lift._usg_walk_identity(
        [('generic', 0), ('generic', 1)],
        [lift.regs['RCX'], None, None]) is None


def test_call_seats_walk_identity_and_drops_the_plumbing_arg():
    lift = make_lifter()
    ins = call_insn()
    lift._insn(ins, [ins], 0, None, ins.next_ip)
    assert lift.out == [(0x1000, 't8.Add(t9);', None)]


def test_call_keeps_honest_fallback_without_shared_candidates():
    lift = make_lifter()
    lift.il.addr_candidates = {}
    ins = call_insn()
    lift._insn(ins, [ins], 0, None, ins.next_ip)
    assert len(lift.out) == 1
    assert 'TryGetValue' not in lift.out[0][1]
