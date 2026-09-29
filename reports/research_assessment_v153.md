# Research assessment after V149–V153

The evidence now includes a new real native system, richer controller comparisons and an independent audit that caught and corrected an analysis bug. It still does not demonstrate a useful transferable benefit-aware router. We have a reproducible negative/mixed empirical result, not grounds to certify Q2 suitability or promise acceptance.

## What was established

V151 analyzed the existing 70 paired cases per model using nested group folds and four fixed predictors: original ridge, richer 18-feature ridge, depth-two tree and RBF kernel ridge. It fitted preprocessing, thresholds and model selection only inside development folds. With eight execution-engine groups, the selected SmolLM predictor made one useful call: equal-group mean gain +0.00754%, missing nine other useful cases and selecting no joint >1% win over sequential and adaptive controls. When related Spark/Hadoop cases share one ecosystem group, both selected predictors make zero calls. The richer features/nonlinear models did not produce robust selection. This is retrospective exploration of exposed data, not an independent confirmation.

V150/V152 executed 40 correctness-checked native Memcached feasibility probes. Short probes failed the predeclared 1% relative-MAD noise screen. A separately frozen, longer workload passed the unchanged screen. Both results remain visible. This is an amendment based on feasibility evidence, not an untouched holdout.

V153 then collected 400 real native evaluations and ten real local-model responses across five seeds and seven continuation arms. Its B20 budget explicitly reserves three acquisitions for fresh validation: ten shared prefix measurements + seven new search settings + three fresh measurements of the chosen incumbent. All 35 choices were sealed before randomized validation. Every native measurement passed fixed-work response/counter checks. One server needed the configured forced-shutdown fallback after its correct measurement; it was reaped and retained in reliability logs.

| Model | Mean gain over sequential | Mean gain over adaptive neighbor | Joint >1% wins | Benefit-controller calls |
|---|---:|---:|---:|---:|
| SmolLM3-3B | +0.0881% | -1.3495% | 0/5 | 0/5 |
| Qwen3-8B | -0.4188% | -1.8655% | 0/5 | 0/5 |

The tiny positive SmolLM mean is not persuasive evidence of optimization benefit. Six of ten model/sequential pairs selected identical configurations; their timing differences cannot represent configuration-selection improvements. Seven of 35 validation arms exceeded 1% relative MAD, with a maximum of 4.665%. Five seeds are one system group, not five independent systems. Neither model had a joint practical win, and the frozen benefit routers selected no calls. The original hypothesis remains unsupported in this setting.

## What verification changed

Independent replay rejected V149 because Spark/Hadoop short case IDs collided. V149 is explicitly invalid and excluded; its outputs and failure logs remain for audit. V151 qualifies keys by engine family, adds a collision regression test, and reruns the same fixed analysis. It preserves all original source experiments. Two later verifier-only issues—roundoff at an exact tree split and an assumption that every reaped native server exited zero—were corrected without altering experimental inputs or measurements. The raw logs retain both initial verifier failures and successful checks.

The final suite passed 1,165 tests with 14 dependency warnings. Independent replay checks the 140 historical model cases, 30 outer folds, all 40 feasibility probes, all 400 new native acquisitions, exact continuations/projections, ten genuine model responses, predecision seals and charged validation. Semantic corruption checks reject four router, six feasibility and three paired-study mutations. Reports, JSON and scientific figures regenerate byte-identically. These checks establish internal reproducibility, not independent-host replication or upstream full regression coverage.

## Costs and scope

This continuation adds ten model starts, 440 native evaluations (including 105 charged validation measurements), and 2,436,165 retained source/document bytes. V153 itself takes 636.533 seconds under its 1,800-second cap. Both models are already pinned local Q4_K_M weights; there are no paid requests, cloud resources or new weights. Actual research cost includes both models, all controls, feasibility and previous development. Estimated deployment uses one chosen continuation at B20 and at most one request; observed time/token estimates do not establish dollar or energy savings.

The coherent recorded-table cohort remains eight engine families, 70 cases per model. Native Memcached is a ninth engine family in the broader evidence, but its 17-search-plus-three-validation target differs from the older 20-distinct-label target. Do not silently pool those results. Native training transfer also changes outcome noise and utility. Memcached was feasibility-explored before paired collection, and all existing results are now exposed development evidence for future revisions.

The focused original-paper audit in [novelty_audit_v153.md](novelty_audit_v153.md) finds closer conditional-LLM optimization work, notably BORA and LB-MCTS. General uncertainty/reliability-aware invocation is not novel by itself. No direct implementation comparison against those methods has run, and their full iterative algorithms cannot be represented by an unlabelled reuse of our single-call cache. SNAP2 adaptations must retain their existing attribution; this native workload is also an adaptation, not an owner benchmark replication.

## Priority for the next research cycle

**Implement and verify explicitly mapped checkpoint adaptations of the closest uncertainty/reliability baselines, then freeze their comparison for a new independent-family cohort.** Use current data only for exploratory diagnosis; preserve failures and every policy, and do not claim a post-hoc winner is confirmed. A strong negative paper would need a clear reason these failures matter, an adequate strongest-method comparison, and enough independent systems to bound the claim. A new positive method would additionally need prospective selective benefit beyond never-call, strong classical continuation and matched-rate random. More unchanged batches or more seeds alone do not resolve these gaps.

The bounded V149–V153 work is complete and all servers are stopped. No resource or permission blocker is pending. See [next_experiment.md](next_experiment.md) for priorities and [../STATUS.md](../STATUS.md) for exact evidence and safe replay commands.
