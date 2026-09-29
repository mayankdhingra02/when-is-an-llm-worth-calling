# STATUS — V149–V153 complete: corrected routing analysis and real native Memcached result

Resume here, then `reports/research_assessment_v153.md`, `reports/native_study_v153.md`, `reports/router_v151.md`, `reports/novelty_audit_v153.md`, the frozen protocols and `reports/next_experiment.md`. All collection is finished, all native/model servers reaped, no job continues outside this session. No permission or memory blocker is pending. All V149–V153 finite allowances are closed. Scientific honesty overrides obtaining a positive result. The evidence is stronger, but a useful transferable router and Q2 suitability are not established.

## Actual new result

**440 real native objective evaluations and ten real local-model calls** ran: 40 Memcached feasibility probes, then a frozen 400-evaluation paired study. Existing SmolLM3-3B and Qwen3-8B Q4_K_M weights were used locally; no new weights, fabricated outputs, paid API or cloud compute. Model hashes, owner revisions and backend provenance are in `artifacts/study_v153/models.json` and each model's preflight seal.

V153: Memcached1.6.45/static libevent2.1.13, 64 settings (threads1..8 × requests/event[1,2,4,8,12,20,32,50]), five seeds11/23/37/53/71, seven arms. Controls: sequential3NN, adaptive-neighbor, fixed-neighbor, random rows, random prototypes. Each arm has **B20 =10 shared-prefix +7 new search +3 fresh incumbent-validation evaluations**. Physical collection is50prefix +175classicalsearch +70modelsearch +105validation =400 acquisitions,35logicalarms,62unique settings. All35choices were sealed before three randomized validation blocks. The primary target is the median of three fresh measurements, not the minimum observed search time. This is a changed budget/utility allocation from historical20distinct-search-label studies; do not silently pool them.

SmolLM always-call mean validation gain vs sequential **+0.0881%**,3wins/0ties/2losses, one >1%win and one >1%harm; vs adaptive **−1.3495%**. Qwen vs sequential **−0.4188%**,1/0/4,one >1%win and three >1%harms; vs adaptive **−1.8655%**. **Neither model beat both controls by >1% in any seed (0/5 each).** Both frozen benefit routers chose zero calls, missing one nominal sequential opportunity each. Uncertainty-q80 chose one call/model and lost0.1904%/0.0795%; SmolLM random-development-rate chose one and lost0.3409%. Full never/always/random/uncertainty/benefit and diagnostic oracle comparisons are saved. Oracle is not deployable.

**Six of ten model/sequential pairs chose identical configurations**, so their timing differences cannot establish configuration-selection benefit. **Seven of35validationarms exceed1%MAD/median**, maximum4.665%. The tiny positive SmolLM mean is not a robust useful optimization result. Five seeds are one family, not independent systems. Memcached was feasibility-explored before paired collection; do not call it wholly unseen. Router fitting used only older seven-ecosystem development data and was frozen before Memcached prefixes, but its recorded/search target differs from native validation medians.

All400evaluations passed exact response/counter checks, each with2,048,000timedGET/SEToperations (819,200,000total). Correctness is a fixed deterministic-value workload, not full protocol conformance or changed-value write testing. Native timing includes local client work/contention.399servers exited0; **one server required configured SIGKILL cleanup** after a correct measurement (acquisition236,Memcached23/SmolLM model-search), was reaped and remains in logs. No hidden retry. Model servers both exited0.

## V149 invalidation and corrected V151 analysis

V149's independent replay found short case-key collisions between Spark/Hadoop workloads. Its preliminary results are **invalid and excluded**, retained under `results/v149_router` and `artifacts/study_v149/invalid_analysis.json`; do not aggregate or cite them as a gain. Historical source experiments were unaffected. V151 qualifies IDs by engine family, adds a collision regression test, and refreezes/reruns the same fixed feature/model analysis without outcome-guided model changes.

