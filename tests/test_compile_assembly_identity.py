"""The output DLL name participates in reference accessibility checks."""
from pathlib import Path
from types import SimpleNamespace as NS
import subprocess

import pytest

import compile_gate as cg
import gate


@pytest.mark.parametrize('name,expected', [
    ('UniTask.Linq', 'UniTask.Linq'), ('My.Game.dll', 'My.Game'),
    ('My.Game.DLL', 'My.Game'), ('Game with spaces', 'Game with spaces'),
])
def test_simple_assembly_name(name, expected):
    assert cg.assembly_simple_name(name) == expected


@pytest.mark.parametrize('name', ['', '.', '..', '.dll', 'Game.', 'Game ',
    '../Game', r'..\Game', '/Game', r'C:\Game.dll', 'x:y', 'x\ny',
    'x\0y', 'x"y', 'x*y', 'x?y', 'CON', 'nul.dll', 'LPT2', None, 12])
def test_bad_output_name_is_a_tool_error_not_a_compiler_success(tmp_path, name):
    # None is the API's intentional legacy anonymous mode, not an explicit name.
    if name is None:
        with pytest.raises(ValueError):
            cg.assembly_simple_name(name)
        return
    rep = cg.run_gate(str(tmp_path), assembly_name=name)
    assert rep['tool_error']
    assert rep['assembly_name'] is None


@pytest.mark.parametrize('failure', [None, 'exception', 'timeout'])
def test_exact_identity_is_isolated_and_cleaned_on_every_exit(tmp_path, monkeypatch, failure):
    source = tmp_path / 'Read.cs'; source.write_bytes(b'class Read {}')
    monkeypatch.setattr(cg, 'find_csc', lambda _: 'csc')
    paths = []

    def compile(cmd, **kwargs):
        target = Path(next(v[5:] for v in cmd if v.startswith('/out:')))
        assert target.name == 'Expected.Friend.dll'
        assert target.parent.is_dir()
        assert not target.is_relative_to(tmp_path)
        paths.append(target)
        target.write_bytes(b'fake compiler output')
        if failure == 'exception':
            raise RuntimeError('compiler failure')
        if failure == 'timeout':
            raise subprocess.TimeoutExpired(cmd, 1)
        return NS(stdout=b'', stderr=b'', returncode=0)

    monkeypatch.setattr(cg.subprocess, 'run', compile)
    for _ in range(2):
        rep = cg.run_gate(str(tmp_path), assembly_name='Expected.Friend.dll')
        assert rep['assembly_name'] == 'Expected.Friend'
        assert bool(rep['tool_error']) == bool(failure)
        assert not paths[-1].parent.exists()
    assert paths[0].parent != paths[1].parent
    assert list(tmp_path.iterdir()) == [source]


def test_explicit_tree_does_not_infer_identity_from_build_label(tmp_path, monkeypatch):
    tree = tmp_path / 'build_label'; tree.mkdir()
    seen = []
    def compile(path, **kwargs):
        seen.append(kwargs['assembly_name'])
        return dict(files=1, syntax=0, binding=0, samples={}, tool_error=None)
    monkeypatch.setattr(cg, 'run_gate', compile)
    for extra in ([], ['--assembly', 'Actual.Game']):
        assert gate.main(['compile', '--tree', str(tree), '--report',
                          str(tmp_path / 'report.json')] + extra) == 0
    assert seen == [None, 'Actual.Game']


def test_resolved_image_identity_is_not_filter_substring(tmp_path, monkeypatch):
    tree = tmp_path / 'build_label'; tree.mkdir()
    (tree / 'Actual.Game').mkdir()
    monkeypatch.setattr(gate, '_tree_for', lambda _: str(tree))
    def compile(path, **kwargs):
        assert Path(path).name == 'Actual.Game'
        assert kwargs['assembly_name'] == 'Actual.Game'
        return dict(files=1, syntax=0, binding=0, samples={}, tool_error=None)
    monkeypatch.setattr(cg, 'run_gate', compile)
    assert gate.main(['compile', '--fixture', 'fake', '--only', 'Game', '--report',
                      str(tmp_path / 'report.json')]) == 0


def test_direct_cli_passes_explicit_assembly_identity(tmp_path, monkeypatch):
    def compile(*args, **kwargs):
        assert kwargs['assembly_name'] == 'Actual.Game.dll'
        return dict(files=1, syntax=0, binding=0, top=[], samples={}, tool_error=None)
    monkeypatch.setattr(cg, 'run_gate', compile)
    monkeypatch.setattr(cg.sys, 'argv', ['compile_gate', '--tree', str(tmp_path),
                                      '--assembly', 'Actual.Game.dll'])
    assert cg.main() == 0
