# STATUS — V59 completed and independently verified

Updated 2026-09-26T00:13:06.359690+00:00. The user's explicit approval covered
576 physical invocations and a 7200-second local collection cap, with zero model
requests or spending. This stage is complete; no experiment remains running.
The broad useful-LLM/router goal is still unachieved. Scientific honesty overrides
finding a positive result. Resume here and in `reports/workload_screen_v59.md`.

## New concrete result

All 576 intended trials ran and passed correctness checks: 288 Java invocations
(288 warmups plus 288 final iterations) and 288 independently validated planning
runs, each with plan cost 105. Zero failures, retries, or unattempted cases.
Collection took 4947.765867 seconds (82.46 minutes),
within 7200 seconds. All four workloads were included: Java/Xalan small and large,
Fast Downward p01 and p10; 48 configurations × three repetitions each. These are
**two software families**, not four independent systems. V57 p20 remains a failed
admission with three CPU timeouts; it is not a negative LLM result.

The frozen offline comparison completed 60 arms, five seeds per workload, with
20 inclusive outcomes per arm and a shared 10-outcome prefix. All 800 recorded
aggregate accesses are charged. Analysis took 5.452215 seconds.
Random, greedy 3NN, and RF-LCB were fixed before collection. Decisions used only
acquired labels; full-table scoring followed all saved choices. No new LLM calls.

| Workload | Best recorded median | Valid-setting median CV | Frozen threshold | Gate cases |
|---|---:|---:|---:|---:|
| Xalan small | 175.000 ms | 6.617% | 13.234% | 0/5 |
| Planning p01 | 120.770 ms | 3.848% | 7.696% | 0/5 |
| Xalan large | 11508.000 ms | 1.635% | 5.000% | 0/5 |
| Planning p10 | 3921.379 ms | 1.704% | 5.000% | 0/5 |

No workload passes the frozen opportunity screen. Crucial qualification: that
screen uses the hindsight best-of-three classical portfolio, not a deployable
20-evaluation policy. The joint research ledger charges 40 aggregate accesses per
case (10 shared prefix plus three 10-step continuations). On p10, random and RF-LCB
each reach the recorded minimum 4/5 times, 3NN only 2/5. Remaining headroom reaches
26.181% for random and 32.505% for both 3NN and RF-LCB, on different seeds.
The portfolio reaches the minimum 5/5. No single arm does. Thus a conservative gate
failure does NOT establish no selective opportunity over one fixed baseline,
no method-selection challenge, no possible LLM gain, or equivalence. Other three
workloads' every actual arm lies below their respective thresholds.

## Evidence and checks

- `reports/workload_screen_v59.md`: regenerated report, figures, arm-specific results,
  complete denominator, source/utility limits, research versus deployment cost.
- `results/v59_workload_physical/`: all 576 start/result/log receipts, schedule,
  complete case journal, Java validation, planning plans/SAS, terminal summary.
- `results/v59_workload_screen/`: 4 tables of 48 three-repeat medians, 20 prefixes,
  60 arms, 800-event ledgers, CSV, summary, and two PNG/SVG figures.
- `artifacts/study_v59/verification.json`: independent reconstruction of all 720
  choices, 800 labels, 60 budgets/prefixes, all medians/CVs/gates, 288 valid plans,
  Java validation and retained output hashes, and 358 frozen input hashes.
- `artifacts/study_v59/tests.log`: **382 tests passed**. Synthetic fixtures remain
  separate from measured data. Both scientific figures visually inspected.
- `data/live_manifest_v59.json`: family-grouped data/runtime/source lineage.
- `artifacts/study_v59/evidence_manifest.json` and `.sha256`: final evidence seal;
  `seal_verification.json` verifies it without rerunning experiments.
- User approval and protocol binding: `configs/authorization_v59.json` and
  `artifacts/study_v59/approval_receipt.json`. The frozen protocol's old title says
  not authorized/executed because it records the pre-approval state; it is immutable.

No frozen collection/analysis settings changed. Initial sandbox `ps` preflight
failed before launching a workload; `preflight.log` preserves it. Approved normal
sandbox escalation then ran the unchanged collector once, successfully. This was
not an experimental failure/retry. No result was excluded. Runtime guard, 60-second
Java wall limit, 30-second planner wall/27-second CPU limit, sampled 2 GiB RSS and
2 GiB scratch limits remained unchanged. The process is finished, exit code 0.

## Commands actually executed

```sh
.venv/bin/python scripts/collect_workloads_v59.py
.venv/bin/python scripts/screen_workloads_v59.py
.venv/bin/python scripts/verify_workloads_v59.py
.venv/bin/python -m pytest -q tests
.venv/bin/python scripts/report_workloads_v59.py
.venv/bin/python scripts/manifest_workloads_v59.py
```

Collector, primary screen and seal are one-shot; never delete outputs to rerun them.
Verifier/report renderer can replay saved evidence without inference. Their logs
are in `artifacts/study_v59/`. No new approval is needed for read-only review.

## Accounting and remaining limits

New actual research cost: 576 physical invocations, 800 recorded aggregate accesses,
4947.765867 seconds physical collection, 5.452215 seconds
offline selection. Verification took 6.469044 seconds; tests report 1.80 seconds.
These are separate from deployment estimates. One deployed 20-outcome arm would
need 60 physical invocations under this median-of-three recipe, conditional on a
known utility contract; setup/admission/validation and warmups are additional costs.

Cumulative recorded accesses: **24,958**. Physical compression: **2,234**; Java:
**441 invocations / 882 iterations**; planning: **444 invocations**. Model requests:
**1,976**, unchanged. No new download; prior ledger remains **4,767,971,303 bytes**,
with **600,737,817 bytes** left under 5 GiB. New external experiment spend USD 0.
Electricity, hardware amortization, and agent/user time costs are unknown.

The unused part of V59's 7200-second cap is not authorization for another campaign.
V59 authorizes zero inference. Preserve historical V49 prompt and V54/V56 grid
stopping decisions. Retire these now-exposed V59 grids from confirmatory tuning.
No paid/cloud resources, push, publication, author contact, or background job.

## Single next action and untested work

**Freeze an independent-software-family evaluation design, with one deployable
classical comparator and application-defined utility, before any further LLM calls.**
Do not reinterpret the hindsight portfolio as that comparator. See prioritized
`reports/next_experiment.md`. Preserve MongoDB/Redis/Storm reservations; audit their
historical exposure before claiming they are held out. Selecting a new family,
source admission, budget, and model request allowance remain to be specified.

Untested: real LLM continuation on these four workloads; a pre-decision selector
that predicts the better classical method; independent-family benefit routing;
independent-machine physical reproduction; general VAL validation; p20 beyond its
failed caps; and gains in larger or different configuration spaces. One host,
three repetitions, noisy recorded minima, and two exposed families do not establish
LLM usefulness, novel routing, generalization, or Q2 journal readiness.

## Prior history

Compact V57/V58 report: `reports/workloads_v57_v58.md`. The complete earlier STATUS,
README, next-experiment plan, and disabled V59 authorization are preserved under
`artifacts/study_v59/previous_snapshot/`, with `mapping.json` binding their original
V58 seal hashes. The original V58 seal is unchanged. Earlier reports/results remain
in place; read them only when their specific evidence is needed.
