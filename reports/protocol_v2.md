# Frozen exploratory follow-up v2 — 2026-09-24

Authorization: after v1 exhausted 100 attempts and the assistant proposed a new bounded development-only feasibility experiment, the user said “why did you stop ,continue please … lmk if you need anything”. The assistant explicitly announced a follow-up allowance of at most 100 additional local attempts, USD 0 external spending, within the original 1,800-second cumulative experiment runtime. The v1 ledger and all outcomes remain unchanged. This is a separate, exploratory follow-up after inspecting v1 failures, never an extension of v1's frozen treatment.

## Fixed intervention

Same pinned Qwen 0.5B model and weights. Use local transformers greedy decoding with a token-position grammar for exactly two complete binary configuration arrays in a JSON candidates object. Fixed punctuation is constrained; at each variable coordinate the model chooses among legal binary values by its logits. No objective oracle, rank, continuation outcome or candidate desirability enters the grammar. Record token constraint schedule/hash, number of choice positions, raw output, all tokens, and ordinary model provenance. Maximum output length is grammar length plus EOS, at most 1,024 tokens. The parser is unchanged and validates decoded output. Generation does not fabricate or fill missing choices outside the model.

Shorten prompt scaffolding: compact integer feature arrays, full feature names and domains, acquired losses sorted worst-to-best and collision information. This is a prompt/decoding adaptation, not a claim to reproduce SNAP2. No further prompt/model/grammar tuning after this protocol is frozen.

## Feasibility gate before software outcomes

Three disjoint synthetic tasks with 9, 16 and 39 binary variables, 32 feature configurations each, fixed seed 20260924, ten supplied synthetic observations. These fixtures are stored under results/v2/feasibility with namespace synthetic_feasibility_real_inference. Their model responses are REAL, but no synthetic quality data enter research aggregates. Exactly one request per fixture, no retry. Gate requires all three to return valid outputs within 60 seconds each. A valid format is a feasibility test, not evidence of optimization skill. If any fails, stop additional inference under v2 and report the gate failure.

## Conditional paired smoke experiment

Only after all three gate checks pass: use the original 15 frozen prefixes and classical continuations, with hash equality. Each LLM branch receives exactly ten additional charged objective acquisitions (two per call, five calls). All current datasets/domains and B=20, t=10, five seeds, delta=0.02, objective scoring, grouping, controller features and development-only fitting rules from v1 remain fixed. No new classical labels are acquired: reuse is explicitly recorded, and historical classical/prefix costs remain in the collection ledger.

Use development groups first (Apache, SQLite), then x264 once; x264 has no prior completed LLM counterfactual, but its classical outcomes have been inspected, so all v2 results are exploratory smoke. Fit controllers after collection with the original fixed procedure, no retuning. If complete, report never/always, uncertainty, benefit, matched-rate random, ablations and hindsight diagnostic. One held-out group cannot demonstrate generalization.

No inference retries in v2. An invalid decoded response uses classical fallback for that batch, logged. A timeout or worker failure stops all further model calls immediately and marks remaining runs blocked. No requests are charged for attempts against a worker already known dead. Worker health is checked before reserving a request; no automatic restart, no repeated failures against a dead process. Releasing/terminating the worker is guaranteed on exit. Recovery means a deliberate new invocation with a documented decision, not hidden automatic continuation.

## Resource accounting

At most 100 new attempts (3 format gate + 75 planned paired calls = 78 expected), each at most 60 seconds; no paid/remote provider; no new model downloads. v2 has its own persistent request ledger, with v1's measured runtime carried forward so total runtime never exceeds 1,800 seconds. The original v1 100-attempt cap stays exhausted. All stages share a global lock, preventing overlapping experiment/model sessions. No indefinite jobs. Preserve source snapshots, protocol/prompt/grammar hashes, parameters, request IDs, actual prompts/raw responses, timeouts, unknown token usage and intended run denominators. Pure syntax constraints are not optimizer proposals; the model's choice tokens must be saved and auditable.

Analysis separates v2 marginal collection cost, v1 historical collection, and selected-branch deployment estimates. Invalid/failed/blocked records never disappear. Synthetic feasibility calls count toward actual runtime/request/token collection costs but are excluded from software-quality estimates. Any change after seeing v2 outcomes needs another labeled protocol and explicit decision.
