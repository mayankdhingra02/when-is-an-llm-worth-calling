# STATUS — V52/V53/V54 completed: new application measured, headroom gate failed

Updated 2026-09-25. User approved new benchmark research. This continuation
completed an eight-family source/utility audit, set up a project-local Java runtime,
ran real correctness-checked application trials, and executed frozen classical
comparisons. No experiment remains running. Broad research/journal-readiness goal
remains incomplete; do not claim a positive LLM or learned-router result.

Resume with `reports/java_screen_v54.md`, `reports/admission_v52.md`, and the
frozen V54 protocol. Do not reread the deep-research report or repeat old runs.

## Actual new result

V52 audited eight unused non-compression families before new timing access.
None of those historical tables passed all stronger provenance/utility gates.
DConvert: 1,910 distinct configurations form 960 fixed-output contracts with at
most TWO thread settings (950 pairs, 10 singletons), insufficient for budget20.
Original JavaGC model names match35/35, but the detailed later Java8/xalan/GC-time
setup must not certify the older Java7 data. DeepArch needs linked accuracy data.
Reserved prospectively: MongoDB, Redis, Storm; their untouched history is not yet
certified. No new target read in admission. See data/family_reservations_v52.json.

V53 downloaded official Temurin17 ARM JRE and DaCapo9.12-MR1 under existing caps,
installed only inside the project. Three real JVM trials passed owner validation
and final output equality to a retained23,901,000-byte reference. Three warmups
plus three timed iterations;10.391s. Clear adaptation, not old JavaGC replication.

V54 froze48 GC configurations, three fresh JVM repetitions each, Xalan default
workload, one application worker and fixed512MiB heap. ALL144 JVM trials passed;
144 warmups +144 timed iterations, no failures/unattempted cases. All final outputs
match the retained reference hash; raw logs and validation receipts retained.
Physical collection466.031s. Optimizer objective is median of three whole-iteration
runtimes. Offline run: five fixed seeds, same saved10-evaluation prefix per seed,
random/3NN/RF-LCB continuations,20 acquired aggregate outcomes per arm,15 arms,
200 recorded-vector accesses;1.429s. Independent replay checks all180 choices.

Concrete result: every10-label prefix already within0.509–1.096% of best recorded
median1173ms. Best-of-three classical arms leave0–0.1702% remaining headroom;
that portfolio is hindsight, not deployable. Median within-setting CV4.7378%.
Frozen threshold max(5%,2*CV)=9.4757%, met in0/5seeds. Gate FAILED. Do not spend
LLM calls on this grid or widen it just to rescue the hypothesis. Retain as a
validated negative-control benchmark. V49 prompt/decoder stopping decision stands.

## Evidence and verification

- V52: results/v52_admission/summary.json; primary source manifest and execution
  receipts in artifacts/sources/v52/ and artifacts/study_v52/.
- V53: reports/java_feasibility_v53.md; results/v53_java_feasibility/; official
  runtime/source payloads in artifacts/sources/v53/; reference output in
  artifacts/sources/live_v53/trial_0/xalan.out.0. .local-runtime/java-v53/ is local.
- V54: reports/java_screen_v54.md; results/v54_java_physical/ (144 raw logs,
  starts/results, validation reports); results/v54_java_screen/ (table/repeats,
  five prefixes,15 arms,200 charges, summaries, CSV, PNG/SVG figures).
- Protocol: reports/protocol_v54_java_screen.md and .freeze.json. Data lineage:
  data/live_manifest_v54.json. Source/config inputs frozen before execution.
- artifacts/study_v54/ contains
  logs, independent verification, tests, resource receipt and final evidence seal.
- ALL365 tests passed. Independent verifier checked144 physical event/log/output
  receipts,288 iterations,200 charges,15 arms,180 decisions, gate and both freezes.
  No frozen collector/primary-analysis correction after outcomes. Renderer alone
  was adjusted to show timing-noise context and prevent title/label cropping;
  figures visually verified. No portable fresh-environment bundle built for V54.

## Costs, failures, limits

New source downloads: V52 5,971,579bytes; V53 242,205,247bytes. Persistent total
4,767,344,738bytes;601,364,382bytes remain under5GiB. No new model download/call,
paid API/cloud spend, system install, publication, remote push or author contact.
Initial source DNS sandbox failure recovered with approved network access;
CM-CASL master422 resolved via main; Adoptium API403 via owner GitHub release;
README404 via released-jar README. Raw source manifests retain successful payloads.

This continuation:200 new recorded aggregate-vector acquisitions;147 fresh Java
JVM trials/294 benchmark iterations including warmups across V53/V54. No new
compression experiment. Cumulative recorded accesses15958; physical compression
trials remain2234; Java physical trials147 listed separately; model requests
including original100 remain1976. Source setup, repeated physical collection,
all counterfactuals and discarded scratch overhead are real research cost.
Estimated one-arm deployment under this measurement recipe:20 aggregate outcomes,
60 JVM invocations/120 benchmark iterations, not the full research grid. Electricity
and user/agent time unknown. Scratch outputs removed only after verification;
canonical output and per-trial hash/size receipts remain. No job is running.

## Commands and next action

```sh
# Completed one-shot collectors; do not overwrite/relaunch into existing outputs:
.venv/bin/python scripts/audit_admission_v52.py
.venv/bin/python scripts/run_java_feasibility_v53.py
.venv/bin/python scripts/collect_java_v54.py
.venv/bin/python scripts/screen_java_v54.py
# Safe reproduction from saved evidence:
.venv/bin/python scripts/verify_admission_v52.py
.venv/bin/python scripts/verify_java_v54.py
.venv/bin/python scripts/report_java_v54.py
.venv/bin/python -m pytest -q tests
```

Single most important next action: resolve a fixed FastDownward planning task's
configuration mapping, plan validity/cost and failed-run accounting, then freeze
and run its classical screen. Its eligibility/headroom remain untested. Keep
MongoDB/Redis/Storm reservations; do not treat JVM variants or seeds as independent
families. No new LLM study or router evaluation is justified by V54, and one narrow
noisy development workload does not establish Q2 readiness or general LLM failure.

---

# STATUS — V50/V51 utility and physical-interface studies completed

Updated 2026-09-25. User requested sustained continuation. Completed TWO additional
studies beyond V49: verified utility contracts, restricted classical experiments,
and fresh paired native-API/CLI physical measurements. Resume here and
`reports/utility_v50.md`, `reports/interface_v51.md`, and their frozen protocols.
No experiment remains running. Broad research/journal-readiness goal incomplete.

## Concrete evidence and scientific decision

