# V42: the fixed shortlist leaves little room for escalation

**The 1.5B model finds the best available shortlist result in 28 of 30 cases, while batch 3NN already does so in 27.** Its weak V41 advantage is therefore not simply a failure to choose good candidates: there is little improvement available inside this particular shortlist. The stronger sequential baseline can explore beyond it.

This is a new **post-hoc diagnostic**, frozen after the V41 model results were inspected. It does not convert those exposed cases into a new held-out study, prove a successful router, or establish journal readiness. It changes the next experimental question from “Can we improve ranking within these shortlists?” to “Can the escalation intervention find useful configurations outside the cheap search's shortlist?”

## Exact random-selection comparison

The previously acquired V41 branches collectively cover every candidate in all thirty twenty-candidate shortlists. No hidden or new target was acquired. From those saved outcomes, compute the exact distribution of the best result after uniformly selecting ten candidates without replacement, retaining the same ten-label prefix. Each hypothetical arm still has twenty logical evaluations.

There are 184,756 possible subsets per case. The analytic order-statistic calculation agrees with independent direct enumeration of all **5,542,680 combinations** across thirty cases. These are computations on recorded labels, not millions of new optimization runs or LLM outputs. The 3,000 V41 outcome accesses that supplied coverage remain actual research cost; complete coverage is not free information available to a deployed optimizer/router.

| Real model | Exact expected relative gain over uniform selection | Cases attaining shortlist ceiling | Mean probability random matches or beats model |
|---|---:|---:|---:|
| Qwen 0.5B | -1.8872% | 15/30 | 94.31% |
| Qwen 1.5B | +1.0689% | 28/30 | 76.61% |

The larger model's family mean is positive in each of the six families against this uniform reference; the smaller model's is negative in each. This is a descriptive result on these recorded cases, not a population significance claim or a causal proof of model reasoning. The large tie probability reflects selecting half the shortlist and retaining an already good prefix. It is not contradictory to a positive mean gain, because rare improvements can affect the mean.

Expected gains average the **ratio for each random outcome**, not the ratio against the random outcome's mean. No candidate, family, seed, baseline or threshold was selected for favorable results. The conditional match probabilities are not p-values for thirty independent software systems.

## What even a perfect shortlisted selector could do

The ceiling uses the best of the fixed prefix and all twenty shortlisted candidates, so any ten-candidate selector can attain it by including a best candidate. The ceiling is outcome-informed and nondeployable. It is a diagnostic upper reference, not an LLM result.

| Reference | Cases with strict improvement possible | Equal ceiling/reference | Ceiling strictly worse | Mean ceiling gain if always used |
|---|---:|---:|---:|---:|
| batch_3nn | 3 | 27 | 0 | +0.1174% |
| full_sequential_3nn | 7 | 15 | 8 | -1.8207% |

Against batch 3NN, only three cases allow any improvement; even perfect selection's mean ceiling is just +0.1174%, compared with the actual 1.5B result of +0.1024%. Against full-domain sequential 3NN, perfect selection used on every case is bounded at −1.8207%, close to the actual −1.8356%. Thus upgrading the selector alone cannot make always-escalate competitive in this design.

**This does not rule out selective escalation.** Seven cases permit a better shortlisted result than full-domain 3NN; fifteen tie it and eight cannot match it. A router might choose useful cases, but the measured transferred router did not. These upper references use post-decision outcomes and must never become controller features or a policy claim.

Figure: `results/v42_selection_reference/shortlist_ceiling.png` (also SVG). All sixty model comparisons and sixty ceiling comparisons are retained in CSV and `summary.json`, including exact rational values and all thirty conditional distributions.

## Verification, cost and limitations

315 tests pass, including fifteen new tests for exact probabilities, ties, prefix clipping, direction reversal and expectation-of-ratios. The exhaustive verifier imports no optimizer implementation. The figure was visually inspected. Original V41 raw evidence, protocols, precommitted policies and review ZIP remain unchanged. V42 has its own 308-input exploratory freeze.

This analysis acquired zero new labels, made zero model calls and spent USD0. Charged computation: 2.187796s. Cumulative runtime: 2860.933003/3600s; model requests remain 290/290.

These are elementary finite-selection calculations, not a new theorem. They identify a limitation of this exact candidate-generation/selection design; they do not prove all LLM optimizers suffer it. The result depends on the saved prefixes, fixed twenty-candidate shortlist, nominal features, admitted subsamples and source benchmark outcomes. It does not validate equal application quality/security, larger/different model families, fresh systems, or a new predictive router. Novelty relative to prior optimization/algorithm-selection work remains to be established.

## Reproduce

```sh
.venv/bin/python -m pytest -q tests/synthetic tests/test_transfer_v41.py
.venv/bin/python -I -S scripts/verify_selection_reference_v42.py
.venv/bin/python scripts/render_selection_reference_v42.py
```

The one-shot analytic collector preserves `results/v42_selection_reference`; its exact procedure and source binding are in `reports/protocol_v42_selection_reference.md` and the companion freeze. This extension is not included in the existing V41 review ZIP, which remains unchanged.

**Next scientific action:** design and justify an escalation treatment that can change the candidate region, evaluated with equal functional utility and an independent development/test split. A larger model restricted to the same twenty candidates cannot remove this ceiling. First compare this specific diagnosis with prior work and review whether it supports the intended contribution; do not assume a new prompt, more seeds on these exposed cases or another batch of calls will deliver a journal-level result.
