# V138: cheap incumbent-neighbor controls

Actual execution: 30 saved B10 cases, six exposed software families, five fixed seeds (11, 23, 37, 53, 71), two B20 continuations per case. The fixed control searches around the best prefix setting; the adaptive control follows its current best observed setting. Both use Hamming distance, deterministic prefix-order tie breaking, and ten charged new evaluations. No LLM is used by either new control.

Positive percentages favor the named cheap control. W/T/L counts describe five repeated seeds within one system, not five independent systems.

| Family | Control | Mean gain vs sequential3NN | W/T/L | Mean gain vs valid one-shot Qwen3-8B | W/T/L |
|---|---|---:|---:|---:|---:|
| berkeleydb | fixed_prefix_neighbor | 0.5552% | 3/1/1 | 1.5882% | 4/1/0 |
| berkeleydb | adaptive_incumbent_neighbor | 0.7075% | 3/1/1 | 1.7406% | 4/1/0 |
| dune_hsmgp | fixed_prefix_neighbor | -11.1482% | 2/2/1 | 6.8072% | 3/2/0 |
| dune_hsmgp | adaptive_incumbent_neighbor | -11.1482% | 2/2/1 | 6.8072% | 3/2/0 |
| hipacc | fixed_prefix_neighbor | -0.8622% | 2/2/1 | 0.0775% | 2/1/2 |
| hipacc | adaptive_incumbent_neighbor | -0.7149% | 2/2/1 | 0.2275% | 3/1/1 |
| llvm | fixed_prefix_neighbor | 0.0506% | 1/2/2 | 2.4493% | 4/1/0 |
| llvm | adaptive_incumbent_neighbor | 0.1371% | 2/2/1 | 2.5353% | 4/1/0 |
| openvpn | fixed_prefix_neighbor | -2.4109% | 0/4/1 | 1.6966% | 1/4/0 |
| openvpn | adaptive_incumbent_neighbor | -2.2274% | 0/4/1 | 1.9229% | 1/4/0 |
| sac | fixed_prefix_neighbor | -0.4036% | 0/3/2 | 0.0000% | 0/5/0 |
| sac | adaptive_incumbent_neighbor | -0.4036% | 0/3/2 | 0.0000% | 0/5/0 |

Historical one-shot comparators use V127 normal responses for five families and V135 capacity-repaired SAC responses. These were real local Qwen3-8B calls, not regenerated or fabricated for this extension. Original failed SAC attempts remain in the historical denominator and collection costs; this table explicitly compares the repaired valid treatment. Historical sequential controls are V41. Same B10 identities and acquired values are checked. Old source manifests may retain their original split names; all six families are exposed development here.

Optional previously declared feedback comparison covers only LLVM and SAC (ten cases):

| Family | Control | Gain vs V136 feedback | W/T/L |
|---|---|---:|---:|
| llvm | fixed_prefix_neighbor | 0.9853% | 3/2/0 |
| llvm | adaptive_incumbent_neighbor | 1.0713% | 3/2/0 |
| sac | fixed_prefix_neighbor | 0.0000% | 0/5/0 |
| sac | adaptive_incumbent_neighbor | 0.0000% | 0/5/0 |

V136 masked and feedback final incumbents coincide in all ten cases, so their contrasts coincide. This does not imply the search paths coincide.

All individual outcomes (raw units; compare within a family only):