V50 actually decoded all 846 saved V17 files; every output matched the original
bytes. Frame audit found 144 Zstandard outputs without a content checksum and
72 LZ4 dependent frames; requested LZ4 dependence sometimes normalized to independent
frames. Exact losslessness and additional stream functionality are distinct.
Feature-only eligibility fixed checksum ON/independent blocks, leaving 48 Zstandard,
48 LZ4 and 90 zlib configurations. Ran all 15 prefixes/30 arms: 450 new recorded
vectors,20 inclusive evaluations per arm, shared ten-label prefix. Remaining
headroom: mean 0.6702% Zstandard,0% LZ4/zlib. No case meets the frozen5% screen.
The old studies remain valid within their older, narrower stated contracts.

V51 actually ran 960 fresh compression trials: same48 settings/family, Zstandard
and LZ4 through API/CLI, five paired rounds. All960 exact roundtrips and frame
checks pass, zero failed/unattempted trials. Median paired CLI/API time ratios:
1.8356× Zstandard,1.9053× LZ4. LZ4 outputs match240/240 pairs; Zstandard40/240.
Do NOT attribute Zstandard's entire timing difference to startup: most outputs
and sizes differ. Native allocation/copy timed, library loading excluded; CLI
launch/pipes timed. Same pinned installed codec libraries/versions/workload.

Separate frozen replay used sealed mode-specific median tables,20cases/40arms,
600 recorded vectors. Native API cheap search reaches the recorded feasible
minimum in ALL10cases, with zero full-table headroom. CLI Zstandard headroom0;
CLI LZ4 mean0.7652%,max1.9129%. Size caps differ for Zstandard API184881 versus
CLI185333 bytes; LZ4 caps both288926 bytes. Do not assert identical cross-mode
optimization contracts or statistical significance for small timing differences.

Post-hoc diagnostic, labeled separately and regenerated by the renderer: ALL10
native prefixes had already reached the recorded feasible minimum at10 evaluations;
CLI7/10 did. This is hindsight on recorded medians, not an online routing rule.

**Decision:** retire this small compression workload/grid as a source of positive
LLM-escalation evidence. Retain it as a correctness/regression/negative-control
benchmark. Do not spend more LLM calls or widen its grid until a favorable score
appears. V49's prompt/decoder-tuning stop also remains in force. These are stronger
bounded negative findings, not proof that LLM optimization cannot work. No Q2
readiness, representative workloads, independent-system router success or novel
general theory established.

## Evidence and actual resources

- V50 raw decode checks, charges, prefixes/arms: `results/v50_utility/`.
  All case metrics, frame results and nine external-manifest utility inventory:
  `results/v50_analysis/`. Source schema alone cannot certify external task utility.
- V51 raw schedule/charges/trials: `results/v51_interfaces/`.
  Actual compressed bytes: `artifacts/sources/live_v51/outputs/` (local/ignored).
  Sealed tables, all setting ratios, case summaries, PNG/SVG figures:
  `results/v51_analysis/`. All prefixes,40arms and600charges:
  `results/v51_classical/`.
- Logs, tests and verification receipts: `artifacts/study_v50/`,
  `artifacts/study_v51/`. Final post-collection manifests bind both studies.
- V50 freeze862 files; V51 freeze27 inputs including native headers/libraries.
  Compilation/tests gated each collection. No post-output collector or primary
  analysis correction. All358 tests pass. Independent audit verifies960payload
  hashes/physical events,480pairs,600source acquisitions and40arms. Frozen replay
  independently reconstructs classical decisions; V50 also replays450events.
- Two synthetic native-wrapper roundtrip checks are separately named fixtures,
  excluded from measured timing/outcome aggregates. No synthetic LLM outputs.

This continuation:846 decode verification operations;960 NEW physical compression
vectors;1050 NEW recorded-vector acquisitions;zero model calls/downloads/spend.
V50 stage4.059s/180s; V51 physical stage53.546s/180s; V51 classical/replay0.228s/30s.
Caps are separate documented extensions; historical ledgers remain unchanged.
Cumulative recorded accesses15758; physical compression trials2234; model requests
including initial100 remain1976 (follow-up including hardware1876). Decode-only
verification operations have a separate ledger. Hardware/electricity cost unknown.
Research collection includes all counterfactual arms and repetitions; do not
report these totals as a20-evaluation deployment cost.

Commands executed:
```sh
.venv/bin/python scripts/collect_utility_v50.py
.venv/bin/python scripts/analyze_utility_v50.py
.venv/bin/python scripts/collect_interface_v51.py
.venv/bin/python scripts/analyze_interface_v51.py
.venv/bin/python scripts/replay_interface_v51.py
.venv/bin/python scripts/verify_interface_v51.py
.venv/bin/python scripts/report_interface_v51.py
.venv/bin/python -m pytest -q tests
```
One-shot collectors/analyzers refuse overwrite; do not delete evidence to rerun.
Verifier/renderer use saved data with no new physical compression or model call.

**Single most important next action:** select a different source-justified
application workload with an auditable correctness/utility contract BEFORE
measuring potential gains, then test whether meaningful opportunity survives
strong classical baselines. Preserve all existing exposed system-family labels;
use independent groups for any eventual confirmatory router evaluation. Current
CLI/API modes, seeds and workload variants are not independent software systems.
This requires scientific redesign, not another decoder setting. No new model
batch, dataset download, spending, publication or author contact was performed.
No claim of work continuing outside the active session.

---

# STATUS — V49 native decoder comparison completed; stopping criterion met

Updated 2026-09-25. Resume here and `reports/decoder_v49.md`, the frozen
`reports/protocol_v49_decoder.md`, and `reports/novelty_boundary_v49.md`.
User continuation executed as a bounded local study, not another plan.
No model/experiment process remains running. Broad research goal is incomplete.

## New concrete result

Executed 54 native full-response selections and nine forced-ID repeat controls
on the same nine V48 symbol-prompt development prefixes (MySQL, Brotli, lrzip;
seeds 11, 37, 71). Native factorial: losses observed/withheld × base/reverse/ID
rotation. Same model, messages, rendered prompts, context and greedy parameters;
removed grammar/forced newlines in the native arm. Thinking remained disabled.

- All 53 valid native selections exactly matched the corresponding historical
  forced-ID configuration SETS. One native response returned invalid `id1` etc.;
  preserved as a failure, without repair/retry/replacement. Native validity 53/54.
- All nine forced repeat controls reproduced original selections.
- Baseline loss removal: 0/8 valid pairs changed; 1/9 unknown due to failed endpoint.
- Observed-loss display reversal: 6/8 valid pairs changed; 1/9 unknown. Overlap
  bounds 22.2%–33.3%, below the predeclared 80% requirement.
