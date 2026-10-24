# Limbus v39 fixture and test migration (2026-10-24)

This is a stop record for the fixture/test migration, not a future update
procedure. The suite now treats a game as a marker-selected fixture rather
than as an ambient `IL2CSHARP_METADATA`/`IL2CSHARP_BINARY` pair.

## Archived build

The test fixture is the immutable copy under
`fixtures/limbus/builds/limbus-v39-20261022/`:

| file | size | SHA-256 |
|---|---:|---|
| `global-metadata.dat` | 49,425,156 | `e17855a55a3f8bcd0245cffbba1d6482b26b07177dffab9bd3ec98b50d8151a7` |
| `GameAssembly.dll` | 164,042,752 | `e6312d9298d823b8ef17aef604136520191fd2d5d11ff524ad4474dbbc38d73e` |

`BUILD.json` records the Steam source paths and capture date;
`SHA256SUMS.txt` repeats the hashes. The registry entry `limbus` points at
this archive. `limbus-live` points at the Steam install and is only for
noticing an update; tests must not use it.

`tests/game_baselines.py` pins the same pair. `game_decompiler` and
`baseline_game_decompiler` are baseline-guarded; `raw_game_decompiler` is for
metadata/layout invariants that intentionally run before a build is pinned.

The gate tree used for this stop record is the scoped tree
`out/limbus/v39-gates/` (label `v39-gates`, only `mscorlib` and
`Unity.Burst.Unsafe`), because those are the images the compile and declaration
gates need. A full-tree build is not claimed here.

## Why the old game tests are not Limbus tests

The 259 existing game tests target the older sample game. Their ground truth
names classes such as `InventoryManager`, `PlayerLobbyHandler`,
`AudioVolumeSliders`, `FPSDisplay`, and `LagCompensationUtils`. Those classes
are absent from Limbus v39 metadata; Limbus has `RPGSystem.RpgInventoryManager`
and a different gameplay tree. Re-pointing the old MethodDef rows by number
would assert unrelated methods, and there is no local copy of the old fixture
to re-freeze them against.

They are therefore marked `pytest.mark.game("shiftatmidnight")`, not
`limbus`. They remain available for a machine that registers that fixture, but
skip cleanly here. No old golden or MethodDef pin is silently reused as a
Limbus pin.

## Current Limbus tests

The `limbus` marker selects 21 tests:

- 13 existing build-independent checks: type sizes, BSS ambiguity, list/
  dictionary layout, CLI no-match behavior, real-SDK compile gates (small
  image green; mscorlib xfail below), declaration gate, and serial-vs-parallel
  build byte identity.
- 8 focused v39 checks in `test_game_limbus_fixture.py` and
  `test_game_limbus_decompile.py`: archived metadata shape, exact fixture
  fingerprints in `MANIFEST.json`, and body text for `DungeonProgress`,
  `RpgInventoryManager`, and the story-return handler.

The Limbus mscorlib compile gate is an explicit xfail: it reports 2,243 syntax
errors, dominated by a recurring dangling `else if` shape (CS8641/CS1525/
CS1003/CS1002/CS1026). That is a real emitter finding for this fixture, not a
fixture-resolution failure. `Unity.Burst.Unsafe` compiles with zero syntax
errors and keeps the Roslyn ingest proof green.

`tests/game_support.py` looks methods up by type/name/arity so a repeated test
does not depend on a bare positional row. The body assertions still rely on
the archived build, exactly like any golden.

## Commands

```text
python -m pytest -q -m "not game"
python -m pytest -q --game limbus
python -m pytest -q --game limbus --strict-games
python -m pytest -q --game shiftatmidnight   # skips without that fixture
```

`IL2CSHARP_LABEL=v39-gates` selects the built tree for `game_tree` tests in
this record. `--strict-games` fails for selected games only; without `--game`
it applies to all game tests.
