# V164: explicit-candidate interface experiment

This development experiment compares fresh numeric-prototype and explicit-catalog calls on the same ten saved prefixes. Both small local models are real. Candidate enumeration, eligible-ID grammar and output representation change together; their individual effects are not identified. No new held-out system or learned-router improvement is claimed.

## Primary interface comparison

Positive gain means the catalog incumbent has lower median fresh-validation utility than the numeric incumbent. Practical wins require >10%, different settings, valid quality, MAD<=5% and both medians>=10ms. All intended cases remain.

| Application | Model | Mean catalog gain vs numeric | Same setting / 5 | Robust catalog wins / losses |
|---|---|---:|---:|---:|
| ripgrep | smollm3_3b | -1.187% | 3 | 0 / 0 |
| hnswlib | smollm3_3b | -0.521% | 5 | 0 / 0 |
| ripgrep | qwen3_8b | +1.096% | 4 | 0 / 0 |
| hnswlib | qwen3_8b | +0.577% | 5 | 0 / 0 |

## Proposal mechanism

Counts below cover only the first seven evaluated proposals per case; all-ten counts are retained in comparison.json. Repeated proposals are resolved to distinct unseen evaluations with the same feature-distance rule. Missing/invalid responses use charged sequential fallback.

| Application | Model / interface | Projected / 35 | Duplicate proposals / 35 | Prefix incumbent / 5 | Fallback cases |
|---|---|---:|---:|---:|---:|
| ripgrep | smollm3_3b / numeric | 13 | 7 | 4 | 0 |
| ripgrep | smollm3_3b / catalog | 0 | 0 | 3 | 0 |
| hnswlib | smollm3_3b / numeric | 24 | 24 | 5 | 0 |
| hnswlib | smollm3_3b / catalog | 0 | 0 | 5 | 0 |
| ripgrep | qwen3_8b / numeric | 14 | 12 | 4 | 0 |
| ripgrep | qwen3_8b / catalog | 0 | 0 | 5 | 0 |
| hnswlib | qwen3_8b / numeric | 26 | 25 | 5 | 0 |
| hnswlib | qwen3_8b / catalog | 0 | 0 | 5 | 0 |

## Secondary comparison with fresh classical continuations

| Application | Model / interface | Mean gain vs sequential | vs adaptive | vs GP-EI | Joint robust wins / 5 |
|---|---|---:|---:|---:|---:|
| ripgrep | smollm3_3b / numeric | +0.237% | +3.769% | +1.242% | 0 |
| ripgrep | smollm3_3b / catalog | -0.915% | +2.682% | +0.107% | 0 |
| ripgrep | qwen3_8b / numeric | -3.201% | +0.539% | -2.185% | 0 |
| ripgrep | qwen3_8b / catalog | -1.959% | +1.696% | -0.927% | 0 |
| hnswlib | smollm3_3b / numeric | -0.122% | +0.529% | -0.108% | 0 |
| hnswlib | smollm3_3b / catalog | -0.642% | +0.009% | -0.630% | 0 |
| hnswlib | qwen3_8b / numeric | -1.014% | -0.357% | -0.999% | 0 |
| hnswlib | qwen3_8b / catalog | -0.422% | +0.228% | -0.407% | 0 |

## Accounting and reliability

New collection: 900 configuration outcomes / 2700 native invocations / 40 model starts. Separately reused historical prefixes:100 outcomes/300 invocations; their collection cost was incurred in V163. Ninety logical B20 arms use10 shared prefix+7 new search+3 validation. All incumbents were fixed before270 randomized validation outcomes. Quality penalties:0; unstable validation cells:1/90; below10ms:0/90. These flags do not remove cases from descriptive means.

| Model / interface | Starts / intended | Valid responses | Observed input / output tokens | Request seconds |
|---|---:|---:|---:|---:|
| smollm3_3b / numeric | 10/10 | 10 | 4653 / 435 | 16.975 |
| smollm3_3b / catalog | 10/10 | 10 | 10814 / 283 | 24.303 |
| qwen3_8b / numeric | 10/10 | 10 | 5418 / 532 | 42.445 |
| qwen3_8b / catalog | 10/10 | 10 | 13182 / 330 | 64.852 |

Native subprocess time301.984s, including231.394objective-seconds; total stage465.352s/1800s. Model cold-start, whole-stage/RSS/exit and unknown-usage fields are retained in comparison.json and raw ledgers. No paid/cloud use, retry or new download. Research collection includes all interfaces and controls. A ten-case deployment would use one branch per case:200 logical outcomes/600 native invocations plus selected requests; that is an estimate, not measured deployment or a dollar/energy claim.

## Interpretation boundaries

Two exposed applications and one host cannot establish generalization. Equal prefix reuse makes the interface pairing explicit but does not remove temporal cache/load drift. Calls are interleaved by a fixed shuffled plan within each model; model order remains fixed. Seeds do not create independent systems. Historical numeric results were not reused as the fresh numeric comparator. Same-setting timing differences, small noisy effects and lowered projection counts do not establish optimizer benefit. No router is refitted; historical controller thresholds are not validated for this interface. Any further prompt selection uses these cases only as development data.

Raw evidence: artifacts/study_v164/freeze.json binds protocol, code, prompts, model pins and reused prefix provenance. results/v164_models holds every request/response and resource ledger. results/v164_native holds900 charged records,90 branch states and270 validations. Analysis code: scripts/report_apps_v164.py.
