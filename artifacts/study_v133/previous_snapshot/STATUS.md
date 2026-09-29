# STATUS — V131–V132 complete: two new native families and prospective router test

Resume here, then `reports/research_assessment_v132.md`, `reports/native_v131.md`, `reports/router_v132.md`, and `reports/next_experiment.md`. All native collectors and the local model server exited. V131 collection allowances are closed. V132 reused those outcomes and adds no collection. No pending permission or background job. Do not rerun create-once collectors. Q2 readiness and useful selective routing remain unestablished.

## Latest concrete result

Two newly admitted native implementations, WavPack 5.9.0 and FFTW 3.3.11, ran with five seeds each (11, 23, 37, 53, 71). Source/workload admission preceded outcomes. Each B10 prefix branches to five B20 arms: sequential 3NN, batch 3NN, matched random proposals/projection, full-domain random, and actual local Qwen3-8B proposals. Initialization includes expert and ordinary-default settings. Branches have isolated state and independently charged continuations. All 50 logical arms end at 20 evaluations.

| New family | Primary mean model gain vs sequential 3NN | Wins/ties/losses | Interpretation |
|---|---:|---:|---|
| WavPack | +0.0058% | 2/2/1 | Mean 25.2 bytes on roughly 432 KB: tiny positive, below the 1% practical margin |
| FFTW | −1.5160% | 1/0/4 | Fresh timing validation; the apparent positive case uses identical settings and reflects variability |

WavPack paired byte gains are −126, +126, 0, 0, +126. Gain versus ordinary default is +3.0098%, versus expert +0.0497%; weaker comparators exaggerate incremental model value. FFTW's two different model-selected configurations are worse in every fresh mixed-order block; their median gains are −5.0751% and −2.7494%. Its other three pairs use identical settings. Keep initial selection timings (mean −1.4095%) separate from fresh validation (primary −1.5160%).

V132 fits benefit-aware ridge and uncertainty-only rules on 40 historical pairs from eight software groups, with group-exclusion development folds, training-only preprocessing and development-calibrated thresholds. All ten new decisions were saved before any new model continuation or fresh timing validation existed. Neither rule calls the model on any new case; both match never-escalate, as do matched zero-rate random policies. This is an actual prospective decision test, but no selective-router advantage. The raw hindsight oracle is non-deployable; its apparent FFTW benefit partly reflects identical-setting timing variability.

A separately labeled post-hoc action-equivalence diagnostic finds zero observed >1% beneficial different-configuration cases and two >1% harmful different-configuration cases. It does not replace the raw primary metric or establish a population bound. Do not tune a nonzero escalation rate on these now-exposed groups.

## What actually ran and costs

**648 native configuration trials:** 500 classical-stage trials, 100 real-model continuation trials, three WavPack expert repeats and 45 FFTW timing-validation trials. All passed correctness checks. WavPack: 303 configurations, 909 encodes and 909 external decodes with exact raw-sample size/hash identity. FFTW: 345 workers, each with complete complex-output validation against NumPy pocketfft. The 45 fresh validation trials never feed back into selection. No native failures or model fallbacks.

**Ten real local Qwen3-8B Q4_K_M calls:** 10/10 valid, zero retries; 473 generated and 5,050 prefill tokens observed, no missing usage; 10,240 output tokens allocated. Model lifecycle 44.723 s including 3.053 s startup, peak sampled process-group RSS 6,025,412,608 bytes; server exit 0. Native collection stages took 118.686622417 + 27.2274835 = 145.914105917 s. Original controller fit/decision wall time was not recorded and is unknown, not zero.

Modeled deployment: 20 native evaluations plus one request when escalating, versus 20 classical evaluations when not. Actual paired research paid for all ten requests and all alternatives regardless of the zero-call policies. Repeats, validation, compilation and preparation are separate research costs. No inferred dollar or energy savings.

Frozen limits: classical 500 trials/900 s; continuation/repeats/validation 148 trials/300 s; native subprocess 10 s; model 10 requests/10,240 allocated tokens/600 s/8 GiB RSS/180 s transport/zero retry. Total collection ceiling 1,800 s. No implicit extension is authorized by replay.

## Protocol and sources

V131 freeze: `reports/protocol_v131.freeze.json`, 5,088 inputs, SHA256 **3935a8059fcd54755c33b7a2c21680c64176465eff8e141dc86de46bdb2cf2e4**, before the first native outcome. Prefix-only prompts/jobs were separately frozen in `artifacts/study_v131/inputs.freeze.json` before inference.

V132 is an explicit versioned router addendum to V131's original no-router scope. Frozen after classical collection but before model continuations/fresh validation: `reports/protocol_v132.freeze.json`, SHA256 **0542e76084b97ca359ab8565d8c64215a1dd733ae3d9b27ab2861918041bf31e**. Fit uses no classical post-checkpoint targets, new model responses or future costs. Temporal receipt: `artifacts/study_v132/before_outcomes.json`. Seven pre-decision features, fixed ridge alpha 1, group-equal weights and development-only threshold grid. Historical training mixes recorded/native tasks, initialization and 512/1,024-token contracts. SAC's structurally impossible old representation is excluded only from compatible training; its failures and costs remain in historical evidence.

