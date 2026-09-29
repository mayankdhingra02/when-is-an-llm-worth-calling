# Research assessment after V172

**The frozen decision rule gives `close_router_question`.**
- **The 14B arm stays under the threshold.** Qwen3-14B, the largest model this 18 GB machine runs comfortably, produced LLM-specific wins in **1 of 7 ecosystems**; the pre-registered threshold was 2.
- **The headroom result extends to 14B.** The V171 finding of little LLM-specific headroom now holds from 3B to 14B within this interface, to that threshold. For these local models on this hardware, the benefit-aware router question cannot be tested: there are no positive-bearing groups across leave-one-group-out folds.
- **Reporting obligation.** Under the pre-registered plan, the next step is to write up the boundary result, reporting every arm.

Numbers come from `reports/model_scale_v172.md`, which is generated from `results/v172_analysis/analysis.json`. The protocol and four amendments are in `reports/protocol_v172*.md`.

## What ran

- **Download.** One owner-published model file (Qwen3-14B Q4_K_M, revision `530227a7…`, 9,001,752,960 bytes), with its SHA256 verified against the owner LFS pointer. The retained-download and model-size limits were raised with the owner's recorded approval.
- **Qwen3-14B arm.** 70 of 70 valid responses to byte-identical historical prompts (checked at preflight). Peak server memory was 10.4–11.3 GB, under the 12 GiB cap.
- **Qwen3-8B re-draw.** 45 of 70 valid responses:
  - Stage B1 stopped at the pre-declared 8 GiB memory cap (8.66 GB observed; this model previously peaked at 6.8–7.5 GB).
  - Stage B2 lost its server, most likely to the same cap, though the cause is unconfirmed.
  - No repair or cap increase followed. The 25 fallback cases stay in the arm.
- **Failed and repaired stage.** Stage A1 failed at a pre-start port check before any request. It was repaired as A1R under amendment 1, written before any 14B scientific output existed.
- **Evaluation.** All 140 selections were sealed before 1,400 recorded acquisitions were charged, in 7.4 s. The independent replay passed after a verifier-only alphabet fix (amendment 3); the initial failed replay is preserved.
- **Tests.** 1,352 tests pass.

## Results

**Primary estimand, LLM-specific wins.** A win beats sequential 3NN, random-full, adaptive neighbor and GP-EI each by >1%.

| Arm | Ecosystems (of 7) | Cases |
|---|---:|---:|
| SmolLM3-3B | 0 | 0 |
| Qwen3-8B, historical draw | 0 | 0 |
| Qwen3-8B, re-draw | 0 (a lower bound) | 0 |
| Qwen3-14B | **1** | **2** |

**Average quality improved with scale, but still loses to cheap search.**
- Qwen3-14B's equal-ecosystem gain against sequential 3NN is −4.00% (log-ratio −3.60%), against −5.24% for the historical 8B draw.
- Paired on the same cases, 14B is >1% better than the historical 8B draw in 16 cases and worse in 5.
- Its hindsight headroom over sequential is 0.45%, still well below GP-EI's 1.28% on the same cohort.
- The 8B re-draw's −3.72% mean is not comparable: it includes 25 cases that rerun the classical fallback. Its valid-response-only mean is −8.02%.

**The two 14B wins are real but narrow.**
- Both are Spark terasort seeds (`terasort_23` and `terasort_71`), at about 21–24% better than every cheap switch. That is the ecosystem where sequential 3NN was already known to stall.
- In `terasort_71`, random proposals pushed through the same projection interface reach the same value. That control was not in the pre-registered switch set, because it exists only for Spark/Hadoop.
- Both cases fall in split 1, after B1 stopped, so **the 8B re-draw is unobserved for exactly these two cases.** The re-draw cannot tell us whether 8B would also have found them.

**Interface behavior is unchanged in kind.** Of the 14B arm's 700 projected proposals, 537 needed nonzero projection and 207 repeated an earlier proposal in the same batch. The projection interface still shapes what gets evaluated.

## What this changes

1. **The boundary result is stronger and now covers a scale range.** Across three model sizes (3B, 8B, 14B) and two 8B draws (the second only 45 of 70 valid), escalation after a B10 prefix produced LLM-specific wins in at most one ecosystem. Even there, one of the two wins is reproduced by random proposals through the same interface. The positive class stays concentrated in one ecosystem, so a leave-one-group-out router evaluation remains uninformative, as V171 found.
2. **Scale helps somewhat, which is worth reporting.** The 14B average loss is smaller and its first wins appeared. This is one draw on exposed tasks within one model family. It supports "larger local models narrow the gap" as an observation, not a trend estimate or an extrapolation to gpt-oss-120b.
3. **The question as originally posed is answered for this setting.** The question: can a small controller predict, after ten evaluations, whether an LLM continuation is worth it? For local 3B–14B models on this hardware, the evidence says there is almost nothing LLM-specific to predict. The rational controller is "never call". The reason is that the positives are too rare and too concentrated to learn from, not that a router was shown to lack skill.

## Limits

- One draw per case per arm. The re-draw is incomplete (45 of 70) and missing for both win cases.
- Exposed recorded tasks, one prompt/grammar/projection interface, a single model family for the scale step, and one host.
- Seeds are not independent systems, and there are no significance tests.
- Qwen3-14B differs from 8B in more than parameter count.
- The whole-study development history (V1–V172) must be disclosed in any paper.

## Recommended next step

**Write the paper-shaped synthesis. Do not collect more data.** The core findings are:
- the paired-prefix design with charged budgets;
- always-call dominated across 13 exposed groups;
- no LLM-specific headroom from 3B to 14B, with the first wins confined to one ecosystem and one of them matched by an interface control;
- router non-identifiability under concentrated positives;
- the methodological lesson that escalation benefit must be measured against the best pre-specified cheap switch.

A larger model (for example gpt-oss-120b, as in SNAP2) would be the only remaining lever on the central confound. It does not fit this 18 GB machine and would need resources the owner has not approved. More seeds, prompts or interfaces on these exposed tasks would be forking-path exploration, not evidence.

**Housekeeping.** The 14B weights are pinned by hash in the sealed manifests but not sealed as a file, so they can be moved off this machine without breaking evidence verification. The SmolLM3 and Qwen3-8B files are still sealed by historical manifests and must stay in place.
