# V19: nine-call candidate ID/display mechanism probe — pending authorization

## Question and scope

V8 observed15 real responses selecting IDs0–9. The grammar allowed20,19,…,11 IDs across ten decision positions, so syntax did not force those selections. Exact first-ten reproduction does not establish a causal effect of display position or ID identity. This fixed exploratory probe separates those two prompt interventions. It does not measure optimization quality, improve a router, establish statistical generalization, or change the completed V17/V18 workload conclusions.

Choose seed11 (the first predefined seed) from each of the three V8 development families: MySQL, lrzip and Brotli. No choice based on response success/quality. Three fixed conditions per case, nine fresh requests total:

1. Original: byte-identical archived prompt; fresh contemporaneous baseline.
2. Reverse display: reverse the20 candidate entries while retaining each feature-to-ID binding.
3. Reverse IDs: retain feature/display order while replacing candidate IDs with their reversed assignment. Update the local ID-to-configuration mapping consistently.

Observed prefix labels, instructions, candidate feature set, sampling, model and grammar remain identical across treatments. Fresh baseline avoids relying entirely on an old-session counterfactual. Counterbalance treatment order in a deterministic three-round Latin rotation across manifest-family order. Requests are stateless and serial. There is one response per case/condition, not repeated independent model samples. No held-out outcomes are used or retuned; families remain exposed development cases.

## Provider, provenance and limits

Use the already downloaded Qwen/Qwen2.5-0.5B-Instruct revision7ae557604adf67be50417f59c2c2f167def9a775, CPUfloat32, four threads, greedy decoding, no seed-support claim. Keep the V8 distinct-ID grammar unchanged. The versioned provider changes only candidate-list permutation admission and bounded cleanup, while retaining original generation/model behavior. It verifies the pinned model files before launch; offline local-only Transformers, no remote code, no HTTP/cloud/credentials/API spending or downloads.

Each request has20 maximum generated tokens including forced separators/EOS and ten model-choice positions, eight-second response timeout, no retries. Stage work/model polling deadline40 seconds, bounded terminate/kill cleanup up to0.75 seconds; reserve two seconds from global remaining time and require45 seconds at preflight. The global cumulative1800-second limit remains unchanged. Time for setup/model load/requests/cleanup/analysis is charged. Source preparation/tokenizer validation is also charged, but no model inference occurs during it.

Existing authorized inference cap128 is exhausted. **Requested scope: nine additional local attempts, cap128→137; USD0 and1800 seconds unchanged.** configs/authorization_v19.json defaults denied and is separate from the scientific freeze. Explicit user permission is required before changing that record. Preflight must reject before model import/load or measured-run files while denied. On permission, preserve the exact approval in the record. Do not treat generic continuation as a new cap. The full nine-request reservation and runtime reserve are checked before starting. A started/finished run cannot be silently restarted.

Freeze the full prepared messages/mappings, protocol, code and dependency/source evidence before inference. Request records contain full prompts, parameters, timestamps, IDs, model revision, cache key, raw token IDs/output, grammar trace, token usage where observable and runtime. Never fill missing outputs with a rule or fabricate model responses. On malformed response, timeout or resource stop, retain it and all unattempted positions in the nine-request denominator; no fallback/retry. A failed setup also leaves a durable started marker for manual audit.

## Fixed analysis

For every intended condition record validity, selected IDs and source configuration rows; whether the selected set equals low IDs0–9, and whether it equals the first ten displayed entries. For each treatment compare its selected configuration set with the fresh original: exact equality and overlap out of ten. Validate actual generated tokens against the unchanged grammar and recorded prompts, model revision and token counts. Preserve all cases/failures; no significance test or causal claim across all software/models.

If selections follow low IDs after display reversal and switch configuration sets after ID reassignment, the controlled responses support ID-assignment sensitivity for these three cases. If selections follow first displayed entries, they support display-position sensitivity for these cases. Mixed/content-sensitive behavior is retained as observed. The two mechanisms can interact; three single responses do not prove an exclusive internal explanation. No empirical result is assumed or required.

This is a response-mechanism experiment: **zero new objective acquisitions**, no new physical benchmarks, no quality scoring, no deployment-saving claim. Only already acquired prefix outcomes enter prompts. Synthetic transformation/permission tests remain under tests/synthetic and outside measured results. Prepared prompts are not model responses.

## Commands

Preparation already allowed: scripts/prepare_order_v19.py (tokenizer only); pytest; scripts/run_order_v19.py --preflight. Actual inference after explicit bounded approval: scripts/run_order_v19.py, then scripts/analyze_order_v19.py. All use project .venv/bin/python from repository root. Stop after these nine attempts irrespective of result. No additional grids, seeds, stronger model or broader learned-router evaluation is authorized here.
