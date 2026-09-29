# V29: a fixed cheap predictor beats the tested LLM averages

**Sequential three-nearest-neighbor search achieved lower average loss than the fixed single-call LLM, the presentation-mean LLM and three-call voting, without model requests.** Its advantage has the same direction under normalized loss and mean relative target reduction. This is a positive result for a stronger cheap baseline on the exposed development sample, not evidence that a benefit-aware LLM router works or that nearest-neighbor search generally dominates LLMs.

We actually executed **30 new continuations, charging300 recorded-label acquisitions**: two fixed modes for each of15 saved prefixes (three families, five seeds). Every arm shared its existing ten-observation prefix and20-row shortlist, acquired ten more configurations, and finished at20 evaluations. All completed; no failure, retry or case exclusion occurred. No model output was generated or fabricated.

## The fixed comparator and the feedback contrast

For each unobserved shortlist row, find the three closest acquired configurations by number of unequal feature coordinates. Predict its objective as the arithmetic mean of those three acquired labels. Neighbor ties follow acquisition order; equal predictions follow the original seeded candidate order. Numeric feature levels remain nominal, matching the existing candidate representation. The implementation uses exact Decimal representations of acquired scalar labels with40-digit precision for deterministic ranking. Hidden objective values and full-table scaling are absent from the recommender.

The **batch** mode ranks all ten selections using only the original ten labels, matching the LLM's one-batch information schedule. The **sequential** mode recomputes predictions after each newly acquired label. The value k=3 and nominal distance were fixed from the earlier V12 control rather than selected through a new parameter search. This ordinary predictor is not claimed as a novel optimizer.

| Method | Equal-family mean normalized loss |
|---|---:|
| Original classical | 0.01558039 |
| Static shortlist rank | 0.01133746 |
| Adaptive centroid shortlist | 0.01314247 |
| LLM, fixed assigned-ID single call | 0.00983661 |
| LLM, mean of three separate presentations | 0.01131896 |
| Three-call voting | 0.00965867 |
| New batch 3NN | 0.01059212 |
| **New sequential 3NN** | **0.00930105** |

These are all exposed-data descriptive results. Do not retrospectively choose a different winning method for each family or present this table as an independently validated model-selection policy.

For the sequential arm, positive gains below favor the cheap optimizer. Relative reductions divide each comparator-minus-new target difference by that comparator's best target before averaging; they are not deployment speedups. For the presentation-mean comparator, average the three pairwise ratios.

| Comparator | Sequential 3NN normalized gain | Relative target reduction | Wins / ties / losses |
|---|---:|---:|---:|
| Original classical | +0.00627933 | +3.3864% | 6 / 8 / 1 |
| Static shortlist | +0.00203641 | +0.8523% | 3 / 11 / 1 |
| Adaptive centroid shortlist | +0.00384142 | +2.0553% | 3 / 11 / 1 |
| Fixed single-call LLM | **+0.00053556** | **+0.8721%** | **6 / 8 / 1** |
| Mean single-call presentation outcome | +0.00201790 | +1.1472% | 10 / 4 / 1 |
| Three-call voting | +0.00035762 | +0.9979% | 7 / 7 / 1 |

The loss against the fixed single-call LLM occurs on MySQL/53: the 3NN target is1.1940% worse. It remains in every aggregate. No significance, equivalence or guaranteed improvement is claimed.

## Sequential feedback matters on this sample

Sequential updating improved on batch 3NN in **3/15 cases**, tied in12 and worsened in0. Mean gain is+0.00129107 normalized loss and+0.7783% relative target reduction. Improvements occur on MySQL/23 (+2.7212%), lrzip/23 (+0.8583%) and lrzip/37 (+8.0955%). These are outcome descriptions, not rules for selecting when to update.

| Family | Batch 3NN loss | Sequential 3NN loss |
|---|---:|---:|
| Brotli | 0.00041457 | 0.00041457 |
| lrzip | 0.00143490 | 0.00076327 |
| MySQL | 0.02992690 | 0.02672532 |

