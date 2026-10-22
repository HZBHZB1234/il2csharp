"""Portable checks for the fixture framework (needs no game on disk).

These pin the parts that must work in a fresh clone: the registry template is
valid, the loader gives actionable errors instead of KeyError/None, output
trees land under out/, and the ignored paths really are ignored.
"""
import json
import os
import subprocess
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
TOOLS = ROOT / 'tools'
sys.path.insert(0, str(TOOLS))

import fixtures  # noqa: E402


def test_registry_example_has_the_required_shape():
    data = json.loads((ROOT / 'fixtures' / 'registry.example.json').read_text(encoding='utf-8'))
    assert 'fixtures' in data and isinstance(data['fixtures'], dict)
    assert data['fixtures'], 'the template must carry at least one example entry'
    for fid, entry in data['fixtures'].items():
        assert isinstance(fid, str) and fid
        assert 'game_dir' in entry, fid
        assert 'metadata' in entry and 'binary' in entry, fid
        # licensing must be explicit, so a future game cannot slip in unpublished
        assert 'license' in entry, fid
        assert 'redistributable' in entry, fid


def test_resolve_without_registry_is_actionable(tmp_path, monkeypatch):
    monkeypatch.setattr(fixtures, 'REGISTRY_PATH', tmp_path / 'nope.json')
    monkeypatch.delenv('IL2CSHARP_FIXTURE', raising=False)
    monkeypatch.delenv('IL2CSHARP_METADATA', raising=False)
    monkeypatch.delenv('IL2CSHARP_BINARY', raising=False)
    with pytest.raises(fixtures.FixtureError) as exc:
        fixtures.resolve()
    assert 'registry.example.json' in str(exc.value)


def test_unknown_fixture_lists_available(tmp_path, monkeypatch):
    reg = tmp_path / 'registry.json'
    reg.write_text(json.dumps({'fixtures': {
        'alpha': {'game_dir': str(tmp_path), 'metadata': 'm.dat', 'binary': 'g.dll'}}}),
        encoding='utf-8')
    monkeypatch.setattr(fixtures, 'REGISTRY_PATH', reg)
    monkeypatch.delenv('IL2CSHARP_METADATA', raising=False)
    monkeypatch.delenv('IL2CSHARP_BINARY', raising=False)
    with pytest.raises(fixtures.FixtureError) as exc:
        fixtures.resolve('beta')
    assert 'alpha' in str(exc.value)


def test_missing_game_dir_names_the_fixture(tmp_path, monkeypatch):
    reg = tmp_path / 'registry.json'
    reg.write_text(json.dumps({'fixtures': {
        'ghost': {'game_dir': str(tmp_path / 'does-not-exist'),
                  'metadata': 'm.dat', 'binary': 'g.dll'}}}), encoding='utf-8')
    monkeypatch.setattr(fixtures, 'REGISTRY_PATH', reg)
    with pytest.raises(fixtures.FixtureError) as exc:
        fixtures.resolve('ghost')
    assert 'ghost' in str(exc.value) and 'game_dir' in str(exc.value)


def test_env_override_skips_the_registry(tmp_path, monkeypatch):
    meta = tmp_path / 'm.dat'
    binary = tmp_path / 'g.dll'
    meta.write_bytes(b'\0' * 8)
    binary.write_bytes(b'\0' * 8)
    monkeypatch.setenv('IL2CSHARP_METADATA', str(meta))
    monkeypatch.setenv('IL2CSHARP_BINARY', str(binary))
    fx = fixtures.resolve()  # no registry needed
    assert fx.id == 'env'
    assert Path(fx.metadata) == meta


def test_doctor_accepts_option_and_positional_id(tmp_path, monkeypatch, capsys):
    """The docs use `doctor --id X`; the original parser only took `doctor X`."""
    reg = tmp_path / 'registry.json'
    reg.write_text(json.dumps({'fixtures': {}}), encoding='utf-8')
    monkeypatch.setattr(fixtures, 'REGISTRY_PATH', reg)
    for arg in (['doctor', '--id', 'nope'], ['doctor', 'nope']):
        assert fixtures.main(arg) == 1
        out = capsys.readouterr()
        assert "unknown fixture 'nope'" in out.out


def test_out_tree_layout_is_out_fixture_label():
    class _FX:
        id = 'somegame'
    tree = fixtures.out_tree(_FX(), 'r1')
    assert tree == fixtures.OUT_ROOT / 'somegame' / 'r1'
    assert 'out' in tree.parts


def test_out_tree_defaults_to_newest_label(tmp_path, monkeypatch):
    class _FX:
        id = 'somegame'
    base = tmp_path / 'somegame'
    old, new = base / 'z-old', base / 'a-new'
    old.mkdir(parents=True)
    new.mkdir()
    os.utime(old, (1, 1))
    os.utime(new, (2, 2))
    monkeypatch.setattr(fixtures, 'OUT_ROOT', tmp_path)
    monkeypatch.delenv('IL2CSHARP_LABEL', raising=False)
    assert fixtures.out_tree(_FX()) == new


def test_tree_is_built_requires_a_source_file(tmp_path):
    assert not fixtures.tree_is_built(tmp_path)
    (tmp_path / 'Type.cs').write_text('class C {}\n', encoding='utf-8')
    assert fixtures.tree_is_built(tmp_path)


def test_fixtures_and_out_are_git_ignored():
    """A fresh clone must never pick up a local game or an output tree."""
    for probe in ('fixtures/registry.json', 'fixtures/x/game/GameAssembly.dll',
                  'out/x/y/MANIFEST.json'):
        r = subprocess.run(['git', 'check-ignore', probe], cwd=str(ROOT),
                           capture_output=True, text=True,
                           encoding='utf-8', errors='replace')
        assert r.returncode == 0, '%s is NOT git-ignored' % probe
    # the tracked template must NOT be ignored
    r = subprocess.run(['git', 'check-ignore', 'fixtures/registry.example.json'],
                       cwd=str(ROOT), capture_output=True, text=True,
                       encoding='utf-8', errors='replace')
    assert r.returncode != 0, 'registry.example.json must stay tracked'
