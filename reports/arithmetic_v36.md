# V36: arithmetic changes five search paths, but no final result

**Exact arithmetic changes5of20continuation trajectories and3acquired configuration sets, but changes none of the20final feasible runtimes.** All60comparisons of unchanged real LLM selections with these controls retain their scores and signs. This is a bounded robustness result: the V34 comparison survives this particular arithmetic ablation on these two exposed systems.

Twenty new continuations actually ran, each with ten additional recorded runtime/size-vector acquisitions after the same ten-row prefix: **200new charged accesses**,20/20completed arms. There were no new model calls, physical executions, downloads or external spending. The exact-arithmetic runner and independent integer-arithmetic evaluator agree on all200adaptive choices. Isolated Python3.10.13 and3.12.14 replays produce the same scientific summary hash.

## Reason for the experiment

V35 found that an independent verifier's floating summation could change tie ordering at five recorded decision states. Its corrected version explicitly reproduces the original binary64 reduction. That solved saved-result reconstruction, but did not answer whether following a different tie path changes the final optimization quality. V36 prospectively froze this finite follow-up after the earlier outcomes were known; it is therefore exploratory, not a new held-out experiment.

The new optimizer changes only the arithmetic of the nominal joint3NN control. It parses the acquired decimal strings as exact fractions, sums the three neighbor outcomes exactly, compares size sum with3×cap and ranks by runtime sum. The division by3 is unnecessary for ordering. Neighbor ties remain in acquired order; mathematically equal candidate predictions use original candidate order. No rounding tolerance or hyperparameter was selected after results. This is a labeled adaptation, not a replacement or correction of historical measurements.

All ten V34 prefixes are reused: Brotli0.3.0 and lrzip530, seeds11,23,37,53,71. The shortlist remains twenty candidates derived from acquired labels; full-domain control is separate. The cap remains the output size of the first fastest prefix row. Only charged acquired values enter recommendations. Objective acquisition logs are written before parsing; invalid and infeasible evaluations consume budget. No intermediate result triggered stopping or case selection.

## Complete trajectory changes

| System / seed | Control | Changed positions (of10) | Acquired set changed? | Original / exact final runtime |
|---|---|---:|---|---:|
| lrzip / 11 | joint_full | 1 | yes | 15587.2 / 15587.2 |
| lrzip / 37 | joint_shortlist | 7 | yes | 15373.6 / 15373.6 |
| lrzip / 53 | joint_full | 8 | yes | 15587.2 / 15587.2 |
| brotli / 37 | joint_shortlist | 2 | no | 1.57 / 1.57 |
| brotli / 53 | joint_shortlist | 3 | no | 1.528 / 1.528 |

The other15trajectories are identical. All20arms retain the same best feasible configuration and source runtime. There are21changed continuation positions overall. Two Brotli paths merely reorder the same configuration set; three lrzip paths acquire different sets. None improves or harms the retained terminal runtime in this experiment. Raw recorded runtime units are preserved within each system; these rows are not pooled as absolute runtimes.

![Trajectory changes and unchanged terminal runtime](../results/v36_arithmetic/arithmetic_sensitivity.png)

## LLM comparisons remain unchanged

LLM gain is `(classical feasible runtime − LLM feasible runtime) / classical feasible runtime`; positive favors the LLM. Average within each system's five seeds, then weight the two systems equally. All three presentations remain included. The fixed assigned-ID result stays **−0.3015%** against the shortlist control and **−1.6470%** against the full-domain control. The reversed-display shortlist mean remains slightly positive and family-dependent; no presentation is chosen after inspection.

| Presentation | Control | Original mean LLM gain | Exact-arithmetic mean LLM gain | Wins / ties / harms |
|---|---|---:|---:|---:|
| assigned_ids | joint_shortlist | -0.3015% | -0.3015% | 1 / 6 / 3 |
| assigned_ids | joint_full | -1.6470% | -1.6470% | 0 / 5 / 5 |
| reverse_display | joint_shortlist | +0.2406% | +0.2406% | 2 / 5 / 3 |
| reverse_display | joint_full | -1.1159% | -1.1159% | 1 / 4 / 5 |
| reassigned_ids | joint_shortlist | -0.2704% | -0.2704% | 1 / 7 / 2 |
| reassigned_ids | joint_full | -1.6040% | -1.6040% | 0 / 4 / 6 |

