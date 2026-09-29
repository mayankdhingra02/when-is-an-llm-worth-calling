# Limitations that bound interpretation

- Only three independently named systems, with two development groups and one held-out smoke group. Repeated seeds are not independent systems; learning a router here cannot establish generalization.
- All selected inputs are binary and each table has only one minimization objective. Multi-objective behavior is unit-tested but not empirically evaluated.
- Objective “evaluations” read old recorded labels. No Apache, SQLite or x264 software was executed; historical measurement cost and repeatability are unknown. The underlying workload/hardware versions are not specified in the selected CSVs.
- Paper-based centroid and LLM adaptations differ from exact SNAP2/EZR: acquired-only min/max normalization, inclusive budgets, explicit state isolation, small Qwen model, greedy generation, array JSON format and declared fallbacks. No claim of upstream numerical reproduction.
- Strict parsing measures one specific prompt/model/interface combination. Format failures do not prove that the same model with constrained decoding, a revised prompt, or a stronger model cannot optimize. We intentionally do not repair the parser after inspecting responses.
- Fallback continuations inherit classical behavior. Equal scores under fallback say nothing about semantic LLM optimization ability or quality equivalence of successful LLM proposals.
- Model pretraining exposure to these public tasks is unknown. Dataset names are not needed for router features, but semantic option names are given to the local model.
- Greedy inference lacks sampling randomness; seeds control classical initial ordering only. Metal/torch numerical determinism across hardware/software revisions is not guaranteed.
- Model startup and collection are instrumented locally. Electricity, hardware depreciation and exact network transfer charges are not measured. External experiment API spending is zero; that does not mean model runtime or Codex usage is free.
- Policies replay paired traces retrospectively; modeled deployment costs are not a separately timed end-to-end deployed service. The hindsight oracle is never a deployable router.
- If the request cap prevents held-out pairs, their absence must block a primary held-out router comparison. Completed development pairs cannot substitute for missing held-out evidence.
- The literature audit verifies load-bearing primary methods and artifacts, not comprehensive novelty. No reviewer acceptance or publication claim is supported.

## Follow-up corrections

The SQLite schema mistake invalidates full-schema interpretations of v1/v2 SQLite results and routers trained on them. A new explicit-manifest gate and regression test protect the corrected v3 representation. See schema_erratum.md; historical successful tests were insufficient to catch that mistake.

v3 uses five candidates per call and two continuation calls, with the model generating binary strings under token constraints. This removes syntax failures by construction and reduces punctuation generation overhead, but also changes the intervention relative to SNAP2's two-candidate batches. All nonconstant bit choices still come from real model logits; constrained validity alone is no evidence of optimization ability. v3 is exploratory after v1 and v2 inspection, and no outcomes are pooled across these treatments.

## V6 expanded smoke

V6 adds six new families with five seeds each, three development and three held-out. This still gives only three independent held-out groups. A one-batch ten-proposal interface and CPU execution differ from v3's two batches and MPS, so versions do not isolate dataset/model effects. All measured v6 feature tables are binary; finite-domain generality was tested synthetically only. Single-target runtime can favor reduced output quality/size settings. Original workload-summary discrepancies are retained in reports/admission_v6.md.

Both trained controllers selected zero held-out calls, making rate-matched random also select zero: equality here is not proof of useful prediction. The real model produced 279/300 exact copies of original prefix configurations. Projection rescued evaluation validity but largely determined subsequent search. That post-hoc mechanism diagnosis cannot establish an improved treatment without a new development-only experiment. The six v6 families are now exposed and cannot serve as untouched test data after adaptive changes.
