"""Fixture registry: local-only game fixtures, resolved by id, never by path.

A "fixture" is one real IL2CPP game this machine has on disk: its game
directory, the metadata/binary pair, and the licensing facts that decide
whether any output from it may ever be committed. Paths live in
``fixtures/registry.json`` (git-ignored); the tracked
``fixtures/registry.example.json`` is the schema template.

Nothing in the repository ever hard-codes a fixture path. Tests, gates and
probes all go through this module::

    from fixtures import resolve, out_tree          # tools/ on sys.path
    fx = resolve('limbus')                           # or resolve() for default
    tree = out_tree(fx, 'r11')                       # out/limbus/r11

Compatibility: ``IL2CSHARP_METADATA`` / ``IL2CSHARP_BINARY`` still work and
take priority over the registry, so every pre-existing command and doc that
uses them keeps running unchanged.
"""
import json
import os
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
FIXTURES_DIR = REPO_ROOT / 'fixtures'
REGISTRY_PATH = FIXTURES_DIR / 'registry.json'
EXAMPLE_PATH = FIXTURES_DIR / 'registry.example.json'
OUT_ROOT = REPO_ROOT / 'out'

ENV_FIXTURE = 'IL2CSHARP_FIXTURE'
ENV_LABEL = 'IL2CSHARP_LABEL'
ENV_METADATA = 'IL2CSHARP_METADATA'
ENV_BINARY = 'IL2CSHARP_BINARY'


class FixtureError(Exception):
    """Raised with an actionable message; never a bare KeyError."""


class Fixture:
    """One resolved fixture. Every path is absolute and validated."""

    __slots__ = ('id', 'game_dir', 'metadata', 'binary', 'metadata_version',
                 'unity_version', 'license', 'source_url', 'redistributable',
                 'notes', 'entry')

    def __init__(self, fid, entry):
        self.id = fid
        self.entry = entry
        self.notes = entry.get('notes') or ''
        self.license = entry.get('license') or 'unknown'
        self.source_url = entry.get('source_url') or ''
        self.redistributable = bool(entry.get('redistributable', False))
        game = entry.get('game_dir')
        if not game:
            raise FixtureError(
                "fixture '%s' has no game_dir; add it to %s" % (fid, REGISTRY_PATH))
        self.game_dir = Path(_abs(game)).expanduser()
        if not self.game_dir.is_dir():
            raise FixtureError(
                "fixture '%s': game_dir does not exist: %s\n"
                "  fix the path in %s, or run `python tools/fixtures.py list`"
                % (fid, self.game_dir, REGISTRY_PATH))
        self.metadata = self._resolve_file(entry.get('metadata'), 'metadata')
        self.binary = self._resolve_file(entry.get('binary'), 'binary')
        self.metadata_version = entry.get('metadata_version')
        self.unity_version = entry.get('unity_version')

    def _resolve_file(self, value, label):
        """Accept a game-dir-relative or absolute path; require existence.

        A relative entry is always relative to this fixture's game_dir, never
        to the repo root, so one registry stays valid when the whole tree
        moves. An absolute entry is used verbatim.
        """
        if not value:
            raise FixtureError(
                "fixture '%s' has no %s; add it to %s"
                % (self.id, label, REGISTRY_PATH))
        path = Path(os.path.expanduser(os.fspath(value)))
        if not path.is_absolute():
            path = self.game_dir / path
        if not path.is_file():
            raise FixtureError(
                "fixture '%s': %s file does not exist: %s" % (self.id, label, path))
        return path

    def describe(self):
        return {
            'id': self.id,
            'game_dir': str(self.game_dir),
            'metadata': str(self.metadata),
            'binary': str(self.binary),
            'metadata_version': self.metadata_version,
            'unity_version': self.unity_version,
            'license': self.license,
            'redistributable': self.redistributable,
        }

    def __repr__(self):
        return '<Fixture %s v%s>' % (self.id, self.metadata_version or '?')


def _abs(value):
    """Expand ~ and make absolute against the repo root when relative."""
    path = Path(os.path.expanduser(os.fspath(value)))
    if not path.is_absolute():
        path = (REPO_ROOT / path)
    return str(path)


def load_registry():
    """Return the raw registry dict, or {} when absent.

    An absent registry is the normal fresh-clone state: no error, no fixture.
    """
    if not REGISTRY_PATH.is_file():
        return {}
    try:
        data = json.loads(REGISTRY_PATH.read_text(encoding='utf-8'))
    except (OSError, ValueError) as ex:
        raise FixtureError('could not read %s: %s' % (REGISTRY_PATH, ex))
    if not isinstance(data, dict) or 'fixtures' not in data:
        raise FixtureError(
            '%s must be an object with a "fixtures" mapping; '
            'copy fixtures/registry.example.json as a starting point'
            % REGISTRY_PATH)
    return data


