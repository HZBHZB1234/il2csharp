"""Keep the package importable and resolve game fixtures by marker.

Game tests declare which game they need:

    pytestmark = pytest.mark.game("limbus")

The marker is the single source of truth for selection and fixture resolution.
``pytest --game limbus`` runs the portable tests plus the Limbus tests;
``pytest --game limbus --strict-games`` turns a missing fixture or a build
fingerprint mismatch into a failure instead of a skip.

A real game fixture lives on the local disk only and is never committed.
Paths are resolved through ``tools/fixtures.py``. The legacy
``IL2CSHARP_METADATA``/``IL2CSHARP_BINARY`` pair still works when no explicit
fixture id is requested.
"""
import json
import os
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / 'tools'))

_SHA_CACHE = {}
_IL_CACHE = {}


def _registry_module():
    try:
        import fixtures  # tools/fixtures.py
        return fixtures
    except Exception:
        return None


def _sha256_cached(path):
    import hashlib
    path = Path(path)
    key = (str(path), path.stat().st_size, path.stat().st_mtime_ns)
    if key not in _SHA_CACHE:
        h = hashlib.sha256()
        with path.open('rb') as fh:
            for chunk in iter(lambda: fh.read(1 << 20), b''):
                h.update(chunk)
        _SHA_CACHE[key] = h.hexdigest()
    return _SHA_CACHE[key]


def _marker_game_id(node):
    marker = node.get_closest_marker('game')
    if marker is not None and marker.args:
        return str(marker.args[0])
    return None


def _strict(request):
    return bool(request.config.getoption('--strict-games'))


def _fail_or_skip(request, message, game_id=None):
    selected = set(request.config.getoption('--game') or [])
    if _strict(request) and (not selected or game_id in selected):
        pytest.fail(message)
    pytest.skip(message)


def fixture_paths(game_id=None):
    """Return (metadata_path, binary_path) or None when no fixture is usable.

    An explicit ``game_id`` wins over the legacy environment pair. With no id,
    ``IL2CSHARP_METADATA``/``IL2CSHARP_BINARY`` take priority, then the
    registry default. Never raises -- an unusable fixture is a skip, not an
    error, unless a fixture-backed test opts into ``--strict-games``.
    """
    if game_id is None:
        meta = os.environ.get('IL2CSHARP_METADATA')
        binary = os.environ.get('IL2CSHARP_BINARY')
        if meta and binary and Path(meta).is_file() and Path(binary).is_file():
            return meta, binary
        game_id = os.environ.get('IL2CSHARP_FIXTURE') or None
    fx_mod = _registry_module()
    if fx_mod is None:
        return None
    try:
        fx = fx_mod.resolve(game_id)
    except Exception:
        return None
    return str(fx.metadata), str(fx.binary)


def fixture_paths_or_skip(reason="no game fixture", game_id=None):
    paths = fixture_paths(game_id)
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
        fx = fx_mod.resolve(fixture or os.environ.get('IL2CSHARP_FIXTURE') or None)
    except Exception:
        return None
    tree = fx_mod.out_tree(fx, label or os.environ.get('IL2CSHARP_LABEL'))
    # out/<id>/ exists as soon as a run touches it; only a tree with at
    # least one emitted source file counts as built.
    if not fx_mod.tree_is_built(tree):
        return None
    return tree


def out_tree_or_skip(label=None, fixture=None, reason="no built tree"):
    tree = out_tree(label, fixture)
    if tree is None:
        pytest.skip(
            "%s: build one with `python il2csharp.py --fixture <id> "
            "--label <name>` (see docs/fixtures.md)" % reason)
    return tree


def pytest_addoption(parser):
    parser.addoption(
        '--game', action='append', default=[], metavar='ID',
        help='only run game-marked tests for ID (repeatable); portable tests still run')
    parser.addoption(
        '--strict-games', action='store_true', default=False,
        help='fail instead of skip when a selected game fixture or baseline is unusable')


def pytest_configure(config):
    config.addinivalue_line(
        'markers',
        'game(id): optional real-binary test; id selects the fixture '
        '(see docs/fixtures.md)')


def pytest_collection_modifyitems(config, items):
    wanted = set(config.getoption('--game') or [])
    if not wanted:
        return
    keep, dropped = [], []
    for item in items:
        marker = item.get_closest_marker('game')
        if marker is None or not marker.args:
            # Portable tests and unlabelled generic game tests stay available.
            keep.append(item)
        elif str(marker.args[0]) in wanted:
            keep.append(item)
        else:
            dropped.append(item)
    if dropped:
        config.hook.pytest_deselected(items=dropped)
    items[:] = keep


