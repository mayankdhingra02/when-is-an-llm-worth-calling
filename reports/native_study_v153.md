# V153: actual native paired Memcached optimization

**Five paired seeds, one feasibility-explored native family, two real pinned local models.** This is a prospective frozen collection, not a wholly unseen-family study or evidence of broad transfer. Every logical arm spends20objective evaluations:10sharedprefix,7newsearchconfigurations,3freshchargedrepetitions of the selected incumbent. Primary performance is median of those3fresh times. This differs from earlier20distinct-search-label studies. No validation measurement is used to select a configuration or change a controller.

Memcached1.6.45, staticlibevent2.1.13 and the V152correctness-checked native client run locally.64feature-onlysettings: threads1..8 ×requests/event[1,2,4,8,12,20,32,50]. Each fresh server completes2,048,000GET/SEToperations with byte-exact response and independent counter checks. Native timing includes the concurrent local clients; this is not isolated server throughput, native cloud deployment or a cloud-dollar optimization. Source/build/feasibility details are in native_feasibility_v152.md.

Actual collection: **400charged native acquisitions, 10real model starts**, 35B20arms, 636.533seconds/1800secondcap.295searchacquisitions plus105freshvalidationmeasurements; 62unique settings. All400nativeacquisitions passed correctness. Earlier40feasibilityprobes and all historical router-training costs remain separate overhead. No free repeated labels. All server children reaped; localmodel ledgers preserve request/token/runtime caps and any failures.

| Model / classical control | Mean validation gain | Wins/ties/losses | >1%wins / harms |
|---|---:|---|---|
| smollm3_3b / sequential_3nn | +0.0881% | 3/0/2 | 1/1 |
| smollm3_3b / adaptive_neighbor | -1.3495% | 0/0/5 | 0/2 |
| smollm3_3b / fixed_neighbor | +0.3276% | 4/0/1 | 2/1 |
| smollm3_3b / random_full | -0.7246% | 2/0/3 | 0/3 |
| smollm3_3b / random_proposal | +0.1810% | 2/0/3 | 1/0 |
| qwen3_8b / sequential_3nn | -0.4188% | 1/0/4 | 1/3 |
| qwen3_8b / adaptive_neighbor | -1.8655% | 1/0/4 | 0/4 |
| qwen3_8b / fixed_neighbor | -0.1722% | 3/0/2 | 1/1 |
| qwen3_8b / random_full | -1.2368% | 0/0/5 | 0/2 |
| qwen3_8b / random_proposal | -0.3269% | 1/0/4 | 0/1 |

| Model / seed | Selected setting | Validation times(s) | Gain vs sequential | Gain vs adaptive | Secondary search-best gain vs sequential |
|---|---|---|---:|---:|---:|
| smollm3_3b / 11 | [6, 50] | 0.785803, 0.790759, 0.793305 | +0.3668% | -1.3104% | +0.0000% |
| smollm3_3b / 23 | [2, 32] | 0.771201, 0.769222, 0.777472 | +2.6784% | -0.4877% | -0.8212% |
| smollm3_3b / 37 | [2, 50] | 0.762445, 0.769560, 0.760612 | +0.0516% | -0.1060% | +0.0000% |
| smollm3_3b / 53 | [2, 50] | 0.768303, 0.779159, 0.769938 | -0.9522% | -0.2565% | +0.0000% |
| smollm3_3b / 71 | [3, 50] | 0.805680, 0.799241, 0.782741 | -1.7043% | -4.5868% | -0.9204% |
| qwen3_8b / 11 | [6, 50] | 0.808198, 0.799862, 0.801607 | -1.0000% | -2.7002% | +0.0000% |
| qwen3_8b / 23 | [2, 50] | 0.758373, 0.776325, 0.785197 | +2.0317% | -1.1554% | -2.0837% |
| qwen3_8b / 37 | [2, 50] | 0.771814, 0.766523, 0.775834 | -1.1765% | -1.3361% | +0.0000% |
| qwen3_8b / 53 | [2, 50] | 0.764200, 0.765707, 0.778746 | -0.3974% | +0.2944% | +0.0000% |
| qwen3_8b / 71 | [4, 32] | 0.801886, 0.792938, 0.798044 | -1.5520% | -4.4302% | -1.0658% |

