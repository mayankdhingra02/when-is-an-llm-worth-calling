# STATUS — V130 complete: new native FLAC family, negative primary comparison

Resume here, then `reports/research_assessment_v130.md`, `reports/flac_v130.md`, `reports/source_audit_v130.md`, and `reports/next_experiment.md`. All collectors and the local model server exited. V130 collection allowances are closed. Do not rerun create-once preparation, native or model collectors. There is no pending external permission, paid endpoint or background job. Q2 readiness and useful unseen-system routing remain unestablished.

## Latest concrete result

Admitted and actually executed FLAC 1.5.0, a new implementation family in this repository. Three real licensed LibriSpeech clips, 26.655 seconds in total, selected by a prewritten speaker/filename rule. All clips/seeds stay in one FLAC group. This is a descriptive new-family pilot, not a multi-family held-out cohort. The application domain remains related to earlier compression tasks.

Five fixed seeds 11, 23, 37, 53, 71. Every B10 prefix starts with the strongest documented preset8, then two shuffled configurations and seven sequential3NN selections. Each saved prefix branches to five independently collected B20 arms: sequential3NN, batch3NN, random feature proposals with matched projection, random full-domain, and real local Qwen3-8B proposals. Finite domain96 argument vectors over block size/LPC/Rice order; distinct settings need not produce distinct outputs. No hidden objective table, target normalization or full-domain hindsight screen.

| Comparator | Mean model gain in bytes | Wins/ties/losses |
|---|---:|---:|
| Sequential3NN (primary) |−0.1869%|0/2/3|
| Batch3NN |−0.2090%|0/3/2|
| Matched random proposals/projection |+0.0479%|2/2/1|
| Random full-domain |−0.1980%|0/3/2|
| Standard strongest preset |+2.6860%|5/0/0|

Positive gain means smaller files. The preset improvement does not demonstrate LLM value: cheap search also improves that preset, and no LLM continuation beat the matched sequential counterfactual. The model improved its own prefix in seeds23/71, but by less than the classical continuation. Two other seeds had already found their final incumbent atB10. On these five observed pairs, even hindsight routing cannot improve quality over never-escalate. This is not a population bound or learned-router evaluation. Keep earlier positive exceptions and differently designed stages separate.

## What actually ran and costs

**303 native configuration trials:**50 shared prefix trials +250 continuation trials +3 separately charged post-selection preset repeats. Each trial encodes three clips, so909 encoder calls and909 external decoder calls, plus three preparation decodes. Every measured output passed internal `-V` verification and exact external raw-sample SHA256/length checks. All preset repeats were455,080bytes, matching five initial preset trials. No native failures or model fallbacks. Same-implementation decoder remains a limitation; no distinct decoder/second-host validation.

**Five real Qwen3-8B Q4_K_M requests:**5/5valid, zero retries/fallbacks;211 observed generated and2,395prefill tokens, no missing usage.5,120output tokens allocated. Model lifecycle20.244s including2.791s startup; peak sampled process-group RSS5,943,099,392bytes; server exit0. Native collection lifecycle14.441s. These are actual local collection costs, not cloud-dollar/energy/latency-optimization claims.

Deployment estimate:20 configuration trials +one request on an escalation, versus20 classical trials or one preset-only trial. The paired alternatives, three repeats, corpus decode and compilation are research overhead. Logical25arms each useB20; physical overlap between arms did not make trials free.

Limits frozen before first native outcome: classical250trials/900s; final53trials/300s; native subprocess10s; model5calls/5,120allocated tokens/900s/8GiB/180s transport/zero retry. No cloud/paid inference or experiment downloads. `reports/protocol_v130.freeze.json` pins925inputs, SHA256 **7c430e5719bea915af026a8081dd4a430874d3349e2c57be7664de99eed5e89c**. Prefix-only prompts/jobs separately sealed in `artifacts/study_v130/inputs.freeze.json` before model inference.

## Source, build and preserved failures

Official FLAC1.5.0 release SHA256f2c1c76592a82ffff8413ba3c4a1299b6c7ab06c734dee03fd88630485c2b920, owner checksum verified. CLI GPL-2.0-or-later, libFLAC Xiph BSD-style license. Project-local build with matching Xcode compiler/SDK15.5; no system settings/install. Binary SHA256bd5914ff8052624308d8eb9a72a967f1580e531d40974ad21e14423d2ae2f1ae. Existing gettext library hash/linkage recorded. No broad upstream conformance suite executed.

OpenSLR12 official LibriSpeech test-clean archive, CC BY4.0, Vassil Panayotov2014; owner MD5 verified and SHA256 recorded. Full clips61-70968-0000,121-121726-0000,237-126133-0000 decode to16kHz mono16-bit PCM, no resampling/trimming. The corpus's original “test-clean” label is not this research's holdout label. Saved selection, sample manifests and original notices under `artifacts/study_v130/`, `data/native_v130/`, `artifacts/sources/v130/`.

