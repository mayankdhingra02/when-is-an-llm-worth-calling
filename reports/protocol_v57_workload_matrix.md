# V57 — outcome-blind workload expansion and bounded feasibility

Freeze before any new workload execution. Development-only, two software families,
not five independent systems. This is workload admission/measurement feasibility,
not a20-evaluation optimizer/router experiment. Do not substitute mock outcomes.
V54/V56 failed grids remain retired; no grid widening, prompt change or inference.

Selection uses only already pinned owner metadata: DaCapo9.12-MR1 Xalan's two
non-default released sizes small10 and large1000 (each repeats17XML transforms),
and tasks p01,p10,p20 (first/lower-middle/last in ordered20-task suite) in
owner aibasel/downward-benchmarks commit e21d49c2cb61d147a46c5966f2581bf6fd422b9f,
data-network-opt18-strips. All selected workloads retained even if they fail.
Task numbers are not assumed monotonic difficulty. Metadata and schemas inspected
before timing; p01 tiny network, p10 small network, p20 ring network. No other tasks
will replace them based on outcomes. Prospective MongoDB/Redis/Storm reservations
unchanged. More workloads do not create more software-system groups.

Pinned Java/runtime/planner/task domain are unchanged from V53/V55. Sources,
compiler binary and relevant code bound by input hashes; downloads <=1MiB for this
stage inside original persistent5GiB allowance. No new package/model/runtime install,
paid API, cloud usage or model requests. Benchmark licenses retain prior limitations;
new PDDL data-specific redistribution permission unresolved, keep sources local.

Exactly15 intended invocations:3 rounds × fixed workload order
[java-small, planning-p01, java-large, planning-p10, planning-p20].
Java GC settings by round[(1,2,8),(4,4,4),(1,2,8)] for
(ParallelGCThreads,NewRatio,SurvivorRatio), fixed512MiB heap, ParallelGC/adaptive OFF,
one application worker, two harness iterations (warmup + measured). Same source
input/workload within each size. Per-JVM60s wall cap. Every invocation/iteration
counts, including reliability repeats and failures; no claims that this admission
work is free initialization inside a later20-outcome deployment budget.

Planning settings by round[astar(lmcut()),astar(hmax()),astar(lmcut())], actual
costs/no transformation, unchanged admissible-search assumptions from V55. Per-run
30s wall, owner27s CPU cap. Independent V55 subset validator checks all actions,
goals and exact cost, which must equal log/plan comment. Cost is initially unknown
for new tasks; compare all successful plans within each task after collection.
A different plan length is allowed at equal total cost. Validity is not a separate
optimality proof. Never use a higher-timeout rescue or a new heuristic after failure.

Wall timestamps: a dedicated p.wait() thread stamps exit; watchdog polling0.1s
no longer quantizes completion to its next tick. Record both exit-based elapsed
and monitor-return elapsed. The watchdog still consumes CPU; no claim of unperturbed
or cycle-accurate timings. This instrumentation change is an adaptation and not
numerically pooled with V53/V55 outer-wall measurements. Java harness final/warmup
milliseconds also retained. Tests use explicitly synthetic short child processes.

One real workload process group at a time; sampled process-group RSS2GiB (no hard
macOS RLIMIT_AS guarantee). Scratch total2GiB. Stage750s; do not launch if remaining
stage time < per-run wall cap +5s. Whole group killed on wall/resource limit;
watchdog errors abort remaining work, counted as unattempted. No indefinite service.
Continue other selected workloads after timeout/correctness failure; no retry.
If a completed plan is invalid or costs disagree, that workload is not admitted.
All15 intended cases remain in final output. Preserve failed outputs and logs.

Xalan validation: released owner checks plus byte-count/hash equality to a
pre-execution expected stream derived from the retained V53 actual output. Verify
that V53's100 batches are byte-identical, use its239010-byte batch repeated10 or1000.
Expected2,390,100 or239,010,000bytes, hashes bound in workload_metadata.json. These
are reference hashes, NOT fabricated measured outputs; actual new files must match.
This verifies equivalence to the released implementation, not formal XSLT conformance.
Preserve first actual validated output per new size; delete later successfully
verified scratch only after recording hash/size. Final output checked; warmup
gets owner validation only, matching earlier limitations.

Admission pass for each workload requires all3 intended trials successful, fixed
utility equality and successful two reference repeats. Partial/time-limited cases
reported separately, not counted as passes. Summarize actual time/memory/output,
validity/failure counts and repeated-reference variability descriptively. Contrast
only has one observation: no credible speedup or headroom claim from this assay.
A repeated successful configuration is not a noise distribution from two samples.

No after-the-fact subset selection or optimization-grid claim. Full48×3 screen
resource estimates may use the measured repeat-reference wall time, clearly labeled
illustrative (two settings cannot predict entire grid; no bound/guarantee). Report
sum across all5 selected workloads, including failure cases/cap scenarios, rather
than silently retaining only cheap successful ones. This stage does not establish
LLM usefulness, generalization or journal readiness. A separate frozen screen and
explicit cap check are prerequisites for further collection; model limits unchanged.
