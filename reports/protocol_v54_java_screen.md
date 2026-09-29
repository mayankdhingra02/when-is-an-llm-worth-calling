# V54 — fixed-budget classical screen on fresh Java/Xalan measurements

Freeze before collection. V53 established feasibility; its three timings are exposed
development diagnostics and are excluded from this new outcome table. This is one
software family, no held-out claim. No model inference or paid services.

Use the exact pinned V53 runtime, jar, default Xalan workload, single application
thread, 512MiB fixed heap, ParallelGC and disabled adaptive size policy. Default
owner validation plus final output equality to V53's retained 23,901,000-byte
reference (SHA2564c72b92f00eca08f8bda35e2734124f92fbfd01884c3bf259f2f5d005e98bddb).
Do not vary workload, heap, input/output fidelity or validation settings.

Full factorial grid, lexicographic configuration IDs, fixed before timings:
ParallelGCThreads in[1,2,4,8], NewRatio in[1,2,4,8], SurvivorRatio in[2,4,8].
48 configurations, three fresh-JVM repetitions each,144 invocations. Each has one
warmup and one measured iteration. Roundwise random order, Python Random(54000+r).
No retries/outlier removal. Record every intended/started/failed/unattempted trial.
Each final output must match the retained reference, owner validation pass and
exit0. Stop on first failure; no incomplete table analysis. Retain raw logs and
hash/size receipts, remove only verified trial scratch. Source V53 retains canonical
output. Fixed two-iteration JVM scheme does not establish steady-state convergence.

Caps:1200s physical collection,60s/JVM,2GiB scratch, one JVM at a time;120s offline
screen. No new downloads. Abort before launching if less than60s stage budget
remains. Three repetitions are physical collection cost, not free validation.

Objective: median of three measured whole-Xalan iteration times in milliseconds,
minimize. Startup, input extraction, warmup, validation and wrapper time recorded
separately as real collection overhead. These are not GC-only times. Every timed
iteration includes the workload's output writing. Source vectors and all repeats
remain available; uncertainty/noise is not erased by the median.

Offline experiment: seeds11,23,37,53,71. Each shared prefix has four seed-random
configurations followed by six acquired-only nearest-neighbor choices. Branch into
random, greedy3NN and random-forest lower-confidence-bound continuations, each
with ten additional distinct acquisitions. Total20 per branch, checkpoint10.
Physical table collection144 trials is separate from200 recorded median-vector
accesses (5*(10+3*10)); deploying one arm would acquire20 aggregate outcomes,
requiring60 timed repetitions under this measurement scheme plus warmups.

Feature encoding is log2 of the three positive power-of-two parameters, scaled
by their known grid ranges. 3NN uses mean acquired times of three nearest points
under mean absolute feature distance. RF uses64 bootstrap regression trees,
min_samples_leaf1, all features, n_jobs1, seed=seed*100+acquired_count; minimize
mean minus one tree-prediction standard deviation. Uncertainty is heuristic.
Ties choose lowest stable ID; no duplicate evaluations. Fixed parameters, no tuning.
RF is a meaningful additional classical comparator, not a claim of the strongest
possible classical method. Optimizers receive only feature matrix and own labels.

Full-table evaluator runs only after all choices are saved. Report best observed
runtime per arm, fractional improvements, per-case checkpoint and final headroom,
paired outcomes versus random, all48 median/dispersion records, and seed-level
denominators. Hindsight remaining headroom uses the best result of all three
classical branches (conservative, non-deployable baseline portfolio reference).
Define percentage headroom100*(classical_best-table_min)/classical_best. Candidate
gate requires headroom at least max(5%, twice the median per-configuration coefficient
of variation expressed in percent) in at least2/5seeds. This is a development
screen, not evidence an LLM can realize that headroom. Full-table minima suffer
selection optimism; three repeats and five seeds cannot establish generalization.
Do not widen the grid/change workload/prompt to rescue a failed gate. Even a pass
requires additional independent families and a new frozen paired LLM protocol.

Use pinned project Python3.10.13/numpy2.2.6/scikit-learn1.6.1. Prefixes, event
ledgers, source/table hashes, parser tests, independent verification, figures,
report and STATUS are required. No hypothesis-driven exclusion of runs or seeds.
