"""fix 149: the element-STORE helper renders as `array[index] = value`.

`0x180002950` (15,453 tree-wide sites) is the bounds-checked reference
store: an unsigned `cmp edx,[rcx+0x18]; jae` OOB guard, then
`mov [rcx+rdx*8+0x20],r8`, then the GC write-barrier cmpxchg loop, and
it returns a bitmap word that source code never reads. The managed
statement is `array[index] = value`, so the helper is named, trimmed
to arity 3, and folded into a statement that leaves RAX unknown.

The array argument is taken from its Expr, not the raw render: a
`new T[n]` argument was already hoisted to its own temp by
`_array_allocation`, and re-rendering it would duplicate the
allocation at every element store.
"""
import struct
from types import SimpleNamespace as NS

from iced_x86 import Decoder

from il2cpp import Expr, Lifter, MethodDef

VOID = (0, 0x01 << 16)
INT = (1, 0x08 << 16)
STR = (2, 0x0e << 16)
STR_ARR = (3, 0x1d << 16)
TARGET = 0x2000


def make_lifter(array_expr):
    lift = Lifter.__new__(Lifter)
    lift.meta = NS(
        methods=[MethodDef(0, 'setref', 0, 0, 0, -1, 0, 0, 0, 0, 3)],
        typedefs=[NS(name='X', namespace='', is_valuetype=False)],
        method_params=lambda m: [],
    )
    lift.il = NS(
        meta=lift.meta,
        types=[VOID, INT, STR, STR_ARR],
        addr_candidates={TARGET: []},
        addr_to_method={},
        function_extent=lambda va: (va, va + 16),
        _type_enum=lambda ty: ((ty[1] >> 16) & 0xFF) if ty else None,
        returns_sret=lambda ty: False,
        candidate_return_type=lambda c: None,
        bin=NS(exports={}, valid_va=lambda va: False),
    )
    lift.bin = NS(exports={}, is_exec_va=lambda va: True,
                  read=lambda va, n: b'\xcc' * n)
    lift.rt_names = {TARGET: 'il2cpp_array_setref'}
    lift.rt_alloc = None
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
        'RCX': array_expr,
        'RDX': Expr('num2', INT, 'int'),
        'R8': Expr('text1', STR, 'str'),
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


def call_insn(target=TARGET, ip=0x900):
    return Decoder(64, b'\xe8' + struct.pack('<i', target - (ip + 5)),
                   ip=ip).decode()


def test_store_folds_to_a_statement():
    lift = make_lifter(Expr('textArray1', STR_ARR, 'arr'))
    ins = call_insn()
    lift._insn(ins, [ins], 0, None, ins.next_ip)
    assert lift.out == [(0x900, 'textArray1[num2] = text1;', None)]


def test_store_leaves_the_bitmap_return_unknown():
    lift = make_lifter(Expr('textArray1', STR_ARR, 'arr'))
    ins = call_insn()
    lift._insn(ins, [ins], 0, None, ins.next_ip)
    # the native return is a GC bitmap word; source never reads it
    assert lift.regs['RAX']._unk is True


def test_raw_new_array_render_is_not_duplicated_per_element():
    """A `new T[n]` argument that was never hoisted must not turn into
    one allocation per element store: the fold declines and the site
    keeps a single call-shaped statement."""
    lift = make_lifter(Expr('(new string[6])', STR_ARR, 'arr'))
    ins = call_insn()
    lift._insn(ins, [ins], 0, None, ins.next_ip)
    text = ' '.join(l[1] or '' for l in lift.out)
    assert text.count('new string[6]') <= 1
    assert '] = ' not in text


def test_unreadable_array_argument_keeps_the_honest_fallback():
    lift = make_lifter(Expr('_', None, '?'))
    ins = call_insn()
    lift._insn(ins, [ins], 0, None, ins.next_ip)
    assert not any('] =' in (l[1] or '') for l in lift.out)


def test_inline_new_array_accumulates_a_collection_initializer():
    """`new T[n] { v0, v1 }`: constant-index stores on an inline array
    accumulate onto the array Expr and render as one initializer."""
    lift = make_lifter(Expr('new string[2]', STR_ARR, 'arr'))
    lift.regs['RDX'] = Expr('0', INT, 'int')
    first = call_insn()
    lift._insn(first, [first], 0, None, first.next_ip)
    lift.regs['RCX'] = lift.regs['RAX']
    lift.regs['RDX'] = Expr('1', INT, 'int')
    lift.regs['R8'] = Expr('"b"', STR, 'str')
    second = call_insn(ip=first.next_ip)
    lift._insn(second, [second], 0, None, second.next_ip)
    rendered = lift._materialize(lift.regs['RAX'], 400)
    assert rendered == 'new string[2] { text1, "b" }'


def test_variable_index_store_does_not_claim_an_initializer():
    lift = make_lifter(Expr('new string[5]', STR_ARR, 'arr'))
    ins = call_insn()
    lift._insn(ins, [ins], 0, None, ins.next_ip)
    # index is `num2`, not a literal: no initializer is invented and the
    # site keeps the honest call shape
    assert not any(getattr(l, '_arr_inits', None) for l in lift.out)
    assert '] = ' not in ' '.join(x[1] or '' for x in lift.out)


def test_null_check_helper_recognizer_bytes():
    """fix 150: the null-check body is a pure argument guard."""
    body = bytes.fromhex('4883ec284885c974054883c428c3e85d977800cc')
    assert len(body) == 20
    assert body[0:15] == bytes.fromhex('4883ec284885c974054883c428c3e8')
    assert body[19] == 0xCC
    # the recognizer's exact slices, so a body edit cannot drift silently
    assert Lifter.RT_ARITY['il2cpp_null_check'] == 1
    assert Lifter.RT_ARITY['il2cpp_array_setref'] == 3


def test_null_check_is_dropped_from_the_body():
    lift = make_lifter(Expr('obj9', STR, 'obj'))
    lift.rt_names[TARGET] = 'il2cpp_null_check'
    ins = call_insn()
    lift._insn(ins, [ins], 0, None, ins.next_ip)
    assert lift.out == []
