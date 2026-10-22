# Handoff — fixture framework (2026-10-22)

Session goal: stop sprinkling "local-only" notes on the docs and instead
**normalise how real games, local (uncommitted) builds, and probes are used**,
so future open-source IL2CPP games drop in without new one-off annotations.

All work is **staged in the working tree, not committed**. One `git status`
block at the end lists it. Nothing under `il2cpp/` changed behaviour except
three additive CLI flags.

---

## 1. What now exists (the new contract)

```
fixtures/
  registry.example.json   tracked  — schema + 2 worked examples
  registry.json           IGNORED  — this machine's real paths
  <id>/game/              IGNORED  — the unpacked game
out/
  <id>/<label>/           IGNORED  — one build + MANIFEST.json
validation_reports/<id>/  tracked  — <label>.<gate>.json summaries only
```

Entry points (all resolve paths through `tools/fixtures.py`, none hard-code a
game):

| command | does |
|---|---|
| `python tools/fixtures.py list` | every fixture: version, licence, tree state |
| `python tools/fixtures.py doctor --id <id>` | probes metadata/Unity version, image/method counts, **and runs the real registration load** |
| `python il2csharp.py --fixture <id> --label <name> [--only A] [--strict]` | build into `out/<id>/<name>/`, writes `MANIFEST.json` |
| `python tools/gate.py {brace,parse,sweep,compile,decl} --fixture <id> --label <name>` | the five gates, uniform interface |
| `python tools/gates/compare_trees.py A B [--scope X]` | file-set + per-file-hash tree diff |
| `python tools/promote.py --fixture <id> --candidate L --baseline B [--move]` | promotion proof (sha256 per file + aggregate); `--move` gated |

`--fixture/--label` are accepted **before or after** the subcommand (the argv
is hoisted). Legacy `python il2csharp.py <gamedir> -o <out>` and
`IL2CSHARP_METADATA`/`IL2CSHARP_BINARY` still work unchanged.

### What was newly written vs. re-used
- **New:** `tools/fixtures.py`, `tools/gate.py`, `tools/gates/tree_brace_audit.py`,
  `tools/gates/compare_trees.py`, `tools/promote.py`, `fixtures/registry.example.json`,
  `docs/fixtures.md`, `tests/test_fixtures_registry.py`.
- **Re-used (already existed, now fronted by `gate.py`):** `tools/validate_corpus.py`
  already had `parse`/`sweep`/`compare` — these *are* the old `work/lib/ts_gate.py`,
  `sweep_audit.py`, `gate_diff.py`. `tools/compile_gate.py` is the `compile` gate.
  So the "missing `work/lib` tooling" was mostly already shipped, just unused.

## 2. Files changed by area

| area | change |
|---|---|
| `.gitignore` | added `fixtures/**` (+ `!fixtures/registry.example.json`), `out/`, `*.manifest.json` |
| `il2cpp/cli.py` | **additive**: `--fixture`, `--label`, and a `MANIFEST.json` writer (`_write_manifest`). Manifest records source commit + per-file sha256, flags, metadata/binary sha256, counts. Default output unchanged; manifest only written on a real build. |
| `tests/conftest.py` | new `fixture_paths()` / `fixture_paths_or_skip()` / `out_tree()` / `out_tree_or_skip()` |
| `tests/test_game_goldens.py`, `test_game_fix133_*`, `test_game_decl_gate.py`, `test_game_compile_gate.py`, `test_game_cli_only.py`, `test_game_parallel_build.py` | resolve the fixture/registry instead of `testgame`/`final_out`/env-only; **skip** (not fail) when absent |
| `pytest.ini` | `game` marker reworded, added `fixture` marker |
| `docs/probes/*.py` (9) | dropped hard-coded `E:\...\limbus_out1` and `C:\Program Files\...\Limbus`; new bootstrap takes a tree from `argv[1]`/`IL2CSHARP_TREE` and a game from `IL2CSHARP_GAME`, else the default fixture |
| `validation_reports/*.json` (58) | `C:\Users\crax\Downloads\il2csharp` → `<repo-root>` (63 subs) |
| `validation_reports/SHA256SUMS.txt` | rebuilt over the 542 files that exist (was 12,638 rows, ~12,400 dead) |
| `tools/compile_gate.py`, `compile_corpus.py`, `csharp_smoke.py`, `gate.py` | pinned `encoding='utf-8'` on `subprocess.run(text=True)` — fixes a real GBK-locale crash on Chinese Windows |
| `README.md`, `CLAUDE.md`, `AGENTS.md`, `docs/README.md`, `docs/public_release.md`, `validation_reports/README.md` | rewritten to the fixture contract |
| `docs/todo.md` + 28 historical docs | one "local-only paths" banner each; bodies byte-identical otherwise |

## 3. Verification (all green at hand-off)

```
compileall il2cpp + tools .......... exit 0
pytest -m "not game" ............... 1374 passed, 271 deselected   (was 1367; +7 new)
tools/verify_release.py ............ 542 files checked; 0 failures (was ~12,400 fail)
fixtures.py list / doctor limbus ... OK (metadata v39, 51,032 types, 299,371/319,100 native)
gate.py brace --fixture limbus --label smoke ... ran on a real build
gate.py parse ... 0 bad on the smoke image; gate.py compile ... reports real syntax errors
promote.py report/--move ........... exercised on two labels
game tests with unresolvable fixture ... 5 skipped, 0 failed  (fresh-clone behaviour)
absolute host paths in tracked files ... 0
```

