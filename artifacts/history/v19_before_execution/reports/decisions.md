# Decisions and deviations

All scientific choices are in protocol v1, hashed before classical collection. Implementation is an adaptation, no exact SNAP2 artifact located. Three binary single-objective tasks selected for schema/size and explicit system identity, not observed optimizer results. SQLite duplicate feature row is first-occurrence deduplicated independently of labels. Known variants must stay in the same group.

Classical gate: 30/30 runs, 20 inclusive evaluations per arm, 12 tests passed before local inference. Additional router tests added without altering optimization, parser or prompt.

Local setup correction before first output: SciPy 1.15.3 imports failed on macOS 27 due to PROPACK Mach-O section layout. SciPy 1.13.1 imports passed; only local dependency pin changed. Failed startup traceback and original failed-stage manifest preserved. Failed startup elapsed time remains in the cumulative resource ledger. No request counter reset.

The frozen protocol remains unchanged after model outputs. Invalid Python fences/nesting are not salvaged by a new parser, and prompts are not tuned to held-out outcomes. Invalid batches use the frozen classical fallback. A model request cap can leave held-out runs blocked; such runs stay in the intended denominator, and no complete-case-only held-out router result is reported.

The hardware check found MPS unavailable in the restricted shell but available under authorized local execution. All inference reads local safetensors and has HF offline flags. No paid client exists; provider validates no-paid configuration before loading.

Setup downloads and environment setup are outside the 30-minute measured experiment runtime. Installed/downloaded payload accounting, including a reserve for metadata, is recorded; exact network bytes are not claimed. Source retrieval initially failed DNS in the restricted shell and succeeded with authorized network access. No remote push, contact or publication occurred.

Evidence preservation after collection began: source files were copied into artifacts/code_snapshots/{classical,paired} and verified against every code hash in each original run manifest, including the original dependency lock for each stage. Later changes only harden config bounds and recover partial acquisition event records from existing checkpoints if a cap interrupts a branch; they do not alter proposals, outcomes or the running collector. The analyzer recovers such checkpoint events for cost accounting and reports incomplete pairs separately. Added tests exercise malformed-response fallback and repeated-proposal projection under a synthetic provider in temporary test directories.

A local Git repository was initialized on main for review. It has no remote and nothing was published.

## User-authorized exploratory continuation v2

The user requested continuation after the bounded-follow-up proposal. A separate allowance of at most 100 local attempts was explicitly announced, preserving USD 0 external spending and the original cumulative 1,800-second runtime cap. configs/followup_v2.yaml and reports/protocol_v2.md record that decision; no v1 counters or outcomes were reset. The prior measured runtime was carried into the separate v2 ledger.

The follow-up fixes dead-worker handling: health is checked before request reservation, and a timeout/provider failure stops model collection. A token grammar constrains syntax and legal binary domains while leaving each configuration value to the real model's logits. Compact prompts and constrained decoding are a new treatment, so v2 is exploratory. Three real model calls on separate synthetic feasibility fixtures passed before any v2 software continuation. Synthetic fixture quality is excluded from research aggregates, but the real calls count toward collection cost.

The initially attempted protocol/config writer used the system Python without PyYAML and failed before creating the config. It was rerun with the pinned project virtual environment; no model requests occurred before protocol hashing and preflight tests. No dependencies or model weights were downloaded for v2.

## Corrected v3 within the same follow-up allowance

The schema audit exposed a missed assertion: raw-table dimensionality and deduplication had been described in documentation but were not checked against the effective parsed candidates. The loader dropped a real SQLite option ending in INDEX. Collection was interrupted on v2 attempt 33; its remaining token usage is unknown. Five Apache continuations completed; SQLite's partial first run had eight newly acquired labels. The stage consumed 58 labels in total. All remaining intended records were explicitly marked aborted/blocked. See schema_erratum.md.

v3 uses explicit schemas with pre-run shape/duplicate checks and a regression test. Corrected classical baselines were rerun and charged (600 accesses). To reduce formatting overhead within the remaining runtime, a newly frozen treatment asks for five fixed-length bit strings per model call. Every bit remains a real model-selected token; row separators are forced and character-to-coordinate parsing is exact. Two calls spend the ten-label continuation budget. This changed batch size/serialization is an adaptation and is not pooled with v2. Three separate synthetic real-inference gate calls preceded v3 software continuations. No request/runtime allowance was increased; v3 uses the same persistent follow-up ledger.

