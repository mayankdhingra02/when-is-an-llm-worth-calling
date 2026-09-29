# V172 amendment 2: Qwen3-8B re-draw stage failures and a descriptive sensitivity

Written 2026-09-28, after inference stages B1 and B2 ended and **before evaluation E read any V172 recorded target**. The earlier freezes (`freeze.json`, `freeze_amendment1.json`) are unchanged. The amended file hashes are in `artifacts/study_v172/freeze_amendment2.json`.

## What happened

**Stage B1** (Qwen3-8B re-draw, split 1) stopped at the pre-declared server-RSS cap.
- The cap was 8 GiB (8,589,934,592 bytes), the historical value for this model. The runtime watchdog sampled a peak of 8,656,781,312 bytes and killed the server (`resource_stop_reason: server_rss_cap`, exit −9) during the 17th request.
- Outcome: 16 valid responses, 1 charged request with no response, and 18 unattempted jobs.
- Earlier Qwen3-8B runs peaked at 6.8–7.5 GB. The higher footprint here is an observed operational difference, not an explained one.

**Stage B2** (Qwen3-8B re-draw, split 2) lost its server during the 30th request, and the client received `RemoteDisconnected`.
- The server log ends mid-generation with no error line, matching B1's watchdog kill. The on-disk ledger's peak of 8,261,091,328 bytes was last written before that request.
- The inherited V148 `close()` then raised `PermissionError(1)` from `os.killpg` on the exiting process group, so the collector wrote no `summary.json` and the in-memory stop reason was lost. **The cause is therefore recorded as unconfirmed; the most likely cause is the same RSS cap.**
- Outcome: 29 valid responses, 1 charged request with no response, and 5 unattempted jobs.
- No llama-server process remained afterwards.
- A summary was reconstructed from persisted files by `scripts/stage_summary_v172.py` and is labeled `reconstructed_after_collector_crash`.

The Qwen3-14B stages A1R and A2 completed 70 of 70 valid responses, with peak RSS 10.42 GB and 11.30 GB under the 12 GiB cap.

## Decisions

1. **No repair, no retry and no cap increase for B1 or B2**, as the protocol and amendment 1 require. The re-draw arm has **45 valid responses and 25 fallback cases**. Fallbacks follow each origin stage's historical fallback rule and count under the re-draw arm.
2. **The primary estimand is unaffected.** It depends only on the complete Qwen3-14B arm; its definition and the frozen decision rule are unchanged.
3. **The re-draw ecosystem count used by the attribution rule is a lower bound.** A fallback can never be an LLM-specific win. The report must say this whenever it applies.
4. **Added descriptive sensitivity**, fixed before any target is read. For both new arms, the analysis reports ecosystem and case counts, mean gain and headroom restricted to cases with a valid response, plus how many ecosystems those cases cover. It is labeled descriptive and does not replace the primary estimand or the decision.
5. **Runtime defect recorded.** In the inherited `runtime_models_v148.Runtime.close`, `os.killpg` can raise `PermissionError` on macOS when the server group is already exiting. This affected only bookkeeping in B2, and no outputs were lost. Future runtimes should tolerate `ProcessLookupError` and `PermissionError` there and persist the stop reason before cleanup. The frozen runtime is not patched retroactively.

## Files changed by this amendment

`scripts/analyze_v172.py` (the sensitivity block), `scripts/report_v172.py` (the sensitivity table and lower-bound note), `scripts/common_v172.py` (ordered freeze overlay), `scripts/stage_summary_v172.py` (new), `tests/synthetic/test_v172.py` (overlay test), and this document.
