# V97 restricted-domain paired follow-up

Freeze before new outcomes. This is a development sensitivity experiment on
the already exposed SuperLU system. It is not an independent family or clean
held-out test, and cannot establish a learned router or journal readiness.
V94/V95/V96 evidence stays unchanged. The continuing local-research permission
covers this separately bounded stage; no exhausted collection is resumed.

Use the same pinned SciPy1.13.1/native solver, HB/orsreg_1 matrix and constructed
RHS as V94. Based on the V96 source audit, restrict relaxation to1,2,4,8 and panel
size to4,8,16, retaining all four permutation codes and five pivot thresholds
(0,.01,.1,.5,1). There are240 candidate configurations. This deliberately changes
the search space and may change optimizer trajectories. It does not patch the
installed library or prove universal solver correctness.

Seeds11,23,37,53,71;20 configuration evaluations per arm with a saved10-label
prefix. Freshly acquire every prefix and continuation label; never substitute
V94/V96 timings or model choices. First4 candidates are seed-shuffled, followed
by6 acquired-label-only centroid recommendations. The V41/V8 prompt/20-candidate
shortlist remains unchanged. From each prefix run four ten-label continuations:
same-pool batch3NN, full-domain sequential3NN, full-domain random and real Qwen3.
Branch order is shuffled with seed+97000. No shared branch/RNG outcomes.

Actual collection250 labels (50 prefix+200 continuation), up to750 physical
solves. Each label remains the median of3 physical executions in an isolated
worker. Timed region, numerical certificates, penalty30seconds, worker30second
deadline and2GiB RSS guard are inherited from V94. No discarded warmups or
uncharged probes. Total native collection cap600seconds across both phases.
Read-only replay recomputes certificates and choices, never acquires new labels.
All failures, incomplete prefixes and unattempted conditions retain their
denominator. No retries; preserve partial output if a limit stops the stage.

Use existing Qwen3-8B Q4_K_M owner weights and llama.cpp b11146,4096context,
reasoning off, greedy seed11, ten one-token ID requests per case. Maximum50
scientific requests,0 compatibility generations,0 retries,300seconds model
lifecycle,8GiB server RSS. Local loopback only, no paid/cloud endpoint, no
downloads. Model choices are collected between native phases, so inference
does not overlap solver timings. Partial/failed choices use the already fixed
prefix-only batch3NN fallback and remain labeled as failures. No fabricated output.

Primary descriptive outcomes: per-seed relative incumbent gain
(classical_seconds−LLM_seconds)/classical_seconds for both strong controls and
random; mean over the five seeds; useful/harmful counts at the existing5% margin;
number of cases beating both strong controls by>=5%. No retuning after results.
Report timing noise from recorded repetitions and repeated acquired configs.
Do not infer a change from V94 solely from different group means: domain,
prefixes, timestamps and selected configurations all differ.

Report never/always escalation plus transfer of V94's frozen benefit and
uncertainty rules, both of which are constant never-call. Random at their
matched zero rate also makes no calls. This degeneracy provides no new evidence
of benefit discrimination. Show a clearly labeled two-arm hindsight oracle
as an unattainable diagnostic reference. No fitting on this group's outcomes.

Separate actual collection from estimated deployment:250 acquired labels and
all inference versus20 labels for one chosen branch, plus inference only when
called. Physical solve costs, worker/lifecycle time, startup, token observations,
failures and unknown usage must be explicit. Report inference-only amortization
as an optimistic scenario, not measured financial savings. External spendUSD0;
electricity/hardware cost unknown. One matrix, one machine, five seeds in one
system group; no population confidence interval. A small no-failure sample does
not establish a reliability guarantee. Independent-machine and new-system
evaluation remain necessary.
