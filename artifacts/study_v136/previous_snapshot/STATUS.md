# STATUS — V133–V135 complete: attribution evidence and a valid negative SAC repair

Resume here, then `reports/research_assessment_v135.md`, `reports/jpeg_v133.md`, `reports/attribution_v134.md`, `reports/repair_v135.md`, and `reports/next_experiment.md`. All finite collectors, model servers and tests have exited. V133/V135 collection allowances are closed. No pending external permission or background job. Do not rerun create-once collectors. A concrete negative research result exists; a successful benefit-aware router and Q2 readiness remain unestablished.

## What actually ran this continuation

**V133: one new native libjpeg family.** Owner libjpeg-turbo 3.1.2 predictive lossless mode, three real full-resolution RGB photographs, five fixed seeds11/23/37/53/71. Seventy configurations over predictor, restart rows and RGB scan layout. Every output is decoded by a separate djpeg process and all pixels/dimensions checked. Same-library decoder remains a limitation. Thirty logical B20 arms share B10 prefixes: sequential3NN, batch3NN, matched random proposals, random full-domain, cheap predictor sweep, and actual Qwen3-8B. Strong reference is not assumed: predictor7 is a fixed anchor, and the additional sweep explicitly tests cheap domain knowledge.

353 physical configurations:50 shared prefix +250 classical continuation +50 model continuation +3 reference repeats; **1,059 encodes and1,059 decodes**, all correct. No failure/fallback/retry. Primary model gain versus sequential: **−0.0455%,0wins/3ties/2losses**. Model versus predictor sweep: five ties. **None of the five model continuations improves its B10 incumbent.** Sequential continuation improves two runs. Apparent gain versus the left-predictor anchor is+4.5716%, entirely achieved before escalation. Do not call that added LLM value.

Five actual model requests, all valid:215generated/2,730prefill tokens, no missing usage;5,120output tokens allocated. Lifecycle21.772151417s, startup2.836792125s, peak sampled server RSS5,989,859,328bytes; server exit0. Native stages19.791341334s +3.460952541s, total23.252s (exact ledgers retained). Feature/prediction time0.002431s across five cases. Historical controller training time remains unknown.

**V134: retrospective attribution audit, zero new collection.** All60 normal cases/12 families in the full-domain proposal series V127/V129/V130/V131/V133, retaining five old SAC fallbacks.15policy outcomes improve their prefix; only4 beat sequential continuation. Among55valid-model cases,13 and4. Positive paired cases: HIPAcc11+1.8271%; WavPack23/71+0.0291%each; FFTW23+1.1020%, but that pair selects identical settings and measures timing variability. Raw FFTW primary remains unchanged. SAC fallback improvements are executed-policy outcomes, not successful LLM responses. Older methods/label-rotation probes remain separately preserved; this is not the whole repository, a uniform confirmatory cohort or60independent systems. No pooled population estimate.

**V135: actual SAC capacity repair.** Same five historical SAC prefixes, same original prompt bytes and sampling seeds, same model/runtime; existing1024-token/canonical-grammar treatment replaces the failed512-token/whitespace-permitting contract. Fifty-nine features have a conservative622-token constructive upper bound including EOS. All **5/5new responses valid**, no fallbacks/retries; **0/5improve prefix**. Mean gain vs historical sequential3NN **−0.4036%,0/3/2**. Exactly50new recorded outcomes charged, five B20 arms, all selections sealed before target parsing. Source correctness/noise/redistribution limitations remain; this is an exposed-family repair, not another holdout or native execution.

V135 model cost:3,013generated/9,500prefill tokens, no missing usage,5,120allocated; lifecycle160.238925375s, startup2.570552500s, peak sampled RSS6,679,609,344bytes, server exit0. Evaluation0.069s, exact ledger retained. Historical classical/control costs remain historical; none are relabeled as free or newly executed. Optional historical single-portfolio control exists for **two seeds only**, shown with its actual denominator; primary comparisons retain all five.

New collection this continuation: **10real requests,353native configurations,50recorded accesses**,3,228generated/12,230prefill tokens,10,240allocated output tokens. Actual model lifecycle182.011s. Sources/build/preparation/paired alternatives are additional collection costs. Modeled deployment costs only one selected B20 arm plus a request when escalating, with explicit startup/controller overhead. Zero-call policies do not erase research collection costs. No dollar/energy savings claimed.

