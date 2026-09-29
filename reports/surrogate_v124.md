# V124: source-grounded local stochastic surrogate adaptation

**Interpretation correction:** Existing V42 hindsight bounds show that no case in this fixed shortlist cohort can meet the joint 5% quality criterion. These runs measure implementation/reliability and actual outcomes, but cannot fairly test that improvement hypothesis. See [attainability audit](attainability_v125.md); old raw results and the frozen criterion are unchanged.

Three exposed development systems, one saved seed11 prefix each. Qwen3-8B Q4_K_M predicts raw performance three times per candidate, temperature0.7/top_p0.95, no numeric clipping or grammar. Population mean/standard deviation feed expected improvement (EI); ranking by mean is a predeclared ablation using the same real responses. Each selects10of20saved candidates from prefix10. This is a compact software-context, local-model, batch adaptation, not a full LLAMBO replication.

| Mode | Control | Mean gain | Wins/ties/losses |
|---|---|---:|---|
| ei | batch_3nn | -0.038% | 0/2/1 |
| ei | full_sequential_3nn | -16.264% | 0/1/2 |
| ei | random_full | -0.771% | 0/1/2 |
| ei | presentation_first10 | -0.336% | 1/1/1 |
| ei | single_portfolio | -0.174% | 0/1/2 |
| mean | batch_3nn | -0.038% | 0/2/1 |
| mean | full_sequential_3nn | -16.264% | 0/1/2 |
| mean | random_full | -0.771% | 0/1/2 |
| mean | presentation_first10 | -0.336% | 1/1/1 |
| mean | single_portfolio | -0.174% | 0/1/2 |

Primary EI screening criterion: NOT MET; joint≥5%wins 0/3. Mean ablation screen: False. This is descriptive development screening, not significance or held-out generalization.

| Family | Mode | Valid predictions /60 | Selected IDs (not prompt input) | Target |
|---|---|---:|---|---:|
| berkeleydb | ei | 60 | B87012349A | 0.36643059 |
| berkeleydb | mean | 60 | 012349ACDF | 0.36643059 |
| dune_hsmgp | ei | 60 | 54HE0A2JFI | 6620.0129 |
| dune_hsmgp | mean | 60 | 2540EHJIFA | 6620.0129 |
| hipacc | ei | 23 | 396AE70JIB | 22.416 |
| hipacc | mean | 23 | 396AE70JIB | 22.416 |

Actual collection: 180charged local requests, 180returned, 143valid scalar predictions, 37invalid returned responses, 0unreturned. Negative predictions: 0; these are preserved, not clipped. At least2of3valid samples per candidate are required; otherwise both arms use recorded batch3NN fallback. Valid samples are aggregated without imputing malformed samples; every failed sample stays in the denominator. No retries or outcome-based response selection.

Generated tokens observed: 2240; missing receipts: 0; allocated: 5760. Lifecycle 944.372s, peak sampled serverRSS 6,303,105,024bytes. New recorded acquisitions: 60. Both branches were charged separately even if their selected sets coincide. Deployment would need60requests and10newobjective evaluations per escalation; mean/EI reuse here is research analysis, not free model deployment. Startup and metadata are extra. No native-time/dollar benefit claim.

The Qwen3-8B model and runtime are unchanged from V123. Prompt fields, raw target scale, stochastic decoding and batch acquisition differ; this is not a one-factor causal ablation. Three stochastic samples are a noisy uncertainty estimate. Prediction-derived dispersion is unavailable before calling the model, so it cannot be a cheap router feature. The same development families have extensive previous exposure; no new holdout, controller training or novelty claim. Original source correctness/noise/licensing limitations remain. The mean ablation cannot replace EI as the primary result after inspecting outcomes.

Owner code/license hashes: artifacts/sources/v124/manifest.json. Protocol and mapping: reports/protocol_v124.md and freeze. Real templates/requests/responses: results/v124_surrogate. Choices and source journals: results/v124_analysis. Prior positive and negative outcomes remain immutable.
