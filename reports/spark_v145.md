# V144–V145 Spark extension: measured result and missing-data recovery

Single Spark family, five workloads, five seeds; exploratory missing-data amendment. The original strict validation failed on a missing TPC-H target. All intended cases and collection costs remain; this is not pristine confirmation or evidence of journal acceptance.

Completed 175 B20arms from 25 shared B10 prefixes. 2000 charged recorded acquisitions: 1999 finite durations and 1 missing outcomes. 50 genuine local request starts, 49 complete responses, 1 incomplete requests with unknown usage and 0 unattempted intents. All failed/unattempted intents use explicitly labeled classical fallback. Original Spark jobs were executed by source authors; we only queried recorded tables.

| Model | Sequential gain* | Comparable /25 | Adaptive gain* | Comparable /25 | >1% win over both / comparable |
|---|---:|---:|---:|---:|---:|
| smollm3_3b | -0.1099% | 25 | -0.4168% | 25 | 4/25 |
| qwen3_8b | -1.9009% | 25 | -2.2181% | 25 | 1/25 |

*Positive favors LLM. Means weight workloads equally, using only complete pairs within each workload. All 25 sequential and adaptive comparisons are complete for each model. Only one random-row comparison per model is inconclusive; missingness can bias that control’s complete-pair summary. A pair with any missing acquisition on either arm is inconclusive for true best duration. Best-observed values, missing flags and sensitivity aggregates for **all 25 cases/model** are preserved in comparison.json. No missing value was imputed as a runtime or silently dropped.

| Model / workload | Sequential gain (n) | Adaptive gain (n) | Random prototypes gain (n) |
|---|---:|---:|---:|
| smollm3_3b / bayes | 0.0000% (5/5) | -1.0285% (5/5) | -2.1981% (5/5) |
| smollm3_3b / pagerank | -2.4323% (5/5) | -0.0433% (5/5) | -1.8958% (5/5) |
| smollm3_3b / terasort | -0.3893% (5/5) | -0.7940% (5/5) | -10.6198% (5/5) |
| smollm3_3b / tpch | 0.2106% (5/5) | -0.3015% (5/5) | 1.4030% (5/5) |
| smollm3_3b / wordcount | 2.0615% (5/5) | 0.0833% (5/5) | 4.6438% (5/5) |
| qwen3_8b / bayes | 0.0000% (5/5) | -1.0285% (5/5) | -2.1981% (5/5) |
| qwen3_8b / pagerank | -5.2758% (5/5) | -2.7793% (5/5) | -4.6038% (5/5) |
| qwen3_8b / terasort | -0.4494% (5/5) | -0.7355% (5/5) | -10.4502% (5/5) |
| qwen3_8b / tpch | -1.6909% (5/5) | -2.2176% (5/5) | -0.4824% (5/5) |
| qwen3_8b / wordcount | -2.0885% (5/5) | -4.3294% (5/5) | 0.5969% (5/5) |

## All controls and reliability

| Model / control | Wins / ties / losses on complete pairs | >1% wins | <−1% harms | Inconclusive /25 | Observed-best mean sensitivity** |
|---|---|---:|---:|---:|---:|
| smollm3_3b / sequential_3nn | 10/8/7 | 7 | 7 | 0 | -0.1099% |
| smollm3_3b / adaptive_neighbor | 7/7/11 | 6 | 10 | 0 | -0.4168% |
| smollm3_3b / fixed_neighbor | 9/6/10 | 6 | 9 | 0 | -0.5540% |
| smollm3_3b / random_full | 7/9/8 | 7 | 5 | 1 | -0.2724% |
| smollm3_3b / random_proposal | 9/8/8 | 9 | 7 | 0 | -1.7334% |
| qwen3_8b / sequential_3nn | 2/11/12 | 2 | 11 | 0 | -1.9009% |
| qwen3_8b / adaptive_neighbor | 3/9/13 | 2 | 13 | 0 | -2.2181% |
| qwen3_8b / fixed_neighbor | 0/10/15 | 0 | 15 | 0 | -2.3250% |
| qwen3_8b / random_full | 3/13/8 | 1 | 8 | 1 | -1.9715% |
| qwen3_8b / random_proposal | 2/11/12 | 2 | 10 | 0 | -3.4275% |

**Sensitivity uses the best among available finite acquisitions even for incomplete arms. It does not estimate true complete-arm quality. No significance or equivalence claim.

## Frozen controller transport

No fitting or threshold changes on Spark. Original V132 model/thresholds and pre-continuation decisions are retained. Qwen-trained controller on SmolLM is an uncalibrated transfer diagnostic. All 25 Spark cases exceed the development range for mean domain cardinality (55.57–58.63 vs 1.71–4.67); other individual feature ranges overlap. This is extrapolation, not evidence of calibrated benefit prediction. The support audit is artifacts/study_v145/router_transport_audit.json. Random decisions exactly match the realized benefit-controller call count.

