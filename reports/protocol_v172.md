# V172 protocol: model-scale test of LLM-specific escalation headroom

This protocol governs V172. It is a **pre-collection amendment** of `reports/proposal_v172.md`, which was hash-frozen in `artifacts/study_v171/freeze.json` before any V172 download, request or acquisition. Everything in that proposal stays in force except the changes listed below. The owner's authorization of the download, the cap increases and this amendment is recorded in `artifacts/study_v172/authorization.json`.

## Amendments to the proposal, made before any V172 outcome existed

1. **Added arm: a matched Qwen3-8B re-draw.** The historical 3B/8B results used one sampled response per case at temperature 0.7. A single 14B draw could pass the decision rule by sampling luck alone.
   - The re-draw reruns Qwen3-8B (the unchanged pinned file) on the same 70 message lists, grammar and parameters.
   - Its sampling seed is the historical seed plus 172000.
   - It estimates draw-to-draw variability at 8B. It is not a second-draw rescue of the 8B result.
2. **Attribution rule.** This refines interpretation of the unchanged primary rule; it does not replace it.
   - **14B ≥ 2 ecosystems and 8B re-draw ≤ 1:** consistent with a scale-related increase in LLM-specific headroom. The router question becomes testable, and the next step is a fresh, headroom-gated large-domain cohort.
   - **14B ≥ 2 and 8B re-draw ≥ 2:** LLM-specific wins also appear at 8B under resampling. Attribution to scale is not supported, and the single historical draw understated headroom. The next step is a multi-draw headroom estimate, not a router study.
   - **14B ≤ 1:** close the router question for these local models on this hardware and write up the boundary result. The 8B re-draw is still reported as sampling-variability evidence.
3. **Stages.**
   - Inference runs in four create-once stages of 35 requests each: A1/A2 for Qwen3-14B, then B1/B2 for the 8B re-draw.
   - Jobs split by a fixed seed-17200 permutation of the 70 cases; the same split serves both models.
   - Each stage has its own 1,800 s cap.
   - A separate preflight stage P and an evaluation stage E follow the gates below.
4. **Resources.** The limits change as follows; everything else is unchanged:
   - 140 scientific requests (35 per stage, each within the 100-request ceiling in `configs/pilot.yaml`) plus one synthetic compatibility request in P;
   - 144,384 allocated output tokens;
   - 1,400 recorded acquisitions;
   - server RSS cap 12 GiB for 14B and 8 GiB for 8B (the historical value).

## Fixed treatment and replay semantics

- **Inputs.** The 70 saved message lists in `artifacts/study_v141/prompts`, `artifacts/study_v144/prompts` and `artifacts/study_v148/prompts`, and the domains and prefixes from each stage's `jobs.json`.
- **Runtime.** llama.cpp b11146 with the historical server flags: `-ngl 99 -c 4096 -np 1 -t 6 -b 512 -ub 128 --reasoning off --jinja --no-warmup`.
- **Payload.** From `scripts/proposal_v128.py`: temperature 0.7, top_p 0.95, top_k 0, min_p 0, repeat_penalty 1, 1,024 output tokens, and the ten-string grammar. Thinking is disabled.
- **Projection and fallback per origin stage, exactly as historically:**
  - V141 cases use Hamming projection (`proposal_v127.project`); an invalid response falls back to batch 3NN (`transfer_v41.rank`).
  - Spark cases use `spark_v144.project`; an invalid response falls back to stepwise sequential 3NN (the `spark_v145.choose` missing-label wrapper). A missing source target is charged and retained as `None`.
  - Hadoop cases use `hadoop_v148.project`; an invalid response falls back to stepwise sequential 3NN. The failure penalty is `hadoop_v148.score_record`.
- **Accounting.** A fallback counts under the arm that produced it and is reported, never hidden.
- **Oracles.** They reuse each stage's parsing and scoring code, but charge a new V172 ledger. They never write into historical result directories.
- **Classical arms.** The historical sequential, random-full, adaptive, fixed and GP-EI arms are reused as-is.

## Gates, in order

1. Authorization recorded, and at least 25 GiB of free disk before the download.
2. Owner LFS pointer, LICENSE (Apache-2.0) and README fetched at the pinned full revision. The model is streamed with a running SHA256, and its hash and size must match the pointer. The retained-download and payload caps are enforced during the transfer.
3. Protocol, config, code, tests and jobs are hash-frozen in `artifacts/study_v172/freeze.json`. Synthetic tests pass before any model start.
4. Preflight P with Qwen3-14B:
   - Render and tokenize all 70 prompts, recording byte equality with the retained Qwen3-8B rendered prompts.
   - Check format capacity (prompt plus 1,024 output tokens within 4,096 context).
   - Make one synthetic compatibility generation, parsed through the same grammar path.
   - Require peak RSS of at most 12 GiB.
   - A rendering difference is recorded, not edited away.
   - The compatibility output is outside every research aggregate.
5. Stages A1, A2, B1 and B2 run in that order, one server at a time, with no concurrent tests or workloads. A stage stopping early keeps its unattempted jobs in the denominator. There are no retries, and no additional stage may be added to make up shortfalls.
6. Evaluation E requires all four inference stages to have ended, whatever their status:
   - Seal all 140 selections before any new recorded target is read.
   - Then charge at most 1,400 acquisitions within 600 s.

## Analysis (frozen in `scripts/analyze_v172.py`)

**Primary: ecosystems with an LLM-specific win for Qwen3-14B.** A win is a case beating sequential 3NN, random-full, adaptive neighbor and GP-EI (ℓ=1) each by >1%, with direction explicit. The seven V151 ecosystems are primary; the eight engine groups are a sensitivity.

The same measures are reported for the 8B re-draw and for the historical SmolLM3-3B and Qwen3-8B draws:
- case counts;
- equal-ecosystem mean relative and log-ratio gain versus sequential;
- hindsight headroom;
- counts against each single switch;
- per-case paired differences (14B versus historical 8B, and re-draw versus historical 8B);
- validity, fallback and projection diagnostics;
- tokens and request time.

Seeds are not independent systems. There are no significance tests, and cohorts are never pooled. Independent replay (`scripts/verify_v172.py`) re-parses every response and recomputes projections and fallbacks. It re-reads every charged target from source bytes and recomputes the primary estimand with separately written code.

## Costs

- **Research cost.** The download bytes, every model start (P, A1, A2, B1, B2), all requests including fallbacks and the compatibility request, and all 1,400 acquisitions. Historical classical and model costs stay in their own ledgers.
- **Deployment estimate.** One escalation call plus ten recorded evaluations after B10 per escalated case, with load time amortized separately.
- **No dollars and no energy estimates.**

No journal-readiness claim follows from any outcome.
