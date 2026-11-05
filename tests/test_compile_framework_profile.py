"""Explicit real-Editor runtime closures; path fixtures are never compiled."""
import json
from pathlib import Path

import pytest

import compile_gate as cg
import gate

RUNTIMES = ('unityjit-win32', 'unityaot-win32', 'net_4_x-win32')
CORE = ('mscorlib.dll', 'System.dll', 'System.Core.dll', 'Facades/netstandard.dll')


def editor_tree(root, profile='unityjit-win32'):
    base = root / 'Editor/Data/MonoBleedingEdge/lib/mono' / profile
    for relative in (*CORE, 'Facades/System.Runtime.dll', 'Extras.DLL'):
        path = base / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(b'path-only fixture; not a managed API stub')
    (base / 'ignored.txt').write_bytes(b'ignored')
    (base / 'Directory.dll').mkdir()
    shim = root / 'Editor/Data/NetStandard/ref/2.1.0/netstandard.dll'
    shim.parent.mkdir(parents=True)
    shim.write_bytes(b'historical path-only shim')
    engine = root / 'Editor/Data/Managed/UnityEngine/UnityEngine.dll'
    engine.parent.mkdir(parents=True)
    engine.write_bytes(b'path-only engine fixture')
    return base


@pytest.mark.parametrize('profile', RUNTIMES)
@pytest.mark.parametrize('editor_subdir', [False, True])
def test_runtime_is_one_profile_with_facades_not_the_netstandard_shims(tmp_path, profile, editor_subdir):
    base = editor_tree(tmp_path, profile)
    root = tmp_path / 'Editor' if editor_subdir else tmp_path
    actual = cg.unity_framework_refs(str(root), profile=profile)
    assert actual == cg.unity_framework_refs(root, profile=profile)
    assert [Path(p).relative_to(base).as_posix() for p in actual] == [
        'Extras.DLL', 'System.Core.dll', 'System.dll', 'mscorlib.dll',
        'Facades/System.Runtime.dll', 'Facades/netstandard.dll']
    assert all(Path(p).is_file() for p in actual)
    assert not any('NetStandard' in p for p in actual)


@pytest.mark.parametrize('profile', RUNTIMES)
@pytest.mark.parametrize('missing', CORE)
def test_incomplete_runtime_never_falls_back_to_available_shims(tmp_path, profile, missing):
    base = editor_tree(tmp_path, profile)
    (base / missing).unlink()
    with pytest.raises(ValueError, match='missing/incomplete'):
        cg.unity_framework_refs(tmp_path, profile=profile)
    assert len(cg.unity_framework_refs(tmp_path)) == 1


@pytest.mark.parametrize('profile', RUNTIMES)
def test_runtime_requires_editor_root_and_never_uses_other_profile(tmp_path, profile):
    with pytest.raises(ValueError, match='requires --unity'):
        cg.unity_framework_refs(profile=profile)
    editor_tree(tmp_path, profile)
    other = next(p for p in RUNTIMES if p != profile)
    with pytest.raises(ValueError, match='missing/incomplete'):
        cg.unity_framework_refs(tmp_path, profile=other)


@pytest.mark.parametrize('profile', ['../unityjit-win32', 'UNITYJIT-WIN32', '', None, 'auto'])
def test_profile_is_an_exact_known_name_not_an_arbitrary_path(tmp_path, profile):
    with pytest.raises(ValueError, match='unsupported'):
        cg.unity_framework_refs(tmp_path, profile=profile)


def test_default_closure_and_empty_default_are_unchanged(tmp_path):
    editor_tree(tmp_path)
    assert cg.unity_framework_refs(tmp_path) == cg.unity_framework_refs(
        tmp_path, profile='netstandard2.1')
    assert cg.unity_framework_refs(None) == []
    assert cg.unity_framework_refs(tmp_path / 'absent') == []


def fake_run(monkeypatch, seen):
    def run(*args, **kwargs):
        seen.update(kwargs)
        if len(args) > 3:
            seen['refs'] = args[3]
        return dict(files=1, syntax=0, binding=4, top=[], samples={},
                    tool_error=None, body_probe_observed=True)
    monkeypatch.setattr(cg, 'run_gate', run)