def available():
    """Every fixture that resolves cleanly on this machine."""
    out = {}
    for fid, entry in (load_registry().get('fixtures') or {}).items():
        try:
            out[fid] = Fixture(fid, entry)
        except FixtureError:
            continue
    return out


def unavailable():
    """{id: reason} for registered-but-unusable fixtures."""
    out = {}
    for fid, entry in (load_registry().get('fixtures') or {}).items():
        try:
            Fixture(fid, entry)
        except FixtureError as ex:
            out[fid] = str(ex)
    return out


def resolve(fid=None):
    """Resolve one fixture by id, else by env/default, else the only one.

    An explicit ``fid`` always wins: selecting ``limbus`` must not be silently
    replaced by ambient ``IL2CSHARP_METADATA``/``IL2CSHARP_BINARY``. With no
    explicit id, the legacy environment pair bypasses the registry entirely
    and yields an ad-hoc fixture (id 'env'), so every pre-registry command
    keeps working on machines that never created a registry.
    """
    if fid is None:
        env_meta = os.environ.get(ENV_METADATA)
        env_bin = os.environ.get(ENV_BINARY)
        if env_meta and env_bin:
            entry = {'game_dir': os.path.dirname(os.path.dirname(os.path.dirname(
                os.path.abspath(env_meta)))),
                'metadata': os.path.abspath(env_meta),
                'binary': os.path.abspath(env_bin),
                'notes': 'ad-hoc fixture from %s/%s' % (ENV_METADATA, ENV_BINARY)}
            return Fixture('env', entry)

    registry = load_registry().get('fixtures') or {}
    if fid is None:
        fid = os.environ.get(ENV_FIXTURE) or (load_registry().get('default'))
    if fid is None and len(registry) == 1:
        fid = next(iter(registry))
    if fid is None:
        if not registry:
            raise FixtureError(
                'no fixtures registered. Copy fixtures/registry.example.json '
                'to fixtures/registry.json and point it at a local game '
                '(see docs/fixtures.md).')
        raise FixtureError(
            'multiple fixtures registered but none selected; pass --id or set '
            '%s. Available: %s' % (ENV_FIXTURE, ', '.join(sorted(registry))))
    if fid not in registry:
        raise FixtureError(
            "unknown fixture '%s'; available: %s"
            % (fid, ', '.join(sorted(registry)) or '(none registered)'))
    return Fixture(fid, registry[fid])


def out_root():
    return OUT_ROOT


def out_tree(fx, label=None):
    """The output directory for one fixture + label.

    ``label`` defaults to ``$IL2CSHARP_LABEL``, then to the newest existing
    directory under ``out/<id>/``. Returns a Path that may not exist yet --
    callers decide whether that is an error (gates) or the build target.
    """
    label = label or os.environ.get(ENV_LABEL)
    base = OUT_ROOT / fx.id
    if label is None and base.is_dir():
        labels = [p for p in base.iterdir() if p.is_dir()]
        if labels:
            label = max(labels, key=lambda p: p.stat().st_mtime).name
    return (base / label) if label else base


def tree_is_built(tree):
    """True when a path holds at least one emitted ``.cs`` file.

    ``out/<fixture>/`` exists as soon as any run touches it, so ``is_dir()``
    alone would let a gate pass on an empty namespace and let tests treat the
    parent of a real label as a tree. One emitted source file is the cheapest
    honest signal that a build happened here.
    """
    tree = Path(tree)
    if not tree.is_dir():
        return False
    return next(tree.rglob('*.cs'), None) is not None


def require_tree(fx, label=None):
    """out_tree() plus a hard, actionable error when the tree is missing."""
    tree = out_tree(fx, label)
    if not tree.is_dir():
        raise FixtureError(
            'no output tree for fixture %r%s: %s\n'
            '  build one with: python il2csharp.py --fixture %s --label <name>'
            % (fx.id, ' label ' + repr(label) if label else '', tree, fx.id))
    if not tree_is_built(tree):
        raise FixtureError(
            'output tree for fixture %r%s has no emitted .cs files: %s\n'
            '  build one with: python il2csharp.py --fixture %s --label <name>'
            % (fx.id, ' label ' + repr(label) if label else '', tree, fx.id))
    return tree


