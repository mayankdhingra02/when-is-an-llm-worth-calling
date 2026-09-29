# V49 — native generation does not remove the observed selection failure

Completed 2026-09-25. Real local SmolLM3-3B Q4_K_M generations, using the exact
saved V48 symbol prompts and nine original development prefixes. The experiment
and analysis were frozen before new model output. No new objective values read.

## Concrete result

**All 53 valid native responses selected the same configuration sets as their
matched historical forced-ID responses.** One of 54 native cases was invalid.
All nine concurrently repeated forced-ID controls reproduced their original
mapped selections. Removing the grammar and forced newlines did not rescue the
observed behavior in this setup.

The failure was `lrzip_11_symbols_observed_base_native`: the raw output was
`id1`, `id2`, …, `id9`, `idA`, each on a separate line. These are not supplied IDs.
The frozen strict parser rejected it; no repair, retry, fallback or replacement
case was used. It counts in the 54-case denominator. There were no duplicate or
truncated responses, missing cases or transport failures. Native validity is
53/54 (98.15%), a descriptive three-family result, not a reliability guarantee.

For baseline loss removal, all eight valid pairs kept their selected sets;
the ninth pair is unknown because of the invalid endpoint. Reversing the display
changed six of eight valid loss-present pairs; the ninth is unknown. Its
family-mean overlap bounds are 22.2%–33.3%, far below the frozen 80% stability
threshold. ID rotation preserved all eight valid loss-present pairs (one unknown).

The predeclared screen FAILED: format validity and forced-repeat reproducibility
passed, but loss responsiveness and row stability failed. No benefit-aware router
was refitted or claimed successful. The observed matching does not prove that
grammar constraints never affect model behavior; one format difference occurred,
and this is one model, runtime and fixed prompting scheme with thinking disabled.

## Design and full denominator

Three development families (MySQL, Brotli, lrzip), seeds 11, 37, 71. Nine saved
ten-observation prefixes with identical twenty-candidate pools. Native factorial:
observed/withheld losses × baseline/reverse/ID-rotated display = 54 cases. Nine
additional observed/baseline controls repeated V48's forced one-token decoder.
The 63 cases were shuffled once with Random(49000). No new test systems exposed.

All messages, rendered chat-template strings and token lists matched V48 exactly.
Native generation used one unconstrained completion with a 128-token limit;
forced controls used ten requests, one ID each, excluding previously used IDs
and injecting newline delimiters. Both were greedy, seed 11, repeat penalty 1,
thinking off, context 4096, the same pinned GGUF and llama.cpp b11146 runtime.
Symbol prompts were chosen because they fit the unchanged context with the
larger output reserve; some actual-value prompts from V48 would not. No new
prompt wording, parsing repair or numeric-value condition was introduced.

Native generation still follows an instruction to output IDs only. It is not
reasoning-enabled generation, unconstrained natural-language planning, or native
configuration synthesis. Grammar, forced delimiters and request chunking change
together. Historical comparisons cover 54 matched cases; only nine forced cases
were concurrently repeated. No separate-device reproducibility claim is made.

## All sensitivity comparisons

| Intervention | Context | Valid pairs / intended | Changed valid sets | Overlap bounds |
|---|---|---:|---:|---:|
| loss_removal | base | 8 / 9 | 0 | 88.9%–100.0% |
| loss_removal | reverse | 9 / 9 | 4 | 55.6%–55.6% |
| loss_removal | relabel | 9 / 9 | 2 | 92.2%–92.2% |
| reverse | observed | 8 / 9 | 6 | 22.2%–33.3% |
| reverse | withheld | 9 / 9 | 3 | 66.7%–66.7% |
| relabel | observed | 8 / 9 | 0 | 88.9%–100.0% |
| relabel | withheld | 9 / 9 | 2 | 92.2%–92.2% |

Overlap is mapped configuration intersection size divided by ten. Bounds assign
unknown failed-endpoint overlaps the full [0,1] range and average first by family.
They are not statistical confidence intervals. Changed-set counts exclude unknown
pairs but those pairs remain in intended denominators. Valid-only family means
and all 63 pair records are saved in JSON. Three families are the independent
units, not 54 conditions or nine seeds. No confirmatory p-values are reported.

## Ordering and reliability

| Losses | Presentation | Valid / intended | Lowest ten ID sets | First ten displayed (valid only) |
|---|---|---:|---:|---:|
| observed | base | 8 / 9 | 8 | 100.0% |
| observed | reverse | 9 / 9 | 2 | 77.8% |
| observed | relabel | 9 / 9 | 0 | 100.0% |
| withheld | base | 9 / 9 | 9 | 100.0% |
| withheld | reverse | 9 / 9 | 6 | 33.3% |
| withheld | relabel | 9 / 9 | 0 | 92.2% |

