# STATUS — V85 real-model batch completed and validated

## Resume here

The user explicitly approved the frozen V85 allowance with “apporved”. Grant: `artifacts/study_v85_execution/user_approval.json`. The real batch completed, not blocked on that old permission: **35 real SmolLM3-3B calls, 115/115 valid fresh H2 trials, five seeds, 284.825 seconds, USD 0 and no downloads**. Server exited 0; no model/native process remains running. The broad research objective remains incomplete; Q2 readiness is unproved.

Read `reports/h2_v85.md`, `reports/next_experiment.md` and the unchanged `reports/protocol_v85.md`. Main result: **0/5 material LLM gains at the frozen 10% margin versus either RF or the cheap prior**. Mean paired gain +0.13% versus RF and −1.53% versus prior; extra selection time versus RF 11.55 seconds/case. RF/LLM chose exactly the same configuration in four seeds; all final configurations used index mask 56. One RF repeat set failed the coarse precision screen and was retained. These are descriptive results for one exposed development family, not a generalization/equivalence result or successful learned router.

## Executed commands and evidence

- `.venv/bin/python scripts/run_h2_v85.py --approved-envelope-sha256 e8ac5ce395f5d36a5f319ecc496a76a7fa54c14a3a972a30bf8d90b5db8f1e17`: initial sandbox `ps` permission denial before model/native/output startup; identical approved escalated rerun completed. Launch record in `artifacts/study_v85_execution/launch.json`. No experimental retries.
- `.venv/bin/python scripts/analyze_h2_v85.py`: passed full frozen semantic reconstruction, all 706,560 scored SQL answers, legal model proposals, acquired-only prompts, RF replay, prefix identity, order and budgets.
- `PYTHONPATH=src .venv/bin/python -m pytest tests -q`: **625 passed in 22.11 seconds**; log `artifacts/study_v85_execution/tests_all.log`. Synthetic fixtures remain separate.
- `.venv/bin/python scripts/report_h2_v85.py`: actual comparison tables, modeled deployment scenarios, PNG/SVG figures and report. No new model/native calls.
- `.venv/bin/python scripts/seal_h2_v85_execution.py --verify-only`: current evidence and historical snapshot verification. The execution sealer explicitly resolves retained snapshots without modifying old manifests.

Raw genuine requests/responses, rendered prompts/token IDs, native outputs, locks and receipts: `results/v85_h2_paired/`. Validated summaries, all repeats, CSV scenarios and figures: `results/v85_h2_analysis/`. Report: `reports/h2_v85.md`. Grant, cumulative costs, tests and exact prior root-document snapshots: `artifacts/study_v85_execution/`. V85 protocol/model/runtime/source pins unchanged.

## Actual costs and limits

115 new physical trials = 70 search + 30 RF/LLM confirmations + 15 prior trials. Fifty historical prefix physical trials reused in both branches; 215 logical charges including those prefixes. Zero invalid model proposals, retries, failed native trials, fallbacks or new unattempted cases. Actual native time 220.638 seconds; selection 59.870 seconds; startup 1.995 seconds. Observed tokens 24,239 evaluated and 298 predicted, no missing usage; 111 total HTTP requests including health/template/tokenization. Peak sampled model RSS 2,332,852,224 bytes.

Cumulative real model calls **2,191**; H2 physical **299** (298 valid, one retained historical failure), eight historical unattempted. Kanzi 1,265/RocksDB 350 physical trials and recorded-table acquisitions 26,358 unchanged. Artifact downloads 4,817,487,882 bytes; 551,221,238 remain under 5 GiB. New downloads/spending 0; electricity/hardware costs unknown. Modeled deployment in the analysis is separate from actual collection.

V85’s generation and physical-trial allowances are exhausted. No automatic allowance extension, paid API, cloud provisioning, publish/push or contact. Older preparation documents accurately describe their historical pre-approval state; this STATUS supersedes them for resuming.

## Single most important next action

Admit a realistic, independently sourced development workload and establish measurable residual optimization opportunity against strong cheap controls before another LLM batch, reserving separate system groups untouched. See the prioritized plan. More seeds or bookkeeping on this exposed H2 workload cannot establish the proposed routing contribution. Stronger-model robustness, independent held-out benefit evidence, practical deployment utility, clean-machine native replication and defensible novelty remain untested.
