"""A low error count must not hide that Roslyn skipped method binding."""
import re
from pathlib import Path
from types import SimpleNamespace as NS

import pytest

import compile_gate as cg


@pytest.mark.parametrize('observe', [True, False])
def test_probe_is_reported_but_not_counted_or_written_to_tree(tmp_path, monkeypatch, observe):
    (tmp_path / 'A.cs').write_bytes(b'class A {}')
    monkeypatch.setattr(cg, 'find_csc', lambda _: 'csc')
    paths = []

    def compile(cmd, **kwargs):
        rsp = Path(cmd[-1][1:])
        sources = [Path(s.strip('"')) for s in rsp.read_text().splitlines()
                   if s.startswith('"')]
        probe = next(p for p in sources if p.name.startswith('gateprobe_'))
        paths.append(probe)
        assert not probe.is_relative_to(tmp_path)
        name = re.search(r'return (\w+);', probe.read_text()).group(1)
        output = 'A.cs(1,2): error CS0535: real declaration error\n'
        if observe:
            output += f"{probe}(1,1): error CS0103: The name '{name}' does not exist\n"
        # Same diagnostic code at a real source file remains counted.
        output += 'A.cs(2,3): error CS0103: real missing value\n'
        return NS(stdout=output.encode(), stderr=b'', returncode=1)

    monkeypatch.setattr(cg.subprocess, 'run', compile)
    rep = cg.run_gate(str(tmp_path), body_probe=True)
    assert rep['body_probe_observed'] is observe
    assert rep['binding'] == 2
    assert rep['files'] == 1
    assert dict(rep['top']) == {'CS0103': 1, 'CS0535': 1}
    assert rep['samples']['CS0103'][0]['file'] == 'A.cs'
    assert all(not p.exists() for p in paths)
    assert [p.name for p in tmp_path.iterdir()] == ['A.cs']


def test_probe_removed_when_compiler_fails(tmp_path, monkeypatch):
    (tmp_path / 'A.cs').write_bytes(b'class A {}')
    monkeypatch.setattr(cg, 'find_csc', lambda _: 'csc')
    paths = []

    def fail(cmd, **kwargs):
        paths.extend(Path(s.strip('"')) for s in Path(cmd[-1][1:]).read_text().splitlines()
                     if 'gateprobe_' in s)
        raise RuntimeError('fake compiler failure')

    monkeypatch.setattr(cg.subprocess, 'run', fail)
    rep = cg.run_gate(str(tmp_path), body_probe=True)
    assert rep['body_probe_observed'] is None
    assert 'fake compiler failure' in rep['tool_error']
    assert paths and all(not p.exists() for p in paths)
