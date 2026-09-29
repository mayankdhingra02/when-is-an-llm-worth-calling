# V148: new Hadoop family, frozen local-model transfer test

One prospective Hadoop MapReduce family; cloud-configuration adaptation; three bigdata tasks, five seeds each. This is one independent execution-engine group, not three independent systems, and shares the Hadoop/Spark ecosystem. No new Hadoop cluster jobs or cloud spending occurred.

Executed 30 real local generation starts, 30 returned responses, 105 B20arms from15shared B10prefixes and1200charged recorded outcomes. Collection82.962s /1800s. Acquired 200 distinct source records. Status counts:{'completed': 1125, 'incomplete_failure_penalty': 75}; unique incomplete records9. Repeated rows across isolated arms still incur separate logical charges.

Primary score is completed elapsed seconds capped at7200, or an explicit7200failure penalty for incomplete source runs. A penalty is **not measured runtime** and does not identify the failure cause. All intended cases and failures remain. No imputation/filtering, new target normalization or post-outcome threshold changes. The classical completion gate passed before inference.

| Model | Gain vs sequential | W/T/L | Gain vs adaptive | W/T/L | >1% win over both /15 |
|---|---:|---|---:|---|---:|
| smollm3_3b | -3.6027% | 3/5/7 | +2.7283% | 4/9/2 | 3 |
| qwen3_8b | -5.2651% | 2/6/7 | +1.3971% | 3/10/2 | 2 |

Positive favors the model. Means give the three workloads equal weight (five seeds each); they are descriptive within one family. No confidence interval over independent seeds or journal-readiness claim.

| Model / workload | Sequential gain | Adaptive gain | Random-prototype gain |
|---|---:|---:|---:|
| smollm3_3b / pagerank | -7.7860% | -2.5953% | -7.7860% |
| smollm3_3b / terasort | -6.8014% | +3.1482% | -9.5319% |
| smollm3_3b / wordcount | +3.7795% | +7.6320% | -9.3808% |
| qwen3_8b / pagerank | -5.7275% | -0.8349% | -5.7275% |
| qwen3_8b / terasort | -12.3856% | -1.2172% | -14.6592% |
| qwen3_8b / wordcount | +2.3179% | +6.2433% | -11.2715% |

## Frozen routing and reliability

Routers were trained on the seven V147 development families and frozen before Hadoop acquisition. All workload variants/seeds stay in the new Hadoop group. Learned thresholds and fixed development80th-percentile diagnostics use no Hadoop outcome. Random matched-rate calls were selected before continuations; expected matched-random gains are descriptive after scoring.

| Model / policy | Calls /15 | Mean gain vs sequential | >1% harmful calls | Missed >1% wins | Joint useful calls |
|---|---:|---:|---:|---:|---:|
| smollm3_3b / never | 0 | +0.0000% | 0 | 3 | 0 |
| smollm3_3b / always | 15 | -3.6027% | 7 | 0 | 3 |
| smollm3_3b / benefit | 0 | +0.0000% | 0 | 3 | 0 |
| smollm3_3b / uncertainty | 0 | +0.0000% | 0 | 3 | 0 |
| smollm3_3b / random_development_rate | 0 | +0.0000% | 0 | 3 | 0 |
| smollm3_3b / random_matched_rate | 0 | +0.0000% | 0 | 3 | 0 |
| smollm3_3b / benefit_80pct | 0 | +0.0000% | 0 | 3 | 0 |
| smollm3_3b / uncertainty_80pct | 9 | -2.4321% | 5 | 2 | 1 |

smollm3_3b: prefix improvements5/15; fallbacks0/15; hindsight oracle gain2.0132% (non-deployable). Feature-support extrapolation15/15. Projection:{'proposals': 150, 'nonzero_distance': 103, 'repeated_prototypes': 2, 'matches_prefix': 5}.

| qwen3_8b / never | 0 | +0.0000% | 0 | 2 | 0 |
| qwen3_8b / always | 15 | -5.2651% | 7 | 0 | 2 |
| qwen3_8b / benefit | 0 | +0.0000% | 0 | 2 | 0 |
| qwen3_8b / uncertainty | 0 | +0.0000% | 0 | 2 | 0 |
| qwen3_8b / random_development_rate | 0 | +0.0000% | 0 | 2 | 0 |
| qwen3_8b / random_matched_rate | 0 | +0.0000% | 0 | 2 | 0 |
| qwen3_8b / benefit_80pct | 0 | +0.0000% | 0 | 2 | 0 |
| qwen3_8b / uncertainty_80pct | 9 | -0.9717% | 3 | 1 | 1 |

qwen3_8b: prefix improvements3/15; fallbacks0/15; hindsight oracle gain1.6341% (non-deployable). Feature-support extrapolation15/15. Projection:{'proposals': 150, 'nonzero_distance': 68, 'repeated_prototypes': 8, 'matches_prefix': 4}.

## Actual collection and deployment estimates

smollm3_3b: {"allocated_output_tokens": 15360, "generated_tokens_lower_bound": 390, "lifecycle_seconds": 21.75443712499691, "peak_server_rss_bytes": 3181674496, "prefill_tokens_lower_bound": 7405, "request_seconds": 19.783975207996264, "request_starts": 15, "responses": 15, "retries": 0, "server_exit_code": 0, "startup_seconds": 1.769278542000393, "unattempted": 0, "unknown_usage_requests": 0}.
qwen3_8b: {"allocated_output_tokens": 15360, "generated_tokens_lower_bound": 492, "lifecycle_seconds": 57.198500583006535, "peak_server_rss_bytes": 6861307904, "prefill_tokens_lower_bound": 8844, "request_seconds": 53.1813728310226, "request_starts": 15, "responses": 15, "retries": 0, "server_exit_code": 0, "startup_seconds": 3.710319875004643, "unattempted": 0, "unknown_usage_requests": 0}.

Actual1200charges comprise150prefix,750classical and300model/fallback acquisitions; all30model intents and both model startups belong to collection cost. Deploying one policy would use20total objective evaluations per case and at mostone model request after B10. Startup amortization, native measurement costs, energy and cloud-dollar costs are not estimated. Recorded author-run cloud experiments are not free historical computation, but our local query time is not their native execution time. Model blocks/templates differ, so timings are descriptive.

## Source and scope limits

Scout data revision e0dfc3a7d08ec4d441578565c0b7d4b24e56d5cb, MIT; original paper and linked measurement code checked in source_audit_v146.md. Variables are cluster VM count and nine VM types, extending software-configuration optimization to deployment resources. Utility is capped completion time, not economic cost; a larger cluster can consume more resources. Source Hadoop2.7 patch/binary identity, correctness, single-measurement noise and benchmark contamination remain unverified. Nominal bigdata class is fixed; reported input bytes vary slightly for PageRank/Wordcount and are not certified identical. Telemetry is excluded. These limits restrict a practical-system or generalization claim.

Reproduce the report with `MPLCONFIGDIR=/tmp/mpl-v148 .venv/bin/python scripts/report_hadoop_v148.py`; independent replay: `.venv/bin/python scripts/verify_hadoop_v148.py`. Do not rerun create-once collection. Raw responses/starts/preflight/runtime logs are in results/v148_models; every charged raw record and arm is in results/v148_hadoop; frozen candidates, prefixes, prompts, model manifests and router decisions are in artifacts/study_v148.
