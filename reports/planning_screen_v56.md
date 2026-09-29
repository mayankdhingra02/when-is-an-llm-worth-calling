# V55/V56 — Fast Downward feasibility and classical screen

Actual execution on the local Apple M3 Pro/18GiB machine, 2026-09-25. Fresh
release24.06.1 adaptation of the historical workload lead; one development family,
not replication of old timings, a new independent test set, or an LLM result.

**Decision:** The prespecified headroom gate FAILED. Retire this fixed grid for positive LLM-benefit discovery; do not widen the grid or change this workload until a favorable score appears. Keep it as a correctness/reliability control.

## What actually ran

V55 compiled pinned owner source locally (GPL3-or-later), without LP solvers.
Initial compiler configuration failed on a linker/SDK mismatch; project-local
MacOSX15.5 SDK selection fixed it. Both build receipts remain. Three feasibility
invocations passed: independent plan costs104, action counts18/17/18, wall seconds
1.104425, 24.705954, 0.884714. Whole stage
26.700502s. Agreement with admissible A* is not an independent
optimality certificate. The validator proves plan feasibility and recomputes cost.

V56 froze48 command settings × three repetitions, shuffled independently by round.
All144/144 intended trials were attempted, 72
passed the full validity/cost contract; status counts: {'valid': 72, 'resource_or_unsolved': 72}. Stage
741.686357s. No retries or dropped cases. Sampled maximum
process-group RSS 87.33MiB. Timeout/resource failures receive20000ms
in the optimization objective; this is an explicit penalty, not invented timing.
Raw wall seconds and exit status are retained. Objective is median of three
penalized wall times; it includes process/translation/monitoring overhead.

Five fixed seeds used the same saved ten-observation prefix per paired comparison;
random,3NN and64-tree RF-LCB each continued to20 inclusive outcomes. All15 arms and
200 charged recorded median-vector acquisitions ran; offline stage
1.342379s. Full-table scoring followed saved decisions. No LLM,
router fit, token usage, paid API or cloud spending in these stages.

## Observed classical results

Best recorded median: **0.886460s**. Noise estimate from
24 settings with three valid repetitions: median CV
1.707%; frozen gate threshold
5.000%. Hindsight best-of-three portfolio meets threshold
in **0/5** seeds. That portfolio is not a deployable policy.
The actual RF-LCB arm independently reaches the best recorded median in
**5/5** seeds. This is an attained classical result on the saved table,
not a guarantee of the physical optimum. The small improvements over the prefix
are below the median timing CV. All72 resource failures belong to hmax settings;
V55 showed hmax can solve the task with more time, so failure here is cap-specific.

| Seed | Prefix10 (s) | Random20 (s) | 3NN20 (s) | RF-LCB20 (s) | Portfolio headroom |
|---|---:|---:|---:|---:|---:|
| 11 | 0.8969 | 0.8969 | 0.8865 | 0.8865 | 0.000% |
| 23 | 0.8969 | 0.8969 | 0.8865 | 0.8865 | 0.000% |
| 37 | 0.8969 | 0.8969 | 0.8865 | 0.8865 | 0.000% |
| 53 | 0.8969 | 0.8969 | 0.8969 | 0.8865 | 0.000% |
| 71 | 0.8969 | 0.8865 | 0.8865 | 0.8865 | 0.000% |

![Measured screen](../results/v56_planning_screen/planning_screen.png)

## Integrity, limits and accounting

- Same domain/problem, actual action costs and validated cost104 for every valid
  run. Different plans/action counts are allowed at equal cost. All heuristics,
  pruning choices and A* tie rules preserve the intended optimal-search contract
  under the inspected source assumptions. No programmatic correctness proof.
- New independent flat typed STRIPS validator rejects unsupported expressions;
  owner documentation flags a VAL bug for this domain. The new validator has
  synthetic/adversarial tests but has not been cross-checked with a mature external
  validator. Dataset redistribution license unresolved; do not publish payloads.
- Feasibility protocol deviation: owner driver removed the V55 intermediate SAS
  files by default; PDDL, plans and full logs remain. V56 explicitly retained all
  translated tasks. This retention omission did not alter plan validation/scoring.
- Owner macOS memory log reports virtual address size, not RSS, often hundreds
  of GiB. Use wrapper sampled process-group RSS instead. Sampling may miss spikes;
  no hard macOS allocation guarantee.0.2s polling quantizes wall observations and
  perturbs timing. Small apparent runtime gaps may be monitoring/host noise.
- Three repetitions, one tiny task and five dependent seeds cannot establish
  population generalization or journal readiness.24.06.1 is pinned, not latest.
  Feasibility outcomes informed the grid/cap; all data are development evidence.
  The configuration-ID order and tie breaks are fixed; no row-permutation ablation
  or independent-machine timing reproduction was run.
- Actual research cost is147 new planner invocations (V55+V56), including repeats
  and failures, plus compilation, validation and200 recorded accesses. Estimated
  deployment for one20-outcome arm is60 physical invocations under this recipe;
  it does not require the entire144-trial collection. That deployment estimate is
  conditional on the already established task/utility contract. A cold deployment
  repeating the three feasibility probes would cost63 invocations, and should not
  be presented as a strict20-outcome end-to-end procedure. Hardware/electricity and
  agent/user time costs unknown; new external experiment spend is USD0.

Raw starts/logs/plans/validation: `results/v55_planning_feasibility/` and
`results/v56_planning_physical/`. Prefixes, arms, table, acquisition journal,
summary, CSV and figures: `results/v56_planning_screen/`. Protocols and input
seals: `reports/protocol_v55_planning_feasibility.*` and
`reports/protocol_v56_planning_screen.*`. Source audit: `planning_source_audit_v55.md`.
Verification/test/evidence receipts: `artifacts/study_v55/` and `artifacts/study_v56/`.
All379 tests passed. Read-only verifier checked all144 trial receipts,75 valid
plans including V55,200 charged acquisitions,15 arms,180 reconstructed choices
and both input seals. PNG was visually checked. This replays measured evidence;
it does not independently rerun the physical timings on a different machine.

Safe saved-evidence replay (does not rerun workloads or acquire new labels):

```sh
.venv/bin/python scripts/verify_planning_v56.py
.venv/bin/python scripts/report_planning_v56.py
.venv/bin/python -m pytest -q tests
```

Collectors and offline screen are one-shot and refuse overwrite. To recollect,
create a new versioned protocol/output tree; do not delete/overwrite this evidence.
