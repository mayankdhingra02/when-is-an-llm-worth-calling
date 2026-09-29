# V6: bounded expanded exploratory smoke

Frozen before any v6 optimization outcomes or new model responses. This is an explicit adaptation, not SNAP2 replication and not the larger 20-group study. The v4/v5 snapshots remain unchanged.

## Admission and allocation

The pinned PerformanceEvolution_Website owner case READMEs explicitly define `performance` as runtime for Brotli, HSQLDB, MySQL, PostgreSQL, VP8, lrzip, and throughput for OpenVPN. Use one target only; all other objective cells remain excluded. See data/manifest_v6.json for source commits, payload/README/feature-model hashes, workload caveats, selected revisions and family aliases. Raw source data stay Git ignored; no upstream algorithm code is executed or reused.

Retain the v5 outcome-blind lexicographically first revision rule (not chronological order). MySQL represents the shared MariaDB family because MariaDB has contradictory crash-gap metadata. VP8 v0.9.1 predates the documented >=v1.4.0 option alias. Seven families are semantically admitted as local offline single-target adaptations; six are selected by ascending SHA256(`v6-bounded:` + family), with the first three development and next three test. OpenVPN is unused. Variants/versions/seeds follow the family allocation. Previous Apache HTTP Server, SQLite and x264 families remain excluded. Opus/z3 target meanings remain unresolved; other registry candidates remain unadmitted, with reasons recorded in the manifest.

Selected development: MySQL 5.6.10, lrzip 530, Brotli 0.3.0. Selected held-out: VP8 v0.9.1, HSQLDB 2.1.0, PostgreSQL 10.0. All five seeds [11,23,37,53,71] stay in each family. All selected feature tables happen to be binary. A mixed-domain synthetic gate tests the broader interface but cannot establish empirical nonbinary performance.

## Treatments and budgets

Use the tested modal-centroid nominal adaptation for an acquired-only 10-evaluation prefix and another 10-evaluation classical continuation. Stable modal ties choose the smallest feature value; feature-space Hamming geometry and shuffled seed order resolve projection ties. Retain the first source row per duplicate feature vector without inspecting duplicate outcomes. Each saved prefix is hashed, including order and acquired labels; each branch clones it independently.

Each case also runs random search from start for 20 labels and a uniform-domain projection continuation for 10 additional labels from the same prefix, with RNG seed = experiment seed + 40000. Each completed case costs 10 prefix + 10 classical + 20 random + 10 projection + 10 LLM = 60 actual acquisition accesses. Branch logical budget is 20, including the prefix. Full 30-case collection costs 1,800 acquisitions. Offline source-table access is not live software execution or the original authors' measurement cost.

Target cells are parsed lazily only when requested by the oracle. Each request is durably journaled, including failed nonnumeric/nonfinite/nonpositive target acquisitions; a duplicate acquisition is rejected. Full-table normalization belongs only to retrospective evaluation: one-target loss in [0,1], lower better, zero for constant targets. Search, features and prompts use acquired-only normalization. For runtime the target is minimized; throughput is maximized. This ignores other tradeoffs such as output size/quality; the result is a single-target adaptation.

## Local LLM and reliability

Pinned Qwen/Qwen2.5-0.5B-Instruct revision 7ae557604adf67be50417f59c2c2f167def9a775, same verified local weights and locked dependencies. Greedy decoding, no effective sampling seed; numerical reproducibility can depend on device. New finite-symbol grammar uses sorted finite domains and alphabet `0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz`, one symbol per feature. Every nonconstant setting is selected using real model logits. Only syntax and domain membership are constrained. Preserve full prompts, raw responses, token IDs, choice positions, grammar hashes, request times, request IDs, cache keys and observable tokens.

One real request produces ten proposal rows per continuation, with no intermediate-label feedback inside that batch. This deliberately changes the previous two batches of five to fit existing resource limits. Project each proposal sequentially to the closest unevaluated candidate. Count projection/duplicates/collisions and retain incumbent. Malformed/error responses trigger explicitly labeled classical fallback if time remains, never fabricated LLM output. No retries; a dead worker/limit stops subsequent requests and preserves intended-run denominators.

Before measured calls, two real synthetic format gates test 4 ternary features and 30 binary features. Their objectives and inference records are in a separate synthetic namespace. Both must parse. No quality tuning or repeated gate attempts. Thirty measured calls plus two gates = 32 new attempts, within the existing 34 remaining. Never reset/increase the 100-attempt follow-up ledger shared since v2. The cumulative 1,800-second runtime cap has approximately 642.7 seconds left before this version. It includes this version's collection, loading, controller fitting and analysis. A complete run is not guaranteed to fit; requests time out at min(60 seconds, remaining time), workers terminate, and blocked cases remain in the denominator. No paid/cloud endpoint.

## Controller and analysis

Complete development classical work first, then gates and all development LLM pairs. Fit and hash-seal controllers before acquiring any held-out target. Features are acquired-only progress, plateau, modal separation, 20-bootstrap recommendation disagreement plus candidate count, variables, objective count, nominal fraction and remaining budget. Bootstrap uses acquired outcomes only. Numeric-looking levels are treated nominally; all selected empirical cases are binary.

Use the existing fixed Ridge(alpha=1) gain router, development-group weighted scaler and leave-one-development-system-out scores. Threshold grid is [-.02,0,.02,.05,infinity], selected for smallest escalation rate whose development group-mean loss is within .02 of always-escalate, with predefined loss/rate ties. Uncertainty-only thresholds are development quantiles [0,.25,.5,.75,1,infinity] under the same criterion. No held-out refitting. Save fit/threshold evidence before first test acquisition.

Report never, always, benefit, uncertainty, Bernoulli random at benefit's development-selected rate (seed 20260924), and an explicitly retrospective random diagnostic matching the held-out realized benefit count without using outcomes (same RNG seed). Hindsight oracle chooses the better observed branch after seeing both; non-deployable. Material help/harm uses loss margin .02. All summaries first average seeds within each system, then systems. Show per-system and per-seed distributions; no significance/generalization claims from three test families. Plot the frozen threshold grid descriptively; never choose a new operating threshold from it.

Actual collection includes gates and both branches. Estimated deployment costs include a 10-label prefix and only one 10-label continuation, one request if escalating, and the chosen branch's recorded tokens/time; future observed usage is evaluation accounting, not a routing input. Loading and development training costs are separate. No cloud-dollar extrapolation. External spend remains zero.

## Integrity and failure rules

Each acquisition is journaled; started transactions cannot silently rerun after interruption. Completed per-case files can be reused without reacquisition if hashes match. Interrupted transactions fail closed for manual journal audit, rather than silently replaying calls/labels. Saving prefixes/checkpoints does not claim arbitrary crash recovery is implemented. Persist an intended 30-case denominator and explicit blocked/fallback statuses. Preserve frozen source snapshots and old version results. If collection is incomplete, show counts and partial data, but do not fit/report policy comparisons from an outcome-selected subset.
