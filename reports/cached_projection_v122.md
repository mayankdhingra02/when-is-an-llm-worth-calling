# V122: development-only projection of real cached configuration strings

All five original V119 responses were retained. They failed the original ID contract and remain failures in V119. Here a newly frozen parser interprets their literal configuration strings, validates each feature index, and projects by feature-only nominal distance onto the remaining saved20-candidate shortlist. Tie breaking follows the saved state order. This is an exploratory changed-parser adaptation on exposed WordCount prefixes, not another model sample or an independent test.

| Control | Mean relative gain | Wins/ties/losses |
|---|---:|---:|
| batch_3nn | 1.092% | 1/3/1 |
| full_sequential_3nn | -0.631% | 2/1/2 |
| random_full | 5.243% | 3/1/1 |
| single_portfolio | 0.780% | 1/2/2 |
| presentation_first10 | -9.465% | 1/2/2 |

Joint≥5% wins against batch, sequential and first-ten: 0/5. Development screening criterion: not met. Malformed/fallback cases: 0/5. Among50 real proposals, 20 required a nonzero-distance projection and13 chose an alternative because the closest row was already selected. All mapping traces are saved before objective acquisition.

| Seed | Target | Batch gain | Sequential gain | First-ten gain |
|---|---:|---:|---:|---:|
| 11 | 68.567 | 0.000% | -7.091% | -33.248% |
| 23 | 47.387 | 0.000% | 0.000% | 0.000% |
| 37 | 49.017 | 6.415% | 24.855% | 0.000% |
| 53 | 64.027 | -0.956% | -24.765% | -21.300% |
| 71 | 47.622 | 0.000% | 3.846% | 7.226% |

Actual new cost:50 recorded acquisitions, zero model requests/downloads/spending; each logical branch is the original prefix10 plus continuation10. The five historical V119 real requests and300 generated tokens remain research cost. A hypothetical deployed adapter needs a real request per escalation; a cached replay is not free inference. No fabricated responses, repaired raw text, hidden-label projection or target-based candidate selection.

The projection rule and selections were frozen before these new branch acquisitions. All five seeds/controls remain; no projection or threshold retuning followed the result. The same table was already exposed and the model/input format differs from the constrained adapter. Neither positive nor negative findings establish unseen-system routing, production reliability, a direct SNAP2 replication or journal readiness. Earlier V92/V93 results already show that unforced decoding alone is not a general cure. This diagnostic tests one different interpretation of preserved model outputs, not a universal solution.

Evidence: reports/protocol_v122.md and .freeze.json; results/v122_projection/choices and selection_seal.json; results/v122_analysis/acquisitions.jsonl and arms; scripts/verify_cached_v122.py. Each cache key includes parser version, original request/response and prefix hash. Source/model/prompt provenance remains V119.
