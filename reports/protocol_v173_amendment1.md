# V173 amendment 1: token cap, rate limits and provider choice

Written 2026-09-28, after stage A1 was stopped by the operator and **before any V173 recorded target was read**. The original `freeze.json` and `protocol_v173.md` are unchanged and remain the pre-collection record. The amended hashes are in `artifacts/study_v173/freeze_amendment1.json`.

## What happened in A1

- **Sent:** 11 requests on the pinned `coreweave/fp4` endpoint.
- **Truncation.** The first two (`sac::sac_AllNumeric_11_normal` and `spark::bayes_53`) returned `finish_reason: length` at exactly 4,000 completion tokens, of which 3,133 and 2,920 were reasoning tokens. Reasoning at effort `medium` used up SNAP2's 4,000-token cap before the 10-proposal answer was complete, so both were invalid.
- **Rate limiting.** The next eight returned HTTP 429, "temporarily rate-limited upstream" from CoreWeave's shared pool, before any generation.
- **Operator stop.** I stopped the stage while an eleventh request was in flight; that request has no recorded response and an unknown cost.
- **Throughput.** The two completed requests ran at about 50–60 output tokens/s. At that rate arm B's roughly 350 requests would take 6–7 hours.
- **Cost.** Recorded spend was $0.0015. No recorded target was read.
- **Record.** The stage is kept as a failed attempt in `results/v173_models/A1/`, with a summary reconstructed after the stop and labeled as such.

Continuing unchanged would have filled arm A with fallbacks caused by our output cap and provider congestion. That would measure infrastructure, not the model's optimization value.

## Changes

1. **Output cap.** `max_tokens` becomes 16,000 for arm A (ten proposals, up to 59 symbols each, plus reasoning) and 8,000 for arm B (two proposals; SNAP2's own cap for larger tasks). Reasoning effort stays `medium`.
2. **Rate limits.**
   - An HTTP 429 is rejected before generation. It is retried after 5, 10, 20, 40 and 60 s, at most 5 times per logical request, and only within the stage wall cap.
   - Every attempt is recorded and charged to the spend ledger; a 429 costs $0.
   - A request still rate-limited after these waits is invalid and takes the historical fallback.
   - Rate-limit retries are not model retries and do not count against the stage's logical request cap.
3. **Provider rule, applied in new stage P2 before any scientific request.**
   - Probe the providers that list every required parameter in the saved endpoint listing, in ascending expected-cost order: `coreweave/fp4, deepinfra/bf16, dekallm/bf16, akashml/bf16, crusoe/bf16, mancer/fp8, deepinfra/turbo, groq, nebius/fp4, phala, parasail/fp4, cerebras/fp16`.
   - Each probe is one synthetic, non-research request: a 30-feature, 10-proposal task at the arm A settings.
   - The first provider that returns HTTP 200, `finish_reason: stop`, schema-valid output and at least 200 completion tokens/s becomes the pinned provider for all later stages.
   - If none qualifies, no scientific stage runs.
   - Providers with unknown quantization (Groq, Phala) are eligible. That is recorded as a provenance limitation; SNAP2's own routing is also unreported.
4. **Stage order.** P (done), A1 (failed, kept), P2, A1R (draw 1 of record, same seeds as A1), A2, E, B1–B4, EB. Arm A evaluation uses A1R and A2.
5. **Unchanged:** the $3 client cap, the prompts, the schema form, the seeds, the analysis estimand and the decision rule. The key's reported $100 limit (planned: $5) is recorded. The owner's $5 credit and the client cap bound exposure.
