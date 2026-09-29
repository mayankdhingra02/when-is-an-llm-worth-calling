# Corrected exploratory pilot v3: real paired results

**The corrected full-schema pilot obtained real local-model continuations.** The three format checks passed, and 15/15 paired software runs completed. This removes v1's format blocker; it does not establish that a learned escalation controller generalizes.

The user authorized continuation after v1 stopped at its cap. One follow-up allowance of 100 local attempts was announced. v2 used 33 of those before a schema defect was found; v3 uses the same remaining allowance, without increasing it. See [protocol_v3.md](protocol_v3.md). The original 30-minute cumulative runtime ceiling and USD 0 external-spending restriction remained. Original v1/v2 evidence is preserved. A schema error silently dropped SQLite's real INDEX option in those versions; see [schema_erratum.md](schema_erratum.md). Their SQLite conclusions are superseded.

## What changed

The same official Qwen 0.5B model used a compact prompt and constrained binary strings. Each call produces five full configurations; each coordinate is selected from the model's logits over its legal domain. Only row separators and EOS syntax are fixed. No JSON guesses or repairs are supplied by the harness. Generated token IDs and the complete constraint schedule are logged so this distinction is auditable. Nothing uses unseen objectives to select tokens or project candidates. A known dead worker now stops collection before reserving another request; a timeout stops the stage.

Three real-model format checks used independent synthetic fixtures with 9, 16 and 39 binary variables. These calls count toward costs but their synthetic quality never enters software results. They passed before the first v3 continuation. No prompt or model was changed after seeing v3 outcomes. This is a changed-treatment exploratory adaptation, not a SNAP2 numerical replication.

## Optimization results

All 30 classical arms were rerun using explicit full schemas, and new ten-label prefixes saved. SQLite now has 39 features, 4,652 unique configurations and one excluded duplicate. Each LLM branch acquired ten additional labels in two batches of five, giving the same logical B=20 per arm. Batch size differs from SNAP2 and the earlier JSON treatment and was frozen before v3 outcomes. The only held-out smoke system is x264; its classical scores had already been inspected during v1, so v3 is explicitly exploratory.

| System | Random mean loss | Centroid mean loss | Constrained LLM mean loss | Mean paired gain |
|---|---:|---:|---:|---:|
| Apache | 0.01333 | 0.00000 | 0.03000 | -0.03000 |
| SQL | 0.17420 | 0.18451 | 0.16484 | +0.01968 |
| X264 | 0.03054 | 0.06175 | 0.05881 | +0.00295 |

Loss is best acquired normalized d2h (lower is better); gain is classical loss minus LLM loss. Across 15 pairs, 2 gains exceeded the predeclared +0.02 material margin, and 3 were below -0.02. These are descriptive counts, not independent-system statistical evidence.

The average LLM gain on x264 is only 0.00295, below the material margin. Random search has lower mean loss than both the centroid and LLM arms on x264, so the LLM comparison does not establish an advantage over the simplest baseline. Apache's classical arm reaches the observed optimum in all five runs, leaving no final-quality improvement headroom against that arm.

![Paired gains](../results/v3/analysis/paired_gains.png)

## Fixed controller comparison

Ridge benefit prediction and both ablations used only Apache+SQLite development groups, with group cross-fitted predictions for threshold selection. Uncertainty thresholds also used development groups only. Preprocessing and fitted weights did not access x264 outcomes. Policies were applied once with fixed thresholds. Repeated seeds are not new software groups.

| Policy | x264 mean loss | Escalations | Selected-branch requests | Missed useful / useful | Harmful escalations |
|---|---:|---:|---:|---:|---:|
| never | 0.06175 | 0/5 | 0 | 1/1 | 0 |
| always | 0.05881 | 5/5 | 10 | 0/1 | 0 |
| benefit | 0.06175 | 0/5 | 0 | 1/1 | 0 |
| random_development_rate | 0.06175 | 0/5 | 0 | 1/1 | 0 |
| random_matched_realized_rate_DIAGNOSTIC | 0.06175 | 0/5 | 0 | 1/1 | 0 |
| benefit_without_uncertainty | 0.06175 | 0/5 | 0 | 1/1 | 0 |
| gain_from_uncertainty_only | 0.06175 | 0/5 | 0 | 1/1 | 0 |
| uncertainty | 0.06176 | 1/5 | 2 | 1/1 | 0 |
| hindsight_NONDEPLOYABLE | 0.05563 | 1/5 | 2 | 0/1 | 0 |

