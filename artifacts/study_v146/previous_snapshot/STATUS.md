# STATUS — V143–V145 complete: one new Spark family, real routing headroom

Resume here, then `reports/research_assessment_v145.md`, `reports/spark_v145.md`, `reports/protocol_v144.md`, `reports/protocol_v145.md` and `reports/next_experiment.md`. All collection finished; all three model-server lifecycles exited0. No collector/server continues outside this session. No permission or memory blocker is pending. The50-request/2000-acquisition/1800-second allowance is **closed**. This is a concrete mixed result, not a successful learned router or Q2-readiness certification.

## New measured finding

Added **one previously unacquired Spark system family**: five fixed workloads (Bayes/bigdata, PageRank/huge, Terasort/ds1, TPC-H/20, Wordcount/bigdata), seeds11,23,37,53,71.499distinct recorded configurations across fixed workload pools. Each of25cases saves a B10prefix, then runs seven B20continuations: sequential3NN, adaptive-neighbor, fixed-neighbor, random rows, random prototypes, SmolLM3-3B and Qwen3-8B. All workloads/seeds stay in one family.

**50 genuine local generation requests;49 valid complete responses,1interrupted request with unknown usage and explicit classical fallback. 175 budget-complete B20arms;2000charged recorded acquisitions (1999finite,1missing).** No new native Spark/cloud execution. The original authors collected the Spark tables; these are local recorded-table acquisitions. Model identities and payloads are real, not Codex-generated replacements.

SmolLM mean relative gain: **−0.1099% vs sequential, −0.4168% vs adaptive**. It achieved >1%gain over **both** in4/25cases: Wordcount11, PageRank71, Terasort53, TPC-H11. Qwen: **−1.9009%, −2.2181%**, with1/25joint practical win (Terasort53). All main sequential/adaptive comparisons have complete labels. SmolLM sequential wins/ties/losses10/8/7, with7practical wins and7practical harms; Qwen2/11/12, with2practical wins and11practical harms. Joint comparison is not a free deployable hindsight-best classical portfolio. No equivalence or independent-system significance claim.

Frozen V132benefit and uncertainty controllers both selected **zero** calls; exact-rate random also zero. They missed7SmolLM and2Qwen >1%sequential wins. All25cases extrapolate on mean domain cardinality (55.57–58.63vs development1.71–4.67). No refit or threshold search on Spark. Hindsight oracle mean gains1.1843%/0.4213% are diagnostic, not policy results. SmolLM improved13prefixes, Qwen7. Nonzero projection240/240 and250/250; repeated prototypes23/240 and192/250. Projections still acquired unique unseen rows; duplicate prototypes are not hidden as parse failures.

## Failure and amendment, retained honestly

V144strict validation stopped at empty duration in TPC-H physical source line76, acquired by seed71random-row arm. At stop:1036charges (1035finite+1missing),78classical arms complete and6acquisitions in next arm. An orchestration error launched the model collector despite classical failure. It made6SmolLM requests,5completed; SIGINT stopped the6th and finally closed server exit0. Original logs/results remain immutable in `results/v144_spark` and `results/v144_models`. No Qwen started then.

V145froze recovery before any model continuation acquisition: import original history with hashes; consume only964remaining acquisitions and44unused requests (19SmolLM+25Qwen); never retry interrupted `bayes_11`. Missing values stay null, count against budget, and never train the optimizer. Any affected comparison is inconclusive for true best duration; all intended rows/arms retained. Only the random-row comparison in one TPC-H case is affected for each model; main comparisons are complete. This is explicitly an exploratory missing-data amendment after partial classical collection, not pristine confirmation. The repaired collector requires classical completion. Source absence is not asserted to be a software execution failure.

## Sources, representation and costs

Original author/lab links and exact pins in `reports/source_audit_v143.md`, `artifacts/sources/v143`, and candidate manifests. Tuneful data commit90ebfe3194a50cca00cf8524da26de21e93e6111; code e863108b566fd57df0ba5c59e557efe575b40554. Paper KDD2020, DOI10.1145/3394486.3403299, Spark2.2.1/HDFS2.7, fourAWS h1.4xlarge nodes. Dataset license not explicitly located; private local analysis, no redistribution grant. Post-execution telemetry files were excluded.30settings only; fixed context/App_id excluded from inputs; unused unnamed trailing cells counted/ignored. Numeric min/max use feature table only; a fixed ten-level prototype grid is an explicit adaptation, with matched random-prototype control. No exact SNAP2/Tuneful replication claimed.

