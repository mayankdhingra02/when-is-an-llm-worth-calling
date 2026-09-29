# V47 — fixed cross-model robustness assay

This is a new model/runtime bundle, chosen before its optimization outcomes,
tested on all 30 original V41 prefixes (six families, seeds 11/23/37/53/71).
No prompt, pool, family, seed or threshold tuning. V41 outcomes are exposed;
this is explicitly exploratory robustness, NOT independent held-out evidence.
It probes whether the negative Qwen result extends to another available local
model family. It does not resume pool/prompt tuning stopped in V44. One batch
only: further work must follow its scientific implications, not chase a win.

Reuse exact V41 message contents, candidates, normalization, prefix and budget.
Model SmolLM3-3B Q4_K_M / pinned V46 GGUF, llama.cpp b11146, Metal GPU,
greedy temperature 0, thinking off, 4096-token context. Recheck full model hash.
Quantization, parameter count, tokenizer and runtime differ from Qwen CPU fp32;
any difference is a model/runtime-bundle result, not a causal family effect.

The original Qwen decoder constrained ten unique IDs with forced newlines.
To retain that semantic constraint with this runtime, use ten one-token local
completion requests per case: grammar permits one remaining ID; inject the
newline and previous chosen IDs into the next prompt. Verify every ID and newline
has a single standalone token before generation. Each of the ten choices comes
from real model logits. Do not invent or repair choices. This is not necessarily
token-for-token decoding equivalence because tokenizer vocabularies differ.
Record 300 intended HTTP generation requests (30 semantic continuations), rather
than calling this 30 requests. Prefix-cache reuse is allowed within each case;
disable cross-case cache reuse on the first choice. Save full rendered prompt,
tokenization, per-choice grammar, request/response, usage and timings. Explicitly
separate generated choice tokens from forced delimiter tokens.

The user's instruction to continue beyond feasibility authorizes this bounded
batch: 600 seconds total live runtime, 300 one-token generation requests, zero
retries/downloads/spending, 300 acquired recorded outcomes. Enforce limits before
requests. Server listens only on 127.0.0.1, disables web UI and network model
fetching, and shuts down in a finally block. Count failed requests. Any incomplete
collection retains all intended cases and refuses primary complete-case means.
Malformed choice or request failure falls back for the entire case to saved
batch3NN; no partial guessed continuation. Stop on a dead server/timeout rather
than retrying. Offline classical fallback for a failed case is not LLM output.

Do all model selection before evaluation: collector reads saved acquired prefixes
only and does not open target tables. Evaluator independently clones each prefix,
acquires 10 selected rows (also charge previously seen rows), retains incumbent,
and checks 20 distinct logical evaluations. Historical comparators reuse their
already collected V41 traces, charging no new acquisitions but disclosing their
historical collection cost. Preserve every model failure in the denominator.

Primary comparators: same-pool batch3NN and stronger full-domain sequential3NN.
Secondary: historical Qwen1.5 and Qwen0.5, all seven V41 classical controls.
Report per-case/per-family raw target and relative gain, equal-family mean,
wins/ties/harms, descriptive six-family bootstrap intervals. Six families are
the inferential units, not 30 seeds. No confirmatory p-value claim or test-set
selection of a comparator. Report all frozen V41 never/always/uncertainty/benefit
and random policy masks without fitting. Hindsight oracle remains diagnostic.
These policies were trained for Qwen and may be miscalibrated for SmolLM3.

Predeclared useful-result criterion: positive equal-family mean against BOTH
primary controls with each descriptive 95% family bootstrap interval excluding
zero. This is a screening criterion, not a journal-readiness or generalization
claim. Otherwise retain a negative/mixed result and stop this batch. Neither a
positive mean nor an oracle benefit establishes learned routing. Next scientific
need is independent groups and a separate frozen development/test design.

Separate actual collection from retrospectively modeled deployment: count all
300 choice requests and 300 new recorded outcomes for this batch, old collection
separately; policy cost includes selected cases' ten requests and tokens, plus
startup separately. Do not infer causal latency superiority over Qwen's different
hardware/runtime or convert local tokens to invented dollar savings.
