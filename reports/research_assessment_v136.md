# Research assessment after V136

The new result is a completed, prospectively frozen feedback ablation, not another plan: 100 real local Qwen3-8B requests, 200 newly charged recorded evaluations, 20 B20 arms, two exposed software families and five fixed seeds each. It strengthens the bounded negative result. It does not establish a successful escalation controller or Q2 readiness.

## What changed in the evidence

Earlier work used one-shot model batches. V136 gives each arm five calls with two proposals per call. The feedback arm sees its newly acquired outcomes; the matched control sees the tried configurations but has those new values masked. Call count, objective budget, initial prefix, output contract and round sampling seeds are matched. The two groups were selected by smallest/largest feature counts among the six original families, not favorable outcomes. The protocol, code and inputs were frozen before collection.

Feedback and masked feedback finish with identical incumbents in all ten cases. Each has zero wins, three ties and two losses against historical sequential3NN within each family. Mean relative gains against sequential3NN are −0.9688% for LLVM and −0.4036% for SAC. On objective quality and model-request count, the historical classical continuation weakly dominates each measured model arm: it scores at least as well and requires no model calls. This is not a full wall-time or monetary dominance claim, because historical execution overhead and real deployment objective costs are not newly measured.

Both model arms improve two LLVM prefixes, with mean prefix-relative improvement +1.5642%. Both also improve on the historical one-shot LLVM treatment in those two seeds, for mean +1.5009% across five seeds. Those are real improvements that must be retained. They do not show a feedback benefit: masking yields the same final values. Historical one-shot prompts, seeds, output caps and interaction differ, so the contrast cannot attribute gains solely to more calls. SAC has no prefix improvements.

The model did not simply return identical answers. A separately labeled post-outcome trace audit finds changed text in36/40 follow-up pairs and changed selected rows in27/40, without a final-incumbent benefit. Response sensitivity is not optimization benefit. These are descriptive within-run observations, not an additional preregistered hypothesis test.

All100 responses were valid, with no retries or fallbacks. Formatting failure is therefore not the explanation for this result. Projection is a major limitation:172/200 proposals required nonzero Hamming projection;112 matched already acquired settings before projection, and10 repeated their partner within a round. Stable nearest-unobserved projection ensures budget-valid novel acquisitions but can materially determine the executed search. Claims about model optimization skill must separate model suggestions from adapter behavior.

## Defensible claim and limits

A defensible local claim is: **for these two recorded tasks and this quantized8B symbolic proposal interface, five rounds of measured feedback did not improve the final incumbent over a call-matched masked control, and neither beat continued sequential3NN.** More favorable prefix or historical-batch comparisons alone would overstate added LLM value.

This is not proof of universal LLM failure, a refutation of SNAP2/LLAMBO, or a confirmatory generalization study. The source-method mapping in reports/source_mapping_v127.md remains applicable. Two proposals per round are not fully sequential single-proposal interaction. Both families were already exposed; ten seeds are only two independent systems. Full-dimensional Hamming projection, one model/host, recorded rather than native correctness/noise measurements, and the long adaptive history limit interpretation. No new router was fitted; current selective-routing evidence remains insufficient.

## Reproducibility and costs

The model lifecycle was854.842s and overall collection854.844s, within the1600s/1800s bounds; server exited0. Observed usage was7,378 generated and140,387 prefill tokens, with no missing receipts. Actual paired research collection used100 requests and200 new recorded acquisitions. A single deployed model continuation would use five requests and ten additional evaluations after B10;1280 output tokens are allocated per escalation. Saved request times exclude shared startup and historical prefix/controller costs. Recorded CSV evaluation time is not native workload execution cost. No dollar, energy or native runtime savings are inferred.

The independent standard-library replay reconstructs prompt masking, prefix/state identity, sampling schedule, parsing, projection, selection-before-acquisition timestamps, original charged source rows, final scores and descriptive summaries. Full tests:1,065passed,14dependency warnings. The compact private bundle excludes full tables, weights and binaries; its acquired-row extracts support saved-record replay, not second-host fresh execution or authentication of omitted files. All synthetic fixtures and corruptions remain separate.

Previous V135 evidence stays sealed and all its mutable root documents were snapshotted before updates. A stale V135 config split string is recorded as an erratum; the governing protocol/report already described exposed development. No prior result is overwritten or relabeled.

## Highest-priority next action

**Freeze a coherent independent system cohort and its comparator contract before further collection.** Include continued classical search, a cheap incumbent-neighbor/projection control, and the now-fixed feedback/masked treatments. Select systems by workload validity and independence, not expected model benefit; predeclare a practical gain margin, group-level analysis, cost/reliability accounting and finite collection cap. Check that the cohort has not been used in the long development history. Do not reuse LLVM/SAC as untouched test systems or keep changing prompts on them.

Cross-model/host and representative native execution remain later robustness work. Novelty still requires an exact comparison to prior conditional escalation work; experiment count and journal quartile are not scientific stopping criteria. This completed finite batch is closed. Nothing continues outside the active session.
