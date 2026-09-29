# V117: how dependent is the conclusion on individual systems?

This is a saved-data sensitivity analysis. No model was called and no objective was acquired. All six groups and all 36 observed LLM continuations remain in the primary analysis. Each sampling replica is averaged within its prefix, prefixes within their family, then families equally. Leave-one-family-out calculations diagnose influence; they do not evaluate a learned router or create new independent test data.

| Comparator | Mean gain | Median group gain | Mean range after omitting one family | Hindsight branch-selection headroom |
|---|---:|---:|---:|---:|
| batch_3nn | -2.672% | -0.060% | -3.368% to 0.096% | 0.168% |
| full_sequential_3nn | -6.446% | -1.440% | -8.248% to -3.384% | 0.653% |
| single_portfolio | -2.252% | -0.060% | -3.112% to 0.557% | 0.568% |

Omitting OpenVPN changes the single-portfolio mean from -2.252% to 0.557%. Thus a general claim of average LLM harm is not robust to this family omission. Do not discard OpenVPN or replace the primary result with the favorable subset. The median group gain is -0.060%; only 2 of six family means are positive.

The original practical-margin result is narrower and stable: no saved LLM replica beats the single portfolio by 5%, so dropping a family cannot create such a win. Report small wins too (nine replicas; maximum3.34%). The original batch and sequential comparisons remain separate; their values are shown above rather than hidden behind the blend.

The hindsight column clips each saved gain at zero and then uses the same nested weighting. It selects between that replica and its classical counterfactual after observing both outcomes, so it is explicitly non-deployable. It is not a controller result, a best-of-three model policy, or a bound on future tasks. Both branches and all historical model calls remain charged in the research ledger.

No p-values or population uncertainty intervals are justified here. These diagnostics refine interpretation of the existing negative-result candidate; they cannot establish Q2 readiness or cross-system routing benefit. Untouched evaluation groups and independent native measurement remain untested.

Reproduce with `.venv/bin/python scripts/analyze_influence_v117.py`. Machine output: `results/v117_influence/summary.json`; plot: `influence.png`/`influence.svg`.
