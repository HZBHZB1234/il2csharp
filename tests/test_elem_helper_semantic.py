"""Element-access helper semantic labels for the stub file (URE §5).

The high-count plain `sub_` helpers are IL2CPP element-access routines
(`sub rsp,0x28; cmp edx,[rcx+0x18]; jae ...`).  `_elem_helper_semantic`
recognises the family by the exact opening bytes and returns a one-line
label that `_stub_owners` appends to the `// 0xVA: ...` comment in
__SharedBodyStubs.cs.  The CALL SITE keeps its honest `sub_<va>`; only
the stub comment gains the label.  Tested on a hand-built byte buffer.
"""
from types import SimpleNamespace

from il2cpp import Emitter


class _Bin:
    def __init__(self, code_map):
        self._m = code_map

    def is_exec_va(self, va):
        return va in self._m

    def read(self, va, n):
        return self._m.get(va, b'')[:n]


def _em(code_map):
    em = Emitter.__new__(Emitter)
    em.il = SimpleNamespace(bin=_Bin(code_map))
    return em


def test_list_getter_label():
    # 4883ec28 3b5118 73 1b 488b4910 ...
    code = bytes.fromhex('4883ec283b5118731b488b4910') + b'\x48\x85\xc9'
    em = _em({0x1000: code})
    lbl = em._elem_helper_semantic('1000')
    assert lbl is not None and 'indexer getter' in lbl


def test_setter_label():
    # 4883ec28 3b5118 73 57 833d...
    code = bytes.fromhex('4883ec283b51187357833d8c5a430900')
    em = _em({0x2000: code})
    lbl = em._elem_helper_semantic('2000')
    assert lbl is not None and 'setter' in lbl


def test_array_element_getter_label():
    code = bytes.fromhex('4883ec283b5118730a488b44d120')
    em = _em({0x3000: code})
    lbl = em._elem_helper_semantic('3000')
    assert lbl is not None and 'array element getter' in lbl


def test_non_helper_declines():
    # wrong prefix
    em = _em({0x4000: bytes.fromhex('554889e54883ec20')})
    assert em._elem_helper_semantic('4000') is None


def test_near_jcc_declines():
    # correct prefix but 0F 83 near jae instead of 73
    code = bytes.fromhex('4883ec283b51180f83aabbccdd')
    em = _em({0x5000: code})
    assert em._elem_helper_semantic('5000') is None


def test_owner_note_uses_label_for_unregistered():
    code = bytes.fromhex('4883ec283b5118731b488b4910') + b'\x48\x85\xc9'
    em = _em({0x6000: code})
    em.il.addr_candidates = {}
    note = em._stub_owners('6000')
    assert 'unregistered native target' in note
    assert 'indexer getter' in note