V151 analyzed140historicalmodelcases (70/model): original7-feature ridge, richer18-feature ridge, depth2tree, RBFkernelridge; all preprocessing/calibration/modelselection in nested whole-group development folds. Every variant and q80 diagnostic remains visible. Eight-engine grouping: SmolLM selected one useful Spark call, equal-group gain **+0.00754%**, no joint useful call,9/10usefulcases missed; Qwen zero calls. **With related Spark/Hadoop merged into one ecosystem, both selected predictors choose zero calls.** Always-call losses are4.956%/5.240% under this conservative grouping. Practical wins are concentrated in one shared ecosystem. These are exploratory analyses of exposed outcomes, not prospective confirmation or a population significance claim.

Independent replay checked140cases/30outerfolds and rejected four semantic mutations. It independently solves ridge/RBF systems and checks tree splits/calibration. Stored normalization is authenticated before use at exact tree boundaries to avoid verifier-only floating-point branch changes. Initial boundary/quantile diagnostic logs are retained. No new model calls or objective acquisitions in V149/V151; corrected analysis1.517seconds/600secondcap.

The coherent historical subset remains eight execution-engine families,70cases/model,140starts/139complete responses. The interrupted historical response remains a fallback/unknown usage. Memcached adds a ninth family to the broader research evidence, but its fivecases/model remain separate because utility/budget allocation differs.

## Native source, build and feasibility

Official Memcached1.6.45 and libevent2.1.13-stable archives/documentation: `reports/source_audit_v150.md`, `artifacts/sources/v150/receipt.json`. Original BSD3-clause/component notices retained and added to THIRD_PARTY. Archive hashes/owner URLs, safe extraction and all build logs saved. Builds/install prefix are project-local `.native-v150`; no system package/service/settings changes. Default SDK/linker configure failed; repaired using existing Xcode clang/MacOS15.5SDK through process-local environment. Failed3.046s +repaired20.045s under600sbuildcap. Upstream full regression suites were not run.

V150:20probes,4settings×5randomizedblocks,128000timedoperations/probe; allcorrect,20.783s/300s, **failed unchanged1%relativeMAD gate** (1.285%–3.248%). V152 explicit frozen amendment:16×longerworkload,2048000ops/probe,20probes,57.755s/300s, **passed same gate** (0.042%–0.410%). All40serversexited0. No threshold loosened; failed screening retained. This pass did not guarantee future noise: V153 variability is reported above. Both stages have charged ledgers/rawstdout/counters/plans/freeze hashes and independent replay (six mutations rejected).

V153 protocol SHA256 `251194b1127d913a5d8e2fc21a13877f1c52e922e637cef74e54b97be13c7c92` (`reports/protocol_v153.freeze.json`,23inputs). One prose sentence said normalized model observations, whereas actual frozen prompts use raw settings plus level lists; search distances are normalized. `artifacts/study_v153/protocol_clarification.json` records this **before model starts**, with no prompt/code/decision change. Preserve the discrepancy and original freeze.

## Costs and closed limits

V153 collection636.533473s/1800s. Ten starts/ten valid responses,zero retries/unknownusage;306generated/3677prefilltokens,10240allocatedoutputtokens. SmolLM5calls,141generated/1785prefill,7.906309slifecycle,1.812570sstartup,peakRSS2,951,839,744bytes. Qwen5calls,165generated/1892prefill,17.980968slifecycle,4.072084sstartup,peakRSS6,063,505,408bytes.300s/model,8GiBRSS,1024outputtokens/request caps respected. All model processes ended before native model-continuation timing. Classical search preceded model search; validation order was randomized. These phases do not establish causal model-size/runtime comparisons.

Actual research cost includes both models, controls,40feasibilityprobes,400pairedmeasurements and all prior development. Estimated deployment uses20evaluations and at most one selected request per case. No dollar/energy saving inferred. Cost receipt: `artifacts/study_v153/cost_receipt.json`.