Retained setup failures: initial sandbox DNS lookup (0bytes); compiler/SDK mismatch; incorrect CMake target name (`flac` vs source-defined `flacapp`); pre-freeze restricted hardware sysctl query. No encoding/model outcome was produced by those failures. Logs and error receipts remain. Fresh CPU/RAM query unavailable in sandbox; previous verified hardware was M3 Pro/18GiB. No retry was hidden in frozen collection.

## Verification and reviewable evidence

**Full tests:1,030passed**,14dependency warnings,35.15s with `.venv/bin/pytest -q tests`. Default pytest discovery only covers tests/synthetic:1,003passed; new focused tests6passed. Use the explicit tests argument when comparing historical full-suite counts.

Independent standard-library replay reconstructs initialization, sequential3NN stable ties, all prefix-only model examples, response decoding/projection,25pairedB20arms,303charged native trials,909encoder/909decoder records, every saved encoded-file hash, all byte targets and comparison arithmetic. Deliberately corrupted model-byte comparison is rejected even after refreshing its transport hash. ZIPCRCpasses. Report/JSON/figure reproduce byte-identically; figure visually inspected. Saved-evidence replay is not second-host native/model execution.

- Assessment: `reports/research_assessment_v130.md`.
- Main report and figure: `reports/flac_v130.md`, `results/v130_native/comparison.png`.
- Native raw records/encoded outputs: `results/v130_native/classical/`, `results/v130_native/continuations/`.
- Prefixes/25arms/comparison: `results/v130_native/`.
- Real prompts/requests/raw responses/usage/server log: `results/v130_proposals/`.
- Source/build/freeze/tests/replay/mutation receipts: `artifacts/study_v130/`.
- Compact private replay ZIP: `output/v130_replay.zip`,572,512bytes,378hashed files. No weights/binaries/audio; compact mode verifies saved records, full verifier additionally checks physical outputs/dependency freeze. Kept local, not published.

Safe commands, no new objective or model collection:

```sh
.venv/bin/python scripts/verify_flac_v130.py
.venv/bin/python scripts/analyze_flac_v130.py
.venv/bin/python -I -S output/v130_replay/replay.py
.venv/bin/python scripts/seal_flac_v130.py --verify-only
```

Do not run `admit_flac_v130.py`, `decode_workloads_v130.py`, `flac_v130.py classical/continuations`, `collect_proposal_v130.py` or packaging again as an implicit restart. Full native source/audio/model artifacts are local; the small ZIP is a deliberately limited evidence subset.

## Most important next action and remaining scope

**Freeze a confirmatory comparison across additional independently admitted software families using the same strong controls and correctness contracts.** Source/workload admission precedes outcomes; do not screen for LLM wins. Keep FLAC and all previous families exposed. A larger native cohort and enough development/test groups are needed before another learned-router fit. The current original hypotheses, distinct contribution versus close prior work, cross-host/model robustness and representative native workloads remain unestablished. Additional seeds/prompt variants on these exposed families cannot certify Q2 readiness. No external permission currently blocks admission work. Nothing continues outside this active session.

## Cumulative ledger and evidence preservation

Real model requests **4,480** (4,475+5). Experimental recorded-table acquisitions remain **35,570**, plus2incidental ExaStencils vectors =35,572recorded exposures with categories retained. New native FLAC303configuration trials/909encodes/909external decodes, plus3preparation decodes. Older native counters unchanged: numerical880; NGINX81attempts/35,853,130byte-valid responses; DuckDB78;H2299;Kanzi1,265;RocksDB350; earlier compression/native series remain separately documented. Do not mistake this list for one exhaustive homogeneous acquisition count.

New instrumented saved downloads347,754,928bytes; cumulative **10,228,941,699/10GiB**, remaining **508,476,541bytes**. Model payload9,126,358,023/9GiBunchanged. Web-provider transfer sizes unknown, not zero. No package/model download, paid/cloud spending, credentials, system-setting change, contact, push or publication.

V130 seal: `artifacts/study_v130/evidence_manifest.json`, receipt `seal_verification.json`; anchors V129 SHA256 **9122669044b226845905970bc4b79337a93e566b4ad2a92547732f238cb33379** and preserves all older checkpoints. Previous mutable root docs and their hash mapping are in `artifacts/study_v130/previous_snapshot/`. Preserve this checkpoint before future root-document edits. Prior V128/V129 interrupted attempt, recovery costs, V127capacity errors and old adaptive history remain unchanged.
