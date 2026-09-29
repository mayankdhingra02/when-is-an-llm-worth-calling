# V165: how much opportunity remains after the cheap prefix?

This separately charged development diagnostic exhaustively measures both exposed 64-setting application domains. It selects a reference using three repetitions and evaluates every setting on three fresh repetitions. The reference is an empirical finite-domain comparator, not a proven global optimum. No optimizer, router or LLM received these full-space outcomes. Earlier primary results remain unchanged.

## Prefix opportunity on fresh validation

Positive headroom means the selected reference is faster than the frozen prefix incumbent. Robust flags require >10%, different settings, correct/quality-feasible validation, relative MAD<=5% and both medians>=10ms. All checkpoints share the original ten-evaluation trajectory; these are not new handoff experiments.

| Application | Acquired prefix labels | Mean observed headroom | Range | Robust >10% cases / 5 | Same reference setting / 5 | Unstable/invalid comparisons |
|---|---:|---:|---:|---:|---:|---:|
| ripgrep | 4 | +8.022% | +0.000% to +18.016% | 2 | 1 | 0 |
| ripgrep | 7 | +6.903% | +0.000% to +12.695% | 2 | 1 | 0 |
| ripgrep | 10 | +5.293% | +0.000% to +12.695% | 1 | 1 | 1 |
| hnswlib | 4 | -0.122% | -5.445% to +5.679% | 0 | 0 | 0 |
| hnswlib | 7 | -1.508% | -5.445% to +5.679% | 0 | 0 | 0 |
| hnswlib | 10 | -3.739% | -5.445% to -1.981% | 0 | 0 | 0 |

## Reference selection and noise

| Application | Selected ID | Selection / validation median seconds | Validation rank / 64 | Validation MAD | Other settings robustly >10% faster |
|---|---:|---:|---:|---:|---:|
| ripgrep | 38 | 0.262863 / 0.269718 | 2 | 2.333% | 0 |
| hnswlib | 49 | 0.090253 / 0.100015 | 9 | 3.522% | 0 |

The validation rank/minimum uses all fresh labels only as an explicitly post-hoc diagnostic; it never replaces the reference selected before validation. Selecting the minimum of64 noisy medians may overfit selection noise. Three independent validation repetitions reduce reuse bias but cannot certify global optimality, a risk bound or equivalence. Negative observed headroom is retained. Same-setting comparisons share one validated value and are exactly zero; this does not retroactively remove the separately timed noise in V163/V164.

All90 V164 frozen arm incumbents are also mapped onto this common validation table in comparison.json, as a diagnostic only. No original primary estimate is overwritten and the768 extra evaluations are not hidden inside a B20 policy budget.

## Actual execution and reproducibility

New collection: 768 configuration outcomes / 2304 native workload invocations, zero model calls. Selection384 outcomes and validation384 outcomes cover all128 settings three times each. Every attempt is charged. Quality penalties:0. Native subprocess305.946s, objective244.382s, stage309.223s/1800s. Historical100prefix outcomes/300invocations and prior inference remain separate existing research costs. No downloads, paid/cloud inference, uncharged warmups, or system changes.

ripgrep: noisy selection/validation cells 2/1; quality-failing selection/validation cells 0/0. None were silently removed from the raw dataset.

hnswlib: noisy selection/validation cells 2/0; quality-failing selection/validation cells 0/0. None were silently removed from the raw dataset.

## Interpretation limits

These tasks, domains and saved trajectories were already exposed and are now exhaustively measured for development analysis. They cannot become a new held-out cohort. Five seeds and three checkpoints are not15independent software systems. All timing is from one host and caches may be warm. The public ANN vectors and text corpus are small fixed inputs. Earlier-checkpoint opportunity does not demonstrate that an LLM would exploit it. No learned router, new method superiority, production benefit or journal readiness follows.

Evidence: artifacts/study_v165/freeze.json binds the prospective protocol, configuration plans and frozen historical selections; results/v165_headroom/reference.freeze.json binds selection before validation. All768 acquisitions, reference IDs, per-cell timing/quality/noise, target mappings and figures are preserved. Analysis: scripts/report_headroom_v165.py; raw correctness/provenance replay: scripts/verify_headroom_v165.py.
