## Current work — ACTIVE, resumed 2026-11-03

The user resumed the goal. The pause at round 54 below is historical, not
current status. Start with `docs/handoff-2026-11-03.md` and its continuation.
The goal is **not achieved**; no output promotion or golden re-pin is authorized.

### Read-only next slice: Int32-parameter SIMD origins (2026-11-05)

`game_out56` remains the accepted source candidate, **not promoted**
(source commit `6e4cfac`). No production recovery or repository tests changed
in this follow-up. All **2,242 / 1,936 / 923 selected method bodies** remain
byte-identical to out56, with zero crashes and frozen source checks. This is
not a full-game conversion census.

A private native-origin inventory finds **2 / 138 / 154** same-block
register-MOVD/CVTDQ2PS sites. A bounded backwards predecessor model identifies
**zero / five / one** candidate Int32-parameter origins, in **zero / four /
one methods**: survivors 69879 (two sites), 70773, 70777, 70778; Limbus 35790.
All six agree with the existing typed scalar parameter text, but the current
production field proof correctly declines them. These are research candidates,
not enabled recoveries or whole-method semantic proofs.

Entry origins come from non-byref Int32 metadata and Win64 positional ABI
(including hidden sret/instance shifts), never variable-name inference. Exact
32-bit register copies are followed across all predecessor paths under one
total 512-state budget including the same-block suffix. Volatile registers
cannot carry an origin across calls; nonvolatile copies can. Partial/arithmetic
writers, conflicting roots, loops, unsupported flow and ambiguous/shared or
generic signatures decline. For survivors 70778 the private trace uses **77
backwards states + one suffix state**, with one native entry copy and **13
preserved call states**. RBP is used as a saved integer here; no production
RBP/frame guard has been relaxed. An initially overstrict private probe rejected
terminal INT3 padding; treating only exact INT3 as a no-successor terminal and
rerunning all three fixtures corrects the census, not production code.

**15 authored private specification cases pass** (not added to repository
suite counts). An unchanged production positive-branch sqrt expression from
70778 disagrees with SSE2 Int32-to-Single conversion followed by SSE sqrt on
**12,110 of 110,001** sampled positive inputs. At **16,785,411**, it returns
**4097.0** rather than **4097.00048828125**. An **authored float-snapshot
proposal only** has zero mismatches on the same sample. These checked/optimized,
default-rounding local checks are not game-native execution, negative-helper,
all-FP-mode or whole-method proofs; no production fix, compiler reduction or
speed gain is claimed for this inventory.

Next: independently verify candidate native paths, entry identity, alias writes,
address escapes/exceptional paths and conversion-point expression lifetime;
then prove a snapshot with zero high MOVD lanes. Preserve opaque helper calls.
Do not broaden the field proof, cast unknown/aggregate tokens, increase caps or
relax aggregate/address/overlap, RBP, interface-sret or scalar-home guards. A
source candidate still needs frozen suites, paired trees/compiler diagnostics
and clean-parent behavioral reproduction. Evidence:
`validation_reports/int32_parameter_simd_inventory_2026-11-05.json`.
No goldens/pins changed or promotion; the goal remains **active, unachieved**.

### Recover caller-proved opaque scalar result channels (2026-11-05)

Accepted `game_out56` source candidate (not promoted), versus out55. The
old linear return predictor stops at branches and untyped self-zeroing,
losing native XMM0 results and leaving joined C# floats/doubles unassigned.
A per-method `ScalarResultFlow` fallback now follows the exact owned forward
native CFG only when the old predictor declines. Every reachable continuation
must first consume the result at the same scalar precision. The original
opaque call, arguments and native error handling remain; **no sqrtf identity
recognizer, helper substitution or input-cast repair** was added.

One total **24-instruction-state** budget covers all arms, not 24 per arm.
Exact whole-XMM copies carry the low-lane fact; Win64 XMM6..15 copies survive
direct calls, volatile aliases do not. Backward/external/mid-instruction or
registered-interior targets, ambiguous RAX uses, indirect flow, unproved
exits, mixed precision, packed/high-lane/bitcast/untyped escapes and lost
copies decline. Exact current MethodDef/native-call ownership, real x64 PE,
executable unregistered/non-exported target and uncounted evidence reads are
required. No existing linear predictor, expression cap, double `rt_sqrt` or
aggregate/address/overlap, RBP, interface-sret or scalar-home guard changed.

Frozen sweeps of **2,242 / 1,936 / 923 selected methods** change **one / three /
two methods**, at **six native call sites** (one Double, five Single). Fresh
binary decoding and an independent exhaustive forward-path replay verify all
six sites across 13 paths. Zero crashes, deterministic changed re-lifts, unchanged opaque
call-name/control-token multisets and no new lexical cap-zero markers; these
are not whole-method or execution-count proofs. Limbus 52889 also recovers a
saved scalar across self-zeroing, without a branch.

Both strict sample trees retain **2,227 / 1,857 bodies**, zero failed/fallback/
type-emit failures and clean brace/parse gates. **Four of 767 C# files** change.
Nine real-reference assembly gates remove **four genuine CS0165 sites**:
survivors Assembly-CSharp **3,769 -> 3,766**, UniTask **4,541 -> 4,540**; the
other seven error totals are unchanged. The sole added message pairs with a
removed CS0103: the same still-undeclared return placeholder changes obj17 to
obj16 on an identical normalized line, not a new error site. Untouched-file
location-aware diagnostic multisets remain identical; all-file multisets do
not. Real Editor/BCL/netstandard2.1 and player-package references, original
assembly names, no self reference or synthetic stubs remain. UniTask.Linq's
body sentinel is still absent; its body compilation remains unproved.

**63 new portable + three new game cases**. Frozen portable **4,807 passed**;
full excluding parallel **4,922 passed / 259 skipped / one non-strict XPASS /
the original three failures**; parallel **two passed**. Scoped clean-parent
proof on `766c8de` reproduces **eight failing / four passing authored legacy
predictor cases**, **three failing game cases**, the 923 parent bodies
byte-identically, and the exact original failure set. The candidate is
restored byte-exactly; no missing-module import is counted as a reproduction.

A checked/optimized production-generated branch, with its original opaque
call and authored effectful helper, passes **140** comparisons of input bits,
returned double bits, call counts and exception propagation. This is neither
game-native helper execution nor whole-method semantic equivalence. Existing
source-lane, phi, aggregate and unknown defects remain; survivors 70778's
Int32 parameter conversion still loses Single rounding. No runtime-speed
improvement, complete method recovery or overall goal completion is claimed.

Evidence: `validation_reports/quality_scalar_result_flow_2026-11-05.json`.
No goldens/pins changed and no promotion. Continue with exact native/type/
lifetime proof for remaining SIMD source origins, not broad casts or caps.

### Read-only next slice: single-precision sqrt-helper ABI (2026-11-04)

`game_out55` remains the accepted source candidate, **not promoted**. No
additional production recovery or tests changed in this inventory. Across
**2,242 / 1,936 / 923 selected methods**, an intentionally incomplete
`sqrtf`/SQRTSS native-shape census finds **zero / one / one candidate
helpers**, with **zero / two / four direct calls** in **zero / two / three
methods**. Decode errors are zero. Candidates are not proved recognizers.

Uncounted observations of the existing handler preserve all five method
bodies byte-identically. **Four of six inputs** are tracked Single; two
still have integer/aggregate-like provenance and must not be fixed by a
numeric cast. **Four calls lose XMM0 and leave an untyped RAX value**, while
two already retain a typed Single XMM0 result under existing heuristics.
Every method has a `sub_` marker, but that method-level observation is not
a count of wholly unresolved sites.

Native review finds two different input lifetimes: survivors spills the
entry value at old RSP+8 and roots from new RSP+0x60 after a 0x58 frame;
Limbus preserves it in XMM2, then roots XMM0. The Limbus MOVSS memory store
matched by the broad census is **zero scratch, not the original input**.
Thus reusing a double spill/opcode/literal signature would not prove the
new contract. NaN tails and domain/error-helper returns need separate proof.

An **authored proposal only**, checked/optimized `(float)Math.Sqrt(x)` and
`MathF.Sqrt(x)`, matches SSE scalar sqrt on **1,004,608 sampled Single bit
patterns**, including sign/exponent/mantissa edges: zero finite/signed-zero,
NaN-classification or sampled payload-bit mismatches. This is not exhaustive,
not production-generated recovery, and does not execute the game CRT helper
or prove its side effects, FP status, special exits or other rounding modes.

Next: prove per-precision identity/input lifetime and return ABI; cover direct
calls and both tail paths, unknown propagation and throw-helper exclusion.
Do not reuse `rt_sqrt` or relax its double-only packed-diamond/high-lane proof;
do not repair the two unproved source lanes by casting. Source-frozen suites,
paired compiler/tree audits and clean-parent reproduction remain mandatory.
Evidence: `validation_reports/single_sqrt_helper_inventory_2026-11-04.json`.
The overall goal remains **unachieved**; no speed/error-count gain is claimed.

### Recover proved GPR-transported Int32-field SIMD conversions (2026-11-04)

Accepted `game_out55` (not promoted), versus out54. A native Int32 field
loaded into a 32-bit GPR, copied by legacy MOVD and converted by CVTDQ2PS
must round to Single before SQRTSS and subsequent float division. The old
survivors method 70595 took the square root of the unrounded integer. At
16,785,411 its result was 4097.0 instead of the native Single-input
4097.00048828125. The conversion-point snapshot now preserves that rounding
and its original evaluation time, plus three positive-zero high lanes.

The same-block proof now finds the exact last GPR-family writer before MOVD
and requires `MOV r32,mem4` from the already-proved reference-instance Int32
field. Both transfers share one 512-instruction contiguous backward budget.
The captured expression must still be exactly the proved receiver-field
expression; typed object/temp/zero tokens do not qualify. Memory writes,
calls/branches, source-XMM and receiver-base alias writes still decline;
GPR writes after MOVD do not change the already-captured XMM bits. Actual
native instruction/list ownership, semantic Int32/non-byref metadata and
all aggregate/address/overlap, RBP, interface-sret and scalar-home guards
remain. No generic GPR, double or expression-budget recovery is enabled.

Production sweeps of **2,242 / 1,936 sample methods** and **923 selected
Limbus methods** change **only survivors 70595**, with one newly accepted
GPR conversion site. Zero crashes, deterministic changed re-lifts, unchanged
call-name/control-token multisets and no new lexical cap-zero markers;
these are not whole-method or execution-count proofs. Both strict trees
retain **2,227 / 1,857 bodies**, zero failed/fallback/type-emit failures and
clean brace/parse gates. **One of 767 C# files** changes. All **nine**
real-reference assembly error totals are unchanged. The only message-aware
pair, **+1/-1 CS0165**, is the existing unassigned joined float renamed
`real1` to `real2`, with identical normalized error context and unchanged
missing definition on the negative sqrt-helper arm. It is not a new error
site. Original assembly identities and real Editor/BCL/netstandard2.1 plus
player-package references remain; UniTask.Linq body compilation is still
unproved because its body sentinel is not observed.

**85 new portable + one new game case**; focused **223 passed**, portable
**4,744 passed**. Frozen full excluding parallel: **4,856 passed / 259
skipped / one non-strict XPASS / the same three existing failures**;
parallel **two passed**. Scoped clean-parent proof on `5cfc8f8` reproduces
**21 failing / 64 passing portable cases**, **one failing game case**, all
923 parent bodies byte-identically, and the exact existing failure set.
The candidate is restored byte-exactly after the scoped stash.

Checked/optimized production-generated clips agree with SSE/SSE2 on
**53,495 lane/division checks** over **4,115 signed Int32 inputs**, plus
**4,115 field-snapshot lifetime checks**, with zero mismatches. A separate
**110,000-positive-input** sqrt check falls from **11,983 parent mismatches
to zero candidate mismatches**. These are local default-rounding hardware
checks, not game-native execution, negative-helper/NaN-payload/all-FP-mode
proof or whole-method equivalence. The method still has unknown/helper,
phi and aggregate defects. No runtime-speed improvement is claimed.

Evidence: `validation_reports/quality_simd_gpr_field_conversion_2026-11-04.json`.
No golden/pin changes or promotion; the overall goal remains **unachieved**.
Next investigate remaining source-lane/type/lifetime and helper-return gaps
with independent native evidence, not broad casts or cap increases. The
field54 acceptance and earlier read-only GPR inventory below are historical
previous-candidate records, not a prohibition on this newly proved subset.

### Previous candidate: proved Int32-field SIMD conversions (2026-11-04)

Accepted `game_out54` (not promoted), versus out52. Legacy memory MOVD
zeroes the high 96 bits, but the scalar expression did not retain that fact;
CVTDQ2PS could leave an integer source feeding native float operations,
including DIVSS rendered as integer division. A new same-block native proof
recognizes only a known reference-instance Int32 field loaded by legacy
four-byte memory MOVD. At CVTDQ2PS it emits a float snapshot and records three
positive-zero high lanes, without changing the MOVD expression's identity.
The snapshot is evaluated at the conversion, not lazily after later field
writes. Int32 is recognized by the metadata primitive enum and non-byref bit,
not raw type-tuple equality (real field attribute/data bits differ).

The proof owns the exact block instruction list and actual native instruction,
scans at most 512 contiguous instructions, rejects calls/branches, intervening
memory writes and source/base alias writes, and requires a plain named CLASS
receiver with no unknown/stack/byte/slice/aggregate provenance. GPR MOVD,
double conversions, flat/cross-block paths and all unproved shapes retain the
old path. No cap increase or aggregate/address/overlap, RBP, interface-sret or
scalar-home guard relaxation. Initial out53 integration wrongly treated
`_insn`'s always-zero structured index hint as the native position: authored
tests passed but production had zero recoveries. Its evidence is rejected;
out54 finds the real block position, tests fixed hints -1/0/999, and reruns
all production audits, trees and suites.

Production sweeps cover **2,242 / 1,936 sample methods** and a **923-method
Limbus selection**, with **zero / 11 / six unique conversion sites** in
**zero / nine / six changed methods**. All have independent native field/
producer checks, zero crashes, identical changed re-lifts, unchanged call-name
multisets and no new expression-cap-to-zero sites. These lexical checks do
not prove execution counts or whole-method equivalence.

Strict sample trees retain **2,227 / 1,857 bodies**, zero failed/fallback/
type-emit failures, clean brace/parse gates and verified source fingerprints.
**Eight of 767 C# files** change. Nine real-reference assembly gates reduce
survivors Assembly-CSharp **3,780 -> 3,769 errors (-11)**; the other eight
assemblies are unchanged. Message-aware deltas are **11 added CS0165 / 11
removed CS0165 / 11 removed CS0266**. The CS0165 pairs are existing VertexJitter
float temporaries renumbered by nine: every occurrence retains the same line
and normalized read/write context; one column moves because an earlier name
gains a digit. They are not new error sites. Existing hoisted declarations
still lack initializers; later backedge writes remain. CS0266 removals are
nine in VertexJitter and two in TreasurePanel. Unchanged-file location-aware
diagnostic multisets are identical; all-file multisets are not. References
are real Editor/BCL/netstandard2.1 and original player packages, original
assembly identities, no self-reference or synthetic stubs. UniTask.Linq still
has no observed body sentinel; its body compilation remains unproved.

**73 new portable + eight new game cases**; focused **137 passed**, portable
**4,659 passed**. Frozen full excluding parallel: **4,770 passed / 259 skipped /
one non-strict xpassed / the same three existing failures**; parallel **two
passed**. Scoped clean-parent proof on `86eed6d` reproduces **19 failing / 54
passing portable cases**, **eight failing game cases**, all 923 parent bodies
byte-identically and exactly the existing failure set; all four candidate
files restore byte-exact. Goldens/pins unchanged.

Production-generated C# compiles under `/checked+ /optimize+` and matches an
authored SSE2/SSE hardware oracle on **4,115 signed-Int32 inputs / 53,495 float
lane-and-division checks / 4,115 field-snapshot checks**, zero mismatches.
This covers local default-rounding arithmetic and snapshot lifetime, not
native game execution or whole-method equivalence. Some converted values
still have broken downstream aggregate/phi consumers; GPR/double and silent
expression-cap recovery remain open. Limbus has not had a full rebuild.
No measured runtime speed improvement, near-recompilability or overall goal
completion is claimed. Aggregate-only evidence:
`validation_reports/quality_simd_field_conversion_2026-11-04.json`.

Read-only follow-up on accepted `741fe89` finds **zero / one / zero**
GPR-field-origin sites across the same **2,242 / 1,936 / 923 methods**, with
all bodies unchanged and source fingerprints verified. The one site (sample
mi 70595) feeds CVTDQ2PS into SQRTSS: losing the input's Single rounding lets
`Math.Sqrt` consume the original Int32 as Double. A production-generated
authored instruction clip, checked against SSE2-convert/SSE-sqrt hardware on
**110,000 positive inputs**, disagrees **11,983 times**; an authored explicit
float-input proposal has **zero mismatches**. This is default-rounding local
arithmetic evidence, not a new source guard, game execution or whole-method
proof. No GPR/double recovery has been accepted. Evidence and remaining
acceptance gates:
`validation_reports/gpr_field_conversion_inventory_2026-11-04.json`.

Next: extend scalar conversion only with independent native source-lane,
width, metadata-type and lifetime proof; broad GPR/double casts remain
rejected. Separately replace cap-to-zero only at a proved bounded evaluation
boundary before revisiting signed SHR. No promotion.


### Preserve one execution per materialized native call (2026-11-04)

Accepted `game_out52` (not promoted), versus out48. A long call argument was
previously copied into an offline snapshot while the original pending-call
`Expr` remained in predecessor end-state. A later phi use could bind that
original again, executing the same native call twice. The length limiter now
uses the existing definition-site binder for the **exact pending object** and
updates its live references. Equal text from distinct native calls is never
identity evidence. Only non-dry, bindable, known int/float/obj/call values with
a recorded definition position qualify; stack/byte/slice/aggregate provenance
and all unproved shapes retain the old snapshot path. No scalar-home,
RBP-copy, interface-sret or aggregate/address/overlap guard is relaxed.

Production sweeps cover **2,242 / 1,936 native methods**, zero crashes, with
**13 / 77 unique materialized native-call sites** independently checked for
exact pending identity, owning definition block and native CALL instruction.
Final output changes **three / 11 methods**. Changed re-lifts are identical.
The changes remove duplicate Concat, async-pipeline and tween creation calls;
one OnStart result moves back to its definition before the next real call.
A separate **923-method Limbus selection** changes **seven methods / ten
unique materialized calls**, removing **seven extra damage calls and four
extra FormatHelper renderings**, without added call-name multiset entries or
new cap-zero sites. This is not a full Limbus rebuild or whole-method proof.

Strict sample builds retain **2,227 / 1,857 bodies**, zero failed/fallback/
type-emit failures, clean brace/parse gates and verified source fingerprints.
**Seven of 767 C# files** change. Nine real-reference assembly gates report
**five fewer errors**, no message-aware added diagnostics: UniTask -2,
survivors Assembly-CSharp -1 and Assembly-CSharp-firstpass -2. Deleting
statements shifts later diagnostic locations; do not claim all location-aware
multisets match. Unchanged-file location-aware multisets are identical.
References are real Editor/BCL/netstandard2.1 and original player packages,
with original assembly names, no self-reference or synthetic stubs.
UniTask.Linq retains 13 declaration errors and no observed body sentinel;
its body compilation remains unproved.

**19 new portable + nine new game cases**; focused **97 passed**, portable
**4,586 passed**. Frozen full excluding parallel: **4,689 passed / 259 skipped /
one non-strict xpassed / the same three existing failures**; parallel
**two passed**. Scoped clean-parent proof on `7242eb7` reproduces **eight
failing / 11 passing portable cases**, **nine failing game cases**, the
923 parent bodies byte-identically and exactly the existing failure set;
all three candidate files restore byte-exact. Goldens/pins unchanged.

Production-generated materialization and phi statements compile and execute
under `/checked+ /optimize+` in **three authored effect models / 12,306
scenarios / 24,612 effectful calls**, zero mismatches in call multiplicity,
order, equal-text distinct identities, argument lifetime and late-phi value.
No game-native execution, whole-game equivalence or measured runtime speed
improvement is claimed. Aggregate-only evidence:
`validation_reports/quality_materialized_call_identity_2026-11-04.json`.

Next: address `_mk`'s existing expression-length cap, which silently emits a
zero instead of the computation. Signed logical SHR prototypes 49/50/51
remain **rejected**: locally correct formulas expand expressions and create
new downstream cap-zero sites; eager SHR binding alone still leaves two new
regressions. Do not raise the cap or accept a compiler-only improvement.
Process-local budget54 research restores those two computations at bounded,
closed-Int32 CMOV evaluation points, but its type, width and lifetime proof
is incomplete; no such source change is accepted. Its 923-method combined
trial has no new cap-zero sites but seven call-name multiset changes, including
restored Round calls behind an existing unknown condition; those need separate
native execution-count review. Zero cap regressions alone is not acceptance.
Preserve native evaluation order and all aggregate/address guards before
revisiting SHR.

Read-only inventory on accepted source `1046ee6` (no SHR prototype) finds
**zero over-cap expressions in 2,242 / 1,936 sample methods**, and **16 in
16 of the selected 923 Limbus methods**: ten int, three float, three unknown
result kinds. Native producers are 13 CMOV and three ADDSS. The tentative
closed-Int32 register CMOV guard has **zero qualifying sites** on this source;
float kind alone also fails as proof because some operand/result types are
unknown or mismatched. Do not ship an unused guard as a production recovery,
or broaden it from guessed text types. Aggregate-only inventory:
`validation_reports/expression_budget_inventory_2026-11-04.json`.

Naive early
field-to-property renaming and byte casts of native wide stores also remain
rejected. No promotion; the overall goal is **not achieved**.


### Preserve unsigned SETcc/CMOVcc conditions (2026-11-04)

Accepted `game_out48` (not promoted), versus out47. The existing same-block
CMP/CF/ZF proof now also serves SETA/SETAE/SETB/SETBE and
CMOVA/CMOVAE/CMOVB/CMOVBE. Low byte/word/dword register comparisons retain
native unsigned bits via explicit `unchecked` normalization. The real defect
is a signed capacity comparison after doubling a queue count: native CMOVA
caps the unsigned overflow, while the old signed relation could miss it.
A shared static operator table replaces the per-call Jcc table; no speed gain
is claimed. Width, operand-type, contiguous-instruction and flag guards are
unchanged. Flat fallback explicitly clears the width before every unsigned
consumer, not just branches. SETcc's existing flag clearing and CMOV selected
values/partial-register model are unchanged.

Independent native flag/width/block checks over **2,242 / 1,936 methods** find
**four / zero unique recovered sites**, in **two / zero methods**, zero crashes.
Final strict trees change **two of 767 C# files**: exactly **four ternary-condition
line replacements**, unchanged call-name multisets and repeated lifts. Builds
retain **2,227 / 1,857 bodies**, zero failed/fallback/type-emit failures, clean
brace/parse gates and verified final-source fingerprints.

**248 new portable + two new game cases**; focused portable **367 passed**,
focused game **two passed**, portable **4,567 passed**. Frozen full excluding
parallel: **4,661 passed / 259 skipped / one non-strict xpassed / the same three
existing failures**; parallel **two passed**. A five-file scoped clean-parent
proof on `00a6783` reproduces the two methods' four old conditions,
**96 failing positive / 152 passing boundary cases**, and exactly the same
existing failure set; all five files restore byte-exact. Goldens/pins unchanged.

Actual production-generated comparison/selection expressions, compiled with
`/checked+ /optimize+`, match **72 authored Win64 programs / 710,856 CPU calls /
710,856 compiled C# checks**, zero mismatches. No game-native code is executed.
This proves local consumer expressions, not arbitrary partial-register
producers, checked arithmetic in other CMOV branches, or whole-method equivalence.

All **nine complete location-aware compiler diagnostic multisets are identical**
using real Editor/BCL/package references and original assembly identities,
without self-reference or synthetic stubs. UniTask.Linq still has 13 declaration
errors and no observed body sentinel. No compiler-error reduction or runtime
speed improvement is claimed. Aggregate-only evidence:
`validation_reports/quality_unsigned_cmp_consumers_2026-11-04.json`.

Next: investigate readonly property recovery only where the exact closed
receiver has a registered native getter proved to be the same field load and
return. Generic-definition getter addresses are zero; registered instantiations
must be checked individually. Dictionary.Count subtracts two fields and must
not be treated as a direct field alias. This is investigation, not accepted
recovery; writes/addresses, virtual override risks and getter self-recursion
must decline. Keep all scalar-home, RBP-copy, interface-sret and aggregate guards.
Read-only closed-instance inventory finds three / ten candidate loads in one /
eight methods. A three-case authored lifetime probe disproves naive early
`_size` -> `Count` renaming: kill-on-write still keys on the native field text
and fails to freeze the renamed read before a field write. No recovery change
is accepted. Preserve storage identity through an alias-aware or late projection
design before revisiting this candidate. Next alternative: inspect integer RHS
truncation on native byte stores; do not repair wide/unproved loads in textpass.
No promotion; many real compiler errors remain and the goal is **not achieved**.


### Preserve unsigned dword CMP/Jcc relations (2026-11-04)

Accepted `game_out47` (not promoted), versus out46. The same-block native
CMP/CF/ZF proof now also covers low **32-bit registers** with IMMEDIATE32,
sign-extended IMMEDIATE8TO32, or same-width register operands. JA/JAE/JB/JBE
relations normalize operands to `uint` under explicit `unchecked` arithmetic.
This prevents negative async states (including -1/-2) from entering a native
unsigned `state <= 1` branch, and preserves range/hash comparison bits.
Closed primitive integral metadata or integer literals are still required.
Qword/memory/high-byte/prefixed operands, unknown or unsupported types,
clobbered/undefined flags, calls, instruction gaps, cross-block provenance and
flat fallback retain their parent behavior. SETcc/CMOVcc are not changed.

Production sweeps cover **2,242 / 1,936 methods**, zero crashes. Independently
checked unique new dword sites: **28 / 8 in 27 / 4 methods**; repeated lifts are
identical and observations are deduplicated by method/native site. Final output
changes **22 / 2 methods in six of 767 C# files**: exactly **26 if-condition
line replacements**, no statement additions/removals and unchanged call-name
multisets. These are local relation checks, not whole-method equivalence.
FormulaParser still has a wrongly char-typed hash accumulator and other defects.

Strict builds retain **2,227 / 1,857 bodies**, zero failed/fallback/type-emit
failures; brace/parse gates are clean and final-source fingerprints verified.
All **nine complete location-aware compiler diagnostic multisets are identical**
using real Unity Editor/BCL/package references, original assembly simple names,
no self-reference or synthetic stubs. UniTask.Linq still has 13 declaration
errors and no observed body sentinel; its body compilation is not proved.
No compiler-error reduction or speed improvement is claimed.

**59 new portable + three new game cases**, removing two obsolete dword-decline
parameters (net portable +57). Portable **4,319 passed**, focused portable
**119 passed**, focused game **four passed**. Frozen full excluding parallel:
**4,411 passed / 259 skipped / one non-strict xpassed / the same three existing
failures**; parallel **two passed**. Scoped clean-parent proof on `3e6fa4d`
reproduces three real changed method boundaries, **26 failing positive / 33
passing boundary cases**, and exactly the same existing failure set, then
restores all four files byte-exact. Goldens/pins are unchanged.

Actual production-generated comparison expressions compiled with
`/checked+ /optimize+` match **20 authored Win64 programs / 382,592 CPU calls /
382,592 compiled C# checks**, zero mismatches, including sign-extended -1,
all-ones and high-bit immediates. No game-native code was executed. Aggregate-only
report: `validation_reports/quality_unsigned_dword_cmp_2026-11-04.json`.

Next: unsigned SETcc/CMOVcc requires its own consumer/flat-fallback proof;
read-only inventory finds four same-block CMOVA sites in two UniTask methods
and no qualifying survivors sites. This is inventory, not an accepted recovery.
Scalar-home identity/type/address lifetimes remain open. Preserve the RBP-copy
quarantine, interface-sret and all aggregate/address/overlap guards. No promotion;
many real compiler errors remain and the goal is **not achieved**.


### Preserve low-byte/word unsigned CMP semantics (2026-11-04)

Accepted `game_out46` (not promoted), versus out45. A real saved-char range
check lost the native **16-bit unsigned wrap**: the old C# comparison
was then algebraically shortened to an upper-bound-only check, accepting
character values **0 through 47** as digits. Live, same-block low-register
CMP + JA/JAE/JB/JBE now normalizes both operands to byte/ushort under explicit
`unchecked` arithmetic. The existing algebra pass cannot erase that modulo
boundary. Only closed primitive integral types or integer literals qualify.
Memory/high-byte/wide/prefixed compares, signed/equality branches, bool/byref/
enum/pointer/unknown operands, overwritten or undefined CF/ZF, calls, skipped
instruction gaps, replaced flags and cross-block provenance decline.

Final review also exposed a flat-fallback boundary: `Lifter.lift` does not
prove merged native flags at labels. It therefore **keeps the parent spelling**
instead of applying the new rule. Two authored regressions cover straight-line
flat lifting and a mixed-width incoming branch join. No scalar-home, aggregate,
RBP-copy or interface-sret guard is relaxed.

Production sweeps cover **2,242 / 1,936 selected native methods**, zero crashes.
There are **four / one unique recovered branch sites** in **two / one methods**
(unitask mi 30424, 30428; survivors mi 69628). Repeated re-lifts are identical;
call-name multisets are unchanged, not a proof of whole-method equivalence.
The site census deduplicates the repeat-stability observations by method and
native site; the raw observation count must not be read as distinct sites.

Strict builds retain **2,227 / 1,857 bodies**, zero failed/fallback/type-emit
failures, clean brace/parse gates and verified final-source fingerprints.
Only **two of 767 C# files / three methods** change. All **nine complete
location-aware compiler diagnostic multisets are identical** with real
Editor/BCL/package references, original assembly names, no self-reference or
stubs. UniTask.Linq still has 13 declaration errors and no observed body
sentinel. The saved char's object-typed, address-escaping home remains a separate
problem; this method is not yet recompilable. There is no compile-error-count
or speed improvement claimed for this correctness slice.

**62 new portable + one new game cases**; focused **63 passed**, portable
**4,262 passed**. Frozen full excluding parallel: **4,351 passed / 259 skipped /
one non-strict xpassed / the same three existing failures**; parallel **two
passed**. Scoped clean-parent proof on `eb90a3d` reproduces the old conditions
in all three changed methods, **23 failing positive boundary cases** and the
same existing failure set, then restores all six files byte-exact. Goldens and
pins are unchanged. Actual generated comparison expressions compiled with
`/checked+ /optimize+` agree with **16 authored Win64 programs / 300,544 CPU
calls / 300,544 compiled C# checks**, zero mismatches. This is not execution of
game native code, whole-method equivalence or speed evidence. Aggregate-only
report: `validation_reports/quality_narrow_unsigned_cmp_2026-11-04.json`.

Next: prove 32-bit unsigned comparisons separately; a process-local prototype
already exposes signed-state/range/hash comparisons but is **not accepted** and
its output is not production evidence. Stable scalar-home identity/type and
address lifetimes also remain open. Preserve the RBP-copy quarantine and all
address/overlap guards. No output promotion; many real compiler errors remain
and the goal is **not achieved**.


### Independently proved native-CFG block-entry stack frames (2026-11-04)

Accepted `game_out45` (not promoted), versus out44. Both analysis passes now
restore **independently proved entry-relative RSP at each executed block**,
instead of inheriting the previous RPO block's epilogue. A new bounded proof
requires an explicit Win64 x64 PE and an exact original-byte decode, solves
native instruction edges independently of production CFG pruning, and verifies
every executed production-block instruction against the solved state. Its
bounds are **8,192 instructions / 65,536 bytes**. Plain r64 PUSH/POP (not RSP),
signed immediate ADD/SUB RSP and balanced near calls under the Win64 ABI are
supported. Joins must agree; external tails and plain returns restore the
entry offset. EH, unknown/partial RSP writes, indirect branches, conflicting
joins, skipped nonzero stack effects and unproved executed blocks decline.
Declined methods keep the old path. RBP, slot naming, scalar/aggregate assembly
and the interface-sret guard are unchanged; no proof state is cached in Lifter.

Production sweeps cover **2,242 / 1,936 selected native methods**: **1,298 /
793 proved**, **944 / 1,142 declined**, with one survivors method bypassing
general analysis. Independent real-store checks find **zero wrong RSP in
1,459 / 298 stores inside proved methods**. Of the prior **19 / 171** wrong
RSP store observations, **13 / two** observations in **ten / two methods**
are corrected; **six / 169 remain** in declined methods. These are store
observations, not counts of wrong emitted lines or compiler errors.

Only **two of 767 C# files / four methods** change (unitask mi 23044, 23068,
23075; survivors mi 69628). Stack homes recover the original vector members
and saved char parameter. Changed-method call-name multisets are unchanged;
this is not whole-method equivalence evidence. Strict builds retain **2,227 /
1,857 bodies**, zero failed/fallback/type-emit failures, clean brace/parse gates
and verified source fingerprints. With real Editor/BCL/package references,
original assembly names, no self-reference or stubs: UniTask **4,545 -> 4,543**
(four CS0103 removed, **two CS0122 added** at recovered private fields).
Survivors Assembly-CSharp stays **3,781** (two CS0103 removed, **one CS0266 and
one CS0208 added** at an existing object-typed char home). Those methods are
not yet recompilable. All other seven complete location-aware diagnostic
multisets, and every unchanged file's diagnostics, are identical. UniTask.Linq
still has 13 declaration errors and no observed body sentinel.

**71 new portable + four new game cases**; focused **75 passed**, portable
**4,200 passed**. Frozen full excluding parallel: **4,288 passed / 259 skipped /
one non-strict xpassed / the same three existing failures**; parallel **two
passed**. A scoped clean-parent proof on `4255d2f` reproduces incorrect entry
RSP in all four changed methods and exactly those three existing failures,
then restores all four candidate files byte-exact. No goldens/pins changed.
An authored runtime cross-check executes **48 Win64 programs / 1,536 CPU calls /
18,432 stack-coordinate and canary checks**, zero mismatches; not game-native
execution, whole-method equivalence or speed evidence. Aggregate-only report:
`validation_reports/quality_native_cfg_stack_frames_2026-11-04.json`.

Next: prove stable scalar-home identity/type and address lifetimes separately.
A read-only follow-up confirms the saved char already has its metadata type
at the native store, but its slot receives no concrete hint and the existing
prologue-text fallback declines its address escape. Do not simply relax that
guard: prove exact byte ranges, all writes/aliases and whole/scalar overlap
first. Preserve the historical RBP-copy quarantine; the earlier combined
RBP/name experiment duplicated effectful calls and remains rejected. No output
promotion; many real compile errors remain and the goal is **not achieved**.

### Materialized sret immediate-MOV boundary correction (2026-11-04)

Accepted `game_out44` (not promoted), versus out43. New boundary probes exposed
an omission in the previous round: the copy interpreter's immediate-MOV arm
imported `IMM_OPS` from `il2cpp.x64`, where it does not exist, and leaked an
`ImportError`. It now imports the existing set from `il2cpp.runtime.meta`.
No layout, byte-identity, lifetime, alias or interface-sret guard is relaxed.

**36 new authored cases** cover five immediate encodings with zero/one/all-ones
values, unrelated constant writes and source overwrites. Constants never prove
source-byte identity. On clean parent `0262f59`, **all 36 fail with that exact
ImportError**; the corrected focused run is **164 synthetic + two game passed**.
Portable **4,129 passed**; frozen full excluding parallel **4,213 passed /
259 skipped / one non-strict xpassed / the same three existing failures**;
parallel **two passed**. The scoped clean-parent proof reproduces the exact
three-failure set and restores both candidate files byte-exact. No re-pins.

Both strict selected builds retain **2,227 / 1,857 bodies**, zero failed,
fallback or type-emission failures, clean brace/parse gates and verified source
fingerprints. **All 474 / 293 C# files are byte-identical to out43**. All nine
complete real Editor/BCL/package diagnostic multisets, **including source
locations**, are unchanged: this is a latent crash fix, not a compiler-error
reduction. UniTask.Linq still has 13 declaration errors and no observed body
sentinel. An authored native runtime check executes **108 Win64 programs /
3,456 calls / 199,296 byte-identity and canary checks**, zero mismatches.
It is not game-native execution, game-consumer equivalence or speed evidence.
Aggregate-only evidence:
`validation_reports/quality_materialized_sret_immediate_boundary_2026-11-04.json`.

Historical **pre-out45 TEMP-only audit** (the RSP-only fix is above):
independent finite CFG frame-coordinate
analysis over **2,242 / 1,936** selected methods solves **2,056 / 1,876** method
frames, declining unsupported operations/joins (one additional survivors method
bypasses general analysis). At **3,937 / 4,180** supported real stack stores,
**19 / 171** RSP observations in **13 / 22** methods disagree with the native
CFG coordinate; **64 / 309** store observations have multiple home keys sharing
one display name. These observations are not counts of wrong emitted lines or
compiler errors. The eleven-method focused audit separately has correct RSP
at all 64 stores, but still exposes RBP-key/name collisions. A combined
unique-name/RBP-coordinate prototype changes one sampled method and can
introduce repeated effectful call text in reconstructed initializers; do not
land it. Preserve the historical RBP-copy quarantine and interface-sret guard.
Block-entry RSP now has separate out45 evidence above; home names and stable
scalar/whole-value lifetimes remain open. Many errors remain; the goal is
**not achieved**.

### Block-local materialized sret values at exact typed consumers (2026-11-04)

Accepted `game_out43` (not promoted), versus out40. A separate, frozen
whole-value record now retains an **already-emitted typed sret temporary**.
It never re-roots scalar/tile/Expr origins and never turns padding into
initialized-byte evidence. Every execution sink owns its own proof: CFG edges,
backedges, dry/real passes and method reuse cannot propagate it. The retained
sink is released at method/pass entry.

The producer must be an explicit Win64 x64 PE, unique direct canonical
nongeneric MethodDef under nongeneric owners, with a closed nonbyref value
return, recursively proved default layout, existing typed temp and native
size **9..64 bytes**. The consumer has the same canonical/closed signature
requirements and an exact by-value parameter. Independently decode and match
the original bounded native window (**96 post-call instructions / 2,048
bytes**), including a prior exact `LEA RCX,[RSP+disp]` hidden-buffer setup
within 16 instructions. A finite interpreter separates pointer addresses from
original source-byte identities and proves every byte of the final argument
copy, its actual argument register (including receiver/sret shifts) and RSP.
Only explicitly supported MOV/LEA/SSE copy/zero operations qualify; unknown
aliases, calls, CFG edges, RMW, unsupported operations, partial GPRs, scalar
SSE lane merges, non-GPR control/debug registers, indexed/segmented/prefixed
and 32-bit-address evidence decline.

**Lifetime correction:** an existing managed temp is not automatically an
immutable SSA snapshot. After *every* replayed instruction, its original source
home must still contain the complete same-offset byte identity. A saved vector
followed by a source write declines even if the destination is intact or the
source is later restored. Idempotent self-copies remain accepted. This closes
the two authored mutation/recovery counterexamples without weakening the
interface-sret guard or changing scalar fragments, raw partial stores, hints,
slots, variable types or statement order.

Independent production sweeps cover **2,242 / 1,936 selected native methods**:
exactly **two / zero** whole-value consumers, with matching dry/real hits and
no new crashes. Across **474 / 293 C# files**, only **two files / two methods**
change: two field initializers become the existing whole temp; the existing
pipeline also removes one dead scalar field read. Reversing precisely those
changes restores every prior source byte. Real Editor/BCL/package references,
original assembly simple names, no self-reference or type stubs:
`Assembly-CSharp` **1,973 -> 1,969**, exactly **four CS0122 removed / zero added**
at the changed lines. The other eight complete diagnostic multisets are
unchanged. UniTask.Linq retains 13 declaration errors with no observed body
sentinel; this is not body-coverage evidence.

Strict builds: **2,227 / 1,857 bodies**, zero failed/fallback/type-emit failures;
brace/parse clean and source fingerprints verified. **104 new portable / two
new game cases**; focused **128 synthetic + two game passed**, portable
**4,093 passed**. Frozen full excluding parallel: **4,177 passed / 259 skipped /
one non-strict xpassed / three existing failures**; parallel **two passed**.
Scoped clean-parent proof on `14db1ec` repeats exactly those same three failures
and restores all six candidate source/test files byte-exact. No golden/pin
changes or output promotion. The report generator independently verifies the
final test counts, exact failure set, source fingerprints and compiler deltas.

An authored native-copy interpreter cross-check executes **1,024 bounded
Win64 programs / 16,384 CPU calls / 1,120,576 byte-identity and canary checks**,
zero mismatches. A separate authored .NET 10 blittable-value harness checks
16/40-byte private readonly payloads against native copies: **8,654 cases /
244,616 managed byte checks / 261,924 native byte-and-canary checks**, zero
mismatches. Neither executes game-native methods or recompiled game consumers,
validates reference-containing game structs, proves whole-method/game
equivalence, or measures speed. The out41/out42 full runs were deliberately
interrupted for boundary/lifetime repairs; neither exploratory label is an
accepted full-suite result. Many compilation errors remain; the goal is
**not achieved**. Aggregate-only evidence:
`validation_reports/quality_materialized_sret_snapshot_2026-11-04.json`.

Next: retain the interface-sret guard. Generic/shared/indirect calls,
cross-CFG snapshots, unknown alias writes and managed reference-containing
native/.NET execution still require separate proofs. Before broadening this
record, address the upstream scalar/whole home collision behind the remaining
Vector3/awaiter assignments, with an independent field-range proof; never
re-root a partial scalar store onto whole-struct display text.

### Exact native-zero small-struct leaf returns (2026-11-04)

Accepted `game_out40` (not promoted), versus out39. An independent leaf proof
now renders a native small-struct zero as `default(original type)`, rather
than an integer zero or an invented constructor call. It requires an explicit
Win64 PE, canonical owned nongeneric nullary MethodDef, original address
candidate and closed nongeneric non-enum return signature. The entry block and
an independent original-binary decode must agree exactly: **XOR EAX,EAX or
XOR RAX,RAX; plain one-byte RET**, without predecessors or extra instructions.
The uncounted nonunknown RAX Expr and existing literal must agree as zero.

The result has a recursively proved default layout and **one full-width
scalar/reference payload at offset zero**, size one/two/four/eight, no sret,
padding or target cctor. Partial/other-register zeros, MOV-zero, segmented/REP
entries, RET-imm, extra effects, malformed metadata, open/generic/byref,
enum/nested-aggregate and packed/explicit/unknown layouts decline. No ctor is
invoked; private/readonly fields are not assigned by an initializer. Register
Exprs, counted uses, hints, slots, variable types and statement order stay
unchanged; the prior copy-ctor, bool and enum return proofs are untouched.

Independent production sweeps: **2,242 / 1,936 selected native methods**, exactly
**one eight-byte default return / zero**. Across **474 / 293 C# files**, exactly
**one file / one return line** changes; reversing that line restores every old
source byte. Real Editor/BCL/package refs, original assembly simple names,
no self-reference or type stubs: UniTask **4,546 -> 4,545**, exactly **one
CS0029 removed / zero diagnostics added**, at that same return line. The other
eight complete diagnostic multisets are unchanged. UniTask.Linq retains 13
declaration errors and no observed body sentinel; no body-coverage claim.

Strict builds: **2,227 / 1,857 bodies**, zero failed/fallback/type-emit failures;
brace/parse clean and source fingerprints verified. **426 new portable / one
new game case**; focused **652 synthetic + one game passed** (including the
prior 226 synthetic copy-ctor cases), portable **3,989 passed**. Frozen full
excluding parallel: **4,071 passed / 259 skipped / one non-strict xpassed /
three existing failures**; parallel **two passed**. Scoped stash proof on
clean `5a434de` reproduces exactly the same three failures and restores the
four candidate files byte-exact. No golden/pin changes or output promotion.

An authored Win64 native/.NET 10 harness compares four EAX/RAX self-XOR
encodings, arbitrary incoming 64-bit values, twelve boundaries and 4,096
deterministic random seeds against seventeen private readonly scalar/reference
managed defaults, checked/unchecked, with native canaries: **558,688 checks /
zero mismatches**. Explicit side-effecting parameterless ctors run **zero**
times. This is not game-native execution, whole-method/game equivalence or
speed evidence; concurrent build/test times are not a performance comparison.
Many compilation errors remain and the goal is **not achieved**.
Aggregate-only evidence:
`validation_reports/quality_leaf_struct_zero_return_2026-11-04.json`.

Next **TEMP-only / not accepted**: the interface-sret guard remains intact.
Tracing the unsafe guard-removal prototype locates the first stale value
before local renaming: the returned stack value is split into fields; a later
whole SIMD reload through the echoed pointer has only those field fragments,
and its empty display text is filled using the instruction displacement rather
than the resolved stack home. Do not fix this with a text substitution or use
padding gaps as initialized bytes. A read-only selected-method inventory counts **123 / 311** alias
composite-load observations across **102 / 130** methods; **106 / 214** have a
recorded sret home. All use a different legacy home key. These include unused
restores and are not counts of incorrect emitted statements or accepted fixes.

A second **TEMP-only rejected prototype** re-roots existing scalar tiles onto
the whole aggregate. Among twelve selected methods it changes seven but
recovers **zero** typed whole-value consumers: partial raw stores can inherit
the whole struct text when scalar extraction declines. Do **not** land this
re-rooting. Preserve scalar display/byte origins and add a separate semantic
snapshot proof instead.

The next architectural slice should retain a materialized aggregate's whole
origin alongside scalar-field ranges, with overlap/write/call/CFG invalidation,
and recover a whole value only at a proved typed consumer with full field
coverage. Keep semantic-value evidence separate from byte/padding evidence.
Interface slot/closed return, hidden buffer/receiver/MethodInfo identity,
RAX echo and exact copy consumer still need independent proof, negative tests,
dry/real-pass agreement and real compiler gates before any guard relaxation.

### Exact local-zero entries for slot-zero interface scans (2026-11-04)

Accepted `game_out39` (not promoted), versus out38. The complete slot-zero
LEA interface-scan proof now also admits a **disjoint exact six-instruction
entry**: receiver klass load, **32-bit self-XOR counter**, eight-byte RIP
interface load, word interface-count load, unsigned word compare, JAE miss.
The original MOVZX-copy seed and legacy ADD matcher remain unchanged. All
four scan blocks, receiver/class/table/count/interface def-use, signed offset
multiplied by 16, exact helper arguments `(same receiver, same interface, 0)`,
entry/region/exit purity and preserved-register liveness remain proved.
Overlapping roles, partial/wide seeds, MOV-zero, wrong widths or branches,
extra/reordered effects, indexes, segments and REP entries decline. Only CFG
reachability and skip membership change; no text-based repair is added.

Independent production sweeps cover **2,242 / 1,936 selected native methods**:
**148 additional scans / zero**, without losing any prior acceptance or
mutating the inspected graphs. A separate concrete integer/memory interpreter
runs the actual decoded CFG with synthetic tables, zero/small/65,535 counts,
hits/misses and signed-offset boundaries: **8,292 cases / zero mismatches**.
This is not game-native execution or an independent runtime-helper proof.

Across **474 / 293 C# files**, **75 / zero** files change: exactly 148 proved
scan regions and their phi plumbing disappear, plus 73 unused System usings.
An exact whole-source causal check preserves all constructors and surviving
statements in order, using literal/comment-safe **bijective per-method temp
maps**, not blanket identifier normalization. Real Editor/BCL/package refs,
original assembly simple names, no self-reference/stubs: UniTask **5,434 ->
4,546**, net **888 fewer** errors. Raw diagnostics are **1,036 removed / 148
added**, not zero additions. All 148 additions are existing undeclared sret
temporaries with changed names, paired by the independently verified source
line/temp maps. The actual removed scan diagnostics are **444 CS1061 + 148
CS0029 + 296 CS0019**. The other eight full diagnostic multisets are unchanged;
UniTask.Linq still has 13 declaration errors with no observed body sentinel.

Strict builds: **2,227 / 1,857 bodies**, zero failed/fallback/type-emit failures,
brace/parse clean and source fingerprints verified. **85 new portable / three
new game cases**; focused **148 synthetic + three game passed**, portable
**3,563 passed**. Frozen full excluding parallel: **3,644 passed / 259 skipped /
one non-strict xpassed / three existing failures**; parallel **two passed**.
Scoped clean-parent proof on `de9fe52` repeats precisely those three failures
and restores all three candidate files byte-exact. No golden/pin changes or
output promotion. No whole-game equivalence or speed claim; the goal is
**not achieved**.

Next, **TEMP-only / not accepted**: simply removing the interface resolver's
sret guard is disproved as a production fix. Three methods gain managed-looking
calls, but subsequent return copies still use stale undeclared obj temps.
A separate slice needs receiver/hidden-context/return-buffer identity and
aggregate-copy propagation proofs, with negative tests and real compiler gates.
The current candidate deliberately keeps honest indirect sret calls.
Aggregate-only evidence:
`validation_reports/quality_interface_direct_zero_entry_2026-11-04.json`.

### Exact small-struct leaf returns through owned copy constructors (2026-11-04)

Accepted `game_out38` (not promoted), versus out37. Two scalar-looking leaf
returns now preserve their missing managed struct wrapper. Only an explicit
Win64 PE, canonical nongeneric nullary instance method with a two-instruction
entry block **MOV EAX/RAX,[RCX+disp]; RET** qualifies. Source/target owners are
closed nongeneric non-enum value types with recursively proved default layout.
The target has exactly one full-width four/eight-byte instance field at payload
offset zero. The original source member, uncounted nonunknown RAX Expr, existing
text and exact native width must agree.

The wrapper uses an **original public owned one-parameter constructor**, never
a fabricated initializer for private/initonly fields. Its exact parameter,
access/flags, void signature and canonical MethodDef/candidate identity are
proved, and its independent native body must be precisely **MOV [RCX],EDX/RDX;
RET**. A known owned MethodDef may have other address sharers: none is guessed
as the target. Same original image and absence of a target cctor prevent added
initialization effects. Ambiguous/private/runtime/synchronized/security ctors,
scalar float arguments in XMM1, unknown/packed/explicit/open/byref layouts,
partial or indexed copies, segments, REP and RET-imm shapes decline. Register
Exprs, counted uses, hints, slots, variable types and statement order are not
mutated; boolean/enum return normalization is unchanged.

Independent production sweeps cover **2,242 / 1,936 selected native methods**:
exactly **two wrappers / zero**. Across all **474 / 293 C# files**, only **two
files / two return lines** change; reversing those wrappers restores every
prior source byte. Real Editor/BCL/package references and original assembly
simple names, without self-reference or type stubs: UniTask **5,436 -> 5,434**,
exactly **two CS0029 removed / zero diagnostics added** at the changed returns.
The other eight complete diagnostic multisets are unchanged. UniTask.Linq
still has 13 declaration errors with no observed body sentinel.

Strict builds: **2,227 / 1,857 bodies**, zero failed/fallback/type-emit failures;
brace/parse clean, source fingerprints verified. **226 new portable / one new
game case**; focused **226 synthetic + one game passed**, portable **3,478
passed**. Frozen full excluding parallel: **3,556 passed / 259 skipped / one
non-strict xpassed / three existing failures**; parallel **two passed**. Scoped
stash proof on clean `7365e11` reproduces exactly the same three failures and
restores all four candidate files byte-exact. No golden/pin changes or output
promotion.

An authored Win64 native/.NET 10 harness compares four/eight-byte loads and
copy ctors with eight readonly managed wrappers (signed, unsigned, enum and
nested float-bit structs), eight source offsets, boundaries and deterministic
random patterns, checked/unchecked, with native source/output canaries:
**525,824 checks / zero mismatches**. It neither executes game-native methods
nor covers reference-containing runtime cases, whole-method/game equivalence
or speed. Many real compiler errors remain; the goal is **not achieved**.

Next **TEMP-only**, not accepted: exact adjacent XOR EAX/RAX + RET can name a
small-struct zero as `default(T)`. The selected inventory finds only **one
eight-byte UniTask method / zero survivors methods**, with return-only deltas;
no production change, complete negative suite or compiler acceptance yet.
Aggregate-only evidence:
`validation_reports/quality_leaf_struct_copy_ctor_2026-11-04.json`.

### Exact false stack homes from native zero registers (2026-11-04)

Accepted `game_out37` (not promoted), versus out36. The existing immediate-only
stack scalar proof now has a separate **false-byte-only** path: exact MOV from a
byte GPR into the outgoing RSP home, with a same-register **32/64-bit self-XOR**
earlier in the same contiguous executed CFG block. The backward walk is bounded
at 512 instructions. Only Win64 preserved registers may carry zero across
canonical ordinary direct metadata calls before the store; **every CALL after
the store is a barrier**. Copies, partial zeros, true, register-derived enums,
unknown instructions/aliases, source clobbers, gaps, segments, RSP changes and
cross-block paths decline. Existing Win64 PE, unique canonical consumer,
signature, ABI and nonunknown literal-agreement checks remain unchanged.

Independent forward native analysis over both selected corpora proves **ten
additional false arguments / three methods** (UniTask eight, survivors two).
The full C# delta is **three files / ten lines**, each exactly one `0` -> `false`
argument replacement. No retyping, renaming, Expr/hint/slot mutation, call-count
change or effect reordering; reversing only those replacements restores all
prior selected C# source bytes.

Nine complete real-reference diagnostic multisets: UniTask **5,444 -> 5,436**;
survivors Assembly-CSharp **3,783 -> 3,781**. Exactly **ten CS1503 removed / zero
added**, all attributed to exact changed argument lines; the other seven
assemblies are unchanged. Real Editor/BCL/package references, original assembly
simple names, no self-reference or type stubs. UniTask.Linq still has 13
declaration errors and no observed body sentinel.

Strict builds: **2,227 / 1,857 bodies**, zero failed/fallback/type-emit failures;
brace/parse clean (**474 / 293 C# files**), source fingerprints verified.
**166 additional portable / two new game cases**; focused **290 synthetic +
three game passed**, portable **3,252 passed**. Frozen full excluding parallel:
**3,329 passed / 259 skipped / 1 non-strict xpassed / 3 existing failures**;
parallel **2 passed**. Scoped stash proof on clean `d1efa42` reproduces exactly
the same three failures and restores all four candidate files byte-exact.
Goldens/pins unchanged; no output promotion.

An authored Win64 synthetic native/.NET 10 harness compares the zero/store
sequences with managed false across all 15 non-RSP GPRs, 32/64-bit self-XOR,
six stack positions, zero/one/three ABI-preserving calls that clobber volatile
GPRs, and post-store source clobbers: **148,800 checks / zero mismatches**,
checked and unchecked. This is not execution of IL2CPP/game-native methods,
whole-method/game semantic equivalence or performance evidence. The goal
remains far from near-zero-error recompilation.

Next **TEMP-only**, not accepted: two exact two-instruction small-struct returns
currently print just an inner field. An initializer prototype finds both, but
original target fields are private (one initonly), so that rendering is declined
rather than relying on publicized output. A follow-up must prove an accessible
constructor's exact native copy semantics, layout, ABI and absence of added
initialization effects; no production change or compiler-gated result yet.
Aggregate-only evidence:
`validation_reports/quality_zero_register_stack_bool_2026-11-04.json`.

### Type-handle setup with a saved preceding result (2026-11-04)

Accepted `game_out36` (not promoted), versus out35. The exact same-block native
kind-2 RCX load + XOR EDX,EDX setup may now include **one full-width MOV from RAX
to a Win64 preserved GPR** (RBX/RBP/RSI/RDI/R12..15), in that order. The bounded
setup is at most 13 bytes. All existing explicit Win64 PE, exact core-library
signature, canonical unique direct MethodDef, closed type, usage identity and
executed CFG requirements remain. Partial saves, volatile/RSP destinations,
other sources, memory writes, segments, other/reordered/extra instructions,
spills, branches and cross-block paths decline. This is not general register
tracing, call capture or statement surgery.

Independent whole-method native decoding across both selected corpora proves
**32 additional consumers / one method**, all with 12-byte setups; survivors has
zero additions. Source review: **one file / 48 lines**, comprising 32 wrapper
removals and the existing inference's **two one-to-one home retypes/renames**.
Every one of their 32 definitions is a proved typeof value. Reversing just those
changes restores all prior source bytes, including statement order; survivors
is byte-identical to out35. Existing reference consumer casts remain intact.
The separately executed cross-block type-handle wrapper is still unrecovered.

Nine complete real-reference diagnostic multisets: UniTask **5,476 -> 5,444**,
exactly **32 CS1503 removed / zero added**, each attributed to its changed
assignment line; the other eight assemblies are unchanged. Real Editor/BCL/
package references, original simple assembly names, no self-reference or stubs.
UniTask.Linq still has 13 declaration errors and no observed body sentinel.
Strict builds: **2,227 / 1,857 bodies**, zero failed/fallback/type-emit failures;
brace/parse clean (**474 / 293 C# files**), source fingerprints verified.

**205 additional portable cases / one new game case**: 78 exact instruction
cases plus 127 additional fixture cases. The existing suite exercises adjacent
and saved-return defaults; explicit instruction-shape cases retain their bytes.
Focused **332 synthetic + three game passed**; portable **3,086 passed**.
Frozen full excluding parallel: **3,161 passed / 259 skipped / 1 non-strict
xpassed / 3 existing failures**; parallel **2 passed**. Scoped stash proof on
clean `62514de` reproduces exactly the same three failures and restores all five
candidate files byte-exact. No golden/pin changes or output promotion.
An authored managed .NET 10 harness checks typeof/RuntimeTypeHandle conversions,
previous null/base/derived results, exceptions and effect order: **128,000 cases /
zero mismatches**, checked and unchecked. Not game-native execution, whole-game
semantic equivalence or performance evidence; the goal remains unmet.

Next **TEMP-only**, not accepted: eight remaining literal-false byte homes in
that method are stored from a preserved register independently zeroed earlier
in the same block. A bounded native prototype traces that zero across canonical
calls only in preserved registers and declines every call after the home store.
**80 synthetic cases pass**. A separate TEMP selected-corpus sweep finds ten
arguments in three methods (unitask eight, survivors two), independently checked
by a forward zero-register/home analysis, with argument and type state unchanged.
No production implementation, complete metadata negative suite, strict rebuild
or compiler gate for this next slice yet.
Aggregate-only evidence:
`validation_reports/quality_type_handle_saved_return_2026-11-04.json`.

### Exact stack reference consumers (2026-11-04)

Accepted `game_out35` (not promoted), versus out34. A bare outgoing stack home
may be cast **only at an exact reference-class parameter use**. Canonical unique
direct nongeneric MethodDef, explicit Win64 PE, closed nonnested nongeneric
class type, exact nonsret/nonbyref return and exact receiver/float ABI positions
are required. The nonunknown object Expr and its printed home must agree. An
independent native backward walk in the same contiguous executed CFG block
proves a full-width home store and GPR copy chain from a unique canonical CALL
returning the **exact same class**. The walk is bounded at 128 instructions.
Before the store, ordinary canonical calls may be crossed only with the source
in a Win64 preserved register; after the store, **every CALL is a barrier**.
Partial/alias writes, source clobbers, unknown instructions, gaps, segments and
RSP changes decline. No statement insertion, capture, repeated call, effect
reordering, home rename, global slot retyping or type-hint mutation.

**32 native reference arguments / 16 lines / one file**, all independently
checked by a separate **forward** native register/home analysis over both selected
sample corpora. Reversing only those casts restores every prior source byte;
call count and statement order remain unchanged. Survivors is byte-identical to
out34. Nine complete real-reference diagnostic multisets: UniTask **5,506 ->
5,476**, exactly **30 CS1503 removed / zero added**; all eight other assemblies
unchanged. Every removed occurrence is attributed to an exact changed argument
line, not normalized or suppressed. Real Editor/BCL/package references, original
assembly simple names, no self-reference or type stubs; UniTask.Linq still has
13 declaration errors and no observed body sentinel.

Strict selected builds: **2,227 / 1,857 bodies**, zero failed/fallback/type-emit
failures; brace/parse clean (**474 / 293 C# files**), fingerprints verified.
**155 new portable / one new game case**; focused **156 passed**, portable
**2,881 passed**. Frozen full excluding parallel: **2,955 passed / 259 skipped /
1 non-strict xpassed / 3 existing failures**; parallel **2 passed**. Scoped stash
proof on clean `a6d0c38` reproduces the exact same three failures and restores all
four candidate files byte-exact. Goldens/pins unchanged; no output promotion.

An independently authored managed .NET 10 harness checks null/base/derived
values, producer/consumer exceptions, reused homes, call count and event order:
**40,000 cases / zero mismatches**, checked and unchecked configurations. This
is not game-native execution, whole-method/game equivalence or speed evidence.
The goal remains far from near-zero-error recompilation.

Next **TEMP-only**, not accepted: 32 more tagged type-handle consumers have the
same-block RCX metadata load and EDX zeroing separated from the CALL only by a
full-width RAX-to-preserved-GPR save. A narrow in-memory prototype recovers those
32 sites in one method without crossing a branch or call; 78 new synthetic
cases plus 127 existing metadata/ABI cases with that setup pass. The 19 probed
cross-block declines remain untouched. No production relaxation, native rebuilt
out36 or compiler gate for that next slice yet.
Aggregate-only evidence:
`validation_reports/quality_exact_stack_references_2026-11-04.json`.

### Explicit Win64 recovery boundary (2026-11-04)

Accepted `game_out34` (not promoted), versus out33. Type-handle consumer recovery
now requires a PE instance, `is64`, the PE signature and COFF x64 machine
`0x8664`. Immediate stack-scalar recovery uses the same shared predicate while
retaining its existing platform boundary. A synthetic ELF64 object with the
previous RCX-shaped test setup formerly recovered `typeof(int)`; it now declines.
ELF, unknown objects, PE32, ARM64/x86 and malformed/truncated headers decline.
This is a recovery-policy fix, **not** Linux/ARM64 game execution or ABI support.

Both selected sample trees are **byte-identical to out33**: **474 / 293 C# files**,
strict **2,227 / 1,857 bodies**, zero failed/fallback/type-emit failures, brace and
parse clean, frozen source fingerprints verified. All nine complete real-reference
compiler diagnostic multisets are identical (**zero added / zero removed**).
Real Editor/BCL/package references, original assembly names, no self-reference
or type stubs. UniTask.Linq still has 13 declaration errors and no observed body
sentinel. This boundary slice does not claim a Windows compiler-error reduction.

**16 new portable cases**; final focused **253 passed**, portable **2,726 passed**.
Frozen full excluding parallel: **2,799 passed / 259 skipped / 1 non-strict
xpassed / 3 existing failures**; parallel **2 passed**. Scoped stash proof on
clean `dba02a6` reproduces the exact same three failures; all five candidate
files restored byte-exact. No golden re-pin, output promotion, whole-game
semantic equivalence or speed claim.

Next **TEMP-only**, not accepted: tail capture predicted 15 future-home cases,
but all shared their definition slot with earlier pending calls; the conservative
prototype declined all 15 rather than risk effect reordering. A separate consumer
cast probe independently traces 32 exact reference-return origins through
full-width GPR copies and Win64 preserved registers to outgoing homes. It changes
only 16 argument lines, preserving call count and statements. Hand-editing those
casts into a copied output tree for feasibility gives UniTask **5,506 -> 5,476**,
**30 CS1503 removed / zero added**, with real references and a body sentinel.
That experiment is **not** a native rebuild or validated production feature.
Next work must add exact metadata/ABI/CFG/alias/width negative tests and full
source/diagnostic review; do not globally retype reused homes or repeat calls.
Aggregate-only evidence:
`validation_reports/quality_win64_recovery_boundary_2026-11-04.json`.

### Exact immediate stack bool/enum arguments (2026-11-04)

Accepted `game_out33` (not promoted), versus out32. Stack positions >= 4 may
recover bool or named int32-enum literals only at a unique exact direct canonical
nongeneric MethodDef call. Explicit **PE/Windows x64** machine guard; nonnested
reference owner, exact nongeneric/nonbyref nonsret return. ABI positions include
instance receivers and floating-point slots. The existing nonunknown integer
stack Expr must equal the printed literal. An independent backward scan inside
the contiguous executed CFG block requires its latest overlapping definition to
be an exact **byte immediate 0/1** or **dword immediate named int32 enum** store.
Enum underlying-field and optional element metadata must agree. Only GPR
MOV/LEA not changing RSP and nonoverlapping RSP writes may intervene. Calls,
branches, alias/unknown writes, gaps, segment overrides, partial stores and
register-derived definitions decline. Slot types and type hints never change.

**31 native argument recoveries / 33 source argument occurrences / three files**:
unitask has 23 (8 bool / 15 enum); survivors has eight native recoveries (5 bool /
3 enum), displayed ten times because an already-duplicated identical structured
line repeats two arguments. Independent native/metadata checks and byte review
prove only these literal replacements, with every other source byte unchanged.
Nine complete real-reference diagnostic multisets: UniTask **5,528 -> 5,506**;
survivors main **3,791 -> 3,783**; the other seven images unchanged. Exactly
**30 CS1503 removed / zero added**, no diagnostic normalization or suppression.
Real Editor/BCL/package references, original assembly names, no self-reference
or synthetic type stubs. UniTask.Linq retains its 13 declaration errors and
unobserved body sentinel; no body-compilation coverage is claimed there.

Strict selected builds: **2,227 / 1,857 bodies**, failed/fallback/type-emit zero;
**474 / 293 C# files**, brace/parse clean, frozen source fingerprints verified.
**119 new portable / 1 new game tests**; focused **120 passed**, portable
**2,710 passed**. Frozen full excluding parallel: **2,783 passed / 259 skipped /
1 non-strict xpassed / 3 existing failures**; parallel **2 passed**. Scoped stash
proof on clean `480eef7` reproduces the exact same three failures and restores
all four candidate files byte-exact. No golden re-pin or output promotion.

Original synthetic Win64 wrappers write immediate scalar homes at ABI positions
4..9; native callees read them, compared with strongly typed managed bool/enum
calls. Checked compilation on/off each gives **4,800 checks / zero mismatches**,
including signed int32 boundary enum values. This is not native game execution,
whole-method/game equivalence or game-speed evidence. Eight register-derived
bool zeros and one register-derived enum zero in the focused method remain raw.

Next read-only probe: 32 full-width System.Type-return stores in Initialize
retain type on their copied stack Expr but lose native definition identity and
anchors; the reused homes remain untyped and emit object declarations. Sixteen
stores come from RAX and sixteen from copied registers. No safe capture/lifetime
proof or production recovery is implemented. Do not globally retype reused homes,
repeat a call at its consumer, or equate matching text with one native call.
Aggregate-only evidence:
`validation_reports/quality_exact_stack_scalars_2026-11-04.json`.

### Exact native type-handle consumers (2026-11-04)

Accepted `game_out32` (not promoted), versus out30. A full-width metadata usage
kind-2 load carries a small origin tag; only the exact unique direct core-library
`System.Type.GetTypeFromHandle(System.RuntimeTypeHandle)` consumer may recover
`typeof(T)`. The helper independently decodes the adjacent RCX load plus optional
EDX zeroing, rechecks canonical usage/type/text and the complete method identity,
and requires the load and call in **the same executed CFG block**. Simple closed
primitive/class/value types only; bounded TypeDef indices. Arrays, generics,
byrefs, pointers, spills, truncations, intervening moves/arithmetic/branches and
kind-1 klass-pointer arithmetic all decline. Flat lifting without a CFG block
also declines. No fixture-specific type name or native address controls it.

Important rejected intermediate: out31's adjacency-only check was insufficient.
An equal-text merge can retain a predecessor Expr and its origin tag, even when
an alternate entry bypasses the nearby load. Out32 adds the block proof; the
full out31 run was intentionally interrupted, **not** counted as passing. Both
final sample trees retain exactly the reviewed out31 C# bytes, with the stronger
gate protecting unsupported control-flow shapes.

**85 exact source-line recoveries / five files** (47 unitask, 38 survivors).
Each changed line differs only by replacing one proven call with its canonical
`typeof(T)`; every other source byte is identical. Nine real-reference compiler
multisets: survivors main **3,829 -> 3,791**, firstpass **814 unchanged**; unitask
UniTask **5,515 -> 5,528**; the seven other images are unchanged. Overall **85 removed /
60 added / net -25 diagnostic occurrences**. The 60 added CS1503 occurrences
are real, not normalized away: four unchanged later-argument errors at each of
15 InsertLoop calls become visible after the invalid inner type-handle argument
is fixed. Exact source/line attribution plus an independent authored Roslyn
example reproduces the diagnostic masking. Do not claim zero added errors or a
per-assembly UniTask improvement. Real Editor/BCL/package references, original
assembly names, no self-reference or type stubs; UniTask.Linq still misses its
body sentinel.

Strict selected rebuilds: **2,227 / 1,857 bodies**, zero failed/fallback/type-emit
failures; brace/parse clean (**474 / 293 C# files**), source fingerprints verified.
**116 new portable / 1 new game tests**; focused **117 passed**, portable
**2,591 passed**. Frozen-source full excluding parallel: **2,663 passed / 259
skipped / 1 non-strict xpassed / 3 existing failures**; parallel **2 passed**.
Scoped stash proof on clean `10d77e3` reproduces the same three failures and
restores all six candidate files byte-exact. No golden re-pin or promotion.

Installed .NET 10 independently checks TypeHandle identity across 19 simple
closed types (**19,000 checks / zero mismatches**) and a null default handle.
This is not execution of IL2CPP/game-native methods, whole-game equivalence, or
speed evidence. Next probe: stack-passed bool/enum arguments are skipped by the
register-only hint walk; InsertLoop exposes unchanged 0/1 bool literals and
known Type-valued stack homes. Any recovery must preserve exact ABI positions,
value evidence and slot lifetime, not blindly cast by callee signature.
Aggregate-only evidence:
`validation_reports/quality_exact_type_handle_2026-11-04.json`.

### Preserve compound-assignment snapshot order (2026-11-04)

Accepted correctness guard `game_out30` (not promoted), versus out29. Hop-folding
`tmp = target + 1; target = tmp;` may cross only blank lines before its exact
writeback. Every nonempty statement is a barrier without an independent
effect/alias proof. The old lexical target-write checks incorrectly crossed
old-value snapshots, observer/throwing calls and receiver/index reassignments.
Adjacent hops and direct arithmetic keep their existing sugar; no game-specific
field names or native addresses participate in the guard.

Survivors TypeRegistry.EnsureInitialized (mi 69928) independently proves the
old list size held in RDX, LEA EAX old+1, size writeback, then an RDX-indexed
array store. The old pass hoisted the increment before the snapshot and indexed
with the new size. All **38** changed sites in five files are the same restored
snapshot/write ordering; undoing only those exact expansions reproduces every
old source byte.

**Explicit compilation cost, not a recompilability improvement:** with the same
real Editor/BCL/package references and original assembly names, unitask UniTask
**5,514 -> 5,515**, survivors Assembly-CSharp **3,792 -> 3,829**. Complete raw
(file, code, message) multisets add **38 CS1061 occurrences**, remove **zero**.
They repeat the existing unavailable List<T>._size member diagnostic, exactly
one per restored snapshot site. The distinct diagnostic-key set is unchanged,
but totals really increase; no normalization, suppression or zero-added claim.
All seven other assemblies are unchanged (survivors firstpass 814); the existing
UniTask.Linq syntax gate remains. Keeping the proven wrong execution order to
reduce error counts is rejected. List-operation recovery needs its own complete
native/CFG proof, not a textual three-line substitution.

Strict selected rebuilds: **2,227 / 1,857 bodies**, zero failed/fallback/type-emit
failures; brace/parse clean (**474 / 293 C# files**), fingerprints verified.
Focused **90 passed**, including **62 new portable / 1 new game** cases;
portable **2,475 passed**. Frozen-source full excluding parallel: **2,546 passed /
259 skipped / 1 non-strict xpassed / 3 existing failures**; parallel **2 passed**.
Scoped stash proof on clean `9132d32` reproduces the same three failures and
restores all candidate bytes. No re-pin or promotion.

Original synthetic Win64 load/increment/store/return-old execution, checked
compilation on/off: each **10,006 checks / zero recovered mismatches**; the old
fold mismatches all 10,006. Inputs exclude signed-int32 overflow; this is not an
overflow/exception or whole-game equivalence proof, nor speed evidence.
Aggregate-only evidence:
`validation_reports/quality_compound_assignment_order_2026-11-04.json`.

### Exact reference-array loads from typed SSA objects (2026-11-04)

Accepted source slice `game_out29` (not promoted), versus out28. A nonbyref
SZARRAY-typed object SSA token may recover one exact reference-element load:
MOV mem64 to reg64, 64-bit base/index, scale 8, header displacement 0x20,
no segment override, typed nonunknown integer index and reference element.
Producer kinds, allocation identity and the legacy array fallback are unchanged.
Partial-width/SIMD/address loads, unknowns, byrefs and scalar/struct/generic
elements decline. Broad producer reclassification was rejected because the
legacy fallback also folds partial reads of reference slots.

Strict selected builds: **2,227 / 1,857 bodies**, zero failures/fallbacks/type-emit
failures, frozen fingerprints verified, brace/parse clean. **One file changes
per fixture**. Real Editor/BCL/package references and original assembly names,
no stubs/self-reference: UniTask **5,515 -> 5,514** (one CS1503 removed);
survivors main **3,797 -> 3,792**; the other seven assemblies are unchanged.
Survivors' raw complete diagnostic multiset is **1 added / 6 removed**: the
added CS0165 is the existing unassigned local renamed obj20 -> obj17. A separate
real recompile restores **only that local name (six occurrences in one method)**,
leaves all other source bytes unchanged, and proves **0 added / 5 removed**.
No global diagnostic-name normalization. UniTask.Linq remains syntax-gated.

**82 new portable / 1 new game test**; portable **2,413 passed**. Frozen full
excluding parallel: **2,483 passed / 259 skipped / 1 non-strict xpassed / 3 failed**;
parallel **2 passed**. Scoped stash proof on clean `9095211` reproduces exactly
the same three baseline failures and restores all three candidate files byte-exact.
Original synthetic Win64 reference-slot loads: checked on/off each **131,190
checks / zero recovered mismatches**; byte truncation gives **119,160 mismatches**.
This uses artificial GCHandle-token storage, not native game execution. No
whole-game equivalence, speedup, near-zero-error recompilation, re-pin or promotion.

Next: `_compound_assign` incorrectly hoists a write across the old-value snapshot
in survivors TypeRegistry.EnsureInitialized (mi 69928); native loads old size,
updates size, then indexes with the old value. Stage probes locate the first
wrong reorder in the compound-assignment pass. Independent repros also expose
crossed observer calls and receiver/index reassignment. Fix must preserve order,
not special-case this method. Aggregate-only evidence:
`validation_reports/quality_typed_reference_array_load_2026-11-04.json`.

### Native-definition capture of pending phi calls (2026-11-04)

Accepted source slice `game_out28` (not promoted), versus out26. An unrendered
CLASS-return pending call flowing directly into a phi is captured once at its
native CALL definition, by **Expr object identity**, before SSA destruction.
Phi copies then read a pure temp; text-twin dead-copy cleanup cannot erase a
loop iteration against the exit path. Definition-slot creation epochs must
remain unchanged. Mixed pending/complex phi cohorts, used/rendered calls,
byrefs, generics and nested/raw/index/address argument spellings decline.
No textual replacement or general effect/lifetime/argument proof is claimed.

Survivors rows **70222 / 70238** each keep one rendered CreateBullet site
inside the proven native natural loop (block 2), instead of once after it.
Original synthetic Win64 callback loop versus recovered output: checked on
and off each **1,005 cases / zero recovered mismatches**; the old output has
**998 mismatches** per mode. This executes original synthetic code, not game
native code and not a whole-method/game equivalence proof.

Strict selected builds: **2,227 / 1,857 bodies**, zero failures/fallbacks/type-emit
failures, source fingerprints verified, brace/parse clean. Five files change
per fixture. All **nine complete compiler diagnostic multisets are unchanged**:
survivors main **3,797**, firstpass **814**; UniTask **5,515**. Real Editor/BCL/
package references, original assembly names, no stubs/self-reference. UniTask.Linq
still misses the body sentinel; no near-zero-error recompilation or speed claim.

**69 new portable / 2 new game tests**; portable **2,331 passed**. Frozen full
excluding parallel: **2,400 passed / 259 skipped / 1 non-strict xpassed / 3 failed**;
parallel **2 passed**. Scoped stash proof on clean `e6d9acd` reproduces exactly
the same three baseline failures, then restores all five candidate files
byte-exact. No golden re-pin or output promotion.

Rejected out27 had a lower diagnostic total but **one added UniTask CS1503**,
and an independent mixed-pending repro reversed two effects sharing one slot.
Out28 declines mixed cohorts and unsafe argument spellings; all nine diagnostic
multisets now match. Next probe: a resolved SZARRAY call retains array type but
uses object kind through a phi, leaving an exact reference load as a raw byte
read. Broad producer reclassification is not accepted: its legacy array fallback
also folds partial-width reads. The separate consumer-only prototype requires
an exact pointer-width MOV and reference-element vector type; not yet landed.
Aggregate-only evidence: `validation_reports/quality_pending_phi_calls_2026-11-04.json`.

### Consumer-only copied scalar struct arguments (2026-11-04)

Accepted source slice `game_out26` (not promoted), versus out23/out20. Managed
Win64 calls can reconstruct a 4/8-byte non-generic value type only from complete
explicit float32 copies, natural public writable fields and no explicit default
constructor. New spellings accept only simple scalar names or float-suffixed
literals; captured names stay captured. Unknowns, partial coverage, overlap,
byrefs, calls, arithmetic and unbound member paths decline. No whole-container
producer type is published. This is not a general lifetime/expression proof.

Strict selected builds: **2,227 / 1,857 bodies**, zero failures/fallbacks/type-emit
failures; brace/parse clean and frozen source fingerprints verified. Unitask's
**474 files and seven complete diagnostic multisets are unchanged**. Survivors
changes **six files / seven call arguments**: main **3,802 -> 3,797**, firstpass
**816 -> 814**, **zero added diagnostics** in either complete multiset. Real
Editor/BCL/package references and original assembly names; no stubs/self refs.
Linq sentinel remains false: still syntax-gated, not zero-error recompilation.

**82 new portable / 7 new game tests**; portable **2,262 passed**. Frozen full
excluding parallel: **2,329 passed / 259 skipped / 1 non-strict xpassed / 3 failed**;
parallel **2 passed**. Scoped stash proof on clean `98bfeff` reproduces exactly
the three existing failures and restores all four candidate files byte-exact.
No re-pin. Original Win64 bit consumer versus six recovered initializer variants:
**1,200,000 checks / zero mismatches per checked mode**, on and off. No game-native,
whole-method equivalence or speedup claim. Existing loop call-placement loss and
repeated TMP getters remain unfixed.

Rejected out24 lowered totals but added **25** survivors diagnostics through
producer aggregate regressions. Rejected out25 accepted unsafe member/arithmetic
spellings: **3 main / 2 firstpass added diagnostics** despite lower totals and
passing synthetic bit checks. Neither has a passing full suite. Next: impure
phi cleanup drops a loop-body call against a post-loop text twin; executable
counter reproduces it, but a lexical-scope prototype is not native identity proof.
Aggregate-only record: `validation_reports/quality_byval_scalar_parts_2026-11-04.json`.

### Byte-bounded aggregate slice projection (2026-11-04)

Accepted source guardrail `game_out23` (not promoted), versus `game_out20`.
`_piece_value` cannot project bytes outside any nested native slice, including
zero-offset slices; `_scalar_parts` clips to copied coverage. The guard only
checks bounds: it preserves captured display names rather than re-reading an
origin field. Negative offsets, invalid widths, cycles and excessive nesting
decline; type/phi/literal evidence cannot expand a copy.

Strict selected rebuilds: **2,227 / 1,857 bodies**, zero failures/fallbacks/
type-emit failures; source fingerprints verified; brace/parse clean. Both
selected C# trees are **byte-identical to out20 (474 + 293 files)**. Full
compiler diagnostic multisets, not merely code counts, match across all nine
selected assemblies with real Editor/BCL/package references and exact assembly
simple names. Survivors main **3,802**, firstpass **816**; unitask counts stay
unchanged. UniTask.Linq sentinel remains false; this is still syntax-gated.
This is a correctness guardrail, **not a measured game-output improvement**.

**24 new tests**, including **114,000** independent byte-coverage queries;
portable **2,180 passed**. Frozen-source full excluding parallel: **2,240
passed / 259 skipped / 1 non-strict xpassed / 3 failed**; parallel **2 passed**.
Failure IDs exactly match the out20 full-suite baseline; no re-pin. Isolated
lift performance is mixed under contention: a 200-sample/mode recheck gives
process CPU totals about **+0.3% / +9.0%** on the two probed vector methods;
there is **no speedup or zero-overhead claim**, nor whole-tree/runtime evidence.

Rejected out21 rerooted zero-offset snapshots and changed unrelated consumers.
Rejected out22 published bounded packed field-prefix parts but damaged existing
aggregate consumers (**3,802 -> 3,811** survivors diagnostics). Their canceled
full suites are not passing evidence; synthetic arithmetic checks do not prove
those aggregate consumers. Next: distinguish copied byte coverage, materialized
snapshot identity and candidate whole-container type; do not publish a whole
struct without independent full coverage. A scalar-consumer-only local probe
is exploratory, not accepted evidence. Aggregate-only record:
`validation_reports/quality_aggregate_slice_bounds_2026-11-04.json`.

### Closed native uint32 string-fold proof (2026-11-04)

Accepted source candidate `game_out20` (not promoted), versus `game_out19`.
A complete 28-instruction Win64 proof now recovers one xor/multiply loop over
UTF-16 code units with explicit unchecked uint32 arithmetic. All branch targets,
operand widths, ABI saves/restores, disjoint caller homes and three distinct
nonvolatile register roles must match. The exact core-library String getter
must resolve uniquely; null returns the native-proven zero. Seed/multiplier are
extracted, not hard-coded fingerprints; method names are not consulted. Extra
instructions, EH, skipped guards, mismatched identities and other ABIs decline.
Assembly-comment mode retains ordinary lifting. This does **not** repair general
integer width/wrap/signedness/phi provenance.

Strict selected rebuilds: 2,227 / 1,857 bodies, zero failures/fallbacks/type-emit
failures; brace/parse clean (474 / 293 C# files), source fingerprints verified.
The unitask selected tree is byte-identical. Survivors changes exactly one
method in one file; all other bytes match. With real Editor/BCL/package DLLs
and original assembly names, survivors Assembly-CSharp **3,805 -> 3,802**
(**CS0266 -3**, no other code delta), firstpass **816**. Every selected unitask
code count is unchanged; UniTask.Linq body sentinel remains false. This is
still syntax-gated, not a zero-error compile.

Portable **2,156 passed**; focused **137 passed** (135 new portable cases plus
two real methods). Frozen-source full excluding parallel: **2,216 passed /
259 skipped / 1 non-strict xpassed / 3 failed**; separate parallel **2 passed**.
The exact failure set is unchanged: two callback count pins and Limbus AddItem's
temporary-number pin. No re-pin. Original synthetic native loops/getters versus
actual recovered C# and an independent masked reference: **2,503,584 checks /
zero mismatches**, checked compilation on and off, 18 seed/multiplier/register
variants, every UTF-16 singleton, surrogate cases and randomized strings. The
getter deliberately clobbers volatile argument registers and poisons high return
bits. No game native body/getter or end-to-end game runtime is executed.

Interleaved isolated lift audit (40 samples/mode, load/warmup excluded): unitask
mi 30307 median **27.531 -> 0.435 ms**, survivors mi 85900 **23.939 -> 0.348 ms**.
External CPU contention and coarse process-CPU resolution limit interpretation;
this is neither whole-tree acceleration nor game-speed evidence. Ten audited
hash copies match the proof; only the one selected-tree method is rebuilt here.
General integer provenance and lifetime-aware aggregate recovery remain open.
Aggregate: `validation_reports/quality_native_string_fold_2026-11-04.json`.

### Globally rooted native sqrt intrinsics (2026-11-03)

Accepted source candidate `game_out19` (not promoted), compared with `game_out17`.
Only proven native SSE/packed-low-lane/helper/tail construction sites now emit
`global::System.Math.Sqrt`, preserving SQRTSS narrowing. User calls, arguments,
comments and literals are not textually rewritten. The using collector no longer
restarts inside explicit global/extern-alias paths; unrooted generic argument
names and ordinary qualified references remain collectible.

Rejected `game_out18` additionally introduced `using System`; its canceled
suites are not final evidence. Out19's general alias repair also removes 42
existing redundant System imports (37 unitask / 5 survivors). These were reviewed,
not assumed harmless: with the same real Editor/BCL/package references, Roslyn
symbols, types, conversions, constants and declarations match on **7,201 nodes**
in all 42 files, including six unchanged error-type nodes. This is limited to
that compilation model, not a runtime-equivalence proof. Separately, 15 survivors
files contain **32** intrinsic qualifications; all other bytes are identical
apart from those imports and at most one associated empty line per file.

Strict selected rebuilds: 2,227 / 1,857 bodies, zero failures/fallbacks/type-emit
failures; brace/parse clean (474 / 293 C# files), source fingerprints verified.
Real references and original assembly names: survivors Assembly-CSharp
**3,820 -> 3,805** (CS0103 -15, no increased code count); firstpass **816**.
Every selected unitask diagnostic-code count is unchanged. UniTask.Linq's body
sentinel remains false; the gate is syntax-gated, not zero-errors success.

Portable **2,021 passed**; focused **57 passed**, including 22 new cases.
Frozen-source full excluding parallel: **2,079 passed / 259 skipped /
1 non-strict xpassed / 3 failed**; separate parallel **2 passed**. Exact failure
set remains the two callback count pins plus Limbus AddItem temporary-number
pin. No re-pin; unavailable ShiftAtMidnight sqrt pins remain skipped/unchanged.
Actual recovered fragments versus synthetic native SSE: **50,055 checks / zero
mismatches**, including user Math/System shadows and the missing-import case.
Non-NaNs match bits including signed zero; NaN payload/sign and nondefault
rounding are not proved; the native helper body is not executed. No game runtime
or speed claim. Next: width/wrap/signedness/phi proof for integer hash arithmetic
and lifetime-aware aggregate provenance, not casts/defaults to hide errors.
Aggregate: `validation_reports/quality_intrinsic_sqrt_scope_2026-11-03.json`.

### Exact metadata-entry string lengths (2026-11-03)

Accepted source candidate `game_out17` (not promoted), compared with `game_out14`.
Exact metadata STRING parameter identities now survive generic GPR display
kinds, including stack parameters. Only a non-unknown exact entry token with
matching metadata type, a dword load and offset `0x10` recovers `.Length`.
Hints, phi tokens, arithmetic, pointer/address/lvalue and other widths decline.
The existing string-kind path is unchanged, not newly asserted correct.

The array-only foreach pass now leaves these string loops indexed: otherwise
it invents object elements and may snapshot a reassigned parameter. Rejected
`game_out15` used unsafe tuple-only proof; rejected `game_out16` omitted this
loop guard. Neither prototype is accepted evidence.

Strict selected rebuilds: 2,227 / 1,857 bodies, zero failures/fallbacks/type-emit
failures; brace/parse clean (474 / 293 C# files), core fingerprints verified.
Unitask trees are byte-identical; exactly two survivors files change. Each has
one native dword length read replacing a byte fallback; after normalizing
redundant unsafe wrappers/raw-address using, all other syntax-tree tokens match.
Real Editor/BCL + original packages, original assembly names: all diagnostic
code counts unchanged (survivors Assembly-CSharp **3,820**, firstpass **816**).
UniTask.Linq's body sentinel remains false; this is not a zero-error compile.

Portable **1,999 passed**; focused **70 passed**. Frozen-source full excluding
parallel: **2,057 passed / 259 skipped / 1 non-strict xpassed / 3 failed**;
separate parallel module **2 passed**. Exact failure set unchanged from out14:
two interface callback count pins plus Limbus AddItem temporary-number pin.
No re-pin. Original synthetic native dword reads versus the actual recovered
expression: **10,014 checks / zero mismatches**, including lengths above 255,
UTF-16 surrogate boundaries and managed null throwing (native null not run).
No game equivalence or speed claim. Exact target mi 71258 retains its indexed
hash loop; its char-typed integer accumulator is still wrong and uncompilable.
Next: intrinsic framework-name binding and integer/aggregate provenance, not
casts or defaults to hide errors. Aggregate:
`validation_reports/quality_entry_string_length_2026-11-03.json`.

### Exact slot-zero LEA interface scans (2026-11-03)

Accepted source candidate `game_out14` (not promoted). A complete four-block
proof now recognizes the zero-start, slot-zero LEA interface-table scan, with
one exact receiver/class/count/table/offset chain and matching helper arguments.
All-reaching-definition zero proof, existing purity/entry/exit and callee-saved
liveness gates remain mandatory. Legacy ADD matching is unchanged.

The earlier `game_out13` prototype is **rejected source evidence**: synthetic
receiver-RDX and interface-R8 argument-setup aliases were incorrectly accepted.
Both failed before the fix; the final version rejects overwritten inputs and
RSP seeds. Fixed-source rebuild fingerprints were verified independently; its
selected emitted trees happen to match prototype bytes, not its unsafe proof.

Real Editor/BCL + original packages, exact assembly names: survivors
Assembly-CSharp **4,012 -> 3,820** (CS0019 -48, CS0103 -24, CS0266 -24,
CS1061 -72, CS1729 -24; no increased code counts). Firstpass remains 816;
all selected unitask trees and diagnostics are unchanged. Two GameInput files
each recover 12 remaining constructors; a now-unused shared stub is removed.
Each file's 78 ordered event operations preserve exact receiver fields, +/-
operation, delegate target and method; 32 other methods per file are unchanged.
This graph review does not prove other statements or evaluation timing.

Strict builds lift 2,227 / 1,857 bodies with zero failures/fallbacks/type-emit
failures; brace/parse clean (474 / 293 C# files). Portable **1,929 passed**;
focused scan proof **58 passed**. Frozen-source full excluding parallel:
**1,987 passed / 259 skipped / 1 non-strict xpassed / 3 failed**. Separate
parallel module **2 passed**. The failure set is exactly the two prior callback
count pins (mi 27494: 12 -> 18; mi 27511: 54 -> 60, each six fewer unresolved
constructors) plus the unchanged Limbus AddItem temporary-number assertion.
**No re-pin**; these assertions remain visibly failing, not hidden or weakened.

Original synthetic x64 execution before/after the actual CFG rewrite passes
**4,729 checks / zero mismatches**, including 0/65,535-entry tables and signed
32-bit offset extremes. Not game execution, invalid-pointer/concurrent-mutation
proof or managed speed evidence. Thousands of compiler errors remain;
UniTask.Linq's body sentinel stays false; the gate is syntax-gated, not a zero
binding-error gate. Next investigate scalar/aggregate type provenance and
string/narrow-integer operations, not casts/defaults to silence diagnostics.
Aggregate: `validation_reports/quality_interface_slot_zero_lea_2026-11-03.json`.

### Exact interface-slot delegate constructors (2026-11-03)

Accepted source candidate `game_out12` (not promoted). Resolve-helper receiver
identity now survives the MethodInfo load independently of expression binding.
Only a fresh delegate allocation, exact interface owner/receiver identity, fully
closed matching Invoke/target signatures (including ref/out), and one actual
constructor candidate qualify. Generic methods, variance and complex receivers
decline; the same allocation completes once, with no fabricated defaults.

Real Editor/BCL + original packages, exact assembly names: survivors
Assembly-CSharp **4,276 -> 4,012** (CS0103 -132, CS1729 -132, no increased
code counts); firstpass stays 816. All selected unitask trees and diagnostics
are byte-for-byte/count-for-count unchanged (Assembly-CSharp 1,973; UniTask
5,515). Only two survivors files change: 132 unresolved construction pairs
become method-group constructions; all non-delegate lines and allocation-variable
multisets match. Strict builds lift 2,227 / 1,857 bodies with zero failures,
fallbacks/type-emit failures; brace/parse clean (474 / 293 C# files).

Portable **1,871 passed**; focused portable/game **28 passed**. Frozen-source
full excluding parallel: **1,931 passed / 259 skipped / 1 non-strict xpassed /
1 failed**, the same Limbus AddItem exact-number assertion as out11. Parallel
module **2 passed**. No re-pin. An original compiled synthetic program passes
**168,002 checks / zero mismatches** for receiver identity, virtual/explicit
interface dispatch, delegate equality, duplicate subscription/removal, exceptions
and null receiver construction. Not game runtime equivalence or a speed proof;
arbitrary allocation/argument evaluation ordering is outside that harness.

The gate remains syntax-gated, not zero-errors success; UniTask.Linq's body
sentinel remains false. Thousands of errors remain. Next: prove the exact
slot-zero LEA interface fast-path fold responsible for 24 residual callback
constructor errors, preserving purity/liveness/entry/exit gates. Wide struct
stack tiles and external BCL implementation references remain unresolved.
Aggregate: `validation_reports/quality_interface_delegate_ctor_2026-11-03.json`.

### Shared-tail type facts and nested-type scope repair (2026-11-03)

Accepted source candidate `game_out11` (not promoted). Tail duplication now
copies each exact type-fact map entry independently; alpha-renaming no longer
turns a known array into `object`. Conflicts/lookup precedence and generic-blocked
membership survive; fresh tokens avoid fact-only names and metadata parameters.
No RHS type inference or entry-byref alias/provenance is invented.

The type-only intermediate `game_out10` reduced survivors Assembly-CSharp
6,263 -> 4,281, but regressed UniTask 5,589 -> 5,663. Precise types exposed a
scope-repair blind spot for nested generic members and raw state-machine names.
The final candidate recognizes those declarations under the existing scope/LCA
proof, hoisting **bare declarations**, never fabricating default assignments.

Real Editor/BCL + original packages, original assembly simple names:

| image | out9 | out10 (type only) | out11 |
|---|---:|---:|---:|
| unitask Assembly-CSharp | 1,989 | 1,985 | 1,973 |
| UniTask | 5,589 | 5,663 | 5,515 |
| UniTask.TextMeshPro | 222 | 222 | 209 |
| survivors Assembly-CSharp | 6,263 | 4,281 | 4,276 |
| survivors firstpass | 834 | 816 | 816 |

Other selected images are unchanged. Survivors CS0021 609 -> 11, CS0019
-1,034 and CS1061 -422, but CS0029 **+108**, CS0208 +6 and CS0212 +4.
UniTask CS0103 -88 and CS1061 -26, but CS0029 **+15**, CS0165 **+20**,
CS0266 +6. These are recorded error transfers/increases, not hidden successes.
UniTask.Linq still has a false body sentinel; other selected images observe
some body binding only. The compiler gate is not a zero-errors success gate.

Strict builds again lift 2,227 / 1,857 bodies with zero failures, fallbacks or
type-emit failures; brace/parse clean (474 / 293 C# files). Out9 -> out11:
23 unitask files (-5,281/+6,061 lines), 36 survivors (-2,258/+2,273), no added
or removed files. Portable **1,845 passed**; frozen-source full suite excluding
parallel: **1,903 passed / 259 skipped / 1 non-strict xpassed**, **one failure**; separate parallel module **2 passed**.
The sole failure is the unchanged Limbus `AddItem` return-number assertion
(`test_inventory_add_item_uses_stack_room`, mi 154731): before local renaming,
return identity is unchanged; final temporary family numbering moved. This
limited proof does not establish equivalence of other changes. **No re-pin.**

An original compiled synthetic nested-generic scope harness passes 50,000 checks,
zero mismatches; a one-arm missing assignment still fails with CS0170. This is
not game runtime equivalence or a speed result. Source freeze lifted only after
both test runs finished. Aggregate-only evidence:
`validation_reports/quality_shared_tail_type_facts_2026-11-03.json`.

Next: investigate the 156 parameterless `Action<InputAction.CallbackContext>`
construction errors in survivors; require exact interface-method/receiver proof
before replacing a shared constructor. Wide SIMD/struct value recovery and
external private BCL implementation references remain unresolved.

### Conservative recovery and real-Editor compile measurements

Working candidate `game_out5` (not promoted): metadata Out-only byrefs now
render `out`, rather than `ref`, in declarations and calls; known root
namespaces shadowed by a child namespace retain `global::`; exact scalar
loads/stores through **actual entry byref aliases** become variable reads/writes.
Byref-typed synthetic phi locals do NOT qualify. Closed generic scalar slices
recover their precise field only after natural layout is proved through nested
valuetype dependencies; explicit/packed/open/unproved layouts decline.

Compile against the installed real Editor engine and BCL plus original player
packages, excluding the current image. `tools/gate.py compile` now supports
`--unity`, `--managed-refs`, and `--body-probe`. Reference filenames merge
case-insensitively, with explicit refs overriding defaults. Compiler-global
errors are counted. The temporary missing-name sentinel checks whether Roslyn
binds **some** method body; it is NOT proof of whole-tree body coverage.
The compile command still exits by the pre-existing syntax gate, not by zero
binding errors; consult both counts and the probe result.

Important phase change: survivors Assembly-CSharp baseline has 63 diagnostics
and sentinel **false**; after declaration fixes it reaches body binding and
has 7,025 diagnostics, sentinel **true**. Do not present this as a 63-to-7,025
regression or compare it to the older stubbed body-tier number. Within the
same observed-body phase, `game_out3` -> `game_out5` is 7,017 -> 7,025;
UniTask is 5,640 -> 5,594. External private/runtime layout references remain
an obstacle; these totals are not pure native-lifting defect counts.

Strict selected-image builds: unitask 481 type emits / 2,227 bodies;
survivors 295 / 1,857; both zero failures, fallbacks and type-emit failures.
Candidate brace/parse gates clean (474 and 293 C# files). Portable baseline
for this slice: 1,731 passed; five targeted game regressions passed. Final frozen
source suite: 1,807 passed / 259 skipped / 1 non-strict xpassed, zero failures
(1,581.67 s), excluding the separately rerun parallel module: 2 passed, zero
failures (958.68 s). No runtime/speed claim is made.
Aggregate-only evidence: `validation_reports/quality_resume_2026-11-03.json`.

Rejected: treating synthetic byref-typed locals as true aliases erased a real
indirect write; publishing whole ref-struct stack values regressed a Vector2
scalar lane. Both were reverted. Honesty takes priority over error count.

Factory identity candidate `game_out8`: early binding is restricted to resolved,
non-getter **static nullary nongeneric own-class CLASS returns**, with byrefs
excluded. Native decoding proves one factory call in UniTask rows 21473/21474;
the output now has one call instead of three. Row 21475 stays at one. The full
selected-image comparison changes only two unitask files (5 removed / 4 added
lines), zero survivors files. All per-image compile code counts and body-probe
results are identical to `game_out5`; brace/parse gates are clean. The broader
reference-return rules were rejected: UniTask 5,594 -> 5,677 or 5,644, and the
broadest survivors firstpass 834 -> 927. Repair generic/stack consumer type
propagation before extending this scope. The 154 CS0311 diagnostics already
existed in the baseline. Factory portable tests: 21 passed. Aggregate evidence:
`validation_reports/quality_factory_identity_2026-11-03.json`.

Validation source freeze: an earlier full suite had identical serial/parallel
output bytes but mismatched source fingerprints because calls.py was edited
between the two builds. It is NOT a clean pass and not an accepted source
regression (`quality_resume_suite_interference_2026-11-03.json`). The final suite
without parallel tests and the separate parallel module both passed on frozen
core sources (counts above); the source freeze is now lifted.

### Exact array stride and scalar members (2026-11-03)

Accepted source candidate `game_out9` (not promoted) normalizes native byte
indices against the **element stride**, not the x64 hardware scale. Only outer
positive constant factors/short shifts are stripped; no division or sum
redistribution is invented. Exact-width whole elements or nongeneric value-type
members recover their actual types. Padding, partial fields, unknown layouts
and wide SIMD slices retain the legacy fallback; wide/multilane copies remain
unresolved, so this is not whole-method equivalence.

Real Editor/BCL + original package references, exact assembly simple names:
UniTask 5,594 -> 5,589; survivors Assembly-CSharp 7,025 -> 6,263; all other
selected images unchanged. Survivors CS0019 2,515 -> 1,274 and CS0029 554 ->
419, but CS0021 **53 -> 609**, CS0266 420 -> 463, CS1061 1,694 -> 1,709,
CS1503 180 -> 185. Exposed object-typed array receivers need separate type-flow
repair, not casts guessed from diagnostics. UniTask.Linq still has a false
body sentinel; other selected images observe it. The sentinel proves some
body binding only; gate exit is still syntax-gated, not zero binding errors.

Strict selected-image rebuilds: unitask 481 type emits / 2,227 bodies and
survivors 295 / 1,857, zero failed/fallback/type-emit errors; brace/parse clean
(474 / 293 C# files). Compared with out8: unitask 1 changed file (-22/+19),
survivors 11 (-2,353/+2,335). Portable 1,826 passed; targeted 45 passed.
Frozen-source full suite excluding parallel: **1,883 passed / 259 skipped /
1 non-strict xpassed**, zero failed (1,424.20 s); parallel module 2 passed,
zero failed (799.87 s). An original compiled synthetic runtime harness checks
71,704 valid-index reads/writes with zero mismatches across strides 376/96/24/40.
This is not a game runtime or speed proof. No pin or output promotion.
Aggregate evidence: `validation_reports/quality_array_element_units_2026-11-03.json`.

### Follow-up: preserve compile assembly identity (2026-11-03)

`tools/compile_gate.py::run_gate(..., assembly_name=...)` now compiles to an
isolated temporary `<original-name>.dll`, not an anonymous gateout DLL. This is
required for real reference assemblies' `InternalsVisibleTo` checks. A minimal
original test library proves anonymous -> exact identity changes CS0122 1 -> 0,
with the body sentinel observed in both. `tools/gate.py compile --only <filter>`
passes the **resolved image name**, never the filter substring; explicit trees
need `--assembly <name>` to assert identity. Both CLIs expose this; the report
records `assembly_name` (null retains legacy anonymous behavior). Output names
are validated as simple names and temporary files cleaned on success/failure.
No assembly version, public key, or signing identity is reconstructed.

On unchanged `game_out8` with real Editor/package DLLs, UniTask.TextMeshPro
235 -> 222 diagnostics (CS0122 15 -> 2), sentinel true both times. UniTask.Linq
still has 13 diagnostics and sentinel false: seven CS0122 become seven CS0052
(publicized fields exposing an internal external type); BCL identity errors
remain. This is measurement repair, not a native-lifting improvement or proof
of body coverage. Portable 1,783 passed; targeted gate tests 40 passed. Core
full-suite evidence above predates only this tools-only change. Aggregate:
`validation_reports/quality_assembly_identity_2026-11-03.json`.

## Previous: 87% of the unitask body tier was ACCESSIBILITY — the real number is 9,619 (2026-11-03, on `main`)

`--publicize` exists as a compile-gate mode (every member public, fields lose
`readonly`); rebuilding unitask with it and re-running the per-image body tier
collapses the number:

| tree | body-tier errors | declaration left |
|---|---|---|
| `full_u10` (normal) | 78,104 | 324 |
| `pub_u1` (`--publicize`) | **9,619** | 248 |

The whole difference is one image: **`Unity.TextMeshPro` 68,111 -> 17**. Its
flood was accessibility — our emitted TMP members are `private`/`protected`
where the source was internal, and C# cascades thousands of name-resolution
errors out of the inaccessible ones. With that gone, the ranking is:
CoreModule 3,662, Assembly-CSharp 2,378, AndroidJNIModule 651,
PropertiesModule 551, PhysicsModule 336, UniTask.TextMeshPro 267,
TextRenderingModule 255, and **UniTask itself 8** (all CS8701).

Publicized top codes: CS0030 1,839, CS0103 1,378, CS1061 1,364, CS0122 711,
CS1503 686, CS0029 683, CS0019 576, CS0266 574, CS0208 316, CS1620 279.

Two lessons, both worth keeping:

1. the per-image body tier must be measured on a **publicized** tree — otherwise
   it measures our member-visibility spelling, not lifting;
2. the read-only-slot/undeclared-temp family (rounds 50-53) is 1,378 CS0103
   after this correction, not 36,942 — still the biggest name family, but a
   fifth of what the non-publicized count suggested.

A survivors publicize build (`pub_s1`, 5 workers) was started at the end of the
round so the same measurement exists for the larger fixture.

## Previous: body tier on BOTH fixtures, per image (2026-11-03, on `main`)

Both fixtures now have a per-image body-tier measurement
(`tools/body_tier_per_image.py`: each image compiled against the original
closure minus its own dll, with the missing-name stub loop):

| fixture | body-tier errors | declaration left | worst images |
|---|---|---|---|
| unitask `full_u10` | **78,104** | 324 | **Unity.TextMeshPro 68,111 (87%)**, CoreModule 3,893, Assembly-CSharp 2,384, UniTask **8** |
| survivors `full_s6` | **30,750** | 582 | CoreModule 11,841, DOTween 5,984, Unity.2D.Common 2,860, ResourceManager 2,495 |

The unitask total is a *one-image artifact*: `Unity.TextMeshPro` is 92 files
carrying 68k errors, so quoting "78,104 for unitask" without that breakdown
misleads — the other 48 images sum to **9,993**. survivors is much more evenly
spread (no image above 12k).

Top families (survivors): CS0030 5,068, CS0122 4,867, CS1061 3,803, CS0103
3,420, CS0019 3,113, CS0029 1,813, CS0266 1,573, CS0208 1,475. Two of those are
*known model artifacts of the per-image shape*: CS0122 (accessibility — our
internal types used from another image; the `--publicize` gate flag exists for
this) and part of CS0030/CS1061 (identity between our copy of a type and the
closure's).

### The `real*` declaration experiment (measured, reverted)

The planning note's family is concentrated in `Unity.TextMeshPro` as `realN`
names. I implemented a `real*`-ONLY variant of the declaration pass (float is
the honest type for a `real` temp) and re-emitted that image:

* before **68,111** (CS0103 35,564, all `real1..realN`)
* after **68,034** (CS0103 35,430, names now `obj6`, `obj10`, `obj31`)

A 0.1% move that only renames the missing identifier. So declaration coverage
is NOT the limiting factor for this family either: the values themselves are
unmodeled, and the `obj*` names that take over are the same read-only-slot
problem. Reverted.

**Conclusion for the next rounds**: the body tier is dominated by unmodeled
native values (read-only slots whose callee outputs were never modeled) and by
per-image identity/accessibility artifacts. Declaration-side text passes are
exhausted; the next real gains are (a) `--publicize`-style measurement to strip
CS0122 from the count, and (b) lifter-side modelling of the callee return that
fills the read-only slots.

## Previous: the body tier's biggest family is an UNDECLARED TEMP (2026-11-03, on `main`)

With the declaration mask gone, CS0103 ("name does not exist") is 36,942 of the
78,104 unitask errors. A census of `UnityEngine.CoreModule`'s 364 CS0103 rows
(quoted name extracted from the localized message) splits them:

| kind | rows |
|---|---|
| **temp** (`obj7`, `num1`, `real6`, ...) | **285 (78%)** |
| runtime helper leaked (`mono_object_unbox_internal`) | 34 |
| the `unknown` marker as a name | 31 |
| other | 14 |

And the temp sites are genuinely undeclared — a full-file search finds no
declaration at all:

```csharp
// ProfilerCategory.cs:29 -- num1 is used three times, declared nowhere
byte[] byteArray1 = (byte[])sub_1801c0840(typeof(byte[]), num1 >> 32);
Marshal.Copy(obj3, byteArray1, 0, num1 >> 32);
return encoding1.GetString(byteArray1, 0, num1 >> 32);

// Application.cs:160 -- obj14 appears only inside a call argument list
object obj13 = sub_1801c07d0(obj12, typeof(Func<bool>), obj14, obj15);
```

So the pipeline renders a temp it never declares. The house convention already
has the shapes needed (`int numN;`, `object objN;`, `float realN;` at method
scale), which makes this look like a *coverage* bug in the declaration passes
rather than a design gap: some lifter-minted temp escapes `_bind`'s
declaration because its first use is inside a nested expression, and nothing
later notices.

Actionable plan (next round, bounded):

1. a final-pass census per method body: temp-shaped tokens
   (`num|real|obj|flag|vector|color` + digits) used but never declared;
2. declare them at method scope with the house types — `num*` -> `int`,
   `real*` -> `float`, `flag*` -> `bool`, `obj*` -> `object`; `vector*`/`color*`
   are NOT safe (their use sites expect a struct) and should decline;
3. measure the CS0103 delta on the per-image body tier.

This is the first body-tier family with a plausible single cause, and at ~28k
of 36.9k CS0103 rows it is worth more than every fidelity slice combined.

### The undeclared-temp family is TYPE loss, not declaration coverage (measured, reverted)

I implemented the planning note's pass — declare every method-scope temp the body
uses but never declares, with the house types (`num*`->`int`, `real*`->`float`,
`flag*`->`bool`, `obj*`->`object`) — and measured it on
`UnityEngine.CoreModule` (442 files, re-emitted with the pass):

| | before | after |
|---|---|---|
| CS0103 rows | **364** | **92** |
| CS0103 "temp" rows | 285 | **13** |
| total errors | 3,893 | **3,913** |

So the declarations do remove the name errors — and the total goes slightly
**up**: 292 errors were converted into CS0266 (+47), CS1061 (+31), CS0019 (+12)
and friends. Declaring `object obj14` where the call expects something else, or
`int num1` where the value is a float, trades one error family for another.

Conclusion, and why it matters: **the CS0103 family is a symptom of the lifter
losing a temp's TYPE, not of a missing declaration.** By the time the text is
rendered, nothing knows what the temp was; a house-type guess cannot recover it.
The pass was reverted (net negative, and it would have obscured the real cause).

Redirect for the next attempt: make the temp carry its type at MINT time — i.e.
`_bind` must declare the temp with the `Expr.ty` it already holds, and every
path that renames or re-homes a temp must keep the declaration with it. That is
a lifter-side fix, and it also explains the `(float2)`/struct-bit-pattern
families: the same type is dropped in three different places.

### Root cause of the undeclared temp: a READ-ONLY stack slot

The raw lifter output for `ProfilerCategory.get_Name` (mi 23293) shows where the
undeclared name comes from — it is not a minted temp at all, it is a stack slot
the body **reads but never writes**:

```
L_181022f6b:
        ProfilerUnsafeUtility.GetCategoryDescription_Injected(this.m_CategoryId, ...)
L_181022fa6:
        s_60 = v6;                       // s_38 is never assigned anywhere
        if (s_40 == null) goto L_181023045;
        var t0 = sub_1801c0840(typeof(byte[]), s_38 >> 32);
        ...
        Marshal.Copy(t1, t0, 0, s_38 >> 32);
```

`s_38` is the high half of a 64-bit return the lifter did not model
(the callee's out/return value), so `slot_var` names it but nothing ever writes
it — and `_rename_locals` then renders it as `num1`, which no declaration pass
can rescue, because every declaration path keys off an ASSIGNMENT or a `_bind`
definition site and this slot has neither.

That is why round 51's house-type declarations failed: they declared the NAME
but had no type, and the uses (`>> 32`, call arguments) need a real one.

Fix design (decline-by-default, matches the `unknown` treatment):

* in the slot-renaming pass, a slot token with no write in the body is NOT a
  value — render it as `default` (spelled through the existing unresolved-value
  path) instead of minting a name;
* that removes the CS0103 without inventing a type, and it is honest: nothing
  in the body knows what the slot held.

Not implemented this round (needs a rebuild + the full gate battery + suite);
the evidence and the design are recorded so it starts from a proven cause.

## Previous: the body tier measured — 78,104 errors on unitask

## Previous: the body tier measured — 78,104 errors on unitask, and every model has artifacts (2026-11-03, on `main`)

With the declaration mask removed, `tools/body_tier_per_image.py` (per image,
stub loop, closure minus the image under test) gives the first body-tier number:

| | value |
|---|---|
| unitask, all 49 images | **78,104 errors**, 324 declaration-tier left |
| top codes | CS0103 36,942 (name does not exist), CS0266 12,627 (cannot convert), CS0841 11,678 (unassigned local), CS0030 3,784, CS1061 2,476, CS0019 2,452, CS0122 1,942, CS0029 1,838 |

That is the honest state of the emitted bodies — three orders of magnitude away
from the "19 errors" the declaration tier was reporting, and it must replace
that number in every claim about recompilability.

Two model artifacts are already visible in these numbers and must be understood
before the number is optimised:

* **per image**: our image may declare types the closure ALSO ships (unitask's
  `Assembly-CSharp` contains copies of `TMPro/Examples/*` that
  `Unity.TextMeshPro.dll` also provides) — that is CS0030/CS0433 identity noise,
  and it inflates the AC image to 2,384 errors on 15 files;
* **whole tree**: cross-image duplicates (CS0101/CS0102/CS0111) are declaration
  errors and mask again.

The clean measurement therefore needs a third model: compile our whole tree as
ONE assembly against a *stub-only* closure (every external name stubbed, no
real assembly whose types we also emit). That is a scaffolding job of its own
and is the next measurement task.

What is already actionable from the top codes: CS0103 (36,942, nearly half) and
CS0841 (11,678) are *name resolution* families — a bounded investigation of the
missing names should be the first fidelity pass now that the mask is gone.

## Previous: the body tier is measurable, and it is large

## Previous: the body tier is measurable, and it is large (2026-11-03, on `main`)

Last round found that **a declaration error suppresses ALL body binding**. This
round built the driver that removes that mask and took the first measurement.

`tools/body_tier.py` copies the source list, compiles, reads the CS0234/CS0246
names out of the report, appends `internal class <Name> { }` stubs (in their
namespace) and recompiles, up to N rounds.

Two results:

1. on a declaration-CLEAN 28-file folder the compile went from **1 error to
   4,636** — including the injected probe that had been invisible for five
   rounds. The mask is real and total.
2. on the whole unitask tree, once CS0234/CS0246 are stubbed away, the count is
   **357 errors**, dominated by CS0111 (273), CS0102 (36) and CS0101 (29):
   duplicate types and members, i.e. the *cross-image* artifact of compiling 49
   assemblies as one (CS8701 18 + CS0644 1 as before).

So the whole-tree number cannot be the body tier either — the duplicate
families are themselves declaration-tier and mask again. The measurement has to
be **per image** (no duplicate types, the closure supplies the siblings, which
is exactly what `gate.py compile --managed-refs` already does).

Plan for the next round: run the stub loop per image (49 for unitask, 75 for
survivors), sum the remaining errors, and *that* is the number worth optimising
and quoting.

## Previous: FOUND — a declaration error suppresses ALL body binding

## Previous: the whole suite is green on the current source (2026-11-03, on `main`)

`PYTHONHASHSEED=0 python -m pytest -q` with the game fixture registered:

```
1705 passed, 259 skipped, 1 xpassed in 1610.93s (0:26:50)
```

That covers the portable unit tests, the game-declaration/golden tests and the
fixture-backed pins, on the source that carries fixes 195-202. It is the first
full-suite run since the fixture-based measurement workstream started, so it is
the broadest regression evidence in this arc.

### The last structural slice is not reachable by a text pass (measured)

`_tidy_gotos` already collapses four goto shapes; the residue in the engine
images is `if (cond) { goto L_xxx; }` where `L_xxx` is a shared block WITH SIDE
EFFECTS (`BackgroundPropertyHelper`: the label body builds and assigns a
`BackgroundPositionKeyword`). I added a branch that duplicates a label's body at
the jump site when the body is a single PURE `return ...;` — sound, since a
`goto` jumps straight there — and measured **UIElements gotos 562 -> 562,
labels 457 -> 457**: no effect, because these labels are not returns. Reverted.
Recovering them means teaching `_seq` the *early-return* shape (the source's
`if (cond) return X;` that the structurer turned into a jump to a trailing
block), not post-processing text.

### FOUND: a declaration error suppresses ALL body binding (this changes every compile number)

The binding question is answered, and the answer invalidates the compile tier as
a quality metric.

**Any declaration-level error in the compilation makes Roslyn skip method-body
binding entirely.** Evidence: the 28-file `TMPro/Examples` folder compiled with
a stub `__SharedBodyStubs` + `TMP_TextEventHandler` — i.e. declaration-clean —
reports **4,636 errors**, including 18 rows for one file and my injected
`int __probe = "x";`. The same folder *with* one declaration error reports
**1 error** and no body diagnostics at all.

Consequences:

* `19 errors (unitask)` and `118 errors (survivors)` are **declaration-tier
  counts**. They are NOT a measure of whether the emitted bodies compile; the
  body tier is unmeasured in every number this project has quoted since the
  fixture workstream began.
* A single missing type (CS0246) anywhere in the compilation hides thousands of
  body errors — the same masking rule already known for CS1519, but global.
* The four earlier "anomalies" (silent `int -> Vector2`, appended probes
  ignored, byte-verified edits not registering, `-errorlimit` runs reporting
  nothing) are all explained by this one rule: every one of those compilations
  carried declaration errors.

Next step, precise and cheap: make the diagnostic compilation
declaration-clean, then count the body tier —

1. merge the per-image `__SharedBodyStubs` (already done by `compile_corpus`);
2. loop: read the CS0234/CS0246 names from the report, emit
   `internal class <Name> { }` stubs into a `__MissingStubs.cs`, recompile,
   repeat until the declaration tier is empty;
3. the remaining error count is the real body tier, and *that* is the number to
   optimise.

### Binding scope: final evidence table, cause still unknown (do not re-open blind)

Every experiment on the emitted trees reports DECLARATION-tier diagnostics and
almost no BODY-tier ones. Recorded so the next session starts from the table:

| compilation | files | body-level errors reported |
|---|---|---|
| 28-file folder (`TMPro/Examples`) | 28 | **0** (29 errors, all CS0246 for the unresolved `using static __SharedBodyStubs`) |
| same folder + a stub `__SharedBodyStubs` class | 29 | **0** (1 error total) |
| the probed file under a neutral file name, same content | 28 | **0** — so it is the content/context, not the path |
| 280-file `Assembly-CSharp` image | 280 | **2 of 27** injected body probes reported |
| whole survivors tree | 4,413 | all 118 errors look declaration-level |
| a hand-written standalone probe file, same closure | 1 | CS0029/CS0117 as expected |

Ruled out: the error limit (not reachable at 63), duplicate declarations (none
for these types), an unresolved `using static` (adding the stub changed
nothing), the file name (a neutral name behaves identically).

Still standing: with the *emitted* files, Roslyn reports declaration errors and
does not report body errors — in every shape from one file to the whole tree —
while a hand-written file with the same compiler and closure reports them fine.

**Consequence for every number this project quotes**: the compile tier measures
DECLARATIONS. Body-level correctness of the emitted trees is unmeasured, so
"19 errors (unitask) / 118 (survivors)" must not be read as "the bodies
compile". Parse (tree-sitter), brace and the source comparison are unaffected
and remain valid evidence.

Do not spend more rounds on this without a new hypothesis; the next real probe
would be a Roslyn-level one (compile the same text through `Microsoft.CodeAnalysis`
directly and inspect the diagnostics list), not another csc invocation.

### The binding-scope question is OPEN and the probe method is unreliable

Trying to size how many files have their method bodies bound went badly, and
the honest record is that the probe method itself is not trustworthy:

* injecting `int __probe = "x";` into the first method body of every 10th file
  (27 files, insertion verified in one by reading the file back) produced **2 of
  27** reported, with the total error count unchanged at 63;
* swapping the probe for a missing-member call (`this.__probe_missing();`)
  produced the **same 2 of 27**, so it is not error-kind-specific;
* recompiling with `-errorlimit:9999` reported **0 errors** and 0 probes --
  i.e. that run silently did nothing, exactly like the earlier "appended file"
  and "nonexistent file" experiments.

So the harness has a failure mode where csc exits without diagnostics, and I
cannot tell a genuine "body not bound" from that mode. Two independent
probe shapes agreeing (2 of 27) argues for a real phenomenon, but a run that
reports zero errors proves the driver is fragile.

Important corollary: **all 118 reported errors appear to be declaration-level**
(CS0234, CS0117 from const initializers, CS8701, CS0111, CS0535, CS0507,
CS0051/52/53, CS0460, CS8345, CS0100, CS0644, CS0115). If bodies really are
mostly unbound, the binding tier is under-reporting substantially -- and the
"19 / 118" figures describe declarations only.

Next step, precise: stop using raw `csc` with a response file. Write a minimal
`.csproj` (`<Compile Include="**/*.cs"/>`, `<NoWarn>` set, `<AllowUnsafeBlocks>`)
next to the tree copy and run `dotnet build`, then read the MSBuild output.
That removes the response-file/option layer that keeps producing silent no-ops.

### Measurement caveat: some files' METHOD BODIES are not bound (unexplained)

Four experiments, all on `Assembly-CSharp/TMPro/Examples/TMP_UiFrameRateCounter.cs`:

1. the tile contains `int num1;` and `rectTransform1.pivot = num1;` where
   `rectTransform1 : RectTransform` and the emitted `RectTransform` declares
   `public Vector2 pivot` — an isolated probe with the same closure is
   **CS0029** for the same assignment, yet the 280-file image compile and the
   whole-tree compile report **nothing** for the file;
2. replacing the file's content with `class {` DOES report 2 errors for it
   (CS1001/CS1513) — the file is read and the DECLARATION tier is reached;
3. a byte-verified `int __bad = "x";` inserted INSIDE a method body (single CRLF
   asserted on disk) still reports nothing;
4. an injection at namespace level reports CS0116 for the same file.

So: declarations are analysed, method bodies are not. And it is not a property
of "files with float bit patterns": **8 of the 162** such files do get
diagnostics in the whole-tree compile.

This is a real caveat for the compile-tier numbers: they may under-report for
some files, and I have no measurement of how many. Everything else about the
trees is unaffected (parse, brace, fidelity), but the "19 / 118 errors" figures
should be read as a lower bound until the binding scope is understood.

Practical way forward if this ever matters: compile a copy with a
deliberate body-level error in every Nth file and count how many stay silent —
that sizes the unbound fraction directly.

### The largest remaining expression family: structs built field-wise from bit patterns

Census of `<temp> = <9-10 digit literal>;` across both trees:

| tree | sites | files |
|---|---|---|
| survivors `full_s6` | **932** | 158 |
| unitask `full_u10` | **471** | 64 |

Sampled shapes show three variants, all "a struct assembled component by
component, one component written as a float bit pattern":

```csharp
// Vector3 (MeleeEnemy)
real5 = 1065353216;                 // 1.0f
real3 = real5;
this.transform.localScale = vector31;

// Vector3 (Benchmark02)
vector32 = 1036831949;              // 0.1f
vector31 = vector32;
gameObject3.transform.localScale = vector32;

// Color (Benchmark02)
color1 = 4278255615;                // 0xFF00FF00
color1 = 255 / 255.0f;
tmpText1.color = color1;
```

This is the same aggregate/composition area the audit already deferred as
"value-type fragment discard": the lifter sometimes merges the parts
(`obj5 = (float2)(1.0f, 1.0f)` does appear) and sometimes leaves them as raw
bit-pattern stores into a temp that is then assigned to a struct-typed member.
A text-level rewrite would have to *guess* the missing components, so the fix
belongs in `_piece_value`/`_aggregate_load` (compose the sibling stores into one
literal), not in a pass.

The sub-case split matters: for a **float** temp (
eal5 = 1065353216;) the
assignment is LEGAL C# (implicit int->float) and silently yields 1.07e9 instead
of 1.0f — a semantic defect with no diagnostic — while a **struct** temp
(color1 = 4278255615; with Color color1) should be CS0029. Census of the
float sub-case on Assembly-CSharp: only **2** sites, so the bulk of the 932 are
struct-typed temps and belong to the composition work.

Note the connection to the open anomaly: these store shapes are exactly what
`TMP_UiFrameRateCounter.cs` contains, and that file is one where the compiler
reports nothing although an `int -> Vector2` assignment is present. Whether the
family's compilability is real cannot be settled while that anomaly stands —
which raises its value from "curiosity" to "blocks a 1,400-site family's
assessment".

### The goto residue: the shape is `if { work; goto L; } else { ... }` with L far below

Dumping `_tidy_gotos`'s INPUT for `ResolveUnityBackgroundScaleMode`
(UIElements, 367 lines, 16 gotos in, 8 out) shows the actual shape:

```
if (s_30 != BackgroundPositionKeyword.Center)
{
    v158 = t1012;
    v159 = v95;
    goto L_181eb9012;          <- last statement of the if arm
}
else
{
    s_30 = 0;
    s_30.ctor(0f);
    ...
    if (!t1015)
    {
        v158 = t1015;
        v159 = v95;
        goto L_181eb9012;      <- and one nested inside the else
    }
    ...
}
... more code ...
L_181eb9012:
```

Three text-level attempts were measured and all declined or had no effect:

1. duplicating a PURE `return ...;` label body at the jump site — these labels
   are not returns (they build and assign a value), gotos 562 -> 562;
2. inverting a single-statement guard — the arms carry work before the goto;
3. dropping a `goto L;` whose label immediately follows the enclosing if/else —
   the label is NOT adjacent; more code and other statements sit between.

So the shared tail genuinely is shared, and reaching it means restructuring the
CFG so the tail is emitted once after the chain and each arm *falls through* to
it: `_seq` must recognise the "all arms converge on block T" case (which is a
join, not a jump) instead of emitting a goto to a label. That is structurer
work; the text layer cannot see the join.

Measured cost of leaving it: 7,595 gotos tree-wide on the survivors fixture
(562 in UIElements, 29 in Assembly-CSharp).

## Previous: both fixtures on one source revision, measured end to end (2026-11-03, on `main`)

## Previous: both fixtures on one source revision, measured end to end (2026-11-03, on `main`)

With fix 202 in, both complete trees were rebuilt and gated with the new
`tools/gate_all.py` (one command: brace, per-image tree-sitter, whole-tree
Roslyn against the exact closure, source comparison):

| | unitask `full_u10` | survivors `full_s6` |
|---|---|---|
| type files / bodies | 3,596 / 23,756 | 7,523 / 80,091 |
| brace | 3,547 files, **0 unbalanced** | 7,448 files, **0 unbalanced** |
| tree-sitter (per image) | **0/0/0/0** | **0/0/0/0**, no image crashed |
| whole-tree Roslyn | **19** (CS8701 x18 + CS0644 x1), `binding_masked: false` | **118**, `binding_masked: false` — CS0234 x61, CS0117 x16, CS8701 x14, CS0111 x7, CS0535 x6, CS0507 x4, CS0052 x2, CS0460 x2, CS8345/CS0100/CS0644/CS0115/CS0053/CS0051 x1 |
| fidelity | call_f1 0.6168 / member_f1 0.3255 / shape 0.7915 | call_f1 0.6666 / member_f1 0.3619 / shape 0.5844 |
| sources/switch (`switch (` / `else if (`) | 235 / 4,928 | 729 / 14,692 |

fix 202's measured effect on the survivors whole tree: `switch (` **709 -> 729**,
`else if (` **14,737 -> 14,692**, `goto` unchanged at 7,595 — so the gain is
bigger than the Assembly-CSharp A/B suggested (+6 there, +14 in the engine
images). Across both fixtures the fix is **+25 switches**.

Compile tier: every remaining error is either a property of the one-assembly
measurement (CS0234 doubled namespace x61, CS0111 cross-image scaffolding x7,
CS0051/52/53 cross-assembly internals, CS8701 profile x14, CS0117 x16) or a
generic-sharing body that is absent from the game's own metadata (CS0535 x6).
No confirmed decompiler defect remains in that tier on either fixture.

### The goto residue is guard jumps to a SHARED COMPLEX block, not to a return

`_tidy_gotos` already collapses four goto shapes; the remaining ones in the
engine images are `if (cond) { goto L_xxx; }` where `L_xxx` is a shared block
with real work, e.g. in `BackgroundPropertyHelper`:

```csharp
if (!((bool)sub_181f4c290(...)))
{
    L_181eb8ef5:
    backgroundPositionKeyword1 = 0;
    backgroundPositionKeyword1.ctor(0f);
    ...
}
```

I added a branch that duplicates a label's body at the jump site when the body
is a single PURE `return ...;` (no call, no `new`, no `++`, no comma, no
conditional, no assignment), which is sound because a `goto` jumps straight
there. **Measured on UIElements: gotos 562 -> 562, labels 457 -> 457 — no
effect**, because these labels are not returns; they are shared continuations
with side effects, and duplicating those would change the call count. The
branch was reverted.

So the residue needs either (a) an *early-return shape* recovered in `_seq`
(the source's `if (cond) return X;` that the structurer turned into a jump to a
trailing block), or (b) nothing — the honest `goto` stays. This is the one
structural slice that a text pass cannot take; it belongs to the CFG
structurer.

## Previous: fix 202 verified on both fixtures (2026-11-03, on `main`)


The switch synthesis landed and was re-measured on both fixtures with full
rebuilds:

| fixture | `switch (` | `else if (` | gates |
|---|---|---|---|
| unitask `full_u9` -> `full_u10` | 230 -> **235** | 4,940 -> **4,928** | brace 0, tree-sitter 0/0/0/0, whole-tree compile **19** (CS8701 x18 + CS0644 x1, `binding_masked: false`) |
| survivors `Assembly-CSharp` (same 293 files) | 5 -> **6** | 152 -> **150** | n/a (image-level A/B) |

So the fix is worth +11 switches across the two fixtures (`Set_FrameCounter_
Position` on the survivors side, five more on unitask), every one of them a
chain over an enum that the source itself wrote as a `switch`. unitask's
fidelity is unchanged to four decimals (call_f1 0.6168 / member_f1 0.3255 /
shape 0.7915), which is expected: swapping an if-ladder for a switch keeps the
call/member sequences and barely moves the construct histogram.

The survivors full rebuild (`full_s6`, 4 workers) was still running at the end
of the round; its gates are the next measurement.

## Previous: fix 202 — switch synthesis restored for enum chains (2026-11-03, on `main`)


The switch slice needed **both** halves; either alone measures as no change
(5 -> 5 switches on Assembly-CSharp, the previous round's negative result).

1. **Repeated index shifts.** MSVC lowers a switch dispatch as a CHAIN of
   shifts, so one subject appears as `x - 1`, `x - 1 - 1`, ... across arms.
   fix 197's `_enum_shift_fold` only matched a single `X - N` (its left side had
   to be a plain dotted identifier), so three of the four arms kept the shifted
   spelling — and `_switch_synth` then saw *different subjects* and refused the
   chain. The fold now accepts `X - a - b - ...` and shifts by the sum.
2. **Enum case constants.** `_switch_synth` accepted only int/hex/char labels.
   An enum member IS a compile-time constant (`case Enum.Member:`), and the
   proof comes from metadata through fix 197's enum table — a plain static field
   is not (CS0150) and still declines.

Measured on `Assembly-CSharp` (same 293 type files):

| | before | after |
|---|---|---|
| `switch (` | 5 | **6** |
| `else if (` | 152 | **150** |

and `TMP_UiFrameRateCounter.Set_FrameCounter_Position` — a 33-line source
switch over four anchor positions — now emits as one, where it was four
`else if (anchor_position == FpsCounterAnchorPositions.X)` arms.

Portable 1,656 passed (the fix-197 tests still cover the single-shift form);
game pins 5 passed.

## Previous: switch synthesis on enum chains — the const gate is not the blocker (2026-11-03, on `main`)

## Previous: current-source state of both fixtures re-measured (2026-11-03, on main)

The unitask tree was rebuilt with the current source (fixes 198-201) and gated
end to end, so both fixtures now have a same-source measurement:

| fixture | brace | tree-sitter | whole-tree compile | fidelity |
|---|---|---|---|---|
| unitask ull_u9 (3,547 files) | 0 unbalanced | 0/0/0/0 | **19 errors** (CS8701 x18 default-interface-method artifact + CS0644 x1 IL2CPP-internal ValueType subclass), inding_masked: false | call_f1 0.6168 / member_f1 0.3255 / shape 0.7915 |
| survivors ull_s5 (7,448 files) | 0 unbalanced | 0/0/0/0 | **118 errors**, all traced to the one-assembly model or tracked families (CS0234 x61 doubled namespace, CS0117 x16 profile, CS8701 x14, CS0111 x7 cross-image scaffolding, CS0051/52/53 x4, CS0535 x6 generic-sharing) | call_f1 0.6666 / member_f1 0.3614 / shape 0.5844 |

unitask's fidelity is bit-identical to the pre-200/201 tree, which is the
expected result: those fixes change specific body shapes (struct fragments,
second-branch conditions) that these aggregates do not weight, and the compile
tier is declaration-driven.

source_compare also gained a fix: its worst-delta sort compared dicts when
two magnitudes tied (a TypeError on the unitask tree).

### Switch synthesis on enum chains: the const gate is not the blocker

`_switch_synth` accepts only int/hex/char literals as case labels, so a chain
over an ENUM can never synthesize. I opened that gate with a metadata proof
(an enum member is a compile-time constant; a plain static field is not, CS0150)
and measured the result on `Assembly-CSharp`: **switch count 5 -> 5, else-if
152 -> 152** — no change, so the const gate was not the blocker and the patch was
reverted rather than kept as dead code.

Instrumenting the pass on `TMP_UiFrameRateCounter.Set_FrameCounter_Position`
shows the first arm passes EVERY early gate (`_SWITCH_CMP_RX` matches,
`_SWITCH_SUBJ_RX` accepts `anchor_position`, and the enum-constant check accepts
`FpsCounterAnchorPositions.TopLeft`), so the decline happens in the arm scan
that follows: `_match_brace(lines, pos)` or the `bad` predicate (break/goto/label
inside an arm) or the `else if` continuation.

Next step: instrument `okchain` and the per-arm `bad` flag inside
`_switch_synth` on that method and read the first `okchain = False` reason. Only
then re-open the const gate — both changes are needed together, and neither is
worth shipping alone.

## Previous: the shape-delta census — what the fidelity gap actually is (2026-11-03, on main)

## Previous: the shape-delta census — what the fidelity gap actually is (2026-11-03, on `main`)

`shape_cos` (0.584 on survivors, 0.792 on unitask) collapses the structural
difference into one number. `source_compare` now also records a per-construct
delta histogram over the whole matched population plus the methods with the
largest deltas, which answers *what* runs long:

| delta | methods |
|---|---|
| `return+1` | 258 |
| `new+1` | 118 |
| `if+1` | 117 |
| `while+1` | 54 |
| `return-1` | 49 |
| `if+2` / `if+3` | 36 / 36 |
| `try+1` | 28 |
| `for-1` | 27 |

The worst offenders are all the SAME mechanism — IL2CPP inlining inflates the
statement count:

* `TMP_TextSelector_B.LateUpdate` — src 8 ifs / 2 fors / 1 switch, out **32
  ifs** / 2 whiles / 3 gotos (the switch became an if chain and `Vector3`
  helpers inlined);
* `TypeRegistry.EnsureInitialized` — src **1 if**, out **33 ifs** + a try + a
  while (the static-initialization helper fully inlined);
* `CameraController.GetPlayerInput` — src 23 ifs, out 48.

Two of them are actionable and already tracked:

* **`Set_FrameCounter_Position`** — fix 197 made every comparison correct
  (`anchor_position == FpsCounterAnchorPositions.BottomLeft`), but
  `_switch_synth` still leaves the 4-case chain as `if`/`else if`, and the
  struct-constant stores (`num1 = 1008981770; rectTransform1.pivot = num1;`)
  are still raw bit patterns: fix 200 covered the narrow *load* at a struct
  field, not the wide *store* that builds the struct.
* `return+1` x258 is mostly the harmless trailing `return;` in void methods
  (196 occurrences in Assembly-CSharp alone), not a defect.

So the fidelity ceiling on these fixtures is dominated by inlining, and the
remaining actionable slices are the wide struct store and switch synthesis on
else-if chains.

### Unresolved anomaly: one int -> Vector2 assignment the compiler accepts

`Assembly-CSharp/TMPro/Examples/TMP_UiFrameRateCounter.cs` contains

```csharp
int num1;
...
num1 = 0;
rectTransform1.pivot = num1;      // rectTransform1 : RectTransform, pivot : Vector2
...
num1 = 1008981770;
rectTransform1.anchorMin = num1;
```

and no compile of that image (280 files, original `UnityEngine.CoreModule` in
the closure) reports anything for the file — verified by compiling the image
directly and grepping every diagnostic line for the file name: **0 lines**.
Yet a minimal probe with the same closure and the same assignment
(`int n; r.pivot = n;`) is **CS0029**, and `RectTransform` in the emitted tree
declares `public Vector2 pivot`.

So either the file that the compiler sees differs from the one on disk (nothing
in the harness suggests that: the same 280 files were passed), or some aspect
of the enclosing `partial` type changes the member lookup. Until this is
understood, treat "this file compiles clean" as unproven; the tree-wide counts
(118 errors on survivors, 19 on unitask) are unaffected either way, but the
*reason* a given file is silent is not always "it is correct".

Next probe: compile the exact 15-line region verbatim inside a copy of the
enclosing type, then delete members of the real file one at a time until the
behaviour flips.

### The appended-probe harness is unreliable (corrects the previous note's probe plan)

Trying to bisect the `int -> Vector2` anomaly with an extra probe file appended
to an image compilation produces **no analysis of that file**:

* an appended file whose content is `int x = "this must fail";` reports
  nothing (the compile still reports only the image's own 2 errors);
* an appended file that does not exist makes csc exit 1 with **no diagnostic
  lines at all** (284 chars of output, both CS8701/CS0644 rows, and nothing
  about the missing file);
* the same machinery with the probe as the ONLY source works (that is how the
  CS0029/CS0117/CS0029 probes in the previous rounds were run).

So csc silently ignores the appended source in this invocation shape, and none
of this round's `with_probe` results may be used as evidence. The image-level
compilation the gates run (`compile_corpus`, `gate.py compile`) passes exactly
the image's own file list, and those numbers stand.

The original observation is unchanged and still unexplained: within the
280-file `Assembly-CSharp` compilation, `TMP_UiFrameRateCounter.cs` gets no
diagnostic although it contains `rectTransform1.pivot = num1;` with
`int num1` — while a single-file probe with the same closure and the same
assignment is CS0029. Next attempt should NOT append a probe file: copy the
image directory, edit the *real* file there, and compile the copy.

### The bisect is inconclusive (both halves measured)

Two halves of the same experiment, on a COPY of the `Assembly-CSharp` image:

* replacing `TMP/Examples/TMP_UiFrameRateCounter.cs` with `class {` DOES report
  **2 errors for that file** (CS1001/CS1513) — so the file is read and analysed,
  and the parse tier is reached (note the total dropped to 2: the syntax errors
  suppress every binding diagnostic, the masking rule again);
* inserting `int __bad = "x";` after `rectTransform1.pivot = num1;` in the same
  file reports **nothing** (63 errors, identical to the unmodified image).

Both cannot be true unless the second edit did not reach the compiler: the copy
was written with `newline='\r\n'` on content that already carried `\r\n`, which
doubles the CR bytes; csc tolerates that for parsing but the experiment is
therefore not clean. The anomaly (`int -> Vector2` accepted) stays **open**.

Next attempt: after editing the copy, read the bytes back and assert the
inserted text is present with single CRLF, then compile. If the error still does
not appear, dump the compiler's file list (`-errorlog` / a deliberate duplicate)
to see which physical path it used.

### Anomaly status: OPEN, low value, do not chase

The `int -> Vector2` silence is now measured with a clean edit and still
unexplained:

* a COPY of the `Assembly-CSharp` image had `int __bad = "x";` inserted right
  after `rectTransform1.pivot = num1;`, with the bytes read back and asserted
  (marker exactly once, insertion exactly once, no doubled CR), the file
  confirmed in the compiler's source list — and the compile still reports the
  same **63 errors, none for that file**, although `int __bad = "x";` alone is
  CS0029;
* replacing the same file's content with `class {` DOES report 2 errors for it
  (CS1001/CS1513), so the file is read and the parse tier is reached.

So the compiler analyses the file's *syntax* but not its *semantics*. The most
plausible remaining explanation is a type-identity conflict with the reference
closure (the emitted `TMPro.Examples.TMP_UiFrameRateCounter` may collide with a
type the closure also exposes), but no probe has confirmed it and the practical
impact is nil: the tree-wide counts come from the same gate for every file, and
one silent file does not change any family.

**Decision: stop investigating.** Recorded here so the next session does not
re-open it without new evidence. If it ever matters, the cleanest probe is to
compile that ONE file with `-errorendlocation` plus a deliberate duplicate-type
declaration to see which copy the compiler binds.

The consequence worth keeping in mind: the *wide struct store*
(`num1 = 1008981770; rectTransform1.pivot = num1;`) is a fidelity defect whose
*compilability* impact cannot be demonstrated while this anomaly stands — so any
fix for it must be justified by fidelity alone, not by gate numbers.

## Previous: the survivors tree's first UNMASKED compile number — 118 errors, 75 explained (2026-11-03, on `main`)


`out/survivors-roguelike-kit/full_s5` (fixes 198-201, 7,523 type files / 80,091
bodies) is the first complete survivors tree whose compile number is not
suppressed by a syntax error:

| gate | result |
|---|---|
| brace | 7,448 files, **0 unbalanced** |
| tree-sitter (per image) | 7,448 files, **0 bad / 0 ERROR / 0 MISSING / 0 recovery**, no image crashed |
| whole-tree Roslyn (4,413 sources, exact closure) | **118 errors in 59 files**, `binding_masked: false` |

| code | n | verdict |
|---|---|---|
| CS0234 | 61 | **artifact of the one-assembly model**: the fixture's own metadata declares 3 types in a DOUBLED namespace `RGame.RoguelikeKit.RGame.RoguelikeKit` (real rows 8054-8056), so inside `namespace RGame.RoguelikeKit` the compiler binds `RGame` to that nested namespace and `RGame.RoguelikeKit.BaseBulletShootState` stops resolving. In the real project those types live in another assembly |
| CS8701 | 14 | default-interface-method artifact of the netstandard2.0 closure |
| CS0117 | 16 | `float.PositiveInfinity` as a DEFAULT PARAMETER VALUE (`UnityEngine.PhysicsModule/PhysicsScene.cs`, `float maxDistance = float.PositiveInfinity`): the compiler says `float` has no such member there. Open — `PositiveInfinity` is a `const` in classic Mono mscorlib, so what `float` binds to in a default-argument position needs a look |
| CS0111 7, CS0535 6, CS0507 4, CS0460 2, CS0052 2, CS8345 1, CS0100 1, CS0644 1, CS0053 1, CS0051 1, CS0115 1 | 27 | real member/accessibility families, sized and to be triaged next |

So the earlier "4 errors" was exactly the trap the new `binding_masked` flag
warns about: the tree actually carries ~118, of which ~75 are model artifacts
and ~43 are real defects in emitted members.

### Triage of the survivors tree's 27 "real" errors

Of `full_s5`'s 118 binding errors, 75 are model artifacts (CS0234 x61 from the
fixture's own doubled namespace, CS8701 x14 from the netstandard2.0 closure).
The remaining 27 split again, and most are *also* artifacts of compiling 75
assemblies as one:

* **CS0111 x7** — the SAME generated scaffolding emitted in several images
  (`IsReadOnlyAttribute` in `Unity.Burst.Unsafe`, `ThrowStub` in
  `System.Xml.Linq`, `_BurstDirectCallInitializer` in `Unity.Burst`,
  `Unity.2D.IK.Runtime` and `Unity.Collections`). Separate assemblies in the
  real build; a duplicate definition when merged.
* **CS0051/CS0052/CS0053 x4** — a `Locale` field/property/parameter less
  accessible than its member: the type is `internal` in the assembly that owns
  it, and the accessor lives in another.
* **CS0535 x6** — interface members with no emitted body, the generic-sharing
  family already documented for `ArrayBufferWriter<T>.GetSpan` (the member is
  absent from the game's own metadata).
* **CS0507 x4, CS0460 x2, CS8345 x1, CS0100 x1, CS0644 x1, CS0115 x1** — mixed
  modifier/accessibility rows, sized for a later pass.

**CS0117 x16 is a closure artifact, verified**: every site is
`float.NaN` / `float.PositiveInfinity` / `double.NaN` / `double.PositiveInfinity`
in a `const` initializer (`Unity.Mathematics.math`, `PhysicsScene`,
`Rigidbody2D`, `LayoutNode`). Against the fixture's player-build mscorlib those
members are **not compile-time constants** (a `const` probe fails with CS0117
while an ordinary expression compiles), so the source's own
`public const double INFINITY_DBL = double.PositiveInfinity;` cannot compile
against that profile — the emission is faithful, the profile differs from the
one the package was written for.

Net: after artifacts, the survivors tree has **no confirmed decompiler defect
of its own** in the compile tier; the remaining families are generic-sharing
stubs and modifier rows, both already tracked.

## Previous: consolidated state of the two fixtures (2026-11-03, on `main`)


The measurement that decides "near-complete recovery and near-recompilable" is
per fixture, and both are close. All numbers below are from trees built with
the current source unless noted.

### unitask (49 images, 3,596 type files, 23,756 bodies) — `full_u8`

| gate | result |
|---|---|
| brace | 3,547 files, **0 unbalanced** |
| tree-sitter | **0 bad / 0 ERROR / 0 MISSING / 0 recovery** |
| whole-tree Roslyn (2,220 sources, exact closure) | **19 errors**: CS8701 x18 (default-interface-method artifact of the netstandard2.0 closure), CS0644 x1 (`Il2CppFullySharedGenericType : ValueType`, an IL2CPP-internal type C# forbids) |
| source comparison | 1,327 matched methods, call_f1 0.617, member_f1 0.325, shape 0.792 |
| unmatched population | every category explained: `stub` 2,283 (generic definitions with `addr=0`), `transformed` 544, `type` 121 (editor/package types absent from the player build), `inlined` 55, `empty_src` 28 / `empty_srcout` 32 / `empty_out` 4 (`[Conditional]` and `#if`-stripped bodies) |

### survivors-roguelike-kit (75 images, 7,523 type files, 80,091 bodies)

| gate | result |
|---|---|
| brace | 7,448 files, **0 unbalanced** |
| tree-sitter, per image | 7,448 files, **0 bad / 0 ERROR / 0 MISSING / 0 recovery** (two images kill the single-process parser; both are 0/0/0/0 in batches) |
| whole-tree Roslyn | `full_s3` read "4 errors, all CS1519" — **masked** (a syntax error suppresses every binding diagnostic), and fix 199 removed that family; the unmasked number comes from `full_s5` |
| source comparison | 810 matched methods, call_f1 0.667, member_f1 0.361, shape 0.584 |

Both fixtures' remaining *text* differences are dominated by IL2CPP inlining
(`Bounds.Equals` expanded into `IsNaN` comparisons, `TrySetResult` inlined into
promise `MoveNext`, `List<T>.Add` inlined to the `_version`/`_size`/`AddWithResize`
triple, 457 sites), which no decompiler can un-inline honestly.

## Previous: fixes 200/201 — struct fragments and the two-branch float compare (2026-11-03, on `main`)


Both come from one 33-line method on the survivors fixture,
`RGame.ScriptableCoreKit.SetScaleStateNode.Validate`, whose source is

```csharp
if (targetScale.x == 0f || targetScale.y == 0f || targetScale.z == 0f)
    issues.Add("Target scale contains zero values, ...");
```

and whose emitted form was an empty-typed `float.IsNaN(this.targetScale)` plus a
label cascade (nine ifs, four gotos, labels *inside* if bodies).

**fix 200** — `_aggregate_load` returned None as soon as a load's offset was ANY
field offset, so `movss xmm0,[rbx+30h]` (a 4-byte read of a `Vector3` field) fell
through to the whole-field render and the operand became the struct. The narrow
case now slices through metadata (`<field>.<first component>`, proved at that
exact width). 2,823 `float.IsNaN(...)` sites exist tree-wide and every one whose
operand is a struct field was type-wrong.

**fix 201** — MSVC lowers a float comparison to ONE compare and TWO branches
(`ucomiss; jp NaN_arm; je equal_arm`), and the jcc handler cleared the flags
operands after the first, so the second printed `? == ?` and the decompiler had
no condition to work with. The operands now stay; staleness is already covered
by `_flags_mn` (any flags-writing instruction, calls included, updates the
setter, and `flag_cond` declines what it cannot derive).

Result on that method:

```csharp
if (float.IsNaN(this.targetScale.x)) goto L_1803d5ad5;   // jp short
if (this.targetScale.x == 0f) goto L_1803d5aed;          // je short  (was ? == ?)
```

every component's condition now the source's own comparison. Portable 1,656
passed, pinned bodies unchanged.

A full survivors rebuild with fixes 198-201 is in flight (`full_s5`); the
earlier `full_s4` run (198/199 only) was cancelled at 20/75 images rather than
measured, since 200/201 change the very shapes it would have counted.

### Correction: the sret byte-stores are a fidelity issue, not a compile error

An `UniTask` method emits its struct return through raw byte stores:

```csharp
Cysharp.Threading.Tasks.UniTask<bool> __ret = default;
((byte*)&__ret + 0x0)[0] = uniTask1;
((short*)((byte*)&__ret + 0xa))[0] = this.token;
return __ret;
```

which looked like CS0029 ("cannot convert `UniTask<bool>` to `byte`"). A minimal
repro with a plain struct DOES fail that way, but the real tree does not: the
whole `UniTask` image (301 files) compiles with **8 errors, all CS8701**, and the
whole unitask tree with 19 (18 CS8701 + 1 CS0644). Measured twice, so the
measurement is not skipping files — the address-of local of a *generic* struct
is evidently not a `byte` lvalue in the same way.

So the family stays a **fidelity** issue (the return value is written field-wise
instead of being constructed), not a compilability one, and the earlier
suspicion that the whole-tree compile silently skips files was wrong. Worth
recording because it is exactly the kind of plausible-looking deduction that
would have sent the next session chasing a non-existent compiler error.

## Previous: fix 200 — narrow loads slice the struct field (2026-11-03, on `main`)

The `float.IsNaN(this.targetScale)` finding from the masked-compile note is
fixed at its root. `_aggregate_load` returned None as soon as a load's offset
was ANY field offset, so `movss xmm0,[rbx+30h]` — a 4-byte read of a `Vector3`
field — fell through to the whole-field render and the compare's operand became
the struct (2,823 `float.IsNaN(...)` sites tree-wide; every one whose operand is
a struct field was type-wrong).

The narrow case now slices through metadata: when the field at that offset is a
closed valuetype and the load is strictly narrower than it, `_fragment` returns
`<field>.<first component>`, proved by the field chain at that exact width. A
whole-field load and a non-valuetype keep today's spelling.

```csharp
if (float.IsNaN(this.targetScale.x))   // was: float.IsNaN(this.targetScale)
```

Portable 1,656 passed; the five pinned bodies are unchanged.

`compile_corpus` also learned to flag a **masked** binding count
(`binding_masked`): a CS1xxx syntax error makes csc skip every binding
diagnostic, which is why the complete survivors tree could read "4 errors"
while almost certainly holding many more.

## Previous: fix 199 — the last CS1519 family on the survivors tree (2026-11-03, on `main`)

The complete survivors tree had four CS1519 errors in one file, and they came
from one display-class field:

```csharp
public UnityEngine.InputSystem.Layouts.InputDeviceMatche3____4__this; // 0x38
```

IL2CPP spells a closure field that refers to *another* closure field
`<>3__<>4__this` — 302 such fields here (298 `<>4__this`, 4
`<>3__<>4__this`). fix 195's bracket walk extends BACK over the identifier's
own characters for the "empty angle pair inside an identifier" case
(`CS$<>8__locals2`), then deletes that many characters from the output. After
the first `<>3__` candidate the output tail is the *mangled* text, which is
shorter than the raw span, so the deletion took the space, the type's last
character and two underscores with it.

The walk now records `chunk_end` (the text index just past the last whole
chunk it appended) and refuses to extend back across it, so a deletion always
covers raw characters that are really in the output. Verified on both affected
images:

```csharp
public UnityEngine.InputSystem.Layouts.InputDeviceMatcher __3____4__this; // 0x38
public UnityEngine.InputForUI.KeyEvent.ButtonsState __3____4__this; // 0x44
```

The standing regressions hold: a shift (`(a & b) << c >> 32`) is untouched, a
deep-nested generic name is mangled whole, and the `CS_<>9__0_0` closure case
still mangles. Portable 1,656 passed (one new test), game pins 5 passed.

A side effect worth recording: while patching this I discovered the earlier
fix-195 splice had left **two copies** of `mangle_generated_names` in
`il2cpp/text.py` (Python used the stale last one, which is why the fix
appeared not to apply on the first three attempts). The file was restored from
HEAD and patched once, precisely; `text.py` now has exactly one definition.

### The survivors "4 compile errors" was a MASKED number

`compile_corpus` on the complete survivors tree reported **4 errors, all
CS1519** — and that headline is not trustworthy: csc reports at most the
syntax tier when a syntax error exists, so all *binding* diagnostics for that
compilation were suppressed. The tree's real binding state is unknown until the
CS1519 family (fixed by fix 199) is gone from a full rebuild.

Two families are already visible as likely binding errors, both in code the
masked run could not reach:

* `float.IsNaN(this.targetScale)` — a **Vector3** passed to `float.IsNaN`
  at `RGame/ScriptableCoreKit/SetScaleStateNode.cs`. 2,823 `float.IsNaN`
  sites exist tree-wide; most take floats, but the source here is
  `targetScale.x == 0f || targetScale.y == 0f || targetScale.z == 0f`, so the
  reconstruction is wrong twice: the argument is the whole struct and the
  predicate is a NaN test instead of a zero test. The `IsNaN` text comes from
  `x64.flag_cond`'s parity-jump fold, where the flags operand rendered as the
  containing struct instead of its float component — the same class of
  text/type inconsistency the `(float2)` family shows.
* the same method also shows the shaping artifact: labels emitted *inside* if
  bodies (`L_1803d5ad5:` followed by more code) and nine ifs + four gotos for
  a one-line source condition.

So the next measurement is not just "how many errors" but "which of them are
one family": both symptoms point at the struct-valued float comparison.

## Previous: the complete survivors tree measured — 4 compile errors over 4,413 sources (2026-11-03, on `main`)

The full 75-image rebuild with fixes 195/196/197 (`out/survivors-roguelike-kit/
full_s3`, 7,523 type files / 80,091 bodies) is the first *complete* survivors
tree measured end to end:

| gate | result |
|---|---|
| brace | 7,448 files, **0 unbalanced** |
| tree-sitter, per image | 7,448 files, **0 bad / 0 ERROR / 0 MISSING / 0 recovery** |
| whole-tree Roslyn (4,413 sources, 6 BCL refs from the exact closure) | **4 errors in 1 file** (CS1519 x4) |

Getting the parse number required the crash-safe gate: two images
(`Unity.InputSystem` 343 files, `UnityEngine.InputForUIModule` 20 files) kill
the single-process parser outright, and both are **0/0/0/0** when parsed in
batches. Before fixes 195/196 the same tree had 4 unparseable files (60 ERROR
+ 8 MISSING); those are gone.

The four remaining errors are one defect shape, seen at
`Unity.InputSystem/.../Layouts/InputDeviceMatcher.cs:963`:

```csharp
public UnityEngine.InputSystem.Layouts.InputDeviceMatche3____4__this; // 0x38
```

A display-class field `<>4__this` whose type and name were mangled **into one
identifier** (the `.`/separator is gone and the type name lost its tail), so
the line has no type at all. It is a mangling interaction, not a parse problem
(tree-sitter accepts it), and it is the next fix.

The old AC-only number (63 binding errors) was an artifact: 61 of them are
CS0234 for namespaces owned by sibling images. Compiling the tree as one unit
is the number to quote, exactly as for unitask (19 errors there, two artifact
families).

## Previous: the `(float2)` literal family — 830 sites of undeclared type (2026-11-03, on `main`)

The lifter spells a two-component float value `(float2)(a, b)` (and
`float3`/`float4`/`doubleN`), but **no such type is ever emitted**, so every
one of those sites is CS0246. Verified by compiling the shape in isolation
against the survivors closure:

```
probe_f2.cs(6,14): error CS0246: the type or namespace name 'float2' could not be found
```

Census (tree text, both fixtures): **830 sites** in the survivors tree
(`Unity.Mathematics` 242, `UIElementsModule` 180, `TextMeshPro` 74, `UI` 66,
`Assembly-CSharp` 48, `DOTween` 46, ...) and **358** in the unitask tree — the
largest undeclared-name family found so far, and it is *not* fixture-shaped:
the spelling comes from the SIMD/aggregate paths and appears in every image.

The two ways out, with the trade-off already worked out:

* **emit the type** — a `float2/float3/float4` (and `doubleN`) struct in the
  scaffolding. To make the *cast* form legal it needs a user-defined
  conversion from `ValueTuple<float,float>` (`(float2)(a, b)` parses as a cast
  of a tuple literal), plus conversions to `Vector2`/`Vector3`/`Color` for the
  assignments to type-check. That is a scaffolding with real semantics and it
  fabricates a type the source never had.
* **spell the real type** — the aggregate path already knows the *expected*
  type (`_piece_value`'s `expected`, and `_color_text` does exactly this for
  `UnityEngine.Color`), so a two-float value whose expected type is `Vector2`
  should render `new Vector2(a, b)`. This is the source's own spelling and
  needs no new type; the work is threading `expected` through the remaining
  call sites and declining when it is unknown.

The second is the right one; the first is the fallback for a site whose
expected type is genuinely unknown (then the value is not recoverable anyway
and the honest marker is better than a fabricated struct).

**fix 198 (done)** — the producer that PROVES the type (alues.py: a SIMD
slot whose struct is exactly Unity.Mathematics.float2 with two float fields)
now emits the fully qualified Unity.Mathematics.float2(a, b); the using-strip
shortens a dotted chain again when the file imports the namespace, so nothing
is lost where it resolved before. The const-pool pair path (insn.py, no type
proof) keeps the house spelling and is the remaining half of the family.

## Previous: the survivors fixture's defect map (2026-11-03, on `main`)

Source-vs-tree on the complete survivors tree (`full_s1`, 810 matched methods,
call_f1 0.667 / member_f1 0.361 / shape 0.584) has 52 of its 200 worst rows
carrying no honesty marker. Most are the same inlining story as unitask
(`Mathf.Clamp`/`Lerp` and `List<T>.Add` expanded in place), but one small
method exposed two real defects at once, and both are families:

`TMP_UiFrameRateCounter.Set_FrameCounter_Position` (a 33-line `switch`):

```csharp
// source
switch (anchor_position) {
    case FpsCounterAnchorPositions.BottomLeft:
        m_frameCounter_transform.pivot = new Vector2(0, 0);
        ...
}
// emitted before fix 197
else if (anchor_position - 1 - 1 == FpsCounterAnchorPositions.TopLeft) { ... }
num1 = 1008981770;
rectTransform1.anchorMin = num1;
```

* **fix 197** (`_enum_shift_fold`) — MSVC's switch dispatch shifts the index
  before comparing, so 892 sites tree-wide read `expr - N == Enum.Member`.
  `enum - int` is CS0019 and the shape also hides the flat `==` chain from
  `_switch_synth`. The fold is exact algebra through `il.enum_members`
  (`x - N == E.M` ⇔ `x == E.<member with value(M) + N>`), declining on an
  unknown/ambiguous enum or a value with no member.
* **open** — a struct constant is printed as a raw integer bit pattern
  (`num1 = 1008981770;` is 0.01f, assigned to a `Vector2` property), so the
  `new Vector2(a, b)` construction is lost. 15 such temps in Assembly-CSharp
  alone; the aggregate/struct-tile pass declines this shape. This is the
  next fidelity target, and it is also a compilability one (int -> Vector2).

### Next fidelity target: a struct constant printed as an integer bit pattern

`TMP_FrameRateCounter.Set_FrameCounter_Position` shows the shape and its
native evidence. The source writes `new Vector2(1, 0)`; the native code writes
`mov qword [rbp+10h], 3F800000h` -- ONE 8-byte store whose low dword is the
float 1.0f and whose high dword is 0 -- and the lifter prints

```csharp
s_10 = 1065353216;          // mov qword [rbp+10h],3F800000h
t2.pivot = s_10;            // Vector2 property
```

so the `new Vector2(1, 0)` construction is lost (15 such temps in
Assembly-CSharp alone; it is also a compilability defect, int -> Vector2).
The neighbouring `movdqa [rbp-10h],xmm0` path already renders
`(float2)(1.0f, 1.0f)` correctly, and a split pair renders
`s_10.x = 1.0f;` for the first half, so only the *single wide immediate*
store misses.

The obstacle is that the store's width and the slot's pointee type are what
decide the render, and the consumer (`pivot = s_10`, a Vector2) is what proves
it: a text-level rewrite would need the member type, and the lifter does not
know the slot type at the store. The two candidate hooks are the immediate
store path in `insn.py` (render `(float2)(f, 0.0f)` for a width-8 store whose
high dword is zero and whose low dword is a finite float) and the aggregate
pass (`aggregates.py`) composing the pair the way it already does for two
4-byte stores. Neither is done yet; the shape is recorded here with the
disassembly so the next session does not have to rediscover it.

### Measurement note: a single-image compile of Assembly-CSharp is not a metric

`gate.py compile` on one image compiles that image alone, so every namespace
its siblings own is unresolved. On the survivors tree, the 63 binding errors
from `Assembly-CSharp` alone are **61 CS0234** of the form "the type or
namespace name `CommonStat` does not exist in the namespace `RGame`" — i.e.
`RGame.CommonStat`, `RGame.Framework`, `RGame.ScriptableCoreKit` come from
*other* images of the same build (they are not missing from the tree; the file
`RGame/RoguelikeKit/BaseBulletShootState.cs` compiles fine once its siblings
are in the compilation). The same effect produced the `__SharedBodyStubs`
CS0246 when a *subdirectory* was compiled alone.

So for these fixtures the number to quote is the **whole-tree compile**
(`compile_corpus.py` with the fixture's exact managed closure for the BCL),
exactly as unitask is measured: the per-image gate answers "does this image
name things its own assembly owns", not "is the recovered code correct".

## Previous: fixes 195/196 — deep-nested generated names and escaped char literals (2026-11-03, on `main`)

Both came out of parse-gating the **complete survivors tree**, which had never
been gated as a tree: the aggregate tree-sitter gate *segfaults* on it (exit
`0xC0000005`, nothing written) although every file parses fine in isolation,
so the gate is now run image by image (7,188 files clean) and the one image it
crashed on (`Unity.Localization`, 260 files) was parsed in batches of 25 with
a fresh parser. That exposed **4 unparseable files, 60 ERROR nodes and 8
MISSING ones** — and both causes are general, not fixture-shaped.

**fix 195** — IL2CPP names a state machine after its whole interface, so a
generated identifier can carry generic arguments nested several levels deep:

```csharp
private sealed partial class <System_Collections_Generic_IEnumerable<
    System_Collections_Generic_KeyValuePair<System_String,
    UnityEngine.Localization...>>__>d__57
```

`MANGLED_IDENT_RX` cannot see more than one level of nesting, so the name
reached four files verbatim. `mangle_generated_names` now **walks** the
brackets instead of matching them: a `<` at an identifier start opens a
candidate, it survives only while every character is a name character
(letters, digits, `_`, `.`, backtick, `[`, `]`, `|`, `,`, space) and the
brackets balance, and `mangle_generated_ident` still applies its two positive
proofs. Two supporting rules: the mangler turns `,`/`[`/`]`/space into `_`
(a mangled `Foo_A, B_` is not an identifier), and an EMPTY angle pair inside
an identifier (`CS$<>8__locals2` → `CS_<>8__locals2` after the `$` sanitize)
mangles from the identifier start. The standing regression still holds: a
shift (`(section & v) << section >> 32`) is untouched, because `&`/`(` end a
candidate immediately.

**fix 196** — a `const char` whose value is a backslash or a quote emitted the
raw character (`internal const char m_CharLiteralEscapeChar = '\';`). Both are
`isprintable()`, so the printable path fired; they are escaped now.

Result: `Unity.Localization` 4 bad files / 60 ERROR / 8 MISSING → **260 files,
0/0/0**. The rebuilt complete unitask tree (`full_u7`) is unchanged:
brace 0, parse 0/0/0/0 over 3,547 files, whole-tree compile 19 errors (the two
known artifacts). Portable 1,650 passed, game pins 5 passed.

## Previous: unitask source-vs-tree diff fully triaged (2026-11-03, on `main`)

`tools/source_compare.py` now splits the unmatched population by side and
records samples (`unmatched_samples`), which makes the whole diff classifiable
instead of a single "mismatch" number. For the complete unitask tree
(`out/unitask/full_u5`, 49 images) every category is accounted for:

| category | count | verdict |
|---|---|---|
| `stub` | 2,283 | generic-DEFINITION methods with no native code: `AsyncLazy<T>`'s rows are all `addr=0` (verified), so the honest `NotImplementedException` stub is correct, not a defect |
| `transformed` | 544 | async/iterator/`[Conditional]`/lambda source methods — the compiler rewrote them, no 1:1 body exists |
| `type` | 121 | source types absent from the PLAYER build: `Editor/` scripts, `External/` packages, unused generic definitions, stripped rows |
| `inlined` | 55 | IL2CPP inlined the async implementation into the sync wrapper; the outer body IS a compiler rewrite |
| `empty_src` / `empty_srcout` | 28 / 32 | `[Conditional("UNITY_EDITOR")]` bodies compiled out in the player (`TaskTracker.TrackActiveTask`, `RemoveTracking`) and pairing noise |
| `empty_out` | 4 | all four are `#if`-guarded or sample-scene code (`BindTo` under `#if !UNITY_2019_1_OR_NEWER`, `SandboxMain.Awake`) |
| `method` | 13 | `PlayerLoopHelper.InitOnEditor` and friends: editor-only (`#if UNITY_EDITOR`) or overload-plus-generic-arity spellings |

The per-method `worst` list is dominated by the same inlining: `Bounds.Equals`
expanded into twelve `IsNaN` comparisons, `TrySetResult` inlined into promise
`MoveNext`, `ThrowArgumentNullException` inlined into its `..Core` call. Those
are what the native code does; the source spelling cannot be recovered without
un-inlining, which would be a guess.

So on this fixture the *matched* population has no unexplained remaining
defect, and the tree's own gates are clean: brace **0** unbalanced over 3,547
files, tree-sitter **0/0/0/0**, whole-tree Roslyn **19 errors** (18 CS8701
target-framework default-interface-method artifact + 1 CS0644
`Il2CppFullySharedGenericType : ValueType`, which C# forbids for user types).

## Previous: fix 194 — real throw arms survive the non-returning prune (2026-11-03, on `main`)

The first defect the source comparison actually convicted (see the triage note
further down) is fixed. `_prune_nonreturning` keeps only paths that reach
`ret`/`stop`, and a managed `throw` compiles to `call raise_helper; int3`, so
its block ends in `abort` and the whole arm was dropped: the awaiter's
`if (continuationAction != null) throw new InvalidOperationException(...)`
rendered as an empty `if { }`, and `GetResult` lost
`if (result.IsError()) throw new UnityWebRequestException(result);`.

The lifter was innocent — it renders both arms correctly, with the message
string and the exception type. The predicate that separates a real throw from
the guard noise the pruning exists to remove is a property of the **call
target**: exactly one metadata candidate, and its declaring type outside
`System.*`. The `System.*` exclusion is load-bearing, not cosmetic — keeping
`System.ThrowHelper.ThrowArgumentOutOfRange_IndexException` restructured
`RpgInventoryManager.AddItem` (190 -> 217 lines) and dropped the event sugar,
which the pinned body test caught immediately.

The prune runs before `_analyze`, so the seed is decided from the
instructions, not from statements (an earlier attempt keyed on
`b.stmts`/`b.ret` was vacuous — every block is empty at that point — and was
measured as a no-op before being replaced).

Verified: the awaiter emits
`Error.ThrowInvalidOperationExceptionCore("continuation is already registered.");`,
`AddItem` is back to its pinned shape, game pins 5 passed, portable 1,650
passed (4 new tests).

### Open lead: constructed-exception (`throw new T(...)`) arms

fix 194 restores arms that call a *managed* throw helper. The other real family
is `throw new Ex<T>(...)`, which compiles as an allocation plus the runtime
raiser, and it is **not** restored:

```csharp
// source
if (result.IsError()) { throw new UnityWebRequestException(result); }
// emitted
(no arm)
```

Two extensions were tried and measured, both reverted:

1. keep any `abort` arm with >= 2 calls — restored
   `UnityWebRequestAsyncOperationAwaiter.GetResult` but took mscorlib's
   `ManifestBasedResourceGroveler` from 0 to 1 unparseable file (a bare
   comparison statement and a `throw;` with code after it, inside a `finally`);
2. allow any `.ctor` call in the arm (the measured shape there is
   `object_new, il2cpp_object_new, UnityWebRequestException..ctor, object_new,
   raise`) — same mscorlib break, and excluding pad blocks *and* pad-reached
   blocks did not stop it.

The reason is visible in the broken text: those discarded arms render as a
bare `throw;` from the **rethrow** helper, which is legal only inside a
`catch`, so keeping the arm also keeps the code after it and the pad's own
condition leaks out as a statement. The distinction needed is *rethrow vs
raise*, and the prune cannot see it — it runs before the lifter renders the
block (statements are empty at that point; that is also why the first
`b.stmts`-keyed attempt was a measured no-op).

Next avenue: decide *after* the lift — mark blocks the lifter rendered with a
`throw new <T>(...)` statement (or a named raise) and re-run the
reachability/purning on that classification, rather than predicating on the
call targets before rendering.

## Previous: full-corpus testing on the two lightweight fixtures (2026-11-02, on `main`)

Per the user's call, the primary corpus is now the two MIT-licensed fixtures
built into complete player trees — **all** their images, not the game images
alone — and the licensed fixture is evidence only. That also unlocks the
strongest reference closure available: each fixture ships its own
`*_BackUpThisFolder_ButDontShipItWithYourGame/Managed/` folder, i.e. the exact
assemblies its player build was compiled from.

`tools/compile_corpus.py` gained the model this needs: images left out of the
*only* BCL images stay in the closure (`source_excluded`), because a tree that
emits every image would otherwise filter its whole closure away and have no
corlib.

### unitask (49 images, 3,596 type files, 23,756 bodies)

| gate | result |
|---|---|
| brace | 3,547 files, **0 unbalanced** |
| tree-sitter | 3,547 files, **0 bad / 0 ERROR / 0 MISSING / 0 recovery** |
| whole-tree Roslyn (2,220 sources, exact closure) | **19 errors in 6 files** |

The path there was 41 -> 76 -> 27 -> **19**, and both fixes are general:

* **fix 192** (CS8051 ×25) — `auto_property_maps` accepted any property whose
  type has an `<X>k__BackingField` field, so a SET-ONLY property emitted
  `public bool X { set; }`, which C# rejects (auto-implementation needs a
  getter), and lifting the setter body instead produced `this.X = value` —
  infinite recursion, because the storage respell had already turned the field
  into the property name. A set-only property was written with an explicit body
  over a plain field: the maps now require a getter, the field keeps
  `__field_X`, and the setter writes it
  (`IgnoreAttribute.DoesNotContributeToSize`).
* **fix 193** (CS0146 ×5 + the CS0311 ×52 that cascaded off it) — the
  using-strip shortened `UnityEngine.UIElements.UxmlTraits` to `UxmlTraits`
  because exactly one visible typedef answered to that head, but inside
  `class VisualElement` — which declares its own nested `UxmlTraits` — the
  short name resolves to the nested type, so the base clause printed
  `class UxmlTraits : UxmlTraits`. `collision_heads` now keeps the prefix for
  a head the FILE declares (its own type and its nested types, both the
  metadata arity spelling and the emitted short one:
  `UxmlObjectTraits`1` / `UxmlObjectTraits`).

The 19 survivors are **artifacts, not decompiler defects**: CS8701 ×18 is
"default interface implementation unsupported" (the exact closure targets
netstandard2.0 while the original player profile supports DIM), and CS0644 ×1
is `Il2CppFullySharedGenericType : ValueType`, which C# forbids for any user
type but IL2CPP's own metadata declares.

### survivors-roguelike-kit (75 images, 11,570 types, 94,205 methods)

Full build in flight at the end of the round (`out/survivors-roguelike-kit/
full_s1`); its gates and whole-tree compile follow the same recipe.


### Source-comparison triage of the full unitask tree (2026-11-02)

`tools/source_compare.py` against `out/unitask/full_u4` (1,327 matched methods,
call_f1 0.618, member_f1 0.326, shape_cos 0.792) says the *worst* list is
dominated by things that are **faithful, not defective**: IL2CPP inlined
`Bounds.Equals` into twelve `IsNaN` comparisons, inlined `TrySetResult` into the
promise `MoveNext` bodies, inlined `ThrowArgumentNullException` into a
`...Core` call. Those are what the native code does.

Only 14 of the 200 worst rows carry **no tell at all** (no `sub_`, no
`obj_temp`, no `byte_ptr`), i.e. shapes that differ without an honesty marker.
Nine of them are the same real defect:

* `AssetBundleRequestAllAssetsAwaiter.UnsafeOnCompleted` (and its web-request
  twin) — the source is
  `if (continuationAction != null) throw new InvalidOperationException(...)`;
  the emitted body is an **empty `if { }`** whose condition is garbage
  (`((byte*)typeof(PooledDelegate<AsyncOperation>) + 0xe0)[0] ==
  this.continuationAction`), and `GetResult` loses its whole
  `if (result.IsError()) throw new UnityWebRequestException(result);` arm.

Instrumenting `_prune_nonreturning` on that method shows the pruned targets are
**empty abort blocks with no predecessors**, so the pruning is not what drops
the throw: the raise call never reaches a block at all, and the surviving
branch keeps a condition whose right-hand side is a klass slot. So this is a
*lift-side* gap (a noreturn raise call / cast-class-throw shape), not the
pruning trade-off. An experimental prune change that seeded reachability with
non-empty abort blocks was measured and reverted: it does not affect this
method and risks reintroducing the null-check-stub noise the pruning exists to
remove.

Next: take the `throw`-helper shape apart at lift time
(`_eh_helper_returns` / `rt_noreturn` / the cast-class throw at
`insn.py:1647`) on that awaiter's method, with the fixture source as ground
truth.

## Previous: two whole-tree models (2026-11-02, on `main`)

 — IL2CPP's glued tuple spelling in explicit qualifiers (2026-11-02, on `main`)
### Known whole-tree artifact: per-assembly anonymous types

Two assemblies each declare their own compiler-generated `<>f__AnonymousType0`
with *different* generic parameters (`_presenceToken_j__TPar` vs
`_product_j__TPar, _metadata_j__TPar` on the game tree)). Per-assembly output is
correct and self-consistent; compiling 90+ assemblies as ONE unit sees two types
with the same emitted name, which surfaces as CS0102 (duplicate) or CS0246 on
the other file's type-parameter spellings. Unlike the byte-identical
scaffolding this cannot be deduped -- the declarations differ -- so it counts as
an artifact of the whole-tree model, not a defect. Same class: `__c` /
`__c__DisplayClassN` collisions between images whose closures happen to share a
name.

### Known minor regression to revisit (2026-11-02)

Diffing the survivors tree before and after fixes 181-191 shows **exactly one
changed file** and no compile-count change, but that file lost a loop counter's
integer type: `int num31 = 0;` became `object obj216 = 0;`
(`VertexShakeB.<AnimateVertexColors>d__10.MoveNext`, 879-line body). Four such
counters flip tree-wide (object-zero declarations 75 -> 79, int-zero 108 ->
104). The temp is integer-only (`>=`, `* 5`, `+= 1`), so `_numeric_obj_retype`
should retype it and declines; its body is far below the 4,000-line guard, so
the guard is not the cause. The rename happens *before* that pass, and the
counter carries an `obj` name already -- i.e. the tracked type was gone at
`_rename_locals` time. Most likely `_order_copies`' rewrite changes which phi
spill owns the value. Worth a targeted look, but it is a *type quality* cost of
4 temps, not a correctness or compilability change.

## Previous: fix 191 — IL2CPP's glued tuple spelling in explicit qualifiers (2026-11-02, on `main`)

IL2CPP names an explicit implementation of a tuple-typed interface with each
element's TYPE and NAME concatenated, so the `_GetConsumedStock_d__77` iterator
declared

```csharp
System.ValueTuple<int, int, int>
System.Collections.Generic.IEnumerator<(System.Int32shopId, System.Int32itemId, System.Int32remaining)>.Current
```

which is not C#: `Int32shopId` is a type and an element name in one token, and
the element names disagree with the interface's own spelling anyway. The
qualifier is repaired by taking each element's longest known type-name prefix
and dropping the name:

```csharp
... System.Collections.Generic.IEnumerator<(int, int, int)>.Current
```

The same tuple type, and no name agreement is needed. Two supporting pieces:
`_iface_qualifier` counts parenthesis depth when it computes a qualifier's
top-level argument count (a tuple argument is ONE argument), and when the
type's own interface list does resolve the qualifier, that spelling —
rendered by `type_name` — is preferred over the metadata string. The repair
runs in both the method and the property path (this case is a property).

Portable suite 1,639 passed; the pinned game bodies are unchanged.

### Note on this round's build

The full rebuild started in round 13 was killed by an interrupted tool call and
left six orphaned pool workers holding a partial `out/limbus/full1`. They are
gone and the build is restarted **without `--only`**, so it produces the
complete 162-image tree: 2,970 type-tasks, 299,371 of 319,100 methods with
native code. Expect ~3-4 h.

## Previous: fix 190 — explicit interface properties are properties (2026-11-02, on `main`)

IL stores a property accessor as a plain method, and an explicit interface
implementation keeps its fully dotted metadata name, so the render was

```csharp
bool TMPro.IRubyText.get_enableAutoSizing()
{
    return this.m_enableAutoSizing;
}
```

which cannot implement a property accessor (**CS0683, 22 sites** in the game
tree). The type emitter now groups an accessor pair back into the property it
implements:

```csharp
bool TMPro.IRubyText.enableAutoSizing
{
    get
    {
        return this.m_enableAutoSizing;
    }
}
```

`emit_property` gained a `force_name` path, because a synthesized property has
no row to read: the accessors are plain methods on *this* type and the property
row lives on the interface. Only a pair whose qualifier is the method's own
dotted path — or one uniquely proved by `_explicit_impl_qualifier` — is
grouped; a lone accessor renders as a property with that single accessor.

Verified: `CustomRubyTextMeshProUGUI`'s three `IRubyText` properties become
properties; the pinned game bodies and the decl gate are unchanged. Portable
suite 1,639 passed.

### Artifacts found while triaging the rest (documented, not fixed)

* **CS0535 `ArrayBufferWriter<T>.GetSpan(int)`** — the metadata for that type
  lists 9 methods and no `GetSpan` at all (every one of them has address 0 and
  renders as a `NotImplementedException` stub). The interface member is
  stripped from the game's own metadata, so no render can implement it.
* **CS0122 99** — `TMP_FontAsset` uses TextCore's `internal`
  `LigatureSubstitutionRecord`/`MarkToBaseAdjustmentRecord`. The real Unity
  package compiles because TextCore ships `[InternalsVisibleTo]` to the TMP
  assembly; a whole-tree compile against the editor's reference dlls cannot
  see that. Cross-assembly inlining artifact, not a decompiler defect.
* **CS0104 15** — `Vector2` is ambiguous between `UnityEngine.Vector2` (game
  metadata) and `System.Numerics.Vector2` (reference closure). The
  using-strip's collision detector works from game metadata only, so it cannot
  see the closure's name.

## Previous: fix 189 — two text defects, generated-type visibility, scaffolding dedupe (2026-11-02, on `main`)

Found by reading the remaining 393 errors apart:

* **`global::` mangling** — `mangle_generated_ident` turned the explicit
  interface spelling
  `byte global::System.Collections.Generic.IEnumerable<byte>.GetEnumerator()`
  into `global__System...` (5 sites, CS0246), because the text matched the
  generated-name heuristic. A name containing `::` is never generated.
* **Generated nested type visibility** — a closure or state machine nested in
  its owner was emitted `private` from its flags, while the local functions and
  inlined bodies that mention it are `internal`, so 33 signatures were CS0051
  (`JsonDocument._CreateForLiteral_g__Create_73_0(byte[], ref
  JsonDocument.__c__DisplayClass73_0 _)`). Generated nested types are `internal`
  now: still implementation detail, and no signature exposes something less
  accessible.
* **Scaffolding dedupe** grows `IsUnmanagedAttribute`, `IsExternalInit`,
  `ScopedRefAttribute`, `CompilerFeatureRequiredAttribute` (-20 artifact
  CS0111).
* Six more referenced images built (`System.Text.Encodings.Web`,
  `Unity.InternalAPIEngineBridge.001`, `Unity.Services.Core`,
  `Unity.2D.Common.Runtime`, `Unity.ProBuilder*`).

A full rebuild (`out/limbus/full1`) is in flight to carry all of it plus fixes
186-188 into the measured tree; the previous measurement stands at 393 errors
with 0 syntax errors, and the families above account for ~58 of them.

## Previous: 393 whole-tree errors, zero syntax errors (2026-11-02, on `main`)


Seventeen images the game references but the tree never emitted were built
(`UnityEngine.Purchasing` and its five siblings, `Unity.ResourceManager`,
`Unity.Addressables`, `Unity.RenderPipelines.Universal.ShaderLibrary`,
`Unity.Services.Core.Internal`, `Firebase.Platform`, the two 2D runtimes, ...),
taking the tree to 93 images / 35,149 files:

| gate | result |
|---|---|
| tree-sitter parse (one process) | 35,149 files, **0 bad / 0 ERROR / 0 MISSING / 0 recovery** |
| brace audit | 35,149 files, **0 unbalanced** |
| Roslyn whole-tree compile (29,764 sources) | **0 syntax errors, 393 semantic errors in 137 files** |

Families: CS0122 99, CS0246 69, CS0051 33, CS0234 22, CS0683 22, CS0111 20,
CS0104 15, CS0535 15, CS0538 15, CS0738 15, CS0100 11, CS0460 10. Two rounds
ago this compile read 4,082 — and that number was meaningless, because Roslyn
skips declaration and binding diagnostics whenever the compilation has a
syntax error.

* **fix 188** — `_UNKNOWN_MEMBER_RX` consumed only `unknown.Member`, so a chain
  or a call's argument list was left behind (`unknown.GetEnumerator(0)` →
  `/*unknown*/ default(0)`, `unknown.AddComponent(a, new P<T>())` →
  `/*unknown*/ default(a, ...)`). Those were the tree's last two syntax-error
  files. The pattern spans the whole chain with one nesting level of
  arguments, and a chain that is an entire statement renders
  `/*unknown call*/;`.
* **harness** — `compile_corpus`'s scratch dir moved beside the report after a
  temp cleaner removed it between writing the merged stub file and invoking
  the compiler (`CS2001: source file not found __SharedBodyStubs.cs`, which
  reads like a decompiler failure and was not one); per-assembly compiler
  scaffolding (`PrivateImplementationDetails`, `EmbeddedAttribute`, the
  nullable/ref-safety attributes, the MonoScript types file) is deduped, which
  removed 484 artifact errors; and `tools/compile_full_tree.py` is the shipped
  whole-tree compile (closure-derived exclusions, so packages the editor does
  not ship stay sources).

Portable suite 1,639 passed. Full suite: 1,683 passed / 1 xpassed with two
disk-state failures -- the game tree's `Unity.Burst.Unsafe` directory was
**empty** (an artifact of the first, killed 161-image build), so the decl and
compile gate tests looked for types that were never emitted. Building that
image (5 files) closes both; that class of failure always means "look at the
tree, not the source".

**Next**: CS0122 99 (accessibility across images — a semantics decision, not a
text fix), CS0246 69 (the long tail of still-unbuilt images), CS0051 33
(inconsistent accessibility: a private type in a public signature),
CS0535/CS0538/CS0738 (interface implementation and explicit-interface shapes),
CS0683 (explicit implementation signature mismatch).

## Previous: fix 186/187 — the whole game tree with zero syntax errors (2026-11-02, on `main`)

`tools/compile_corpus.py` over the whole tree (29,366 sources; editor closure
of 260 refs; the 21 images the closure provides are excluded):

| | value |
|---|---|
| syntax errors | **0** |
| tree-sitter parse (whole tree, one process) | **34,590 files, 0 bad / 0 ERROR / 0 MISSING / 0 recovery** |
| brace audit | **34,590 files, 0 unbalanced** |
| semantic errors | **1,629** in 367 files |
| families | CS0246 821, CS0102 219 (cross-image duplicate helper types — a harness artifact), CS0234 187, CS0111 122, CS0122 96, CS0051 33, CS0683 22, CS0538 17, CS0104 15, CS0535 15 |

Getting there closed the last two syntax defects and, at last, emitted
`TMPro.TextMeshProUGUI` (2,435 references were failing on the missing type):

* **fix 186** — `mangle_generated_ident` declined every match without a double
  underscore, so `<PrivateImplementationDetails>` kept raw angle brackets
  (CS1001) in every image's `PrivateImplementationDetails.cs`. A generated name
  also never contains whitespace, which every false positive (a shift or a
  comparison inside brackets) does — that is the second positive proof now.
* **fix 187** — a parameter named `<p0>` (Roslyn's spelling) reached the
  signature as `void f(TMP_TextInfo <p0>)`. `safe_ident` must keep angle
  brackets for generic TYPE spellings, so a new `names.ident_name` strips them
  for identifiers and the emitter uses it for every parameter.
* **performance** — `TextMeshProUGUI.GenerateTextMesh` (116k statements) lifts in
  **147 s** now: `_rewrite_unknowns` returns early without a `?`, the
  hetero-assignment census uses a generic identifier + name-set check instead
  of an alternation over every renamed token, `drop_dead_cardmark_fragments`
  counts occurrences once behind a substring pre-filter, and `lift_method`
  skips the remaining cleanup passes above 20,000 statements (they are folds,
  not correctness requirements).

**Measurement lesson, recorded because it cost a wrong headline**: an earlier
run of this same compile reported "1 error". Roslyn skips declaration and
binding diagnostics entirely when the compilation has ANY syntax error, so two
unparseable files masked the whole 1,629-error backlog. Read the syntax count
first; a small total next to a syntax error means the compiler never checked
the rest.

**Next**: CS0246 821 is dominated by types from images this tree never emitted
(`Unity.Addressables`/`ResourceManagement`, `Unity.InputSystem`, `Uniject`,
`Unity.Localization`, ...) — build those images and the count should fall the
way TMP's did. CS0102/CS0111 341 are duplicate helper types across images, an
artifact of compiling 60 assemblies as one unit (the per-image gates do not see
them). CS0122 96 / CS0051 33 / CS0538 17 are real accessibility and explicit-
interface defects.

## Previous: fix 181 — the generated-name mangler no longer eats shift expressions (2026-11-02, on `main`)

The file boundary replaces the angle brackets of compiler-generated
identifiers (`<Foo>d__13`, `<>c`, `<>9__0_0`, a nested
`<IEnumerable<T>_GetEnumerator>d__21`) because no C# grammar accepts them.
`MANGLED_IDENT_RX`'s nested-bracket alternative accepted spaces, so a plain
shift expression matched it. The game tree's **only** `Assembly-CSharp` parse
error was

```csharp
ulong num1 = ... | (section & value) __ section __ 32 & 63;   // << section >> 32
```

— 45 sites in 5 files, all hand-optimized bit-twiddling code
(`BitVector64`, `Base64`, `RIPEMD160Managed`, `X86`, `IPv4AddressHelper`).
`mangle_generated_ident` now declines any match without a double underscore
(every Roslyn-generated name carries one: `d__`, `c__`, `9__`, `g__`, `b__`,
`f__`) and keeps the bare `<>`-prefixed closure family.

Measured: re-emitting the offending types gives `<< section >> 32 & 63`, the
game tree now has **0** dunder sites, `Assembly-CSharp/Server` parses 907
files / 0 errors, and two images that previously *segfaulted* the parse gate
(`System`, `Unity.Burst`) now parse clean. Portable suite **1,617 passed**
(4 new tests).

### Open defect found while gating (next fix candidate)

`mscorlib` still has one parse error, and it is a **statement spliced into a
ternary arm**, not a mangling artifact:

```csharp
// out/limbus/full0/mscorlib/System/Buffer.cs:195
((byte*)dstOffset + 0x20 + dst)[0] = num4 == dst ? srcOffset + 0x20 + num4; return : srcOffset + 0x20 + num4;
```

The true arm carries `; return`, i.e. some pass composed the arm from text that
included a following statement. Reproduce by lifting the `Buffer.BlockCopy`
overload at that site; the ternary builder to suspect is the one that composes
arms from multi-statement text (not `_ternary_pass`, which requires the exact
one-assignment-per-arm layout).

### Current work: the game's own Assembly-CSharp now parses 100% clean (2026-11-02, on `main`)

`tools/gate.py parse --tree out/limbus/full0/Assembly-CSharp`:
**24,739 files, 0 bad files, 0 ERROR, 0 MISSING, 0 recovery nodes** (98.9 s).
That is the licensed fixture's own code — 178,649 lifted bodies — with every
class of syntax defect the gates can see gone: the last two were fix 181's
mangled shift expression (45 sites in 5 files) and fix 182's statement
spliced into a ternary arm.

The rest of the tree: 58 of 60 emitted images parse clean (per-image reports
in `validation_reports/limbus/full0.parse.*.json`); `mscorlib` and
`UnityEngine.TextCoreTextEngineModule` still cannot be gated in one process
(see the harness limitation below) and mscorlib's `Hashtable.cs` / `Marshal.cs`
still carry real defects (above). Brace gate: 34,582 files, **0 unbalanced**.

### fix 182 — a two-statement ternary arm no longer splices (2026-11-02, on `main`)

`_ternary_pass` folds `if (c) { x = a; } else { x = b; }` into `x = c ? a : b;`.
An arm line can carry more than its own statement — a joined inline return
puts `X = v; return;` on one line — and folding that spliced the second
statement into the ternary:

```csharp
((byte*)dstOffset + 0x20 + dst)[0] = num4 == dst ? srcOffset + 0x20 + num4; return : srcOffset + 0x20 + num4;
```

That was the one unparseable line on the game tree's mscorlib
(`System/Buffer.cs`, `Buffer.BlockCopy`, VA 0x185C200D0). An arm whose RHS runs
past its own `;` now declines and both arms stay as `if`/`else` (valid C#).
Verified: the method re-lifts with the `if`/`else` intact and the re-emitted
`Buffer.cs` leaves the image's bad-file list. Portable suite **1,620 passed**
(3 new tests).

### Still open in mscorlib (next fix candidates)

The same census found two more syntax defects, both real:

* `System/Collections/Hashtable.cs` — 70 ERROR + 29 MISSING nodes; the first
  node's text is an `OnDeserialization(object sender)` signature, i.e. a
  cascade whose root is earlier in the file (both declarations in the emitted
  file do have bodies, so the break is inside one of their bodies).
* `System/Marshal.cs` — 2 errors whose node text is `?` (an unexpanded select
  or nullable mark).

### Harness limitation (documented, mitigated)

`tools/gate.py parse` parses a corpus in one process and **segfaults at
teardown** on the largest images (`mscorlib`, `UnityEngine.TextCoreTextEngineModule`):
the same files parse fine file-by-file and every subdirectory alone is clean,
so it is a native free/stack limit, not a verdict. The gate now (a) recreates
the `Parser` every 100 files and (b) caps the per-file detail list at 60 nodes
(`DETAIL_NODES`, with a `truncated` map) so a cascading recovery cannot blow up
the report. Parse the remaining two images by subdirectory until the teardown
crash is root-caused.

## Previous: fix 180 — an `object` local takes the type metadata already knows (2026-11-02, on `main`)

A virtual/interface call resolved *textually* after lifting leaves its temp
untyped, so the declaration printed `object` although the callee's return
type (or the member's own type) is metadata:

```csharp
object obj9 = battleUnitModel1.IsDead();     // IsDead() : bool
object obj2 = dateTime1.Hour;                // Hour     : int
```

`object` locals are the largest single population in the game tree —
**165,538** declarations in `Assembly-CSharp`, of which 45,258 come from a call
and 16,103 from a member access. `_rhs_ref_type` (dec/highlevel.py, inside the
declaration pass that already owns the scoped declaration map) recovers four
shapes, each with an exact proof:

* **calls** — `recv.Method(args)` / `Method(args)` on the declaring type by
  name + arity, with a generic return closed from the call's explicit type
  arguments (`GetComponent<Image>()` → `Image`);
* **members** — `recv.Member` / `this.Member` as a field's type or a property
  getter's return type. Property accessor rows store method indices **relative
  to the owning type's method range** (metadata v27+); reading them absolutely
  returned an unrelated method, which is how `DateTime.Hour` first looked like
  a pointer;
* **copies** — `object obj5 = source1;` takes a *reference* local's spelling
  (a value-type copy may be a box, so it declines);
* **allocations** — `new T(...)` when T is a proven reference type.

Decline-by-default: a receiver that is not a declared local or `this`, an
ambiguous name+arity, an open generic return without explicit call arguments,
and user struct/enum value types all keep `object`. `_td_by_suffix` (cached
per binary) resolves shortened declaration spellings, indexing both the
`List`1` and the `List` form.

Measured: survivors `Assembly-CSharp` object locals **1,446 → 1,340** (-7.3%),
binding errors unchanged at 2 (unrelated `ref`-vs-`out` CS0535); unitask
`Assembly-CSharp` **4,720 → 4,664**, binding 2,375 → 2,372; brace **0**,
tree-sitter **0/0/0/0** on both. Portable suite **1,613 passed** (19 new
tests). The game-wide effect is the point of the slice (~60k candidate
declarations) and needs a full game build to measure.

## Previous: game-wide measurement of fixes 173-179 (2026-11-02, on `main`)

A full 161-image build of the licensed fixture with every fix from this
session (`out/limbus/full0`, 24,738-file `Assembly-CSharp`) gives the first
game-wide numbers for the output-quality work, measured on the same corpus
the earlier censuses used (`f169`, built 2026-10-30 before these fixes):

| census (Assembly-CSharp) | `f169` | `full0` |
|---|---|---|
| `__field_` backing-field noise (fix 177) | 13,966 | **2,648** |
| bare `unknown` markers (fix 178) | 10,940 | **5,039** |
| `/*unknown*/ default` markers | 0 | **5,530** |
| auto-properties emitted `{ get; }` / `{ get; set; }` | 0 | **575 / 94** |

So fix 177 removes **81%** of the backing-field noise on the game and fix 178
makes **54%** of the unresolved-value markers compile (the rest are in
expression positions — `x * unknown`, `f(unknown, ...)`, `unknown ? a : b`,
comparisons — where a target-typed `default` would need a type the tree does
not carry; the largest of those, a ternary condition, is provably `bool` and
is the next safe slice).

**Why the whole-tree compile is the only honest game metric.** A
game-vs-engine compile of the pre-fix tree reported 17,131 errors for 14
images / 24,948 files, but 14,259 of them are CS0246 and there are **zero**
CS0103 — Roslyn never binds a body whose signature has an unresolved type, so
every body defect is invisible until the reference graph closes. `full0`
closes it for the *game* images (all 161 images are emitted, including the
Unity packages the editor does not ship), which is what makes the next
measurement meaningful; `tools/compile_corpus.py --exclude-dirs` (added this
round) is how the BCL/engine images are kept out of the diagnostic assembly
so those types come from the editor closure instead.

## Previous work: fix 179 — a bare `x = 0` under a struct/class declaration compiles (2026-11-02, on `main`)

IL2CPP renders stack-slot zeroing as `= 0` under whatever type the slot
carries. The *declaration* path already respells that (`_bare_rhs_needs_default`,
fix 97b: `UniTask.Awaiter awaiter1 = 0;` → `= default`), but a plain
**re-assignment of an already-declared local** was left alone — and
`awaiter1 = 0;` under a struct is the same CS0029. The shapes concentrate in
the async/iterator machinery: 227 CS0029 in unitask's `Assembly-CSharp`
alone, and 176 such `= 0` sites across the two MIT trees.

`_zero_assign_default` (dec/flow.py) is a final pass, run after the last
rename next to `_null_zero_rewrite` because it needs concrete declaration
spellings: a bare `name = 0;` whose declaration is visible in the body
becomes `= default;` when the declared type *provably* cannot convert from
the int literal (reference types and non-enum value types). `object` boxes,
numerics and enums convert, so all keep their faithful `= 0`;
generic/array/nullable/pointer spellings and doubly-declared locals decline.
Value-preserving: `default` is the zero every one of those types starts with.

Measured (unitask `Assembly-CSharp`, where the shape concentrates): binding
errors **2,447 → 2,375**, entirely CS0029 **227 → 155**, no other code
moving; the unitask library images and both survivors images unchanged;
brace **0**, tree-sitter **0/0/0/0**. Portable suite **1,591 passed** (9 new
tests).

## Previous work: fix 178 — the unresolved-value marker compiles without hiding itself (2026-11-02, on `main`)

An unresolved native value renders the bare text `unknown` (from
`_rewrite_unknowns`). It is honest and it parses, but it does not compile:
CS0103, **10,940** sites on the licensed game tree — the largest single
compiler-error family there, and the class is purely a rendering choice.

At the file boundary, where no type context is left to recover, the marker
moves into a comment and the expression becomes a target-typed `default`:
`x = unknown;` → `x = /*unknown*/ default;`. The site compiles and the text
still says the value was not recovered. Only shapes whose target type is
certain qualify:

* an assignment RHS (`x = unknown;`) — every recovered declaration spells its
  type, and neither fixture nor the game tree contains a single `var`;
* a `return` (`return unknown;`) — the signature's return type is declared;
* a member access on an unresolved value (`unknown.nFileSizeLow`) — the member
  name is fabricated, so the whole expression becomes the marker.

`unknown` inside a larger expression (`unknown + 1`, `f(unknown, 2)`, an
operand of `==`, `unknown[0]`) keeps today's text: `default` there would need
a type the tree does not have. The scan is literal-aware (NUL-masked lines),
so a string or comment that spells any of this is untouched, and it runs
*after* `_drop_dead_unknown_store` / `_strip_dangling_default`, which key on
the bare token.

Measured: projected onto the licensed `f169` tree (the transform is
file-boundary, so applying it to an existing tree is what a rebuild would
produce for those lines) **10,940 → 5,242** bare markers in 2,332 files, and
the projected tree still parses **0 bad / 0 ERROR / 0 MISSING / 0 recovery**
over 24,957 files. On the MIT fixtures (which carry few markers) the compile
gate moves: unitask AC 2,449 → **2,447**, TextMeshPro 269 → **267**,
survivors firstpass 914 → **900**, everything else unchanged; brace **0**,
tree-sitter **0/0/0/0**. Portable suite **1,582 passed** (7 new tests).

## Previous work: fix 177 — an auto-property reads as its property (2026-11-02, on `main`)

`<X>k__BackingField` is emitted by the C# compiler for an auto-property and
for nothing else. That made it a *compiler guarantee*, not a heuristic, and
fix 177 uses it three ways:

* **the property keeps its source shape.** `emit_property` takes the bodyless
  `{ get; }` / `{ get; set; }` path it already had for abstract members
  instead of lifting the trivial accessor (`return this.__field_X;`). This is
  also what makes the rest safe: lifting that body after the access respell
  below would have produced a self-call.
* **every access reads as the property.** `fields._storage_name` is the single
  choke point every field-name path goes through (instance and static chains,
  the static blob, the closed-generic layout), so a backing field now renders
  `o.X`. That is what the source wrote, and it is what binds across
  assemblies: the renamed `__field_X` storage has no counterpart anywhere,
  which is why `tween.active` (an *inlined* auto-property getter — `Tween.active`
  is auto) rendered `tween.__field_active` and could not resolve against the
  original `DOTween.dll`.
* **the two address-take sites respell back to the field.** A property has no
  address (CS0206), so oddly-named-but-legal `&o.__field_X` is required at
  those instructions: `lea r,[this+off]` (the byref receiver of a value-type
  instance call) and `add r,[obj+off]` (a GC write-barrier field address).
  `_field_expr` tags the member expression (`Expr._aprop`), and
  `_addr_field_text` respells. Real evidence for both halves: the LEA path
  was 511 sites in limbus `f169`, and the barrier path is the
  `((byte*)&token.__field_Value + 0x0)[0] = ...` family.

The (typedef, property name) ↔ field index map is a per-`Il2Cpp` lazy cache
(`csharp.auto_property_maps`), keyed by FieldDef identity and requiring the
property to live on the *same* typedef. Non-auto collisions keep today's
spelling: a real field named like a member still renders `__field_X`
(there is no property to point at), and an event field named like the event
stays renamed because events have no auto form.

Measured on the two MIT fixtures (`out/unitask/cw7`, `out/survivors-roguelike-kit/cw7s`):

| | unitask | survivors |
|---|---|---|
| `__field_` accesses | 151 → **101** | 650 → **232** |
| auto properties emitted | 28 | 39 |
| bodies lifted | 2,238 → 2,223 | 1,936 → 1,857 |
| binding errors, AC image | 2,458 → **2,449** | 2 → 2 (CS0535, unrelated) |
| binding errors, firstpass | — | 932 → **914** |

The drop in lifted bodies is the accessor bodies that are no longer lifted at
all (15 and 79). No `CS0206` anywhere, brace **0 unbalanced**, tree-sitter
**0/0/0/0** on both trees. `this.t.active` now resolves against the original
`DOTween.dll`; the CS1061s that remain in that image are `object` receivers
(the unresolved-value family), not backing fields. Portable suite **1,575
passed** (6 new tests), and the limbus game tests whose bodies touch these
shapes (`test_game_member_recovery`, `test_game_review80`,
`test_game_limbus_decompile`, `test_game_interlocked`) still pass unchanged —
the change is narrow because only compiler-generated `<X>k__BackingField`
rows qualify. The **full** suite (portable + every limbus game test) is
**1,621 passed / 1 xpassed** in 21.6 min, and a licensed-fixture build of
`Assembly-CSharp-firstpass` (51 types / 729 bodies) is 0 failed / 0
fallbacks with brace 0 and parse 0/0/0. The game-wide `__field_` population
(13,966 in `f169`) sits almost entirely in `Assembly-CSharp`, which was not
rebuilt this round (a full game body build is ~2.5 h here).

## Previous work: fix 176 — a whole-tree compile harness, and the next three families sized (2026-11-02, on `main`)

**176a — the corpus compile gate can take a real reference closure.**
`tools/compile_corpus.py` compiles a whole recovered tree as one diagnostic
assembly. It only ever referenced the local .NET SDK pack, so any tree that
does not re-emit mscorlib (`--only` builds) reported every engine name as
CS0246. It now takes the same three closures the per-image gate has
(`--managed-refs`, `--unity`, `--refs-dir`), auto-excludes the image dlls the
tree itself emits, and drops the SDK pack when a closure is supplied (mixing
Unity's mscorlib with .NET's leaves `System.Object` ambiguous: 40,427 CS0518).

Measured on the two MIT trees, whole tree as one unit:

| tree | files | closure refs | errors | by code |
|---|---|---|---|---|
| `out/survivors-roguelike-kit/cw3s` | 289 | 72 | **9** | CS0102 5, CS0535 2, CS0111 2 |
| `out/unitask/cw3` | 460 | 42 | **43** | CS0102 25, CS0111 10, CS8701 8 |

The CS0102/CS0111 blocks are the harness's own artefact:
`UnitySourceGeneratedAssemblyMonoScriptTypes_v1` is a *different* type that
every Unity-generated assembly legitimately declares, and one-assembly mode
cannot represent that. What remains after removing them is **2 CS0535**
(survivors: one `ref` that should be `out`, below) and **8 CS8701**
(unitask: default-interface-methods, which Unity's IL2CPP does support — the
reference `mscorlib` from the build's `Managed/` folder is what does not
advertise `RuntimeFeature.DefaultImplementationsOfInterfaces`). So the
recovered survivors game assembly is **two errors** from compiling as one
image, one of them a genuine recovery defect.

**176b — the merged shared-stub file was syntactically broken (fixed).**
`__SharedBodyStubs.cs` members are real methods with bodies now
(`internal static object sub_<va>(params object[] args) { throw ...; }`), but
the merge still collected *signature lines* only, producing an unparseable
temporary file — 91 CS1002 in a compile that should have measured bodies.
The merge now extracts whole member blocks (deduped by address) and the
compiler sees valid code. This was invisible while the gate had no reference
closure: without one, the first error was CS0518 and the stub file was never
reached.

**176c — the next three families, sized (not yet fixed).**
* **Backing-field noise, and it breaks cross-assembly references.**
  `csharp.source_field_name` renames a compiler auto-property backing field
  `<X>k__BackingField` to `__field_X` so the emitted field declaration cannot
  collide with the property `X` (CS0102), and every *access* prints
  `__field_X`. Limbus `f169`: **13,966** accesses (511 address-taken, where a
  property spelling would be illegal). The real source wrote `X`; the rename
  also means `tween.active` (an inlined auto-property getter — `Tween.active`
  IS auto) renders `tween.__field_active`, which cannot bind against the
  original `DOTween.dll`. The shape of the fix is a **compiler-guaranteed
  proof**: `<X>k__BackingField` exists only for auto-properties, so the
  property can be emitted `{ get; set; }`/`{ get; }` and its accesses spelled
  `X`, with the field kept for the address-taken sites (declines otherwise).
  Concretely: `_storage_name` (the single choke point every field-name path
  goes through) returns the property name, `emit_property` takes the
  bodyless `{ get; }`/`{ get; set; }` path it already has, the field
  declaration stays (renamed, so no CS0102), and the address-take path
  respells from a field row stashed on the `_field_expr` result — that is the
  only place a property spelling would be illegal.
* **The `unknown` marker is the top CS0103 family.** An unresolved value
  renders the text `unknown` (from `_rewrite_unknowns`), which is honest and
  parseable but not compilable: **10,940** occurrences in limbus `f169`, 251
  in survivors, 17 in unitask (`vector32 = unknown;`,
  `Vector2 vector21 = unknown;`, `RuntimeHelpers.InitializeArray(a,
  unknown.nFileSizeLow)`). Any fix must keep the marker visible in the text
  (a bare `default` would fabricate a zero silently) and must keep
  `_drop_dead_unknown_store` / `_strip_dangling_default` working, which key
  on the literal token.
* **`ref` vs `out` is unrecoverable from metadata.** IL2CPP's parameter row
  carries no `Il2CppParameterAttributes` word at all — `out` and `ref` are
  the same byref type — so the survivors `GameInput.FindBinding` (source:
  `out InputAction`) renders `ref` and that one mismatch is CS0535. A fix
  needs a body proof (the byref slot is never *read*, and is written on every
  exit, plus no `ref`-shaped use), not a heuristic on names.

**Harness finding, recorded so nobody repeats it:** a per-image "rebuild the
solution" gate (each recovered image compiled into its own assembly and used
as a reference by the images that depend on it) cannot bootstrap. `csc` does
not write an output assembly that has errors, so an image with any error is
unavailable to its dependents, and the first reference to it turns into
thousands of CS0246. A pilot of exactly that (`tools/recompile_tree.py`,
dependencies derived from the metadata's type→image map) reported 5,829
errors for unitask's six images — all cascade, none information — and was
dropped rather than shipped. The per-image gate against the *original*
sibling assemblies plus the whole-tree single-unit gate above are the two
modes that measure something today.

## Previous work: fix 175 — the one generated name whose brackets hold a type-argument list (2026-11-02, on `main`)

The file writer mangles IL-only characters out of compiler-generated
identifiers (`<>c`, `<Foo>d__13`, `<>9__0_0`) so C# can lex them. The pattern
matched a bracket run of word characters and dots, plus a literal `<>` form —
between them every generated name in the game's own assemblies.

`System.Core`/`System.Linq.Parallel.QueryResults` carries one more shape:
`<System_Collections_Generic_IEnumerable<T>_GetEnumerator>d__21`, an iterator
state machine named after the interface it implements. Its own brackets
contain a type-agument list, so neither form could span it and raw `<`/`>`
reached the file. That single name was the **only** parse failure (1 file / 4
ERROR nodes) on a 36,331-file declaration build of all 161 images — invisible
until this round because the standing parse evidence was game-only (14
images) and `System.Core` was never emitted.

`MANGLED_IDENT_RX` gained a third alternative for `<\w.*<args>\w*>suffix`
with one nested bracket group. It is deliberately narrow: the inside is word
characters and dots only, so a comparison chain (`a < b && c > d`), a legal
nested generic (`List<Foo<int>>`, excluded by the same lookbehind the other
branches use), and a rich-text literal (`"<color=yellow>"`,
`"<auto-generated>"`) all stay untouched — the mangler runs on raw file text
*before* any literal masking, which is what makes the last two conditions
load-bearing. Probed over the two MIT trees: the new branch matches nothing
outside existing stub comments. Rebuilt type: `QueryResults.cs` now declares
and constructs `_System_Collections_Generic_IEnumerable_T__GetEnumerator_d__21`.
5 new tests pin the mangled form, the untouched legal forms, and the
rich-text literals (portable suite **1,566 passed**).

**Verification of 173-175 on the licensed fixture (declarations only).** A
full `--decls-only` build of all 161 images (`out/limbus/cw4d`, 36,493 type
files / 0 failed / 0 fallbacks) gates **brace 0 unbalanced** and tree-sitter
**0 bad / 0 ERROR / 0 MISSING / 0 recovery** over 36,331 files — the same
build before 175 had exactly the one `QueryResults.cs` file in `details`, and
a tree diff between the two shows **1 changed file, 0 added, 0 removed**.
Limbus *bodies* were not rebuilt this round (a full tree is ~2.5 h here; the
standing 24,971-file `f169` tree is game-only), so the body-level evidence is
the two MIT sweeps: **0 crashes** and **0 changed method hashes** against
their pre-fix baselines (1,981 and 1,936 common methods), which is what a
declaration-level fix should look like.

## Previous work: fix 174 — a generic instantiation is not 8 arguments long (2026-11-02, on `main`)

The compile gate's arity family (CS0305 `CombineLatest<T1,T2,TResult> requires
3 type arguments`, CS0308 `UniTask.WhenAllPromise.__c<T1..T8>`) had one root
cause: `_argv_names` rendered `min(argc, 8)` closed arguments. That cap is
Win64 ABI vocabulary (four integer + four float argument registers) applied to
a *metadata* list, and real arities exceed it — `CombineLatest`16` (15 sources
plus `TResult`), `WhenAllPromise`9..15`, the generated `CombineLatest`
extension methods.

A truncated list is worse than a short one because `_distribute_nested_args`
distributes only when a nested type's segment arities sum **exactly** to the
argument count. With 8 of 12 arguments the proof failed and the legacy
single-list rendering took over, attaching every argument to the innermost
segment: `UniTask.WhenAllPromise.<>c<T1..T8>` — CS0308, since the non-generic
`WhenAllPromise` cannot take type arguments — instead of
`UniTask.WhenAllPromise<T1..T8>.__c`.

`_argv_names` now reads the whole list under the same 64-entry guard
`_argv_type_tuples` already used, and returns `None` (unresolvable, legacy
spelling) rather than a partial tuple when the count is absurd or the argument
array is missing. Probed against the fixture: `<>c` display classes inside
`WhenAllPromise`9`..`15` now all render
`...WhenAllPromise<T1..TN>.<>c`. 7 new tests pin the list length, the 16-arity
case, the decline shapes, and the distribution/mismatch pair (portable suite
**1,561 passed**).

## Previous work: fix 173 — generic parameter constraints, and a compile gate with the real build references (2026-11-02, on `main`)

Two things landed: metadata's generic-parameter constraints are now part of
the emitted declarations, and the compile gate can be pointed at the exact
managed reference closure of a Unity player build, which turns "does it
recompile" into a number measured against the *original* assemblies instead
of against nothing.

**173a — constraints were parsed nowhere.** `global-metadata.dat` keeps one
flat `genericParameterConstraints` TypeIndex array plus, per generic
parameter row, a `(constraintsStart, constraintsCount)` range and the CLI
`GenericParameterAttributes` word. `Metadata` read neither, so every emitted
generic lost its `where` clause (`WithCancellation<T>(...)` printed without
`where T : UnityEngine.Object`) and interfaces lost their `out`/`in` variance.
The row is a TypeIndex, so v38+ packs it at the metadata's own width: the
header's `genericParameterConstraintsCount` decides first, `type_w` second
(Limbus 4 — byte-identical to a fixed read; the narrow survivors file 2,
where a 4-byte read consumes two rows per entry and misranges every
parameter).

**173b — emission, decline by default.** `Emitter._where_clause` renders
`class`/`struct`/`new()` from the attributes word, the base class first
(CS0401), then interfaces in metadata order, then a parameter constraint
(`where U : T`). It declines the whole parameter's clause for: an
unreadable index, a pointer/array/unknown spelling, `System.Array` /
`System.MulticastDelegate` (CS0702), a value-type or sealed class constraint
(CS0701), and a second class constraint. `System.Object`/`System.ValueType`
rows are dropped because the flags word already spells them.
`_type_param_indices` now owns "which rows this type declares" (nested own
suffix vs full container), so the `<T>` list, the constraints and the
variance all read one list; variance is emitted only for interfaces, where
the CLI allows it.

Measured on the two MIT fixtures (6-image unitask tree, 2-image survivors
tree): **33** `where` clauses + **4** variant interfaces (unitask), **5**
clauses (survivors). Survivors' own source has exactly four `where` clauses,
three of which are recovered — the fourth lives in an Editor-only file that
never reached the IL2CPP build. Tree diff unitask `q9` -> `cw2`: 466 files,
**20 changed, 446 identical**, 41 added / 37 removed lines, and every changed
line is a `where` clause or a variance prefix plus the `using` it pulls in
(zero body changes). Builds: 472 files / 2,238 bodies / 0 failed / 0
fallbacks (unitask), 293 / 1,936 / 0 / 0 (survivors); brace **0 unbalanced**,
tree-sitter parse **0/0/0/0** on both.

**173c — the compile gate finally has real references.** An IL2CPP player
build keeps the exact managed assemblies it compiled from under
`<Player>_BackUpThisFolder_ButDontShipItWithYourGame/Managed/` (both fixtures
have it: 47 and 73 assemblies). `tools/compile_gate.py` gained
`--managed-refs BUILD_DIR --exclude DLL` (plus `--refs-dir`), per-code sample
diagnostics, `/utf8output`, and locale-safe decoding; `tools/gate.py compile
--managed-refs --fixture <id>` derives the folder from the fixture and
excludes the image under test, so the compiler resolves every name the
decompiler did *not* emit. First census (the tree built before 173a):

| fixture | image | files | syntax | binding |
|---|---|---|---|---|
| unitask | Assembly-CSharp | 15 | 2 | 2458 |
| unitask | UniTask | 301 | 0 | **29** |
| unitask | UniTask.Linq | 142 | 0 | **20** |
| unitask | UniTask.TextMeshPro | 4 | 0 | 269 |
| unitask | UniTask.Addressables / .DOTween | 2 / 2 | 0 | 5 / 5 |
| survivors | Assembly-CSharp | 280 | 0 | **2** |
| survivors | Assembly-CSharp-firstpass | 11 | 2 | 932 |

So a 280-file recovered game assembly is **2 errors** away from compiling
(both `CS0535 GameInput` interface members), and UniTask's own image is 29
away. That is a much sharper target than a reference-free gate: every
remaining error is now the decompiler's or a compiler rewrite's, never a
missing external.

The families, by size (all 8 images): async/iterator **state-machine noise**
(unitask `Assembly-CSharp` is the demo/test scripts: `_Test3_d__20`,
`AsyncUniTaskMethodBuilder<int>` misuse, `TStateMachine` unresolved — 2,458
errors of compiler-rewritten code, not decompiler misses); `objN` receivers
losing members (`CS1061 object does not contain Start/MoveNext`); raw
pointer honesty (`CS0030 object -> byte*`, which `--raw-addr` exists to
address); **nested generic references that put every type argument on the
inner segment** (`CS0305 CombineLatest<T1,T2,TResult> requires 3 type
arguments` for an 8-argument instantiation, `CS0308
UniTask.WhenAllPromise.__c<T1..T8>`); and a handful of one-off shapes
(CS0571 event accessor as a call, CS0103 `objN` used outside its declaring
block, CS0159 label scope, CS8917/CS1729 closure ctor).

**173d — what it bought.** Constraint emission alone takes `UniTask`
**29 -> 22** and `UniTask.Linq` **20 -> 17** with zero new errors anywhere
(CS0452 2 -> 0 and CS0314 5 -> 0 in UniTask, CS0452 3 -> 0 in Linq); the
remaining families above are the next slices. Portable suite **1,554
passed** (12 new tests pin both constraint table layouts, the packing width,
and the rendered/declined shapes).

## Previous work: fix 172 — source-differential honesty and three output fixes (2026-11-01, on `main`)

Fix 171 made source comparison possible; fix 172 makes the report trustworthy
and lands the first fixes it exposed. The two MIT fixtures are unchanged
(local-only under `fixtures/`, git-ignored).

**172a — the report no longer scores code the compiler rewrote.**
`tools/source_compare.py` now:
* strips comments before call/member/shape extraction — a body that is only
  comments compiles to `{}`, and 51 Unitask + 45 survivors source methods were
  being scored against an empty method;
* indexes nested types without repeating the namespace (`N.Outer.Inner` was
  `N.N.Outer.Inner`), which hid every nested source method;
* skips test project folders (`NetCoreTests`, `*.Tests`) like `tests/`;
* treats `[Conditional]` methods, lambdas/local functions, and an output body
  containing an inlined async/iterator state machine as transformed (a new
  `inlined` bucket). IL2CPP/MSVC inlines tiny wrappers (`ChangeAnimation`,
  `WhenAll`, even `Vector3.Equals`), so source and lifted bodies are no longer
  the same method; scoring them as missing calls measured the inliner, not the
  decompiler.

After the change Unitask has 510 source types (was 556), type-unmatched
methods 122 (was 369), and 55 `inlined` methods; survivors has 16 `inlined`.
The averages are not directly comparable to fix 171 because dishonest rows
are gone. On the remaining rows: Unitask call F1 **0.600 -> 0.617**, recall
**0.629 -> 0.644**, full-call recall **739/1,481 (49.9%) -> 687/1,326
(51.8%)**; survivors F1 **0.647 -> 0.667**, full recall **530/964 (55.0%) ->
497/810 (61.4%)**. The worst list is now dominated by genuinely inlined
bodies and async state machines, not by comment/lambda noise.

**172b — empty class-init guards with a lifted class pointer.**
The fix-171 pattern covered `((byte*)typeof(X) + 0xe0)[0]`; the same runtime
guard renders as `((int*)((byte*)objN + 0xe0))[0] == 0` in state machines.
**158** empty Unitask guards removed (empty `if` blocks **177 -> 19** tree-wide;
survivors unchanged at 56, none of this shape).

**172c — a hidden-sret full-struct copy is one managed assignment.**
`T __ret` receiving a value was emitted as one byte store per 16-byte chunk:
`((byte*)&__ret + 0x0)[0] = uniTask1; ... + 0x10 ...`. When a contiguous run
names the same local and that local has `__ret`'s exact type, the run becomes
`__ret = uniTask1;`. A single 16-byte chunk folds only when metadata knows the
return type is at most 16 bytes; field-level stores in other `if` arms are
preserved. Unitask `&__ret` stores **712 -> 478 (-234)** and the 6-image tree
**4,456,338 -> 4,421,308 bytes**; survivors 66 -> 62.

**172d — a primitive instance call on a struct's first field.**
`self.x.Equals(vector.x)` lowers to `Single.Equals` with hidden `this =
&self`; at offset 0 the receiver printed as the whole struct
(`self.Equals(vector.x)`, a method that does not exist). When the callee owner
is a value type and the receiver's first field (metadata offset 0x10) has
exactly the owner's type, the field is used: `self.x.Equals(vector.x)`. The
proof declines for padding/non-first fields, static calls, and receivers that
are not a simple local/member chain. A 200-method Limbus sample lifted
before/after showed **0 changed**, and the survivors tree is byte-identical
with/without it; the Unitask diff is 3 `self.x` receivers plus one `self.r`
(Color). Its regression test is the first Unitask-marked game test,
`tests/test_game_unitask_struct_receiver.py`.

**Build/gate state (`out/unitask/q9`, `out/survivors-roguelike-kit/q5s`).**
Unitask: 466 files / 2,238 bodies; survivors: 291 files / 1,936 bodies. Both
build with **0 failed / 0 fallbacks / 0 type-emit failures**, brace **0
unbalanced**, tree-sitter parse **0 bad / 0 ERROR / 0 MISSING / 0 recovery**;
direct sweeps (2,238 and 1,936 methods) report **0 crashes**. Portable suite
**1,542 passed** (15 new tests cover the metric exclusions, the sret fold,
the extra class-init guard and the receiver proof). Limbus game suite:
**1,584 passed / 2 failed / 1 xfailed**, the same two known
`Unity.Burst.Unsafe` environment failures in the archived partial `f169` tree;
`tests/test_game_parallel_build.py` still hangs on this box's named-pipe path
and was ignored.

**What remains, by size.** Unitask still has 2,284 source methods emitted as
the unavailable-body stub; most are generic methods/types with no registered
instantiation (the generic-sharing model is still the largest open feature).
The report's worst rows are now **inlined callees** (`PlayerAnim.Update` has
no `ChangeAnimation` call because the callee's body is inlined at the native
site) and **async/iterator state machines**; both are compiler rewrites, not
decompiler misses. The 478 remaining `&__ret` stores are mostly `objN` copies
whose argument temp was never bound (`((byte*)&__ret + 0x0)[0] =
((byte*)obj16 + 0x0)[0]`), and 712 `__ret` mentions remain tree-wide.


## Previous work: fix 171 — the open-source differential corpus and four output fixes (2026-11-01, on `main`)

**Two MIT projects now have both the source and an IL2CPP build**, so output
can be compared with ground truth instead of only with another decompiler.
Both are local-only (`fixtures/registry.json`, git-ignored):

| fixture | source | build | metadata | native methods |
|---|---|---|---|---|
| `unitask` | Cysharp/UniTask (MIT) | Unity 2022.3.39f1, Windows x64 | v31 | 24,643 |
| `survivors-roguelike-kit` | Roo-Roo-Roo (MIT) | Unity 6000.3.12f1, Windows x64 | v39 narrow (type_w 2) | 83,855 |

**New measurement: [`tools/source_compare.py`](../tools/source_compare.py).**
It parses the source checkout and the emitted tree with tree-sitter, matches
type/method/arity (property accessors included), and reports call/member
precision and recall, control-flow cosine, and decompiler tells. Async and
iterator methods are excluded (the C# compiler rewrites them into state
machines), as are `Method body was not recovered` stubs. This is the first
metric in the repo tied to the original source rather than to a previous
build; it reports a small worst-method list instead of pretending 100k
bodies were reviewed.

**171a — the v39 `interfaces` table is packed at `type_w`.** The parser read
a fixed 4 bytes/row. On the narrow survivors file the table is 2 bytes/row,
so 3,909 rows became 1,954 and every type whose interface range sat in the
lost tail raised `IndexError` in `type_decl_line`: **54 type-emit failures ->
0**, and the recovered body count rose **1,378 -> 1,936** because those
types never reached their methods. Limbus (type_w 4) is byte-identical.
Test: the synthetic v39 narrow file now carries an interfaces table.

**171b — generic method table rows index `genericMethodPointers[row[1]]`.**
The row is `{methodSpecIndex, methodPointerIndex, invokerIndex,
adjustorThunk}`, not a parallel array: the two counts differ (UniTask 59,586
pointers / 59,725 rows; survivors 96,876 / 97,126). Pairing by row number
shifted every generic target after the first hole, which is why
`BoolWrapper.Reset` called `WhereSelectEnumerableIterator<...>.ctor`,
`GetComponent<T>` called `Memmove<...>`, and the async builders printed
service methods instead of their generic methods. Cross-checked against
Il2CppDumper's own read: `genericMethodPointers[table.indices.methodIndex]`.
Measured with the source differential (same tool, same 1,481/964 matched
methods):

| tree | call F1 | full call recall | zero-call methods |
|---|---|---|---|
| Unitask before | 0.447 | 552/1,481 (37.3%) | 524 |
| Unitask after | **0.600** | **739/1,481 (49.9%)** | **367** |
| survivors before | 0.630 | 515/964 (53.4%) | 161 |
| survivors after | **0.647** | **530/964 (55.0%)** | **150** |

A Limbus A/B (112 sampled `Assembly-CSharp` bodies, snapshot from `HEAD`
`bf72db7`) compared 112 / changed 14, **+52/-50 lines, two inserts, zero
missing, zero crashes** (`out/limbus-ab-final.txt`, local); the changes are
named enum returns, `GetComponent<T>`, correct generic owners, and two
materialized repeated calls. No full Limbus tree was built or promoted.

**171c — generic single-spec tails and qualified generic names.** A tail
whose address carries one generic spec now goes through
`_tail_generic_call` / `_tail_method_args` like a call (both the Lifter and
the pass-2 twin), and the accessor fold sees the trimmed argument list.
`BoolWrapper.Reset` went from
`WhereSelectEnumerableIterator<...>.ctor(this, 0, WrapperT<bool>.set_Value, obj1)`
to `this.Value = false;`. The method-name slice now splits on the last dot
outside generic brackets, so `List<T>.RemoveAll` stays `list.RemoveAll` and
`Component.GetComponent<UnityEngine.Rigidbody2D>` stops printing bare
`GetComponent()` (`PlayerAnim.Awake` now matches its source).

**171d — output cleanup, all exact-shape and decline-by-default.**
* the empty class-init guard pattern also matches the post-fix-134 raw
  spelling `((byte*)typeof(X) + 0xe0)[0] == 0`; **1,423 -> 30** guard lines
  on Unitask (30 have real bodies and stay);
* a raw GC-barrier field store immediately followed by its identical
  managed twin is dropped: survivors' raw `+0x0` stores **400 -> 111**
  (the pre-fix census found 312 exact adjacent twins; single stores and
  differing values stay);
* a void method's trailing inline `return;` after a complete statement is
  removed: **365 -> 110** on Unitask, **321 -> 173** on survivors (returns
  inside loops/conditionals stay);
* a literal return is named through the method's own return type:
  `return 1;` on `UniTaskStatus` becomes `Succeeded`, a bool becomes
  `true`, and `[Flags]` combinations with no exact member keep the literal.

**Build/gate state (`out/unitask/q3`, `out/survivors-roguelike-kit/q3`).**
Unitask 466 files / 2,238 bodies; survivors 291 files / 1,936 bodies; both
build with **0 failed / 0 fallbacks / 0 type-emit failures**, brace **0
unbalanced**, tree-sitter parse **0 bad / 0 ERROR / 0 MISSING / 0 recovery**.
The Unitask tree is 4,544,933 bytes vs 4,787,784 before (-5.1%) with the
same file set. Portable suite **1,527 passed**; new tests cover the
registration table, the narrow interfaces row, the three text passes, the
literal-return proof, and the two survivors bodies. Limbus game suite:
**1,569 passed / 2 failed / 1 xfailed**, both failures the known
`Unity.Burst.Unsafe` absence from the archived partial `f169` tree;
`tests/test_game_parallel_build.py` hangs on this box's named-pipe path
and was excluded. No promotion, no golden/pin re-pin.

One focused Limbus test encoded the OLD misalignment: it expected
`SetPropertyUtility.SetStruct<float>` at an address Il2CppDumper identifies
as `StoryProgressManager.SetScenario<object>` (dump.cs RVA 0x3A9D460, four
parameters; the native site passes all four). The test now asserts the
ground-truth call, with the dump evidence in its comment. The two remaining
Limbus failures are the known partial-`f169` environment gap
(`Unity.Burst.Unsafe` is absent from that archived scoped tree, so the
compile-gate and decl-gate tests cannot find it); `test_game_parallel_build`
hangs on this box's named-pipe path and was excluded from the run.

**What remains, by size.** Unitask still has 2,393 source methods whose
emitted body is the unavailable-body stub; most are methods of generic type
definitions (`AsyncReactiveProperty<T>` and friends), which have no module
method pointer at all. Recovering them needs a generic-context body model,
not a spelling fix. Coroutine/async state machines are compiler rewrites and
are excluded from the metric; shared generic bodies with one registered
representative can still name a sibling instantiation, and the SRE
`__ret` byte stores (712 Unitask sites) remain the largest single textual
family. These are recorded, not silently claimed.

## Current work: fix 170 — v38+ metadata rows are PACKED, not fixed-width (2026-11-01, on `main`)

**Found by registering new open-source fixtures**, not by a gate: the
decompiler had only ever been calibrated on Limbus's metadata shape.

Every v38+ table row carrying a type index packs it at `type_w`, so the
stride follows the widths derived in `_parse_tables` (`type_w` itself comes
from `parametersSize / parametersCount - 8`). The parser hard-coded the
**Limbus** shape (type_w 4) everywhere:

| table | Limbus (type_w 4) | narrow file (type_w 2) |
|---|---|---|
| methods | 32 | **30** |
| parameters | 12 | **10** |
| fields | 12 | **10** |
| events | 24 | **22** |
| field/parameter defaults | 12 | **10** |

Reading the Limbus constants on a narrow file shifts **every row after the
first**. On `survivors-roguelike-kit` (v39, Unity 6000.3.12f1, 94,205
methods) that produced fragmented method names (`arSpacing`, `cted`),
garbage `rid` (0 / 16711680 / 16777215), and therefore a starved
method-address map:

- **native code: 11,427 / 94,205 (12.1%) → 83,855 / 94,205 (89.0%)**
- fields truncated 38,765 / 46,518; the missing tail raised `IndexError`
  in `source_field_name` during a lift
- default-value tables lost a fifth of their rows (8,450 / 12,629)

`limbus` (v39, type_w 4) is **byte-identical before and after** — 299,371 /
319,100 both sides — which is why the bug stayed invisible.

Landed in `fd29fe1`. Verified: survivors lift 120/120, limbus lift 150/150,
unitask lift 100/100, portable 1517 passed (2 new narrow-row tests in
`tests/test_metadata_versions.py`, including the field/parameter default
tables), limbus game suite 407 passed with the single pre-existing
`Unity.Burst.Unsafe` environment failure (fails identically stashed).

**Implication for the corpus:** metadata calibration now has three
independent points (unitask v31 / survivors v39 narrow / limbus v39 wide).
Any future v38+ work must be checked against all three, not Limbus alone.
See `docs/fixtures.md`; the two new fixtures are local-only and
git-ignored.

## Previous work: fix 169 (C8) — generic type identifiers spell the natural C# name; binding debt halved (2026-10-30, on `main`)

**This is fix 117 inverted.** fix 117 deliberately rendered a metadata
arity backtick as an `_N` suffix (`List`1` → `List_1`) so references
spelled the same identifier as our own re-emitted declarations. That is
self-consistent but binds to NOTHING real: a genuine BCL/engine assembly
declares `List<T>`. Against the real Unity 6000 closure the `_N` form was
the single largest error source on the game's own code.

**The change is a PARAMETER, not a default flip.**
`csharp_type_name(..., strip_arity=True)` drops the backtick instead of
turning it into `_N`, and every TYPE-IDENTIFIER site passes it: the
declaration header, the constructor signature, the finalizer, the delegate
name, `type_name`/`_generic_inst_name` (so base lists, parameters, locals,
typeof/alloc text and callee receivers all follow), the interface
qualifier proof, and the enum-member fold. `sanitize()` is shared with
MEMBER names, so it was left alone; the type-only path is
`Emitter._type_ident`. Method names keep the default (they carry no arity).

**A real regression this exposed, and its fix.** `typeof(<name>)` cells
carry NO closed arguments, so stripping arity printed
`typeof(KeyValuePair)` — invalid C#, since a generic definition has no
such closed form. `test_game_bss_ties` caught it. The typeof site now
keeps the `_N` spelling when the typedef HAS a generic container, and
strips only otherwise.

**A second, welcome consequence found by A/B.** `_semantic_type_prefix`
derives a local's readable stem from its declared type TEXT, so `List_1`
lexed as `['List','1']` → stem `list1` → the local printed `list11` (the
arity digit doubled into the counter). With the strip the stem is `list`
and locals read `list1`. Every such local's number therefore moves — that
is the bulk of the tree delta, and it is a naming improvement.

**Measured, per-image, against the real Unity 6000 closure (139 engine +
121 BCL refs), fix-168 tree `post167` vs fix-169 tree `f169`:**

| image | post167 binding | f169 binding |
| --- | --- | --- |
| Assembly-CSharp | 58,697 | **23,075** |
| CommonAssembly | 715 | **49** |
| ServiceAssembly | 138 | **4** |
| RpgSystemCore | 74 | **15** |
| ProjectMoon.BaseStructures | 29 | **10** |
| (6 more) | 400 | 289 |
| ProjectMoon.Battle.Effect.RevolvedSurface | 19 | 2,726 |
| **TOTAL** | **60,161** | **26,352 (−56%)** |

**Real parse errors: 0 on both trees.** The tree-sitter gate on `f169`
reads 24,957 files / **0 bad / 0 errors / 0 missing / 0 recovery**. The
one image that got WORSE (RevolvedSurface 19 → 2,726) is the SAME masking
effect already documented twice: while its types were unresolvable, Roslyn
suppressed every downstream semantic error, so 19 was a floor. The 2,726
are pre-existing decompiler defects in that image (`unknown` /
`data_18943c730` unresolved statics, arithmetic on `object`) that only
become visible once the types bind — the `unknown` token count is
byte-identical between the two trees.

**`tools/compile_gate.py:classify()` corrected.** It treated the whole
CS1xxx band as syntax, so 215 CS1061/CS1501/CS1503/CS1620 (all genuine
BINDING errors) made a clean tree look broken and contradicted the
tree-sitter gate. Those four codes plus CS1750 are now classified as
binding, with the reasoning recorded in the docstring.

**A/B (the new fast loop)**: 112 methods, 24 changed, **+169/−169 lines,
zero insert/delete opcodes** — a pure spelling change. Full build `f169`:
24,971 files / 178,025 bodies / 0 failed / 0 fallbacks / 0 emit failures.

**Eight test files pinned the old `_N` spelling and were reversed**
(`test_review117_arity_spellings`, `test_review120_nested_paths`,
`test_review114_method_flags`, `test_game_fix133_generic_class_layout`,
`test_game_fix148_alloc_family`, `test_game_fix142_iface_resolve`,
`test_game_fix147_usg_walk`, `test_game_limbus_decompile`); 9 new tests in
`tests/test_fix169_generic_arity_strip.py` cover the strip, the keyword
mapping, the declaration/ctor/header agreement, and the typeof guard.

**Not done here (needs the user's re-pin call):** goldens and pins are NOT
re-pinned, and `f169` is NOT promoted. The tree delta is large by design
(every generic local renumber), so re-pinning is a separate approved
action.

## Current work: fix 168 — the enum tables were EMPTY for the whole game, and a fast A/B loop replaces the full rebuild (2026-10-29, on `main`)

**The root cause was metadata-shape, not codegen.** The v39 Limbus
metadata records `element == -1` on **every one of its 3,227 enum
typedefs**. `enum_members` gated its per-member decode on
`0 <= td.element < len(self.types)` and so `continue`d every member,
returning **None for every enum in the game**. The whole enum machinery
(fix 86's blob decoder, the argument/compare/store folds, the
`parse_default` cast) was running against an empty table: no enum ever
rendered a member name or a cast.

**A — `enum_members` reads the underlying type from `value__`.** An enum's
own `value__` instance field carries the same underlying type, and it is
authoritative (first instance slot, `System.Int32` for an int enum). The
fallback fires **only** when `element` is absent, so a metadata that does
record `element` is untouched. Result on `Assembly-CSharp`: **CS0266
6,034 → 7**, **CS1750 287 → 0**.

**B — the enum HEADER had the same hole.** `emit_type` derived `enum E :
uint` from the same `td.element`, so 150 enums with a non-int underlying
printed a bare `enum E` and their members failed to convert (the 7
remaining CS0266 were all `BattleEventBit`, a `long` enum). Same
`value__` fallback. Census of the underlying types actually present:
int 3,077 / byte 69 / uint 48 / ushort 18 / long 5 / short 5 / sbyte 3 /
ulong 2 — i.e. **150 enums were silently missing their base clause**.

**Measured on a fresh full build (`out/limbus/f168`, then discarded after
the A/B below):** 24,971 files / 178,025 bodies / 0 failed / 0 fallbacks /
0 emit failures; tree-sitter parse **0 bad / 0 errors / 0 missing / 0
recovery**; per-image compile vs the real Unity 6000 closure (139 engine
+ 121 BCL): **CS1xxx 324 → 0**, binding 59,837 → 54,241. The 7 leftover
CS0266 are a DIFFERENT family (`uint`/`long` → `int`, not enums) and stay
open. The +412 CS0246 are newly-spelled cross-assembly enum type names
(e.g. `ATTRIBUTE_TYPE`, which lives in `InterfacesLibraryAssembly`), not
defects.

**Quality, proven by A/B rather than by reading:** 176 methods lifted
from the same source both ways, **20 changed, +41/−41 lines, zero
insert/delete opcodes** — a pure spelling change, every one of them a
bare int becoming a named member (`95 → StringSplitOptions.None`,
`1597 → BUFF_UNIQUE_KEYWORD.Inspire`, `41 → BUFF_UNIQUE_KEYWORD.Burst`,
`2 → VIEW_TYPE.BATTLE`, `7 → NumberStyles.Integer`).

**NEW TOOL — `tools/ab_lift.py`: the per-slice loop no longer needs a full
rebuild.** User call 2026-10-29: a full 14-image build costs 65–101
minutes and is a MILESTONE tool, not a per-slice one. `ab_lift.py snap`
lifts N methods (default 60, ~1 s each) from the current source;
`ab_lift.py diff --ref <snap>` re-lifts the same rows and reports
opcode-level counts. `--strict` exits nonzero when any method's LINE COUNT
changed (the shape a structural regression takes; a spelling change is
always a balanced `replace`). **1–3 minutes instead of 60–100.** The
fix-168 slice above is its first use.

Suites: portable **1,505 passed** (6 new in
`tests/test_fix168_enum_underlying.py`: the `value__` fallback, the
recorded-`element` path, the decline when neither is knowable, and the
three header shapes). Game **1,548 passed / 4 skipped / 0 failed** — the 4
skips were the partial `f168` tree being newest-by-mtime with no
MANIFEST; after removing it they fall back to `post167` and 2 of them fail
on the KNOWN environment gap (`Unity.Burst.Unsafe` absent from the
`game-original` role set), i.e. the same 2 failures the docs already
record, zero regression.

## Current work: real-dependency compile test of the fix-167 tree — parse is clean, and the binding debt is now finally VISIBLE (2026-10-29, measurement only, no source change)

**Goal this session:** rebuild the game's own assemblies from HEAD
(`380076e`, fix 165+166+167) and compile them against the REAL engine +
REAL BCL from `D:\unity_editor_6000`, then read the result.

**Fresh build `out/limbus/post167`** (`--roles game-original`,
byte-matches the fix-164 counts): 24,971 type files / 178,025 bodies /
0 failed / 0 fallbacks / 0 type-emit failures. tree-sitter parse gate on
the WHOLE fresh tree: **24,957 files, 0 bad / 0 errors / 0 missing / 0
recovery nodes** — fix 165–167 hold on a from-scratch build, not just the
28-file sweep.

**Per-image compile with 139 engine + 121 BCL refs** (report
`validation_reports/limbus/post167.realcompile.summary.json`,
per-image `post167.unity.compile.json`):

| image | files | real parse errors | CS1xxx band (all CS1750) | binding |
| --- | --- | --- | --- | --- |
| Assembly-CSharp | 24,739 | **0** | 287 | 58,410 |
| Assembly-CSharp-firstpass | 50 | 0 | 19 | 416 |
| CommonAssembly | 44 | 0 | 18 | 697 |
| ServiceAssembly | 8 | 0 | 0 | 138 |
| (9 others) | 108 | 0 | 0 | 176 |

**Key fact this exposes (the old gate number was a Roslyn artifact).**
The fix-164 `gameonly` tree also reports `syntax=75 / binding=12` — but
that 12 is NOT a real binding figure: **a file with parse errors makes
Roslyn skip the entire binding phase**. With 75 real parse errors present
the compiler never got past parsing, so "binding=12" was a floor, not a
measurement. fix 167 drives those 75 to **0**, the binding phase runs for
the first time, and the true debt appears: **58,410** for Assembly-CSharp
(287 "syntax" are all CS1750, an int→enum default-arg, i.e. binding-class
misfiled into the CS1xxx band; real parser errors = **0**).

**The binding debt decomposes into three honestly-named families:**

1. **C8 generic spelling — the biggest real defect (28,361 CS0246).** The
   emitter renders a metadata arity backtick as an `_N` suffix everywhere
   (`List\`1` → `List_1<T>`, `Dictionary\`2` → `Dictionary_2<K,V>`,
   `Nullable\`1`, `Func\`2`, `Action\`1`, …). That is a deliberate
   self-hosting choice (`common.py:csharp_type_name` comment: references
   spell the same identifier the declaration does) — but against REAL
   BCL/engine DLLs every framework generic then fails to bind. **Prototype
   measured** (strip `_N` before `<`, text-level, compiled): AC binding
   **58,410 → 28,697 (−29,713)**, CS0246 47,843 → 20,333, and **CS0101
   duplicate-type = 0** (C# allows `Foo`/`Foo<T>`/`Foo<T,U>` to coexist;
   same-arity stripped collisions do not exist in metadata). The proto's
   122 CS1520 came from its blunt regex eating ctor names — a real fix at
   the emit sites (`_type_generic_params`, `class_hdr`, `ctor_sig`, and
   `csharp_type_name`) will not, because names are sanitized there without
   an arity suffix. The doc's earlier "C8 closed in practice" note
   (fix-163 probe) was wrong: its own example `List_1<UnitSinModel>` is
   itself the bad spelling.
2. **Enum literals (6,034 CS0266 + 287 CS1750).** A field/const initialised
   with a bare int, or an enum-typed parameter default, prints without a
   cast (`private const E _KEYWORD = 287` → needs `(E)287`).
3. **External names — NOT decompiler defects (14,144 CS0246 + 3,769
   CS0234).** Third-party plugin types (CodeStage, FMOD, UniTask/Cysharp,
   TextMeshPro, Spine, DOTween, Newtonsoft, Timeline, …) and engine UI
   types absent from the `game-original` role set. A further **5,338**
   are cross-game-assembly refs (`ATTRIBUTE_TYPE` lives in
   `InterfacesLibraryAssembly`, so AC alone can't see it) — resolved by
   compiling with sibling game DLLs as refs.

**Conclusion for this goal.** The "remaining unfinished work" that the
real compile test was asked to verify splits cleanly: the PARSE-error
program is finished (0/0/0/0 on a fresh build); the remaining debt is
(1) C8 generic spelling and (2) enum literal casts — both real and both
sized, and C8 is now the single largest lever (−29.7k on one image). These
are codegen changes with a large golden blast radius, so they are staged
next rather than folded into this measurement pass.

## Current work: fix 167 — the LAST parse-error families: 28 files / 298 nodes -> 0 / 0 (2026-10-29, on `main`)

**Both remaining families were structural, and both were caught by
bisecting which pass changed the culprit line.**

**A — `_elseif_flatten.negate` sliced `!(...)` blindly (1 file, and it
was the SAME file as the pipe-condition node).** `negate` peeled
`!(` ... `)` by `cond[2:-1]` whenever the text merely STARTED with `!(`
and ENDED with `)`. For a condition `!(A) | (B)` that cut from the `!`
to the LAST `)`, leaving the stray tail `A) | (B`, which rendered the
unparseable `if (A) | (B)` head in
`RpgArtifactEffect_KillSpawnBlackFluid.ProcessBursting`. The arm now
requires `_paren_wraps_whole(cond[1:])` -- the paren opened right after
the `!` must close at the end -- which is exactly the `!(X)` shape.
`!(A == B)` and plain conditions keep their old behaviour.

**B — `_seh_emit_clause` orphaned the clause of a HOISTED region (3
files).** A hoisted try whose close block sits past the join reaches its
close on the teardown `return`. By then an enclosing `_brace_pop` has
popped the try frame, and because `_seh_close_top_try` deliberately
SKIPS a hoisted region, the try's own `}` was never written. The `}`
that was in the buffer belonged to the ENCLOSING block (the `else` arm),
so the old `out.append('}'); ... clause` put the finally AFTER it:

```
try { ... goto L; } } finally { }      <- finally has no matching try
```

The fix inserts the MISSING `}` plus the clause immediately BEFORE the
brace that balances the try's `{` (`_seh_matching_brace`, literal-aware,
walking from the recorded `try_idx`), and shifts every recorded
`try_idx` / `body_idx` / `clause_end` at or after the insertion point.
The discriminator is the FRAME STATE (`len(_bstack) < brace_pos`), NOT
the last line's text: an earlier attempt keyed on `out[-1] == '}'`
matched the normal path too and regressed 3 nodes into 580 across 16
files (measured, reverted). Emitting the `}` at the end at all was
wrong -- it closes the enclosing block.

**Result: the game-only tree's parse errors are GONE.** The 28-file
re-emit + tree-sitter sweep goes **28 files / 298 nodes -> 0 files / 0
nodes**, and a whole-image tree-sitter pass is also clean. Roslyn, whose
`classify` heuristically counts every `CS1xxx` as "syntax", agrees once
the non-parse `CS1750` (a default-argument `int -> enum` conversion,
which is BINDING, miscounted into the `CS1xxx` band) is separated out:
**75 -> 0** genuine parse errors on the whole `Assembly-CSharp` image.

**Real-dependency compile gate extended.** `tools/compile_gate.py` now:
- resolves a Unity install root, its `Editor` dir, OR the managed dir
  (`unity_refs`, descending to `Editor/Data/Managed/UnityEngine`);
- adds the Editor's own BCL reference set (`unity_framework_refs`: the
  `netstandard.dll` ref plus the 17 netfx + 103 netstandard shims, which
  is where `mscorlib` lives), since engine modules alone leave every
  `System.*` name unresolved;
- reports `refs=N engine + M bcl` and has `--no-framework`.

Measured on this box with `D:\unity_editor_6000` (Unity 6000, the same
generation as the fixture's 6000.3.12f1): **139 engine + 121 BCL = 260
references**.

**Suites.** Portable **1,495 passed** (7 new in
`tests/test_fix167_structural_families.py`: the negate slice on a pipe
condition vs a simple comparison, the brace-matcher on literal/comment
inputs, and its decline paths).

## Current work: fix 164 — image roles: build only the game's own assemblies (2026-10-27, on `main`)

**The engine and the plugins ship as real managed DLLs.** The fixture's
162 images split three ways (measured, bodies = methods with native
code):

| role | images | types | bodies | % bodies |
| --- | --- | --- | --- | --- |
| engine (`UnityEngine*`, `UnityEditor*`, `mscorlib`, `netstandard`, `System*`, `Mono.*`, `Microsoft.*`) | 77 | 10,149 | 67,139 | 22.4% |
| third-party (Newtonsoft, UniTask, DOTween, spine, FMOD, Steamworks, Firebase, ProBuilder, TextMeshPro, Cinemachine, RenderPipelines, Burst, Collections, Mathematics, …) | 71 | 7,627 | 54,059 | 18.1% |
| game-original (`Assembly-CSharp` + 13 ProjectMoon/game assemblies) | 14 | 33,256 | 178,173 | 59.5% |

Lifting the first two reproduces information that already exists —
worse: a Unity install's `Editor/Data/Managed/UnityEngine/*.dll` (or the
vendor's NuGet package) has the true names, signatures and XML docs.
They are also where most of the whole-tree Roslyn error debt lives, so
the game-vs-engine compile gate (roadmap P5 slice C) is the metric
that means something.

**`tools/role_classify.py` + `--roles` / `--exclude` / `--exclude-roles`.**
Classification is by image-name prefix — the roadmap's slice A3 design.
`--roles game-original` keeps only the 14 game assemblies; `--exclude`
takes name substrings; `--exclude-roles engine,third-party` is the same
filter spelled from the other side. An unknown name lands in
`game-original` on purpose: dropping an image by accident costs more
than keeping one extra.

**The assemblies tables stay partly undecoded, and that is recorded.**
The v39 `assemblies` table is 68 bytes/row × 162 (11,016 bytes) with
the row's `nameIndex` at `+0x14` (verified 162/162 against the image
names). The `referencedAssemblies` table is 3,860 bytes (965 dwords,
values 1..160 — assembly row indices). But no candidate start/count
field is monotone across the 162 rows, so the reference graph is NOT
reliably decoded and the prefix table is the honest source of truth.
Decoding it would give the third parties' exact versions and an
automatic engine/third-party/game split; that stays open, with the
table layout above as the starting evidence.

**Validation — the game-only milestone build (`gameonly`, commit
`9ae22f5`, 6 workers):**

| | value |
| --- | --- |
| images | **14** (vs the full build's 162) |
| type files | 24,971 |
| bodies lifted | **178,025** |
| failed / fallbacks / type-emit failures | **0 / 0 / 0** |
| wall | 4,645 s (77 min, vs 3 h+ for the full build) |
| brace | **0 unbalanced** / 24,957 files |
| parse (per image, see the note below) | 24,957 files, **28 with errors, 298 ERROR/MISSING nodes** |
| Roslyn compile, `Assembly-CSharp` | **syntax 75 / binding 12** (24,739 files) |

**The 12 binding errors are the headline.** The whole-tree figure of
~455k Roslyn errors was overwhelmingly the engine and plugin images --
exactly the assemblies that already ship as real managed DLLs. On the
game's own code the binding tier is nearly clean, and the parse errors
concentrate in one place (26 of 28 files, 294 of 298 nodes, all in
`Assembly-CSharp`; RpgSystemCore and ServiceAssembly contribute one
each). That is now the concrete target list.

**Environment note (P0-1's known issue, reproduced).** A whole-tree
`gate.py parse` run segfaults on this box; per-image runs are clean, so
the parse number above comes from a per-image sweep (same grammar, one
process per image). Portable suite green; 9 role tests.

## Current work: fix 165 — five parse-error families, 298 nodes -> 7 (2026-10-27, on `main`)

**The 298 nodes were five independent root causes, not one.** Each was
reproduced in isolation first (a probe that feeds one line to the pass),
then fixed at the pass that owns the shape. The order below is by node
count.

**A — `_unsafify`'s fixed 16-iteration cap (258 nodes, 1 file).** The
pass's paren-matched arm peels exactly ONE `*(EXPR)` per iteration, so
`for _ in range(16)` silently left the remainder raw on any line with
more than 16 derefs. `UnitInformationSummaryTabContent.InitContents`
has one 20-deep ternary chain, and `*(A.B + 0x2a)` is not C# (`*` is
not a prefix operator there). The bound is now
`16 + 2 * text.count('*(')`: each iteration consumes at least one `*(`
and the rewrite never introduces a new one, so it always terminates.
That one statement produced 258 of the 298 nodes.

**B — a constant deref after an opening keyword (8 nodes, 8 files).**
`_NCONST_RX`'s `(?<!\w\s)` lookbehind exists to keep a multiplication
(`a * 16`) untouched; it also blocked the deref in `return *16 == 3;`,
which stayed raw. A keyword is never a multiplication operand, so a
second arm (`_NCONST_OPEN_RX`, anchored on `return`/`case`/`throw`/
`default`/`yield`/`await`/`in`/`is`/`as`/`out`/`ref`) converts it to
the same honest `((byte*)16)[0]` the main arm already produces.
Verified: `a * 16`, `b = a * 3`, `f(a * 2, b)` and `(byte*)a * 2` are
all untouched.

**C — a float constant colliding with the usage-slot tag (8 nodes, 1
file).** `-3.1415927f` is `0xC0490FDB` -- odd, high dword 0 -- which is
exactly `decode_slot`'s tag test, so a 4-byte constant-pool load
decoded as MethodRef #2394093 and rendered the placeholder
`GenericMethod#2394093` as a float operand. A usage slot is a
pointer-sized cell, so only a pointer-wide read can be one; both the
`decode_slot` arm and the constant-pool exclusion that guards against
tag-shaped data are now gated on `MemorySizeExt.size(...) >= 8`.
**This one also improves output**: `GetCurrentWaltzAngle`'s whole
second half comes back (`-3.1415927f > real2 - referenceAngle`, then a
`while` loop with `6.2831855f` and `-3.1415927f` as real constants)
where it used to be a `GenericMethod#N` comparison followed by a
`real2 + ?` / `+ unknown` spray.

**D — `==` read as an assignment in the dangling-`default` strip (2
files).** `_strip_dangling_default` clears its live-`?` context on a
`;`, `{`, or assignment `=`. `==` was not excluded, so a ternary whose
CONDITION compares lost its false arm:
`newSortType == t ? (c == 0 ? 1 : 0) : default` rendered
`newSortType == t ? (c == 0 ? 1 : 0) ;`. Neither `=` of a `==` pair
clears the context now; a genuine dangling `Foo(a, b) : default;` still
strips.

**E — the double-negation head (1 node).** `_fix_cond_line`'s
`!(!` arm stripped the outer negation whenever the condition merely
STARTED with `!(!`, because `group(2)` is greedy:
`!(!flag5 ? 1 : 0) | flag1` became `flag5 ? 1 : 0) | flag1` (stray
`)`, unparseable). The outer `!` must now span the whole condition
(`Decompiler._paren_wraps_whole`); real `!(!x)` and single negations
still fold.

**F — the null-conditional fold orphaning an `else` (11 files, the
largest family).** `_null_conditional` folds
`if (x != null) { x.M(); }` to `x?.M();` when the body is one statement
rooted at the tested object -- without checking what follows the block.
An `else` after it lost its `if` (`mail1?.UpdateData(o)` then a bare
`else {`), which no later pass can re-attach. The fold now declines
when the block's follower is `else`.

**Validation.** Per-file re-emit + parse sweep over the 28 error files
(the game-only tree, current source): **28 files / 298 nodes -> 4 files
/ 7 nodes**. The 4 remaining files are all one shape and are NOT fixed
here:

- 3 x an orphaned `finally` (IllustSpineService.FindInstanceByGameObject,
  StageScript_1345, SkillAbility_ToSuperCoin...): a hoisted try whose
  close arrives only on the teardown `return`, after its own frame was
  popped, so `_seh_emit_clause` appends the clause past the ENCLOSING
  `}`. Splicing it behind the try's own `}` was tried and measured: it
  fixed the `finally` but produced a different imbalance in the same
  method (the raw structure has a second mis-associated close), so it
  was reverted whole. Needs a region-plan change, not a splice.
- 1 x `RpgArtifactEffect_KillSpawnBlackFluid` (4 nodes): the condition
  itself is `if (0f >= ? ? 1 : 0) | ((0f < real3) ? flag1 : 1)` at the
  lifter's select form; a `?` inside an `if` head with a top-level `|`
  does not fit `_fix_select`'s statement-level rule.

**Blast radius (measured, no full build).** Re-emitting the
`Assembly-CSharp` image with the current source and diffing against
`out/limbus/gameonly`: **19,746 of the image's 24,738 files emitted
(the sweep was cut at a 90-minute cap, so the last 5k are UNMEASURED),
58 changed, 0 added, +472 / -482 lines (net -10)**. Every changed
delta was reviewed and each is an improvement: `unknown`/`data_`
operands becoming real constants, float-lane folds collapsing an
if/else into a ternary, and the 4 added `: default` false arms being
the D fix. Top files: `Eases.cs` (142), `StageScript_1522` (94),
`Ch10_RPG_FakeLightShadowArea` (88), `JointLineEffect3DEasy` (52),
`BattleDuelViewer_BeatDuel` (50, the C fix). The brace audit over the
same emitted subset is **0 unbalanced**.

An earlier, unsound version of this paragraph reported "11,781 files,
32 changed": that run was truncated mid-emission and its "changed"
count only covered the first 11.7k files. The subset above is the
honest number for what was actually emitted; a full-image rebuild is
the promotion-time check.

**Suites.** Portable **1,478 passed** (24 new in
`tests/test_fix165_parse_error_families.py`, one per family plus the
guards that must NOT fire). Game suite: failure SET **byte-identical**
to the triaged list -- the 2 known environment failures
(`test_game_compile_gate.py::test_small_image_zero_syntax_errors`,
`test_game_decl_gate.py::test_decl_gate_end_to_end`), both needing the
`Unity.Burst.Unsafe` image absent from the standing partial tree.

## Current work: C3 probe — sized, and it is a VALUE bug, not a spelling one (2026-10-28, probe only, no source change)

**The roadmap's mi-24267 repro is already clean** (`GetExpectedAttackDmgMultiplier`
now renders `if (this.CheckCondition(action)) { return this._dmuMul; }`).
So the C3 population had to be measured directly on the tree.

**The real shape is a dropped lane, not a split store.** `movsd
[rbx],xmm0` copies EIGHT bytes; the lifter renders it as a single
`.x` lane:

```
0x1815736d9 movsd xmm0,qword ptr [rax]
0x1815736e5 movsd qword ptr [rbx],xmm0      ; 8 bytes
0x1815736e9 mov [rbx+8],eax                 ; the .z tail
```
renders as
```
((byte*)&__ret + 0x0)[0] = obj6.x;   <- the 8-byte copy, spelled as .x
__ret.z = obj6.z;
return __ret;
```
i.e. `obj6.y` is silently absent. Merging the pair into
`__ret = obj6;` is the correct fix and is what C3 asks for.

**Measured population (game-only tree, `Assembly-CSharp`):**

| shape | sites |
| --- | --- |
| `((byte*)&BASE + 0x0)[0] = SRC.lane;` followed by more lane writes to BASE (the movsd split) | **39**, of which all 39 are the exact `.x` + `.z` pair reading one source struct |
| `((byte*)&BASE + 0x0)[0] = <anything>` with NO lane tail (a whole-struct store already) | 1,768 |
| the same with 1 lane tail | 372 |
| raw lane stores at `+0x4`/`+0x8` | 66 |

So the provable merge set is **39 sites**, and the merge is sound only
when every tail lane reads the SAME source struct and the lanes
partition the struct -- the census shows all 39 do.

**SHUFPS's co-required half is measured too.** The per-lane map is
generic over any imm8 (not the three immediates the comment names), and
its gate is whether `_lane_value` resolves each lane: an instrumented
400-method lift resolves **108 lanes and declines 30 (78% accept)**. The
28,810 SHUFPS sites tree-wide are therefore mostly modeled; the open
half remains DESTINATION INVALIDATION (an unproven lane keeps the
pre-shift register value live), which is what must co-land.

**Why this is still a probe and not a slice:** the merge changes 39
struct returns' VALUES, so it needs the paired partial build and a
delta review that the current measurement budget does not cover
alongside the SHUFPS invalidation work. Recorded here with the shape,
the population and the exact sites so the slice can be taken whole.

## Current work: P5 slice C — the game-vs-engine compile gate is wired, and the answer is "refs don't matter" (2026-10-28, on `main`; engine upgraded to Unity 6000 on 2026-10-29)

**Superseded 2026-10-29 by a newer, matching install.** The user then
pointed at `D:\unity_editor_6000` — Unity **6000**, the same generation
as the fixture's own `6000.3.12f1` — whose
`Editor/Data/Managed/UnityEngine/` holds **139 managed engine
assemblies**, and whose `Editor/Data/NetStandard/` carries the matching
**121 mscorlib/netstandard reference shims**. That is the install all
the numbers in the fix-167 section were measured with; the 2022 install
below is kept only as the historical record of the first wiring.

**The first blocker (2026-10-28): a Unity Editor IS installed here.**
`Unity Hub`'s `editors-v2.json` registered 2022.3.61f1c1 at
`C:\Users\tester\3D Objects\Editor`, and its
`Data/Managed/UnityEngine/` held **87 managed engine assemblies**
(`UnityEngine.dll`, `UnityEngine.CoreModule.dll`, every module, plus
the `.xml` docs).

**`tools/compile_gate.py --unity <editor-root-or-managed-dir>`.** The
gate always ran with NO reference closure, which made every external
name a binding error and the tier a measure of unresolved externals
rather than of the decompiler. `unity_refs()` resolves an Editor
install root, its `Editor` dir, or the managed dir directly (descending
to `Editor/Data/Managed/UnityEngine`, not taking the first existing
directory -- an install root holds native helpers like `Calc.dll` and
no managed engine assemblies at all); `unity_framework_refs()` adds the
Editor's own BCL set. `run_gate(..., refs=...)` writes `/r:` lines into
the response file and reports `refs=N engine + M bcl`.

**The first "refs don't matter" answer was a Roslyn artifact — corrected
2026-10-29.** The original measurement (below, kept for the record) read
`syntax 75 / binding 12` under all three ref closures and concluded the
closure was irrelevant. The `binding=12` was fake: **a file with parse
errors aborts Roslyn's binding phase entirely**, so with 75 real parse
errors still present the compiler never reached binding and 12 was a
floor. Once fix 167 drove those 75 to 0 (see the top section), the
binding phase runs and the true debt on the game's own `Assembly-CSharp`
is **58,410** — dominated by C8 generic spelling (28,361) and enum
literals (6,321), with 14,144 genuinely-external third-party names and
5,338 cross-game-assembly names. So the closure DOES matter the moment
the parse tier is clean; the earlier "nearly clean at the binding tier"
conclusion was wrong for exactly that reason.

**Original (superseded) 2026-10-28 measurement:**

| mode | files | syntax | binding |
| --- | --- | --- | --- |
| refs = 0 (no closure) | 24,739 | 75 | 12 |
| refs = 87 (2022.3 UnityEngine only) | 24,739 | 75 | 12 |
| refs = 139 engine + 121 bcl (Unity 6000) | 24,739 | 75 | 12 |

The 12 were **12 `CS8641 "else" without a matching if`** sites -- real
decompiler defects, exactly fix 165's family F (and the same file as the
`|`-in-an-if-head select form). Those are fixed now. The `binding=12`
floor is the artifact described above: parsing had already failed.

**Fix 165 verified at the compiler, not just the parser.** Compiling
just the 28 fix-165 files against the same 87 refs: **syntax 298 -> 18,
binding 12 -> 1** (the last `else` downstream of the open `|` head).

**Environment note for re-running this.** The full-image emission sweep
does not finish in 90 minutes on this box (24,738 files, ~3 s/file
serial), so the blast-radius numbers are a measured SUBSET; the compile
gate above is complete (all 24,739 files) and is the authoritative
figure. Portable suite 1,485 passed (7 new in
`tests/test_p5c_unity_compile_gate.py`: Editor-root vs managed-dir
resolution, the descend-not-first-dir rule, absent path, ref count, and
that the `/r:` lines really reach the response file).

## Current work: fix 163 probe — P2-5 small families, three of four already closed (2026-10-27, probe only)

**C6 and C8 were closed by the earlier slices; C4 needs its own
design; C10 is a user call.** Measured on HEAD, not on the stale v39
tree:

- **C6 (undeclared stack-arg temps): closed.** CS0103 is no longer in
  the compile gate's top ten at all (the top is CS0518 35,142 /
  CS0246 5,570 / CS0234 1,000 / CS0115 628 / CS0656 458 — the
  runtime-image baseline debt, not this family). fix 155's `_` →
  `default` and the earlier arity/trim work removed the population
  that used to print bare `objN` arguments.
- **C8 (generic spelling): closed in practice.** The v39 tree's 1,558
  `List_1<T>` / `Dictionary_2<T…>` lines are stale-build artifacts:
  a fresh lift of the roadmap's own example
  (`ActionSlotDetail.GetNotSelectedSin_SortedByAscending`) now renders
  `List_1<UnitSinModel>` — the alloc fold already takes the closed
  type from the same statement's `typeof(...)`. A 600-method random
  fresh-lift sample finds **2** unbound-generic occurrences total.
- **C4 (`Il2CppRaw.Ref<T>` raw fallback helper): needs a design
  first.** The roadmap itself defers it until the file-header
  annotation format is settled ("先定文件头注记格式再动"), and no
  `Il2CppRaw` exists in the package today. Its principle — a degraded
  product must be DECLARED — is already honoured by every current
  fallback (the raw `((byte*)x + 0xN)[0]` deref is legal C#, the `_`
  sentinel renders `default`, `object objN` is a declared local), so
  the helper would be a readability layer, not a correctness fix.
  Deferred with that reasoning.
- **C10 (publicize, opt-in): a user call by definition** — the
  roadmap marks it opt-in and the standing user-call list keeps
  emitter-wide spelling changes out of autonomous landings.

## Current work: fix 162 — C2 lands: recursive inner-offset field resolution (2026-10-27, on `main`)

**The gap was exactly what the roadmap predicted.** `instance_field_chain`
merges a class's whole base chain but stops at each field: an offset
INSIDE an embedded value type -- the roadmap's `0x18` inside a field at
`0x10` → `.field.z` -- finds no entry and renders
`((byte*)recv + 0x18)[0]`. `Il2Cpp.nested_field_path` walks it: the
chain's nearest value-typed field at or below the offset, then that
struct's own chain for the remainder, recursively.

**Four guards, each a decline rather than a guess.** (1) Only a value
type whose `value_type_size` actually covers the remainder is followed
-- a union-like or over-approximated layout declines. (2) A
class-typed field is never followed: its object is a pointer, not
inline storage. (3) The depth is bounded at 4, so a self-referential
value type cannot recurse. (4) The offset convention mirrors the flat
branch EXACTLY -- a value-type receiver maps its read offset into the
chain at `disp + 0x10` (the boxed header shift), a class receiver at
`disp`. The first draft used `disp - 0x10` and rendered
`this.propertyPath.m_Part0.m_Kind` for a `0x40` store; the A/B diff
caught it before any build (the live ground truth
`PropertyPath` chain is `0x10 m_Part0 / 0x30 m_Part1 / 0x50 m_Part2`,
all `PropertyPathPart` value types, and `nested_field_path(0x40)`
correctly answers `m_Part1.m_Kind`).

**Measured on a 1,500-body random sample (seed 0, in-process A/B, no
build):** 15 bodies change (1.0%), raw-deref lines **151 → 94
(−38%)**, net −12 lines. The renders are the point:

    this.m_Enumerator.type = enumerator1.m_Object;         (was ((byte*)this + 0x28)[0])
    fastGlitchUrpPass1.tempCopy.m_BufferPointer = 0;       (was ((long*)(...) + 0x110))
    this.m_HighlightState.color = state.highlightState.padding.m_Bottom;
    animationEvent1.m_AnimatorStateInfo.m_Name = obj37;

**Honest scope note.** A first probe of
`Unity.Collections.DataStreamWriter.get_Capacity` looked like a C2
miss (`this + 0xc`), but the typedef has only two fields (`m_Data`@0x10,
`m_SendHandleData`@0x30) -- that read is a larger enclosing struct's
offset, not an inner one, so it correctly stays raw. The fold only
fires where the layout genuinely nests.

**Validation.** Portable 1,445 (+8 unit tests: flat field, the
roadmap's inner case, three-level nesting, class-field decline,
past-the-size decline, unknown-size decline, depth bound, no-chain
decline). Paired `--only UnityEngine.UIElementsModule` (c2pre vs
c2post7, 851 files both sides): **76 files changed, brace 0
unbalanced**, compile gate **syntax flat at 17, binding 42,922 →
42,925 (+3)** — and those 3 are an HONEST GAIN, not a regression: the
fold now states the real `PropertyPathPartKind` where the pre-render
laundered it through `int num3 = ....m_Kind.value__`, and that enum
(`Unity.Properties.PropertyPathPartKind`, metadata td 48479) is simply
not emitted in this image — the pre-render hid a pre-existing export
gap behind a type lie. Two bugs the A/B caught before any build is
accepted, both now guarded: (a) applying `_recv_member_ty` (outer
generic substitution) to a nested struct's member rendered
`m_Node = 0f`, (b) running the nested walk on the STORE path rendered
`m_HierarchyFlattened = real1` / `= null`, so the walk is now
`load=True`-only and every store site keeps its honest raw deref.
Full suite: **1,489 passed / 2 known env failures / 1 xfailed** —
failure SET byte-identical to fix-159, zero pin moves.

## Current work: fix 161 probe — C3's lane merge, sized and re-scoped (2026-10-26, probe only, no source change)

**The roadmap's C3 repro is already fixed; the real population is the
whole SIMD-store surface.** `mi 24267`
(`EGOGiftAbility_98416.GetExpectedAttackDmgMultiplier`) now renders
`return this._dmgMul;` — the split-store case the roadmap pinned as
C3's repro was closed by later field/return work, so it is no longer
evidence of an open gap. Measured directly over both executable
sections: **109,339 `movsd`/`movss` memory stores** (13,407 in
`.text`, 95,932 in `il2cpp`) plus **6,945 `shufps`**. That is the
honest C3 scope, and it is exactly why the roadmap binds it to the
SHUFPS destination-invalidation model as one slice: merging a split
store into a struct assignment without modelling SHUFPS's destination
clobber would let a stale lane survive across the merge. Per the
decline-by-default rule and the build policy, this stays deferred as
a single paired slice rather than a partial landing.

## Current work: fix 160 probe — C2's raw-offset field resolution, measured (2026-10-26, probe only, no source change)

**The gap is recursive inner offsets, not receiver typing.** The
`(byte*)RECV + 0xN)[0]` raw-deref population splits 152,940 generic
temps / 74,716 named receivers tree-wide, and `this` alone carries
9,299 sites over 343 distinct offsets — all real class fields. The
existing `_field_expr` chain fold DOES resolve a class's own offsets
(`DataStreamWriter + 0x10 → m_Data`, verified live), so a `this`-based
miss is not a typing failure: `Unity.Collections.DataStreamWriter` is
a **value type**, and its `get_Capacity` reads `this + 0xc` — the
capacity lives INSIDE the `m_Data` (Unity.Collections.DataStream)
sub-struct at `+0x10`, i.e. the roadmap's exact C2 case (an inner
offset `0x18` inside a field at `0x10` → `.field.z`). Resolving those
needs the recursive chain walk with the inner struct's own layout —
the Expr/lifter-layer work the roadmap already scopes as C2, not a
template or a recognizer.

**Two measured sub-populations, both blocked on the same walk.**
(1) The 719 `((byte*)objN + 0x20)[0] = unknown` stores come from
`0x1807eaf40`'s enum-entry result (declined above for the same
reason: 97.6% of its sites are these stores). (2) The ~400
`rectTransform1.anchoredPosition = unknown` / `list11._items[numN*3] =
unknown` lines are NOT field-resolution failures — the field name and
the receiver both resolved; the VALUE is what the lifter could not
prove, and `unknown` is the honest marker for it. Counting them as C2
would overstate the payoff, so the C2 scope stays: the recursive inner
offset, with the `this`-sites (9,299) and the enum-entry stores (719)
as its two provable populations.

## Current work: fix 159 — the interface dispatch twins, admitted by the landed arity proof (2026-10-26, on `main`)

**The twins were already solved — one register-name comparison away.**
`0x180013b50`/`0x180016f40` (2,778 call sites) are the SHARED-GENERIC
interface dispatch thunks: (u16 methodSlot, interfaceTypeIndex, recv,
<first method arg>) with the stack args forwarded — the body scans the
receiver klass's interfaceOffsets (count `klass+0x12E`, table
`klass+0xB0`), computes the vtable slot at
`klass + 0x138 + 16*(offset + slot)`, tail-jumps `[slot]` with the
MethodInfo* in R8, and falls back to `il2cpp_interface_get_method` on
a miss. That is byte-for-byte the shape `_iface_dispatch_arity`
already recognizes (the landed landing-8 proof: one 0x12E count, one
0xB0 table, one 0x138 add, one shl 4, an indirect tail jmp, a miss
call — a read of R9 means one forwarded argument) — and the twins'
call sites route through the landed `_param_interface_dispatch` fold,
stack-arg recovery and closed-generic substitution included.

**The bug was `_r9_touch`'s operand compare.** The twins extract the
forwarded argument as `movzx esi,r9w` / `mov esi,r9d` — SUB-register
forms whose iced `op1_register` is R9W/R9D, not R9 — so the first
touch read as None and both thunks sat at arity 0. The fix normalizes
operand registers through their 64-bit name before comparing; the
sub-register extractions now read as the forwarded argument they are,
both twins admit at arity 1, and the landed fold renders the sites as
the interface's own method (slot = the interface's method-row order,
verified on IReadOnlyList`1 slot 0 = get_Item and IUniTaskSource
slot 2 = GetResult):

    if (readOnlyList11[num2] == this._curSkillMotion)

— the fix-158-era render `sub_180016f40(0, typeof(...), recv, num2)`
becomes the closed-generic indexer call, arguments recovered, no
residue. A duplicate recognizer + fold arm written during the probe
was removed whole: the landed machinery (stack-arg tiles, closed
generics, ABI gates) is strictly stronger than anything the duplicate
did, and shadowing it would have rendered worse code.

**Validation.** Portable 1,437 (no regressions); the fix-139/142
interface-fold tests pass unchanged; game +3 (both thunk builds admit
at arity 1 through the memoized choke, the closed-generic indexer site
folds, the stack-argument recovery site folds). Paired
`--only Assembly-CSharp` (ifacepre/ifacepost, 24,789 files /
176,785 bodies both sides, serial — the 8-worker runs hung twice in
this box and were killed; the serial run is the honest schedule):
**474 files changed, net −1,484 lines, the twin `sub_` lines
2,394 → 915 (−1,479, 62%)**, brace **0 unbalanced across 24,789
files**. The 915 honest remains split 778 IUniTaskSource (the R9
argument renders `_` in the surrounding state machine — no provable
argument, so the fold declines) and 137 opaque-interface expressions.
Sample folded renders, all correct:

    uniTaskSource2.GetResult(num8);
    string text3 = retryHandler.GetTurnCountText(turnCount);
    string text1 = staticDataJson.GetDataByIndex(num4);
    if (readOnlyList11[num2] == this._curSkillMotion)

Full suite: **1,481 passed / 2 known env failures / 1 xfailed** —
failure SET byte-identical to fix-158, zero pin moves.

## Current work: fix 158 — the P/Invoke resolver folds to the managed DllImport call (2026-10-26, on `main`)

**The attribute blob decoder proved DllImport is stripped.** The v39
custom-attribute blob format was decoded byte-exact this session
(`CompressedUInt32 count`, `count × int32 ctorIndex` (4-byte fixed,
global MethodDef row), then per attribute `CompressedUInt32
argumentCount/fieldCount/propertyCount` with self-describing values —
one tag byte (0x0E string, 0x55 enum + CompressedInt32 type index,
0x1D array), strings `CompressedInt32` byte length + UTF-8, named
arguments value-first then a `CompressedInt32` member index; the
compressed uint has no 3-byte form). The probe decodes 16,728 of
16,744 method blobs and names real attributes —
`FreeFunctionAttribute("UnityEngine_Identifiers_GetInstallationId")`
exact — and **DllImportAttribute appears zero times**: il2cpp consumes
it at codegen time. The (module, EntryPoint) → method mapping cannot
come from the attribute table.

**What survives is the stub.** 2,032 methods carry `flags & 0x2000`
(pinvokeimpl): Facepunch.Steamworks.Win64 1,024, FMODUnity 583,
Firebase 244, System 112, mscorlib 48. Their codegen fnptr
(`module.method_pointers[(token & 0xFFFFFF)-1]`) is the resolver stub
whose descriptor stages the same two literals the inlined call sites
build — the module name UTF-16, the entrypoint ASCII. The method's
metadata name is the entrypoint (`FMOD.Factory.FMOD5_System_Create`),
and an explicit EntryPoint override is only visible in the stub, so
the stub decode is the source of truth.

**The scan and the fold.** `scan_pinvoke_stubs` (wired next to
`scan_icall_cache`) votes the shared resolver from the stubs' call
targets (`0x18078d570` — the same helper every site uses), decodes
1,999/2,032 stubs into `pinvoke_map[(module, entrypoint)] = mi`, and
maps 2,018 inlined fill sites' cache cells into `pinvoke_cells`
(cell → mi) by decoding each call site's window — the two rip-leas
name the pair, the post-call store names the cell; only pairs that
resolve in the map are taken. `decode_slot` serves those cells with
the fix-66 fptr annotation, and `_call`'s early arm (beside the icall
arm) collects the `&"literal"` texts the site staged — registers
uncounted plus the tracked stack slots — and pair-matches them against
`pinvoke_map`; the resolve renders nothing and the guarded invoke
collapses to the direct managed call with hidden-arg trimming:

    FMOD.Studio.EventInstance.FMOD_Studio_EventInstance_SetTimelinePosition(
        BattleSoundGenerator._currentInstance, millisec);

**Validation.** Portable 1,437 (no regressions); game +3 (the map and
resolver detected, the SetBgmStartPos site renders both managed calls,
cell reads render names not `data_NNN`). Paired `--only FMODUnity`
(pinvpre/pinvpost, 305 files both sides): 29 files changed,
**net −11,048 lines**, `sub_18078d570` **1,251 → 2** (the remaining
two are the shared-stub declaration), brace 0, compile gate
**binding 12,628 → 12,624, syntax flat at 6** — the removed junk was
`data_`-cell assignments, which the emitter declares, so the compile
gate barely sees this win; readability is the metric (the diff shape:
eight fill-dance lines plus a `/*indirect*/` phi-invoke become one
typed `return`). Tree-wide the fold covers 4,392 sites (Steamworks
2,359, FMODUnity 1,248, Assembly-CSharp 414, System 264, mscorlib 103).
Full suite: **1,478 passed / 2 known env failures / 1 xfailed** —
the failure SET moved by exactly two fix-141 shape pins whose sites the
fold improved past their pinned spellings
(`FMOD.Channel.setFrequency` now renders
`return FMOD.Channel.FMOD5_Channel_SetFrequency(this.handle, frequency);`
and `ISteamMusicRemote.GetUserInterfacePointer`
`return Steamworks.ISteamMusicRemote.SteamAPI_SteamMusicRemote_v001();`)
— both test assertions updated to the new (better) shape per the
established precedent; no golden or pin moved.

## Current work: fix 157 — the isinst family's generic-variable build, lazily named (2026-10-26, on `main`)

**`0x1807e3c60` (10,696 sites) is the isinst helper's second body.**
Same prologue as the census-named `0x180479f80`
(`mov [rsp+8],rbx; mov [rsp+10h],rsi; push rdi; sub rsp,20h;
mov rbx,rdx; mov rdi,rcx; test rcx,rcx`), the
IsAssignableFrom-shaped predicate call, the VAR/MVAR (0x13/0x1E) type-
kind checks, the interface-offset fallback, and the same
`cmp rbx,[rip]; cmove rax,rdi` System.Object short-circuit. The
relaxed fix-151 recognizer already matches it (`_is_isinst_helper`
returns True) — it was never probed because the census sample is
Assembly-CSharp-only and the lazy prober did not carry the isinst
check. The hot-target census can never reach this body: its sites are
shared-generic code living outside the sample.

**The lazy prober now carries it.** `_array_addr_name` extends with the
isinst arm: the recognizer's structural proof registers the address in
`rt_isinst` and names it `il2cpp_object_isinst`. Sites whose klass
argument renders `typeof(T)` route through the fix-151 `obj as T`
fold; on this fixture the common shape takes the target klass from the
rgctx (`[klass+0x40]` — a startup-initialized constant the bytes do
not carry), so the fold declines there and the honest named call
remains. Propagating those rgctx constants is the follow-up that would
flip ~9.5k tree-wide sites to `obj as T`; it needs the
Il2CppClass-rgctx slot decode, not a recognizer.

**Validation.** Portable 1,437 (no new tests needed — the recognizer
is fix-151's, already covered); game +2 (the lazy naming plus a
declines-without-typeof ground truth on StencilMaterial.Add). Paired
`--only UnityEngine.UI` (isinstpost vs the fix-156 tree, 981 files /
12,249 bodies both sides): 28 files changed, 96 renders renamed,
**0 `sub_1807e3c60` lines remain**, brace 0, compile gate
**50,513 → 50,506 binding (−7), syntax flat at 17**. Full suite:
**1,475 passed / 2 known env failures / 1 xfailed** — failure SET
byte-identical to fix-156, zero pin moves.

## Current work: fix 156 — the icall resolver found again; every eager resolve site renders the managed call (2026-10-26, on `main`)

**`scan_icall_cache` was silent on this fixture.** The icall thunk
caches are BSS cells filled by
`lea rcx,[sig]; call resolve_icall; mov [rel CELL],rax` — and the scan
pinned that layout. The v39 fixture never emits it bare: the null guard
`test rax,rax; je +N` always sits between the call and the store, and
an optional spill (`mov r10,rax`) sometimes precedes the guard, so the
scan found nothing, `rt_icall_resolve` stayed unset, and every eager
resolve site rendered as an unannotated
`sub_1807a5bf0(&"UnityEngine.X::M(sig)", <invoke args merged>)` with
the invoke's arguments sprayed in. Cell reads stayed annotated (they
flow through the class-cache scan's `::` fallback), so the whole fill
dance printed five junk lines around one indirect call.

**The scan now walks the tail: spill?, guard?, store** (rel8 and rel32
`je` accepted), and the helper vote counts signature-valid fills only —
the same-shaped class-name caches whose first argument is a bare name
share the tail and would win a raw-count vote. Result: the helper is
`0x1807a5bf0`, **29,126 signature-valid fills, 4,197 distinct cache
cells**, a single vote candidate (no pinvoke-resolver ambiguity — a
pinvoke variant with `::` signatures could poison the vote; none
exists here).

**The resolve call itself renders nothing.** `_call`'s early arm (moved
before the argument build so the feeding `lea` never use-binds into a
temp — the post-argument arm leaked a dead
`object objN = &"sig"` CS0214 operand at every jmp-detour site) reads
the signature from RCX uncounted and seats the annotated fptr in RAX.
The clobber pops go FIRST — `VOLATILE` includes RAX, and stamping
before the pop lost the fptr to a fresh `vN`. When the guard load
already put the cell's fptr in RAX the arm keeps that Expr, so the
merge lanes hold one value. The guarded invoke then renders the
managed call: `UnityEngine.Transform.SetPositionAndRotation_Injected(num1,
ref vector32, ref quaternion2)` — hidden-arg trimming and `ref` typing
from the ordinary resolved-call path.

**Honest remains.** At jmp-detour fills (the store sits behind
interleaved code) the guard branch is structural — the same guard is
the loop's re-check when the thunk sits in a `while` — and the
structure pass renders a degenerate merge: `object objN = <icall>;
objM = objN(args)`. That is no worse than the pre-fix render (which
added the `sub_` line and the leaked operand), and swallowing the
guard branch there once collapsed a whole loop body — so the detour
shape stays honest junk in the C-family backlog.

**Validation.** Portable 1,437 (+8: guarded/tight/spill+rel32 fill
shapes, the sig-validity vote, non-winner cells unmapped, the early
arm's no-render + fptr seating + RAX keep + unresolved decline); game
3 new tests (resolver detected, the NoirNailAlly site renders the
managed call, the detour site leaks no operand). Paired
`--only UnityEngine.UI` (icalpost3 vs the fix-155 tree, 981 files /
12,249 bodies both sides): 59 files changed, **0 `sub_1807a5bf0`
lines and 0 `= &"` operands remain** (defaultpost3: 27 / 0), brace 0,
compile gate **50,529 → 50,513 binding (−16), syntax flat at 17**.
Full suite: **1,473 passed / 2 known env failures / 1 xfailed** —
failure SET byte-identical to fix-155, zero pin moves.

**Remaining C5 population, probed this session.** `0x18078d570`
(5,000 sites) is the **P/Invoke resolver**: the caller builds a
0x30-byte descriptor `{module_chars@0, module_len@8,
entrypoint_chars@0x10, entrypoint_len@0x18, ...}` from two literals
(`"fmodstudio"`, `FMOD_Studio_EventInstance_SetTimelinePosition`),
caches the native fnptr in a data cell, and invokes it. The module
name is stored **UTF-16** in the literal pool (a plain `cstr` reads
only `'f'` — that is why the lifter rendered `&"fmodstudio"`: its
wide-string decode already handles it), entrypoint names follow as
ASCII, and **no data-section pointer references the literals** — the
descriptors are built per call site and the resolver resolves live.

**fix 158 probe, round 2 — the custom-attribute blob decoder is
built, and it cannot supply the mapping.** The v39 metadata header
already parses `attributeData` (byte blob) and `attributeDataRange`
(8-byte entries = `(ownerToken u32, blobStart u32)`, 94,709 rows;
owner tokens are ECMA tags — 0x02 TypeDef, 0x04 Field, 0x06 MethodDef
(31,075), 0x08 Param, 0x17 Property, 0x20 Assembly). The blob format
(per Il2CppDumper's CustomAttributeDataReader, verified byte-exact
against this fixture): `CompressedUInt32 count`, then `count × int32
ctorIndex` (4-byte fixed, global MethodDef row), then per attribute in
ctor order: `CompressedUInt32 argumentCount, fieldCount,
propertyCount`; each value self-describing — one tag byte (the
Il2CppType enum; 0x0E string, 0x55 enum + CompressedInt32 type index,
0x1D array), strings `CompressedInt32 byteLength` (sign bit) + UTF-8
(`52` = 82 = 41 << 1), I4/U4 compressed in v29+, named arguments value
FIRST then `CompressedInt32` member index (negative = -(i+1) followed
by a CompressedUInt32 declaring-type index). The compressed-uint has
NO 3-byte form: 1/2/4 bytes, plus 0xF0 (5-byte), 0xFE (Int32.Max),
0xFF (0xFFFFFFFF). The probe decodes **16,728 of 16,744 method blobs
cleanly** (the 16 are genuine edge shapes) and the ctor histogram
names real attributes (CompilerGenerated 5,551, DebuggerHidden 4,350,
FreeFunction 525 — blob 0x6000002 decodes to
`FreeFunctionAttribute("UnityEngine_Identifiers_GetInstallationId")`,
ctor 317,555, exact). **DllImportAttribute appears ZERO times** —
il2cpp consumes it at codegen time and strips it from the runtime
blob, so the attribute table cannot map (module, EntryPoint) → method.

**The working mapping path is the pinvoke stub scan.** 2,032 methods
carry `flags & 0x2000` (pinvokeimpl): Facepunch.Steamworks.Win64
1,024, FMODUnity 583, Firebase 198+46, System 112, mscorlib 48. Their
metadata NAME is the entrypoint (`FMOD.Factory.FMOD5_System_Create`),
and their codegen fnptr (module.method_pointers[(token & 0xFFFFFF)-1])
is the descriptor-builder stub — `FMOD5_System_Create`'s stub at
0x18358e670 leas the SAME literals as the SetBgmStartPos call site
(0x187532488 = "fmodstudio" UTF-16). Fix 158 is therefore: (1) a scan
enumerating pinvokeimpl methods → fnptr stub → decode the two
descriptor literals → `pinvoke_map[(module, entrypoint)] = mi`; (2) a
`_call` fold for the resolver shape (the descriptor's two leas from
the stack-store state → map lookup → the resolve+cell+invoke collapses
to the managed call `M(args)`, the same machinery fix 156 uses). The
twins `0x180013b50`/`0x180016f40` (2,778 sites) were LANDED as fix 159
(see the top section). `0x1807e3c60` (10,696
sites) is the **isinst family's generic-variable build** — the relaxed
fix-151 recognizer already matches it (prologue + one `cmove` + the
System.Object short-circuit); it only needs the lazy prober extended,
but most of its sites take the target klass from the rgctx
(`[klass+0x40]`), which no `typeof()` argument renders.

**`0x1807eaf40` (3,993 sites) — CLOSED-DECLINED, with the census as the
evidence.** The body is an enum-keyed dictionary lookup
(`(typeof(enum), flag, dict, key)` → a cached entry; 292 bytes; a
16-way jump table over the enum's underlying byte, recursive through
`[obj]` for nullable wrappers, callees `0x1807eb070` /
`0x1807eeed0` / `0x1807efe10` all unnamed). Naming it would change
nothing a reader sees, because **3,647 of its 3,735 site lines
(97.6%) consume the result as a raw pointer field store** —
`((byte*)objN + 0x20)[0] = unknown;` — i.e. the gap is C2's raw-offset
field resolution, not the callee's name; the remaining 88 are 48
unclear, 38 managed-ish, 2 other-shape. Per the decline-by-default
rule the address keeps its honest `sub_`, and the payoff is filed
under C2.

## Current work: fix 155 — the `_` placeholder becomes `default` at render time (2026-10-26, on `main`)

**`_` is CS0103 in an ordinary argument list.** The lifter uses `_` as
its internal "this slot rendered to nothing" sentinel, and it is the
right tool internally: every trim (`while out[-1] == '_'`), every tail
path and every shared-body arity proof compares against it. But it
reached the OUTPUT too, where C# 8 discards cover only out-arguments
and declarations -- `FixedString.Format(..., _)`,
`obj5.SetProperty<int>(_, _)`, `GetComponentsInParent(_, _)` are all
compile errors. 235 such lines in the UI image alone.

**The fix is placement, not the sentinel.** `Lifter._render_args`
maps `_` to `default` and every render point uses it: `_call`'s final
`call =` line and its vtable fallback, the three `cand =` receiver-fold
sites, `insn.py`'s resolved-call and tail emit, and `analyze.py`'s four
mirror sites. `default` is legal anywhere and states the same thing
honestly. An earlier attempt that changed the sentinel itself was
reverted: it broke the trims.

**Validation.** Portable 1,428 (+1: the helper's mapping, including
the empty list); game **1,462 passed / 2 known env failures / 1
xfailed, failure SET byte-identical to fix-154, zero pin moves** --
after two test assertions that had pinned the old spelling were
updated (`test_tail_calls` expecting `_`, and fix 147's two
`TryGetValue(x, _)` ground truths, which now read
`TryGetValue(x, default)`). Paired `--only UnityEngine.UI`
(defaultpost3 vs the fix-154 tree, 981 files / 12,249 bodies both
sides): illegal `_` argument lines **235 -> 0**, brace 0, compile gate
flat at 50,529 (the placeholder was a binding error, not a syntax one,
so the syntax tier cannot move).

## Current work: fix 154 — the class-init fast path onto the allocator (2026-10-26, on `main`)

**`0x180002de0` is the class-init fast path** (14 bytes, **1,543
sites**): `cmp dword [rcx+0xE4],0; je <alloc>; ret` -- an
already-initialized klass returns immediately, otherwise the
allocator runs. The `je` target is 0x1807933d0, the `il2cpp_object_new`
the census already names, so naming this entry the same routes its
sites through the existing fold: `new Func_1<Delegate>()` instead of
`sub_180002de0(...)`.

**Two guards beyond the byte template.** `function_extent` is chunked
in this fixture (4,096-byte blocks), so the proof is the 9-byte prefix
through the `je` opcode plus the trailing `ret`, decoded as exactly
`cmp` / `je rel32` / `ret`. The same bytes also occur once INSIDE a
jump-table body (off a function boundary, not 16-aligned, preceded by
table data), so a second gate requires the entry to be 16-aligned or
to directly follow `ret`/`int3`/`nop`. The `je` must also land on a
known allocator (`rt_alloc` or the `rt_allocs` family).

**Validation.** Portable 1,428 (+1: the 14-byte body); paired
`--only UnityEngine.UI` against the fix-153 tree (fastpathpost, 981
files / 12,249 bodies both sides): **3 files, 514 `sub_180002de0`
lines removed**, 2,454 added (typed `new Func_1<Delegate>()`
allocations and their temp renumbering), brace 0, compile gate
**50,532 -> 50,529 (syntax flat at 17)**.

## Current work: fix 153 — value-type boxing, found by structure because the symbol is absent (2026-10-26, on `main`)

**`0x1807e3960` is the value-type BOX helper** (41 bytes, **8,554
sites**). `cmp dword [rcx+0x28],0` tests the klass's valuetype flag,
`jl` returns the reference path as-is, otherwise the body falls
through to the box slow path. The managed shape is
`(object)(value)` for a `(klass, &value)` call -- exactly what the
existing `rt_value_box` fold already rendered.

**Why it was never found: the fold looked only at exports.**
`rt_value_box` was `next(va for va, nm in b.exports.items() if nm ==
'il2cpp_value_box')`, and this fixture exports no such symbol, so the
fold's `target == rt_box` gate could never match. Recognition is now
structural (byte-exact 41-byte template, unique in .text), and the
fold accepts `name == 'il2cpp_value_box'` as well as the export.

**Validation.** Portable 1,427 (+2: the `(object)(num4)` fold and the
41-byte body); ground truth (EGOGiftAbility, mi 98334) renders
`string.Format("EGOGiftAbility_{0}", (object)(num4))` -- the source
shape. Paired `--only UnityEngine.UI` against the fix-152 tree
(boxpost, 981 files / 12,249 bodies both sides): 71 files changed,
**182 `sub_1807e3960` lines removed**, 289 `(object)(...)` casts
added, brace 0, compile gate **50,539 -> 50,532 (syntax flat at 17)**.
Every changed line is a target shape (`string.Format(..., (object)(x))`,
`((object)(color1)).GetHashCode()`, `((object)(num1)).getClass()`).

## Current work: fix 152 — the parameterless init wrapper, and why it must NOT reuse the census name (2026-10-26, on `main`)

**`0x18078c0b0` is the no-argument entry of the runtime-metadata
initializer** (19 bytes, 2,849 sites): `sub rsp,28h; call <init>;
lock or dword [rsp],0; add rsp,28h; ret`. Template byte-exact with the
call rel32 as the only wildcard; unique in .text.

**First attempt was wrong and the paired diff caught it.** Naming it
`il2cpp_codegen_initialize_runtime_metadata` (the census name) routed
the sites through the existing elision, which *propagates the RCX slot
value into RAX* -- correct for the one-argument entry that reads a
metadata slot, **wrong here**: this wrapper takes no argument, so RCX
is register residue. The first build leaked that residue into
downstream expressions (4,195 added lines with shapes like
`float real3 = real2` appearing near the changed sites). It got its
own name, `il2cpp_runtime_init_meta_void`, with a drop-only arm in
`_call`: registers are cleared and RAX goes unknown, nothing travels.

**Validation.** Portable 1,425 (+1: the 19-byte body). Paired
`--only UnityEngine.UI` against the fix-151 tree (initpost2, 981 files
/ 12,249 bodies both sides): 70 files changed, **242
`sub_18078c0b0` lines removed**, brace 0, compile gate **50,542 ->
50,539 (syntax flat at 17)**. The normalized net change is all
positive: the stale `object objN = sub_1807e3c60(x, typeof(Type))`
probes (results unused) and their `if (x != null)` wrappers disappear,
while `as` folds land (`Action_2<int,float> action23 = delegate1 as
Action_2<int,float>`, `INotifyBindablePropertyChanged`,
`ICanvasRaycastFilter`) and a stale `x = x.layoutPriority` reads
`layoutElement1.layoutPriority`. Checked and cleared as pre-existing,
not caused here: the 49 `real3 = real2` lines exist identically in the
fix-151 baseline tree.

## Current work: fix 151 — element LOAD + the isinst family's second build (2026-10-26, on `main`)

**`0x180010df0` is `il2cpp_array_getref`** (56 bytes, 7,484 sites):
`cmp edx,[rcx+0x18]; jae` then `mov rcx,[rcx+0x10]` (the vector one
hop down -- the multi-dim/nested layout), a second OOB guard on it,
then `mov rax,[rcx+rax*8+0x20]`. Managed shape: `array[index]` as a
VALUE, rendered in place so the result keeps flowing through the
ordinary value path. Byte-exact template with the three jae rel8s and
the three fail-call rel32s as wildcards; verified UNIQUE in the
fixture's whole .text.

**The isinst recognizer was pinned to one build.** `_is_isinst_helper`
required a 21-byte literal prefix with the register spills at
`rsp+10h`/`rsp+18h`, and **none of the fixture's three isinst-family
addresses matched it** -- including 0x180479f80, which the docstring
called ground truth. `0x1807e3c60` (177 bytes, **10,696 sites**) is
the same function compiled with the spills at `rsp+8`/`rsp+10h`. The
recognizer now checks the prologue SHAPE (two spills, `push rdi`,
`sub rsp,20h`, `mov rbx,rdx; mov rdi,rcx`) with the spill slots as a
two-value alternation, plus the result plumbing (`cmp rbx,[rip]` and
`cmove rax,rdi` exactly once each, and the assignable probe -- the
indirect `call [rax+10h]` or the direct call this build uses). The
existing `as` fold in `_call` then renders
`System.IDisposable disposable1 = enumerator2 as System.IDisposable;`
with no new naming logic.

**Validation.** Portable 1,424 (+3: getref index fold, getref decline,
the three helpers' arities are distinct); per-caller re-lift across
the UI image: **32 of 35 isinst callers fold to `as`**, 3 keep the
honest call (4-arg spray / non-typeof klass shapes). Paired
`--only UnityEngine.UI` against the fix-150 tree (getrefpost, 981
files / 12,249 bodies both sides): 29 files changed, **65
`sub_180010df0` + 7 `sub_1807e3c60` lines removed**, 118 indexed
element reads added, brace 0, compile gate **50,549 -> 50,542
(syntax flat at 17)**. Bonus shapes in the same delta: raw
`((byte*)((byte*)obj + 0x0)[0] + 0x1c8)[0]()(...)` vtable calls become
`list13[num1].getClass()` / `/*vtable slot 9*/ list13[num1](...)`,
and a store helper's `sub_180010df0(list11, num4, ...)` becomes
`if (list11[num4] != null)`.

## Current work: fix 150 — the null-check helper; 10,136 guard statements vanish (2026-10-26, on `main`)

**`0x180002df0` is `il2cpp_null_check`** (20 bytes, **10,136 call
sites**). The entire body is `sub rsp,28h; test rcx,rcx; je +5;
add rsp,28h; ret; call NullReference; int3` -- an argument guard with
no other effect, and **C# has no spelling for it** (null checks are
implicit). The correct render is therefore to DROP the statement and
leave the registers flowing; the checked value is untouched.

Recognition is the 15-byte prefix through the call opcode plus the
trailing `int3`, with the NullReference rel32 as the only wildcard.
The same 20 bytes occur once at a real method entry (0x185f461e0) and
the `addr_candidates` guard excludes it, leaving 0x180002df0.

**Naming had to become lazy.** The first wiring put the check in the
`_init_runtime_ids` census loop, which only walks the hot-target
sample (Assembly-CSharp) -- and this helper serves other images. The
site census caught it: StaticDataManager.LoadStaticDataFromJsonFile
still had 151 null-check lines after that change. `_array_addr_name`
(the existing memoized lazy prober that `_call_name` consults for
every otherwise-unresolved target) now also proves the element-store
and null-check helpers, so coverage no longer depends on which image
was sampled.

**Validation.** Portable 1,419 (+2: the exact body bytes and the two
RT_ARITY rows, plus the drop leaving no statement); ground truth:
StaticDataManager.LoadStaticDataFromJsonFile (mi 118470) goes from
**151 null-check lines to 0**. Paired `--only UnityEngine.UI` against
the fix-149 tree (nullpost, 981 files / 12,249 bodies both sides):
5 files changed, **340 null-check lines removed** (339 call sites + 3
stub-file lines; the helper's `__SharedBodyStubs` entry disappears
entirely), brace 0, compile gate **50,552 -> 50,549 (syntax flat at
17)**. Two side effects, both improvements: 32 declarations whose
`object` was a stale lane now carry the real struct type
(`Length obj158`, `BackgroundRepeat obj207`, `MaterialDefinition`,
`Ratio`) because dropping the guard restores the phi merge's type
proof, and the rest of the 1,127 added lines is temp renumbering
(declaration blocks shift once the guards are gone).

## Current work: fix 149 — the element-store helper; collection initializers recover (2026-10-26, on `main`)

**`0x180002950` is `il2cpp_array_setref`** (102 bytes, **15,453
call sites** tree-wide): unsigned `cmp edx,[rcx+0x18]; jae` OOB guard
(Il2CppArray SZARRAY layout -- length at +0x18, vector at +0x20), then
`mov [rcx+rdx*8+0x20],r8`, then the GC write-barrier cmpxchg loop over
the bitmap cell, returning a bitmap word. Recognition is a byte-exact
template with the two RIP displacements and the barrier call rel32 as
wildcards, derived programmatically from the real body and verified
**unique across the fixture's whole .text**; `RT_ARITY` trims it to 3.

**Two source shapes, and the dominant one was being destroyed.** A
sampled census of 8,110 sites: **8,104 are expressions**
`il2cpp_array_setref(new T[n], <literal i>, v)` and only 6 are plain
statements. That ratio is the signature of a **collection
initializer**: `new T[] { v0, v1, ... }` compiles to one allocation
plus constant-index stores, then the array is consumed as a value.
Rendering each store as its own `object objN = sub_...(...)` (the old
shape) re-allocated the array once per element and invented a value
from the barrier word. Now:
- an inline `new T[n]` accumulates its literal-index stores on the
  array Expr (`_arr_inits`) and `_materialize` renders the whole thing
  as `new string[6] { "...", obj23, "\n", ... }` -- one allocation,
  source-level shape;
- a store on an already-hoisted array (`_array_allocation` gave the
  `new T[n]` its own temp) still renders `arr[i] = v;` as a statement;
- a variable index or an unreadable receiver declines to today's
  honest call shape.

**Validation.** Portable 1,417 (+6: statement fold, bitmap return goes
unknown, no per-element re-allocation, unreadable receiver declines,
initializer accumulation across two stores, variable index invents
nothing); game +2 ground truths (OnGotHash renders
`new string[6] { "Code hash differs...", ... }` with no
`sub_180002950`; Clone has none left). Sampled re-lift of 120
site-owning callers: **0 still contain `sub_180002950`**, 331 array
stores/initializers rendered. Paired `--only UnityEngine.UI`
(setrefpre/setrefpost, stash-proven, 981 files / 12,249 bodies both
sides): 99 files changed, **648 `sub_180002950` lines removed**, 82
collection initializers + 272 element-store statements added, brace 0,
compile gate **50,559 -> 50,552 (syntax flat at 17)**. Every changed
line is a target shape -- no renumbering-only or unrelated edits.

## Current work: fix 148 — the alloc-helper family; the 5,845-site delegate族 collapses (2026-10-26, on `main`)

**Root cause: a single-slot classifier on a multi-entry helper.** The
helper census (`state.py`, klass-argument call shapes) kept exactly ONE
address in `rt_alloc` (`if self.rt_alloc is None`), so the fixture's
second klass-argument allocator -- `0x1807e3d20`, the class-init
wrapper around the same allocator (1,226 klass sites, 99.7% klass
ratio) -- never entered the fold. Its sites rendered
`object objN = sub_1807e3d20(typeof(T))`: an UNTYPED `object`, which
then blocked every downstream proof.

**The blocked population was the tree's largest single family.** The
5,845 sites at `0x1811cce50` are 30 delegate `.ctor/2` candidates
(Action/UnityAction/DelegateEvent/ThreadStart...), and every one is
built as `sub_1811cce50(obj, target, X.Y_handler)` where `obj` came
from that untyped alloc. With the alloc typed, the EXISTING delegate
arm (`recv.ty` -> delegate `Invoke` -> `.ctor/2` -> bound-method owner)
completes on its own -- no new naming logic was needed. Ground truth
(ObscuredFilePrefsExamples.Start, mi 311171):

    object obj21 = sub_1807e3d20(typeof(Action));
    sub_1811cce50/*shared body, 30 candidates*/(obj21, this, ...OnNotGenuine...);

becomes

    System.Action action1 = new System.Action(this.OnNotGenuineDataDetected);

Second, independent unlock: an inlined `List<T>.Add` fast path reads
its fields through the now-typed receiver, so
`((byte*)__addr(list11) + 0x1c)[0]` becomes `list11._version` /
`list11._size` / `list11._items` (the C2 field-resolution shape,
arriving for free). The remaining `sub_180002950(list11._items, ...)`
is that family's own next slice.

**Implementation.** `rt_allocs` (the complete klass-argument family;
`rt_alloc` keeps first-seen for consumers that only need one) and the
`_call` fold tests membership. Three lines of classification change,
zero new naming machinery.

**Validation.** Portable 1,413 (+3: both family members fold to
`new System.Action()`, a non-family helper keeps the honest fallback);
game **1,444 passed / 2 known env failures / 1 xfailed — failure SET
byte-identical to fix-147, zero pin moves**. Ground truths: delegate
ctor renders `new System.Action(...)` twice with no
`sub_1811cce50`/`sub_1807e3d20` left (mi 311171); the typed allocation
unlocks `list11._size`/`_items` (DeserializeProductDescriptions). One
test needed loosening, not re-pinning: `test_dungeon_progress_clone_
copies_every_list` asserted hard-coded temp numbers (`list11`,
`list17`, `list112`); the body there went **79 lines -> 28** as every
`(List<T>)sub_1807e3d20(typeof(...), this, obj2, obj3)` +
`listN.ctor(src)` + `&__ret.X >> 12 & 63` barrier residue collapsed
into one `new List<T>(src)` per field, so the assertions now name that
shape and the fields, never temp numbers. Paired
`--only UnityEngine.Purchasing.Stores` (allocpre/allocpost,
stash-proven): 76 files changed, **640 `sub_` lines removed**, 110
`new <DelegateType>(...)` lines added, brace 0, compile gate
**6,366 -> 6,326 (-40, syntax flat at 0)**.

**Not a regression (checked).** A full-suite run under load reported
10 failed + 7 errors; the 7 errors were child-process/temp-tree
contention in `test_missing_method_bodies.py` / `test_validation.py`
(both pass standalone: 15/15), and the 10 included the temp-number
test above plus the 2 env failures. The clean re-run is the record.

## Current work: fix 147 — shared-body identity from the MethodRef pointer walk; C1 step 3 closed as unsound (2026-10-26, on `main`)

**The registration-name hazard (probe, decisive).** C1 step 3 planned
to resolve shared generic bodies by matching the receiver's closed type
against candidate class instantiations. Implementation + live census
DISPROVED the premise: this fixture's registration pairs wrong method
names onto shared bodies. Ground truth (full disassembly): the bodies
at 0x183c23bc0 (21 Remove specs, K=object) and 0x1857f89d0 (6 Remove
specs, K=int) are **pure-search FindEntry code** — every path converges
on `mov eax,ebx; ret` (entry index, zero mutation) — while the callers
use the result with int semantics (`test eax,eax; jns`,
`shr eax,1fh`). 0x1808cda40 hosts 4 different methods × 204
instantiations on one `xor eax,eax; ret` body. A receiver-matching arm
built with every planned guard (per-declaring-TypeDef name+arity
unanimity, exact class-inst key match, unanimous render) fired 470
times across 1,727 site-owning callers and **~445 of those were
provably wrong** (all Dictionary.Remove-family). The arm was reverted
whole; the exact-inst guard only excludes the mismatched
instantiations (string/enum receivers vs K=object canonical rows), and
this game does have `Dictionary<object,X>` receivers. Rule going
forward: a registered candidate name is NEVER identity proof for a
shared body on this fixture; only the runtime's own identity is.

**fix 147: the identity pointer walk (C5-lite).** At these sites the
caller inlines the SOURCE method's core (ContainsKey/TryGetValue
inlining FindEntry; Add inlining its grow path) and calls the shared
helper body, passing the identity MethodInfo* through a short walk
rooted at a lazy MethodRef cell: `mov rax,[rel cell]; mov rcx,[rax+
0x20]; mov r8,[rcx+0xC0]; mov r8,[r8+0x70]`. The existing
`decode_slot` decodes the root cells (kind 6) to the SOURCE-level
call — verified: `0x1890771c8` → `Dictionary`2<string,bool>.
TryGetValue`, `0x1890771e8` → ContainsKey, `0x1890a81d0` →
`List`1<ObscuredInt>.Add` (the ActionSlotDetail Add-slow-path site
whose callee spec is a registry-missed sharer). Implementation:
`Expr._usg_root` (new slot) — `_read_mem_raw` propagates a base
expr's `_usg_idx`/`_usg_root` onto every plain `[base+off]` deref
(source code never derefs a method-group value, so any such deref is
identity plumbing); `_usg_walk_identity` + a `_call` arm seat the root
at any shared-body call whose spray carries exactly one distinct root,
dropping the plumbing argument. The root outranks every registered
name — it is what the runtime itself receives.

**Validation.** Ground-truth `--mi` lifts: DestroyPart (110185)
renders `this.parts_Breakable.ContainsKey(text1)` /
`TryGetValue(text1, _)`; HasKeyword (1817) renders
`this._keywordDic.TryGetValue(keyword, _)`; ActionSlotDetail ctor
(104984) recovers the nine-element `list11.Add(...)` chain (b21:
`object objN = sub_1842e7380(list11)` ×9). Batch re-lift of all 1,727
site-owning callers: **3,876 walk fires**, every rendered name the
expected source-level call for its receiver's instantiation
(TryGetValue/ContainsKey/Add/get_Item across ~300 instantiations),
remaining honest `sub_` markers on the 12 tracked VAs down to 14
lines. Portable 1,410 (+6: slot default, walk-identity
resolve/decline×2, E2E call, no-candidates fallback); game 1,439
passed / 2 known env failures / 1 xfailed — failure SET byte-identical
to fix-141, **zero pin moves**. Paired `--only Unity.ProBuilder`
(c5pre/c5post, stash-proven): 30 files changed, 219 `sub_/*shared
body*/` lines removed vs 221 resolved-call lines added (the rest of
the 5,178-line delta is temp renumbering), brace 0 unbalanced,
compile gate **9,774 → 9,750 (-24, syntax flat at 8)**. Known shape
changes, both honest: unused pure `get_Item` reads drop as dead code
(EdgeLookup: the pre-render's `bool flagN = (bool)sub_...(lookup,
cur)` captures were fake-bool lies over an inlined-ctor indexer read),
and the delegate-construction raw-store sequence
(`func23+0x10/0x20/0x28 = methodPtr/target/methodInfo`) becomes
visible where the phi-collapse used to eat it — that family's sugar
is C1 step 3d.

## Current work: fix 146 landed — the Type.GetType(string) helper, C1's ctor-family decomposition (2026-10-25, on `main`)

**The ctor-as-value census decomposed (probe, no build).** The C1 entry
census's "~5,520 ctor-as-value lines" split under a paren-matched tree
scan into three very different families: (a) **213 sites of the
Type.GetType(string) native helper** `sub_18078cf40` — no metadata
candidates, not exported — called as (RCX=assembly-qualified type
name, RDX=dead slot, R8=caller's MethodRef context), result
user-cast to `Type`; the `.ctor`/`EnablePostProcessing` context args
that named the census are these sites' R8 plumbing; (b) **2,636
mi-pointer-walk lines** (1,649 files): `[mi+0x20]→+0xc0→+0x10→
+0x135` chains — the inlined generic delegate-creation + class-init
walk through a MethodRef cell value, which is C5's inlined
class-init family, not callee naming; (c) the rest are already-
resolved `this..ctor(...)`/`base..ctor(...)` calls (benign).

**fix 146 (landing-9 style).** `_is_type_gettype_helper`: a 51-byte
head template with two wildcards (RIP displacement + call rel32),
programmatically derived from the real body (the hand-transcribed
first attempt had two byte errors — 4C vs 49 REX — the recurring
lesson: never transcribe, always dump). The template is UNIQUE in the
fixture's whole .text (one hit). `rt_type_gettype` + `rt_names` mark
it; `_call`'s special case renders `System.Type.GetType(arg0)` —
arity one: the ABI's RCX is the name, RDX is overwritten by the
exception-out zero-store before any read (dead), R8 is the hidden
context. The result is stamped with the real `System.Type` type tuple
(`_system_type_ty`, memoized one-pass lookup), so the local declares
`System.Type type1 = System.Type.GetType(text2);` instead of
inheriting the stale string/object lane.

**Validation.** `--mi` lifts of both ground truths: AcquiredEgoGift
ctor (mi 98337, 5 params) renders `System.Type.GetType(text2)` /
`System.Type.GetType("EGOGiftAbility_Normal")`; DemoCamera.
EnablePostProcessingForURP (mi 314868) renders the literal
assembly-qualified name. Portable 1,404 (+5 template tests incl.
wildcard and decline-registered-body proofs); game suite green with
2 new ground-truth tests. Paired-build proof deferred to the next
Assembly-CSharp paired rebuild (the 213 sites live mostly there;
a 40+ min pair is not proportionate per the build policy — the
failure-SET gate plus the pinned --mi proofs carry this slice).

**C1 after 145+146.** Remaining addressable: the 2,636-line inlined
class-init/delegate walk (C5 family, needs the walk-shape decoder),
and the ~38k no-identity shared markers (receiver/type arms, C1
step 3).

## Current work: fix 145 landed — C1's first slice, hidden-MethodInfo tail slots (2026-10-25, on `main`)

**C1 step-0 census corrections (probe, no build).** The roadmap's C1
entry guess ("hidden `MethodInfo*` names the true callee at RDX/last")
needed three ground-truth corrections on the v39 corpus. (1) The
`data_NNN` cells at shared-body call sites are NOT metadata cells —
`va2off` is None (BSS, runtime-filled); the actual metadata cells are
the **named MethodRef slots** the project already decodes
(`Dictionary_2<Type, ITweenPlugin>.Clear`, `Enumerable.Where<Type>` —
tree-wide census: only 4 sites carry a `data_` arg, ~225 carry a
named `Type<...>.Member` identity arg). (2) The 38,085-site
population is dominated by **generic shared bodies**: `addr_candidates`
rows are `('generic', spec)` pairs from `generic_method_pointers`
(e.g. 0x183c16050 = 205 specs), so the `_call` identity arms were
never the bottleneck for them. (3) The upstream "dec direct-tail
bypass" hypothesis is CONFIRMED: tail jumps assemble their own spray
in `insn.py` and resolve through `_tail_hidden_generic`, which used to
require the identity to be TRAILING — dead GPRs after the identity
declined it.

**fix 145 (the ABI-slot proof).** IL2CPP passes a shared generic
body's callee identity (the method's own MethodInfo, from a lazy
MethodRef usage slot) at a FIXED ABI position: one GPR slot past the
declared argument slots (hidden sret buffer + receiver + non-float
params; floats ride XMM and take no GPR slot — the same
classification `_shared_slot_classes` uses). New
`_methodinfo_slot(spec)` computes the slot; `_tail_hidden_generic`
accepts an identity sitting exactly there even when stale written
spray follows it (a stale cell landing on that precise slot would be
a coincidence the ABI forbids; slots ≥ 4 are stack homes the GPR
spray can never show, and decline). The resolved spec then flows the
existing fix-94 machinery: `_tail_generic_call` → `_tail_method_args`
positional rebuild → signature trim → receiver fold.

**Validation (paired partial builds, per the build policy).** Paired
`--only DOTween` rebuilds (stash/pop, otherwise identical): the pure
fix-145 delta is **2 files**. `PluginsManager.PurgeAll` (mi 294568)
tails `Dictionary`2<Type,ITweenPlugin>.Clear` with two dead GPRs
behind the MethodRef: now `PluginsManager._customPlugins.Clear();
return;` — and the entire phi spray chain that fed the old unresolved
call (tweenPlugin1..13 + the GC write-barrier residue
`&PluginsManager._xPlugin >> 12 & 63` guards) dies with it, 41 lines
→ 18; `__SharedBodyStubs.cs` drops the 0x183c16050 stub (its only
reference in the image resolved). `RenderPipelineChecker.GetTypesSafe`
(mi 314901, Assembly-CSharp side) resolves its `Enumerable.Where<Type>`
tail (`--mi` lift proof). Zero regressions: every changed line in the
paired diff is the PurgeAll simplification or the stub deletion.
Portable 1,399 (+4 tail tests); game 1,423 / 2 env / 1 xfailed (after
fixing my new GetTypesSafe test's own params bug — its first run
matched 0 rows because GetTypesSafe takes 1 param, not 0), failure
SET byte-identical to the fix-141 state, **zero pin moves**. Two new
game tests (`tests/test_game_fix145_tail_methodinfo.py`) pin the two
ground truths.

**C1 residual (next slices).** The 225 direct-identity sites beyond
DOTween (mostly Assembly-CSharp: `List_1<T>.RemoveAll`,
`Enumerable.Any/Where` tails) are validated but not yet in a build —
the paired DOTween probe only covers its own image; the Assembly-
CSharp side gets its paired rebuild in the next C1 slice together
with the ctor-as-value family (~5,520 lines). The ~38k remaining
shared markers are dominated by shapes whose identity is NOT in the
spray (all-candidate registry rows with no MethodRef argument) —
those need the receiver/type arms, which is C1's step 2.

## Current work: b21 salvage + Stage 1.5 landed + fix 144 found (2026-10-25, on `main`)

**v39b21 postmortem.** The full rebuild (source `88e2373`) HUNG at the
final pool-consumption phase: the mid-session software restart lost one
pool task — workers idle at the task queue, parent waiting forever on
the future at `cli.py:332` (py-spy dump, 2026-10-25). Killed at ~7 h.
Salvage: the 36,330-file partial tree (99% of type files, 0 of the
per-assembly stub tails) gated with `tools/gate_tree.py`:
**648 errors (syntax 541 + binding 107)** vs b20's 65,939 — the
else-family collapse (65,890 → ~599 residual) is fix 143's effect seen
tree-wide, and the residual is a DIFFERENT, pre-existing defect
(b20 carries the identical broken shapes).

**fix 144 (found, not yet fixed).** The residual `if (c) { else if ...}`
shapes: 40 sites / 14 images. Root cause narrowed by pass-trace at
mi 119627 (`BattleMapSwitchUtility.ResolveMapId`): the multi-if chain
fold's output is VALID C# (`if (X) {} else if (A) {} else if (B) {}`),
and a LATER arm-swap pass (condition inversion `< num4` → `>= num4`
with arm promotion) moves the else-arm's chain into the true arm
WITHOUT stripping the chain heads' `else` prefix. Pre-existing (b20
has the same shapes — drowned in the 13k peephole noise until now).

**Build policy (user call 2026-10-25): no more full builds except
promotion milestones.** Validation = paired `--only` rebuilds (minutes)
+ `--mi` lifts (seconds) + metadata-level probes (no files) +
`gate_tree` (52 s, needs only a built tree). A fresh full rebuild is
deferred to the next promotion.

**Stage 1.5 landed (`54480f8`).** The state-machine note claims the
honest kind from the typedef's own interface list (binary truth — the
attribute-table decoder the plan assumed necessary is not needed):
metadata-level census 1,863/1,863 classified, 0 declines (1,052 async
+ 811 iterator). ACTk paired rebuild: 3 async + 7 iterator notes, ZERO
neutral residue, 0 non-note line changes; brace 0. Portable 1,390
(+3); game 1,412 / 2 env / 1 xfailed, failure SET byte-identical,
zero pin moves. C9 is thereby CLOSED as delivered: identification +
honest kind labels; stages 2/3 declined with the probe-C evidence
(docs/plans/2026-10-21-async-state-machine.md §2.3/§2.4); the
machine-specific residual (666 bodies with an unclosed `TAwaiter`
generic declaration) is tracked in the C8 family.

**fix 144 landed (`1ab0b84`).** The drop arm in `_render`'s empty-block
walk now declines for ANY else continuation (the bare-else invert arm
is unchanged). mi 119627 fresh lift: zero orphans, the chain intact
inside the promoted arm. Paired System.Data rebuild: orphans 3 → 0,
else quintet gone (syntax 16 → 1 — the 1 is a pre-existing CS1750
`int`-default-for-`DataRowAction` declaration item, a C-family
residual). Portable 1,395 (+5); game 1,417 / 2 env / 1 xfailed,
failure SET byte-identical, zero pin moves. **Methodology caveat
(correction to the 648 figure below): csc suppresses binding
diagnostics while syntax errors exist, so the b21-partial 648 was a
parse-tier LOWER BOUND — the true binding tier needs a syntax-clean
tree (promotion-milestone item).** With fix 144 landed, the parse
tier's else-family floor is gone from the source side; the next full
rebuild (promotion time) will measure the real tier-0 baseline.

## Current work: b20-local gate + fix 143 — the else-if peephole was parse-broken on v39 (2026-10-25, on `main`)

The b20-local baseline (`out/limbus/v39b20`, source `3f1a1f5`,
`--strict --publicize --raw-addr`, 162 images / 36,765 files /
297,975 bodies / 0 failed / 0 fallbacks, 23,617 s wall; per-image csc
census in `validation_reports/limbus/b20local.roslyn.json`, driver
written for the session, 61 s gate) found **52,785 syntax errors** —
a tier the whole b1-b20 chain had held at zero. Four codes at ~13.18k
each (CS1002/CS1003/CS1026/CS1525) + CS8641 x13,164 (else-cannot-start-
a-block, classified binding by the 1000-2000 rule): ~13.2k broken
lines from `_elseif_flatten_multi` (`c99e579`, the local else-if-chain
peephole, landed 2026-10-21 AFTER the last Roslyn gate, invisible to
the brace audit because the broken shape stays brace-balanced, and
invisible to tree-sitter because that gate segfaults on this box for
whole-image parses). Probe at mi 317598 (`MaterialBehaviour.
ApplyToMaterial`) reproduced it: the fold minted `if (c) { else if
(...) ... }` — an orphan else head INSIDE a block, with a dropped
closing brace.

Two holes in `_chunk_is_liftable` (`il2cpp/dec/flow.py`): the depth
tracker only updated while depth==0 (a chunk never closed in the
tracker, so an else tail inside a chunk was never seen), and a
statement between two ifs of the else-block (`bool flag1 = target ==
null;` sat between the first and second if) silently joined the
preceding chunk. The tracker now updates on every line and any
non-brace line at depth 0 after the head declines the chunk. Paired
material-timeline rebuild: csc syntax 56 -> 0; diffs read (the
scrambled region returns to its honest nesting). Portable 1,387
passed (+4 tests in `tests/test_peephole_version_independent.py`
pinning the decline shapes and the intended lift); game recount in
flight. Commit `765adb8`.

Binding tier (63,221) is methodology-noisy so far: CS0518 x45,345 is
"no mscorlib referenced" — the per-image census compiles each image
standalone (tools/compile_gate.py semantics, documented
"unresolved externals are expected noise"), while the b1-b20 chain
compiled 10 reference-closed groups. A gate v2 with group/reference
closure is the next session's first item, then the post-143 full
rebuild + re-gate for the REAL b20-local number (projected: syntax ~0,
binding ~50k before the else-fix's cascades).

## Current work: fix 142a — the v39 interface-resolve helper is named, ifaceprune wakes up (2026-10-25, on `main`)

Root cause found while probing the fix-138 "interface-offset-table scan"
next-slice candidate (`docs/plans/2026-10-25-todo-roadmap.md` P1-1): fix
139's `ifaceprune` gates on the miss-call helper being NAMED
(`names.get(target) == 'il2cpp_interface_get_method'`), and the name comes
from `_is_iface_resolve_helper` (`lifter/state.py`) — a byte template
pinned to the 2022-fixture helper (exact prologue, exactly 4 `call rel32`,
0x89 extent). The v39 runtime's helper at 0x180789290 (Unity
6000.3.12f1) is a different codegen entirely (eight pushes, 0x1aa extent,
13 internal calls), so the template failed, the name never fired, and
**ifaceprune was blind on every v39 build**: 3,240 for-head scan lines in
1,146 files, 3,434 unnamed `sub_180789290` calls, 0 named. The landing:

- `il2cpp/lifter/state.py`: `_is_iface_resolve_helper` tries the 2022
  template first, then `_is_iface_resolve_helper_v39` — ground truth
  0x180789290, pinned 30-byte prologue (pushes + frame + slot movzx +
  iface/object saves + klass deref), the `test byte [klass+0x136],0x10`
  initialized-flag invariant (same displacement as 2022), the
  `cmp [obj+0x10],rax` hit compare, and the
  `movzx r8d,r14w; mov rdx,rbp; mov rcx,r13; call rel32; int3` resolver
  tail. R9 never read in the v39 body (full disassembly), so the 4th
  arg is still fast-path spray and arity-3 naming carries over.
- Naming lights three systems at once: the arity trim (spray 4th arg
  dropped), fix 139's ifaceprune (scans pruned), and the landing-8
  managed dispatch fold (`Expr._ifm` → `recv.I_Member`).

Native-verified renders (post-fix `--mi` re-lifts): mi 290837
`BuildHashes.PrintToConsole` renders `enumerator12.MoveNext()` and
`FileHash fileHash1 = enumerator12.Current;` — slot 0 and slot 1 both
named correctly with the `FileHash` element type closed from
`IEnumerator_1<FileHash>`, which is also the empirical proof that the
R8 argument is the method slot on v39 (the roadmap's 142b question —
resolved affirmatively; MoveNext/Current would swap if R8 were read
wrong). mi 1816 `AbilityBase.SetKeywords` renders
GetEnumerator/MoveNext and `obj42?.Dispose();` with no scan residue.

Paired image rebuild (`--only ACTk.Runtime`, pre = `out/limbus/v39b20`
vs post = `out/limbus/v39b20-post142`, same gate flags, brace 0
unbalanced both sides): 6 files changed, net -281 lines, every changed
file a scan-bearing file; post census has **0** for-head scan lines and
**0** `sub_180789290` calls (pre: 3,240 / 3,434 tree-wide). Diff read
line by line on ProgressExtensionMethods (33 lines of count read +
count test + helper call + for-head scan + 0x138 fold + indirect
`call [entry]` collapses to 3 lines ending `progress.Report(filesProgress1);`)
and spot-checked on PrefsSerialization (`IObscuredFilePrefsSerializer`
typed var + named Serialize/DeserializePrefsDictionary). Known nit, on
a degenerate site only: a null-receiver dispatch (receiver literal 0,
pre: `sub_180789290(0, typeof(IDisposable), 0, ...)`) now renders
`IDisposable.Dispose(0);` — the receiver demoted into the argument
list; both spellings are uncompilable, the post one reads better.
Filed as a 142b follow-up nit.

Tests: `tests/test_recovery_followup.py` +3 (v39 template recognized,
three mutation rejections, 2022 template unshadowed — 89 in the file);
`tests/test_game_fix142_iface_resolve.py` +2 (mi 290837 managed
renders with no residue, mi 1816 no residue). Suites: portable 1,383
passed (+3); game recount in flight. b20-local gate tree rebuilt
(`out/limbus/v39b20`, source `3f1a1f5`, `--strict --publicize
--raw-addr`, 36,765 files / 297,975 bodies / 0 failed / 0 fallbacks /
0 emit-failed, 23,617 s wall): the pre-142 baseline the Roslyn gate
runs against next.

## Current work: fix 141 hand-synced from upstream — all-unknown join phis are `_unk` (2026-10-24, on `main`)

Upstream `mynamescrax/il2csharp` `c3195dc` (fix 141, 2026-10-23) applied to
`main` by hand: local diverged after `5291b7c` (fix 140 docs), so the commit
is not mergeable as-is (AGENTS.md / docs conflicts, and the upstream game
test still targets the removed pre-fixture-framework world). Landed:
`il2cpp/dec/analyze.py` +26 (at the pass-2 phi merge, a phi whose every
incoming value is missing or `_unk` is itself `_unk` — guarded by "every
predecessor emitted this pass" so a loop latch's stale dry end_state cannot
falsely unknown a carried value; `_phi_all_unknown` shared with the fix-126
fixed point), the upstream portable test `tests/test_fix141_unk_phi_spray.py`
(3 tests), and `tests/test_game_fix141_unk_phi_spray.py` rewritten on the
local `game("limbus")` framework (upstream's file imported the old
`game_decompiler` + old-fixture mi rows 28594/26440, dead here). Doc
conflicts resolve toward this structure; upstream's gate numbers were
measured on the removed old fixture and do not transfer (b19 454,955 ->
b20 439,578, CS0103 -15,619 — upstream's evidence only).

Mechanism: a cached-function-pointer guard join whose resolve arm clobbers
the volatile registers mints phis the call argument builder printed as
undeclared trailing `objN` arguments (CS0103 at Roslyn). The merge now marks
the all-unknown phi `_unk` and the builder drops it; phis carrying any real
value stay honest.

Local evidence (limbus v39 archive, `--mi` re-lifts pre vs post):

- `FMOD.Channel.setFrequency` 0x18359AED0 (mi 287840): 8 args -> 5,
  undeclared obj20..obj22 dropped (carried obj17..obj19 stay — they are not
  all-unknown). Steam interface-pointer shared body 0x183473B70 (mi 253839,
  `SteamAPI_SteamMusicRemote_v001` sharer): `(this, obj12..obj18)` ->
  `(this)`; the real call takes no arguments.
- Census (temp-dir probe: indirect-call lines whose trailing temps are
  declared nowhere in the emitted file): standing `out/limbus/v39` tree =
  2,213 lines across 521 files (pre-patch population). Paired image rebuild
  `--only Facepunch.Steamworks.Win64` (`fix141-pre` = HEAD vs `fix141-post`
  = worktree, `--workers 8`, 546 types / 4,942 bodies, 0 failed /
  0 fallbacks both sides): 607 sprayed lines in 73 files -> 1 line in 1 file
  (`Ugc/Editor.cs` L845, an async state-machine body whose tail is not an
  all-unknown join phi — the 141b predecessor guard correctly declines it);
  321/546 type files changed, 10,670 lines, all dropped `_unk` args on
  indirect and `sub_` helper calls plus downstream temp renumbering. Brace
  gate 0 unbalanced (`validation_reports/limbus/fix141-post.brace.json`);
  the tree-sitter parse gate segfaults on this box for whole-image parses —
  reproduced identically on `fix141-pre`, environmental, not the fix.
- Suites: portable 1,380 passed (incl. the 3 new). `--game limbus` 1,400
  passed / 2 failed / 1 xfailed — the 2 failures
  (`test_game_compile_gate.py::test_small_image_zero_syntax_errors`,
  `test_game_decl_gate.py::test_decl_gate_end_to_end`) need the
  `Unity.Burst.Unsafe` image, which the standing partial `out/limbus/v39`
  tree lacks; both reproduce byte-identically with the fix stashed (HEAD)
  and pass against the complete `v39-gates` tree — pre-existing, zero new
  failures, zero pin moves (every exact-text body pin green).

Next: the remaining v39 spray sites are carried-value shapes fix 141
declines; upstream continues the same Roslyn-gate program, so re-check
upstream after future local landings.

## Current work: perf — per-type parallel emission + hotspot rewrite (2026-10-21, on `main`)

Context: `docs/il2csharp-jit-feasibility.md` (in `../docs/`) proved a Python JIT
is the wrong lever (CPython 3.13 here ships no JIT; iced-x86 is a C ext at 0% of
runtime; the interpreter share is small and sits on regex/C-API). The real
levers are **parallelism** and **hotspot algorithms**. Plan:
`../docs/il2csharp-opt-plan.md`.

Measured baseline (2026-10-21, current source, Assembly-CSharp one image):
`--workers 4` uses **~90% of ONE core** (7 idle) because `--workers` only split
ACROSS images and AC is one image. Full AC build = **2.98 h / 176,704 bodies**.
Per-method lifting ~128–138 ms; phases `_structure` 37.4% / `_decode` 23.3% /
`_analyze` 21.1% / `_make_blocks` 7.4%; `textpass._mask_line_spans` alone 14.8%.

### Phase A — per-type parallel emission (LANDED 2026-10-21)

`--workers N` now runs ONE pool over per-image, **per-top-type** tasks, so a
single monolithic image uses every core. Every task writes only its own type
file; the per-assembly files (`__SharedBodyStubs.cs`/`__Addr.cs`/`.csproj`) are
written ONCE by the parent from the collected union, so the tree is
**byte-identical to serial regardless of schedule**.

- `emitter.py`: extracted `_emit_one_top` (one top type's file, returns the
  pre-transform `sub_` set + raw flag), `_plan_top_files` (assembly-local
  file-base names, dedup in metadata order — proven identical to the old
  sequential naming across **all 162 images / 36,321 names**), `_iter_top_types`,
  `_assembly_dir_name`, and `write_assembly_tail`/`write_csproj` (the per-
  assembly tail, shared by serial and the pool parent). `write_assembly_split`
  is now a thin serial walk over the same plan.
- `cli.py`: `_worker_emit_types(payload)` (per-type batch; fresh Emitter per
  task over ONE runtime load in `_per_type_init` — isolates per-type caches
  like `_short_ns_idx`/`_us_cache` while loading metadata once per worker);
  `_emit_assemblies` builds the flat job list (`_split_balanced`, contiguous,
  heaviest image first), collects deltas + `sub`/`raw` union per image, then
  writes each image's tail in metadata order. `_worker_count` **relaxes the
  "one image ⇒ serial" rule**; only `--max-methods`/`--bodies` still decline.
- **Evidence**: A-1 refactor byte-identical (1443/1443 files, old-vs-new @
  `--types Dungeon`). A-2 pool vs serial @ `--types Dungeon --workers 4`:
  **1607/1607 paths identical, 0 differ, 0 only-side** (incl. the union
  `__SharedBodyStubs.cs`, every `.csproj`); timing 562 s vs 731 s serial *with
  4× the 37 s metadata load*, and real speedup grows with body count (fixed
  load dominates this small scope; a monolithic AC image has 176k bodies).
  Portable suite 1367 passed (+10: `tests/test_per_type_parallel.py`, plus
  `test_parallel_build.py`'s single-image rule flipped to `(8, None)`).
  ProcessPoolExecutor works in this sandbox here (no EPERM). `testgame/` is
  absent in this checkout, so all `-m game` tests (incl. the real-fixture
  serial-vs-pool byte-identity) skip; my real-Limbus `--types Dungeon` A/B is
  the standing proof.

### Phase B — `_mask_line_spans`/`_mask_literals` precompiled-regex rewrite (LANDED 2026-10-21)

`_mask_line_spans` (textpass) and `_mask_literals` (highlevel) were two identical
char-by-char `while` scans of every rendered line (14.8% of lifting, 4.6M
`startswith`). Both now delegate to one `il2cpp.text.mask_spans` — a single
precompiled regex scanned left-to-right (`//`→EOL, `/* */` with cross-line state,
`@'…'` verbatim, `\`-escape strings, `'…'` chars), same equal-length NUL output,
same `in_block_comment` contract. `textpass._mask_line_spans` keeps its signature
(module shim) so partial test doubles still work.

**Evidence**: byte-for-byte equal to the old char scan on the whole corpus
(5,080,197 lines / 24,781 files, prototype) and re-confirmed committed-vs-real-old
(pulled from git `61dc8db`, 489,895 lines + 30 edge cases, 0 mismatches); build
A/B post-B vs pre-B `--types Utils` 411/411 paths byte-identical; micro-benchmark
1.72× faster on 200k lines; portable suite 1367 passed. Commit `1ed2c2b`.

### Phase C — dynamic `re.*` → `lru_cache` `_rx` factory (DECLINED 2026-10-21, measured)

Idea: 260 literal `re.sub/search/...` sites hit `re._compile` ~1.8e4/method.
A counting-wrapper experiment first showed an implausible "1.61× / 38%"; a
**clean** re-run (no wrapper, warmup + repeat, cold cache each run) showed
`re._MAXCACHE` sizing had **no reliable win** (small 39.9 s vs large 45.6 s; the
"lookup drop" was the wrapper's own per-call overhead — an artifact). So the
hot cost is `re` C-engine matching (`search`/`match`/`sub` are already C), not
recompilation, and `re`'s 512-entry cache is adequate. Rewriting 260 sites for
a not-reproducible single-digit % is not justified — **declined, documented**.

### Full-scale result (2026-10-21)

Full Assembly-CSharp rebuild with A+B, `--workers 6`, on this 4-physical-core
i5-1145G7: **24,783 files / 176,704 bodies / 0 failed / 0 fallbacks in 5,183,552 ms
(86.4 min)** vs the serial baseline **15,010,749 ms (250 min)** = **2.90× wall**;
6 workers delivered 3.42 cores of throughput vs 0.85 serial ~4.0× compute (the
laptop tail / HT caps wall at ~2.9× — a true 8-physical-core box should approach
6–8×). Brace audit 0 unbalanced / 24,781 files. Byte-identity: the tree matches
the serial baseline in file set and body count (24,732 = 24,732; 176,704 =
176,704) — and the 2,144 differing files were proven **100% attributable to two
HUMAN commits that landed DURING the 11:21–16:21 baseline build**, not to A/B:
`ecd9649` (11:51, "drop dead GC cardmark-index fragments") removes exactly the
`X n = (typeof(...).__static_fields & 8589930496) >> 18` lines (2143 files, 2558
lines, every one contains `8589930496` = Boehm card mask, 0 additions, 0
violations), and one `__SharedBodyStubs.cs` reflects the concurrent stub-
annotation commit. By construction the pool is schedule-independent and equals a
serial walk of the same plan (proven at scope level: `--types Dungeon` workers
1==4, 1607/1607).

## Current work: fixes 126-140 compile-gate slices (2026-10-06 .. 2026-10-12, on `main`)

**Fix 140 (2026-10-12, unresolved vtable-slot receivers): a
`/*vtable slot N*/ recv(recv, ...)` site (1,193 at b15) now resolves the
slot through the object the klass was read from. Three receiver
sources, in order, in `lifter/calls.py` VIRT_CALL resolution: (a) the
klass-load object `vt_recv` when arg0's own type names no slot; (b) arg1
when arg0 is the hidden sret buffer (`&objN`) -- accepted only when the
resolved callee really returns through a buffer; (c) a dominating
inlined castclass/isinst hierarchy check, recorded by
`_note_cast_narrow` (`lifter/insn.py`) at `cmp [K.typeHierarchy +
d*8 - 8], typeof(T)` (the throw arms are already elided as noreturn
guards, so the cast was invisible), rendered `((T)x).M()` (ASN1.GetBytes:
`((Mono.Security.ASN1)enumerator1.Current).GetBytes()`). A receiver arg
typed above the dispatch type gets the same `(T)x` spelling. Slots
resolved this way bind at the call (as the unresolved form did; a lazy
render duplicated the call). Also: the sret struct-return fold now folds
parameter / named-local / `arr[i]` / `(T)x` receivers (`node.GetVertex(1)`,
was `TriangleMeshNode.GetVertex(node, 1)` -- CS1501 on every sret
instance call with a parameter receiver, not just vtable ones; also the
ReadSpan / GetBounds goldens: `buffer.Slice(num3)`,
`matrix.MultiplyPoint3x4(...)`). The hierarchy-pointer read in
`_note_cast_narrow` is uncounted (`dict.get`): a counted `regs.get` bound
it to a temp and split the `else if` cast check (mi 7021). Gate b19
vs b15: 457,497 -> 454,955 (-2,542; CS1061 -828, CS0149 -486, CS1501
-422, CS0103 -346, CS1955 -227, CS1503 -139; rise CS0214 +60 = newly
resolved calls exposing raw pointer reads); parse codes unchanged, brace 0; vs
r_base -45.1%. Unresolved vtable sites 1,193 -> 381 (simple 219, slot
None 112, sret 37, member 13). Known nit: a bound narrowed result can
declare `object` (`object obj35 = ((ASN1)...).GetBytes()`, mi 277) though
the bind carries byte[]. Closes the fix 139 follow-up: CS1955
`IEnumerator.Current` 250 -> 23. Tests: `tests/test_fix140_vslot_recv.py`
(4 portable), `tests/test_game_fix140_vslot_recv.py` (3 game: mi 277
ASN1.GetBytes cast receiver, mi 104143 `this.GetFeetPosition()`, mi
105366/105369 sret param / `arr[i]` receivers). Commit 72e3590. Suites:
portable 1,322 passed; game 261 passed / 10 failed = the 8 fix 137/139
pin moves + 2 golden improvements (`mi-11974-ReadSpan`,
`mi-104428-GetBounds`) -- re-pin of all 10 pending user approval.
(Status 2026-10-25: superseded -- the v39 fixture migration (`d1ea2d2`)
rebuilt the golden corpus, and on it the post-141 game suite shows zero
pin moves; the old-fixture re-pin list no longer exists. See the fix 141
section and `docs/plans/2026-10-25-todo-roadmap.md` P0-2.)
Remaining: 381 unresolved vtable sites (simple 219 = receiver type has
no slot and no klass-load object / narrowing; slot None 112), 90 fix 139
d_tail ifaceprune declines, `!(x.MoveNext())` paren cosmetic.**

**Fix 139 (2026-10-11, inline interface dispatch): IL2CPP inlines an
interface call as a scan of the receiver klass's interface table
(`movzx n,word [k+0x12E]`, `mov t,[k+0xB0]`, `cmp [t+i*16],iface` loop;
hit arm folds `k + 0x138 + 16*(offset+slot)`) whose miss arm calls the
resolve helper `il2cpp_interface_get_method(obj, typeof(I), S)`; both
join with the same VirtualInvokeData and `call [entry]`. New
`il2cpp/dec/ifaceprune.py` (called from `lift_method` after
`_prewire_switches`) forces the entry test onto the miss arm when the
scan region is entered only through the test, exits only to miss/join,
holds the 0x138 fold + 0xB0 table load, does no store/call/non-GPR
write, and every callee-saved register it writes is dead at the join
(volatiles are undefined after the miss call); the forced test's
count load + compare join `skip_ips` when nothing else reads them.
Lifter (`lifter/calls.py` `_iface_resolve_target`, `values.py`
`_field_expr`, `Expr._ifm`): the helper result carries slot S of I
(declared method S, class VARs closed from typeof(I), sret/open
returns decline) and `call [rax]` / `mov rax,[rdx]; call rax` render
through the existing `ic_mi` resolved-call path (arity trim drops the
`[rax+8]` MethodInfo). Census: 2,163 of 2,262 helper sites pruned (90
decline on non-copy tails, 9 on entry shape). Tests
`tests/test_fix139_iface_inline.py` (5, fixture bytes + mutations),
`tests/test_game_fix139_iface_inline.py` (mi 26440 Teleport, mi 141
OnStartElement with RDI counter, mi 277 MoveNext via copied entry).
Gate b15 vs b13: 474,095 -> 457,497 (-16,598; CS0019 -7,041, CS1061
-3,438, CS0103 -2,054, CS0165 -1,297, CS0266 -1,279, CS0149 -1,060;
rises CS0214 +148, CS1503 +86, CS1955 +74), zero parse codes, brace 0;
vs r_base -44.8%. Newly visible follow-up: CS1955 `IEnumerator.Current`
(152 at b14) -- an unresolved `/*vtable slot N*/` call on the Current
result renders the receiver text as the callee (`recv.Current(recv.Current,
...)`, ASN1.GetBytes); also a duplicated virtual `GetEnumerator()` when
the result is spilled to a stack slot first (mi 277). Portable 1,318
passed; game 259 passed / 9 failed -> 8 after the fix139 test accepts
`!(e.MoveNext())`: 4 fix-137 pin moves + 4 fix-139 pin moves (iface_resolve
mi 122, interface_dispatch x2 mi 25368/25872, fix131 mi 25872 counter
rename) -- re-pin pending user approval.**

**Fix 138 (2026-10-11, for-head counter declarations; closes the fix 137
blocker): `_for_sugar` folds a counter's entry copy into the loop head
without a type when the counter outlives the loop or its init is not a
literal (`for (num4 = 0; ...)`). When no enclosing scope had declared
the counter, nothing ever did -- a pre-existing class, 11,582 CS0103 on
for-head lines alone in gate b12 (769 files), of which RegistryKey
`num10` (mi 516 FixupPath) was the fix-137-exposed instance.
`_rename_locals` (`il2cpp/dec/highlevel.py`, `forhead_rx`) now emits a
bare `T name;` on the line before such a head (same tracked-type lookup
as a first-use bare assignment; every one of the 3,037 minted decls in
b13 is `int`); `hoist_escaping_locals` lifts it when a read escapes the
block. Already-declared counters and typed heads are untouched. Patch
`work/cg8/patch138.py`; tests `tests/test_fix138_forhead_decl.py` (4),
`tests/test_game_fix138_forhead_decl.py` (mi 24664
ConstrictedInteractable.CheckForCurItem, mi 516). Gate b13 (post-137b +
138, 10/10 groups exit 0, 11,262 files, brace audit 0) vs b12: 486,559
-> 474,095 (-12,464; CS0103 -19,091, CS0019 +6,349, CS0266 +117, CS0021
+61, CS0029 +44, CS1503 +35), ZERO parse codes; vs r_base 828,571 ->
474,095 (-42.8%). For-head CS0103 11,582 -> 0. The CS0019 rise is newly
visible type errors on lines whose undeclared counter used to mask them:
for-head CS0019 62 -> 2,479, 2,320 of them the interface-offset-table
scan `((byte*)__addr(k) + (i + i)*8 + 0x0)[0] != typeof(I)` (the 1-byte
index-form raw read deferred from fix 134 -- next slice candidate).
Suites: portable 1,313 passed; game FAILED set identical to game138 (the
4 fix-137 pin moves below, still awaiting the user's re-pin call).**

**Fix 137 (IN FLIGHT, accessor sugar): proved property-row accessors use
the member syntax the emitter declares (`lifter/calls.py` `_accessor_prop`
/ `_accessor_sugar`: `s.get_Chars(i)` -> `s[i]`, static getters ->
`Owner.Prop`, setters -> assignments incl. indexer sets; tails in
`dec/analyze.py` + `lifter/insn.py`, short2 + normal call paths).
Fix 137b: the sugar travels the pipeline as call-shaped markers
(`__accget(R.X)` / `__accset(R.X)(v)`, `il2cpp/expr.py`) so every text
purity test keeps treating the accessor as the call it is; `lift_method`
(`dec/build.py`) unwraps them last, after all DCE/CSE. The hole it
closes: a bare `R.X` getter reads as a pure load and was DCE'd when
unused / re-evaluated into a loop head (mi 5694 AppendFormatHelper's
`format.get_Chars(i)` -- a call that can throw -- vanished; post-fix it
reads `format[i]` and the loops resugar to `for`). Portable 1,309
passed (7 new marker/unwrap tests). mdiff (7 methods, post-marker):
six one/two-line improvements (mi 26747 Rpc_CMD_Heal `set_health` ->
`health =`, 24208 tail setter, 23902 static getter, 23554 2x static
setter, 12710 Chars indexer, 59905 `List<T>.get_Item(hits, i)` ->
`hits[i]`) + the mi 5694 reshape. Game suite: 263 passed / 4 failed =
the mi-26747 golden (intended) + 3 mi-5694 temp-renumber pins (intents
hold: `this.Append(character1)`, `Format(obj155, obj74, provider)`,
`if (obj84 == 0)`); all 4 need a user-approved re-pin. Gate b11 was
built from PRE-marker code: 492,867 -> 486,624 (-6,243; CS1061 -4,069,
CS0571 -2,433) but parse codes rose (CS1525 +36, CS1002/CS1003/CS1513
+18 each) -- the bare sugar let `_ternary` fold `if (c) X = a; return;
else X = b; return;` into `X = c ? a; return : b; return;`
(SlowmoToggler/KeybindsManager/CheckMSAA/TMP_InputField); post-marker
lifts of all three shapes are clean if/else. Gate b12 (post-marker
code, 10/10 groups exit 0, 11,262 files, brace audit 0, zero `__acc`
leaks tree-wide) vs cg7: 513,959 -> 486,559 (-27,400). Fix-137-only
delta b10 -> b12: 492,867 -> 486,559 (-6,308; CS1061 -4,048, CS0571
-2,433, CS0019 -455; relabel rises CS1503 +364, CS0103 +107, CS0266
+95, CS0021 +88, CS0029 +37, CS0120 +13) with ZERO parse codes in the
delta. Sampled rises are relabels of already-broken lines (same
precedent as fix 135/136): CaseInsensitiveAscii.cs:37
`obj7.get_Chars(0)` (CS1061) -> `obj7[0]` (CS0021); Guid.cs
`string.IndexOf(...)` same statement, shifted line; XsdDateTime.cs file
total 2,434 -> 1,445 (-989) with its CS1503 +205 unveiled on
object-typed receivers. RESOLVED by fix 138 (was the landing blocker):
mscorlib RegistryKey.cs +14 CS0103 `num10` -- the newly-pure
`stringBuilder1[num10]` loop resugared while->for and the minted
for-header reads `num10` with no declaration in the body (rename /
decl-drop interaction exposed by the sugar, repro mi 516 FixupPath).
Full game suite with final code not yet re-run (game138 ran pre-marker
code). NOT landed, NOT pushed, NOT re-pinned (all need user call).**
(Status correction 2026-10-25: the line above was written mid-flight and
never updated. The markers ARE landed on `main` -- commit `2e440fe`,
with its RegistryKey blocker closed by fix 138 `e1d9803`; gate b13
numbers below are post-marker. The 4 pin moves were dissolved by the
v39 fixture migration: zero pin moves post-141.)

**Fix 135 (CS0019 slice, 2026-10-06): `_numeric_obj_retype` in
`il2cpp/dec/highlevel.py` (end of `_rename_locals`) retypes an untracked
`object objN` temp to `int`/`long` (renamed into the num family) when
every def is an int literal / integer operator / integer local / itself
and no use is reference-like (member/index/call, null, is/as, casts,
&/ref/out, `__addr`). Gate b8 -> b9: total 499,479 -> 494,104 (-5,375);
CS0019 -3,319, CS0266 -3,036, CS0029 +1,132 (relabel: the same broken
lines now read `int -> struct` instead of `object -> struct`), no parse
codes, brace audit 0. Portable 1,300 passed, game 263 passed. Next:
float-used temps (`real`), the `objN + 0xK` `__addr` shapes, call-defined
temps, CS0103 remainder.**

**Fix 136 (CS0019/CS0266 float slice, 2026-10-06): `_numeric_obj_retype`
now also types float lanes -- float literals (`0.6f`, `1e5f`) and
float/double locals make the temp `float`/`double` (`realN` family; rank
int < long < float < double); float temps used with bitwise/shift/% keep
`object`. Gate b9 -> b10: 494,104 -> 492,867 (-1,237; CS0266 -1,146,
CS1503 -193, CS0019 -165, CS0029 +285 relabel), no parse codes, brace
audit 0. Portable 1,302; game 262 + 1 golden re-pinned (mi 23931
FPSDisplay.Update: `object obj10 = 1000.0f / real11` -> `float real13`).**

**Status: RE-PINNED 2026-10-06 (user-approved). The 39 moved
goldens/pins (21 goldens in `tests/goldens_review84.json` via
`work/cg8/repin_goldens.py`, 18 pin assertions in 13 test files) were
updated to the reviewed fix 125-134 output, with each test's intent kept.
Notable: the fp32 binary-op pin now requires both operands
(`(float)sub_180001cf0((float)(numN), 0.0001f)`); review87 accepts
`new System.NotImplementedException()`; review88 drops the
no-longer-emitted metadata-init check and keeps the no-bare-`throw;`
guard plus the concrete `ArgumentOutOfRangeException("level")`. Suites:
game 263 passed / 0 failed (11:36), portable 1,294 passed. Next slice:
CS0019 `object op int` (untyped integer temps).**

**Status: LANDED on `main` and pushed 2026-10-06 (`8b2d724`, fast-forward;
user call -- one branch, no split branches/worktrees from here on).
`final_out/` not promoted; goldens and pins NOT re-pinned (user call).**
Historical chain (branches deleted after the fast-forward):
`fix125-compile-gate-scope` -> `fix126-unknown-phi-copies` ->
`fix127-publicize` -> `fix128-raw-addr` -> `fix129-vtable-usage-decode`
-> `fix130-init-meta-value` -> `fix131-block-flags` ->
`fix132-entry-live-args` -> `fix133-generic-class-layout` (worktree
`%TEMP%\opencode\wt131`). Fix 134 (load widths) was done directly on
`main`. Latest gate `work/cg8/b8` (through fix 134):
**499,479 errors (-329,092 / -39.7% vs r_base)**; b6 (through 133)
501,046; b3 (through 132e) 505,396. Handoff + standard procedure:
`docs/handoff-2026-10-06.md`.

Gate (`work/cg5/`, chain through fix 130, `--strict --publicize
--raw-addr`, 10 groups, 0 failed / 0 fallbacks / 0 type-emit failures,
11,262 files): **828,571 (r_base) -> 515,786 errors (-312,785, -37.7%)**,
declaration-tier 1,232 -> 739. Step counts (whole-tree gates):
cg2 fix 125 727,579; cg3 +fix 126 699,602 (-27,977); cg4 +fix 127
`--publicize` 633,078 (-66,524); cg4r = cg4 post-processed with the fix
128 rewrite 554,297 (-78,781, estimate); cg5 real build 515,786 (-38,511
vs cg4r: CS0103 -15.5k, CS1061 -9.5k, CS0191 -6.7k (readonly drop),
CS0149 -4.4k, CS1955 -2.6k). Remaining top: CS0103 128k, CS0019 82k,
CS0266 66k, CS1061 66k, CS0029 52k, CS1503 43k.

1. **Fix 126 -- phi copies never read an unknown register**
   (`dec/analyze.py` `_unknown_phis`, greatest fixed point): an in-edge
   whose value is `_unk` or an all-unknown phi gets no copy (`phi = vN;`
   read a name nothing defines). The phi stays unassigned on that path
   and the compiler says so (CS0165) only if a read can see it. cg3:
   CS0103 -24.8k, CS0165 -1.4k. Tests `tests/test_fix126_unknown_phi_copies.py`.
2. **Fix 127 -- opt-in `--publicize`** (emitter): every member public,
   fields drop `readonly` (CS0122 87.5k -> 300; CS0191 then 0). Gate mode
   only; default output byte-identical.
3. **Fix 128 -- opt-in `--raw-addr`** (`il2cpp/rawaddr.py`): `(byte*)E`
   outside literals/comments becomes `(byte*)__addr(E)`; `__RawAddr.cs`
   (internal static unsafe overloads for void*/long/ulong/IntPtr/UIntPtr,
   `object` throws NotSupportedException) is written per assembly when
   used. CS0030 112.8k -> 3.5k. Tests `tests/test_fix128_raw_addr.py`.
4. **Fix 129 -- vtable rows are metadata usages** (`runtime/types.py`
   `vtable_method`/`slot_max_arity`): usage-6 (MethodRef) rows index
   methodSpecs (8,846 rows were decoded as MethodDefs; 64 agreed), empty
   rows (1,523) name the unique instance method carrying that metadata
   `slot` on the type or an ancestor (0 ambiguous). System.Xml A/B:
   `/*vtable slot N*/` sites 2,330 -> 100. **129b** (`lifter/calls.py`):
   a slot declared on the receiver's own generic definition binds class
   VARs from the receiver's GENERICINST args, so `Comparer<float>.Compare
   (T, T)` reads XMM1/XMM2 (Computer.ShouldRankBefore). Tests
   `tests/test_fix129_vtable_usage_decode.py`, `tests/test_game_fix129_generic_slot_args.py`.
5. **Fix 130 -- the initialize_runtime_metadata jmp thunk returns its
   slot item** (`lifter/calls.py`; disasm EnumBuilder.GetMembers
   0x181BD4E80: `lea rcx,[slot]; call 0x180435420; mov rcx,rax; call
   il2cpp_object_new`): RAX carries the slot expression, so allocations
   read `new T()` instead of `il2cpp_object_new(objN)`. The name-path
   `il2cpp_array_new` result now binds one identity via
   `_array_allocation` (was re-printing `new object[1]` at every use).
   Test `tests/test_game_fix130_init_meta_value.py` (System.IO.__Error.WinIOError).
6. **Fix 131 -- per-block condition flags** (`dec/analyze.py`,
   `lifter/values.py`; branch `fix131-block-flags`): `L.flags` was
   lifter-global, so a pass-2 block opened with the flags of whichever
   block executed last (Computer.ShouldRankBefore mi 24622 0x18069C7A0
   `setg al` printed `return num1 >> 31 > 0` instead of
   `Compare(...) > 0`). Each block now records its end flags (a jcc
   stashes the pair it consumed in `L._jcc_flags`); a block restores a
   pair only when it reads a flag before defining one (`_flags_live_in`,
   iced `rflags_read`/`rflags_modified`) and every done predecessor
   agrees (`_flags_key`); entry / orphan blocks start with None. The
   restored operands are private copies (`_restored_pair`) unless the
   operand is one whole call (`_top_call`), so a successor's reads never
   bind a loop-header Expr into the body (KeybindsManager.Update `for (i
   = 0; i < objN; ...)` with objN assigned inside) while `Compare(...)`
   still binds once. A register write that kills a carried pair drops
   it instead of materializing an `object objN = <cond>` twin
   (`L._carried_flags`, `_kill_stale`); `_kill_stale` also never freezes
   the `!flags` merge sentinel (its `lhs<0x01>rhs` text became an
   `object objN = op_Implicit(...)` twin). Without the live-in gate the
   extra sentinels drew pass-2 phi numbers and shifted clobber
   placeholders against pass 1 (undeclared `sub_180434660(..., obj36,
   obj37)` in AudiencePath.DrawCurved).
   Assembly-CSharp A/B: `unknown == unknown` conditions -111 (now e.g.
   `realN == 0f`); ShouldRankBefore reads `int num1 = Compare(...); if
   (num1 != 0) return num1 > 0;` (was an undeclared `num1`). Test
   `tests/test_game_fix131_block_flags.py`.
   **131b**: `_restored_pair(None)` raised TypeError (method fell back to
   unstructured `if (? <= ?) goto`, cg6 517,994 = +2,208 vs cg5 with
   CS1525 +2.1k / CS1003 +0.7k in Unity.Mathematics); it now returns
   None, and a block that writes no flag passes its predecessor pair
   through (`math.uint2(float)` mi 68399 `if (0f <= v)`).
   Gate `work/cg7/` (chain through 131b, same flags, 11,262 files,
   0 failed / 0 fallbacks): **513,959 (-1,827 vs cg5; -314,612 / -38.0%
   vs r_base)**: CS0103 -2,383, CS0019 +441, CS0029 +102 (conditions that
   were `unknown` now carry real typed operands and surface type errors).
7. **Fix 132 -- entry-live arguments for plain `sub_` callees**
   (`il2cpp/entrylive.py` new, `lifter/calls.py`, `lifter/insn.py`;
   branch `fix132-entry-live-args`). A `sub_VA` call with no metadata
   candidate and no export printed the 4-GPR spray (`sub_1804d05a8(v,
   obj2, obj3, obj4)`), dropped XMM arguments and assumed an RAX result
   (`return obj5 * 57.29578f`). Probe: 15,983 CS0103 sat in `sub_`
   arguments, ~5.7k in positions the callee provably never reads.
   `entry_live_args(il, va)` walks the callee's extent (iced
   InstructionInfo) for read-before-write of RCX/RDX/R8/R9/XMM0-3: only
   full writes define (8/16-bit GPR writes do not; low-lane scalar
   writes `movss/movsd/cvt*/sqrt*/round` with src != dest define the XMM,
   132c); direct calls/jumps out of extent recurse (memoized, depth 10,
   order-independent); an unprovable call makes every still-undefined
   register live; indirect branches, tail jumps to unprovable targets,
   falling off the extent, untrackable RSP math and stack-argument reads
   (entry offset >= 0x28) decline (None). The call prints position i as
   the GPR or the XMM the callee reads, `0` for a dead interior
   position, and keeps the spray when a position reads both, the value
   is unknown, or the text cannot parse (132e: `GenericMethod#N`
   placeholders, bare `?`). **132b/d** `xmm0_result_width`: the caller's
   next uses decide a float/double XMM0 result (scalar SS/SD reads, RMW,
   packed PS/PD sources, whole-register copies followed across a later
   call into XMM6+; any RAX touch, untyped read, branch or ret
   declines), giving `float real1 = (float)sub_...(...)`.
   **132e** (`lifter/insn.py` `_unary_txt`): NEG/NOT shared one
   `'-%s'` spelling -- NOT printed as negation, `-(-x)` as the
   predecrement `--x` (FrameRate CS1059), `-(a + b)` as `-a + b`. NOT is
   now `~`; a composed, sign-led or space-bearing operand is
   parenthesised.
   Examples: GetAngleDeg mi 28756 `float real1 = (float)sub_1804d05a8(v.x,
   v.z); return real1 * 57.29578f;`; PathProcessor
   CalculatePathsThreaded `path3.duration = real1` from
   `(float)sub_180001cf0((float)(num3), 0.0001f)` (native `mulss
   xmm0,xmm1; ret`; was `sub_180001cf0(obj48, obj49, obj50, obj51)` and
   `= unknown`); EncodingTable `sub_18032f5e0(arr, 57, &obj24)` (native
   reads RCX/EDX/R8; the junk 4th argument is gone).
   Gates vs cg7 513,959: b1 (132a-c) 505,586; b2 (+d) 505,230; **b3
   (+e) 505,396 (-8,563)**: CS0103 -8,790, CS0023 -264, CS0165 -144,
   CS1059 8 -> 0; up CS0019 +399, CS1503 +244, CS0029 +99 (sampled:
   newly visible -- e.g. `&obj24` to an `object` stub parameter was
   masked by the undeclared 4th argument). b1/b2 had +1 CS1026/CS1003/
   CS1040 (placeholder argument) -- fixed by 132e, back to baseline.
   b3 gives back ~170 vs b2 by declining unparsable arguments (P4).
   Tests `tests/test_fix132_entry_live_args.py` (17),
   `tests/test_fix132e_unary_and_xmm_args.py` (5),
   `tests/test_game_fix132_entry_live_args.py`.
   **Pin move (review for re-pin):**
   `test_game_fp32_unary.py::test_binary_op_keeps_honest_spelling`
   asserts the old `object objN = sub_180001cf0(` spray. Its intent --
   never drop the XMM1 input into a wrong unary float -- holds: the call
   now carries both inputs and a float result, matching native.
8. **Fix 133 -- open generic class layouts** (`runtime/fields.py`,
   `lifter/values.py`; branch `fix133-generic-class-layout`, from
   `fix132-entry-live-args`). IL2CPP stores all-zero instance offsets for
   an open generic definition, so `instance_field_chain(List`1)` was
   `{0x0: _items}`: the object header was misnamed and `_size` (0x18)
   never resolved -- 105,592 `((byte*)__addr(B) + off)[0]` raw derefs in
   b3, many of them collection reads. **133a** `_class_level_offsets`:
   an all-zero class level whose instance fields are argument-invariant
   (primitives, string, pointers, class/array/object references, class
   GENERICINST, byref) is laid out the IL2CPP way -- parent instance end,
   declaration order, natural alignment; by-value VAR/struct fields or
   explicit layout decline (the level then names nothing, never offset
   0). Validated (`work/cg8/layoutval.py`): 4,984/4,985 non-generic
   classes and 4,732/4,743 value types reproduce their real offsets
   (misses: Pack=4 structs, excluded by the rule); 6,179 recorded class
   sizes equal the reconstructed end. List`1 = {0x10 _items, 0x18 _size,
   0x1c _version, 0x20 _syncRoot}. **133b** `_recv_member_ty`: the
   chain carries the definition's field type (`T[]`), which leaked an
   unbound `T` into caller declarations (b4: CS0246 'T' +322). A member
   type mentioning class parameters is kept only when all belong to the
   receiver typedef's own container -- closed through a GENERICINST
   receiver (`_subst_closed`; `T[]` reuses the binary's closed array
   row, or `object[]` for a reference element with no row -- array
   covariance), or left in scope for the definition's own `this`; base
   level parameters, MVARs and unclosable arguments drop the type but
   keep the member and its kind (`T[]` stays 'arr'; a dropped type
   once fell through to 'int' and printed `int num2 = x._items`).
   Examples: AudiencePath.SpawnPeople mi 23555 (0x1804FEDF0) `int num1 =
   list11._size - 1;` (native `mov ebx,[rdi+18h]`); TMP_FontAsset
   TryAddCharacters mi 95397 `UnityEngine.TextCore.Glyph[] glyphArray1 =
   this.m_GlyphTable._items;`; ObiColliderWorld `object[] objectArray1 =
   this.implementations._items;`.
   Gates vs b3 505,396: b4 (133a) 501,289; b5 (+133b) 501,289 (CS0246
   -360, but CS0029 +186 from the 'int' kind fall-through); **b6 (+kind
   fix, object[] fallback) 501,046 (-4,350; -327,525 vs r_base, -39.5%)**.
   b6 vs b3: CS0019 -3,008, CS1503 -949, CS1061 -475, CS0266 -315,
   CS0246 -7; up CS0214 +367 (a method whose raw derefs are now named
   loses its `unsafe` cover while a leftover `&local` still needs it --
   `textpass` keys unsafe wrapping on raw derefs, not on `&`; follow-up),
   CS0103 +30, CS0021 +19 (newly typed arrays indexed with pre-existing
   junk indices, e.g. `obj19[num2 * 3]`). Brace audit 0 unbalanced; no
   parse-code increase. Tests `tests/test_fix133_generic_class_layout.py`
   (5), `tests/test_fix133b_member_type_scope.py` (8),
   `tests/test_game_fix133_generic_class_layout.py` (3). Portable 1,285
   passed.
   **Pin move (review for re-pin):**
   `test_game_review80.py::test_direction_dispatch_is_not_dropped_from_draw_curved_loop`
   anchors its loop slice on `if (((byte*)this.pathPoint`; mi 23566
   (PeopleWalkPath.DrawCurved) now reads `if (this.pathPoint._size >=
   2)`. Loop content unchanged (all six direction strings, both
   `this._forward[num2] = true/false`, no goto).
9. **Fix 134 -- raw loads keep their native width** (on `main`;
   `lifter/insn.py`, `dec/textpass.py`, `dec/sugar.py`,
   `lifter/state.py`). `textpass._unsafify` spelled every width-less
   `*(E + N)` as `((byte*)E + N)[0]` -- a 1-byte read in C# where native
   loads 2/4 bytes (a correctness bug, not only a type error). **134a-d**
   `_width_mark`: a whole single raw field load `[base+disp]` (no index;
   base a plain identifier/member chain, not an array/string receiver)
   whose expression has no type is wrapped as `(__w_T)*(...)` with T from
   the instruction (`_W134`: MOV r32 -> int, MOV r16 -> short, MOVZX
   word -> ushort, MOVSX byte/word -> sbyte/short, MOVSXD -> int,
   CMP/TEST mem32/16 -> int/short) and typed int; byte zero-extends and
   qwords stay unmarked. `textpass._widen_marked` spells it
   `((T*)((byte*)E + N))[0]` (byte-addressed displacement, as fix 124
   stores); leftover markers are stripped. A first version that marked
   every read form (b7 501,045, net -1) hid index-form reads (interface
   offset tables) and `*(arr + 0x18)` `.Length` reads from later text
   folds -- hence the field-form-only scope. **134e** `_member_fold`'s
   stale-receiver-paren strip `(?<![\w.])\((tok)\)\.` also fired on a
   generic call's argument paren (pre-existing, b6 already had
   `FindObjectsOfType<TMP_Dropdown>true.Length`); `(` glued to `>`, `)`
   or `]` is now left alone. **134f** the oversized-temp spill comment
   (`var vN = 0; // <expr>`, `state._mk`) is opaque to textpass, so the
   lifter strips markers there itself.
   Examples (native-verified): TouchscreenStateEvent OnStateEvent mi
   32833 (0x18264A0D0) `mov ebx,[rax+14h]; cmp ebx,eax` ->
   `int num2 = ((int*)((byte*)inputEventPtr2 + 0x14))[0];` compared with
   `TouchState.Format`; KeybindsManager.Update mi 25872 (0x180547380)
   `call unbox; mov esi,[rax]` -> `int numN = ((int*)((byte*)objN +
   0x0))[0];`.
   **Gate b8 vs b6 501,046: 499,479 (-1,567)**: CS0019 -1,221, CS1503
   -722, CS0266 -668, CS1061 -142, CS0103 -104, CS1579 -49 (134e),
   CS0119 -25; up CS0029 +1,310 -- cascade unmasking: temps that were
   `int* intPtr1 = this._object.Ptr` (Fusion RPC stubs) now type as
   `NetworkId`, so `RpcHeader.Create(networkId1, ...)` binds and the
   pre-existing struct-store width error `((byte*)__addr(msg) +
   0x1c)[0] = RpcHeader.Create(...)` surfaces (RpcHeader->byte +405,
   int*->struct +464, int->struct +571; embedded-struct stores are a
   listed follow-up); CS0021 +29, CS0023 +21, CS0165 +18. No parse-code
   increase; brace audit 0 unbalanced. Tests
   `tests/test_fix134_load_width.py` (9),
   `tests/test_game_fix134_load_width.py` (3). Portable 1,294 passed.
   **Pin moves (review for re-pin)** -- all temp renumbering from a new
   int temp, plus width-correct reads:
   `test_game_fix131_block_flags.py::test_restored_operands_do_not_bind_the_loop_bound`
   (the loop variable is now `num6`; the bound is still
   `UnityEngine.Object.FindObjectsByType<ChangeTextToKeybind>(FindObjectsSortMode.None).Length`,
   never `obj`); golden `mi-80548-Execute` (`int num5 = ((int*)((byte*)num4
   + 0x18))[0];` hoisted and reused for both index reads and the store;
   the qword `>> 32` reads stay byte-spelled); golden/pin mi 32833
   (`review80::test_touchscreen_condition_is_recomputed_in_the_loop`: its
   `num7 = unknown + this.currentStatePtr` marker is now `num8`, and the
   compare reads `((int*)((byte*)num5 + 0x0))[0]`).

Game suite (run in worktrees; `cli_only`, `decl_gate`, `compile_gate`,
`parallel_build` fail there for path reasons -- relative `testgame`,
no `final_out/` -- and pass in the main checkout): beyond fix 125's 22
known failures, fix 126 moves goldens mi 0, 21027, 128953 and pins
`elemclass::test_unknown_provenance_declines`,
`iface_param::test_resolved_string_result_null_tests_null`,
`interface_dispatch` x2, `null_zero::test_object_zero_keeps_zero` --
reviewed: temp renumbering and dropped unknown copies only. Fix 129 moves
golden mi 83647 (`type.AssemblyQualifiedName` for a `/*vtable slot 25*/`
call) and pin `isinst_tail::test_tail_typeof_folds_to_as` (mi 3446 now
`element.GetCustomAttributes(...) as Attribute[]` and `element.MemberType`
compares). Fix 130 moves pins
`review87_eh_helpers::test_pad_less_caller_renders_the_proven_helper_as_a_throw`
(mi 106196 now `object obj1 = new System.NotImplementedException(); throw
obj1;` -- the test looks for `obj1 = il2cpp_object_new(`) and
`review88_eh_helper_set::test_metadata_init_is_not_flattened_to_a_throw`
(mi 77946 GetTraceEventType no longer prints an
`il2cpp_codegen_initialize_runtime_metadata(` statement; still no bare
`throw;` and still `throw obj3;` of `new ArgumentOutOfRangeException("level")`).
wt131 game suite: 39 failed = wt129's 37 + those two. With fix 132a-e
(`work/cg8/game132.out`): 40 failed = those 39 + the fp32_unary pin move
above (no other changes). With fix 133 (`work/cg8/game133*.out`): 41
failed = those 40 + the review80 anchor move above. Fix 134, main
checkout (`work/cg8/game134.out`): 39 failed = those 41 minus the 5
path-only tests (they pass in the main checkout) + the 3 fix-134 moves
above. All need a user-approved re-pin.

**Next-slice probe (CS0019, b3; `work/cg8/cs0019.py`, `objdefs.py`):**
34,689 CS0019 have an `object` operand. Shapes: 6,443 are
`__addr((objN + 0x80))` frame/struct bases (`objN := &local | (objN +
0x80)`); ~25k are `object objN` temps used as numbers. By definition
(12,098 distinct method/temp pairs): raw deref 3,016 (e.g.
`((byte*)__addr(this.m_Items) + 0x18)[0]` -- a List `_size` read),
arith 2,061, call 847, temp copy 703, int literal 601, mixed rest.
Root cause worth fixing first: `textpass._unsafify` spells every
width-less `*(E + N)` as `((byte*)E + N)[0]`, which in C# is a 1-byte
read while native loads 4/8 bytes -- a correctness bug, not only a
type error. Options: (a) the lifter spells the load width at the deref
(`((int*)((byte*)E + N))[0]`; insn.py already does this for typed
wide accesses, lines ~2015-2047), then temps typed from it; (b) resolve
generic-instance fields (`List<T>._size` at 0x18) so the deref never
exists. Either moves many goldens -- needs a user call on approach.
(Done: (b) is fix 133, (a) for field-form loads is fix 134.)

Follow-ups seen while landing: CS0019 `object op int` (untyped integer
temps, 82k); CS0165 phi arms minted under different names; `unknown`
SIMD lane placeholders (`unpcklps` + `movsd` into Vector3 fields);
indirect calls `X[0]() /*indirect*/(args)` (CS0149 9.4k).
(Status 2026-10-25: CS0019 object-op-int landed as fixes 135/136; the
indirect-call item is largely covered by fixes 139/140 (CS0149 -486 at
b19, 381 vtable sites left) and the SIMD item by F1 lane modeling
(SHUFPS half still open, co-land with MOVSS merge). Still fully open:
CS0165 phi-arm naming, embedded-struct stores, the CS0214 unsafe-cover
keying. Live tracking: `docs/plans/2026-10-25-todo-roadmap.md`.)

## Current work: fix 125 compile-gate first slice (2026-10-05, branch `fix125-compile-gate-scope`)

**Status: on branch, not merged/promoted. Goldens NOT re-pinned (user call).**
(Status correction 2026-10-27: the branch above no longer exists --
fix 125's compile-gate work is in `main`'s shared history; the
goldens/pins were re-pinned at the 2026-10-06 call and the v39
fixture migration (`d1ea2d2`) rebuilt the corpus afterwards.)
First use of the P1 Roslyn compile gate as the primary metric.

Gate tooling (all git-ignored scratch in `work/cgate/`):
- `work/cgate/rgate/` -- per-assembly Roslyn gate (SDK 10.0.302 Roslyn
  DLLs; one `CSharpCompilation` per image wired by CompilationReferences
  in topological order from `deps.json`, mscorlib as corlib,
  `__Generated` referenced by all). Run:
  `dotnet work\cgate\rgate\bin_out\rgate.dll <flat tree> work\cgate\deps.json <outdir>`
  (~13 s whole tree) -> `log.txt` + `summary.json`.
- `work/cgate/deps.py` (image reference graph), `cmp.py` (per-code
  before/after), `top.py`, `sample.py`, `initshape.py` (shape census),
  `undecl.py` (CS0103 temp classifier), `launch.ps1 -Out <dir>` (10
  balanced per-group strict builds) + `merge_gate.ps1 -Out <dir>` (merge
  to `flat`, run gate, compare against baseline).
- Baseline `work/cgate/r_base/` (main @ d97dd15, 91 images, 11,107
  files): **828,571 errors** (1,232 declaration-tier). Top: CS0103 283k,
  CS0030 106k, CS1061 95k, CS0122 86k, CS0019 73k, CS0266 47k.

Landed on the branch (three source slices + tests):
1. **Escaping-local hoist** (`il2cpp/dec/build.py`
   `hoist_escaping_locals`, run after `_final_text`): a minted local
   (name ends in a digit, single declared type, not a param/pattern/
   loop/lambda name) whose uses are not all inside a scope that declares
   it earlier gets one bare `T name;` at the top of the lowest common
   block (never inside a switch block) and its inner declarations become
   assignments. No `= default` -- a path the native code never assigns
   stays visible as CS0165. Prototype on the baseline tree: 46,339
   hoists, CS0103 -57.9k, CS0136 -3.2k, CS0841 -2.3k, CS0165 +9.6k
   (honest unassigned reads, mostly phi arms minted under different
   names), and newly bound names surface ~+15k type errors
   (CS0030/CS0266/CS1503/CS0019) that were masked behind CS0103.
2. **Empty class-init guard drop** (`drop_empty_init_guards`):
   `if (typeof(X).initialized ==|!= ident|0) { }` with an empty body and
   no `else` is a no-op flag read; 24k+ sites (CS1061 on `Type`).
   Guards with a body are untouched (`_class_init_strip` still owns them).
3. **Callee-side hidden sret buffer** (`lifter/state.py` setup):
   methods that return a large struct now seed RCX as `&__ret`
   (slot type = return type), so stores through it fold to
   `__ret.field` via the existing `&s_N` valuetype path, the
   `mov rax,rcx` echo returns `return __ret;` (`dec/analyze.py`), and
   `_sret_local_decl` declares `T __ret = default;` once (mirrors the
   caller-zeroed buffer). Previously every such body read an undefined
   register (`((byte*)obj2 + 0x0)[0] = obj1; return obj2;`, mi 24266
   BabyDoll.get_NetworkedPosition; Unity.Mathematics swizzles).
   Guard added in `lifter/values.py`: an access WIDER than the member
   it starts at (`movsd [rcx],xmm0` = Vector3.x+y) keeps the raw deref
   instead of naming only the first field (this also applies to the
   caller-side `&s_N` echo -- correctness, P4).
- Tests: new `tests/test_scope_repair.py` (6).

Gate results (whole tree `work/cg1/`, see `work/cg1/cmp.txt`):
- Build `work/cg1/` (all three slices, BEFORE the `__ret` decl-guard
  fix below): 10 strict groups, 0 failed bodies / 0 fallbacks / 0
  type-emit failures, 11,183 files. **828,571 -> 761,086 errors
  (-67,485, -8.1%)**, declaration-tier 1,232 -> 1,217. CS0103
  283,183 -> 216,428; CS1061 95,250 -> 72,869; CS0136 3,668 -> 60;
  CS0841 2,824 -> 39; CS0165 147 -> 10,754 (honest unassigned reads);
  masked type errors surface: CS0030 +5.5k, CS0266 +3.5k, CS1503 +2.8k,
  CS0019 +2.3k, CS0029 +2.0k.
- Bug found in that build: `_sret_local_decl`'s "already declared"
  guard matched `return __ret;`, so `T __ret = default;` was never
  emitted (47,626 errors in `work/cg1` name `__ret`). Fixed on the
  branch (guard excludes `return/throw/goto`); mi 24266 relift now
  declares it.
- **Rebuild `work/cg2/` (branch HEAD, all slices + guard fix), 2026-10-05:**
  10 strict groups, 0 failed / 0 fallbacks / 0 emit failures, 11,183
  files. **828,571 -> 727,579 errors (-100,992, -12.2%)**; vs cg1
  -33,507. CS0103 283,183 -> 168,802; CS1061 95,250 -> 72,897;
  CS0136 -3.6k; CS0841 -2.8k; CS0165 147 -> 10,754; surfaced CS0266
  +11.5k, CS0029 +6.2k, CS0030 +5.5k, CS1503 +3.0k, CS0019 +2.5k
  (statements that now bind far enough to show type errors).
- Game suite re-run on the guard-fixed source (2026-10-05): **220
  passed / 22 failed -- the identical 22** (16 goldens + 6 pins listed
  below); nothing new broke. Still NOT re-pinned (user call).
- Portable suite: 1,229 passed. Game suite (run on the cg1 source):
  220 passed / 22 failed -- **16 goldens** (mi 5769, 11974, 26747,
  32832, 32833, 32837, 37191, 39789, 42414, 45016, 64986, 70050, 75101,
  86310, 104428, 109664 list in `work/cgate/pt2.out`) and 6 text pins,
  all expected spelling changes from this fix, NOT re-pinned (user call):
  `test_game_fp32_unary`/`test_game_jcc_flag_chain` audio x4 (pin
  `float real2 = ...` now hoisted `float real2;` + `real2 = ...`),
  `test_game_single_field::test_timespan_assign_folds_to_whole`
  (hoisted `System.TimeSpan timeSpan2;`), `test_game_review81` packed
  lanes (raw base is now `&__ret` instead of undefined `obj3`). Every
  golden diff must still be read line by line before re-pinning, and
  the game suite re-run after the `__ret` guard fix.

Next (ranked by gate yield, from the baseline census):
- C6/C1 never-defined register temps (~120k CS0103): phi copies of
  undefined registers (`object obj6 = obj7;`, 56k) and spray args of
  shared/ICF calls (28k). Root-cause in phi seeding, not text.
- C5 rest: `il2cpp_codegen_initialize_runtime_metadata(...)` assignments
  (8.5k CS0103; e.g. `object obj1 = ...(typeof(NotSupportedException));
  il2cpp_object_new(obj1)` should read `new NotSupportedException()`),
  `il2cpp_object_new` 3.3k, `mono_object_unbox_internal` 2.5k,
  `il2cpp_interface_get_method` 2.4k, `typeHierarchyDepth` 2.8k,
  `__static_fields`.
- C4 `X -> byte*` raw casts (CS0030 ~106k): compilable raw helper.
- C10 private member access across types (CS0122 86k): emit-side
  accessibility relaxation or accessor routing.
- `get_Chars`/`.ctor`/`getClass` sugar (CS1061 ~20k), C8 generic
  spellings (`Dictionary_2<...>`).
- Phi arms minted under different names (new CS0165s): unify names.
- Lane coalescing (C3): 8-byte movsd copies of two float fields.

## Previous work: fix 124 wide-store byte offsets (2026-10-04, DONE on branch)

**Status: complete on branch `fix124-wide-store-byte-offsets`.** Source fix,
tests, goldens and the full gate set landed together; evidence in
`validation_reports/review124_*` (raw artifacts in the git-ignored
`work/fix124_ab/`). Next up is the compiler-error backlog below.

- Native re-check of all 8 affected MethodDefs: every re-spelled store's
  byte offset equals the native memory displacement; each pre-fix typed
  spelling wrote `offset * sizeof(T)` (mi 25626 byte 0x20, 26747 0x90,
  32837 0x40, 75101 0x20/0x50/0x80, 109194 0x10/0x20/0x30, 128953 0x80;
  1935 is offset 0 and spelling-only).
- Paired strict `--only Assembly-CSharp` builds (main source from
  `git archive HEAD` vs branch; both 490 files / 6,622 bodies / 0 failed
  / 0 fallbacks / 0 type-emit failures): 155 files, 1,701 changed lines,
  **every changed line a pure fix-124 reshuffle, 0 unexpected, 0
  line-count deltas**; brace 0 unbalanced; parse 0/0/0/0.
- Whole tree (91 images, 11,183 unique files, built as 10 balanced
  concurrent per-image runs because this sandbox denies the `--workers`
  process pool): brace 0 unbalanced, parse 11,183 files 0/0/0/0.
- Paired whole-corpus direct sweep (116,178 bodies): 0 crashes, brace
  0/0, dangling 0, empty-args 0, `into_block` 8,075/2,046 unchanged;
  main-vs-branch compare 9,339 changed methods, **0 structural changes,
  0 new crashes**; purity proof 9,339/9,339 pure fix-124 (9,313 by exact
  canonical-body hash, 26 by fresh-process line-pair comparison).
- Goldens: 64 snapshots, 59 unchanged, 5 re-pinned (26747, 32837, 75101,
  80548, 128953) -- every diff line read and confirmed pure fix-124.
- Suite: 1,463 passed / 2 failed of 1,465 (portable 1,223 + game 242);
  both failures are this sandbox's named-pipe denial for
  `test_game_parallel_build.py`, reproduced by a three-line
  `ProcessPoolExecutor(2)` call with no il2cpp code involved (see
  `validation_reports/review124_environment.json`).
- Unrelated untracked `.freebuff/` in the worktree: not ours, leave it.

Branch `fix124-wide-store-byte-offsets`. Fix 102/103's
wide display rendered `((T*)E + N)[0]`; C# pointer arithmetic scales N
by sizeof(T), so every non-byte raw store wrote the wrong address.
Native proof (fixture): mi 24267 `BabyDoll.set_NetworkedPosition`,
`0x18060cdaa mov [rcx+8],eax` rendered `((float*)this.Ptr + 0x8)[0]`
(= byte 0x20). Census: 1,636 such store lines in fixture r11
Assembly-CSharp alone. Parse/brace gates could never see it.

Landed on the branch:
- `il2cpp/lifter/insn.py` `_wide_store_disp` / `_wide_rmw_disp`:
  emit `((T*)((byte*)E + N))[0]` (indexed: `((T*)((byte*)E + i*s + N))[0]`),
  the same shape `_wide_raw_lvalue` already used. CRLF binary patch.
- `il2cpp/text.py` `_canon_wide_cast`: strips a whole-span inner
  `((byte*)...)` so `_norm_twin` still meets the raw barrier twin
  `*(E + N)`; a byte-cast READ base (`((byte*)b + 0x10)[0] + N`) is
  untouched.
- Tests: 7 end-to-end pins repinned in
  `tests/test_review102_raw_store_widths.py` (input-only canon/unsafify
  tests keep the old spelling as valid input); new
  `tests/test_fix124_wide_store_byte_offsets.py` (+6: address shape,
  canon strip, byte-load-base decline, twin bridge, unsafify fixpoint).

Repins landed with the fix: the 3 non-golden failures were old-spelling
pins only (`test_game_param_names[1935]` `((uint*)v1 + 0x0)`,
`test_game_review81::test_packed_float_intrinsic_...` (mi 109194; its
0x4/0x8/0xc lanes were bytes 0x10/0x20/0x30 under the old spelling),
`test_game_rpc_payload::test_stores_use_typed_widths_...`), plus the 5
goldens (mi 26747, 32837, 75101, 80548, 128953). Portable suite 1,223
passed; `work/fix124_ab/golden_diff.txt` holds every golden diff line,
and `work/fix124_ab/purity.json` + `pair_purity.json` the corpus proof.

Two process notes for the next fix, both paid for here:
- `--workers` cannot run in this sandbox (named-pipe denial). Multi-image
  builds must be split into per-image/per-group processes; a single-image
  `--only` build silently takes the serial path, so it is *not* evidence
  that the pool works.
- The whole-body "canonicalize the new body and hash it" purity method is
  unsound when pre-existing `((T*)((byte*)E + N))[0]` lines from
  `_wide_raw_lvalue` are present in both sources; it over-strips them.
  Use the line-pair predicate (only *differing* pairs must reduce to the
  other side), which is sound and found 0 real deltas.

Known sibling (not fixed here): an 8-byte `movsd qword [rcx], xmm0`
store of two float lanes renders `((byte*)this.Ptr + 0x0)[0] = value.x;`
(mi 24267, first store) -- width and the y lane are lost. See C3.

## Compiler-error backlog (2026-10-04, PLAN)

The promotion gates (brace, tree-sitter parse, goldens, 0 failed
bodies) measure parseability, not compilability. On a second, larger
external Unity 6 corpus (Assembly-CSharp, 8,617 type files / 60,518
bodies, 0 failed; NOT tracked, never redistribute) the emitted tree
carries ~498k Roslyn errors across 5,358 files while every gate is
green. Top codes: CS0103 78.9k, CS0030 38.6k, CS1061 25.9k, CS1503
21.0k, CS0122 12.8k, CS0019 12.6k, CS0029 11.1k, CS0246 8.1k, CS0266
5.9k, CS0571 5.8k, CS0208 5.8k. Raw-text census of that tree: 96.9k
`(byte*)`, 80.4k `((T*)X + N)` sites (45.0k named/param/field
receivers, 32.7k temps, 2.7k `this`), 2,153
`il2cpp_codegen_initialize_runtime_metadata`, 701 `__static_fields`,
4,943 `sub_`, 3,496 `unknown`, 5,638 `goto`.

Process changes (do first):
- P1. Roslyn compile gate as the primary metric: per-rebuild census by
  CS code + message pattern, failure SET tracked like the test-failure
  set. A fix lands only if its family count drops with goldens/tests
  green. Note csc reports body errors only after declaration errors are
  zero -- clear the declaration tier first or the count is misleading.
- P2. Add a second, larger fixture (licensed) so families that barely
  occur in ShiftAtMidnight are exercised (see C1).
- P3. One agent per error family, 4-6 in parallel max, worktrees, same
  landing protocol. `dec/structure` pass order matters and goldens regen
  serializes; more parallelism mostly produces conflicts.
- P4. "Compiles" never outranks "correct": every fix still needs native
  proof; decline-by-default stays. Don't make code compile by guessing
  casts.

Families, by expected yield:
- C1. Shared/ICF call naming (largest CS0103 driver). In the external
  corpus 92% of sampled undeclared `obj#`/`num#` sites (552/597, files
  untouched by hand) are spray args of one shape:
  `Unrelated_1<bool>.SomeMethod(this, Base_1<TModel>.ctor, obj1, obj2);`
  (anonymized; the external tree is never quoted verbatim)
  inside a ctor that should be `: base()` with an empty body. The jump
  target is a shared (ICF-folded / generic-shared) body; naming by VA
  picks an unrelated owner, while the hidden MethodInfo* arg (RDX/last
  arg, kind `methodinfo`) names the true target. ~10.2k trailing-spray
  sites, ~4.0k `.ctor`-as-value sites. The fixture renders its single
  instance honestly (`sub_180de4fa0/*shared body, 229 candidates*/`,
  mi at VA 0x18061FDB0, FEngineering), so some path (suspect the dec
  direct-tail `_emit_tail` path, cf. slice 2b) bypasses the candidates
  check. Fix: resolve the callee from the methodinfo arg when present,
  drop it and spray beyond the resolved arity; base-ctor tail ->
  `: base(...)`. Also fixes many CS1061/CS1503/CS0117.
- C2. Field resolution for raw offsets, including interior offsets into
  value-type fields (recursive: 0x18 inside a Vector3 field at 0x10 ->
  `.field.z`). Must happen at Expr/lifter level where types live,
  not in textpass. Biggest share of CS0030/CS0208.
- C3. Lane coalescing: split SIMD/qword stores of one struct value
  (`movsd [rcx],xmm0` + `mov [rcx+8],eax`) -> one struct assignment
  (`this.f = v;`), and never emit a lane into a struct-typed field
  (`this.f = v.x;` -> CS0029). Fixture repro: mi 24267.
- C4. Compilable raw fallback: C# cannot cast a managed reference to a
  pointer, so every residual `((T*)ref + N)` is CS0030 regardless of
  fix 124. Emit a declared helper (e.g. `Il2CppRaw.Ref<T>(obj, 0x18)`
  over `Unsafe.As`/`Unsafe.AddByteOffset`). Honest and compiles; track
  the helper count as debt -- IL2CPP vs Mono object layouts can differ,
  so these sites may be wrong at runtime.
- C5. Runtime-bookkeeping removal: `il2cpp_codegen_initialize_runtime_metadata`,
  `Type.typeHierarchyDepth` / `.initialized` / `.name` checks (~17k
  klass-field matches), `IntPtr.m_target`; `__static_fields` blob ->
  `Class.Field`.
- C6. Undeclared outgoing stack-arg temps (`obj7 = ...;` then
  `Call(..., obj7)`): declare with the callee parameter type or inline.
- C7. Accessor/operator sugar: `X.get_Item(a)` -> indexer,
  `op_Equality(a, b)` -> `==` etc. (CS0571 ~5.8k).
- C8. Generic spellings in references: `Name_1<T>` / `Name_1<>` vs
  declared names (CS0246/CS0103 still non-zero on the
  external corpus although fixture CS0246 is zero).
- C9. async/iterator state machines: `TStateMachine`/`TAwaiter`,
  `object.Current/Dispose/Start/Task` -> `async`/`yield` re-sugar or
  emit the compiler-generated types faithfully (~2k+ sites).
- C10. Accessibility: CS0122 ~12.8k -- emit publicized declarations
  (opt-in flag) or route through declared accessors.

Longer-term (structural): many passes are regex over rendered text
(`textpass`, `_sub_outside_literals`). Families C2/C3/C5 need type
information that is gone by then; prefer moving them onto `Expr`/IR.

## Note: slice-2 throw-vs-null reconciliation (2026-10-02, DOCUMENTED)

`183a92b` closed slice 2 with all 17 typeof sites declining, including
3 my tail fold also covers (2x Attribute tails, 1x Recorder tail), on
two grounds: the callee throws like castclass (so `as` would trade
throw for null), and trimming the arity-4 spray is unsound. Native
evidence disproves both grounds FOR THIS ADDRESS FAMILY
(`0x180434690` thunk -> `0x180479f80` final, exactly `rt_isinst`):
- The final's 79-instruction body has 3 exits, all value-returning:
  mismatch falls through to `xor eax,eax` (`0x18047A051`, NULL),
  with the System.Object short-circuit `cmove rax,rdi` and match
  `mov rax,rdi` (object), null input `xor eax,eax` (NULL). Its 6
  calls are IsAssignableFrom/interface-resolve/indirect slots --
  no exception/throw helper is invoked anywhere.
- R8 appears only as `lea r8,[rsp+30h]` / `mov r8,[rsp+30h]`
  (callee spill/scratch); R9 never appears; no incoming stack-arg
  home is read. The helper consumes exactly RCX (obj) + RDX (klass),
  so dropping trailing spray args is sound (same proof shape as the
  array-addr and class-init trims).
The 4 landed tail folds stand on this evidence. Everything else in
the foreign verdict stands unmodified: Obi discarded-result
statements gain nothing from `as` (decline kept), non-klass `_call`
kinds still decline via the kind gate, and the sibling addresses
outside `rt_isinst` (e.g. `0x1804346B0`) can never fire the gate --
whatever their semantics, today's `sub_` spelling holds there.

## Current work: Dec F5 residuals R1-R4, guarded (2026-10-02, LANDED)

Four verified-red literals/comments-blind substitutions beyond the
landed Dec F5 families: `_fix_select` appending ` : default` inside
comments (R1), `_strip_dangling_default` stripping `: default` inside
comments (R2), `_rewrite_unknowns` rewriting `?` operands inside
comments (R3), and `_len_sugar` matching `*(a + 0x18)` with no masking
at all -- including inside string literals (R4, the only one touching
literal bytes). All four reproduced red on `main` with in-memory
probes before the fix; code-fire controls fired throughout.

Guards mirror the landed fix (match on the NUL mask, splice into the
original by offsets): R1 scans the mask and re-masks after each
insertion; R2/R3 copy masked spans through at the char-walk top (the
old quote-skips stay as dead-but-harmless); R4 matches `_LEN_RX` on
`self._mask_literals` output and splices via the highlevel
`_sub_outside_literals` twin (function reps supported), so no new
import was needed.

Evidence (paired `--only Assembly-CSharp` strict builds on the
landing base): 490 types / 6622 bodies / 0 failed / 0 structured
fallbacks both sides; recursive per-file diff exactly 3 files / 24
lines, every changed line inside a dead-placeholder `//` comment
(`unknown` -> raw `?`, the honest-raw direction; strict check: 0
changed lines carry `?`/`unknown` outside `//`). Tree-wide static
census over r11 `final_out` (11,183 files) bounds it: 0 R4-shaped
literal lines, 23 R2-shaped + 57 R1-shaped comment lines (mostly full
ternaries the old gates already declined on).

Gates: brace 0 unbalanced / 490; parse 0 bad / 0 ERROR / 0 MISSING
(JSON); goldens 64/64 post-regen (exactly one move: mi-80548
`Execute`, 56 -> 56 lines, all 17 diff lines in dead-placeholder
comments, zero real code -- read line by line); portable 1217 passed
/ 0 failed (20 new + 6 mixin); full suite 1458 passed with only the
pre-regen mi-80548 golden failing, then 64/64 post-regen (same
protocol as the Dec F5 landing).

Tests: +20 (`tests/test_decF5_residuals.py`: each family x
string/verbatim/line-comment/block-comment byte-identity plus
code-fire controls, incl. the R4 splice case where code folds and
the comment survives on one line).

Still open: the `_call` text-exact typeof fallback (non-klass kinds);
Cpp2IL side B (spec + side-A tools landed by others); single-field
follow-ups and dispatch in flight elsewhere; sidecar next phases.

## Current work: IsInst tail-path `as` fold, slice 2b (2026-10-02, LANDED)

Direct tail jumps to the proved IsInst helper (`rt_isinst =
{0x180434690, 0x180479f80}`) with a klass-kind bare `typeof(T)` klass
now fold to the managed `(obj as T)`, mirroring `_call`'s long-standing
intrinsic exactly (same kind + bare-typeof gates; spray tail dropped by
the same early return). Opaque klass tails keep the honest `sub_`.
The gap was structural, not textual: the dec direct-tail path
(`il2cpp/dec/analyze.py`, `_call_name` branch) rendered every tail
through `_emit_tail` with no intrinsic check, so klass-kind typeof
tails could never fold -- even though the value already carried the
exact proof `_call` demands. Found by tracing mi 3446
(`System.Attribute.GetCustomAttributes`, 4-arg spray tail) through
three silent hooks: the lifter `JMP`/`_call` paths never see direct
tails (dec intercepts first), and `rt_isinst` recognition was fine.

Evidence (paired `--only mscorlib,System.Xml,PhotonVoice` strict
builds on the landing base): 2072 type files / 18362 bodies / 0 failed
/ 0 structured fallbacks both sides; recursive per-file diff exactly
4 files, each a single-line fold with spray-DCE and redundant-cast
collapse (mscorlib `Attribute.cs` x2 `GetCustomAttributes`,
`XPathNavigator`/`XmlReader` `IXmlSchemaInfo` getters,
PhotonVoice `Recorder` voice getter); file sets identical. Tree-wide
static census bounds it: 4 tail-form sites in 36 images with any
typeof shape (the 10 Assembly-CSharp sites are call-form and
untouched -- paired AC build 0/490 changed).

Gates: brace 0 unbalanced / 2072; parse 0 bad / 0 ERROR / 0 MISSING
(JSON); goldens 64/64 unmoved (zero overlap with folded methods, no
regen); portable 1197 passed / 0 failed; +2 game pins
(`tests/test_game_isinst_tail.py`: mi 3446 fold, mi 200 field-klass
decline); full suite 1437 passed with 2 failures both PROVEN
environmental (below) and individually green: effective full green.

Repo-level finding (not mine, recorded): `test_game_decl_gate` and
`test_game_compile_gate` REQUIRE the gitignored local `final_out/`
tree (promotion built it in the main workdir only). Fresh worktrees
lack it, so decl-gate extracts 0 files ("missing emitted type") and
compile-gate fails its `tree.is_dir()` assert. Both fail identically
without any source change and pass once the subdirs are materialized
(decl-gate 4.4s, compile-gate 0.7s in-worktree; both green on main).
Future worktree gating must materialize `final_out/<images>` first.

Tests: +2 game (fold + decline pins above).

Still open (isinst program): slice 2 `_call` text-exact fallback for
non-klass kinds (17 sites, needs settled `calls.py`); loop-carried
proof loss (~25, dry-header fixture still wanted -- the 6 primitive
pins hold); field-store identity (91, needs callee-store analysis).

## Current work: iface-zero probe mi5694 -- FIXED on main, probe CLOSED (2026-10-01, DOCUMENTED)

The OPEN probe (lines 408-420: `customFormatter12 == 0`, untyped
indirect-call temp at TEST time, single TEST / zero CMP-reg-0) is fixed
on `main` 572c8d4 with no source change. Fresh lift
(`tools/inspect_methods.py --mi 5694 --save`, 2026-10-01) renders
`if (customFormatter12 == null)`; controls hold (`obj83 == 0`,
`readOnlySpan11 == 0` per `tests/test_game_null_zero.py`). The analyze
TEST-null gate correctly declines the untyped temp at flag time
(`_test_is_value` False for te 0x12/kind obj; `values.py:911-929`,
`insn.py:1220-1224`, `analyze.py:192-212`), then `_null_zero_rewrite`
(`flow.py:1203`, wired `structure.py:197`) fires downstream on the
unique `System.ICustomFormatter` decl (`_eq_typedef_map`,
`highlevel.py:2598`). Pins green: 52 passed
(`test_game_dry_merge` + `test_game_null_zero` + `test_null_zero` +
`test_loop_proof` + `test_single_field`); full suite 1437 passed;
goldens 64/64. Probe closed; no further action.

## Current work: sidecar 112 + (2)/(3)/(4) -- honest kills, coverless by construction (2026-10-01, DOCUMENTED)

Repro on `main` 572c8d4 (`PYTHONHASHSEED=0`): `tcensus.py FIMSpace`
1017 methods / 4801 sites (fwd:sliceless 2669, fwd:divergent 922,
loop:fwdU+backNoSl 296, loop:fwdU+backSlDiff 239); `dropprobe.py` 112 =
80 retiled-someNoSlice / 15 retiled-allslice / 9 killed (5
`_stack_store` + 4 `_call`) / 5 absent-at-dry-header / 3
vanished-no-event -- byte-exact match for the 333->112 fix. No source
change; the 112 are honest, and (2)/(3)/(4) are blocked without sidecar
use->def:
- 80-bucket: sample mi29353 `!mem:-740:4` -- dry stores are genuine
overwrites (`*(this+0x78)`, float expr `(300,…)`, `s_0`, all sliceless;
`dropprobe2.py 29353 -740 -736`) bearing no relation to the forward
tile (`v128`). Keeping the forward tile would claim a struct tile where
a float was written -- unsound. Honest divergent; decline stands.
- (2) 105 `?`: back-value census gives 97 `?` + 82 missing
(nonexpr/None). Sample mi29353 bid 18 `!mem:-624:4`: fwd tile
`(t1002.z, 0, 4, closed)` vs single back `?`. Dry body stores
`t1047.z` (sliced) but the back edge is `?` -- killed later in-body by
`_stack_store`/`_call` (killer stats above). A dry-header fixpoint
re-propagates `?` and still diverges. Honest; no fixpoint.
- (3) renumber-tolerant: dry/real renumbering proven at identical IPs
(mi29353: DRY `t1001`/`t1047.z` vs REAL `t1002`/`t1083.z` @0x180646d04 /
0x1806476e3). Normalizing temp numbers unifies distinct temps sharing
a shape (two structs' `.z`) -- unsound without def-use proof. Sized ~5%
(26/535 then, ~12 of 239 now). Declined; needs sidecar use->def, not
text compare.
- (4) first consumer: zero unanimous sliced-both-sides sites in census
(no `fwdU+backSlSame` bucket; only `fwdU+backSlDiff` 239,
`fwdNoSl+backSlDiff` 216, `fwdDiv+backSlDiff` 2). `_tile_proof_for`
(`expr.py:104`) requires unanimous texts and runs only on the phi path,
which exact-unanimous tiles never take -- coverless by construction, so
wiring `_piece_value` offset-0 changes nothing. Blocked on (2)/(3).
Next: sidecar use->def per-arm types + field sidecar (large, deferred
by design); Cpp2IL side B (external binary); Megabonk 46 (awaiting
method list/binaries). Suite: full 1437 / portable 1197 / goldens 64 /
targeted 52, all green; 0 goldens moved.

## Current work: dry-pass merge keeps frame address + unanimous tiles (2026-10-01, LANDED)

Answers census next-step (1) below ("why does the dry loop body drop the
`!mem:` key"): it is neither kill nor clobber. Pass 1's merge
(il2cpp/dec/analyze.py) rebuilt every merged value as `Expr(text)`, so
an RBP / RSP-copy base lost `_stack_offset` at the first CFG merge.
`_stack_address` then returns None and every later `[base+N]` in the dry
pass takes the legacy disp-keyed slot (`&s_50` where pass 2 says
`&s_b0`, mi 29353 @0x180646d04), so the sret `_stack_store` never runs
and the dry back-edge carries no tile at all. Probe
(`%TEMP%\opencode\dropprobe.py`: TrackingDict on dry `L.regs` + per-block
start snapshots) on the 333 FIMSpace missing-key sites: 249 absent at the
dry header (this cause), 81 retiled, 3 other, 0 killed.

Fix, pass 1 only: on a unanimous-text merge keep `_stack_offset` when
every pred agrees on it, and for `!mem:` keys keep `_slice`/`_bytes`
when `_tile_proof_for` proves a whole-tile (same origin, closed type,
offset, width, bytes) -- the dry analogue of `_dry_proof`. FIMSpace
re-census: missing back keys 333 -> 112 (80 retiled-sliceless, 15
retiled-sliced, 9 killed by `_stack_store`/`_call`, 5 absent, 3 other);
loop sites with a sliced back edge 3 -> 457.

Gates: paired scoped builds vs `main` 02cf261 (HEAD worktree). Assembly-
CSharp 493/493 files, sets identical, 14 changed, -77 lines; `unknown`,
`goto`, `sub_`, `((byte*)` flat; `object obj` -8. mscorlib 1353/1353,
57 changed, -778 lines; `unknown`/`goto`/`sub_`/`= default` flat,
`object obj` -115, `((byte*)` +35 (re-inlined loop-invariant klass
loads, e.g. TypeSpec's dispatch loop condition, where the phi temp
disappears). Read diffs: loop-invariant `this`/param copies stop being
phis (SaveManager `saveManager1..6` -> `this`, MiscHelpers `list11 =
source`, Rijndael `byteArray18` -> `inputBuffer`, mi 5694
`stringBuilder1.Append` -> `this.Append`), and TypeSpec's interface
dispatch result stops aliasing the enumerator phi (`list13 = list14` ->
`obj28 = <dispatch address>`). Brace 0 both trees. Suite: 1432 passed /
3 failed, all three reviewed renumber-only moves (mi 80548 comment
`vN` shift, golden hash-synced; mi 5694 pins `obj172/obj76` ->
`obj171/obj75`, `obj84` -> `obj83`), re-run green; +2 game pins
(tests/test_game_dry_merge.py: dry RCX keeps `&s_b0`/-632; mi 5694
`this.Append`). Portable 1197/1197.

Note: a pure field-load text now survives where a phi temp used to pin
it (FusionNetworkManager `action11` -> `pendingSpawnCallback1._callback`
read after an interface call). That is the decompiler's standing model
for unanimous texts, not new to this change, but it is visible here.

Next: the remaining 112 (80 retiled-sliceless: dry stores whose value
has no slice re-tile the range; look at `_scalar_parts` on dry values),
then re-run tcensus for the `fwdU+backSlDiff` 239 bucket (dry
renumbering `t1000` vs `t1001` -- step (3) below is now the larger
share), then the first consumer.

## Current work: sidecar consumer redesign -- census (2026-10-01, OPEN)

Why phase 1 is coverless: `_tile_proof_for` is only reached on the phi
path (il2cpp/dec/analyze.py pass 2), which only runs when pred texts
differ -- an exact unanimous tile has identical texts and never becomes
a phi. The record cannot fire by construction; wiring a consumer to it
changes nothing.

Census (spy on `_tile_proof_for` + caller-frame rpo/preds; script
`%TEMP%\opencode\tcensus.py <ns> <cap> <out.json>`), FIMSpace, 1,017
methods / 4,212 `!mem:` phi sites, 15.5 s: fwd-only sliceless 2,423,
fwd-only divergent 921, loop sites 868 (fwd-unanimous + sliceless
back-edge 535; fwd-sliceless 266+19; fwd-divergent 45; back sliced but
different 3). The 535 bucket, by back-edge (dry end_state) value:
missing key 333, dry-divergent `?` 105, genuinely different 70,
renumber-only 26 (`t1001.z` vs dry `t1000.z`), same text 1.

Next: (1) find why the dry loop body drops the `!mem:` key (333) --
kill/clobber vs never-set; (2) dry-pass merges keep `_slice` the way
`_dry_proof` is kept (analyze.py ~line 478) and iterate the dry header
to a fixpoint for the 105; (3) renumber-tolerant same-tile compare is
only ~5% of the bucket; (4) first consumer = the declined
`_piece_value` offset-0 unwrap, re-measured with paired
Assembly-CSharp gates.

External input (Megabonk port notes, Unity 2023.2 / metadata v29):
46 struct temps passed as `default` after dropped stores (e.g.
`AegisRenderer.SetAmount`) -- real miscompile, not reproducible here
yet (asked for the method list / binaries). Same patterns counted in
r11 Assembly-CSharp (490 files): empty `typeof(T).initialized` guards
2,962 of 2,999 (cheap, safe cleanup), raw `((byte*)x + 0x` 6,076,
`__field_` 4,098, inlined Unity statics (`upVector` etc.) 1,144,
`op_Multiply(` 92, `/*vtable slot` 30, `sub_` calls 1,585.

## final_out promoted to r11 (2026-10-01)

Rebuilt from `main` `1cafd3f` (strict, 8 workers): 11,183 files / 114,458
bodies, 0 failed / 0 fallbacks; brace 0; parse 0/0/0; 2,838 files changed vs
r10 (0 added / 0 removed). 11,276 files, aggregate `735f2e9a…1707f`, 0
mismatches (`validation_reports/promotion_r11.json`). r10 tree kept outside
the repo for rollback.

## Current work: twin single-field-return relax + box-only hetero guard (2026-10-01, LANDED)

Closes the DEFERRED twin item below (branches `twin-guard-wip` +
`twin-hardening`, squashed onto `main`). Two halves:

- **Twin relax** (`il2cpp/lifter/calls.py`, the resolved-dispatch
  return gate): single-field struct returns now flow whole; only
  unreadable typedefs/field chains decline. Consumers that want the lane
  still get it through F2-C1 (decls) / F2-C2 (call args). This resolves
  the `sub_180006590(14, typeof(IConvertible), c, p)` dispatch to
  `c.ToDateTime(p)` (Convert.cs x4, mi 86310).
- **Hetero-decl guard** (`il2cpp/dec/highlevel.py` `_rename_locals`,
  `_hetero_decl` / `_hetero_vetoed`): a namespaced decl whose slot takes
  >= 2 distinct non-derived closed types from single-identifier RHS
  assignments is printed `object` -- but ONLY when every read of the temp
  is a boxing use. Box-only rule: mask the def (`X =` / `T X =`),
  `(object)(X)` / `(object)X`, builtin object members
  (`ToString/GetHashCode/GetType/Equals`), an object-method `return X;`,
  and `&X` either bound to an `object` binder (undeclared/`var` binders
  resolve through `_decl_type_of`: mi 1242 `v188 = &s_10;`) or passed to
  an unresolved `sub_<hex>(...)` helper (innermost enclosing call; no C#
  signature, no parameter type). Any other occurrence vetoes: ref/out/in,
  members, indexers, typed returns, call args incl. generic
  (`TryGetArray<byte>(X, ...)`) and nested-paren calls, field/element
  stores (`_activator = X`), arithmetic (`X * k`), casts, compound
  assigns, plain copies. Subclass tolerance via `base_chain_tds`.

mi 1242 (`Convert.ChangeType` box-staging slot `s_10`, every arm writes
then `&slot` -> object binder / helper): today's `object obj1` is kept
while the ToDateTime arm resolves (`DateTime dateTime1 =
convertible1.ToDateTime(provider); obj1 = dateTime1;`). The first
candidate (twin + guard + helper/binder exemptions, no box-only rule)
retyped 7 more mscorlib/Assembly-CSharp files with typed consumers
(Decimal `Buf16` -> `object obj6`, MemoryStream/UnmanagedMemoryStream
`ReadOnlyMemory`, RuntimeType `BindingFlags`, ActivationServices
`IActivator`, TaskToApm `IAsyncResult`, LAM_DirectionalMovement) --
the box-only rule cleared all of them.

Gates: paired scoped builds vs `main` 19916ac (mscorlib +
Assembly-CSharp, 1844/1844 files, file sets identical; 17337 bodies,
0 failed / 0 fallbacks / 0 type-emit failures): 2 files changed --
Convert.cs (exactly the 4 `ToDateTime` dispatch recoveries) and
PlatformManager_Steam.cs (renumbering, one pure-copy fold
`CSteamID cSteamId2 = num1; (object)(cSteamId2)` -> `(object)(num1)`
x3, and 3 stores `cSteamId2 = <GetSteamID temp>;` dropped -- each
proven dead in text: no read of `cSteamId2` before the next sibling
decl). Brace 0; parse 0 bad / 0 ERROR / 0 MISSING. One golden moved
and was read: mi 86310 `DateTimeStorage.Set`, the single line
`(DateTime)sub_180006590(14, ...)` -> `convertible1.ToDateTime(
formatProvider1)` (no `._dateData` projection; the 2026-09-28 hazard
stays closed). Tests: tests/test_hetero_veto.py (21: escape/member/
return/call-arg vetoes, boxing carve-outs, subclass tolerance, helper
`&` + undeclared-object-binder exemptions, value-read/field-store/
generic/nested-paren vetoes); goldens hash-synced for mi 86310 only
(64/64 after sync); full suite 1435 passed / 0 failed (pre-sync run:
1434 + the one reviewed mi 86310 move).

Still open (unchanged by this landing): sidecar consumer redesign
(dry-pass tile proofs for loops, same-tile-respell detection) -- the
natural home for per-arm types that would also unblock the
primitive-hetero guard; Cpp2IL side B.

## Current work: single-field call-arg fold F2-C2 + interface-zero (2026-10-01, OPEN)

Second slice of the single-field use-proof, plus the interface-zero
close. F2-C2 folds `Foo(X.f)` to `Foo(X)` at struct-typed params
(`Lifter._single_field_arg`, il2cpp/lifter/calls.py: pure decision --
exact param/arg tuple match, closed non-enum single-field VALUETYPE
holder, field-name match, bare `X.f` only; generic/sret/arity/byref/
call-base/unknown declines at the `_call` site). C1
(il2cpp/dec/sugar.py) and C2 both require `is_valuetype` (audit
close: a single-field reference holder is a field load, not the whole
value).

Interface-zero textpass (`_null_zero_rewrite`, il2cpp/dec/flow.py,
wired outermost in il2cpp/dec/structure.py): `X == 0` -> `X == null`
when X's unique declaration spelling resolves to a non-valuetype
non-enum non-Object type (`_eq_typedef_map`; unique shorts count,
strings fire, `object` declines). Slot-reuse veto (nonzero numerics,
true/false, literals, primitive-declared RHS, `&`/ref/out/in
escapes); yoda/`!=` fold in place; mask-then-splice throughout. mi
5694 `customFormatter12 == 0` was an untyped indirect-call temp at
TEST time; the declaration knows `System.ICustomFormatter`.

DEFERRED with evidence (since LANDED -- see the section above): the twin single-field-return
relax + decl-heterogeneity guard. The twin resolves dispatch sites
(Convert.cs `convertible1.ToDateTime(provider)` x4) but retypes mi
1242's box-temp; the guard fixed that yet fired on slots with typed
consumers (paired mscorlib + Assembly-CSharp diffs, 31 + 14 files:
`ref Vector3` -> `ref obj`, typed call args `TryGetArray(obj11)` /
`Synchronized(obj13)`, `return obj5` for Component, an unproven
dropped store in PlatformManager_Steam). Next: consumer vetoes
(escape, non-boxing call args, member reads) + subclass tolerance,
then re-measure. mi 86310 keeps today's lane spelling meanwhile
(golden untouched).

Gates: paired mscorlib (1353/1353 files, 19 changed, file sets
identical; 10715 bodies, 0 failed / 0 fallbacks / 0 type-emit
failures) + Assembly-CSharp (493/493 files, 3 changed; 6622 bodies,
0 failed); every hunk an `X == 0` -> `X == null` rewrite on a proven
reference decl (no retypes, drops, or renumbers); brace 0 both trees;
parse 0 bad / 0 ERROR / 0 MISSING both trees; goldens 64/64 unmoved;
suite 1377 passed / 0 failed. Tests:
tests/test_single_field.py (18: C1 + C2 fire/declines + valuetype),
tests/test_null_zero.py (22), tests/test_game_null_zero.py (mi 5694 +
obj84/span controls), goldens hash-synced (no moves; mi 5694 not in
set).

Open follow-ups: primitive-hetero guard (bool-numeric 95 sites, no
implicit conversion either way; spec'd; repro MI 807 pure `bool
flag1 = num1` decl copies + MI 113095 `int num1 = flag3` slot-reuse;
te-exact trigger, narrowing-only int-float, declaring-RHS vote --
BUILT, then REVERTED with evidence: both repros `return` the temp
into bool methods, so object-ifying trades 15 broken assigns for 1
broken return with no net compile win; vetoing returns leaves zero
known fires. Needs sidecar/use->def per-arm types (or duotone
temps), not a decl-level rule; scripts in temp scratch); `default\b` veto-boundary hardening (LANDED in the zero
pass); single-field v2 stores LANDED (`_single_field_store` pure
helper + plain-path (`_write_mem`, holder type from base temp) and
barrier-path (`_wb_operands`, name-match + pointer-size proof)
wirings, display-only with raw-text bookkeeping; latent on this
corpus -- paired mscorlib (1353 files) + Assembly-CSharp (493
files) 0 changed, file sets identical; brace 0; parse 0/0/0;
goldens 64/64 unmoved; suite 1417/0; returns/byref stay declined);
twin+guard LANDED 2026-10-01 (box-only reads rule; section
above); isinst slice
2 (fence helper `_bare_typeof_target` LANDED + 9 pins; `_call` gate
DECLINED with a full-tree census (11,183 files / 114,458 bodies):
exactly 17 typeof-carrying `sub_180434690` sites, all declined --
9x Obi checked-cast with discarded result (arity 4), 5x cast-with-
context `return (T)sub(obj, typeof(T), a, b)` (arity 4; folding to
`as` would trade throw for null), 2x Attribute (arity 4 / wrapped
`GetTypeFromHandle`), 1x Recorder (arity 4). Trimming the extra
args as spray is unsound: castclass-throw vs `as`-null diverge
exactly where the result is discarded or cast. Markers stay
honest); decl-gate v2 field-statics LANDED (`F s=` both sides via
`field_attrs`, enum members exempt s=0; 15 portable + tiny e2e green,
mscorlib 18,894 decls 0 problems) + property/event rows LANDED
(`P s/get/set`, `E s/add/rem` both sides, mirrored on emitter truth:
indexers as bare `this`, incomplete event pairs skipped, expression
bodies count as getters; 19 portable incl. snippet-extract pins +
tiny e2e green, mscorlib 20,874 decls 0 problems, 0 skipped) + delegate Invoke rows
LANDED (dump stops filtering Invoke on pure delegates, full M grammar
reused with zero parser changes; extract synthesizes one Invoke M
row per delegate_declaration; 21 portable incl. arity pins + tiny
e2e green, mscorlib 20,934 decls 0 problems, 0 skipped) + full
type-spelling `--strict-types` LANDED (extract type tails, spell
side-maps through parse/norm, `canon_full` keyword/qualification/
arity/mangled-name tolerant with signatures/tuples/generics/suffixes
decomposed, spell-preferring multiset pairing; default path
bit-identical; 24 portable incl. strict pins + tiny e2e green,
mscorlib default 0, strict 0 problems) + compile gate LANDED
(syntax-vs-binding split with exit codes; 6 portable incl. fake-
compiler plumbing + game mscorlib syntax==0 green; 1350 files,
0 syntax, 40 binding residuals); sidecar phase 1 record LANDED
(`_tile_proof_for` pure primitive + merge-side attach on unanimous
`!mem:` tiles, `__slots__` + default; no consumer reads it yet;
paired Assembly-CSharp 493/493 files 0 changed, file sets identical,
brace 0; goldens 64/64; portable 1176 + full suite 1414/0; 11 proof
pins; census over 26 merge-heavy methods: 777 merge sites, 0
exact-unanimous (354 partial-presence incl. loop headers, 219
asymmetric-slice, 204 divergent) -- the record is honest but
coverless as designed; consumers need redesign (dry-pass tile
proofs for loops a la `_dry_proof`, same-tile-respell detection),
not wiring; open next); Cpp2IL
side B (external binary).

## Current work: single-field assign fold F2-C1 (2026-10-01, LANDED)

First slice of the single-field use-proof: `T t = X.f` (decl or plain
reassignment) folds to `T t = X` when T is a closed non-enum
single-field value type, f is its single field, and X resolves to T
(lifter maps, body decls, or method params; exactly one type each).
Int/ulong/object/enum consumers, unknown types, call/complex bases,
multi-field structs and multi-def temps keep today's spelling;
literal/comment masking throughout. Placement after `_selfcopy_drop`
(copy-prop transparent) so folded decls drop via `_drop_dead_locals`.

Gates: paired scoped builds (mscorlib + Assembly-CSharp): 4 files
changed, file sets identical, all 12 hunks genuine single-field
recoveries (`TimeSpan ts = offset`, `DateTime dt = dateTime`,
`CancellationToken ct = cancellationToken`, `PlayerRef pr = player`,
incl. reassignment shapes) with renumber-only cascades; brace 0;
parse 0/0/0/0. Goldens 64/64 unmoved. Suite 1345 passed / 0 failed
(+9 portable `tests/test_single_field.py`, +3 game
`tests/test_game_single_field.py` incl. the `ulong`-lane control
that must keep its lane). Next: C2 call-arg fold, then the twin.

## Current work: IsInst A2 sugar twin -- probed, census-closed, DECLINED (2026-10-01, DOCUMENTED)

The 21 `arr.getClass() + 0x40` sites (getClass sugar for the klass
load instead of `[arr]+0`) cannot fold without newarr-exactness, and
none has it. Provenance census of every klass source (9 arrays across
8 methods): 5× shared-body call results (`sub_182b9e210(...)`, mi
24722/24730/24862/28097/27318), 2× temp copies of params/fields
(`= nodeArray2`, `= valueArray1`, `= dataRowArray1`), 1× untyped call
result, 9× field (`this.touchControlArray`, FastTouchscreen). Zero
same-method newarrs. A fold to `typeof(E)` on any of them mistypes
when the tested object is E-but-not-D (the E[]-typed local holding a
D[] at runtime still yields D's element klass, and `as E` vs `as D`
diverge exactly there), so the honest `sub_` markers stand. Same
exactness bar as landing 9; the relief is field-store identity /
sidecar (family 2), not a weaker fold -- none exists (there is no
klass spelling weaker than `typeof(E)` that the IsInst fold accepts).

## Current work: Cpp2IL declaration gate, side A landed (2026-10-01, LANDED)

The proposed-but-never-filed cross-check now exists as three tools
plus tests: `tools/dump_decls.py` (canonical per-assembly declaration
dump from metadata: CLR owner paths, kind, emitter-mirrored base
(parent omitted for enum/valuetype/interface/delegate/object-parent),
enum underlying keyword, full member signatures with flags, fields via
`source_field_name`), `tools/extract_decls.py` (tree-sitter parse of
emitted files into the same grammar: namespaces, nesting, enum
members, ctors/dtors/operators/conversions mapped, properties/events
skipped like their folded accessors), `tools/diff_decls.py`
(structural compare with emitter-exact normalization: render +
file-boundary mangle rules imported, not reimplemented; nesting dots;
first-interface-as-base; two-pass member matching with tail +
qualifier compatibility and multiset counts; exit code gates).

Validated: tiny image (Unity.Burst.Unsafe, 41 decls) byte-stable dumps
and zero diffs; mscorlib (18,894 decls both sides) zero problems after
driving out nesting namespaces, accessor/delegate exclusion, enum
members/underlying, explicit-impl qualifiers, backing-field renames,
first-interface order, and generated-name mangling. Gates: 14 portable
+ 1 game (tiny end-to-end) green.

Side B (open, external binary): run Cpp2IL on the same fixture dump,
reduce its reconstructed DLLs to this grammar (reflection FullNames
map to CLR owner paths; signatures to the M/F shapes), diff. v2
(open): property/event rows both sides, full type-spelling compare
(currently structural: names/arity/staticness/counts, short outers),
field static flags, delegate Invoke-shape rows, compile gate.

## Current work: IsInst slice 3 (initmeta-wrapper klass identity) -- probed, KEEPER (2026-10-01, DOCUMENTED)

The 15 initmeta-wrapper sites stay as-is: none of the wrappers behind
`il2cpp_codegen_initialize_runtime_metadata` preserves its RCX klass
across the internal call, so a `call_wrapper(typeof(T)) -> typeof(T)`
fold would be unsound. Per-VA verdicts (native extents + decodes):
- `0x180435400` (named outer): single-ret but passthrough, not
  identity -- RAX is the inner call's return, never restored from the
  RCX spill. Needs inner proof, which fails.
- `0x180490FB0` (named inner): not single-ret (0 rets; `mov dl,1`
  + tail-shim to `0x1804455C0`), preserves nothing into RAX.
- `0x1804455C0` (real routine): multi-exit via jump-table; the
  fast path returns `*slot` (deref after `lock xadd`), not RCX, and
  the slow path returns a computed RBX with a store. The
  `mov-rax-rcx` identity is affirmatively FALSE (slot address is not
  the klass value).
Call-site sample (mi 24167; 23994 is a 2-insn thunk, 24742 a
forwarder): `lea rcx,[slot]; call` x2 with RAX discarded and the slot
re-read from memory -- the RAX-read-back shape is absent. (The
`0x18043E360` class-init helper fast path IS `mov rax,rbx`
identity, but that is a different chain.) No source change, no
goldens moved. Resurrection would need a wrapper proved byte-identical
to an identity shape, none observed.

## Current work: `_piece_value` offset-0 slice -- probed, built, measured, DECLINED (2026-10-01, DOCUMENTED)

The `_slice` unwrap in `Lifter._piece_value`
(il2cpp/lifter/aggregates.py:94-96) skips `sl[1] == 0`, so offset-0
fragment chains never reroot to their base (inconsistent with the
`_scalar_parts` sibling, which unwraps all slices). Three guarded
variants were built in the `piece0` worktree and measured with paired
`--only Assembly-CSharp` strict builds (490 types / 6622 bodies /
0 failed / 0 fallbacks both sides) plus recursive per-file diffs:
- v1 (unwrap all contained slices + overhang decline): 16/490 files
  changed, `unknown` 1338 both sides (delta 0).
- v2 (+ only unwrap unrefined chains by text equality): 14/490.
- v3 (+ offset-0 only when `origin.ty is None`): 14/490, regressions
  persist -- the miscompiled frags are untyped too.
Regressions (decline reason): dropped scalar lanes
(`vector34 * vector34.x` -> `vector34 * vector34`,
`vector33.x`/`vector31.x` -> whole vector where a float is required)
and a re-pointed base (`Vector3.zeroVector.z` -> `vector34.z`) on
merge-heavy FIMSpace sites. Mechanism: unwrapping exposes the lossy
whole-vector phi path (offset == 0 returns the whole origin text) at
sites where the old fall-through declined honestly. No guard on this
unwrap is safe without merge-side provenance (sidecar phase 1); the
benign hunks in the same diff (repeated-expression hoists,
`Vector3.upVector` component recovery) do not justify the miscompiles.
Reverted in full (no source residue).

Kept: two regression pins (tests/test_recovery_followup.py:
zero-offset slice resolves through base, overhang declines) that hold
pre/post patch, plus the loop-proof primitive pins. Gates for the kept
pins: portable 1087 passed / 0 failed, game goldens 64/64 on main.

Resurrection path (not planned): merge-side unanimous whole-tile
preservation first (sidecar phase 1), then re-measure; or a
result-checking unwrap that declines whenever the rerooted spelling
is coarser than the frag's own refined text.

## Current work: loop-carried proof primitive pins, test-only (2026-10-01, LANDED)

`_merge_arr_proof` (il2cpp/expr.py:76-94) is the per-input primitive
behind the landing-9 dry-unanimous merge (il2cpp/dec/analyze.py:479-484):
live `_newarr` + ty or `_dry_proof` (ty, True) proves exact, everything
else declines (params/fields/statics covariance-unproven). Six unit pins
(tests/test_loop_proof.py): newarr fire, dry-proof fire, plain decline,
newarr-without-ty decline, malformed-dry-proof decline, non-Expr decline.
No source change, no goldens moved. Gates: 6/6 new, portable 1085 passed
/ 0 failed (231 game deselected), game goldens 64/64 still green on main.

Still open: dry-header merge-level fixture (entry proven + latch dry
end_state at loop header, unanimous vs divergent vs entry-unproven
discriminants); field-store identity (91, needs callee-store analysis);
slice 2/3; single-field use-proof; sidecar phase 1 (merge-side unanimous
whole-tile, analyze.py-owned); Cpp2IL side B; parallel-build residual.

## Current work: interface-zero probe (2026-10-01, OPEN)

`if (customFormatter12 == 0)` (mi 5694, pre-existing) is NOT the
TEST-null rewrite: a spy on every `_test_is_value` call during the
lift shows the single customFormatter test (an `as`-result,
te 0x12, kind `obj`) correctly returns False, and disassembly shows
exactly one TEST and zero CMP-reg-0 in the method. A guard extension
to all reference tes (0x12/0x14/0x1c/0x1d) changed nothing and was
reverted to the proven 0x0e/0x0f guard. Remaining suspects: a
rename-desync (condition built on an int-kind temp later renamed to
the interface-typed name) or a non-TEST/CMP flag source. Needs a
lift-time (kind, ty) trace at the exact flag-setting instruction.

## Current work: bounds slice B (`arr[i].field`) -- probed, built, measured, DECLINED (2026-10-01, DOCUMENTED)

Slice A named `il2cpp_array_addr(arr, idx)` (764 sites). Slice B would
fold `((W*)addr + 0xK)[0]` to `arr[idx].field`. Designed twice:
first lifter-side (addr-proof on Exprs, mirroring landing-9), then --
after the reassignment analysis showed temps are SSA-frozen but field
idcs are not -- as a dec text pass (`_array_index_fold` after
`_selfcopy_drop`) with per-use intervening-write scans (redefinitions,
ref/out/&, foreach/catch binders, calls for dotted tokens,
return/throw; loop trips containing the use extend the scan instead
of declining). Stride needs no check (compiler pairs helper stride
with element size by construction; field offsets are layout-fixed).

Measured on TextMeshPro (135 types / 1,743 bodies / 0 failed):
**0 folds from the pass** (330 addr sites remain; the 6
`arr[i].field` shapes in TMP_Text are pre-existing inline
`_arr_elem_expr` renders). Root cause, proved with per-rule
attribution on mi 96741: the population is loop-carried -- addr temps
defined once before goto/brace loops, used across trips with a
per-trip-incremented field index (`this.m_characterCount += 1`
caught live by the scan twice). Folding those reads the fresh index
against the frozen address: silently wrong, not prettier. The scan
is correct to decline; the remaining straight-line population does
not justify ~250 lines of scanning machinery. Reverted in full (no
source residue); no goldens moved; suite green before/after.

Resurrection path (not planned): field sidecar + use->def proving
loop-invariance per pair, or a straight-line-only variant if a
census shows a straight-line population worth it. Nested-suboffset,
merge-composed proofs and class elements stay open regardless.

## Current work: parameterized dispatch, multi-param + typed-unknown R9 (2026-10-01, LANDED)

The A-family twin (`_param_interface_dispatch`) resolves two more
shapes, both probed with native evidence: (1) multi-parameter targets
recover params 1.. from the Win64 stack homes `[rsp+0x20+8k]` via
`_stack_piece` with per-parameter GPR-class, width (4 for int32, 8
for words) and spelling gates (mi 6160
`TransformFinalBlock(inputBuffer, 0, inputCount)`); (2) a merged
`default`-poisoned R9 keeps the exact declared type under kind `?`
and is accepted only on exact-or-closed type proof (mi 104027
`onSearchPath = action1`, which folds to the setter). Float/double,
struct, byref, generic-var and sub-word stack params decline; stack
recovery snapshots/restores the ambient hint tables so speculative
proving never leaks into declined methods (Blinker-class pollution,
caught by pair diff: 112 files -> 19). The twin's new string-typed
results exposed a latent miscompile: call results classify te < 0x10
by register (string lands on kind `int`), and the analyze TEST-null
rewrite trusted kind over type (`text5 != 0` on a string, mi 5694).
The rewrite now treats the type tuple as authoritative for 0x0e/0x0f
(~993 reference null-tests fixed tree-wide: `s != null`,
`ReadLine() == null`, `bytePtr1 != null`, `ptr == null`).

Gates: paired scoped builds (Astar/mscorlib/Assembly-CSharp, F1-only
vs F1+dispatch+guard): 19 files changed, file sets identical, 22
dispatcher sites resolved, 0 gained, every hunk a resolution +
downstream cleanup (setter folds, `Compare`/`CopyTo`/`Activate`/
indexer renders, stub pruning); brace 0; parse 0/0/0/0. Full strict
build: 11,183 files / 114,458 bodies / 0 failed / 0 fallbacks, brace
0, parse 0/0/0. Two goldens moved and read (mi 5769 `chars != null`,
mi 26747 `Ptr != null`); hashes synced. Suite 1289 passed / 0 failed.

Correction to the 2026-10-01 stride entry: the committed F1 models
(`29ebbd9`, model-only + spellability guard) are sounder than the
quarantine note claims -- Blinker lanes render r/g/b/a-distinct and
all 64 goldens pass on that tree. The earlier 2-golden failures came
from uncommitted working-tree states, not the commit. Open remains
the invalidation half, the `_piece_value` offset-0 slice fix, and
interface-typed zero rendering (`customFormatter12 == 0`, mi 5694,
pre-existing, different path).

## Current work: Dec F5 literal-blind substitutions, guarded (2026-10-01, LANDED)

Four latent corruption families (plus two adjacent call-finds)
rewrote string literals, verbatim strings and comments because they
matched raw line text: `_fold_consts` const folding (F5-1),
`_unsafify` deref rewrites (F5-2), `_render` marker/keyword subs
(F5-3), `_foreach_sugar` element masking (F5-4), plus
`_fold_concat` / `_format_interp` call-head finds. Corpus census:
0 hits over 11,183 files / 3.08M lines -- latent, proven red only on
synthetic vectors (16 fired).

Guards mirror the landed literal-safety fix: match on the mask,
splice into the original by offsets (the `_rename_locals` pattern);
per-line masking (in_block=False) with the documented
spanning-block-comment residual (fidelity-only); `:530`-before-`:699`
order preserved; `idx_rx` disqualification stays on the original
(decline preservation); call heads + paren depth walk on the mask,
parts sliced from the original.
- Mixin robustness: textpass code paths run through partial test
  doubles lacking the composed class, so cross-mixin mask calls die
  (6 pre-existing tests red). Fix is a module-level mask twin in
  textpass.py (no MRO, no self) with structural asserts (mixin
  methods intact, one module fn); highlevel keeps its method
  versions. A v1 mid-class insertion nested the mixin dead (caught
  by the new asserts, never shipped); v2 appends at EOF.
- Adjacent `_UK_RX` is dead (zero references); the live scanner is
  the only site (plus the F1 tail-tolerance already landed there).

Evidence (synthetic red/green, then tree gates):
- Probe vectors (pre-patch RED: 16 fired across the families;
  controls green) become 21 passing unit tests
  (`tests/test_decF5_literal_blind.py`: each family x
  string/verbatim/line-comment/block-comment byte-identity, plus
  code-fire counterparts; F5-4 asserts the literal survives AND the
  fold declines).
- mi-80548 golden moves (the only one): 16/16 diff lines are
  dead-placeholder comment text (`((byte*)v+N)[0]` vs `*(v+N)`
  alternation), ZERO real-code changes (56 -> 56 lines).
- Paired strict builds (--only Assembly-CSharp, dispatch base):
  490/6622/0/0 in 197.5 s vs 164.8 s; recursive per-file diff
  0/490 changed, file set identical.

Gates: paired strict builds (above); brace 0 unbalanced / 490;
parse 0 bad / 0 ERROR / 0 MISSING (490 files, JSON); goldens 64/64
post-regen (1 move: mi-80548 comment-only, read); suite 1309
passed pre-regen (1 golden, accepted move) + 64/64 post-regen
(1079 portable incl. 21 new + 6 mixin tests); sweep 6634 methods /
0 crashes (scoped AC report for regen mechanics).

Tests: +21 new file (byte-identity reds + code-fire greens +
decline-preservation).

Still open: isinst slice 2 (typeof-residual -- needs settled
calls.py; dispatch follow-ups in flight); slice 3 (initmeta --
needs sibling verdict); loop-carried proof loss; field-store
identity; bounds slice B (`&arr[i]`, foreign `_array_index_fold`
in flight); single-field returns (needs F2 use-proof + analyze.py
consumer recording); sidecar program (phased); Cpp2IL declaration
gate (prototype filed separately); parallel-build residual;
platform scope (deferred).

## Current work: IsInst element-class slice 1 -- closed generic-instance `as` (2026-10-01, LANDED)

The opaque-klass IsInst remainder (~4,666 sites post-landing-9) is
dominated by covariance-barred klass sources (fields, params, statics,
unknowns) and object-element noise. The first closable slice: arrays
whose element is a CLOSED generic-instance class (`StructWrapper_1`,
`IComparer_1`, `List_1`, `Task_1`, `IProcessor_1` on corpus -- zero
struct instantiations, zero open args observed). Landing-9's newarr
proof already fixes the array's runtime klass to exactly `E[]`, so
`element_class` is definitionally `E` and covariance is irrelevant;
the gate is only about rendering `obj as E` legally.

- `_elem_klass_name` admits `te == 0x15` to a dedicated
  `_geninst_as_target` validator: closed (no VAR/MVAR at any depth
  via `_open_generic`), definition typedef non-valuetype/non-enum
  (`Nullable<T>` by construction), readable args, nameable spelling
  (existing object/paren guards reused).
- `_open_generic` deep walk (depth-capped): 0x15 recurses class args,
  0x1d/0x14 recurse element, 0x0f/0x10 recurse pointee; unreadable
  (None) or over-deep reads as open. Bin access is exception-guarded
  so pre-existing bin-less Lifter doubles decline instead of crashing
  (landing-9's `test_gate_genericinst_ptr_nested_decline` pin holds).
- Methodology note: `tools/inspect_methods.py` defaults `--source`
  to the repo, silently voiding worktree lifts (three null-probe
  cycles burned on this). Always pass `--source` explicitly for
  worktree lifts.

Evidence (paired lifts with explicit `--source`):
- mi 113247 StructWrapperPools..cctor: 133 sites -> 0 (535 -> 402
  lines, exactly one line per site; OBJs already closed-typed so the
  folds DCE-collapse entirely, mi-84/471 class).
- mi 105419 PointKDTree..cctor: 3 sites -> 0, read line by line
  (dead null-guarded checks + empty guards + unsafe wrapper drop;
  stores and static assignment identical).
- mi 123638: 1 site -> 0; the gate keys on the PROOF type
  (`IProcessor_1<short>` allocation), not the local's declared open
  type (`IProcessor_1<T>[]`).
- Declines hold: mi 102073 nested arrays (3 sites retained), mi 2717
  object elements (3 retained), mi 200 field (pinned), mi 30694
  field (pinned).

Gates: scoped strict builds (Photon3Unity3D + AstarPathfindingProject
+ PhotonVoice.API/Fusion/Voice: 407 type files / 3848 bodies /
0 failed / 0 structured fallbacks / 0 type-emission failures in
69,595 ms); brace 0 unbalanced / 407; parse 0 bad / 0 ERROR /
0 MISSING; goldens 64/64 (0 moves -- no golden MI folds, no regen);
suite 1285 passed / 0 failed (1055 portable + 230 game); sweep
116178 methods / 0 crashes / into_block 8075/2046 identical to
baseline / tail-args identical (JSON); in-scope remaining
`sub_180434690` call sites 0 (5 stub declarations retained per
image by pre-existing policy); declines live outside these images
per the census buckets.

Tests: +8 portable (`tests/test_native_values.py`: closed fire,
open-VAR/nested-open/valuetype/object/paren/unreadable declines,
direct open-generic table) + 4 game (`tests/test_game_elemclass.py`:
113247/105419/123638 folds, 102073 nested decline) + docstring line.

Still open (isinst program): slice 2 -- typeof-residual text-exact
fold (17 sites); slice 3 -- initmeta-wrapper klass identity (15);
loop-carried proof loss (~25, needs dry-header discriminating test,
not a textual rule); field-store identity (91, needs callee-store
analysis); the covariance kernel stays declined with prejudice.

## Current work: F1 lane modeling, model-only + spellability + unknown tail (2026-10-01, LANDED)

SIMD lane provenance for the audit's F1 (unmodelled instructions leave a
stale destination live: SHUFPS ~1,646 / CVTDQ2PS ~197 live reads in
Assembly-CSharp). Two earlier landings of the invalidation half were
reverted/probed-and-declined (Blinker all-from-.a collapse, mi80548
57->37 `_mk`-cap placeholder collapse, 6 goldens incl. mi32832
float->double). This landing models the lanes and explicitly does NOT
invalidate:

- `MOVSS` reg-reg merges (low lane from src, lanes 1-3 preserved;
  decline keeps today's full copy, never pops -- a copy is closer to
  truth than unknown).
- `SHUFPS`/`PSHUFD`/`UNPCKHPS`/`CVTDQ2PS` decode exact per-lane maps
  (identity 0xE4, broadcast 0x00, reverse 0x1B pinned) into
  UNPCKLPS-shaped `_parts` on a `?`/`bits` dest (zero `_mk` calls, hence
  zero `_mk`-cap pressure -- the mi80548 lesson). Any unproven lane
  keeps today's spelling (falls through to the asm comment, exactly as
  before). Genuinely-unmodelled destinations are still ignored
  silently -- invalidation stays OPEN.
- `_lane_value` spellability guard: a lane carrying the bare `?`/`_`
  placeholder text (unproven value that happens to have parts) declines
  -- stamping it renders `real27 * ?`, which is unparseable
  (LegsAnimator VA 0x180644EF0 gate).
- `_rewrite_unknowns` tail tolerance: the bare-`?`-operand rewrite
  fired only with an immediately-adjacent delimiter; with a space
  before it (`real27 * ? }`) the `?` survived. The head side already
  skips whitespace and real ternary/select marks are excluded by the
  prev/back value check first, so tolerating whitespace before the
  delimiter class (plus the missing `}`) only widens unknown-operand
  rewriting. `_UK_RX` is dead (zero references); the live scanner is
  the only site.

Evidence (paired HEAD-baseline lifts, same scoped tree):
- Blinker mi23906 LateUpdate: g/b/a channels recover per-lane
  `(original.g - color.g)` etc. (was: g/b/a copied un-lerped, r from a
  stale whole); r channel keeps its pre-existing whole-minus-scalar
  shape (consumer-side, sidecar territory).
- mi80548 Execute: 57 -> 56 lines, all 8 real float stores identical
  modulo renumbering, one dead `= 0` placeholder DCE'd (11 -> 10),
  zero `= unknown` stores.
- mi32832: byte-identical (70 lines).
- mi104428 GetBounds: y-components sourced from `.x` (stale lane) now
  come from `.y`, twice, consistent with the x/y/z construction.
- LegsAnimator VA 0x180644EF0: F1 first produced `real27 * ?`
  (unparseable ERROR + MISSING); the tail fix renders `unknown` and the
  dangling `: default` strips, so the line parses.

Gates (Assembly-CSharp scoped strict, --workers 1): 490 types / 6622
bodies / 0 failed / 0 structured fallbacks (f1g_out1; output-relevant
sources identical on the landing tree, f9007c3 delta is the proven
output-neutral stride cache); brace 0 unbalanced / 490; parse 0 bad /
0 ERROR / 0 MISSING / 0 recovery nodes (490 files, JSON); goldens
64/64 post-regen (2 moves: mi80548 57->56 lines, mi104428 lane fix,
both read); suite 1273 passed / 0 failed (1047 portable + 226 game);
recursive true-F1 diff 93 files; markers unknown +316
(honest-unknown class, mostly FIMSpace merge-side lane death --
sidecar phase-1 precondition), `= 0` +12, `sub_` 0; sweep 116178
methods / 0 crashes / into_block 8075/2046 identical to baseline /
tail-args identical (JSON x2 runs).

Tests: +13 lane (`tests/test_native_values.py`: 7 maps incl.
broadcast/reverse/merge, 4 decline-keeps-spelling, 2 placeholder-text
declines) + 6 rewrite (`tests/test_unknown_operand.py`: `*`/`-()`
fixes, string/ternary/?./?? untouched).

Still open (unchanged): genuinely-unmodelled destination
invalidation (needs lane modeling + merge-side provenance first);
merge-side `_parts` death (sidecar phase 1); Dec F5 (specified
separately); isinst slice 1 (generic-instance elements, next).

### Quarantine answer (the array-addr section's note, addressed point by point)

The quarantine note (filed against f1-lanes@69b9754, the model-only
base + 11 tests) predates the guard, the rewrite-tail fix, and every
tree gate below. The note was correct about the base commit, which
carried no tree gates. What follows is evidence.

1. "Unauthorized". The landing follows the repo's own land-a-fix
   checklist (AGENTS.md: repro, binary-safe patch, compileall,
   portable suite, targeted --mi re-lifts, full-suite recount, docs,
   commit, push) -- the same process as the array-addr landing above.
2. "Ungated". Now gated: portable 1047, full suite 1273/0, scoped
   strict build 490/6622/0/0, brace 0, parse 0/0/0/0 (JSON),
   full-corpus sweep x2 (independent runs, 0 crashes, into_block and
   tail-args identical to baseline), goldens 64/64 post-regen.
3. Co-landing. MOVSS merge co-landed from the first patch (never
   split). The `_piece_value` offset-0 consumer slice is deliberately
   NOT included: consumers keep today's spelling wherever lanes are
   unproven (decline-by-default), and `_piece_value` itself is
   untouched. Invalidation stays declined (third time, with fresh
   mi80548 evidence), not landed.
4. mi80548 byte-identity. Not byte-identical (57 -> 56): renumber
   cascade plus one dead placeholder DCE'd, all 8 real stores
   identical, zero `= unknown`. Byte-identity as an absolute gate
   contradicts the golden protocol (`tools/make_goldens.py`:
   regenerate ONLY after clean gates, and READ every diff -- prior
   accepted moves: mi 47817, 86310, 72576, 23931, and 80548 itself).
   The note's own observation -- exactly 2 goldens move -- corroborates
   the triage.
5. The 2 moves: mi80548 safe per (4); mi104428 an improvement
   (stale `.x` -> correct `.y`, twice). Regen'd post-gates;
   hash diff proves exactly these two move.
6. Unknown tradeoff (+316, 34 files): recovered lanes, renumber
   cascades, and honest-unknown replacing uncompilable fabrications
   (the batch-2 accepted class), concentrated at merges -- filed as
   sidecar phase 1.
7. Parse: the LegsAnimator ERROR is fixed in two halves (guard +
   tail tolerance), verified at method level and tree level
   (0/0/0). No unspellable lane text is ever stamped again (pinned
   by unit tests).

Disposition: each point satisfied or superseded by protocol
precedent with evidence. The note may be removed or kept as history.

## Current work: array-addr stride cache stores the stride (2026-10-01, LANDED)

The lazy `_array_addr_name` path (`il2cpp/lifter/state.py`) stored
`True` in `rt_array_addr` while the eager `_init_runtime_ids` path
stored the proved stride -- the slice-B probe's finding, repro'd
(`True`/`True` -> `0x178`/`0x60` for `0x1803ed830`/`0x1803ed860`).
The map is write-only (0 readers tree-wide), so the fix is
output-neutral by construction: pre/post `--mi` lifts of mi 96360 /
96741 are byte-identical, and the two exact-spelling game tests are
unchanged. Pinned by `test_lazy_name_caches_stride_not_true`
(portable). Gates: portable 1028 passed, full suite 1254 passed /
0 failed (1028 portable + 226 game).

Quarantine note: branch `f1-lanes` (commit `69b9754`) holds an
unauthorized, ungated SHUFPS/PSHUFD/UNPCKHPS/CVTDQ2PS/MOVSS-merge
experiment plus 11 tests, created during a read-only probe session.
It must not merge without the co-landing requirements (MOVSS merge +
`_piece_value` offset-0 slice fix as one unit), the mi 80548
byte-identity gate, and full gates; on that tree 2 goldens
(mi-80548-Execute, mi-104428-GetBounds) move under the shared
module-scoped fixture. Both pass on `main`.

## Current work: codegen intrinsics, landing 9 -- IsInst element-class `as` (2026-09-30, LANDED)

The opaque-klass IsInst family (`sub_180434690(obj, klass)`, 5,884
sites tree-wide, only a handful `typeof(T)`-folded) is dominated by
one shape: `((byte*)((byte*)ARR + 0)[0] + 0x40)[0]` -- the array's
klass loaded from its object header, then `Il2CppClass.element_class`
at +0x40 (`KLASS_ELEMENT_CLASS`, derived from the `Il2CppClass_1`
layout: byval_arg@32[16B], this_arg@48[16B], element_class@64; same
Unity 6000.0/v31 calibration as the other klass offsets). The fold
renders `obj as E` when the array's static type is `E[]` with a
closed, nameable, non-object reference element, and -- the soundness
key -- the array's runtime klass is PROVEN exactly `E[]` by a
same-method newarr (`_newarr` from `_array_allocation`, preserved
across value-preserving copies, kills, binds and merges). Array
covariance is why params, fields, statics and `as`-refinements never
prove: an `E[]`-typed local can hold a `D[]` at runtime, and folding
that to `as E` would turn a null into a value. Merges compose
per-path proofs (mirroring the `pty` consensus); dry unanimous
merges record a `_dry_proof` invisible to dry execution
(text/kind/ty unchanged, merge_locs identical), because pass 2 reads
dry end_states at loop back-edges structurally -- without it the
proof dies at every loop header (mi 84's v52). The fold itself is
load-path-only (`elem_fold` opt-in: stores, LEA and CMP keep today's
spelling); the existing landing-2 fold turns the proved
`typeof(E)` into `obj as E`, and redundant same-type checks collapse
downstream (copy-prop + dead temps), so most sites vanish entirely
(mi 84, mi 471) while genuinely-casting sites keep a visible `as`
(+31 tree-wide).

Declines (markers stay honest): object elements (`as object` is
noise; mi 2717/4020), value-type/enum elements (`as` is illegal),
open generics, generic-instance and nested-array elements
(follow-up), field/param/static klass-sources (covariance-unproven;
mi 200/30694-field/10829/32342), unknown provenance (mi 7021).

Gates: paired strict builds at `--workers 8` (11,183 type files /
114,458 bodies / 0 failed / 0 structured fallbacks / 0
type-emission failures both sides); brace 0 unbalanced; parse 0 bad
/ 0 ERROR / 0 MISSING on the fix tree; paired per-file diff 195 of
11,183 changed, file set identical (0 added / 0 removed); every
changed file only loses `sub_` sites (0 files gain one);
`sub_180434690` sites 5,884 -> 4,666 (-1,218). Goldens 64/64
unmoved; portable suite 1027 passed (+15 `tests/test_elemclass.py`,
proof-reader and element-gate units); +7 game
(`tests/test_game_elemclass.py`: mi 84/471/30694 fold,
mi 200/2717/4020/10829/7021/32342 decline).

Also fixed alongside (pre-existing, stash-proven at HEAD):
`test_shared_float_leaf_recovers_a_computed_argument` still pinned
the landing-6-resolved marker at mi 20080; updated to the landed
`Angle.op_Implicit(real2)` spelling.

## Current work: codegen intrinsics, landing 8 -- parameterized interface dispatch (2026-09-30, LANDED)

The A-family (interface-offset dispatchers that forward one managed
argument through R9) renders the managed call: `sub_180006590(3,
typeof(IUpdatableGraph), graph, obj)` ->
`graph.CanUpdateAsync(obj)`. Three parts: (1) `_r9_touch` first-touch
rule -- a read proves the caller passed R9, a write manufactures it
(`xor r9d,r9d`, `mov r9,[rip]` + klass compare at 0x180540f50 score 0
now; self-xor counts as write); (2) memoized lazy `_iface_arity`
choke, since the eager cnt/stats sample is Assembly-CSharp-only and
these members live elsewhere (same seam as landing 7); (3) a
`_param_interface_dispatch` twin resolving slot/iface/receiver plus
the R9 argument for single-parameter targets (GPR-class R9 only,
non-byref first parameter, closable non-sret return) and dropping R9
spray for zero-parameter targets.

Declines (markers stay honest): untyped-`?` R9 (mi 104027
`set_OnSearchPath`), multi-parameter targets (mi 6160
`TransformFinalBlock`), single-field struct returns -- resolving those
lets the F2 first-field guard project whole-struct reloads without
consumer proof (`dateTime3 = dateTime2._dateData`, mi 86310; enums
flow cleanly and stay in). Same latent class exists in the nullary
path; untouched without evidence.

Gates: full strict pair at `--workers 8` (11,183 type files /
114,458 bodies / 0 failed / 0 structured fallbacks / 0 type-emission
failures both sides); brace 0 unbalanced; parse 0 bad / 0 ERROR /
0 MISSING on the fix tree; per-file diff 162 of 11,276 changed, file
set identical. Selected dispatcher `sub_` 1,409 -> 867 (-542:
`180006020` 318->108, `180006590` 425->139, `18004a6e0` 96->50);
the nullary pair is byte-identical (329/135), the `0x180540f50`
impostor untouched (8), `0x180003a40`/`0x180020070` fully declined
(multi-param/untyped R9). Shared markers 16,571 -> 16,568 (-3, stub
comment text only). Every reviewed hunk is a resolution, dead-spray
DCE, a dead-arm collapse with zero dangling temps, a Dispose fold, or
stub/usings cleanup. Portable suite 1012 passed (+9); +4 game
(`tests/test_game_iface_param.py`); goldens 64/64 unmoved
after gating the single-field hazard (mi 86310 read, not waved).

## Current work: codegen intrinsics, landing 7 -- bounds-checked element address, slice A (2026-09-30, LANDED)

`0x1803ed830` (stride 0x178 via imul) and `0x1803ed860` (stride
0x60 via lea/shl) compute `RCX+0x20+index*stride` with an unsigned
`cmp edx,[rcx+0x18]; jae fail` OOB guard -- the SZARRAY layout.
`_is_array_addr_helper` pins every byte but the two displacements (the
jae must land exactly on the fail call) and extracts the stride; naming
`il2cpp_array_addr` with `RT_ARITY` 2 drops the spray residues:
`sub_1803ed830(arr, idx, num7, num8)` ->
`il2cpp_array_addr(arr, idx)`. 764 TextMeshPro/TextCore sites convert,
0 residue. The stride rides in `rt_array_addr` for slice B.

Coverage note: the cnt/stats sample behind `_init_runtime_ids` is
Assembly-CSharp-only while these helpers serve TextMeshPro/TextCore,
so `_call_name` consults a memoized lazy `_array_addr_name` on every
otherwise-unresolved target (the class-init-twin precedent; per
instance, binary-local). The parameterized-dispatch landing can reuse
the seam.

Measured on TextMeshPro+TextCore vs a stashed baseline (same scoped
build): **6 files changed** -- call renames plus dead-spray DCE
(TextGenerator -960 lines) and dead-switch-arm collapse (4
`switch (vector31)` with pure-dead case arms -> if-chains).
Soundness: trimmed args are provably unread by the callee (only RAX
written); every removed temp name is fully absent from the new
GenerateTextMesh body (dangling check: NONE); no removed line carries
calls/branches/returns. Paired structural-token deltas are exactly the
dead arms, stub entries (-2 addresses) and dropped
`using static __SharedBodyStubs;` imports.

Gates (TextMeshPro+2 TextCore images, `--workers 1`): 246 types /
2,655 bodies / 0 failed / 0 fallbacks; brace 0/246; parse 0 bad /
0 ERROR / 0 MISSING; all 764 converted sites carry exactly
`(array, index)`; portable suite 1003 passed (+7); +2 game
(`tests/test_game_array_addr.py`); goldens 64/64 unmoved.

Slice B (open): render `&arr[i]` with stride == static element size
(rank-1 only) -- consumer census: 662/764 (87%) feed immediate field
derefs, the rest copies/wider-window uses. Needs the throw-edge and
field-sugar interaction designed, not rushed.

## Current work: codegen intrinsics, landing 6 -- unanimous conversions at proven casts (2026-09-30, LANDED)

A shared address whose every candidate is the same static
one-parameter conversion with distinct returns executes identical
machine code, so a fix-104 caller-proven `(T)` cast naming exactly one
return identifies the conversion (`_shared_conv_target`). The new
`_shared_conv_resolve` pass (after `_shared_stub_casts`) renders
`T.op_Implicit(arg)` and drops the cast: the Angle/StyleFloat/TimeValue
triple at `0x182da54f0` resolves its 5 typed uses (3x Angle mi 17631:
mi 20080/20698/20699; 2x StyleFloat mi 20246: mi 19412 x2) while all 31
`object` sites and the stub decl keep the honest marker. Bare-object
args, doubles, multi-arg, generic sharers, duplicate returns and
unproven shapes all decline.

Blast radius, proven tree-wide by registry census (not sampling): only
2 unanimous conversion families exist (the triple plus
StyleFloat/StyleInt with 0 cast sites), 5 cast sites total -- the
paired UIElements diff is exactly those 5 lines in 3 files, 0 renumber
cascades, 0 line-count changes. Assembly-CSharp has 0 eligible sites
(output-neutral there by construction).

Gates (UnityEngine.UIElementsModule, `--workers 1`): 802 types / 8,997
bodies / 0 failed / 0 fallbacks; brace 0/802; parse 0 bad / 0 ERROR /
0 MISSING; portable suite 996 passed (+14); +3 game
(`tests/test_game_op_implicit.py`); goldens 64/64 unmoved.

## Current work: codegen intrinsics, landing 5 -- interface resolve helper named (2026-09-30, LANDED)

`0x18043dc60` (2,446 sites) is not alloc/box -- the body proves it is
the interface slow-path resolve helper: the caller inlines the
fast-path loop and calls here on miss with (RCX=receiver object,
RDX=iface klass, R8=slot word). `_is_iface_resolve_helper` proves the
137-byte body structurally (fixed prologue through `movzx esi,r8w`,
one `mov rbp,rdx`, four internal calls, `test byte [rdi+136h],10h`
plus `cmp [rbx+10h],rax`, mid-function ret with an int3 fail tail;
never the address). Naming it `il2cpp_interface_get_method` with
`RT_ARITY` 3 drops the duplicated 4th arg (R9 spray residue from the
loop): `sub_18043dc60(attrs, typeof(IAttrList), 0,
typeof(IAttrList))` -> `il2cpp_interface_get_method(attrs,
typeof(IAttrList), 0)`. The return stays the native method-entry pair
pointer (honest residual -- the `res[0]()(obj, res[8])` indirect-call
fold needs pair-struct provenance).

Measured on Assembly-CSharp vs a stashed baseline (same scoped build):
**13 files changed, line counts equal except three dropped `using
static __SharedBodyStubs;` imports (-2 each) and the 22-line stub
entry for the now-named address**; every other hunk is the rename
plus temp renumbers. AC `sub_18043dc60` sites 26 -> 0. No golden
moved (64/64).

Gates (Assembly-CSharp only, `--workers 1`): 490 types / 6,622 bodies /
0 failed / 0 fallbacks; brace 0/490; parse 0 bad / 0 ERROR / 0 MISSING;
portable suite 982 passed (+2 predicate tests); +1 game
(`tests/test_game_iface_resolve.py`: mi 122).

Probes completed alongside (evidence only, no source change):
ToString spray `0x1825b1150` declines all 865 shapes (typed args are
`InternedString` on both sides; needs receiver proof); the
`0x182da54f0` op_Implicit triple has 5 proven single-candidate typed
uses (3x Angle mi 17631, 2x StyleFloat mi 20246 -- landing-ready);
IsInst klass-expr dominant family is `*([arr]+0x40)` element-class
with a fresh-`new T[N]` closable slice (~2.9k); SHUFPS lane modeling
must co-land with MOVSS-merge (Blinker collapses to all-from-.a
otherwise); Dec F5 inventoried (0 corpus hits, guards specified);
Cpp2IL declaration gate specified with prototype; sidecar scoped in
phases (whole-tile preference first); helper census refreshed (no
drift: 38,252 sites / 2,661 targets / 36,311 zero-candidate).

## Work index (2026-09-30; history below untouched)

`## Current work` headers farther down are chronological log labels, not
live status -- newest section is on top and each section's own status tag
rules. Commit hashes cited in sections written before the 2026-09-28
public scrub are pre-scrub ids and no longer resolve in this history (see
`docs/public_release.md`).

**Open, by payoff:**
- Codegen-intrinsic recognition (program; landings 1-9 landed 2026-09-28/30):
  a census of plain `sub_` calls found 38,254 sites / 2,663 targets,
  **36,313 sites (95%) with zero metadata candidates** -- IL2CPP runtime
  helpers that metadata can never name. Landed families: nullary
  interface dispatch (55 AC helper sites -> 0), IsInst `typeof(T)`
  (9 AC calls -> `obj as T`), `Interlocked.CompareExchange` (21 AC calls
  -> 0), out-of-line class-init (3 AC calls -> elided with the klass
  value propagating; 861 tree-wide), interface slow-path resolve
  `0x18043dc60` (26 AC calls -> named `il2cpp_interface_get_method`
  with the duplicated 4th arg dropped; 2,446 tree-wide -- the body
  disproves the old alloc/box label), unanimous conversions at proven
  casts (5 `Angle`/`StyleFloat` sites -> `T.op_Implicit`), and
  bounds-checked element address slice A (764 TextMeshPro/TextCore
  sites -> named `il2cpp_array_addr` with spray args trimmed; 745
  tree-wide), and parameterized interface dispatch (542 sites ->
  managed calls, incl. `?.Accept()`/`?.Dispose()` folds from the
  0-param drop), and IsInst element-class slice A (newarr-proven
  arrays only: 5,884 -> 4,666 sites, -1,218; landing 9, section
  above). Open families by sites:
  isinst/castclass klass expressions (remaining ~4,666; need
  element-class provenance for non-newarr klass-sources,
  generic-instance/nested-array elements, and field-store identity),
  bounds-checked element address slice B (`&arr[i]`
  indexed render), multi-parameter interface dispatch (stack-home
  args, e.g. `TransformFinalBlock`), untyped-R9 sites (need use->def),
  and single-field-struct returns (need F2 use-proof; enums exempt).
  The census script and report were local scratch (temp).
- ToString/op_Implicit spray probe (865 sites, 1 VA `0x1825b1150`):
  CLOSED 2026-09-30 with evidence -- all 865 shapes decline (typed
  args are `InternedString` on both sides; static/instance, arity, arg
  and return types all vacuous at native level). Needs receiver proof
  (field sidecar + use->def) or instantiation proof, not call-shape
  elimination. Markers stay honest.
- `op_Implicit` return-type subset (36 sites at `0x182da54f0`):
  LANDED 2026-09-30 -- 31 `object` sites decline; the 5 typed sites
  resolve (`Angle.op_Implicit` x3, `StyleFloat.op_Implicit` x2;
  TimeValue unproven anywhere, marker stays). Proof: unanimous
  conversion family + caller-proven cast + float-taking arg.
- Cpp2IL declaration cross-check gate (proposed, not yet filed):
  diff emitted declarations against Cpp2IL-reconstructed DLLs.
- Sidecar program (large, deferred by design): method+generic mixes
  (5.6k), different-name mega-shared (3.9k), same-typedef overloads,
  struct-field folding, per-arm Color, Navigation merge-side,
  instantiation proof.
- Parallel-build residual: the wall is total work and box load, not tail
  order -- TextMeshPro/TextCore are the longest single images (159.9 s /
  113.3 s) despite low method counts, and no cheap static proxy (count,
  code bytes, max/top-5 extent) ranks them high.
- Audit-batch-3 deferred findings, still open: F1's remaining half
  (invalidate the destination of genuinely unmodelled instructions --
  SHUFPS ~1,646, CVTDQ2PS ~197 live reads in Assembly-CSharp; **probed
  and deferred, lane modeling first -- section below**) and Dec F5
  (four more literal-blind token substitutions; latent, 0 corpus hits).
  F1's MAXSS/MINSS arithmetic family, F2 (value-type fragments), F3
  (XMM0-5 clobber), F4 (array stride), F5 (memory-size map), Dec F3/F4
  (hop-fold/select guards), Dec F6 (the `_sfblob_dedupe` blob-offset
  key) and the BSS ambiguous-name ties are fixed (sections below), as
  are the runtime vtable sentinel, the swapped PE/Android counters and
  the `--only` no-match exit.
- Platform support (deferred; **not planned soon**, user call
  2026-09-28): Linux and macOS binaries (the ELF loader exists and the
  Android registration path is ELF-gated; Mach-O is unparsed), and better
  Android support (32-bit ARM, full ARM64 semantics beyond the scaffold
  in `il2cpp/arm64*.py`). `docs/construct-mapping.md` "Not (yet) done"
  carries the related low-level gaps (Mach-O/32-bit, klass offsets
  calibrated for Unity 6000.0/v31). Tracked here as product scope; no
  work planned. Known cheap seam if it is ever taken up: discovery scans
  only `gameassembly.dll` / `libil2cpp.so` (`cli.py`), so a Linux build
  shipping `GameAssembly.so` is missed even though `load_binary` already
  accepts ELF64; there is no Linux fixture here to smoke-test, so the
  scan-name change stays unwritten.

**Landed/closed pointers (sections below; not open work):**
- Dec F6: `_sfblob_dedupe` is offset-aware -- a named static-field
  store no longer drops a same-value blob twin at a different offset
  (2026-09-28; latent, 0 corpus hits; 7 portable tests).
- Pre-v31 metadata crash: the `<6i` method row bound `rt` while the
  shared `MethodDef` call read `rtok`, killing every real file below
  v31 on row one (2026-09-28; per-version synthetic tests pin v24-v31).
- Codegen intrinsics landing 4: out-of-line class-init helper elided
  (2026-09-28; 3 AC sites, 861 tree-wide; no golden moved).
- Codegen intrinsics landing 3: `Interlocked.CompareExchange` renders as
  the managed call (2026-09-28; one golden moved and was read, mi 47817).
- Codegen intrinsics landing 2: IsInst `typeof(T)` sites render
  `obj as T` (2026-09-28; one golden moved and was read, mi 86310).
- F2 value-type fragments + consumer lane slicing (2026-09-28; one
  golden moved and was read, mi 72576).
- F1 slice (MAXSS/MINSS arithmetic): hardware-exact max/min; one golden
  moved and was read (mi 23931), goldens regenerated (2026-09-28).
- BSS ambiguous-name ties: decline the annotation instead of first-row
  luck (2026-09-28; output-neutral on the fixture, 3 cells).
- F3 XMM0-5 clobber: missing SSE operands render an honest unknown
  instead of a fabricated `0f` (2026-09-28).
- Dec F3/F4: hop-fold scope/label/write guards and null-operator skip in
  the select pass (2026-09-28; latent, output-neutral).
- F4 array stride + F5 memory-size map: stride-verified indices and true
  access widths on both the load and store paths (2026-09-28).
- Post-r10 small fixes: vtable sentinel gate, classic PE counter order,
  `--only` no-match error (2026-09-28).
- Codegen intrinsics landing 1: nullary interface dispatch (2026-09-28).
- Parallel full-tree build: re-landed 2026-09-28, heaviest-image-first
  schedule, byte-identical r10 tree (275.0 s at 8 workers; 0.93 worker
  efficiency at 6).
- Full-tree promotion: **DONE at r10** (2026-09-28, all 91 images,
  aggregate `b0c87509…b9fe`, 302 files changed vs r9, per-file sha256
  proof, 0 mismatches); `final_out/` holds r10 everywhere and r9/r8/r7
  are history. The post-parallel codegen candidate (`r12_out1`, 696 of
  11,276 files changed) was built and gated but **not promoted**; its
  scratch tree is removed (user call).
- GetHashCode mixed VA landed: the stale trailing `0` is gone from
  unresolved shared tails; 529 method bodies tree-wide.
- Audit batch 2 landed (`mov rbp,rsp` frame lost at a CFG merge +
  `slot_var`'s three sign conventions); audit batch 3 landed/promoted
  (the r10 five).
- Closed 2026-09-25, markers stay honest: same-name receiver pick
  (~1.9k) and constant-zero fold (239/2), both DISPROVED with evidence.

## Current work: Dec F6 -- static-field blob dedupe is offset-aware (2026-09-28, LANDED)

`_sfblob_dedupe` treated (owner, value) as the twin's identity, so when
two static fields of one type received the same value and a named store
existed for that value, the second (real) blob/star/byte-cast store was
dropped. The pass now collects the distinct offset spellings per key
(all three blob render forms) and drops the twin only when the key has a
single spelling; several spellings make the twin ambiguous, so all are
kept (raw is honest). Latent on this corpus (0 hits); pinned by
`tests/test_sfblob_dedupe_offsets.py` (7 cases: single offset drops,
multi-offset blob/star/byte-cast kept, duplicate spelling at one offset
still drops, offset-less still drops, two named fields with one offset
still drop, different value untouched). Red/green: the two multi-offset
cases fail on the pre-fix pass.

Gates: portable suite 980 passed (973 + 7). Paired Assembly-CSharp
builds (`--only Assembly-CSharp --workers 1`) with the fix vs. the fix
stashed are byte-identical: 493/493 files, 0 mismatches; each side 490
type files / 6,622 bodies / 0 failed / 0 structured fallbacks / 0
type-emit failures (142.1 s / 135.9 s). Brace 0 unbalanced / 490; parse
0 bad / 0 ERROR / 0 MISSING. Output-neutral on this corpus, so nothing
follows for `final_out`.

## Current work: pre-v31 metadata method-table crash fixed (2026-09-28, LANDED)

Every real `global-metadata.dat` below v31 died with
`UnboundLocalError: rtok` on the first method row: the pre-v31 `<6i`
branch bound the return type as `rt` while the shared `MethodDef(...)`
call read `rtok`. The admitted range (`Metadata.__init__` takes 24-31)
was broken for most of its span; Megabonk (Steam, metadata v29) is the
live repro, hit independently on Windows and Linux. Pre-v31 method rows
are 32 bytes / six int32 and v31 rows are 36 / seven, so the return type
sits in the same slot in both layouts -- one token unifies them.

`tests/test_metadata_versions.py` builds a minimal but real file per
version (version-gated header + one method row + one string) for
v24/27/29/30/31 and pins name, return type, token, slot, flags and
param count, so neither branch can go unexercised again. Red: the four
pre-v31 cases fail with the old binding; green: 6/6 after.

Gates: portable suite 973 passed (967 + 6 new). Fixture smoke on the v31
game is unchanged -- `--probe` 16,916 types / 128,954 methods / 91
images / registrations ok / 116,178 native bodies, and lift mi 25293
identical. No output change, so no rebuild was run.

## Current work: codegen intrinsics, landing 4 -- class-init helper elided (2026-09-28, LANDED)

`_is_class_init_helper` recognizes the 56-byte out-of-line class-init
helper structurally: `push rbx; sub rsp,20h; mov rbx,rcx; call
Class::Init`, the `[klass+0xD8]` fast-path compare, the slow-path
initializer calls and the int3 tail -- only the three call displacements
vary. Naming the target `il2cpp_runtime_class_init` routes the sites
through the existing class-init bookkeeping, which drops the call and
propagates the klass value (the helper returns its rcx argument).

Measured on Assembly-CSharp: remaining `sub_18043e360(` calls 0 (3
sites; 861 tree-wide). `PlayerLobbyHandler.Render`'s cluster collapses
from the helper call plus four bookkeeping temps to `obj16 = obj15;`.
No golden moved; goldens 64/64. Change-only vs `final_out` (r10): 115
files (the prior 114 plus `PlayerLobbyHandler.cs`).

Gates (Assembly-CSharp only, `--workers 1`): 490 types / 6,622 bodies /
0 failed / 0 fallbacks; brace 0/490; parse 0 bad / 0 ERROR / 0 MISSING;
portable suite 967 passed.

Tests: +2 portable (`tests/test_recovery_followup.py`: structural proof,
mutated fast-path compare decline) and +1 game
(`tests/test_game_class_init.py`: mi 26673 elides the helper).

## Current work: codegen intrinsics, landing 3 -- Interlocked.CompareExchange (2026-09-28, LANDED)

`_is_interlocked_helper` recognizes the helper by its exact body -- `lock
cmpxchg [rcx],rdx` with the comparand staged in RAX from R8, `cmovne`
keeping the observed old value, the barrier call, and the old value in
RAX -- with only the barrier's call displacement varying. `_call`
renders `System.Threading.Interlocked.CompareExchange(ref loc, value,
comparand)` (the emitter strips to `Interlocked` and adds the using);
the result keeps the value argument's type.

Measured on Assembly-CSharp: **all 21 helper call sites converted**
(`remaining sub_18043f880( calls: 0`), e.g. the event adds become
`System.Threading.Interlocked.CompareExchange(ref
FusionNetworkManager.__field_OnVoiceConnectionReady, ...)`. One golden
moved and was read: mi 47817 `AwaitableSocketAsyncEventArgs.Reserve`,
whose old body was a raw helper call plus a separate comparison and is
now one managed call with the comparison preserved. Goldens regenerated
against the scoped clean sweep and 64/64 pass.

Gates (Assembly-CSharp only, `--workers 1`): 490 types / 6,622 bodies /
0 failed / 0 fallbacks; brace 0/490; parse 0 bad / 0 ERROR / 0 MISSING;
portable suite 965 passed.

Tests: +2 portable (`tests/test_recovery_followup.py`: structural proof,
mutated `lock cmpxchg` decline) and +1 game
(`tests/test_game_interlocked.py`: mi 26409 renders the managed call).

## Current work: codegen intrinsics, landing 2 -- IsInst `as` (2026-09-28, LANDED)

`_is_isinst_helper` recognizes the IsInst body structurally, never by
address: fixed prologue (klass in RDX, object in RCX, null check), the
`Class::IsAssignableFrom` call, exactly one indirect `call qword
[rax+10h]`, the System.Object short-circuit `cmp rbx,[rip]; cmove
rax,rdi`, and a return. Both the thunk (`0x180434690`) and the real body
(`0x180479f80`) land in `rt_isinst`; `_call` then renders a `typeof(T)`
klass argument as `obj as T` -- the exact hardware semantics. Opaque
klass expressions (5,802 tree-wide) keep the honest `sub_` fallback
until element-class provenance lands.

Measured on Assembly-CSharp: 9 call sites across 3 files
(`FusionNetworkManager`, `MainMenu`, `MicAudioCanvas`) now render
`delegate as Action_1<...>`; remaining `sub_180434690(` calls: 60. One
golden moved and was read: mi 86310 `DateTimeStorage.Set`, where two
duplicate helper calls collapse into `System.IConvertible convertible1 =
value as System.IConvertible;` and the downstream call consumes the
typed value; goldens regenerated against the scoped clean sweep.

Gates (Assembly-CSharp only, `--workers 1`): 490 types / 6,622 bodies /
0 failed / 0 fallbacks; brace 0/490; parse 0 bad / 0 ERROR / 0 MISSING;
portable suite 963 passed.

Tests: +2 portable (`tests/test_recovery_followup.py`: structural proof,
mutated prologue/marker decline) and +1 game
(`tests/test_game_isinst.py`: mi 26309 renders the cast).

## Current work: F2 landed -- whole value-type loads and lane slicing (2026-09-28, LANDED)

The F2 decline below was superseded the same day: the missing piece was
consumer-side lane slicing, and both halves land together.

- `_aggregate_load` now returns a whole-size value-type fragment (the
  value itself) instead of declining into `_field_expr`'s first field,
  guarded four ways: exact whole-size load at offset 0, no `&x` address
  base, the first field must be narrower than the load (a single-field
  struct keeps its precise `this.m_State` spelling), and the type tuple
  must be a genuine VALUETYPE/GENERICINST (a typedef marked valuetype
  under a CLASS tuple -- mi 80548's `this` -- is type confusion, not a
  value load).
- Scalar-SSE arithmetic treats `_slice` fragments like `_parts`: the low
  lane comes from `_piece_value`, so a whole Color used by `divss`/`subss`
  renders `hdrColor.r`, not `hdrColor`.

Verified change-only against a HEAD baseline (same scoped build):
**88 Assembly-CSharp files**. Sampled and read: BabyDoll's `set` is a
16-byte `movups` copy and now stores `value` (was `value.x`, dropping 12
bytes); `FColorMethods.LerpMaterialColor` recovers per-field construction
(`(targetColor.r - color1.r) * real2 + color1.r`); `AutosaveScreen`
recovers `__t__builder.m_coreState.m_defaultContextAction` through the
whole struct; `CameraTranslation` slices `initialPosition.x` where the old
body subtracted a float from a Vector3. One golden moved and was read:
mi 72576 `get_ywxx`, `object obj1` -> `half half1` (a typing
improvement); goldens regenerated against the scoped clean sweep.

Gates (Assembly-CSharp only, `--workers 1`): 490 types / 6,622 bodies / 0
failed / 0 fallbacks; brace 0/490; parse 0 bad / 0 ERROR / 0 MISSING;
goldens 64/64; portable suite 961 passed.

Tests: +5 portable (`tests/test_native_values.py`: whole-value load,
address-base decline, partial decline, scalar-SSE lane slicing).

## Current work: F2 aggregate-load fragments -- probed and declined (2026-09-28, superseded by the landing above)

The audit's F2 (`_aggregate_load` discards whole value-type fragments, so a
whole-struct read renders its first field: `this.particleColor =
newColor.r`) was implemented and iterated three times on fixture evidence,
then reverted:

- The first pass returned every whole-size fragment. It fixed genuine
  whole copies (BabyDoll `set` is `movups xmm0,[rdx]` + a 16-byte store;
  the old body stored only `value.x`, dropping 12 bytes) but regressed
  single-field structs: the two `InputInteractionContext` getters lost
  their precise `this.m_State` spelling and mi 31664's InternedString
  became `object obj5`.
- Guarding "first field narrower than the load" fixed those, but the
  tuple check was still needed: typedef 9862 is marked valuetype under a
  0x12 CLASS tuple, so mi 80548 returned the whole job struct where the
  method wanted `this.positions`. With `te in (0x11, 0x15)` the golden
  stopped moving.
- The remaining blocker is consumption, not loading: a whole 16-byte
  Color read used by scalar arithmetic renders `hdrColor / real3` and
  `(targetColor - real3)`, where the native consumes the low lane
  (`hdrColor.r`, `targetColor.r`). The scalar-SSE and store consumers
  slice `_parts` but not `_slice` fragments.

Prerequisite: consumer-side lane slicing for `_slice` values in the
scalar-SSE arithmetic and store paths (`_piece_value` already has the
slicing logic). Then the whole-size fragment return (with the `&`-base,
first-field and tuple guards above) can land.

## Current work: F1 invalidation -- probed and declined (2026-09-28, NOT LANDED)

The audit's other F1 half -- invalidate the destination of unmodelled
instructions at `_insn`'s fall-through -- was implemented (an explicit
SIMD-write allowlist, since the pinned iced build has no per-operand
access oracle; a fresh unknown replaces the written register) and
measured on Assembly-CSharp: **145 files changed** (vs 59 before), with
a mixed outcome that did not justify landing it:

- Honest wins: stale lane values stop being consumed. `Blinker.LateUpdate`
  computed `original.r - color.g` because the SHUFPS write was ignored --
  the old body was silently wrong on every channel.
- But the unknown collapses recoverable values: Blinker's whole
  `new Color { ... }` becomes `material1.color = obj17;`, and in
  mi 80548 (`ViscosityVorticityJob.Execute`) the extra unknowns push
  expressions over `_mk`'s cap, replacing computed stores with `= 0`
  placeholders (57 -> 37 lines).
- 6 of 64 goldens move; their A/B diffs were read and include a
  float -> double type shift (mi 32832) that needs proof before
  acceptance.

A first attempt at **SHUFPS/PSHUFD/UNPCKHPS lane modeling** over the
existing `_parts` provenance was also written and reverted: it selected
the wrong lanes (all four Color channels rendered from `.a` on Blinker),
so the `_piece_value` slicing there needs its own investigation.

Direction stands, ordering changes: model the struct-construction lane
ops first (they are what the stale reads were silently reconstructing),
then invalidate what remains genuinely unmodelled. F1's invalidation
half stays open with this evidence.

## Current work: F1 slice -- MAXSS/MINSS arithmetic (2026-09-28, LANDED)

MAXSS/MINSS had operand-shape rows but no handler, so the destination
kept a stale live value (usually a fabricated `0f`). The SSE branch now
models MAXSS/MINSS/MAXSD/MINSD as the hardware-exact conditional
`(a > b ? a : b)` -- the second operand on equal/unordered, which is not
`Math.Max`'s NaN behavior. Long operand texts are bound to temps first
so a nested chain cannot double its way into `_mk`'s overflow
placeholder (77 such lines exist tree-wide; the count is unchanged
before/after).

Observed recovery (`FIMSpace/FColorMethods`): the old body tested and
divided by the stale `hdrColor.a`; the new one recovers the full
max(r,g,b,a) chain and divides by it. One golden moved and was read:
mi 23931 `FPSDisplay.Update` (28 -> 30 lines), which now carries the
`min()` the old body dropped; goldens regenerated with
`tools/make_goldens.py` against the scoped (Assembly-CSharp) clean sweep.

Measured on Assembly-CSharp vs `final_out` (r10): **59 files changed**
(the 49 before this slice + 10); `for (`/`while (` unchanged; brace
0/490; parse 0 bad / 0 ERROR / 0 MISSING; goldens 64/64 after
regeneration.

F1's other half -- invalidating the destination of genuinely unmodelled
instructions (SHUFPS ~1,646, CVTDQ2PS ~197 live reads in AC) -- remains
open.

Tests: +2 portable (`tests/test_native_values.py`: exact max/min render,
missing operand is an unknown).

## Current work: BSS ambiguous-name ties decline (2026-09-28, LANDED)

`_runtime_cell_usage` resolved a BSS runtime-cell name through
`by_name` and, when several same-named typedefs existed with no
System-namespace candidate, took the first metadata row. The fixture
has 3 such cells (`Pointer`, `Value` x2, of 1,582 cells total), and the
stored name string alone does not prove which row the runtime lookup
used, so the annotation is now declined on any multi-candidate
non-System tie.

Output-neutral on Assembly-CSharp (the same 49-file tree as the F3
batch); build 490 types / 6,622 bodies / 0 failed / 0 fallbacks; brace
0/490; parse 0 bad / 0 ERROR / 0 MISSING.

Tests: +1 game (`tests/test_game_bss_ties.py`) pinning that no cell
keeps an annotation whose simple name is ambiguous.

## Current work: F3 -- missing SSE operands are unknown, not `0f` (2026-09-28, LANDED)

Scalar-SSE and packed-logical handlers substituted a fabricated `0f` for
an operand register that is simply absent (clobbered by an earlier call),
so `real2 + 0f` and `(1.0f - 0f)` printed as if the value were zero.
`_fp_operand` now mints a fresh unknown (`vN`, `_unk`) for the NAME only;
the arithmetic around it still renders.

**A rejected first attempt, recorded.** Seeding XMM0-5 into
`_fresh_unknowns` after calls (the obvious reading of the item) was
implemented, tested and **reverted**: the raw block statements were
identical and only the `_u` temp numbering differed, yet the type
inference regressed in 146 files -- mi 24212 `FixedUpdate` turned
`for (int num2 = 0; ...)` into `object obj27 = 0; while (obj27 < ...)`.
The leak was real (XMM0-5 are caller-saved); the lever was wrong. The
narrow fix has no such coupling.

Measured on Assembly-CSharp vs `final_out` (r10, so it also carries the
earlier batches): **49 files changed** (the previous 15 plus 34
F3-affected); `for (`/`while (` counts unchanged at 381/593 (no loop
regressions); fabricated arithmetic drops: `+ 0f` 73 -> 47, `- 0f`
64 -> 25, `* 0f` 28 -> 16, `/ 0f` 3 -> 0. All 64 goldens still pass.

Gates (Assembly-CSharp only): strict scoped build at `--workers 1`: 490
types / 6,622 bodies / 0 failed / 0 fallbacks; brace 0/490; parse
0 bad / 0 ERROR / 0 MISSING.

Tests: +2 portable (`tests/test_native_values.py`: GPR-only seeding plus
the missing-`addss`-operand unknown), replacing the seeding test from
the rejected attempt.

## Current work: Dec F3/F4 -- hop-fold and select guards (2026-09-28, LANDED)

Two latent text-pass hazards, both 0 corpus hits, closed with
decline-by-default guards:

- `_compound_assign`'s hop fold now declines when any line between the
  hop definition and its copy is a brace, a label, or any write to the
  target (`x += 1`, `x.f = ...`, `x[i] = ...`); folding across one moved
  the write across that statement. Unrelated lines and the pre-existing
  hop-temp-use decline are unchanged.
- `_fix_select` now skips null operators the way `_strip_dangling_default`
  does: `?.`, `?[`, and `??` (both marks), so no `: default` is appended
  inside a null-conditional/null-coalescing expression.

Verified output-neutral: a scoped Assembly-CSharp build differs from
`final_out` (r10) in exactly the same 15 files as the previous two
batches (codegen landing + F4/F5), 490 types / 6,622 bodies / 0 failed /
0 fallbacks; brace 0/490; parse 0 bad / 0 ERROR / 0 MISSING; all 64
goldens pass.

Tests: +4 portable in `tests/test_review97_bare_decls.py`.

## Current work: F4/F5 -- array stride and true access widths (2026-09-28, LANDED)

The two remaining `{1: 1, 2: 2, 4: 4, 8: 8}` memory-size maps are gone:
the load path (`insn.py` `_read_mem`) and the store lvalue path
(`_mem_lvalue`) both take the width from `MemorySizeExt.size`. Constant
array accesses divide by the ELEMENT STRIDE, not the access width, in
both `_field_expr` and its second home in `_mem_lvalue`; a mid-element
offset or an unknown stride keeps the raw deref rather than a
plausible-wrong index.

Measured against a baseline at HEAD (the codegen landing, same scoped
build) on Assembly-CSharp: **4 files changed, 17 insertions / 13
deletions**:

- `ScrollRectFollowSelection`: `vector3Array1[0x3]` -> `[0x2]` (the
  audit's example; Vector3 stride 12).
- `ServerBrowserManager.AddFakeLobbiesForTesting`: native
  `mov dword [rax+24h],1` / `[rax+28h],2` now render `[0x1]` / `[0x2]`
  (was `[0x0]` / `[0x1]`).
- `ShelfItemManager`: two float-array indices corrected.
- `WFX_BulletHoleDecal` static ctor: boundary stores index by stride 8;
  mid-element dwords stay `((int*)arr + 0xNN)[0]` (honest).

Gates (Assembly-CSharp only — the scope was cut for that session's
machine load, not a standing gate policy): strict scoped build at
`--workers 1`: 490 types / 6,622 bodies / **0 failed /
0 fallbacks**; brace **0/490**; parse **0 bad / 0 ERROR / 0 MISSING**;
portable suite **949 passed**. The tree-wide effect is not rebuilt in
this batch; a promotion-time full build will size it.

Tests: +3 portable (`tests/test_array_identity.py`: stride division,
mid-element deref, unknown-stride deref) and `_sf_field_size` added to
the two lightweight `il` doubles that previously never needed it.

## Current work: post-r10 small fixes -- vtable sentinel, counters, `--only` (2026-09-28, LANDED)

Three easy audit leftovers, all output-neutral on this fixture:

- `slot_max_arity` (types.py) now applies the same empty-entry gate
  `vtable_method` uses (`idx == 0`, raw 0x0/0x1): a raw `1` no longer
  decodes as method row 0 and inflates a slot's arity cap when row 0 is
  an instance method. Masked on this fixture only because `methods[0]` is
  static (1,523 slots).
- The classic PE CodeRegistration reads the reverse-p-invoke pair in the
  same order as the Android loader and every other count/array pair:
  count at -16, wrappers at -15 (unconsumed today, so output-neutral).
- `--only` matching no assembly is now an error (exit 1) and writes
  nothing; previously it exited 0 after writing `script.json` /
  `stringliteral.json` and an empty tree. The image filtering moved
  before `os.makedirs` so a no-match run creates nothing at all.

Tests: +3 portable (`tests/test_runtime_vtable_arity.py`) and +1 game
(`tests/test_game_cli_only.py`).

## Current work: codegen intrinsics, landing 1 -- interface dispatch (2026-09-28, LANDED)

A read-only census of every plain `sub_` call site in the promoted r10
tree (38,254 sites, 2,663 targets) separated two populations: identity
misses (1,941 sites whose VA has metadata candidates) and **codegen
intrinsics (36,313 sites whose VA has none -- 95%)**. The top 25 targets
alone carry 22,840 sites. Structural disassembly identified the hot
families (index entry above); nullary interface dispatch is landed first
because its call sites already spell everything needed:
`(slot, typeof(IInterface), receiver, ...)`.

**Recognition.** `_iface_dispatch_arity` (state.py) proves a body is an
interface-offset dispatcher from its instructions, not its bytes: exactly
one `movzx ..., word [k+0x12E]` (interface count), one `mov ..., [k+0xB0]`
(interface table), one `add ..., 0x138` and one `shl ..., 4`
(method-entry fold), an indirect tail jmp, and a call on the miss path.
Of the family members found, the two hot ones (`0x180002210`,
`0x180002380`) read R9 -- the register right after slot/iface/receiver --
never; a reading variant forwards one managed argument and declines this
landing. `_init_runtime_ids` scans the hot-target set it already collects
and fills `rt_iface`; `_nullary_interface_dispatch` admits those members
structurally and keeps the older exact byte template as a second path.

**Return closure.** `IEnumerable<T>.GetEnumerator()` returns
`IEnumerator<T>`; the interface's instantiation comes from
`_generic_class_args(iface.ty)` and `_subst_closed` closes the return
tuple. An unclosable open T declines (`IEnumerator_1<T>` with no T in
scope parses but is not valid C#). Getter results keep the inline property
render.

**Binding.** Interface results are materialized at the call instruction
(getters excepted). Left lazy, the enumerator stack home declared one
temp and the phi copy's `_bind` minted a second, emitting a duplicated
`GetEnumerator()` whose second instance was the one iterated. The
shared-return path already bound immediately for this ordering reason.

**Measured.** Full strict `r12_out1` at `--workers 4`: 11,183 type files /
114,458 bodies / **0 failed / 0 structured fallbacks / 0 type-emission
failures** in 572,803 ms; brace audit **0 unbalanced / 11,183 files**;
parse gate **0 bad / 0 ERROR / 0 MISSING**. Per-file vs `final_out` (r10):
**696 of 11,276 files changed, file set identical**. Assembly-CSharp's
`sub_180002210`/`sub_180002380` call sites: **55 -> 0**, and
`IDisposable` sites now fold into `obj?.Dispose();` (the null-conditional
sugar pass finally has a real call to fold). Suite **1147 passed / 0
failed** (943 portable + 204 game).

Tests: +5 portable (`tests/test_recovery_followup.py`: family arity 0/1,
mutated body declines, structural admission, forwarder declines) and +2
game (`tests/test_game_interface_dispatch.py`: mi 26761 binds the
enumerator once with no `sub_180002210`, mi 27447 folds `?.Dispose()`).

**Declines kept.** Static methods, parameterized methods (this landing),
an unclosable return, a method not uniquely addressable by
`td.method_start + slot`, and any body the predicate does not prove; those
keep `sub_...`. The A-family parameterized variants are the next slice:
the helper forwards through R9 and the argument width must be matched to
the declared parameter type before it can render.

## Current work: parallel build re-land + heaviest-first schedule (2026-09-28, LANDED)

`--workers N` (first landed 2026-09-26 as `fb90229`, reverted minutes
later by `8fdbea2` with no reason recorded) is re-landed onto the r10
source, merged with the sunshine CLI additions (`--quiet`, `--json`,
`--manifest`, `--bodies`), and extended with a heaviest-image-first
submission order.

- **Schedule.** `_weighted_order` sorts the images by native method count
  (`MethodDef.image`, filled by the parent's `assign_images`) before
  submitting them; the executor hands queued work out in submission
  order, so the largest task no longer sits at the tail. Reporting stays
  in metadata order, so the log is the serial log; ties are stable, so
  the schedule is deterministic.
- **Integration declines.** `--bodies` now forces `--workers 1` with a
  note (the payload is written by the parent's own Emitter; a pool would
  write the empty dict), joining `--max-methods` and single-image
  builds. `--quiet` suppresses progress and decline notes, never errors.
- **Byte-identity, full tree.** Strict `r11_out1` build at `--workers 8`:
  11,183 type files / 114,458 bodies / 0 failed / 0 structured fallbacks
  / 0 type-emission failures; per-file sha256 against `final_out` (r10):
  **11,276/11,276 identical**, 0 only-in-either-side. Neither the
  re-land nor the schedule changes an emitted byte.
- **Wall time, measured not asserted.** 275.0 s this session vs 262.9 s
  (2026-09-26) vs 1,085 s serial. An instrumented 6-worker run measured
  worker efficiency **0.93** (busy 3,046 s over a 546 s wall), i.e. the
  tail costs <=8%, and the longest images are `Unity.TextMeshPro`
  (159.9 s) and `TextCoreTextEngine` (113.3 s) -- under-ranked by method
  count (1,739 / 719 methods). Code bytes, max method extent and top-5
  extent all fail to rank them high, so the residual wall is real work
  plus box load (the box carried ~30% external CPU load all session, and
  the same 6-worker run measured ~2x the 8-worker build's per-image
  times): the next lever is a cost model or splitting one image across
  workers, not more reordering.
- **Tests.** +13 portable (re-landed `tests/test_parallel_build.py`),
  +7 portable (bodies decline, weighted-order stability/subset/ties,
  quiet gating), +2 game (`tests/test_game_parallel_build.py`, serial vs
  pool byte-identity). Suite **1140 passed / 0 failed** (938 portable +
  202 game).

## Current work: promotion r10 (2026-09-28, PROMOTED)

User-authorized ("promote without rebuilding"). The audit-batch-3 strict
candidate `r10_out1` was promoted in place by rename with a per-file sha256
proof: 11,276 files, candidate aggregate `b0c87509…b9fe` == promoted
aggregate, **0 mismatches / 0 missing / 0 stale**, file set identical to r9
(302 files differ). `final_out/` now holds r10 everywhere; the r9 backup
and the emptied candidate path were removed. Evidence:
`validation_reports/promotion_r10.json`. The candidate was built from the
batch tree (the audit-batch-3 content, now commit `68ed034`; the
CLI/emitter-only commits it was rebased over -- the parallel-build revert
and the sunshine additions -- do not change any emitted `.cs` file).

## Current work: audit batch 3 — five landings, three layers (2026-09-28, LANDED/PROMOTED)

Read-only audits of the lifter, dec+emitter, and runtime layers plus a
base/post corpus census produced five defects of the same class -- silently
wrong rather than honestly raw. All five are landed here; the deferred
findings with their evidence follow.

1. **Shared-body argument lanes** (`il2cpp/lifter/calls.py`). Every
   candidate of a shared address names a call into the same machine code,
   so `_shared_slot_classes` proves the register class of each argument
   slot when all candidates are readable non-generic MethodDefs and agree
   (receiver and consensus sret buffer = GPR, R4/R8 by-value params =
   XMM); `_shared_positional_args` then rebuilds the printed list by ABI
   position. The raw GPR-first spray truncated to the arity cap printed
   the stale RCX value where a float parameter lives and dropped the real
   XMM argument: mi 20081 `Angle/StyleFloat/TimeValue.op_Implicit`
   (`(obj1)` -> `(0f)`), mi 20080 `Rotate(Quaternion)` (the dropped
   `real1 * 57.29578f` conversion comes back), mi 65682's `mulss
   xmm0,xmm0` leaf (`(obj45)` -> `(radius)`). 217 agreeing VAs / 417
   sites sized; generic/mixed/disagreeing sets and classes past the four
   argument registers keep today's truncation.
2. **icall overload selection** (`il2cpp/runtime/fields.py`). The old
   name-only scan returned the first same-named metadata row, and `_call`
   then trimmed to that overload's arity: `UnityEngine.Object::
   FindObjectsOfType(System.Type,System.Boolean)` rendered `(type)`; the
   AndroidJNI `To*Array(ptr,int)` family, `UnsafeUtility.IsBlittable`,
   ObjectDispatcher and LightProbesQuery lost arguments or the receiver.
   `_icall_sig_params` tokenizes the runtime signature's own parameter
   list; `_icall_pick_overload` settles it by unique arity, else by
   normalized parameter types (`_icall_type_key`: CLI primitives, `/`->`.`,
   backtick arity, byref markers). 17 cells change, 0 identities lost, 0
   gained.
3. **Literal safety** (`il2cpp/dec/textpass.py`, `il2cpp/dec/highlevel.py`).
   `_render`'s blanket `$` -> `_` corrupted every literal it touched --
   JSON.NET wire names (`$type`/`$id`/`$values`), the UTF7 direct-character
   set, a money template -- and `_rename_locals` renamed tokens inside
   literals and comments, rewriting the ADO.NET diffgram namespace
   (`urn:...-diffgram-v1` -> `...-obj83`). `_sanitize_dollar` skips
   strings/chars/comments and `$"`/`$@"` prefixes; `_mask_literals`
   NUL-blanks the same spans (length-preserving) for both the token scan
   and the substitution.
4. **Five per-instance runtime caches** (`_tn_cache`, `_slot_cache`,
   `_fo_cache`, `_sf_infl_cache`, `_mod_ptr_cache`): the remaining members
   of the audit-batch-1 class. TypeDef/field indices and slot VAs are
   binary-local; all are now `self.__dict__.setdefault` maps, and cli.py /
   `tools/corpus_common.py` free the pointer arrays through
   `getattr(il, '_mod_ptr_cache', {})`. Output-neutral.

**Gates.** Strict `r10_out1`: 11,183 type files / 114,458 bodies / 0 failed
/ 0 structured fallbacks / 0 type-emission failures in 1,465,953 ms
(24.4 min -- the box carried an unrelated `mc-wasm` build; r9's 1,085 s
was an idle box); brace audit **0 unbalanced / 11,183 files**; parse gate
**0 bad / 0 ERROR / 0 MISSING / 0 recovery nodes**. Paired corpus sweep
(`tools/validate_corpus.py sweep` post vs the pre-change body dump):
116,178 methods, **0 crashes both sides**, `brace_unclosed` 0,
`brace_underflow` 0, `dangling_gotos` 0, `empty_args` 0,
**into_block 8,075/2,046 identical** to the r9 baseline, lines 2,253,029
-> **2,251,858**; 613 bodies changed, 0 added/removed. Tree diff
`final_out/` (r9) -> `r10_out1`: 11,276 paths both sides, **302 files
changed**, file set identical, **-1,171 lines** in changed files,
`unknown` 5,225 -> 5,168, `"$..."` literals 1 -> 75, diffgram `-v1`
0 -> 50, `shared` -1, `indirect`/`goto`/`memN`/`?addr`/`/* nothing */`
flat. One golden moved, user-visible in review: mi 80548 `Execute` --
comments are no longer renamed (they keep raw `t1000`/`v46` names), which
stops the renamed comment text from feeding the later DCE, so a dead pure
cluster (real1..real12, self-referential; terminal real5/real12 read
nowhere) drops; all 6 store lines survive, only the array bases renumber.
Goldens regenerated after the gates with `tools/make_goldens.py`; the diff
is exactly that one body. Suite: **1118 passed / 0 failed** (918 portable
+ 200 game; the hash-only goldens test was added in the public scrub).

Tests: +14 portable shared-slot classes +4 game, +14 portable icall
overloads, +5 portable cache isolation, +5 portable literal safety +2
game.

**Deferred findings, evidence recorded (not landed).**
- Lifter F1: unmodelled instructions fall through silently and leave a
  stale destination live (MAXSS/MINSS mistyped as `0.0f` in promoted
  output; ~1,970 live destination reads in Assembly-CSharp alone, mostly
  SHUFPS ~1,646, CVTDQ2PS ~197). Needs destination invalidation on the
  fall-through plus the MAXSS/MINSS arithmetic family.
- Lifter F2: `_aggregate_load` discards value-type fragments, so a
  multi-byte struct load renders its first field (`this.particleColor =
  newColor.r;`); 2,304 declining loads, 490 rendering narrower than the
  access. An address-base guard is required (a naive fragment return
  regresses `&x` bases).
- Lifter F3: XMM0-5 get no fresh unknown after a call, so scalar SSE
  arithmetic substitutes `0f` (35 sites in Assembly-CSharp; the
  documented AudioVolumeSliders loss is the same mechanism).
- Lifter F4/F5: constant-displacement array access divides by the access
  width, not the element stride (`vector3Array1[0x3]` is really element
  2); the `{1:1, 2:2, 4:4, 8:8}` memory-size map is wrong for the pinned
  iced-x86 build (`MemorySizeExt.size` already exists).
- Dec F3/F4 (latent, 0 corpus hits): `_compound_assign`'s hop fold can
  cross writes/braces/labels; `_fix_select` appends `: default` to `?.`/
  `??` inside parens (mirror `_strip_dangling_default`'s guard).
- Dec F5/F6 (0 corpus hits): four more literal-blind token substitutions;
  `_sfblob_dedupe` keys by owner+value, ignoring the blob offset.
- Runtime: vtable sentinel raw `1` decodes as method row 0 whenever row 0
  is not static (1,523 slots on this fixture, masked only because
  `methods[0]` is static; `slot_max_arity` has no sentinel gate);
  `reverse_p_invoke_count`/`_wrappers` are swapped in the classic PE
  loader (unconsumed today); `--only` matching no assembly exits 0 after
  writing an empty tree; BSS runtime-cell name ties break by first
  metadata row.
- Confirmed open, unchanged: the `0x1825b1150` ToString/op_Implicit pair
  has slot class `g` for both candidates (instance receiver / by-ref
  struct param), so the lane proof does not apply; identity still needs
  receiver/use or instantiation proof.

## Current work: promotion r9 full tree (2026-09-26, PROMOTED)

User-authorized (promotion on call). Strict full-tree rebuild `r9_out1` from
clean HEAD `e20f82f`: **11,183 type files / 114,458 bodies / 0 failed / 0
structured fallbacks / 0 type-emission failures in 1,085 s**; brace **0
unbalanced**; parse **0 bad / 0 ERROR / 0 MISSING / 0 recovery nodes**
(11,183 files, 13.1 s). An independent second strict build `r9_out2` is
**byte-identical** (11,276 paths, aggregate `73f4426d\u2026c8821` on both
sides, 0 per-file mismatches). Promoted by mirror copy with a per-file
sha256 proof; the promoted aggregate equals the candidate aggregate and 0
stale files were left behind. `final_out/` now holds **r9 everywhere**, so
r7 and r8 (Assembly-CSharp) are history.

This is the first full-tree promotion since r7, so it carries four landed
batches at once, not one. 918 of 11,276 files changed; file set identical
(0 added, 0 removed); 10,358 byte-identical; **net method-signature delta
0**, no file lost a declaration; net +58,613 lines (286 shrank, 401 grew,
231 same). Measured, not asserted:

- **Audit batch 2 (the RBP frame).** Fabricated pointer arithmetic
  97,531 -> **83,314** (-14,217) in 3,126 -> 3,088 files, reproduced with an
  independent regex (the batch's own figure was -14,169, 0.3% apart).
  Shrinkers are the expected shape: `TypeConversion.cs` -658, `X86.cs`
  -592, `ConverterGroups.cs` -549, `VisualElement.cs` -375.
- **Shared-tail arity trim.** Shared calls carrying an invented trailing
  `0`: 3,880 -> **3,519** (-361) in 1,086 -> 923 files. Calls keep a real
  trailing `0`; mi 24077 keeps its four-argument `List<T>.CopyTo` tail.
- **Noreturn-shared forwarder returns.** `/* nothing */` **63 -> 0**, with
  63 `return Neon.<s8-variant>(...)` in `Arm.cs`.
- **Identical-render collapse + stub comments, tree-wide.** Resolved
  identical-render names 52 -> 109 occurrences; every `__SharedBodyStubs.cs`
  grows (mscorlib 1,250 -> 9,995 lines, UIElements 606 -> 5,162, ten more
  assemblies) from the native-disassembly comments that until now were
  promoted only for Assembly-CSharp.
- **Flat where it should be flat.** `goto`, `memN`, `qaddr` unchanged;
  `indirect` -4; `shared` 16,916 -> 16,834 (net **-82**).

Marker increases, read rather than waved through:
- `unknown` **+53 across 59 files** -- typed-but-unknown frame slots
  (`Vector3 vector35 = unknown;`) replacing fabricated pointer arithmetic
  in the same statements, which is the trade batch 2 documented. The
  fabricated count falls 14,217 in the same diff.
- **One** net shared-marker increase tree-wide, user-called and accepted:
  mi 23602 `StandingPeopleConcert.SpawnPeople` loses
  `Quaternion.Internal_FromEulerRad` to `sub_180895b20/*shared body, 9
  candidates*/`, because E3 typed the frame home `Vector3` and a partial
  vector store leaves the value honestly `unknown`, so the call argument is
  no longer a reconstructed `new Vector3 { ... }` literal for `_call` to key
  on. One lost callee name against a value that is no longer fabricated.

Evidence in `validation_reports/promotion_r9.json`. Suite at the promoted
commit: **1071 passed / 0 failed** (877 portable + 194 game). Scratch trees
removed. **Timing correction:** a full 91-image strict build is 1,085 s
(18.1 min) for 114,458 bodies on this box, not the 1,359 s the index and
`AGENTS.md` carried from the batch-1 measurement.

## Current work: one shared body, one argument list (2026-09-26, LANDED)

The `GetHashCode` mixed-VA item from the shared-residual audit is closed,
narrowly. What the audit had found was a rendering inconsistency, not a
missing identity: MSVC folds the no-arg `GetHashCode` forwarders onto one
body (`xor edx,edx; jmp 0x181b14c10`), so the same address printed two
different argument lists depending on how it was reached.

    // mi 8752 ConstructorInfo.GetHashCode, before
    return (int)sub_181b14c10/*shared body, 13 candidates*/(this, 0);
    // mi 3961 Delegate.GetHashCode, same address, called not jumped
    int num2 = (int)sub_181b14c10/*shared body, 13 candidates*/(this.m_target);

The `0` is callee-zeroed plumbing. The forwarder zeroes EDX for the callee,
no candidate at that address declares a second parameter, and the two twins
that *do* resolve at the same VA (`EventInfo` mi 8771, `FieldInfo` mi 8790)
already printed one argument. After: `return (int)sub_181b14c10/*shared
body, 13 candidates*/(this);` -- the call and the tail finally agree.

**The proof is 21j's, reused rather than reinvented.** Every candidate at an
address names a call into the same compiled machine code, so they all consume
the same argument registers, and the largest declared arity among them --
receiver included, plus the hidden sret buffer when the return is the
all-candidates consensus -- bounds the slots. `_call` has used that bound
since batch 21j; the inline loop is now `_shared_arity_cap`, and
`_shared_tail_keep` reuses it for a tail. Extracting it also hardened the
`_call` side for free: the old inline loop indexed `meta.methods[c[1]]`
unchecked and let a malformed candidate row propagate, while the helper
bounds the index and skips what it cannot read (`None` = nothing readable =
keep today's spelling).

**Narrow on purpose.** Only a trailing run of literal `0` is droppable, and
only below the cap, because that is the register a shared forwarder zeroed
(`xor edx,edx` / `mov r8d,0` right ahead of the jmp) rather than something
the source wrote. Everything else declines to today's spelling: a non-zero
extra argument inside the four argument registers, a single candidate, an
unreadable candidate, a cap that does not sit below the list, and a list of
one or fewer. Past `ARG_REGS` the zero-run check does not read at all --
those slots are stack-passed, where no candidate's declared arity can reach,
so the cap alone bounds them. A *resolved* tail is never touched -- an
identified callee owns its own signature, and the receiver /
hidden-generic / same-render proofs above the new trim still run first.

**Scale, measured rather than sampled.** The only methods this can touch are
those that `jmp` into a multi-candidate address: 5,437 of 114,458. That set
was lifted twice -- once from a pre-change source root (the package with the
three touched files restored from `HEAD`, so the working tree was never
stashed) and once from the new one -- and the two body sets diffed:

- **349 bodies changed / 363 lines, 0 new crashes** (0 pre, 0 post), 0
  line-count changes, 0 bodies longer. Every changed line is byte-for-byte
  its pre-image with the *last* `, 0` removed from that shared call's
  argument list; nothing else moved on any line.
- 386 methods fire in the real pass. The 37 whose body does not change have
  their shared marker replaced downstream (identical-render collapse:
  `return x == y;` at mi 2603), so the trim is invisible there, not wrong.

The instrumented census behind that: 775 fires -- 399 real pass, 376 dry
pass -- over 531 (method, address) pairs, 529 distinct methods, 112
addresses, and every fire removed exactly one argument (295 `2->1`,
413 `3->2`, 67 `4->3`). Largest families by distinct methods:
`0x182b75030` 97 (30 candidates, the `(this, 0)` `.ctor` shape),
`0x181af7520` 73 (string `Equals`/`op_Equality`, `(x, y, 0)`), `0x182be3aa0`
54 (`DockInSlot`), `0x1807ee180` 29, `0x181bb6bf0` 16 (handle
`Release`/`Close`), `0x181cffb70` 15 (`GetHashCode`).

**Unchanged, deliberately.** Calls were already bounded by 21j, so the 196
tree-wide `return (T)sub_...(... , 0)` lines whose `0` is a real argument
(`op_Equality(x, null)` and friends, cap 2 = the list) keep it. So does a
tail whose extra registers are genuinely read: `mi 24077 SelectNuisanceType`
still prints the four-argument `List<T>.CopyTo` tail at `0x180df9c30`, the
probed case where the registry missed a sharer that dispatches on R8.

**Accepted risk, stated rather than hidden.** A registry-missed sharer whose
extra register is a *zero* the body really reads would lose that argument,
and the absence of such a sharer is unprovable from the registry. The visible
alternative -- one body printing `(x)` at a call and `(x, 0)` at a tail, in
the same file -- is the defect being removed, and it is the shape a reader
cannot tell from a real parameter.

Tests: +18 portable (`tests/test_shared_tail_arity.py`: cap arithmetic, the
sret slot, generic specs, unreadable rows, and every decline arm), +6 game
(`tests/test_game_shared_tail_arity.py`: mi 8752 / 13198 / 78202 / 1231
trimmed, mi 8771 / 8790 twins unchanged, mi 3961's call site unchanged, mi
24077's read registers unchanged). Full suite **1071 passed / 0 failed**
(877 portable + 194 game) with the change in place; no golden moved.

## Current work: audit batch 2 -- the RBP frame survives a CFG merge (2026-09-26, LANDED)

The largest quality defect the audit found: a method that sets up a frame
pointer loses it at the first CFG merge, and every `[rbp+N]` in the merged
region becomes pointer arithmetic on the never-written seed.

**E1 -- the frame fact.** `_rbp_is_frame()` read the register *value*, and
the pass-2 phi merge rewrites that value out from under it. A never-written
`RBP = None` (exactly what `mov rbp,rsp` produces, since RSP is never
tracked) becomes `Expr('?', None, '?')` at `analyze.py:460`, and `_bind`
then rewrites that into a temp name. In a merged block *every* arm of the
predicate failed -- `None`, `'?addr'`, `_unk`, `&s_` -- and `_read_mem` /
`_mem_lvalue` fell out of the frame branch into the raw-deref branch.
Measured on `WrapRopePlayerController` (mi 24062, `push rbp; mov rbp,rsp;
sub rsp,50h`): **21 sites** like

    ((byte*)obj9 - 0x30)[0] = vector31;      // movsd [rbp-30h], xmm6
    ((float*)obj9 - 0x28)[0] = real1;         // mov   [rbp-28h], ebx
    this.rb.AddForce((obj9 - 0x30), ForceMode.Acceleration);

`obj9` is not a pointer, and because it was *named* every statement was legal
C#, so the parse gate saw nothing. An instrumented trace showed 64
consultations split across two states -- 32 with RBP text `'?'`, 32 with
`'v45'` -- which is why the obvious `t == '?'` test fixed only half of them.

The fix tracks the fact instead of inferring it: `_rbp_frame` is set by
`mov rbp,rsp`, cleared by any other write to RBP inside `set_reg` (the one
place every register write passes through), and never derived from the
register value. It survives the merge because the merge installs values with
`L.regs[k] = ...` and so bypasses `set_reg`. `_defpos` is not a usable
discriminator either: `_copy_expr` drops it, so "no definition site" cannot
distinguish an unwritten register from a copy of a written one.

Same method after: typed `UnityEngine.Vector3` locals, a real
`Vector3.Normalize(...)`, and the real `this.rb.AddForce(vector32,
ForceMode.Acceleration)`. The 16-byte `movsd` store into a Vector3 home
stays `vector32 = unknown`, which is the honest marker, not a guess.

**E3 -- one home, one key.** `slot_var` keys by `off + rsp_delta` and names
by `abs(off)`, but callers disagreed on sign: the RSP-copy path passes an
already sign-extended `_stack_address`, while the RSP/RBP direct paths and
the LEA path pass `ins.memory_displacement` raw (iced-x86 reports `[rbp-0x30]`
as `0xffffffffffffffd0`). One method held two coordinate systems for one
native home -- mi 24062 held both `(-24, 's_40')` and
`(18446744073709551480, 's_ffffffffffffffd0')` -- so a `[copy+N]` write and
an `[rsp+M]` read of one slot became two C# locals and the provenance layer
could not see the naming layer. `slot_var` now normalizes with `sdisp` at
that single choke point; `sdisp` is idempotent on an already-negative value,
so every correct caller's name is byte-identical and only the raw paths move.

**Scale.** A regex census of the pre-batch-2 full build counts **87,471
fabricated-pointer sites in 2,795 files** -- well past the audit's
per-method extrapolation (~25k instruction sites), because an affected
method carries many sites. Worst hit: `Unity.Mathematics` at 22,432, then
UIElements 8,576, mscorlib 6,830, System.Xml 4,713. Assembly-CSharp scoped
rebuild: **2,938 -> 2,027** (-911, -31%) with 60 of 491 files changed. The
residue is the honest unknown-base decline rather than the frame bug: a
`[rbp+N]` off a base the lifter never proved still renders raw, which is the
intended direction.

Tests: +16 portable (`tests/test_rbp_frame.py`), +8 game
(`tests/test_game_rbp_frame.py`, `tests/test_game_rbp_frame_reset.py`).

Gates, all against the final source:
- **Paired full-corpus sweep, pre- vs post-**: 116,178 methods, 0 crashes
  both sides; `into_block` **8,075 / 2,046 identical** (so the +4 sites /
  -2 methods against the `CLAUDE.md` baseline is pre-existing drift from
  earlier commits, not this batch); brace 0 unclosed / 0 underflow; 0
  dangling gotos; 0 empty args; tail-arg changes 1,881 / methods 1,801
  identical; 2,253,753 -> 2,253,029 lines.
- **Per-method compare**: 1,537 changed bodies, **0 structural changes, 0
  new crashes**, 0 added / 0 removed methods.
- **Full strict rebuild**: 11,183 type files / 114,458 bodies / 0 failed /
  0 structured fallbacks / 0 type-emission failures; brace audit
  **0 unbalanced**; parse gate **0 bad files / 0 ERROR / 0 MISSING / 0
  recovery nodes**, exit 0.
- Corpus-wide fabricated-pointer sites **87,471 -> 73,302** (-14,169,
  -16.2%), files 2,795 -> 2,752.

Read before accepting, per the golden rule:
- `Computer.cs`: 72 fabricated sites -> 0, and MSVC's struct-copy idiom
  comes back as real Unity code -- twelve invented byte-pokes through
  `obj13` become `Navigation navigation2 = navigation1; navigation1.m_Mode
  = Mode.Vertical; this.inputText.navigation = navigation1;`.
- `CurrentDayManager.cs`: 51 -> 0, `Quaternion quaternion1 = default;`
  replacing `((int*)obj1 + 0x28)[0] = 0;`.
- `mi 104428 GetBounds` (golden moved): the value no longer round-trips
  through a fabricated `((byte*)obj41 + 0x0)[0]` hop before reaching the
  frame slot. The surviving `((byte*)obj40 + 0x0)[0]` is the honest
  unknown-base decline, not a regression.
- `mi 105455 ValidateLine` (486 lines, `lea rbp,[rsp-70h]`): recovering the
  frame **retyped** its slots from `object` to `UnityEngine.Vector3`, so
  the `object obj87 = unknown;` twin that test pinned no longer occurs
  there and the use-site is now the better `UnityEngine.Vector3 vector36 =
  vector34.normalized;`. The dead-unknown-store pass stays pinned by the
  LagCompensationUtils test.

One honest cost, measured rather than waved through. `mi 32833 OnStateEvent`
is a `lea rbp,[rsp-38h]` method, so it moves under **E3 alone** (E1 does
not touch LEA frames): `int num1 = default;` becomes `int num1 = 0;
num1 = 0f;`. The int type and the zero value are now correctly recovered
from the slot's `num1 != 1` use, but a **new CS0266** appears -- `0f`
assigned to an `int` local -- next to the pre-existing one (`object` into
`int`). Counted across Assembly-CSharp, scalar-declared-with-float-RHS goes
**550 -> 557 (+7)**, in **3 of the 60 changed files**. That is a
pre-existing lossy area (550 instances before this batch) touched
marginally, against 911 fabricated pointer sites removed in the same
assembly, so it is accepted and recorded here rather than used as a reason
to narrow a provably-correct key-space fix.

Invariants recorded in `CLAUDE.md`.

## Current work: audit batch 1 -- per-instance caches, struct sizes, ELF gate (2026-09-26, LANDED)

A read-only audit of the whole package (lifter / dec+emitter / runtime+
metadata / repo+docs, plus an independent corpus census and a full timed
rebuild) produced three defects that all share one failure mode: silently
wrong rather than honestly raw. All three are fixed here, and none changes
a byte of emitted output.

**1. Three class-level caches keyed by a binary-local TypeDef index.**
`Decompiler._TDNAME_CACHE` (`dec/sugar.py:344`) was a class attribute
written through the `_LateDecompiler` proxy, and `Emitter._us_cache`
(`emitter.py:637`) / `_delegate_cache` (`:671`) were mutable
class-attribute dicts never reset in `__init__`. TypeDef indices are
binary-local -- the invariant `CLAUDE.md` states for `_chain_cache` /
`_bases_cache` -- so a shared map hands a second `Decompiler` / `Emitter`
(a second fixture, which the open Cpp2IL cross-check needs) **another
binary's index**. Reproduced: with `('Alpha','Widget')` at index 0 in
binary A and index 1 in binary B, B resolved 0, and `_static_field_name`
then emits *another type's* static field name -- a wrong name with no
marker, not a crash. All four maps are now per instance, created lazily
via `self.__dict__.setdefault` because ~80 test sites build a
`Lifter`/`Decompiler`/`Emitter` with `__new__` and never run `__init__`.
The two delegate answers also move into separate dicts: they shared one
dict, distinguishable only because an `int` key can never equal a
`('viable', int)` key. The `Emitter._delegate_cache.clear()` workaround at
`tests/test_review113_type_decls.py:27` existed only because of the class
attribute and is gone.

**2. Negative struct sizes.** `runtime/registration.py:522` read
`v - 0x10 if v else None`, whose guard caught only `v == 0`, so every
`0 < instance_size < 0x10` became a **negative** size -- 91 rows in the
fixture (values `-15` and `-8`, all `<Module>` definitions), against a
comment three lines above promising "kept as `None` rather than a
negative number". Nothing consumes those today (`returns_sret` tests
`== 0x11`, `_return_abi_is_known` tests `> 0`), which is luck rather than
design: a negative size is exactly the value that flips a hidden-sret
decision and shifts every argument register. Now `v >= 0x10`.

**3. The Android registration fallback ran on a PE.** `cli.py` caught
any `RuntimeError` from `find_registrations()` and then tried
`find_registrations_android()`, which assumes a *different struct
shape*. Probed on the x64 fixture it does not fail: `code_reg_va =
0x183067830` against the classic `0x183067820` -- 0x10 low -- with the
same 91 modules and the same 116,178/128,954 resolved coverage. So a PE
with no classic registration traded a clean error for a silently wrong
one. The fallback is now gated on `isinstance(bin_, ELF)`, and the whole
registration phase reports `error:` instead of tracebacking.

Tests: +7 portable (`tests/test_cache_isolation.py`), +3 game
(`tests/test_game_type_sizes.py`). Full suite **1023 passed / 0 failed**
(843 portable + 180 game), no golden regeneration -- the 64 frozen bodies
are unchanged, which is the first evidence the batch is output-neutral.
Output-neutrality gate: a scoped strict rebuild (mscorlib,
Assembly-CSharp, Unity.Mathematics, Fusion.Runtime) is byte-identical to
the same assemblies from the pre-patch full build. Invariants recorded in
`CLAUDE.md`. The `~7-9 min` full-rebuild figure at `CLAUDE.md:407` is
**stale**: measured 1,359 s (22.7 min) for 114,458 bodies on this
12-core box, against a 1,374 s serial prediction (1.5% error).

## Current work: constant-zero fold DISPROVED (2026-09-25, DOCUMENTED)

Subagent census + independent ground-truth probes closed the
"constant-zero fold (239 sites, 2 VAs)" as a fold slice -- no source
change, markers stay honest.

The 2 VAs (scan counts sum exactly 216 + 23 = 239; claimed N ==
method+generic on both):
- `0x180625830` (216 sites): `xor al,al; ret`. 459 method owners
  (`bool` 456 + 3 structs) + 3,075 generic sharers. `xor al,al`
  zeroes only the low byte -- and struct owners share the address
  (probed mi 5208 `Task.Yield->YieldAwaitable` at the same VA), so
  multi-byte readers take entry-stale upper bits: not even
  value-uniform, disproved at native level before typing.
- `0x180507630` (23 sites): `xor eax,eax; ret`. Value-uniform zero
  (zero-extends full rax), but 304 owners across `int`/`string`/
  `XmlSchema`/`object`/`Material`/`long`/`Nullable<int>`/enums/arrays
  + 17 generic sharers -- no single C# literal spells zero across
  them; generic gate blocks regardless.

Call-site shapes (probed, not just scanned): `0x180625830` fires only
in `MoveNext()` triple-patterns with `object` results
(`object obj25 = sub_180625830/*shared body, 3534 candidates*/(0)`,
forwarded then `== null` null-tested) -- folding to `false`/`0`
mistypes the box, guesses the null test, and corrupts awaiter slots.
`0x180507630` sites are heterogeneous reference casts
(`(Material)sub(...)`, `return sub(...)` as reference) where `0`
does not compile; only `null` would work, needing owner proof.
Neither VA is the bare-`ret`, identity-leaf, string-fallback, or
struct-buffer zero nearby (`0x180506120`/`0x18063ac90`/
`0x1825b1150`/`0x180d931a0` all disjoint, checked).

This also confronts the unknown-never-becomes-zero guardrail
(`test_recovery_completion.py:490`): a fold here would rewrite
untyped `object`/`unknown` text, exactly what the pin forbids.
Verdict: decline both VAs. Next payoff: the ToString/op_Implicit
static+arity spray probe (865 sites, 1 VA `0x1825b1150`, disjoint).
No goldens moved; suite untouched (no source change; portable
836/0 re-verified green this session).

## Current work: same-name receiver pick DISPROVED (2026-09-25, DOCUMENTED)

Subagent census + ground-truth probes closed the multi-owner same-name
bucket as a return/static/arity elimination slice -- no source change,
markers stay honest.

Census (read-only regex over `final_out/` 11,183 files + a per-VA
`Il2Cpp.addr_candidates` join; scripts + `scan.json`/`join.json` live
only in temp): 2,772 sites / 159 VAs with one shared short name across
owner typedefs (audit's 2,752/155 plus the r8 ACS churn delta; marker N
== live method+generic counts on all spot checks). 54% of bucket sites
(1,493 / 29 VAs) carry generic sharers, so any sig slicer must decline
them first anyway.

Probes (`tools/inspect_methods.py`, `PYTHONHASHSEED=0`):
- GetResult 8478 vs 8497 share `0x181baa030` byte-identically, both
  instance `()->void`; caller 62090 passes `&object` with a void use --
  return, static/instance and arity are all vacuous.
- get_IsCompleted 8475 vs 8494, both instance `()->bool` (+ 34 generic
  sharers); the `test al,al` bool use is shared by both candidates.
- float2/3/4 `get_Item` 70880/71276/71965 share `0x180d259b0`, all
  instance `(int)->float` (+ 2 generic) -- generic gate blocks regardless.
- `InternedString.ToString` 35666 (instance, 0 params) vs `op_Implicit`
  35675 (static, 1 param) share `0x1825b1150` (`mov rax,[rcx]...ret`),
  865 sites: both consume exactly one register and return `string`, so
  static/instance+arity cannot split them; callers pass `&object`
  (32174 `string text1 = (string)sub_1825b1150(&obj14)`). Same shape for
  the `Char.ToString` twins (82 sites).
- `HexToInt` 96557 (`int`) vs 110140 (`uint`) share `0x182af9c50`
  byte-identically; caller 110055's uses are sign-agnostic
  (`num58 + (num57 << 4)` -- `+`/`<<` identical for int/uint), so a
  return-use rule must decline; a fire needs a sign-proving use, none
  found.
- `op_Implicit` triple `0x182da54f0` (Angle/StyleFloat/TimeValue):
  caller 13332 passes untyped `object`, result flows to `object` --
  use-type is `object`, declines.
- Mixed `GetHashCode` VA `0x181b14c10` (10 sites, 12 instance +
  `RuntimeHelpers` static): the shared body is a 2-insn forwarder
  (`xor edx,edx; jmp`), so the trailing `0` in `(this, 0)` renders is
  callee-zeroed stale, not a param -- and both shapes still fit one
  register. Tail rendering is already inconsistent across identical
  twins there (EventInfo/FieldInfo resolve, ConstructorInfo keeps the
  marker); touch nothing.

Verdict: the headline ~1.9k (GetResult 412 + get_IsCompleted 347 +
floatN get_Item 323 + ToString/op_Implicit 865) needs receiver proof
(field sidecar + use->def + whole-tile preference, per the 25687/24238
TaskAwaiter precedent) or instantiation proof -- not sig elimination.
Remaining next payoff (constant-zero since disproved, see above): the
ToString/op_Implicit spray probe (865 sites, 1 VA `0x1825b1150`).
No goldens moved; suite untouched (no source change).

## Current work: promotion r8 Assembly-CSharp (2026-09-24, PROMOTED)

User-scoped (Assembly-CSharp only; full-tree rebuild aborted by user
call after ACS completed). Strict `--only Assembly-CSharp` rebuild from
clean HEAD `e3c7512`: 490 type files / 6,622 bodies / 0 failed / 0
fallbacks / 0 type-emission failures; brace 0 unbalanced; parse 0/0/0;
file set identical to r7 ACS (491 paths, 4 files differ). Triage:
identical-render `ComputeStringHash` x3 (ControllerLayoutMenu,
InventoryManager, Telephone) + stub disassembly comments
(`__SharedBodyStubs.cs` 367 -> 2,872 lines); shared 1,086 -> 1,083,
indirect/unknown/goto/memN flat, zero per-file marker increases. An
independent second build was byte-identical (determinism cross-check).
Promoted by mirror copy (ACS aggregate `d6b9147c…ffcc`); evidence in
`validation_reports/promotion_r8.json`. Scratch trees removed; tree
committed and pushed. Rest of `final_out/` still holds r7.

## Current work: noreturn-shared forwarder returns (2026-09-24, LANDED)

The 63 `/* nothing */` bodies (all `Neon` in `Arm.cs`) were shared
`call; int3` forwarders (`vmvn/vand/vorn` families) whose single proven
target throws `NotImplementedException` on x64. `_dead_shared_forwarder`
dropped the pending call; `_dead_shared_forwarder_return` now renders
`return Target(args);` when the target is one readable MethodDef with
the caller's exact return tuple (both non-void) and the call text is
marker-free -- MSVC's own abort is the noreturn evidence, so the tail
return compiles and names only proven identities. Everything else
declines to the old drop.

Evidence: fresh lifts of the whole 2,407-method Neon type show 0
`/* nothing */` and 63 `return Neon.<s8-variant>(args);` (e.g. 107037
`return Neon.vmvn_s8(a0);`, 107123 `return Neon.vorn_s8(a0, a1);`).
Corpus shape census: 70 methods match, all Neon, all return-equal, so
the blast radius is one family. Tests: +2 portable (fire + 7 declines)
+2 game; full suite 1013 passed / 0 failed after one reviewed golden
update (107123 only). `final_out/` still holds r7 (unpromoted).

## Current work: shared stubs show SOME code (2026-09-24, LANDED)

Unresolved `__SharedBodyStubs` entries listed only the owner note plus a
throwing body -- no code. Each stub now also lists the address's first
native instructions (up to 16, stopping at the first ret/int3/ud2) as
`//` comments: real bytes, no managed owner selected. The signature,
throw, and owner note are unchanged, so call sites and runtime honesty
are byte-identical; failures decline to the old throw-only shape.
Probed ground truth: 0x18063ac90 shows `mov rax,rcx; ret` (the identity
leaf), 0x1825b1150 its 7-insn null-check fallback, 0x180506120 a bare
`ret 0`. Tests: +5 portable; full suite 1009 passed / 0 failed.

## Current work: identical-render shared collapse (2026-09-24, LANDED)

Method-only twins that render identically collapse to the first row:
same owner-qualified name, same static/instance shape, same exact
parameter types, same return. Call text, arity trim and result type
are identical either way, so the pick is unobservable, not an owner
guess. Constructors, generic methods/specs and sret returns decline;
everything else keeps the honest marker. Tails use the same proof
(the tail path already collapsed identical renders via caller-return
filtering; non-tails had no equivalent until now). The hash-name
match also accepts `<PrivateImplementationDetails>.` owners so the
resolved `ComputeStringHash` still feeds `switch(string)`.

Evidence: 70 sites resolve (ComputeStringHash 33, HashHelpers.Combine
28, Kernel.Multiply 6, Enumerator.Dispose 2, Locale.GetText 1);
ValueStringBuilder .ctor 23 honestly retained (ctor decline).
Ground truth: 24694 renders
`uint num15 = <PrivateImplementationDetails>.ComputeStringHash(text1);`
(switch gotos still decline, as triaged); 2991/2992 render only
`System.Numerics.Hashing.HashHelpers.Combine` (tails already did);
422/120851 render `Kernel.Multiply` / `Locale.GetText`. Tests: +7
portable (fire + owner/sig/ctor/generic/sret/arity declines) +3 game;
full suite 1004 passed / 0 failed. No goldens changed; `final_out/`
holds r7.

## Current work: shared-residual audit (2026-09-24, DOCUMENTED)

Why the 16,919 remaining shared-body markers stay (r7 tree, per-VA
metadata join over all 1,011 bodies with markers). Partitions below
overlap on the generic dimension; treats are per bucket:
- method+generic mixes: 5,676 sites / 137 VAs need instantiation
  proof (e.g. `BindingsAllocator.GetNativeOwnedDataPointer` sharing
  one body with 15 `ConvertExistingDataToNativeArray` specs) --
  synthetic-table program, the largest bucket.
- Same-typedef multi-signature: 5,432 / 337. Identical twins
  (F1/F2/F3) are permanently unresolvable; overloads need
  conversion-witness or exact-only arg-type elimination (future).
- Multi-owner same method name: 2,752 / 155 (GetResult/get_IsCompleted/
  get_Item/ToString pairs) -- sig elimination DISPROVED 2026-09-25
  (see top sections); needs receiver/instantiation proof (sidecar).
- Multi-owner different names: 3,859 / 259, incl. mega-shared tiny
  bodies -- owner proof at scale (field sidecar + use→def).
- Static/instance mixes: 3,394 / 43 (ToString/op_Implicit 865 sites) --
  mostly mega-shared tiny bodies (declined); the crisp `0x1825b1150`
  pair's spray probe is still open (see index).
- Non-method (pure generic) addresses: 1,282 / 191 -- instantiation
  proof, same program as the first bucket.
- Identical full signatures: 200 / 25 -- same-render collapsing LANDED
  2026-09-24 (70 sites); remainder keeps markers.
- Corrected mid-audit: an early "14 true-duplicate VAs" read was a
  filter artifact (method rows only, hiding generic sharers); the full
  map has ZERO exact-duplicate addresses, so a registration dedup was
  prototyped and reverted before landing (no effect, no test could pin
  it). Audit your tools, not just the tree.

## Current work: promotion r7 (2026-09-24, PROMOTED)

User-authorized (promotion on call). Strict rebuild `r7_out1` from
clean HEAD `d109bb2`: 11,183 files / 114,458 bodies / 0 failed / 0
fallbacks / 0 type-emission failures; brace 0 unbalanced; parse 0/0/0;
file set identical to r5 (11,276 paths, 745 files differ). Triage: five
audited shared-body rounds (Object/value-type/static-signature/
identity/string-equality); shared 18,889 → 16,919 (−121 files),
indirect 6,262 → 6,061 (−48 files), unknown −34, memN/goto/`?addr`
flat, zero per-file marker increases; sampled resolutions verified
(`this.MemberwiseClone()`, `== "Gamepad"`, `op_Inequality` with TimeSpan
declines kept). No golden regen needed beyond the two reviewed updates
already in-tree (suite 994/0 green proves currency). Promoted by mirror
copy (aggregate `19aa6964…f137502`); evidence in
`validation_reports/promotion_r7.json`. Scratch tree removed; tree
committed and pushed.

## Current work: shared string equality semantics (2026-09-24, VALIDATED)

`System.String.Equals(string,string)` and `op_Equality(string,string)`
share one native body and the same static bool ABI. When both operands are
tracked strings, string literals, or null, render their common `==`
behavior without selecting an original MethodDef or source spelling.
Dropped extra register expressions must be pure. The five previously
marked `ReadReference` comparisons now spell `ReadName() == literal`;
unknown operand types retain the marker. All 994 full-suite tests pass.
The strict Assembly-CSharp build covered 490 files / 6,622 bodies with
0 failures / 0 fallbacks / 0 type-emission failures, brace 0, parse
0/0/0. In those files, this alias's markers
fell 138 → 11 against promoted r5; all shared markers fell 1,287 →
1,086 with no per-file increases (that total includes earlier
unpromoted changes). `final_out/` remains unchanged.

## Current work: exact shared identity leaf (2026-09-24, VALIDATED)

The exact executable bytes `mov rax, rcx; ret` prove that a shared native
body copies its first argument without selecting any MethodDef owner. The
fold requires a pure tracked first argument and pure extra register values;
effectful expressions, unknown values, pointers without a safe tracked
value, and any other native bytes retain the honest shared-body marker.
`<FindGraphWhichInheritsFrom>b__0` folds its `this.type` copy but retains
the `graph.GetType()` call marker. `Touchscreen.OnStateEvent` now carries
the copied `InputEvent*` type through its field reads; its reviewed
MethodDef 32833 golden was updated.

Evidence: 992 full-suite tests pass. Strict AstarPathfindingProject and
Unity.InputSystem build: 513 files / 7,249 bodies, 0 failures / 0
fallbacks / 0 type-emission failures; brace 0, parse 0/0/0. In those
files, address `0x18063ac90` markers fell 55 → 1 against promoted r5;
all shared markers fell 302 → 241 in 16 changed files with no per-file
increase (the latter includes preceding unpromoted changes). `final_out/`
remains unchanged.

## Current work: shared static signature proof (2026-09-24, VALIDATED)

A common non-generic static ABI plus call-site parameter types can name a
shared native address when exactly one metadata owner accepts every known
argument. Class compatibility includes ancestors; an `object` or interface
parameter blocks the proof because a more specific observed type could
also bind it. Pointer/byref, sret, mixed arity, unsupported argument
types, stale typed registers beyond the declared arity, and duplicate
signatures decline. This names two `Type.op_Inequality` calls in
`DateTimeFormat.ExpandPredefinedFormat` (MethodDef 1745) while its two
`TimeSpan` sites keep markers: one operand is exposed only as `_ticks`.
The `Object.Equals` / reflection `op_Equality` family stays ambiguous.

Evidence: 986 full-suite tests pass; strict mscorlib scratch build
1,350 files / 10,715 bodies, 0 failures / 0 fallbacks / 0 type-emission
failures, brace 0, parse 0/0/0. Against promoted r5, mscorlib markers
fell 1,374 → 1,301 with no per-file increases; that comparison includes
the preceding unpromoted receiver fixes. `final_out/` remains unchanged.

## Current work: exact value-type shared receivers (2026-09-24, VALIDATED)

An address-of stack slot can identify a shared instance getter when its
tracked pointee is one concrete nongeneric value TypeDef. The candidate
set must contain only readable instance methods with no sret; a second
method or MethodSpec on the same declaring type declines. Static calls,
conflicting type evidence, open owners, and untyped pointer arithmetic
keep the shared marker. This resolves `StyleValueHandle.get_valueType`
from `&s_8` in `IsVarFunction`, while `ReadAsString`'s raw pointer stays
unresolved. A closed enum parameter now casts a proven integer expression
at the call argument, preserving `StyleEnum<SliceType>.ctor((SliceType)
styleInt.value, keyword)` after its two getter markers disappear.

Evidence: full suite 978 passed / 0 failed after one reviewed golden
update (MethodDef 18054 only); strict UIElements scratch build 802 files /
8,997 bodies, 0 failed / 0 fallbacks / 0 type-emission failures,
brace 0, parse 0/0/0. Shared markers in UIElements fell 1,332 → 1,277
(55 fewer in six files, no increases). The prior r5 promoted tree remains
the comparison reference; no output promotion here.

## Current work: Object shared-body fallback (2026-09-24, VALIDATED)

A narrow full-candidate receiver proof resolves `Delegate.Clone` /
`Object.MemberwiseClone` shared body calls for a concrete class receiver
outside Delegate's inheritance chain. Every candidate must be a closed,
parameterless, non-sret instance MethodDef; the receiver must have a
class TypeDef and exactly Object may remain in its complete base chain.
The broad shared-receiver heuristic still excludes Object. Typed
`FUniversalVariable.Copy` and `XmlWriterSettings.Clone` now render
`this.MemberwiseClone()`; the untyped `SchemaCollectionCompiler` site
keeps its marker.

Validation: 969 full-suite tests pass; compileall passes. A strict
`Assembly-CSharp,System.Xml` scratch build lifted 13,204 bodies with
0 failures / 0 structured fallbacks / 0 type-emission failures;
1,048 files have 0 unbalanced braces and parse 0/0/0. In those
assemblies, shared markers fell 2,195 → 2,174 with zero per-file
increases. `final_out/` remains the r5 promoted reference.

## Current work: shared/indirect disproofs + measurements (2026-09-24, DOCUMENTED)

Subagent census follow-ups that disproved (with native/metadata
evidence) rather than landed -- no source change, by the same rule as
the generic-slice closure. Small-N shared bodies are NOT in general
resolvable: F2 `StartCoroutine` twins (56318/56319, identical static
  `(IEnumerator)` signatures), F1 string twins (602/604
  `Equals`/`op_Equality`, identical static `(string,string)->bool` over
  one folded body -- method identity and source spelling remain unknown;
  typed operands now permit their shared `==` semantics), F3 Transform
  triple (56836/56838/56840, same declaring
typedef, so the same-typedef-twins invariant applies directly). Their
markers stay honestly.
- C-shape text fold (`((byte*)R+0)[0]` to klass) is unsound: EntryDoor
  25181's native loads a struct field pointer (`mov rsi,[rsp+78h]` +
  null check = the embedded `List<Enemy>` of a `List_1<Enemy>.Enumerator`
  home) and dispatches slot 30 on the List, so a klass fold would
  misread struct first-fields. The correct fix is struct-field folding
  into the existing VIRT_CALL path (lifter field-layout reasoning) --
  deferred to the sidecar program.
- Dead-unknown window extension measured: 42 adjacent vs +6 in 1-3
  statement windows -- declined, not worth the machinery.
- B2 `this`-base count is 0/271, so the batch-38b bare-base guard
  stands for lack of any trivially-provable base.
- The 32 typeof-decl-but-indirect sites are heterogeneous non-shapes,
  correctly declined (e.g. SessionInfo: no slot computation exists;
  the typeof travels as a call argument, not a dispatch proof).
- Next lead if wanted: deref-trail slots (335 sites shaped
  `... + ((byte*)TOK + 0x0)[0]` with inline typeof nearby) need a
  typedef-to-implemented-interfaces table plus unique-match gating;
  that table is sidecar-program plumbing, so this stays designed.

## Current work: dead-unknown stores + inline-typeof dispatch (2026-09-24, LANDED)

Two subagent-triaged slices from the shared/indirect/unknown census
(18,889 shared / 6,262 indirect / ~13.1k unknown). (A) Adjacent
`LHS = unknown;` overwritten by the next statement folds away
(`_drop_dead_unknown_store`, after the fix-99 DCE rerun): bare/index-
slot lines drop, plain-typed decls strip to `Type x;`; labels, `==`,
calls/`new` in the destination, `var`/`ref`/keyword decls, fields, and
second-RHS reads of the destination all decline. Ground truth:
LagCompensationUtils 63027 twins, RaycastModifier 105455 strip + use
survival, GraphCollision pointer slot honestly declines (reassign is 4
stmts away, not adjacent). (B) Interface dispatch with inline
`typeof(IFace)` in the scan-loop comparator (`_itf_inline_typeof`,
dual agreement with the slot trail token's declared type; the trail
token is corroboration only, never rendered; `typeof(X).Member` static
access never counts as a scan comparison). Ground truth:
EndlessGenerationManager 25132 `values.GetEnumerator()`.

Evidence: full strict rebuild r6_out1 (11,183 files / 114,458 bodies,
0 failed / 0 fallbacks, brace 0, parse 0/0/0): 124 files differ --
112 dispatch resolutions (`get_Item`/`TryGetValue`/`Equals`/`Compare`/
`MoveNext`/etc. on named receivers; NetworkRunner/ObiSolver/Path keep
markers for lack of agreement) and 11 dead-store folds plus 1 mixed,
all hand-sampled correct; indirect 6,262 → 6,052 (−50 files), unknown
13,097 → 13,063, shared/mem/goto/`?addr` flat, zero per-file marker
increases. Tests: +4 portable +3 game; focused 28 passed; full suite
964 passed / 0 failed. No goldens changed; `final_out/` holds r5.

## Current work: promotion r5 (2026-09-24, PROMOTED)

User-authorized (standing permission for regen/promotion whenever
needed). Strict rebuild `r5_out1` from clean HEAD `37811e9`: 11,183
files / 114,458 bodies / 0 failed / 0 fallbacks / 0 type-emission
failures; brace 0 unbalanced; parse 0/0/0; file set identical to r4d
(11,276 paths, 456 files differ). Triage: scalar prologue-copy typing
corpus-wide plus FP32/R8 unary-leaf recovery (log10f + double leaf,
immediate/conditional/conversion/copy consumes); net −79 unknown (−1
file), shared/indirect/memN/goto/`?addr` flat, zero per-file marker
increases; no regressions. No golden regen was needed (green suite
proves currency: 957 passed / 0 failed). Promoted by mirror copy
(aggregate `5a31b119…0d79`); evidence in
`validation_reports/promotion_r5.json`. Scratch tree removed; tree
committed and pushed.

## Current work: R8 double-unary leaves (2026-09-24, LANDED)

The FP proof extends to double callees, proved on 0x1804CD9D0 (CRT
errno-adjacent double leaf behind Slider's `sub_1804CD9D0` calls):
+MOVSD/+SETcc/+SUBSD table shapes, register-count shifts (op1 read is
tracked, MUST discounts scratch uses), frameless functions over the
0x28 shadow store (entry-block-dominated homes read clean, others join
SHADOWARG), and GEN/KILL over XMM0-15 (YMM/ZMM fold in). The last item
closed a real hole found by the re-sweep: `mulss xmm0,xmm1` passed with
inputs=={XMM0} and the render dropped the multiplier; it now declines
with inputs=={XMM0,XMM1} (pinned portably and by PathProcessor 104653's
unchanged object spray). The consumer gate returns 'f'/'d'/None;
CVTSD2SI/CVTTSD2SI with source XMM0 fire double, and the render binds
`double` in XMM0. Fix-104 casts stay for both widths (they unbox
against the object stubs -- verified by declaration audit).

Evidence: SliderLerpUnclamped (15267) chains
`float real2 = (float)sub_1804cdb00(...)` into
`double real3 = (double)sub_1804CD9D0((double)(real2))` and on to
`(int)`; FEngineering (2 sites), Panel (2 pixel sites), and
StylePropertyAnimationSystem (1 site) gain the same double recovery;
remaining sites decline honestly. Corpus sweep holds at exactly 2
passing targets (log10f + R8). Tests: +3 portable (SD widths,
binary-op decline, frameless/SHADOWARG) +1 game (binary-op pin), -1
obsolete cast-skip test; focused 21 passed; full suite 957 passed /
0 failed. Strict scratch builds
(490/6,622 + 802/8,997, all zero), brace 0, parse 0/0/0. Isolated diff
vs stashed baseline: 4 files, all improvements plus renumber cascades.
No goldens changed.

## Current work: FP32-unary conversion/copy consumes (2026-09-24, LANDED)

The consumer gate additionally fires on float-consuming conversions
with source XMM0 (`cvtss2sd/cvtss2si/cvttss2si`, rendered by the
existing `(double)/(int)` casts) and on `movaps` reg,reg copies from
XMM0 (bitwise copy preserves the value); double-source conversions
(`cvtsd2ss` et al) and VEX forms still decline. A new `_fp32_arg_ok`
helper declines arguments containing a bare `?` (never parses;
`?.`/`??`/`unknown` pass).

Evidence: Slider `SliderLerpUnclamped` (15267) recovers two sites --
`float real2 = sub_1804cdb00(real1 & float.NaN);` and `float real3 =
...` feeding `(double)(real3)` / `(int)(5.0d - (double)(real3))`
chains; the third site honestly declines (its argument carries
`(double)(?)`, unspellable until SIMD-lane provenance heals upstream).
Corpus-isolated diff vs stashed baseline: exactly 1 file (Slider.cs),
improvements plus renumber cascades. Tests: +2 portable (conversion/
copy fires, arg spellability) +1 game; focused 18 passed; full suite
954 passed / 0 failed. Strict scratch builds (490/6,622 + 802/8,997,
all zero), brace 0, parse 0/0/0. No goldens changed.

## Current work: FP32-unary conditional consume (2026-09-24, LANDED)

`_fp32_scalar_next` now walks up to 16 instructions forward to the
scalar XMM0 consume instead of requiring it immediately after the call.
Skipped instructions must not touch the value channel (no XMM0/YMM0
mention, no calls, no returns/jumps/indirect flow, no kernel
transitions); flag tests, conditional branches, NOPs, constant loads,
and unrelated moves all skip. A branch target landing between call and
consume declines (merge, not the call's value), as do revisits, decode
failures, and running past the cap. Fire shapes unchanged (SS arith +
`movss` from XMM0); VEX/`movaps`-copy/double-width consumes decline.

Evidence: PlayerManager `FixedUpdate` (26741, `call; test; je; ...;
mulss xmm0`) renders `float real15 =
sub_1804cdb00(PlayerPrefs.GetFloat("SFXVolume"));` into `SetFloat(
"DeathAudio", real15 * 20.0f)` at both sites; StoreManager `Spawned`
(27765) and three more KeybindsManager volume restores gain the same
improvement class. Slider `SliderLerpUnclamped` (15267) correctly
declines twice (double-width `cvtss2sd` consume; `movaps`-copy consume).
Corpus-isolated diff vs stashed baseline: exactly 3 files, all
improvements plus renumber cascades. Tests: +4 portable (walk fire +
rejoin/clobber/call/cap declines) +2 game; focused 15 passed; full
suite 951 passed / 0 failed. Strict scratch builds (490/6,622 +
802/8,997, all zero), brace 0, parse 0/0/0. No goldens changed.

## Current work: unregistered FP32-unary leaves (2026-09-24, LANDED)

`sub_1804cdb00(volume)` (CRT log10f, 0x1804cdb00) is proved, never
named: a MUST-fixpoint input proof over the callee (`_is_fp32_unary_leaf`
in `il2cpp/lifter/state.py`, next to the sqrt/fence recognizers) shows
exactly XMM0 read, no GPR/stack arguments, and no caller-visible
effects (pdata extent, recursive-descent CFG, operand-access allowlist,
RSP-frame/alias bounds, must-be-written fixpoint; depth-1 input
propagation; unregistered-identity floor below with the CRT-substrate
residual documented). The call site additionally requires a scalar
XMM0 consume on the next instruction (`_fp32_scalar_next`) and a known
XMM0 value. The render keeps the honest `sub_X` name with one float
argument and a float XMM0 result; fix-104's `(float)` cast stays (it
unboxes against the object-returning stub declarations -- skipping it
broke compilation while staying parse-green, so the skip was designed,
prototyped, and reverted before landing; casts are load-bearing).

Evidence: 23548/23549 render `float real2 =
(float)sub_1804cdb00(volume);`
with `real3 = real2 * 20.0f;` (was 4-arg spray + `object` + dropped
`0f * 20.0f`), dead arg scaffolding DCE'd; KeybindsManager's three
volume methods (SetSFX/Music/PlayerVoiceVolume) gain the identical
improvement. Corpus sweep: exactly 1 of 2,676 unregistered targets
passes (21 sites); PlayerManager/StoreManager/Slider/stub sites decline
(principled: no immediate scalar consume -- conditional use after flag
tests needs branch-aware tracking, a follow-up). Strict scratch builds
(Assembly-CSharp 490/6,622 + UIElementsModule 802/8,997, all 0 failed /
0 fallbacks), brace 0, parse 0/0/0 on both. Against a stashed baseline
build, exactly 2 files differ (both improvements). Tests: +7 portable
(synthetic callee bytes, decline shapes, consumer gate) +2
game; focused 11 passed; full suite 947 passed / 0 failed (fully
green). No goldens changed; `final_out/` holds r4d. Package CRLF/no-BOM,
tests LF.

## Current work: scalar parameter-copy inference (2026-09-23, LANDED)

A single prologue copy of a scalar metadata parameter now carries its
exact declared type (`il2cpp/dec/highlevel.py`, in the hint seeding
ahead of `_rename_locals`). This recovers stack homes like
`s_10 = volume` (float) as `float real1 = volume` without inferring
from an unrelated later use. A second write or an address /
`ref` / `out` / `in` escape declines; existing concrete hints win.

Evidence: both AudioVolumeSliders methods (23548/23549) render
`float real1 = volume` with `real1.ToString("0.0")` while keeping the
paired-Jcc and branch-chain recoveries; the StreamBuffer 8-arg
overload (113044) stays fully bound with renumbered int temps (its
game assertion now pins the parameter at the store, which is the
regression invariant). Tests: +1 portable (single-write fire,
rewrite/address-escape declines) plus evolved game pins; focused 30
passed. Full suite: 938 passed / 0 failed (fully green, +1 vs r4d).
Strict `Assembly-CSharp` scratch build: 490 files / 6,622 bodies, 0
failed, 0 fallbacks, 0 type emission failures; brace 0/490; parse 0
bad / 0 ERROR / 0 MISSING. Scratch-tree AudioVolumeSliders verified
(`float real1 = volume`, no `unknown != unknown`). No goldens
changed; `final_out/` + `validation_reports/` hold r4d until an
explicit promotion call. Package source kept CRLF/no-BOM, tests LF.

Open lead (unchanged): AudioVolumeSliders still calls unregistered
`sub_1804cdb00` (native XMM0 scalar result, identity and arity
unproved; current lift renders `real2 = 0f * 20.0f`). Prove
call/result provenance before replacing the raw call; do not guess
from `Mathf.Log10` (its registered target differs).

## Current work: promotion r4d (2026-09-23, PROMOTED)

User-authorized (`promote final out`). Strict rebuild `r4d_out1` from
clean HEAD `1920c71` (the uncommitted scalar parameter-copy slice was
stashed pre-build and is NOT in this tree): 11,183 files / 114,458
bodies / 0 failed / 0 fallbacks / 0 type-emission failures; brace 0
unbalanced; parse 0/0/0; file set identical to r4c (11,276 paths, 783
files differ). Triage: branch-chain + recursive phi decl hoists across
the corpus; paired-Jcc float-condition recovery (`unknown != unknown`
to real lane comparisons, e.g. float3x3) unblocking existing ternary
folds (net −2,479 unknown, −52 unknown-files); one native-faithful
dead-diamond resurrection class (mi 104158 `get_remainingDistance`,
bisected to 2481c16, verified against disassembly — native computes
pos.z then clobbers it); renumber cascades; shared +5, indirect/memN/
goto/`?addr` flat, no regressions. Promoted by mirror copy
(aggregate `b0f798b4…2280`); evidence in
`validation_reports/promotion_r4d.json`. Post-build suite: 937 passed
/ 0 failed (fully green). Scratch tree + worktrees removed; tree
committed and pushed. WIP scalar-copy slice restored to the working
tree after promotion (still unlanded, see `docs/handoff-2026-09-23.md`).

## Historical handoff: 2026-09-23 stop (LANDED)

The fourth scalar parameter-copy change described here is now landed
(see the top section): focused 30 passed, full suite 938 passed / 0
failed, strict `Assembly-CSharp` scratch build plus brace/parse gates
passed, committed and pushed. The `TODONOW.md` working-tree addenda
were preserved as committed. No goldens were changed; `final_out/` +
`validation_reports/` hold the r4d promotion above. The `sub_1804cdb00`
provenance lead from [handoff-2026-09-23.md](handoff-2026-09-23.md) is
now closed by the top section (FP32-unary leaves, LANDED).

## Current work: complete branch-chain declarations (2026-09-23, fixed in source)

`AudioVolumeSliders.SetMusicVolumeInternal` and
`SetSFXVolumeInternal` (23548/23549) assigned `float real1` in all
three `if / else if / else` arms, then read it at `SetFloat` after
the join. A late `_phi_chain_decl_hoist` now places one concrete typed
declaration before a complete chain and leaves each arm's assignment
in place. It requires matching tail declarations, a final `else`, no
flow exits or earlier use, no address escape, and a later read.
Unknown `object`/`dynamic` value markers decline: an initial wider
pass changed frozen MethodDef 39789's unresolved 0/1 aliases, so that
case remains golden-exact until its type is proved.

Portable tests pin the three-arm fold and missing-else, early-return,
and unresolved-type declines; game tests pin both audio bodies.
Full suite: 937 passed. Strict `Assembly-CSharp` scratch build: 490
files / 6,622 bodies, 0 failed, 0 fallbacks, 0 type emission failures;
brace 0/490; parse 0 bad / 0 ERROR / 0 MISSING. Against the prior
scratch build, 44 files differ; sampled changes hoist branch-complete
declarations in AudioVolumeSliders, InventoryManager, FPSController,
and FIMSpace. `final_out/` and goldens remain untouched.

## Current work: paired float Jcc flags (2026-09-23, fixed in source)

MethodDefs 23548/23549 (`AudioVolumeSliders.SetMusicVolumeInternal` /
`SetSFXVolumeInternal`) use native `ucomiss xmm1, 0; jp X; jne X`.
The `JP` correctly rendered `float.IsNaN(volume)`, then cleared the
comparison operands before the fallthrough `JNE`, producing
`else if (unknown != unknown)`. For the exact `UCOMISS; JP X; JNE X`
shape with one predecessor at the second jump, the CFG executor now
carries the operands and setter across the first jump. The second
condition renders `volume != 0f` in both methods. Unregistered
`sub_1804cdb00` result typing remains open. The later `real1`
declaration is now hoisted by the follow-up above; these bodies still
contain other unresolved values and are not claimed to compile.

The broader Jcc carry changed MethodDef 45016's frozen double body,
so it was narrowed to this proved single-precision shape; 45016 is
golden-exact again. Two game tests pin the audio conditions. Full suite:
936 passed. Strict AudioVolumeSliders scratch build: 8 bodies, 0 failed,
0 fallbacks, 0 type emission failures; brace 0/2; parse 0/0/0.
`final_out/` and goldens were not regenerated or promoted.

## Current work: InventoryManager join loss (2026-09-23, fixed in source)

`UpdateInventorySlotsUI` (MethodDef 25624, VA `0x18070b620`) has an
unbound `image3.sprite = obj21` in the promoted and fresh lifts. Native
block `0x18070baf4` calls the sprite setter after two paths: predecessor
68 (`0x18070ba96`) carries `RCX = t1014` and
`RDX = this.objSprites[this.inventoryIds[v145]]`; predecessor 75
(`0x18070baed`) carries `RCX = this.inventorySprites_[v145]` and
`RDX = this.emptySprite`. The setter therefore runs on both paths.
`_build_phi_copies` creates a phi for `RDX` (`v223`) but none for
`RCX`; the structured body already has `t1014.sprite = v223` before
`_rename_locals`. The latter merely names the unbound value `image3`.

Real-pass instrumentation proved both `RCX` expressions had identical
text at the equality check, but separate definition sites and one use
each. Later binding renamed only the first expression. The merge now
keeps a typed object array-element value with distinct definitions as
a phi, even when its texts match. `_phi_decl_hoist` then lifts the
receiver and sprite declarations above the diamond, preserving each
arm's assignment. The historical twin-tail match remains first; the
non-tail extension runs only after a prior hoist on that shape.

Evidence: MethodDef 25624 now renders `Image obj22; Sprite obj23;`
before the branch, assigns both in each arm, and calls
`obj22.sprite = obj23;` at the join. A game regression and a portable
two-value hoist test pin it. Full suite: 934 passed. Strict scratch
build (`--types InventoryManager --only Assembly-CSharp`): 158 bodies,
0 failures, 0 fallbacks, 0 type emission failures; brace audit 0/2.
Strict `Assembly-CSharp` scratch build: 490 files / 6,622 bodies,
0 failures, 0 fallbacks, 0 type emission failures; brace audit 0/490;
tree-sitter parse 0 bad / 0 ERROR / 0 MISSING. Against promoted r4c,
27 Assembly-CSharp files differ; sampled diffs are phi copies and
declaration hoists, with the target's two receiver assignments intact.
`final_out/` remains the read-only promoted r4c tree. No snapshot
regeneration or promotion was done.

## Current work: promotion r4c (2026-09-23, PROMOTED)

User-authorized (`just promote`). Strict rebuild `r4c_out1`: 11,183
files / 114,458 bodies / 0 failed / 0 fallbacks / 0 type-emission
failures; brace 0 unbalanced; parse 0/0/0; file set identical to r4a
(11,276 paths, 49 files differ). 49-file triage: SIMD composites
(+13), struct-literal recoveries (GridGraph/AstarDebugger/WFX Color,
native-verified), float typings, renumber cascades, honest residuals
(net −86 unknown); no regressions (WFX alpha ternary verified
native-faithful; `?addr` tightening stayed reverted). Promoted by
byte-identical copy (aggregate `c0ee1b78…1236`); evidence in
`validation_reports/promotion_r4c.json`. New census: shared
18,884/2,278, indirect 6,262/884, unknown 15,655/1,365, mem[N]
398/127, mem_hex 359 strict, goto unchanged, `?addr` 1 (honest
elision). Post-promotion suite: 932 passed / 0 failed (fully green).
Scratch tree + build logs removed; tree committed and pushed.

## Current work: ?addr-tightening DISPROVED (2026-09-22, reverted clean)

Narrowing the RSP-copy declines to text-`?` bases rescued mi 65244's
last `?addr` as `((byte*)obj44 + num55*4)[0] = 4294967295` -- then
traced end to end and disproved it: obj44 textually aliases a reused
home (0f/data_ on disjoint arms) while native uses a fresh
&s_1d0+idx address; the address-of is lost in write-barrier
conversion and the width/value mismatches, so the line miscompiles
where the elision honestly declined. Reverted byte-identically (lifts
match pre-tightening bodies); the elision itself is now pinned by a
game test against recurrence. Portable anonymous-copy guard kept.
- Gates: full suite 932 passed / 0 failed (first fully-green run
  stands).
- Lesson recorded: rescues must prove the rendered base denotes the
  native address on the reaching path, not just spell it.

## Current work: SIMD consumer-side round (2026-09-22, unpromoted)

Subagent-traced (both constants' death sites + 80548 guard shape).
Same rules: `final_out/` untouched, no promotion (tree rebuild is a
separate user call). `il2cpp/` edits via binary patches with
CRLF/no-BOM asserts; `tests/` edits LF.

- Fix LANDED, tails-only staging: (A) scalar const-pool loads attach
  bytes (mirrors PACKED128; only adds float-expected lane reads);
  (B) `_tail_method_args` materializes GPR `?` args at closed
  all-float vector slots from byte-proven float-suffixed lanes --
  width-4 renders the literal, width-8 renders house `(float2)(l0,l1)`
  for Unity.Mathematics.float2 only. Instance/sret/stack/byref/
  double/open/unresolved/uncovered/part-less/text-mismatched all
  decline; direct calls keep today's spelling.
- Evidence: 67525 renders `clamp(x, (float2)(0.0f, 0.0f),
  (float2)(1.0f, 1.0f))` (signature-exact float2x3, mi 67517; parses;
  the old scalars relied on implicit conversion no overload proves).
  80548 guard holds (`int num2`, `(unknown >> 32)`, golden-pinned).
- Golden REGENED for 67525 only (surgical script, fixture SHAs verified,
  source_sha256 refreshed, CRLF kept, 63 other bodies identical).
  Suite is 930/0 -- first fully green run.
- Follow-up (direct calls, same gates): the tail loop refactored into
  shared `_materialize_float_lanes`, wired into the resolved-direct
  path after positional rebuild + trim. mi 67836 smoothstep renders
  `clamp(unknown, (float2)(0.0f, 0f), (float2)(1.0f, 1.0f))` (+`.x`/`.y`
  reads); uncovered first arg honestly stays unknown; mixed `0.0f`/`0f`
  lane spellings kept verbatim (values exact, no normalization pass).
- Tests: +3 game (`test_game_simd_lanes.py`: tail composite,
  direct composites, 80548 integer-carry guard).
- Gates: full suite 933 passed / 0 failed.
- Open SIMD remainder: per-arm Color (use→def), general packed
  tracking (still declined).

## Current work: sidecar grounding turn (2026-09-22, unpromoted, no source change)

Traced mi 23762's three defects to their exact producers (semantic-input
dump + `_field_expr` generic-base trace + addr_of audit) to scope the
sidecar honestly:

- `selectable1 = dictionary22`: the key type comes from USE-side proof
  (`_hint_accessor_recv` on the `.navigation` store), never from a
  proved-struct store -- so a store-side lane writer would never fire
  here. Needs byte-range slots (documented sidecar), not a writer.
- Zero closed-genericinst bases reach `_field_expr` in the method, so
  the inflated-chain swap is a proven no-op here too.
- `obj17` (Navigation lane): XMM-lane traffic through spills, needs
  SIMD-lane provenance, not field chains.
- `obj11 = &dictionary23` + `obj11.Dispose()`: the receiver is a bare
  temp at lift; `addr_of` tracks memory homes only. Needs use→def.
- Verdict: all three need deferred machinery (sidecar/SIMD/use→def);
  no narrow slice exists. No invisible infra shipped.

## Current work: ?addr extinction round (2026-09-22, unpromoted)

Follows the promoted census (last `?addr`: ReflectionProbeManager).
Same rules: `final_out/` untouched, no snapshot regen, no promotion.
`il2cpp/` edits via binary patches with CRLF/no-BOM asserts; `tests/`
edits LF.

- Root cause was our own quarantine over-firing: the indexed-copy
  declines caught NAMED `&s_xx` homes (mi 65244 `lea rcx,[rcx+r12*4]`
  over `&s_1d0`), not just anonymous `mov r64,rsp` copies. Tightened
  all 5 decline sites (MOV-RBP, LEA-RBP-dst, LEA/load/store indexed)
  to text-`?` bases; named homes keep legacy honest composites.
- Verified the rescued store is correct, not just present: it uses the
  home's address (`&s_1d0` slot identity), so stale home values on
  disjoint arms don't alias it.
- `?addr` count is now 0 in fresh lifts (was 1); the promoted tree
  still shows its 1 until the next rebuild.
- Tests: +2 portable (named home keeps home, anonymous stays unknown)
  +1 game (65244: no ?addr/elided, exact store line).
- Gates: compileall pass; portable 782 green; full suite 926 passed /
  1 failed (67525 honest SIMD decline only); zero golden movement.

## Current work: generic-slice closure (2026-09-22, unpromoted, no source change)

Subagent-designed, empirically closed without a patch. Same rules:
`final_out/` untouched, no regen, no promotion.

- Verified on mi 23762: MethodRef kind-6 slot path already closes all
  generic homes; closed-generic bases never reach `_field_expr`
  (0 hits traced), so the inflated-chain swap is a proven no-op here;
  `selectable1` needs byte-range sidecar (documented), `obj17` needs
  SIMD lanes, `obj11` needs use→def (bare-temp receiver at lift).
- Corpus mining for hook-shaped sites (open result + correctly
  attributed closed-generic receiver + pure-result-typing fix): ZERO
  hits. 9 open-result sites need downstream-consumer proof (use→def);
  the 1 closed-receiver + object case (24679) is a misattributed field
  lane with zero `get_Current` candidates; 109849 likewise; the 187
  family is void/closed/slot-named already.
- Verdict: receiver-driven substitution deferred to sidecar machinery
  alongside hinted receivers. No invisible infra shipped.

## Current work: promotion r4a (2026-09-22, PROMOTED)

User-authorized. Strict rebuild `r4a_out1`: 11,183 files / 114,458
bodies / 0 failed / 0 fallbacks / 0 type-emission failures; brace
audit 0 unbalanced; parse gate 0/0/0; file set identical to the prior
tree (11,276 paths). Spot-verified in-tree (GetEnumerator/MoveNext/
Current, IsSameObject(obj1, obj2), StreamBuffer v0). Promoted by
byte-identical copy (aggregate `e7f406db…bdabf`); evidence in
`validation_reports/promotion_r4a.json`. New census: shared
18,884/2,278, indirect 6,262/884, unknown 15,748/1,365, mem[N]
398/127 (was ~13k — the RSP-copy round at corpus scale), mem_hex 359
strict, goto unchanged, `?addr` down to its last site
(ReflectionProbeManager:434, funclet home). The memhex remainder is
honest (be-None path byte-identical in diff; sampled sites are
exception/funclet homes). Post-promotion suite: 923 passed / 1 failed
(67525 honest SIMD decline only). Scratch tree + build logs removed;
tree committed and pushed.

## Current work: promotion round — regen + rebuild (2026-09-22)

User-authorized regen/promotion. `tests/goldens_review84.json`
surgically regened for mi 32837 (70→66 lines, dead spills out) and mi
104428 (38→26, spills out, aggregates back) only -- 67525 keeps its
ground-truth `clamp(x, 0f, 1.0f)` expectation (honest SIMD decline,
never enshrine `unknown`). `source_sha256` refreshed to the current
tree; the other 62 bodies byte-identical. Expected suite after regen:
all green except 67525.

## Current work: boxed-bool fold round (2026-09-22, unpromoted)

Subagent-designed from the interface round's residual. Same rules:
`final_out/` untouched, no snapshot regen, no promotion. `il2cpp/`
edits via binary patches with CRLF/no-BOM asserts; `tests/` edits LF.

- Fix LANDED: `object X = <bool dispatch>; if (X == null)` folded to
  `bool X = ...; if (!X)` (and `!=` to bare). The bool proof exists
  only after render-stage dispatch naming (at lift time the callee is
  unknown, so the null test is honest): `_name_interface_dispatch`
  records bool-returning resolutions, new `_boxed_bool_null_fold` runs
  last after semantic names. Single exact `object X = <call>` decl,
  all-uses-must-be-bool via `_bool_use_ok`, no reassign/address-take,
  standalone heads only; no inlining (MoveNext is impure), no renames.
- Evidence: 8 methods fold (25368, 24059, 25132, 25872, 26880, 27213,
  97399, 105906; native `test al,al` verified on two); unbox/`&` uses
  (25872 obj52, 97399 obj49) correctly decline, as do ref-null tests
  and already-bool `!(objN)` uses.
- Tests: +5 portable (fire, ne-shape, object-use/reassign/byref
  declines, unrecorded/non-call declines) +1 game (25368 fold, 25872
  fold + unbox decline).
- Gates: compileall pass; portable 778 green (773 + 5); full suite 921
  passed / 3 failed -- identical IDs (32837 improvement-pin, 67525
  honest SIMD, 104428 stale); the fold moved zero goldens.

## Current work: interface-dispatch round (2026-09-22, unpromoted)

TODONOW #2 first slice, subagent-mined. Same rules: `final_out/`
untouched, no snapshot regen, no promotion. `il2cpp/` edits via binary
patches with CRLF/no-BOM asserts; `tests/` edits LF.

- Fix LANDED (mi 25368 `GameManager.CheckAllReady`): three back-to-back
  interfaceOffsets searches resolved to `GetEnumerator`/`MoveNext`/
  `Current`, missing on three crisp gates: (1) slot lines carry decl
  prefixes at render stage (`object obj19 = ...`) -- `_ITF_SLOT_RX`
  admits an optional type prefix; (2) the typeof token is referenced at
  the call, outside the old (typeof, slot] span -- search runs through
  the call line (monotonic widening); (3) display spells arity `_N`
  while metadata names use `` `N `` -- exact key first (genuine `Foo_2`
  rows keep resolving), normalized fallback for generic displays only.
  All existing declines preserved (unrelated typeof, unresolvable key,
  out-of-range rel, unshaped receiver, non-16 K, missing slot).
- Residual note: `object obj32 = obj5.MoveNext(); if (obj32 == null)`
  boxes the bool (same shape as the old unknown call -- not a
  regression); a bool-fold of null-tested proved bools is its own
  future proof, not this round.
- Tests: +3 portable (arity-key normalize/range, genuine-underscore
  exactness, slot-prefix/bare shapes) +1 game
  (`test_game_interface_dispatch.py`: all three lines, zero
  `/*indirect*/` left in the method).
- Gates: compileall pass; portable 773 green (770 + 3); full suite 915
  passed / 3 failed -- identical IDs (32837 improvement-pin, 67525
  honest SIMD, 104428 stale); the slice moved zero goldens.
- Next #2 slices: vtable-slot occupants on abstract bases (needs
  store-provenance sidecar -- disproved-adjacent, do not touch without
  it), fnptr cells (fix-66 covers icalls; zero `fnptr_` hits tree-wide).

## Current work: param-exclusion rename round (2026-09-22, unpromoted)

Follows the unbound census (vN residuals were renamed *parameters*).
Same rules: `final_out/` untouched, no snapshot regen, no promotion.
`il2cpp/` edits via binary patches with CRLF/no-BOM asserts; `tests/`
edits LF.

- Fix LANDED: `_rename_locals` renamed body tokens matching metadata
  parameter names (StreamBuffer.WriteBytes v0/v1 became obj5/obj6 while
  the emitter kept v0/v1 -- every use disconnected, spine unbound).
  Params already declare their names; rename targets now exclude every
  metadata parameter spelling (a lifter temp sharing one keeps its
  honest lift-stage name instead of a silent capture).
- Evidence: mi 113041-113044 (2/3/4/8-arg overloads) render
  `this.buf[numN] = vK;` throughout, fully bound.
- Tests: +1 portable (param spellings kept, temp still renames) +4 game
  (`test_game_param_names.py`, all overloads, no obj5/obj6).
- Gates: compileall pass; portable 770 green (769 + 1); full suite 911
  passed / 3 failed -- identical IDs (32837 improvement-pin, 67525
  honest SIMD, 104428 stale); the exclusion moved zero goldens.
- Census remainder now: tN temps, SIMD type-position FPs, vN true-temp
  collisions (if any survive the exclusion -- re-run census at
  promotion time).
- Follow-up (same fix, no source change): every other census residual
  checks out as a metadata parameter -- HashCode.Initialize
  (ref uint v1-v4), MeshVoxelizer.GetTriangleBounds, JValue.ValuesEquals
  and the rest all render bound in fresh lifts; the 5 SIMD hits are
  type-position FPs of the checker. TODONOW §5's actionable set is
  ~zero in fresh lifts: +2 game pins (1935, 79519).

## Current work: rename-barrier + unbound-census round (2026-09-22, unpromoted)

TODONOW §5 work order (classify before patching) plus one real fix it
surfaced. Same rules: `final_out/` untouched, no snapshot regen, no
promotion. `il2cpp/` edits via binary patches with CRLF/no-BOM asserts;
`tests/` edits LF (one pre-existing CRLF game file kept as-is).

- Census LANDED (temp `unbound_census2.py`, read-only over `final_out/`,
  11,183 files): comment/string scrub, method-region split, textual
  dominance (earlier line, depth <= use). Result: **55 distinct unbound
  tokens in 21 files** (naive upper bound was ~8,700/~2,200) --
  scope/multi-decl/DCE-residue/comment noise was 99%+. Remainder: vN
  residuals (StreamBuffer v0-v7 et al.), tN oversize/bind temps
  (DateTime/TimeSpan/JToken...), SIMD type-position FPs (v128/v64/v256
  in Burst files), and exactly one obj-family case below.
- Fix LANDED (the obj-family case, mi 124140
  `AndroidJNI.IsSameObject`): native forwards `(obj1, obj2)` correctly
  (rcx via rdi, rdx via rbx), but output printed `(obj2, obj2)`.
  Traced end to end: `_seq` emits `(obj1, obj2)`; `_rename_locals`
  minted `s_8`/`v4` as `obj1`/`obj2`, shadowing the params, declared
  `object obj1 = obj2;`, and `_copy_prop` merged the dropped argument.
  Fix mirrors `_semantic_local_names`' barrier: reserve every
  obj/num/flag/real token in the lines plus every metadata parameter
  name, bumping until free (`_rename_locals(lines, m)`; single caller).
- Tests: +2 portable (body-identifier skip, unused-param skip via
  metadata) +1 game (`test_game_rename_barrier.py`: exact return line,
  no shadow decl).
- Gates: compileall pass; portable 769 green (767 + 2); full suite 904
  passed / 3 failed -- identical IDs (32837 improvement-pin, 67525
  honest SIMD, 104428 stale); the barrier moved zero goldens.
- Open from the census: vN/tN residual producers in the 21 files
  (StreamBuffer first), still unclassified by native cause.

## Current work: array-receiver shared-call round (2026-09-22, unpromoted)

TODONOW #1 first slice, subagent-mined. Same rules: `final_out/`
untouched, no snapshot regen, no promotion. `il2cpp/` edits via binary
patches with CRLF/no-BOM asserts; `tests/` edits LF.

- Fix LANDED: `_td_of` maps no array type, so array-typed receivers
  never reached the chain filter. New `Il2Cpp._system_array_td`
  (mirrors `_system_object_td`, per-instance cache) +
  `Lifter._array_receiver_td` (SZARRAY/ARRAY only, byref declines) +
  2-line fallback at all three chain-filter twins (`_call`, tail jmp,
  analyze jmp). Arrays have no subclasses and Array owns Clone, so the
  Array typedef roots the chain; sret-clear, ctor, generic, and
  `len(hits)==1` gates run unchanged.
- Evidence: mi 275/326 (`this.m_aValue`/`this.state`, byte[] homes) and
  mi 4047 (`this.delegates`, Delegate[]) resolve the 9-candidate Clone
  fold to `...Clone()` instance rendering (4047 even takes a typed
  `Delegate[]` decl); mi 144 string twins (Equals/op_Equality, one
  typedef) keep all 5 markers.
- Tests: +2 portable (array mapping, non-array/byref/missing/ambiguous
  declines) +4 game (`test_game_shared_twins.py`: 3 resolutions, 1
  must-decline count pin).
- Gates: compileall pass; portable 767 green; full suite 901 passed /
  3 failed -- identical IDs to the RSP-copy round (32837
  improvement-pin, 67525 honest SIMD decline, 104428 stale golden);
  none of 275/326/4047/144 is in the golden set.
- Next #1 slices: slot/hint-typed receivers (side-table corroboration),
  then receiver-driven generic substitution (needs synthetic table).
- DISPROVED with evidence (hinted receivers reverted, no residue):
  `&raycastHit1`→`distance` and `&taskAwaiter1`→`GetResult`/`IsCompleted`
  resolved cleanly, but resolving IsCompleted removed the
  ambiguous-shape union-kill that used to clear s_50's tile; the
  surviving tile was field-split by `_scalar_parts` (TaskAwaiter-typed
  RAX) and the whole-struct reload projected `.m_task` into the
  TaskAwaiter home (`<>u__1 = task1.GetAwaiter().m_task`, ill-typed,
  gate-invisible). Until whole-struct reloads prefer whole tiles
  (byte-range sidecar round), hint-driven resolution stays out -- same
  SHUFPS/80548 precedent. Repro analysis preserved in Temp
  (`probe_*`/`trace_*`/`diag_*` scripts); 25687/24238 revert lifts are
  byte-identical to pre-hint baselines.

## Current work: RSP-copy home round (2026-09-22, unpromoted)

Subagent-proposed, human-implemented. Same rules: `final_out/`
untouched, no snapshot regen, no promotion. `il2cpp/` edits via binary
patches with CRLF/no-BOM asserts; `tests/` edits LF.

- Fix LANDED (mi 117615 NetBitBuffer.WriteInt32AtOffset): `mov r64,rsp`
  now carries the frame offset (`_stack_offset`, `?`-text) instead of
  None, so [copy+N] keys slots by absolute address and aliases [rsp+M]
  of the same home (`_read_mem`/`_mem_lvalue`/LEA copy branches; RSP-path
  keys identical, `_aggregate_load` untouched after the quarantine below).
  Body went from `mem[8] = this;`/`mem_8`/raw twins to `this._offsetBits
  = offset;`/`this.WriteSlow(value, bits);`. Arithmetic/index/32-bit
  uses decline to unknown-base shapes; `mov rbp,rsp` keeps the pinned
  frame idiom (follow-up: RBP never takes a copy offset, one portable
  regression caught and fixed).
- Must-decline PINNED (mi 23900 ActorSpawner.Update): same-typedef
  Transform twins (get_parent triple, set_parent pair) keep their
  markers -- no receiver proof can split one declaring typedef.
- Quarantine (stash-proven): first cut tracked `lea rbp,[rsp-C]`-style
  frame offsets absolutely and split RBP-disp-keyed homes (80548
  `int num2` -> `object obj1` + unbound `num2`). RBP stays on legacy
  frame paths byte-identically (MOV/LEA/load/store/indexed all skip
  RBP; `_aggregate_load` reverted untouched). 80548 back to golden.
- Triage, all same improvement class (prologue spills through
  `mov r64,rsp` copies resolve to slots; dead ones drop; RBP untouched):
  32837 golden holds 4 raw `mem[]` stores, actual drops them
  (renumber-only fallout, native `mov rax,rsp` + 3 spills proven) --
  NEW red, consigned to regen; 108722 both native address-triples now
  print (`&obj6,&obj5` / `&obj5,&obj6`, old site-1
  `(default,default,default)` was copy blindness) -- review83 pin
  evolved to the faithful spelling with native cites; 104428 diff grew
  by the same mem-removal (its golden holds `mem[8]` too) -- same
  already-red ID, still awaiting the gated-regen user call.
- Tests: +4 portable (`test_recovery_completion.py`: slot roundtrip +
  cross-delta alias, arithmetic/index/32-bit+RBP declines) +3 game
  (`test_game_frame_copy.py`: 117615 improvement, 23900 markers, both
  `?addr` extinctions).
- `?addr` EXTINCT in fresh lifts: the promoted tree's only two hits
  (104380 `LineCircleIntersectionFactor`, 82799 `RestBendingConstraint`,
  both `store into untracked ?addr` in copy-heavy methods) render no
  `?addr` and no `mem[]` (dead-spill removal, renumber-only fallout;
  82799's 1-line `return real2` residue is pre-existing in its old body
  too). Pinned by the third game test above.
- Residual (honest, not regressed): 117615's replayed finally tail
  keeps one undeclared `obj6` phantom (was three undeclared
  mem[8]/mem_8/obj2); 67525 (SIMD UNPCK) unchanged.
- Gates: compileall pass; portable 765 green; full suite 895 passed /
  3 failed -- 67525 (honest SIMD decline) + 104428 (stale golden) were
  already red; 32837 is new but proved improvement (its golden holds
  the same 4 raw `mem[]` spills the fix removes; renumber-only
  fallout). 80548 quarantine-restored; review83 evolved green; `?addr`
  extinction pinned (3/3 game).

## Current work: TODONOW guardrail round (2026-09-22, unpromoted)

Subagent-assisted analysis of TODONOW.md 1-5 (4 analyses: census,
shared+indirect design, unknown+raw design, unbound-temp analysis).
Same rules: `final_out/` untouched, no snapshot regen, no promotion.
No `il2cpp/` source change (broad receiver/provenance fixes need
use→def machinery + synthetic nested-type sidecar; see deferrals).

- Inventory (read-only, python regex over `final_out/**/*.cs`,
  11183 files): shared 19013/2304, indirect 7091/975, unknown
  16045/1382, mem[N] 13189/805, mem_hex 343/69, goto 8707/903.
  Matches the TODONOW handoff figures up to scanner-definition deltas
  (case/`\b` token vs diagnostic hits, broad vs load-twin memhex);
  confirms the census note, not silently ignored files.
- Guardrails LANDED (`tests/test_recovery_completion.py` +4, LF):
  ambiguous shared keeps `/*shared body, N candidates*/`; consensus
  never resolves identity; untracked-base load/store stays raw
  (`mem_xx`/`mem[N]`); `unknown` never becomes zero/`default`.
- Targeted lifts: 67525 (`clamp(x, unknown, unknown)` -- honest SIMD
  UNPCK decline, const-pool+XMM lanes need stronger proof after 80548)
  and 104428 (modern static-field spelling + recovered aggregates;
  golden stale by design) unchanged by construction (test-only diff).
- Gates: compileall pass; portable 761 green (757 + 4 new); full
  suite 889 passed / 2 failed -- failure SET byte-identical to the
  triaged baseline (67525 honest SIMD decline, 104428 stale golden).
- DEFERRED with designs (not regressed, still open): broad
  shared-body receiver resolution + indirect/interface dispatch
  (proof-driven `_shared_receiver_target` + receiver-driven generic
  substitution designs ready; needs closed-receiver + synthetic table
  + field sidecar), unknown/raw provenance (tile/copy `_parts`
  threading, SIMD spill/lane gating, call-result consensus typing,
  base recovery -- all decline-by-default), unbound-temp re-census
  only after upstream (count is upper-bound with scope/multi-decl/
  DCE-residue/commentnoise false positives), per-arm Color (use→def
  const rewrite; 1445-site churn for 8 cosmetic sites), Navigation
  merge-side facts, 35 golden/review regens + promotion (user call).

## Current work: recovery follow-up round 3e (2026-09-20, unpromoted)

Continued TODONOW.md's blockers 1-3 plus cosmetic items 4-5. Same rules:
`final_out/` untouched, no snapshot regen, no promotion. All `il2cpp/`
edits via binary patches with CRLF/no-BOM asserts; `tests/` edits LF.
`tests/test_recovery_completion.py` grows 5 -> 17 synthetic tests;
`tests/test_game_synth_types.py` pins 4 synthetic-type behaviors.
Accessor-receiver hint (`_hint_accessor_recv` at the `set_` fold):
a resolved instance accessor proves its receiver through the
non-generic declaring typedef (slots/bare `t`-temps; byref-`this`
homes for valuetypes; dotted/`this`/generic/static/foreign kinds
decline). 23762's key is now `Selectable selectable1` with a
guarded typed assignment. 2 unit tests.
Copy-prop type guard: registering `dst = src` declines when both
sides declare different concrete non-object types (a struct home
copied over a typed temp is not value-preserving). Keeps 23762's key
and assignment from merging into the enumerator name; same-type and
object copies fold as before. 2 unit tests. Residual: `Selectable
selectable1 = dictionary22;` over-claims a 16-byte lane copy as a
full-struct copy (pre-existing whole-slot convention); single naming
forces one error site either way -- documented, awaits byte-range
slot versioning (the sidecar).
S6 layout steps (subagent-verified byte-exact vs native): nested-open
fields close through enclosing args in `_sf_infl_chain` (`_current`
carries closed KVP); `returns_sret` admits closed 0x15 with proved
size outside {1,2,4,8} (72-byte Enumerator folds the hidden buffer;
unproven shapes keep the fix-54 stand-down).
Candidate-tree gate for the five affected types (ConsoleUINavigation,
GlobalUINavigation, CollisionEventHandler, AnimationEventTrigger,
MicAudioCanvas, `--types` one build each into Temp): strict build 54
bodies / 0 failed / 0 fallbacks; tree-sitter parse 0/0/0; Roslyn probe
83 errors, all CS0246 missing-assembly scope noise, none on any
recovered identifier; before/after diff strictly improving (no more
elided static stores, unsafe raw blocks, or object soup where typed).
Full-tree compile remains a promotion-time gate.

- Blocker 2 LANDED (24655 OnEnable): the `t1012__1_0` store was NOT a
  `_mem_lvalue` bug (probe: `_field_expr` renders the correct
  `ConsoleUINavigation.<>c.<>9__1_0` every time). Root cause is
  `_bind`'s blind `str.replace`: binding `...<>c.<>9` rewrote the
  longer field name mid-identifier. New `_bind_replace` (`expr.py`,
  used at all 10 `_bind` sites in `lifter/state.py`) rewrites
  whole-token occurrences only (member access on the value still
  folds). Store now reads `ConsoleUINavigation.<>c.<>9__1_0 =
  predicate13;`. 3 unit tests.
- Blocker 3 LANDED (23761 DisableAllActiveSelectables): three parts.
  (1) `_hint_arg_types` `&slot` branch now types by-VALUE struct homes
  from the substituted closed parameter type (`&s_20` + TValue ->
  Navigation at `Dictionary.Add`; TRUST-gated like the `ref`
  rewrite, closed-key proof, setdefault). (2) Stack-slot stores of
  whole-field struct values record the type (`_struct_home_ty`:
  exact closed valuetype, no slices/parts/addresses). (3) A scalar
  constant at a struct-typed home's base renders field-precisely
  (`_home_field_store`: exact-width offset-0 field proof +
  `_fimm`-compiles gate, else today's scalar). Result: `Navigation
  navigation1` at `Add`, `navigation2.m_Mode = Mode.None`, no scalar
  soup; the home-construction residue stays (loop-DCE conservatism is
  load-bearing) but is fully typed and compiling. 3 unit tests.
- Blocker 5 LANDED (23917 contact): the lifter emits exactly one
  packed spelling, `(float2)(lit, lit)` over float literals (constant
  pool) -- provably pure. `_PURE_LOAD_RX` admits paren-free-arg
  `(float2)(...)` (mirroring the `typeof` carve-out; a later
  substituted call keeps parens and still declines), so the dead
  packed temp drops in ordinary DCE. Cyan kept. 1 unit test.
- Improvement (45016 ConvertTo): struct-home recording types the
  `TimeOfDay` temp (`object obj29` -> `System.TimeSpan timeSpan1`),
  fixing an object-member access that cannot compile. Consigned to
  the regen list (below), not reverted.
- Blocker 4 LANDED (`_subexpr_cse`, new pass after `_value_cse`):
  anchor decls (`num`/`obj`/`t`, single-assigned, pure RHS) lend their token
  to later subexpression occurrences (`num3 = num2 | num2 >> 16`). Purity is
  the exact `_value_cse` test (no auto `?` decline; one well-formed ternary
  required); kills mirror the strictest passes (depth/labels/goto/case/
  catch/finally/break-loop-frames/backward-gotos/stores/byref); fix-58b
  holds (calls/`new` never seed); whole-token replacement with atom-paren
  strip. Both pow2 sites fold (23761, 23767). 5 unit tests. Side effect:
  the 25626 offset chain compacts too (`num4 + bytePtr1`, was fully
  re-expanded) -- the pinning test over-fits the old spelling, consigned
  to regen, not a revert.
- Blocker 1 foundation LANDED (table + recursion + homes, zero blast radius):
  S4 (subagent) root-caused B11's loss: NOT a line pass but
  `_abandon_at_region_close` firing on the loop latch (region opened at
  the header, closed on the latch) and emitting `break` + deleting the
  block's statements -- flow inversion by construction. Fix in
  `dec/emit.py`: a latch block carrying statements emits label + stmts,
  marks consumed, emits the backedge copies, and falls off (the
  structured loop IS the backedge); empty latches keep the old
  break-out. 23762 now keeps `if (obj5 != null) { obj5.navigation =
  obj18; }`.
  S5 (subagent) corrected the call map (MethodRef kind-6 slots prove
  closed generic identities: GetEnumerator/MoveNext/Dispose/Clear over
  (Selectable, Navigation); no get_Current call; s_38/s_48 are silent
  aggregate fills) and designed home typing: `_proved_struct_home`
  seeds `slot_types` at proved-generic `info` sites (`&s_N`
  buffer/receiver + closed-struct substitution; static path additionally
  requires struct return and no byref/pointer params). 23762 now
  declares `Dictionary_2<...>.Enumerator dictionary21` with named
  MoveNext/Dispose. s_30 buffer typing skipped (size unprovable for
  open defs); key/value field subst still needs the sidecar.
  Fixed along the way: fake-VA allocator is process-wide (class-level
  `_tn_cache` is shared across Il2Cpp instances -- an order-dependent
  cross-test collision, caught by the suite).

  `_synthetic_inst` (fake-VA side table on `Il2Cpp`, keyed cache for
  dry/real stability) + reader branches (`_generic_inst_name`,
  `_closed_type_key`, `td_of_ty`, `_generic_inst_args`, `_td_of`,
  `_generic_class_args`, `_byval_struct`, `_type_has_var`) +
  recursive `_subst_closed` wired into `candidate_return_type`
  (all-or-None, byref preserved, tails untouched, SRET/`trust`
  stand-downs frozen). Proved on real rows: `Dictionary_2<Selectable,
  Navigation>.Enumerator` renders exact, keys structurally, td 1514
  round-trips; real specs close (`ChangeEvent_1<bool>`). 23762 itself
  is unchanged (no spec carries our args; interface path dominates) --
  the receiver-driven + field-sidecar slice stays next per blueprint.
- DEFERRED with designs (not regressed, still open): blocker 1 remainder
  (23762: no closed Enumerator/KVP rows exist by scan, so return
  substitution alone cannot represent the type; deeper: NO MethodSpec
  carries (Selectable, Navigation), so substitution must be
  receiver-driven (closed Dictionary row 6766 + open 11337 return), not
  spec-driven; `type_sizes[1514]` is None and its field chain shows only
  `_dictionary`, so size/field fast paths need the inflated chain; S1's
  consumer audit (exact touch list in session record) covers table +
  reader branches + recursion + home typing, but homes (0x15 excluded
  from `_struct_home_ty` by design) and field-type substitution at use
  sites still need a sidecar design -- table-alone buys ~2 decl lines
  for corpus-wide hot-path churn, so implementation waits for the full
  blueprint; key/value reads are
  field loads and the assignment loss is structural -- needs a
  synthetic nested-type table + home typing + receiver resolution +
  field substitution; the double Dispose is faithful, two native
  calls; the finally `obj14.Dispose()` on `&obj3` needs the same
  struct-typing machinery) and blocker 4 (power-of-two reuse needs
  subexpression-CSE/value-numbering: `_value_cse` is whole-RHS only
  and lifter `_bind` is per-OBJECT by fix-58b design; output is
  correct and compiling today).
- Crash fixes (prior drift exposed by volume, fixed narrowly): tied
  pending-call sort (`sorted` on Expr compare -> stable key sort +
  discovery order; 129 build fallbacks cleared); unknown-size
  `_stack_store` guard in the sret fold (3 lost bodies recovered);
  `_kill_one` preserves `_mi`/`_usg_idx` + delegate-index guard (8 sweep
  `list[None]` crashes cleared). 1 unit test; repro probes in Temp.
- Parse fixes (prior null-base-address drift): `_wb_operands` renders
  numeric dst as the twin-matching deref (`16 = v` unparseable);
  `_unsafify` repairs cast-prefixed `(T*)*N` (multiplication untouched);
  `_subexpr_cse` paren-strip declines call/type/index/shared-marker
  contexts (77059 + TextGeneratorUtilities cases). 3 unit tests.
- Crash repairs (prior volume exposing HEAD-latent bugs, all
  stash-proven not-mine): tied pending-call `sorted` on Expr compare
  (129 build fallbacks cleared, discovery order kept); unknown-size
  `_stack_store` in the sret fold (3 lost bodies recovered);
  `_kill_one` dropping `_mi`/`_usg_idx` + delegate-index guard (8 sweep
  crashes cleared). 1 unit test; repro probes in Temp.
- Parse repairs (prior null-base/bool drift, all stash-proven
  not-mine): `_wb_operands` renders numeric dst as the twin-matching
  deref; `_unsafify` repairs cast-prefixed `(T*)*N` (multiplication
  untouched); `_subexpr_cse` paren-strip declines call/generic/index/
  shared-marker contexts (77059 + TextGeneratorUtilities cases);
  `_bool_sugar` paren-wrapped folds take the `[^?]` guard (101899
  family); `_simplify_cond` requires whole-group negation
  (MinMaxAABB family). 5 unit tests.
- Parse-0 repairs (prior drift, each stash-proven not-mine except
  where noted): `_bool_sugar` paren-wrapped folds take the `[^?]`
  guard (101899 family: lazy group spanned `&`-joined ternaries);
  `_simplify_cond` requires whole-group negation (MinMaxAABB family:
  `!(A) & (B)` is not `!((A) & (B))`); `FOLD_RE` declines call-argument
  parens like `SUB_CMP_RE` (`s_28.ctor(0 + 1)` kept intact,
  XmlNodeConverter). 3 unit tests.
- Gates: strict rebuild 11,181 files / 114,458 bodies / 0 failed / 0
  fallbacks (matches promoted baseline exactly); brace 0 unbalanced;
  parse 0 bad / 0 ERROR / 0 MISSING (was 109 / 5349 / 33);
  portable 751 green (718 + 33 new); full suite 846 passed / 35
  failed, failure SET byte-identical across every stage. The 34
  = baseline triaged 22 + 12 inherited-drift items, EACH proven
  not-from-this-session (prior tree fails the same 12: P6 files 2,
  unpcklps handler 1, owner-strip 4+closure+45016-line, klass-bind
  gate 4 incl. 39789/packed/datetime/26747-guard; my tree adds only
  the 45016 TimeSpan improvement hunk). Per-item evidence in
  TODONOW.md's session addendum. No new failures from this session
  (the +1 vs the earlier 34-count is the 25626 improvement pinning the
  old spelling, plus 5 new CSE tests on the passing side).
- Leftovers: blocker-1 remainder (receiver-driven substitution +
  field sidecar + structuring, blueprint ready), Navigation merge-side
  facts, per-arm Color, 35 golden/review items awaiting gated regen
  (22 triaged + 12 drift + 1 improvement-pin), promotion (user call).


## Current work: recovery follow-up round 3d (2026-09-20, unpromoted)

Same rules: `final_out/` untouched, no snapshot regen, no promotion.
Portable 718 green; full suite 822 passed / 22 failed (identical triaged
set as 3c — the pass moved none of them).

- `switch(string)` phase 1 (`_hash_string_switch` in `flow.py`, after
  `_switch_synth`): Roslyn string-switch is a ComputeStringHash
  binary-search + per-arm string-equality confirm; ranges only route,
  confirms dispatch. FNV-1a/32 over UTF-16 units verified against 20
  observed constants; every leaf proves itself (unanimous
  ComputeStringHash callee via IL candidates, literal FNV == arm hash
  const, pairwise-distinct hashes, String Equals/op_Equality callees,
  no rebindable flow or S/H refs, H dead past tree, >=3 cases).
  Handles direct `==`, temp-mediated and inline Equals confirms, and
  negated `if (!V) {} else {}` pass-time shapes; declension for gotos,
  loop arms, collisions, unverified leaves. Dead literal/equals temps
  collected downstream. Folds 25293 (8 cases), 24765 (8 cases +
  breaks), twins 25577/26314; 24694 declines honestly (gotos).
  Post-fold hardening: unjumped labels allowed in arm prefixes (26314
  has two dead ones; jumped labels abort anywhere since C# forbids
  jumping into a switch section and dropped labels dangle), plus a
  cross-arm/outside-span temp-use post-check (prefix temps vanish with
  the span). Full suite 822/22 identical triaged set.
- Per-arm Color: deferred with evidence, no source change. All three
  repro shapes flow through phi copies into Color-typed sinks (26794
  `Color color1`, 27827 `.color = ternary`, 23917 `set_color`), but
  text level cannot recover the hidden B/A channels from `(float2)`
  display, and rendering all four floats churns 1445 corpus sites in
  352 files for 8 cosmetic sites (values are correct 16B throughout;
  only display is lossy). Needs use→def const rewrite machinery.
- Leftovers: Navigation merge-side facts, 22 goldens awaiting gated regen.

## Current work: recovery follow-up round 3c (2026-09-20, unpromoted)

Same rules: `final_out/` untouched, no snapshot regen, no promotion.
Portable 718 green; full suite 822 passed / 22 failed (70050 + 107123
restored to golden, no new breaks; remaining 18 snapshots + 4 review
tests match prior triage).

- SIMD twin-consistent, both shapes (design: twin-unanimity with
  raw/honest fallback; looseness is cosmetic-only, never wrongness).
  - Shape B (107123 vorn_u32 -> `/* nothing */`): `_dead_shared_forwarder`
    in `calls.py` declines the pending bare-statement when the caller VA
    is multi-candidate, the target is single-candidate, and the next
    insn is int3/ud2. Single-caller `RemoveAll` still flushes.
  - Shape A (70050 double3x3 negate, byte-exact golden): `_xor_twin_load_sites`
    scan in `build.py` (sqrt-site precedent) proves same -0.0 const +
    same base reg + packed-16/scalar-8 adjacency; scalar loads decline
    member sugar in `_aggregate_load` + `_field_expr`, the `_R4_TY`
    width rule restores `byte*`, textpass renders the golden.
- Event `+=`/`-=` folds mirroring `set_` (void-gated, 3 unit tests);
  native-list `.Count` for field receivers; exact `<T>` narrowed to
  method-level args after a live misfire; assignment-ternary bool
  materialization with all-uses retype.
- DISPROVED with evidence (no source change): Navigation phi-atom
  read-side acceptance. The phi atoms are Navigation-typed chunks
  (v165/v166), so the bool Wrap field can take neither (compile break
  under loose naming; `v166.m_Mode` misread via struct-chain). Needs
  merge-side unanimous-subrange preservation (the stuck design).
- Censuses (read-only, JSON under `%TEMP%/opencode`): hash-switch
  family is real — ComputeStringHash + range splits + string confirms,
  single-write pure temps (25293 FPSController.ConvertStringToKeyCode
  smallest complete + 4 twins, 24765, 24694 with loop-continue arms);
  divergent color ternaries in 8 methods (23917 contact red/green
  headline, 27827 3-way, 26794 if/else stores).
- DEFERRED with designs (not regressed, still open): per-arm Color
  (bytes lost at text level; load can't know Color vs Vector2 — needs
  consumer-type proof); Navigation merge-side design.
  (`switch(string)` landed in 3d below.)
- Leftovers: 22 triaged goldens (regen only after gates).

## Current work: recovery follow-up round 3b (2026-09-20, unpromoted)

Subagent-assisted fixes + reverts. Same rules: `final_out/` untouched, no
snapshot regen, no promotion.

- Exact generic `<T>` call tokens (method-level args only; type-level
  declined after a misfire caught by golden 21027).
- COUNT macro simplified to two shapes; native-list field receivers.
- Assignment-ternary `? 1:0` materialization with all-uses-bool retype;
  phi-decl hoist (mic block fully bool-typed; Update verified).
- Ambiguous-shape slot kill (32837 zeros gone); name-shadow renames.
- Reverted with evidence: full SIMD tracking (stash-proven 0 wins, broke
  twins/sqrt in 3 goldens), partial structs (undeclared slots),
  identity/single-origin folds.
- Gates: portable green; game goldens hold prior fixes (31361/2, 45016,
  21027, review83 typed-shared, review81).
- Leftovers: Navigation path-sensitive facts, color ternary arms, full
  SIMD redesign (twin-consistent), 24 triaged goldens (regen vs genuine:
  32837-shape, 104428-tail, 32832/11974 unclear).

## Current work: recovery follow-up round 3 (2026-09-20, unpromoted)

Subagent-assisted round (4 analyses + 2 implementations, all gated).
Same rules: `final_out/` untouched, no snapshot regen, no promotion.

- Exact generic `<T>` call tokens from proved slot identity (method-level
  type args only; generic-type case declined after a misfire).
- Byref params kill slot caches (80548 head back); ambiguous-shape calls
  union-kill arg0 slots (32837 stale zeros gone); `.ctor`-on-stack-buffer
  records construction (31664 whole).
- VT-echo/exact-first guards (m_State/m_StateBlock); fragment type
  preservation (104428 call type); static RGBA bytes to Color (generalized
  structs, phi-bytes infra that honestly declines divergent arms).
- Ternary bool reconciliation, assignment `? 1:0` materialization with
  all-uses-bool retype, phi-decl hoist (mic block fully bool-typed);
  native-list `+0x28` Count sugar incl. field receivers.
- Reverted with evidence: full SIMD tracking (0 wins, broke twins/sqrt in
  3 goldens — stash-proven), partial structs (undeclared slots),
  identity/single-origin folds.
- Gates: portable 718 green (45 followup tests); full suite 816 passed / 24 failed, every failure triaged
  (improvements-awaiting-regen vs genuine: 32837-shape, 104428-tail,
  32832/11974 unclear, 83s neutral/brittle).
- Leftovers: Navigation path-sensitive facts, color ternary arms, full
  SIMD redesign (twin-consistent), per-golden regen only after gates.

## Current work: recovery follow-up round 2 (2026-09-20, unpromoted)

Continues the prior session (committed 5b13c9d). Same rules: `final_out/`
untouched, no snapshot regen, no promotion. CRLF/no-BOM kept via binary
patches; `tests/test_recovery_followup.py` (LF) now pins 40+ behaviors.

- Exact-tiling composites with per-tile routing (`_parts`), proven-prefix
  recording, fragment type preservation, slot-type fill on composites.
- Ignored-call flush twin-proofed (mov-copies, phi copies, rendered text);
  ambiguous-shape calls union-kill arg0 slots; byref params kill slot
  caches (viscosity head back); `.ctor`-on-stack-buffer records.
- Call rendering: exact generic `<T>` tokens (method-level args only),
  VT-echo/exact-first guards (`.m_State`/`.m_StateBlock` back),
  List `.Count`, native-list `+0x28` `.Count` sugar, static RGBA bytes to
  `Color.*`/`new Color` (+ generalized RGBA structs).
- Dec passes: ternary bool-arm reconciliation, assignment-ternary `? 1:0`
  materialization with all-uses-bool retype, phi-decl hoist (Update mic
  block fully bool-typed; enum decls via hint-guard; IntPtr tests null).
- Reverted with evidence: partial struct assembly (undeclared slots),
  identity/single-origin folds, fragment re-root reversal confusion.
- Fixed-then-verified regressions: 31664 ctor/store/return, 32837 stale
  zeros, 104428 call type, 31361/2, 45016, 126258 null-check, 5769 byte.
- Gates: portable 711 green; full suite ~807 passed / 24 failed, every
  failure triaged (improvements-awaiting-regen vs genuine: 32837-shape,
  104428-tail, 32832/11974 unclear, 83s neutral/brittle).
- Leftovers: Navigation path-sensitive facts, color ternary arms, SIMD
  lanes, `GetComponent` (done), mic scope (done), per-golden regen only
  after gates.

## Current work: decompiler recovery follow-up (2026-09-19, unpromoted)

Continues `nowtodo.md` (2026-09-19 stop record, committed alongside): the
experimental aggregate/interface/null-edge work plus new fixes below. Nothing
here is promoted: `final_out/` untouched, no snapshot regen, no rebuild. All
`il2cpp/` edits kept the CRLF/no-BOM contract (binary patches with
line-ending asserts); `tests/test_recovery_followup.py` (LF) pins the new
behavior (38 tests).

- Aggregate audit: `_write_mem` no longer suppresses sliced stack stores
  (suppression + merge-killed slices produced undefined temps; contact's
  `obj22` is now a defined `contact1.pointB.x`), mem-facts keep the value's
  refined text, exact-tiling composites route per-tile (`_parts`), narrow
  provenance records its prefix, valuetype loads fall through on degraded
  fragments, reference loads defer to exact `_field_expr` hits.
- Ignored non-void calls flush once as bare statements at defpos after phi
  destruction (replaces bind-everything; used calls stay inline; twin-proofed
  against mov-copies and phi copies). `RemoveAll` retained in OnEnable.
- Write barriers and `.ctor`-on-stack-buffer record their stores; byref
  params kill the slot cache (viscosity `num1<num2` + stride back).
- LEA names unified to the `slot_var` convention (no more `s_ffff…`
  aliases); MOVDQA/MOVDQU stores/loads handled; List `+0x18` renders
  `.Count`; static RGBA bytes render `Color.*`/`new Color` via `_color_text`.
- Proven-type beats instruction-shape hints (`InputMode` decls back);
  IntPtr/UIntPtr (any TE spelling) test against null; unknown-kind TESTs
  stay null-style.
- Fixed goldens now passing: 31361/2 (`.m_State`), 32833 field
  (`.m_StateBlock`, entry drift remains), 31664 (ctor/store/return),
  45016, review80-touchscreen. Remaining 24 failures triaged per item
  (several read as improvements pending gated regen; open regressions:
  32837 value→zero folding, 104428 call-absorbs-select, SIMD-lane vectors,
  color ternary arms, Navigation full struct, `GetComponent<T>` args).
- Gates: portable 695+ green; full suite 803 passed / 24 failed (HEAD
  stash-proves-clean at 795/795, so all 24 are working-tree drift).

Leftovers: Navigation struct assembly needs path-sensitive facts
(first-item skip-join legitimately phis); contact color arms + SIMD lanes +
custom `+0x28` count; mic bool/int `SetActive` + PTT flag scope; item 9
(hash-switch/events) correctly deferred; per-golden native review before
any regen/promotion.

## Package split (2026-09-12, no behaviour change)

`il2csharp.py` (10,061 lines) and `decompiler.py` (8,407 lines) were split into
the `il2cpp/` package (42 modules). Lines were moved by binary CRLF slicing,
never retyped, under coverage and line-preservation asserts; the splitter is
`work/split/split_pkg.py` and the import smoke is `work/split/smoke.py`.

- Big classes are composed from mixins, one file per mixin: `Il2Cpp`
  (`runtime/`: registration, types, fields, eh), `Lifter` (`lifter/`: state,
  values, insn, calls, render), `Decompiler` (`dec/`: build, analyze,
  structure, sugar, seh, flow, dataflow, highlevel, textpass, emit).
  Pass order inside `_structure`/`_final_text` is untouched.
- Cycle-free by construction: leaf helpers live in `il2cpp/names.py` and
  `il2cpp/runtime/meta.py`, `runtime/__init__.py` is deliberately import-free,
  and `dec/sugar.py` + `stmt_text.py` reach `Decompiler` through a late-bound
  proxy. `python -c "import il2cpp"` is the cycle regression check.
- `il2csharp.py` is now a launcher (CRLF + UTF-8 BOM retained), so
  `python il2csharp.py <target> -o <out>` still works; `python -m il2cpp` too.
  `decompiler.py` is gone (`bckups/presplit_20260912/` holds both originals).
- Consumers moved to real imports (no re-export shims): 271 import lines in
  154 files across `tests/`, `tools/`, `work/`. Historical monolith snapshots
  under `bckups/`, `final_out/`, and `work/review8*` were deliberately
  left untouched.
- Contract test `tests/test_source_format.py` now asserts CRLF + no BOM across
  `il2cpp/**/*.py` and CRLF + BOM on the launcher. `source_sha256` in
  `tools/validate_corpus.py` / `tools/make_goldens.py` now pins every package
  file via `corpus_common.source_fingerprints()`.
- `tests/test_diagnostics.py` imports `il2cpp.cli` (not the facade) because
  `main()` resolves `Emitter`/`Metadata`/`is_arm64_binary` in that module.
- Gates: 436 tests pass (317 portable + 64 snapshots + 54 native, plus the
  extra source-format case); byte-identity rebuild vs `final_out/` recorded in
  `validation_reports/split_rebuild_verification.json`.
- Root cleanup: `scan_stale.py` -> `tools/scan_stale.py`, `SHA256SUMS.txt` ->
  `validation_reports/SHA256SUMS.txt` (`tools/verify_release.py` looks there
  first, then the tree root).
- `work/` reorg (2026-09-12, moves only, no renames): the flat tree is now
  grouped into `artifacts/`, `batches/`, `census/`, `experiments/`, `lib/`,
  `logs/`, `patches/`, `probes/`, `review81/`-`review89/`, `runners/`, and
  `split/` (routing table in `work/README.md`; `review83/`, `review84/`, and
  the `reviewNN_out/` trees predate the reorg and were left as-is). The 176
  root-deriving scripts were depth-rewritten in the same pass
  (`parents[1]` -> `parents[2]`, one more `dirname(...)`);
  `work/split/verify_reorg.py` proves every root expression still resolves
  (167 expressions across 162 files).
- Release manifest refreshed after the split + reorg:
  `validation_reports/SHA256SUMS.txt` 12,597 -> 12,638 entries (406
  relocated, 11,391 rehashed — the old manifest still pinned the Review 84
  tree while `final_out/` holds the promoted Review 89 tree, as proved by
  `work/split/probe_manifest_era.py`: 400/400 sampled `final_out/` digests
  match `bckups/final_out_r84`, 0 match the current tree — 1 dropped
  `decompiler.py`, 42 added `il2cpp/` files; the pre-split manifest is
  archived at `validation_reports/SHA256SUMS.presplit_20260912.txt`).
  `tools/verify_release.py` passes with 0 failures.
- Post-verification cleanup: `work/split/rebuild_out/` (the 11,200-file,
  ~138MB byte-identical rebuild used once for the split proof) deleted; the
  proof stands in `validation_reports/split_rebuild_verification.json` and
  `work/split/rebuild.log`. Small evidence logs kept (`rebuild.log`,
  `fulltest.log` with the 436-pass run).

## Current work: unavailable method bodies (committed 3bf35b3, pushed 2026-09-19)

Concrete methods with no native address now emit a throwing body instead of
an illegal semicolon declaration. The shared body path also covers accessors,
declaration-only output, unavailable lifting backends, and method limits.
Abstract/interface contracts retain semicolons, and successfully recovered
empty bodies remain empty. Missing bodies throw `NotImplementedException`
with an explicit recovery message; these are placeholders, not recovered
implementations, and do not increment lift/failure/fallback counters.
The final namespace-shortening pass preserves alias-qualified names such as
`global::System.NotImplementedException`; stripping `System` there would bind
the exception in the global namespace instead.

Regression coverage compiles generated constructors, ordinary and explicit
interface methods, indexers, properties, and events with Roslyn in all three
unavailable-body modes. Committed evidence: `validation_reports/method_bodies_{parse,
delta,regeneration}.json`; build/compile/tests logs were removed in the
2026-09-19 cleanup. Candidate tree `work/method_bodies_out/` was removed in
the same cleanup (superseded by `work/rpc_payload_out/` below).

Gates: 795 tests pass (669 portable + 126 native); strict build 11,181 files /
114,458 lifted bodies / 0 lift failures / 0 structured fallbacks / 0 type-emission
failures. After the namespace correction, 1,005 files containing `::` were
regenerated through the emitter (21,944 lifts, all failure counters zero),
copied back by TypeDefIndex with full-build shared stubs retained; provenance
and final source fingerprints are in `method_bodies_regeneration.json`.
Final parse: 0 bad files / 0 errors / 0 recovery nodes. Compiler probe:
10,305 → 2,463 errors, 1,516 → 726 files with errors; CS0501 7,718 → 0,
CS0535 88 → 0, CS0073 26 → 0, CS8051 9 → 0, CS0523 1 → 0. Other diagnostic
counts are unchanged. The tree contains 9,193 explicit unavailable-body throws;
it still does not compile or provide those implementations. No control-flow
lifting changes were made. Next largest category is CS0737 (880), followed by
CS0111 (384) and CS0052 (308).

Duplicate-method triage must distinguish actual emission collisions from the
combined-assembly probe: for example, `IsUnmanagedAttribute` has one constructor
in each source assembly, but combining those partial types produces CS0111.
Deleting those constructors would damage the individual recovered assemblies.

## Current work: accessor recovery + RPC payload typing (committed 3bf35b3, pushed 2026-09-19)

Committed tree stacks two units on the promoted fix-123 tree:
`il2cpp/csharp.py` + `emitter.py` + `runtime/fields.py` (storage identity
`__field_X`, real property/event bodies; `tests/test_member_recovery.py`,
`tests/test_game_member_recovery.py`) and `il2cpp/lifter/{state,insn,values}.py`
+ `runtime/types.py` (pointer/array operand typing, below). `final_out/` still
holds fix 123; `work/accessors_out/` and `work/rpc_payload_out/` were the two
gated candidate trees (both 11,181 files, 0 failed lifts, parse 0/0/0).
`work/accessors_out/` was removed in the 2026-09-19 cleanup;
`work/rpc_payload_out/` is the retained newest output and matches the pushed source.

RPC payload typing (specimen InventoryManager.Rpc_CMD_UpdateInventoryForHost,
mi 25626, VA 0x180704750): unbound `obj1` and `object` payload arithmetic are
gone — `inventoryIds_.Length`, `byte* bytePtr1 = (byte*)simulationMessagePtr1
+ 0x1c`, `int` offset chains, `((int*)bytePtr1 + off*1 + 0x0)` stores, one
`num5` temp. Fixes: RBP-as-frame is now value-tested (`_rbp_is_frame`: None /
`&s_xx` / `?addr` / never-written stay slots; params/objects/composites
resolve normally); array-typed entry params carry kind `arr` ([arr+0x18]
folds to `.Length`); `lea` over int is int math while past-struct lea from a
typed pointer spells a `(byte*)` cursor from a genuine metadata `byte*` row
(temps declare `byte*`); int-base + byte*-index SIB renders pointer-first at
scale 1 only; long binop operands bind typed instead of minting anonymous
twins; ADD int+ptr yields ptr (byte-proven type only); `.Length` carries Int32;
empty vtable rows (raw 0x1, no method bits) decline instead of naming mi 0
(healed three pinned `Interop.GetRandomBytes` misresolutions: 39789 hunks,
83647, 109664). Gates: 665 portable + 126 game pass (10 new lifter unit tests
in `tests/test_pointer_operand_typing.py`, 4 game asserts in
`tests/test_game_rpc_payload.py`); sweep 116,178 / 0 crashes / 0 new crashes /
1 structural delta (mi 37884 into_block 1→0, +1 line, nothing dropped);
9,200 changed bodies vs accessors; rebuild 11,181 files / 114,458 bodies / 0
failed; parse 0/0/0; probe 10,305 errors, per-code identical to accessors
(all 1,393 pair moves are line-number shifts). Committed evidence:
`validation_reports/rpc_payload_{parse,sweep}.json` plus
`rpc_payload_sweep.tail-args.jsonl.gz`; build/compile/sweep logs were removed
in the 2026-09-19 cleanup. Retained tree: `work/rpc_payload_out/`.
14 goldens regen'd after review (8 accessor renames untouched by this unit +
6 here: 39789/62312/83647/109664 improvements, 11974 renumber, 5769 noted below).

Open follow-ups: GetChars (mi 5769): merge type preservation for cmov-selected
values is done -- the pass wipe ran after entry setup and discarded the stack
parameter names/types, so the decoder arrived at the cmov as untyped `s_88`;
wiping before setup plus slot reloads restoring the recorded kind recovers
`baseDecoder`/`getClass()`/`charCount`/`_mustFlush`/`_bytesUsed` (was: undeclared
`num3`, then raw decoder derefs). Widths are done: a CMOVE
`recv.getClass() == typeof(T)` selecting `recv` stamps the exact type (klass
equality is exact, unlike `is`; the compared `typeof` usage already carries
the typedef -- td 691 `UTF7Encoding.Decoder` holds exactly `bits@0x30`,
`bitCount@0x34`, `firstByte@0x38`). The predicted alias rule proved
unnecessary: the existing single-known-type phi/var rule carries the derived
type to the working temps on its own. The rule generalizes (delegate types,
`_source`/`_token`, shared-call resolution, enum members, `ref` field args;
two sampled methods shed `unsafe`). Still open: the post-loop arm-scope reads
(`flag5`/`num5`/`num6`), which need declaration hoisting across the loop
boundary (structuring risk) -- do not treat as resolved. Analysis (2026-09-19):
the loop is single-trip (unconditional trailing `break`, no `continue`), and
the snapshots are load-bearing spills (arm C reads old `num2` mid-arm, so they
cannot be eliminated). Hoist-with-state-init is sound only under single-trip
(multi-trip + a non-assigning arm, e.g. `num5` in arm B, would read stale
init instead of the leftover), and the init mapping itself needs the
header-exit-edge register state -- textual `first bare copy` cannot prove
which pre-loop register the 0-trip path reads. Reading the state temps
instead is wrong on arm-C-break (snapshot `num2+6-16` vs pre-arm `num2`).
Verdict: needs exit-path-sensitive phis, not a text hoist;
CopyFromArray dest args reprint the ids extent instead of reusing `num4`:
investigated to ground truth and accepted as residue -- native executes three
copy calls (0x1807048f7/922/94c, mi 25626); the two extra ids-copy texts are
phantoms (one execution re-rendered) over idempotent same-byte rewrites, so
output values/order are faithful. Reusing `num4` would delete executions,
which needs execution-identity proof the pipeline does not have: _bind folds
per OBJECT, never per text, precisely so real duplicate calls are never
merged (fix 58b SaveManager rule). Two honest attempts reverted: counting
movsxd copies as uses bound earlier but collapsed the `num4`/`num5` temp
boundary the spec pins; rewriting live superstrings at bind time did the same
with added epoch hazards. Needs value provenance, not a window tweak.
`&this.field`-in-rbp and genuine `T* + N` element arithmetic keep today's
spelling.

Gate for the three unnumbered follow-ups above (float shortening, cmov
merge-type, exact-type stamp; pushed `a2887e9`): `work/followups_out` built
strict, 11,181 files / 114,458 bodies / 0 failed lifts / 0 structured fallbacks
/ 0 type-emission failures; brace audit 0 unbalanced; tree-sitter parse 0 bad
files / 0 ERROR / 0 MISSING; full-corpus sweep 116,178 methods / 0 crashes;
2,759 files differ from `work/rpc_payload_out` (none added/removed), all
sampled diffs rename/type/field-only. Follow-up: float tie-break prefers fixed
point on length ties (`10000.0f`, not `1e+04f`; 14 addresses moved, 0 crashes)
and `tests/goldens_review84.json` was regenerated with `tools/make_goldens.py`
against the refreshed sweep/parse reports: 6/64 snapshots changed (GetChars,
ReadSpan, Update, OnNextUpdate, ConvertTo, Execute), each reviewed
individually, all structurally identical; full suite 795 passed. Promoted
2026-09-19: `final_out/` holds `work/promote_out` (11,274 files, aggregate
`db468523…050c36105`, 0 mismatches); see `docs/archive/reviews-log.md` 0bg
and `validation_reports/followups_promotion_verification.json`.

## Cleanup 2026-09-19 (after the 3bf35b3 push; `bckups/` deleted later the same day)

Deleted per user call: all untracked build/compile/sweep/tests logs under
`validation_reports/` (reviews 114–123, accessors, method bodies, rpc_payload,
partial_unsafe — the committed parse/sweep/promotion/delta/regeneration JSONs
and tail-args blobs stay, 472 tracked files), all gitignored sweep/compare
blobs (`*.methods.jsonl.gz`, `*_vs*.json`, `*comparison.json`,
`output_audit.json` — regenerable via rebuild/sweep), the superseded
candidate trees `work/accessors_out/` + `work/method_bodies_out/`, and finally
the whole `bckups/` dir (9 promoted-tree copies fix99–fix122 + review97e,
1.24 GB — GitHub is now the history authority; no tracked file was touched).
Work-tree pass the same day: all `work/review98_out`–`work/review123_out`
(26 gated trees, ~3.6 GB — `review123_out` was byte-identical to `final_out/`,
`review114_out` was an unfinished partial rebuild), the unreferenced
`work/method_bodies_alias_regenerated/` intermediate (already copied back),
and `work/accessors_preview/` probe artifacts. Every deleted tree rebuilds
from git history in ~7–9 min; per-fix paragraphs below keep their `built tree`
citations as the gate record.
Kept: `final_out/` (promoted fix-123 baseline), `work/rpc_payload_out/`
(matches pushed source), and the older `work/review*_out` + `work/partial_*_out`
trees. Historical paragraphs below that cite a removed log/blob/tree keep
their original lists as the gate record — the file itself is gone.

## Historical residue: post-promotion (fix 123 era; counts predate r4c, see below)

`final_out/` holds the follow-up tree (probe 2,463 errors / 726 files,
`validation_reports/probe_final_out.json`). CS0053 is 0 there and 0 on the
retained `work/rpc_payload_out` tree (`probe_rpc_payload_out.json`: 10,305 /
1,516, matching the recorded baseline exactly) -- the 222 fix-123-era sites
cleared before this session (likely the accessor-recovery unit), so the
accessibility-honesty lane needs no policy decision. Live lanes: CS0737 done (880 -> 0: private+final+virtual methods with plain
names qualify via the unique directly-listed interface method with the same
name and rendered signature -- async `MoveNext`/`SetStateMachine`, iterator
`MoveNext`; trigger census matched the error count exactly, probe delta is
the sole change, `work/iface_out` + `validation_reports/probe_iface_out.json`);
CS0052 done (308 -> 0: private nested `__StaticArrayInitTypeSize=N` / Mono
`$ArrayType=N` blob structs, always empty, render `internal` -- over-visible
never errors -- with a CS0262 knock-on (28 -> 16: 12 sizes exist as
split-visibility duplicate typedefs, `0x113` vs `0x115`, unified on the
metadata majority; `work/blob_out` + `validation_reports/probe_blob_out.json`);
CS0111 384
(combined-partial duplicate constructors, known do-not-touch: deleting them
would damage the individual assemblies); CS0052 308
(`__StaticArrayInitTypeSize_N` field accessibility); the masked
body-pointer-local layer (needs expression typing first); project wiring.
The complete game is not yet compilable.

## Previous work — fix 123 (collision-aware using/strip; gated + promoted 2026-09-17)

CS0104 triage (140 sites) showed shortening rebinds references two ways:
duplicate short names across imported namespaces (`Hashtable`,
`Object`, `Random`) and heads matching a visible namespace final segment
(`HID.HIDDeviceDescriptor`). `collision_heads` (new in `il2cpp/csharp.py`,
mirroring `rep()`) flags exactly the heads shortening could produce, proven
per file against the metadata short-name table (global-ns rows excluded —
usings win over globals empirically); `strip_namespaces` keeps those full
chains. Generic arguments render full paths at every depth (the `ErrorEventArgs`
bare-arg gap), and explicit *method* qualifiers split before sanitizing
(`IDictionary<TKey,TValue>` kept its commas). Gates: **759 tests** (6 in
`tests/test_review123_collisions.py` — 5 unit + 1 game-backed); strict
rebuild 11,181 files / 113,938 bodies / 0 failures (`work/review123_out`);
parser 0 bad files; direct sweep 116,178 methods / 0 crashes / 0 structural
changes vs fix 122; probe **10,794 → 10,602 (−192)**: CS0104 140→3,
CS0246 43→0, CS0305/CS0308/CS0426/CS0538 →0, CS0535 −13, against CS0053 +21
(accessibility unmasking, characterized above). One golden diff reviewed
(fulldepth args only) before regen; one game-test expectation corrected to
the faithful `System.EventHandler_1<...>` spelling. Reports:
`validation_reports/review123_*`. Promoted 2026-09-17: `final_out/` now
holds `work/review123_out` (11,274 files, aggregate `45711645…3791d3c6`, 0
mismatches; the `bckups/final_out_fix122` copy was removed 2026-09-19, see the
cleanup note above).
Post-promotion parse recheck 0 bad files.

Comparison temps (`obj227 < 6`) are CLOSED with no code change: a full
`.pdata`-extent native scan of `InventoryManager.Update` finds no compare,
test, or arithmetic instruction with immediate 6 anywhere — the literal is
decompiler-synthesized (jump-table/switch-bound recovery), so no width/sign
evidence exists to thread and any numeric cast would invent semantics.
Where a real `cmp reg, nonzero-imm` executes, the existing chain (CMP hint
→ rename classifier → `_decl_type_of` → fix-104 cast) already emits exactly
the desired shape — same VA, other branch: `int num11 =
(int)sub_180001da0(...); if (num11 < 6)`. The remaining work is provenance
for synthesized switch-bound literals, not temp typing.

## Previous work — fix 122 (receiver-proven stub temps; gated + promoted 2026-09-17)

The user's specimen (`object obj228 = sub_...; obj228.SetTrigger("Reload")`)
opened the shared-body/`objN` lane. Triage: two of its three addresses are
unregistered natives (zero candidates — call identity unknowable, only
use-types recoverable); the third is StartCoroutine/StartCoroutine_Auto
(already cast-covered). New rule (`_stub_receiver_decls`, feeding the
existing fix-104 cast machinery): an `object X = sub_(...)` declaration
whose only other mention is one bare `X.Method(literals)` call, resolving
by literal-applicability to exactly one instance non-generic metadata
method (exact arity, or provable defaults; params-array expansion honestly
unmodeled so larger arities without full defaults decline), is retyped to
the owner with a caller-proven cast. Writes, address-takes, ref/out/in,
redeclarations, non-literal args, and accessor-shaped names all decline.
Census: 116 unique-owner sites (game types: StoreManager 30, JSONAccess 7…),
380 non-literal, 195 ambiguous. Ground truth: `UnityEngine.Animator
animator2 = (UnityEngine.Animator)sub_180001d80(...);
animator2.SetTrigger("Reload");` — and the semantic renamer adopts the
proven type for temp names. Gates: **752 tests** (10 new in
`tests/test_review122_receiver_casts.py`); strict rebuild 11,181 files /
113,938 bodies / 0 failures (`work/review122_out`); parser 0 bad files;
direct sweep 116,178 methods / 0 crashes / 0 structural changes vs fix 121
(49 changed bodies, every diff a retype+cast+rename audited file by file);
probe **10,794 → 10,794**: the fix is probe-invisible today because
error-typed/unbound upstream values mask downstream binding (verified: the
fixed shape errors standalone, the region is silent in-tree), so it removes
future CS1061s rather than present ones — zero cost either way. Reports:
`validation_reports/review122_*`; 64 goldens untouched. Promoted 2026-09-17:
`final_out/` now holds `work/review122_out` (11,274 files, aggregate
`3a513e9a…13b49de`, 0 mismatches; the fix-121 tree is kept at
`bckups/final_out_fix121`). Post-promotion parse recheck 0 bad files.

## Previous work — fixes 120 and 121 (nested owner paths + mirror completion; gated + promoted 2026-09-17)

CS0246 triage crowned the nested-qualification gap: the typedef `declaring`
field is -1 top-level and out of range for all 5,719 nested rows, so
`typedef_full`'s owner walk never fired and nested references rendered bare
(`CallbackContext` for `InputAction.CallbackContext`). Owners now resolve
through the forward `nested_types` table inverted once per instance
(`_nested_owner`; top-level `declaring == -1` consumers untouched), with the
outermost namespace on the path. Generic owners distribute instantiation
args outer-first (`List_1<T>.Enumerator`, `Dictionary_2<TKey,
TValue>.KeyCollection`). Nested containers holding mirrored owner params
plus own trailing ones (290 mirror vs 184 independent by census) declare
only the own suffix (`DispatchDelegate(T)` exactly as Valve wrote it;
`ConstraintComparer<K>`), because same-named independence is inexpressible
in C# — proven by names+counts, declined otherwise. Along the way: blob
`__StaticArrayInitTypeSize=`/`$ArrayType=` rewrites match the terminal
segment (48 parse-failing files), reference spellings sanitize per segment
(the guid-braced `PrivateImplementationDetails` owner), and strip keeps
self-shadowed full chains (`HID.HID...`). Gates: **742 tests** (13 in
`tests/test_review120_nested_paths.py` + qualifier/sanitize cases);
strict rebuild 11,181 files / 113,938 bodies / 0 failures
(`work/review121_out`); parser 0 bad files; direct sweep 116,178 methods /
0 crashes / 0 structural changes vs fix 119 (8,081 spelling-only bodies);
probe **13,352 → 10,794 (−2,558)**: CS0246 2,423→43, CS0540 38→0, CS0308
43→4, CS0305 13→4, plus drops across CS0111/CS0146/CS0523/CS0534/CS0535 and
CS0118→0, against CS0053 +6 (accessibility unmasking, characterized), one
documented CS0426 collision cost and CS0234-class silence above. The 6
golden diffs and 2 assertion updates were each reviewed (owner-path
spellings only) before regen. Reports: `validation_reports/review121_*`.
Promoted 2026-09-17: `final_out/` now holds `work/review121_out` (11,274
files, aggregate `b84d8e05…c94253`, 0 mismatches; the fix-119 tree is kept
at `bckups/final_out_fix119`). Post-promotion parse recheck 0 bad files.
(Fix 120 was gated through sweep/tests but held unpromoted when its probe
showed the CS0305 mirror spike; fix 121 completes it — same two-stage
rhythm as 117/118.)

## Previous work — fix 119 (using-feeding qualified spellings; gated + promoted 2026-09-17)

CS0246 triage crowned the using-generation gap: `IntPtr` rendered bare
because `PRIM` carried no namespace (1,076 sites), and `[Serializable]` /
`[SerializeField]` never named one (338/32 sites each). All three now render
qualified pre-strip (`System.IntPtr` / `System.UIntPtr` /
`System.TypedReference`; `[System.Serializable]`; `[UnityEngine.
SerializeField]`), so the tracker imports the namespace and the boundary
strips back to short form — the partial-tree diff is exactly added `using`
lines plus blank separators. Mechanism audit: `type_name` is also the
body-spelling path, so 2,148 lifted bodies changed; tree-wide audit shows
11,167 files identifier-identical, the rest renames plus 14 reflow files of
the known temp-materialization class (traced equivalent); the `_bind` /
`_kill_stale` text-identity gates that select those cascades are
spelling-agnostic within a run. Gates: **727 tests** (5 new in
`tests/test_review119_usings.py`); strict rebuild 11,181 files / 113,938
bodies / 0 failures (`work/review119_out`); parser 0 bad files; direct
sweep 116,178 methods / 0 crashes / 0 structural changes vs fix 118; probe
**15,183 → 13,352 (−1,831)**: CS0246 −1,823, CS0535 −9, no other moves
except the single documented CS0104 ambiguity cost above. Reports:
`validation_reports/review119_*`; 64 goldens untouched. Promoted 2026-09-17:
`final_out/` now holds `work/review119_out` (11,274 files, aggregate
`5855ed65…baf5d`, 0 mismatches; the fix-118 tree is kept at
`bckups/final_out_fix118`). Post-promotion parse recheck 0 bad files.

## Previous work — fix 118 (explicit-qualifier completion; gated + promoted 2026-09-17)

Fix 117's new `_N` references unmasked two explicit-member gaps. First, the
qualifier proof trusted arity-less name strings while the true interface is
the declaring type's tuple: members spelled `IObserver_1<InputRemoting.
Message>` against base `IObserver_1<Message>` (`_iface_qualifier`, unique
tuple match or decline). Second, `sanitize()` ate generic structure inside
qualifiers (`KeyValuePair<TKey, TValue>` → `KeyValuePair<TKey__TValue>`,
`T[]` → `T__`): new structure-aware `sanitize_qualifier` (`il2cpp/names.py`)
sanitizes identifier segments only. Gates: **722 tests** (12 in
`tests/test_review117_arity_spellings.py` — 7 arity + 5 qualifier/sanitize);
strict rebuild 11,181 files / 113,938 bodies / 0 failures
(`work/review118_out`); parser 0 bad files; direct sweep 116,178 methods /
0 crashes / 0 structural changes vs fix 117; probe **15,677 → 15,183
(−307), zero increases**: CS9334 30→0, CS9333→0, CS0540 124→38, plus
knock-on drops. The 38 residual CS0540 are the nested-shadowing family
above, characterized for the next fix. Reports:
`validation_reports/review118_*`; 64 goldens untouched (0 changed bodies).
Promoted 2026-09-17: `final_out/` now holds `work/review118_out` (11,274
files, aggregate `bede44dc…74d418`, 0 mismatches; the fix-117 tree is kept
at `bckups/final_out_fix117`). Post-promotion parse recheck 0 bad files.

## Previous work — fix 117 (generic `_N` reference spellings; gated + promoted 2026-09-17)

CS0115 triage (266 sites) root-caused a declaration/reference convention
split, not wrong override keywords: type declarations spell
`EqualityComparer_1<T>` (fix-113 arity convention) while every reference
spelled `EqualityComparer<byte>`, so derived overrides bound against the
*reference-assembly* base (which has no `IndexOf`) instead of the local one.
`csharp_type_name` (`il2cpp/common.py`) now renders `` `N `` as `_N`, so
references spell the declared identifier; explicit interface qualifiers
(which come from arity-less metadata name strings) recover the suffix
through a (namespace, path, top-level arg-count) typedef proof
(`_arity_qualifier` in `il2cpp/emitter.py`, wired into `method_sig` and
`emit_property`; declines on unknown/ambiguous shapes). Audit surface: 2
`split('<')[0]` uses (both against non-generic names), one `_BACKTICK_RX`
use-site, 0 methods with backticks, 779 generic typedefs.

Provenance (full old-vs-new tree audit, 3,477 changed files): 45,394
arity-insertion tokens; renames from the arity-embedding local renamer
(`list1`→`list11`, `dictionary1`→`dictionary21`; decl↔use consistent, zero
pre-existing collision targets); 18 reflow files (±1–6 lines) of one class —
a `static` generic read materialized into a temp (`object objN =
Span_1<byte>.Slice`) plus renumber cascade, traced semantically identical in
`Convert.TryFromBase64Chars` by old-vs-new direct re-lift; one loop flip
(`while (c)` → header-replay `while (true)`) via the documented `h.stmts`
rule, sound by construction. The 6 golden diffs were each reviewed
(spelling + consistent renames, decl-uniqueness unchanged) before regen;
one stale `Optional<string>` assertion updated to `Optional_1<string>`.

Gates: **717 tests** (7 new in
`tests/test_review117_arity_spellings.py`); strict rebuild 11,181 files /
113,938 bodies / 0 failures (`work/review117_out`); parser 0 bad files;
direct sweep 116,178 methods / 0 crashes / 0 structural changes vs fix 116
(7,275 changed bodies, into_block identical); probe **24,078 → 15,677
(−8,401)**: CS0115 266→0, CS0246 10,337→4,358, CS0535 1,171→191, CS0308
646→49, CS0737 −276, CS0738 259→50, CS0452/CS0453/CS0509/CS8345 →0, with
unmasked CS0540 +4 / CS9334 +3 and single-digit noise elsewhere; CS0501
steady. The mid-gate probe without the qualifier fix read 16,966 (CS0540
+512/CS9334 +148), which scoped exactly the qualifier completion above.
Reports: `validation_reports/review117_*`; goldens regenerated (6 reviewed
bodies, 58 untouched, fingerprints refreshed). Promoted 2026-09-17:
`final_out/` now holds `work/review117_out` (11,274 files, aggregate
`1bd83c61…a46467`, 0 mismatches; the fix-116 tree is kept at
`bckups/final_out_fix116`). Post-promotion parse recheck 0 bad files.

## Previous work — fix 116 (unsafe fields/properties, CS0214 zero; gated + promoted 2026-09-17)

The 517 CS0214 residue classified declaration-only: 465 pointer fields, 52
pointer properties, 0 body lines (the 2 apparent locals are
`[SerializeField]`-prefixed fields). `emit_type` field mods and both
`emit_property` paths now append `unsafe` on `'*'` spellings
(`il2cpp/emitter.py`); all shapes Roslyn-probed, including interface and
explicit-impl properties. Gates: **710 tests** (7 new in
`tests/test_review116_unsafe_members.py`); strict rebuild 11,181 files /
113,938 bodies / 0 failures (`work/review116_out`); parser 0 bad files;
direct sweep 116,178 methods / 0 crashes / 0 structural changes vs fix 115;
probe **24,595 → 24,078, the only delta CS0214 517 → 0**. Body-level
pointer locals (e.g. `NetworkBehaviour` 596) stay silent only through error
cascading — a standalone repro proves the declaration CS0214 masks them, so
a future typing fix will unmask a method-level-`unsafe` lane; nothing to do
until then. Reports: `validation_reports/review116_*`; 64 goldens untouched.
Promoted 2026-09-17: `final_out/` now holds `work/review116_out` (11,274
files, aggregate `8e93363d…9ff462b9`, 0 mismatches; the fix-115 tree is kept
at `bckups/final_out_fix115`). Post-promotion parse recheck 0 bad files.
(Note: the fix-116 promotion run briefly overwrote
`review115_promotion_verification.json` with a stale comparison; restored
from the verified fix-115 values, noted in the file.)

## Previous work — fixes 114 and 115 (dispatch, ctors, unsafe; gated + promoted 2026-09-17)

Corrected CLI MethodAttributes: Virtual=0x40, Final=0x20, NewSlot=0x100,
Abstract=0x400. The old emitter confused these with each other. Methods now
preserve virtual slots, overrides, sealed overrides and abstract overrides.
Final new-slot interface implementations remain ordinary methods; explicit
interface implementations omit access/virtual modifiers. Abstract methods
consistently have no body, even when metadata carries an address. Static
abstract interface members retain their modifiers.

Generic constructors now match their emitted type identifier: Box_1<T> has
Box_1() and static Box_1(), rather than Box(). The metadata census finds
21,410 changed method signatures and 858 changed constructor signatures.
Evidence: validation_reports/review114_declaration_census.json.

Validation: **698 tests pass**, including all 118 fixture tests and a real
Roslyn compilation of generated dispatch/constructor declarations. The Review 83
shared-boolean assertion was stale since fix 110; the prior candidate already
emits proven string equality, and the test now checks those exact conditions.
The 64 frozen method bodies remain unchanged. The strict rebuild was stopped at
the requested wrap-up point after **97,291 bodies with 0 failures**; its partial
candidate is `work/review114_out` and its log was
`validation_reports/review114_build.log` (removed in the 2026-09-19 cleanup). That rebuild never finished, so
fix 114 alone claims no whole-tree result — the Fix 115 gate below rebuilds
the same source completely and supersedes it.

New tools/compile_corpus.py invokes installed Roslyn directly, records a source
inventory digest and diagnostic counts, and saves compressed complete logs.
It merges shared stubs only in temporary storage. This is a single diagnostic
assembly, not verification of project wiring or behavior, and includes some
cross-assembly collisions. Its fix-113 baseline is **34,262 errors**, counted
once per diagnostic. Compare only with the same probe; older build-log totals
can repeat diagnostics and use different compiler references. Its largest
measured groups are missing types/usings (CS0246: 10,337), concrete declarations
without bodies (CS0501: 7,558), pointer declarations outside unsafe contexts
(CS0214: 3,627), and unimplemented abstract/interface members (CS0534: 3,527).

Follow-up (partial, ungated): pointer-signature methods and constructors now
carry `unsafe` (`method_sig`/`ctor_sig` in `il2cpp/emitter.py`, same `'*'`
spelling rule `emit_delegate` already used). Metadata census: 2,564
pointer-signature methods and 82 constructors; ground truth `NodeSwitch`
`@Invoker`s render `protected static unsafe void ...(..., SimulationMessage*
message)`. Partial evidence only: 27 targeted tests (5 new) plus an 87-test
portable subset pass, single-method re-lift of mi 23560 is unchanged, and a
single-file Roslyn probe compiles the new shapes including explicit-interface
`unsafe void IFoo.Bar(byte* p)`. Superseded the same day by the Fix 115 full
gate below (strict rebuild, sweep, probe); pointer fields/properties became
fix 116 above.

CS0501 triage (metadata-only, partial): 9,397 concrete address-less methods —
204 runtime-impl, all delegate members already suppressed through
`emit_delegate`; 8,645 plain managed (iflags 0), including whole
metadata-only types such as `DictionaryLookupTable`2` (all 11 methods
address-less); 520 aggressive-inlining, 28 no-inlining. No blanket `throw`,
`abstract`, `extern`, or `partial` rule is sound without per-method ground
truth (stripped/uninstantiated generics versus real misses), so no code
changed.

Unsafe follow-up, Assembly-CSharp gate (partial, not a full rebuild):
`--only Assembly-CSharp` strict rebuild into `work/partial_unsafe_acs_out`
(490 types, 6,610 bodies, 0 failed, ~67s; `PYTHONHASHSEED=0` — the one
non-unsafe diff in the unseeded run was hash-order noise, byte-identical on
repro). Old-vs-new diff over `work/review114_out/Assembly-CSharp`: 87 files
changed, 518 added lines, every one an `unsafe` insertion, 0 files with any
other change. Single-assembly Roslyn probe
(`validation_reports/partial_unsafe_acs_compile.json`, removed in the
2026-09-19 cleanup): ACS-scope CS0214
falls 518 → 0 (exactly the 518 insertions) and CS0106 199 → 0 (fix-114
explicit-impl rule); CS0501 holds 35 → 35, untouched by design. The 9,196
probe total is dominated by CS0246 scope artifact (8,937: cross-assembly
references are absent from a one-assembly tree), not a regression.

CS0501 tree-wide census (read-only over `work/review113_out`, 11,181 files):
8,926 bare declaration lines = 755 legal `abstract` + ~615 legal `delegate`
+ 3,647 concrete open-generic definitions with no compiled instantiation
(ACS scope: all 35 probe sites are this shape — `Shuffle<T>`,
`ConvertNestedList<T>`, `GetModule<T>`, display-class ctors) + ~3,900
closed concrete without bodies (metadata-only/editor-stripped types such as
`SerializedDictionary` ctors). Concrete-bare minus delegates closes against
the 7,558 diagnostics within noise. No body exists in the binary for any of
these, so no rendering change is sound; the bare signature stays as the
honest marker.

## Fix 115 gate and promotion (2026-09-17, full gate lifted per user call)

Fix 115 is the unsafe-signature follow-up above, built on the fix-114
source. Gates: **703 tests** (698 + 5 new unsafe-signature cases, incl. 118
game fixture tests and the 64 goldens, all live); strict rebuild 11,181
files / 113,938 bodies / 0 failures or fallbacks (`work/review115_out`);
parser 0 bad files; direct sweep 116,178 methods / 0 crashes / 0 structural
changes vs fix 113 (`validation_reports/review115_vs113.json`: 0 changed
bodies — the combined fix-114 + fix-115 delta is declaration-only);
 Roslyn probe **34,262 → 24,595 errors** (−9,667), fully attributed —
CS0106 2,402 → 0, CS0533 226 → 0, CS0534 3,527 → 3, CS1520 797 → 0,
CS0214 3,627 → 517 (residue: pointer fields and body locals only, sampled),
unmasking CS0115 266 / CS0249 121 / CS0507 4; CS0246/CS0501/CS0535/CS0737
unchanged. Reports: `validation_reports/review115_{build.log,sweep.json,
vs113.json,parse.json,compile.json,tests.log}` (build/compile/tests logs and
the vs-compare blob removed in the 2026-09-19 cleanup; sweep/parse JSONs stay
tracked); built tree
`work/review115_out`. The 64 goldens are untouched (0 changed bodies, no
regen needed). Promoted 2026-09-17: `final_out/` now holds
`work/review115_out` (11,274 files — 74 more than the fix-99 tree, exactly
the fix-104 stub files minus the 3 fix-113 orphans; candidate and promoted
aggregate sha256 both
`2379110f106b51f6958d0eb0a3f0c7bdc1a6b0de2a0490ba5612d0e03e9a07a4`, 0
mismatches; the fix-99 tree is kept at `bckups/final_out_fix99`).
Promotion record: `validation_reports/review115_promotion_verification.json`;
post-promotion parse recheck
`validation_reports/review115_recheck_parse_final.json` (11,274 files, 0
bad).

## Previous work — fix 113 (legal type declarations, gated 2026-09-18)

The Roslyn probe's semantic layer is dominated by declaration
shapes, all emitted wrong the same way. `type_decl_line` read
`0x20 & ~0x80` for interfaces — but ECMA mandates abstract+interface
together, so nearly all 636 interfaces rendered as classes (fixing
CS1721/CS0527/CS1722/CS0737 at the root: all four codes go to zero).
Abstract+sealed renders `static partial class` (census: all 1,015
have no instance fields/methods/properties/events, no bases or
interfaces — zero tradeoff). User delegates (616, via MulticastDelegate
parentage) render `delegate R Name(params);` through Invoke (generic
arity mirrors the `List_1<T>` class convention so references match;
.ctor/Invoke/BeginInvoke/EndInvoke suppressed as compiler-provided;
falls back to class rendering if Invoke/fields/props/events/nested
are ever missing/present). Interface members lose access/instance
modifiers (DIM bodies kept under a new `<LangVersion>latest</LangVersion>`
in the csproj template); properties/events propagate accessor
staticness (all-static on the 431/19 absseal ones; mixed would fall
back). Gates: **682 tests (564 portable incl. 6 new in
`tests/test_review113_type_decls.py` + 118 game); direct sweep 116,178 methods / 0 crashes / 0 structural changes vs
fix 112 (0 bodies changed — emitter-only); strict build 11,181 files
/ 113,938 bodies / 0 failures or fallbacks (`work/review113_out`);
parser 0 bad files**. Reports: `validation_reports/review113_sweep.json`,
`review113_vs112.json` (0 changed, 0 structural),
`review113_parse.json`; built tree `work/review113_out`. The 64
goldens are untouched (0 overlapping MIs; fingerprints refreshed).
NOT promoted — `final_out/` still holds the fix-99 tree pending a
human promotion call.

- [x] Fix 113: 2,001 files changed — exactly 1,015 `static`,
  636 `interface`, 615 `delegate` headers (census-exact), plus
  modifier-stripped members; 3 orphaned `__SharedBodyStubs.cs`
  dropped (delegate-suppressed bodies took the only refs).
- [x] Recompile probe: **87,224 → 68,528 instances, 5,461 → 4,097
  files; CS1721/CS0527/CS0418/CS0644/CS1722/CS0708 all go to
  exactly zero** (CS0708 needed the property/event staticness
  follow-through: 900 → 0). ZipEntry.cs (12 delegate-shape errors
  after fix 112) is fully clean.
- [x] Residue is the next program: missing types (CS0246 20.7k:
  usings, nested qualification, open generics, absent types),
  bodiless methods (CS0501 15.1k), unsafe modifiers (CS0214 7.3k),
  unimplemented members (CS0534 7.1k), overrides (CS0533/CS0535),
  ctors (CS1520), overload collisions, ref/out ABI — then the
  unmasked body layer (gotos, definite assignment).

## Previous work — fix 112 (fresh-array bracket repair, gated 2026-09-18)

`new T[N][i]` parses as an invalid rank specifier and
`new T[N](idx)[0]` (single argument, ldelema shape) as an invalid
call (the last 2 parse-failing files). `_fresh_array_brackets`
(new dec text pass) parenthesizes the creation — `(new T[N])[i]`,
`(new T[N])[idx]` — meaning-preserving everywhere (allocation,
size, and index survive verbatim; verified parsing with Roslyn).
Multi-arg calls, bare calls without a deref, and unbalanced spans
decline. Gates: **676 tests (558 portable incl. 8 new in
`tests/test_review112_array_brackets.py` + 118 game); direct sweep
116,178 methods / 0 crashes / 0 structural changes vs fix 111 (181
bodies changed, all line-neutral); strict build 11,184 files /
115,658 bodies / 0 failures or fallbacks (`work/review112_out`);
parser 0 bad files**. Reports: `validation_reports/review112_sweep.json`,
`review112_vs111.json` (181 changed, 0 structural),
`review112_parse.json`; built tree `work/review112_out`. The 64
goldens are untouched (0 overlapping MIs; fingerprints refreshed
with fix 113's). Provenance: 709/709 paired paren insertions, zero
other diff lines. SqlDecimal.cs fully clean; ZipEntry.cs left 12
delegate-shape errors for fix 113 (which cleared them).

## Previous work — fix 111 (C# keyword escaping, gated 2026-09-18)

The Roslyn whole-tree compile probe (new methodology: `dotnet
build` over all 11,184 files as one project, `__SharedBodyStubs`
deduplicated probe-only) showed 10,778 errors collapsing to root
breaks in just 48 files — 44 of them one class: reserved words as
identifiers (`.namespace` ×194, `.in` ×5, `.interface` ×3, field
`string interface`), which tree-sitter parses but Roslyn rejects
(CS1001 + cascades). The fix routes every metadata-name declaration
(type headers, enum members, methods incl. explicit-`IFoo.Bar`,
fields, events, ctors, properties) through the existing
`safe_ident` (trailing-underscore convention, already used for
params), and adds `_escape_keywords` (dec text pass after the stub
casts): a reserved word after `.`/`->` is never a keyword use, so
masked-line rewriting is exact; strings/comments never match and
already-escaped names never re-match. `nameof()` emission tracks the
escaped spelling. Metadata census: 6 keyword fields, 1,283
keyword params (all `object`/`method`-style delegate plumbing,
already consistent), zero keyword typedefs/methods/namespaces.
Gates: **668 tests (550 portable incl. 6 new in
`tests/test_review111_keywords.py` + 118 game); direct sweep
116,178 methods / 0 crashes / 0 structural changes vs fix 110 (81
bodies changed, all line-neutral); strict build 11,184 files /
115,658 bodies / 0 failures or fallbacks (`work/review111_out`);
parser 0 bad files**. Reports: `validation_reports/review111_sweep.json`,
`review111_vs110.json` (81 changed, 0 structural),
`review111_parse.json`; built tree `work/review111_out`. The 64
goldens are untouched (0 overlapping MIs, no regen needed). NOT
promoted — `final_out/` still holds the fix-99 tree pending a human
promotion call.

- [x] Fix 111: residual `(\.|->)keyword` census is ZERO tree-wide
  (masked scan, 11,184 files); decl/uses agree exactly
  (`private bool async;` + all 8 `this.async_` uses verified in
  FileStream.cs).
- [x] Recompile probe: **10,778 → 40 error instances, 48 → 2
  files**. Everything keyword-related is gone; the survivors are
  the `new X[N](args)` / `new X[N][i]` mistranslation family
  (ZipEntry.cs, SqlDecimal.cs) — fix 112.
- [x] Also proven by probe: into-block `goto` is CS0159-hard-illegal
  (labels are block-scoped for goto; fails with no decls and into
  `try` alike) — no cleverness at the goto level, only
  tail-duplication/hoisting work counts toward compilation.

### Next priorities (fix 111 follow-ups)

1. **Fix 112: `new X[N][i]` 2D-index mistranslation** (751 lines,
   e.g. `new char[1][0x0] = 32`) **and `new X[N](args)`**
   indirect-call misrender (30 lines). Precise lifter shapes.
2. **Semantic layer** (surfaced by the probe once parse falls):
   definite assignment, conversions, duplicate locals — measure
   after fix 112; the goto program (8,071 sites) feeds
   CS0165-class errors.
3. **Project wiring**: per-assembly `.csproj` files exist but
   carry no cross-assembly references (the probe sidestepped this
   with one project).
4. Receiver-driven instance twins, call/indexer `==` operands,
   duplication residue, 447 shared tails — all stand.

## Previous work — fix 110 (unanimous == / != shared calls fold to operators, gated 2026-09-18)

Six shared addresses (~2,726 uses) carry only static 2-parameter bool
`op_Equality` candidates (`Equals` twins allowed) or unanimous
`op_Inequality` (census: `0x181af7520` String 2,282,
`0x18061a510` 17-cand != 201, plus four small ones; the 252-cand
mixed `0x1807ee180` and 1,806-cand `0x18063ac90` decline by
non-unanimity). Address-sharing proves one machine code, so the
operator spelling is behavior-exact with no owner attribution — but
each operand must still prove the exact same operand type for some
candidate, or `a == b` could bind a different overload (notably
`object.==`/ReferenceEquals for object-typed temps). `_eq_addr_info`
(new in `il2cpp/dec/highlevel.py`, cached) proves unanimity (all
`method` candidates, static, 2 params, bool return, GPR-safe param
kinds per matched pair — floats ride XMM, structs carry ABI risk);
`_eq_operand_spelling` proves operand types (string/int literals,
uniquely-declared temps via `_stub_assign_types`, `this`/temp/
`typeof` member paths through metadata fields with
instance/static/literal discipline); `_shared_equality_ops` (wired
between the fence pass and the stub casts, so no `(bool)` cast is
ever synthesized for a rewritten site) folds proven-bool positions
only (whole if/while/do-while tests, top-level &&/|| operands,
`!`-chains, `bool` decl RHS, bool returns; ternary arms, call
arguments, bare statements, and non-bool decls decline). Integer
literals self-type by C# literal rules. Along the way the legacy
bare-`typeof(` check was found to also match `typeof(X).Get()`
(zero corpus sites, closed with `_fence_bare_typeof` in fix 109).
Gates: **662 tests (544 portable incl. ~29 new in
`tests/test_review110_equality_ops.py` + 118 game, 64 goldens
verified live against fixtures); direct sweep 116,178 methods / 0
crashes / 0 structural changes vs fix 109 (312 bodies changed, all
line-neutral); strict build 11,184 files / 115,658 bodies / 0
failures or fallbacks (`work/review110_out`); parser 0 bad files**.
Reports: `validation_reports/review110_sweep.json`,
`review110_vs109.json` (312 changed, 0 structural),
`review110_parse.json`; built tree `work/review110_out`. The 64
goldens were regenerated after individual review of the single
overlapping diff (mi 15013 `set_columnName`: the `!((bool)sub_…)`
condition becomes `this.m_ColumnName != value` — private string
field plus setter string param, exact). NOT promoted — `final_out/`
still holds the fix-99 tree pending a human promotion call.

- [x] Fix 110: ~846 new `==`/`!=` lines (per-method normalized
  multiset audit: the ONLY added lines tree-wide are operators plus
  3 `using System.Threading;`; every removed line is a
  shared-equality call, a dead copy/decl cascade, a dropped stub
  entry, or brace realignment). Ground truth: 3-level field paths
  rewrite (`this.playerInput.m_CurrentActionMap.m_Name ==
  "Interrogation"`) while property twins stay
  (`this.playerInput.currentControlScheme` — getters are calls).
- [x] Residue, all verified declined by design: property/call/
  indexer operands (expression typing open), object-vs-string mixed
  pairs (would bind ReferenceEquals), non-bool positions,
  `0x180434690`-class unregistered dispatch blobs (8,046 uses —
  decoded: jmp thunk onto an unregistered virtual-dispatch
  routine; `0x180002210/380` are interface search loops into the
  `0x18043DC60` slow path — no honest name exists for any of
  them, shapes recorded, `sub_` rendering stays).
- [x] Bugs found by tests while building: an operator-precedence
  slip in the region guard, a trim-based operand matcher that ate
  the call's own close paren, an unreachable typeof branch, and a
  head-gate rejecting `!`/parens before the operand path ran.

### Next priorities (fix 110 follow-ups)

1. **Call/indexer operands for ==** (`ToLower()`,
   `playerIds[i]`): needs expression return-type/element-type
   proof — the general expression-typing problem (fix-105 item 1).
2. **Receiver-driven instance twins** (`TaskAwaiter.GetResult`
   vs `ConfiguredTaskAwaiter.GetResult`, 529 uses; 367
   multi-owner-instance addresses, 3,579 uses): exact receiver
   type proof at lifter level, never a guess.
3. **Unregistered dispatch blobs** (above): naming needs a
   registered/exported identity that does not exist; revisit only
   with new ground truth.
4. **Duplication residue** (~2.7k both-sides-unknown branches),
   **447 remaining shared tails**, **8,067 into-block gotos**,
   Review 87 lists — all stand.

## Previous work — fix 109 (single-level typeof-member fence args, gated 2026-09-18)

Of 151 remaining fence sites, 127 have only plain or
`typeof(X).Member` arguments (census over the fix-108 tree: all 140
typeof-member args are single-level static accesses on hot framework
types — Encoding, TraceInternal, Socket, Uri, Xml*, RegistryKey…).
`_fence_trivial_arg` (in `il2cpp/dec/highlevel.py`) now accepts
exactly `typeof(X).Member` via `_fence_typeof_member` (balanced-paren
scan in `_fence_typeof_end`, one dotted name, checked on masked text
so quoted text can never shape-match). Soundness: no null dereference
is possible (static access only — strictly fewer load effects than
the already-shipped `obj.f` chains), no calls/indexers/further
levels; the tempering precedent is fix 72d's `_PURE_LOAD_RX`, which
already defines typeof-member chains as pure loads for DCE (fix 109
stays on the conservative single-level subset: zero multi-level sites
observed). Along the way the legacy bare-`typeof(`-prefix check was
tightened to whole-string balanced (`_fence_bare_typeof`): it also
matched `typeof(X).Get()`, silently dropping a call (zero corpus
sites ever matched that shape — verified over the pre-fence tree —
but the hole was real; regression-tested). Gates: **639 tests (521
portable incl. 16 new in `tests/test_review109_typeof_args.py` — one
fix-107 expectation corrected for the tightened check — + 118 game);
direct sweep 116,178 methods / 0 crashes / 0 structural changes vs
fix 108 (76 bodies changed, net -335 lines); strict build 11,184
files / 115,658 bodies / 0 failures or fallbacks
(`work/review109_out`); parser 0 bad files**. Reports:
`validation_reports/review109_sweep.json`,
`review109_vs108.json` (76 changed, 0 structural),
`review109_parse.json`; built tree `work/review109_out`. The 64
goldens are untouched (0 overlapping MIs, no regen needed). NOT
promoted — `final_out/` still holds the fix-99 tree pending a human
promotion call.

- [x] Fix 109: ~131 new `Thread.MemoryBarrier()` lines (per-method
  normalized multiset audit: the ONLY added lines tree-wide are
  barriers + 3 `using System.Threading;`; every removed line is a
  fence decl, a dead copy/decl cascade, a dropped
  `0x1804355f0` stub entry, a pure-load decl
  (`getClass()`/`typeof`, per `_PURE_LOAD_RX` doctrine), or brace
  realignment). `sub_1804355f0` falls 159 → 25 lines.
- [x] Residue, all verified declined by design (17 decls + 8 stub
  defs): pointer arithmetic/deref (`(p + 0x88)`,
  `((byte*)obj7 + 0x0)[0]` — 9 sites), integer arithmetic
  (`*`, `>>`, `+` — 5 sites; temp-name typing is not purity
  proof), call args (`obj.getClass()` — pure per doctrine but
  call-shaped; needs a `_PURE_LOAD_RX`-consistent arg rule),
  live-temp plain/zero-arg sites.

### Next priorities (fix 109 follow-ups)

1. **Call-shaped pure args** (`obj.getClass()` and friends):
   align `_fence_trivial_arg` with `_PURE_LOAD_RX` (member chains,
   no calls/Indexers) — the doctrine already exists, needs its own
   gate.
2. **Other top unregistered VAs** (thunk finals,
   interface-dispatch twins from the fix-104 list): native
   structural proof on the fence precedent, never a name guess.
3. **Duplication residue with degraded conditions** (~2.7k
   both-sides-unknown branches, fix-106 list), **447 remaining
   shared tails**, **8,067 into-block gotos**, Review 87 lists —
   all stand.

## Previous work — fix 108 (scope-aware deadness for fence-called temps, gated 2026-09-17)

Fix 107's method-wide liveness treated every same-name mention as a
read, so one colliding scratch temp (sibling scopes re-declare: fix
97c) pinned all of them. `_fence_temp_dead_scoped` (new in
`il2cpp/dec/highlevel.py`, OR-ed with the fix-107 check so nothing it
rewrote can regress) walks forward from the fence declaration at brace
depth d0 over masked lines: a same-block `T nm = ...` rebinds the temp
away outright, a nested declaration or foreach/catch binder shadows its
subtree (depths from `_fence_line_depths`, pruned as blocks close),
outer-scope declarations are different variables, and outer mentions,
unplaceable brace-mixed mentions, initializers reading an outer `nm`,
and any depth anomaly decline exactly as before. `_fence_redecl_of`
reuses `_STUB_DECL_RX` (with the `_STUB_KEYWORDS` guard, so
`return x = ...` never counts) plus the foreach/catch binder regexes.
Gates: **633 tests (515 portable incl. 15 new — 14 in
`tests/test_review108_scoped_fence.py`, one split out of the flipped
fix-107 dup-temp expectation — + 118 game); direct sweep 116,178
methods / 0 crashes / 0 structural changes vs fix 107 (8 bodies
changed, net -96 lines); strict build 11,184 files / 115,658 bodies /
0 failures or fallbacks (`work/review108_out`); parser 0 bad files**.
Reports: `validation_reports/review108_sweep.json`,
`review108_vs107.json` (8 changed, 0 structural),
`review108_parse.json`; built tree `work/review108_out`. The 64
goldens are untouched (0 overlapping MIs, no regen needed). NOT
promoted — `final_out/` still holds the fix-99 tree pending a human
promotion call.

- [x] Fix 108: 23 new `Thread.MemoryBarrier()` lines;
  `sub_1804355f0` falls 185 → 159 lines (8 stub defs + 151 decls
  remain). Of 8 changed methods 6 are line-neutral, 2 shrink
  (`Task.Dispose` -13, `ReaderWriterLockSlim.
  TryEnterUpgradeableReadLockCore` -83) through the same honest DCE
  cascade as fix 107 (orphaned copy chains, one `using static`
  per newly-unreferenced assembly). Ground truth: the
  `FusionNetworkManager` colliding-`obj13` sites rewrite; the
  `ReaderWriterLockSlim` `if`-arm fence rewrites while its
  genuinely-live `else`-arm twin stays.
- [x] Refinement found by probe (single-method re-lift of mi
  103865): an outer-scope re-declaration is a different variable and
  no longer declines the site; decided by reading all five `obj84`
  decls' fates, with a dedicated regression test.
- [x] Residue, all verified declined by design: genuinely-read
  temps, effectful-argument sites (out of scope — the pass never
  touched argument rules), `using`-var/`is`-pattern rebinds,
  mid-line-brace placements.

### Next priorities (fix 108 follow-ups)

1. **Effectful-argument fence sites** (`sub_1804355f0(Foo(), ...)`
   with dead temps): needs call-effect analysis, never blind
   dropping.
2. **Other top unregistered VAs** (thunk finals,
   interface-dispatch twins from the fix-104 list): native
   structural proof on the fence precedent, never a name guess.
3. **Duplication residue with degraded conditions** (~2.7k
   both-sides-unknown branches, fix-106 list), **447 remaining
   shared tails**, **8,067 into-block gotos**, Review 87 lists —
   all stand.

## Previous work — fix 107 (proved fence-thunk calls render Thread.MemoryBarrier(), gated 2026-09-17)

`lock or dword ptr [rsp],0; ret` is the full barrier MSVC emits where the
source calls `Thread.MemoryBarrier`, reached directly or through a short
`jmp` thunk (`0x1804355f0`, the fix-104 follow-up membarrier suspect —
1,465 sites). `_is_fence_body` (new in `il2cpp/lifter/state.py`) proves
exactly that shape: locked `OR`, RSP base, zero displacement, dword
width, zero immediate (both `0x83` and `0x81` encodings), `ret`
terminating the extent; registered/exported/non-exec/unreadable targets
decline. `_fence_target` follows the thunk (itself or <=3 jmp hops),
memoized, never a hardcoded address. `_fence_void_calls` (new in
`il2cpp/dec/highlevel.py`, wired in `il2cpp/dec/structure.py` after the
delegate fold, before the stub casts) rewrites only positions that need
no value: bare statements, void `; return;` tails (split in two), and
declarations whose temp is dead method-wide. Every argument must be
side-effect-free (plain temps/fields, literals, typeof, strings);
conditions, value returns, live temps, and `Thread.MemoryBarrier` itself
keep today's rendering. Gates: **618 tests (500 portable incl. 12 new
in `tests/test_review107_fence_calls.py` + 118 game); direct sweep
116,178 methods / 0 crashes / 0 structural changes vs fix 106b (544
bodies changed, net -2,202 lines); strict build 11,184 files / 115,658
bodies / 0 failures or fallbacks (`work/review107_out`); parser 0 bad
files**. Reports: `validation_reports/review107_sweep.json`,
`review107_vs106b.json` (544 changed, 0 structural),
`review107_parse.json`; built tree `work/review107_out`. The 64
goldens are untouched (0 overlapping MIs, no regen needed). NOT
promoted — `final_out/` still holds the fix-99 tree pending a human
promotion call.

- [x] Fix 107: 1,279 `Thread.MemoryBarrier()` lines (3 pre-existing
  resolved calls + 1,276 rewrites); `sub_1804355f0` falls 1,465 → 185
  lines. Of 544 changed methods 386 are line-neutral, 157 shrink
  (dead-decl plus the honest DCE cascade its orphaned copies allow),
  1 grows by design (bare `...; return;` splits in two:
  `Socket.Connect`). Ground truth: `Thread.MemoryBarrier`'s own body
  (RVA 0x1D1F380) is one call to `0x1804429c0` and is deliberately NOT
  rewritten (self-guard); `Fusion.AtomicInt`'s seven members drop
  their dead `object objN = sub_1804355f0(...)` decls and the
  now-unused `using static __SharedBodyStubs;`.
- [x] Residue, all verified declined by design: 174 decls whose temp
  is live or textually collides with a reused scratch temp later in
  the method (safe-miss direction — e.g. `FusionNetworkManager`
  `obj13` reused as `_StartGame_d__58`), 9 `__SharedBodyStubs`
  definitions that must stay, effectful-arg and value-position sites.
- [x] into_block gotos identical 8,071 (both sweeps), parse re-gated
  on the built tree.

### Next priorities (fix 107 follow-ups)

1. **Remaining `sub_1804355f0` residue above** (live-temp value
   positions): needs value-proof the fence returns nothing at the
   call site, never deletion of a live temp.
2. **Other top unregistered VAs** (thunk finals, interface-dispatch
   twins from the fix-104 list): each needs native structural proof
   on the sqrt-wrapper/fence precedent, never a name guess.
3. **Duplication residue with degraded conditions** (~2.7k
   both-sides-unknown branches, fix-106 list), **one-side-unknown
   comparisons** (~700+), **447 remaining shared tails**, **8,067
   into-block gotos**, Review 87 lists — all stand.

## Previous work — fix 106 (parity-jump NaN fold drops literal arms, gated 2026-09-16)

`ucomiss` + `jp` rendered `IsNaN(a) || IsNaN(b)` even when one side is
a constant (`IsNaN(0f)` — provably false, 665 sites). No numeric
literal spelling denotes NaN, so `_is_non_nan_literal` (new in
`il2cpp/x64.py`, reusing `_int_lit` plus finite-float parsing) drops
such arms in `flag_cond`; the `x != x` idiom and unknown/nullary
operands are untouched, and all-constant pairs decline as before.
Gates: **606 tests (598 + 8 new in
`tests/test_review106_float_parity.py`); direct sweep 116,178 methods
/ 0 crashes / 0 structural changes vs fix 105 (294 bodies changed);
strict build 11,184 files / 115,658 bodies / 0 failures or fallbacks
(`work/review106_out`); parser 0 bad files**. Reports:
`validation_reports/review106_sweep.json`, `review106_vs105.json`
(294 changed, 0 structural), `review106_parse.json`; built tree
`work/review106_out`. The 64 goldens were regenerated after individual
review of the single diff (`DateTimeConverter.ConvertTo`, double
width). NOT promoted — `final_out/` still holds the fix-99 tree
pending a human promotion call.

- [x] Fix 106: 665 literal arms dropped in 144 files (full tree
  audit, 0 unexplained). The single flagged hunk hand-verified
  correct: the arm was a literal at lift time, bound to a temp only
  later (`object obj1 = 1.79…e+308d` feeding a `comisd`).
  `IsNaN(<const>)` falls 665 → 0 (4,968 live-value arms remain).
- [x] Fix 106b: first-char guard (an `inf`-spelled identifier can
  never be taken for a literal). Zero-diff proof on this corpus:
  direct sweep 0/116,178 changed vs fix 106, rebuilt tree
  byte-identical across all 11,184 files (`work/review106b_out`),
  parse re-gated. Reports: `review106b_sweep.json`,
  `review106b_vs106.json`, `review106b_parse.json`.
- [x] Ground truth: `AudioVolumeSliders.SetMusicVolumeInternal` —
  native `ucomiss; jp; jne` to one target; the `IsNaN(0f)` arm is
  gone (the surviving `unknown != unknown` duplication residue is a
  separate structuring matter, below).

### Next priorities (fix 106 follow-ups)

1. **Duplication residue with degraded conditions** (~2.7k
   both-sides-unknown branches with sibling-identical bodies, e.g.
   `else if (unknown != unknown)`): needs _seq/fold-level proof
   (never delete — an unprovable condition can't lose its arm).
2. **One-side-unknown comparisons** (~700+), unbound decls/arithmetic
   (`object obj17 = unknown;`), **honest names** for the top
   unregistered VAs (thunk finals, membarrier, interface-dispatch
   twins), **447 remaining shared tails**, **8,067 into-block gotos**,
   Review 87 lists — all stand.

## Previous work — fix 105 (ternary-condition casts, arm leniency, do-while, gated 2026-09-16)

Same caller-proven rule, one level deeper: a sub_ call in a ternary
CONDITION proves `bool` there (arms keep the line's type), arms without
calls pass through instead of vetoing the line, and `} while (...)`
proves `bool` like `if`/`while`. `== null`, `&&`/`||`, arithmetic and
call-nested conditions still decline whole-line, correctly. Gates:
**598 tests (22-case stub file extended: ternary conds, arm leniency,
do-while); direct sweep 116,178 methods / 0 crashes / 0 structural
changes vs fix 104 (47 bodies changed); strict build 11,184 files /
115,658 bodies / 0 failures or fallbacks (`work/review105_out`);
parser 0 bad files**. Reports: `validation_reports/review105_sweep.json`,
`review105_vs104.json` (47 changed, 0 structural),
`review105_parse.json`; built tree `work/review105_out`. The 64
goldens are untouched (0 overlapping MIs, no regen needed). NOT
promoted — `final_out/` still holds the fix-99 tree pending a human
promotion call.

- [x] Fix 105: 59 cast lines in 42 files, every one a cast-only swap
  at identical indent, 0 suspicious casts (full tree audit).
  Ground truth: `string text4 = (bool)sub_Equals(...) ?
  string.Format(...) : ...`, `float real22 = !((bool)sub_...(304)) ?
  ...`, `Object object1 = (bool)sub_...(type5, ...) ? ... : ...`.
- [x] Returns proven COMPLETE: all 99 bare `return sub_` lines sit in
  void/object methods (pointer returns excluded by design); the 12
  apparent counterexamples were property/nested-class misattributions
  in the audit scaffolding, each verified by hand.

### Next priorities (fix 105 follow-ups)

1. **Operator-nested bool positions** (`&&`/`||` operands,
   `== <lit>` with numeric proof, ternary-in-ternary conds):
   needs per-operator expression typing.
2. **Byref/pointer arguments** into stubs (`&` address-of, `void*`
   params); **honest names** for the top unregistered VAs (thunk
   finals, membarrier, interface-dispatch twins); **447 remaining
   shared tails** (10 via the `this`-rule), **8,067 into-block
   gotos**, Review 87 noreturn-EH/leftover lists — all stand.

## Previous work — fix 104 (object stubs for unresolved sub_ + caller casts, gated 2026-09-16)

53,984 `sub_X(...)` references pointed at methods declared nowhere
(2,687 distinct VAs, 0 definitions tree-wide). The emitter now writes
one global `__SharedBodyStubs` class per assembly (`internal static
object sub_X(params object[] args)`, throwing, with per-VA owner
comments) plus `using static __SharedBodyStubs;` per referencing file,
and a late dec pass (`_shared_stub_casts` in `il2cpp/dec/highlevel.py`,
after the delegate fold) inserts caller-proven `(T)` casts: decl TYPE
(83% of sites), whole-condition `bool`, method return (`void` splits
to call-then-return), unique-mapped plain assigns. Only direct value
positions rewrite (root, ternary arms with sub_-free conditions,
`!`-chains, one paren layer); nested args keep the object spelling;
real metadata `sub_<hex>` names never stub or cast. Gates: **598
tests (576 + 22 new in `tests/test_review104_shared_stubs.py`; 4
review83 spellings updated, behaviors intact); direct sweep 116,178
methods / 0 crashes / 0 structural changes vs fix 103 (7,096 bodies
changed); strict build 11,184 files (11,107 + 77 stub files) /
115,658 bodies / 0 failures or fallbacks (`work/review104_out`);
parser 0 bad files**. Reports: `validation_reports/review104_sweep.json`,
`review104_vs103.json` (7,096 changed, 0 structural),
`review104_parse.json`; built tree `work/review104_out`. The 64
goldens were regenerated after individual review of all 5 diffs (each
exactly a caller-proven cast). NOT promoted — `final_out/` still holds
the fix-99 tree pending a human promotion call.

- [x] Fix 104: 12,716 cast lines (8,584 decl + 1,319 return + 2,544
  conditions + 269 assigns), every cast type proven against its own
  line/method/metadata (decl casts equal their decl, conditions are
  `(bool)`, returns match file signatures and metadata sharer sets,
  assigns match unique decl maps); 3,627 usings; 77 stub files;
  0 void splits left (fix 95 owned them), 0 unexplained hunks.
  Hardening along the way: `\x01` mask alphabet for comments (104c),
  string-aware balanced spans, chained-assign shape proven
  unmatchable so its guards were removed (104e).
- [x] Residue, all verified declined by design: `&`/pointer args
  (~9k, need byref recovery — the method now resolves, the argument
  still doesn't), nested-expression positions (~2.6k conditions with
  calls under operators, `is`/`as`, `??`), untyped sources.
- [x] Next honest-naming targets identified (not attempted): the top
  unregistered VAs are analyzable natives — `0x180434690` (8,046
  uses) is a `jmp` thunk onto `0x180479F80`, `0x1804355f0` (1,449) a
  thunk onto a `lock or [rsp],0` memory barrier, `0x180002210` /
  `0x180002380` (~5,700) near-identical interface-dispatch search
  loops, plus `0x18043dc60`, `0x18043e360`, `0x1804346a0`. Each needs
  native structural proof (sqrt-wrapper precedent), never a name
  guess. A generic `<T>` stub was rejected (C# never infers from
  return position); casts express caller-side need and stay valid if
  a VA later resolves honestly.

### Next priorities (fix 104 follow-ups)

1. **Condition/nested-expression casts** (`&&`/`||` operands,
   `== <lit>` comparisons, ternary conditions, `is`/`as` left alone
   correctly): needs expression-type analysis per operator.
2. **Byref/pointer arguments** into stubs; **honest names** for the
   top unregistered VAs above; **447 remaining shared tails** (10 via
   the `this`-rule), **8,067 into-block gotos**, Review 87
   noreturn-EH/leftover lists — all stand.

## Previous work — fix 103 (native-width INDEXED raw-store lvalues, gated 2026-09-16)

Same display-only rule as fix 102, extended to the indexed raw branch
(`base + idx*scale + disp`): the index/scale pair is recorded in
`_mem_lvalue` and the display mirrors the raw branch's own `_term_up`
construction exactly, so output is identical modulo the cast
(verified `_unsafify` fixpoints, incl. composite and byte*-read
indices). Gates: **576 tests (571 + 5 new indexed cases in
`tests/test_review102_raw_store_widths.py`); direct sweep 116,178
methods / 0 crashes / 0 structural changes vs fix 102 (478 bodies
changed); strict build 11,107 files / 115,658 bodies / 0 failures or
fallbacks (`work/review103_out`); parser 0 bad files**. Reports:
`validation_reports/review103_sweep.json`, `review103_vs102.json`
(478 changed, 0 structural), `review103_parse.json`; built tree
`work/review103_out`. The 64 goldens were regenerated after individual
review of the single diff (`ViscosityVorticityJob.Execute`: indexed
`inc dword` RMW → `int*`; its untyped `mov`-triple sibling correctly
stays byte*). NOT promoted — `final_out/` still holds the fix-99 tree
pending a human promotion call.

- [x] Fix 103: 1,287 widened lines in 276 files, every one a
  cast-only swap at identical indent (full tree audit, 0 unexplained,
  0 added, 0 dropped). Out-of-range literal stores fall 189 → 118;
  byte* stores overall 3,579 → 3,205.
- [x] Residue after fix 103 (each verified declined by design):
  untyped register sources (add-expr `READ + 1` with unknown type),
  `__static_fields` blobs, reference/array/`new` RHS, wide source in
  narrow store, width-1 stores of non-byte values (unencodable
  natively — the value proves a wider write elsewhere).

### Next priorities (fix 103 follow-ups)

1. **Untyped register sources** (expression-typed `READ op LIT`
   values): needs expression type inference, not spelling guesses.
2. **Wide-source-in-narrow-store** and **reference stores through raw
   pointers**: both need field-type recovery.
3. **447 remaining shared tails** (receiver `this`-rule scoped at 10
   `MemberwiseClone` sites), **8,067 into-block gotos**, Review 87
   noreturn-EH/leftover lists — all stand.

## Previous work — fix 102 (native-width raw-store lvalues, gated 2026-09-16)

A raw `*(base + disp)` store lvalue rendered `((byte*)base + disp)[0]`,
which fails to compile whenever the stored value is not a byte (1,524
out-of-range literals tree-wide, plus mistyped variables). The native
width is ground truth from the store instruction, so the statement now
spells a same-width cast (`_wide_src_cast`/`_wide_rmw_cast` +
`_wide_store_disp`/`_wide_rmw_disp` in `il2cpp/lifter/insn.py`, parts
recorded in `_mem_lvalue`). Only the emitted statement spells the
width — kills, slots, barriers and twin dedup keep the raw text; the
barrier twin still renders raw, bridged by `_canon_wide_cast` in
`_norm_twin` (`il2cpp/text.py`); the `unsafe` detector covers all
pointer casts (`il2cpp/dec/textpass.py`). Gates: **571 tests (544 + 27
new in `tests/test_review102_raw_store_widths.py`, incl. end-to-end
`_write_mem`/`_rmw_mem` and an updated packed-lane spelling in
`tests/test_game_review81.py`); direct sweep 116,178 methods / 0
crashes / 0 structural changes vs fix 101 (9,269 bodies changed);
strict build 11,107 files / 115,658 bodies / 0 failures or fallbacks
(`work/review102_out`); parser 0 bad files**. Reports:
`validation_reports/review102_sweep.json`, `review102_vs101.json`
(9,269 changed, 0 structural), `review102_parse.json`; built tree
`work/review102_out`. The 64 goldens were regenerated after individual
review of all 4 diffs (each exactly a width improvement:
`GetChars`, `Rpc_CMD_Heal`, `uint3x3.op_Explicit`, `Finalize`).
NOT promoted — `final_out/` still holds the fix-99 tree pending a
human promotion call.

- [x] Fix 102: integer literals pick signedness by fit (signed first),
  float literals keep their suffixed width (`f`→float, `d`/bare→
  double; fix 102b), register sources are accepted only when the
  source type's size equals the native width so every rendered byte is
  value-determined (a narrower source would leave upper bytes
  unexplained — e.g. a long in a dword store stays honest). RMW keeps
  result unity (`int`/`long`/`uint`/`ulong`/`float`/`double` only,
  width 4/8). Declines on unknown/reference/enum/bool sources,
  indexed stores, `__static_fields` blobs (19 sites, all compiling —
  keeps the sfblob twin machinery byte-identical), and un fitting
  values/widths.
- [x] Fix 102c: `_field_expr`'s miss over a dotted base returned the
  raw text through the field branch, bypassing width recording
  (`this.ropeRenderer + 0x54`, `this.heap[0x0] + 0x22`, ...). The
  exact-passthrough spelling now records the identical parts at true
  instruction width; returned text is byte-identical either way.
- [x] Provenance verified on the built trees (11,107 files, inventory
  identical): 25,765 widened lines in 1,820 files, every one a
  cast-only swap at identical indent; +1 honest line (`Decimal.Abs`:
  a 16-byte struct copy plus a dword flags fixup previously
  accidentally deduped to one line — verified against native);
  3 honest ternary unfolds (one arm widened while a genuinely
  different-width sibling arm stayed byte* — merging them would be the
  bug); 0 unexplained changes. Out-of-range literal stores fall
  1,524 → 189 (residue: indexed fills, untyped registers,
  wide-in-narrow, `__static_fields` — each verified declined by
  design, modulo comparison/indexed census false positives).
- [x] Ground truth: `mov dword [rbx],0FFFFFFFEh` → `((uint*)num1 +
  0x0)[0] = 4294967294;`, `movss` float lanes → `((float*)obj4 +
  0x4)[0] = ...` (review81 proof intact: 4 Sqrt, no helper, no
  unknown), `mov word [x],0FFFFh` → `((ushort*)...)[0] = 65535;` —
  full cases in the test file.

### Next priorities (fix 102 follow-ups)

1. **Indexed raw stores** (`base + idx*scale + disp`, e.g. float-1.0
   array fills): same helper extends naturally, needs its own gate.
2. **Untyped register sources** (`void*` params, untyped slots) and
   **wide-source-in-narrow-store** (long into dword field): both need
   field-type recovery, not spelling guesses.
3. **Reference/array/`new` RHS** through raw pointers: barrier and
   field-recovery territory, never a pointer cast.
4. **447 remaining shared tails** (fix 100 list stands — receiver
   `this`-rule scoped at 10 `MemberwiseClone` sites), **8,067
   into-block gotos**, Review 87 noreturn-EH/leftover lists — all
   stand.

## Previous work — fix 101 (bare-param declaration hints close over `new` RHS, gated 2026-09-16)

A tracked hint that is one bare VAR/MVAR (`T`, `T1`, `TValue` —
top-level 0x13/0x1e with a matching spelling, openness proved
structurally by `_type_has_var`) names no type at all, while the same
line's `new ObiPinConstraintsBatch()` / `new List<int>()` is the exact
closed allocation identity (`_bare_closed_new_type` +
`_bare_new_rhs_type` in `il2cpp/dec/highlevel.py`, wired into
`_decl_type_of` after the fix-98 same-base path). `T x = new C(...)`
never compiles under any binding of `T`, so no compiling method can
regress. Gates: **544 tests (526 + 18 new in
`tests/test_review101_bare_t_decls.py`); direct sweep 116,178 methods /
0 crashes / 0 structural changes vs fix 100 (234 bodies changed, all
line-neutral); strict build 11,107 files / 115,658 bodies / 0 failures
or fallbacks (`work/review101_out`); parser 0 bad files**. Reports:
`validation_reports/review101_sweep.json`, `review101_vs100.json` (234
changed, 0 structural), `review101_parse.json`; built tree
`work/review101_out`. The 64 goldens are untouched (0 overlapping MIs,
no regen needed). NOT promoted — `final_out/` still holds the fix-99
tree pending a human promotion call.

- [x] Fix 101: bare-param hints take the RHS `new` spelling — non-generic
  (`T value1 = new ObiPinConstraintsBatch()`), generic over bare
  (`T value1 = new List<int>()` via the fix-98 path,
  `TValue value1 = new List<GameObject>()`), and qualified
  (`T value1 = new TMPro.KerningPair()` — only the last dotted
  component decides openness, fix-98 invariant; fix 101b). Declines on
  non-bare tuples, non-bare spellings, unreadable openness, open
  generic RHS (`new List<TKey>()`), bare `new T()`, non-`new`/array/
  initializer RHS, `<>c__` display-class spellings (normalized only at
  the file boundary, not a valid mid-pipeline decl type), and T-like
  bare targets (`new TMP_Character()`). Never invents a type: the
  spelling comes literally from the emitted RHS.
- [x] Provenance verified old-vs-new on all 234 changed bodies:
  line-count-identical everywhere; every diff line is a bare-`T`
  declaration-type change (463) or a consistent rename projection of
  one (319 binder renames incl. `foreach` binders, 1,475 use-site
  renames, 0 failures, 0 conflicts, 0 collisions). Every new decl type
  matches its own line's `new` target literally (the one apparent
  mismatch is a whitespace-only audit artifact:
  `List<byte[]>` vs `new List<byte[]>()`).
- [x] Residue: 8 bare-`T`-over-`new` sites in 5 files, both families
  declined by design — 4× `T1 t11 = new __c__DisplayClassN_0()`
  (mid-pipeline `<>c__` spelling; closing needs an emitter-coupled
  mangled-spelling proof) and 4× TMP sites
  (`new WeakReference<TMP_FontAsset>`, `new TMP_Character()`,
  `new TMP_SpriteCharacter()`: `TMP_*` collides textually with the
  bare-param regex, so the RHS reads open; closing needs a metadata
  typedef-closedness proof, not a textual one).

### Next priorities (fix 101 follow-ups)

1. **8 residual sites above**: emitter-coupled `<>c__` decl spelling,
   metadata typedef-closedness for T-like concrete RHS names.
2. **447 remaining shared tails** (fix 100 list stands), **8,067
   into-block gotos**, Review 87 byte-store/noreturn-EH/leftover lists
   — all stand.
3. Discovered and NOT changed: `_args_contain_open_param` is purely
   textual, so concrete `TMP_*` types read as open params on the RHS
   (tracked-tuple side is structurally proved and unaffected); the
   `<>c__` → `__c__` file-boundary mangling runs after all decl
   passes.

## Previous work — fix 100 (shared-tail resolution by caller return type, gated 2026-09-16)

A `return <call>` tail delivers the callee's value as the caller's own,
so the true callee's closed, spec-inflated return must equal the
caller's exact metadata return (`_shared_tail_return_target` +
`_tail_sig_key`/`_tail_subst_closed` in `il2cpp/lifter/calls.py`, wired
into both tail-jmp paths in `il2cpp/lifter/insn.py` and
`il2cpp/dec/analyze.py` — the analyze.py mirror is the one that emits
production tails; insn.py covers mid-block jumps). Gates: **526 tests
(509 + 17 new in `tests/test_review100_tail_returns.py`, incl. an
end-to-end `_insn` twin render); direct sweep 116,178 methods / 0
crashes / 0 structural changes vs fix 99 (64 bodies changed, net -212
lines); strict build 11,107 files / 115,658 bodies / 0 failures or
fallbacks (`work/review100_out`); parser 0 bad files**. Reports:
`validation_reports/review100_sweep.json`, `review100_vs99.json` (64
changed, 0 structural), `review100_parse.json`; built tree
`work/review100_out`. The 64 goldens are untouched (0 overlapping MIs,
no regen needed). NOT promoted — `final_out/` still holds the fix-99
tree pending a human promotion call.

- [x] Fix 100: keep nothing on speculation (open/unreadable rows decline
  the whole resolution), drop closed return mismatches, resolve only on
  one distinct rendering. Declines on void callers (fix 95 owns them),
  open/unknown callers, empty/split survivors, open generic definitions,
  and non-method/generic rows. Winners render through the existing
  resolved-tail emitters. Ground truth: `GameServer.GetHSteamPipe`
  (mi 97624) `return sub_18073e050...(GetHSteamPipe(), 0)` becomes
  `return HSteamPipe.op_Explicit(...);`, `Int32.IConvertible.ToInt64`
  (mi 2044) loses 8 lines of guard/phi scaffolding collapsing to
  `return Convert.ToInt64(this.m_value);`, `CloudServices.get_LocalPlayerRef`
  (-12) becomes `return PlayerRef.FromIndex(cloudServices1 >> 32);`,
  `ValueTuple.CombineHashCodes` ×7 (-6 each) become
  `return HashHelpers.Combine(...);`.
- [x] Provenance verified on the built trees: all 13,646 lost
  call-shaped lines are dead `Type V = typeof(X)` (fix-99 audit; the 3
  apparent gains are renumbering artifacts); every added tree line is a
  consistent rename of a surviving live line. Impure-line conservation
  holds modulo locals.
- [x] Residue: `return sub_*shared body` tails fall 511 → 447 (97 → 87
  addresses). Deliberately honest remainder, by family: string
  `Equals`/`op_Equality` (74, behavior-identical twins), `Compare`/
  `CompareTo` (9), `GetHashCode`/`InternalGetHashCode` (15),
  `Clone`/`MemberwiseClone` (10), `get_Module`/`GetRuntimeModule` (8),
  thunk-address pairs whose finals carry no candidates, same-signature
  twins (`GetTexture`/`GetTextureImpl`, surrogate/`IsDigit` pairs),
  and high-count addresses needing receiver instantiation (`List.Add`,
  `Dictionary.get_IsReadOnly`, `Nullable`) or arg-type overload proof
  (`Convert.ToBoolean` short/ushort, `Exchange` long/IntPtr).

### Next priorities (fix 100 follow-ups)

1. **447 remaining tails**: receiver-driven instantiation (same-owner
   generic families), arg-type overload disambiguation, forwarder
   direction via body-call analysis. Never max-arity guesses.
2. **Bare-`T` declaration LHS** (~425 sites), **8,067 into-block gotos**,
   byte-store/noreturn-EH/leftover lists — all stand.
3. Discovered and NOT changed: `_IMPURE` never matches generic calls
   (`Foo<Bar>(...)`), so pre-existing DCE already treats dead generic
   calls as droppable (see fix 99 notes); the analyze.py/insn.py tail
   mirrors must stay in sync — fix 94/100 wire both.

## Previous work — fix 99 (post-render dead-pure-load DCE, gated 2026-09-15)

`_render` drops empty pure-cond `if`s (e.g. an emptied class-init guard
`if (!(k.initialized != 0)) { }`), orphaning the pure klass loads they
alone read — no DCE ran after render, so `System.Type objN = typeof(X)`
survived dead into output and was renamed `Type typeN`. `_structure`
(`il2cpp/dec/structure.py`) now re-runs the proven `_drop_dead_locals`
on the rendered lines: same predicate (pure RHS incl. pure-loads drop,
impure calls stay), later timing. Gates: **509 tests (499 + 10 new in
`tests/test_review99_render_orphans.py`); direct sweep 116,178 methods /
0 crashes / 0 structural changes vs fix 98 (10,062 bodies changed, every
one pure line deletions, net -16,555 lines); strict build 11,107 files /
115,658 bodies / 0 failures or fallbacks (`work/review99_out`); parser 0
bad files**. Reports: `validation_reports/review99_sweep.json`,
`review99_vs98.json` (10,062 changed, 0 structural), `review99_parse.json`;
built tree `work/review99_out`. The 64 goldens were regenerated after
individual review of all 6 diffs (each exactly dead-typeof removals plus
required renumbering cascades). Promoted 2026-09-15: `final_out/` now holds
`work/review99_out` (11,200 files, candidate and promoted aggregate sha256
both `c14263784492b2f209ff695018376404cf0093f06862e1b20e928da89391f2e7`, 0
mismatches; the fix-97e tree is kept at `bckups/final_out_review97e`).
Promotion record: `validation_reports/review99_promotion_verification.json`;
post-promotion parse recheck
`validation_reports/review99_recheck_parse_final.json` (11,107 files, 0
bad).

- [x] Fix 99: one post-render `_drop_dead_locals` call. Ground truth:
  ActorCOMTransform.Update (mi 23898) ships `Type type1 =
  typeof(Object)` whose only reader is the guard `_render` removes;
  KerningTable.AddKerningPair (mi 95457) is untouched.
- [x] Provenance verified on the built trees: all 13,646 lost
  call-shaped lines are `Type V = typeof(X)` (dead pure loads); the 3
  apparent gains are local-renumbering artifacts of the audit's own
  normalizer (verified method-full diffs); every added tree line is a
  consistent rename (`type2` → `type1`) of a surviving live line.
- [x] Residue: dead `Type typeN = typeof(X)` decls fall 12,700 → 10 (the
  10 survivors are kept by `//` line-comment contents seeding liveness —
  over-retention, safe direction). Diagnosed but NOT changed: `_IMPURE`
  (`[\w\]\)]\s*\(`) never matches generic calls (`Foo<Bar>(...)`), so the
  pre-existing DCE already treats dead generic calls as droppable; fix 99
  adds no new unsoundness class (1 such drop corpus-wide:
  `CompileFunctionPointer<...>` in GPUResidentDrawerBurst).

### Next priorities (fix 99 follow-ups)

1. **511 remaining `return sub_*shared body` tails** (fix 94 list stands).
2. **Bare-`T` declaration LHS** (`T value1 = new KerningPair();`, ~425
   sites), **8,067 into-block gotos**, Review 87 byte-store/noreturn-EH
   lists — all stand.
3. **`UnityAction<T0>` LHS is DONE (fix 98); dead-`typeof` LHS is DONE
   (fix 99)** except the 10 comment-pinned survivors above.

## Previous work — fix 98 (open-generic declaration LHS closes over `new` RHS, gated 2026-09-15)

Open-generic tracked hints (`UnityAction<T0>`, `EventCallback<TEventType>`,
`Func<TSource, bool>`, …) now declare with the same line's closed `new`
allocation spelling when the generic definition matches (same short base,
same arity) and the RHS is textually closed. Gates: **499 tests (483 + 16
new in `tests/test_review98_open_generic_decls.py`); direct sweep 116,178
methods / 0 crashes / 0 structural changes vs fix 97e (229 bodies changed,
all line-neutral declaration-only); strict build 11,107 files / 115,658
bodies / 0 failures or fallbacks (`work/review98_out`); parser 0 bad
files**. Reports: `validation_reports/review98_sweep.json`,
`review98_vs97e.json` (229 changed, 0 structural), `review98_parse.json`;
built tree `work/review98_out`. The 64 goldens are untouched (0 overlapping
MIs, no regen needed).

- [x] Fix 98: `_decl_type_of` (`il2cpp/dec/highlevel.py`) propagates the
  closed RHS `new` type when the tracked type structurally contains
  VAR/MVAR (`_type_has_var` binary walk, not a name guess), the RHS parses
  as a generic `new` (`_new_rhs_type`, arrays/non-generics decline), both
  sides split to the same short base and arity (`_split_generic`), and
  generic-argument-position openness agrees
  (`_args_contain_open_param`: `TMPro.KerningPair`-style qualified names no
  longer read as open). Different bases (`IList<T>` vs `new List<int>()`),
  open RHS, non-`new` RHS (`Enumerator<T> = obj.GetEnumerator()`), bare-`T`
  LHS (`T value1 = new KerningPair()`), and closed/unknown tracked types all
  decline. Built-tree same-base open→closed `new` sites fall 414 → 0 (the 3
  remaining `UnityAction<T0>` lines are legitimate method signatures).

### Next priorities (fix 98 follow-ups)

1. **511 remaining `return sub_*shared body` tails** (fix 94 list stands).
2. **Bare-`T` declaration LHS** (`T value1 = new KerningPair();` family),
   **dead `Type type1 = typeof(Object);` lines** (2,791 sites), Review 87
   byte-store/noreturn-EH/leftover lists — all stand (see below).
3. **`UnityAction<T0>` declaration LHS is DONE (fix 98 above)** except the 3
   legitimate open-generic method signatures, which must stay open.

## Previous work — fix 97 (bare first-use temp declarations + 97e render repair, gated 2026-09-14)

Declare bare first-use temps (`objN = rhs;` with no prior declaration from
stack-slot zeroing, phi copies, unbound call results) exactly like `var`
lines, from the same tracked-type lookup; a later `var` line for the same
temp keeps only its assignment. Gates: **483 tests (462 + 21 new: 15 in
`tests/test_review97_bare_decls.py` plus 6 fix-97e `_render` cases); direct
sweep 116,178 methods / 0 crashes / 0 structural changes vs fix 94 (39,478
bodies changed, net declaration additions); strict build 11,107 files /
115,658 bodies / 0 failures or fallbacks (`work/review97_out`); parser 0
bad files**. Reports: `validation_reports/review97e_sweep.json`,
`review97e_vs97.json` (25 changed, 0 structural — the 97e repair only),
`review97e_parse.json`; built tree `work/review97_out`. The 64 goldens were
regenerated with **0 body changes** (none of the 25 repaired methods is a
golden MI; only source fingerprints refreshed). Promotion record:
`validation_reports/review97e_promotion_verification.json`; post-promotion
parse recheck `validation_reports/review97e_recheck_parse_final.json`.

- [x] Fix 97: first-use bare assignments declare (`_rename_locals` in
  `il2cpp/dec/highlevel.py`, wired through the existing `var` type path).
- [x] Fix 97b: `= default` for zero-literal RHS that cannot spell the
  declaration type (`_bare_rhs_needs_default`: only zero-valued numerics
  rewrite; nonzero literals keep their faithful value).
- [x] Fix 97c: scope-aware declaration tracking (sibling scopes re-declare;
  enclosing declarations suppress).
- [x] Fix 97d: (folded into 97b) nonzero-literal fidelity.
- [x] Companion updates: typed `bool flagN` sugar variants (`_bool_sugar`
  in `il2cpp/dec/sugar.py`), ternary arm declaration normalization
  (`_ternary_pass`), typed hop-temp acceptance (`_HOP_DEF_RX` in
  `_compound_assign`).
- [x] Fix 97e (render-strip repair, found by the parse gate, not the
  sweep): the first `work/review97_out` build gated **23 bad files / 26
  ERROR nodes** (review 94: 0/0/0). Chain: 97b synthesizes `: default`
  false arms, `_ternary` folds `if (!c) { T x = call(); } else
  { T x = default; }` into `T x = c ? call() : default;`, then
  `_strip_dangling_default` (`il2cpp/dec/textpass.py`, inside `_render`)
  dropped the tail — its flat `region_q` flag reset on every `(` (the
  call's parens) and `,` (multi-arg calls), orphaning unparseable
  `? call() ;`, which `_fix_select` cannot repair (statement-level `?`).
  The strip now tracks the paren depth of each live ternary/select `?`
  mark: `(` no longer resets, `,` only forgets marks at its own depth or
  deeper, `)` forgets the closed group's marks, `;{=` still clear the
  region, and `??`/`?.`/nullable `?` never become marks. All 26 sites
  (e.g. `IntPtr num2 = num1 != null ? AndroidJNI.NewGlobalRef(num1) ;`
  → `... : default;`) verified fixed in the rebuilt tree; dangling tails
  (`Foo(a : default)`, including after `int?` declarations) still strip.
  Side note: `tools/validate_corpus.py parse` segfaulted on the broken
  tree (native tree-sitter flakiness; per-file processes and `ts_gate.py`
  were unaffected) and succeeds on the fixed tree.

### Next priorities (fix 97 follow-ups)

1. **511 remaining `return sub_*shared body` tails** (fix 94 list stands).
2. **`UnityAction<T0>` declaration LHS** (61 sites), **dead
   `Type type1 = typeof(Object);` lines** (2,791 sites), Review 87
   byte-store/noreturn-EH/leftover lists — all stand (see below).

## Current work — fixes 94, 95, 96 (gated + promoted 2026-09-13)

Tail-call honesty, void-caller tails, and a `_value_cse` allocation hole,
found by reading `AudioVolumeSliders.Start` end to end. Gates: **462
tests (446 + 16 new); direct sweep 116,178 methods / 0 crashes / 0
structural changes vs fix 92 (3,879 bodies changed, net +1,466 lines,
3,405 line-neutral); strict build 11,107 files / 115,658 bodies / 0
failures or fallbacks (`work/review94_out`); parser 0 bad files**.
Reports: `validation_reports/review94_sweep.json`,
`review94_vs92.json` (3,879 changed, 0 structural),
`review94_comparison.json` (vs Review 84: 17,843 changed, same 4
pre-existing fix-91 structural entries, 0 new crashes),
`review94_parse.json`; built tree `work/review94_out`. Promoted
2026-09-13: `final_out/` now holds `work/review94_out` (11,200 files,
candidate and promoted aggregate sha256 both
`6ec3c6f45deb2f653c1f3bf02053a82251c322f169f5b0df7c8f0249b64e679b`, 0
mismatches; the Review 89 tree is kept at
`bckups/final_out_review89`, the fix-91 tree at
`bckups/final_out_review88`, the Review 84 tree at
`bckups/final_out_r84`). Promotion record:
`validation_reports/review94_promotion_verification.json`;
post-promotion parse recheck
`validation_reports/review94_recheck_parse_final.json` (11,107 files, 0
bad). `validation_reports/SHA256SUMS.txt` still pins the Review 84 era
(prior promotions likewise left it; see the split notes). The 64 goldens
were regenerated after individual review of all 5
diffs (4 void-shape, 1 shared-ctor-tail initializer).

- [x] Fix 94: shared tails strip the hidden instantiation argument
  (exact-text identity proof, trailing-position + single-spec
  tightenings), trim trailing stale unknowns (fix-58 mirror), and render
  the true generic callee instance-folded; resolved ctors take the
  `..ctor` pseudo-form the emitter promotes (`_tail_hidden_generic`,
  `_tail_trim_stale`, `_tail_generic_call` in `il2cpp/lifter/calls.py`,
  wired into both tail-jmp paths). Ground truth: the Start tail's
  `mov r8,[slot]` + dispatch-through-R8 body proves R8 selects
  `UnityEvent<float>.AddListener`, which the 8 listed candidates (all
  zero-arg TypeTraits getters) miss — so NO max-arity trim: the
  candidate set is provably incomplete (a cap of 0 wiped real args in
  testing). `return sub_*shared body` tails fall 1,939 → 511.
  Regressions: `tests/test_review94_tails.py` (12 portable).
- [x] Fix 95: value-returning tails in exact-metadata-void callers render
  `<call>; return;` (`_caller_is_void`, `_emit_tail`; each site keeps its
  `/* tail */` habit). Covers resolved, shared, array-new, and
  generic-resolved tails in both paths.
- [x] Fix 96: `_value_cse` never caches `new` allocations (fresh identity
  per execution; parameterless `new T()` slipped past `_IMPURE`).
  Restores wrongly aliased objects, e.g. all 133
  `StructWrapper<byte>` pool instances in `StructWrapperPools..cctor`
  (+132 lines there). Regressions:
  `tests/test_review96_value_cse.py` (4 portable).

### Next priorities (fixes 94-96 follow-ups)

1. **511 remaining `return sub_*shared body` tails** have no trailing
   hidden identity (absent, non-trailing, or conflicting). The registry
   misses true sharers (fix 94 proof), so closing these needs sharer
   discovery beyond `addr_candidates`, never a max-arity guess.
2. **`UnityAction<T0>` declaration LHS** (61 sites): open-signature hints
   type the declaration while the `new` RHS is closed. Propagate the
   closed RHS type when the hint is an unresolved generic parameter.
3. **Dead `Type type1 = typeof(Object);` lines** (2,791 sites): bound
   results of side-effect-only class-init calls. Drop the result binding
   for class-init helpers.
4. **Review 87 list stands:** untyped `((byte*)+0)[0] = 4294967294`
   stores, five sub-threshold noreturn EH targets, 15 constructor
   leftovers, `object objN` / empty-allocation provenance, ABI gaps,
   8,067 into-block gotos, vector/ARM64/fixture breadth.

## Current work — Review 87 (fix 92, gated 2026-09-11, promoted 2026-09-12)

`docs/reviews/REVIEW87.md`, `validation_reports/review85/sweep4.json`,
`sweep4_comparison.json`, and `parse4.json` describe one source fix (92):
MethodSpec instantiation indices are zero-based with -1 absent. Gates:
**435 tests (317 portable + 64 snapshots + 54 native); strict build 11,107
C# files / 115,658 bodies with 0 failures or fallbacks
(`work/review89_out`); parser 0 bad files; direct sweep 116,178 methods /
0 crashes / 0 new structural changes vs Review 84 (same 4 fix-91
entries)**. Promoted 2026-09-12: `final_out/` now holds `work/review89_out`
(11,200 files, candidate and promoted aggregate sha256 both
`0b906f7d1c8ab400a8718f745df1182bad9e9ffbb55a2bea18c30f51839323b5`, 0
mismatches; the fix-91 tree is kept at `bckups/final_out_review88`, the
Review 84 tree at `bckups/final_out_r84`). Promotion record:
`validation_reports/review85/promotion_verification_review89.json`;
post-promotion parse recheck
`validation_reports/review85/recheck_parse_final.json` (11,107 files, 0 bad).
Note: this section previously reserved "candidate fix 92" for the two
named raisers; that unshipped candidate is renumbered to fix 93.

Completed in this batch:

- [x] Read `classIndexIndex`/`methodIndexIndex` zero-based in
  `generic_method_name` and `_method_spec_type_args`, with -1 as the only
  absent spelling (row 0 is a real instantiation). Proved over all 175,736
  specs: zero-based matches every declared generic arity (32,671 method +
  144,977 class rows, zero exceptions), one-based contradicts 2,749.
  Evidence: `work/review89_spec_arity_census.py`,
  `work/review89_spec_index_base.py`.
- [x] Fixed `Object.Instantiate<Font>`: 66 sites become `GameObject`, 0
  `Font` remain; every generic name steps off its neighbouring row
  (`EpilepsyHandler` -> `ComputeShader`, `Obi.*` -> `Vector2`/`byte`/
  `TouchPhase`/etc.). 16,119 bodies changed, all name-only; inventory and
  line-count shape unchanged.
- [x] Regenerated the 64 golden snapshots: 5 reviewed generic-name changes,
  59 unchanged. Regressions: `tests/test_review89_spec_indices.py` (11
  portable); `tests/test_shared_returns.py` updated to the proved spelling.

### Next priorities (Review 87)

1. **Type the untyped `((byte*)objN + 0x0)[0] = 4294967294;` stores.**
   Carried over from Review 85: the lvalue has no declared width, so the
   immediate cannot be sign-flipped on evidence yet.
2. **DONE - fix 93 shipped 2026-09-13: the two named raisers render as
   `throw new`.** `raise_IndexOutOfRangeException` /
   `raise_NullReferenceException` are each one specific new exception raised
   by a `sub rsp,X; call T; int3` noreturn forwarder, so
   `object objN = raise_NullReferenceException();` becomes
   `throw new NullReferenceException();` (0 old-style sites remain, 834
   throw-new sites in `work/review93_out`). Gates: 446 tests (436 + 10 new
   in `tests/test_review93_named_raise.py`); direct sweep 116,178 methods /
   0 crashes / 0 structural changes vs fix 92 (76 bodies changed, -76
   lines); strict build 11,107 files / 115,658 bodies / 0 failures; parse
   gate 0 bad files. Reports: `validation_reports/review93_sweep.json`,
   `review93_vs92.json` (`review93_comparison.json` vs Review 84),
   `review93_parse.json`. Predicate: exact evidence-derived name, arity 0,
   unregistered target, forwarder shape (`_named_raise_throw` in
   `il2cpp/lifter/calls.py`, wired into `_call` and both tail-jmp paths).
3. **Prove the five sub-threshold noreturn EH targets**
   (`0x180435040`, role-ambiguous `0x1804346b0`, `0x180434690`,
   `0x180001ea0`, `0x180002070`) with evidence other than witness counts,
   then tighten per-method/proven-set agreement.
4. **Review 84 list stands:** 15 constructor leftovers, 112,423
   `object objN` declarations, 13,254 empty allocations, ABI gaps, 8,067
   into-block gotos, vector/ARM64/fixture breadth (see the Current
   replacement section below).

## Previous work — Reviews 85 and 86 (2026-09-10/11)

`docs/reviews/REVIEW85.md` and `validation_reports/review85/` describe five source fixes
(85-89), one validation-tool fix, and one newly diagnosed defect. Gates:
**399 tests (289 portable + 64 snapshots + 46 native); strict build 11,107 C#
files / 115,658 bodies with 0 failures or fallbacks; parser 0 bad files;
direct sweep 116,178 methods / 0 crashes / 0 structural-metric changes / 0 new
crashes vs Review 84**. Promoted 2026-09-11 (itself superseded 2026-09-12 by
the Review 87 promotion; the fix-91 tree is kept at
`bckups/final_out_review88`): `final_out` then held
`work/review88_out`, the tree gated after fixes 90, 91, 91b, and 91c (11,200
files, candidate and promoted aggregate sha256 both
`0ef7607e317dbb00f59ad72ccaa8089b36ccf0a79c42bae7f525ebeb30118d00`, 0
mismatches; the Review 84 tree is kept at `bckups/final_out_r84`).
`work/review86_out` was never promoted. Gates for that tree: 424 tests,
strict build 11,107 files / 115,658 bodies / 0 failures, parse gate 0 errors
and 0 recovery nodes, direct sweep 116,178 methods / 0 crashes, 64 goldens
regenerated with 0 changes. See `docs/reviews/REVIEW86.md`.

Completed in this batch:

- [x] Decode enum member tables through the enum's underlying element type
  with the compressed (zigzag) reader. The old raw fixed-width read doubled
  every value and invented junk members; eight member names are confirmed
  wrong before and correct after, including `DateTimeKind.Utc` -> `Local` and
  `Token.XdrDatatype` -> `XsdSchema`.
- [x] Fold enum-valued call arguments to `Type.Member`, so
  `new FileStream(text2, 3)` becomes `new FileStream(text2, FileMode.Open)`.
- [x] Stop `_int_lit` stripping the hex digits `d` and `f` as float suffixes.
  It had read `0x3d` as 3, `0x7f` as 7, and `0xf` as unparseable.
- [x] Fold literal-base address composition, `(0 + 0x3)` -> `3`, without
  touching `_field_expr`'s dereference form.
- [x] Reinterpret immediates at their declared signed width, `4294967294` ->
  `-2`; 188 rewrites in the first 4,000 methods. Unsigned and native-int type
  codes deliberately excluded.
- [x] Relocate sweep manifests relative to the report that names them, fixing
  moved-report reads on Windows.
- [x] Regenerate the 64 golden snapshots: 9 changed, +37 / -37 lines, every
  changed line an enum-member fold.

### Next priorities (Review 85, historical; use the Current work list above)

1. **DONE - EH helper naming is now evidence based (fixes 90, 91, 91b, 91c).**
   `_seh_helpers` used to discover the raise/rethrow VAs from whichever method
   was lifted first and write them onto the shared lifter, so output depended
   on process partitioning and lift order. That part was right, and it still
   explains 1,913 of the 10,758 changed bodies in that batch, which are **not**
   attributable to fixes 85-89.
   The rest of the diagnosis above was wrong about which side was correct. A
   census of all 4,526 pad-bearing methods found 99 distinct rethrow targets
   and 9 raise targets, and 51 of the rethrow targets were ordinary registered
   methods -- `AsyncTaskMethodBuilder.SetException`, `Debug.LogException`,
   `Marshal.FreeHGlobal`, even `DateTime.AddYears` -- so a large share of
   those 3,113 `throw` statements were leaked values that had each eaten a
   real call, not correct output.
   Fix 90 clears both fields for every method and requires an unregistered
   native target. Fix 91 then proves the pair once from the whole binary:
   `0x180435740` rethrow (3,403 witnesses against 126) and `0x180435670`
   raise (183 against 25). Fix 91b rejects plumbing the lifter can already
   name, directly or through a jmp thunk -- `0x180435420` is a thunk onto
   `il2cpp_codegen_initialize_runtime_metadata` that 181 methods had taught
   as a helper -- and fix 91c rejects any routine with a reachable `ret`,
   which removed five impostors including the 45-witness `0x180002650`.
   Evidence: `work/review87_helper_census.py`,
   `work/review87_helper_classify.py`, `work/review88_helper_ident.py`,
   `work/review88_anchor_diff.py`, `work/review88_sample.py`. Regressions:
   `tests/test_review87_eh_helpers.py`,
   `tests/test_review88_eh_helper_set.py`.
   Still open: five noreturn but sub-threshold targets (`0x180435040` 13/0,
   `0x1804346b0` 12 rethrow against 13 raise, `0x180434690` 8/0,
   `0x180001ea0` 6/0, `0x180002070` 3/0) remain on per-method evidence only,
   and the two named raisers still render as calls rather than
   `throw new IndexOutOfRangeException();` / `throw new
   NullReferenceException();` -- candidate fix 92 (renumbered to fix 93, since
   fix 92 shipped the MethodSpec base; see the Current work section).
2. **Type the untyped `((byte*)objN + 0x0)[0] = 4294967294;` stores.** The
   lvalue has no declared width, so the immediate cannot be sign-flipped on
   evidence yet. Recover the store type and width first.
3. **DONE - Fix the wrong generic argument in `Object.Instantiate<Font>`.**
   Shipped as fix 92; see the Current work section above and `docs/reviews/REVIEW87.md`.

## Current replacement — Review 84 (2026-09-10)

`docs/reviews/REVIEW84.md`, `docs/archive/reviews-log.md` §0bb, and `validation_reports/review84/` describe the
current source and complete output. Release: **358 tests (260 portable + 64
snapshots + 34 native); strict build 11,107 C# files / 115,658 bodies with 0
failures or fallbacks; parser 0 bad files; direct sweep 116,178 methods / 0
crashes / 0 structural-metric changes; constructor sweep 11,737 methods / 0
crashes**. The original DLL/metadata remain unchanged and were read statically,
never executed.

Completed in this release:

- [x] Complete class inheritance chains through a unique
  `IL2CPP_TYPE_OBJECT` → `System.Object` mapping, stop cycles, and isolate
  inheritance/field caches per `Il2Cpp` instance.
- [x] Resolve folded parameterless constructors only from typed current-ctor
  `this` or exact fresh-allocation provenance, one concrete closed MethodDef,
  a reference-type inheritance match, and exact instance/void/zero-argument
  metadata. Decline generic, multiple-match, byref, value-type, or malformed
  cases.
- [x] Distinguish same-type `: this(args)` from ancestor `: base(args)` and
  recover parameterized resolved initializers without leaving raw pseudo calls
  in generated C#.
- [x] Carry exact `_alloc` provenance through binding/copies and complete one
  allocation declaration in place. Audited discarded constructor allocations
  fall 13,292 → 0; empty allocation declarations fall 21,624 → 13,254.
- [x] Reduce `sub_180506120` constructor-family markers 2,958 → 160, legacy
  `this.ctor(...)` text 2,186 → 45, all shared calls 21,504 → 18,703, and
  `object objN` declarations 113,155 → 112,423.
- [x] Increase real `: base(...)` initializers 5,960 → 9,530 and
  `: this(...)` initializers 0 → 325 while shrinking generated C# by 20,568
  lines with no file-inventory change.
- [x] Preserve unrelated shared-call behavior by excluding the newly visible
  Object tail from the broad legacy receiver heuristic; freeze the regression
  where `System.Type.op_Equality` must not become an Object method.
- [x] Freeze the same 64 MethodDefs in `goldens_review84.json`: 56 unchanged and
  eight reviewed constructor/allocation changes.
- [x] Strict-build, overlap-verify, parse, directly sweep all methods and all
  constructors, compare, test, promote, checksum, and package the complete
  replacement.

### Next priorities (current, not archived diagnoses)

1. **Prove the 15 conservative constructor leftovers.** Twelve native
   constructors still contain `sub_180506120` because multiple eligible
   ancestor constructors share it; three complex generic/scope constructors
   retain `this.ctor(...)`. Add receiver/generic proof, never a cosmetic guess.
2. **Trace the producers of the remaining 112,423 `object objN` declarations.**
   Recover register seeds, stack-slot reads, local copy/store provenance, and
   alias identity. Type the producing value before changing its declaration.
3. **Finish allocation and indirect-call identity.** Classify the remaining
   13,254 empty allocations, virtual/function-pointer constructor targets, and
   cyclic allocations with dominance and per-iteration alias proof.
4. **Complete missing return/call ABIs.** Generic value-type instantiated sizes,
   source-level `ref` returns, non-address hidden buffers, mixed candidates, and
   broader stack/vector arguments need explicit models and negative tests.
5. **Finish legal structured control flow and compilation readiness.** 8,067
   into-block gotos remain across 2,047 methods, along with definite assignment,
   project references, constructor/SEH, identifier/type, and ref-return issues.
6. **Vector, ARM64, and fixture breadth.** General packed-lane state, ARM64
   semantics, and an independent licensed fixture remain open.

---

## Appendix: TODONOW.md — 2026-09-22 failure-class inventory (merged 2026-09-28)

> **HISTORICAL (2026-09-22, r4c era).** The former root `TODONOW.md`,
> folded in here so `docs/todo.md` is the single todo file. Live work is
> the "Open, by payoff" index at the top and the `## Current work`
> sections above; this appendix is kept for the failure-class inventory
> and source anchors. Line numbers may have moved, and every count below
> is r4c-era.

Generated 2026-09-22 from the current promoted tree. This is a handoff for
the next agent. The generated C# tree is `final_out/`; do not edit it by hand.
The source of truth is the decompiler under `il2cpp/`. Fixture inputs are
`testgame/ShiftAtMidnight_Data/il2cpp_data/Metadata/global-metadata.dat` and
`testgame/GameAssembly.dll`.

## Baseline gates (r4c promotion, 2026-09-23 — prior numbers archived below)

- Strict rebuild: 114,458 bodies, 0 failures, 0 fallbacks (matches).
- Brace audit: 0 unbalanced files. Parse gate: 0 bad / 0 ERROR / 0 MISSING.
- Full suite: 933 passed, 0 failed (first fully-green run; 67525
  regened to the signature-exact composite).
- `final_out/` is promoted output and must remain read-only.
- The fixture is private/licensed; never redistribute it.

## Exact fresh census of `final_out/`

All paths below are relative to `C:\Users\crax\Downloads\il2csharp`.
The count is occurrences/lines first and distinct `.cs` files second.

| category | promoted r4c scan | 2026-09-22 handoff figure | exact output root |
|---|---:|---:|---|
| shared-body marker `/*shared body, N candidates*/` | 18,884 / 2,278 | 19,013 / 2,304 | `final_out/**/*.cs` |
| `/*indirect*/` | 6,262 / 884 | 7,091 / 975 | `final_out/**/*.cs` |
| literal `unknown` | 15,655 / 1,361 | 16,044 / 1,382 | `final_out/**/*.cs` |
| raw `mem[N]` | 398 / 127 | ~13,189 / 805 | `final_out/**/*.cs` |
| `mem_<hex>` load twins | 359 / 95 strict (`mem_addr` params excluded) | 234 / 69 | `final_out/**/*.cs` |
| `goto` | 8,707 / 903 | 8,705 / 901 | `final_out/**/*.cs` |
| `/* nothing */` | 63 / 1 | 63 / — | `final_out/**/*.cs` |
| `?addr` | 1 / 1 | 22 / 6 | `final_out/**/*.cs` |

`?addr` follow-up (unpromoted): the last site (mi 65244) was our own
quarantine over-firing on a named `&s_1d0` home, so the declines were
narrowed to text-`?` bases and the store rescued -- then the rescue
was traced and disproved (rendered base aliases a reused home while
native uses a fresh address; address-of lost in write-barrier
conversion), and reverted byte-identically with the elision pinned by
a game test. `?addr` stays 1, honestly.

The differences are scanner-definition differences, not silently ignored
files: use the commands in the Census reproducibility section. In particular,
`unknown` can be counted as tokens, lines, or diagnostic hits; `?addr` can be
counted in historical reports rather than the promoted tree; and the shared
body/goto totals have changed by small formatting/regen deltas.

## 1. Runtime-broken — shared-body calls

### Exact files

Every affected file is under `final_out/` and matches the shared-body marker.
There are 2,304 distinct files. The exact complete inventory is reproducible
with the first command below; do not use a hand-curated sample as the scope.

### Source ownership

- Primary renderer: `il2cpp/lifter/calls.py:925` — emits
  `sub_%x/*shared body, %d candidates*/` when the native VA has multiple
  metadata owners.
- Shared-call pipeline and candidate/ABI logic: `il2cpp/lifter/calls.py`
  (especially the shared-call sections around lines 84, 1345, 1600, and
  1964–2051).
- Receiver/type lookup and shared target metadata: `il2cpp/runtime/core.py`,
  `il2cpp/runtime/registration.py`, `il2cpp/runtime/types.py`.
- Call-site analysis/indirect-tail handoff: `il2cpp/dec/analyze.py:180–205`.

### Why it is broken

The output names a native shared body but cannot select the concrete managed
MethodDef at the call site. It is therefore not a callable C# declaration;
the unresolved target throws at runtime. The honest spelling must remain for
ambiguous cases until receiver type, generic instantiation, ABI, and owner
proof all agree.

### Required fix direction

Implement receiver-type resolution at the call site, not a global VA rename.
Preserve all-candidate consensus rules, open-generic rejection, shared sret
rules, and the 15 conservative constructor leftovers documented in
`CLAUDE.md`. Add negative tests for ambiguous receivers and shared addresses.

## 2. Runtime-broken — indirect calls

### Exact files

975 files under `final_out/` contain 7,091 `/*indirect*/` occurrences.
Generate the complete path list with the second census command below.

### Source ownership

- Indirect call rendering: `il2cpp/lifter/calls.py:1139–1141` and
  `il2cpp/lifter/calls.py:1521`.
- Virtual/interface unresolved dispatch: `il2cpp/lifter/calls.py:1964–2051`.
- Indirect memory/control-flow classification: `il2cpp/lifter/insn.py:1231–1234`.
- CFG safety/unknown indirect control flow: `il2cpp/dec/build.py:25–44` and
  `il2cpp/dec/analyze.py:180–205`.
- Higher-level dispatch folding (must decline when proof is absent):
  `il2cpp/dec/flow.py:917–920` and `il2cpp/dec/sugar.py:328`.

### Required fix direction

Same fix family as shared bodies: infer the receiver/interface slot and exact
closed MethodDef from metadata plus native evidence. Do not resolve by helper
VA, class name, or majority candidate. Preserve `/*indirect*/` when proof is
missing.

## 3. Compile-broken — unknown values

### Exact files

Fresh token scan: 12,084 `unknown` tokens in 1,383 files under
`final_out/`. The historical handoff reports 16,044 hits/1,382 files because
its hit definition includes additional unknown-value diagnostics. Treat the
union of both scans as the investigation scope.

### Source ownership and producer families

- Unknown minting: `il2cpp/lifter/state.py:1131–1132` (`_fresh_unknowns`).
- Register/value propagation: `il2cpp/lifter/state.py`,
  `il2cpp/lifter/values.py`, `il2cpp/lifter/aggregates.py`.
- Unknown call results and ABI fallback: `il2cpp/lifter/calls.py:1185–1262`.
- Unknown memory operands: `il2cpp/lifter/insn.py:1675–1695`.
- Unknown cleanup/rendering: `il2cpp/dec/textpass.py:458–529` and
  `il2cpp/dec/textpass.py:599`.

### Known remainder classes

1. stale stack tiles surviving copies/merges;
2. SIMD/vector lanes not carried through spills, `UNPCK*`, or calls;
3. unknown results from unresolved shared/indirect calls;
4. genuine unknown branch conditions and pointer bases.

Fix producers and provenance; never replace `unknown` textually with zero,
`default`, or a guessed type.

## 4. Compile-broken — raw `mem[N]` stores and `mem_xx` loads

### Exact files

- `mem[N]`: 13,189 occurrences in 805 files under `final_out/`.
- `mem_<hex>`: 324 occurrences in 70 files by the current broad scan; the
  handoff's narrower load-twin census is 234/69.

### Exact source

- `il2cpp/lifter/insn.py:1345`: load fallback returns `Expr('mem_%x' % disp,
  None, 'ptr')` when the base register is untracked.
- `il2cpp/lifter/insn.py:1349`: `_mem_lvalue` begins raw-store generation.
- `il2cpp/lifter/insn.py:1379`: `if be is None: return 'mem[%d]' % sdisp(disp)`.
- Store consumers: `il2cpp/lifter/insn.py:1695–1787`.
- Raw-width/type tests and intended conservative behavior:
  `tests/test_review102_raw_store_widths.py:251–359`.

### Required fix direction

Recover the base register/aggregate provenance and declared pointee width
before emitting a named field or typed pointer. A raw store is currently an
undeclared C# identifier and therefore a compile error. Do not make up fields
from displacement alone; preserve raw output when ownership/layout is not
proved.

## 5. Compile-broken — unbound temps

### Exact files

Upper bound: up to 8,700 tokens across as many as 2,200 output files. This is
not a clean compiler count: it includes false positives such as multi-
declarations and identifiers introduced in a branch whose declaration is
outside the textual region. The exact candidate path inventory is produced by
the unbound-temp command below.

### Source ownership

- Register/stack seed and copy state: `il2cpp/lifter/state.py`,
  `il2cpp/lifter/values.py`, `il2cpp/lifter/aggregates.py`.
- Phi/merge materialization and copies: `il2cpp/dec/analyze.py:448–510`.
- Declaration/use binding and dead-local cleanup:
  `il2cpp/dec/dataflow.py`, `il2cpp/dec/emit.py`, `il2cpp/dec/textpass.py`.
- Final semantic names (must not invent type evidence):
  `il2cpp/dec/emit.py` / `_semantic_local_names` and the invariants in
  `CLAUDE.md`.

### Required fix direction

Trace each candidate to its native definition, stack home, phi edge, or call
result. Fix the producer/provenance and scope merge. Do not globally declare
all `objN` names or substitute `default`; that would hide missing native
values and create runtime corruption.

## 6–11. Resolved or harness artifacts — do not re-investigate

- Duplicate members: genuine intra-assembly duplicates were fixed by
  conversion-operator emission. Remaining CS0101/CS0111/CS0102 spikes are
  cross-assembly BCL twins caused by the single-assembly harness. See
  `il2cpp/emitter.py` and the Roslyn ledger in `nowtodo.md` Addenda 14–15.
- Enum/int edges: fixed by enum-aware `(E)v` casts, underlying declarations,
  parentheses, and `unchecked`; verify with Roslyn only. Do not reopen.
- Finalizers: fixed in `il2cpp/headers.py`/signature emission; exact `~X()`
  output is already covered. Do not reopen.
- Optional parameter order: fixed in parameter emission (`= default` for
  dropped trailing null rows; genuine mid-default rows stripped). Do not
  reorder parameters.
- CS0115 bad overrides: harness artifact; adding Mono.Security to the check
  scope reduces the reported 14 to zero.
- `_1<T>` qualifier remainder: harness artifact; declarations live in
  uncompiled Fusion directories.

## 12–15. Cosmetic/by-design — do not spend fix effort

- `goto`: current scan 8,707/903; compiles and represents unresolved
  unstructured control flow. Emitter/structured pipeline is under
  `il2cpp/dec/structure.py`, `flow.py`, and `emit.py`.
- `/* nothing */`: 63 occurrences in one file (`Arm.cs` Neon forwarders);
  fresh lifts now render all 63 as `return Neon.<s8-variant>(args);`
  (noreturn-shared forwarder proof, 2026-09-24). Promoted `final_out/`
  still shows the old bodies until a rebuild.
- `__SharedBodyStubs`: throwing stubs are intentional behavior for unresolved
  runtime targets; see `il2cpp/emitter.py` stub generation.
- `?addr`: current promoted tree has only 2 occurrences in 2 files; nearly
  extinct and not a priority.

## Census reproducibility (PowerShell, from repository root)

```powershell
$out = 'final_out'
rg -n --glob '*.cs' 'sub_[0-9A-Fa-fx]+/\*shared body, [0-9]+ candidates\*/' $out
rg -n --glob '*.cs' '/\*indirect\*/' $out
rg -n --glob '*.cs' '\bunknown\b' $out
rg -n --glob '*.cs' '\bmem\[[^]]+\]' $out
rg -n --glob '*.cs' '\bmem_[A-Za-z0-9_]+' $out
rg -n --glob '*.cs' '\bgoto\b' $out
rg -n --glob '*.cs' '/\* nothing \*/' $out
rg -n --glob '*.cs' '\?addr' $out
```

To obtain exact distinct paths for any category, pipe a command's output
through this PowerShell expression (it preserves the `file:line:text` output
for follow-up inspection):

```powershell
$hits = rg -n --glob '*.cs' '/\*indirect\*/' final_out
$hits | ForEach-Object { ($_ -split ':',3)[0] } | Sort-Object -Unique
```

Replace the pattern with the other marker. For source ownership, use
`rg -n` against the exact files listed above; line numbers are current source
line anchors and must be rechecked after edits.

## Work order for the fixing agent (status as of r4c promotion)

1. Inventory: done (census table above, re-counted at promotion).
2. Shared-body receiver resolution + indirect/interface dispatch:
   landed as proof-driven slices (array receivers, twins pins,
   interface dispatch); hinted receivers and generic substitution
   disproved/deferred with evidence (see addenda).
3. Unknown values + raw memory: landed as provenance slices (RSP-copy
   homes, SIMD consumer-side tails + direct); general packed tracking
   stays declined.
4. Unbound temps: classified (55 distinct in 21 files, all params or
   checker FPs in fresh lifts) and fixed (rename barrier + param
   exclusion); actionable set ~zero.
5. Gates + suite: 932 passed / 0 failed (first fully-green run; the
   old 67525/104428 reds were regened after per-hunk review).
6. Never regenerate or promote `final_out/` without an explicit user call.

## Stop record — 2026-09-22, SIMD/stack provenance follow-up

The decompiler changes are in the primary repository package under
`il2cpp/`; the scripts under
`C:\Users\crax\AppData\Local\Temp\opencode` were tracing/patch helpers only
and are not imported by the project. `final_out/` was not edited, rebuilt, or
promoted.

### Source changes

- `il2cpp/lifter/insn.py`: scalar SSE arithmetic preserves untouched upper
  lanes when the input already carries proved packed provenance. General
  `SHUFPS` recovery was attempted, but reverted after MethodDef 80548 proved
  the same local shape can be integer/index bookkeeping; it remains a
  conservative no-op until stronger use-site proof exists.
- `il2cpp/lifter/aggregates.py`: an offset lane crosses a CFG phi only when
  every predecessor reconstructs the same typed value.
- `il2cpp/lifter/state.py`: use-binding keeps packed-phi provenance reachable
  after a `vN` expression is renamed to a `tN` temp.
- `il2cpp/lifter/values.py`: kill-on-write freezes packed lanes that read an
  overwritten location instead of discarding their provenance.
- `il2cpp/lifter/calls.py`: the early sret-return path now uses the existing
  Win64 positional-argument reconstruction and reconstructs by-value structs
  from stack homes, matching the ordinary resolved-call path.
- `tests/test_recovery_completion.py`: six portable regressions cover
  scalar-lane preservation, unanimous/disputed phi lanes, bind-time
  provenance, and safe/stale kill-on-write lanes.

### MethodDef 104428 (`GraphUpdateShape.GetBounds`)

The two emitted `unknown` arguments are gone. The final native call now has
all six declared parameters present and typed; its first two difference
vectors are reconstructed from the packed XMM/stack tiles, and the 5th+
Win64 arguments are read from the stack home area rather than a stale XMM
tail. The fresh body still differs from the frozen golden (including modern
static-field spelling and the newly recovered aggregate expressions), so
`tests/test_game_goldens.py` remains red for 104428 until that body is
reviewed and an explicit golden-regeneration call is made. Do not blindly
regenerate it.

### Validation at stop

- `python -m compileall -q il2cpp il2csharp.py`: pass.
- Source-format assertions for every touched `il2cpp/lifter/*.py`: CRLF,
  no BOM, pass.
- `git diff --check`: pass.
- Final portable suite: **757 passed, 130 deselected**.
- Focused new tests after that revert: **7 passed**; the only selected failure was the expected
  stale 104428 golden.
- Final full licensed suite: **885 passed / 2 failed**. The only failures are
  the documented stale snapshots for MethodDef 67525 and 104428; no new
  failures were introduced.

### Resume point

Review the fresh 104428 call arguments against the native stores at
`0x18072e410`–`0x18072e456`, then run a direct corpus sweep before considering
a golden update. MethodDef 67525 remains the
documented honest SIMD decline. The broad shared-body, indirect-call,
unknown/raw-memory, and unbound-temp inventories above remain open; this
follow-up fixes one producer family, not the whole census.

## Stop record — 2026-09-22, RSP-copy home round (unpromoted)

Subagent-proposed, human-implemented. Same rules: `final_out/`
untouched (its census above still stands), no snapshot regen, no
promotion, no rebuild. All `il2cpp/` edits via binary patches with
CRLF/no-BOM asserts; `tests/` edits LF (one pre-existing CRLF game
file kept byte-identical in endings).

### Source changes (`il2cpp/lifter/insn.py` only)

- `mov r64,rsp` now carries the frame offset (`_stack_offset` on a
  `?`-text ptr) instead of dropping to `None`, so `[copy+N]` keys slots
  by absolute address and aliases `[rsp+M]` of the same home. Wired
  through `_read_mem`, `_mem_lvalue`, and the `lea` address path;
  arithmetic/index/32-bit uses decline to the unknown-base shapes.
- RBP quarantine (stash-proven): the first cut tracked
  `lea rbp,[rsp-C]`-style frame offsets absolutely and split
  RBP-disp-keyed homes (80548 `int num2` became `object obj1` plus an
  unbound `num2`). RBP stays on the legacy frame paths byte-identically
  (MOV/LEA/load/store/indexed all skip RBP); `aggregates.py` reverted
  untouched. 80548 matches its golden again.
- `tests/test_recovery_completion.py` +4 portable (slot roundtrip +
  cross-delta alias, arithmetic/index/32-bit+RBP declines);
  `tests/test_game_frame_copy.py` new (+3 game: 117615 improvement,
  23900 same-typedef must-decline, both `?addr` extinctions);
  `tests/test_game_review83.py` sret pin evolved to the faithful
  spelling (old site-1 `(default,default,default)` was copy blindness;
  native passes three addresses at `0x182529283`–297).

### Method evidence (each `--mi` re-lifted, base-vs-new diffed)

- 117615 (`WriteInt32AtOffset`): `mem[8] = this;`/`mem_8`/raw twins
  become `this._offsetBits = offset;`/`this.WriteSlow(value, bits);`.
  One undeclared `obj6` phantom survives in the replayed finally tail
  (was three undeclared `mem[8]`/`mem_8`/`obj2`).
- 32837 (`Touchscreen.Reset`): golden holds 4 raw `mem[]` prologue
  spills (`mov rax,rsp` proven); actual drops them, renumber-only
  fallout. NEW red, consigned to regen.
- 108722 (sret): both native address-triples print; unobserved
  stand-downs stay pinned portably (unknown receiver/size).
- 104428: 11 raw `mem[]` spills removed (its golden holds `mem[8]`
  too); same already-red ID, still awaiting the gated-regen user call.
- 80548: quarantine restored the golden byte-identically.
- 82799/104380: the promoted tree's only two `?addr` hits
  (`store into untracked ?addr` in copy-heavy methods) render no
  `?addr` and no `mem[]` in fresh lifts; 82799's `return real2`
  residue is pre-existing (unbound in the old body too).

### Validation at stop

- `python -m compileall -q il2cpp il2csharp.py`: pass.
- Source-format assertions (`insn.py` CRLF/no-BOM): pass.
- `git diff --check`: pass.
- Portable suite: **765 passed** (761 + 4 new), 132 deselected.
- Game pins: `test_game_frame_copy.py` 3/3,
  `test_game_review83.py` 7/7 (with the evolved pin).
- Full licensed suite: **894 passed / 3 failed** — 67525 (honest SIMD
  decline) + 104428 (stale golden) were already red; 32837 is new but
  proved improvement (above). No other breaks.

### Resume point (superseded by r4c promotion — historical record follows)

Work order §4 was completed after this stop record: the unbound census
collapsed to 55 distinct tokens (all params/checker FPs in fresh
lifts) and the rename barrier + param exclusion fixed the producers.
Corpus was rebuilt + regened + promoted twice since (r4a, r4c);
`final_out/` census above is the r4c recount, not this stop record's
era. Remaining work is tracked in `docs/todo.md` Current work.

## Addendum — 2026-09-22, TODONOW #1 first slice (unpromoted)

Array receivers now resolve shared calls (subagent-mined mi 275/326/
4047: 9-candidate Clone fold → `System.Array.Clone` instance rendering;
mi 144 string twins pinned must-decline, 5 markers). Mechanism:
`Il2Cpp._system_array_td` + `Lifter._array_receiver_td` with a 2-line
fallback at all three chain-filter twins; sret/ctor/generic/unanimity
gates untouched. Portable + game pins green; full suite holds the
RSP-copy-round failure set byte-identically (32837/67525/104428 — none
of the four touched methods is in the golden set). Remaining #1 work:
slot/hint-typed receivers, indirect/interface dispatch, then
receiver-driven generic substitution (needs the synthetic table).

## Addendum — 2026-09-22, hinted receivers DISPROVED (reverted clean)

Side-table corroboration (`slot_types` vs per-pass `_type_hints`,
dual-agreement + closed-key) resolved `&raycastHit1`→`distance`
(25687) and `&taskAwaiter1`→`GetResult`/`IsCompleted` (24238) with
correct trims — then reverted with zero residue. Root cause, traced to
the instruction: resolving IsCompleted removed the ambiguous-shape
union-kill that used to clear the `s_50` home tile; the surviving tile
had been field-split by `_scalar_parts` (TaskAwaiter-typed RAX from the
already-resolved `GetAwaiter`), so the whole-struct reload projected
`.m_task` into the TaskAwaiter-typed `<>u__1` home — an ill-typed line
the suite cannot see (same IDs pass either way). Rule: hint-driven
resolution stays out until whole-struct reloads prefer whole tiles
(byte-range sidecar); the `_td_of`/array paths keep their pinned
behavior. Repro/diagnostic probes kept in Temp; post-revert lifts of
25687/24238 are byte-identical to the pre-hint baselines.

## Addendum — 2026-09-22, SIMD consumer-side recovery (unpromoted)

67525's constants died at: scalar-pool loads dropping bytes (vs the
PACKED128 `_bytes` attach) and `unpcklps` lane reads failing untyped,
then tail args reading `.text` only. Fix, tails-only: byte provenance
on scalar const loads + typed GPR-slot materialization at closed
all-float vector slots (house `(float2)(l0,l1)` for
Unity.Mathematics.float2; width-4 literal). 80548 stays intact
(PSRLDQ-popped/integer-tainted values carry no parts -- the guard).
Fresh: `clamp(x, (float2)(0.0f, 0.0f), (float2)(1.0f, 1.0f))`,
signature-exact where the golden scalars needed unprovable implicit
conversions -- golden regened (surgical, SHAs verified). Follow-up:
same gates wired into resolved direct calls via a shared helper
(67836 smoothstep renders composites, uncovered args stay unknown).
Suite 933/0. Open: per-arm Color, general packed tracking.

## Status — end of 2026-09-22 session (paused, tree clean)

Suite: **932 passed / 0 failed** (fully green; 67525 regened to the
signature-exact composite). Last source change: direct-call
float-lane materialization via shared helper (67836 renders
composites, uncovered args stay unknown). Reverted same day:
?-text tightening (rescued store miscompiled -- elision was honest,
now pinned by a game test).
`final_out/` holds the r4a tree (predates SIMD + direct-call);
next rebuild will carry them plus the ?addr-tightening revert
(net: SIMD/direct improvements only).
Open, hardest-first: field-provenance sidecar (designs + two
disproofs on file), general packed SIMD (80548-bounded), per-arm
Color (needs use→def), runtime-generated vtables (decline forever).
No blockers, no red tests, no uncommitted work.

## Addendum — 2026-09-22, unbound census + rename barrier (unpromoted)

Work-order §4 (classify before patching), done as a read-only text
tool (comment/string scrub, method regions, dominance = earlier line
at depth <= use): the ~8,700-token/~2,200-file upper bound collapses
to **55 distinct unbound tokens in 21 files**. Remainder by family:
lift-stage vN residuals (StreamBuffer v0-v7 et al.), tN oversize/bind
temps, SIMD type-position FPs (v128/v64/v256), and one obj-family case
fixed below. The census itself moves no gates.

The obj-family case (mi 124140 `AndroidJNI.IsSameObject`) forwarded
`(obj2, obj2)` for native `(obj1, obj2)`: `_seq` was correct and
`phi_alias` empty — `_rename_locals` had minted the dead spill as
`object obj1 = obj2`, shadowing the params, and `_copy_prop` merged
the argument. Fixed with `_semantic_local_names`' barrier (reserve
body identifiers + metadata params, bump until free). Portable + game
pins green; zero golden movement. The vN/tN residuals in the other 20
files are still open, now with exact file:line inventories.

## Addendum — 2026-09-22, param-exclusion rename (unpromoted)

The census vN family turned out to be renamed *parameters*:
StreamBuffer.WriteBytes(byte v0, byte v1) (mi 113041-113044)
rendered `this.buf[num2] = obj5` for native `v0` -- `_rename_locals`
rewrites vN tokens including metadata params while the emitter keeps
them, disconnecting every use. Rename targets now exclude every
metadata parameter spelling (a colliding lifter temp keeps its honest
lift-stage name instead of a silent capture). All four overloads
render fully bound; +1 portable / +4 game pins green; zero golden
movement (909 passed / same 3 IDs).

Follow-up: all remaining census residuals resolve as metadata
parameters (HashCode v1-v4, MeshVoxelizer, JValue, TimeSpan, Version,
JToken, TypeUtils, ExceptionBuilder, TMPro, GradientSettingsAtlas --
each verified bound in fresh lifts) except 5 SIMD type-position
checker FPs (v128/v64/v256 as types). The §5 actionable set is ~zero
in fresh lifts; +2 game pins (1935, 79519).

## Addendum — 2026-09-22, interface dispatch slice (unpromoted)

TODONOW #2 first blood, subagent-mined: `GameManager.CheckAllReady`
(mi 25368) carries three back-to-back interfaceOffsets searches that
resolve to GetEnumerator/MoveNext/get_Current exactly (the ground
truth `dec/flow.py` cites). They missed on three decline-preserving
defects, all fixed: slot-line decl prefixes at render stage, the
typeof-reference span ending at the slot instead of the call, and
`_N` display arity vs `` `N `` metadata names (exact-first, fallback
for generic displays only). Full body diff is resolutions + dead
scaffold DCE + one consistent rename; zero `/*indirect*/` remains in
the method. Portable + game pins green; full suite holds the failure
set byte-identically (same 3 IDs). Open #2 remainder: vtable occupants
on abstract bases (needs store provenance -- do not touch without it),
receiver-driven generic substitution (synthetic table).

## Addendum — 2026-09-22, generic slice closed without patch

Designed (extractor + hook + inflated-chain swap) then empirically
closed: 23762's homes already close via the MethodRef slot path,
closed-generic bases never reach `_field_expr` there (0 hits traced),
and corpus mining found zero hook-shaped sites (open result +
correctly-attributed closed receiver + pure-result fix) -- the 9
open-result sites need use→def consumers, 24679/109849 are
misattributed field lanes, the 187 family is already fine.
`selectable1`/`obj17`/`obj11` need sidecar/SIMD-lanes/use→def
respectively (documented). Deferred with the hinted round; no
invisible infra shipped.

## Addendum — 2026-09-22, boxed-bool fold (unpromoted)

The interface round left `object obj32 = obj5.MoveNext();
if (obj32 == null)` -- dead (boxed bools are never null) and wrong on
false (native `test al,al` breaks). `_name_interface_dispatch` now
records bool-returning resolutions; `_boxed_bool_null_fold` runs last
(single `object X = <call>` decl, all-uses-bool via `_bool_use_ok`, no
reassign/address-take, standalone heads; no inlining, no renames).
Folds in 8 methods (25368, 24059, 25132, 25872, 26880, 27213, 97399,
105906); unbox/`&` uses and ref-null tests decline. Portable + game
pins green; full suite holds the failure set byte-identically (same 3
IDs, zero golden movement).

## Addendum — 2026-09-23, InventoryManager audit (15 findings)

| # | Category | Count / Location | Notes |
|---|----------|------------------|-------|
| 1 | Unresolved sub_ decompiler stubs | 27 unique, 419+ calls | Shared IL2CPP generic bodies (array getters, singleton getters, coroutine wrapper, GetComponent). Harmless but need manual relabeling for readability. |
| 2 | image3 uninitialized-branch bug | UpdateInventorySlotsUI, ~line 445 | Fixed in decompiler source 2026-09-23: distinct native array-element loads now receive a join phi; both receiver and sprite are assigned on both arms. The promoted r4c tree still shows the old output. |
| 3 | Unvalidated RPC input | Rpc_ChangeItemStorage/Rpc_CMD_ChangeItemStorage | No bounds/range check on invSlot, value, value2 before array write; client predicts locally first. |
| 4 | God-class architecture | whole file, 403 fields, 16,380 lines | Weapons, mop, trash, UI, and 40-item placement system all crammed into InventoryManager. |
| 5 | Hardcoded per-item Template/TemplateRed fields | 204 ...TemplateRed field declarations | Should be a dictionary/ScriptableObject-driven table instead of ~100 hand-declared Transform pairs. |
| 6 | String-typed, hash-compared item RPC | PlaceItem/Rpc_CMD_PlaceItem, 29 distinct big-int hash comparisons (num1 != 39xxxxxxxxx) | Compiled from a switch(type) on string literals; fragile, no compile-time safety, wastes bandwidth sending strings over the wire. |
| 7 | Empty decompiler noise blocks | 200 if (X.initialized == 0) { } stubs, 18 il2cpp_codegen_initialize_runtime_metadata/il2cpp_object_new manual exception-construction blocks | Purely decompiler scaffolding for type initializers and thrown exceptions (e.g. the NotSupportedException in IEnumerator.Reset()); safe to ignore/strip when cleaning up. |
| 8 | Dead/empty conditional | IsValidItemIndex, if (data_183e71c21 == null) { } | No-op branch, leftover static-field init check. |
| 9 | Reference-vs-null array comparison | IsValidItemIndex: StoreManager.__field_Instance.pickupObjs != 0 | Should read as != null; decompiler rendering artifact, not a runtime bug. |
| 10 | Pointless array re-fetch in loop | UpdateInventorySlotsUI, animatorArray1 = this.inventorySlots; re-assigned every iteration | Bounds-check codegen noise, no functional effect, just visual clutter. |
| 11 | Raw unsafe pointer/offset RPC serialization | 419 occurrences of (byte*)/(int*) casts with hardcoded offsets like +0x1c, +0x24 | Normal Fusion RPC codegen, but brittle: any change to SimulationMessage layout or Fusion version silently breaks these offsets. |
| 12 | Bare catch with manual SetException | 1 occurrence, in _Rpc_CMD_PlaceItem_d__288.MoveNext | Swallows the real exception type — typical of decompiled async/IAsyncStateMachine machinery, not something you'd write by hand. |
| 13 | 6 manual NotSupportedException/NotImplementedException throws | e.g. _StopIgnore_d__242.Reset() | Standard IEnumerator.Reset() boilerplate — expected, not a real issue. |
| 14 | Only 11 Debug.LogError guard rails across 16k lines | scattered | Very sparse defensive logging for a class this large and this networked — most array/index accesses have no bounds guard beyond the few IsValidItemIndex call sites. |
| 15 | Inconsistent field naming | inventorySprites vs inventorySprites_ | Trailing underscore suggests a renamed/duplicated field the original devs never cleaned up; easy to swap them by mistake (as arguably happened in issue #2). |

## Addendum — 2026-09-23, session handoff

Three fixes are committed and pushed: join receiver phi (`2481c16`),
paired float Jcc flags (`14e2ae0`), and complete branch-chain local
hoist (`1920c71`). The follow-up scalar parameter-copy inference and
tests are still uncommitted: 30 focused tests passed, while the full
suite was interrupted near 69% and has no final result. Resume from
`docs/handoff-2026-09-23.md` before landing it. The unregistered
`sub_1804cdb00` audio scalar result remains open; do not guess its
identity or regenerate the promoted output.

## Addendum — 2026-09-24, stub code + forwarder returns + r8 ACS

Three source changes landed since (all committed and pushed): shared
stubs list their address's first native instructions as comments (throw
preserved), identical-render method twins collapse to the first row (70
sites), and noreturn-shared `call; int3` forwarders render
`return Target(args)` (all 63 `/* nothing */` in `Arm.cs` Neon).
`final_out/` Assembly-CSharp promoted to r8 (4 files differ vs r7:
ComputeStringHash x3 + stub comments; evidence in
`validation_reports/promotion_r8.json`); rest of tree holds r7. Full
suite: 1013 passed / 0 failed (836 portable + 177 game). Open, by
payoff: same-name multi-owner receiver pick (~1.5k sites), static/
instance+arity ToString/op_Implicit (865 sites, 1 VA), constant-zero
fold (239 sites, 2 VAs). Census table above still scans the r4c/r7
eras; fresh counts live in `docs/todo.md` Current work.
