# V98: bounded reasoning with a separate final-answer allowance

Freeze before generation and before acquiring any new objective cells. This
development-only procedure addresses V95's inability to obtain completed
thinking answers. It is not unrestricted reasoning, a paper replication, a
new independent-system test, or an outcome-dependent continuation of V95.

Use the same18 old prefixes from six V41/V91 development systems, seeds11,37,71.
For each prefix collect thinking and nonthinking conditions (36 total), with
the full condition order shuffled once using seed98000. All system variants
and seeds retain their original system-group membership. No V94/V97 numerical
system is used for tuning or model choices here.

Real Qwen3-8B Q4_K_M and llama.cpp b11146,6144context, one loopback server.
Reuse the exact original messages and candidate mappings. Thinking receives
up to512 output tokens with a stop string `</think>`. The server documents that
this stopping string is excluded from returned content. Accept only context-
untruncated `limit` or matching `word` stops with positive observed token count.
Then append the *actual returned thought text* and the explicit control
delimiter `\n</think>\n\n` to its original prompt. A second model request has
128 output tokens reserved for the final answer. The inserted delimiter is
prompt scaffolding, never represented as generated text. Save both requests,
both raw responses, the constructed prompt and exact provenance.

Nonthinking uses the same explicit empty-thought scaffold as V95b and one
128-token request. Thinking sampling remains temperature.6/top_p.95 for both
phases; nonthinking uses.7/.8. Both use top_k20,min_p0,presence_penalty1.5,
repeat_penalty1, case seed, no grammar, no cache reuse. This comparison bundles
owner-informed mode-specific sampling with the reasoning intervention; it does
not isolate reasoning alone. No added hint, answer text or guessed candidate ID.
Accept only an EOS-ended, context-untruncated final answer containing exactly
ten unique candidate IDs, one per line. No repair or projection. Invalid final
answers use the original prefix-only batch3NN fallback; report all failures.

Caps:54 generation requests (18×2 thinking +18 nonthinking),13,824 allocated
output tokens,1800s lifecycle,8GiB sampled model RSS,120s HTTP deadline,0retries,
0downloads,0paid/cloudspend. Any request/transport/settings exception stops
collection and leaves the rest explicitly unattempted. Invalid output syntax
is a measured fallback condition and does not trigger a retry. A second phase
is part of the predeclared procedure, not a retry. Existing interrupted or
completed batches remain unchanged. Token usage is unknown where unobserved.

After inference finishes, evaluate all36 intended policy arms, including
fallback/unattempted conditions, with ten new recorded-table acquisitions each:
360 additional charged accesses. Shared old10-label prefixes give logicalB20;
past prefix/reference/model collection costs are historical and not free.
Compare the new selections to saved same-prefix batch3NN, sequential3NN,
random and earlier greedy Qwen outputs. No classical reference is refit.
The model collector cannot import the objective oracle or access target tables.

Primary outcomes: valid-final coverage18permode, both-strong-controls>=5%
benefit count, per-system mean paired gain versus each strong control, full
intended-policy and valid-model-only summaries distinguished. Show all six
systems and all failures. No learned router fit, held-out claim, significance
claim or choosing a new threshold from these outcomes. Failed reasoning quality
must be attributed to its fallback rather than the model. Cost includes BOTH
thinking/final requests and their repeated prefill, all tokens observed and
startup. Compare costs directly; no unsupported monetary conversion.

Implementation basis: see `reports/source_audit_v98.md`. Budget forcing is prior
work, not a claimed contribution. The short two-stage adaptation here uses a
different model/task/runtime from s1 and is not its numerical replication.
