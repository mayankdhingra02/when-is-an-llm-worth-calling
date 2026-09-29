# STATUS — V146–V148 complete: useful LLM exceptions, routers miss them

Resume here, then `reports/research_assessment_v148.md`, `reports/hadoop_v148.md`, `reports/router_v147.md`, the frozen protocols147/148, and `reports/next_experiment.md`. All collection is finished; both model servers exited0. No job continues outside this session, and no permission or memory blocker is pending. V148's30-request/1200-acquisition/1800-second allowance is closed. Scientific honesty overrides obtaining a positive result. This is not a successful generalizable router or Q2-readiness certification.

## Actual new result

V148 added one previously unacquired **Hadoop MapReduce family**, with PageRank, Terasort and Wordcount,69configurations/workload, seeds11,23,37,53,71. All15cases stay in one group. Each saved B10prefix feeds seven B20arms: sequential3NN, adaptive-neighbor, fixed-neighbor, random rows, random prototypes, SmolLM3-3B and Qwen3-8B. Both are existing pinned real local Q4_K_M models; no fabricated output, new weights or cloud execution.

**30 real requests,30 valid responses,0 retries/fallbacks/unknown usage;105 budget-complete arms;1200charged recorded outcomes.** Those include1125completed acquisitions and75acquisitions of explicit7200-second failure-penalty scores.200distinct source records acquired,9incomplete. Failure penalties are a declared utility, not measured failure runtimes or a claim that every failure was a timeout. No native Hadoop execution occurred.

SmolLM always-call mean relative gain versus sequential is **−3.6027%**, wins/ties/losses3/5/7. Versus adaptive it is+2.7283%. It beat both by >1% in **3/15cases**, Wordcount37/53/71. Qwen's sequential gain is **−5.2651%**,2/6/7, adaptive+1.3971%, with **2/15joint wins**, Wordcount23/53. Random-prototype control also beats both models on average. These are paired case results within one family, not independent-system significance or general model superiority.

Both frozen benefit-aware and calibrated uncertainty controllers chose **zero calls** and missed all3/2useful sequential opportunities. Development80th-percentile benefit also chose zero; uncertainty quantile made9calls/model, losing2.4321%/0.9717%. All15cases extrapolate in at least one feature. Oracle gains2.0132%/1.6341% are hindsight diagnostics only. Model headroom exists, but the current prefix predictor cannot select it.

## V147 development analysis, before Hadoop

Executed nested leave-one-family-out validation on seven previously exposed families,55cases/model, equal-family weighting; all fitting, scaling and thresholds use inner development folds. This is explicitly retrospective/exploratory, not fresh confirmation. Compared all7features, no-cardinality, trajectory-only, calibrated uncertainty, fixed development80th-percentile policies, never/always and matched-rate random. One historical interrupted response remains a fallback in the denominator.

Always-call family mean losses4.7688%/5.0596%; all three benefit variants selected zero calls. Removing cardinality alone did not repair routing. Benefit quantile made6SmolLM/7Qwen calls, both losing0.0577%; no credible superiority over matched random. Independent augmented-least-squares replay verified110cases/14outer folds and rejected four semantic mutations. Runtime4.320s/600-second cap; zero new model calls/outcome acquisitions. V148 routers were fit on these seven groups and frozen before Hadoop labels. No Hadoop tuning.

Current coherent paired-model subset: eight execution-engine families,70cases/model,140real starts/139complete responses. This is not140independent systems; Hadoop/Spark share an ecosystem. Only V148's new family is this continuation's prospective transfer test.

## Source audit and limitations

`reports/source_audit_v146.md` and hashed owner receipts under `artifacts/sources/v146` document the audit. PTSSBench XLS/XLSX are metric/range dictionaries, not configuration/outcome tables. Inspected Cassandra-Tuning exports contain elites/aggregates and final-configuration tests; a complete matrix was not found. Hyrise's index/encoding constraint leaves36validsettings/fixedscan, below unchanged40admission rule. Do not inflate pools by combining contexts or replace missing artifacts with invented data.

Scout owner oxhead/scout, MIT, pin e0dfc3a7d08ec4d441578565c0b7d4b24e56d5cb, supplied207small report records. Paper/owner-linked scripts verify completed/elapsed_time semantics. Hadoop2.7, nominal bigdata contexts, one owner run/configuration; actual input bytes vary slightly for two apps. Two features are cluster VM count and nominal VM type. Models see prefix labels plus feature-only domains, produce ten prototypes, and a frozen mixed numeric/categorical projection selects unique unseen rows. This is a cloud-deployment configuration adaptation, not exact SNAP2/Scout replication, economic cloud optimization or native correctness/noise evidence. Full source labels stay out of optimizer/router/model inputs. Invalid acquisitions are charged before failing; no outcome-based row filtering.

