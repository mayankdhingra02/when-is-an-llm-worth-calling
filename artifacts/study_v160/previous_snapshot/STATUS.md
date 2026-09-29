# STATUS — V156–V159 complete: two native solvers, paired real local-model study

Resume here, then reports/research_assessment_v159.md, reports/solvers_v159.md, the frozen V159 protocol and reports/next_experiment.md. Collection, analysis and tests are complete. No model server, native worker or background experiment remains. No permission/memory/access blocker is pending. All V156–V159 finite allowances are closed. Scientific honesty overrides obtaining a positive result: this strengthens bounded negative evidence, not a successful general router or Q2-readiness claim.

## What actually ran

**V156 source admission:** cvc5 1.4.1 and Google OR-Tools CP-SAT 9.14.6206, official CPython3.10/macOSarm64 wheels with registry SHA256 and owner release verification. Twelve hash-locked packages installed offline in separate .venv-solvers156; old .venv unchanged. pip check passed. Source notices, metadata and 187 installed native-library hashes saved. Scoped exposure audit checked 852 prior files with no engine-name matches. A post-collection CVC4 predecessor alias check also found none; its timing is explicit. Both engines share the constraint-solving/N-queens domain, and Z3 was previously exposed. No claim of two independent industrial applications.

First sandbox fetch failed DNS, retaining zero bytes. Network-enabled fetch retained cvc5/two metadata files, then rejected an OR-Tools response after reading 20,000,001 bytes: its 20,203,764-byte wheel exceeded the original20MB/file cap. Explicit source amendment allowed40MB/file with unchanged150MB total stage/global allowance, reused existing verified files, and preserved failure receipts. Total new retained content48,933,967bytes; discarded content20,000,001 separately counted. No source distribution compilation or arbitrary installer.

**V157 first feasibility:** 40 real probes, four fixed settings × five repeats × two engines, N=32,10sinternal/15schild caps. All20cvc5 probes timed out. All20CP-SAT probes were correct/stable, but one cell median6.993ms failed the frozen10msminimum. Neither engine admitted; full failure denominator retained. Stage224.952s/600s.

**V158 prospective workload repair:** board sizes changed to cvc5 N=10 / CP-SAT N=48; configuration set, correctness, timing gate and caps unchanged. Another40real probes, allvalid. Every cell relativeMAD below1.2%, all medians>=10ms. Stage47.095s/600s. Both admitted for the separately frozen paired study. This is feasibility-exposed workload design, not wholly untouched-family confirmation. No LLM response or gain was observed before workload selection.

**V159 paired collection:** 800 actual native objective evaluations;20 real local-model starts/responses (ten each, both valid);70logicalB20arms across ten prefixes. Five fixed seeds per engine,64settings each. Same savedB10prefix per arm, then7newsearchsettings and3fresh incumbent validations. Controls: sequential3NN, adaptive neighbor, GP-EI(length1 fixed mixedkernel), randomfull and randomproposal. Models: existing pinned SmolLM3-3B/Qwen3-8B Q4_K_M. Prefix features, saved historical benefit/uncertainty decisions and source-mapped BORA/rank adaptations frozen before allcontinuations. No retraining or threshold selection on V157–159. Full original BORA/LB-MCTS algorithms remain unrun.

Actual evaluations:100sharedprefix+350classicalsearch+140modelsearch+210freshvalidation=800. All800exactsolutions independently validated; no timeout penalty, incorrect result, retry or fallback inV159. All70searchincumbents fixed before randomized validation blocks. All70validationcells relativeMAD<=5%. Both local model servers exited0. Collection401.366s/3600scap; driver401.473s. Maximum modelRSS3.042GBSmol/6.823GBQwen below8GiBcap.

## New result

Positive gain means shorter median fresh-validation runtime. Per-engine means overfive seeds:

| Engine / model | Gain vs sequential | vs adaptive | vs GP-EI | Robust joint wins |
|---|---:|---:|---:|---:|
| cvc5 / SmolLM3-3B | +0.402% | -0.388% | -0.263% | 0/5 |
| cvc5 / Qwen3-8B | +0.623% | -0.149% | -0.030% | 0/5 |
| CP-SAT / SmolLM3-3B | -22.024% | -21.713% | -21.200% | 0/5 |
| CP-SAT / Qwen3-8B | -21.203% | -20.900% | -20.377% | 0/5 |

Robust joint win required >10%gain against sequential/adaptive/GP, different configurationIDs, exact valid outputs and <=5%validationMAD. Zero model-cases met it. Twelve of20model/sequentialpairs selected the same configuration. Benefit and calibrated uncertainty policies chose0/10calls/model; BORA and rank draw each3/10 and lost meanquality. Rank expectation is a mathematical diagnostic, not fractional measured inference. Hindsightoracle remains nondeployable.

Post-outcome diagnostic: CP-SAT's sequential/adaptive/GP improved acquired searchincumbents in3/5cases; both modelarms kept prefixincumbents5/5. Smol/Qwen CP-SAT projections16/35and19/35, duplicates7/35and15/35among evaluated proposals. This is no proof of causal failure or known globaloptimum. It motivates a separately designed representationablation, not retrospective prompttuning. cvc5 had little observed searchheadroom. Sixteen validationmedians fell slightly below the feasibility10msfloor(min9.548ms); the paired practical-win rule did not include thatfloor and remains unchanged. No1%effectclaim from this10%marginexperiment.

