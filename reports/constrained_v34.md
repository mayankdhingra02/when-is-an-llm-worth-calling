# V34: output-size constraints change the comparison

The fixed assigned-ID selections from the real 1.5B model have **−0.3015% mean feasible-runtime gain** against size-aware shortlist 3NN: **one win, six ties and three harms across ten cases**. Family means are −0.4421% for Brotli and −0.1608% for lrzip. There is no primary-comparator advantage in this exploratory result.

A positive result exists against static ranking (+1.3495%), but stronger controls remove it: −1.6470% against full-domain joint3NN and −2.6023% against runtime-only sequential3NN with the same feasible final-selection rule. Across all three model presentations versus runtime3NN there are **zero wins, nineteen ties and eleven harms in thirty comparisons**. Those thirty observations reuse ten prefixes from two families; they are not thirty independent systems. A positive comparison with a weaker control does not establish useful escalation.

The output-size constraint matters. On the same acquired sets, assigned-ID LLM versus full-domain joint3NN changes from +1.8075% unconstrained to −1.6470% constrained; versus static ranking it changes from −0.4225% to +1.3495%. This is evidence that the runtime-only ordering can change when the chosen configurations must meet a constraint. It is not evidence that one scoring rule should be selected for a favorable result.

## What actually ran

Ten saved V6 prefixes: all five fixed seeds (11,23,37,53,71) for Brotli0.3.0 and lrzip530. Both source owners document runtime and compressed output size. MySQL does not provide the required output-size objective. Dataset identity, schemas, filters, feature deduplication and source README hashes are in [the frozen manifest](../data/constrained_v34.json). Owner artifact: ChristianKaltenecker/PerformanceEvolution_Website, commit `4ee53dad6b81543c444d44282053def0d82d97b3`, GPL-2.0; prior provenance and caveats are retained.

The cap is the recorded output size of the first fastest configuration in each ten-evaluation prefix, identical to the V11/V12 research rule. It is determined only from acquired prefix labels and guarantees a feasible incumbent. Seven continuations run for each prefix: joint3NN over the same twenty-row shortlist, joint3NN over the full domain, static ranking, frozen runtime3NN, and three cached real model presentations. Each branch acquires ten additional distinct runtime/size vectors, and the final selector retains the fastest acquired feasible configuration. Infeasible acquisitions still consume budget.

**70/70 arms completed.** The new journal contains **800 charged recorded-vector accesses**: 100 to reacquire joint prefixes and 700 for continuations. Logical branch totals sum to 1,400 including the shared prefix. These are accesses to published measurements, not fresh physical runs or 800 globally unique configurations. Previous accesses remain in the historical account. All source labels and all 200 adaptive joint-control decisions were replayed independently. Full-domain control trajectories exactly reproduce V12.

The model selections come from actual V22 `Qwen/Qwen2.5-1.5B-Instruct`, revision `989aa7980e4cf806f80c7fef2b1adb7bc71aa306`, local CPU float32 inference. Thirty original requests are reused here: three presentations per case. Exact-repeat requests are excluded from efficacy but retained in historical cost. Raw outputs, ID mapping, original prompt, cache keys, token traces and selected rows were checked. **The original prompts were runtime-only. This is retrospective constrained evaluation of unchanged actions, not an LLM answering a size-aware prompt.** No model outputs were invented, regenerated or substituted.

## Complete comparison

Gain is `(classical feasible runtime − LLM feasible runtime) / classical feasible runtime`. Positive favors the LLM. Means average five seeds within each family, then weight the two families equally. Unconstrained columns use each arm's fastest acquired row without the size filter; proposal trajectories are unchanged. No raw runtime is averaged across systems.

| Presentation | Comparator | Mean constrained gain | Unconstrained gain on same rows | Wins / ties / harms |
|---|---|---:|---:|---:|
| assigned_ids | joint_shortlist | -0.3015% | -0.9333% | 1 / 6 / 3 |
| assigned_ids | joint_full | -1.6470% | +1.8075% | 0 / 5 / 5 |
| assigned_ids | static_rank | +1.3495% | -0.4225% | 2 / 5 / 3 |
| assigned_ids | runtime_3nn | -2.6023% | -1.2571% | 0 / 6 / 4 |
| reverse_display | joint_shortlist | +0.2406% | -1.1220% | 2 / 5 / 3 |
| reverse_display | joint_full | -1.1159% | +1.5174% | 1 / 4 / 5 |
| reverse_display | static_rank | +2.0932% | -0.5399% | 3 / 5 / 2 |
| reverse_display | runtime_3nn | -1.7339% | -1.4458% | 0 / 7 / 3 |
| reassigned_ids | joint_shortlist | -0.2704% | -0.9891% | 1 / 7 / 2 |
| reassigned_ids | joint_full | -1.6040% | +1.7276% | 0 / 4 / 6 |
| reassigned_ids | static_rank | +1.4478% | -0.4508% | 1 / 8 / 1 |
| reassigned_ids | runtime_3nn | -2.5720% | -1.3137% | 0 / 6 / 4 |

