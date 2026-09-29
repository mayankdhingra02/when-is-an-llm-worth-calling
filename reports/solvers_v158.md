# V158: two new solver engines, native feasibility result

Executed40/40 charged probes in47.095s, no LLM calls. Fixed cvc5 N=10 / CP-SAT N=48, four settings/engine, five repeats. Every returned assignment is independently checked by an O(N²) pairwise validator. No objective value was inferred or mocked.

| Engine / candidate | Correct / intended | Median valid solve (s) | Relative MAD | Admission cell |
|---|---:|---:|---:|---|
| cvc5 / 0 | 5/5 | 0.041803 | 0.221% | pass |
| cvc5 / 21 | 5/5 | 0.031309 | 0.278% | pass |
| cvc5 / 42 | 5/5 | 2.324668 | 0.381% | pass |
| cvc5 / 63 | 5/5 | 1.485518 | 0.720% | pass |
| ortools / 0 | 5/5 | 0.025134 | 0.255% | pass |
| ortools / 21 | 5/5 | 0.012694 | 1.152% | pass |
| ortools / 42 | 5/5 | 3.835041 | 0.346% | pass |
| ortools / 63 | 5/5 | 0.171515 | 0.112% | pass |

Admission requires all20valid results/engine and every cell median>=10ms/relativeMAD<=5%. This gate and a prospective10%paired practical margin were frozen before measurements. It is distinct from the earlier1%study; no claim about1%effects follows. Timeouts have missing successful-runtime values, not a measured10second solution. All intended probes remain in the denominator.

Admitted engines: cvc5, ortools. No paired stage may proceed for an inadmissible engine under this protocol.

Total subprocess collection time47.067s; total observed solve time39.667s. Import/model construction and validation are separately logged. This is actual feasibility-collection cost, not estimated B20deployment cost. Per-probe native process exits are saved; no server/background inference used.

The two implementations share a mathematical benchmark/domain, and Z3 was historically exposed in the repository. Neither engine is a new industrial application. Configuration variants/repeats cannot be counted as independent systems; feasibility now exposes bothfamilies for subsequent workload selection. Runtime feasibility does not establish useful LLM escalation, router generalization or journal readiness. External-host reproducibility and upstream full regressions remain untested.

Evidence: results/v158_solvers/{001..040}.json,intents.jsonl,completion.json,summary.json,feasibility.png/svg; artifacts/study_v158/freeze.json,jobs.json. Raw solver text and exact solution vectors retained. Safe regeneration: `.venv/bin/python scripts/solver_feasibility_v158.py summarize`; `MPLCONFIGDIR=/tmp/mpl-v158 .venv/bin/python scripts/report_solvers_v158.py`. Collect is create-once; do not rerun it.
