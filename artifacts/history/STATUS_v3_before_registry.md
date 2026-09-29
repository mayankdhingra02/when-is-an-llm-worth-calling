# Status — 2026-09-24, corrected exploratory v3 complete

## Actual state

**The requested bounded pilot has run: corrected classical baselines, real local-model paired continuations, controller comparisons, tests, figures and report.** The usable result is exploratory v3. It does **not** demonstrate that benefit-aware routing generalizes or beats simple alternatives. Start with [the v3 report](reports/pilot_report_v3.md).

- **30/30 corrected classical arms**: Apache, SQLite, x264 × seeds 11,23,37,53,71 × random/adapted centroid. Each has exactly 20 unique acquired outcomes and a checkpoint after 10. All system variants/seeds remain grouped.
- **15/15 real paired continuations**, each using the same saved centroid prefix and ten additional acquisitions. Each makes two local Qwen requests producing five configurations apiece. All completed with no provider errors, retries, malformed responses or fallback acquisitions.
- **33 v3 requests**: three separate synthetic format checks plus 30 software-continuation calls. Synthetic quality is excluded from measured aggregates. Generated tokens, raw responses, prompts and constraint schedules are retained.
- **2/15 materially useful and 3/15 materially harmful escalations**, using the predeclared ±0.02 normalized-loss margin. These counts are descriptive; seeds are not independent systems.
- On the sole held-out smoke system, x264, mean loss is random **0.03054**, centroid/never **0.06175**, always-LLM **0.05881**. Lower is better. The development-fitted benefit router selects no escalations, misses the one materially useful case and ties never. Zero-rate matched random is degenerate; uncertainty escalates once but misses the useful case. Hindsight **0.05563** is a non-deployable diagnostic.
- **23 tests passed**. Independent evidence verification passed: dataset schema/hashes, inclusive budgets, deterministic classical replay, prefix equality, exact recorded labels, prompt reconstruction, token decoding/constraints, projection replay and metrics.
- No paid API, cloud resource, remote push, publication, author contact or email. No experiment or model worker remains running. Local Git repository has no remote; files are uncommitted.

## Important correction and version history

The original loader silently dropped SQLite's real `sQLITE_OMIT_AUTOMATIC_INDEX` option because its name ended in X. v1/v2 actually used 38 features and 4,132 configurations, while earlier prose incorrectly claimed the full schema. On discovery, v2 was interrupted, the error documented, explicit schema validation added, and **all 30 classical arms rerun**. Corrected SQLite uses 39 features and 4,652 configurations, excluding one duplicate. See [schema erratum](reports/schema_erratum.md).

- **v1:** 100 attempts (51 dispatched, 50 malformed responses, one timeout, 49 dead-worker failures); ten fallback-only continuations, five blocked. 700 charged label accesses. Historical logs unchanged; affected SQLite/controller conclusions superseded.
- **v2:** constrained JSON feasibility passed; stopped during schema audit. 33 attempts and 58 new labels. Request 33 interrupted, usage unknown. Completed/partial/blocked records are preserved. Do not pool with v3.
- **v3:** corrected schema and fresh prefixes; compact constrained binary strings, five candidates per call. 33 requests and 750 new label accesses. Protocol/source snapshots distinguish the changed treatment. A stale prompt phrase was corrected in preflight before any v3 inference; decisions.md records this. This is an exploratory adaptation after earlier classical outcomes were inspected.

The original STATUS is preserved at artifacts/history/STATUS_v1_before_schema_audit.md. Never treat its obsolete blocker or schema claims as the current state.

## Read first on continuation

1. This file and [reports/pilot_report_v3.md](reports/pilot_report_v3.md).
2. [reports/protocol_v3.md](reports/protocol_v3.md), original [protocol.md](reports/protocol.md), [schema_erratum.md](reports/schema_erratum.md), and [decisions.md](reports/decisions.md).
3. Relevant implementation/tests and [next_experiment.md](reports/next_experiment.md).
4. [source_audit.md](reports/source_audit.md) for verified primary sources; do not reread the supplied literature report without a specific new need.

## Evidence locations

