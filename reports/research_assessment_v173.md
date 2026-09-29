# Research assessment after V173

**The frozen V173 decision is positive, but it is fragile.** SNAP2's own model, `openai/gpt-oss-120b`, produced LLM-specific wins in **2 of 7 ecosystems in arm A's first draw**, exactly the pre-registered threshold. That is the first time any arm in this study has reached it.

- **The threshold is not reproduced.** The second draw and the SNAP2-style iterative arm reach 1 ecosystem each.
- **The deciding wins are marginal.** Two HIPAcc cases are just above the 1% margin (+1.7% and +1.9%) and vanish in the other two runs.
- **Post-hoc checks agree.** At a 2% margin, or requiring a win to recur, every gpt-oss run falls to 1 ecosystem, Spark/Hadoop.

Numbers come from the generated `reports/snap2_model_v173.md` and `results/v173_analysis/analysis.json`. Post-hoc sensitivities, computed after inspecting outcomes and labeled as such, are in `results/v173_analysis/posthoc_sensitivity.json`.

## What ran

- **Setup.** Hosted inference via OpenRouter under the owner's recorded approval, on the exposed 70-case recorded cohort, with the V172 classical comparators and win definition. The protocol and two pre-outcome amendments are in `reports/protocol_v173*.md`.
- **Arm A.** V172's exact one-shot, 10-proposal interface; two draws; **140 of 140 valid responses and no fallbacks**.
- **Arm B.** A SNAP2-style loop of 5 rounds × 2 proposals with trajectory feedback, collision lists and one retry per round; **all 70 cases completed**.
  - 348 model rounds, 2 fallback rounds, 13 rounds needing a retry.
  - 356 proposals collided with already-measured settings; each was nudged to the nearest unmeasured one and fed back.
- **Recorded acquisitions:** 2,100 (1,400 + 700).
- **Provider.** DeepInfra `turbo` (bf16), chosen by the probe rule declared in advance.
- **Cost.** **$1.38** over 539 recorded attempts (513 responses, 26 rate-limit rejections), plus one request lost in flight during the stopped A1 attempt, with unknown cost.
- **Verification.** The independent replay passed on its first run: 0 errors, the primary estimand recomputed, and the prompt-leakage mutation rejected.

## Results

| Arm | Ecosystems with a win (of 7) | Win cases | Eq.-ecosystem gain vs sequential | Hindsight headroom |
|---|---:|---:|---:|---:|
| SmolLM3-3B (local) | 0 | 0 | −4.96% | 0.22% |
| Qwen3-8B (local) | 0 | 0 | −5.24% | 0.18% |
| Qwen3-14B (local, V172) | 1 | 2 | −4.00% | 0.45% |
| gpt-oss-120b, arm A draw 1 | **2** | 3 | −3.73% | 0.53% |
| gpt-oss-120b, arm A draw 2 | 1 | 1 | −3.16% | 0.76% |
| gpt-oss-120b, arm B (SNAP2-style) | 1 | 2 | −3.14% | 0.87% |

For comparison, GP-EI's hindsight headroom over sequential on the same cases is 1.28%.

1. **A replicated LLM-specific win exists, a first for this study.** `spark::bayes_11` beats every cheap switch in all three gpt-oss runs: +8.3% in both one-shot draws and **+31.5%** in the iterative arm. No local model found it. In `spark::terasort_23`, arm B reaches the same +24% configuration Qwen3-14B found.
2. **The deciding HIPAcc wins look like sampling noise at the margin.** `hipacc_37` and `hipacc_53` score +1.9% and +1.7% in draw 1, then −5.6% and 0.0% in draw 2, and −1.7% and −2.0% in arm B.
3. **Averages still favor cheap classical search.** Every gpt-oss arm loses to continued sequential 3NN on average, though by less than the small models. Its headroom stays below GP-EI's.
4. **The iterative SNAP2-style interface helps.** It has the best mean and headroom and the largest wins. Paired against arm A's first draw, it is >1% better in 19 cases and worse in 10. SNAP2's design choice (classical first, then iterative LLM proposals) is supported as mattering, within this cohort.
5. **Scale and training help.** Against the historical Qwen3-8B draw, gpt-oss arm A is >1% better in 27 cases and worse in 5.

## What this means for the research question

The question: can a small controller predict, after ten classical evaluations, whether an LLM continuation is worth it?

- **Local 3B–14B models: no LLM-specific signal to predict (V171–V172).**
- **SNAP2's model: real but rare LLM-specific value.** It formally reaches the frozen threshold, but reproducible wins are confined to **one ecosystem** (Spark/Hadoop), where sequential 3NN is already known to stall. With the positives in one group, a leave-one-group-out router is still not informative on this cohort.
- **What the frozen rule implies.** A router study now needs a **fresh, headroom-gated cohort with positives in several independent groups.** The admissible unexposed pool for that is nearly exhausted (V171).

The paper's story becomes more nuanced, and arguably stronger:
- Small local models add nothing beyond cheap switching.
- SNAP2's model adds real value in rare, concentrated cases, most visibly under iterative feedback, while still losing on average.
- That rarity and concentration are exactly what makes benefit-aware routing hard to learn across systems.

This answers the "you only tested small models" objection directly, with a careful and honest positive-but-bounded result.

## Limits

- **Exposed tasks.** The cohort is exposed, arm A has two draws per case and arm B one, and seeds are not independent systems. There are no significance tests.
- **Hosted inference.** Weights can't be hash-verified (bf16 on DeepInfra `turbo`). The reasoning effort (`medium`) is our choice; SNAP2 doesn't report its own.
- **Arm B is an adaptation.** It follows SNAP2's prompt structure with our encodings, not SNAP2's code.
- **Amendments.** Two amendments were made before any target was read: output cap, rate limits and provider (1); continuation stages (2). The stopped A1 attempt is preserved.
- **Key limit.** The key reported a $100 limit rather than the planned $5. The account's $5 credit and the $3 client cap bounded exposure.

## Recommended next step

1. **Write the paper around this graded result.** Report the frozen V173 decision exactly, with the post-hoc sensitivities alongside, clearly labeled.
2. **Optional: one pre-registered replication to settle the fragility.** Run two more arm B draws, the best interface, on the same cohort, with a rule fixed in advance, for example "≥2 ecosystems in at least 2 of 3 arm B draws." At about $0.89 per draw (arm B's measured cost) that's roughly $1.77. It fits under the remaining $3 client cap ($1.62 left) only if the cap is raised. **This needs your decision.** It would estimate how reliably gpt-oss finds LLM-specific wins; it would not by itself create a router test.
3. **Don't train a router on these exposed cases,** or report a leave-one-group-out router as if it generalized. The positives are still concentrated.