A source-edit replacement initially left a two-array phrase in the unexecuted v3 prompt. A direct preflight inspection caught and corrected it to five bit strings before any v3 model inference; a regression assertion verifies that instruction. Corrected classical source snapshots preserve their exact code hashes, and the paired stage records its later executed snapshot. No scientific parameter changed after v3 model outputs.

## V4 — larger-study admission and projection-only diagnostic

The user accepted the next action (“do it”). Implemented/froze the larger study design, audited pinned tables by features only, and added/executed a uniform-coordinate projection control on already exposed v3 prefixes. No new LLM allowance was inferred and no new-system optimizer outcome was inspected. The proposed 203-call/60-minute larger-stage allowance remains explicitly unapproved; existing caps are unchanged.

A 47-table audit yields four untouched named systems compatible with the frozen binary treatment. SS labels and HSMGP/rs/sol/wc remain quarantined without original-system lineage. Identical feature-value matrices across several SS/rs/wc aliases and SS-N/systems-x264 are overlap warnings; they cannot prove independent groups. Named-product identity and schema compatibility are not complete workload/objective provenance. The 20-system split gate fails closed with no assignments.

Freeze manifest protocol_v4.freeze.json bound 46 code/input files before any control acquisition. Uniform legal-coordinate RNG uses dataset hash and seed, isolated from model/search RNG; the same projection rule then acquires ten fresh labels per saved prefix. This is a measured non-LLM namespace, not a mocked provider or an LLM result. All 15 controls completed, adding 150 accesses and zero calls. No controller refit or prompt change followed the diagnostic. Mixed model/control gains and the one-seed-dominated x264 mean are reported without generalization claims.

The full larger-study collector is intentionally not represented as complete: admitted system breadth, final manifests, objective provenance and a concrete larger resource authorization remain prerequisites. Current deliverables include executable admission checks, the frozen design, verified diagnostic code/logs and reproducible analysis.

## V5 — expand original-source lineage without collecting new outcomes

The user requested continuation of the registry audit. Pinned DeepPerf, VEER and Performance Evolution owner artifacts, preserving old v4 files. Exact normalized feature-name/matrix comparisons resolved fourteen MOOT correspondences; family-level mappings additionally use original FLASH/MoConfig descriptions. Related BerkeleyDB implementations, libvpx codecs, MySQL/MariaDB and DUNE/HSMGP are conservatively grouped. Hardware cases are excluded. No source's SS letters are blindly copied onto another source's filenames.

The owner feature-model check caught an undocumented Fast Downward CSV option. Retained the failing log and excluded the case rather than weakening validation. VEER SS-C's paper/artifact schema mismatch stays unresolved. The broader candidate count is 22 after this exclusion, not 23 admitted systems. OpenVPN throughput orientation, MariaDB's documented crashing-release gap and Z3 workload conditioning are explicit admission checks.

Added an isolated finite-domain nominal optimizer core and synthetic tests as preparation; no real model adapter or full collector is claimed. Broader dimensions/row limits are not installed into frozen v4. No new objective payloads, model calls, outcome acquisitions, cap changes or controller fits occurred. The next work is semantic target/revision admission before final treatment/split/resource freeze.

## V6 continuation: execute within existing limits

- Replaced the open-ended larger-registry milestone with a concrete bounded six-family follow-up. Seven owner case READMEs explicitly support target semantics. Use the first six by SHA256(v6-bounded:family), first three development, next three held-out; retain five fixed seeds. Preserve unadmitted family reasons and all previous freezes.
- Use one real local request for all ten continuation proposals, instead of the previous two batches of five. Two real synthetic format gates + 30 pairs = 32 requests, fitting the existing 34 remaining. This is a versioned treatment change, not a numerical replication.
- Add a lazy target oracle and durable acquisition journal, finite-symbol grammar/model adapter, modal acquired-only features, explicit paired states, and development-sealed router before held-out acquisitions. A crashed started transaction fails closed pending audit; no silent repeated acquisition.
- All selected empirical tables are binary. Finite-domain capability beyond binary is tested synthetically only. Keep all other objectives hidden and report single-target quality tradeoff limitations.
- Current local inference selects CPU; prior v3 selected MPS. Model identity/revision stay fixed; record device and avoid asserting cross-device equivalence.

