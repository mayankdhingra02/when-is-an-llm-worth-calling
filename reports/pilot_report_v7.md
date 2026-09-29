# V7: development-only prefix-copy exclusion

This is a versioned exploratory response to v6's observed copying behavior, not a fresh held-out routing evaluation. Only MySQL, lrzip and Brotli development groups enter, with all five original seeds and exactly the same ten-label prefixes. No controller is retrained and no held-out outcomes are used in this analysis.

The sole model intervention is decoding-time exclusion of the original ten feature strings. Prompts, model/revision, CPU/float32, greedy decoding, candidate domains, ten-proposal batch, projection and budgets match v6. A corresponding uniform-random control samples exactly from the domain complement of those same strings. Repeated novel proposals within a batch remain possible. Zero original-prefix copies is enforced by construction, not a scientific success criterion.

**Both new arms completed: 15 constrained local-LLM continuations and 15 matched random controls.** These are development-only measurements, not validation of generalization.

Against original_llm: mean normalized-loss gain -0.001713, material help 0/15, material harm 1/15 (fixed .02 margin).

Against classical: mean normalized-loss gain -0.002786, material help 0/15, material harm 1/15 (fixed .02 margin).

Against uniform_excluded: mean normalized-loss gain -0.002251, material help 0/15, material harm 1/15 (fixed .02 margin).

The exclusion constraint removed original-prefix copying (137/150 → 0/150 on the same 15 cases), but did not establish improved optimization. Only 7/150 raw proposals matched an available recorded configuration; the rest needed projection. Absence from the table does not prove a configuration is invalid in the real software. Within-batch repetition increased from 6 to 14. These are post-hoc descriptive diagnostics, not a new selected treatment.

| Family | classical | original_llm | uniform_original | uniform_excluded | llm_excluded |
|---|---:|---:|---:|---:|---:|
| brotli | 0.000690 | 0.000232 | 0.000447 | 0.000255 | 0.000500 |
| lrzip | 0.001392 | 0.002580 | 0.002521 | 0.001444 | 0.002096 |
| mysql_family | 0.044660 | 0.047146 | 0.034186 | 0.046647 | 0.052502 |

Values are mean normalized loss over five seeds per development family; lower is better. Original arms are immutable v6 records, not new collection. The new conditioned-uniform sampler has the correct conditional distribution, but the same seed does not imply identical random draws to the old coordinate-wise sampler. Differences between those random controls are not an isolated causal estimate of exclusion.

![Development comparison](../results/v7/comparison.png)

![Paired gains](../results/v7/paired_gains.png)

| Arm | Completed / intended | Projections | Acquired-row collisions | Fallback acquisitions |
|---|---:|---:|---:|---:|
| uniform_excluded | 15/15 | 150 | 0 | 0 |
| llm | 15/15 | 143 | 36 | 0 |

Actual model startup/load wall time was 4.953 seconds, separate from request time. Hypothetically deploying just the new LLM continuation across these 15 cases would require 15 × 20 = 300 logical objective acquisitions (including prefixes) and 15 requests. This is distinct from the new research acquisitions below, which cover both new branches while reusing historical prefixes.

Actual v7 collection: **300 new objective acquisitions**, **15 local-model attempts**, 13283 observed input tokens and 4050 output tokens, 148.437 request wall seconds. External spending is USD 0. All prefix, classical and original LLM costs remain part of historical research collection. The full intended ablation costs 300 new acquisitions and 15 real model calls; each new continuation has logical budget 20 including its shared prefix.

Verification passed: deterministic proposal/projection replay, source labels, inclusive 20-label budgets, original prefix hashes, development-only allocation, model/token evidence for any executed requests, and prior scientific freezes. Tests actually ran: **54 passed in 1.32s**. Fifteen additional real-tokenizer traversals were synthetic syntax checks, not model inference or research outcomes.

The ledger is **113/113 requests used**, with 169.880 seconds remaining under the unchanged 1800-second runtime limit. The user explicitly approved cap 100 → 113 with the reply `approve`, granting 13 additional attempts beyond the two then remaining. The authorization and preflight are snapshotted in `results/v7/authorization_at_inference_start.json`. No paid inference, new weights, cloud or runtime-limit increase was used. `configs/authorization_v7.json` records the approval.

The scientific protocol and 97 code/input files were frozen before the new controls in `reports/protocol_v7.freeze.json`. Raw acquired labels and branch states are in `results/v7/`; all 30 intended new branch slots remain in `progress.json`. `artifacts/study_v7/` holds tests, tokenizer checks, actual commands, blocked preflight and verification. Source snapshots and versioned cached baselines support reproducibility; no old results were overwritten.

Remaining limits: only three development families; no new test data; small constrained model; binary empirical feature tables; single-target quality tradeoffs; retrospective/adaptive choice of this ablation following v6. Valid novel syntax may still project to configurations selected mainly by geometry. A positive development result would require a frozen follow-up on genuinely untouched families.

```sh
PYTHONPATH=src .venv/bin/python -m pytest -q
PYTHONPATH=src .venv/bin/python -m escalation.study_v7 preflight
# Completed cases are reused; no automatic repeat or new allowance:
PYTHONPATH=src .venv/bin/python -m escalation.study_v7 llm
PYTHONPATH=src .venv/bin/python -m escalation.analyze_v7
.venv/bin/python scripts/verify_v7.py
.venv/bin/python scripts/diagnose_v7.py
.venv/bin/python scripts/report_v7.py
```

The most important next experiment is a development-only comparison of selecting existing unevaluated candidate rows against generating new feature strings, with a matched random-selection control. This would separate model ranking from nearest-row projection. It is not implemented or run here, and new model calls require new explicit allowance because the approved 113 attempts are exhausted. A stronger model and untouched-system generalization remain untested.

No background job is left running. No paper, email, remote push or publication occurred.
