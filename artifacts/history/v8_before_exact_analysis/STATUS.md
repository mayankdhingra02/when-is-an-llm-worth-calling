# Status — 2026-09-24, approved V8 comparison complete

## Resume here

**All 15 approved real local-model cases completed.** The frozen V8 experiment now contains 45 completed branches (15 uniform-selection controls, 15 static-rank controls, 15 LLM continuations), **450 new target acquisitions**, 15 real requests, no errors/retries/fallbacks, and **64 passing tests**. Independent replay verified all 45 states and all 150 model selection positions. All earlier scientific freezes remain intact.

**Central finding:** in every case the model output IDs 0 through 9, the first ten displayed candidates. Because presentation was randomized, the observed choices are exactly reproducible by taking the first half of that shuffled list. The better aggregate scores therefore do not demonstrate learned ranking or incremental model value. This is an actual-response diagnostic, not fabricated inference or an additional collected model-free arm.

Start with reports/review_note.md for the overall discussion, reports/pilot_report_v8.md for measured results, and reports/protocol_v8.md plus relevant v8 code for implementation. The latest held-out routing result remains reports/pilot_report_v6.md. Do not reread the original deep-research report. All preapproval state is preserved in artifacts/history/v8_before_approval/; previous v7 root docs are in artifacts/history/v7_before_v8/.

## Authorization and actual execution

The user replied **`Approved`** to the explicit allowance **113 → 128** for fifteen additional local calls. Exact text and recording timestamp are in configs/authorization_v8.json, snapshotted before inference in results/v8/authorization_at_inference_start.json. Historical counts were not reset. Runtime stayed capped at 1,800 seconds; external spending stayed USD 0. No download, cloud, credentials, remote publication or system-setting changes.

Model: Qwen/Qwen2.5-0.5B-Instruct, revision 7ae557604adf67be50417f59c2c2f167def9a775; CPU/float32, four threads, greedy decoding, local files only. All three development systems (MySQL, lrzip, Brotli) and five seeds [11,23,37,53,71] completed. The exact saved ten-acquisition v6 prefixes were cloned; ten more labels were acquired per new branch, logical budget 20. Same fixed acquired-only top-20 shortlist for all three arms; presentation seed+70000, random control seed+40000. No projection or duplicate acquisition in the LLM selection arm.

This approval added **150** LLM-branch target acquisitions; prior V8 controls added 300. All 450 are recorded in results/v8/acquisitions.jsonl. Reused prefixes and comparison arms retain their historical collection costs. No held-out data was used to change a V8 treatment or train a new controller.

Commands actually executed after approval:

```sh
PYTHONPATH=src .venv/bin/python -u -m escalation.study_v8 llm
PYTHONPATH=src .venv/bin/python -m pytest -q
PYTHONPATH=src .venv/bin/python -m escalation.analyze_v8
.venv/bin/python scripts/verify_v8.py
.venv/bin/python scripts/diagnose_v8.py
.venv/bin/python scripts/report_v8.py
```

Tests: 64 passed in 1.05 seconds after approval. Collector exit was successful, all cases retained, ledger inactive and worker terminated. The preapproval preflight exit2 was a deliberate resource gate, now resolved by the recorded approval. The supplied model generation config emits warnings about sampling parameters ignored by greedy decoding; these are preserved in the execution log and do not indicate sampling or failed requests.

## Results and their limit

Positive gain means baseline loss minus new LLM loss; fixed material margin .02. Three independent development families, five seeds each; no significance/generalization claim.

| Baseline | Mean paired gain | Material help /15 | Material harm /15 |
|---|---:|---:|---:|
| classical | 0.005349 | 2 | 0 |
| original_llm | 0.006421 | 2 | 0 |
| excluded_llm | 0.008134 | 2 | 0 |
| uniform_selection | 0.003497 | 1 | 0 |
| static_rank | 0.001106 | 1 | 0 |

V8 LLM mean loss: Brotli .000499, lrzip .000763, MySQL .029433. Per-seed outcomes, including smaller deteriorations below the .02 margin, are all in results/v8/outcomes.csv. Zero material harms does not mean every case improved. Both material gains over adaptive classical occur in MySQL. Static-rank comparison has only one material benefit. The all-first-ten response pattern prevents interpreting the favorable mean as learned content-sensitive ranking. A future permutation test would be needed to assess order sensitivity under changed presentations; none was run here.