The thirty model selections are the actual V22 Qwen2.5-1.5B-Instruct responses with revision`989aa7980e4cf806f80c7fef2b1adb7bc71aa306`. This stage binds their raw output IDs to the saved candidate mappings and outcome states; full original token/cache provenance was independently verified in V35 and frozen as input. No model response was synthesized. Those prompts were runtime-only, and terminal size filtering is retrospective; V36 does not test a new size-aware model or a benefit-aware router.

## Verification and reproducibility

The collector uses Fraction arithmetic. A separate standard-library evaluator parses decimal tuples into integers at a common scale, then replays selections without Fraction or optimizer imports. It reconstructs source filtering/deduplication, all prefixes, budgets, exact prediction traces, final feasibility, the200ordered journal charges, all20paired classical changes and60model comparisons. Source targets appear only in acquisition or offline evaluation, never as unacquired input to a chooser.

**246 tests passed in1.24s.** **391 inputs** were frozen before collection. Both isolated interpreter replays passed with summary hash`29154293e59585dd76f781c4e9ec8a222769aa2b99569b7fbe6688cd0e553b6a`. The historical audit passes **3,149frozen references**. The PNG/SVG figure was inspected. No original protocol, source implementation, model response, V34 output or reproduction archive was overwritten.

Executed from the project root:

```sh
.venv/bin/python scripts/prepare_arithmetic_v36.py
.venv/bin/python -m pytest -q
.venv/bin/python scripts/run_arithmetic_v36.py
.venv/bin/python scripts/analyze_arithmetic_v36.py
.venv/bin/python -I -S scripts/verify_arithmetic_v36.py
.venv/bin/python scripts/audit_history_v30.py
```

A second verifier run used the already available Python3.12 interpreter with`-I -S`. The prepare/collection/analysis commands refuse to overwrite completed outputs; the verifier is read-only. Plotting is `render(summary)` in the analyzer. The experiment's exact manifest is `data/arithmetic_v36.json`, protocol/freeze are `reports/protocol_v36_arithmetic.*`, raw outputs and tables are `results/v36_arithmetic/`, and command logs/accounting/replay receipts are `artifacts/study_v36/`. The V35.1 portable ZIP remains a verified V34 snapshot and does not include these new V36 arms.

## Actual collection versus deployment cost

New collection: **200joint-vector lookups**, reusing100previously charged prefix vectors across20branches. Logical per-arm totals sum to400. Historical prefix/model/control costs remain in the total; reuse is not new inference or globally unseen data. A hypothetical one-method deployment for all10cases still consumes200vectors inclusive of prefixes; an LLM policy would additionally need requests and controller/startup costs. V36 measures no deployment savings.

Collection took **2.868505 ledger seconds**, analysis/rendering **2.273446**, total **5.141951**. Tests/development/read-only replays are outside the experiment-runtime ledger. Cumulative charged runtime **2286.489703/3600s**, remaining **1313.510297s**. Historical recorded acquisitions **9,308**, physical trials **1,274**, model requests **200/200follow-up**(300includinginitial). Original V22 request/token/runtime costs are unchanged and retained. No new model requests,retries,tokens,physical trials,downloads or external spend occurred; no job remains active.

## Limits and next action

This finding concerns two exposed families, two fixed controls and one fixed20/10budget. It does not prove numerical equivalence on other systems, budgets or objectives, or that a change in trajectory is harmless in general. Repeated seeds are not independent systems; no confidence interval or formal guarantee is claimed. The prefix-size cap is a research default, not application-approved utility or decompression correctness. No fresh size-aware LLM evaluation, unseen-system learned routing or physical deployment was tested.

**Single next action:** run the existing V35.1 archive on a second machine for independent review before expanding data collection. The numerical robustness question is now resolved for the tested cases; further numerical variants on them are not a substitute for new independent evidence. New scientific collection still follows [the prospective plan](next_experiment_v34.md): application-grounded quality/gain, untouched groups,strong controls and an explicit bounded model allowance or compatible cache. The current request allowance is exhausted.