- Screen FAILED: format validity and control reproduction pass; responsiveness
  and stability fail. Full denominator and unknown-overlap bounds retained.

**Stop this prompt/decoder-tweaking branch on these cases**, as frozen before
collection. Native generation did not rescue the observed behavior. This does
not show that every LLM/decoder fails or that grammar never affects outputs.
No new optimization score, useful router, independent-group validation, or Q2
readiness established. Only three independent development families.

## Evidence and verification

- `results/v49_decoder/`: all 144 HTTP generation starts/responses, 63 preflight
  records and parsed outputs, runtime/model provenance and ledger.
- `results/v49_analysis/`: all 63 cases, 63 within-native pairs, family summaries,
  historical comparisons, tables and PNG/SVG figure (visually inspected).
- `artifacts/study_v49/`: collection/server logs, full test receipts, independent
  verification, aggregate crosscheck and final `evidence_manifest.json`.
- All 306 pre-inference frozen hashes intact; 63 rendered prompts/token lists
  match V48; all 144 traces, parser decisions, mappings and sensitivity arithmetic
  verified without opening raw targets. All 353 tests pass before/after collection.
- A post-collection verifier mistakenly checked retained `tokens_cached` instead
  of reuse `timings.cache_n`. Corrected the verifier; initial failure/source/hash
  audit preserved in `verification_field_correction.json` and sibling receipts.
  No frozen collection/analysis code or measured result changed.
- Focused primary-source check confirms prior order/ID bias and generated-text
  versus first-token studies. Full details/version boundaries/access limits are
  in `reports/novelty_boundary_v49.md`; no standalone novelty claim.

## Actual costs and commands

Live stage 121.836 seconds (900-second cap). All 144 allowed generation requests
consumed: 54 native and 90 forced. Native generated 1,090 tokens; controls 90.
Native input/prefill 51,729 tokens; controls full-context sum 91,490, actual prefill
9,230. Request wall time 103.568s native, 17.236s forced, with different condition
counts/mixes; not a matched deployment-speed claim. Server exited 0; port 18475
has no listener. Zero retries, downloads, new objective acquisitions or paid spend.
One malformed native response; zero missing cases, duplicates or transport errors.

Cumulative follow-up requests including hardware fixtures: 1,876 (1,976 including
initial 100); recorded objective accesses remain 14,708, physical trials 1,274.
Historical ledgers untouched. Hardware/electricity cost unknown. All factorial
conditions are research collection cost; deployment would select one condition.

Commands executed:
```sh
.venv/bin/python scripts/prepare_decoder_v49.py
.venv/bin/python scripts/collect_decoder_v49.py
.venv/bin/python scripts/analyze_decoder_v49.py
.venv/bin/python scripts/verify_decoder_v49.py
.venv/bin/python scripts/report_decoder_v49.py
.venv/bin/python -m pytest -q tests
```
Successful compilation/full tests gated protocol freeze and launch. Collector
ran with approved host Metal/loopback access. Do not rerun one-shot collection
or overwrite outputs. Verifier/renderer use saved records without inference.

**Single most important next action:** audit benchmark configurations for equal
application quality/correctness and freeze a utility-matched independent-family
comparison before further LLM optimization collection. Keep this failed adapter
as a negative baseline. Additional reasoning-enabled/larger-model or direct
configuration proposals are untested possibilities, not automatically authorized
new batches or assured remedies. Do not turn exposed cases into fresh confirmation.
No paid spending, publication, push or author contact; none performed. No claim
that work continues outside the active session.

---

# STATUS — V48 controlled diagnostic completed; display-order sensitivity verified

Updated 2026-09-25. Resume here, `reports/sensitivity_v48.md`, the frozen
`reports/protocol_v48_sensitivity.md`, and `results/v48_analysis/summary.json`.
The user's continuation was executed as a bounded development-only diagnostic.
No experiment or model server remains running. The research goal is incomplete.

## New concrete result

Completed all 108 real SmolLM3-3B Q4_K_M continuations: three original development
families (MySQL, Brotli, lrzip), three fixed seeds, two representations, losses
observed/withheld, and three display/ID arrangements. Ten one-token requests per
continuation: 1,080 generation requests, not 108. Protocol, prompts and analysis
were frozen before inference. No new objective acquisition or held-out exposure.

- Removing observed losses in the standard display left selections unchanged in
  17/18 representation/prefix pairs. All nine prefixes had ten distinct losses.
- Reversing candidate display changed selections in 14/18 loss-present pairs;
  mean mapped-configuration overlap was only 22.2% for both representations.
- Rotating arbitrary IDs while retaining displayed feature order preserved
  selected rows in all nine original-symbol cases. This separates display-order
  dependence from merely preferring the lowest numerical IDs.
- Actual numeric settings under named columns did not pass the frozen screen.
  Both representations failed responsiveness and stability criteria.
- Loss removal changed 10/54 sets across all presentation contexts. Do not claim
  the model never uses observed losses. No optimization-quality claim from V48.

This strengthens the local failure explanation from V47. It does not establish
novelty, useful benefit-aware routing, independent-system generalization or Q2
readiness. Three families are the independent groups; seeds are repeated cases.
Model/interface/decoder effects remain confounded. No repeated identical-prompt
runs quantify device nondeterminism. No prompt tuning followed these outcomes.

## Evidence, verification and costs

- Raw prompts and execution receipts: `artifacts/study_v48/`.
- Runtime, preflights, requests, responses and choices: `results/v48_sensitivity/`.
- All 108 cases, 126 paired sensitivities, aggregate tables and PNG/SVG figure:
  `results/v48_analysis/`. Figure visually inspected.
- Independent verifier passed all 163 frozen hashes, 108 prompt transformations,
  1,080 request/response sequences and both screening decisions. Nine baseline
  symbol messages exactly match saved V8 originals; no raw target tables read.
- Full suite: 348 tests passed (`artifacts/study_v48/tests_all.txt`). Successful
  compilation and preflight tests gated launch. No analyzer correction in V48.
- Final artifact hashes: `artifacts/study_v48/evidence_manifest.json`; this is
  a post-collection integrity manifest, distinct from the pre-inference freeze.

Actual local stage: 464.482 seconds; request wall-time sum: 462.790 seconds.
1,080 generated choice tokens; 2,433,720 summed full-context input tokens;
244,344 actually prefilled tokens reported after within-case cache reuse.
Zero retries/failures/fallbacks, new objective accesses, downloads or paid spend.
Server exited 0. Hardware/electricity cost is unknown. All factorial conditions
are research-collection cost; no deployment-cost savings are claimed.