## Frozen controls and limits

V133 native freeze: `reports/protocol_v133.freeze.json`,5,757inputs, SHA256 **2144a2f46207519c707af0d01a3e6235f4fa2f0af12eca52d9f064c100abb558**, before any native outcome. Prompt/prefix/decision seal: `artifacts/study_v133/inputs.freeze.json`. Unchanged V132 historical model (40pairs/eight groups); each V133 decision saved before that seed's classical continuation and all model requests. Benefit and uncertainty rules select0/5calls, match never, and show no selective advantage. Together with V131, only three new groups have this frozen-router test; repeated seeds are not independent systems.

V133 bounds:300classical trials/900s,53final trials/300s,10s per native command; five requests/5,120allocated tokens/600s/8GiB RSS/180s transport/zero retry. Collection total ceiling1,800s. Source retrieval20MB/180s, build300s. Actual retrieval3,937,204bytes/12.792s, local build7.122s.

V134 explicitly post-outcome exploratory protocol: `reports/protocol_v134.md`; source hashes `results/v134_attribution/inputs.json`. No model/native/refit/data download allowance.

V135 freeze: `reports/protocol_v135.freeze.json`,6,226inputs, SHA256 **4abcde01b5efbb44a3ae07322941ad19271571bfc0f5760da9386e34a99133d3**, before new requests/outcomes. Five requests/5,120allocated tokens/600s/8GiB/180s transport/zero retries;50recorded accesses/180s; no native run or download. Separate allowance, no modification to V133. All selected rows pinned in `results/v135_analysis/selection_seal.json`. This repair changes cap and grammar together; same seed does not imply cross-runtime deterministic output. Original V127/V134 failures remain intact.

## Sources, integrity and failures

libjpeg-turbo owner tag3.1.2 source archive local SHA256 **560f6338b547544c4f9721b18d8b87685d433ec78b3c644c70d77adad22c55e6** (not claimed owner-signed checksum). Composite IJG/modified-BSD/zlib notices retained. Static cjpeg/djpeg built project-locally with Xcode clang/SDK15.5, no system install. Predictor/scan semantics verified against owner manual and source. No source patch. See `reports/source_audit_v133.md`, `artifacts/sources/v133/`, `artifacts/study_v133/build.json`.

scikit-image v0.20.0 astronaut(NASA/public domain), coffee(Rachel Michetti/CC0), rocket(SpaceX/public-domain attribution): all three verified against owner's SHA256 registry. Existing Pillow12.3.0, pinned in requirements.lock.txt, prepares complete RGB PPMs with no resize/crop. Rocket starts as JPEG; its decoded pixels are the task input. No scikit-image package installation, new weights or generated fixture used as measured workload. Photographs and source images remain local.

Preserved setup/report failures: restricted DNS fetch failed with0bytes before successful bounded authorized retrieval; an initial reporting script assumed optional single-portfolio control existed for all seeds and raised KeyError. Failure source/receipt retained under `artifacts/study_v135/report_failure*`; corrected optional-control denominators and regression tests. No new objective/model acquisition from reporting retries. A restricted exploratory curl produced no output. Web-provider traffic sizes unknown, not zero. Older failures/positive exceptions/adaptive stages unchanged.

## Verification and reviewable evidence

**Full suite:1,059passed**,14dependency warnings,31.23s, command `.venv/bin/pytest -q tests`, receipt `artifacts/study_v135/all_tests.log`. Earlier run receipts1,051/1,057also retained; use latest. Synthetic fixtures and deliberate corruption live in separate test/mutation namespaces and never enter measured aggregates.

Independent standard-library replay verifies353native receipts, saved encoded-file hashes,30logical B20arms, five real JPEG responses, prefix-only features/decisions and ordering; reconstructs60retrospective source/metric/direction/denominator rows; reconstructs five repaired SAC responses/projections,50charged original source rows, prefix/state identity and historical controls. Receipts: `artifacts/study_v133/verification.json`, `artifacts/study_v133/attribution_verification.json`, `artifacts/study_v135/verification.json`.

Eight report/JSON/figure artifacts reproduce byte-identically (`artifacts/study_v135/reproduction.json`, `final_reproduction_check.json`); both figures visually inspected. Native/attribution summary mutations are rejected; altered SAC result is rejected even after refreshing compact transport hash (`mutation_checks.json`, `compact_mutation_check.json`).

