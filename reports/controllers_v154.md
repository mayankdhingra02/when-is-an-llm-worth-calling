# V154: conditional-call checkpoint adaptations

Exploratory reuse of140genuine historical model-cases,70/model, eight engine families or seven ecosystems with Spark/Hadoop merged. No new LLM call, synthetic response, or objective acquisition. Prior collection costs remain paid. These are paper-inspired fixed-checkpoint adaptations, not full BORA/LB-MCTS execution; exact mapping and departures are frozen in [protocol_v154.md](protocol_v154.md). Both kernel scales and capped-history diagnostic remain reported.

## ecosystem grouping

| Model / policy | Calls or expected calls /70 | Group mean gain | Above matched random | Gain vs adaptive | Useful / harmful | Joint useful |
|---|---:|---:|---:|---:|---|---:|
| qwen3_8b / always | 70.00 | -5.2398% | +0.0000pp | -3.0869% | 5.00 / 29.00 | 3.00 |
| qwen3_8b / benefit_v151 | 0.00 | +0.0000% | +0.0000pp | +1.6151% | 0.00 / 0.00 | 0.00 |
| qwen3_8b / bora_0.2 | 14.00 | -3.2476% | -0.1123pp | -1.0077% | 0.00 / 8.00 | 0.00 |
| qwen3_8b / bora_1.0 | 14.00 | -3.2476% | -0.1123pp | -1.0077% | 0.00 / 8.00 | 0.00 |
| qwen3_8b / bora_capped_0.2 | 46.00 | -4.9073% | -0.5775pp | -2.7742% | 3.00 / 21.00 | 1.00 |
| qwen3_8b / bora_capped_1.0 | 46.00 | -4.9073% | -0.5775pp | -2.7742% | 3.00 / 21.00 | 1.00 |
| qwen3_8b / gp_uncertainty_calibrated | 0.00 | +0.0000% | +0.0000pp | +1.6151% | 0.00 / 0.00 | 0.00 |
| qwen3_8b / never | 0.00 | +0.0000% | +0.0000pp | +1.6151% | 0.00 / 0.00 | 0.00 |
| qwen3_8b / rank_calibrated | 0.00 | +0.0000% | +0.0000pp | +1.6151% | 0.00 / 0.00 | 0.00 |
| qwen3_8b / rank_draw_0.2 | 27.00 | -3.0983% | -1.2492pp | -0.9758% | 2.00 / 11.00 | 1.00 |
| qwen3_8b / rank_draw_1.0 | 23.00 | -2.8562% | -1.1111pp | -0.7336% | 2.00 / 7.00 | 1.00 |
| qwen3_8b / rank_expected_0.2 | 24.35 | -1.8539% | -0.6270pp | -0.0404% | 2.00 / 10.40 | 1.20 |
| qwen3_8b / rank_expected_1.0 | 23.95 | -1.4877% | -0.3222pp | +0.3169% | 2.40 / 10.00 | 1.40 |
| qwen3_8b / uncertainty_v151 | 0.00 | +0.0000% | +0.0000pp | +1.6151% | 0.00 / 0.00 | 0.00 |
| smollm3_3b / always | 70.00 | -4.9559% | +0.0000pp | -2.8289% | 10.00 / 24.00 | 7.00 |
| smollm3_3b / benefit_v151 | 0.00 | +0.0000% | +0.0000pp | +1.6151% | 0.00 / 0.00 | 0.00 |
| smollm3_3b / bora_0.2 | 14.00 | -3.1021% | -0.0721pp | -0.8733% | 2.00 / 6.00 | 2.00 |
| smollm3_3b / bora_1.0 | 14.00 | -3.1021% | -0.0721pp | -0.8733% | 2.00 / 6.00 | 2.00 |
| smollm3_3b / bora_capped_0.2 | 46.00 | -4.6826% | -0.5500pp | -2.5678% | 7.00 / 16.00 | 5.00 |
| smollm3_3b / bora_capped_1.0 | 46.00 | -4.6826% | -0.5500pp | -2.5678% | 7.00 / 16.00 | 5.00 |
| smollm3_3b / gp_uncertainty_calibrated | 0.00 | +0.0000% | +0.0000pp | +1.6151% | 0.00 / 0.00 | 0.00 |
| smollm3_3b / never | 0.00 | +0.0000% | +0.0000pp | +1.6151% | 0.00 / 0.00 | 0.00 |
| smollm3_3b / rank_calibrated | 0.00 | +0.0000% | +0.0000pp | +1.6151% | 0.00 / 0.00 | 0.00 |
| smollm3_3b / rank_draw_0.2 | 27.00 | -3.0660% | -1.3371pp | -0.9460% | 3.00 / 10.00 | 2.00 |
| smollm3_3b / rank_draw_1.0 | 23.00 | -2.8390% | -1.2103pp | -0.7192% | 6.00 / 6.00 | 4.00 |
| smollm3_3b / rank_expected_0.2 | 24.35 | -1.7794% | -0.6760pp | +0.0286% | 3.80 / 8.50 | 2.40 |
| smollm3_3b / rank_expected_1.0 | 23.95 | -1.4361% | -0.3916pp | +0.3625% | 4.80 / 7.50 | 3.40 |
| smollm3_3b / uncertainty_v151 | 1.00 | +0.0000% | +0.2022pp | +1.6151% | 0.00 / 0.00 | 0.00 |

