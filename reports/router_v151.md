# V151: rare-benefit prediction and related-system sensitivity

**Exploratory analysis of70existing real paired cases/model; no new LLM calls or acquired objectives.** The fixed candidate models are original ridge, richer18-feature ridge, depth2tree and RBFkernel ridge. Nested whole-group folds fit preprocessing, models, thresholds and model selection on development only. Prior exposure still prevents a confirmatory claim. All variants appear below.

V149 was rejected by independent replay because Spark/Hadoop short case names collided. Its invalid outputs are retained but excluded from all tables here. V151 qualifies case keys by original engine family and adds a collision regression test before refreezing/rerunning the identical analysis. Historical experiments remain intact.

## Eight execution-engine groups

| Model / policy | Calls /70 | Equal-group gain | Above matched random | Useful >1% | Harmful >1% | Joint useful | Missed useful |
|---|---:|---:|---:|---:|---:|---:|---:|
| smollm3_3b / always | 70 | -4.62300% | +0.00000% | 10 | 24 | 7 | 0 |
| smollm3_3b / never | 0 | +0.00000% | +0.00000% | 0 | 0 | 0 | 10 |
| smollm3_3b / rbf_extended | 0 | +0.00000% | +0.00000% | 0 | 0 | 0 | 10 |
| smollm3_3b / rbf_extended_q80 | 6 | -0.05045% | +0.00827% | 0 | 1 | 0 | 10 |
| smollm3_3b / ridge_extended | 0 | +0.00000% | +0.00000% | 0 | 0 | 0 | 10 |
| smollm3_3b / ridge_extended_q80 | 28 | -0.05225% | -0.01370% | 7 | 8 | 4 | 3 |
| smollm3_3b / ridge_original | 0 | +0.00000% | +0.00000% | 0 | 0 | 0 | 10 |
| smollm3_3b / ridge_original_q80 | 28 | -0.03040% | +0.01360% | 7 | 7 | 4 | 3 |
| smollm3_3b / selected_predictor | 1 | +0.00754% | +0.00809% | 1 | 0 | 0 | 9 |
| smollm3_3b / tree_extended | 1 | +0.00754% | +0.00809% | 1 | 0 | 0 | 9 |
| smollm3_3b / tree_extended_q80 | 18 | -0.56836% | +0.00841% | 2 | 7 | 1 | 8 |
| smollm3_3b / uncertainty | 1 | +0.00000% | +0.17692% | 0 | 0 | 0 | 10 |
| smollm3_3b / uncertainty_q80 | 25 | -2.90137% | -1.33817% | 4 | 9 | 3 | 6 |
| qwen3_8b / always | 70 | -5.08530% | +0.00000% | 5 | 29 | 3 | 0 |
| qwen3_8b / never | 0 | +0.00000% | +0.00000% | 0 | 0 | 0 | 5 |
| qwen3_8b / rbf_extended | 0 | +0.00000% | +0.00000% | 0 | 0 | 0 | 5 |
| qwen3_8b / rbf_extended_q80 | 5 | -0.05045% | +0.00000% | 0 | 1 | 0 | 5 |
| qwen3_8b / ridge_extended | 0 | +0.00000% | +0.00000% | 0 | 0 | 0 | 5 |
| qwen3_8b / ridge_extended_q80 | 29 | -0.27612% | -0.04499% | 2 | 12 | 1 | 3 |
| qwen3_8b / ridge_original | 0 | +0.00000% | +0.00000% | 0 | 0 | 0 | 5 |
| qwen3_8b / ridge_original_q80 | 30 | -0.28807% | +0.00000% | 2 | 12 | 1 | 3 |
| qwen3_8b / selected_predictor | 0 | +0.00000% | +0.00000% | 0 | 0 | 0 | 5 |
| qwen3_8b / tree_extended | 0 | +0.00000% | +0.00000% | 0 | 0 | 0 | 5 |
| qwen3_8b / tree_extended_q80 | 20 | -0.92412% | -0.13312% | 2 | 12 | 2 | 3 |
| qwen3_8b / uncertainty | 0 | +0.00000% | +0.00000% | 0 | 0 | 0 | 5 |
| qwen3_8b / uncertainty_q80 | 25 | -2.83358% | -1.01830% | 1 | 8 | 1 | 4 |
## Seven groups: Spark and Hadoop merged

