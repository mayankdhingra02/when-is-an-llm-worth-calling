# V170: source-executed EZR continuation controls

Executed unchanged pinned EZR0.9.4 acquire/centroid/Naive Bayes code with an explicit saved-prefix wrapper. This is a checkpoint adaptation, not full from-scratch EZR or SNAP2 replication. Unknown objective slots were question marks; callbacks acquired one label at a time.

40 new continuation arms used10historical prefix labels +7new native outcomes +3fresh validations each. All140historical V159/V163 model/control selections were additionally revalidated in the same randomized blocks. Those420extra measurements are diagnostic research costs outside the original closed budgets.

## Same-session validated outcomes

| Application | Arm | Mean of five validation medians (seconds) | Quality-valid /5 | Unstable /5 |
|---|---|---:|---:|---:|
| cvc5 | sequential_3nn | 0.031493 | 5 | 0 |
| cvc5 | adaptive_neighbor | 0.031409 | 5 | 0 |
| cvc5 | gp_ei | 0.031390 | 5 | 0 |
| cvc5 | random_full | 0.031379 | 5 | 0 |
| cvc5 | random_proposal | 0.031526 | 5 | 0 |
| cvc5 | ezr_upstream_centroid | 0.031222 | 5 | 0 |
| cvc5 | ezr_upstream_bayes | 0.031219 | 5 | 0 |
| cvc5 | smollm3_3b | 0.031528 | 5 | 0 |
| cvc5 | qwen3_8b | 0.031441 | 5 | 0 |
| ortools | sequential_3nn | 0.009598 | 5 | 0 |
| ortools | adaptive_neighbor | 0.009554 | 5 | 0 |
| ortools | gp_ei | 0.009539 | 5 | 0 |
| ortools | random_full | 0.011520 | 5 | 0 |
| ortools | random_proposal | 0.011516 | 5 | 0 |
| ortools | ezr_upstream_centroid | 0.009626 | 5 | 0 |
| ortools | ezr_upstream_bayes | 0.009567 | 5 | 0 |
| ortools | smollm3_3b | 0.011562 | 5 | 0 |
| ortools | qwen3_8b | 0.011518 | 5 | 0 |
| ripgrep | sequential_3nn | 0.269756 | 5 | 0 |
| ripgrep | adaptive_neighbor | 0.271154 | 5 | 0 |
| ripgrep | gp_ei | 0.269682 | 5 | 0 |
| ripgrep | random_full | 0.279150 | 5 | 0 |
| ripgrep | random_proposal | 0.273860 | 5 | 0 |
| ripgrep | ezr_upstream_centroid | 0.273887 | 5 | 0 |
| ripgrep | ezr_upstream_bayes | 0.275815 | 5 | 0 |
| ripgrep | smollm3_3b | 0.275478 | 5 | 0 |
| ripgrep | qwen3_8b | 0.270546 | 5 | 0 |
| hnswlib | sequential_3nn | 0.095482 | 5 | 0 |
| hnswlib | adaptive_neighbor | 0.095316 | 5 | 0 |
| hnswlib | gp_ei | 0.095631 | 5 | 0 |
| hnswlib | random_full | 0.095604 | 5 | 0 |
| hnswlib | random_proposal | 0.095959 | 5 | 0 |
| hnswlib | ezr_upstream_centroid | 0.095492 | 5 | 0 |
| hnswlib | ezr_upstream_bayes | 0.095629 | 5 | 0 |
| hnswlib | smollm3_3b | 0.095621 | 5 | 0 |
| hnswlib | qwen3_8b | 0.095713 | 5 | 0 |

Positive paired gain favors the historical model-selected configuration. Gains below are means of per-case ratios; they differ from ratios of mean runtimes.

| Application | Model | vs sequential | vs adaptive | vs GP | vs EZR centroid | vs EZR Bayes | Joint robust wins /5 |
|---|---|---:|---:|---:|---:|---:|---:|
| cvc5 | smollm3_3b | -0.110% | -0.393% | -0.442% | -0.987% | -1.003% | 0 |
| cvc5 | qwen3_8b | +0.165% | -0.104% | -0.158% | -0.704% | -0.717% | 0 |
| ortools | smollm3_3b | -20.672% | -21.175% | -21.350% | -20.439% | -21.123% | 0 |
| ortools | qwen3_8b | -20.220% | -20.722% | -20.896% | -19.993% | -20.671% | 0 |
| ripgrep | smollm3_3b | -2.171% | -1.601% | -2.264% | -0.601% | +0.125% | 0 |
| ripgrep | qwen3_8b | -0.323% | +0.220% | -0.386% | +1.162% | +1.801% | 0 |
| hnswlib | smollm3_3b | -0.147% | -0.323% | +0.010% | -0.137% | +0.008% | 0 |
| hnswlib | qwen3_8b | -0.241% | -0.416% | -0.084% | -0.231% | -0.086% | 0 |

Robust joint gain requires >10% over all five listed comparators, different configurations, all fresh quality-valid results, medians>=10ms and relativeMAD<=5%. No case is dropped for failing that diagnostic. Candidate-level outputs and every gain remain in comparison.json.

## Cost and provenance

820new acquired outcomes;1640native workload invocations;280new search outcomes and540fresh validation outcomes. Actual stage 247.603s/1800s, native objective time 132.943s, subprocess wall 243.458s. Owner-optimizer/bridge process CPU 0.098974s excludes child native execution. Quality penalties: 0. No new model request, download, retry, cloud use or payment. Original source/input/model collection remains a historical cost.

The source is pinned to bfda80b3b797d142378f7fb8746c3485610fb17e with MIT notice retained. Native workers remain unchanged: cvc5/OR-Tools solve the constructed N-queens tasks; ripgrep/hnswlib use the original CPython/Optdigits inputs. No new industrial workload is claimed. The existing Python3.13.3 interpreter supports owner syntax; its binary hash is frozen. Acquire itself is unchanged; warm-start order, ten cached labels, seven additional acquisitions, feature typing, single scalar loss and raw-loss incumbent selection are documented adaptations. Literal normalization, smoothing and cached-centroid behavior are preserved.

## Limits

New EZR search occurred later than the original classical/model search. Simultaneous randomized validation reduces final-scoring timing differences but cannot remove temporal effects on historical search selection. No LLM response was regenerated, synthesized or substituted; all model selections derive from the exact retained real responses and prefixes. This is an exploratory control extension after prior outcome exposure, not a new held-out model study. Four implementation groups, one host, repeated seeds and a shared constructed N-queens task do not establish population generalization. Source execution narrows an implementation gap; full prior methods and independent-host replication remain untested.

Evidence: artifacts/study_v170/{freeze.json,plan.json,runtime.json}; results/v170_ezr/{optimizer_inputs,optimizer_events,search,acquisitions,selections.json,validation_plan.json,comparison.json}. Prior V159/V163 results remain unchanged.