Compact private bundle: **`output/v135_replay.zip`,1,753,505bytes,643hashed files**, ZIP SHA256 **eece30d8a01cbbc1785d25eadac9edece70b988d9c4e1e3cc5b3ce8af8e78c95**, CRC verified. Python standard-library-only replay, no network/new inference/objectives. Excludes photographs, encoded outputs, full original tables, source archives, binaries and weights. Includes only already acquired source-row extracts for the SAC repair. Full local verification additionally checks omitted physical/source artifacts. This is not fresh native execution, second-host replication or public redistribution permission.

Key evidence:

- Assessment: `reports/research_assessment_v135.md`.
- Native report/raw logs/figure: `reports/jpeg_v133.md`, `results/v133_native/`, `results/v133_native/comparison.png`.
- Native-model provenance: `results/v133_proposals/`.
- Retrospective audit/figure/input mapping: `reports/attribution_v134.md`, `results/v134_attribution/`.
- SAC repair/model logs/charged acquisitions: `reports/repair_v135.md`, `results/v135_proposals/`, `results/v135_analysis/`.
- Source/build/tests/verification/failure/cost receipts: `artifacts/study_v133/`, `artifacts/study_v135/`.

Safe commands (no new collection):

```sh
.venv/bin/python scripts/verify_jpeg_v133.py
.venv/bin/python scripts/verify_attribution_v134.py
.venv/bin/python scripts/verify_repair_v135.py
.venv/bin/python scripts/analyze_jpeg_v133.py
.venv/bin/python scripts/attribution_v134.py
.venv/bin/python scripts/report_repair_v135.py
.venv/bin/python -I -S output/v135_replay/replay.py
.venv/bin/python scripts/seal_research_v135.py --verify-only
```

Do not rerun fetch/build/prepare/collect/jpeg classical-or-continuation/evaluate_repair/packaging scripts as an implicit restart. Analysis/replay does not authorize new objectives or requests.

## Next action, interpretation and remaining resources

**Most important next action: freeze a cost-accounted batch-versus-sequential-feedback LLM comparison from identical prefixes.** Interaction style is a material adaptation from source methods; address that uncertainty before more unrelated small native tasks. Charge every additional request and newly acquired outcome. Existing families are exposed, so such a method diagnostic is exploratory; subsequent generalization still needs a coherent independent cohort. See `reports/next_experiment.md`.

Current evidence supports a bounded negative claim about this local8B batch-proposal implementation. It does not establish H1/H2, universal LLM failure, novelty, an exact SNAP2/LLAMBO replication/refutation or Q2 readiness. Cross-model/host robustness, wider native workloads, independent decoding and sufficient independent held-out groups remain untested. Do not collect repeatedly merely to obtain a favorable result. No external-resource permission is currently pending. Nothing continues outside the active session.

Cumulative real model requests **4,500** (4,490+10). Experimental recorded-table acquisitions **35,620**, plus2incidental ExaStencils exposures =35,622exposed recorded vectors. New libjpeg353native configurations/1,059encodes/1,059decodes. Prior native counters remain separate: WavPack303/909/909, FFTW345workers, FLAC303/909/909 plus3preparation decodes; older numerical880, NGINX81attempts/35,853,130validatedresponses, DuckDB78,H2299,Kanzi1,265,RocksDB350 and earlier native series retain their own ledgers. Not one exhaustive homogeneous total.

Cumulative saved downloads **10,238,031,060/10GiB**, remaining **499,387,180bytes**. Model payload unchanged9,126,358,023/9GiB. No new package/model payload, paid/cloud inference, credentials, system changes, contacts, publication or push.

Combined seal: `artifacts/study_v135/evidence_manifest.json` and `seal_verification.json`, anchors V132 manifest SHA256 **7ec4146fd052356944c5781e5d84d28e7eb2281d009bc47684f3b3c5b3ada3fc** and preserves previous checkpoints. Previous mutable root documents and mapping are in `artifacts/study_v133/previous_snapshot/`. Preserve this combined checkpoint before future root-document edits. V134 is retrospective and V135 is a separate exposed repair, never silently relabel either as untouched evaluation.
