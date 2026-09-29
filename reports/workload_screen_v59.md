# V59 — expanded, correctness-checked classical screen

Actual local execution after explicit user approval of a 7200 s collection cap.
**No workload passed the frozen opportunity screen. Do not retune these exposed grids or launch additional model calls on them under this protocol. This is a bounded negative development result, not proof that LLM optimization cannot work.** Four workloads belong to two software families; there is no new
independent-system or held-out router claim. V57's failed p20 admission remains
reported (three CPU timeouts) and is not relabeled as a negative LLM result.

## Execution and evidence

All 576 / 576 intended invocations attempted, 576 valid,
0 resource failures, 0 unattempted; no retries or
outcome-driven exclusions. Stage 4947.765867 s / 7200 s. Workload/configuration
order, three repetitions, correctness checks and penalties were frozen before
collection. Plan validity and recomputed cost 105 checked independently; Java output
hashes match the predeclared workload-specific reference streams. The full grid
uses unchanged V54/V56 configuration choices on V57-admitted new workloads.

Completed 60 classical arms: five seeds per workload, shared 10-observation prefix,
random/3NN/RF-LCB continuations to 20 inclusive aggregate outcomes.800 actual recorded
acquisitions, offline 5.452215 s / 180 s. All labels charged; own acquired
labels/features only. Full-table scores computed after all choices were saved.
No LLM output, inference requests, downloads, cloud resources or external spending.

| Workload | Valid trials | Best recorded median (ms) | Median valid-setting CV | Gate threshold | Cases meeting gate | Decision |
|---|---:|---:|---:|---:|---:|---|
| javagc / small | 144/144 | 175.000 | 6.617% | 13.234% | 0/5 | FAIL |
| fastdownward / p01 | 144/144 | 120.770 | 3.848% | 7.696% | 0/5 | FAIL |
| javagc / large | 144/144 | 11508.000 | 1.635% | 5.000% | 0/5 | FAIL |
| fastdownward / p10 | 144/144 | 3921.379 | 1.704% | 5.000% | 0/5 | FAIL |

Gate compares the hindsight best-of-three classical portfolio with recorded minimum;
it is deliberately conservative and NOT a deployable policy. Its success cannot be
attributed to a single 20-evaluation arm without checking that arm's own results:

| Workload | Random exact minimum | 3NN exact minimum | RF-LCB exact minimum | Prefix headroom range |
|---|---:|---:|---:|---|
| javagc / small | 1/5 | 2/5 | 2/5 | 1.685–3.846% |
| fastdownward / p01 | 0/5 | 4/5 | 4/5 | 0.712–1.639% |
| javagc / large | 3/5 | 1/5 | 1/5 | 0.139–0.844% |
| fastdownward / p10 | 4/5 | 2/5 | 4/5 | 0.000–32.505% |

The actual arms retain different amounts of opportunity. These ranges cover all
five fixed seeds; they are descriptive, not confidence intervals:

| Workload | Random20 remaining headroom | 3NN20 remaining headroom | RF-LCB20 remaining headroom |
|---|---:|---:|---:|
| javagc / small | 0.000–2.778% | 0.000–2.778% | 0.000–2.778% |
| fastdownward / p01 | 0.571–0.582% | 0.000–0.582% | 0.000–0.571% |
| javagc / large | 0.000–0.484% | 0.000–0.208% | 0.000–0.484% |
| fastdownward / p10 | 0.000–26.181% | 0.000–32.505% | 0.000–32.505% |

In particular, p10's best-of-three result must not be reported as success of every
cheap optimizer. No arm reaches the recorded minimum in all five seeds. The shared-prefix
research ledger charges 40 aggregate acquisitions per case (10 prefix plus three
10-outcome continuations), while each individual arm uses 20. Selecting the best
arm after observing outcomes uses hindsight; the screen does not supply a reliable
pre-decision method selector. A failed conservative gate therefore does not rule
out selective gains over one fixed baseline, nor establish that an LLM can supply
them. All measured responses in this stage are classical.

![Physical records](../results/v59_workload_screen/physical_tables.png)

![Actual classical continuations](../results/v59_workload_screen/classical_headroom.png)

## Validation, interpretation and limits

Independent saved-evidence verifier checks 358 frozen inputs, approval/protocol binding,
576 raw trial receipts and schedule, 288 valid plans,
288 JVM invocations / 576 completed
harness iterations, retained actual Java output hashes, all 800 charged labels,
60 shared-prefix/budget traces and 720 reconstructed choices. It recomputes every
median/CV/threshold/headroom/case decision. This is verification of saved evidence,
not independent-machine reproduction of physical timings.

Java objective is the final timed harness iteration (warmup overhead charged as
collection cost). Planning objective includes process/translation/search/monitoring
wall time. Each objective is median of three repetitions. Resource penalties are
120000 ms Java / 60000 ms planning, explicitly scores rather than fabricated runtimes.
Raw wall/exit/status and failures remain available. Do not pool these raw objectives
across workloads or pretend repeated seeds/tasks are independent systems.

Only two families, two measured grid workloads each; selection follows V57 admission,
which itself used metadata-selected five workloads. The hardest planning task p20
lacks a completed reference under its cap. One host, limited repeats/one warmup,
no independent external VAL, limited STRIPS validator, and noisy recorded minima
constrain claims. Validity/cost equality is not an independently certified optimality
proof. RSS 2 GiB watchdog is sampled, not a hard macOS memory bound. Exit timestamps
avoid watchdog tick rounding; monitoring/OS load can still perturb timings. A gate
failure is not a statistical proof of equivalence or an upper bound beyond this grid.

## Cost and reproducibility

New actual research collection: 576 physical trials, including all repetitions,
failures, Java warmups and validation; 800 recorded aggregate accesses for four-workload
counterfactual replay. Reference-admission probes from V57 are prior additional cost.
Estimated one 20-outcome deployed arm needs 60 physical trials under this recipe,
conditional on a known utility contract; include separate admission/setup cost if
needed. No new model calls; local electricity/hardware and agent/user time costs
unknown. External experiment spend USD 0. Paid inference remains disabled.

Raw logs/plans/SAS/validation and complete case denominator:
results/v59_workload_physical/. Medians/repeats, prefixes, arms, acquisition journals,
CSV, figures and summaries: results/v59_workload_screen/. Exact runtime/task
provenance is inherited from the 358-input freeze; approval and verification in
artifacts/study_v59/. Sources/data-specific redistribution limits remain unchanged.
The immutable protocol title reflects its pre-approval state; approval_receipt.json
and STATUS record actual authorization/execution without rewriting frozen inputs.

Safe saved-evidence reproduction:

```sh
.venv/bin/python scripts/verify_workloads_v59.py
.venv/bin/python scripts/report_workloads_v59.py
.venv/bin/python -m pytest -q tests
```

Collector and primary analysis are one-shot: preserve outputs; do not delete to
rerun, silently extend caps or retune thresholds after outcomes. Detailed source
and experimental decisions remain in STATUS. No publication, push or contact.
