# STATUS — V136 complete: matched feedback adds no final-score benefit

Resume here, then `reports/research_assessment_v136.md`, `reports/feedback_v136.md`, `reports/protocol_v136.md` and `reports/next_experiment.md`. The finite collector and its model server exited; no job or external approval is pending. The V136 allowance is closed. Do not rerun create-once collectors. Scientific evidence remains insufficient for a successful benefit-aware router or a Q2-readiness claim.

## Actual new result

**100 real local Qwen3-8B calls and200 newly charged recorded evaluations completed**, with20 B20 arms from10 saved B10 prefixes. Two exposed systems, LLVM(10features) and SAC(59), selected by smallest/largest feature counts among the six original families. All five fixed seeds11/23/37/53/71. Two proposals per round, five calls per arm. Feedback sees its own new measurements; the matched masked arm sees tried settings with new measurements withheld. Same initial prefix, paired per-round sampling seeds, deterministic shuffled/interleaved execution, isolated states and charged oracle acquisitions.

**Feedback and masked finish with the same incumbent in10/10 cases.** Neither beats historical sequential3NN in any case: each family has0wins/3ties/2losses. Mean model gain versus sequential: LLVM−0.9688%, SAC−0.4036%. Each model arm improves two LLVM prefixes (mean+1.5642%) and two historical one-shot outcomes (mean+1.5009% across five seeds); both matched arms share those gains. SAC has no prefix improvements. Historical one-shot prompts/caps/seeds differ, so this is not a causal estimate of call-count benefit. Previous historical controls retain their original collection costs.

All100 responses valid,0fallbacks/0retries.172/200 proposals need nonzero Hamming projection;112match already acquired configurations before projection and10repeat their partner within a round. All executed rows are unique within each B20 arm. Initial matched prompts/seeds produce identical output10/10. A **post-outcome exploratory trace audit** finds changed outputs36/40 follow-up pairs and changed selected rows27/40, yet no final-score benefit. Do not infer that the model ignored feedback; changed responses alone do not establish useful feedback.

LLVM's source target is compiler optimization time; SAC's is n-body simulation execution time, both minimized in original recorded units. No new native execution, correctness/noise verification or independent family added. Two systems, not ten independent systems. No router fitting, threshold selection or new holdout claim.

## Collection cost and limits

Actual model lifecycle854.842235875s; total collection854.843790959s; startup3.044558291s; server exit0; peak sampled RSS6,336,479,232bytes. Observed7,378generated and140,387prefill tokens, no missing usage.25,600output tokens allocated. Recorded evaluation0.090712s (exact value in comparison.json), not native workload runtime. Paired collection counts both arms and all200 newly acquired outcomes even when targets were seen historically. No new downloads, packages, weights, paid/cloud inference, credentials, system changes, contact, publication or push.

Modeled deployment for one selected arm: five requests,1280allocated output tokens, ten new evaluations after B10, B20total. Per-arm measured request times exclude shared startup and historical prefix/controller overhead. No dollar, energy or real-workload cost savings inferred. On objective quality and request count only, the historical classical continuation weakly dominates these model outcomes.

Frozen bounds:100requests,200acquisitions,25,600allocated tokens,1600smodel/1800stotal,8GiB sampled serverRSS,180s/request,zero retries/probes/downloads/spending. `reports/protocol_v136.freeze.json`:6,248inputs, SHA256 **88a8d1bd8ebcfccac72ddb785fb8709ad69d074fade1a17937e3f7d8a0dbe41e**. The freeze predates all new generation/acquisition. Every round saves decision state/messages, rendered template/tokens/payload/capacity proof, raw response and selected rows before target parsing. Full original source/model/runtime hashes retained.

## Verification and reproducibility

**Full suite:1,065passed**,14dependency warnings,32.22s: `artifacts/study_v136/all_tests.log`. Five precollection interface tests check masked-label noninterference, feedback sensitivity, prefix identity, capacity/context, projection novelty and malformed outputs. A later synthetic transport-failure integration test verifies all20 intended arms/200 charged labels and labeled fallbacks. Its first fixture omitted a temporary results parent and failed before any generation; fixture corrected. These fixtures are never measured results.

Independent standard-library replay reconstructs all100 rounds, sampling order, exact model messages/masking, raw parse/projection, source-row acquisitions, selection-before-acquisition ordering,20 B20states, historical controls, group comparisons, costs and post-outcome trace audit. Full local replay checks complete source file hashes; compact replay uses only already acquired source-row extracts. Receipts: `verification.json` and `compact_verification.json` under artifacts/study_v136.

