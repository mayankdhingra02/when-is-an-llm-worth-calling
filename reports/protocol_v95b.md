# V95b adapter correction before the first generation

Original V95 stopped at a template-boundary assertion after 1.148365 seconds,
six HTTP metadata requests and ZERO generations/objective acquisitions.
Preserve `results/v95_reasoning/`, original code/tests/config/freeze unchanged.

llama.cpp b11146 `/apply-template` in the observed auto mode returns the
assistant header without a thinking tag. Its
[version-pinned endpoint documentation](https://github.com/ggml-org/llama.cpp/blob/b11146/tools/server/README.md)
documents messages and supports modifying the returned prefix before completion;
it does not promise the per-request template kwargs used in the original
assumption. Use the observed base template and explicit CONTROL prefixes:
`<think>\n` for thinking, `<think>\n\n</think>\n\n` for non-thinking.
These are prompt scaffolding, not fabricated model outputs. All actual reasoning,
candidate choices and final answers remain real model generation. Save both
base rendering and explicit control prefix. Fail closed if the base template
does not end in the exact assistant header. This explicit-prefill procedure
is an adaptation, not an exact owner-inference replication.

The same pinned API reports `stop_type` (eos/limit/word/none), rather than a
required `stopped_limit` Boolean. Accept complete answers only when `stop_type`
is `eos` and `truncated` is false. This fixes a parser compatibility issue
found before any generated response; no observed model output is used to
relax validity rules. Keep all other strict ID and thinking-end requirements.

Cases, order, prompts apart from the disclosed control tags, sampling, model,
context, output allocations and request caps are unchanged. Runtime allowance
is 1,798 seconds, reserving two seconds for the original preflight, so combined
V95/V95b remains inside 1,800 seconds. Same8GiB RSS guard,36 requests,39,168
allocated output tokens,360 maximum subsequent table acquisitions, zero retries,
downloads/spend. This is continuation of wholly unattempted scientific cases,
not a repeated search for favorable outputs. Original failure remains visible.
