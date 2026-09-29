# V165: exhaustive candidate-space headroom diagnostic

Freeze before new measurements. This is a post-V164 development diagnostic on already exposed ripgrep/hnswlib tasks. It asks whether the fixed B10 prefix already approaches an empirically selected best configuration, which could limit the opportunity to demonstrate useful escalation. It is not a new held-out cohort, LLM experiment, deployable oracle, or revision of earlier primary results.

## Measured design

Use the exact V162 64-setting domain and V163/V164 workloads, source bytes, quality constraints and native binaries. No additional downloads, models, source retrieval or system changes. The historical ten prefixes and all90 V164 arm selections are fixed and hashed before collection.

Phase1: evaluate every configuration three times, in three independently shuffled blocks covering both applications (128 configurations/block, seeds165100+block). All384 outcomes are charged. For each application choose the quality-feasible setting with the smallest median utility; ties use numeric candidate ID. A setting is quality-feasible only if all three outputs meet the existing exact-count/95%-ANN-recall contract. Preserve all infeasible and noisy cells; do not remove them from the dataset. If no setting is feasible, stop and report that failure. Selection does not use validation outputs.

Freeze the two selected reference IDs and all phase1 hashes. Phase2: three new shuffled blocks over all128 configurations (seeds165200+block), another384 charged outcomes. This measures validation for every candidate, including historical prefix/model/classical incumbents. Do not reselect the primary reference using phase2. The validation minimum may be disclosed as an explicitly post-hoc secondary statistic, never substituted as the primary reference. No benchmark execution overlaps inference or tests; there is no inference in this stage.

## Analysis fixed before collection

Primary descriptive headroom at the original B10 checkpoint: `(validated_prefix_loss - validated_reference_loss) / validated_prefix_loss`, for all five saved seeds in each application. Prefix incumbent is fixed by its originally acquired labels. Evaluate the selected reference and each frozen incumbent using phase2 median utility. Positive values indicate observed available improvement to the reference. Preserve negative values; the selected reference need not remain fastest on validation.

Also show checkpoints4 and7 using the corresponding acquired-label prefix subsequences from the SAME saved trajectory, and a separately labeled shared-validation diagnostic of the frozen V164 arm incumbents. These do not simulate a different optimizer or LLM handoff at earlier budgets. They expose the current tasks for any future design and cannot establish which early handoff would work.

A robust practical headroom flag requires >10% improvement to the reference, different IDs, all three validation outputs quality-feasible, relative MAD<=5% in both cells, and both medians>=10ms. Same-ID comparisons share one validated value and have exactly zero headroom. This shared-label diagnostic is distinct from earlier separately timed arm validation; do not overwrite/reinterpret their primary estimates. Report noisy/quality-failing cells and every intended outcome. Two systems, not30checkpoint-seed groups; no population significance or equivalence claim.

The reference is the empirically selected best within a fixed finite domain, not the true global runtime optimum. Exhaustive selection remains susceptible to winner selection and host/cache noise; fresh validation separates selection from scoring, but three repetitions cannot certify global optimality or a probabilistic bound. No claim about larger inputs, other model families, production deployments or journal readiness follows.

## Information and cost boundaries

All768 new objective acquisitions belong to an offline evaluator diagnostic, outside prior B20 policy budgets. They never enter previous or new optimizer/router/model inputs; no new controller fit or threshold/prompt selection. Exact candidate inputs and reused prefix labels are already acquired; hidden candidate objective observations remain under results/v165_headroom and are clearly labeled post-outcome research evidence. The historical100prefix outcomes/300invocations and prior model requests remain separate existing costs.

Caps:768 outcomes (384/application),2,304 native invocations (384text×5queries +384ANN×1),1800s total,60s worker,60s reserve, no retries or extra warmups. Every attempt is charged before execution. Incorrect output or worker failure stops collection and preserves missing/failed denominators. Paid/cloud inference and model requests are disabled (zero allowance); downloads zero. Do not silently expand limits. Exact selection, integrity, raw-output, replay and budget tests must pass; synthetic tests remain separate. Preserve prior evidence seals and update STATUS after execution.