SmolLM projected103/150proposals nontrivially, with2repeated prototypes/5prefix matches; Qwen68/150,8/4. Projection still selects unique unseen settings. Output validity does not imply high-quality proposals. Runtime/model-order observations are descriptive, not causal size comparisons.

## Costs and limits

V148 collection wall82.961602s/1800s. SmolLM15requests,390generated/7405prefill tokens,21.754437s lifecycle,peakRSS3,181,674,496bytes. Qwen15requests,492generated/8844prefill,57.198501s lifecycle,peakRSS6,861,307,904bytes. Both exit0;700seconds/model,8GiBRSS,180seconds/request,1024outputtokens/request limits respected.30720allocated outputtokens;882actually generated,16249prefill. Collection includes both model branches, controls and startup. Modeled deployment is20evaluations/case plus at most one selected request; recorded-table lookup time is not native software runtime or a dollar/energy saving.

Cumulative starts **4745**, charged recorded acquisitions **40220**, plus2historical incidental exposures. Counters include historical missing labels/new penalties, not unique successful native executions. New source bytes1,187,506/5,000,000; cumulative retained10,255,310,232/10GiB, remaining482,108,008bytes. Existing model payload9,126,358,023/9GiB unchanged. xlrd2.0.1 was imported from a PyPI hash-checked pure-Python wheel for the audit, not installed. No new package installation, model download, paid inference, cloud spending, credentials, system changes, publication, push or author contact. Historical discarded download300001bytes remains recorded; none new.

## Evidence, verification and commands

1107tests passed before collection; final suite result is in `artifacts/study_v148/all_tests.log`. Independent V148 replay verifies all1200charges, source scores, prefixes, choices,105arms, frozen trained decisions,30raw requests/responses, budgets, timing and costs; four in-memory mutations (outcome, gain, request count, late selection) rejected. V147 and V148 reports/JSON/PNG/SVG regenerate byte-identically and figures were visually inspected. Synthetic fixtures remain separate from measured aggregates. Replay is not independent-host/native replication.

- Reports: `reports/hadoop_v148.md`, `reports/router_v147.md`, `reports/research_assessment_v148.md`.
- Raw source audit/receipts: `artifacts/study_v146`, `artifacts/sources/v146`.
- Nested fits/folds/policies/figure: `results/v147_router`; freeze/replay/tests: `artifacts/study_v147`.
- Raw requests, prompts, output, usage, server/ledger/runtime: `results/v148_models/{model}`.
- Acquisitions, classical/model arms, comparisons and figure: `results/v148_hadoop`.
- Feature-only candidates, prefixes, prompts, frozen routers/decisions, model identities, tests/replay/cost receipts: `artifacts/study_v148`.
- V147 freeze SHA8847f965407fcd777502d8969338c6a82765e09fb775d589fff18f56fa7cdffb.
- V148 protocol/input freeze SHA642dbbf587102642a5b62145f249973ed33fce4c86d87d50bcc1e31ccb801766;246files. Prefixes/decisions have a further precontinuation seal at `artifacts/study_v148/inputs.freeze.json`.

Executed create-once collection: `.venv/bin/python scripts/run_hadoop_v148.py` (prefixes, successful classical gate, both real models, evaluation). Do not rerun collection or edit frozen inputs. Future changes need a new version. Safe verification:

```sh
.venv/bin/pytest -q tests
.venv/bin/python scripts/verify_router_v147.py
.venv/bin/python scripts/verify_hadoop_v148.py
MPLCONFIGDIR=/tmp/mpl-v148 .venv/bin/python scripts/report_router_v147.py
MPLCONFIGDIR=/tmp/mpl-v148 .venv/bin/python scripts/report_hadoop_v148.py
.venv/bin/python scripts/seal_research_v148.py --verify-only
```

V145 prior manifest8e8b872024d7edb4619b87ec740f11080a03141fe28ab153624568c797537545 verified at turn start. Previous mutable documents are preserved in `artifacts/study_v146/previous_snapshot`; use the current sealer to resolve historical roots. New evidence manifest/verification in study_v148 preserves61historical checkpoints.

## Single most important next action

**Freeze a revised prefix-only benefit predictor using currently exposed families as development, then test once on genuinely fresh independent families.** Preserve all harms/ablation results; do not retune Hadoop then call it holdout. No permission blocker prevents future finite local work, but prior finite allowances are closed and must not be silently reopened. Additional independent families, useful selective routing, native noisy-runtime/correctness replication and focused novelty comparison remain untested. More seeds or unchanged no-call batches alone do not establish Q2 suitability.
