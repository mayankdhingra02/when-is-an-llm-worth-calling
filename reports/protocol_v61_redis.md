# V61 — a deployable classical comparator on fresh Redis workloads

Prospective development screen; freeze before inspecting V60 timing values or
new grid outcomes. V60 established six valid executions only. Source, fixed
workloads, output checks, bounded server settings and warmup/client parameters
remain the V60 contract. Redis is ONE development family. Neither workload is a
held-out independent group; MongoDB/Storm reservations remain unchanged.

Primary comparator: RF-LCB, fixed 64 trees, min_samples_leaf1, max_features1,
bootstrap true, one job, seed=100*run_seed+acquired_count; score mean minus one
tree standard deviation. Random and 3NN continuations are controls, never a
post-outcome choice of the primary method. All arms share 4 random +6 greedy3NN
prefix outcomes, checkpoint10, and finish at20 inclusive. Seeds11,23,37,53,71.
The prefix matches V59's rule. Two workloads ×5 seeds ×3 continuations =30arms;
10prefix plus30 continuation labels per case =400 charged recorded acquisitions.
Only acquired labels and declared-domain features enter selection. Full-table
evaluation after ALL decisions. Grid-known scaling, no hidden-label normalization.

Grid chosen from owner option semantics and defaults, without new timing selection:
hash-max-listpack-entries[64,512], hash-max-listpack-value[32,64],
(io-threads,io-threads-do-reads)[(1,no),(2,no),(2,yes),(4,no),(4,yes)], hz[10,100],
activerehashing[no,yes]. Thus80 unique parameter settings; exclude reads=yes with
one IO thread because owner comments say that thread mode uses only the main thread.
Configurations can still be behaviorally equivalent on a particular workload;
do not present80 as80 distinct execution mechanisms. Two fields f000/f127; all
other semantics and loaded data fixed. All three repetitions per setting collected.
480 physical trials. Per round, field0 then127, configurations shuffled by
Random(61000+1000*round+field_index). No resampling or retries.

900-second physical cap, under the pilot's30-minute per-experiment default; one
workload at a time. No launch after855s. 40-second whole-trial cap, 15-second
benchmark-phase cap, sampled process-group RSS1GiB and Redis maxmemory256MiB.
Stop on invalid output/unexpected failure; preserve all480 intended rows, including
unattempted. Genuine resource failure scores80000ms, explicitly a penalty rather
than measured runtime. Incomplete table cannot enter full analysis. No cap extension.
180-second offline screen cap. Zero new model requests, dollars or downloads.

Objective: median of3 measured benchmark-process exit-wall milliseconds, including
client startup and per-reply checks. Unlike V60's feasibility receipt, V61 uses
a dedicated process waiter: Python's timeout wait can quantize very short process
times. This code-audit change was made before examining timing values. Do not pool
V60 and V61 wall metrics. Child inherits its worker process group, ensuring the
outer watchdog also kills server/client on timeout. Raw owner CSV remains separate.

Exploratory opportunity gate now compares the actual RF-LCB arm to the recorded
grid minimum: headroom=(RF_loss-minimum)/RF_loss. Threshold=max(5%,2*medianCV%)
among settings with three valid repetitions. Require >=2/5 seeds per workload.
No fully valid setting makes the threshold undefined, not zero. Portfolio minimum
is separately labeled hindsight, never the gate. This new primary question does
not reverse or retune V59's historical portfolio decision. Report all controls,
failures and per-workload outcomes; no pooling raw losses or independent-seed tests.

A passing gate permits preparation, not an implicit authorization or claim, of a
real paired-model study. A failed gate stops model collection on this grid. Never
change thresholds, query field, client concurrency, payload or settings after seeing
results to obtain a positive score. Further workload/family designs must be separately
justified. This stage cannot validate a learned cross-system router or Q2 readiness.
