# Archived probes

Scratch analysis scripts that produced numbers cited in
`docs/research-2026-10-21-urengine.md` and
`docs/plans/2026-10-21-async-state-machine.md`.

They are LF, run with `PYTHONHASHSEED=0`, and expect the il2csharp
repo root on `sys.path`. They are NOT tests -- no assertion failures
here mean anything; read the printed numbers.

| script | measures |
| --- | --- |
| `urengine_statemachine_tree.py` | Counts state-machine classes in the OUTPUT TREE. Reads 0 because the emitter strips "<>" from identifiers -- kept as the negative control that proves you must query metadata instead. |
| `urengine_statemachine_metadata.py` | Ground truth: queries METADATA for <MethodName>d__N types, MoveNext methods and display classes. This is where the 1,950 / 2,169 / 4,012 numbers come from. |
| `v39_typedef_stride_parity.py` | Proves the width-derived typedef stride is behaviour-neutral on Limbus: re-parses all 51,021 rows with an explicit 82-byte walk and compares every dataclass field (0 mismatches). |
| `v39_codereg_base.py` | Proves Il2CppCodeRegistration starts at codeGenModules_field - 16*8 (17 qwords), which is what the code_reg_va log fix is based on. |
| `v39_string_literal_pool.py` | Settles the string-literal layout: 930,512 is stringLiteralDataSize, 128,500 is stringLiteralSize (the boundary array). |
| `v39_header_structure.py` | Structural validation of the v39 triple-column header: 31 tables, 380-byte header, per-table size/count strides. |
| `brace_audit.py` | Literal-aware brace audit (work/lib/tree_brace_audit.py is absent from this checkout). Used for the 0-unbalanced / 8,583-file result. |
| `audit_quality.py` | Output-quality audit: deterministic 40-file sample of limbus_out1, counts objN / sub_ / goto / (byte*) / unknown density per 100 lines and ranks files. Basis of docs/audit-2026-10-21-output-quality.md. |
| `read_worst_bodies.py` | Prints full bodies from the noisiest files found by audit_quality.py, so the defects can be read rather than counted. |