## V7: implement mechanism study before asking for a cap change

The model intervention excludes only exact original-prefix configurations during decoding. The prompt/model/device/batch/projection stay fixed; repeated novel rows remain possible. This avoids conflating prefix exclusion with an additional within-batch diversity intervention. It is more than syntax, so zero copying is an enforced validity property rather than evidence of intelligence.

Added exact uniform-complement sampling to separate model benefit from exclusion alone. All 15 controls were executed and verified with 150 acquisitions under existing limits. Fifty-four tests and 15 real-tokenizer checks pass. No LLM call was fabricated or dispatched: the full-arm preflight refuses 15 required calls against two remaining. Requested explicit cap 100 → 113 only after implementation, freeze, controls and verification; authorization remains false pending the user's answer. No runtime or spending increase is proposed.

## V7 approval and completed mechanism result

The user explicitly replied `approve` to cap 100 → 113. Applied only that bounded request allowance; retained the 1800-second cumulative runtime and USD 0 rule. All 15 real CPU model continuations completed with no retries/fallbacks and used the entire approved request allowance. Frozen treatment/input files were unchanged.

On the same development cases, exclusion removed original-prefix copies (137/150 → 0/150) but yielded zero material improvements and one material harm against each original-LLM/classical/matched-control comparison. Only 7/150 raw proposals matched recorded candidates. Do not call missing recorded configurations invalid real software configurations. No router was refit or held-out treatment selected. Next priority is an explicitly controlled candidate-selection formulation, not claiming that removing copying solved useful exploration.

## 2026-09-24 — V8 candidate selection, controls completed

Following the user's request to continue to a good-enough result, define adequacy as credible paired evidence regardless of sign. Freeze one development-only formulation that selects existing rows rather than generates/project features. Same fifteen v6 development prefixes; acquired-only top20 shortlist, shuffled IDs, ten distinct selections; two matched model-free controls. No adaptation to v6 test outcomes. Both controls actually completed300 new accesses;64 tests and independent replay passed. Full inference preflight blocks at113/113 requests. Proposed allowance is113→128, not implicitly granted by generic continuation; runtime1800seconds and USD0 unchanged. Source/code freeze120files; old scientific freezes unchanged. Conclude this formulation before reviewing any wider/model-changing study, rather than seek a positive result by repeated tuning.

## 2026-09-24 — V8 explicit approval, real collection and stopping decision

User replied exactly `Approved` to cap113→128; recorded before inference with unchanged1800-second cumulative runtime and USD0 spending. All15 real local CPU/float32 model cases completed, adding150 targets (450 V8 total), no errors/retries/fallbacks. All64 tests passed; independent replay verified45 states and150 token-choice positions. Mean gain vs adaptive classical .005349, two material benefits and zero material harms; vs static shortlist .001106, one material benefit.

Raw responses then revealed every case selected IDs0–9 in display order. Post-hoc diagnostic verifies those first-half row sequences equal all actual LLM selections; it adds no acquired labels or model calls and is not a newly measured control. Random ID assignment makes this observed rule distributed as random shortlist selection. Therefore improved realized scores do not establish learned ranking. Document this prominently rather than present a positive LLM result. Preserve protocol/source/results unchanged; no treatment retuning. Stop this bounded pilot and recommend a predeclared order-permutation study before scaling router data collection. Final shared request count128/128, historical228, labels4208. Preapproval documentation retained under artifacts/history/v8_before_approval/.

## 2026-09-24 — Exact reference and final original-scope audit

The user requested a concrete result beyond another continuation plan. Add a separately versioned post-hoc evaluator (V9), not another model treatment: exact uniform ten-of-twenty minimum-loss distributions from frozen V8 development pools, independently checked by enumerating184756 subsets per case. Uniform expected group mean loss .012250 vs adaptive classical .015580; observed model .010232. Random subsets match/beat the observed model loss with probability at least .5 in every individual case. These are conditional finite-pool references, never p-values or additional experiments. No model calls/acquisitions; no protocol or outcome tuning.