Cumulative modelstarts **4755**; recorded-table acquisition charges remain **40220**, plus2historical incidental exposures. **440newnativeevaluations** are a separate incremental counter, not a claim that all historical recorded charges were native executions. Retained source/document bytes added2,436,165/5,000,000; cumulative **10,257,746,397/10GiB**, remaining **479,671,843bytes**. Existing modelpayload **9,126,358,023/9GiB** unchanged. No paid inference/cloud spend/newweights/packageinstallation/credentials/systemsettings/publication/push/contact. All closed allowances require a new prospectively specified version for further collection, not silent reuse.

## Evidence and safe reproduction

- Assessment: `reports/research_assessment_v153.md`; actual result `reports/native_study_v153.md`; corrected router `reports/router_v151.md`; feasibility `reports/native_feasibility_v152.md`.
- Native raw records: `results/v153_native/acquisitions/000.json` through399, serverlogs,search,selectionseal,validationplan/105validationrecords,ledger/completion/comparison.json,PNG/SVG.
- Real model prompts/provenance/starts/rawresponses/tokens/runtime/ledgers/serverlogs: `artifacts/study_v153` and `results/v153_models/{model}`.
- Router folds/coefficients/trees/calibration/completepolicies: `results/v151_router`; frozeninputs/replay in `artifacts/study_v151`.
- Feasibility raw logs/correctness/medians/gates: `results/v150_native`, `results/v152_native`; freezes/replays in corresponding artifacts.
- Focused primary-source novelty comparison: `reports/novelty_audit_v153.md`. BORA and LB-MCTS directly motivate stronger comparisons. Their complete algorithms have not run here; general conditional LLM invocation is not novel by itself. Do not invent inaccessible artifacts or call checkpoint adaptations exact replications.

**1165tests passed**,14dependencywarnings,30.90s (`artifacts/study_v153/all_tests.log`). Independent replays passed all140historicalcases,40feasibilityprobes and400pairedacquisitions/10responses, memberships/seals/budgets/choices/metrics/correctness. Threepaired-study semanticmutations rejected. Initial verifier-only nativeexit0assumptionfailed; repaired to check correct measurement plus permitted reaped−9cleanup. No frozen experimental input/data changed. Logs preserve both outcomes. Reports/JSON/PNG/SVG regenerated byte-identically; PNGs visually inspected; reproduction receipts in study_v151/152/153. Synthetic tests remain separate from research aggregates.

Executed collection: `scripts/native_feasibility_v150.py`, `scripts/native_feasibility_v152.py`, `scripts/run_native_v153.py`; do not rerun create-once collectors or edit frozen inputs. Safe checks:

```sh
.venv/bin/pytest -q tests
.venv/bin/python scripts/verify_router_v151.py
.venv/bin/python scripts/verify_native_v152.py
.venv/bin/python scripts/verify_native_study_v153.py
MPLCONFIGDIR=/tmp/mpl-v153 .venv/bin/python scripts/report_router_v151.py
MPLCONFIGDIR=/tmp/mpl-v153 .venv/bin/python scripts/report_native_v152.py
MPLCONFIGDIR=/tmp/mpl-v153 .venv/bin/python scripts/report_native_v153.py
.venv/bin/python scripts/seal_research_v153.py --verify-only
```

V148prior manifest SHA2566f944e3680f1e0442331b4dd9b968acc35ef5ac4e98006147135d72e16032bd4 verified before edits. Prior mutable root documents saved in `artifacts/study_v149/previous_snapshot`; current sealer resolves older root locations and preserves62historicalcheckpoints. Current evidence manifest/verification: `artifacts/study_v153/evidence_manifest.json` and `seal_verification.json`. Use latest sealer for historical roots. This is internal reproducibility, not independent-host replication.

## Single most important next action

**Implement source-mapped checkpoint adaptations of the closest uncertainty/reliability-based prior methods, then freeze a new independent-family comparison.** Existing outcomes are development evidence for any revised method. Do not tune on them and call the result confirmation. The prior-method comparison, several fresh independent families, independent-host replication and robust measurement/effect separation remain untested. A bounded negative empirical paper may be possible, but journal quartile is not a scientific stopping rule or acceptance guarantee. See `reports/next_experiment.md`. No external access request is currently needed.
