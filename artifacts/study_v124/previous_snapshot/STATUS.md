# STATUS — V123 pointwise surrogate experiment complete

Resume here, then `reports/pointwise_v123.md`, `reports/pointwise_attribution_v123.md`, `reports/research_assessment_v123.md` and `reports/reference_surrogate_audit_v123.md`. No model server or native job remains running. V123's99-request/1584-allocated-token/30-acquisition stage is closed at its declared limits. Do not rerun create-once collectors or tune this adapter against these outcomes. The broader research hypothesis remains unsupported; this is completed development work, not a Q2-readiness claim or an external-access blocker.

## Latest actual result

Implemented and executed a different interface: Qwen3-8B Q4_K_M predicts a scalar loss for one actual configuration at a time, without candidate IDs/list in the prompt. Three exposed families were selected alphabetically (BerkeleyDB, Dune/HSMGP, HIPAcc), seed11 only, original saved prefix10 and20-candidate shortlist.60normal predictions,30loss-removal probes,9reversed-observation probes; all99real requests returned valid scalars. Choices and diagnostics were sealed before30new recorded acquisitions, ten per branch. Each logical arm remainsB20. All15historical comparator states share the exact prefix and preserve their old collection cost.

| Comparator | Mean relative gain | Wins/ties/losses |
|---|---:|---:|
| Same-pool batch3NN | +0.038% | 1/0/2 |
| Full-domain sequential3NN | -16.352% | 0/1/2 |
| Random full domain | -0.685% | 0/1/2 |
| Free first-ten | -0.251% | 0/2/1 |
| Single B20 classical portfolio | -0.096% | 1/0/2 |

**Frozen quality screen failed;0/3joint5%wins.** Loss responsiveness passed3/3families; all9order probes passed. The diagnostic checks are therefore insufficient evidence of useful ranking. Do not promote the tiny positive batch mean while hiding stronger controls. No router was fitted to this new adapter.

Post-hoc attribution was added after repeated zeros were noticed during collection; it changes no prompt, selection, outcome or predeclared criterion.54/60normal predictions were0.00: BerkeleyDB20/20, Dune14/20, HIPAcc20/20. All ten selected positions in each family came from a zero-valued tie. Fixed ID-order tie breaking exactly reproduced first-ten in two families; Dune's changed set lost0.754%against first-ten and47.344%against sequential3NN. This is descriptive evidence about this adapter, not causal proof that clipping, grammar or model size alone caused failure. The selected-only calibration uses already charged labels and is not full-table predictive accuracy.

## What actually ran and cost

-99new real local generation requests;0retries,0fallback branches,0missing output-token receipts.
-495reported generated tokens;1584allocated;130,274reported prefill tokens. Unknown older-stage usage remains unknown.
-553.493s model lifecycle,2.388s startup; peak sampled serverRSS7,383,220,224bytes below8GiB. Server exited0; independent process listing found none remaining.
-30new recorded acquisitions; original30prefix labels and15reference branches reused, not counted as newly collected or retrospectively free.
-Estimated deployment:20normal requests/320allocated output tokens per escalation, plus startup/rendering and10objective evaluations. Measured normal request totals per family were95.984s,75.292s and172.604s, interleaved with probes; these are not full cold-start deployment measurements.39probe calls are research overhead. No electricity/agent/dollar/native objective-time break-even claim.
-No model/package/source artifact downloads, paid/cloud inference, credentials, system-setting changes, publications, remote pushes or messages. A separate read-only owner-code web audit followed collection; web-provider transfer sizes are unobservable and not counted as zero network bytes.

## Verification and evidence

Protocol `reports/protocol_v123.md`; precollection freeze `reports/protocol_v123.freeze.json` covers287inputs (SHA25655663fb9809a3d36b61047d9636e14a84ee9b8205304cc38d72531d46e4426ac). Prompts/jobs/input freeze: `artifacts/study_v123/`. Raw templates,99request starts/responses, backend settings, tokens, ledger and server log: `results/v123_pointwise/`. Predictions, intervention pairs, sealed selections, charged source cells and paired states: `results/v123_analysis/`.

Independent replay verified all99requests and30source events, B20budget, actual feature serialization, acquired-only normalization, old comparator prefix identity and gains. All99returned backend prompts/seed/temperature/grammar/output limits/repeat penalties match sent settings. No extra inference or objective acquisitions during verification.

Precollection and final suites: **938passed**,14third-party deprecation warnings; final30.48s. New28synthetic tests cover poisoned unused targets/state, intervention isolation, numeric parsing/incomplete output, complete-score selection, ties, cap-before-network and charged transport failure. Fixtures remain outside measured aggregates. A missing source-path import was corrected before protocol freeze; no real request was affected. Matplotlib used a temporary cache because the home cache is unwritable; explicit temporary MPLCONFIGDIR was used for replay. No model/request/resource failure occurred.