The post-hoc diagnostic checks actual raw IDs against displayed order and actual acquired row sequence, matching 15/15 cases. It changes no prompt, pool, threshold, outcome or treatment and makes no new call/acquisition. The predeclared shortlist hindsight reference uses hidden labels only for retrospective scoring and is not deployable or a budgeted policy.

V6 held-out evidence remains unchanged: 2/15 material benefits, 3/15 harms, zero escalations by both learned-benefit and uncertainty controllers, and no observed routing advantage. Three test groups are insufficient. V7 eliminated original-prefix copying but showed no material improvement and one harm against each main comparator. V8 is adaptive development evidence, not a fresh held-out routing result.

## Evidence and reproducibility

- Human reports: reports/pilot_report_v8.md; reports/review_note.md; reports/next_experiment.md.
- Frozen scientific protocol and 120-file map: reports/protocol_v8.md; protocol_v8.freeze.json.
- Data schema, source/version hashes, exact prefixes/pools/prompt digests: data/manifest_v8.json.
- Raw real model evidence: results/v8/request_starts.jsonl; requests.jsonl; model_runtime.json.
- Approval-before-request record: configs/authorization_v8.json; results/v8/authorization_at_inference_start.json.
- All acquired source outcomes: results/v8/acquisitions.jsonl.
- All states/checkpoints: results/v8/uniform_selection/; static_rank/; llm/; checkpoints/.
- All intended runs: results/v8/progress.json (45/45 complete).
- Machine analysis: results/v8/summary.json; outcomes.csv.
- Actual-response diagnostic: results/v8/selection_diagnostics.json; scripts/diagnose_v8.py.
- Reproducible, visually inspected figures: results/v8/comparison.png and .svg.
- Actual source snapshot: results/v8/source_snapshot/.
- Logs: artifacts/study_v8/llm_collection.log; analysis_complete.log; verification_complete.log; diagnostics.log; tests_after_approval.log.
- Evidence index and final accounting: artifacts/study_v8/evidence_complete.json; final_ledger_snapshot.json.

Independent verification replayed source values/row IDs, exact prefixes, fixed shortlist rankings, budget counts, model token IDs/dynamic allowed masks/raw decoding, rendered prompt hashes/token counts, CPU/model revision and approval-before-request timing. Synthetic tokenizer checks remain explicitly separate. Completed collectors reuse existing cases without recharging; interrupted transactions fail closed. Do not delete outputs or reset ledgers. Older version-specific verifiers describe their own accounting checkpoints; use current v8 verification for cumulative counts.

## Actual cost and remaining limits

- V8: 450 new objective acquisitions, 15 real local requests, **23,930 input tokens and 300 output tokens**, **28.6607 seconds request wall time**, **3.7997 seconds startup** separately.
- Full V8 experiment ledger time (controls, inference, analysis, diagnosis): **38.7021 seconds**; after this approval: **35.3958 seconds**. Coding/tests/forensic verification are excluded from experiment-collection time.
- Cumulative runtime **1668.8222/1800 seconds**, **131.1778 remaining**, inactive ledger.
- Shared follow-up attempts **128/128 exhausted**; historical attempts including v1 **228**. Historical failed-call token usage remains unknown where unobserved.
- Historical charged objective acquisitions **4,208** (3,758 before V8 +450). Recorded-table accesses are not newly executed live software benchmarks.
- Hypothetical LLM-only deployment across these 15 cases uses 300 logical labels including prefixes plus 15 requests. This differs from actual three-arm collection and all historical costs; no production latency or cloud-price savings asserted.
- Downloads unchanged at 1,412,812,979 bytes; model 999,602,607 bytes. **USD 0 external spending**. No worker, scheduled/background job, email, remote push, publication or submission remains.

## Completion and single next action

The fixed V8 comparison and the bounded pilot are complete. This is a credible small methods finding, not evidence that the core benefit-router hypothesis succeeded. Stop adaptive treatment search rather than continue until positive.

**Single most important next research action: predeclare a candidate-order permutation diagnostic against the first-half rule before funding broader router data collection.** Use reports/review_note.md to discuss that decision with Tim; nothing has been sent. A stronger model can be a separately fixed future treatment. Any new inference requires a new concrete allowance because 128/128 requests are used; do not silently increase limits.

Untested: behavior under independently permuted orders, stronger local models, empirical nonbinary tasks, multiple budgets/objectives, broader independent families and a fresh held-out routing evaluation. Existing six V6 groups are exposed and cannot be adaptively reused as untouched tests. No novelty, professor acceptance or publication-readiness guarantee. No work is scheduled outside this session.
