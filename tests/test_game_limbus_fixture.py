"""Limbus v39 fixture identity and metadata shape.

These checks are deliberately metadata-only where possible.  The exact body
tests live in ``test_game_limbus_decompile.py`` and run only on the archived
fixture pinned by ``tests/game_baselines.py``.
"""
import json
from pathlib import Path

import pytest

from game_baselines import BASELINES
from game_support import find_method, find_type

pytestmark = pytest.mark.game("limbus")


def test_fixture_is_the_reviewed_archive(game_fixture):
    assert game_fixture.id == 'limbus'
    assert Path(game_fixture.metadata).name == 'global-metadata.dat'
    assert Path(game_fixture.binary).name == 'GameAssembly.dll'
    assert Path(game_fixture.metadata).is_file()
    assert Path(game_fixture.binary).is_file()


def test_metadata_identity(baseline_game_decompiler):
    il, _ = baseline_game_decompiler
    meta = il.meta
    assert meta.version == 39
    assert len(meta.images) == 162
    assert len(meta.typedefs) == 51032
    assert len(meta.methods) == 319100

    # A few stable Limbus types prove this is the game tree, not a generic
    # Unity/System-only fixture.
    assert find_type(il, 'RPGSystem.RpgInventoryManager')
    assert find_type(il, 'Dungeon.DungeonProgress')
    assert find_type(
        il, 'LimbusCompany.Logics.ReturnFromStoryLibs.EnterStorySceneFromInventory')

    mi, m, _ = find_method(il, 'Dungeon.DungeonProgress', 'IsEmpty', 0)
    assert mi == 175155 and m.addr == 0x18255aa10


def test_manifest_records_the_same_fixture(game_tree, game_fixture):
    manifest_path = Path(game_tree) / 'MANIFEST.json'
    manifest = json.loads(manifest_path.read_text(encoding='utf-8'))
    pinned = BASELINES['limbus']
    assert manifest['metadata_sha256'] == pinned['metadata_sha256']
    assert manifest['binary_sha256'] == pinned['binary_sha256']
