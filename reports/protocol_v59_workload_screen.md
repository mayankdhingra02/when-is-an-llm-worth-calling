# V59 — prepared expanded classical screen (NOT authorized or executed)

New requested resource envelope:576 physical invocations, up to7200s local
collection, no model requests/downloads/cloud/external spending. This exceeds
configs/pilot.yaml's30-minute default and needs explicit user approval; the
collector refuses to start while configs/authorization_v59.json is false. Approval
must bind this freeze's SHA256 and exact envelope. Do not infer it from generic
continuation or old approvals predating this concrete request.

Include ALL four V57-admitted workloads: Java/Xalan small and large, planning p01
and p10. Retain p20 as an explicitly reported failed admission (0/3, CPU timeout),
not evidence that LLM escalation cannot help it. These are two development families;
all variants/seeds remain grouped. The original V54/V56 workloads stay retired;
new variants are not independent systems or held-out samples. Selection is based
on the entire prespecified V57 admission matrix, not a favorable speedup.

Use unchanged V54 Java48-setting grid: GCthreads[1,2,4,8] ×NewRatio[1,2,4,8]
×SurvivorRatio[2,4,8]; original heap512MiB,ParallelGC/adaptiveOFF,1worker,n2 with
warmup+final. Use unchanged V56 planning48 commands: heuristic2 ×pruning4 ×cache2
×tie3, optimal-search assumptions unchanged. Same pinned owner runtimes/sources.
Three fresh repetitions per setting/task:4*48*3=576. Workload order per round
[small,p01,large,p10]; settings shuffled by Random(59000+round*10+workload_index).
No retries, outcome-driven grid changes or post-hoc exclusion. Preserve all intended,
failed, completed and unattempted cases. Incomplete collection cannot be analyzed as
complete; do not extend caps or silently launch a second collector to finish it.

Use V57 precise exit waiter and sampled process-group RSS2GiB/scratch2GiB monitor.
Java60s wall cap; planner30s wall and27s CPU cap. No new run when stage time remaining
is less than wallcap+5s. Kill whole group on breach. Watchdog/configuration/internal
errors or invalid output stop collection, remaining cases unattempted. Genuine
resource failures remain objective penalties, not successful results. All returned
plans require independent validator cost105, owner log/comment agreement. Java
requires owner validation and exact V57 precomputed repeated-reference output hash;
retain first actual validated output per size and all failure outputs, delete later
scratch only after verification/receipt. Keep planner plans/SAS/logs.

Objective by workload: median of3 final Java harness milliseconds; timeout/RSS/scratch
penalty120000ms. Planning median of3 exit-based whole-process wall milliseconds;
CPU/time/RSS/scratch failure penalty60000ms. Penalties are declared PAR2-style scores,
NOT measured runtimes. Raw timings/failures kept. Different workload/objective units
are not pooled into raw means. Actual collection includes all warmups, repetitions,
source-admission probes and validation overhead. A20-outcome deployment per task
would use60 physical invocations under this recipe, conditional on utility contract;
admission/calibration is additional, not free evaluations.

After completed table admission, offline screen for each workload: five seeds
[11,23,37,53,71],4random +6greedy3NN shared prefix10, then random/3NN/RF-LCB
continuations10 each. Same fixed feature encoders/model hyperparameters as V54/V56,
no tuning;20inclusive per arm,60arms,800charged aggregate accesses total. Hidden
values held in per-case oracle, full-table scoring after saved choices only.
Offline180s cap. For each workload, report all cases/failures and headroom to best
recorded median. Gate uses same fixed max(5%,2*medianCV% of all-three-valid settings)
and >=2/5seeds remaining opportunity against hindsight best-of-three portfolio.
No fully valid setting => undefined/no admission, not synthetic zero runtime.
No claim of noise-free optimum, LLM benefit, trained router or generalization.

V57 reference-wall projection for one48×3grid per workload suggests about80minutes
for all four, not a runtime guarantee: only two settings were measured, and the
instrumentation/other configurations may change cost. The proposed120-minute cap
has finite headroom and still may stop incomplete. Any later LLM study requires its
own frozen design, independent groups and explicit request allowance; this envelope
authorizes ZERO inference. No sending/publishing/pushing is requested.