V48's 1,080-request allowance is consumed, within its 900-second live-stage cap.
Earlier ledgers remain unchanged. Cumulative follow-up generation requests are
1,732 including two hardware fixtures (1,832 including the initial 100 requests).
Recorded objective accesses remain 14,708; physical trials remain 1,274. No
additional inference allowance is silently created by this status update.

Commands actually executed:
```sh
.venv/bin/python scripts/prepare_sensitivity_v48.py
.venv/bin/python scripts/collect_sensitivity_v48.py
.venv/bin/python scripts/analyze_sensitivity_v48.py
.venv/bin/python scripts/verify_sensitivity_v48.py
.venv/bin/python scripts/report_sensitivity_v48.py
.venv/bin/python -m pytest -q tests
```
Collector/preparation/analysis are one-shot; do not overwrite original outputs.
Verifier and figure renderer replay saved evidence without new inference.

**Single most important next action:** freeze a bounded development comparison
of the forced one-token decoder against native multi-token selection, retaining
these loss/order controls. This would test whether the interface prevents useful
selection. It is proposed, not executed. Do not merely revise table wording until
it passes. Only a stable, label-responsive intervention that also beats strong
classical controls should advance to independent-group evaluation. Otherwise
consolidate the negative finding and audit novelty. No publication, push or author
contact is authorized or performed; no work continues outside an active session.

---

# STATUS — V47 cross-model robustness study completed; negative result verified

Updated 2026-09-25. User explicitly requested research continuation after V46.
Executed one frozen SmolLM3-3B Q4_K_M batch: thirty continuations across six
exposed software families × five seeds, with the exact V41 prefixes/pools/messages.
All 300 one-token local generation requests and 300 recorded-objective accesses
completed without failure/fallback/retry. Collection 66.917 seconds; server exited
cleanly. No active model process, paid spend, downloads or remote publication.

**Result:** SmolLM3 mean relative gain -3.026% versus matched batch3NN,
-4.926% versus full-domain sequential3NN, -3.130% versus Qwen1.5. Predeclared
positive screening criterion failed. This is exploratory exposed-system evidence,
not held-out router validation or journal readiness.

**New mechanism diagnostic:** SmolLM3 selects IDs 0..9 in 29/30 cases. The
post-hoc first-ten-ID no-LLM control achieves identical final targets in 30/30,
using already acquired outcomes. Ordering shortcut is a supported interpretation,
not a proven causal explanation. Do not resume tuning this adapter on these cases.

Read `reports/smollm_v47.md`, `reports/protocol_v47_smollm.md` and
`results/v47_analysis/summary.json`. Raw requests/choices:
`results/v47_smollm/`; outcomes/figures: `results/v47_analysis/`.
Independent verification checked 300 request sequences, 300 source acquisitions,
270 contrasts, 18 policy summaries. All 344 tests pass (`pytest -q tests`).
One frozen-analyzer syntax error was corrected in a separate preserved copy
before analysis; audit: `artifacts/study_v47/analysis_syntax_correction.json`.

Resources: 650 research follow-up generation requests plus 2 hardware-check
requests = 652 (752 including initial100). V47's specific 300-request allowance
is consumed; historical350 ledger retained unchanged. 14,708 cumulative recorded
outcome accesses; physical trials unchanged at1,274. See separate V46/V47 ledgers
for setup/model/evaluation runtimes rather than silently resetting old costs.

**Next scientific action:** a frozen development-only representation/order and
label-sensitivity diagnostic, followed by an exposure audit for untouched groups.
Useful routing must pass development evidence before a new held-out collection.
Admission-only audit saved 33 candidate entries across 11 group names absent
from local admitted manifests; see `artifacts/study_v47/future_group_admission_audit.json`.
These are not yet verified untouched/eligible groups; no new raw targets read.
The main research goal is not complete; a Q2-ready positive result is not promised.
Do not claim work continues outside an active session.

Read-only replay:
`.venv/bin/python scripts/verify_smollm_v47.py`
`.venv/bin/python scripts/report_smollm_v47.py`
`.venv/bin/python -m pytest -q tests`

---

# STATUS — V46 SmolLM3 local feasibility completed

Updated 2026-09-25. The user's new local-install/speed-test authorization was
executed after the user-requested Next.js and Docker shutdown. SmolLM3-3B Q4_K_M
is now installed project-locally with pinned official llama.cpp b11146.
Two real offline generations completed, no failures or retries: 54.4 and 50.6
reported generation tokens/s, each about 2.205 GiB peak RSS. Entire inference
stage 24.746 seconds. Full GPU offload requested; Metal Apple M3 Pro availability
verified, exact layer placement not logged. No model process remains running.
Two new targeted tests passed; receipt: `artifacts/study_v46/tests.txt`.

Read `reports/local_feasibility_v46.md` and
`artifacts/study_v46/verified_measurements.json`. Raw commands/prompts/outputs are
in `artifacts/study_v46/feasibility/`. Recheck without inference:
`.venv/bin/python scripts/verify_smollm_feasibility_v46.py`.

Downloaded 1,926,495,026 payload bytes plus <=1-MiB metadata reserve under the
new 3-GiB setup bound. Both payload SHA256s match publisher records. The separate
two-request feasibility allowance is consumed; old research ledger remains
350/350. Combined follow-up requests 352 (452 including initial stage).
No objective acquisitions or paid spend; no changes to existing research results.
Exact token totals and separate model-load duration were not exposed by CLI.
Synthetic prompt and its real response are hardware fixtures, not research data.

**Next action:** freeze a new cross-family research comparison and resource budget
using this verified local runtime. The old adaptation's stopping rule still
applies. No positive optimization or Q2-readiness claim follows from this test.
The previous resource/scientific blocker below is historical for the research
batch; the explicit new user approval resolved local setup only.

---

# STATUS — Broader research goal blocked; approved experiments and replay complete

Updated 2026-09-25. Goal status is **blocked**, not complete. Revalidated current
350/350model-call usage, intact V45archive, complete V44collection,338test
receipt and the frozen scientific stopping decision. The preceding turn made
progress by completing the portable replay artifact. This turn produced no
new experiment or scientific evidence; it audited the remaining blocker.

The exhausted350-call allowance has persisted since the approved V44collection,
through V45packaging and this audit (threeconsecutive goal turns). All work in
the approved collection and independent verification/replay deliverables is
finished. No experiment is running. This is a fresh post-V44resource/scientific
impasse, not the resolved V44approval blocker at290calls.

