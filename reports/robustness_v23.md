# V23: the small LLM gain does not consistently survive presentation controls

**None of the 15 saved prefixes shows a strictly positive LLM gain over the first-displayed-ten control under all three tested presentations.** Four show a gain under at least one presentation. No case/presentation exceeds the earlier 0.02 normalized-loss margin against that control. This is a new, explicitly post-hoc analysis of the completed V22 measurements, with no new model calls or objective acquisitions.

The question matters because [V22](larger_model_v22.md) had a positive average gain. Repeated answers were stable, yet arbitrary candidate display/ID changes often changed the selected configurations. Here we check the resulting *quality*, pairing each LLM response with its corresponding control rather than assuming changed selections imply changed utility.

## Actual computation

All 15 prefixes from MySQL, Brotli and lrzip, five seeds each, enter the analysis. For each baseline and prefix, calculate baseline loss minus LLM loss under assigned IDs, reversed display and reassigned IDs. Keep the minimum, mean and maximum gain. Exclude exact repeats from quality summaries but retain their historical collection costs. A gain is strictly positive above 1e-12; smaller differences are numerical ties. The 0.02 margin comes from the earlier pilot and is not an application-validated threshold.

| Comparison | Gain in all 3 presentations | Gain in at least 1 | Both positive and negative gain | Gain >0.02 in all / any |
|---|---:|---:|---:|---:|
| Classical continuation | 3/15 | 6/15 | 1/15 | 1/15 / 2/15 |
| Exact uniform expectation | 2/15 | 11/15 | 9/15 | 0/15 / 1/15 |
| First displayed ten | **0/15** | 4/15 | 1/15 | **0/15 / 0/15** |
| Lowest IDs | 2/15 | 8/15 | 4/15 | 0/15 / 2/15 |

“Not positive in all three” can include ties; it does not mean the LLM was worse in every case. The first-display control itself changes its selected configurations when display order is reversed. These comparisons deliberately match each observed presentation. Uniform expectation is the saved exact retrospective reference, not a newly collected random arm.

The three prefixes with positive gain over classical under all tested presentations are MySQL/23, Brotli/23 and Brotli/71. Only MySQL/23 exceeds 0.02 under all three. That case still ties the first-display control, illustrating why classical-only comparisons can overstate the extra value of the LLM.

## How much depends on presentation and family?

Average the case-specific minimum, mean and maximum within family, then equally across the three families:

| Baseline | Mean of case minima | Original mean gain | Mean of case maxima |
|---|---:|---:|---:|
| Classical | +0.00013311 | +0.00426143 | +0.00672947 |
| Uniform expectation | -0.00319726 | +0.00093106 | +0.00339910 |
| First displayed ten | **-0.00014152** | +0.00019175 | +0.00071677 |
| Lowest IDs | +0.00147099 | +0.00493810 | +0.00813066 |

These minima/maxima describe only the three observed presentations and require hindsight per-case presentation selection. They are not confidence bounds, performance guarantees, adversarial robustness certificates or deployable routing results.

Omitting MySQL leaves the Brotli/lrzip average gain at +0.00018400 versus classical, **-0.00006553 versus first displayed**, -0.00011211 versus uniform expectation and -0.00010193 versus lowest IDs. The positive average against those cheap references depends on including MySQL. This is a concentration diagnostic, not a reason to discard either favorable or unfavorable families.

![Actual gain envelopes for all 15 prefixes](../results/v23_robustness/gain_envelopes.png)

Lines show observed min–max gain; dots show means. Panels have separate horizontal scales. Full per-case gains, classifications, family summaries and omission checks are in [case_envelopes.csv](../results/v23_robustness/case_envelopes.csv) and [summary.json](../results/v23_robustness/summary.json).

## Integrity, costs and limitations

The [V23 plan](protocol_v23_robustness.md), code, tests and exact V22 inputs were hashed before computing these new summaries, **after V22 results were exposed**. This is exploratory follow-up, not a prospective confirmatory study. No new model/prompt/permutation was searched, no controller was fit, and no held-out data was used. All original V22 average gains are reproduced unchanged.

**164 tests passed in 2.57 seconds**, including synthetic missing/duplicate/nonfinite-data rejection, ties, material gains, repeat exclusion and changing matched controls. The actual-data audit checked 180 min/mean/max values using independent Decimal arithmetic from the V22 CSV, then separately checked 300 case classification predicates. Read-only numerical replay passed; the figure was visually inspected. Logs and receipts are in [artifacts/study_v23](../artifacts/study_v23/).

This computation and plotting charged **0.684720 seconds**. Model requests, objective acquisitions, physical trials, downloads and external spending added: **zero**. Historical collection remains charged. Current request count is200/200; cumulative experimental runtime2249.673503/3600 seconds, remaining1350.326497 seconds. No active experiment worker remains.

There are still only three exposed software families, and three presentations do not characterize all possible formatting. Selecting the best observed presentation or favorable prefix after seeing outcomes is not a usable policy. The apparent effects cannot establish generalization, an internal model mechanism, model-size causality, real-world runtime savings or cost-benefit superiority. V22's original result is preserved; V23 adds a more restrictive interpretation.

**Next action:** agree on a practical benefit/cost threshold and require improvement beyond cheap selection controls before funding a new, prospectively specified held-out routing study. This evidence does not justify deploying or scaling the present router.

Executed commands:

```sh
PYTHONPATH=src .venv/bin/python -m pytest -q
.venv/bin/python scripts/analyze_robustness_v23.py
.venv/bin/python scripts/analyze_robustness_v23.py --verify-only
```

The first analysis refuses existing outputs. The read-only command recomputes the result from frozen V22 files without inference, new acquisitions or ledger mutation. Do not delete results or reset accounting to rerun collection.