Line-ending contract holds: `il2cpp/*.py` and `tools/*.py` are CRLF no-BOM,
`tests/*.py` and `*.md` are LF, JSON CRLF (all re-checked).

## 4. Things a next session must know

1. **`fixtures/registry.json` is per machine and git-ignored.** It currently
   holds `limbus` (proprietary — `redistributable: false`). A fresh clone has
   only `registry.example.json`; `tools/fixtures.py list` will say "no
   fixtures registered" until a registry is created. That is intended.
2. **Never commit output from a `redistributable: false` fixture.** During this
   session `validation_reports/limbus/` was produced by the smoke gates and then
   **deleted** before hand-off. Do the same for any proprietary run: keep the
   numbers in a local note, not in the repo. Only redistributable fixtures
   (e.g. an open-source game) may gain a tracked `validation_reports/<id>/`.
3. **The Limbus fixture updated mid-session.** `GameAssembly.dll` is
   2026-10-22 13:20 (164,042,752 B) and `BepInEx/decrypted-metadata.dat` is
   2026-10-22 22:55 (49,425,156 B; v39, 51,032 types). A stale metadata against
   a newer DLL fails registration lookup — `tools/fixtures.py doctor` catches
   exactly that, which is why it exists. If registration ever fails again,
   refresh **both** files together first.
4. **`docs/probes/*.py` were repointed but not re-validated against data.**
   They compile and `brace_audit.py` runs on a tree; the others need a specific
   tree/game to produce their historical numbers.
5. **Goldens are still one file** (`tests/goldens_review84.json`) for one
   fixture. `docs/fixtures.md §7` states the convention: each new fixture gets
   `tests/goldens_<id>.json`. Not yet wired into discovery — do that when the
   second fixture arrives.
6. **`sim_rewrite.py` / `make_sim_base.py` / `classify_into2.py` were NOT
   rebuilt** (they are machine-local simulators; the docs now say so). If a
   future session needs the fast `_final_text` sim loop, that is new work.
7. `docs/fixtures.md` is the single source of truth. Keep it current when the
   registry schema or gate matrix changes.

## 5. Staged change set (uncommitted)

```
 M .gitignore  AGENTS.md  CLAUDE.md  README.md  pytest.ini  il2cpp/cli.py
 M docs/*  (40 files: rewritten or banner)
 M tests/* (7 files: conftest + 6 game tests)
 M tools/compile_gate.py compile_corpus.py csharp_smoke.py
 M validation_reports/* (60 files: 58 JSON + README + SHA256SUMS)
?? fixtures/registry.example.json   (staged: A)
?? docs/fixtures.md  tools/fixtures.py  tools/gate.py  tools/promote.py
?? tools/gates/  tests/test_fixtures_registry.py
```

Recommended next steps, in order: (a) review the diff of `il2cpp/cli.py` (the
only runtime-adjacent change), (b) run `python -m pytest -q` once with the
Limbus fixture registered to confirm the game tests (64 goldens) still pass on
the *new* DLL/metadata — they were **not** run this session because the fixture
changed under us and goldens are pinned to the old hashes, (c) commit.

## 6. Continuation 2026-10-23

(a) `il2cpp/cli.py` reviewed: the fixture resolution and manifest writer are
additive; no runtime path changed without `--fixture`/`--label`.

(b) Verification against the new Limbus build found and fixed four framework
bugs before the suite could be trusted:

- `tools/fixtures.py doctor` documented `--id X` but only accepted the
  positional `doctor X`; both forms now work, and an unknown id is an error
  (not a traceback). Test added.
- `out/<id>/` exists as soon as anything touches it, so tests and gates
  treated an empty directory as a built tree. `tree_is_built()` now requires
  at least one emitted `.cs`; gates refuse an empty tree and tests skip.
- `out_tree()` chose the lexicographically last label, not the newest;
  it now uses directory mtime, as documented. Tests added.
- `_probe_versions()` read only the first 64 MB, so the Unity version at
  142 MB in the current `GameAssembly.dll` was invisible; it now scans in
  chunks. `doctor --id limbus` reports `unity_version: 6000.3.12f1`.

`test_game_parallel_build` compared `MANIFEST.json` byte-for-byte even though
the manifest records `--workers` and elapsed time by design. It now compares
all emitted files byte-for-byte and the stable manifest fields separately
(source hashes, fixture hashes, flags minus `workers`, counts).

The 64 golden pins **cannot pass on the 2026-10-22 build**: MethodDef rows are
positional and all 64 indices now resolve to different methods. The old
metadata/binary pair is not on disk. Rather than silently failing 263 tests,
`game_decompiler` now skips with both fingerprint pairs in the reason; fix 133
does the same. The goldens themselves were not regenerated — that still needs
an explicit user call after a clean gated build. `docs/fixtures.md §7` records
the policy.

Final verification on this machine:

```
python tools/fixtures.py doctor --id limbus ... v39, 51,032 types,
  319,100 methods, 299,371 native, unity 6000.3.12f1, load OK
python -m pytest -q ................ 1380 passed, 268 skipped (14m10s)
python il2csharp.py --fixture limbus --label smoke-verify \
  --only Unity.Burst.Unsafe --strict ... rc=0, MANIFEST written
gate.py brace / parse on that tree .... 0 unbalanced / 0 bad
python tools/verify_release.py ........ 550 files checked, 0 failures
```

The 268 skips are the 64 golden rows, fix 133 (3), the two tree-gated tests,
and the other game tests that share the pinned fixture. The parallel-build
and CLI-only game tests ran for real and passed.
