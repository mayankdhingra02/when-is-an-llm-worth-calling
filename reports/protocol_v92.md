# V92: Qwen3-8B loss and presentation sensitivity

Frozen prospectively before this stage's inference. This is an exploratory model adaptation of V48, using exactly the same saved development messages, candidate mappings, condition order and analysis. It is not a replication of SNAP2 or a held-out evaluation. Latest user instruction to continue the research authorizes this new bounded diagnostic; V91 remains closed at 303 requests. No legacy configuration is changed.

## Question and sample

Does Qwen3 change its selections when acquired losses are removed, and does it preserve selections when irrelevant display order or candidate IDs change? These are necessary checks for interpreting its optimization behavior, not proof that its choices are useful.

Use all nine V48 development prefixes: MySQL, Brotli and lrzip, seeds 11, 37, 71. Each has ten acquired observations and the same twenty unobserved candidate configurations. No new target labels are acquired and no objective table is read by collection or diagnostic analysis. Every family and seed remains in its original development split. Repeated conditions are not independent systems.

The full factorial is two representations (original symbol JSON, decoded numeric values), two loss modes (observed, all acquired losses withheld), and three presentations (base, reverse candidate display while preserving ID mapping, rotate IDs by ten while preserving displayed configurations). Total: 108 conditions, ten selected IDs per condition, at most 1,080 real one-token requests. Reuse the exact V48 job order shuffled with seed 48000. No favorable-case selection or prompt revision after results.

## Model, collection and limits

Use the existing owner-pinned Qwen3-8B Q4_K_M weights, revision 7c41481f57cb95916b40956ab2f0b139b296d974, SHA256 d98cdcbd03e17ce47681435b5150e34c1417f50b5c0019dd560e4882c5745785. Existing llama.cpp b11146 runtime, loopback only, no thinking, greedy decoding, seed 11, 4,096 context, one request at a time. Reuse V91's bounded runtime and ID validation. Cross-device determinism is not guaranteed.

Each request emits one previously unused ID under the frozen grammar. The previous selections plus newlines are appended exactly as in V48/V91. Tokenization must show twenty distinct one-token IDs and a distinct one-token newline. All 108 rendered prompts must fit the context with twenty tokens reserved before any scientific request. Seal rendered inputs before generation. No additional compatibility generations: V91 already checked the unchanged model/runtime; metadata checks are repeated.

Stage ceiling: 1,080 scientific generation requests, zero retries, zero downloads, zero new objective acquisitions, zero external spending; 1,800 seconds lifecycle and 8 GiB sampled server RSS. The inherited watchdog reserves 125 seconds before the wall limit and terminates the server on a guard failure. No concurrent managed experiment, testing or analysis during timed inference. All model requests are charged before sending. Shut down the server in a finally block.

Preserve the 108-condition intended denominator. Invalid responses stay invalid; no repaired IDs or model-free fallback. Resource, timeout or server failures stop collection. Analysis refuses complete-case primary summaries if any intended condition is incomplete. Missing conditions and attempted requests remain in logs. Do not restart or increase caps automatically.

## Frozen analysis and decision

Use mapped configuration sets, never ID-string equality, for overlap (intersection size divided by ten). Report each representation separately:

1. Loss-removal set changes and overlaps at each presentation.
2. Reverse-order and relabel overlaps against base for each loss mode.
3. Lowest-ten-ID selection rate and fraction chosen from the first ten displayed configurations.

Screen inherited unchanged from V48: baseline loss removal must change sets in at least two of three seeds in at least two of three families; equal-family observed-loss mean overlap must be at least 0.8 for both reverse and relabel. Passing is necessary, not sufficient, for useful optimization. Report all conditions whether either screen passes or fails. Do not choose a representation for a quality claim based on this screen. Cross-model comparison with V48 is descriptive and must use exact matched conditions.

No router fitting, benefit estimation, new held-out claim, significance claim from nine seeds, or deployment policy estimate. Actual diagnostic collection cost is reported separately from the earlier paired optimization experiment. Record tokens, cache-prefill counts, full-context counts, time, sampled RSS, raw responses, all HTTP and generation charges, failures and server exit. Prior totals are 2,494 real model requests and 26,658 recorded acquisitions; add only actual new requests.

## Reproduction

Project-local Python commands: `scripts/freeze_sensitivity_v92.py`, `scripts/collect_sensitivity_v92.py`, `scripts/analyze_sensitivity_v92.py`, `scripts/verify_sensitivity_v92.py`, `scripts/report_sensitivity_v92.py`. Collection refuses an existing output directory; replay analysis in an isolated copy if the result directory already exists. Synthetic tests remain under `tests/synthetic/`. Preserve earlier sealed evidence through exact document snapshots.

After this diagnostic, evaluate evidence quality rather than continuing to tune these exposed prompts. An outcome-sensitive and stable result would motivate a prospectively fixed independent-system evaluation. A failed screen would narrow the claim to the tested model/interface and require a separately designed intervention before more routing experiments. Neither outcome establishes Q2 acceptance.
