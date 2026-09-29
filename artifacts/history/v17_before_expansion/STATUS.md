# Status — 2026-09-24, live measurements and paired controls complete

## Resume here

Latest reports: **reports/live_measurements_v15.md** and **reports/classical_controls_v16.md**. The user requested continuation; this time we built/executed a real local measurement campaign and immediately checked paired classical continuation on the resulting data. There is a positive infrastructure-feasibility result, but still **no demonstrated useful LLM selection or benefit-router advantage**.

## What actually ran

**V15 physical collection:** installed Zstandard1.5.7, LZ4 1.10.0 and Python zlib1.2.12;32 predefined configurations per family ×3 trials = **288/288 physical trials**. Input: a901120-byte deterministic archive of three unmodified CPythonv3.10.13 source files, pinned to49965601d6afedafe47cc85556d99b7a24981051. All actual outputs passed exact decoded-byte equality, with no failures/timeouts. Every compressed payload is saved. No free warmups/retries.

Median within-setting timing CV: **1.64% Zstandard,1.48% LZ4,1.13% zlib**. One setting exceeds the predeclared10% noise flag. Three trials only; do not claim precise uncertainty or representative production performance. Distinct output digests:32/20/24 respectively from32 nominal settings each. CLI timing includes launch/pipes; zlib timing uses its API. No cross-family speed ranking is claimed.

**V16 paired classical test:** all three new tables/all five fixed seeds;15 cases/30 arms, budget20 and shared checkpoint10. Prefix uses reference+three random acquisitions+six joint3NN steps, then paired joint3NN/random continuations. Every oracle lookup is charged; **450 new recorded-vector accesses**. Independent replay verified all source labels, acquired-only choices, identical prefixes and budgets.

Cheap versus random mean relative gains: Zstandard **−0.00384%**, LZ4 **+0.00321%**, zlib **0%**. Effectively tied at the resolution of this small measurement study; no formal equivalence/significance claim. Mean full-table feasible hindsight headroom after cheap continuation: **0.2753% Zstandard,0% LZ4,0% zlib**. None above10%. This32-setting/single-workload space gives little selection opportunity; no additional inference is justified on this setup.

All three new families are **development/exposed** in data/live_manifest_v15.json. Future exposure audits must include this manifest alongside V3/V6. Do not call them untouched test families. Shared implementation dependencies still need consideration before claiming independent-system generalization.

## Verification, commands and artifacts

**116 tests passed.** V15 initially caught/fixed a trial-ID scheduling bug before source freeze/collection; preserved note under artifacts/study_v15/. The first render warned about a font cache, used a temporary cache, completed and charged its time. Later presentation rerender uses project-local caches. These were not missing or failed physical measurements. Completed collector reuse was tested and made no extra trials.

```sh
.venv/bin/python scripts/fetch_workload_v15.py
.venv/bin/python scripts/collect_live_v15.py
.venv/bin/python scripts/analyze_live_v15.py
.venv/bin/python scripts/render_live_v15.py
.venv/bin/python scripts/run_classical_v16.py
.venv/bin/python scripts/analyze_verify_classical_v16.py
PYTHONPATH=src .venv/bin/python -m pytest -q
```

- Physical raw records/charges/fixed schedule: results/v15_measurements/trials.jsonl, acquisitions.jsonl, schedule.json, progress.json, complete.json.
- Actual compressed bytes: artifacts/sources/live_v15/outputs/; provenance/digests in raw records. CPython sources/license/archive under artifacts/sources/live_v15/cpython/ (Git ignored).
- Physical setting summaries/figure: results/v15_measurements/configuration_summary.csv, summary.json, timing_variability.png/.svg.
- New optimizer raw prefixes/arms/charges: results/v16_classical/prefixes/, joint_3nn/, random/, acquisitions.jsonl.
- New control outcomes/complete denominator: results/v16_classical/outcomes.csv, summary.json, progress.json.
- Frozen inputs/code/protocol: reports/protocol_v15_live.md/.freeze.json; reports/protocol_v16_classical.md/.freeze.json. Feature/exposure manifest: data/live_manifest_v15.json.
- Execution/tests/replay: artifacts/study_v15/collection.log, analysis.log, tests.log, verification.json, render.log; artifacts/study_v16/collection.log, analysis_verification.log, precollection_tests.log, verification.json.
- Current costs/index: artifacts/study_v16/final_accounting.json, evidence.json. Prior mutable docs: artifacts/history/v15_before_live_measurements/.

## Costs and limits

This continuation: **288 physical-vector attempts +450 recorded-vector lookups**, **0 model requests**, **26.8343seconds** of charged collection/analysis/render time and **914260 new download bytes**. Prior4508 recorded accesses remain counted. Current totals: **4958 recorded-table accesses +288 physical trials** (5246 combined, with cost types kept distinct).

Model allowance **128/128 exhausted**,228 historical attempts including initial stage. Experiment runtime **1698.3121/1800seconds**, **101.6879seconds remaining**, ledger inactive. Downloads **1415316681bytes**, model bytes unchanged999602607, external spendUSD0. No packages/models installed, paid/cloud inference, credentials, system settings, contact, push or publication. No background worker remains; nothing is scheduled.

## Earlier evidence remains unchanged

V3 corrected three-system/five-seed paired smoke completed. V6 has three independent held-out families and no router advantage (benefit/uncertainty choose zero escalation). V8 all15 direct-selection model outputs choose IDs0–9; V9 exact uniform reference shows random subsets match/beat every observed model result with probability≥0.5 (conditional diagnostic, not p-value). V10–V12 metric/quality audits and constrained controls remain separately labeled. V13.1 found no untouched size-bearing family in the81-table registry. V14 pinned three external sources but admitted none: published450 measurements represented only one configuration per codec/input context; execution commit was unknown. All earlier failures/schema errata and scientific freezes are preserved.

## Single next action / untested

**Specify a more demanding development task/candidate space with a justified runtime/size utility, and establish headroom beyond cheap search before any new inference.** V15 demonstrates that a small correctness-aware local dataset can be collected; V16 shows the present32-setting spaces are nearly saturated by cheap search. Do not expand/select tasks until a favorable LLM score appears. Further changes must be prospectively frozen and exploratory; reserve genuinely untouched evaluation families.

Untested: application-approved utility, broader workloads/configuration spaces, sufficiently repeated timing uncertainty, stronger models/new-order responses, other evaluation budgets, live deployment benefit and broad router generalization. The original bounded pilot is complete; a positive LLM research claim is still unsupported.
