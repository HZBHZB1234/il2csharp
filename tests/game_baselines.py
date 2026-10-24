"""Reviewed build fingerprints for game tests.

Only hashes and version facts belong here. Game paths stay in the local,
git-ignored ``fixtures/registry.json``.

A test that indexes MethodDef rows or asserts body text uses
``baseline_game_decompiler`` (or its ``game_decompiler`` alias) and is skipped
(or failed with ``--strict-games``) when the active fixture does not match this
table. Tests that only assert build-independent invariants use
``raw_game_decompiler`` and can run against any fixture of the same game.
"""

BASELINES = {
    "limbus": {
        "metadata_sha256": "e17855a55a3f8bcd0245cffbba1d6482b26b07177dffab9bd3ec98b50d8151a7",
        "binary_sha256": "e6312d9298d823b8ef17aef604136520191fd2d5d11ff524ad4474dbbc38d73e",
        "metadata_version": 39,
        "unity_version": "6000.3.12f1",
    },
}