Current evidence does not prove useful predictive routing or Q2readiness.
Further model evidence needs a scientifically different study with an explicit
new resource allowance. Repeating the stopped candidate-ID/small-model
adaptation on exposed cases is not a justified next step. No additional calls,
downloads, spending or author contact are inferred from automatic continuation.
Do not mark the goal complete or generate more packaging as if it were evidence.

**Next action:** use `reports/review_guide_v45.md` and the local V45review ZIP to
review the negative result's contribution with Tim before defining another
collection. No communication has been sent. If that leads to a new study,
freeze an independent design and concrete resource request before inference.
No arbitrary additional call batch is currently proposed.

Audit: `artifacts/study_v45/goal_blocked_audit.json`. Resources and results below
remain unchanged;305.253415seconds runtime remain but zero inference requests.

---

# STATUS — V45 portable results replay completed

Updated 2026-09-25. V45 packages the completed V41–V44 evidence; no new model
experiment, objective acquisition or scientific quality result. The previous
turn completed60real V44calls and source/arithmetic verification. This turn
closed the missing portable-replay deliverable for the latest results.

**Local review ZIP:** `output/llm_escalation_v45_review.zip`
3,106,475bytes;974files (973hashed payloads plus manifest).
SHA256 `0d29d3ad60e8a12a600a8199eb9b48d04ca94de43d3dbaaa50112d3e7c96bd0d`.
Start with `reports/review_guide_v45.md`. After extraction:

```sh
python3 -I -S scripts/verify_review_bundle_v45.py
```

Executed `scripts/build_review_bundle_v45.py`: two isolated Python interpreters
agree, using only the standard library. Checks4,800recorded acquisition events;
replays420V41contrasts/14summaries/108policymeans,120V43comparisons,
240V44comparisons/60exactrandomreferences/8aggregates. V42exhaustive receipts are
included but its full enumeration is not rerun by this command. Hash-tampered
evidence and a deliberately changed gain with an updated hash were both
rejected. Extracted copy was restored and all973hashes rechecked. Original
V41ZIP and all measured evidence remain unchanged.

Evidence: `artifacts/study_v45/review_bundle.json`, `replay_attempts.json`,
`arithmetic_corruption_rejection.json`, `build.log`, `final_checks.json`.
The archive was not uploaded/published/sent. It omits weights, original full
source tables, papers and credentials. Dataset-specific redistribution
permission remains unresolved. This is acquired-record results replay, not
fresh inference, original-data authenticity checking, independent hardware
replication or proof of journal readiness. Local source-check receipts describe
checks requiring omitted source data. No new software-test count is claimed;
V44's338passed-tests receipt is included.

The scientific conclusion remains V44's negative result. The frozen stopping
rule ends more tuning of the current small-model/candidate-ID adaptation on
these exposed systems. Useful predictive routing, independent-model
validation, equal application utility and established novelty remain absent.
The overall goal is NOT complete.

**Single most important next action:** review the bounded negative finding and
its novelty with Tim Menzies before another collection design. No contact is
authorized. A substantive new inference study also needs a new bounded resource
allowance; all350approved follow-up calls are consumed. Do not infer another
extension from automatic continuation or treat artifact packaging as fresh
research evidence.

Resources:350/350follow-up calls;3294.746585/3,600seconds;
305.253415seconds remaining. No new calls/accesses/downloads/spending.
14,408cumulative recorded accesses,1,274physical trials unchanged. No active job.

---

# STATUS — V44 real-model experiment completed; this adaptation meets its stopping rule

Updated 2026-09-25. Resume from this section and `reports/models_v44.md`.
The user's exact60-call approval was recorded and fully executed. That approval
blocker is resolved. The broader research goal remains unachieved: no validated
benefit-aware router or Q2-readiness claim. No current process remains running.

## Concrete new result

Completed60real Qwen2.5-1.5B-Instruct calls: six exposed software families × five
seeds × both frozen alternative pools. Same saved10-label prefixes,10new
outcomes per arm,20logical evaluations. No missing cases/errors/retries/fallbacks.

| Pool | Reference | Mean relative gain | Wins/ties/harms |
|---|---|---:|---:|
| Uniform20 | Own-pool batch3NN | -1.21144% | 0/24/6 |
| Uniform20 | Full-domain sequential3NN | -4.01660% | 1/14/15 |
| Retained10 + diverse10 | Own-pool batch3NN | +0.00248% | 3/21/6 |
| Retained10 + diverse10 | Full-domain sequential3NN | -1.94405% | 4/15/11 |

All four frozen references and exact random-selection expectations are retained
in the report/JSON/CSV. Uniform-pool LLM selection is never better than its own
cheap batch control on these30cases; no router choosing between those branches
can gain quality on this sample. This is a finite-sample observation, not a
universal LLM impossibility claim. The diversity pool's tiny favorable mean
against its own control does not survive full-domain sequential3NN.

V43's widened hindsight opportunity was not robustly exploited. Per the frozen
V44 decision rule, **stop this particular candidate-ID/small-model adaptation**.
Do not tune these exposed cases until favorable. No new inference extension is
proposed merely to obtain a positive result.

## Actual cost and evidence

60requests;600newrecorded outcome accesses;98,358input/1,200output tokens;
397.139428seconds request wall time;413.729752seconds model stage, below450.
Zero new physical trials/downloads/external spending. Follow-up cap350/350
(450includinginitial); cumulative recorded accesses14,408; physical trials1,274.
Final cumulative runtime3,293.338663/3,600seconds;306.661337seconds remain.

- `results/v44_models/`: all raw starts/responses/provenance/token IDs,60arms,
  prefix checkpoints and600-event journal.
- `results/v44_model_analysis/`: complete240row paired CSV,8contrasts,60exact
  random comparisons, per-family/capture/cost data, PNG/SVGfigure.
- `artifacts/study_v44/`: collection and analysis logs, independent verifier,
  cost receipts, corruption-rejection receipt, tests and `final_checks.json`.
- **338tests pass**. Independent stdlib checks match600acquisitions to565source
  rows and recompute all240contrasts/60exactrandom comparisons/8aggregates.
  All60token/prompt/grammar traces replay. Deliberately corrupted temporary
  data are rejected. All original and correction freezes remain intact.
- Figure visually inspected. Model logits were not reproduced on another
  machine. Previous V41review ZIP remains unchanged and excludes V42–V44.

## Analysis correction, preserved honestly

Original frozen `scripts/analyze_pool_models_v44.py` stopped on the paired-state
check: shared mutable lists changed the in-memory prefix between pools. Disk
prefixes and raw model outputs were unaffected. Its failed output/log and
2.695453seconds are retained in `artifacts/study_v44/analysis_attempt1/`.

