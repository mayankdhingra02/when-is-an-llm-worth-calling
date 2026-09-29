# V48 — Controlled development diagnostic finds strong display-order sensitivity

Completed 2026-09-25. This is a real SmolLM3-3B Q4_K_M inference diagnostic,
not a synthetic-output experiment and not an optimization-quality evaluation.
The full protocol, prompts and analysis were frozen before model generation.

## Main finding

For the standard candidate display, removing the acquired performance losses
left the selected configuration set unchanged in **17/18** representation/prefix
pairs: 9/9 symbol prompts and 8/9 actual-value prompts. Reversing candidate display
while holding configuration-to-ID mapping fixed changed the selected set in
**14/18** loss-present pairs: 7/9 for each representation. The mean selected-row
overlap under display reversal was only **22.2%** for each representation.

The original symbol prompt followed the first ten displayed candidates in all
nine loss-present baseline cases AND all nine ID-rotation cases. Rotating arbitrary
IDs while preserving displayed configuration order left its selected configurations
unchanged in 9/9. This distinguishes strong display-order dependence from a simple
rule of always choosing numerically lowest IDs. V47 alone could not separate them.
For actual-value prompts, mean overlap after ID rotation was 75.6%; switching to
numeric settings under named columns did not reliably remove the problem.

These statements concern sets of underlying configurations, after undoing each
ID mapping. A changed output string alone was never counted as instability.

Both representations **failed the predeclared screen**: neither had baseline
loss-removal set changes in two seeds within each of two families; neither achieved
>=80% mean row overlap under both loss-present order interventions. This screen
was a necessary development check, not a sufficient condition for useful search.

The model is not completely insensitive to labels: over all three presentation
contexts, loss removal changed 10/54 matched sets. The effect interacts with
presentation. Do not generalize baseline 17/18 invariance into a claim that the
model never uses observed losses. Each of the nine acquired prefixes contains ten
distinct losses spanning its acquired-only normalization range 0..1, so baseline
invariance is not due to constant observed labels.

## Design and scope

Original development families only: MySQL, Brotli and lrzip, with seeds 11, 37, 71.
The seeds are the first/middle/last of the original fixed five, selected before
new outputs. Nine saved V6 ten-observation prefixes and their V8 twenty-candidate
pools. No V41 transfer families or potentially untouched registry systems used.

Full factorial: two representations (original symbol JSON; table with decoded
numeric settings and feature names), losses observed or withheld, and three
presentations (baseline; reverse display with IDs fixed; rotate IDs by ten with
feature display fixed). Thus 108 continuations, each choosing ten distinct IDs.
The actual settings are decoded exactly from the saved symbol/value mapping;
no invented explanations, feature units or replacement objective values.

The same pinned local model and V47 constrained decoder were used, greedy with
thinking off. There are ten one-token HTTP requests per continuation, with forced
newlines and exclusion of used IDs. This measures the combined model/interface/
decoder behavior; it does not isolate model weights or represent native unconstrained
chat. The direct-value table also changes serialization/instruction wording, so its
comparison is a representation bundle. Removing losses explicitly says they are
withheld, which is part of that intervention. Case order was shuffled with seed 48000.
No wording or condition was changed after responses. All 108 prompts passed preflight
before generation, ranging from 816 to 4,071 tokens, with a 20-token context reserve.

## All paired results

| Representation | Intervention | Context | Changed sets / 9 | Mean row overlap |
|---|---|---|---:|---:|
| symbols | loss_removal | base | 0 / 9 | 100.0% |
| symbols | loss_removal | reverse | 4 / 9 | 55.6% |
| symbols | loss_removal | relabel | 2 / 9 | 92.2% |
| symbols | reverse | observed | 7 / 9 | 22.2% |
| symbols | reverse | withheld | 3 / 9 | 66.7% |
| symbols | relabel | observed | 0 / 9 | 100.0% |
| symbols | relabel | withheld | 2 / 9 | 92.2% |
| values | loss_removal | base | 1 / 9 | 88.9% |
| values | loss_removal | reverse | 1 / 9 | 88.9% |
| values | loss_removal | relabel | 2 / 9 | 97.8% |
| values | reverse | observed | 7 / 9 | 22.2% |
| values | reverse | withheld | 7 / 9 | 22.2% |
| values | relabel | observed | 4 / 9 | 75.6% |
| values | relabel | withheld | 1 / 9 | 88.9% |

Overlap is intersection size divided by ten. High overlap is desirable under an
arbitrary presentation change; high overlap after removing informative observations
can indicate weak responsiveness. Neither directly measures optimization quality.
Three family groups—not nine seeds or 108 conditions—limit inference. No confirmatory
p-values or generalization claims are made.

## All ordering rates

