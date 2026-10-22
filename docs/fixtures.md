# Fixtures, output trees, and gates

This document is the single source of truth for how `il2csharp` is run against
real IL2CPP games and how its output trees are validated. It replaces the old
`work/lib/*` scripts and the hand-typed paths that used to live in
`CLAUDE.md`/`AGENTS.md`.

Nothing in this repository hard-codes a game path. Real games, their built
output trees and any scratch probes live **outside git**; the repository holds
only the tooling and the schemas.

## 1. Layout

```
fixtures/
  registry.example.json    tracked: the schema + two worked examples
  registry.json            IGNORED: this machine's real paths
  <id>/game/               IGNORED: the unpacked game (metadata + binary)
out/
  <id>/<label>/            IGNORED: one build; carries MANIFEST.json
validation_reports/
  <id>/<label>.<gate>.json tracked: small gate summaries only
```

`.gitignore` ignores `fixtures/**` (except `registry.example.json`) and `out/`.
`tests/test_fixtures_registry.py` proves both rules. A directory counts as a
built tree only when it holds at least one emitted `.cs` file: `out/<id>/`
appears as soon as any command touches it, which must not make an empty
namespace look like a valid build to a gate or a test.

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

## 4. Gates

All gates go through one entry point and address their input by fixture:

```text
python tools/gate.py brace   --fixture limbus --label r11
python tools/gate.py parse   --fixture limbus --label r11
python tools/gate.py sweep   --fixture limbus --only Assembly-CSharp
python tools/gate.py compile --fixture limbus --label r11 --only mscorlib
python tools/gate.py decl    --fixture limbus --label r11 --only Unity.Burst.Unsafe
```

(`--fixture/--label` may be written before or after the subcommand.)
Each writes `validation_reports/<id>/<label>.<gate>.json` unless `--report`
is given, and exits non-zero on failure.

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
python tools/gates/compare_trees.py out/limbus/r11 out/limbus/r12 --scope Assembly-CSharp
python tools/promote.py --fixture limbus --candidate r12 --baseline r11
python tools/promote.py --fixture limbus --candidate r12 --baseline r11 --move
```

`compare_trees.py` reports file-set and per-file differences (there are no
default trees; both must be given). `promote.py` writes a per-file sha256 proof
and aggregate digest, and only replaces the baseline with an explicit `--move`;
it refuses to promote a candidate that silently drops files.

## 6. Tests

`tests/conftest.py` exposes `fixture_paths()` / `fixture_paths_or_skip()` and
`out_tree()` / `out_tree_or_skip()`. Game-marked tests skip with an actionable
message when no fixture or tree is present, so a fresh clone is
`pass + skip`, never `fail`:

```text
python -m pytest -q -m "not game"      # portable only, no game needed
python -m pytest -q                    # + game tests (skip if no fixture)
```

Point a run at a specific fixture with `IL2CSHARP_FIXTURE`, and at a specific
tree label with `IL2CSHARP_LABEL`.

## 7. Goldens

`tests/goldens_review84.json` is the hash-only snapshot set for the fixture it
was frozen against (`limbus`/the original licensed build). MethodDef rows are
positional, so a game update invalidates every pin at once: when the registered
metadata/binary fingerprints differ from the golden's, the game tests now
**skip with the two fingerprint pairs in the reason** instead of failing on
unrelated indices. A new fixture adds its own `tests/goldens_<id>.json`;
regenerate with `tools/make_goldens.py` only after a gated build, and never
commit a body-bearing (`--full`) file.

## 8. Archived probes

`docs/probes/*.py` are historical scratch analyses. They no longer carry
absolute paths: each takes a tree from `argv[1]` or `IL2CSHARP_TREE` (falling
back to the default fixture's newest tree) and a game directory from
`IL2CSHARP_GAME` (falling back to the default fixture). They are not tests.