| Model / policy | Calls /25 | Conditional mean gain* | Inconclusive | Harmful calls | Missed useful | Usefulness unknown |
|---|---:|---:|---:|---:|---:|---:|
| smollm3_3b / never | 0 | 0.0000% | 0 | 0 | 7 | 0 |
| smollm3_3b / always | 25 | -0.1099% | 0 | 7 | 0 | 0 |
| smollm3_3b / benefit | 0 | 0.0000% | 0 | 0 | 7 | 0 |
| smollm3_3b / uncertainty | 0 | 0.0000% | 0 | 0 | 7 | 0 |
| smollm3_3b / random_matched_rate | 0 | 0.0000% | 0 | 0 | 7 | 0 |
| qwen3_8b / never | 0 | 0.0000% | 0 | 0 | 2 | 0 |
| qwen3_8b / always | 25 | -1.9009% | 0 | 11 | 0 | 0 |
| qwen3_8b / benefit | 0 | 0.0000% | 0 | 0 | 2 | 0 |
| qwen3_8b / uncertainty | 0 | 0.0000% | 0 | 0 | 2 | 0 |
| qwen3_8b / random_matched_rate | 0 | 0.0000% | 0 | 0 | 2 | 0 |

smollm3_3b: hindsight oracle gain on complete sequential/model pairs 1.1843% (non-deployable diagnostic on the evaluated cases). Best-observed prefix improvements 13/25. Fallbacks 1; projection diagnostics{'count': 240, 'nonzero': 240, 'repeated': 23, 'matches_prefix': 0}.


qwen3_8b: hindsight oracle gain on complete sequential/model pairs 0.4213% (non-deployable diagnostic on the evaluated cases). Best-observed prefix improvements 7/25. Fallbacks 0; projection diagnostics{'count': 250, 'nonzero': 250, 'repeated': 192, 'matches_prefix': 0}.

## Collection cost versus deployment scenario

Actual collection consumed 987.294s from original first prefix through final outcome; capped at 1,800s. 2,000 acquisitions include 250 prefix + 1,250 classical + 500 model/fallback, across all treatments. Copied/imported histories are counted once. The 6 original SmolLM requests include the interrupted one; repaired collection could use only 44 unused starts; actual counts below reflect runtime guards. No generation retry. The failed orchestration gate is preserved and the repaired collector requires classical completion before starting. No new weights/runtime/packages, paid inference, cloud use or new native Spark jobs.

smollm3_3b: 25starts/24complete; observed generated≥3290, prefill≥46736tokens; unknown-usage requests1; allocated25600; lifecycle164.020s, startup3.294s, completed-response request wall159.115s, peakRSS4223598592bytes, server exits[0, 0].
qwen3_8b: 25starts/25complete; observed generated≥7825, prefill≥63495tokens; unknown-usage requests0; allocated25600; lifecycle590.765s, startup4.582s, completed-response request wall585.583s, peakRSS7456636928bytes, server exits[0].

A deployment policy after B10 uses 10 new outcomes and at most one generation request; model loading needs a separate amortization assumption. All-control/two-model collection is larger than one policy deployment. Timings include different model blocks; no speed causality, source-unit-to-dollar, energy, or native-runtime savings claim.

## Limits and next experiment

Only **one independent software family** was added. Workloads/seeds are dependent; missing durations, uncertain source-wide failure denominator, single historical durations, unverified runtime noise/correctness and public-data contamination constrain the claim. 30 feature inputs use transductive scaling and a fixed ten-level numeric proposal grid; random-proposal control tests this representation. This differs from prior nominal experiments. The amendment was frozen after partial classical outcomes and is explicitly exploratory. More seeds/prompt searches here would not supply an independent-family confirmation.

Next priority: admit further independent systems with documented measured targets and an explicit missing/failure rule before collection, then run a single frozen cross-family confirmation. A successful learned escalation controller is not established by repeated never-call behavior. Negative results are retained alongside workload exceptions; journal quartile readiness is not certified.

Evidence: raw results/v144_models and results/v145_models; original failed acquisitions/results/v144_spark; consolidated imported-plus-new ledger/results/v145_spark; protocol_v144.md and protocol_v145.md; feature-only source_audit_v143.md; source hashes and pre-decision inputs/artifacts/study_v144. Replay `.venv/bin/python scripts/verify_spark_v145.py`; regenerate `MPLCONFIGDIR=/tmp/mpl-v145 .venv/bin/python scripts/report_spark_v145.py`.
