# V168 exploratory modeled break-even diagnostic

Each number is an estimate from measured branch/request costs and fresh-validation medians. It assumes repeating this same workload. No production workload or deployment savings were measured. Null means no positive break-even claim under the fixed rule. Cold startup is charged once per hypothetical case.

| Case | Model | Robust gain vs sequential | Warm marginal seconds | Warm break-even bundles | Cold break-even bundles |
|---|---|---|---:|---:|---:|
| polars_11 | smollm3_3b | False | 1.7822553359874291 | 1674 | 3351 |
| polars_23 | smollm3_3b | False | 1.4323499590100255 | None | None |
| polars_37 | smollm3_3b | False | 2.051035622978816 | None | None |
| polars_53 | smollm3_3b | False | 2.2192759979807306 | None | None |
| polars_71 | smollm3_3b | False | 1.6259143730130745 | None | None |
| xgboost_11 | smollm3_3b | False | 3.8042595009465003 | None | None |
| xgboost_23 | smollm3_3b | False | 3.65963658306282 | None | None |
| xgboost_37 | smollm3_3b | False | 6.827609330997802 | None | None |
| xgboost_53 | smollm3_3b | False | 3.974057372979587 | None | None |
| xgboost_71 | smollm3_3b | False | 7.4415651229792275 | None | None |
| polars_11 | qwen3_8b | False | 4.696724918001564 | None | None |
| polars_23 | qwen3_8b | False | 4.768173916992964 | None | None |
| polars_37 | qwen3_8b | False | 4.624658583998098 | None | None |
| polars_53 | qwen3_8b | False | 4.748731830986799 | None | None |
| polars_71 | qwen3_8b | False | 4.605705328009208 | None | None |
| xgboost_11 | qwen3_8b | False | 6.124711706943344 | None | None |
| xgboost_23 | qwen3_8b | False | 6.764095414022449 | None | None |
| xgboost_37 | qwen3_8b | False | 5.738733161982964 | None | None |
| xgboost_53 | qwen3_8b | False | 5.745576709028683 | 1594 | 2927 |
| xgboost_71 | qwen3_8b | False | 10.357478331017774 | None | None |

Break-even does not establish a reliable controller, superiority to GP, or a positive amortized result for a different workload. Full noise, quality, same-setting, costs and fixed-count net-time projections are retained in results/v168_native/cost_diagnostic.json. Actual source, failed admission and all-branch collection costs remain separate.