## engine grouping

| Model / policy | Calls or expected calls /70 | Group mean gain | Above matched random | Gain vs adaptive | Useful / harmful | Joint useful |
|---|---:|---:|---:|---:|---|---:|
| qwen3_8b / always | 70.00 | -5.0853% | +0.0000pp | -2.6959% | 5.00 / 29.00 | 3.00 |
| qwen3_8b / benefit_v151 | 0.00 | +0.0000% | +0.0000pp | +1.8430% | 0.00 / 0.00 | 0.00 |
| qwen3_8b / bora_0.2 | 14.00 | -3.1537% | -0.1043pp | -0.7201% | 0.00 / 8.00 | 0.00 |
| qwen3_8b / bora_1.0 | 14.00 | -3.1537% | -0.1043pp | -0.7201% | 0.00 / 8.00 | 0.00 |
| qwen3_8b / bora_capped_0.2 | 46.00 | -4.6738% | -0.5857pp | -2.3296% | 3.00 / 21.00 | 1.00 |
| qwen3_8b / bora_capped_1.0 | 46.00 | -4.6738% | -0.5857pp | -2.3296% | 3.00 / 21.00 | 1.00 |
| qwen3_8b / gp_uncertainty_calibrated | 0.00 | +0.0000% | +0.0000pp | +1.8430% | 0.00 / 0.00 | 0.00 |
| qwen3_8b / never | 0.00 | +0.0000% | +0.0000pp | +1.8430% | 0.00 / 0.00 | 0.00 |
| qwen3_8b / rank_calibrated | 0.00 | +0.0000% | +0.0000pp | +1.8430% | 0.00 / 0.00 | 0.00 |
| qwen3_8b / rank_draw_0.2 | 27.00 | -2.7125% | -0.8948pp | -0.4270% | 2.00 / 11.00 | 1.00 |
| qwen3_8b / rank_draw_1.0 | 23.00 | -2.4610% | -0.8026pp | -0.1777% | 2.00 / 7.00 | 1.00 |
| qwen3_8b / rank_expected_0.2 | 24.35 | -1.7287% | -0.4763pp | +0.2952% | 2.00 / 10.40 | 1.20 |
| qwen3_8b / rank_expected_1.0 | 23.95 | -1.3970% | -0.2259pp | +0.6195% | 2.40 / 10.00 | 1.40 |
| qwen3_8b / uncertainty_v151 | 0.00 | +0.0000% | +0.0000pp | +1.8430% | 0.00 / 0.00 | 0.00 |
| smollm3_3b / always | 70.00 | -4.6230% | +0.0000pp | -2.2817% | 10.00 / 24.00 | 7.00 |
| smollm3_3b / benefit_v151 | 1.00 | +0.0075% | +0.0081pp | +1.8511% | 1.00 / 0.00 | 0.00 |
| smollm3_3b / bora_0.2 | 14.00 | -2.8860% | -0.0044pp | -0.4700% | 2.00 / 6.00 | 2.00 |
| smollm3_3b / bora_1.0 | 14.00 | -2.8860% | -0.0044pp | -0.4700% | 2.00 / 6.00 | 2.00 |
| smollm3_3b / bora_capped_0.2 | 46.00 | -4.2805% | -0.5002pp | -1.9619% | 7.00 / 16.00 | 5.00 |
| smollm3_3b / bora_capped_1.0 | 46.00 | -4.2805% | -0.5002pp | -1.9619% | 7.00 / 16.00 | 5.00 |
| smollm3_3b / gp_uncertainty_calibrated | 0.00 | +0.0000% | +0.0000pp | +1.8430% | 0.00 / 0.00 | 0.00 |
| smollm3_3b / never | 0.00 | +0.0000% | +0.0000pp | +1.8430% | 0.00 / 0.00 | 0.00 |
| smollm3_3b / rank_calibrated | 0.00 | +0.0000% | +0.0000pp | +1.8430% | 0.00 / 0.00 | 0.00 |
| smollm3_3b / rank_draw_0.2 | 27.00 | -2.7134% | -1.0898pp | -0.4219% | 3.00 / 10.00 | 2.00 |
| smollm3_3b / rank_draw_1.0 | 23.00 | -2.4564% | -0.9756pp | -0.1672% | 6.00 / 6.00 | 4.00 |
| smollm3_3b / rank_expected_0.2 | 24.35 | -1.6050% | -0.5494pp | +0.4106% | 3.80 / 8.50 | 2.40 |
| smollm3_3b / rank_expected_1.0 | 23.95 | -1.3058% | -0.3260pp | +0.7055% | 4.80 / 7.50 | 3.40 |
| smollm3_3b / uncertainty_v151 | 1.00 | +0.0000% | +0.1769pp | +1.8430% | 0.00 / 0.00 | 0.00 |