Five report/JSON/PNG/SVG/trace artifacts reproduce byte-identically on two repeated analysis runs (`reproduction.json`). Figure visually checked (`visual_review.json`). Four isolated corruption tests reject fabricated aggregate gain, budget undercount, acquisition-before-selection and a leaked masked measurement, even after refreshing the altered file's compact transport hash (`mutation_checks.json`).

Private compact bundle: **output/v136_replay.zip**,1,644,675bytes,479hashed files, SHA256 **b3ff9dc3b3d45a2216e9655c11bc9ffc96a4cbfd91aedc0fe2aa4f52540b3e43**, CRCverified. Python standard-library replay, no network/inference/new objectives. Excludes full tables, model weights and runtime binaries. This is saved-record replay, not independent-host fresh execution or new redistribution permission.

Matplotlib used its permitted temporary font cache because the home cache is not writable; figures reproduced successfully. Initial sandboxed process listing was denied; purpose-bound read-only listing then verified no collector/model server remained. No experimental failure or hidden retry resulted. See process_check.json.

## Evidence and commands

- Assessment: `reports/research_assessment_v136.md`.
- Result/report/figure: `reports/feedback_v136.md`, `results/v136_feedback/comparison.json`, `comparison.png` and `comparison.svg`.
- Actual raw evidence: `results/v136_feedback/decisions`, `preflight`, `generation_starts.jsonl`, `responses.jsonl`, `selections`, `acquisitions.jsonl`, `rounds`, `arms`, `ledger.json` and `summary.json`.
- Protocol/admission/provenance: `reports/protocol_v136.md` and freeze; `configs/study_v136.json`; `artifacts/study_v136/jobs.json`, `admission.json`, `candidates/`.
- Tests/replay/receipts: `artifacts/study_v136/` and `output/v136_replay.zip`.

Safe commands (zero new collection):

```sh
.venv/bin/python scripts/verify_feedback_v136.py
.venv/bin/python scripts/analyze_feedback_v136.py
.venv/bin/python -I -S output/v136_replay/replay.py
.venv/bin/python scripts/seal_research_v136.py --verify-only
```

Actually executed collection command: `.venv/bin/python scripts/collect_feedback_v136.py`. It is create-once and must not be rerun as a resume action. `prepare_feedback_v136.py` and `package_feedback_v136.py` are also create-once. Analysis/replay does not authorize more requests/acquisitions.

## Continuity, interpretation and next action

Previous V133–V135 results are unchanged: native JPEG no model prefix improvements; retrospective full-domain60case/12family audit retains positive exceptions and old failures; corrected SAC representation produced5valid responses but no prefix improvements. V136 addresses one interaction uncertainty using matched calls, not the exact source method or an untouched test set. SNAP2/LLAMBO source mapping remains `reports/source_mapping_v127.md`. No journal quartile/acceptance or universal LLM-failure claim is justified.

**Single most important next action: freeze a coherent independent system cohort and comparator contract before further collection.** Include a cheap incumbent-neighbor/projection control alongside classical search and the fixed feedback/masked treatments. Predeclare validity/independence admission, practical margins, grouped analysis and finite cost caps. Audit exposure history before calling any family held out. Cross-model/host replication and representative native correctness/noise remain untested. Do not select new settings merely to obtain a positive result.

Cumulative real model requests **4,600** (4,500+100). Experimental recorded-table acquisitions **35,820**, plus2incidental exposures =35,822exposed vectors. Native counters remain unchanged and separate, recorded in the previous checkpoint. Saved downloads remain **10,238,031,060/10GiB**, remaining499,387,180bytes; model payload9,126,358,023/9GiB unchanged. No new allowance is implied by reporting these remaining bytes.

V135 sealed manifest SHA256 **69f6fd022b73a8edc40865a4210ef40672fe2c489e0ddd452dd646fdd256965b** remains anchored. Previous root STATUS/README/THIRD_PARTY/next_experiment and mapping are in `artifacts/study_v136/previous_snapshot/`. A stale V135 config split label is preserved with erratum `prior_metadata_erratum.json`; its protocol/report already correctly identify exposed development. V136 combined seal: `artifacts/study_v136/evidence_manifest.json` and `seal_verification.json`. Preserve this checkpoint before future root-document edits. Nothing continues outside the active session.
