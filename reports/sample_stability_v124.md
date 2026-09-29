# V124 post-hoc sample and format diagnostics

This analysis uses only real responses and acquired prefix labels. It adds no objective evaluations and changes no declared choices or primary result. Removing one sampling seed is a descriptive stability check, not a confidence interval or a new optimization arm. Missing two-sample candidate sets remain unavailable.

| Family | Candidates with3valid samples /20 | Identical valid samples | Accepted family |
|---|---:|---:|---|
| berkeleydb | 20 | 17 | True |
| dune_hsmgp | 20 | 0 | True |
| hipacc | 0 | 3 | False |

EI selection overlap with the original10choices after omitting one sampling seed:
- berkeleydb: seed101: 9/10; seed102: 10/10; seed103: 10/10
- dune_hsmgp: seed101: 10/10; seed102: 10/10; seed103: 10/10
- hipacc: family fallback; no LLM ranking evaluated

Invalid returned scalar responses: 37. Exact texts, finish reasons and token counts are in results/v124_analysis/sample_stability.json. Placeholder echoes are retained failures, not repaired predictions. All original responses remain in the source journal. Three stochastic samples per candidate cannot establish calibrated uncertainty. Sampling-derived features also require model calls, so they are not cheap pre-escalation controller inputs.
