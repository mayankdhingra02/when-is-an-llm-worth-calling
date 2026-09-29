# V159: paired native solver study

This is a completed local experiment on two solver implementations. It tests transfer after feasibility-based workload selection; it is not confirmation on an untouched industrial cohort. The two engines share the N-queens benchmark and constraint-solving domain.

Executed **800 native objective evaluations**, **20 real local-model requests**, and **70 logical B20 arms** across ten saved prefixes. Each arm used ten shared prefix evaluations, seven further search evaluations and three fresh incumbent validations. No fabricated responses or inferred runtimes were used.

## Measured model comparisons

Positive gain means a lower median validation runtime than the comparator. Means below weight the five seeds equally within each engine. A robust practical win requires >10% gain, different configurations, three valid solutions per arm and <=5% relative MAD. Joint wins must beat sequential 3NN, adaptive neighbor and GP-EI under all those conditions.

| Engine | Model | Mean gain vs sequential | vs adaptive | vs GP-EI | Joint robust wins |
|---|---|---:|---:|---:|---:|
| cvc5 | smollm3_3b | +0.402% | -0.388% | -0.263% | 0/5 |
| cvc5 | qwen3_8b | +0.623% | -0.149% | -0.030% | 0/5 |
| ortools | smollm3_3b | -22.024% | -21.713% | -21.200% | 0/5 |
| ortools | qwen3_8b | -21.203% | -20.900% | -20.377% | 0/5 |

Same-configuration model/sequential selections: 12/20. Validation arms above the frozen 5% relative-MAD threshold: 0/70. Correct native evaluations: 800/800; timeout utility penalties: 0. A penalty is a declared utility value, not a successful runtime. Unfiltered gains are retained even when they fail the practical/reliability rule.

## Frozen routing policies

The exact saved historical benefit predictor and uncertainty threshold were used without fitting on these engines. Prefix features, paper-inspired signals and all decisions were hashed before any continuation. The BORA/rank rules remain checkpoint adaptations, not the complete original algorithms. Rank expectation is computed over the two real outcomes; the hindsight oracle is nondeployable.

| Model | Policy | Calls / 10 (expected where applicable) | Equal-engine mean gain vs never |
|---|---|---:|---:|
| smollm3_3b | never | 0.00 | +0.000% |
| smollm3_3b | always | 10.00 | -10.811% |
| smollm3_3b | benefit | 0.00 | +0.000% |
| smollm3_3b | uncertainty | 0.00 | +0.000% |
| smollm3_3b | random_development_rate | 1.00 | -1.014% |
| smollm3_3b | bora_adaptation | 3.00 | -0.910% |
| smollm3_3b | rank_draw_adaptation | 3.00 | -0.915% |
| smollm3_3b | random_matched_rate | 0.00 | +0.000% |
| smollm3_3b | rank_expected_adaptation | 3.00 | -0.473% |
| smollm3_3b | hindsight_oracle | 4.00 | +0.305% |
| qwen3_8b | never | 0.00 | +0.000% |
| qwen3_8b | always | 10.00 | -10.290% |
| qwen3_8b | benefit | 0.00 | +0.000% |
| qwen3_8b | uncertainty | 0.00 | +0.000% |
| qwen3_8b | random_development_rate | 0.00 | +0.000% |
| qwen3_8b | bora_adaptation | 3.00 | -0.500% |
| qwen3_8b | rank_draw_adaptation | 3.00 | -0.589% |
| qwen3_8b | random_matched_rate | 0.00 | +0.000% |
| qwen3_8b | rank_expected_adaptation | 3.00 | -0.360% |
| qwen3_8b | hindsight_oracle | 3.00 | +0.562% |

## Cost and reliability

Actual native collection consumed 323.868 subprocess-seconds, including 178.683 solve-seconds. End-to-end experiment time was 401.366 seconds. The earlier 80 feasibility probes and their failures are additional actual research cost, outside these 800 evaluations. Both branches, random controls and fresh validation were collected; none becomes free by being reused for policy analysis.

- smollm3_3b: 10 starts, 10 responses; observed input/output tokens 5148/410; unknown-usage requests {'tokens_predicted': 0, 'tokens_evaluated': 0}; 0 invalid/missing responses; 16.921 request-seconds; 18.864 total model-stage seconds; peak server RSS 3042017280 bytes; server exit 0.
- qwen3_8b: 10 starts, 10 responses; observed input/output tokens 5941/670; unknown-usage requests {'tokens_predicted': 0, 'tokens_evaluated': 0}; 0 invalid/missing responses; 49.171 request-seconds; 53.814 total model-stage seconds; peak server RSS 6823395328 bytes; server exit 0.

Modeled deployment for each ten-case policy uses 200 objective evaluations plus its selected request count. `comparison.json` also gives a retrospective selected-branch collection-time proxy using measured branch and request durations; it excludes model cold-start time, which is separately logged. It is not a measured deployment run, an invoice, or an energy estimate. If a selected request has unknown duration, that proxy is unknown rather than zero. Paid/cloud inference was disabled; no new model weights were downloaded.

## Limits and next evidence

Five repeated seeds are not five independent software systems. There are only two new implementations, a shared task/domain, different board sizes, and feasibility exposure. The historical router was trained against a different 20-search target, while this study reserves three evaluations for validation. Domain shift, this transport mismatch, local quantization, public-benchmark familiarity, one host, and validation noise limit conclusions. Some selected settings ran faster than the four feasibility probes: 16 of 70 validation medians fell below the earlier 10 ms feasibility floor (minimum 9.548 ms). The paired protocol did not include this floor in its robust-win rule; that distinction is retained rather than changing the rule after observing results. All 70 validation cells met the declared 5% MAD criterion. No learned-router generalization, equivalence, population significance, industrial performance, or journal acceptance follows from this sample. Report any positive cells alongside all unfavorable controls and seeds.

The next substantive evidence should come from additional independently sourced application families with fixed workload/output contracts, selected before inspecting model gains. Do not tune a new router on these results and call them held out. Independent-host replication and an external methodological review are still missing.

Evidence: `artifacts/study_v159` contains the protocol/input hashes, candidate definitions, saved prefixes/prompts and pre-continuation decisions. `results/v159_native` contains all acquisitions, seven branches per prefix, frozen incumbents, validation blocks and aggregates. `results/v159_models` contains both pinned runtimes, requests, raw responses, tokens, failures and exit receipts. Figures can be regenerated with `.venv/bin/python scripts/report_solvers_v159.py`. Collection is create-once; do not rerun the collector.
