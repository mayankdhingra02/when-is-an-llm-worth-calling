# STATUS — V92 and amended V93 diagnostics finished and verified

**New concrete result:** Qwen3 failed V92's frozen loss/order screen in both representations. Free native decoding did not change any of the 53 returned configuration sets compared with forced decoding; all nine forced controls reproduced. One memory-guard failure remains charged and unknown. Native reversal overlap is bounded at 57.8%–68.9%, below the 80% screen even in the best case; relabel overlap is 55.6%. This strengthens a scoped negative result, not useful held-out routing or Q2 readiness. Read `reports/decoder_v93.md`, `reports/sensitivity_v92.md`, and `reports/research_readiness_v93.md`.

## What ran

- V92: 108 conditions, 1,080 real one-token calls, zero invalid outputs/retries. Original 4,096-context preflight failed before generation; V92b used 8,192 with unchanged cases/screens and shared caps. Lifecycle 1,330.323 seconds plus 0.938 seconds failed preflight; peak 8,166,637,568 bytes; exit 0. Independent 108-prompt / 126-contrast verification passed. Frozen 184 original / 187 amended pins.
- V93: 67 charged calls / 66 responses / 30 complete cases before RSS guard stopped at 8,609,628,160 bytes and 221.691 seconds, exit −9. Failed native case `MySQL_71_symbols_observed_reverse_native` was never retried. Original partial data, code, protocol and 421-pin freeze are preserved.
- V93b: all 32 wholly unattempted cases continued at 4,096 context, unchanged prompt tokens (maximum native prompt plus reserve 1,904), memory ceiling and remaining allowances. 77 calls, 241.903 seconds, peak 8,285,880,320 bytes, exit 0. 531 inputs frozen; 21 amendment tests passed beforehand.
- Combined decoder result: 144 requests / 143 responses; 53/54 native and 9/9 forced cases complete. Both shared original request/time caps respected; first resource failure disclosed. 1,150 returned generated tokens plus unknown failed-request usage, bounded by its 128-token allocation. No new objective labels, downloads or paid spending. All 738 tests passed in 21.74 seconds. No server or experiment remains running.

## Evidence and reproduction

Raw original V92/V93/V93b requests, failures and ledgers: `results/v92b_sensitivity/`, `results/v93_decoder/`, `results/v93b_decoder/`. Derived source-bound view and coverage: `results/v93_combined/`. Analysis and PNG/SVG: `results/v92b_analysis/`, `results/v93_combined_analysis/`. Independent audit receipts: `artifacts/study_v92/`, `artifacts/study_v93/`. The combined decoder verifier checks original source records and freezes, not just summaries. Two contexts and a missing response are explicit limitations.

Portable combined saved-response replay: `output/diagnostics_v93_reproduction.zip`. It includes no model weights and does not execute inference. Commands: `scripts/verify_decoder_v93_combined.py`, `scripts/replay_sensitivity_v92.py`; portable decoder replay `scripts/replay_decoder_v93_combined.py` runs inside the extracted bundle with its manifest. Seal integrity with `scripts/seal_decoder_v93.py --verify-only`. Earlier root docs are snapshotted under `artifacts/study_v92/previous_snapshot/` and `artifacts/study_v93/previous_snapshot/`; preserve old seals. Do not rerun completed inference in place or reuse exhausted allowances.

## Limits and next action

Cumulative real-model requests: **3,718**. Recorded acquisitions: **26,658**. This turn added 1,224 requests and zero objective acquisitions. Native counts unchanged: DuckDB 78 physical (77 valid, one timeout; 71 unattempted separately); H2 299 (298 valid, one failure; eight historical unattempted); Kanzi 1,265; RocksDB 350. External spend USD 0; electricity/hardware unknown.

Downloads unchanged: 9,867,753,109 total bytes / 10 GiB, leaving 869,665,131; model payload 9,126,358,023 / 9 GiB, leaving 537,318,393. Model already local. V92 and V93 shared request caps are fully consumed. No paid API, cloud, credentials, publishing, pushing or external contact authorized. No request to raise the memory guard was needed; only unattempted cases continued with lower context.

**Single most important next action:** freeze an evaluation on genuinely untouched software families before inspecting outcomes, with a clearly chosen confirmatory claim and unchanged strong cheap controls. Check prior exposure/admission audits first. Existing seeds and repeated prompts are not independent systems. Native clean-machine replication and reasoning-enabled behavior also remain untested. Do not tune these exposed cases further to chase a positive result. The broad original routing research goal remains open; the bounded diagnostics are complete and reviewable.
