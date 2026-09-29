# STATUS — V60–V65 complete; no experiment running

Updated 2026-09-26 UTC. Resume here and from the relevant frozen protocol, not the
initial long research report. The user wants credible research for a possible Q2
paper. That threshold is **not established**: no generalizable benefit-aware routing
advantage is demonstrated. Scientific honesty overrides finding a positive score.

## Latest concrete result

V64 completed all **288 physical SAT trials** in 579.614 seconds: 279 independently
validated solutions, 9 retained resource noncompletions, no retries or missing
trials. Thirty classical arms used 400 recorded aggregate acquisitions, five fixed
seeds, shared 10-evaluation prefixes and 20-inclusive budgets. RF-LCB was primary
before timings. planted_256 fails its gate (1/5); planted_512 passes (2/5), with
47.134659% remaining headroom in seeds37/71, approximately43.55ms absolute.

V65 then ran **five real local SmolLM3-3B Q4_K_M requests**, all five admitted-task
prefixes, under a separately approved frozen allowance. Actual collection28.295903s,
including0.833906s startup; 1,091 generated tokens, 3,005 evaluated input tokens.
**0/5 contract-valid outputs; 5/5 paired RF fallbacks; no LLM-attributable gain.**
No new recorded acquisitions were charged because no valid native proposal arm
was evaluated. RF fallback observations reuse already-paid V64 acquisitions.

Every response used a code fence. A labeled post-hoc diagnostic strips that fence
without acquiring labels: all five still reuse observed configurations (5–8 distinct
IDs), four contain duplicates, and none satisfies the unique-unobserved contract.
This does not replace the frozen strict result or create a repaired measured arm.
No retries, prompt changes, hidden-label input, paid inference or fabricated output.
Dedicated model server exited0. All intended requests and failures are retained.

## Other new work in this continuation

- Redis V60/V61: built pinned owner7.2.11, adapted its C benchmark to check every
  value. 486/486 physical invocations valid; 53,460,000 benchmark replies checked.
  Two generated workloads,80settings,three repetitions. RF reaches recorded minimum
  9/10cases; largest remaining gap0.067925%, both frozen gates fail0/5. Stop that grid.
- SAT V62/V63: pinned owner MiniSat core with two saved compiler-declaration fixes,
  search code unchanged. Nine admission invocations: six valid solutions and three
  retained n1024 CPU failures. One disclosed adaptive n512 midpoint; no further
  size calibration. V64 includes both admitted tasks, n256 and n512.
- Redis is one development family. MiniSat is conservatively grouped with exposed
  Z3; generated tasks/seeds are not independent systems. MongoDB/Storm reservations
  remain unadmitted. No fresh held-out group or learned-router validation added.

## Evidence and verification

Reports: reports/redis_v60_v61.md; reports/sat_admission_v62_v63.md;
reports/sat_screen_v64.md; reports/sat_llm_v65.md.
Raw logs: results/v60_redis_feasibility/, v61_redis_physical/, v62_sat_feasibility/,
v63_sat_midpoint/, v64_sat_physical/, v65_sat_llm/.
Classical/paired journals, tables, figures: results/v61_redis_screen/,
v64_sat_screen/, v65_sat_llm_analysis/. PNG/SVG figures visually checked.
Sources/build failures/patches: artifacts/sources/v60/ and v62/; artifacts/study_v60/
and study_v62/. Data/source manifest: data/live_manifest_v60_v65.json.
Frozen protocols and source hashes: reports/protocol_v60 through v65 files.
V64/V65 separate approval receipts are saved; do not reuse their old allowances.

Independent verification passed: all486 Redis receipts and counts; all297 SAT
receipts, every one of285 valid returned SAT models,800 recorded acquisitions,
720 reconstructed classical choices; all5 raw native outputs, strict contract,
paired fallback budgets, model/runtime/input provenance and token/cost totals.
**415 Python tests passed**, including10 new V65 parser/input tests. Four actual
native-client synthetic controls accept valid bytes and reject wrong/nil/type replies;
these are separate test overhead, not measured research outcomes.

Read-only replay (no model/server/solver calls):
```
.venv/bin/python scripts/verify_redis_v61.py
.venv/bin/python scripts/verify_sat_v62.py
.venv/bin/python scripts/verify_sat_v63.py
.venv/bin/python scripts/verify_sat_v64.py
.venv/bin/python scripts/verify_sat_llm_v65.py
.venv/bin/python scripts/seal_evidence_v65.py --verify-only
.venv/bin/python -m pytest -q tests
```
Collectors and primary analyzers are one-shot. Do not delete results to rerun them.
Report renderers can regenerate descriptive figures but alter image metadata bytes;
use a copy if preserving the final evidence seal. No clean-machine reconstruction
of these latest stages is claimed; earlier portable bundles remain historical.

## Costs and preservation

This continuation:783 physical invocations (771valid,12resource noncompletions),
800 recorded aggregate acquisitions,5 real model requests. Separate synthetic and
build/test/audit overhead is retained. Cumulative recorded acquisitions25,758;
model requests1,981; physical compression2,234, Java441/882harness iterations,
planning444, Redis486, MiniSat297. These categories are not interchangeable.
External experiment spendUSD0; hardware/electricity/researcher cost unknown.
Source downloads3,491,269 new bytes; cumulative4,771,462,572 bytes; remaining
597,246,548 under5GiB. Exact new costs: artifacts/study_v65/resource_ledger.json.
Actual table-building/model costs are not deployment estimates. V65 has no finite
observed inference break-even because it yields no improvement beyond fallback.

V58/V59 seals verified via exact prior mutable-document snapshots in
artifacts/study_v59/previous_snapshot/ and study_v60/previous_snapshot/; raw evidence
unchanged. Final V60–V65 seal: artifacts/study_v65/evidence_manifest.json, with
verification receipt beside it. An initial packaging seal mistakenly included its
own changing stdout log; verification caught it. The invalid manifest and erratum
are retained, the exclusion is fixed, and the final seal is independently checked.
No experiment or analysis changed. Future edits must preserve exact snapshots first.
No publication, remote push, cloud spending, service installation or author contact.

## Next action and limits

Single priority: prepare a reliability-preserving legal-proposal interface for a
prospectively frozen **fresh multi-system evaluation**, with matched strong controls.
See reports/next_experiment.md. Existing local model access works; the limitation
is the exhausted5/5 V65 call allowance, its explicit stop-on-exposed-cases rule,
and insufficient independent evaluation groups, not missing model credentials.
Complete admission and a concrete new bounded protocol before requesting more scope.

Untested: constrained legal proposals on fresh systems, stronger/reasoning models,
independent-machine replication, generalizable routing and meaningful net benefit.
Do not tune V65 prompts/decoder/grid after seeing these outputs or claim Q2 readiness.
No background experiment or automatic continuation is scheduled.
