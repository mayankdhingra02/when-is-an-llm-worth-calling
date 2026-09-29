# Resume checkpoint: V172 model-scale headroom test complete

Start with `reports/research_assessment_v172.md`, then `reports/model_scale_v172.md` (generated tables) and `reports/audit_v171.md` (independent audit). The V171 status this replaces is preserved in `artifacts/study_v172/previous_snapshot/STATUS.md`; older checkpoints are chained through earlier snapshots.

## Result

**The frozen V172 decision is `close_router_question`.**
- **Qwen3-14B stays under the threshold.** It reached LLM-specific wins in 1 of 7 recorded-cohort ecosystems (2 of 70 cases, both Spark terasort), below the pre-registered threshold of 2.
- **Wins across all arms.** SmolLM3-3B, the historical Qwen3-8B draw and a partial Qwen3-8B re-draw each had 0 ecosystems. A win means beating sequential 3NN, random-full, adaptive neighbor and GP-EI each by >1%.
- **Average quality and headroom.** Qwen3-14B improved the average relative to 8B (−4.00% vs −5.24% against sequential; 16 better and 5 worse paired cases) but still loses on average. Its hindsight headroom (0.45%) stays below GP-EI's (1.28%).
- **The two wins.** One of the two 14B wins is matched by random proposals through the same projection interface. The 8B re-draw is unobserved for both win cases.
- **Consequence.** For local 3B–14B models on this 18 GB machine, the router question cannot be tested (positives are confined to one ecosystem), and the rational controller is "never call".

## What V172 did (all under the owner's recorded approval, `artifacts/study_v172/authorization.json`)

- **Download.** `Qwen/Qwen3-14B-GGUF` `Qwen3-14B-Q4_K_M.gguf`, revision `530227a7d994db8eca5ab5ced2fb692b614357fd`, 9,001,752,960 bytes, SHA256 `500a8806…`, verified against the owner LFS pointer and API metadata. Apache-2.0 license retained in `artifacts/sources/v172`.
- **Freezing.** The protocol (`reports/protocol_v172.md`), config, code, jobs and inputs were frozen before any model start: 332 files, plus a runtime-directory hash.
- **Preflight.** All 70 prompts rendered byte- and token-identical to the historical Qwen3-8B renders.
- **Qwen3-14B stages A1R and A2.** 70 of 70 valid responses, peak RSS 10.4 and 11.3 GB under the 12 GiB cap.
- **Qwen3-8B re-draw stages B1 and B2.** 45 of 70 valid.
  - B1 stopped at the pre-declared 8 GiB RSS cap.
  - B2 lost its server with the cause unconfirmed, most likely the same cap. Its summary was reconstructed from persisted files and labeled as such.
  - No repair or cap increase followed; 25 fallbacks stay in the arm.
- **Evaluation.** 140 selections were sealed, then exactly 1,400 recorded acquisitions were charged, in 7.4 s.
- **Replay.** The independent replay passed: 0 errors, primary recomputed, 1,400 charges reconciled, 4 of 4 mutations rejected.
- **Tests.** 1,352 tests pass.

## Deviations, all documented and none outcome-dependent

1. `protocol_v172_amendment1.md`: stage A1 failed at a pre-start port probe (TIME_WAIT) with zero requests and was repaired as A1R before any 14B scientific output. The runtime now waits for the port; A2 needed a 12 s wait.
2. `protocol_v172_amendment2.md`: the B1/B2 failures are recorded; a descriptive valid-response-only sensitivity was added before evaluation; and a runtime `close()` defect (a macOS `killpg` EPERM) is noted.
3. `protocol_v172_amendment3.md`: after evaluation, the independent verifier's parser alphabet was corrected. It had used lowercase before uppercase, against the grammar's order. The initial failed replay is preserved.
4. `protocol_v172_amendment4.md`: report wording only, plus freeze-file discovery. The first generated report is preserved.

## Replay commands (no new collection)

    .venv/bin/python scripts/analyze_v172.py --check
    .venv/bin/python scripts/report_v172.py --check
    .venv/bin/python scripts/verify_v172.py
    .venv/bin/python scripts/audit_v171.py --check
    .venv/bin/pytest -q -p no:cacheprovider tests
    .venv/bin/python scripts/seal_research_v172.py --verify-only

Collectors (`fetch_qwen_v172.py`, `prepare_v172.py`, `freeze_v172.py`, `collect_models_v172.py`, `evaluate_v172.py`) are create-once; do not rerun them into existing directories. Older sealers report STATUS.md and `next_experiment.md` as changed by design; `seal_research_v172.py` verifies the full chain through the snapshots.

## Counters (`artifacts/study_v172/closeout.json`)

- **Model starts.** Cumulative 4,973: 118 new generation requests, of which 117 were scientific and 1 was a synthetic compatibility request.
- **Recorded-table charges.** Cumulative 43,013 (1,400 new), plus 2 historical incidental exposures. Native counters are separate and unchanged.
- **Retained downloads.** 19,381,944,226 of the V172-approved 20 GiB cap; 2,092,892,254 bytes remain.
- **Model payload.** 18,128,110,983 of the V172-approved 19 GiB cap.
- **Scope of the approval.** The raised caps applied to V172 only; they are not standing permission.
- **Excluded activity.** No paid or cloud use, credentials, publishing, contact, remote push or system-wide change.

## Files and housekeeping

- **Weights still in `models/`:** Qwen3-14B (9.0 GB), Qwen3-8B (5.0 GB) and SmolLM3 (1.9 GB).
  - The **14B file is pinned by hash but not sealed as a file**, so it can be moved off this machine without breaking verification.
  - **SmolLM3 and Qwen3-8B are sealed by historical manifests (V65–V93) and must stay.**
- The two Qwen2.5 safetensors files were moved off-machine by the owner; nothing depends on them.

## Single most important next action

**Write the paper-shaped synthesis from V141–V172; do not collect more data with local models.** Pre-registered V172 found no testable router question for 3B–14B local models.
- **Larger models.** The remaining lever is a much larger model, such as SNAP2's gpt-oss-120b. It does not fit this hardware and would need new, explicit owner decisions on resources.
- **Other variations.** More seeds, prompts or interfaces on these exposed tasks would be exploration, not evidence.

No work continues outside this session.
