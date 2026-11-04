"""Whole-value recovery without changing scalar tiles or padding facts."""
import re

import pytest

from game_support import lift_text
from il2cpp.lifter import materialized

pytestmark = pytest.mark.game('unitask')


@pytest.mark.parametrize('mi,type_name,size,home', [
    (30505, 'UnityEngine.Rendering.AsyncGPUReadbackRequest', 16, -200),
    (30549, 'UnityEngine.LowLevel.PlayerLoopSystem', 40, -104),
])
def test_native_copy_keeps_materialized_value_at_typed_consumer(
        raw_game_decompiler, monkeypatch, mi, type_name, size, home):
    il, dec = raw_game_decompiler
    original = materialized.recover_materialized_sret
    hits = []

    def observe(lift, address, ty):
        regs = {k: tuple(getattr(v, a, None) for a in v.__slots__) if v else None
                for k, v in dict.items(lift.regs)}
        hints = dict(lift._type_hints)
        slots, types = dict(lift.slot_types), dict(lift._var_types)
        result = original(lift, address, ty)
        assert regs == {k: tuple(getattr(v, a, None) for a in v.__slots__) if v else None
                        for k, v in dict.items(lift.regs)}
        assert hints == lift._type_hints and slots == lift.slot_types and types == lift._var_types
        if result is not None:
            assert lift._current_method.index == mi
            assert il.type_name(ty) == type_name
            assert il._sf_field_size(ty, 0) == size
            assert address == home
            assert lift._materialized_sret.scope is lift.out
            hits.append((lift.dry, result))
        return result

    monkeypatch.setattr(materialized, 'recover_materialized_sret', observe)
    candidate = lift_text(il, dec, mi)
    assert [dry for dry, _ in hits] == [True, False]
    monkeypatch.setattr(materialized, 'recover_materialized_sret', lambda *args: None)
    baseline = lift_text(il, dec, mi)
    # Compare proven substitutions, not a golden hash or an output body.
    if mi == 30505:
        pattern = (r'new UnityEngine.Rendering.AsyncGPUReadbackRequest \{ '
                   r'm_Ptr = (\w+)\.m_Ptr, m_Version = \1\.m_Version \}')
        rewritten, count = re.subn(pattern, r'\1', baseline)
    else:
        pattern = (r'System.IntPtr (?P<scalar>num\d+) = (?P<whole>\w+)\.loopConditionFunction;\n'
                   r'PlayerLoopInfo.DumpPlayerLoop\("Default", new UnityEngine.LowLevel.PlayerLoopSystem \{ '
                   r'type = (?P=whole)\.type, subSystemList = (?P=whole)\.subSystemList, '
                   r'updateDelegate = (?P=whole)\.updateDelegate, updateFunction = (?P=whole)\.updateFunction, '
                   r'loopConditionFunction = (?P=scalar) \}\);')
        rewritten, count = re.subn(pattern, r'PlayerLoopInfo.DumpPlayerLoop("Default", \g<whole>);', baseline)
    assert count == 1 and rewritten == candidate