@pytest.fixture
def game_fixture(request):
    """Resolve the fixture named by the closest ``game(id)`` marker."""
    gid = _marker_game_id(request.node)
    fx_mod = _registry_module()
    if fx_mod is None:
        _fail_or_skip(
            request,
            'fixture resolver is unavailable: add tools/ to PYTHONPATH')
    try:
        return fx_mod.resolve(gid)
    except Exception as ex:
        _fail_or_skip(
            request,
            'game fixture %r is unavailable: %s\n'
            '  fix fixtures/registry.json or run `python tools/fixtures.py list`'
            % (gid or '<default>', ex),
            gid)


@pytest.fixture
def game_id(game_fixture):
    return game_fixture.id


@pytest.fixture
def game_paths(game_fixture):
    return str(game_fixture.metadata), str(game_fixture.binary)


def _load_decompiler(game_paths):
    # A full Limbus load is expensive (tens of seconds and hundreds of MB).
    # Every current game test only reads the immutable fixture, so reuse one
    # loaded corpus for the whole session instead of once per module.
    key = (str(game_paths[0]), str(game_paths[1]))
    if key not in _IL_CACHE:
        from corpus_common import load
        metadata, binary = game_paths
        _IL_CACHE[key] = load(ROOT, metadata, binary)
    from il2cpp import Decompiler, Lifter
    il = _IL_CACHE[key]
    return il, Decompiler(Lifter(il))


@pytest.fixture
def raw_game_decompiler(game_paths):
    """Load a fixture without a build-fingerprint check (invariant tests)."""
    return _load_decompiler(game_paths)


@pytest.fixture
def game_decompiler(baseline_game_decompiler):
    """Default game fixture: current build must match the reviewed baseline."""
    return baseline_game_decompiler


@pytest.fixture
def baseline_game_decompiler(game_fixture, game_paths, request):
    """Load a fixture only when it matches its reviewed build baseline."""
    from game_baselines import BASELINES
    metadata, binary = game_paths
    pinned = BASELINES.get(game_fixture.id)
    if pinned is None:
        _fail_or_skip(
            request,
            "no build baseline for game %r; add it to tests/game_baselines.py"
            % game_fixture.id, game_fixture.id)
    actual = (_sha256_cached(metadata), _sha256_cached(binary))
    expected = (pinned['metadata_sha256'], pinned['binary_sha256'])
    if actual != expected:
        _fail_or_skip(
            request,
            "game %r is pinned to a different build "
            "(metadata %s..., binary %s...; this fixture is metadata %s..., "
            "binary %s...). Re-pin only after a clean gated build."
            % (game_fixture.id, expected[0][:12], expected[1][:12],
               actual[0][:12], actual[1][:12]), game_fixture.id)
    return _load_decompiler(game_paths)


@pytest.fixture
def game_tree(game_fixture, request):
    """Return a built tree whose MANIFEST.json matches the active fixture."""
    fx_mod = _registry_module()
    tree = fx_mod.out_tree(game_fixture, os.environ.get('IL2CSHARP_LABEL'))
    if not fx_mod.tree_is_built(tree):
        _fail_or_skip(
            request,
            "game %r has no built tree at %s; build one with "
            "`python il2csharp.py --fixture %s --label <name>`"
            % (game_fixture.id, tree, game_fixture.id), game_fixture.id)
    manifest_path = Path(tree) / 'MANIFEST.json'
    if not manifest_path.is_file():
        _fail_or_skip(
            request,
            "game %r tree %s has no MANIFEST.json; rebuild it with --fixture "
            "so the build identity is recorded" % (game_fixture.id, tree),
            game_fixture.id)
    try:
        manifest = json.loads(manifest_path.read_text(encoding='utf-8'))
    except (OSError, ValueError) as ex:
        _fail_or_skip(
            request,
            "could not read %s: %s" % (manifest_path, ex),
            game_fixture.id)
    actual = (_sha256_cached(game_fixture.metadata),
              _sha256_cached(game_fixture.binary))
    expected = (manifest.get('metadata_sha256'), manifest.get('binary_sha256'))
    if expected != actual:
        _fail_or_skip(
            request,
            "game %r tree %s belongs to a different build "
            "(manifest metadata %s..., binary %s...; fixture is metadata %s..., "
            "binary %s...); rebuild the tree"
            % (game_fixture.id, tree,
               (expected[0] or '?')[:12], (expected[1] or '?')[:12],
               actual[0][:12], actual[1][:12]), game_fixture.id)
    return Path(tree)