The hindsight row chooses after seeing both outcomes and is **non-deployable**. Its selected-branch requests are an accounting reference, not the cost of obtaining oracle knowledge. Random realized-rate matching uses only the count of selected cases, never outcome quality; it is a retrospective diagnostic with one fixed random draw. All fixed-grid points are retained in threshold_curves.csv. No further test-set threshold selection was performed.

**The learned router has not demonstrated useful selection.** Development-only threshold fitting selects an infinite benefit threshold (serialized as null), so the router makes no x264 calls and misses its one materially useful escalation. Both zero-rate random comparisons are consequently degenerate: they cannot establish selection quality beyond random. The uncertainty policy escalates once, but misses the useful case too. Avoided calls describe these fixed policies under the chosen development criterion; they do not prove generalizable cost savings or equivalent quality.

Only two development systems and one held-out system are available. Router evidence remains insufficient regardless of the ordering in this five-seed table. No confidence intervals, significance tests, non-inferiority claims or generalization claims are made.

![Fixed threshold curves](../results/v3/analysis/quality_cost_curve.png)

## Reliability and costs

- 33 additional real local requests: 3 format checks and 30 software-continuation requests; 0 provider errors, 0 malformed paired responses, 0 retries.
- 0 fallback acquisitions; 141 proposals required nonzero feature projection distance; 61 were exact duplicates of an acquired configuration; 110 were nearer an acquired row than their selected unevaluated row. Projection still charges a fresh label, and duplicate suggestions still have model cost.
- Observed v3 tokens: 32,809 input and 3,685 output, including grammar-forced syntax and the three feasibility calls. This is real inference, not hand-produced JSON proposals.
- **750 new label accesses** in v3: 600 corrected classical accesses plus 150 LLM continuation accesses. Earlier collection remains charged: v1 used 700 and interrupted v2 used 58, giving 1508 cumulative accesses. Saved prefixes are reused only within each corrected pair.
- v3 request wall time: 313.79 seconds. Cumulative recorded experiment time: 1156.14/1,800 seconds, of which 627.84 seconds were charged to the complete follow-up, including the interrupted v2 stage, corrected baselines and analysis. Model startup/loading is separately recorded in model_runtime.json.
- Additional experiment spending: **USD 0**. No new dependencies, weights or cloud resources. Electricity and hardware costs remain unknown. v1 timeout tokens remain unknown; v3 observed usage does not retroactively fill that gap.

Policy deployment costs select only the chosen branch plus prefix/feature computation; per-router prediction overhead is separately recorded in router files and is very small, but this is trace replay rather than a separately timed deployed service. Historical training/paired collection and model loading are not advertised as free. The cumulative ledgers and per-request raw logs remain authoritative.

## Evidence and limits

[results/v3](../results/v3/) contains the frozen manifest/source snapshot, real raw requests, generated token IDs, constraints, feasibility fixtures, checkpoints and run records. The verifier checks exact prefix equality, 20-label budgets, table outcomes, prompt reconstruction from acquired observations only, projection replay, token-to-text decoding, legal token schedules and metrics. Original v1 verification remains separate.

The constrained format gate is largely guaranteed by construction; it checks execution and serialization, not model reasoning. The small model, binary single-objective tables, offline objectives and three software groups sharply limit scientific claims. Optimizer normalization/projection and the model differ from the source paper. Dataset pretraining contamination and original workload/hardware versions remain unresolved. See [limitations.md](limitations.md).

In particular, 141/150 suggestions required projection onto the measured configuration table. The result therefore evaluates the model plus this feature-distance projection rule, with substantial duplicate/collision behavior; it cannot isolate the model's optimization contribution. No model-free projection ablation was run. A stale prompt phrase was corrected during preflight before any v3 inference; the correction and the distinct classical/paired code snapshots are recorded in decisions.md.

## Next action

Review the paired gains and policy table with the source-alignment caveats, then freeze a larger evaluation with more independent software systems. Before spending on scale, assess whether useful LLM gains and harmful cases provide enough routing variation. Do not tune repeatedly on this x264 smoke result. A meaningful generalization study needs untouched system groups, a validated system/variant registry and a new resource plan.
