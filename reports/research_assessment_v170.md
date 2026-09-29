# Research assessment after V169–V170

The new concrete result is a source-executed baseline comparison across six native implementations. Neither retained local model produced a robust >10% improvement over sequential 3NN or upstream EZR Bayes in these secondary comparisons. This strengthens a bounded negative finding about these models, prompts, budgets and workloads. It does not establish that LLM escalation is generally ineffective, that the methods are equivalent, or that the original benefit-aware controller works.

## What was added

Two prospectively bounded collection stages executed the unchanged acquisition functions from timm/ezr 0.9.4, commit `bfda80b3b797d142378f7fb8746c3485610fb17e`, with a documented checkpoint wrapper. Sixty new centroid/Bayes continuation arms cover Polars, XGBoost, cvc5, OR-Tools, ripgrep and hnswlib at five fixed seeds. Each arm uses the original ten acquired prefix labels, seven new configuration outcomes and three fresh incumbent validations. Unknown outcomes are absent from optimizer inputs. The original source and MIT notice are retained; source execution uses an existing hash-pinned Python 3.13.3 interpreter without installing anything globally.

All 60 new and 210 historical selections were fixed before randomized validation blocks. This collected **1,230 new objective outcomes and 2,460 native workload executions**, including 420 new search labels and 810 validation labels. Fourteen search outcomes received the predefined quality penalty; none was dropped. All 270 final validation cells were quality-valid. No new model calls, responses, downloads or retries occurred. The model selections derive from 60 historical real responses; this stage remeasured their configurations rather than rerunning inference.

## Findings and qualifications

The [per-implementation synthesis](ezr_synthesis_v170.md) retains all mean gains; stage comparison JSON files retain every case. Across the 60 model cases, no robust gain occurred against sequential or EZR Bayes and no model beat all five main classical comparators under the joint rule. This denominator consists of repeated cases, not 60 independent software systems; no pooled significance claim is made.

One exception matters: Qwen3-8B on XGBoost seed 37 improved by 22.683% against GP-EI and 20.893% against EZR centroid, passing the robust pairwise rule. It was worse by 1.550% against sequential and 1.187% against EZR Bayes. Reporting only the two favorable comparators would misrepresent the practical decision.

Four Polars validation cells failed the relative-MAD stability rule. Forty of the 45 OR-Tools cells had medians below the 10 ms floor. All remain in the unfiltered tables. The secondary robust rule requires a >10% gain, distinct configurations, valid quality, relative MAD <=5% and both medians >=10 ms; failure of that rule is not an equivalence test or proof of no benefit. The 10 ms floor is secondary for the older solver cohort and does not replace its original published-in-repository rule.

The source-baseline implementation gap has narrowed, with these explicit departures from a full original-method replication: injected saved prefix and order, start=10, seven additional acquisitions, typed raw features, one scalar loss and raw-loss incumbent selection. Source normalization, smoothing and the literal cached-rest-centroid behavior remain unchanged. We did not silently repair upstream behavior or claim a full SNAP2 replication.

## Why a journal-readiness claim remains premature

The research now has actual native execution, real-model provenance, meaningful cheap controls, cost records and reproducible negative findings. Those are reviewable contributions. A journal quartile is not a methodological acceptance threshold, and these results alone do not justify certifying the work as Q2-ready.

The main limits remain:

- All new measurements use one physical host. New EZR searches occurred later than historical model/control searches. Joint randomized revalidation reduces final-scoring timing differences but cannot remove temporal effects on search selection.
- Six implementations are not six independently sampled production workloads. The two solvers share constructed N-queens problems; Polars reuses the earlier DuckDB flight contract. Other real public inputs are compact and task-specific.
- These tasks were already exposed. The extension is secondary/exploratory even though its new collection protocol was frozen. Neither models nor routers gained a fresh held-out evaluation here.
- Both local models, their prompts and their proposal interfaces represent a narrow model sample. The learned controller has not demonstrated useful discrimination that generalizes to unseen software systems.
- Three validation observations per cell give limited noise characterization. Short-runtime floors, same-setting selections and quality constraints restrict interpretation.
- Same-source deterministic replay checks execution integrity; it is not an independent implementation or a second-host replication.

The defensible discussion topic is currently a reproducible study of when these particular small local-model continuations fail to justify their cost, with explicit isolated opportunities and comparator dependence. It is not a positive general-purpose routing result.

## Costs and verification

Actual new collection took 460.617 seconds across two separately capped 1,800-second stages. There were 300 unique historical prefix outcomes reused through 600 cached callbacks; those were not newly measured. The 630 extra validations of historical selections are research costs outside their closed B20 budgets. Existing model/source collection costs remain additional. Optimizer/bridge process CPU totaled 0.176132 seconds, excluding native children; it must not be compared directly to end-to-end model wall time as if they measured the same quantity. No new deployment, dollar saving or energy measurement is claimed.

All 60 source bridges exited successfully; collectors completed their full intended denominators. Replays checked source choices and separate native-output/quality calculations, rejecting value, native-output and configuration corruptions. The complete suite passed **1,325 tests** with 14 dependency deprecation warnings. Five V169 and seven V170 analysis/report/figure artifacts reproduce byte-identically without new acquisitions. Figures were visually inspected. Test counts demonstrate regression coverage, not scientific validity.

Evidence: `artifacts/study_v169` and `artifacts/study_v170`; raw traces: `results/v169_ezr` and `results/v170_ezr`; protocols: [V169](protocol_v169.md) and [V170](protocol_v170.md); replay: [instructions](reproduction_v170.md). V168 and all earlier results are preserved through the evidence-manifest chain.

**Single highest-priority next action:** obtain access to a second physical host and run a newly frozen replication of the paired application comparison, with all acquisition arms collected in the same campaign. No such access is established. A later successful-controller claim additionally needs an adequately sized, prospectively selected, system-grouped cohort with useful and harmful escalation cases; repeated local seeds cannot supply that evidence.
