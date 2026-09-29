# V19 order/ID probe: prepared, inference not authorized

**Nine concrete local-model requests are prepared and frozen, but none has run.** The inference preflight and actual runner both rejected launch before model loading because the authorized128-request allowance is exhausted. This is a request-cap blocker, not missing model access, a failed model response, or automatic approval-review rejection.

The probe tests whether V8's first-ten selection pattern follows candidate IDs or display positions. It uses the first fixed seed11 for all three V8 development families (MySQL, lrzip, Brotli), with three fresh conditions per case: original prompt, reversed display retaining IDs, and reversed ID assignment retaining feature order. All conditions use the same candidate configurations and acquired prefix labels. Counterbalanced execution order and a fresh baseline are fixed before inference. No hidden candidate targets, new objective acquisitions, quality score, grid expansion or stronger model is involved.

The exact [nine prepared prompts/mappings](../data/order_probe_v19.json), [protocol](protocol_v19_order.md), [25-file freeze](protocol_v19_order.freeze.json), [local adapter](../src/escalation/provider_v19.py), [guarded runner](../scripts/run_order_v19.py) and [response analyzer](../scripts/analyze_order_v19.py) are ready for review. Model identity is the existing pinned Qwen2.5-0.5B-Instruct revision7ae557604adf67be50417f59c2c2f167def9a775, CPUfloat32/greedy/four threads. No installation, model download, credentials, paid API or cloud usage.

## What actually ran

- Nine message transformations from archived, provenance-checked V8 inputs.
- Real local tokenizer/context checks: input token counts1402/1615/1771 by family, each repeated across three conditions;20 maximum output tokens per request. Ten grammar decisions each retain20 down to11 allowable IDs, so syntax does not force a first-ten sequence. Tokenizer work is not inference.
-134 tests passed, including intervention invariants, unchanged feature/ID mappings as appropriate, invalid-response rejection, exact authorization bounds and stopping before a request reservation when the stage expires.
- Python compilation checks passed. Preflight and actual runner both returned expected blocked status before loading a model or creating measured-run artifacts. [Logs](../artifacts/study_v19/).

The prepared model worker and response analyzer have **not** been exercised with new real responses; their end-to-end behavior remains untested until permission and execution. Synthetic tests never stand in for model results.

## Exact requested allowance

Authorize **nine additional local attempts**, changing the cumulative follow-up request cap from128 to137. Keep the existing1800-second cumulative runtime limit, USD0 external spend and all download limits unchanged. The probe has a40-second work/polling deadline plus bounded cleanup, eight-second request timeout, zero retries, and a complete nine-condition failure denominator. It stops after the fixed probe regardless of result. This does not authorize a larger model, further prompts, new hardware, paid/cloud access or publication.

[Authorization record](../configs/authorization_v19.json) remains denied. On explicit approval, record the user's approval text and timestamp, set granted=true and request_cap=137, retaining all other bounds. Do not reset the ledger. Run scripts/run_order_v19.py, then scripts/analyze_order_v19.py using project Python. Any started-run marker requires audit before a retry; the runner refuses automatic recollection. If the current45-second minimum runtime reserve is lost, stop rather than increase it.

Current runtime is1746.9059/1800seconds, with53.0941seconds remaining. Preparation used2.7051seconds; no new requests, outcomes, physical trials, downloads or spending. Model requests remain128/128, historical228 including initial stage. Physical trials1134 and recorded objective acquisitions5408 remain unchanged.

## Scope of the possible finding

This is a small exploratory mechanism probe on three exposed cases, not a positive optimization or benefit-routing result. V6's selected zero escalation rate makes its matched-rate policies identical at that operating point; it does not demonstrate useful selection at a nonzero rate. The V17/V18 tiny headroom findings remain unchanged. This probe can test the observed V8 behavior under controlled prompt changes, but cannot repair insufficient independent groups or establish generalization. All completed prior evidence is retained.