Collection clock **987.294s /1800s**, including recovery work. SmolLM25starts/24responses, at least3290generated/46736prefill tokens; one unknown-usage request. Combined lifecycles164.020s (original36.454+repair127.566), peakRSS4,223,598,592bytes. Qwen25/25,7825generated/63495prefill,590.765s lifecycle,peakRSS7,456,636,928bytes.51200allocated outputtokens total; zero generation retries. Limits25starts/model,800s/model total,8GiBRSS,180s/request respected. Research cost includes all arms/models/failure/startups. Estimated deployment: one policy,10new evaluations and at most1model request after B10, plus loading amortization; no dollar/energy/native-time saving inferred.

Cumulative model request starts **4715**. Recorded acquisition budget charges **39020**, plus2historical incidental exposures; new batch includes1missing target rather than2000finite labels. Previous counters are preserved rather than recast as successful outcomes. Native counters unchanged. Source audit retained3,745,927new bytes; one discarded oversized API body read300001additional bytes, explicit and not retained. Cumulative retained downloads **10,254,122,726 /10GiB**, remaining483,295,514bytes. Existing model payload9,126,358,023/9GiB unchanged. No new packages/weights, paid/cloud inference, credentials, system changes, publication, push or contact.

## Verification and evidence

**1091tests passed**,14dependency warnings,30.77s. Precollection suite1088passed; two amendment tests passed before freeze; missing-budget test and full suite afterward. Synthetic fixtures remain separate. Independent standard-library full replay validates all50request starts/49responses, shared prefixes, source-row outcomes, exact budgets, geometry/projection, frozen controller decisions, source imports, timestamps, aggregate gains and cost counters. Four in-memory semantic mutations (reported gain, request undercount, changed target, late selection) rejected without changing actual files. Report/JSON/PNG/SVG regenerate byte-identically and figure visually reviewed. Saved-evidence replay is not independent-host inference/native replication.

- Report/assessment: `reports/spark_v145.md`, `reports/research_assessment_v145.md`.
- Figure/case data: `results/v145_spark/comparison.{png,svg,json}`.
- Complete acquisition ledger and classical/model/fallback arms: `results/v145_spark/`; original stopped records: `results/v144_spark/`.
- Original plus repaired model payloads/raw responses/usage/server logs: `results/v144_models/`, `results/v145_models/`.
- Feature-only candidates, prefixes, messages, decisions: `artifacts/study_v144/`.
- Tests/replay/mutations/reproduction/support/source-cost receipts: `artifacts/study_v145/`.
- V144freezeSHA065230e4be8698a8a992274e0102ba2fcbf80229d159eabac1993b24eaff07ea (1114inputs).
- V145amendment freezeSHA3527f7f81d50b66988327ad81692c36a5607227f7035bf624a929f47dd898ae7.

```sh
.venv/bin/python scripts/verify_spark_v145.py
MPLCONFIGDIR=/tmp/mpl-v145 .venv/bin/python scripts/report_spark_v145.py
.venv/bin/python scripts/seal_research_v145.py --verify-only
```

Do not rerun create-once collection. Executed stages: spark_v144 prepare/prefixes/classical(failed), collect_models_v144(interrupted); spark_v145 initialize/classical/evaluate, collect_models_v145(completed). Protocols, implementation, original failure and input seals are frozen; future edits need a new version.

Previous V141seal1fac36317236fdc15fba963298f939a51bfd5815693790d6c1f4602cb3dfac4d verified at turn start. Previous mutable-root documents are under `artifacts/study_v143/previous_snapshot`. New final evidence manifest/verification under study_v145 preserves the historical chain through those snapshots. Use current sealer for mutable-root history.

## Single most important next action

**Freeze and execute a confirmation on additional independent numeric-configuration families**, with documented target/failure semantics and development-only controller selection. Current Spark outcomes are now exposed; do not retune and call them fresh holdout. Further independent groups, native/second-host noisy-runtime correctness and successful selective routing remain untested. This result supplies real opportunities and failures to explain; it does not justify promising Q2 acceptance.
