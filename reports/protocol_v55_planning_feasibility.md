# V55 — Fast Downward correctness and feasibility (development only)

Freeze before any planner invocation on the task. This is a fresh adaptation,
not replication of the historical performance-evolution table. One family/task;
no independent test set, LLM request, controller fit or positive-result guarantee.

Planner owner aibasel/downward release-24.06.1, commit
1eef26b2cbf599a1894606aa898d9d49e1034cb9, GPL-3.0-or-later; release/no LP build,
Apple Clang17 with installed MacOSX15.5 SDK, two compile workers. First configure
failed because default SDK27 was incompatible with the selected linker. Preserve
failure and corrected local build receipts. No global environment/settings change.
Build/setup is separate from physical collection. Downloads cap64MiB inside the
existing persistent5GiB allowance; no model download. Stable24.06.1 is deliberate,
not the latest release. All executable source/binary inputs sealed below.

Pinned task aibasel/downward-benchmarks commit
e21d49c2cb61d147a46c5966f2581bf6fd422b9f,
data-network-opt18-strips/domain.pddl and p05.pddl. Problem name
p9-3-15-tiny-network-4. Owner collection calls itself unofficial; exact equivalence
to old paper workload bytes is unverified. Data authors in domain: Manuel Heusner,
Florian Pommerening, Alvaro Torralba. Standalone dataset redistribution license
unresolved; keep payloads out of shareable Git history.

Historical data has table-only disjunctiveLMs, no usable command mapping in its
feature-model outputString fields, and does not establish plan validity/equal
plan cost. Its timings remain unadmitted and are not read in this stage.

Three intended fresh processes in fixed order: astar(lmcut()), astar(hmax()),
astar(lmcut()). Same full task, actual action costs, default deterministic order,
no cost transformation, no heuristic caching changes, no warmup omitted from cost.
Source documents lmcut admissible and hmax admissible without axioms; A* reopens
closed nodes. Inspected task subset has no axioms/conditional effects. Completion
under these assumptions should be optimal; independent plan validation establishes
only validity and exact cost, not an independently certified optimality bound.

Each invocation includes translation and search. Wall cap45s per invocation,
CPU cap40s through owner driver, stage150s, one process group at a time. Aggregate
process-group RSS watchdog2GiB, polling0.2s; macOS lacks RLIMIT_AS support, so this
is sampled termination, NOT an instantaneous hard allocation cap. Scratch cap
256MiB polled with RSS. Kill whole group on limits; record observed maxima,
exit status, wall seconds, full logs and any partial plans. No retries; run all
three cases even if one times out, unless stage/resource monitoring fails. All
intended/unattempted cases retained. Preflight ps permission before creating run
output or invoking planner. Watchdog runtime is measurement overhead and can perturb
runtime. No timing-speedup conclusion from three trials.

Independent project validator interprets flat typed STRIPS actions with conjunction,
negative preconditions, add/delete effects and nonnegative static action costs.
It rejects unsupported actual expressions before execution, validates typed ground
actions and every precondition, recomputes cost, and checks all goals. It does not
use the planner-reported cost to derive its answer. Owner BUILD.md flags a VAL bug
for IPC18 data-network; modern VAL is not silently trusted. The project validator
is limited/newly tested, not a replacement for a mature general PDDL validator.
Require exit0, exactly one complete sas_plan, independent validity, and agreement
between recomputed cost, plan comment and planner log. All three costs must equal.
Failure prevents grid admission. Retain all plan bytes, translated tasks and logs.

Pass means this exact workload supports correctness-checked measurement, NOT
that a20-evaluation grid exists or has optimization/LLM headroom. If passed, inspect
source-defined independent configuration choices and freeze a separate grid before
new trials. A failed feasibility task is not replaced with an easier task in V55.
Each physical invocation, including repeats/timeouts, counts as research collection;
no offline objective-table acquisition or deployment-arm claim at this stage.
The preflight performs no workload execution; synthetic fixtures stay in tests.
