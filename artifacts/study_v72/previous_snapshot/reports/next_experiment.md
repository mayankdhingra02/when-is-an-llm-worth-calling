# Next experiment after V71

The repaired native runner now passes full-workload validation. V71 supplies 200
live classical evaluations, 15 arms and independent in-budget confirmation, not
an LLM benefit result. See reports/rocksdb_v70_v71.md and readiness_v71.md.

## Next concrete action

Implement and prospectively freeze a small paired local-model experiment from ALL
five saved V71 prefixes (not just seeds where RF was weak). This is exploratory
development: classical outcomes have been inspected, and one software family plus
five seeds cannot establish held-out routing or satisfy the larger admission rule.

Use the pinned local SmolLM3-3B runtime, the legal complete-vector interface and
7 sequential proposal/evaluation steps followed by 3 fresh confirmations of the
selected incumbent. Keep total prefix + continuation evaluations at 20, counting
all confirmation outcomes. Charge every model request before transport, retain raw
responses/provenance and all failures, and freeze truncation/fallback rules.

Prepare an exact numerical request allowance (seven proposals x five prefixes =
35 calls before any separately counted runtime probes), no retries unless included
prospectively, local-only/no-spend enforcement, output tokens and runtime caps.
V65's allowance is exhausted; neither V70 nor V71 authorizes inference. Finish
implementation and synthetic/compile checks before seeking any scope approval.

Freshly measure RF continuations and a simple domain-prior control under identical
model-resident conditions. The prior must use public option meaning and features,
not V71 outcomes (for example a declared capacity/block-size ordering); freeze it
and explain that its choice is exploratory after V71 exposure. If useful, include
matched legal random proposals. An LLM advantage over RF alone may be an obvious
cache-capacity heuristic, not a need for an LLM. Count all added physical calls.

Freeze prompts, model/grammar versions, controls, arm ordering, seed support,
request/projection/fallback counters and cost accounting before calls. Existing
V71 timings were collected with no resident LLM; do not silently use them as the
only cost/runtime-matched control. Reuse prefix evidence identically; confirmations
never influence choices. Keep raw timing instrumentation unchanged across arms.

## Broader research requirements

The 512-vector grid is nominal; only 129 vectors were measured, and 400 effective
settings are not established. Real grammar/model sampling remains untested. A
successful exploratory continuation still needs independently admitted system
families, development-only controller fitting, held-out grouped evaluation with a
precision target, and comparisons against uncertainty/random/always/never routing.
No significance or generalization claim from seed counts; no invented global optimum.

Remaining persistent download allowance 568438763 bytes; no new model download is
needed by default. Respect 30-minute stage caps, one active experiment, bounded
process/memory use and no indefinite jobs. No paid/cloud calls, credentials, new
terms, system-wide installs, remote publication/push or author contact. The active
journal-quality goal is incomplete; proceed by falsifiable bounded studies, not
by repeatedly tuning until a favorable number appears.
