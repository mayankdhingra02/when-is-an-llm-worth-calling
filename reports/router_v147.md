# V147: does benefit prediction transfer across the paired-model cohort?

**Exploratory nested evaluation of seven previously exposed software families.** All 55 paired cases per model are included; Spark contributes 25 cases but only one-seventh of the primary aggregate. No new model call or objective acquisition occurred. One historical interrupted SmolLM call retains its classical fallback. This analysis does not create a fresh holdout or establish journal readiness.

Each outer fold holds out a whole family. Six development families supply inner group folds, all standardization, ridge fitting and threshold selection. The primary ridge uses the seven pre-decision V132 features. Every declared ablation is shown. Adaptive outcomes never select a threshold. All-feature and uncertainty 80th-percentile policies use development quantiles and are fixed diagnostics against trivial no-call solutions, not tuned test rates.

| Model / policy | Calls /55 | Family gain vs sequential | Gain above matched random | >1% harmful calls | Missed >1% wins |
|---|---:|---:|---:|---:|---:|
| smollm3_3b / never | 0 | +0.0000% | +0.0000% | 0 | 7 |
| smollm3_3b / always | 55 | -4.7688% | +0.0000% | 17 | 0 |
| smollm3_3b / benefit_all | 0 | +0.0000% | +0.0000% | 0 | 7 |
| smollm3_3b / benefit_no_cardinality | 0 | +0.0000% | +0.0000% | 0 | 7 |
| smollm3_3b / benefit_trajectory | 0 | +0.0000% | +0.0000% | 0 | 7 |
| smollm3_3b / uncertainty | 1 | +0.0000% | +0.2022% | 0 | 7 |
| smollm3_3b / benefit_80pct | 6 | -0.0577% | +0.0095% | 1 | 7 |
| smollm3_3b / uncertainty_80pct | 18 | -2.9709% | -1.4919% | 5 | 4 |
| qwen3_8b / never | 0 | +0.0000% | +0.0000% | 0 | 3 |
| qwen3_8b / always | 55 | -5.0596% | +0.0000% | 22 | 0 |
| qwen3_8b / benefit_all | 0 | +0.0000% | +0.0000% | 0 | 3 |
| qwen3_8b / benefit_no_cardinality | 0 | +0.0000% | +0.0000% | 0 | 3 |
| qwen3_8b / benefit_trajectory | 0 | +0.0000% | +0.0000% | 0 | 3 |
| qwen3_8b / uncertainty | 0 | +0.0000% | +0.0000% | 0 | 3 |
| qwen3_8b / benefit_80pct | 7 | -0.0577% | -0.0037% | 1 | 3 |
| qwen3_8b / uncertainty_80pct | 18 | -3.1264% | -1.4813% | 7 | 3 |

Random reference matches each policy’s realized call count **within each family** and samples without observing outcomes. Its analytic expected gain is subtracted above; this is a retrospective matched-rate diagnostic. 10,000 fixed-seed random draws supply reference bands in comparison.json. These bands describe random selection on these saved cases, not population uncertainty or a confirmatory significance test. Call rate and pooled-case means are also saved; primary results give families equal weight.

| Model / family | Primary benefit calls / n | Primary gain | Always gain | Matched-random expectation |
|---|---:|---:|---:|---:|
| smollm3_3b / berkeleydb | 0/5 | +0.0000% | -0.3308% | -0.0000% |
| smollm3_3b / dune_hsmgp | 0/5 | +0.0000% | -20.8911% | -0.0000% |
| smollm3_3b / hipacc | 0/5 | +0.0000% | -2.5977% | -0.0000% |
| smollm3_3b / llvm | 0/5 | +0.0000% | -1.9716% | -0.0000% |
| smollm3_3b / openvpn | 0/5 | +0.0000% | -7.0766% | -0.0000% |
| smollm3_3b / sac | 0/5 | +0.0000% | -0.4036% | -0.0000% |
| smollm3_3b / spark | 0/25 | +0.0000% | -0.1099% | -0.0000% |
| qwen3_8b / berkeleydb | 0/5 | +0.0000% | +0.0648% | +0.0000% |
| qwen3_8b / dune_hsmgp | 0/5 | +0.0000% | -21.2355% | -0.0000% |
| qwen3_8b / hipacc | 0/5 | +0.0000% | -2.9068% | -0.0000% |
| qwen3_8b / llvm | 0/5 | +0.0000% | -2.1592% | -0.0000% |
| qwen3_8b / openvpn | 0/5 | +0.0000% | -6.8761% | -0.0000% |
| qwen3_8b / sac | 0/5 | +0.0000% | -0.4036% | -0.0000% |
| qwen3_8b / spark | 0/25 | +0.0000% | -1.9009% | -0.0000% |

