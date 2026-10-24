# Fixtures, output trees, gates, and game tests

This document is the single source of truth for how `il2csharp` is run against
real IL2CPP games, how a build is archived for tests, and how the test suite
selects a game. It replaces the old `work/lib/*` scripts and the hand-typed
paths that used to live in `CLAUDE.md`/`AGENTS.md`.

Nothing in this repository hard-codes a game path. Real games, archived
builds, their output trees and scratch probes live **outside git**; the
repository holds only tooling and schemas.

## 1. Layout

```text
fixtures/
  registry.example.json             tracked: schema + worked examples
  registry.json                     IGNORED: this machine's real paths
  <id>/game/                        IGNORED: a live unpacked game
  <id>/builds/<build-id>/           IGNORED: an immutable archived build
    global-metadata.dat
    GameAssembly.dll
    BUILD.json                      provenance + per-file SHA-256
    SHA256SUMS.txt                  copy of the same hashes
out/
  <id>/<label>/                     IGNORED: one build; carries MANIFEST.json
validation_reports/
  <id>/<label>.<gate>.json          tracked: small gate summaries only
```

`.gitignore` ignores `fixtures/**` (except `registry.example.json`) and `out/`.
`tests/test_fixtures_registry.py` proves both rules. A directory counts as a
built tree only when it holds at least one emitted `.cs` file: `out/<id>/`
appears as soon as any command touches it, which must not make an empty
namespace look like a valid build to a gate or a test.

The current Limbus test fixture is the immutable archive
`fixtures/limbus/builds/limbus-v39-20261022/`; the registry entry `limbus-live`
points at the Steam installation and is for update checks only. Never point
the suite at `limbus-live`: a Steam update would silently change every
MethodDef row under the tests. See
[`limbus-v39-test-migration.md`](limbus-v39-test-migration.md) for the
migration record and the kept/skipped split.

## 2. Adding a fixture

1. Unpack (or junction) the game under `fixtures/<id>/game/`. The directory must
   contain a metadata file and a binary; they do not have to be the default
   names (see `limbus` in the example: `BepInEx/decrypted-metadata.dat`).
2. Copy `fixtures/registry.example.json` to `fixtures/registry.json` and add an
   entry:

   ```json
   "mygame": {
     "game_dir": "fixtures/mygame/game",
     "metadata": "Game_Data/il2cpp_data/Metadata/global-metadata.dat",
     "binary": "GameAssembly.dll",
     "license": "MIT (open source, redistributable)",
     "source_url": "https://github.com/...",
     "redistributable": true,
     "notes": "anything a future reader needs"
   }
   ```

   `game_dir` is resolved against the repo root; `metadata`/`binary` are
   resolved against `game_dir`. Absolute paths are used verbatim.
3. `python tools/fixtures.py doctor --id mygame` prints the probed metadata
   version, Unity version, image/method counts and whether the real
   registration pipeline loads it. Fix the registry until `load: OK`.
4. `python tools/fixtures.py list` shows every fixture, its licence, whether it
   resolves, and whether a tree exists.

`redistributable` is not cosmetic: only a `true` fixture may have its output or
counts written into a committed `validation_reports/` file. Licensed games must
stay `false`.

### Archiving a build for tests

A branch or registry entry that points at a live install is not a test
fixture. Copy the pair to a build directory and record provenance:

```text
fixtures/<id>/builds/<id>-<version>-<date>/
  global-metadata.dat
  GameAssembly.dll
  BUILD.json
  SHA256SUMS.txt
```

`BUILD.json` records the source directory, capture date, metadata version,
Unity version, licence, file sizes and SHA-256 hashes. `SHA256SUMS.txt` is the
same hash list in `sha256sum` form. Point the registry at that directory, not
at the live install. `tests/game_baselines.py` records the reviewed pair; a
test fixture must match it, and `game_tree` additionally requires the built
tree's `MANIFEST.json` to match the same pair.

## 3. Building a tree

```text
python il2csharp.py --fixture <id> --label <name> [--only ASSEMBLY] [--strict]
```

- `--fixture` resolves the metadata/binary from the registry; an explicit
  `--target`/`--metadata`/`--binary` still wins, so both styles work.
- `--label` puts the build at `out/<id>/<name>/` and writes `MANIFEST.json`:
  source commit, per-source-file sha256, the exact flags, the metadata/binary
  sha256, and the file/body/failure counts. That manifest is what promotion and
  comparison read later.
- Without `--label`, `--fixture` builds into `out/<id>/` (or `-o`).
- The legacy form `python il2csharp.py <game-dir> -o <outdir>` and the
  `IL2CSHARP_METADATA`/`IL2CSHARP_BINARY` environment variables are unchanged.

The gate tests use `IL2CSHARP_LABEL` to select `out/limbus/<label>/`. Set
`IL2CSHARP_LABEL=v39-gates` for the scoped gate tree used in this migration
(mscorlib + Unity.Burst.Unsafe); a full-tree label can be used once a full
build has its `MANIFEST.json`.

## 4. Gates

All gates go through one entry point and address their input by fixture:

```text
python tools/gate.py brace   --fixture limbus --label v39
python tools/gate.py parse   --fixture limbus --label v39
python tools/gate.py sweep   --fixture limbus --only Assembly-CSharp
python tools/gate.py compile --fixture limbus --label v39 --only mscorlib
python tools/gate.py decl    --fixture limbus --label v39 --only Unity.Burst.Unsafe
```

(`--fixture/--label` may be written before or after the subcommand.)
Each writes `validation_reports/<id>/<label>.<gate>.json` unless `--report` is
given, and exits non-zero on failure.

| gate | what it proves | needs |
|---|---|---|
| `brace` | every emitted file has balanced braces (literal-aware) | the tree only |
| `parse` | every file parses as C# (tree-sitter) | `tree-sitter`, `tree-sitter-c-sharp` |
| `sweep` | every native method lifts in memory without crashing | the fixture |
| `compile` | one image has zero Roslyn *syntax* errors | .NET SDK |
| `decl` | declarations match the metadata dump | the fixture + the tree |

`tree-sitter` is optional (declared in `requirements-dev.txt`); `parse` fails
with a clear message if it is missing. `compile` needs a `dotnet`/Roslyn SDK;
without one the check reports an explicit tool error rather than a false pass.

## 5. Comparing and promoting trees

```text
python tools/gates/compare_trees.py out/limbus/v38 out/limbus/v39 --scope Assembly-CSharp
python tools/promote.py --fixture limbus --candidate v39 --baseline v38
python tools/promote.py --fixture limbus --candidate v39 --baseline v38 --move
```

`compare_trees.py` reports file-set and per-file differences (there are no
default trees; both must be given). `promote.py` writes a per-file sha256 proof
and aggregate digest, and only replaces the baseline with an explicit `--move`;
it refuses to promote a candidate that silently drops files.

## 6. Tests and per-game selection

Each game test module declares exactly which game it needs:

```python
import pytest

pytestmark = pytest.mark.game("limbus")
```

The `game(id)` marker is the single source of truth for both selection and
fixture resolution. Tests without the marker are portable and need no game.
Tests for another game use that game's id; for example, the older sample-game
regressions under `tests/test_game_*.py` are marked `shiftatmidnight` and stay
in the tree for a fixture that is not installed on this machine. They skip with
an actionable reason rather than accidentally running against Limbus.

Commands:

```text
python -m pytest -q -m "not game"                 # portable only
python -m pytest -q --game limbus                 # portable + Limbus
python -m pytest -q --game limbus --strict-games  # fail on missing/mismatched Limbus
python -m pytest -q                               # all; unavailable games skip
```

`--game` is repeatable. `--strict-games` turns a missing fixture, missing
baseline, or tree/manifest fingerprint mismatch into a failure only for the
games selected with `--game`; without `--game`, it applies to every game test.
This is what makes the suite safe on a fresh clone and strict in CI for the
games that are supposed to be present.

Shared fixtures in `tests/conftest.py`:

| fixture | meaning |
|---|---|
| `game_fixture` | registry entry selected by the module's marker |
| `game_id` | its id, e.g. `limbus` |
| `game_paths` | `(metadata_path, binary_path)` |
| `raw_game_decompiler` | loaded `(il, decompiler)` without a baseline check |
| `baseline_game_decompiler` | loaded only when the pair matches `tests/game_baselines.py` |
| `game_decompiler` | baseline-checked alias used by normal game tests |
| `game_tree` | built tree selected by `IL2CSHARP_LABEL`, checked against `MANIFEST.json` and the baseline |

The loaded corpus is cached for the session because a Limbus load is large;
the fixture files are immutable, so tests must treat the object graph as
read-only. Use `raw_game_decompiler` only for metadata/layout invariants that
are supposed to run before a build is pinned; use `baseline_game_decompiler`
for body text.

Method lookups in `tests/game_support.py` use type and name (and arity for
overloads), not a bare MethodDef row. That keeps a repeated test readable and
prevents a row shift from silently selecting an unrelated method. The exact
text is still pinned by the archived fixture and its baseline.

`tests/game_baselines.py` is the reviewed fingerprint table. Add an entry when
a new game/build is intentionally frozen; never update it just to make a
Steam-drifted live install pass.

## 7. Goldens

`tests/goldens_review84.json` is the hash-only snapshot set for the **older
sample game**; it has 64 snapshots and is retained with the
`shiftatmidnight` tests. It is not a Limbus golden set. The current Limbus
migration uses focused body tests (`tests/test_game_limbus_*.py`) plus the
fixture/metadata identity checks instead of pretending the old MethodDef rows
still refer to the same game code.

Per-game goldens follow the same rule as fixtures: add
`tests/goldens_<id>.json`, regenerate it with `tools/make_goldens.py` only
after a clean gated build, review every changed snapshot, and never commit a
body-bearing (`--full`) file. Never generate or re-freeze goldens from inside
pytest.

## 8. Archived probes

`docs/probes/*.py` are historical scratch analyses. They no longer carry
absolute paths: each takes a tree from `argv[1]` or `IL2CSHARP_TREE` (falling
back to the default fixture's newest tree) and a game directory from
`IL2CSHARP_GAME` (falling back to the default fixture). They are not tests.
