# Decision brief — 24 September 2026

**Close the current bounded pilot; do not scale LLM/router collection on this design.** We implemented and executed real local-model comparisons, but have not demonstrated useful LLM selection or a benefit-aware router advantage. The strongest result is a reproducible diagnosis of why apparently favorable optimization scores were insufficient evidence of model value. This is a discussion-ready pilot, not a validated general result or a publication claim.

## What actually ran and what it means

| Evidence | Observed result | Interpretation |
|---|---|---|
| Corrected initial smoke (V3) | Three software systems, five seeds, total budget 20 and checkpoint 10; classical and real local-model continuations | Executable paired pipeline; a paper-based adaptation, not a SNAP2 numerical replication |
| Grouped routing study (V6) | Three development and three held-out families, five seeds each. Held-out never-escalate loss 0.06150 versus always-escalate 0.07458 (lower is better). Benefit and uncertainty policies selected zero escalations | No routing advantage. Zero-rate random comparisons provide no evidence of selective discrimination; three test families are insufficient for broad conclusions |
| Direct candidate selection (V8) | All 15 real model outputs selected IDs 0–9, the first ten displayed rows | A trivial first-half rule exactly reproduces the observed choices. This does not prove what the model would do under untested prompt reorderings |
| Exact random reference (V9) | Enumerated all 184,756 ten-of-twenty subsets per case. Random selection has at least 0.5 probability of matching/beating each observed model result | Conditional finite-pool mathematics, not a significance test. Favorable model scores do not establish learned ranking |
| Actual size-constrained controls (V12) | 20 continuations, 300 charged runtime/size vector accesses. Cheap nearest-neighbor versus random: +4.82% lrzip, −2.79% Brotli, +1.01% equal-family mean | Mixed exploratory classical result on two development families; no LLM evidence or statistical reliability claim |

V6 uses a normalized single-target loss; V12 uses per-case relative runtime improvement at a fixed prefix-derived output-size cap. These metrics and treatments must not be pooled. Configuration evaluations are acquisitions from recorded tables, not new live software benchmarks. All seeds/variants remain grouped by software family.

## Why more inference is premature

The metric itself needs application validation. V10 found that the original 0.02 normalized improvement margin corresponds to 7.85 seconds for Brotli, exceeding the entire 1.53–1.90 second static-incumbent range. V11 therefore examined runtime under a size cap as a separately labeled retrospective analysis; it did not rewrite the original success criterion.

V12 then tested actual cheap size-aware continuations. Even perfect full-table selection after that cheap optimizer offers only 0.37% mean remaining runtime improvement on lrzip and 9.09% on Brotli. Only two of ten cases have above-10% opportunity, both Brotli. Those are hindsight upper bounds, not achieved improvements. We lack demonstrated opportunity across enough independent systems to justify training a larger router.

## Evidence, cost and limits

- [Source audit](source_audit.md) and [attribution](../THIRD_PARTY.md): primary-source verification; exact SNAP2 artifact not located in the bounded search. Classical implementation and small local Qwen model are explicit adaptations.
- [Held-out report](pilot_report_v6.md), [policy data](../results/v6/policies.csv), [candidate-selection report](pilot_report_v8.md), [exact reference](../results/v9_analysis/summary.json), and [constrained-controls report](constrained_controls_v12.md) retain the measured denominators and failures.
- [Reproduction instructions](../REPRODUCE.md) distinguish historical replay, fresh collection and clean-environment limitations. The latest completed test suite has 95 passing tests; [V12 replay](../artifacts/study_v12/verification.json) verifies all 20 branches and budgets.
- Actual collection: 228 historical request attempts including the initial 100; the approved follow-up allowance is exhausted at 128/128. Across versions, 4,508 charged configuration accesses include V12's 300 joint vectors. Recorded cumulative experiment/analysis time is 1,671.48/1,800 seconds; external spend is USD 0. This is not total human effort or total machine time.
- Estimated deployment costs select only a policy's chosen continuation; they are separately recorded in V6 policy data. Historical paired collection, retries and diagnostics are not free deployment savings.

Still untested: a stronger model, fresh order-permutation responses, live compression correctness and measurement noise, application-approved utility, other budgets, and generalization across many untouched software families. Old failures and the SQLite schema erratum remain preserved.

## Single next action

**Review and specify an application-grounded task/utility before authorizing further inference.** The concrete discussion is whether minimizing runtime under a justified output-size/correctness constraint is useful, and which independent systems can support it. If that task is worth pursuing, predeclare admission and meaningful margins, check development-only headroom against cheap controls, then freeze a bounded model/order test and reserve genuinely untouched families for evaluation. Do not select tasks from favorable held-out outcomes.

This packet is ready for the user's review and discussion with Tim Menzies. Nothing has been sent, published or scheduled. A stronger model may help, but these data do not support a numerical probability of eventual success.
