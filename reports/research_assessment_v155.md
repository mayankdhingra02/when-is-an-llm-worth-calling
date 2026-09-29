# Research assessment after V154–V155

We now have a more credible negative comparison: within this small-model, fixed-checkpoint setting, useful LLM exceptions do not translate into useful uncertainty/reliability-based selection. The new work tests both published-rule adaptations and a Gaussian-process continuation. It does not establish a successful benefit-aware method, full published-method superiority, or Q2 acceptance/readiness.

## New experiments actually executed

V154 implemented and executed two explicitly mapped checkpoint adaptations on the 140 provenance-checked historical model-cases (70 per model). A BORA-inspired rule combines plateau and GP uncertainty; an LB-MCTS-inspired rule uses cross-validated surrogate ranking reliability. Their full algorithms, prompting and iterative behavior were not executed. Every departure and both fixed kernel settings are documented in the frozen protocol. No historical model output was replaced or fabricated.

With seven ecosystem groups (Spark/Hadoop together), the primary BORA-inspired rule calls 14/70 cases per model and loses 3.1021% for SmolLM and 3.2476% for Qwen relative to sequential continuation. The rank rule has 23.95 expected calls and loses 1.4361%/1.4877%; one fixed outcome-independent randomization calls 23 and loses 2.8390%/2.8562%. Both underperform the corresponding matched-rate random expectations. Development-calibrated rank and GP-uncertainty thresholds select zero calls, as do both saved benefit predictors. Expected values are mathematical policy averages over two real outcomes, not newly generated traces or fractional measured calls.

There is a concrete small-budget mismatch: 50/70 prefixes lack enough post-initialization updates for BORA's default plateau length. A separately named capped-history diagnostic increases calls to 46/70 and worsens average quality. The fixed GP uncertainty remains a feature-geometry signal; four of 350 two-point rank-validation folds are undefined and receive the declared neutral value. These findings identify limitations in the adaptations rather than proving the complete prior methods fail.

V155 executed 140 intended GP expected-improvement continuations from the same prefixes: two predeclared fixed kernels, ten new labels per arm, 1,393 charged acquisition attempts. 139 arms completed. One sensitivity arm encountered the known empty Spark TPCH source duration on its third acquisition; it remains unscorable, with seven slots unattempted. All 70 primary-kernel arms completed. No new LLM request, model download, native execution or cloud resource was used.

| Primary seven-ecosystem comparison | SmolLM3-3B | Qwen3-8B |
|---|---:|---:|
| Mean LLM gain over GP-EI | -2.7741% | -3.0585% |
| Cases with >1% benefit over GP | 5/70 | 4/70 |
| Cases with >1% harm against GP | 29/70 | 34/70 |
| Joint >1% wins over GP and adaptive neighbor | 2/70 | 1/70 |

Both models lose on average in every primary ecosystem group against this GP. GP itself loses 2.1945% against sequential 3NN and 0.1423% against adaptive neighbor in equal-ecosystem means. Hence GP is a useful extra comparator, not a universally stronger baseline. The evidence supports keeping strong cheap controls; it does not support choosing whichever comparator makes an LLM look best. The sensitivity's full-cohort mean remains null because of the missing source cell; its known wins/harms and complete group means remain visible without dropping the failed case.

## What this adds to the previous result

V151 had already shown that richer benefit predictors' tiny apparent gain disappeared when related Spark/Hadoop systems were grouped together. V153 supplied 400 actual native Memcached evaluations and ten real model calls, but no model won jointly over sequential and adaptive by >1% in any seed. It also exposed same-configuration timing differences and validation noise. V154–V155 show that the negative evidence extends to additional uncertainty/reliability heuristics and a different classical optimizer, under precisely limited adaptations.

The coherent historical cohort has eight engine families/seven ecosystems, 70 cases per model. Seeds and application variants are dependent. The native Memcached 17-search-plus-three-validation design remains separate. Do not sum these heterogeneous arms into a larger confirmatory dataset. All inspected families and this continuation's comparisons are exploratory evidence for any next design.

## Evidence quality and remaining gaps

1,190 repository tests passed with 14 dependency warnings. V154 independently replays mixed-kernel posterior calculations, folds, probabilities, calibration and aggregate quality, rejecting three semantic corruptions. V155 checks the source acquisitions, EI-optimality, arm budgets and comparisons separately; two solver-level near ties are retained with exact EI gaps in its replay receipt. Both reports/JSON/PNG/SVG regenerate byte-identically and figures were visually inspected. Latest replay receipts and the evidence seal are in artifacts/study_v155. This is internal reproducibility, not external replication.

The narrow potential contribution is an empirical boundary result: low-cost local-model escalation can have rare benefits while standard prefix uncertainty, plateau, rank reliability and simple learned benefit rules fail to select them reliably across systems. Claiming universal uselessness of LLM optimization would be unsupported. Quantization/model family, batch output representation, the B10/B20 budget, fixed kernels, source noise, public-data contamination, prior outcome exposure and small independent-group count limit the claim. Full original BORA/LB-MCTS runs and tuned GP hyperparameters are not covered by these adaptations. There is no formal risk or non-inferiority guarantee.

**Most important next action: freeze this comparison set and evaluate it on several additional independent software families selected without seeing gains.** The missing requirement is new independent evidence, not another round of tuning against these outcomes. A prospective cohort should retain the strong cheap controls, the mapped adaptations, one fixed benefit rule, both pinned models, complete failure denominators and charged validation where native noise requires it. Admission should use source schema/licensing/correctness, not expected model success. Do not present the current exploratory controller comparisons as held-out confirmation or promise a quartile outcome.

Reports: [controller adaptations](controllers_v154.md), [GP continuations](gp_v155.md), [previous native result](native_study_v153.md). Exact commands, budgets, failures and resume instructions: [STATUS](../STATUS.md).