The batch-only result is weaker: it loses to the fixed LLM on normalized loss by0.00075551, although relative target gain is+0.0412%. Thus the sequential result cannot be interpreted as a pure comparison of model intelligence under identical feedback. It is a practical equal-evaluation-budget continuation comparison. [All30 outcomes and all six comparators](../results/v29_neighbors/cases.csv) are retained.

![Three-neighbor comparison](../results/v29_neighbors/comparison.png)

## Actual execution, costs and verification

The [protocol](protocol_v29_neighbors.md), code, tests, original source inputs and reused results were frozen before any of the300 new acquisitions:176 checksummed references. This freeze occurred after earlier results were known, so the comparison remains exploratory. The collection stage had a60-second cap, used one sequential worker, and preserved checkpoints and intended status for all30 arms. Each journal read was charged even if a historical arm had already seen that configuration's outcome.

**205 tests passed in1.22seconds.** Hand-calculated synthetic tests cover nearest-neighbor and prediction ties, acquired-label requirements, batch independence from newly acquired targets, sequential use of new evidence, branch isolation, valid candidate sets and exact acquisition counts. Synthetic fixtures are excluded from measured aggregates.

A separate evaluator used vectorized mismatch distances and stable neighbor ordering, independently reconstructed all300 choices, supporting neighbor IDs and predicted targets, checked original-source journal values, and replayed30 final states. A second Decimal source scorer checked360 paired metric values,24 aggregate comparisons,72 win/tie/loss counts and30 feedback-pair metrics. Read-only replay passed. The figure was visually inspected. Historical integrity audit passed all1999 frozen references. [Execution/test/verification receipts](../artifacts/study_v29/decimal_verification.json), [tests](../artifacts/study_v29/tests.log), [acquisition journal](../results/v29_neighbors/acquisitions.jsonl) and [complete statuses](../results/v29_neighbors/progress.json) are saved.

Actual collection charged1.452749 seconds and analysis/plotting0.667621: **2.120370 experimental seconds added**. The batch loops totaled0.329642 seconds and sequential loops0.363619 seconds across15 cases each; these are offline local computations and CSV acquisitions, not end-to-end service latency or fresh physical measurements. No new inference, physical trials, downloads or external spending occurred.

Actual historical recorded-label accesses now total7508; physical trials remain1134; follow-up requests remain200/200 (300 including the initial stage). Runtime is2258.334693/3600seconds, with1341.665307 remaining and no active session. A hypothetical deployment of either new method across15 cases uses300 logical evaluations andzero model requests; the actual research collection acquired both continuations and retains all historical model costs. No monetary savings or speedup against deployment has been estimated.

Commands actually executed:

```sh
PYTHONPATH=src .venv/bin/python -m pytest -q
.venv/bin/python scripts/run_neighbors_v29.py
.venv/bin/python scripts/analyze_neighbors_v29.py
.venv/bin/python scripts/analyze_neighbors_v29.py --verify-only
.venv/bin/python scripts/verify_neighbors_v29.py
.venv/bin/python scripts/audit_goal_completion.py
```

Collection refuses an existing result directory; analysis refuses an existing summary. Verification reads only. Prior docs and ledger are preserved in `artifacts/history/v29_before_execution/`. Earlier protocols/outcomes remain unchanged. The V26 standalone archive reconstructs V25 and does not include the subsequent V27–V29 experiments.

## Limits and next action

This comparison was chosen after many analyses of the same three development families. Freezing its rule prevents within-run tuning but does not remove that accumulated selection bias. Seeds are not independent systems. The positive average therefore needs untouched-family confirmation and cannot support a population claim, acceptance prediction or probability of eventual success. No new model or fresh LLM inference was tested, no router was fit, and no application-specific benefit/cost contract was established. Recorded target reductions do not include model latency or measurement uncertainty.

**Single next action:** carry this fixed sequential3NN baseline into a prospectively specified paired evaluation on genuinely untouched software families, with an application-defined quality/cost metric and a separately bounded inference allowance. The present result strengthens the cheap alternative that an escalation controller must beat; do not keep changing this predictor on the same exposed outcomes.