WavPack official 5.9.0 release SHA256 **b5291bc4e6d69ebbd3da3800c5bf4a70f19bb92679b23e09b3b612c1e648d1ff** (local pin, not claimed owner-published checksum). BSD-3-Clause; David Bryant. FFTW official 3.3.11 owner MD5 **40ec8d0447d03b8f01f8c90aa77bd16f** verified, SHA256 in source receipts; Frigo/Johnson authors, Frigo/MIT library copyright, GPL-2.0-or-later library with separately noted API-header license exception. Local static double/NEON/pthreads build; no system changes. Build times WavPack 8.914996917 s, FFTW 97.397132083 s. Sources, licenses and build commands are under `artifacts/sources/v131/` and `artifacts/study_v131/`; audit `reports/source_audit_v131.md`.

Reuse three V130 CC BY 4.0 LibriSpeech clips (26.655 s total). WavPack uses full 16-kHz mono 16-bit clips; FFTW uses first 8,192 samples of each, 8 warmups then 256 executions per clip. FFTW target includes input reset and execution, excludes planning; every complex value checked against a saved pocketfft reference. Domains: 80 codec and 36 FFT argument vectors, with possible effective equivalences. Same shared speech input does not provide unrelated workload evidence. No new full-domain target scan. No second-host rerun or broad upstream conformance suite.

## Tests, replay and preserved failure

**Full tests: 1,042 passed**, 14 dependency warnings, 31.20 s, via `.venv/bin/pytest -q tests`. Log: `artifacts/study_v132/all_tests.log`. New focused tests: eight V131 and four V132.

Independent standard-library verifiers reconstruct all 648 native receipts, physical saved outputs, 50 B20 arms, ten real responses and 45 fresh timing validations; also all 50 prefix feature rows, historical training targets, group folds/scaling/ridge fits/thresholds, decisions and ordering before all 148 new native starts. Receipts: `artifacts/study_v131/verification.json`, `artifacts/study_v132/verification.json`.

Both reports, both comparison JSON files and the scientific figure reproduce byte-identically (`artifacts/study_v132/reproduction_final.json`); figure visually inspected. Semantic corruption of a serialized native target is rejected after its transport hash is refreshed (`mutation_check.json`). Compact replay is verified but is not fresh model/native execution or second-host replication.

Compact bundle: `output/v132_replay.zip`, **1,370,953 bytes / 870 hashed files**, standard-library-only replay, ZIP CRC verified. It excludes audio, physical encoded/numerical outputs, source archives, binaries and weights; full local verification checks these separately. Latest package receipt: `artifacts/study_v132/package_notes_final.json`. Initial packaging failed because the release license filename is `COPYING`, not the repository's `license.txt`; failure script/receipt and partial folder preserved. No experiment outcomes were affected.

Key evidence:

- Assessment: `reports/research_assessment_v132.md`.
- Native results/figure: `reports/native_v131.md`, `results/v131_native/comparison.json`, `results/v131_native/comparison.png`.
- Router result: `reports/router_v132.md`, `results/v132_router/comparison.json`.
- Raw native records and outputs: `results/v131_native/classical/`, `results/v131_native/continuations/`.
- Real model prompts/raw responses/usage/server logs: `results/v131_proposals/`.
- Frozen historical training/folds/model/decisions: `artifacts/study_v132/`.

Safe commands (no new objective/model collection):

```sh
.venv/bin/python scripts/verify_native_v131.py
.venv/bin/python scripts/verify_router_v132.py
.venv/bin/python scripts/analyze_native_v131.py
.venv/bin/python scripts/analyze_router_v132.py
.venv/bin/python -I -S output/v132_replay/replay.py
.venv/bin/python scripts/seal_native_router_v132.py --verify-only
```

Do not rerun create-once source/preparation/native/model/router-fit/packaging scripts as an implicit restart. The native and router analysis scripts above regenerate saved-data reports only.

## Next action and remaining limits

**Most important next action: extend the locked, correctness-checked comparison to additional independently admitted software families before further controller tuning.** Admission must precede outcomes and must not require a favorable model result. WavPack, FFTW, FLAC and all earlier families are exposed. More seeds/prompts on them do not create new held-out systems. A coherent larger native cohort, meaningful benefit variation, close-prior-work novelty assessment and cross-model/host robustness remain needed. Two new groups, tiny codec effects and timing variation cannot certify a journal quartile. A narrower negative contribution may be viable; H1/H2 and Q2 readiness remain unsupported. No external permission currently blocks ordinary source admission. Nothing continues outside the active session.

Cumulative real model requests **4,490** (4,480 + 10). Recorded-table acquisitions unchanged: **35,570**, plus two incidental ExaStencils vectors = 35,572 exposed recorded vectors. New native counts: WavPack 303 configurations/909 encodes/909 decodes; FFTW 345 workers. Prior FLAC 303/909/909 plus three preparation decodes unchanged. Older native counters remain separately documented: numerical 880; NGINX 81 attempts/35,853,130 validated responses; DuckDB 78; H2 299; Kanzi 1,265; RocksDB 350. This is not one exhaustive homogeneous count.

New saved source/metadata downloads **5,152,157 bytes**, 4.330 s; cumulative **10,234,093,856/10 GiB**, remaining **503,324,384 bytes**. Model payload unchanged at 9,126,358,023/9 GiB. Web transfer unknown, not zero. No new model/package/corpus download, cloud spending, credentials, system-setting change, contact, push or publication.

Combined seal: `artifacts/study_v132/evidence_manifest.json`, receipt `seal_verification.json`; anchors V130 SHA256 **4fda8d683fc6a20097baf31c06dad035a863c488f73308660fb089aea4c6c196** and preserves older checkpoints. Previous mutable root docs and their mapping are in `artifacts/study_v131/previous_snapshot/`. Preserve the combined seal and snapshots before any future root-document edits. Older interrupted runs, capacity failures and adaptive history remain unchanged.
