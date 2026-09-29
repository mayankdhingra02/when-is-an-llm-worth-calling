# V24: how much opportunity is left for even a perfect router?

**Perfect hindsight routing can improve average normalized loss by at most 0.00023694 over first-displayed-ten selection in the average-presentation scenario.** It reaches that bound with four of fifteen calls. Uniform random escalation at the same four-call budget has expected gain 0.00005113. When using each prefix's minimum gain over the three observed presentations, the best hindsight gain over that control is **zero**, achieved with no calls.

These are new, exactly computed diagnostics from existing real V22 results. They are **not** learned-router performance. Hindsight knows the LLM and baseline outcomes before choosing which prefixes to escalate, information unavailable to a deployable controller. All prior collection costs remain counted.

## Complete result

Use all15 saved development prefixes (three families, five seeds each). For each baseline, assign every case either its mean gain over three unique presentations or its minimum observed gain. Evaluate every call budget k=0..15. At each k, the hindsight reference picks the best k gains; the matched-rate random reference uniformly selects k prefixes without outcomes. Independent exhaustive enumeration covers32768 subsets per comparison, **262144 allocations across all eight comparisons**.

| Baseline | Presentation-gain scenario | Maximum hindsight mean gain | Fewest calls at maximum |
|---|---|---:|---:|
| Classical continuation | Mean | +0.00499637 | 6/15 |
| Classical continuation | Minimum observed | +0.00263456 | 3/15 |
| Uniform expectation | Mean | +0.00113888 | 5/15 |
| Uniform expectation | Minimum observed | +0.00000291 | 2/15 |
| First displayed ten | Mean | **+0.00023694** | **4/15** |
| First displayed ten | Minimum observed | **0.00000000** | **0/15** |
| Lowest IDs | Mean | +0.00500804 | 5/15 |
| Lowest IDs | Minimum observed | +0.00172090 | 2/15 |

The comparison baseline matters: apparent routing opportunity against the classical continuation is substantially larger than opportunity against first-display selection on this shortlist. The positive mean-case oracle result should not be mistaken for a practical service improvement or a percent runtime saving. No application-specific value for these normalized-loss units has been established.

Against first displayed ten, the average-case hindsight selection is MySQL/53, MySQL/37, Brotli/23 and lrzip/11. Their identities are reported for audit only; using these observed cases as a routing rule would memorize exposed data. Exact random four-call escalation spans gains from -0.00004519 to +0.00023694, with mean +0.00005113 across1365 possible subsets. That distribution is a finite allocation diagnostic, **not** a confidence interval or p-value. The oracle's advantage over random at matched rate is about0.00018581; this is available hindsight opportunity, not demonstrated predictability from predecision features.

Always escalating all15 cases yields the prior mean gain +0.00019175. Choosing four cases perfectly increases that mean gain by only about0.00004519 while reducing the scenario's calls. An actual controller might do worse; this calculation makes no claim it can identify those four cases.

![All exact call-budget comparisons](../results/v24_opportunity/frontiers.png)

Panels have separate vertical scales. Solid curves use mean gains; dashed curves use minimum observed gains. Every budget, all baselines, allocation ranges and selected case identities are saved in [summary.json](../results/v24_opportunity/summary.json) and [frontiers.csv](../results/v24_opportunity/frontiers.csv). The first-display minimum-gain oracle can tie zero with some extra calls, but the fewest-call tie-break chooses zero.

## Cost interpretation

For the four-case mean-gain oracle versus first displayed, summing observed model request usage averaged over each case's three presentations gives **28.3981 request-seconds,6192 input tokens and80 output tokens**. Random four-case selection gives28.3050 expected request-seconds,6381.33 expected input tokens and80 output tokens. Fractional tokens are expectations across alternative presentations/subsets, not measured fractional tokens.

These are retrospective one-branch usage scenarios, excluding model startup, learning a controller, control computation and actual paired research overhead. Future runtime is not known at the decision point and is not used as a router feature. The minimum-quality scenario's usage still averages presentation times; it is not the latency of a selected worst-case presentation. A15-case deployment scenario retains300 logical objective evaluations, whichever branches it selects. No monetary utility, cloud-price saving or quality/time exchange rate is invented.

This analysis added **0.914865 seconds** of charged computation/plotting and **zero** model calls, objective acquisitions, physical trials, downloads or external spending. Actual historical inference remains200/200 follow-up calls,300 including the initial stage. Cumulative experiment runtime is2250.588368/3600seconds,1349.411632seconds remaining; active_since isnull. No further inference is authorized.

## Validation and limits

**171 tests passed in1.42seconds.** Synthetic checks cover hand-calculable frontiers, negative/tied gains, ordering invariance and invalid inputs. All128 frontier rows passed separate Decimal reconstruction from the original V22 CSV, including selected-case sums and exact combination counts. Exhaustive allocation maxima agree with sorted-gain maxima, and random means agree with the analytical expectation. Read-only replay passed and the figure was visually inspected. [Logs, tests and verification](../artifacts/study_v24/).

The [analysis protocol](protocol_v24_opportunity.md), code, tests and fixed inputs were frozen before computing these frontiers, after exposure to V22/V23. This remains post-hoc development analysis; it is not independent confirmation. Fifteen cases across three families are not fifteen independent software systems. Means assume equal use of the three observed presentations; minima cover only those presentations. The uniform baseline is an earlier retrospective expectation. Hindsight policies, robust routing, learned predictability, unseen-system generalization, practical cost justification and deployment are not demonstrated.

**Next action:** use the combined V22–V24 evidence to decide with Tim whether the small opportunity beyond cheap controls warrants a new application-grounded study. A useful next collection needs a practical benefit/cost threshold, genuinely untouched systems and a separate bounded allowance. Fitting additional routers to these same15 exposed prefixes would not resolve that evidence gap.

```sh
PYTHONPATH=src .venv/bin/python -m pytest -q
.venv/bin/python scripts/analyze_opportunity_v24.py
.venv/bin/python scripts/analyze_opportunity_v24.py --verify-only
```

All three commands actually ran. Completed analysis refuses overwrite; read-only replay makes no model calls, acquisitions or ledger changes. Preserve historical data, guards and ledgers.
