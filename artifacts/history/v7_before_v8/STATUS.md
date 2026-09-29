# Status — 2026-09-24, v7 approved inference completed

## Current state

**All 15 approved real local-LLM continuations completed.** Together with the previously completed 15 matched random controls, the v7 development-only ablation is complete: **300 new objective acquisitions, 15 real model requests, no failures/fallbacks, and 54 passing tests**.

Start with **reports/pilot_report_v7.md**, then reports/protocol_v7.md and relevant v7 code. The latest held-out routing evidence remains reports/pilot_report_v6.md. No held-out outcomes were used to select or fit a v7 policy; no v7 router was trained. Do not reread the initial literature report. Pre-approval status and reports are preserved under artifacts/history/v7_before_approval/.

## Approval and actual execution

The user replied **`approve`** to the explicit request to raise the shared follow-up request cap **100 → 113**, permitting 15 new calls from count 98. Recorded exact approval/scope in configs/authorization_v7.json and snapshotted it at inference start in results/v7/authorization_at_inference_start.json. No older frozen configuration or historical count was changed. The cumulative runtime cap stayed **1,800 seconds**, external spending stayed **USD 0**, and no download/model limits changed.

Executed all five seeds [11,23,37,53,71] on the same MySQL, lrzip and Brotli development prefixes as v6. Same pinned Qwen/Qwen2.5-0.5B-Instruct revision 7ae557604adf67be50417f59c2c2f167def9a775, CPU/float32, greedy decoding, prompt text, ten proposals per request, projection and budget. The only model intervention excluded the original ten prefix feature strings during decoding. Repeated novel proposals within the batch remained permitted.

Each new branch starts from its saved ten-label prefix and acquires ten more labels. All 30 v7 branches (15 uniform-excluded controls + 15 LLM continuations) have logical budget 20 and are retained. This turn added 150 real LLM-branch label acquisitions; prior controls added 150. Historical prefixes and original v6 comparison arms were reused without recharging them as new collection; their prior cost remains recorded.

## Measured result

The intervention prevented copying but did not improve optimization. Across 15 paired development cases:

| Comparison baseline | Mean gain, baseline loss minus v7 loss | Material help | Material harm |
|---|---:|---:|---:|
| Original v6 LLM | -0.001713 | 0/15 | 1/15 |
| Classical continuation | -0.002786 | 0/15 | 1/15 |
| Matched uniform-exclusion control | -0.002251 | 0/15 | 1/15 |

Positive gain favors v7; the frozen material margin is .02 normalized loss. Five seeds are averaged within each of three development families. These are exploratory development results, not a claim about generalization.

On these same 15 cases, original-prefix copies fell **137/150 → 0/150**, as enforced by the constraint. Only **7/150** new raw proposals matched an available recorded candidate, so **143/150** required projection. Absence from the recorded table does not prove a configuration is invalid in the actual software. There were 36 acquired-row collisions, zero duplicate acquisitions and zero fallback acquisitions. Within-batch repeated raw proposals increased from 6 to 14. The post-hoc diagnostic is descriptive; no prompt, threshold or treatment was changed after collection.

Per-family new LLM mean losses: Brotli 0.000500, lrzip 0.002096, MySQL 0.052502. Full per-seed outcomes and comparisons are in results/v7/outcomes.csv. V6 still showed no held-out routing advantage; v7 does not overturn that result.

## Verification, evidence and reproduction

**54 tests passed in 1.32 seconds after approval.** Independent verification replayed all 30 v7 branch states and checked source labels, exact prefixes, prompt equality, dynamic grammar masks/token IDs, raw tokenizer decoding, input-token counts/rendered-prompt hashes, CPU/model revision, approval-before-request timestamps and both budgets. All v4/v5/v6/v7 scientific freezes remain intact. Fifteen precollection real-tokenizer traversals were synthetic checks, never model results.

| Evidence | Location |
|---|---|
| Generated complete report | reports/pilot_report_v7.md |
| Scientific treatment / 97-file freeze | reports/protocol_v7.md; protocol_v7.freeze.json |
| Development-only manifest and reused hashes | data/manifest_v7.json |
| Explicit approval / start snapshot | configs/authorization_v7.json; results/v7/authorization_at_inference_start.json |
| Actual model prompts/responses/tokens | results/v7/request_starts.jsonl; requests.jsonl; model_runtime.json |
| All 300 new charged target accesses | results/v7/acquisitions.jsonl |
| All new complete states / checkpoints | results/v7/llm/; uniform_excluded/; checkpoints/ |
| Complete intended denominator | results/v7/progress.json |
| Results / per-case losses | results/v7/summary.json; outcomes.csv |
| Descriptive proposal diagnosis | results/v7/proposal_diagnostics.json |
| Visually inspected figures | results/v7/comparison.png, .svg; paired_gains.png, .svg |
| Execution/tests/verification logs | artifacts/study_v7/llm_collection.log; tests_after_approval.log; verification_complete.log |
| Actual code snapshot | results/v7/source_snapshot/ |

Commands actually executed after approval:

```sh
PYTHONPATH=src .venv/bin/python -u -m escalation.study_v7 llm
PYTHONPATH=src .venv/bin/python -m pytest -q
PYTHONPATH=src .venv/bin/python -m escalation.analyze_v7
.venv/bin/python scripts/verify_v7.py
.venv/bin/python scripts/diagnose_v7.py
.venv/bin/python scripts/report_v7.py
```

The collector reuses already completed cases and does not repeat calls automatically. Analyses make no new model calls or optimizer acquisitions but consume remaining experiment-runtime allowance. Earlier version-specific verifier ledger checks describe their own execution checkpoint, not a claim that subsequent collection was free. Do not reset counts or delete outputs to rerun.

## Costs and remaining limits

- V7 actual model usage: **13,283 input tokens, 4,050 output tokens**, **148.437 seconds request wall time**; startup/load wall time **4.953 seconds** separately.
- Full v7 controls/collection/analysis/diagnostics ledger time: **159.0124 seconds** (about 157.1104 after this approval).
- Cumulative experiment runtime: **1,630.1201/1,800 seconds**, **169.8799 seconds remaining**; ledger inactive.
- Shared follow-up attempts: **113/113 used — zero remaining**. Historical attempts including v1: **213**. Missing historical failed-request token usage remains unknown.
- Historical charged objective accesses: **3,758** (3,458 before v7 + 300).
- Hypothetical deployment of only the new arm across 15 cases requires 300 logical label accesses including prefixes and 15 requests; this is separate from both-arm research collection and historical baselines.
- Downloads unchanged at 1,412,812,979 bytes, model bytes 999,602,607. **USD 0 external spending.** No new packages, model weights, cloud, credentials, remote push, contact or publication. No worker/background job remains.

## Single most important next action

**Test selection from existing unevaluated candidate rows against generated feature strings, using development data and a matched random-selection control.** That would separate model ranking from the nearest-row projection dominating these runs. It is a proposed next experiment, not implemented or run; see reports/next_experiment.md.

Further model calls require a new explicit allowance because the approved cap is exhausted. A stronger model, empirical nonbinary tasks and adequately broad untouched-system routing remain untested. Existing v6 test families are exposed; do not reuse them adaptively as untouched test data. Nothing is scheduled outside this session.
