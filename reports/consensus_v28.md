# V28: three-response voting gives a mixed gain at three times the requests

**Combining three real LLM selections improved normalized loss slightly over the fixed single-call condition, but worsened mean relative objective value by 0.133%.** It changed the final objective value in only three of fifteen cases: two improved and one worsened. This does not establish that three-call voting is worth its additional cost.

We executed **15 new continuations and charged 150 recorded-label acquisitions**, each from the same saved ten-label prefix with ten further evaluations. The model outputs were the three existing, provenance-checked real V22 responses for each prefix, not fabricated selections or fresh inference. All arms completed; none was dropped or retried. The 200-call follow-up allowance remained unchanged and exhausted.

## Fixed rule and actual result

Map each presentation's proposed IDs back to configuration rows, count votes across the three ten-row selections, and keep ten rows with the most votes. Break ties by the original classical shortlist rank, computed from candidate features and the ten acquired labels. All fifteen selection plans were saved and frozen before new outcome acquisition. The rule never used continuation labels. It is a hybrid of model votes and classical ranking, not a claim that voting alone caused any improvement.

Positive gains below favor voting. Normalized gain is comparator loss minus voting loss. Relative gain is `(best comparator target - best voting target) / best comparator target`, averaged within prefix/family as specified in the protocol. For the presentation-mean comparator, compute each of the three relative ratios separately before averaging.

| Comparator | Voting gain in normalized loss | Voting relative target reduction | Wins / ties / losses |
|---|---:|---:|---:|
| Original full-space classical | +0.00592171 | +2.4003% | 6 / 5 / 4 |
| Static shortlist rank | +0.00167879 | **−0.1695%** | 3 / 6 / 6 |
| Adaptive shortlist | +0.00348380 | +1.0219% | 3 / 6 / 6 |
| Single call, assigned IDs | +0.00017794 | **−0.1326%** | 2 / 12 / 1 |
| Mean of three separate one-call outcomes | +0.00166028 | +0.1398% | 7 / 4 / 4 |

Wins/ties/losses use normalized gain at tolerance 1e-12. For the last row the comparator is an average across alternative presentations, not an actual one-call output or a policy choosing the best presentation. All three families and five seeds remain included and families receive equal weight.

| Family | Static rank loss | Single assigned-ID loss | Mean one-call loss | Voting loss |
|---|---:|---:|---:|---:|
| Brotli | 0.00041457 | 0.00049911 | 0.00046855 | 0.00049198 |
| lrzip | 0.00139187 | 0.00092816 | 0.00124491 | 0.00116998 |
| MySQL | 0.03220595 | 0.02808258 | 0.03224341 | 0.02731406 |
| Equal-family mean | 0.01133746 | 0.00983661 | 0.01131896 | **0.00965867** |

The three cases whose final target changed relative to the assigned-ID response were MySQL/37 (+0.6296% relative reduction), Brotli/23 (+0.8685%) and lrzip/37 (−3.4878%). These examples explain the mixed aggregate; they are not an exclusion rule or a learned selector. All outcomes are in [cases.csv](../results/v28_consensus/cases.csv).

Voting reproduced the exact selected set of at least one component response in **12/15** cases. Classical ranking resolved a membership tie at the tenth position in **2/15** cases. None of the voting sets exactly matched the static top-ten set. Invariance to the order of these three ballots is built into the rule; robustness to other prompts, IDs, displays or model generations was not tested.

No voting arm beat the best observed component outcome. This is a **structural consistency check**, not a new negative efficacy finding: the vote-selected rows are a subset of the component union, so the best target in that union is an upper quality reference the vote cannot exceed. Choosing that best component after observing its outcome would be hindsight, not a deployable method.

![Measured voting comparison](../results/v28_consensus/comparison_readable.png)

## Cost: cached collection versus a future three-call scenario

V28 reused 45 real, already-paid-in-computation model responses. Actual **new inference was zero**, but the historical model cost is retained. The new branch acquisitions cost another 150 recorded-label accesses even where earlier arms acquired the same rows. These are offline table acquisitions, not fresh physical software measurements.

The deployment scenarios below use the observed V22 request usage for the included responses. Each scenario keeps 300 logical objective evaluations across fifteen cases. They are accounting scenarios, not fresh measured ensemble-service latency.

