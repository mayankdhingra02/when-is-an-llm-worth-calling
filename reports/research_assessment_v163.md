# Research assessment after V163

We now have a stronger, reproducible negative finding about the **specific escalation procedure tested**. We have not demonstrated a useful general benefit-aware controller. This checkpoint does not justify saying the research is Q2-ready; that is a methodological judgment for review, and journal quartile cannot certify a result.

## New evidence

The previous native solver experiment used two implementations of generated N-queens. This study adds two independent application lineages with real public inputs: ripgrep searches 3,407 CPython source/documentation files; hnswlib indexes 3,823 and queries 1,797 published Optdigits vectors. Query types, vectors and five repeated seeds do not increase the independent-system count. Workload/domain choices were exposed during separately recorded feasibility; these are not untouched production workloads.

The paired study used the existing SmolLM3-3B and Qwen3-8B Q4_K_M models, unchanged saved historical controllers, and five classical comparators. The same ten-evaluation prefix was cloned for each continuation. Each logical arm used seven new search configurations and three fresh incumbent validations, charging all outcomes. No controller was fitted to the new outcomes.

Actual collection was 800 configuration outcomes, 2,400 native invocations, 20 real local-model calls and 70 logical B20 arms. The distinction matters: one text-search outcome times a fixed bundle of five distinct queries. The original failed admission remains visible: 40 V161 outcomes, including five inadequate ANN recalls and unstable text timing. A separately frozen V162 repair passed all 40 admission outcomes. No LLM output was used to select the repair.

| Family | Model | Mean gain vs sequential | vs adaptive | vs GP-EI | Robust joint wins |
|---|---|---:|---:|---:|---:|
| ripgrep | SmolLM3-3B | -1.295% | -0.647% | -2.174% | 0/5 |
| ripgrep | Qwen3-8B | -0.368% | +0.258% | -1.218% | 0/5 |
| hnswlib | SmolLM3-3B | -0.401% | -0.347% | +0.750% | 0/5 |
| hnswlib | Qwen3-8B | -0.123% | -0.075% | +1.029% | 0/5 |

Positive gain means lower fresh-validation utility. The predeclared practical win required over 10% improvement against all three strong controls, distinct configurations, quality-feasible outputs, relative MAD at most 5%, and median time at least 10 ms. No model-case met that rule. All 800 paired outcomes met quality/correctness requirements. Two of 70 validation cells exceeded the MAD threshold; none fell below the timing floor. Unfiltered averages retain all outcomes, including unstable cells. The small signed means do not support equivalence or reliable sub-percent effects.

Frozen benefit and uncertainty policies selected zero calls. A random policy at the same rate therefore also makes zero calls: matching it is not evidence of learned selection value. Adapted BORA/rank policies call in some cases; their small positive/negative averages do not demonstrate a robust deployable advantage. The oracle remains a nondeployable upper reference.

## What the mechanism check adds

This is a post-outcome diagnostic using only already acquired observations, not a new policy or causal explanation. Sixteen of 20 model/sequential pairs selected the same configuration, so differences between those pairs are timing variation of the same setting. Both model arms retained a prefix setting in all five hnswlib cases; sequential, GP and random controls did too. Adaptive improved its noisy search minimum in one case. Thus this ANN task has little *observed* continuation headroom at the chosen checkpoint; the global optimum is unknown.

For ripgrep, sequential/adaptive improved their search incumbent in two of five cases. Qwen also improved in two, while Smol improved in none. Mean acquired search improvements were small (about 1.7% for sequential, adaptive and Qwen), below the separately predeclared practical-win margin. These are search minima and not fresh-validation effect estimates.

Projection and repetition further narrow the claim. On ANN, 21/35 Smol and 24/35 Qwen evaluated proposals needed projection; duplicate proposal counts were 21/35 and 23/35. The collector resolved duplicates and charged the resulting unique evaluations. On text search, projection counts were 17/35 and 9/35. A representation ablation could test whether these restrictions suppress useful proposals, but choosing a new prompt on these outcomes would be exploratory. The data do not establish that an unrestricted, larger, or differently prompted model would fail.

## Reproducibility and cost

All 1,258 tests passed (14 dependency deprecation warnings). Separate replay reconstructed text counts and ANN exact distances, validated all outcomes and shared prefixes, independently checked 70 GP choices, verified model provenance and all 210 fresh validations, and rejected objective/output/identity corruptions. Ten report/data/figure artifacts reproduce byte-identically. Figures were visually inspected. These are internal checks, not external replication.

Collection took 330.818 seconds end to end (331.046 seconds including driver bookkeeping), within its 1,800-second cap. Both servers exited normally. Model calls observed 10,071 input and 919 output tokens, with no unknown usage, retries or fallbacks. All branches, admission failures, reference construction and compilation are research costs. The initial reference-preparation time is unknown and remains so. Estimated one-branch deployment cost is separately labeled; no real deployment, energy measurement or paid/cloud inference occurred.

## Claims suitable for discussion

A defensible claim is: under these fixed small-model, representation, checkpoint, budget and workload conditions, calling the model did not reliably buy a practical improvement beyond cheap classical continuation. Historical studies and this native study offer evidence for that bounded claim, but different budgets, margins, sources and measurement designs must be reported separately rather than pooled into one significance test.

Still untested are independent-host replication, a broadly sampled application population, production-scale inputs, the full original comparison methods, and model/prompt generalization. The historical controller learned a 20-search target whereas this native target is 17 search plus three validation outcomes. There are only two new independent lineages; repeated seeds cannot repair that limitation. The small fixed tasks and lack of observed headroom are especially important threats to generalization.

**Highest-value next action: independently replicate a frozen application experiment on another host, including its raw correctness checks and fresh validations.** The existing one-host result is now reproducible internally; further local seeds do not supply external reproducibility. A follow-on prospective workload cohort should also include realistic larger workloads, with source/correctness/feasibility admission fixed before LLM gains and a development-only checkpoint/representation study. Do not hunt until a positive case appears. A bounded negative empirical paper is a reasonable direction for discussion with Tim Menzies, with these limitations explicit; no contact or submission has been made.

Evidence: [paired report](apps_v163.md), [feasibility report](apps_feasibility_v163.md), [source audit](source_audit_v160.md), [protocol](protocol_v163.md), [resume status](../STATUS.md), [post-outcome diagnostic](../results/v163_native/representation_diagnostic.json).