| Evidence | Path |
|---|---|
| Frozen corrected protocol/hash | reports/protocol_v3.md, reports/protocol_v3.sha256 |
| Source audit, licenses, versions | reports/source_audit.md, THIRD_PARTY.md, artifacts/source_manifest.json |
| Explicit dataset schema/group/hash manifest | data/manifest_v3.json; data/raw/ originals are Git ignored |
| Corrected classical logs/schema/prefixes | results/v3/classical/runs.jsonl, *_schema.json, prefixes/ |
| Paired acquired labels and completion | results/v3/runs.jsonl, completed.json, checkpoints/ |
| Real inference provenance/raw tokens/prompts | results/v3/requests.jsonl, request_starts.jsonl, validation.jsonl, model_runtime.json |
| Separate synthetic feasibility gate | results/v3/feasibility/ |
| Executed collection code snapshots | results/v3/classical/source_snapshot/, results/v3/source_snapshot/ |
| Policy choices, fits, tables, costs, figures | results/v3/analysis/ |
| Tests and evidence audits | artifacts/tests_v3_final.txt, result_verification_v3.json, verification_v3.json, verification_v3.log |
| Analysis input/code/output hashes | artifacts/analysis_manifest_v3.json |
| Commands and logs | artifacts/commands.md, classical_v3.log, followup_v3.log, analysis_v3.log, report_v3.log |
| Historical evidence | results/classical/, results/paired/, results/v2/; original ledgers and snapshots retained |

## Reproduce without new inference

From this folder, with the existing project-local environment and pinned data/tokenizer:

```sh
PYTHONPATH=src .venv/bin/python -m pytest -q
.venv/bin/python scripts/verify_results_v3.py
.venv/bin/python scripts/verify_v3.py
PYTHONPATH=src .venv/bin/python -m escalation.analyze_v3
.venv/bin/python scripts/report_v3.py
.venv/bin/python scripts/record_analysis_manifest.py
```

These commands make no model calls or new objective acquisitions. Analysis updates measured runtime in the persistent ledger; refresh the report/manifest afterward. Timing/plot bytes may differ on another machine. README.md documents fresh environment/source/model retrieval. Historical verifiers deliberately use a labeled legacy parser to reproduce what actually happened. Do not overwrite collection logs or reset ledgers.

## Reproducibility and remaining limits

- MOOT commit `90803be51b00f881305db45aa0cf6a3b5340804f`; EZR inspected v0.9.4 commit `bfda80b3b797d142378f7fb8746c3485610fb17e`. No exact SNAP2 repository located in the bounded primary-source audit. Independent code is a paper adaptation, not an exact numerical replication.
- Official Qwen/Qwen2.5-0.5B-Instruct revision `7ae557604adf67be50417f59c2c2f167def9a775`, Apache-2.0, greedy constrained generation, local safetensors, HF offline and no remote code. Legal nonconstant coordinates are selected from model logits; fixed separators do not substitute for LLM choices.
- Python 3.10.13, pinned requirements.lock.txt; torch 2.6.0, transformers 4.49.0, SciPy 1.13.1. Original SciPy 1.15.3/macOS import failure retained. Apple M3 Pro, 18 GB RAM, 14-core GPU. Metal inference requires authorized execution outside the restricted shell. Cross-device generation determinism is untested.
- Follow-up **66/100 attempts consumed; 34 remain**, shared by v2+v3. Original v1 remains 100/100. **166 total historical attempts**; the follow-up did not erase earlier failures.
- Cumulative experiment/analysis runtime **1,156.1367/1,800 seconds**, leaving **643.8633 seconds**. Authoritative ledger: artifacts/resource_ledger_v2.json (despite its name, this includes v3 and carried v1 runtime); active_since is null. Setup, tests, source audit and document rendering are separate overhead, not complete end-to-end researcher time.
- **1,508 cumulative charged label accesses**: v1 700 + v2 58 + v3 750. Both continuation branches count when they acquire overlapping rows. These are recorded-table lookups, not live system measurements.
- v3 observed tokens **32,809 input + 3,685 output**, request wall time **313.79 seconds**. Whole-history token usage remains unknown due to v1 timeout and interrupted v2 request. Missing usage is not zero.
- Payload remains 999,602,607 bytes; total accounted setup downloads 1,286,573,416 bytes, under 4 GiB model / 5 GiB overall limits. No new downloads in the follow-up. External experiment spending **USD 0**; electricity, depreciation and Codex usage costs unknown.
- Deployment costs are selected-branch trace estimates, separately labeled from actual paired research collection. Model loading/training data are not claimed free. No standalone deployed service was timed.

## What remains untested

Credible generalization across independent software systems; source-paper model/artifact equivalence; stronger local models; unconstrained proposal reliability; projection-only ablation (141/150 proposals needed projection); numeric/categorical or multi-objective data; other budgets; live application runtime/cost; pretraining contamination and original workload/hardware provenance. Three systems and five seeds are a smoke test, not a meaningful held-out learned-router evaluation. Passing constrained formatting tests does not establish optimization reasoning.

## Single most important next action

**Freeze a larger evaluation on untouched software-system groups, with an explicit system/variant/schema registry and a projection-only baseline.** Use this pilot's mixed gains and high projection rate to specify the question before new collection. Review model/artifact alignment and set a new resource plan first; do not spend the remaining allowance tuning against x264. Details are prioritized in reports/next_experiment.md. No work is promised outside this active session.
