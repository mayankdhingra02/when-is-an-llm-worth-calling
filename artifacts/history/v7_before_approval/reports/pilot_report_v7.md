# V7: development-only prefix-copy exclusion

This is a versioned exploratory response to v6's observed copying behavior, not a fresh held-out routing evaluation. Only MySQL, lrzip and Brotli development groups enter, with all five original seeds and exactly the same ten-label prefixes. No controller is retrained and no held-out outcomes are used in this analysis.

The sole model intervention is decoding-time exclusion of the original ten feature strings. Prompts, model/revision, CPU/float32, greedy decoding, candidate domains, ten-proposal batch, projection and budgets match v6. A corresponding uniform-random control samples exactly from the domain complement of those same strings. Repeated novel proposals within a batch remain possible. Zero original-prefix copies is enforced by construction, not a scientific success criterion.

**Actual execution: all 15 no-model controls completed; the 15-call LLM arm is blocked by the request allowance.** No v7 LLM response or comparative LLM benefit is claimed. The preflight exits 2 before model loading or request reservation because only two calls remain.

| Family | classical | original_llm | uniform_original | uniform_excluded |
|---|---:|---:|---:|---:|
| brotli | 0.000690 | 0.000232 | 0.000447 | 0.000255 |
| lrzip | 0.001392 | 0.002580 | 0.002521 | 0.001444 |
| mysql_family | 0.044660 | 0.047146 | 0.034186 | 0.046647 |

Values are mean normalized loss over five seeds per development family; lower is better. Original arms are immutable v6 records, not new collection. The new conditioned-uniform sampler has the correct conditional distribution, but the same seed does not imply identical random draws to the old coordinate-wise sampler. Differences between those random controls are not an isolated causal estimate of exclusion.

![Development comparison](../results/v7/comparison.png)

Actual v7 collection: **150 new objective acquisitions**, **0 local-model attempts**, 0 observed input tokens and 0 output tokens, 0.000 request wall seconds. External spending is USD 0. All prefix, classical and original LLM costs remain part of historical research collection. The full intended ablation costs 300 new acquisitions and 15 real model calls; each new continuation has logical budget 20 including its shared prefix.

Verification passed: deterministic proposal/projection replay, source labels, inclusive 20-label budgets, original prefix hashes, development-only allocation, model/token evidence for any executed requests, and prior scientific freezes. Tests actually ran: **54 passed in 0.96s**. Fifteen additional real-tokenizer traversals were synthetic syntax checks, not model inference or research outcomes.

The ledger is **98 requests used**, with 326.990 seconds remaining under the unchanged 1800-second runtime limit. The concrete approval request is cap 100 → 113, granting 13 additional attempts beyond the two remaining so all 15 prepared calls fit. No paid inference, new weights, cloud or runtime-limit increase is requested. `configs/authorization_v7.json` is the explicit authorization gate.

The scientific protocol and 97 code/input files were frozen before the new controls in `reports/protocol_v7.freeze.json`. Raw acquired labels and branch states are in `results/v7/`; all 30 intended new branch slots remain in `progress.json`. `artifacts/study_v7/` holds tests, tokenizer checks, actual commands, blocked preflight and verification. Source snapshots and versioned cached baselines support reproducibility; no old results were overwritten.

Remaining limits: only three development families; no new test data; small constrained model; binary empirical feature tables; single-target quality tradeoffs; retrospective/adaptive choice of this ablation following v6. Valid novel syntax may still project to configurations selected mainly by geometry. A positive development result would require a frozen follow-up on genuinely untouched families.

```sh
PYTHONPATH=src .venv/bin/python -m pytest -q
PYTHONPATH=src .venv/bin/python -m escalation.study_v7 preflight
# Inference command is gated on explicit allowance:
PYTHONPATH=src .venv/bin/python -m escalation.study_v7 llm
PYTHONPATH=src .venv/bin/python -m escalation.analyze_v7
.venv/bin/python scripts/verify_v7.py
.venv/bin/python scripts/report_v7.py
```

No background job is left running. No paper, email, remote push or publication occurred.
