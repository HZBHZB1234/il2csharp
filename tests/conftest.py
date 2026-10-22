"""Keep the package importable and resolve game fixtures by registry.

A "game" fixture (a real IL2CPP build) lives on the local disk only and is
never committed. Tests reach it through :func:`fixture_paths`, which prefers
``IL2CSHARP_METADATA``/``IL2CSHARP_BINARY`` (the legacy override) and falls
back to ``fixtures/registry.json``. When neither is present the test skips
with an actionable message instead of failing.
"""
import os
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / 'tools'))


def _registry_module():
    try:
        import fixtures  # tools/fixtures.py
        return fixtures
    except Exception:
        return None


def fixture_paths():
    """Return (metadata_path, binary_path) or None when no fixture is usable.

    Explicit env vars win; otherwise the registry default. Never raises --
    an unusable fixture is a skip, not an error.
    """
    meta = os.environ.get('IL2CSHARP_METADATA')
    binary = os.environ.get('IL2CSHARP_BINARY')
    if meta and binary and Path(meta).is_file() and Path(binary).is_file():
        return meta, binary
    fx_mod = _registry_module()
    if fx_mod is None:
        return None
    try:
        fx = fx_mod.resolve(os.environ.get('IL2CSHARP_FIXTURE'))
    except Exception:
        return None
    return str(fx.metadata), str(fx.binary)


def fixture_paths_or_skip(reason="no game fixture"):
    paths = fixture_paths()
    if paths is None:
        pytest.skip(
            "%s: set IL2CSHARP_METADATA/IL2CSHARP_BINARY or add a fixture to "
            "fixtures/registry.json (see docs/fixtures.md)" % reason)
    return paths


def out_tree(label=None, fixture=None):
    """Return the Path of a built tree for a fixture, or None when absent."""
    fx_mod = _registry_module()
    if fx_mod is None:
        return None
    try:
        fx = fx_mod.resolve(fixture or os.environ.get('IL2CSHARP_FIXTURE'))
    except Exception:
        return None
    tree = fx_mod.out_tree(fx, label or os.environ.get('IL2CSHARP_LABEL'))
    # out/<id>/ exists as soon as a run touches it; only a tree with at
    # least one emitted source file counts as built.
    if not tree.is_dir() or next(tree.rglob('*.cs'), None) is None:
        return None
    return tree


def out_tree_or_skip(label=None, fixture=None, reason="no built tree"):
    tree = out_tree(label, fixture)
    if tree is None:
        pytest.skip(
            "%s: build one with `python il2csharp.py --fixture <id> "
            "--label <name>` (see docs/fixtures.md)" % reason)
    return tree