MySQL and Brotli each produced 18/18 valid native outputs; lrzip produced 17/18.
All 9/9 forced controls were valid. Within-native loss removal changes six valid
sets across the three presentation contexts; do not claim absolute label
insensitivity. V49's ordering results remain essentially those of V48 on valid
cases. No hidden target scores were used to choose or evaluate these outputs.

## Actual collection cost

| Mode | Cases | HTTP requests | Generated tokens | Full-context input sum | Runtime-reported actual prefill tokens | Request wall time |
|---|---:|---:|---:|---:|---:|---:|
| native | 54 | 54 | 1,090 | 51,729 | 51,729 | 103.568s |
| forced | 9 | 90 | 90 | 91,490 | 9,230 | 17.236s |

Total live stage: 121.836 seconds, including startup and cleanup; server exited
cleanly. All 144 authorized generation requests consumed; under the 900-second
cap. Generated tokens total 1,180, below the 7,002-token maximum. Native tokens
include model-generated separators and any runtime-counted termination tokens;
forced delimiters were injected and are not generated tokens. First-request
`timings.cache_n` was zero for every case. Only forced controls reuse within-case
prefix cache. No request retries, downloads, objective acquisitions or paid spend.
Hardware/electricity cost remains unknown. No process remains running.

Full-context sums are not actual model prefill counts. Research cost includes
all 63 counterfactual conditions; deployment would run one selection. Native uses
one request versus ten, but this is not evidence of quality-preserving cost savings.
The two aggregate timing rows have different condition mixes and denominators.
No standalone deployment latency comparison is inferred from them.

Cumulative follow-up requests, including two earlier hardware fixtures: 1,876;
including the initial 100 requests: 1,976. Recorded objective accesses remain
14,708 and physical trials remain 1,274. Earlier ledgers are unchanged.

## Verification and artifacts

Independent stdlib replay passed: 306 frozen input hashes; 63 unchanged rendered
prompts; 144 raw request/response sequences; strict parser decisions; mapped
selections; 63 sensitivity pairs, family means, costs and screening decisions.
All 353 tests passed, both before and after collection. The PNG/SVG figure was
visually inspected. Synthetic parser tests are separate from measured logs.

The post-collection verifier initially checked the wrong runtime cache field:
`tokens_cached` describes the retained cache, while `timings.cache_n` records
reuse during a request. The verifier was corrected to the same first-request
check used in V48. Initial failure, original verifier copy and hash correction
are saved in `artifacts/study_v49/verification_field_correction.json` and sibling
receipts. No frozen collector, parser, analysis or measured output was changed.

- Frozen protocol/config: `reports/protocol_v49_decoder.md`, corresponding
  `.freeze.json`, and `configs/study_v49.json`.
- Prepared jobs, tests, collection log, server log, verification receipts:
  `artifacts/study_v49/`.
- Raw prompts, request starts, responses, parsed choices and cost ledger:
  `results/v49_decoder/`.
- All cases, pairs, summary, regenerated tables and scientific figure:
  `results/v49_analysis/`.
- Final post-collection hashes: `artifacts/study_v49/evidence_manifest.json`.

Read-only replay (no model calls or target-table reads):
```sh
.venv/bin/python scripts/verify_decoder_v49.py
.venv/bin/python scripts/report_decoder_v49.py
.venv/bin/python -m pytest -q tests
```
Preparation, collector and analyzer refuse implicit overwrite/restart. The model
was actually run locally; no Codex-generated choices were used as experiment data.

## Scientific decision and next action

The screen failed, so the predeclared stopping rule applies: end this branch of
prompt/decoder tweaking on the exposed cases. V49 weakens the specific explanation
that forced-ID decoding alone caused V48's ordering effect. It does not prove
that model weights, quantization, prompt semantics or task structure are the cause.
No new optimization gain, independent-system generalization or Q2 readiness follows.

The focused primary-source audit in `reports/novelty_boundary_v49.md` confirms
that option-order bias and first-token versus generated-answer effects already
have close prior work. Our reproducible controls support the software-optimization
study; those phenomena are not themselves new discoveries. V49 is not a replication
or refutation of the prior MCQ studies, which use different tasks and extractors.

**Next action:** audit benchmark configurations for equivalent application quality
and correctness, then freeze a utility-matched, independently grouped comparison
before further LLM optimization collection. Keep this failed selection adaptation
as a negative baseline. Larger/reasoning models and direct configuration proposals
remain untested; none is assumed to fix the issue. No new inference is scheduled,
and nothing was published, pushed or sent to anyone.