All77 tests pass. New whole-pilot audit checks primary-source/model hashes, corrected initial smoke, all paired evidence, prefix-only features, development-only refit and seven held-out policies. Historical verifier ledger counts use preserved stage snapshots, with no live-ledger mutation. Exact snapshot/result input freezes preserved. Original seven-stage bounded pilot is complete; usefulness/generalization of a benefit controller remains unestablished. New concrete_result.md distinguishes apparently favorable scores from the all-first-half observed response rule. A further voice approval during analysis does not define an unspecified cap increase. Stop adaptive search after this concrete audited deliverable; no guarantee of eventual positive research outcome.

## 2026-09-24 — V10 headroom decision

User approved the proposed no-call headroom check. Per-case shortlist/full-table hindsight bounds were computed for all15 development cases against fixed static ranking, adaptive classical, observed LLM and exact uniform expectation. No new inference/acquisitions or changed historical criterion. Perfect same-shortlist selection clears the frozen .02 margin in only1/15 cases vs static ranking (MySQL only),2/15 vs adaptive classical,0/15 vs observed LLM. The full-table bound vs static gives3/15, still one family.84 tests and120-reference replay passed.

Do not recommend the same-design stronger-model rerun. A distinct issue is metric validity: Brotli's .02 normalized margin equals7.85396seconds, exceeding the entire selected static-runtime range1.526–1.900seconds. Raw full-table reductions4.3–23.2% can therefore be hidden by that threshold, but quality/size equivalence is unvalidated. Do not retroactively change success criteria. Next action is objective/quality validation and a new candidate/task protocol before more inference, superseding the earlier priority of immediate model/order testing.

## 2026-09-24 — Quality constraint and actual cheap control, without positive-result selection

User requested continuation until positive. Reaffirm scientific honesty: retain all cases and old negative results, no positive-only stopping rule. V11 source-checked runtime/output-size feasibility on both eligible development compression families/all5 seeds, with a cap from the fastest prefix row. It found two above10% shortlist oracle opportunities; these are hidden-label hindsight, not model outputs or achieved algorithm gains. Brotli seed23 improves runtime16.5% and file size; lrzip seed37 improves runtime19.5% while meeting its anchor cap but increasing size49 source units over the static incumbent.

Finished independent unblocked work by freezing/running V12 actual cheap joint-outcome controls. Each10-row prefix reacquired/charged as joint pairs; matched nearest-neighbor and random continuations each get10 more, total300 new vector accesses and20 complete branches.95 tests and deterministic source-value replay passed. Mean relative cheap gain over random: lrzip+4.82%, Brotli-2.79%, overall+1.01%; negative and zero cases retained. Ideal remaining headroom on lrzip is only0.37% on average; broader LLM study still lacks validated independent-system opportunity. No new model calls, cap increase, downloads or spending. Never relabel these feasible/classical effects as positive LLM evidence.


## 2026-09-24 — Close the bounded pilot and consolidate for review

The user delegated judgment (“Do what you think is right”). Do not chase an eventual positive LLM result. Consolidate the full evidence in decision_brief.md, replace confusing accumulated README/status summaries, and distinguish the original V9 audit from later V10–V12 replay. Preserve mutable document snapshots and all scientific freezes. No new experimental version, model calls, acquisitions or allowance changes. A lightweight review verifier checks frozen hashes and reported arithmetic without rerunning inference or rewriting measured outcomes.

The next substantive action is application/task review: justify runtime/size/correctness utility and practical margins, then establish independent-system headroom beyond cheap controls on development data before a new bounded model/order study. The 1.01% mixed classical mean is not used to recast the original LLM hypothesis as supported. No external communication or publication is authorized or performed.


## 2026-09-24 — V13.1 prospective metadata audit

On “Continue”, execute unblocked metadata admission rather than request an unspecified model-cap increase. Freeze a runtime/size/correctness task contract (application utility unresolved), all 81 registry rows, source README evidence, an exposure/split guard and synthetic tests. Four size-bearing tables map to three previously used families; zero untouched size families are available. No numerical objective CSV was opened. Do not infer video-output quality from lossless input or call VP9 independent of VP8.

Review caught the initial V13 omission of x264's legacy `heldout_smoke` label. Preserve that first pass and add frozen V13.1 correction/regression; all nine exposed families retained, unknown split spellings fail closed. 102 tests pass. A bounded owner-doc lookup identifies lzbench/Zstandard as possible measurement leads only. No new model/data download, collection, outcome inspection, cap change or external contact. Next data requirement: genuinely new family evidence meeting the task contract before another routing study.


