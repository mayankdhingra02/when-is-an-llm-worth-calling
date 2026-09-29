# V157: two new solver engines, native feasibility result

Executed40/40 charged probes in224.952s, no LLM calls. Fixed N=32, four settings/engine, five repeats. Every returned assignment is independently checked by an O(N²) pairwise validator. No objective value was inferred or mocked.

| Engine / candidate | Correct / intended | Median valid solve (s) | Relative MAD | Admission cell |
|---|---:|---:|---:|---|
| cvc5 / 0 | 0/5 | unknown | unknown | fail |
| cvc5 / 21 | 0/5 | unknown | unknown | fail |
| cvc5 / 42 | 0/5 | unknown | unknown | fail |
| cvc5 / 63 | 0/5 | unknown | unknown | fail |
| ortools / 0 | 5/5 | 0.012481 | 1.117% | pass |
| ortools / 21 | 5/5 | 0.006993 | 0.450% | fail |
| ortools / 42 | 5/5 | 0.471525 | 1.323% | pass |
| ortools / 63 | 5/5 | 0.121367 | 0.408% | pass |

Admission requires all20valid results/engine and every cell median>=10ms/relativeMAD<=5%. This gate and a prospective10%paired practical margin were frozen before measurements. It is distinct from the earlier1%study; no claim about1%effects follows. Timeouts have missing successful-runtime values, not a measured10second solution. All intended probes remain in the denominator.

Admitted engines: none. No paired stage may proceed for an inadmissible engine under this protocol.

Total subprocess collection time224.926s; total observed solve time203.088s. Import/model construction and validation are separately logged. This is actual feasibility-collection cost, not estimated B20deployment cost. Per-probe native process exits are saved; no server/background inference used.

The two implementations share a mathematical benchmark/domain, and Z3 was historically exposed in the repository. Neither engine is a new industrial application. Configuration variants/repeats cannot be counted as independent systems; feasibility now exposes bothfamilies for subsequent workload selection. Runtime feasibility does not establish useful LLM escalation, router generalization or journal readiness. External-host reproducibility and upstream full regressions remain untested.

Evidence: results/v157_solvers/{001..040}.json,intents.jsonl,completion.json,summary.json,feasibility.png/svg; artifacts/study_v157/freeze.json,jobs.json. Raw solver text and exact solution vectors retained. Safe regeneration: `.venv/bin/python scripts/solver_feasibility_v157.py summarize`; `MPLCONFIGDIR=/tmp/mpl-v157 .venv/bin/python scripts/report_solvers_v157.py`. Collect is create-once; do not rerun it.