| Model / policy | Calls /70 | Equal-group gain | Above matched random | Useful >1% | Harmful >1% | Joint useful | Missed useful |
|---|---:|---:|---:|---:|---:|---:|---:|
| smollm3_3b / always | 70 | -4.95588% | +0.00000% | 10 | 24 | 7 | 0 |
| smollm3_3b / never | 0 | +0.00000% | +0.00000% | 0 | 0 | 0 | 10 |
| smollm3_3b / rbf_extended | 0 | +0.00000% | +0.00000% | 0 | 0 | 0 | 10 |
| smollm3_3b / rbf_extended_q80 | 5 | -0.05766% | +0.00000% | 0 | 1 | 0 | 10 |
| smollm3_3b / ridge_extended | 0 | +0.00000% | +0.00000% | 0 | 0 | 0 | 10 |
| smollm3_3b / ridge_extended_q80 | 9 | -0.10492% | -0.00945% | 0 | 2 | 0 | 10 |
| smollm3_3b / ridge_original | 0 | +0.00000% | +0.00000% | 0 | 0 | 0 | 10 |
| smollm3_3b / ridge_original_q80 | 8 | -0.10492% | -0.01890% | 0 | 2 | 0 | 10 |
| smollm3_3b / selected_predictor | 0 | +0.00000% | +0.00000% | 0 | 0 | 0 | 10 |
| smollm3_3b / tree_extended | 0 | +0.00000% | +0.00000% | 0 | 0 | 0 | 10 |
| smollm3_3b / tree_extended_q80 | 4 | -2.96964% | -0.58209% | 0 | 2 | 0 | 10 |
| smollm3_3b / uncertainty | 1 | +0.00000% | +0.20219% | 0 | 0 | 0 | 10 |
| smollm3_3b / uncertainty_q80 | 27 | -3.12346% | -1.53666% | 4 | 10 | 3 | 6 |
| qwen3_8b / always | 70 | -5.23985% | +0.00000% | 5 | 29 | 3 | 0 |
| qwen3_8b / never | 0 | +0.00000% | +0.00000% | 0 | 0 | 0 | 5 |
| qwen3_8b / rbf_extended | 0 | +0.00000% | +0.00000% | 0 | 0 | 0 | 5 |
| qwen3_8b / rbf_extended_q80 | 5 | -0.05766% | +0.00000% | 0 | 1 | 0 | 5 |
| qwen3_8b / ridge_extended | 0 | +0.00000% | +0.00000% | 0 | 0 | 0 | 5 |
| qwen3_8b / ridge_extended_q80 | 9 | -0.10167% | -0.05142% | 0 | 2 | 0 | 5 |
| qwen3_8b / ridge_original | 0 | +0.00000% | +0.00000% | 0 | 0 | 0 | 5 |
| qwen3_8b / ridge_original_q80 | 7 | -0.05766% | -0.00371% | 0 | 1 | 0 | 5 |
| qwen3_8b / selected_predictor | 0 | +0.00000% | +0.00000% | 0 | 0 | 0 | 5 |
| qwen3_8b / tree_extended | 0 | +0.00000% | +0.00000% | 0 | 0 | 0 | 5 |
| qwen3_8b / tree_extended_q80 | 8 | -0.44856% | +1.78689% | 0 | 4 | 0 | 5 |
| qwen3_8b / uncertainty | 0 | +0.00000% | +0.00000% | 0 | 0 | 0 | 5 |
| qwen3_8b / uncertainty_q80 | 27 | -3.15763% | -1.40488% | 1 | 10 | 1 | 4 |

The selected predictor uses inner development utility to choose among allfourfixed models; the table also retains each separate predictor and its development80th-percentile policy. Matched random is a retrospective expected score at the same held-group call count; no outcome informs its selection. Never-call has zero gain by definition. A positive difference from random can still be a loss against never-call.

With eight engine groups, SmolLM selected one useful Spark call: equal-group gain+0.00754%, above matched random+0.00809percentage points. It missed9/10useful opportunities and selected no joint >1%win over both sequential and adaptive. Qwen selected no calls. When Spark/Hadoop are one ecosystem group, both selected predictors choose zero calls. This small apparent success is therefore insufficient evidence of independent-system transfer or a practically useful general router. It must not be promoted to a successful method by selecting only the favorable grouping.

| Grouping / model | Oracle equal-group gain | Useful-opportunity groups | Joint-opportunity groups |
|---|---:|---|---|
| engine / smollm3_3b | 0.40708% | hadoop_mapreduce, spark | hadoop_mapreduce, spark |
| engine / qwen3_8b | 0.30354% | berkeleydb, hadoop_mapreduce, spark | hadoop_mapreduce, spark |
| ecosystem / smollm3_3b | 0.22204% | spark_hadoop_ecosystem | spark_hadoop_ecosystem |
| ecosystem / qwen3_8b | 0.17843% | berkeleydb, spark_hadoop_ecosystem | spark_hadoop_ecosystem |

Oracle is diagnostic hindsight, not deployable. Per-family ranking AUCs, all inner/outer training memberships and fitted coefficients/trees, threshold grids, prediction scores, decisions, exact selected case IDs, pooled means, leave-one-group aggregate ranges, usage/fallback counters and fixed random selections are stored in folds.json/comparison.json. AUC is undefined in one-class families; those remain null, not zero or silently excluded cases.

Analysis consumed1.517seconds/600second cap. Selected-token/time fields reuse observed historical costs as counterfactual deployment estimates; original data-collection costs remain paid in the project ledger. One historical interrupted SmolLM request stays as fallback with unknown usage. No new native run, request, token or acquisition is caused by this analysis.

Independent replay verifies140cases,30outer folds, ridge/RBF fits via augmented least-squares algebra, tree split optimality, group exclusions, calibration, decisions and primary aggregates, and rejects four in-memory semantic mutations. Saved normalization is authenticated against independently recomputed moments and then used at exact tree split boundaries to prevent verifier-only roundoff from changing a branch. The initial verifier boundary/quantile diagnostic logs are retained. Figures and this report are deterministic.

Limitations: onlysevenecosystems, most practical wins in the shared Spark/Hadoop ecosystem, heterogeneous representations/targets, prior inspection and repeated seeds, tiny gain at one selected case, and no prospective validation of these new predictors. The practical margin remains1%per case; it is not an aggregate non-inferiority margin. No population confidence/significance, equivalence, novelty or journal acceptance claim follows. The native Memcached feasibility check is separate and does not enter these aggregates.
