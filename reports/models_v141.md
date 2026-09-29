# V141–V142: matched local-model replication with preserved startup repair

Both models actually ran on the same 30 original B10 prefixes: six previously exposed software families, five seeds each. Byte-identical messages, canonical ten-proposal grammar, output budget1024, thinking off, same sampling seed per case. Each continuation acquired ten recorded outcomes, retaining the prefix incumbent. Native software was not executed. Model templates/tokenizers differ; this is a comparison of complete model treatments, not a causal parameter-count experiment.

Positive percentages favor the named model over the control. Seeds within a family are dependent; no population significance or held-out claim.

| Family | Model | Gain vs sequential | W/T/L | Gain vs adaptive neighbor | W/T/L |
|---|---|---:|---|---:|---|
| berkeleydb | qwen3_8b | +0.0648% | 1/3/1 | -0.7435% | 2/1/2 |
| berkeleydb | smollm3_3b | -0.3308% | 0/3/2 | -1.1418% | 1/1/3 |
| dune_hsmgp | qwen3_8b | -21.2355% | 0/1/4 | -10.2669% | 0/1/4 |
| dune_hsmgp | smollm3_3b | -20.8911% | 1/0/4 | -9.9624% | 1/0/4 |
| hipacc | qwen3_8b | -2.9068% | 0/2/3 | -2.2191% | 0/1/4 |
| hipacc | smollm3_3b | -2.5977% | 0/2/3 | -1.8958% | 0/1/4 |
| llvm | qwen3_8b | -2.1592% | 0/2/3 | -2.2956% | 0/1/4 |
| llvm | smollm3_3b | -1.9716% | 0/2/3 | -2.1082% | 0/1/4 |
| openvpn | qwen3_8b | -6.8761% | 0/3/2 | -5.2209% | 0/3/2 |
| openvpn | smollm3_3b | -7.0766% | 0/4/1 | -5.4570% | 0/4/1 |
| sac | qwen3_8b | -0.4036% | 0/3/2 | +0.0000% | 0/5/0 |
| sac | smollm3_3b | -0.4036% | 0/3/2 | +0.0000% | 0/5/0 |

Equal-seed family means receive equal weight here (five seeds each); do not confuse 30 cases with 30 systems. All secondary controls and individual cases are in comparison.json.

| Model | Control | Mean gain | W/T/L | >1% benefit / harm |
|---|---|---:|---|---|
| qwen3_8b | sequential_3nn | -5.5861% | 1/14/15 | 1/11 |
| qwen3_8b | adaptive_incumbent_neighbor | -3.4577% | 2/12/16 | 1/9 |
| qwen3_8b | fixed_prefix_neighbor | -3.3619% | 2/12/16 | 1/9 |
| qwen3_8b | random_full | -1.6068% | 4/19/7 | 2/4 |
| qwen3_8b | prefix | +1.1453% | 7/23/0 | 6/0 |
| smollm3_3b | sequential_3nn | -5.5452% | 1/14/15 | 0/10 |
| smollm3_3b | adaptive_incumbent_neighbor | -3.4275% | 2/12/16 | 1/9 |
| smollm3_3b | fixed_prefix_neighbor | -3.3328% | 2/12/16 | 1/9 |
| smollm3_3b | random_full | -1.5806% | 5/18/7 | 2/4 |
| smollm3_3b | prefix | +1.1411% | 11/19/0 | 7/0 |

| Family | SmolLM gain vs Qwen | W/T/L |
|---|---:|---|
| berkeleydb | -0.4027% | 0/3/2 |
| dune_hsmgp | +0.2786% | 4/1/0 |
| hipacc | +0.2939% | 2/2/1 |
| llvm | +0.1754% | 1/4/0 |
| openvpn | -0.3462% | 1/3/1 |
| sac | +0.0000% | 0/5/0 |

## Reliability and actual cost

SmolLM initially failed its local pre-start socket check after Qwen exited; no SmolLM process, HTTP request or generation occurred in that attempt. Before any new objective acquisition, V142 froze one startup repair on a distinct loopback port, retaining the original60-request/600-acquisition/1800-second limits. Original failed startup cost0.763504625s is additional to the per-model lifecycle figures below; startup repairs1, model-request retries0. Original failure receipts remain unchanged.

qwen3_8b: 30/30 requests, 30 valid, 0 fallback; 0 retries. Generated/prefill observed tokens 8025/27974, missing intended usage 0/0. Lifecycle 438.494s; request-only sum 433.786s; peak sampled RSS 7,537,180,672bytes. Projected away from proposed setting 225/300; repeated proposals 52; proposals matching prefix 1. Joint >1% benefit over both sequential and adaptive neighbor: 0/30.

smollm3_3b: 30/30 requests, 30 valid, 0 fallback; 0 retries. Generated/prefill observed tokens 3209/21458, missing intended usage 0/0. Lifecycle 98.107s; request-only sum 96.024s; peak sampled RSS 3,388,637,184bytes. Projected away from proposed setting 263/300; repeated proposals 49; proposals matching prefix 134. Joint >1% benefit over both sequential and adaptive neighbor: 0/30.

Actual new collection: 600 recorded acquisitions, 6.769s evaluation stage, 720.261s combined collection. Historical prefixes and four comparator arms per case are reused with verified identities and original costs retained. Estimated deployment chooses one model, one request and B20 total; collecting both arms costs twice the new-label budget. Zero paid/cloud use or new downloads. Model-block order and cache/thermal effects limit latency comparisons; missing usage is not zero.

## Scope and interpretation

This fixed replication assesses whether cheap-control comparisons depend on the model. It does not fit or validate a benefit-aware controller, create new independent test families, establish model reasoning, or reproduce SNAP2 exactly. Frozen practical margin is1%; all cases including failures remain in the denominator. Recorded-source correctness/noise/utility qualifications persist. Older SAC failures and earlier conflicting results are not replaced. Two differently trained models and quantized templates are not a model-size scaling study. Repeatedly exposed families and protocol development rule out confirmatory generalization claims.

Next priority remains a coherent prospective independent-family evaluation. Do not choose its families, prompts or thresholds because of favorable outcomes here. Cross-host/native and further model replication address distinct gaps; no journal acceptance guarantee.

Artifacts: reports/protocol_v141.md and protocol_v142.md with their freezes; artifacts/study_v141 (jobs, models, inputs, source extracts, tests); results/v141_models and results/v142_smollm (actual payloads/preflight/raw responses/ledgers); results/v141_analysis (sealed selections,600 acquisition receipts,60 arms,comparison.json and figures).
