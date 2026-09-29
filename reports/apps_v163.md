# V163: paired native application study

The study is complete on two application lineages using real public input: ripgrep code analytics over CPython source, and hnswlib indexing/querying Optdigits vectors. Workload design was exposed by feasibility. This is a prospective paired comparison after feasibility, not an untouched production cohort or a journal-readiness certificate.

## What ran

**800 configuration-outcome evaluations**, **2400 native workload invocations**, **20 real local-model starts**, and **70 B20 arms**. Ten saved prefixes (five seeds per family) were cloned into five classical controls and two model continuations. Each arm had ten shared prefix evaluations, seven new configurations and three fresh incumbent validations. A ripgrep outcome times one fixed bundle of five distinct queries; individual-query timings are not measured or supplied as extra labels.

## Measured results

Positive gain means a lower median fresh-validation utility. ANN utility requires at least95% tie-aware recall; otherwise the declared20second penalty applies. A robust joint win requires >10% gain over sequential, adaptive and GP-EI, different configuration IDs, all validations quality-feasible, MAD<=5% and both medians>=10ms.

| Application | Model | Mean gain vs sequential | vs adaptive | vs GP-EI | Joint robust wins |
|---|---|---:|---:|---:|---:|
| ripgrep | smollm3_3b | -1.295% | -0.647% | -2.174% | 0/5 |
| ripgrep | qwen3_8b | -0.368% | +0.258% | -1.218% | 0/5 |
| hnswlib | smollm3_3b | -0.401% | -0.347% | +0.750% | 0/5 |
| hnswlib | qwen3_8b | -0.123% | -0.075% | +1.029% | 0/5 |

Quality-feasible acquisitions: 800/800; quality penalties: 0. Minimum observed ANN recall: 98.169%. Validation cells above5% MAD: 2/70; below10ms: 0/70. Model/sequential pairs selecting the same setting: 16/20. These flags do not remove outcomes from the unfiltered mean. All five classical controls and individual gains remain in comparison.json.

## Frozen routing policies

Historical benefit/uncertainty models were transported unchanged; no threshold was fitted on these applications. Pre-continuation features and decisions were saved and hashed. BORA/rank rules remain checkpoint adaptations of source methods, not full original implementations. Rank expectation is a mathematical counterfactual average over real measured outcomes. The hindsight oracle is not deployable.

| Model | Policy | Calls or expected calls / 10 | Equal-family mean gain vs never |
|---|---|---:|---:|
| smollm3_3b | never | 0.00 | +0.000% |
| smollm3_3b | always | 10.00 | -0.848% |
| smollm3_3b | benefit | 0.00 | +0.000% |
| smollm3_3b | uncertainty | 0.00 | +0.000% |
| smollm3_3b | random_development_rate | 0.00 | +0.000% |
| smollm3_3b | bora_adaptation | 6.00 | -0.308% |
| smollm3_3b | rank_draw_adaptation | 1.00 | +0.153% |
| smollm3_3b | random_matched_rate | 0.00 | +0.000% |
| smollm3_3b | rank_expected_adaptation | 2.40 | -0.081% |
| smollm3_3b | hindsight_oracle | 3.00 | +0.203% |
| qwen3_8b | never | 0.00 | +0.000% |
| qwen3_8b | always | 10.00 | -0.246% |
| qwen3_8b | benefit | 0.00 | +0.000% |
| qwen3_8b | uncertainty | 0.00 | +0.000% |
| qwen3_8b | random_development_rate | 0.00 | +0.000% |
| qwen3_8b | bora_adaptation | 6.00 | +0.008% |
| qwen3_8b | rank_draw_adaptation | 1.00 | +0.067% |
| qwen3_8b | random_matched_rate | 0.00 | +0.000% |
| qwen3_8b | rank_expected_adaptation | 2.40 | -0.099% |
| qwen3_8b | hindsight_oracle | 4.00 | +0.408% |

## Collection cost versus deployment estimate

Actual paired native collection: 258.324 subprocess-seconds, including 195.997 objective-seconds. End-to-end paired stage: 330.818s. Prior80 feasibility outcomes/160 native invocations, source retrieval, compilation and correctness-reference work are additional research costs. Both continuations, controls and validation remain charged.

- smollm3_3b: 10 starts/10 responses; observed input/output tokens 4653/376; unknown-usage request counts {'tokens_evaluated': 0, 'tokens_predicted': 0}; request time 15.608s; total model-stage time 17.536s; peak RSS 2985312256 bytes; server exit 0.
- qwen3_8b: 10 starts/10 responses; observed input/output tokens 5418/543; unknown-usage request counts {'tokens_evaluated': 0, 'tokens_predicted': 0}; request time 42.583s; total model-stage time 47.129s; peak RSS 6561988608 bytes; server exit 0.

For ten-case deployment, one selected arm per case uses200 configuration evaluations and600 native invocations (five ripgrep cases ×100 invocations plus five ANN cases ×20). Model request count depends on the policy. comparison.json gives a retrospective selected-branch time proxy using measured branch/request durations; cold-start time is separate. It is not a measured deployment, invoice or energy estimate. No paid/cloud inference or new model download occurred.

## Scope and limitations

Only two independent implementation groups are added. Seeds, query types and vectors are not independent systems. Inputs are real public data but these tasks are not production deployments. Source/reference reads warm caches; no cache flushing or system changes were used. Timing is from one machine. Approximate-neighbor quality is task-specific, and the historical router target used20 search evaluations versus the present17+3 design. Quantized model families, constrained batch proposals, projection, public-data familiarity, budget and workload-design exposure limit generalization. No population significance, equivalence, full prior-method replication or journal acceptance follows.

Failed V161 admission and the separately frozen V162 repair are retained. GNU sort was excluded after an alias audit found prior measured history. All observed outcomes belong to development/exploratory evidence for any subsequent protocol; do not retune here and call the same cases held out. The next priority is independent replication and broader prospectively selected application evidence, with this comparison set fixed.

Evidence: artifacts/study_v163 contains frozen inputs, prefixes/prompts, model pins and router decisions. results/v163_native contains all800 acquisitions, branch states, fixed selections,210 validations, aggregates and figures. results/v163_models contains raw prompts/responses, starts, token accounting, capacity checks and process-exit receipts. Safe report replay: .venv/bin/python scripts/report_apps_v163.py; collectors are create-once.