Use **`scripts/analyze_pool_models_v44_fixed.py`**. It deep-clones the prefix,
passes the new two-pool/direction regression, and retains all original scientific
endpoints. Original code is preserved. Correction and raw outputs are bound by
`reports/analysis_correction_v44.md` and its freeze. No failed summary was used.
The corrected analysis completed and the independent verifier agrees.

Commands actually executed:
```sh
.venv/bin/python scripts/run_pool_models_v44.py
.venv/bin/python scripts/analyze_pool_models_v44.py  # failed; preserved
.venv/bin/python scripts/analyze_pool_models_v44_fixed.py
.venv/bin/python -I -S scripts/verify_pool_models_v44.py
.venv/bin/python scripts/render_pool_models_v44.py
.venv/bin/python -m pytest -q tests/synthetic tests/test_transfer_v41.py
```
Collection terminalexit0 was confirmed through tool session66555. The corrected
analyzer and verifier also exited0. Do not rerun one-shot collectors or overwrite
measured outputs. No indefinite background job.

## Single most important next action

Review this negative mechanism result and its distinction from close prior work
with Tim Menzies before authorizing a new collection design. No author contact
is authorized or performed. If more research is justified, prioritize a
semantically informed intervention with a genuinely different model family,
equal application utility/correctness and independent development/test systems.
Current evidence remains exploratory: the model study, hindsight ceiling and
336/338software checks do not establish a useful predictive router or publication
readiness. Independent hardware replication and live utility validation remain
untested. Do not claim goal completion or guaranteed journal acceptance.

---

# STATUS — V44 approved and collecting real local-model responses

The user explicitly approved the60-call extension. Approval is recorded in
`configs/authorization_v44.json`, bound to the unchanged frozen protocol.
Collection is running via `scripts/run_pool_models_v44.py`, tool session66555;
confirm that handle/process state before any recovery. Never restart based on
an observation timeout. Logs: `artifacts/study_v44/collection.log`.

Request cap350;450second stage; unchanged3,600second globalruntime;600recorded
accesses maximum; no retries/downloads/spending. It runs outside the sandbox
with environment approval to avoid the previously verified OpenMP SHM failure.
No model settings or scientific endpoints changed. No quality results have
been analyzed yet; wait for the complete intended60-case denominator.

---

# STATUS — Goal blocked pending the new model-call allowance

Updated 2026-09-25. Goal status is now **blocked**, not complete. The same
resource-approval blocker has persisted for three consecutive goal turns.
The preceding turn made independent progress by implementing and testing the
V44 analysis; that preparation is complete. This turn revalidated the actual
approval/configuration state and both freezes. It produced no new experiment.

`configs/authorization_v44.json` remains false. All290approved follow-up calls
are consumed. There are no V44 model outputs or measured analyses. All203
protocol inputs and126analysis inputs remain unchanged. The336-test receipt
is preserved; no redundant test run or model request was performed.

To resume the prepared assay, approve **60additional local requests, cap290->350,
450seconds maximum collection inside the unchanged3,600second globalcap,
at most600recorded accesses, zero retries/downloads/spending**. Then record
the actual approval against the existing freeze and execute the frozen V44
collector and analysis. Do not infer permission from automatic goal wake-ups.

Remaining runtime727.202468seconds; no new costs or acquisitions. The latest
measured finding remains V43's candidate-pool opportunity/selection gap, not
a validated positive LLM/router result. Q2 research readiness remains unproven.
No indefinite job or background continuation was started. Audit receipt:
`artifacts/study_v44/blocked_audit.json`. Full evidence and resume details below.

---

# STATUS — V44 analysis implemented and tested; call approval still pending

Updated 2026-09-25. The previous goal turn made concrete progress: V43 acquired
1,200 outcomes and completed120continuations. This turn completed analysis
implementation and failure-path tests without running new inference.

- `scripts/analyze_pool_models_v44.py`: validates complete request/prefix/state/
  acquisition provenance and token grammar; compares both pools with all four
  frozen references and exact uniform selection; preserves unknown usage and
  refuses incomplete-case quality aggregates.
- `src/escalation/pool_analysis_v44.py`: exact signed headroom capture, null for
  nonpositive headroom, family aggregation and selection/fallback checks.
- `reports/analysis_addendum_v44.md` and `.freeze.json`: operational definitions
  and126input hashes, frozen before any V44 response. Original V43/V44 protocol,
  collector, model interface, prompts and proposed authorization are unchanged.
- **336 tests passed**, including15new synthetic analysis tests. The real CLI
  correctly refuses absent model data, creates no measured analysis directory,
  and leaves the resource ledger unchanged. Receipts/logs are under
  `artifacts/study_v44/analysis_readiness.json`, `analysis_tests.log`, and
  `no_data_analysis.log`. Synthetic tests are not experimental LLM outputs.

The full postprocessor has not yet run on real V44 responses because those
responses do not exist. It must be exercised and checked against independent
arithmetic after real collection. Nothing is claimed about new model quality,
useful routing, or journal readiness from these software checks.

**Single next action remains approval of the prepared60-call V44 assay**:
290->350calls,450seconds maximum inside unchanged3,600seconds, at most600new
recorded accesses, zero retries/downloads/spending. The previous direct user
approval was consumed by V41. This automatic goal continuation is not new
resource authorization. `configs/authorization_v44.json` remains false.
No process is running; there is no live-job wait.

After explicit approval: record it against the unchanged V44 protocol freeze;
run `scripts/run_pool_models_v44.py`; retain every failure; then run
`scripts/analyze_pool_models_v44.py` and independently verify real outputs.
Do not modify sealed prompts/policies after seeing new results.

Resources remain290/290calls,2,872.797532/3,600seconds,727.202468seconds remaining;
13,808cumulative recorded accesses and1,274physical trials. No calls/acquisitions/
experimental computations this turn beyond software tests/validation. The
research goal remains active and incomplete. The same cap blocker was first
reported in the preceding V43 turn; this is its second consecutive turn, with
independent implementation progress completed rather than an idle wait.

---

# STATUS — V43 candidate-pool experiment completed; V44 model test prepared

Updated 2026-09-25. Resume here and from `reports/pool_ablation_v43.md`.
The original goal remains unachieved: useful predictive escalation and Q2
research readiness are not established. Scientific honesty takes precedence
over obtaining a positive result.

## New concrete result

