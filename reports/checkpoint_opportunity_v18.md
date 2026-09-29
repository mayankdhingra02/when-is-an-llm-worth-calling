# V18: the reference already leaves little opportunity

**The initial reference itself limits possible improvement on these measured tasks.** On the expanded V17 grid, the full-table feasible optimum improves reference runtime by at most2.929% for Zstandard,0.987% for LZ4 and0% for zlib. On the V16 grid, the corresponding limits are2.510%,0.025% and0%. These are bounds over recorded medians under the fixed reference-size constraint, not bounds on unknown true runtimes.

This explains more than the earlier statement that cheap search left little headroom: a10% improvement was already impossible relative to the initial reference in these recorded tables. More settings or a stronger model cannot overcome that finite-table limit while retaining the same objective, constraint and reference incumbent. It does **not** establish that LLM optimization generally lacks value.

## Executed audit

Recomputed every saved V16/V17 joint3NN arm: two grids ×three exposed families ×five seeds =30 cases. No model, physical measurement or optimizer was run. This is explicitly post-hoc development analysis after inspecting earlier outcomes; its complete case list and formulas were frozen before execution. Source labels, reference-derived cap, unique10/20 budgets, incumbent monotonicity and the savings identity were verified. A second --verify-only execution reproduced the saved summary.127 synthetic/infrastructure tests passed; fixtures are excluded from measured results.

| Grid | Family | Feasible/total settings | Headroom at reference | Mean at checkpoint10 | Mean after cheap20 | Cheap continuation improved |
|---|---|---:|---:|---:|---:|---:|
| V16 | zstd | 20/32 | 2.510% | 1.053% | 0.275% | 3/5 |
| V16 | lz4 | 28/32 | 0.025% | 0.010% | 0.000% | 2/5 |
| V16 | zlib | 5/32 | 0.000% | 0.000% | 0.000% | 0/5 |
| V17 | zstd | 72/96 | 2.929% | 1.123% | 0.537% | 2/5 |
| V17 | lz4 | 92/96 | 0.987% | 0.790% | 0.197% | 3/5 |
| V17 | zlib | 12/90 | 0.000% | 0.000% | 0.000% | 0/5 |

Reference headroom is constant across seeds within a grid/family. Checkpoint/final headroom uses its corresponding incumbent as denominator, averaged over five seeds. Counts are exact comparisons of saved medians, not tests of statistically meaningful improvements. The two grids reuse families/workload and do not yield six independent systems. Twelve feasible zlib settings in V17 do not provide useful runtime improvement over the selected reference in the recorded table.

## Why this is an upper bound in the recorded problem

Let R be the initial reference runtime, P the best feasible runtime at checkpoint10, C the cheap-arm best runtime at20, and O the minimum feasible recorded runtime in the complete grid. Incumbent retention gives O≤C≤P≤R. Even an ideal alternative continuation with access to any grid setting can improve over C by at most(C−O)/C≤(R−O)/R. The observed V17 values of(R−O)/R are all below3%, so the previously fixed10% headroom diagnostic cannot be reached under these recorded conditions. This is an arithmetic bound, not a statistical uncertainty guarantee or an application-approved utility margin.

For an additive decomposition we use one denominator: savings before checkpoint=(R−P)/R, during cheap continuation=(P−C)/R, and remaining hindsight opportunity=(C−O)/R. Their sum equals(R−O)/R. The figure uses this common denominator; its bars must not be confused with the separately normalized headroom columns above.

![Opportunity decomposition](../results/v18_checkpoint_audit/decomposition.png)

The full-table optimum is available only to this offline evaluator, after dataset construction. It is not an optimizer/router feature or a zero-cost deployment signal. All original physical measurement and paired-collection costs remain charged. Timing noise, three repetitions, a single small source archive, CLI launch overhead, constrained output size and the predefined reference explain why this cannot establish general optimality or cross-application benefit. V15/V17 timing boundaries also differ, so differences between grids are not causal effects of expansion.

## Evidence, reproduction and costs

- [All30 case rows](../results/v18_checkpoint_audit/cases.csv), [machine-readable summary](../results/v18_checkpoint_audit/summary.json), [protocol](protocol_v18_checkpoint.md), [71-file freeze](protocol_v18_checkpoint.freeze.json).
- [Executed analysis](../artifacts/study_v18/analysis.log), [replay](../artifacts/study_v18/replay.log), [127 passing tests](../artifacts/study_v18/tests.log).
- Run `.venv/bin/python scripts/audit_checkpoint_v18.py --verify-only` to recompute the saved audit. The initial command without that option generated the CSV/PNG/SVG and refuses to overwrite a completed audit. Both modes charge analysis runtime; neither acquires labels or invokes models.

New cost:0 physical trials,0 optimizer label acquisitions,0 model requests,0 downloads,USD0 external spend;0.3939seconds charged for analysis/render/replay. Cumulative runtime1744.2008/1800seconds with55.7992seconds remaining. Inference128/128 remains exhausted. Historical totals remain1134 physical trials and5408 recorded-table acquisitions, separate cost types. No live-deployment cost savings were measured or estimated.

The next useful decision is an application-grounded task/utility specification that admits meaningful improvement over a credible starting configuration. Simply selecting a deliberately weak reference to force a positive result would change the question and is not justified. No new benchmark or model campaign starts here. The [discussion note](review_note.md) now distinguishes exact reproduction of V8's first-ten choices from an untested causal effect of candidate order.