| Model / frozen policy | Calls /5 | Mean gain vs sequential | Above matched random | Useful / harmful | Missed useful |
|---|---:|---:|---:|---|---:|
| smollm3_3b / never | 0 | +0.0000% | +0.0000% | 0/0 | 1 |
| smollm3_3b / always | 5 | +0.0881% | +0.0000% | 1/1 | 0 |
| smollm3_3b / benefit | 0 | +0.0000% | +0.0000% | 0/0 | 1 |
| smollm3_3b / benefit_q80 | 0 | +0.0000% | +0.0000% | 0/0 | 1 |
| smollm3_3b / uncertainty | 0 | +0.0000% | +0.0000% | 0/0 | 1 |
| smollm3_3b / uncertainty_q80 | 1 | -0.1904% | -0.2080% | 0/0 | 1 |
| smollm3_3b / random_development_rate | 1 | -0.3409% | -0.3585% | 0/1 | 1 |
| smollm3_3b / random_matched_rate | 0 | +0.0000% | +0.0000% | 0/0 | 1 |
| qwen3_8b / never | 0 | +0.0000% | +0.0000% | 0/0 | 1 |
| qwen3_8b / always | 5 | -0.4188% | -0.0000% | 1/3 | 0 |
| qwen3_8b / benefit | 0 | +0.0000% | +0.0000% | 0/0 | 1 |
| qwen3_8b / benefit_q80 | 0 | +0.0000% | +0.0000% | 0/0 | 1 |
| qwen3_8b / uncertainty | 0 | +0.0000% | +0.0000% | 0/0 | 1 |
| qwen3_8b / uncertainty_q80 | 1 | -0.0795% | +0.0043% | 0/0 | 1 |
| qwen3_8b / random_development_rate | 0 | +0.0000% | +0.0000% | 0/0 | 1 |
| qwen3_8b / random_matched_rate | 0 | +0.0000% | +0.0000% | 0/0 | 1 |

Selected-configuration identity: 6/10model/classical pairs selected exactly the same configuration. Those observed timing differences cannot establish a configuration-selection advantage; all raw contrasts remain in the table.

Policies were fit/calibrated only on V151existing development data grouped by ecosystem and frozen before any Memcachedprefix. Prefix-only decisions were sealed before continuation. Their training target used earlier recorded/search outcomes; the new native validation-median target is an explicit shift. Random expected gain is a retrospective matched-rate diagnostic. Hindsight oracle is nondeployable. Allfivecases form onesystemgroup; repeated seeds are not independent systems. No significance/equivalence/generalization claim follows.

smollm3_3b: joint >1%wins against sequential/adaptive 0/5; hindsightoraclemean0.6194%. 5starts/5complete responses, 141observedgenerated/1785prefilltokens, 0unknownusage; lifecycle7.906s,peakRSS2951839744bytes,serverexit0.
qwen3_8b: joint >1%wins against sequential/adaptive 0/5; hindsightoraclemean0.4063%. 5starts/5complete responses, 165observedgenerated/1892prefilltokens, 0unknownusage; lifecycle17.981s,peakRSS6063505408bytes,serverexit0.

Validation variability: 7/35arms exceed1%MAD/median across3repetitions; maximum4.665%. The earlier five-repetition feasibility pass is not a guarantee for every new setting/run. Tiny differences, particularly when arms selected the same configuration, may reflect timing noise rather than optimization advantage. No repeated validation was added after seeing these values.

Estimated deployment spends20evaluations and at mostonechosenmodelrequest/case, including its validation allocation; actual research spends400nativeevaluations plusbothmodels and earlierdevelopment. Selected-token/time estimates reuse observed historical response costs and are descriptive, with coldstart cost recorded separately. Search phases ran classical before model; validation was randomized in threecompleteblocks after all35choices were frozen. This reduces validation-order bias but cannot eliminate search-order, thermal, client/server contention or background-load effects.

Protocol clarification: frozen prompt code uses raw numeric settings and indexed level lists, whereas one protocol sentence said normalized observations. Search/projection uses normalized distances. The discrepancy was recorded before model starts; no prompt/code/decision changed mid-run. Fixed-value GET/SET checks are not full protocol conformance testing.

Native shutdown diagnostics: {'-9': 1, '0': 399}. One server was killed by the configured cleanup fallback after a correct measurement and was reaped. This is retained as an operational event, not silently counted as an exit0.

Evidence: raw native acquisition records/serverlogs, model payloads/rawresponses, candidate/prefix manifests, router coefficients/trees and decisionseals, selectionseal, complete validationplan and logs, budgets, model/backend hashes and reproduction scripts. This is one bounded native result, not Q2-readiness certification.
