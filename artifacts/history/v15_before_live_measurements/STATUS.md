# Status — 2026-09-24, external artifact audit complete

## Resume here

Latest: **reports/external_admission_v14.md**. The original bounded optimization pilot is complete; useful LLM selection and a benefit-router advantage remain unestablished. The latest continuation investigated the missing new-family dataset rather than consume an unspecified model allowance.

## What actually ran this continuation

Pinned and inspected three primary-owner repositories: compression-codec-benchmark, PDS-Throughput and lzbench. Downloaded inventories, licenses, selected source/configuration/methodology files and one published raw benchmark CSV. No upstream code was executed.

Implemented and executed a metadata-only coverage/provenance audit. Published codec CSV: **540 rows = 90 warmups + 450 measurements**, **90 codec/input contexts**, **15 inputs**, **6 codecs**, but only **one measured configuration per context** with five repetitions. **Zero contexts support20 distinct evaluations.** Execution manifest records unknown Git commit/null dirty state; a pinned download does not repair that history. PDS scripts/PDFs and lzbench's raw-looking regression/log files did not supply a qualifying optimization table. All three artifacts remain unadmitted; this was a bounded search, not proof of global absence.

**108 tests passed** (six new synthetic metadata checks). Runtime/size outcome values were not converted, ranked or aggregated. There were **0 new model calls and0 new optimizer acquisitions**. Initial sandbox DNS failed, then normal network escalation permitted public retrieval; see artifacts/study_v14/network_attempts.json and fetch logs.

Executed:

```sh
.venv/bin/python scripts/fetch_admission_sources_v14.py
.venv/bin/python scripts/fetch_admission_files_v14.py
.venv/bin/python scripts/fetch_admission_edge_files_v14.py
.venv/bin/python scripts/audit_external_admission_v14.py
PYTHONPATH=src .venv/bin/python -m pytest -q
```

## Evidence

- Latest report: reports/external_admission_v14.md.
- Frozen main audit: reports/protocol_v14_external_admission.md/.freeze.json.
- All90 contexts and explicit coverage/provenance fields: results/v14_external_admission/summary.json.
- Owner commits, URLs, Git blobs, hashes: artifacts/study_v14/source_inventory.json, source_files.json, source_edge_files.json. Raw third-party files: artifacts/sources/admission_v14/ (Git ignored).
- Actual audit/tests: artifacts/study_v14/audit.log, verification.json, tests.log.
- Costs: artifacts/study_v14/accounting.json; current final index: artifacts/study_v14/evidence.json.
- Previous mutable documents preserved: artifacts/history/v14_before_external_audit/.

## Established prior results

- Corrected V3: three systems × five seeds; budget20/checkpoint10; real paired classical/local-model smoke.
- V6: three development/three held-out families. Never-escalate held-out loss0.06150 vs always0.07458; benefit/uncertainty policies choose zero escalation. No selective advantage; only three independent test groups.
- V8: all15 real direct-selection responses choose the first ten displayed IDs. Model-free first-half rule reproduces every observed choice.
- V9: exact uniform reference enumerated184756 subsets/case; random matches/beats each observed model result with probability at least0.5. Conditional diagnostic, not a p-value.
- V10–V12: metric/headroom audit and20 actual constrained cheap continuations/300 new joint-vector accesses. Classical gain vs random:+4.82% lrzip,−2.79% Brotli,+1.01% overall; mixed descriptive result, no LLM finding. Remaining full-table hindsight headroom:0.37% lrzip,9.09% Brotli.
- V13.1: all81 registered tables audited. Four size-bearing tables belong to three already exposed families; zero untouched size-bearing families. Corrected legacy `heldout_smoke` omission; all nine exposed families retained. First V13 pass preserved as superseded.

Full review: reports/decision_brief.md. Raw optimization evidence and real model responses remain in results/v3/, results/v6/, results/v7/, results/v8/. Later analysis/controls are separately namespaced. All historical failures/schema errata remain intact; repeated seeds are not independent systems.

## Costs and limits

Follow-up requests **128/128 exhausted**,228 including initial attempts. Historical optimizer accesses **4508**. Recorded experiment/analysis runtime **1671.4778/1800sec**, **128.5222sec remaining**; experiment ledger unchanged/inactive. This source audit adds **1589442 payload bytes**; persistent total **1414402421 bytes**, model bytes unchanged **999602607**. These downloads remain within the5GiB cap. External spendUSD0. Source inspection/tests are not benchmark collection time.

No new inference, physical benchmark, credentials, cloud resource, contact, push or publication. No worker remains running and nothing is scheduled outside this session. Additional inference requires a concrete allowance; generic continuation does not change caps.

## Single next action / untested

**Specify a bounded new measurement campaign with sufficient configurations per new software family**, using the task/utility and family-admission checks before collecting outcomes. Existing published benchmarks inspected here do not fill that gap. Validate harness/configuration coverage, correctness, workload identity, raw repetitions and resource preflight; do not count different files/codecs/repetitions as extra settings of one system. The source-owner lzbench tool is a candidate, not an installed or selected implementation.

Still untested: this new campaign, application-approved utility, live correctness/noise in our environment, stronger models, reordered prompts, other budgets and broad router generalization. Scientific honesty overrides producing a positive score.
