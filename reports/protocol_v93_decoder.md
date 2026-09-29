# V93: does the output grammar explain Qwen3's sensitivity?

Prepared before interpretation of V92. This is a separate bounded continuation under the user's instruction to keep researching. It does not reopen V91 or enlarge V92. The design reuses the original V49 decoder diagnostic on Qwen3-8B with unchanged source messages. There is no prompt search, held-out evaluation, new objective acquisition or learned-router fitting.

## Fixed design

Use all 54 symbol-representation conditions from V92/V48: three development families (MySQL, Brotli, lrzip), seeds 11, 37, 71, two loss modes and three presentations. Omit the numeric representation consistently with the historical V49 design, not according to Qwen3 outcomes. Add nine concurrent forced-decoder repeats of all observed-loss/base-presentation prefixes. Use the exact V49 deterministic shuffle with seed 49000, 63 total intended cases. Native cases each have one request with maximum 128 generated tokens, no grammar and no manually inserted delimiters. Forced controls use ten one-token requests exactly as V92. Both receive the same template-rendered messages as V92b; assert exact token and text equality before any generation.

Use the same owner-pinned Qwen3-8B Q4_K_M model, llama.cpp b11146, greedy seed 11, no thinking, 8,192 context and V92b runtime settings. Request seed is not a cross-device reproducibility guarantee. No compatibility probe generations are needed for the unchanged verified binary/model. All generation payloads and responses are saved. Independent verification reconstructs selections and contrasts from raw outputs.

Maximum: 144 new generation requests, 7,002 output tokens, 1,800 seconds lifecycle, 8 GiB sampled server RSS; zero retries, new objective outcomes, downloads, cloud or external spending. Use the inherited watchdog, process shutdown and pre-send charge logging. Run no other managed compute during timed inference. Stop on resource/server/timeout failure; retain all 63 intended cases and missing/invalid entries. Do not silently restart or increase limits. No scientific response is repaired or replaced by a classical guess.

## Strict parsing and analysis

A valid native answer contains exactly ten unique candidate IDs, one per nonempty line; whitespace stripping is allowed. Explanations, bullets, commas, unknown IDs, duplicates, wrong counts, truncation or token-limit termination are invalid. Reuse V49's parser. Invalid native cases remain in the denominator and cannot be compared as if they were valid choices.

Compare mapped configuration sets, not ID strings. Compute loss-removal overlap and reverse/relabel overlap as in V92, and native-versus-V92 forced overlap for every condition. A missing or invalid endpoint has unknown overlap in [0,1]; retain this interval in family-balanced summaries. Report valid-only overlap only as secondary descriptive information. Forced repeats must reproduce the nine saved V92 base configuration sets; any differences undermine interpretation of a native-versus-forced change.

Frozen V49 screening rule: native format validity at least 95%; loss removal changes the baseline selected set in at least two of three seeds in at least two of three families; observed-loss lower-bound family mean overlap at least 0.8 for both reversal and relabeling; all nine concurrent forced controls reproduce V92 selections. All criteria must pass. Passing remains only a necessary diagnostic, not evidence of useful optimization or benefit-aware routing. Failure ends decoder/prompt tuning on these cases for this stage. Report every planned contrast and all failures.

Actual collection costs include both decoder modes and startup. Do not describe these extra diagnostic calls as policy deployment costs. Native and forced responses are not independent software systems. The Qwen3 study uses a larger context capacity than historical SmolLM3, and model architecture/training also differ; do not attribute differences solely to parameter count. This experiment addresses the forced-output confound while leaving reasoning mode, public-data contamination and unseen-system validity unresolved.

## Execution and evidence

Commands in the project environment: `scripts/prepare_decoder_v93.py`, `scripts/freeze_decoder_v93.py`, `scripts/collect_decoder_v93.py`, `scripts/analyze_decoder_v93.py`, `scripts/verify_decoder_v93.py`. Freeze after V92 completion and sealing, before V93 generation. Raw evidence: `results/v93_decoder/`; analysis: `results/v93_analysis/`; audit receipts: `artifacts/study_v93/`. If collection cannot finish, analyze missing-case bounds and report incomplete evidence rather than selecting completed successes.
