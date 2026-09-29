# STATUS — V91 Qwen3-8B comparison completed

## Resume here

User approved “okay do it” after the concrete resource proposal and hardware discussion. The owner-pinned model was downloaded and verified. **All 30 cases completed: 300 scientific requests, three separate compatibility requests, 300 new recorded outcomes, no fallbacks or retries.** Report: `reports/qwen_v91.md`. Raw outputs: `results/v91_qwen/`. Analysis and figures: `results/v91_analysis/`.

**Result:** equal-family mean gain +1.221% versus SmolLM3-3B and the presentation-first-ten rule, but −1.259% versus same-pool batch 3NN and −3.203% versus full-domain sequential 3NN; −1.363% versus historical Qwen1.5. The frozen primary screen failed. Wins/ties/harms: 2/18/10 versus batch; 5/12/13 versus full sequential. Six exposed families, five seeds each: not independent held-out evidence or Q2 readiness.

Qwen3 selected the first ten displayed IDs in 21/30 cases and matched that rule’s final target in 24/30. Choices changed in some cases, but loss responsiveness and order stability for this model remain untested. **Next scientific action:** prepare a bounded Qwen3 loss/order diagnostic on the original development groups using V48/V49’s controlled design. Do not repeat completed SmolLM3 diagnostics or select favorable cases. All 303 V91 requests are consumed; additional inference requires a new bounded allowance. Routine independent implementation remains authorized.

## What actually ran

- Owner revision `7c41481f57cb95916b40956ab2f0b139b296d974`; Q4_K_M model SHA256 `d98cdcbd03e17ce47681435b5150e34c1417f50b5c0019dd560e4882c5745785`, 5,027,783,488 bytes. Exact license, README and pointer retained; Apache 2.0. No downloaded installer executed.
- Existing llama.cpp b11146, local loopback, single slot, non-thinking greedy selection, 4,096 context. Full GPU offload requested; actual device residency not enumerated in logs. One control-token metadata warning retained; tokenization, context and response checks passed.
- Frozen 471 inputs before any generation: `reports/protocol_v91.freeze.json`. Exact V41/V47 messages, pools and ten-observation prefixes; 20 logical evaluations per branch. Collector never read target tables. All 11 comparators and 18 frozen policy summaries retained; no router refit.
- Inference lifecycle 238.415 seconds, startup 4.097 seconds, scientific request wall sum 233.002 seconds. Peak sampled server RSS 5,952,241,664 bytes (~5.95 GB), below 8 GiB guard. No concurrent managed compute during inference.
- Generated 303 tokens including probes. Scientific full-context token sum 495,610; actual prefill count reported as 49,831. All 404 HTTP calls include metadata/health. Server exit 0; no process left running.
- Independent verification: 300 source outcomes, 300 research responses, 330 paired contrasts and 18 policies. Additional runtime/cost audit checks all 303 charges, three probes, model hash and budgets. Receipts under `artifacts/study_v91/`.
- **685 tests passed in 21.61 seconds**, log `artifacts/study_v91/tests_final.log`. Precollection tests and additional guard tests passed before freeze. Synthetic tests/probes are excluded from research aggregates.

Commands executed with `.venv/bin/python`: `scripts/check_resources_v91.py`, `scripts/fetch_qwen_v91.py`, `scripts/freeze_qwen_v91.py`, `scripts/collect_qwen_v91.py`, `scripts/analyze_qwen_v91.py`, `scripts/verify_qwen_v91.py`, `scripts/audit_runtime_qwen_v91.py`, `scripts/report_qwen_v91.py`; full tests `-m pytest -q tests`. Initial zero-byte DNS and precollection process-monitor sandbox denials were resolved with actual execution approval. No scientific request was retried.

## Limits and totals

Approval `artifacts/study_v91/approval.json` binds the proposal hash and user message. Cumulative download ceilings are now **10 GiB total / 9 GiB models**. The immutable historical proposal and pilot files remain unchanged; the approval is an explicit stage override. It does not authorize unlimited future inference. V91’s 303 generation requests are fully consumed.

New payload: 5,027,802,744 bytes, including 19,256 metadata bytes. Cumulative total: **9,867,753,109 bytes**, with **869,665,131 remaining** under 10 GiB. Cumulative model payload: **9,126,358,023 bytes**, with **537,318,393 remaining** under 9 GiB. The old `artifacts/download_ledger.json` is a historical subtotal; use the current pinned base plus V91 receipt for current accounting. Qwen3 weights are now local, so reusing them needs no download.

Real model requests: **2,494** (2,191 + 303). Recorded-table acquisitions: **26,658** (26,358 + 300). Native counts unchanged: DuckDB 78 physical (77 valid, one timeout; preserve V89’s 71 unattempted entries separately), H2 299 (298 valid, one failure; eight unattempted), Kanzi 1,265, RocksDB 350. Actual external spend USD 0; electricity/hardware unknown. No cloud, credentials, publishing, pushing or contacting authors authorized.

## Remaining evidence gaps and integrity

V86’s scoped native negative result remains separate from this recorded-table robustness result. Do not pool settings or claim universal LLM failure. Qwen3 has not had the V48/V49 loss/order diagnostic; independent untouched systems, native clean-machine replication and meaningful held-out routing still remain absent. The broad research goal is not complete. Close the small V90 DuckDB domain; preserve its baseline instability and the V89 timeout/test-overlap confound.

Exact previous root documents are preserved in `artifacts/study_v91/previous_snapshot/`. Current integrity command: `.venv/bin/python scripts/seal_qwen_v91.py --verify-only`. All older frozen inputs/manifests remain immutable. See `reports/next_experiment.md` for the next scientific action. This bounded run needed no hardware upgrade; that is not a guarantee for other workloads or context lengths.
