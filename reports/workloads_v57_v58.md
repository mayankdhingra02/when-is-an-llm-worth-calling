# V57/V58 — broader workloads and a stronger order-sensitivity check

Two completed experiments, local only, 2026-09-25. **Four of five preselected
workloads passed admission.** A retrospective robustness study also found that poor
ten-evaluation prefixes can recover with cheap continuation: planning RF-LCB reaches
the best recorded result in100/100 ID-permuted cases. This is not new LLM evidence.

## Broader physical workload matrix (V57)

Selected Xalan's released non-default sizes and the first/lower-middle/last task
from the pinned20-task planning suite before new timings. All15 intended invocations
ran;12 valid,3 CPU-limit failures,0 dropped/unattempted/retried. Stage
181.211122s. Six JVM invocations include six warmups and six timed
iterations. Nine planner invocations, six independently valid plans. Same owner
versions/hardware as V53/V55, no new models/runtimes. All five workloads remain in
the denominator; they form TWO software families, not five independent systems.

| Family / workload | Valid | Reference / contrast / repeat wall seconds | Plan cost | Admitted |
|---|---:|---|---|---|
| javagc / small | 3/3 | 0.932 / 0.708 / 0.844 | — | Yes |
| fastdownward / p01 | 3/3 | 0.145 / 0.150 / 0.162 | 105 | Yes |
| javagc / large | 3/3 | 26.659 / 27.994 / 27.136 | — | Yes |
| fastdownward / p10 | 3/3 | 6.283 / 4.123 / 5.846 | 105 | Yes |
| fastdownward / p20 | 0/3 | 26.634 / 26.778 / 26.440 | — | No |

Xalan actual final outputs match precomputed reference hashes:2,390,100bytes small,
239,010,000bytes large. These reference hashes were derived before execution from
100 identical batches in the retained real V53 output; no generated stream is
reported as a measured result. First new actual output per size is retained; later
validated scratch is removed with hashes retained. Warmup gets owner validation,
not separate byte equality. Equivalence is to released implementation, not a formal
XSLT correctness proof. All new valid planning plans have independently recomputed
cost105 (not old p05's104). Validator remains a limited independent subset checker;
external VAL and an independent optimality certificate remain untested.

A lead worth replication: p10's hmax contrast completed in4.123s, versus two lmcut
references6.283/5.846s; old p05 had the opposite ordering. This is ONE contrast,
not a statistically established speedup, configuration optimum or LLM opportunity.
Xalan small also shows timing variation; no policy was selected from these15runs.
p20 timed out on all three attempts with owner exit23; its absence of a completed
reference prevents admission, not evidence that the task is unsolvable.

![Actual workload matrix](../results/v57_workload_matrix/workload_feasibility.png)

New timestamping uses a blocking process-exit waiter, independently of0.1s memory
watchdog polls. Both timings retained; it removes the old polling-interval rounding
but still includes process startup/monitor interference. Do not pool changed outer
wall timings with old protocols as if identical instruments. Memory cap is sampled
RSS2GiB, not a hard macOS allocation cap. Total scratch cap2GiB; per-JVM60s wall,
per-planner30s wall/27s CPU; stage750s. No cap increased during execution.

## Retrospective ID-order sensitivity (V58)

Used existing V54 Java/default and V56 planning/p05 tables, no physical reruns.
Twenty seeded ID permutations per family × five seeds =200dependent cases,
600 actual recorded-data arms,8,000 charged aggregate-vector acquisitions. Physical
initial four settings are held fixed under relabeling. Same encoders/3NN/RF-LCB
parameters; each arm uses20 inclusive outcomes from its shared10 prefix. No tuning.
Collection57.355308s, complete. Full-table scoring
runs only after choices are saved. This is exposed development data, not confirmation.

| Family | Worst prefix headroom | Prefixes crossing threshold | RF exact recorded minimum | Worst portfolio headroom | Permutations passing gate |
|---|---:|---:|---:|---:|---:|
| javagc | 1.346% | 0/100 | 26/100 | 0.845% | 0/20 |
| fastdownward | 63.487% | 5/100 | 100/100 | 0.000% | 0/20 |

**Qualification to V56:** the original ordering's nearly-optimal ten-label prefix
is not robust to arbitrary ID order. Five planning cases have poor prefixes, with
worst remaining headroom63.487%. Nevertheless, RF-LCB recovers the best recorded
planning result in all100 cases; no final classical arm crosses its5% opportunity
threshold. Java's largest final-arm headroom is1.263%, below its9.476% noise-aware
threshold. Both original final headroom decisions survive every tested permutation.
Thus poor current progress alone does not establish a need for an LLM; further
cheap search can recover. This observation is conditional on these finite tables,
these budgets/controls and the sampled orderings. It is not a general theorem.

![Saved-table order diagnostic](../results/v58_order_sensitivity/order_sensitivity.png)

All acquisition values map to source rows; shared prefixes/20budgets/8000charges
verified. Independent replay reconstructs7,200 recommendations from each own acquired
state, including RF fits. This costs replay compute, not new objective acquisition.
100cases are not100software systems; no population p-values or held-out learning claim.
The recorded minimum is noise-sensitive and not a certified physical optimum.

## Resources and next concrete experiment

Reference-wall extrapolation for48×3measurements on all four admitted workloads is
**81.6minutes**. This is an illustrative cost projection, not a bound:
two tested configurations cannot predict a full grid. It exceeds the current
30-minute default; the larger Xalan workload alone drives much of that estimate.
p20 remains explicitly unadmitted with a separate timeout-cap scenario in
capacity_estimates.json; it is not silently dropped to claim a representative suite.

A concrete, frozen V59 collector and offline screen are prepared for all four
admitted workloads:576physical invocations,60classical arms,800recorded acquisitions,
up to120minutes local collection, zero model calls/downloads/spending. Authorization
is FALSE and the guard was exercised before any workload process/output directory.
Approval must bind reports/protocol_v59_workload_screen.freeze.json and the exact
resource envelope; generic continuation is not treated as an increased runtime cap.
The collector may still stop incomplete at its cap. V59 has NOT run.

Completed costs:15new physical invocations;8000new recorded accesses;0LLM requests,
0new runtime/model downloads, USD0 new external spend. Source downloads:three pinned
PDDL files34,033bytes. Actual collection includes failures, repeats and warmups;
replay costs are separate. Electricity/agent/user time unknown. V57 admission probes
are real prior cost, not free initialization in a later20-outcome arm.

Primary data/source identities: artifacts/sources/v57/manifest.json and
artifacts/study_v57/workload_metadata.json. Runtime/source audit fromV53/V55 remains
applicable. New PDDL redistribution permission unresolved, sources local only.
V57freeze349inputs; V58freeze9inputs; V59 prepared freeze358inputs. Raw logs/results:
results/v57_workload_matrix/, results/v58_order_sensitivity/. Verification receipts:
artifacts/study_v57/, artifacts/study_v58/. STATUS contains resume instructions.

Safe commands (no application/model reruns):

```sh
.venv/bin/python scripts/verify_workload_matrix_v57.py
.venv/bin/python scripts/verify_order_choices_v58.py
.venv/bin/python scripts/report_workloads_v57_v58.py
.venv/bin/python -m pytest -q tests
```

The primary collectors/analyzer are one-shot. These results improve measurement and
robustness evidence, but do not establish useful LLM routing, enough independent
families, novelty or Q2 readiness. No publication, push, cloud resource or author
contact occurred. Next action is approval of the bounded V59 local runtime extension.
