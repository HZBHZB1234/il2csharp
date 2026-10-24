"""Optional sample-game goldens; the 64 rows are not Limbus snapshots.

The original goldens_review77.json is retained unchanged. Review 84 keeps the
same 64 MethodDefs and freezes its constructor/allocation bodies only after the
complete strict-build, parse, direct-sweep, and output-audit gates.  That
fixture is the older sample game, so the module is marked
``shiftatmidnight``; it skips when that fixture is not registered instead of
pointing its positional pins at Limbus.

Fixture resolution goes through ``tests/conftest.py``: ``IL2CSHARP_METADATA``/
``IL2CSHARP_BINARY`` still work for an explicitly selected fixture.
"""
import hashlib
import json
from pathlib import Path

import pytest

GOLDEN_PATH = Path(__file__).with_name("goldens_review84.json")
GOLDENS = json.loads(GOLDEN_PATH.read_text(encoding="utf-8")) if GOLDEN_PATH.exists() else {}
SNAPSHOTS = GOLDENS.get("methods", [None])

pytestmark = pytest.mark.game("shiftatmidnight")


@pytest.mark.parametrize("snapshot", SNAPSHOTS, ids=[
    f"mi-{s['mi']}-{s['name']}" if s is not None else "not-generated" for s in SNAPSHOTS
])
def test_real_method_snapshot(baseline_game_decompiler, snapshot):
    il, dec = baseline_game_decompiler
    m = il.meta.methods[snapshot["mi"]]
    assert hex(m.addr) == snapshot["va"]
    actual = dec.lift_method(m, il.meta.typedefs[m.declaring])
    if "body" in snapshot:
        assert actual == snapshot["body"]
        return
    # hash-only (public) variant: the same pin without the game-derived text
    digest = hashlib.sha256("\n".join(actual).encode("utf-8")).hexdigest()
    assert digest == snapshot["body_sha256"]