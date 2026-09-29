# Status — 2026-09-24, expanded-grid follow-up complete

## Resume here

Read **reports/expanded_grid_v17.md** and **reports/review_note.md**. The bounded pilot and this continuation are complete. No demonstrated useful LLM selection or benefit-router advantage. The latest work actually collected846 new physical trials and ran30 classical arms. This is a negative development result with preserved raw evidence, not a reason to keep changing grids until positive.

## Latest execution

V17 prospectively froze one larger grid before measurements:96 Zstandard,96 LZ4 and90 zlib settings, strict supersets of V15. Three fresh randomized repetitions per setting on the unchanged pinned901120-byte CPython archive. **846/846 succeeded with exact decoded-byte equality**, all compressed outputs saved. No retries/failures/timeouts/unattempted cases. Median timing CV:1.87%/2.39%/2.81%;8 settings above10% diagnostic, none excluded. Distinct outputs96/60/75; nominal configurations are not necessarily distinct behaviors.

Then **15 cases/30 classical arms**, five seeds per family,20 labels including shared checkpoint10. **450 recorded-vector accesses**, independently replayed against source medians. Cheap-minus-random runtime gain means:+0.499% Zstandard,+0.592% LZ4,0% zlib. Mean remaining full-table feasible hindsight headroom:0.537%,0.197%,0%; maximum case1.132%, none above10%. Small effects need caution given timing variation and three repetitions. No claim of superiority/equivalence, LLM benefit or generalization.

All three families, all variants and seeds are development/exposed. Future audits must include data/live_manifest_v15.json and data/live_manifest_v17.json alongside V3/V6. One small workload; no new independent held-out systems. Parameter-list construction moved outside CLI timing in V17; no direct V15/V17 runtime comparison.

## Evidence and commands

**120 tests passed before collection.** All15 source freezes/1038 references intact.846 saved payload digests,282 medians,450 lookup charges and all30 optimizer paths verified. Both figures visually inspected. No live workers or scheduled jobs remain.

```sh
PYTHONPATH=src .venv/bin/python -m pytest -q
.venv/bin/python scripts/collect_live_v17.py
.venv/bin/python scripts/analyze_live_v17.py
.venv/bin/python scripts/run_classical_v17.py
.venv/bin/python scripts/analyze_verify_classical_v17.py
.venv/bin/python scripts/render_expansion_v17.py
.venv/bin/python scripts/verify_expansion_v17.py
```

These are the commands that actually ran. Completed collectors refuse/reuse output to prevent recollection. Read REPRODUCE.md before rerunning; analysis guards preserve original outputs. No ledger reset is authorized.

- Protocol/source hashes: reports/protocol_v17_expansion.md/.freeze.json; configs/live_measurement_v17.json.
- Features: data/live_manifest_v17.json. Workload/binary provenance remains artifacts/study_v15/workload_manifest.json and environment.json.
- Physical raw/charges/schedule/complete denominator: results/v17_measurements/; compressed bytes artifacts/sources/live_v17/outputs/ (Git ignored).
- Prefixes/arms/charges/all outcomes/figure: results/v17_classical/.
- Logs/tests/verification/accounting/evidence index: artifacts/study_v17/.
- Mutable docs before this continuation: artifacts/history/v17_before_expansion/.
- Harmless emitted filename physical_analysis_ledger_ledger.json is preserved. Pre-freeze generation assertion was fixed before any collection; no measured trial failed.

## Current resource ledger

New this continuation: **846 physical trials +450 recorded accesses,0 model requests,45.4948 charged experiment seconds,0 downloads,USD0 external spend**.

Cumulative **1134 physical-vector attempts +5408 recorded-table vector accesses** (6542 combined, distinct cost types). Inference remains **128/128** follow-up attempts,228 including initial stage. Runtime **1743.8069/1800seconds**, **56.1931seconds remaining**, active_since null. Download ledger unchanged1415316681bytes,999602607 model bytes. No package installation, paid/cloud inference, credentials, remote contact/push/publication or system changes.

Dataset-construction cost is separate from a modeled20-acquisition deployed arm. No new LLM cost or deployment savings are estimated here.

## Prior evidence preserved

Original corrected V3 three-system/five-seed paired smoke and V6 held-out router evaluation ran with real local Qwen. V6 benefit/uncertainty select zero escalation; no router advantage. V8 all15 direct-selection outputs choose IDs0–9; trivial first-half selection exactly reproduces choices. V9 exact random-subset reference matches/beats each observed LLM score with probability≥0.5 (conditional diagnostic, not p-values). V10–V14 utility/headroom/admission audits and all earlier schema/model failures retained. V15 collected288 physical trials; V16 added450 recorded accesses and showed little headroom in32-setting spaces. None of these is a SNAP2 numerical replication or a demonstrated positive LLM routing result.

## Single next action and untested work

**Review reports/review_note.md with Tim and agree on an application-grounded runtime/size task before another campaign.** This is a discussion document, not sent to anyone. The single expanded-grid stop rule is now satisfied; do not keep broadening settings based on observed results or reset limits on generic continuation.

Untested: application-approved utility, broader realistic workloads, precise timing uncertainty, stronger-model/candidate-order tests, enough untouched systems for controller generalization, live deployment costs/benefit. Further inference is blocked by the128-request allowance; no new permission or positive result is inferred. Original pilot is ready for review; no automatic work continues outside this session.
