# Resume checkpoint: V160–V163 complete

Read this file, reports/research_assessment_v163.md, reports/protocol_v163.md and relevant code. Do not reread the full deep-research report. **New concrete result:** two real-input native application families, 800 paired configuration outcomes, 2,400 native workload invocations and20 genuine local-model calls; neither model achieved the predeclared robust joint10% improvement. All1,258 tests passed. This strengthens a bounded negative result; a useful general router and Q2 readiness remain unestablished.

All finite collection stages are closed; both model servers exited0 and a process check found none active. There is no active permission/memory blocker for replay and no experiment continuing outside this session. Independent-host collection would require a second host. No subagents, background automation, paid/cloud inference, new weights, publishing, contact or remote push were used.

## Sources and admissions

V160 downloaded22,137,051 retained bytes from official owners in4.112s under100MB/600s caps: ripgrep15.2.0 macOSarm64 owner release with matched ownerSHA256; hnswlib0.8.0 source headers; CPython3.10.13 source; UCIOptdigits. Sources and exact hashes: artifacts/sources/v160/receipt.json; audit: reports/source_audit_v160.md. Unmodified upstream algorithms, original project workload wrappers. Reused existing pinned Python environment, models and llama.cpp b11146. No new Python package installed.

A scoped852-file historical manifest plus V156–159 report/config additions contained no ripgrep or hnswlib/nmslib identity matches. GNU sort/coreutils was excluded after deeper alias matching found actual V66–67 history. Copied sort binary, license/receipt and unused prepared sort input remain; zero new sort objectives. This audit is scoped evidence, not universal absence proof.

ripgrep searches3,407 real source/docs files with five fixed distinct queries. Its exact count maps are verified independently. hnswlib indexes3,823 published training and queries1,797 test vectors, discards class labels, and measures construction+query under a95% tie-aware recall constraint. Original Optdigits is a classification dataset; this is an adapted ANN workload. Source-derived correctness references are not optimizer labels. Reading input may warm caches; no cache flushing or uncharged native warmups.

Initial C++ link failed on the default SDK27stub format. A120s-bounded build with the existing Xcode toolchain/macOS15.5SDK succeeded using process-local environment only. Original failure and repair logs remain. Initial reference preparation completed data but failed its receipt while the executable was missing; elapsed time unknown, not zero. V162 reference preparation has its own receipt.

V161:40 actual feasibility outcomes/40 native invocations. ripgrep failed5% MAD in two cells; lowest ANN cell returned valid IDs but89.416% recall in allfive repetitions, below95%. These five outcomes retain measured raw times and declared20s utility penalties. Neither application admitted.

V162 separately froze a five-query aggregate text workload and higher minimum ANN M/constructionef before observing model gains. Another40 outcomes/120 invocations, all quality-valid, all admission cells >=10ms andMAD<=5%. This is feasibility-exposed design; no untouched production-cohort claim. Both stages retain all80 outcomes and160 invocations.

## Paired V163 experiment

Five seeds11,23,37,53,71 per application;64settings each. Same saved B10prefix per arm, then seven new search configurations and three fresh incumbent validations. Five deterministic classical comparators: sequential3NN, adaptive neighbor, GP-EI with fixed length1, random full and random proposal. Existing SmolLM3-3B and Qwen3-8B Q4_K_M are genuine local inference, not generated substitutes. Historical benefit/uncertainty models and mapped BORA/rank checkpoint rules frozen unchanged before continuation; no new fit or threshold selection. Full original source methods remain unreplicated.

Accounting:100shared-prefix+350classical-search+140model-search+210fresh-validation=800 configuration outcomes;400text outcomes×5invocations+400ANN×1=2,400native invocations. One fixed five-distinct-query bundle is one text objective; individual query times are not measured as extra labels. All70 search incumbents fixed before three randomized validation blocks. Total70 logical B20arms across ten prefixes. No hidden objective supplied to optimizers/router/model.

All800 paired outcomes passed correctness/quality; minimum ANN recall98.169%, no paired quality penalties. Twenty model starts/responses, all parsed, no retries/fallbacks. Robust practical win requires >10%fresh-validation gain against sequential/adaptive/GP, different configurationIDs, all valid outputs, MAD<=5%, bothmedians>=10ms. Two of70validation cells exceededMAD; none fell below10ms. Failed stability cells remain in descriptive means.

| Application / model | Mean gain vs sequential | vs adaptive | vs GP-EI | Robust joint wins |
|---|---:|---:|---:|---:|
| ripgrep / SmolLM3-3B | -1.295% | -0.647% | -2.174% | 0/5 |
| ripgrep / Qwen3-8B | -0.368% | +0.258% | -1.218% | 0/5 |
| hnswlib / SmolLM3-3B | -0.401% | -0.347% | +0.750% | 0/5 |
| hnswlib / Qwen3-8B | -0.123% | -0.075% | +1.029% | 0/5 |

Positive gain means lower validation utility. Sixteen of20model/sequentialpairs selected the same configuration; their timing differences do not indicate a better setting. Frozen benefit/uncertainty chose0/10calls/model. Matched random also0, so no evidence of superior learnedselection. Small signed means do not support sub-percent effects, equivalence or population significance. Seeds/querytypes/vectors are not independent systems.