Executed 120 classical/coverage continuations across all six V41 software
families and five seeds, with 1,200 charged recorded outcome accesses. Same
saved ten-label prefixes; every arm has twenty logical evaluations. Two new
candidate pools were frozen before acquisition. No cases were dropped.

Against full-domain sequential 3NN:

| Pool | Actual batch 3NN gain | Perfect selector, always used | Perfect selection + routing |
|---|---:|---:|---:|
| Original shortlist | -1.9416% | -1.8207% | +0.2915% |
| Uniform20 | -2.7912% | -0.6179% | +2.7127% |
| Retained10 + diverse10 | -1.9524% | -1.7064% | +0.3038% |

Last two columns are nondeployable hindsight diagnostics, not LLM/controller
results. Uniform sampling reveals more potential, concentrated mainly in Dune
and BerkeleyDB; cheap selection fails to capture some large opportunities.
Geometric diversity alone adds little. These are exposed-system exploratory
findings, not new held-out confirmation. No new LLM output was generated.

## Evidence and checks

- `reports/protocol_v43_pool_ablation.md` and `.freeze.json`: pre-acquisition
  protocol, algorithms, source hashes, thirty prefixes and sixty pool plans.
- `results/v43_pool_ablation/`: all 120 arms, complete acquisition journal,
  summary JSON, all comparisons CSV and visually checked PNG/SVG figure.
- `artifacts/study_v43/`: collection/analysis/test logs, independent verification,
  resource receipts and final checks. All 1,200 events match 1,047 distinct
  source rows. Sixty exact distributions checked by enumerating 11,085,360
  hypothetical subsets; those are calculations, not additional experiments.
- Final combined suite: **321 tests passed**. V41/V42/V43/V44 freezes verified.
  V41 review ZIP remains unchanged and does not include V42/V43.
- `reports/literature_update_v43.md`: primary-source audit confirms LLAMBO
  already separates candidate generation and selection, and SNAP2's projected
  proposals differ materially from this fixed-shortlist adaptation. No novelty
  or replication claim. Repository commit lookup failed; not silently pinned.

Actual commands:
```sh
.venv/bin/python scripts/run_pool_ablation_v43.py prepare
.venv/bin/python scripts/run_pool_ablation_v43.py collect
.venv/bin/python scripts/run_pool_ablation_v43.py analyze
.venv/bin/python -I -S scripts/verify_pool_ablation_v43.py
.venv/bin/python scripts/render_pool_ablation_v43.py
.venv/bin/python scripts/prepare_pool_models_v44.py
.venv/bin/python -m pytest -q tests/synthetic tests/test_transfer_v41.py
```
Collection/preparation/analysis are one-shot; preserve outputs. A deliberately
disabled V44 collector invocation correctly raised PermissionError before any
model startup, did not create model results, and left the ledger unchanged.
This was the configured authorization guard, not an automatic approval-review
rejection or an attempted model experiment.

## Prepared next action and precise blocker

The single next action is the real **V44 changed-pool model assay**:
`reports/protocol_v44_pool_models.md` and its freeze; collector
`scripts/run_pool_models_v44.py`. All sixty prompts are saved in
`results/v44_preflight/`, locally tokenized (maximum 3,301 input tokens), and
bound to frozen prefixes/pools. Uses installed Qwen2.5-1.5B, both pools, all
six families/five seeds; no favorable-pool selection. Inference remains untested.
The implementation's disabled/overbroad approval checks passed; real V44 model
execution and its outcome analysis have NOT run.

Required new bounded approval: **60 additional local calls, cap 290 -> 350;
450-second collection stage within unchanged 3,600-second global cap;
maximum 600 recorded accesses; zero request retries, downloads or spending**.
`configs/authorization_v44.json` is explicitly false and bound to the protocol
freeze. Do not infer approval from automatic continuation. On explicit approval,
record the actual user approval and run the frozen collector. The old V41
60-call approval was already fully consumed. If sandbox OpenMP shared-memory
startup fails, preserve logs and use normal environment escalation; never alter
model settings or silently rerun completed requests.

Even a positive V44 result is a mechanism result on exposed cases. Independent
development/test groups, equal application utility/correctness, another model
family and novelty remain untested. No publication, push or author contact.

## Remaining resources

Follow-up model calls 290/290 (390 including initial stage). Cumulative runtime
2,872.797532/3,600 seconds; 727.202468 seconds remain. V43 charged 7.256034 seconds;
V44 prompt preparation charged 4.608495 seconds. Cumulative recorded accesses
13,808; physical trials remain 1,274. No new external spending or download.
No active model or experiment process. Broad research goal remains incomplete.

---

# STATUS — V42 exact shortlist diagnostic executed

Updated 2026-09-25. Resume from this section, `reports/selection_reference_v42.md`, `reports/protocol_v42_selection_reference.md` and its freeze. The V41 measured study below is unchanged; V42 is explicitly post-hoc, not a new held-out confirmation.

New concrete result: every saved shortlist was fully covered by already acquired branches. Exact uniform ten-of-twenty selection distributions were computed for all30prefixes and independently checked by enumerating5,542,680subsets. No new model call or objective acquisition.

-1.5B attains the shortlist ceiling28/30times; batch3NN already does27/30. Maximum possible mean gain over batch3NN is only+0.1174%, versus the measured+0.1024%.
-Against full-domain sequential3NN, a perfect shortlisted selector used on every case is bounded at−1.8207%, versus measured1.5B−1.8356%. Seven cases still permit selective gains, fifteen tie and eight cannot match full-domain search. Do not claim all possible routers are dominated.
-Exact expected relative gain vs uniform selection:1.5B+1.0689%,0.5B−1.8872%; all six family means respectively positive/negative. Conditional random-match probabilities are not population p-values.

This separates within-shortlist selection quality from a candidate-pool limitation. It supports a more specific negative/mixed contribution, but Q2 readiness, novelty and useful routing remain unproven. Larger selectors alone cannot remove a fixed-pool ceiling. Do not retune the exposed cases until favorable.

Evidence: `results/v42_selection_reference/summary.json`, all60model comparisons/60ceiling comparisons inCSV, PNG/SVGfigure; `artifacts/study_v42/analysis.log`, `exhaustive_verification.json`, `tests.log`;315tests pass. Original308inputs frozen before these new calculations; exact formulas checked by independent enumeration. Figure visually verified. No new LLM output or live physical trial. The V41review ZIP is unchanged and excludes V42.

Commands actually run:
```
.venv/bin/python scripts/analyze_selection_reference_v42.py
.venv/bin/python -I -S scripts/verify_selection_reference_v42.py
.venv/bin/python -m pytest -q tests/synthetic tests/test_transfer_v41.py
.venv/bin/python scripts/render_selection_reference_v42.py
```

