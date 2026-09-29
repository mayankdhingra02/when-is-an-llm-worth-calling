# Status — 2026-09-24

## Actual state

Implemented and executed the bounded pilot. **Classical work complete; LLM format/recovery feasibility failed; held-out benefit-router evaluation blocked.** No scientific evidence that benefit-aware escalation works. Negative engineering findings are documented in [reports/pilot_report.md](reports/pilot_report.md).

- 30/30 classical arms completed: Apache, SQLite, x264 × seeds 11,23,37,53,71 × random/adapted centroid. Each used exactly 20 unique objective acquisitions, including initialization, with saved 10-label prefixes.
- 10/15 hybrid continuations completed on development groups, all 100 continuation acquisitions by classical fallback. All paired gains are zero due to fallback, not successful LLM optimization.
- 100/100 counted request attempts: **51 dispatched**, **50 actual responses (all malformed)**, **1 timeout**, **49 worker-unavailable failures before dispatch**. The worker was not restarted after the timeout; this is a harness recovery limitation. Do not interpret this as 100 real generations.
- All five x264 LLM continuations are blocked, explicitly retained in the denominator. No held-out policy comparison or oracle headroom result exists.
- Benefit/uncertainty controllers and ablations implemented; development-only ridge fits ran and are degenerate (zero gain targets). Prospective x264 choices are explicitly UNEVALUATED.
- 18 synthetic tests passed. Independent saved-result verification passed: table hashes, actual labels, logical budgets, prefix equality, deterministic replay, metric recalculation, and real local inference provenance. Exact executed code snapshots match manifest hashes.
- No remote, paid API, cloud resource, author contact, publication or push. Local Git repository initialized on main; files are not committed. No background model server or experiment remains running.

## Read first on continuation

1. This file.
2. [reports/protocol.md](reports/protocol.md) and [reports/decisions.md](reports/decisions.md).
3. [reports/pilot_report.md](reports/pilot_report.md), then relevant code under src/escalation/.
4. Consult [reports/source_audit.md](reports/source_audit.md) for verified sources; do not reread the full supplied report unless a new question requires it.

## Evidence locations

| Evidence | Path |
|---|---|
| Frozen protocol and checksum | reports/protocol.md, reports/protocol.sha256 |
| Sources, differences, licenses | reports/source_audit.md, THIRD_PARTY.md, artifacts/source_manifest.json |
| Dataset commit/hashes/groups | data/manifest.json; original CSVs in data/raw/ (Git ignored) |
| Classical raw runs/schema | results/classical/runs.jsonl, results/classical/*_schema.json |
| Frozen prefixes/features | results/classical/prefixes/*.json |
| Paired status and acquisitions | results/paired/runs.jsonl, completed.json, checkpoints/*.json |
| Real model provenance and raw text | results/paired/request_starts.jsonl, requests.jsonl, validation.jsonl, model_runtime.json |
| Measured tables/figures | results/analysis/method_summary.csv, paired_gains.csv, costs.json, quality.png, paired_gains.png, reliability.png |
| Unusable/unevaluated routing evidence | results/analysis/router_blocked.json, *_UNEVALUATED.json, prospective_choices_UNEVALUATED.csv |
| Tests and independent audits | artifacts/tests_all.txt, result_verification.json, verification.log |
| Commands, setup failures | artifacts/commands.md, install.log, scipy_compat_install.log, model_startup_failure.log, paired_run.log |
| Executed code/environment snapshots | artifacts/code_snapshots/{classical,paired}/; original hashes in run manifests |
| Prioritized next steps | reports/next_experiment.md; discussion note is unsent |

## Versions and adaptations

- Protocol v1 frozen before outcomes; exact SHA in reports/protocol.sha256 and both run manifests.
- MOOT: 90803be51b00f881305db45aa0cf6a3b5340804f. Selected named tables before optimizer outcomes; keep first duplicate feature row, independent of labels. SQLite has 4,652 unique configurations after one exclusion.
- Inspected EZR v0.9.4: bfda80b3b797d142378f7fb8746c3485610fb17e. Upstream code was not executed. The independent centroid implementation uses acquired-label min/max normalization and an inclusive budget. No exact SNAP2 artifact located in the bounded audit.
- Real model: official Qwen/Qwen2.5-0.5B-Instruct revision 7ae557604adf67be50417f59c2c2f167def9a775, Apache-2.0, torch 2.6.0, transformers 4.49.0, Metal float16. Greedy generation; no promise of cross-device determinism.
- Python 3.10.13; dependencies fully pinned in requirements.lock.txt. SciPy 1.15.3 failed import on macOS 27; 1.13.1 fixed it before any model output. Original failure and original lock are preserved.
- Apple M3 Pro, 18 GB RAM, 14-core GPU. MPS requires authorized execution outside the restricted shell. Inference uses local files, no remote code, no credentials and offline HF settings.

## Reproduce without new inference

From this folder:

```sh
PYTHONPATH=src .venv/bin/python -m pytest -q
.venv/bin/python scripts/check_integrity.py
.venv/bin/python scripts/verify_results.py
PYTHONPATH=src .venv/bin/python -m escalation.analyze
.venv/bin/python scripts/write_report.py
```

Analysis reads real saved records; it does not acquire objectives or call a model. Its measured runtime is added to the ledger. Setup/fresh-reproduction commands and exact pinned downloads are in README.md. Do not overwrite or delete raw logs to rerun collection.

## Resource accounting and remaining limits

- Persistent cap: **100 of 100 request attempts consumed; zero remain.** It was conservatively charged even when a dead worker prevented dispatch. Do not reset the ledger or reinterpret undispatched attempts as free capacity after seeing outcomes.
- Recorded cumulative collection/analysis time is about **528.3 seconds of 1,800**, including failed startup, leaving about **1,271.7 seconds**. Read artifacts/resource_ledger.json for the exact current value; repeat analysis adds time. Setup, tests, audit and first rendering overhead are separate, not silently counted as measured runtime.
- Actual collection: **700 charged label accesses**, versus 495 distinct configurations summed per dataset/seed. Both branches' acquisitions remain charged when they overlap. No live application evaluation costs were measured.
- Observed completed-response tokens: **49,079 input + 4,846 output**. Whole-study token usage is unknown because timeout usage is unavailable.
- Model payload: **999,602,607 bytes** (~0.93 GiB), below 4 GiB. Total accounted setup downloads including a conservative allowance: **1,286,573,416 bytes** (~1.20 GiB), below 5 GiB. Pip sizes are rounded; exact network transfer is not claimed. Subsequent owner-file downloads have a persistent guard in scripts/download_guard.py, seeded from the existing accounting.
- External experiment spending **USD 0**. Electricity, hardware depreciation and Codex usage cost unknown.

## Single most important next action

**Approve a new, explicitly bounded development-only format-feasibility experiment to obtain valid real-model proposals, with worker recovery specified before collection.** Consider constrained decoding or a more capable local model. The current request cap is exhausted; this session must not continue inference under it. Freeze a new protocol before changes, preserve this negative v1 result, and do not tune against x264 outcomes. Then plan a larger evaluation with many independent software groups.

No claim that work will continue outside the active session. No messages have been sent to Tim Menzies or anyone else.
