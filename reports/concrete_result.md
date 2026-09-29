# A concrete pilot result: apparent LLM gains can come from a model-free selection rule

**In all 15 direct-selection cases, the real local LLM chose exactly the first ten displayed candidate IDs. Those choices and their recorded optimization outcomes are reproducible without a model.** Although average loss improved over the adaptive classical continuation, this experiment does not demonstrate useful learned ranking. The earlier held-out experiment also did not demonstrate benefit-aware routing advantage. This is a bounded negative methods result suitable for review, not a claim that LLM optimization generally fails.

## What was actually executed

The repository implements paired software-configuration optimization with a ten-evaluation classical prefix and twenty-evaluation total per branch. Corrected initial smoke runs covered three software systems and five fixed seeds. A subsequent six-family run collected 30 real-model continuations and evaluated a development-trained, sealed controller on three held-out families. Those test families were never used to fit its thresholds. The later mechanism experiments use only the three development families: MySQL, lrzip and Brotli.

The final direct-selection experiment (V8) completed 45 branches: 15 real LLM continuations, 15 uniform-selection controls and 15 static classical ranking controls. Each restored an identical saved prefix and acquired ten more outcomes. All three arms received the same twenty-row shortlist, built from features and acquired labels only. Candidate display order was shuffled independently of ranking. The pinned Qwen2.5-0.5B-Instruct model ran locally on CPU/float32 with greedy constrained decoding. Raw responses, tokens, masks, prompts, source labels and costs are retained. No model outputs were fabricated.

## Why the favorable score is insufficient

Across three development systems, averaged equally after averaging seeds:

| Continuation | Mean normalized loss, lower is better | Evidence type |
|---|---:|---|
| Adaptive classical | 0.015580 | Previously measured paired continuation |
| Uniform shortlist | 0.012250 | Exact retrospective expectation over every possible ten-row subset |
| Static shortlist ranking | 0.011337 | Newly measured control |
| Local LLM | 0.010232 | Newly measured continuation; all choices equal first displayed half |

The observed LLM gain over adaptive classical was 0.005349, with two material improvements and zero material harms at the frozen .02 margin. Both material improvements occurred in MySQL. Smaller deteriorations are retained; zero material harms does not mean every case improved. The LLM's extra realized advantage over uniform expectation was 0.002018. That difference is **not evidence of learned selection**: every observed model response is the same positional rule, with candidate identities randomly assigned to those positions.

To quantify the model-free reference, the new V9 analysis independently enumerated **all 184,756 ten-of-twenty subsets for each of 15 cases**, checking a combinatorial formula against every outcome. Uniform shortlist selection already has an expected gain of **0.003330** over the adaptive classical baseline. In every individual case, a random subset has **at least 50% probability** of matching or beating the observed model loss, with ties included. Expected material benefits from uniform selection total 1.484 across these fixed cases; the observed LLM had two. These are conditional finite-pool calculations, **not p-values, confidence intervals, 2.77 million new experiments, or evidence about unseen systems**.

The distribution calculation is explicitly post-hoc and separate from measured data. It reads recorded full-table targets only in the offline evaluator, acquires no labels for an optimizer, makes no model calls, and changes no prompt, shortlist, threshold or treatment. It does not prove what the model would do under untested order permutations. The observed first-half equivalence is exact; claims about future behavior remain untested.

![Exact retrospective reference alongside measured arms](../results/v9_analysis/exact_reference.png)

## Answer to “When is the LLM worth calling?”

**For these 15 recorded candidate-selection decisions, the model calls contributed no selections beyond a trivial first-half rule.** Removing the calls while reproducing that rule would reproduce the same chosen rows and recorded outcomes. This is a retrospective substitution, not a prospectively evaluated policy. It would avoid those requests; replacement-code runtime and behavior on new cases were not benchmarked. The historical inference cost was still paid in local computation: **15 calls, 23,930 input tokens, 300 output tokens, 28.661 seconds of request wall time**, plus 3.800 seconds startup. Actual V8 research collection cost was 450 new target accesses; hypothetical deployment of one branch for all cases would use 300 logical accesses including prefixes. External spending was USD 0.

For the original routing question, the strongest held-out result remains V6: 2/15 material benefits and 3/15 harms from always escalating; mean loss .074581 versus .061505 for never escalating. The benefit-aware and uncertainty-only controllers both chose zero escalations, yielding no demonstrated selection advantage. The hindsight oracle is nondeployable. Three development and three held-out families are too few to support broad learned-router conclusions; repeated seeds do not change that group count.

The preceding V7 ablation prevented copies of observed configurations but did not materially improve optimization. V8 then removed projection by selecting existing rows, exposing a positional response rule. Together, these results motivate checking whether a continuation makes useful content-sensitive decisions **before** spending heavily on router training data. This is an incremental methods observation, not a verified novelty claim or a successful replication of SNAP2's much larger model.

## Evidence, limitations and one next action

**77 tests pass.** The whole-pilot audit replays the corrected classical and paired states, verifies source and model hashes, checks every model token against its recorded constraint, recomputes all V6 prefix-only features, refits only development data to reproduce the sealed coefficients/thresholds, and reproduces all seven held-out policies. It preserves old verifiers' historical ledger checkpoints and separately checks the unchanged current ledger. Details: [completion audit](completion_audit.md).

Reproduce the current evidence checks from the project root:

```sh
PYTHONPATH=src .venv/bin/python -m pytest -q
.venv/bin/python scripts/verify_pilot_completion.py
```

Exact-analysis specification/code: `reports/protocol_v9_analysis.md`, `src/escalation/selection_null_v9.py`, `scripts/analyze_selection_null_v9.py`. Numerical evidence: `results/v9_analysis/summary.json`, `cases.csv`, `exact_distributions.json`; independent enumeration assertions and actual execution output: `artifacts/study_v9/analysis.log`. Figure regeneration: `scripts/render_selection_null_v9.py`. Analysis consumes recorded runtime but no inference allowance; its completed-output guard prevents silent overwrite.

Scope is limited by a tiny single model, constrained greedy output, binary empirical features, one target/budget, public-table contamination uncertainty, only three development groups, and adaptive development follow-ups. The exact SNAP2 artifact was not established; the optimizer and changed-model experiments are labeled adaptations. Original V1/V2 schema issues and failed requests remain documented rather than silently repaired or pooled. Source audit, licenses and versions are retained.

**The next research action is a predeclared candidate-order permutation test against first-half and uniform controls, before a broader router study.** That would require new model allowance; current 128/128 follow-up requests are exhausted. Stronger models, new orderings, empirical nonbinary tasks and a credible untouched-system routing evaluation remain untested. There is no basis to promise that the benefit-router hypothesis will succeed. The current repository does provide a concrete, reproducible finding to discuss with Tim; nothing has been emailed, published, pushed or submitted.