## Interpretation

At primary lengthscale1, 50/70prefixes have fewer post-initialization updates than the default plateau length requires. That produces no-call decisions by construction; the separately named capped-history policy exposes this sensitivity. The GP uncertainty ratio spans0.3245–0.7464; fixed covariance makes it a geometric signal rather than an outcome-calibrated uncertainty estimate. Across350two-point CVfolds, 4have undefined/tied rank correlation and receive the prospectively specified neutral0. Tiny folds and correlated sampled observations limit surrogate-reliability estimation.

In the primary seven-ecosystem analysis, BORA-inspired calls14/70cases/model and loses3.1021%/3.2476% for SmolLM/Qwen. Rank-reliability has23.95expectedcalls and loses1.4361%/1.4877%; fixed draws call23and lose2.8390%/2.8562%. These policies also underperform their matched-rate random expectations. Calibrated GP-uncertainty and rank rules select no calls for either model. The saved benefit predictor likewise selects none. Thus these particular uncertainty/reliability adaptations do not recover the useful exceptions. This is not a finding that the complete original algorithms fail.

Fractional calls, opportunities, harms, tokens and times under rank_expected are exact expectations over a Bernoulli selection of the two real saved outcomes. They are not fractional measured requests, new inference or synthetic outcomes. The separately retained rank_draw is one reproducible outcome-independent randomization. Random comparison uses the same per-group mean rate; no hidden outcome selects a case. Actual model costs and one historical fallback/unknown usage stay in the source denominator.

All fitted scalar thresholds exclude the entire held system/ ecosystem. V151 benefit rules retain their prior nested calibration; no favorable policy is selected across this table. Prior repeated inspection makes all new results exploratory. Seven ecosystems and dependent seeds do not support a population equivalence/generalization claim. The practical1%margin is per case; above-random improvement alone does not establish improvement over never-call. Native Memcached17+3results are excluded from this20-search cohort.

Prefix signal computation took0.385472seconds under600secondcap; evaluation adds0.166933seconds. This is measured controller-analysis overhead; estimated deployment only pays for its chosen branch and controller. No dollar/energy claim. Independent scalar-kernel/least-squares replay passed, including three semantic-corruption checks. Exact decisions, CVpredictions, monitor histories, calibration grids, per-group outcomes and usage estimates are saved in artifacts/study_v154 and results/v154_controllers.
