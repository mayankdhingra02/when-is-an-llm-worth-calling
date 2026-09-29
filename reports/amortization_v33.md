# V33: recovering model-request time depends on baseline strength and presentation

**Against fixed sequential 3NN, only one of fifteen assigned-ID LLM outcomes improves the recorded target; eight tie and six worsen it.** In the improving case, the hypothetical future baseline work needed to recover the observed model request is **444.06 seconds**. That case ties the classical result after IDs are reassigned, so **no case has a finite recovery threshold under every one of the three observed presentations**.

This is a newly executed cost-scenario analysis using real V22 model responses and previously collected classical outcomes. It is not fresh inference, measured deployment savings or a working benefit router. Both the response provenance and the arithmetic were independently replayed. The stronger comparator and exposed-data limitations remain central.

## Scenario and assumptions

For each paired outcome, let `b` be the classical arm's best positive recorded target, `l` the LLM arm's, and `g=(b−l)/b`. Let `C` be the exact observed request wall time. If a future workload would take `S` seconds under the classical-selected configuration, the modeled request-time-adjusted saving is:

`net seconds = S × g − C`

When `g>0`, equality occurs at `S*=C/g`; a positive saving requires `S>S*`. A tie or harm (`g<=0`) cannot recover a positive request cost in this scenario.

**Assumptions:** the recorded target ratio transfers proportionally to future elapsed work, settings have equally acceptable quality, the effect persists, and other differential costs cancel or are excluded. None of these is established by this analysis. Expressing `S` in baseline-work seconds avoids assuming absolute units for the original tables; it does not validate the target-to-runtime relationship. Model startup, controller time, differing objective-evaluation costs, quality validation and future retries are excluded. This is recovery of one cost component, not a complete net-cost analysis or a lower bound on total deployment cost.

Primary presentation is the original assigned-ID condition. A secondary hypothetical scenario chooses one of the three observed presentations with equal probability, using `mean(C)/mean(g)` when the mean gain is positive. This is one call, not a three-call ensemble. Recovery for every observed presentation requires each individual gain to be positive and uses `max(C_j/g_j)`. It covers only three tested conditions, not all possible prompts or future model behavior. Post-call latency is evaluation evidence, never a controller input here.

## All baseline results

All fifteen prefixes, three exposed software families and five seeds per family remain included. All four baselines are fixed; no baseline or presentation is chosen per case to improve the result. The original full-space baseline, static shortlist rank and adaptive shortlist centroid are secondary comparisons; sequential 3NN is primary.

| Comparator | Fixed-presentation improvements / ties / harms | Fixed-presentation mean relative gain | Always-call recovery: equal baseline-work seconds per case | Cases improving in all three presentations |
|---|---:|---:|---:|---:|
| **Sequential 3NN** | **1 / 8 / 6** | **−0.9106%** | **No finite threshold** | **0/15** |
| Original full-space classical | 6 / 5 / 4 | +2.5250% | 275.83 | 3/15 |
| Static shortlist rank | 3 / 6 / 6 | −0.0574% | No finite threshold | 1/15 |
| Adaptive shortlist centroid | 3 / 7 / 5 | +1.1655% | 597.59 | 2/15 |

The aggregate threshold uses equal future baseline work `S` for every case, with within-family and then equal-family averaging. It is not the average of per-case thresholds and does not mean every called case benefits. Different deployment frequencies or work amounts could change the aggregate. The original normalized-loss metric is unchanged in earlier reports; this new conditional cost scenario explicitly uses paired target ratios.

Under the equal-probability one-presentation scenario, the always-call aggregate has no finite recovery point against sequential 3NN or static rank. Thresholds against original classical and adaptive shortlist centroid are 315.81 and 812.92 seconds per case, respectively. These more favorable comparisons are retained rather than suppressed.

## The sole improving case against sequential 3NN

MySQL, seed 53, has a classical target of 52.7769. The observations are:

| Presentation | LLM target | Relative gain | Actual request time | Scenario recovery threshold |
|---|---:|---:|---:|---:|
| Assigned IDs, primary | 52.1542 | +1.17987% | 5.23933 s | 444.06 baseline-work s |
| Reversed display | 52.1542 | +1.17987% | 5.34913 s | 453.36 baseline-work s |
| Reassigned IDs | 52.7769 | 0% | 5.73275 s | No finite threshold |

The hypothetical one-presentation mean threshold is 691.65 seconds. It does not guarantee recovery on a particular call. The MySQL case identity is disclosed for audit, not proposed as a memorized routing rule. The percent differs from the reverse comparison reported in V29 because the denominator is now the classical target, not the LLM target.

The fixed work grid is `S = 0, 1, 10, 100, 1000, 10000, 100000` seconds per case. Against sequential 3NN at `S=1000`, always calling yields −16.0709 modeled seconds per case on average. A nondeployable hindsight selector calls only the one helpful case and yields +0.4373 seconds per case averaged over all fifteen. At `S<=100`, even that hindsight selector calls nobody. No predecision model has been shown to identify profitable calls.

