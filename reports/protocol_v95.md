# V95 development-only, budget-constrained thinking comparison

Freeze before any V95 generation. Same existing Qwen3-8B Q4_K_M weights and
llama.cpp b11146; no downloads, money, external services or new software groups.
Question: does an owner-informed native decoding policy with thinking enabled
alter the negative result enough to justify a new prospective evaluation?
This is development evidence, not a fresh held-out result or exact SNAP2 code.

Use all six V91/V41 exposed systems, seeds 11,37,71 (18 saved prefixes), each
with thinking and non-thinking native decoding (36 intended conditions).
Related variants and seeds remain grouped. Same prompt and 20-candidate pool,
same shared ten-label prefix, same ten-label continuation budget. No outcomes
from V94 numerical families are used; they remain reported as completed tests.
Mode order is seed-randomized in the saved job list, before generations.

The pinned owner GGUF card (`artifacts/sources/v91/README.md`, Best Practices;
[Qwen owner artifact](https://huggingface.co/Qwen/Qwen3-8B-GGUF)) warns against
greedy thinking and recommends temperature .6/top-p .95 for thinking, .7/.8
for non-thinking, top-k20/min-p0 and presence penalty1.5 for the quantized model.
Use those settings and each case's explicit seed, with no grammar. Check the
server's returned settings rather than assuming parameters took effect. This
changes mode AND recommended sampling policy, so it cannot isolate a pure
causal effect of thinking. Earlier greedy forced-ID results remain unchanged.

Resource adaptation: thinking output maximum2,048 tokens, non-thinking128;
39,168 allocated tokens across36 requests. The owner's recommended32,768 output
length is not executed and is NOT claimed. Unfinished thinking is a real
budget failure, not evidence that unrestricted reasoning cannot work.
Context6,144 fits the largest saved prompt plus2,048 reserve; preflight every
case before first generation, verify template ends at the correct thinking
boundary. Loopback only, one request, no retries, maximum36 new requests,
1,800s lifecycle,8GiB server RSS,120s HTTP timeout, charged before sending.
Same shutdown/watchdog as V91. Stop on a request/resource/provenance failure,
retaining all unattempted cases in the denominator. Do not raise caps mid-run.

Thinking output must contain exactly one closing `</think>` and a final
answer of ten distinct supplied IDs, one per line. Native non-thinking must
meet the same final-answer format. Whitespace-only blank lines are ignored;
no prose extraction, repair, projection or replacement model guesses. Reject
context truncation, output-limit truncation, missing thinking end, duplicates
and malformed answers. Save complete raw outputs and token/timing metadata.

For each intended condition, valid choices are evaluated via the charged
indexed oracle. Failed/unattempted conditions fall back to prefix-only batch
3NN with explicit failure labels; do not describe fallbacks as LLM output.
At most360 recorded table acquisitions, counting every newly read continuation
cell even for repeated configurations in another arm. Logical budget20 each;
shared prefixes are existing research collection, not free deployment input.
Save every branch and compare never/full sequential3NN, same-pool batch3NN,
earlier forced greedy Qwen3, and thinking/non-thinking native. Family-first
descriptive means and useful/harmful counts at predeclared5% margin. No new
controller training, threshold tuning, pooled confirmatory significance test
or exclusion of failed conditions. Separate new collection cost from modeled
deployment (prefix plus chosen branch, including failed model requests).

If both modes rarely help, retain the negative finding. If thinking helps,
that motivates a future frozen untouched-system test, not a victory claim on
these development groups. No new batch follows automatically from a good or
bad sign; finish analysis and checkpoint all limits and outstanding work.
