# Research assessment after V115

The study now has a stronger, reviewable **negative-result contribution**, but it has not demonstrated a useful benefit-aware router or established Q2 readiness. This continuation added real sampling replication and a single executable classical control; it did not add independent software groups.

## New empirical evidence

| Question | Actual experiment | Finding |
|---|---|---|
| Was the earlier result peculiar to one stochastic answer? | V114: 36 new Qwen3-8B requests, three sampling seeds for each of 12 fixed prefixes across six exposed groups; 360 charged recorded outcomes | All answers valid; zero >=5% wins over both original strong controls. Four prefixes changed selected sets, but only two changed final objectives. |
| Does the comparison require deploying two classical continuations and choosing their best outcome? | V115: one fixed alternating batch/sequential 3NN continuation, ten new evaluations per prefix; 120 charged recorded outcomes | Against this single B20 control, LLM outcomes had 9 wins, 15 ties and 12 losses; largest win 3.34%, none >=5%; group-first mean -2.25%. |
| Are small native runtime effects trustworthy here? | V113: 90 fresh confirmations and 270 independently certified physical solves | Five of eight equal-configuration contrasts appeared different by >=5%; native effect magnitudes remain qualified. No new native measurements in V114–V115. |

V114 mean gains were -2.67% against batch 3NN and -6.45% against sequential 3NN. No joint benefit classification changed at the fixed 5% margin across the three samples. This supports persistence of the observed negative result under the tested sampling seeds, not proof that all possible outputs or models fail. Two optimization seeds and three generation seeds per prefix are not additional systems.

V115 addresses a real interpretation issue: “better than both separate controls” is a conservative screening criterion, not an automatically deployable best-of-two reference. Its alternating portfolio is executable within one B20 budget. It was specified after inspecting V114 and must remain exploratory. The portfolio sacrifices some constituent-control quality; all original comparisons remain. Seven LLM replicas beat it by at least 2%, so the result is not “LLMs never improve anything.” No threshold was lowered to select a positive headline.

## Defensible paper direction

A scoped empirical replication/robustness study can report that the evaluated local-model procedures did not deliver the predeclared practical advantage over strong cheap controls on this corpus, even after changing model bundle, decoding/reasoning adaptations, and sampled answers. Separate these stages and their differing protocols; do not pool them as independent confirmatory trials. Strong classical controls, actual inference/validation costs, response reliability, and the distinction between different answers and different outcomes are central to the evidence.

That is different from the original proposed contribution of predicting useful escalation on unseen systems. The data still do not establish useful headroom for such a predictor at the fixed margin. A “never call” controller can be sensible here without being a novel or successfully learned routing method. Native timing diagnostics are a limitation and methodological observation, not a substitute for independent optimization evidence.

## Remaining scientific gaps

1. All six recorded groups were already exposed. No new untouched system-group test was created by this continuation, and no learned-router generalization claim is warranted.
2. One quantized model/runtime bundle and one host cannot settle the value of larger models, different interfaces, or sufficiently different optimization tasks. Prior owner source audits still label the method an adaptation, not exact SNAP2 replication.
3. The recorded tables preserve their original measurement and provenance limitations. Native V113 timing variation cannot be cured by relabeling table replay as fresh software execution.
4. Three sampled answers per prefix cannot establish calibrated benefit probabilities or formal reliability guarantees. Positive/negative classes at a fixed practical margin are not population risk bounds.
5. Novelty and venue suitability require technical review against the verified related work. More same-corpus seeds alone do not establish journal readiness.

## Next action

The highest-value empirical next action remains **independent validation**, rather than another prompt or seed search on these exposed groups. The concrete ready-to-run resource is the fixed-incumbent packet at `output/v113_replication/`, requiring a second quiet CPU host to test native measurement portability. It needs no model or GPU; independent-host execution is still untested and no access has been provided. For a recorded-data-only paper claim, an additional independently admitted software-system cohort would address generalization instead; candidate outcomes must not guide admission.

Before expanding collection again, use this assessment, the V114/V115 reports and their raw traces for a technical review of the narrower negative-study contribution. Nothing has been emailed, uploaded, published, or submitted. Acceptance and a journal quartile cannot be guaranteed by an agent or inferred from passing tests.
