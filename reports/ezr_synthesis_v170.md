# Source-executed EZR baseline extension: six implementations

The unchanged pinned EZR acquisition code now executes as two explicitly adapted checkpoint controls across all six recent native implementations. Existing real-model choices are revalidated beside these controls. This addresses source-code execution and comparator coverage; it does not test an improved model or retrain the controller.

| Implementation | Model | Gain vs sequential | vs EZR centroid | vs EZR Bayes | Joint robust wins /5 |
|---|---|---:|---:|---:|---:|
| cvc5 | smollm3_3b | -0.110% | -0.987% | -1.003% | 0 |
| cvc5 | qwen3_8b | +0.165% | -0.704% | -0.717% | 0 |
| ortools | smollm3_3b | -20.672% | -20.439% | -21.123% | 0 |
| ortools | qwen3_8b | -20.220% | -19.993% | -20.671% | 0 |
| ripgrep | smollm3_3b | -2.171% | -0.601% | +0.125% | 0 |
| ripgrep | qwen3_8b | -0.323% | +1.162% | +1.801% | 0 |
| hnswlib | smollm3_3b | -0.147% | -0.137% | +0.008% | 0 |
| hnswlib | qwen3_8b | -0.241% | -0.231% | -0.086% | 0 |
| polars | smollm3_3b | -5.068% | -0.863% | -4.790% | 0 |
| polars | qwen3_8b | -4.828% | -0.892% | -4.620% | 0 |
| xgboost | smollm3_3b | -26.111% | -12.100% | -23.183% | 0 |
| xgboost | qwen3_8b | -19.525% | -7.092% | -16.631% | 0 |

All comparator gains, individual cases, same-setting flags and noise/quality diagnostics are retained in the two stage comparison.json files. Gains use same-stage fresh-validation medians; old primary results remain unchanged. No new model request, response, prompt or source download occurred.

New collection: 1230 outcomes; 2460 workload executions; 420 search labels and 810 validation labels; 460.617 seconds across two bounded stages. Sixty new source-method B20 arms reuse300historically acquired prefix outcomes (600logical cached prefix callbacks). Revalidation of210historical selected settings costs630additional outcomes outside their closed policy budgets.

The six implementation labels are not six randomly sampled independent production tasks. cvc5/OR-Tools share constructed N-queens workloads; Polars shares an earlier DuckDB flight workload; ripgrep/hnswlib use compact real public inputs. Repeated seeds, source-method variants and revalidation do not add software systems. Historical searches and new source searches occurred at different times. These secondary results provide no population significance, useful-controller guarantee or journal-quartile certification.

Reports: reports/ezr_v169.md and reports/ezr_v170.md. Protocol/source adaptations: reports/protocol_v169.md and reports/protocol_v170.md. All independent-host, broader-model and full original-method limitations remain.