| Family / seed | B10 | Fixed | Adaptive | Historical sequential | Historical model |
|---|---:|---:|---:|---:|---:|
| berkeleydb / 11 | 0.36643059 | 0.363065077 | 0.363065077 | 0.36643059 | 0.36643059 |
| berkeleydb / 23 | 0.448242513 | 0.448077718 | 0.448077718 | 0.432443897 | 0.448242513 |
| berkeleydb / 37 | 0.382528667 | 0.362512641 | 0.359598282 | 0.382528667 | 0.382528667 |
| berkeleydb / 53 | 0.353774026 | 0.353774026 | 0.353774026 | 0.353774026 | 0.353774026 |
| berkeleydb / 71 | 0.368982231 | 0.362512641 | 0.362512641 | 0.363384821 | 0.368982231 |
| dune_hsmgp / 11 | 7263.26036 | 7208.78571 | 7208.78571 | 4545.78321 | 7263.26036 |
| dune_hsmgp / 23 | 6585.6 | 6567.89643 | 6567.89643 | 6575.88571 | 6585.6 |
| dune_hsmgp / 37 | 6601.92571 | 4422.17214 | 4422.17214 | 4545.78321 | 6601.92571 |
| dune_hsmgp / 53 | 6595.38821 | 6595.38821 | 6595.38821 | 6595.38821 | 6595.38821 |
| dune_hsmgp / 71 | 6672.10464 | 6567.89643 | 6567.89643 | 6567.89643 | 6567.89643 |
| hipacc / 11 | 23.081 | 21.484 | 21.324 | 21.729 | 21.332 |
| hipacc / 23 | 21.187 | 21.173 | 21.173 | 21.187 | 21.187 |
| hipacc / 37 | 23.9 | 22.77 | 22.77 | 21.582 | 22.461 |
| hipacc / 53 | 22.077 | 21.545 | 21.545 | 21.545 | 22.077 |
| hipacc / 71 | 21.571 | 21.571 | 21.571 | 21.571 | 21.571 |
| llvm / 11 | 201.546667 | 200.82 | 199.953333 | 200.38 | 201.546667 |
| llvm / 23 | 206.9 | 200.38 | 200.38 | 200.38 | 206.226667 |
| llvm / 37 | 199.953333 | 199.953333 | 199.953333 | 199.953333 | 199.953333 |
| llvm / 53 | 219.153333 | 200.66 | 200.66 | 200.38 | 219.153333 |
| llvm / 71 | 201.896667 | 200.66 | 200.66 | 201.896667 | 201.896667 |
| openvpn / 11 | 519.399657 | 761.205428 | 769.147446 | 865.541902 | 701.683083 |
| openvpn / 23 | 867.37698 | 867.37698 | 867.37698 | 867.37698 | 867.37698 |
| openvpn / 37 | 867.56787 | 867.56787 | 867.56787 | 867.56787 | 867.56787 |
| openvpn / 53 | 867.37698 | 867.37698 | 867.37698 | 867.37698 | 867.37698 |
| openvpn / 71 | 770.671336 | 864.75166 | 864.75166 | 864.75166 | 864.75166 |
| sac / 11 | 1.5 | 1.5 | 1.5 | 1.5 | 1.5 |
| sac / 23 | 1.5 | 1.5 | 1.5 | 1.5 | 1.5 |
| sac / 37 | 1.5 | 1.5 | 1.5 | 1.5 | 1.5 |
| sac / 53 | 1.51 | 1.51 | 1.51 | 1.5 | 1.51 |
| sac / 71 | 1.5 | 1.5 | 1.5 | 1.48 | 1.5 |

Actual new collection: 600 recorded outcomes, 60 completed arms, zero new model requests or native executions, 2.895211s collector runtime. Includes repeated historical rows as new charges in each arm. Table-access runtime is not native software cost. Modeled deployment selects one arm: B10 plus ten evaluations, B20 total, no model tokens/requests. Historical inference/prefix costs are not erased or attributed to this new collector.

These controls were frozen before their outcomes were acquired, but designed after earlier LLM/projection findings. This is a development extension, not a confirmatory holdout or novel optimizer. Neither the six systems nor the repeated seeds provide a fresh learned-router test. Hamming geometry, fixed recorded targets, unknown per-row noise/correctness, and historical one-shot prompt differences limit causal attribution. A control matching an LLM does not prove it generated the model behavior. No threshold, router, significance-driven retry or outcome-selected subgroup is fitted here.

Protocol and freeze: reports/protocol_v138.md and protocol_v138.freeze.json. Raw evidence: results/v138_incumbent/selections, acquisitions.jsonl, arms and summary.json. Reproduce with `.venv/bin/python scripts/analyze_incumbent_v138.py`; independently verify with `.venv/bin/python scripts/verify_incumbent_v138.py`. Neither command acquires new outcomes.
