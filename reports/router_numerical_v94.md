# V94 secondary frozen router transfer

Decisions were sealed after prefix collection but before the first continuation outcome. Ridge coefficients and both thresholds used only 30 older Qwen3 paired cases grouped into six development systems. No new-family outcome was used to choose a threshold. The addition was exploratory and its timing is disclosed.

| Policy | Calls / 10 | SuperLU gain | HiGHS gain | Useful cases missed | Harmful calls |
|---|---:|---:|---:|---:|---:|
| never | 0 | +0.00% | +0.00% | 0 | 0 |
| always | 10 | -10.21% | -9.69% | 0 | 3 |
| benefit | 0 | +0.00% | +0.00% | 0 | 0 |
| uncertainty | 0 | +0.00% | +0.00% | 0 | 0 |
| random_development_benefit | 0 | +0.00% | +0.00% | 0 | 0 |
| random_matched_benefit_diagnostic | 0 | +0.00% | +0.00% | 0 | 0 |
| random_development_uncertainty | 0 | +0.00% | +0.00% | 0 | 0 |
| random_matched_uncertainty_diagnostic | 0 | +0.00% | +0.00% | 0 | 0 |
| hindsight_oracle_diagnostic | 2 | +0.47% | +0.10% | 0 | 0 |

The benefit and uncertainty thresholds both selected never-call on development data. This saves every model request, but does not demonstrate benefit prediction or superiority over random routing. All matched-rate random decisions also call zero times. A positive hindsight value is available headroom, not an achieved policy.

Only two fresh test groups were evaluated. No confidence interval or population claim is made. Quality gains above use measured final incumbents; failures stay in the paired arms. The 0.05 development penalty was a quality-preference scenario, not a monetary price or calibrated reliability guarantee.

Saved evidence: `artifacts/study_v94/router_precommit.json`, `results/v94_analysis/policies.json`. Reproduce: `.venv/bin/python scripts/evaluate_router_numerical_v94.py`.