## 2026-09-24 — V14 pinned external artifact audit

On “Continue”, retrieve and inspect primary-owner data leads under persistent download caps; no upstream execution. Pin compression-codec-benchmark, PDS-Throughput and lzbench. Implement/freeze/run a metadata projection and coverage audit:540 CSV rows,450 measured,90 contexts,15 inputs,6 codecs,1 measured configuration/context and5 repetitions. No context supports20 settings. Execution manifest unknown Git commit remains unresolved despite pinned download. Correctness checks are code/source evidence, not our physical rerun; timed compression outputs are discarded while canonical decompression is checked.

Inspect raw-looking lzbench edge files rather than assume none exist: Zstandard regression CSV has sizes without runtime; Density log lacks the required task/repetition/provenance table. PDS inventory has scripts/PDFs, not an admitted raw table. All three remain unadmitted.108 tests pass,0 new model calls/acquisitions, experiment ledger unchanged; download bytes charged. Preserve raw objectives without parsing/scoring them. Next route is a concretely scoped new measurement campaign; no permission/cap increase or positive-result guarantee inferred.


## 2026-09-24 — V15 actual live dataset and V16 paired controls

On continued authorization, use installed compressors and a pinned CPython source archive to build a genuinely measured small dataset within existing limits. Freeze32 settings each of zstd/lz4/zlib, three randomized rounds, explicit process-group deadlines and per-physical-trial charges. All288 trials complete, exact byte equality verified on every actual output, no failures. Save payloads and record different CLI/API timing scopes.113 tests pass at V15. A schedule-ID bug was found/fixed by tests before freezing or collecting; font-cache warnings during analysis were retained and runtime charged.

Finish the next independent unblocked check in the same turn: freeze and run15 paired classical cases/30 arms over the saved medians with20-evaluation budgets and shared10-prefixes. Fixed reference size caps, acquired-only nominal3NN versus random,450 charged recorded lookups. Independent replay passes;116 tests pass. Gains effectively zero and hindsight headroom0.2753% zstd/0% lz4/0% zlib. Do not invoke a model on this near-saturated32-setting test merely because the collector worked. All newly measured families remain development/exposed; no fresh held-out result claimed.

Historical costs stay distinct:4958 table accesses plus288 physical trials;128/128 follow-up model calls unchanged. No new model/packages/cloud/credentials/system settings/publication. The feasible infrastructure result is positive; the LLM/router hypothesis remains unsupported. Further task design requires prospective justification and useful opportunity beyond cheap search, not repeated positive-result selection.

## V17 — single expanded grid, stop rule reached

User continuation authorized ordinary bounded local work, not cap increases. Froze96/96/90 settings,846 fresh trials and unchanged15-case classical comparison before collection. All trials/arms completed; no calls/downloads. Recorded headroom still small (means0.537%/0.197%/0%). Stop after this grid regardless of sign.120 tests passed;15 freezes intact. No positive LLM or superiority claim. Updated review note/STATUS; older docs archived under artifacts/history/v17_before_expansion/. Remaining runtime56.1931s; requests128/128.

## V18 — explain initial/checkpoint opportunity without new outcomes

Continued with one fixed post-hoc decomposition of all30 V16/V17 development cases, no extra grid/model campaign. Initial-reference ceiling on expanded recorded tasks2.929%/0.987%/0%;10% diagnostic impossible there even before optimization. Full-table evaluator only, not deployable features.127 tests passed; analysis and exact source replay executed. Tightened V8 review wording: first-ten equivalence is observed, causal order effect untested. Charged0.3939s;55.7992s remain,128/128 requests unchanged.

## V19 — prepare finite real-model mechanism test; cap blocker explicit

Rather than infer ID/display causality from V8's first-ten equivalence, prepared nine fresh requests on first seed11/allthree V8 development families. Fresh original baseline plus independent display/ID interventions; same pinned local model, no quality scoring or new objective acquisitions. Tested transforms/permission/deadline guards;134 tests passed, real tokenizer checks passed. Scientific25-file freeze saved; authorization remains denied. Actual runner correctly blocked before model loading. Preparation cost2.7051s;53.0941s remain,128/128 requests unchanged. Need explicit nine-call approval128→137; runtime/spending unchanged. No real V19 responses exist yet.