| Scenario across fifteen cases | Model requests | Input tokens | Output tokens | Recorded request-seconds |
|---|---:|---:|---:|---:|
| Fixed assigned-ID single call | 15 | 23,930 | 300 | 104.4697 |
| Mean one-call presentation usage | 15 | 23,930 | 300 | 106.1437 |
| Three-call voting | **45** | **71,790** | **900** | **318.4311** |

Voting therefore uses three times the requests/tokens; its summed observed request time is about 3.05 times the fixed assigned-ID condition. Loading, voting/control overhead and physical objective execution are excluded from these scenario totals. Actual V28 branch loops sum 0.277656 seconds, but that is local cached-data execution and does not measure a deployed optimizer's overhead. No cloud-dollar savings, practical utility or quality/time exchange rate is assumed. Relative objective percentages are not end-to-end speedups.

Actual preparation charged 1.103586 seconds, collection 0.974471, analysis/initial plotting 0.590581, and the readable figure 0.470656: **3.139294 experimental seconds** added. The ledger now totals 2256.214323/3600 seconds, with 1343.785677 remaining and no active session. Recorded-label acquisitions total7208; physical trials remain1134; model requests remain200/200 follow-up (300 including the initial stage). New downloads, external spending, publication and contact: none.

## Verification and reproducibility

The [protocol](protocol_v28_consensus.md), code, tests, fifteen selected-row plans, real cached responses and source inputs were frozen before collection:153 checksummed references. Preparation verified exact prompts and hashes, prefix identity, model/revision, generation parameters, mappings and raw output token decoding, then recomputed the shortlist from features and acquired labels.

**197 tests passed in 1.24 seconds.** Synthetic tests cover hand-calculated votes, boundary ties, ballot/order invariance, invalid responses, branch isolation and acquisition budgets. The separate evaluator independently reconstructed all fifteen vote selections and final states, checked all150 journal targets against original source rows, and verified paired budgets. A second verifier using 40-digit Decimal arithmetic checked150 paired metric values,10 aggregate gains and9 request-usage totals; it rebuilt votes directly from raw responses rather than trusting the plan. Read-only replay passed. Historical integrity audit passed all1823 frozen references.

The initial figure had crowded labels; a separate presentation-only script produced the inspected readable figure. Original plotting code and original image remain retained. Frozen collection/evaluation code and numerical outcomes were not changed.

Evidence: [full summary](../results/v28_consensus/summary.json), [acquisition journal](../results/v28_consensus/acquisitions.jsonl), [intended statuses](../results/v28_consensus/progress.json), [selection plans](../data/consensus_v28.json), [tests](../artifacts/study_v28/tests.log), [independent verification](../artifacts/study_v28/decimal_verification.json). Model output provenance remains in `results/v22_larger/requests.jsonl`.

Commands actually executed:

```sh
PYTHONPATH=src .venv/bin/python -m pytest -q
.venv/bin/python scripts/prepare_consensus_v28.py
.venv/bin/python scripts/run_consensus_v28.py
.venv/bin/python scripts/analyze_consensus_v28.py
.venv/bin/python scripts/analyze_consensus_v28.py --verify-only
.venv/bin/python scripts/verify_consensus_v28.py
.venv/bin/python scripts/render_consensus_v28.py
.venv/bin/python scripts/audit_goal_completion.py
```

Preparation ran inside the existing resource-accounting wrapper; its command output is saved. Preparation, collection and analysis refuse existing respective outputs. Verifiers read only. Mutable docs/ledger were archived under `artifacts/history/v28_before_execution/`. The V26 ZIP remains unchanged and covers V25, not V27/V28.

## Interpretation and next action

This is a small exploratory cache-based ensemble experiment on three exposed development families. It did not establish learned routing, unseen-system benefit, a universal robustness fix or the value of additional calls in production. Metric sensitivity remains: a normalized advantage coexists with a relative-target disadvantage against the fixed single call and static rank. More requests alone did not resolve that issue.

**Single next action:** prospectively specify the application's quality/latency tradeoff and untouched evaluation families before funding any new model/router collection. Keep static shortlist and a fixed one-call condition as controls; the present evidence does not justify adopting three-call voting as the default.
