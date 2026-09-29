# V103: local reasoning delivery works, but escalation did not earn its cost

The completed exploratory comparison covers six previously exposed software-system groups, two fixed seeds per group and two modes. It made **36 real local Qwen3-8B requests**, retained all **24 intended conditions**, and acquired **240 recorded objective outcomes**. Every continuation used its saved ten-evaluation prefix and exactly ten additional outcomes. These are recorded-table experiments, not new native software measurements.

| Procedure | Valid finals | Mean gain vs sequential 3NN | Mean gain vs batch 3NN | Valid cases >=5% better than BOTH |
|---|---:|---:|---:|---:|
| 128-token thought + 128-token final | 10/12 | -7.64% | -3.97% | 0 |
| Nonthinking, 128-token final | 12/12 | -6.52% | -2.74% | 0 |

Means first average seeds within each system, then weight the six systems equally. Full policy results include the two fixed classical fallbacks. Valid-only results are saved separately and lead to the same zero count of useful wins against both controls. Dune contributes a large part of the mean loss; this is not evidence of uniform harm across every system.

One BerkeleyDB case in each mode improved on sequential 3NN by about 5%. The thinking case only tied batch 3NN; nonthinking was slightly worse than batch. That is why it would be misleading to present the sequential-only win as evidence that an LLM was needed.

## Reliability and cost

All 36 requests returned, with zero retries, transport failures or unattempted conditions. Two thinking final answers failed strict parsing: OpenVPN seed 11 returned nine IDs, and SAC seed 11 reached its output limit with invalid formatting. Those answers were preserved without repair. Both receive the predeclared classical fallback; its quality is not credited to the model. All twelve thoughts reached their 128-token ceiling.

Thinking used 24 requests and 1,882 generated tokens, including its failed final answers; nonthinking used 12 requests and 240 generated tokens. Mean observed case time was 55.64 seconds for thinking and 22.16 seconds for nonthinking. Their difference is descriptive on this host and run order, not an isolated causal estimate of reasoning overhead. Both phases' prompt processing is charged: 60,806 actual prefill tokens across the batch. There are no missing usage records in V103.

The model lifecycle lasted 936.011 seconds (15.60 minutes), with peak sampled model RSS 8,356,478,976 bytes, below the 8 GiB cap; server exit 0. Allocation was 4,608 output tokens; actual generation was 2,122. No new downloads, paid service or cloud use. Electricity/hardware cost is unknown. Historical prefixes and classical references retain their prior collection costs.

For a hypothetical deployment, one thinking escalation uses at most two requests and 256 allocated output tokens; nonthinking uses one request and 128 tokens. Both allow ten objective evaluations after the ten-evaluation checkpoint. This accounting scenario is distinct from actual research collection, which ran both counterfactual modes. It is not a claim of deployed savings.

## What changed after restart

V101 repeated the previous feasibility test after the user's Mac restart. Nonthinking returned, but its 512-token thought request timed out; missing response usage remains unknown. V102 then separately froze a 128-token thought adaptation using delivery/runtime evidence only, without scoring new objectives. Both final answers arrived in three real requests. V103 used fresh responses and a preselected smaller cohort to remain within the existing 30-minute stage limit. The restart and reduced thought budget must not be described as a single isolated causal intervention or a proven memory fix.

The two preliminary stages added five real requests and zero objective acquisitions. Their failures and costs remain separate from V103. No feasibility response was reused as a new research observation.

## Validation and scope

Independent replay verified all 24 conditions, the 240 saved acquisitions, budget-20 states and metrics with zero new labels or calls. The full suite passed 777 tests. Three additional synthetic corruption checks rejected altered thought text, final prompts and selected IDs; they operate on copies and never enter research aggregates. Total current passing tests: 780. The report, two derived JSON tables and PNG/SVG figures reproduced byte-for-byte. The figure was visually inspected.

This is an adaptation of prior budget-forcing work, using a quantized model and a very short thought allowance. Mode-specific sampling differs too. The six groups were already exposed during development, each has only two seeds, public-data contamination is possible, and this is one local host. No new router was fit on these outcomes, no useful predictor is established, and the findings do not rule out stronger models or larger reasoning budgets. **Q2 readiness is not established.**

The supported conclusion is narrow: on this frozen small-budget development cohort, neither tested procedure produced a >=5% gain over both strong cheap controls, while thinking added cost and two final-format failures.

## Next experiment

The single highest-priority next action is to freeze an independent-system replication before inspecting any of its continuation outcomes. Keep strong cheap controls and the practical benefit threshold, retain all variants/seeds within system groups, and size the independent group count for the desired claim before collection. Independent-machine execution would separately test runtime portability; no second host is connected. Do not keep adjusting this exposed cohort to obtain a positive result. A learned router needs demonstrable, reproducible escalation opportunities and enough independent groups to evaluate prediction honestly.

Evidence: [frozen protocol](protocol_v103.md), [full report](reasoning_v103.md), [raw model records](../results/v103_reasoning/), [acquired outcomes and analyses](../results/v103_analysis/), [execution and validation receipts](../artifacts/study_v103/). Start future sessions from [STATUS](../STATUS.md).