The reversed-display primary mean is slightly positive (+0.2406%) but splits into +3.3014% for Brotli and −2.8203% for lrzip. Reassigned IDs give −0.2704%. All conditions are retained; selecting reversed display after observing these outcomes would be exploratory tuning.

![Constrained gain by family and comparator](../results/v34_constrained/constrained_gains.png)

## Constraint diagnostics

| Arm | Runtime-only final choice violates cap (of 10) | Infeasible continuation vectors (of 100) |
|---|---:|---:|
| joint_shortlist | 2 | 31 |
| joint_full | 1 | 17 |
| static_rank | 3 | 24 |
| runtime_3nn | 2 | 35 |
| cached_llm_assigned_ids | 3 | 25 |
| cached_llm_reverse_display | 4 | 25 |
| cached_llm_reassigned_ids | 2 | 25 |

All reported constrained final choices satisfy their cap, because the selector keeps a feasible acquired incumbent. The violations above describe the *unconstrained* fastest choice and the exploration budget consumed by infeasible proposals. They are not malformed-response counts or validated deployment failure probabilities.

## Cost and verification

Collection took 1.780991 ledger seconds; analysis/rendering took 2.448270. Total new experiment time is 4.229261 seconds. Development, tests and read-only verification are not included in that experiment-runtime counter. New model calls: **0**. New physical trials: **0**. New external spend: **USD0**. Downloads unchanged.

Cumulative charged runtime: **2281.347753/3600 seconds**; remaining **1318.652247 seconds**. Follow-up model calls remain **200/200** (300 total with the initial stage). Recorded accesses total **9,108**; physical trials remain **1,274**. No active job remains.

A hypothetical deployment of one method for these ten cases would need 200 joint-vector evaluations. An LLM method would also require ten model requests, plus startup/controller cost; cached analysis is not zero-cost deployment. The original V22 collection used sixty requests, 95,720 input tokens, 1,200 output tokens and 431.694863 request seconds across three families/presentations/repeats. That historical expense is retained and is not charged again here. V34 does not estimate dollar savings or observed deployment amortization.

**233 tests passed**, with synthetic fixtures isolated. **224 inputs** were frozen before this collection. Independent replay checked 800 ordered raw-label journal entries, 70 arms and 120 paired comparisons; **240 gains were reconstructed with Decimal directly from source strings**. A fresh original V22 verifier replayed all sixty request/token provenance records. All **2,736 historical/current frozen references** passed. The figure was visually inspected. These checks are not a fresh-machine reproduction; the V26 ZIP still covers only through V25.

## Reproduction

From the project root with the pinned local environment:

```sh
.venv/bin/python -m pytest -q
.venv/bin/python scripts/analyze_constrained_v34.py --verify-only
.venv/bin/python scripts/verify_report_larger_v22.py --verify-only
.venv/bin/python scripts/audit_history_v30.py
```

Actual preparation/collection/analysis commands were `scripts/prepare_constrained_v34.py`, `scripts/run_constrained_v34.py`, and `scripts/analyze_constrained_v34.py`. They refuse to overwrite completed outputs. The collector verifies [the freeze](protocol_v34_constrained.freeze.json) before running. A separate research copy can rerun them only with its own output namespace and explicit resource ledger; do not delete historical outputs to rerun in place. Plot generation is `render(summary)` in the analyzer and uses only the saved numerical summary. Logs and receipts are in `artifacts/study_v34/`.

## Limits and next experiment

Only two already-exposed software families and one old workload/revision per family were used. Seeds share data. No held-out test, confidence interval, generalizable learned-router gain, production speedup or application-approved quality requirement is established. The size cap is a research default. Size is not a decompression-correctness proof, and the source table does not supply per-row timing uncertainty. Local model generation was constrained candidate selection, not free-form semantic optimization. Prompt presentation remains consequential.

The single highest-priority next action is to **freeze an application-grounded prospective protocol with a stated quality bound and practical gain margin before collecting fresh size-aware LLM responses**. It must retain strong cheap controls, reserve untouched software-system groups, and account for configuration reuse and request cost. A new bounded local-inference allowance or genuinely compatible provenance-checked cache is required: the existing 200-call follow-up allowance is exhausted, and V22 responses cannot stand in for new size-aware prompts. Until that exists, these completed negative/control-sensitive findings are the honest reviewable result; further variants on exposed cases will not establish routing generalization.
