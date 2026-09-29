# V95: owner-informed, budget-constrained native decoding

This development-only comparison changes both thinking mode and owner-recommended sampling policy. It uses explicit thinking-control prompt prefixes and short generation limits; it is not unrestricted Qwen3 reasoning, a pure thinking-only causal intervention, or a new held-out evaluation.

| Mode | Charged / intended | Valid / returned | Fallbacks | Mean gain vs sequential 3NN | >=5% wins | >=5% harms |
|---|---:|---:|---:|---:|---:|---:|
| thinking | 13 / 18 | 0 / 12 | 18 | -2.58% | 1 | 1 |
| nonthinking | 12 / 18 | 12 / 12 | 6 | -2.75% | 1 | 1 |

Gain includes the frozen batch-3NN fallback for invalid or unattempted model conditions. A fallback is never labeled successful LLM selection. Family means weight the six development groups equally; seeds remain grouped. Every intended condition is retained.

Unattempted conditions stopped by a study-level cap are NOT model generation failures. Their predeclared fallback is included only in the full intended-cohort analysis. Use charged/returned denominators for model reliability. Unknown usage applies to charged requests without responses; unattempted conditions made zero requests. See `coverage.json`.

| Family | Charged thinking / non-thinking | Thinking + fallback gain | Non-thinking + fallback gain |
|---|---:|---:|---:|
| berkeleydb | 3 / 3 | +1.86% | +1.19% |
| dune_hsmgp | 3 / 3 | -14.30% | -14.96% |
| hipacc | 3 / 3 | -2.28% | -2.00% |
| llvm | 3 / 3 | -0.19% | -0.19% |
| openvpn | 0 / 0 | -0.08% | -0.08% |
| sac | 1 / 0 | -0.45% | -0.45% |

Failure reasons (a case may have several): `{"no_unique_thinking_end": 12, "request_failure": 1, "unattempted": 11}`.

Collector stop/errors: `[{"at": "2026-09-27T06:40:41.522563+00:00", "error": "TimeoutError('timed out')", "key": "sac_AllNumeric_11_thinking", "wall_seconds": 120.00451274996158}]`.

## Actual collection

25 charged requests, 24 responses, 360 new recorded-table acquisitions. Model lifecycle 1459.030s plus preserved failed preflight 1.148s; peak RSS 7,374,618,624 bytes; resource stop None. The adapter charged every request before sending. No retries/downloads/paid or cloud calls.

Returned output tokens: 24,816; missing usage cases: 12. Summed full-context tokens: 30,490; reported actual prefill tokens: 30,490. Missing/unreturned usage is unknown, never free. The existing shared prefixes and classical branches have historical collection costs. Deployment would use one 20-label arm, with model cost only when called; this analysis is not a measured end-to-end deployment benchmark.

## Interpretation and limits

The original V95 preflight made zero generations and stopped at a wrong template-boundary assumption. V95b corrected the template scaffold and stop_type parser before the first generation, preserving the original failure and shared request/time limits. Owner sampling settings were checked against server response metadata. No output repair or outcome-based filtering was performed.

The owner recommends much longer output capacity than this local budget. Unfinished thinking proves failure under this declared budget, not failure of unrestricted thinking. This experiment cannot establish Q2 readiness, broad model inferiority, router benefit prediction, or new-system generalization. The V94 two-engine test remains unchanged. Further policy development must use development groups and receive a new untouched-system evaluation before any confirmatory claim.

Raw prompts, outputs, token metadata and failures: `results/v95b_reasoning/`. Paired branches and acquisition logs: `results/v95_analysis/`. Original/amended freezes: `reports/protocol_v95.freeze.json`, `reports/protocol_v95b.freeze.json`. Recreate this report and figure from saved outcomes with `scripts/report_reasoning_v95.py`; do not rerun `analyze_reasoning_v95.py` over existing outputs, as it is a charged acquisition stage.

## Additional observable usage for the timed-out request

The sole final request without an HTTP response has server-log usage: 2,048 generated and 3,304 prefill tokens. Together with returned responses, 26,864 generated tokens are observable. The original response-only aggregates remain unchanged. The missing answer cannot be recovered from these counts and was not fabricated. The request stays a transport timeout and the arm uses its predefined fallback. See `results/v95_analysis/transport_timeout_usage.json` for the hashed log and exact source lines.