Report, comparison JSON and scientific PNG reproduced byte-identically; figure visually inspected. Private package `output/v123_replay.zip` is736,788bytes with347hashed files and a standard-library `replay.py`; isolated Python replay passed99requests/30events. It checks saved evidence, not fresh inference or the complete full-project protocol dependency closure. No weights/binary included. Original source redistribution qualifications apply; no upload occurred. Older private `output/v121_replay.zip` remains available.

Executed create-once commands (do not repeat):

```sh
.venv/bin/python scripts/prepare_pointwise_v123.py
.venv/bin/python scripts/collect_pointwise_v123.py
.venv/bin/python scripts/analyze_pointwise_v123.py
.venv/bin/python scripts/package_pointwise_v123.py
```

Safe replay:

```sh
.venv/bin/python scripts/verify_pointwise_v123.py
MPLCONFIGDIR=/private/tmp/llm-study-v123-mpl .venv/bin/python scripts/analyze_pointwise_v123.py --report
.venv/bin/python scripts/diagnose_pointwise_v123.py
.venv/bin/python -I output/v123_replay/replay.py
.venv/bin/python -m pytest tests -q
.venv/bin/python scripts/seal_pointwise_v123.py --verify-only
```

## Reference audit and most important next action

**Implement a source-grounded local adaptation of the published numeric surrogate contract on exposed development cases before consuming another holdout.** The owner LLAMBO code was inspected at commit196fe237f60a3d3a2fa53cbf8f474ec20a01dd57, MIT. It uses supplied performance values, repeated stochastic predictions, uncertainty and expected improvement, unlike V123's clipped greedy scalar/batch ranking. Source links and precise boundaries are in `reports/reference_surrogate_audit_v123.md`. This is a code-read audit, not an executed reproduction; source-byte capture/vendoring is still unperformed. The upstream provider module reads API environment variables at import: do not import it. Original paid-model reproduction remains outside authorized scope; a local software-domain version must stay labeled adaptation.

A new bounded protocol must freeze target scaling, parsing, sampling, acquisition rule and cost before running. Do not silently extend V123's closed limits, substitute synthetic outputs or repeatedly retune to obtain a positive result. `reports/next_experiment.md` prioritizes this comparison, then a model/interface-matched controller and newly reserved independent families only if justified. No work is promised outside this active session.

## What remains untested / readiness

The pointwise adapter has only3exposed families and1seed each, not an independent router test. A reference-grounded surrogate comparison, fresh inference on another machine and native noise portability remain unperformed. Original benchmark correctness/noise/licensing uncertainties remain; stronger V52admission is not upgraded. Existing V113second-host requirement and V111NGINXfailure remain unchanged. No external machine has been provisioned.

There is a reproducible negative-result research candidate for technical discussion; original useful-generalizing-router hypotheses and Q2-level novelty are not established. Known positional bias and small-model reproducibility literature limit generic novelty claims. More same-family trials cannot establish independent generalization. Keep all earlier genuine LLM gains, failures and source limitations visible.

## Prior results that must stay visible

V120WordCount's reported gains matched free first-ten exactly in5/5cases. V121prospective MongoDB also matched first-ten5/5normal cases; the first-ten-target router escalated5/5for0%gain. Paired loss removal changed one of five MongoDB selections, so universal loss-insensitivity is false. V122real-cache projection lost9.465%against first-ten with0/5joint5%wins. V91contains genuine exceptions to first-ten equivalence. V92/V93already tested order/loss/decoder alternatives; do not present grammar removal as an untested cure. Old reports/raw data were not rewritten.

## Cumulative ledger and immutable checkpoint

Real model requests **4,228**; recorded-table acquisitions **29,288**. Numerical native880; NGINX81charged attempts/35,853,130byte-valid responses; DuckDB78,H2299,Kanzi1,265,RocksDB350 unchanged. Keep these units distinct.

Instrumented artifact downloads remain9,881,167,234/10GiB; remaining856,251,006bytes. Model payload unchanged9,126,358,023/9GiB. Web-tool metadata/code reads have unknown provider-transfer size and do not represent downloaded local model/source artifacts.

V123anchors V122manifest SHA256aa979016eb0db7f9dadb0ef767fe81f7cd43f2010b7407e6a3a41dd766f55720. All49historical checkpoints verified. Original root documents preserved under `artifacts/study_v123/previous_snapshot/`; new evidence seal is `artifacts/study_v123/evidence_manifest.json`. Historical raw outputs, protocols and manifests remain immutable. See `artifacts/study_v123/seal_verification.json` for the final current-seal receipt.