Resources:290/290follow-up calls;2860.933003/3600seconds, remaining739.066997s. V42 charged2.187796s, zero calls/acquisitions/downloads/USD. No active job. Previous turn was substantive progress(real60-call V41); this turn made progress with a new exact diagnostic. Broad goal remains unachieved; no completion claim.

**Next scientific action:** compare this specific candidate-pool diagnosis with prior work and develop an escalation intervention that can expand useful search regions under equal application quality and independent development/test groups. More ranking calls on these same shortlists cannot solve the observed limitation. Any new inference still requires a concrete bounded extension; no cap increase is inferred from automatic continuation. No author contact/publication authorized.

---

# STATUS — V41 real-model study completed and verified

Updated2026-09-25. Resume from this file, `reports/models_v41.md`, the unchanged original protocol/analysis seals and the measured summaries. Do not reread the full literature report. The user's exact60-call extension was approved and fully executed. The old approval blocker is resolved; the broader Q2-quality objective remains unachieved and is not marked complete.

## New concrete research result

Completed60real local-model cases: six newly admitted software families × five fixed seeds × two Qwen2.5-Instruct sizes(0.5B/1.5B). Each shares its original10-evaluation prefix and acquires10continuation outcomes. No completed cases, seeds, failed attempts or poor results were dropped. Seven classical controls were fixed in advance.

-1.5B vs primary batch3NN: **+0.1024%** equal-family mean,2wins/27ties/1harm; family bootstrap95%[0%,0.3073%], exact sign-flip p=1. Only HIPAcc has a nonzero family mean.
-1.5B vs full-domain sequential3NN: **−1.8356%**,6wins/15ties/9harms; exact family p=.15625.
-0.5B vs batch3NN: **−3.0260%**; vs full-domain sequential3NN: **−4.9260%**.
-The unchanged benefit router selects1/30cases. On1.5B it ties batch3NN and slightly harms the strong control; on0.5B it harms quality. Uncertainty selects0calls. No successful useful routing claim.
-1.5B hindsight oracle opportunity is only0.1075% vs batch3NN(2calls) or0.2816% vs full-domain3NN(6calls), before cost. Diagnostic/nondeployable.

This is a stronger negative/mixed empirical result than the previous two-family study, not evidence that the original hypothesis is established. Six groups, two sizes of one model family, benchmark age/subsampling/nominal encoding, unknown application quality and unresolved novelty still prevent a Q2-readiness claim. Do not keep tuning these now-exposed cases until a mean becomes positive.

## Execution and reliability

The0.5B model completed30cases. The first1.5B worker failed during startup with OpenMP Error179(Cannot open SHM), before issuing any request. Terminal original run and logs are preserved in `artifacts/study_v41/recovery_attempt1/`. User-approved sandbox escalation allowed the one-shot recovery wrapper to run only the30unattempted1.5B cases with unchanged settings. All63completed0.5B files were hash-preserved. Failed-startup time counted against the same700-second stage cap. No request retry; one startup retry/failure. Transformers implementation warnings remain in raw logs.

Actual model collection:60requests,600newrecorded outcome accesses,98,342input tokens,1,200output tokens,254.780243s request wall time,277.213992s total stage time including startup/failure/recovery. Combined V41 collection:3,000recorded accesses including the210classical continuations. Every logical deployment arm remains20evaluations. No new physical trials, downloads, cloud usage or external spending.

## Verified evidence

- `results/v41_models/`: all requests/request-starts/model identities,60branches, checkpoints,600-event acquisition journal and complete denominator.
- `results/v41_model_analysis/`: all420paired comparator rows,14contrasts,108policy views, complete cost summary, two PNG/SVGfigures.
- `results/v41_policy_precommit/`: decisions and analysis seal from before all new model responses;29/30prefixes outside at least one development range; no refit.
- `artifacts/study_v41/`: collection/recovery logs, source/token/arithmetic checks, tests, archive receipts.
-300tests pass. All600acquired targets match source rows(542distinct rows), independently on Python3.10/3.12. All60prompt/token/grammar/cache-key traces replay. Fraction arithmetic independently agrees on420contrasts,14summaries and108policy means on both interpreters.
-Original103-input protocol freeze and later analysis/policy seal remain intact. Model logits were not regenerated, and a separate physical machine was not used.

## Portable local review artifact

`output/llm_escalation_v41_review.zip` — 1,613,626bytes,465files; SHA256 `84a935ae4373a7299dbf49f14f58434b3528fd893fad026245f426b3e75657c8`.
Extract locally and run `python3 -I -S scripts/verify_review_bundle_v41.py`. Verified in isolated3.10/3.12 processes; deliberate corruption of an extracted copy was rejected. It reproduces acquired-record arithmetic, not fresh model inference. Full datasets, weights and papers are omitted; source manifests/hashes and local-check receipts remain. Nothing was uploaded, pushed or sent to anyone. DeepPerf data-specific redistribution permission remains unresolved.

## Commands actually executed

```sh
.venv/bin/python scripts/run_models_v41.py
.venv/bin/python scripts/resume_models_v41.py
.venv/bin/python -I -S scripts/verify_source_events_v41.py --kind model
.venv/bin/python scripts/analyze_models_v41.py
.venv/bin/python scripts/verify_model_tokens_v41.py
.venv/bin/python -I -S scripts/verify_model_results_v41.py
.venv/bin/python scripts/render_models_v41.py
.venv/bin/python -m pytest -q tests/synthetic tests/test_transfer_v41.py
.venv/bin/python scripts/build_review_bundle_v41.py
```

Initial collector failed after the0.5B stage as described; recovery completed the denominator. Source/arithmetic/bundle verification also ran under the installed Python3.12 interpreter. Collectors/archive builder are one-shot; do not overwrite original outputs. Reanalysis counts computational runtime but no new objective acquisition.

## Limits and next decision

Follow-up requests **290/290**(390includinginitial), cumulative experiment runtime **2858.745207/3600s**, remaining **741.254793s**. Cumulative recorded outcome accesses12,608; physical trials remain1,274. No active model or experiment process. No remaining model-call allowance; do not silently extend it.

**Single most important next action:** assess with Tim Menzies whether this now-broader negative/control-transfer result offers a distinct enough contribution against the close prior work in `reports/literature_update_v40.md`, before authorizing another experimental design. A reviewable report and local replay kit are ready; do not contact him automatically. If further collection is scientifically justified, prioritize independent development families, an independent model family and equal application-utility/correctness constraints before another held-out router. A stronger result is not guaranteed by more calls.
