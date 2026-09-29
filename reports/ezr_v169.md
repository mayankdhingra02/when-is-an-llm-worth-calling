# V169: source-executed EZR continuation controls

Executed unchanged pinned EZR0.9.4 acquire/centroid/Naive Bayes code with an explicit saved-prefix wrapper. This is a checkpoint adaptation, not full from-scratch EZR or SNAP2 replication. Unknown objective slots were question marks; callbacks acquired one label at a time.

20 new continuation arms used10historical prefix labels +7new native outcomes +3fresh validations each. All70historical V168 model/control selections were additionally revalidated in the same randomized blocks. Those210extra measurements are diagnostic research costs outside the original closed budgets.

## Same-session validated outcomes

| Application | Arm | Mean of five validation medians (seconds) | Quality-valid /5 | Unstable /5 |
|---|---|---:|---:|---:|
| polars | sequential_3nn | 0.022173 | 5 | 0 |
| polars | adaptive_neighbor | 0.022200 | 5 | 2 |
| polars | gp_ei | 0.023379 | 5 | 0 |
| polars | random_full | 0.023442 | 5 | 1 |
| polars | random_proposal | 0.023139 | 5 | 0 |
| polars | ezr_upstream_centroid | 0.023053 | 5 | 0 |
| polars | ezr_upstream_bayes | 0.022182 | 5 | 0 |
| polars | smollm3_3b | 0.023244 | 5 | 1 |
| polars | qwen3_8b | 0.023208 | 5 | 0 |
| xgboost | sequential_3nn | 0.208979 | 5 | 0 |
| xgboost | adaptive_neighbor | 0.209205 | 5 | 0 |
| xgboost | gp_ei | 0.261162 | 5 | 0 |
| xgboost | random_full | 0.229578 | 5 | 0 |
| xgboost | random_proposal | 0.234098 | 5 | 0 |
| xgboost | ezr_upstream_centroid | 0.235868 | 5 | 0 |
| xgboost | ezr_upstream_bayes | 0.213383 | 5 | 0 |
| xgboost | smollm3_3b | 0.263613 | 5 | 0 |
| xgboost | qwen3_8b | 0.249850 | 5 | 0 |

Positive paired gain favors the historical model-selected configuration. Gains below are means of per-case ratios; they differ from ratios of mean runtimes.

| Application | Model | vs sequential | vs adaptive | vs GP | vs EZR centroid | vs EZR Bayes | Joint robust wins /5 |
|---|---|---:|---:|---:|---:|---:|---:|
| polars | smollm3_3b | -5.068% | -4.703% | +0.506% | -0.863% | -4.790% | 0 |
| polars | qwen3_8b | -4.828% | -4.508% | +0.630% | -0.892% | -4.620% | 0 |
| xgboost | smollm3_3b | -26.111% | -26.129% | -0.753% | -12.100% | -23.183% | 0 |
| xgboost | qwen3_8b | -19.525% | -19.537% | +4.119% | -7.092% | -16.631% | 0 |

Robust joint gain requires >10% over all five listed comparators, different configurations, all fresh quality-valid results, medians>=10ms and relativeMAD<=5%. No case is dropped for failing that diagnostic. Candidate-level outputs and every gain remain in comparison.json.

## Cost and provenance

410new acquired outcomes;820query/training executions;140new search outcomes and270fresh validation outcomes. Actual stage 213.014s/1800s, native objective time 59.587s, subprocess wall 211.281s. Owner-optimizer/bridge process CPU 0.077158s excludes child native execution. Quality penalties: 14. No new model request, download, retry, cloud use or payment. Original source/input/model collection remains a historical cost.

The source is pinned to bfda80b3b797d142378f7fb8746c3485610fb17e with MIT notice retained. Native workers remain the unchanged Polars/XGBoost versions. The existing Python3.13.3 interpreter supports owner syntax; its binary hash is frozen. Acquire itself is unchanged; warm-start order, ten cached labels, seven additional acquisitions, feature typing, single scalar loss and raw-loss incumbent selection are documented adaptations. Literal normalization, smoothing and cached-centroid behavior are preserved.

## Limits

New EZR search occurred later than the original classical/model search. Simultaneous randomized validation reduces final-scoring timing differences but cannot remove temporal effects on historical search selection. No LLM response was regenerated, synthesized or substituted; all model selections derive from the exact retained real responses and prefixes. This is an exploratory control extension after prior outcome exposure, not a new held-out model study. Two implementation groups, one host, repeated seeds and shared flight workload do not establish population generalization. Source execution narrows an implementation gap; full prior methods and independent-host replication remain untested.

Evidence: artifacts/study_v169/{freeze.json,plan.json,runtime.json}; results/v169_ezr/{optimizer_inputs,optimizer_events,search,acquisitions,selections.json,validation_plan.json,comparison.json}. Prior V168 results remain unchanged.
