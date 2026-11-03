"""Editor references override player engine/BCL without duplicate identities."""
import json
from types import SimpleNamespace as NS

import compile_gate as cg
import gate


def test_merge_uses_case_insensitive_names_deterministic_order_and_latest_group():
    actual = cg.merge_refs(['player/UNITYENGINE.dll', 'player/netstandard.dll',
                            'player/Package.dll'],
                           ['editor/UnityEngine.dll', 'editor/NetStandard.dll'],
                           ['override/Package.dll'])
    assert actual == ['editor/NetStandard.dll', 'override/Package.dll',
                      'editor/UnityEngine.dll']


def test_exclude_applies_to_every_reference_group_and_path_style():
    assert cg.merge_refs([r'C:\player\Game.dll'], ['editor/Game.dll', 'Extra.dll'],
                         exclude=['GAME.DLL']) == ['Extra.dll']


def test_global_compiler_errors_are_not_a_zero_error_result():
    output = ('error CS0006: Metadata file missing\n'
              'CSC : error CS1704: An assembly with the same simple name was imported\n'
              'csc.exe : warning CS2023: ignored option\n')
    assert cg.classify(output) == (1, 1, [('CS0006', 1), ('CS1704', 1)])
    samples = cg.first_samples(output)
    assert samples['CS0006'][0]['file'] == '<compiler>'
    assert samples['CS0006'][0]['line'] == 0


def test_gate_exposes_editor_closure_and_body_probe_in_either_option_order(tmp_path, monkeypatch):
    tree = tmp_path / 'Game'; tree.mkdir()
    report = tmp_path / 'report.json'
    seen = {}
    monkeypatch.setattr(gate, 'resolve', lambda _: NS(game_dir=tmp_path / 'build'))
    monkeypatch.setattr(cg, 'managed_refs', lambda path, exclude:
                        ['player/Game.dll', 'player/UnityEngine.dll',
                         'player/netstandard.dll', 'player/Package.dll'])
    monkeypatch.setattr(cg, 'unity_refs', lambda path: ['editor/UnityEngine.dll'])
    monkeypatch.setattr(cg, 'unity_framework_refs', lambda path: ['editor/netstandard.dll'])

    def compile(tree, **kwargs):
        seen.update(kwargs)
        return dict(files=1, syntax=0, binding=0, samples={}, tool_error=None,
                    body_probe_observed=True)
    monkeypatch.setattr(cg, 'run_gate', compile)
    assert gate.main(['compile', '--tree', str(tree), '--fixture', 'fake',
                      '--managed-refs', '--unity', 'editor', '--body-probe',
                      '--report', str(report)]) == 0
    assert seen['refs'] == ['editor/netstandard.dll', 'player/Package.dll',
                            'editor/UnityEngine.dll']
    assert seen['body_probe'] is True
    assert json.loads(report.read_bytes())['body_probe_observed'] is True
    assert gate._normalize_argv(['--body-probe', 'compile', '--unity=editor',
                                 '--managed-refs', '--no-framework']) == [
        '--body-probe', '--unity=editor', '--managed-refs', '--no-framework', 'compile']


def test_compile_cli_uses_the_same_merge_policy(tmp_path, monkeypatch):
    seen = {}
    monkeypatch.setattr(cg, 'managed_refs', lambda path:
                        ['player/UnityEngine.dll', 'player/netstandard.dll',
                         'player/Package.dll', 'player/Game.dll'])
    monkeypatch.setattr(cg, 'unity_refs', lambda path: ['editor/UnityEngine.dll'])
    monkeypatch.setattr(cg, 'unity_framework_refs', lambda path: ['editor/netstandard.dll'])

    def compile(*args, **kwargs):
        seen['refs'] = args[3]
        return dict(files=1, syntax=0, binding=0, top=[], samples={}, tool_error=None)
    monkeypatch.setattr(cg, 'run_gate', compile)
    monkeypatch.setattr(cg.sys, 'argv', ['compile_gate', '--tree', str(tmp_path),
                        '--unity', 'editor', '--managed-refs', 'build', '--exclude', 'Game.dll'])
    assert cg.main() == 0
    assert seen['refs'] == ['editor/netstandard.dll', 'player/Package.dll',
                            'editor/UnityEngine.dll']


def test_image_substring_excludes_the_actual_resolved_image(tmp_path, monkeypatch):
    tree = tmp_path / 'tree'; tree.mkdir()
    image = tree / 'Actual.Game'; image.mkdir()
    report = tmp_path / 'report.json'
    monkeypatch.setattr(gate, '_tree_for', lambda args: str(tree))
    monkeypatch.setattr(gate, 'resolve', lambda _: NS(game_dir=tmp_path / 'build'))
    def refs(path, excludes):
        assert 'Actual.Game.dll' in excludes
        assert 'Game.dll' not in excludes
        return ['player/Package.dll']
    monkeypatch.setattr(cg, 'managed_refs', refs)
    monkeypatch.setattr(cg, 'unity_refs', lambda path: [])
    monkeypatch.setattr(cg, 'unity_framework_refs', lambda path: [])
    def compile(path, **kwargs):
        assert path == str(image)
        return dict(files=1, syntax=0, binding=0, samples={}, tool_error=None)
    monkeypatch.setattr(cg, 'run_gate', compile)
    assert gate.main(['compile', '--fixture', 'fake', '--only', 'Game',
                      '--managed-refs', '--report', str(report)]) == 0