## Headroom, support and strong-control checks

smollm3_3b: 7/55 >1% opportunities against sequential in families spark; 4/55 exceed both sequential and adaptive by >1%. Hindsight family-mean gain 0.1776% is a non-deployable upper reference. Primary policy gain against adaptive +1.2840%; joint useful calls 0. 41/55 cases have at least one feature outside their outer-training min/max range. Primary aggregate after omitting each one family ranges from +0.0000% to +0.0000%; this is sensitivity, not a confidence interval.
qwen3_8b: 3/55 >1% opportunities against sequential in families berkeleydb, spark; 1/55 exceed both sequential and adaptive by >1%. Hindsight family-mean gain 0.1135% is a non-deployable upper reference. Primary policy gain against adaptive +1.2840%; joint useful calls 0. 41/55 cases have at least one feature outside their outer-training min/max range. Primary aggregate after omitting each one family ranges from +0.0000% to +0.0000%; this is sensitivity, not a confidence interval.

Against adaptive, a no-call decision deploys the actual sequential arm and therefore can still lose to adaptive. Never-call is not silently replaced with a hindsight-best classical portfolio. Domain cardinality removal is motivated by the already observed Spark extrapolation; its result is an exposed-data ablation, not independent confirmation.

## Costs and reproducibility

New collection: zero requests, zero objective acquisitions, zero native executions. Historical cohort collection: 110 real generation starts, 109 complete responses and one interrupted request with unknown usage; 1,100 model-continuation acquisitions plus original prefixes and classical controls. Prior acquisition/request totals are unchanged. Raw provenance and collection costs stay in V141–V145; this is reuse, not free historical inference.

smollm3_3b: historical generated≥6499, prefill≥68194 tokens; unknown-usage requests 1. Hypothetical policy deployment calls equal the table counts and use B20 each. Per-family replayed request runtime and generated-token lower bounds are saved for selected branches. They exclude model startup/amortization and unknown interrupted runtime, and are evaluation quantities, never router inputs. No dollars or native-time savings inferred.
qwen3_8b: historical generated≥15850, prefill≥91469 tokens; unknown-usage requests 0. Hypothetical policy deployment calls equal the table counts and use B20 each. Per-family replayed request runtime and generated-token lower bounds are saved for selected branches. They exclude model startup/amortization and unknown interrupted runtime, and are evaluation quantities, never router inputs. No dollars or native-time savings inferred.

Commands:

```sh
.venv/bin/python scripts/verify_router_v147.py
MPLCONFIGDIR=/tmp/mpl-v147 .venv/bin/python scripts/report_router_v147.py
```

The create-once fitting command was `scripts/router_v147.py run`; its input/protocol/source hashes are in artifacts/study_v147/freeze.json and runtime is in runtime.json. Full inner/outer models, transformations, calibration grids, support flags and decisions: results/v147_router/folds.json. Per-case paired inputs: artifacts/study_v147/inputs.json. Independent replay uses augmented least squares, separately checks prefix features and raw paired targets, and rejects semantic mutations.

## Limits and next action

Seven groups, two fixed quantized models, heterogeneous nominal/numeric proposal representations, reused classical prefixes and exposed outcomes limit generalization. The family-held-out mechanics prevent direct fold leakage; they do not undo earlier human/agent inspection or provide a prospective replication. Source correctness/noise/contamination limitations and the Spark missing-data amendment persist. Repeated seeds/workloads are dependent. No classifier accuracy, non-inferiority, equivalence or journal-quartile claim is justified by this table.

The next priority is an outcome-unexposed, source-validated configuration cohort with enough independent families, then one frozen controller test. The V146 source audit excluded PTSS metric dictionaries, incomplete Cassandra trace exports and Hyrise’s 36-valid-setting scan partitions without relaxing admission to obtain more favorable evidence. A usable original per-configuration Cassandra outcome matrix is a concrete missing artifact; its current elite logs do not substitute for one.
