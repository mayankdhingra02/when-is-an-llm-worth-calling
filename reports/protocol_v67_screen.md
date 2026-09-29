# V67 — three-system classical opportunity screen

All three V66 candidates passed their fixed correctness admission (9/9 trials).
Use all three, their unchanged generated inputs and the48-setting domains frozen
before V66 timings. Do not select workloads/configurations using admission timing
advantages. No task-size adjustment, utility relaxation, model call or router fit.
DuckDB, GNU sort and OpenJPEG are three development system groups, not a held-out
test set. Group each implementation's variants and seeds; shared use of libc does
not by itself make these distinct applications one software family.

Collect3fresh repetitions of all48settings per system,432configuration trials.
Order: repetition0..2, then duckdb/gnu_sort/openjpeg; shuffle settings with
Random(67000+1000*repetition+family_index). Unchanged V66 worker and correctness
checks. Three OpenJPEG validations per setting add144decoder invocations as
actual collection overhead:576application invocations planned, plus supervisors.
Objective remains first materialized query time for DuckDB and whole-process
exit time for sort/encoder. These different tasks are compared within systems;
raw milliseconds are not pooled across applications as interchangeable quantities.

Per trial45s outer wall, sampled1GiB group RSS, native child20s. Total1800s;
no launch with less than50s left. All intended cases retained. CPU/wall/RSS/OOM
noncompletion receives a declared90000ms penalty (not measured runtime). Wrong
answers or unexpected failures stop the stage. Incomplete tables are not analyzed.
No retries, concurrent trials, background continuation or automatic cap extension.
Do not weaken admission or rerun after inspecting a failed/negative outcome.

Offline screen cap180s,45arms and600charged recorded acquisitions. Seeds11/23/37/53/71,
shared4random+6greedy3NN prefixes of10, random/3NN/RF-LCB continuations to20 inclusive.
RF-LCB is the primary comparator before full-grid outcomes;64trees, mean-minus-tree
standard deviation, deterministic seed100*seed+acquired_count as inV64. Numeric
features use only declared-domain scales, no hidden-score normalization. Each
family owns a distinct acquisition ledger capped200. Full-table scoring only
after every decision. Medians of three penalized values form the recorded table.

Screen gate unchanged: RF remaining headroom to recorded minimum at least
max(5%,2*median CV percentage among settings with3valid trials) for>=2/5 seeds.
Undefined thresholds cannot pass. This is descriptive admission, not statistical
significance or proof of LLM benefit. Random and3NN controls remain reported even
if they outperform RF. Portfolio is labeled hindsight and cannot replace primary.

Passing a group only permits preparation of a separately bounded real-model assay
using the new legal interface, ALL five prefixes, frozen messages and strong matched
controls. It does not authorize any model request. Failed groups receive none.
No model/threshold/parameter tuning on failed grids. Collection cost remains actual,
including validation; a deployment20-outcome median-of-three arm entails60configuration
trials plus associated validation, not the free reuse of a measured full table.
Zero new downloads/spending/inference are included in this stage.
