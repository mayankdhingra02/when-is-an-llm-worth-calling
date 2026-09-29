# V56 — fixed-budget classical screen on a validated planning task

Development-only adaptation, frozen before grid collection. V55's three observed
feasibility runs are excluded from the outcome table. They establish validity,
common cost104 and broad heuristic runtime variation. Thus this grid and cap are
informed by exposed feasibility outcomes, not a prospectively untouched test.
Same V55 pinned planner/build/task, no downloads, no LLM. No source changes.
One software family regardless of number of settings, plans or repeated seeds.

Full factorial48 distinct command configurations in stable product order:
heuristic[lmcut,hmax] × pruning[null,stubborn_sets_simple,stubborn_sets_ec,
atom_centric_stubborn_sets] × cache_estimates[true,false] ×
A* equal-f tie rule[low_h,low_g,FIFO]. The eager search queue always sorts first
by g+h, unsafe_pruning=false, reopen_closed=true, cost_type=normal, unlimited
cost bound. The heuristic is shared through --evaluator h=... . Source plugin
comments document admissibility/optimality-preserving pruning; deque buckets use
FIFO. This is implementation-configuration optimization on a fixed problem,
not a new planning algorithm. Settings can have equivalent behavior on this task;
we do not count48 independent algorithms. No unproved satisficing substitutions.

Run three new repetitions per setting,144 physical invocations. Roundwise shuffled
order Random(56000+round); no retries, outlier exclusion or post-outcome grid change.
Preserve every start, failure, completed plan, log and translated SAS task. Per-run
wall timeout10s, owner overall CPU timeout9s, sampled process-group RSS2GiB and
scratch256MiB, polling0.2s (sampled watchdog, not a hard allocation bound). Stage
1500s, one invocation at a time, no next run unless at least11s remain. All intended
and unattempted cases retained; incomplete stage forbids complete-table claims.
This bounded continuation remains below original30-minute per-run resource default;
prior historical ledgers are not reset or rewritten. Compilation/setup separately
reported. No model request/call-cap increase.

Objective: median of three penalized wall milliseconds, lower is better. Successful
trial requires exit0, finish within10s, exactly one plan, independent V55 validator
pass and computed/log/comment cost104. Wall includes process startup/translation,
search and monitoring wait; validation time is additional collection overhead.
Timeout/CPU/resource-exhausted trials receive fixed20000ms (PAR2-style penalty,
NOT measured runtime). Report failure counts and raw uncensored wall times alongside
penalized score. CPU limit is an additional safety cap, so failure is not always
10s wall censoring. Parse/configuration/internal errors or incorrect/unequal-cost
plans stop collection and prevent table admission; never hide them as poor timing.
Owner return codes20-24 are resource-exhaustion outcomes; other nonzero codes stop.
No successful plan is called cost-optimal on the basis of validator alone.

Offline choices follow V54's fixed rules, without tuning: seeds11,23,37,53,71,
four random initial settings then six greedy3NN acquisitions, shared saved prefix10;
random, greedy3NN and64-tree RF-LCB each add ten distinct acquisitions, inclusive
budget20. One-hot encoding of all four categorical dimensions (each mismatch
contributes equally); no ordinal invented heuristic ranking. Fixed distance mean
absolute difference,3NN tie by acquisition order, configuration score tie by lowest
ID. RF seeds seed*100+acquired_count; n_jobs1. Only own acquired labels are visible.
Feature-only grid never contains outcome extrema, failure labels or hindsight.
All200 aggregate-vector accesses are charged separately from144 physical runs.
An estimated deployed20-outcome arm requires60physical trials under this recipe;
research cost also includes other branches, full grid and V55 feasibility.

Only after all choices/arms are saved, full-table evaluator computes recorded
minimum and remaining headroom100*(arm_best-minimum)/arm_best. Gate: best-of-three
classical portfolio still has headroom at least max(5%,2*median CV percent among
settings with all3valid trials) in at least2/5seeds. Portfolio is hindsight and
non-deployable. If no all-valid setting, gate is undefined/failed. Censored settings
are excluded ONLY from noise estimate; retained in objectives and all comparisons.
Report gate, prefixes, all arms and complete144-denominator; never select a better
metric after outcomes. Offline120s cap. Recorded minima and three repeats can be
noise-optimistic; no significance/held-out/generalization claim from five seeds.
Gate failure retires this grid for positive LLM discovery; do not widen it or alter
workload until favorable. Pass merely warrants new independent-family design and
frozen real-model collection, not evidence of useful LLM escalation or Q2 readiness.
