# V21: three interleaved-ID calls prepared, not executed

**The model test is ready; all three real responses remain unobserved.** It distinguishes two rules that fit all24 prior outputs: selecting the first displayed ten versus continuing the canonical ID sequence. See [the completed ambiguity audit](rule_identifiability_v20.md).

Use the same MySQL/lrzip/Brotli seed11 original features and acquired observations. Keep feature order, assign candidate IDs0,J,1,I,…,9,A, and make one request per case. The first-display rule and endpoint-sequence rule now predict different selected sets. The same pinned local Qwen0.5B, greedy CPUfloat32 settings, provider and distinct-ID grammar are retained. No new objective acquisitions or selection-quality analysis.

All three exact [prompts/mappings](../data/nonmonotone_probe_v21.json) are prepared and checked with the pinned tokenizer:1402/1615/1771 input tokens,20-token maximum output each (a limit, not measured output usage). **140 tests pass**. Python compilation checks passed. The [27-file scientific freeze](protocol_v21_nonmonotone.freeze.json) precedes any new inference. The actual runner returned expected blocked status2 before model loading. No measured V21 directory exists. The new runner/analyzer are implemented but not yet exercised with real V21 responses.

## Exact approval needed

Authorize **three additional local attempts, cap137→140**, keeping **USD0 spending and the existing1800-second runtime limit**. There are23.6160seconds left. The probe requires22 seconds remaining at preflight, uses a14-second work/polling deadline plus bounded cleanup,6-second per-request timeout,20 output tokens per request and no retries. Five seconds are reserved for actual-response analysis. If a bound is hit, retain failed/unattempted cases and stop; no extra limit is implied.

[Authorization](../configs/authorization_v21.json) remains denied. On direct approval of this bounded request, record the user's text/timestamp and set granted=true/request_cap140 without altering other fields. Then run project Python on scripts/run_nonmonotone_v21.py and scripts/analyze_nonmonotone_v21.py. No paid API, model download/install, cloud resources, credentials, publication or contact.

## Limits and costs

This is one new permutation for three exposed development cases, not independent-system validation or a general internal-mechanism test. There is no fresh original-condition rerun in this three-call extension; comparison to V19 originals is across sessions. The primary result is which fixed rule, if any, matches each actual new response. Mixed/neither outcomes are retained; do not adapt prompts after them.

Tokenization/preparation used2.7895charged seconds and0 model requests; no objective/physical outcomes/downloads/spending. Runtime is1776.3840/1800seconds,ledger inactive. Inference remains137/137 exhausted;237 historical attempts including initial stage. Historical1134 physical trials and5408 recorded objective acquisitions are unchanged.

[Protocol](protocol_v21_nonmonotone.md), [tests](../artifacts/study_v21/tests.log), [tokenizer check](../artifacts/study_v21/tokenizer_preflight.json), [denied run](../artifacts/study_v21/denied_run.log). The only pending permission is the exact three-call increment; no result is fabricated from the rule predictions.
