# V62 — bounded satisfiable-SAT configuration feasibility

Metadata-driven candidate, frozen before timings. Owner MiniSat core at commit
37dc6c67e2af26379d88ce349eb9c4c6160e8543, local Release build, macOS15.5 SDK,
system zlib. MIT license archived. Modern compiler rejects two old declarations;
preserve failed build and exact compatibility patch (memory-report signature and
default-argument placement). Solver search code unchanged; label patched adaptation.

Do not yet count MiniSat as a new independent group. For future grouping, put it
with historically exposed Z3 under a conservative logic-solvers group pending a
more complete code-lineage analysis. Independent source identity is not a proof of
statistical independence. Redis is already development; MongoDB/Storm remain reserved.

Generate exactly two known-satisfiable 3-CNF tasks: n256/seed62001 and n1024/seed62002,
floor(4.3*n) distinct clauses. Uniform distinct variables; reject clauses unsatisfied
by a separately stored random planted assignment. Generator and both files frozen
before execution. These are generated application workloads, not production or
SAT-competition samples. Planted-instance bias limits inference. The witness is
validation-only, excluded from any future optimizer/model inputs.

Six trials, each task reference/contrast/reference. Reference var-decay.95,
cla-decay.999,rfirst100,rinc2,phase-saving2; contrast .8,.9,25,1.2,0.
Both use owner default Luby restart, random-frequency0, fixed default random seed,
core executable (no simplifier), CPU-limit18s, verbosity1. Multiple knobs change
together; no isolated-factor or optimization claim. Every SAT output must exit10
and independently satisfy every original clause. UNSAT on a planted instance,
malformed model, config/internal error stops collection. Resource noncompletion is
retained and is not a valid solution or zero runtime. No retries/parameter changes.

Per-run20s wall, sampled RSS512MiB, stage180s; no launch after155s. Kill dedicated
process group on cap. Objective receipt is exit-based whole-process wall time;
all validation/generation/build/probe costs reported separately. Preserve raw logs,
models, intended/failed/unattempted denominator. No full-grid optimization, new
recorded acquisitions, inference or spending. This feasibility stage cannot establish
headroom, model benefit, router generalization or journal readiness. Any later
grid needs its own outcome-blind frozen design and unchanged scientific stop rules.
