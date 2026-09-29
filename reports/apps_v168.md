# V168: paired Polars and XGBoost study

Prospective paired development comparison on two additional native implementations. Polars reuses a flight workload previously exposed with DuckDB; XGBoost uses real Covertype data. Feasibility exposed both tasks. This is not independent production or unseen-system router validation.

800 new configuration outcomes, 1600 query/training executions, 70 logical B20 arms (10 shared prefix +7 search +3 fresh validation), five fixed seeds per application. Model calls use the two existing pinned local quantized models.

## Fresh validation results

Positive gain favors the model. Quality utility uses actual runtime when valid; XGBoost accuracy below75% receives the frozen60-second penalty. Robust joint win requires >10% improvement over sequential, adaptive and GP-EI, different setting IDs, all quality-valid, MAD<=5% and medians>=10ms. All unfiltered gains remain included.

| Application | Model | Mean gain vs sequential | vs adaptive | vs GP-EI | Joint robust wins |
|---|---|---:|---:|---:|---:|
| polars | smollm3_3b | +0.071% | -5.087% | -1.266% | 0/5 |
| polars | qwen3_8b | -0.816% | -5.958% | -2.064% | 0/5 |
| xgboost | smollm3_3b | -25.538% | -25.185% | +0.263% | 0/5 |
| xgboost | qwen3_8b | -19.402% | -19.096% | +4.973% | 0/5 |

Quality-valid acquisitions: 754/800; penalties: 46. Minimum acquired XGBoost accuracy: 73.291%. Unstable validation cells: 1/70. Below10ms: 0/70. Same configuration as sequential: 6/20. These flags do not exclude cases from means.

## Frozen routing policies

Benefit/uncertainty thresholds were transported unchanged from historical development groups. No refitting on these outcomes. Hindsight is a non-deployable reference; BORA/rank are checkpoint adaptations, not full original implementations.

| Model | Policy | Calls / 10 | Equal-family mean gain vs never |
|---|---|---:|---:|
| smollm3_3b | never | 0.00 | +0.000% |
| smollm3_3b | always | 10.00 | -12.734% |
| smollm3_3b | benefit | 0.00 | +0.000% |
| smollm3_3b | uncertainty | 0.00 | +0.000% |
| smollm3_3b | random_development_rate | 1.00 | -5.240% |
| smollm3_3b | bora_adaptation | 7.00 | -7.542% |
| smollm3_3b | rank_draw_adaptation | 4.00 | -5.034% |
| smollm3_3b | random_matched_rate | 0.00 | +0.000% |
| smollm3_3b | rank_expected_adaptation | 2.70 | -4.449% |
| smollm3_3b | hindsight_oracle | 4.00 | +1.343% |
| qwen3_8b | never | 0.00 | +0.000% |
| qwen3_8b | always | 10.00 | -10.109% |
| qwen3_8b | benefit | 0.00 | +0.000% |
| qwen3_8b | uncertainty | 0.00 | +0.000% |
| qwen3_8b | random_development_rate | 0.00 | +0.000% |
| qwen3_8b | bora_adaptation | 7.00 | -5.112% |
| qwen3_8b | rank_draw_adaptation | 4.00 | -6.644% |
| qwen3_8b | random_matched_rate | 0.00 | +0.000% |
| qwen3_8b | rank_expected_adaptation | 2.70 | -4.338% |
| qwen3_8b | hindsight_oracle | 4.00 | +1.897% |

## Actual research cost and deployment estimates

Native collection: 470.697 subprocess-seconds including 187.919 objective-seconds. End-to-end paired collection 544.017s. Earlier source/preparation work and60feasibility attempts (including20failed Polars attempts) are additional costs. No paid/cloud requests.

- smollm3_3b: 10 starts, 10 responses; observed input/output tokens 4833/411; unknown usage {'tokens_evaluated': 0, 'tokens_predicted': 0}; requests 16.373s; entire model stage 18.315s; peak RSS 3031203840bytes; server exit 0.
- qwen3_8b: 10 starts, 10 responses; observed input/output tokens 5714/581; unknown usage {'tokens_evaluated': 0, 'tokens_predicted': 0}; requests 43.791s; entire model stage 48.863s; peak RSS 6778339328bytes; server exit 0.

One selected deployment branch per case would use200configuration outcomes and400query/training executions across ten cases. comparison.json estimates time by selecting recorded prefix/branch/request costs. This is a retrospective proxy, not an actual deployment; cold model startup is separate. Actual study collection includes every counterfactual branch and therefore costs more.

## Limitations

Two software implementations, one host, five seeds each. Repeated seeds are not independent systems. Polars shares its data/query contract with earlier DuckDB work. XGBoost quality-validation labels constrain optimization, not classifier-generalization evaluation. Native threading, warmed filesystem caches, constrained proposals, projection, fixed seeds, small finite grids and quantized models limit scope. Historical router calibration used a different budget/target and may not transfer. Quality penalties alter the loss distribution. No journal quartile or population-level benefit follows from these measurements. Both applications are development-exposed for future work.

All failed V166 Polars attempts remain visible. V167 repaired only NA null parsing under a new freeze; no threshold or workload was selected by LLM benefit. Source provenance and admission reports: reports/protocol_v166.md, reports/feasibility_v166.md, reports/feasibility_v167.md. Frozen V168 code, prompts, prefixes, models and router decisions: artifacts/study_v168. All native records and validations: results/v168_native; real model requests/responses/costs: results/v168_models. Safe report replay: .venv/bin/python scripts/report_apps_v168.py.
