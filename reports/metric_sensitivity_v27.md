# V27: the LLM-versus-static comparison changes sign with the metric

**The small average LLM advantage over static shortlist selection is not stable across two quality metrics.** On the existing normalized-loss scale, the LLM improves by +0.00001851. On mean relative reduction in the recorded objective, it loses by **0.3394%**. The same configurations and outcomes produce both numbers; no new model response or objective measurement was collected.

This is a new, executed exploratory sensitivity analysis, not a change to the primary outcome or independent confirmation. It uses every one of the 15 development prefixes, three software families and five fixed seeds, with three unique real V22 presentations per prefix. Each of the three fixed classical baselines is compared to all 45 LLM outcomes: **135 paired comparisons** in total. Exact repeated prompts remain part of historical model cost but are excluded from the three-presentation efficacy mean.

## Two views of the same outcomes

For each arm, take its smallest recorded target among its twenty acquired configurations. Relative gain favoring the LLM is `(best_classical - best_LLM) / best_classical`. Compute the ratio for each paired presentation first; average presentations within seed, seeds within family, and then families equally. Do not divide pooled raw means or combine raw target units across systems. All inspected targets are positive and minimized.

| Classical comparator | LLM gain in normalized loss | LLM relative target reduction |
|---|---:|---:|
| Original full-space classical | +0.00426143 | +2.2407% |
| Static shortlist rank | +0.00001851 | **−0.3394%** |
| Adaptive shortlist | +0.00182351 | +0.8705% |

A negative relative reduction means the LLM's chosen configuration has a higher recorded target than the comparator. It is not a measured deployment slowdown: inference overhead, loading, and real execution variability are outside this quality ratio. Neither metric has been established as an application-specific utility.

| Family | LLM versus original classical | LLM versus static shortlist | LLM versus adaptive shortlist |
|---|---:|---:|---:|
| Brotli | +4.3523% | −1.3117% | +3.0194% |
| lrzip | +0.3697% | +0.3697% | −1.3158% |
| MySQL | +2.0001% | −0.0763% | +0.9078% |

Every individual paired comparison retains the same win/tie/loss direction under both metrics. Aggregation changes the weighting: normalized loss divides a target difference by a dataset's full target range, while the relative ratio divides it by the paired classical incumbent. This can reverse an average even with equal family weighting. The LLM's average advantage against original classical survives either metric; its advantage against static rank does not. This supports reporting the stronger cheap control and both views, without selecting a metric because it favors one method.

The median per-prefix relative gain is 0% versus original classical and −0.3980% versus either shortlist control. Means and medians describe different aspects of these few exposed observations; neither establishes statistical significance.

## Presentation and family sensitivity

Against static rank, the counts below retain all 15 prefixes. A prefix can appear in both “help in any” and “harm in any” if changing the presentation reverses its outcome. “All” covers only the three tested presentations.

| Relative margin | Help in any | Help in all | Harm in any | Harm in all |
|---|---:|---:|---:|---:|
| Strict improvement, >0% | 3 | 1 | 8 | 0 |
| >1% | 2 | 1 | 7 | 0 |
| >5% | 2 | 0 | 2 | 0 |
| >10% | 0 | 0 | 1 | 0 |

These are a frozen descriptive margin grid, not application-approved quality constraints or probabilistic guarantees. One prefix improves on static rank under all presentations at the 1% margin; none does so at 5%. This does not imply a predecision controller can identify that prefix.

Omitting Brotli changes the LLM-versus-static relative mean to +0.1467%; omitting lrzip gives −0.6940%; omitting MySQL gives −0.4710%. These are descriptive exclusions of each family in turn, not cross-validation or three new independent experiments. The full three-family result remains the reported result. Full sensitivity values for every baseline are retained in [summary.json](../results/v27_metric_sensitivity/summary.json).

![Relative objective gains by family and comparator](../results/v27_metric_sensitivity/relative_gain.png)

## Execution, verification and cost

The [exploratory protocol](protocol_v27_metric_sensitivity.md), implementation, tests and 133 input references were frozen before computing these summaries. Earlier outcomes were already known; this is explicitly post-hoc development analysis. Arm validation checked identical ten-observation prefixes, twenty unique configurations per arm, scalar positive targets and complete case/presentation denominators. The analyzer uses saved acquired labels and never calls the objective oracle or provider.

**190 tests passed in 1.33 seconds.** Hand-computable synthetic checks cover ratio arithmetic, unit scaling, invalid targets, family weighting, complete denominators and presentation-margin predicates. A separate verifier using 40-digit Decimal arithmetic reconstructed all 135 relative gains directly from saved arm labels, all nine family means, three overall means, nine family-exclusion means and 48 margin counts. Read-only analysis replay passed. The figure was visually inspected. Historical integrity audit passed for 1,670 frozen references, including the 133 new ones.

Actual analysis/plotting charged **0.462317 seconds**. New model calls, objective acquisitions, physical trials, downloads and external spending were all zero. The historical ledger now records 2253.075028/3600 experimental seconds, with 1346.924972 seconds remaining and no active session. Model calls remain exhausted at 200/200 follow-up requests (300 including the initial stage); historical recorded-label accesses remain 7058, with 1134 separate physical trials. Reusing observations does not erase their collection cost. No deployment-cost estimate or cloud-dollar saving is inferred from the relative percentages.

Evidence: [all comparisons](../results/v27_metric_sensitivity/comparisons.csv), [execution log](../artifacts/study_v27/run.log), [test log](../artifacts/study_v27/tests.log), [independent arithmetic](../artifacts/study_v27/decimal_verification.json), [accounting](../artifacts/study_v27/accounting.json).

Commands actually executed:

```sh
PYTHONPATH=src .venv/bin/python -m pytest -q
.venv/bin/python scripts/analyze_metric_sensitivity_v27.py
.venv/bin/python scripts/analyze_metric_sensitivity_v27.py --verify-only
.venv/bin/python scripts/verify_metric_sensitivity_v27.py
.venv/bin/python scripts/audit_goal_completion.py
```

The analysis refuses an existing output directory. Verification reads only. Prior docs and the pre-analysis ledger are archived in `artifacts/history/v27_before_analysis/`. The V26 reconstruction ZIP remains byte-for-byte unchanged and covers V25; it does not contain this new V27 analysis.

## Limits and next action

Three exposed development families cannot establish held-out routing success, practical cost justification or a general model advantage. Public-data contamination, measurement noise, untested presentations and model/prompt dependence remain unresolved. Ratios also depend on the objective's meaningful zero and on the chosen baseline; they are not universally preferable to normalized loss. No hypothesis test or equivalence claim is made.

**Next action:** agree on a prospective application-specific benefit/cost metric with Tim, using this sign reversal and the static control as concrete evidence, before collecting new held-out model/router outcomes. Preserve normalized loss as the original metric; do not retroactively choose whichever metric yields a positive result.
