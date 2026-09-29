# V64 — prepared SAT configuration screen, resource extension required

Use ALL validated admission tasks: V62 n256 and V63 n512. Retain V62 n1024's
three CPU-limit noncompletions in the admission report. Do not choose a favorable
task or seed. V63 was an explicitly adaptive single size calibration, now stopped.
Both included tasks are generated planted-CNF development workloads; they are
not independent systems or a sample of real-world SAT instances. For future splits,
conservatively group MiniSat with Z3. No new independent-group claim.

Primary method RF-LCB as in V61. Shared prefix4random+6greedy3NN, checkpoint10,
total20 inclusive, seeds11/23/37/53/71. Random and3NN continuations are controls.
Use pinned64-tree RF-LCB implementation, mean minus tree standard deviation,
no fitting of hyperparameters to these tasks. Full-table scoring after all choices.
Two tasks ×5seeds ×3arms =30arms,400 charged recorded acquisitions.

48-setting grid: var-decay[.8,.95], cla-decay[.9,.999], rfirst[25,100,400],
rinc[1.2,2], phase-saving[0,2]. Includes both feasibility reference and contrast;
restart interval spans quarter/default/four-times default. Fixed Luby=true,
random-frequency0 and owner random seed. Parameter choices follow exposed
feasibility and owner semantics, not held-out data. Freeze before any full-grid
outcomes. All settings/tasks included; no pruning or outcome-led expansion.
Three fresh repetitions each:48×2×3=288 physical invocations. Per round, n256 then
n512; configuration order shuffled with Random(64000+1000*round+task_index).

Each outcome must exit10 and independently satisfy every original CNF clause.
Use the pinned, compatibility-patched V62 binary. CPU cap18s, wall20s, sampled
process-group RSS512MiB. Valid objective is whole-process exit-wall milliseconds;
resource noncompletion gets a declared40000ms PAR2-style score, not a fabricated
runtime. Preserve raw logs/models/timeouts. Unexpected failure or invalid model
stops the whole stage; remaining trials unattempted. No retries. Median of3 penalized
scores defines each recorded table row. Check acquired labels before each selection.

Gate: actual preselected RF-LCB headroom to recorded minimum, threshold
max(5%,2*median CV among three-valid settings); >=2/5seeds. Undefined/no admission
if no fully valid setting. Portfolio remains a labeled hindsight diagnostic.
Failure of this gate ends model collection on this grid. Passing means only that
preparation of a paired-model assay may be justified, not proof an LLM will help.

Resource request: up to7200s physical collection (2h),288 trials,180s offline screen,
400 recorded accesses, zero model requests/downloads/spending. This exceeds the
pilot30-minute default; explicit scope approval is required. Worst-case288×20s
is5760s before validation, so the requested cap has finite overhead room. The
n512 reference projects roughly13.3minutes for that half-grid, but is not a bound;
some unmeasured settings could hit18s CPU. No launch with less than25s remaining.
Incomplete table cannot be analyzed as complete, and no automatic cap extension.

The collector must reject execution unless passed the exact frozen-envelope SHA
through an explicitly approved scope invocation. Receipt binds this hash, command,
trial/runtime/request/spend limits. No reuse of V59 authorization or old model-call
allowances. All incurred V60–V63 source/build/admission costs remain in the ledger.
No publication, remote push, service installation, cloud spending or author contact.