@pytest.mark.parametrize('position', ['before', 'after', 'equals'])
def test_gate_cli_hoists_profile_and_records_selection_without_changing_identity(tmp_path, monkeypatch, position):
    base = editor_tree(tmp_path)
    tree = tmp_path / 'Game'
    tree.mkdir()
    report = tmp_path / 'gate.json'
    seen = {}
    fake_run(monkeypatch, seen)
    options = ['--tree', str(tree), '--unity', str(tmp_path), '--assembly', 'Original.Game',
               '--body-probe', '--report', str(report)]
    profile = ['--framework-profile', 'unityjit-win32']
    argv = (profile + ['compile'] + options if position == 'before' else
            ['compile'] + options + (['--framework-profile=unityjit-win32']
                                     if position == 'equals' else profile))
    assert gate.main(argv) == 0
    assert seen['assembly_name'] == 'Original.Game'
    assert seen['body_probe'] is True
    assert set(seen['refs']) == set(cg.merge_refs(cg.unity_refs(tmp_path),
                                                 cg.unity_framework_refs(tmp_path, profile='unityjit-win32')))
    payload = json.loads(report.read_bytes())
    assert payload['framework_profile'] == 'unityjit-win32'
    assert payload['framework_refs'] == 6
    assert payload['binding'] == 4 and payload['body_probe_observed'] is True
    assert str(base / 'Facades/netstandard.dll') in seen['refs']


def test_standalone_cli_passes_runtime_to_compiler_and_keeps_explicit_overrides(tmp_path, monkeypatch, capsys):
    editor_tree(tmp_path)
    extra = tmp_path / 'overrides'
    extra.mkdir()
    (extra / 'System.dll').write_bytes(b'explicit path override')
    seen = {}
    fake_run(monkeypatch, seen)
    monkeypatch.setattr(cg.sys, 'argv', ['compile_gate', '--tree', str(tmp_path),
                        '--unity', str(tmp_path), '--framework-profile', 'unityjit-win32',
                        '--refs-dir', str(extra), '--exclude', 'System.Core.dll'])
    assert cg.main() == 0
    assert str(extra / 'System.dll') in seen['refs']
    assert not any(Path(p).name == 'System.Core.dll' for p in seen['refs'])
    assert 'Editor framework profile: unityjit-win32' in capsys.readouterr().out


@pytest.mark.parametrize('cli', ['gate', 'standalone'])
@pytest.mark.parametrize('flags', [
    ['--framework-profile', 'unityjit-win32', '--no-framework'],
    ['--framework-profile', 'unityjit-win32'],
    ['--framework-profile', 'netstandard2.1'],
])
def test_explicit_missing_or_disabled_profile_is_a_usage_error_not_an_empty_closure(tmp_path, monkeypatch, cli, flags):
    seen = {}
    fake_run(monkeypatch, seen)
    args = ['--tree', str(tmp_path), *flags]
    if cli == 'gate':
        assert gate.main(['compile', *args]) == 2
    else:
        monkeypatch.setattr(cg.sys, 'argv', ['compile_gate', *args])
        assert cg.main() == 2
    assert seen == {}


@pytest.mark.parametrize('cli', ['gate', 'standalone'])
def test_no_framework_never_loads_default_shims(tmp_path, monkeypatch, cli):
    seen = {}
    fake_run(monkeypatch, seen)
    def forbidden(*args, **kwargs):
        raise AssertionError('framework selector called despite --no-framework')
    monkeypatch.setattr(cg, 'unity_framework_refs', forbidden)
    args = ['--tree', str(tmp_path), '--no-framework']
    if cli == 'gate':
        args += ['--report', str(tmp_path / 'gate.json')]
        assert gate.main(['compile', *args]) == 0
        assert json.loads((tmp_path / 'gate.json').read_bytes())['framework_profile'] == 'none'
    else:
        monkeypatch.setattr(cg.sys, 'argv', ['compile_gate', *args])
        assert cg.main() == 0
    assert seen['refs'] == []