Post-outcome acquired-label diagnostic: both models retained prefixsettings in5/5ANNcases, as did sequential/GP/random; adaptive improved in1/5. ripgrep sequential/adaptive/Qwen improved in2/5, Smol0/5. ANN projection counts21/35Smol,24/35Qwen; duplicateproposals21/35and23/35. No new outcomes or policy changes. These observations suggest limited headroom and a representation limitation, not known global optimality or causal proof.

## Evidence and verification

- Source, preparation/build, exposure audit: artifacts/study_v160; reports/source_audit_v160.md.
- Failed and repaired feasibility: protocols_v161/v162 (filenames reports/protocol_v161.md and protocol_v162.md), artifacts/study_v161/162, results/v161_apps/v162_apps; reports/apps_feasibility_v163.md. Independent receipt/figure understudy_v163/feasibility*.
- Paired protocol/config: reports/protocol_v163.md; configs/study_v163.json. Main and input hash freezes, candidate tables, model pins, historical routers, prefixes, prompts, plans and decisions: artifacts/study_v163.
- Raw outcomes, branchstates, frozen selections, validationblocks, comparison.json and paired_gains.png/svg: results/v163_native. Raw inference, starts/prompts/responses/tokenization/capacity/usage/exit receipts: results/v163_models.
- 1,258tests passed,14dependencywarnings,44.05s; artifacts/study_v163/all_tests.log. Synthetic fixtures remain tests/synthetic and are excluded from scientific results.
- Independent replay reconstructs exact text counts and ANN distances; checks800outcomes/2,400invocations,70arms,70GPchoices(maxEIgap0),210validations,20realrequestprovenances, allprefixdecisions and aggregates. Objective/output/identity mutations rejected. Prefix-policy recomputation uses existing tested helpers. replay.json/log; internal verification, not external replication.
- Ten report/data/figure artifacts regenerate byte-identically, no new native/model requests: reproduction.json/log. Figures visually inspected. Post-outcome diagnostic: representation_diagnostic.json and diagnostic.log.
- Main report: reports/apps_v163.md; interpretation: research_assessment_v163.md; prioritized follow-up: next_experiment.md. Cost and cleanup receipts in study_v163.

## Costs and remaining limits

New80feasibility+800paired configuration outcomes are880outcomes and2,560nativeinvocations, distinct from recorded-table charges. New20modelstarts bring cumulative starts to4,795 (not one homogeneous cohort). Recorded-table acquisitioncharges41,613 plus2historical incidentalexposures unchanged. Observed10,071input/919outputtokens, unknownusage0requests. Model request seconds15.608Smol/42.583Qwen; modelstage17.536/47.129s, including separately observed startup1.764/4.326s. Peak serverRSS2.985/6.562GB, below8GiB. Model/output/request/timeout limits enforced.

Paired native subprocess258.324s, including195.997objective-seconds. End-to-end330.818s/1,800s cap; driver331.046s. Feasibility, downloads, build and references are additional collection costs; initial reference time remains unknown. Modeled deployment selects one B20arm and request per case; ten cases use200outcomes/600nativeinvocations. It is a retrospective branch-time proxy excluding separately logged cold start, not a measured deployment, dollar invoice or energy estimate.

Newretainedsourcebytes22,137,051, discardedcontent0. Cumulative retaineddownloads10,328,817,415/10GiB;408,600,825bytes remain. Modelpayload9,126,358,023/9GiB unchanged. No new allowance is silently opened. Any new collection requires a prospective finite protocol under standing authorization.

## Preserve history and resume safely

V149invalid Spark/Hadoop case collision remains excluded. V151corrected grouping, V154rules/V155GP, V153Memcached and V159solver evidence remain unchanged; historical70cases/model/sevenecosystems are separate from native17+3 designs. Priorrootdocuments were copied before editing to artifacts/study_v160/previous_snapshot.

Predecessor V159manifest SHA256:8a877c829b1b247266a1a5dc265ba42bdc268657d021df80ac5963ab0355cf86. Latest V163sealer verifies65priorcheckpoints with oldroot-file redirects. Use study_v163/evidence_manifest.json and seal_verification.json, not obsolete historicalrootchecks. Frozen measured data, collectors and policies were not repaired after outcomes. Routine report path-inspection error had no effect on experiments.

Safe replay (no collection):

    .venv/bin/pytest -q tests
    MPLCONFIGDIR=/tmp/mpl-v163 .venv/bin/python scripts/report_apps_v163.py
    MPLCONFIGDIR=/tmp/mpl-v163 .venv/bin/python scripts/report_apps_feasibility_v163.py
    .venv/bin/python scripts/verify_apps_v163.py
    .venv/bin/python scripts/diagnose_apps_v163.py
    .venv/bin/python scripts/reproduce_apps_v163.py
    .venv/bin/python scripts/seal_research_v163.py --verify-only

Collectors are create-once. Do not execute them into completed directories. Compiler/runtime/input dependencies remain project-local and source-hash documented; native outputs are host-specific. Standalone second-host collection has not been performed.

## Single most important next action

**Independent-host replication of the frozen application comparison.** This is the next validity gap after completing two real-input applications, raw-output replay and deterministic reporting. A larger prospective application cohort and development-only representation/checkpoint ablation follow. Model-family generalization, production-scale workloads, full original-method replication and external replication remain untested. The existing evidence supports discussing a bounded negative paper; it does not certify Q2 readiness. No external message was sent.
