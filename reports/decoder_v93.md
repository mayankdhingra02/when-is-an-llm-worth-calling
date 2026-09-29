# V93: native decoding does not change the observed Qwen3 selections

**Measured result:** all 53 returned native answers selected the same configuration sets as their V92 forced-decoder counterparts; all nine concurrent forced controls reproduced V92. One native request failed at the memory guard and was not retried. Thus 53/54 intended native cases and 9/9 forced controls completed, with 144 total charged requests and 143 responses. No returned answer was malformed or repaired.

This is evidence against the forced one-token grammar being the sole cause of these observed selections. It is not a universal claim about decoding, reasoning modes or Qwen3. The resource-compatible continuation changed context capacity, so the combined result is explicitly an amended two-context diagnostic, not a clean single-runtime replication.

The frozen screen did not pass. Native format validity is 53/54 (98.15% with the resource failure retained) and forced reproduction is 9/9. Baseline loss removal changed four of nine configuration sets, but only one family reached two changed seeds; the rule required two families. Observed-loss reversal overlap is bounded at **57.8%–68.9%**, below the 80% stability criterion even if the missing case were maximally stable. Relabel overlap is **55.6%** with all nine pairs observed. Neither response validity nor some loss responsiveness establishes useful optimization.

| Native diagnostic | Valid pairs / intended | Changed sets | Family overlap including unknowns |
|---|---:|---:|---:|
| loss_removal / base | 9/9 | 4 | 55.6%–55.6% |
| loss_removal / reverse | 8/9 | 6 | 34.4%–45.6% |
| loss_removal / relabel | 9/9 | 4 | 72.2%–72.2% |
| reverse / observed | 8/9 | 4 | 57.8%–68.9% |
| reverse / withheld | 9/9 | 8 | 13.3%–13.3% |
| relabel / observed | 9/9 | 6 | 55.6%–55.6% |
| relabel / withheld | 9/9 | 2 | 87.8%–87.8% |

The native-versus-historical-forced family overlap bound is 98.15%–100% over all 54 intended cases; the valid-only overlap is 100%. Do not replace the missing answer with its historical forced answer. These are finite-sample missing-response bounds, not population confidence intervals. V92 and V93 reuse the same three development families and nine prefixes; repeated conditions are not independent systems. V91's optimization comparison remains separate and negative against both primary cheap controls.

## Preserved failure and bounded continuation

The original V93 protocol and 421 input pins were frozen before inference. The 8,192-context run stopped after 67 charged requests, 66 responses and 30 completed cases when sampled RSS reached **8,609,628,160 bytes**, above the 8 GiB threshold. The watchdog killed the server (exit −9) at 221.690684 seconds. The failed case is `MySQL_71_symbols_observed_reverse_native`; its response and actual token usage are unknown. Original raw data and partial analysis remain under `results/v93_decoder/` and `results/v93_analysis/`. The original complete-run verifier was not used to claim success; a separately labeled partial-run audit passed.

Saved preflight records showed the symbol-only prompts plus native answer allowance require at most 1,904 tokens. The V93b amendment lowered context to 4,096 and continued only the 32 wholly unattempted cases, in the same order. It used the remaining 77 requests and a 1,578-second lifecycle ceiling, keeping the combined original ceilings at 144 requests and 1,800 seconds. The 8 GiB RSS guard was unchanged. No failed or partially attempted case was repeated. Twenty-one targeted amendment tests passed and 531 inputs were frozen before continuation. Sandbox process-monitor denials occurred before inference and are retained separately.

V93b completed all 32 cases with 77 requests in 241.902532 seconds, peak RSS **8,285,880,320 bytes**, exit 0. It made no retry. Both source logs remain authoritative. `results/v93_combined/` is a derived view with per-record source paths, source hashes, case contexts, and explicit failed-case coverage; it does not backdate a preflight seal or modify original responses.

## Actual research collection cost

Total decoder lifecycle: **463.593216 seconds**, including both startups and the failed request. Native mode: 54 requests, 53 responses, 1,060 returned generated tokens, 79,857 full-context tokens and 79,857 reported prefill tokens. Forced controls: 90 requests/responses, 90 generated tokens, 144,820 full-context tokens and 14,563 prefill tokens. Returned request wall-time sum is 460.461283 seconds; it excludes the unreturned request's separately logged failure duration, while lifecycle includes it.

Generated-token count is **at least 1,150**, with up to the failed request's allocated 128 tokens unreported. The shared theoretical allocation remains 7,002 tokens: original attempted native/forced allocations plus all unattempted-case allocations, including the failed request's full cap. Missing usage is not zero. Combined HTTP calls: 343, including metadata/health. No deployment-policy cost estimate is claimed for these diagnostic interventions.

No new objective acquisitions, downloads, paid spending or cloud access. Electricity/hardware cost remains unknown. Cumulative real-model requests are **3,718**; recorded acquisitions remain **26,658**. This turn added 1,224 real requests (V92 1,080 + V93/V93b 144). All stage request ceilings are consumed. No model server remains running.

## Verification and reproduction

All **738 tests passed in 21.74 seconds** after collection. Independent verification checks both protocol freezes, original raw-source hashes, all 144 charged requests, 143 responses, 63 preflight records, 63 intended paired diagnostics, nine forced repeats, and disjoint attempted/unattempted case sets. It checks both original preflight seals against actual request times. Missing-case bounds and screen decisions are recomputed independently. The amended scientific figure was rendered and visually inspected; its hatching represents the missing response, not a malformed answer.

Commands: `.venv/bin/python scripts/verify_decoder_v93_combined.py` and `scripts/report_decoder_v93_combined.py`. Recreate the derived view only in a clean isolated copy with `scripts/combine_decoder_v93.py` and `scripts/analyze_decoder_v93_combined.py`; existing outputs are protected. Original frozen V93 scripts remain unchanged and represent the pre-amendment protocol.

The combined archive `output/diagnostics_v93_reproduction.zip` provides standard-library saved-response replay for V48/V92 and V93/V93b. It excludes model weights and explicitly reports absent model/runtime pins; it verifies saved data and calculations, not a fresh model or hardware replication. Source/adaptation scripts and all actual failure evidence are included. Use `scripts/seal_decoder_v93.py --verify-only` for the full repository integrity audit after sealing.

## Scientific consequence

The larger model and unconstrained answer format did not rescue the observed choices. The narrow negative result is stronger than before, but the original claim of useful, generalizable benefit-aware routing remains unsupported. Reasoning-enabled inference, genuinely untouched system evaluation, model contamination, different workloads and independent native-machine replication remain untested. See `reports/research_readiness_v93.md` for the supported claim and prioritized next experiment. Do not keep tuning these exposed cases to obtain a favorable result.
