# V126: exhaustive admitted-domain feasibility audit

This coverage audit follows rediscovery of the prior V42fixed-shortlist bound. It asks whether moving outside that shortlist could make a5%gain possible. All six existing development families and five prefixes each are retained; none is a new holdout. The direction-aware optimum is over the admitted, feature-restricted/subsampled domain, not every possible configuration of the real software. All values come from original recorded benchmark tables, not fresh native execution.

| Family | Domain rows | Mean maximum gain vs sequential3NN | Joint5%possible /5 | Sequential already global-best /5 |
|---|---:|---:|---:|---:|
| berkeleydb | 1024 | 6.362% | 1 | 1 |
| dune_hsmgp | 384 | 20.762% | 3 | 0 |
| hipacc | 1024 | 1.618% | 0 | 0 |
| llvm | 1024 | 0.455% | 0 | 0 |
| openvpn | 512 | 0.121% | 0 | 1 |
| sac | 1024 | 1.067% | 0 | 1 |

Across30exposed prefixes, 4could in principle gain≥5%against both batch and full sequential3NN if the unrestricted admitted-domain optimum were found; 5could beat sequential alone by≥5%. Equal-family mean ceiling versus sequential: 5.064%. This is hindsight opportunity, not an achieved LLM gain or a learned controller result.

Actual audit collection: 4932new recorded outcome accesses in 497coverage branches, 3.234s, zero model calls. Each branch reuses an existing seed11prefix10 and acquires at most10new outcomes, so no branch exceedsB20. Short final chunks use fewer evaluations and are coverage diagnostics, not competitive policies. Original60prefix outcomes retain their historical cost; the4932remaining outcomes complete the4992-row admitted domains and are covered by the charged journal. Historical control states for all30prefixes are matched to this domain and their labels replayed.

The coverage plan was frozen using only existing feature order and prefix IDs before these new accesses. The merged outcome map is evaluator-only. Never provide it, its extrema/ranks, or the hindsight opportunity label to optimizer/LLM/controller inputs. Development feasibility can motivate a new intervention; filtering fresh test cases by their revealed optimum would leak outcomes. Known portfolio references are included when available (not fabricated for missing seeds); primary feasibility covers all30against fixed batch/sequential controls.

This audit does not establish that an LLM can identify the good configurations, that stochastic proposals beat a cheap optimizer, or that the original benchmark rows have verified equal functional utility. Prior V43/V44uniform/diverse-pool results remain relevant. It does not justify selecting favorable families/seeds for a confirmatory evaluation. No threshold was changed to call an old failure positive; the fixed-pool5%screen remains unattainable.
