# V94: fixed-policy extension to two new numerical engines

Freeze before the first solver outcome. This is a prospective, descriptive
extension of the fixed Qwen3 procedure, not a new learned-router validation and
not a replication of SNAP2. No acceptance or positive-outcome stopping rule.
The user's continuing local-research authorization covers this separately
bounded stage; exhausted V92/V93 allowances are not reused. Existing total
download/model limits remain unchanged. No paid/cloud calls.

## Claim and admission

Question: does the unchanged Qwen3-8B selection procedure improve validated
runtime by at least 5% against BOTH same-pool batch 3NN and full-domain sequential
3NN on each of two previously unmeasured native engines? Report every seed and
the mean paired relative gain within each engine, including negative results.
Do not tune settings, prompts, workload, margin or thresholds after outcomes.
Two engine groups are too few for population confidence intervals or a learned
router generalization claim. All seeds/workload variants stay in the engine group.

SuperLU uses SciPy 1.13.1's bundled SuperLU 6.0.1 and the public HB/orsreg_1
matrix (2,205 square, 14,133 entries), selected on provenance, full numerical
rank and moderate conditioning metadata. The RHS is constructed from a fixed
known solution. This is a real measured numerical workload, with a constructed
RHS, not a recorded software table. HiGHS 1.7.2 uses owner-distributed 25fv47.mps
(821 constraints, 1,571 continuous variables). Shared Python/NumPy/SciPy
infrastructure and one machine limit independence and transportability.

SuperLU domain: permutation code 0=NATURAL, 1=MMD_ATA, 2=MMD_AT_PLUS_A,
3=COLAMD; diagonal pivot threshold {0,.01,.1,.5,1}; relax {1,2,4,8,16};
panel size {4,8,16,32}: 400 configurations. The SciPy wrapper forces symmetric
mode for NATURAL; this coupled behavior is retained and disclosed. Parameters
are forwarded into gstrf; Equil/IterRefine are NOT used as extra dimensions.

HiGHS domain: presolve {off,on}; simplex scaling {0,2,3,4}; dual-edge weights
{0,1,2}; update limit {10,25,50,100,200}; permutation {0,1}: 240 configurations.
Dual serial simplex, one thread, parallel off, seed 11, feasibility tolerances
1e-7 and per-solve 5 seconds are fixed. Every option is checked after setting.
Different legal option vectors can produce identical paths on a particular
matrix; unique vectors are not a guarantee of unique effective behavior.

## Acquisition, correctness and budgets

Seeds 11,23,37,53,71; B=20, checkpoint=10. Existing finite nominal centroid
adaptation: first four seed-shuffled candidates, six acquired-label-only
centroid recommendations. Save the whole prefix state and prompt. Continue
each identical prefix with ten NEW configurations for each of four arms:
same-pool batch 3NN, full-domain sequential 3NN, full-domain random, Qwen3.
No optimizer receives labels from another branch or seed. Even overlapping
configurations are freshly measured and charged. No full-grid timing table.
Prefix acquisition costs 100 labels; four continuations cost 400: 500 total.
Each logical 20-label branch includes its shared prefix; actual collection is
50 labels per case. Branch execution order is seed-randomized before outcomes.
All prefixes are acquired first, then all model calls, then all continuations;
model inference never overlaps native timed measurements.

Each acquired label is the median of THREE physical solver executions in a
fresh worker. All three are correctness checked; none is discarded as warmup.
The timed region includes SuperLU factorization plus solve, or HiGHS run
(including presolve), excluding input parsing/option setup/certification.
No post-selection remeasurement is free: no extra outcome probes are planned.
Selection on noisy medians and block timing drift remain explicit limitations.
Raw vectors for all returned solves are saved for independent certification.

SuperLU must pass scaled residual <=1e-8 and relative forward error <=1e-6.
HiGHS must report optimal and independently pass primal bound feasibility,
dual stationarity, finite-bound dual sign checks and primal-dual relative gap
<=1e-6. Failed/incorrect/timed-out configurations cost one label and receive
30 seconds, retaining the incumbent. Physical starts/returns are journaled;
unreturned work is unknown, never zero. Whole worker: 30 seconds and 2 GiB RSS
watchdog. Whole native collection: 1,800 seconds across both phases. Preserve
all partial records and intended denominators if a cap is reached; no retries.

## Fixed real model

Existing owner Qwen3-8B Q4_K_M weights, revision/hash inherited from V91;
llama.cpp b11146, 4,096 context, reasoning off, greedy seed 11, one token per
candidate ID, ten requests per case, no duplicates. Unchanged V41/V8 shortlist
and prompt; permutation codes are explicit numeric configuration features, not
hidden labels. No semantic explanation/prompt tuning for the new engines.
Exactly 100 scientific requests maximum, zero compatibility generations,
zero retries, 1,800-second lifecycle and 8 GiB server RSS cap. Reuse existing
local-only adapter and charge before sending. Record prompts, raw outputs,
usage, latency, starts, errors and the model/runtime hashes. Unsupported or
failed choices use same-pool prefix-only batch 3NN to fill remaining slots;
retain the LLM failure in the denominator. No fabricated choices.

## Analysis and costs

Primary per-seed gain = (classical incumbent seconds - LLM incumbent seconds)
/ classical incumbent seconds. Report both strong controls and random, all
ten cases, mean within each engine, and empirical useful/harmful counts at
the fixed 5% margin. A two-arm hindsight oracle is a non-deployable diagnostic.
No new router is fit on these outcomes. Earlier routers remain implemented
but this stage does not establish their portability to native numerical work.
No claim of equivalence from nonsignificance, and no seed-as-system inference.

Separate actual collection (500 labels / up to 1,500 physical solves, model
requests and startup/runtime) from deployment (20 labels / 60 physical solves
and only a selected branch). External spending zero; electricity/hardware cost
unknown. Local inference overhead can overwhelm a millisecond-scale objective;
report that directly, not a hypothetical cloud-dollar saving. Save a figure,
raw logs, machine-readable comparison and reproducible correctness/audit script.
Keep source/inputs and all executed code hashes; do not alter prior evidence.