| Representation | Losses | Presentation | Lowest-ten-ID sets / 9 | Fraction selected from first ten displayed |
|---|---|---|---:|---:|
| symbols | observed | base | 9 / 9 | 100.0% |
| symbols | observed | reverse | 2 / 9 | 77.8% |
| symbols | observed | relabel | 0 / 9 | 100.0% |
| symbols | withheld | base | 9 / 9 | 100.0% |
| symbols | withheld | reverse | 6 / 9 | 33.3% |
| symbols | withheld | relabel | 0 / 9 | 92.2% |
| values | observed | base | 7 / 9 | 77.8% |
| values | observed | reverse | 2 / 9 | 77.8% |
| values | observed | relabel | 0 / 9 | 97.8% |
| values | withheld | base | 8 / 9 | 88.9% |
| values | withheld | reverse | 1 / 9 | 88.9% |
| values | withheld | relabel | 0 / 9 | 100.0% |

## Actual collection costs and verification

- 108/108 real continuations complete; 1,080/1,080 generation requests complete.
- Zero failures, retries, fallbacks, new objective accesses or physical trials.
- Local runtime stage: 464.482s; summed request wall time:
 462.790s. Server exited cleanly; port 18474 no longer listening.
- 1,080 generated choice tokens. Forced delimiters are not generated tokens.
- 2,433,720 summed full-context input-token counts;
 244,344 actually evaluated prompt tokens reported by runtime
 counters after within-case prefix-cache reuse. First choices had zero cross-case cache.
- $0 external spending, no downloads. Hardware/electricity cost remains unmeasured.
- Cumulative follow-up requests including two V46 hardware calls: 1,732;
 including the original hundred-request stage: 1,832. There are 140 SmolLM3 generation sequences
 across V46–V48 (2 hardware fixtures, 30 V47 continuations, 108 V48 continuations);
 count HTTP requests explicitly rather than using continuation counts as requests.
- Recorded objective accesses remain 14,708; physical trials remain 1,274.

All factorial arms count toward research collection. A deployment would execute
one selected condition, not all twelve; no deployment savings or quality claim is
made here. Earlier ledgers are preserved rather than reset. V48's specific 1,080-
request allowance is consumed; its actual stage stayed inside 900 seconds.

Independent stdlib verification checked all 108 prompt transformations, 1,080 raw
request/response sequences, 126 paired sensitivities and both screening decisions.
Nine symbol/observed/baseline messages exactly match the original saved V8 messages.
It checks losses are removed only in withheld conditions, numeric settings decode
correctly, candidate mappings and permutations are correct, cache/budget invariants
hold, and selected-row overlap arithmetic agrees. It reads no raw target tables.
The full test invocation `pytest -q tests` passed 348 tests. Compilation and tests
were gated successfully before launch; unlike V47 there was no analyzer correction.

## Evidence and replay

Protocol: `reports/protocol_v48_sensitivity.md` and its 163-file freeze.
Prepared prompts/config: `artifacts/study_v48/`, `configs/study_v48.json`.
Raw runtime, preflights, requests, responses, choices: `results/v48_sensitivity/`.
Case-level and aggregate diagnostics, PNG/SVG: `results/v48_analysis/`.
Verification and test receipts: `artifacts/study_v48/verification.json`,
`artifacts/study_v48/tests_all.txt`. Runtime/model provenance is inherited from
V46 and byte-verified against frozen runtime inputs and GGUF hash.

Read-only replay, without new model requests or objective acquisition:

```sh
.venv/bin/python scripts/verify_sensitivity_v48.py
.venv/bin/python scripts/report_sensitivity_v48.py
.venv/bin/python -m pytest -q tests
```

## Limits and next decision

This is a stronger local mechanism result than V47's post-hoc ordering explanation:
controlled presentation changes cause large changes in this deterministic setup.
However, it is exploratory work on three development families and one quantized
model/runtime/decoder. There are no repeated same-prompt runs to quantify device
nondeterminism. Ordering bias itself is not claimed novel, and the study does not
establish utility equivalence of original benchmark configurations or eliminate
pretraining contamination. No held-out systems were newly exposed. No useful
benefit-aware routing result or Q1/Q2-readiness claim follows.

Do not run another version of this table wording on the same cases just to pass
its screen. The next decisive development experiment should separate the constrained
one-token decoder from native multi-token selection (optionally reasoning enabled),
with the same loss/order controls and explicit cost bounds. This tests whether
forcing immediate ID choices is the bottleneck. Only an intervention that passes
predeclared stability/responsiveness AND a separate classical-baseline quality
comparison should advance to independent-group evaluation. If it still fails,
consolidate the bounded negative finding and audit its novelty rather than chase
positive held-out scores. Nothing was published, pushed or sent.
