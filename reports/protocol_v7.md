# V7 development-only prefix-exclusion ablation

This is a post-v6 exploratory mechanism study, not a fresh test of routing/generalization. The v6 diagnosis observed 279/300 original-prefix copies. No treatment will be selected on held-out data; v6 held-out outcomes are not read by this collector or analysis. There is no router fitting here.

## Cases and unchanged treatment components

Use all five fixed seeds [11,23,37,53,71] from the three v6 development families, in their existing order: MySQL, lrzip, Brotli. Bind the exact v6 source/prefix/classical/paired files and original request log. Reuse their already acquired ten-label prefixes and original classical, random, uniform-projection and LLM comparisons without new collection charges. Reused inference is historical, not free. Data, directions, target isolation, model identity/revision, CPU/float32, greedy decoding, ten proposals per request, prompt text, acquired-only loss scaling, projection, tie breaking, retries (zero), 60-second timeout and 1,024-token maximum remain unchanged. Require every v7 prompt to equal its original v6 message payload exactly. No paid API, download, new model or cloud.

## Sole LLM intervention

At decoding time, exclude the ten exact feature strings from the original prefix. The constraint checks only feature symbols, never labels or their ranks. For a candidate next token, disallow it only if every possible domain-valid completion would be in the forbidden prefix set. This handles trailing constant features correctly and cannot reach a dead end when an unobserved combination exists. All remaining token choices are made by the real model's logits. Record the base schedule, forbidden strings, dynamic exclusion trace, generated IDs and raw output; verify every token against the dynamic rule after collection.

This is an explicit search constraint beyond syntax, not evidence of model insight by itself. It excludes only the original ten configurations, not previously generated novel rows within the same batch. Thus repeated novel proposals and feature-infeasible Cartesian combinations remain possible and are counted. Sequential nearest-unseen-row projection still applies. Zero prefix copies is guaranteed by the intervention, so it is a validity check rather than a substantive success result.

## Matched control and measurements

Run 15 new uniform-proposal continuations conditioned on the identical original-prefix exclusion. Sample an exact uniform rank from the complement of the forbidden Cartesian domain strings and decode mixed radix, seed = original seed + 40000, ten proposals. This avoids arbitrary rejection limits; repeated novel proposals remain allowed. Use the same saved prefix and projection. This control is model-free and is explicitly labeled as such. It is not a fabricated LLM result.

Both new branches use ten additional label acquisitions, hence logical budget 20 including the reused prefix. Actual new collection: 150 control labels + 150 real LLM labels = 300 total; 15 real model requests. All acquisitions, failures, malformed outputs, timeouts, fallback acquisitions and blocked cases are retained. Malformed/error model responses use a clearly marked classical fallback if time remains. Resource exhaustion/dead worker blocks subsequent cases. No additional reliability acquisitions or synthetic inference calls. Synthetic grammar tests and real-tokenizer checks precede collection and are kept separate from measured data.

Evaluate retrospectively using the same full-table normalized one-target loss as v6, kept out of search/constraints/prompts. Report within-case gain against the original v6 LLM, classical and both unconstrained/constrained uniform projection controls. Margin .02 is unchanged. Aggregate seeds within each family, then the three development families; no independence/generalization/significance claim. Compare proposal copies, novel repetition, projections, acquired-row collisions, fallbacks, tokens and wall times. Preserve per-case gains and all denominators. If the LLM arm is incomplete, report only the available control results and completion counts; no complete-case LLM comparison.

## Resource gate and approval boundary

The existing shared follow-up ledger has 98/100 requests and approximately 328.9/1800 seconds remaining at preparation. Execute the 15 no-model controls under the existing limits. Refuse to start the full LLM arm until all 15 requests fit the authorized allowance. The concrete requested change is **request cap 100 → 113**, providing 13 additional allowed attempts on top of the 2 already remaining. Exactly 15 new attempts maximum, no retries. **Do not change the 1,800-second runtime limit, USD 0 spending rule, model/download limits or historical counts.** If runtime proves insufficient, stop and preserve the full intended denominator.

`configs/authorization_v7.json` defaults to `granted:false`, cap 100. It may be changed only after explicit user approval; generic continuation is not interpreted as a resource-cap increase. This authorization record is separate from the frozen scientific treatment and is snapshotted at any actual inference start. The same persistent ledger is used; no resetting or bypassing caps.

## Integrity and execution

Freeze source, tests, protocol, development manifest and all paired input hashes before new control labels. Preserve v4/v5/v6 freezes. Completed branches can be reused without reacquisition; an incomplete started transaction fails closed for manual journal audit. Each new run has a distinct v7 namespace/source snapshot. No indefinite worker remains after exit.

```sh
PYTHONPATH=src .venv/bin/python -m escalation.study_v7 controls
PYTHONPATH=src .venv/bin/python -m escalation.study_v7 preflight
# Only after explicit request-cap approval:
PYTHONPATH=src .venv/bin/python -m escalation.study_v7 llm
PYTHONPATH=src .venv/bin/python -m escalation.analyze_v7
.venv/bin/python scripts/verify_v7.py
```