## Evidence and checks

- Sources/runtime: reports/source_audit_v156.md; configs/solvers_v156.lock.txt; artifacts/sources/v156; artifacts/study_v156.
- Feasibility: reports/solvers_v157.md and solvers_v158.md; artifacts/study_v157/158; results/v157_solvers and v158_solvers, including all80rawprobes, assignments/timeouts, order and figures.
- Paired experiment: reports/protocol_v159.md; configs/study_v159.json; artifacts/study_v159 contains candidate tables, plan, saved prefixes/prompts, exact model pins, historical router and precontinuationdecisions/freezes.
- Raw measurements: results/v159_native/acquisitions/001.json through800.json; search states, fixed selections, validation blocks, comparison.json, representation_diagnostic.json and paired_gains.png/svg.
- Real inference: results/v159_models/{smollm3_3b,qwen3_8b}, including runtimes, full raw responses/starts/prompts/tokenization, capacity checks, ledgers and server-exit logs.
- 1,227tests passed,14existingdependencywarnings,31.14s; artifacts/study_v159/all_tests.log. Thirteen analysis tests repeated after report/verifier-only changes and passed.
- Independent replay checks800objectives,70branches,70GPchoices(maxEIgap0),210validations,20realrequestprovenances and aggregates; rejects objective/solution/identity mutations. Prefix-only policy recomputation also passed using existing tested helpers. Receipts: replay.json/replay.log. This is internal replay, not external replication.
- Thirteen report/data/PNG/SVG artifacts regenerate byte-identically; reproduction.json/log. Figures visually checked. No new measurements during replay.

One metadata-inspection serialization error (bytes-valued version) was fixed before solves. A precollection static review caught a collector module-name typo; original collector/freeze preserved, corrected before firstV159measurement. Documentation-only tool syntax/patch errors had no experimental effect. No frozen measured data or post-outcome policy was repaired. Original runtime metadata contains an unbounded default encoded as Infinity; a strict-JSON canonical derivative is retained separately and the original frozen observation is unchanged.

## Costs and limits

NewV156–159:80feasibility+800pairednativeattempts,20modelstarts,zeroexisting-tableacquisitions. Cumulative modelstarts4,775; recorded-table acquisitioncharges41,613 plus2historical incidentalexposures. Different counters: these are not41,613nativeexecutions or a coherent4,775casecohort. Modelusage observed11,089input/1,080outputtokens; unknownusage0requests. Smol/Qwen actualrequestseconds16.921/49.171, totalmodelstageseconds18.864/53.814. Nativepairedsubprocesscost323.868s, including178.683solveseconds. Feasibilityandallpreviouscollection are additional actualcost.

Modeled deployment uses B20onechosenbranch and a selectedrequest, not bothmeasuredbranches. comparison.json has a retrospective selected-branch costproxy excluding separately recorded coldstart. No measured deployment, dollar invoice or energyestimate. No paid/cloud inference,newmodelweights,newterms,credentials,systemsettings,publication,pushorcontact.

Retaineddownloads10,306,680,364/10GiB;430,737,876bytesremaining. Modelpayload9,126,358,023/9GiBunchanged. Newsourceallowance150MB closed at48,933,967retainedbytes. Costreceipt artifacts/study_v159/cost_receipt.json. Any further collection needs a new finite protocol; do not silently reopen caps.

## Preserve prior evidence

V149invalid Spark/Hadoop key collision remains excluded. V151corrected router grouping and V154/V155 rule/GPresults remain intact; historical140modelcases are separate from V159's17+3design. V153Memcached remains400nativeevaluations/10modelcalls with0jointpracticalwins. See prior snapshots/assessment155 for detail rather than reingesting the full literature report.

Predecessor V155evidencemanifest SHA256:382163478ffadba42762e1f69b6b7a9fa2ea15ab5ce0bc83afe98f1084e2ff01. Mutable root files were backed up before edits in artifacts/study_v156/previous_snapshot. The latest sealer resolves old root-document redirects and preserves64priorcheckpoints. Use latest evidence_manifest.json/seal_verification.json in study_v159, not historical root-file verification commands.

Safe replay commands (collectors are create-once):

    .venv/bin/pytest -q tests
    MPLCONFIGDIR=/tmp/mpl-v157 .venv/bin/python scripts/report_solvers_v159.py
    MPLCONFIGDIR=/tmp/mpl-v157 .venv/bin/python scripts/verify_solvers_v159.py
    .venv/bin/python scripts/diagnose_solvers_v159.py
    .venv/bin/python scripts/seal_research_v159.py --verify-only

## Single most important next action

**Freeze and run a cohort of independent application workloads with the current comparison set unchanged.** Two solverimplementations on a shared generatedbenchmark do not close that gap. Independent-host replication, productionworkloads, fuller modelcoverage and originalmethodreplication remain untested. The historicalrouter's20searchtarget vs native17+3target is also a transportlimitation. A bounded negative empirical paper is a reasonable discussion direction, but journalquartile/acceptance cannot be certified. No experiment continues outside this active session.