![Request-time recovery scenarios](../results/v33_amortization/recovery.png)

The figure shows signed-log axes, nonnegative work values and separate panel ranges. Hindsight uses the realized gain/cost, and never-call is zero by the scenario's definition. All **56 grid rows**, including both presentation scenarios and every comparator, are retained in [curves.csv](../results/v33_amortization/curves.csv). Per-response values and request/cache identities are in [comparisons.csv](../results/v33_amortization/comparisons.csv); all sixty case/comparator scenarios are in [cases.csv](../results/v33_amortization/cases.csv).

## Actual execution, provenance and cost

The [protocol](protocol_v33_amortization.md), code, tests, source data, real responses, saved branches and validation log were frozen in [199 references](protocol_v33_amortization.freeze.json) before scenario calculation. Earlier outcomes were already exposed; this is exploratory analysis. No samples were added, filtered or reclassified as independent systems.

- **224 tests passed in 1.44 seconds.** Synthetic checks cover the recovery equation, ties/harms, invalid or missing costs, duplicate presentations and the distinction between ratios of means and mean thresholds.
- The existing local-tokenizer verifier freshly replayed **all sixty real V22 request/token/cache/provenance mappings**, 150 paired arms and their original 1,500 charged acquisitions, without inference.
- The new analyzer checked real response-to-selection mapping, same saved prefix, twenty distinct acquired rows per arm, positive scalar targets, exact model identity/revision, measured namespaces and known usage. It calculated **180 paired comparisons** and **sixty case scenarios**.
- A separate Decimal verifier reconstructed targets from original source CSVs and reconciled real request costs, checking **1,457 numeric values**, twenty aggregate counts and every grid row. Read-only replay passed.
- All **2,512 historical/current frozen references** passed integrity checks. The V26 standalone ZIP is unchanged and remains a V25 snapshot.

The real source model remains Qwen/Qwen2.5-1.5B-Instruct at revision `989aa7980e4cf806f80c7fef2b1adb7bc71aa306`, local CPU float32, greedy generation and twenty output tokens. V22's historical collection comprises **60 requests, 95,720 input tokens, 1,200 output tokens and 431.694863 request-seconds**. This includes fifteen exact-repeat calls even though they are excluded from the three-unique-presentation efficacy scenario. The one observed model-session startup was 8.565649 seconds, including 4.493516 seconds of loading; these must not be summed or multiplied by sixty. Reusing these records does not erase historical collection cost.

V33 added **0 model calls, 0 objective acquisitions, 0 physical trials and 0 downloads**. Analysis/initial rendering charged 0.700935 seconds. Visual inspection found that automatic signed-log scaling displayed impossible negative work values; a separate renderer constrained the horizontal axis to the scenario domain, charging 0.321947 seconds. Initial figures are retained, frozen scientific code is unchanged, and no numerical result changed. The corrected figure was visually inspected. Total added experiment runtime: **1.022882 seconds**.

Global runtime is **2,277.118492 / 3,600 seconds**, leaving **1,322.881508 seconds**, with no active job. Recorded acquisitions remain 8,308 and physical trials 1,274. Follow-up requests remain exhausted at 200/200, 300 including the original stage. Read-only validation/test time is separate under the established accounting convention. External spend is USD 0; no cloud, publication, remote push or external contact occurred.

Executed commands:

```sh
PYTHONPATH=src .venv/bin/python -m pytest -q
.venv/bin/python scripts/verify_report_larger_v22.py --verify-only
.venv/bin/python scripts/analyze_amortization_v33.py
.venv/bin/python scripts/analyze_amortization_v33.py --verify-only
.venv/bin/python scripts/verify_amortization_v33.py
.venv/bin/python scripts/render_amortization_v33.py
.venv/bin/python scripts/audit_history_v30.py
```

The analyzer refuses completed outputs. Receipts, the real-model provenance replay, arithmetic verification, accounting and render correction are under [artifacts/study_v33](../artifacts/study_v33/).

## Limits and next action

This does not establish cost-effective escalation or a useful learned router. Three exposed families, repeated post-hoc analyses, presentation sensitivity, unvalidated application quality and unknown future workload frequency prevent that claim. Actual future request latency and target ratios may differ. V32 measured timing variation on different compression tasks; its variability cannot be imported as an uncertainty interval for these V22 targets. The three-presentation requirement is a finite observed-condition check, not a reliability guarantee.

**Next action:** specify the application quality constraint, expected configuration reuse and practical gain margin before authorizing new paired collection. Then use development measurements to set repetition/cost estimates, freeze the strong classical comparator and evaluate on untouched system groups. A new bounded local-inference allowance or compatible provenance-checked cache is required for fresh LLM evidence. Further arithmetic on these same exposed cases will not establish generalizable routing success.