def _probe_versions(fx):
    """Fill metadata_version / unity_version by reading the fixture.

    Read-only: parses the metadata header and greps the binary's unity
    version string. Never executes the game binary.
    """
    import re
    import struct
    from pathlib import Path as _P

    info = {}
    try:
        data = _P(fx.metadata).read_bytes()
        version = struct.unpack_from('<I', data, 4)[0]
        info['metadata_version'] = version
    except Exception:
        pass
    # The version string can sit anywhere in a >100 MB binary (Limbus: 142 MB
    # in), so scan in chunks with a small overlap instead of reading a prefix.
    pattern = re.compile(rb'(20\d{2}\.\d+\.\d+[a-z]\d+|6000\.\d+\.\d+[a-z]\d+)')
    tail = b''
    try:
        with open(fx.binary, 'rb') as fh:
            while True:
                chunk = fh.read(8 * 1024 * 1024)
                if not chunk:
                    break
                m = pattern.search(tail + chunk)
                if m:
                    info['unity_version'] = m.group(1).decode('ascii', 'replace')
                    break
                tail = chunk[-64:]
    except Exception:
        pass
    return info


def cmd_list(argv):
    registry = load_registry().get('fixtures') or {}
    default = load_registry().get('default')
    print('registry: %s%s' % (REGISTRY_PATH, '' if REGISTRY_PATH.is_file() else '  (absent)'))
    if not registry:
        print('  no fixtures registered; see docs/fixtures.md')
        return 0
    for fid in sorted(registry):
        entry = registry[fid]
        try:
            fx = Fixture(fid, entry)
        except FixtureError as ex:
            print('  %-18s MISSING  %s' % (fid, str(ex).splitlines()[0]))
            continue
        mark = '*' if fid == default else ' '
        print('  %s%-18s v%-4s %s' % (
            mark, fid, fx.metadata_version or '?', fx.game_dir))
        print('      license=%s redistributable=%s' % (fx.license, fx.redistributable))
        if fx.notes:
            print('      notes: %s' % fx.notes)
        tree = out_tree(fx)
        print('      tree: %s%s' % (tree, '' if tree_is_built(tree) else '  (absent)'))
    print('(* = default; select with --id or $%s)' % ENV_FIXTURE)
    return 0


def cmd_doctor(argv):
    fid = argv[0] if argv else None
    fx = resolve(fid)
    print('fixture          : %s' % fx.id)
    print('game dir         : %s' % fx.game_dir)
    print('metadata         : %s' % fx.metadata)
    print('binary           : %s' % fx.binary)
    print('license          : %s (redistributable=%s)' % (fx.license, fx.redistributable))
    if fx.source_url:
        print('source           : %s' % fx.source_url)
    if fx.notes:
        print('notes            : %s' % fx.notes)
    probed = _probe_versions(fx)
    for key, value in sorted(probed.items()):
        print('%-17s: %s%s' % (key, value,
                               '' if fx.__getattribute__(key) == value
                               else '   (registry says %r)' % fx.__getattribute__(key)))
    # Confirm the real pipeline can load it, without lifting anything.
    sys.path.insert(0, str(REPO_ROOT))
    try:
        from il2cpp import Il2Cpp, Metadata, load_binary
    except ImportError as ex:
        print('load             : SKIPPED (%s)' % ex)
        return 0
    try:
        meta = Metadata(str(fx.metadata))
        bin_ = load_binary(str(fx.binary))
        il = Il2Cpp(meta, bin_)
        il.assign_images()
        il.find_registrations()
        il.load_function_bounds()
        il.resolve_method_addrs()
        n_addr = sum(1 for m in meta.methods if m.addr)
        print('load             : OK')
        print('metadata v%d | %d types | %d methods | %d images | %d literals' % (
            meta.version, len(meta.typedefs), len(meta.methods),
            len(meta.images), len(meta.string_literals)))
        print('native code      : %d/%d methods' % (n_addr, len(meta.methods)))
        il.__dict__.get('_mod_ptr_cache', {}).clear()
    except Exception as ex:
        print('load             : FAILED  %s: %s' % (type(ex).__name__, ex))
        return 1
    return 0


def main(argv=None):
    argv = list(sys.argv[1:] if argv is None else argv)
    import argparse
    ap = argparse.ArgumentParser(
        prog='fixtures',
        description='List and validate local game fixtures (paths never committed).')
    sub = ap.add_subparsers(dest='command', required=True)
    sub.add_parser('list', help='registered fixtures and their state')
    d = sub.add_parser('doctor', help='full profile of one fixture, incl. a real load')
    d.add_argument('id', nargs='?', default=None,
                   help='fixture id (default: registry default)')
    d.add_argument('--id', dest='id_option', metavar='ID',
                   help='same as the positional id')
    args = ap.parse_args(argv)
    try:
        if args.command == 'list':
            return cmd_list([])
        fid = args.id_option or args.id
        return cmd_doctor([fid] if fid else [])
    except FixtureError as ex:
        print('error:', ex)
        return 1


if __name__ == '__main__':
    sys.exit(main())
