# STATUS — V66/V67 complete; no experiment running

Updated2026-09-26UTC. Resume here and from the relevant frozen protocol; do not
reread the initial long research report. Scientific honesty overrides obtaining a
positive result. The user wants research suitable for a possible Q2 paper; that
level of novelty/generalization is not established.

## Latest concrete result

Built and executed three additional systems: DuckDB1.3.2, GNU sort9.7 and
OpenJPEG2.5.3. All9 fixed admission trials passed. Then all432 full-grid trials
passed correctness checks, no timeout/failure/retry/missing case, in149.650159s.
Each system has one fixed generated application workload,48configurations and
three physical repetitions. All are development groups, not fresh held-out tests.

Ran45 classical arms,5fixed seeds per system, shared10-evaluation prefixes and
20-inclusive budgets. Charged600new recorded aggregate acquisitions. Both primary
RF-LCB and3NN reached the recorded minimum in **15/15 cases**. Prefix already at
minimum7/15; random continuation at minimum9/15. All three predeclared opportunity
gates fail0/5. DuckDB threshold11.459680%; sort/OpenJPEG5%. No model calls on these
failed grids; stop tuning them under V67. Recorded minima are not noise-free global
physical optima. Coverage20/48(41.7%), small regular spaces and generated short jobs
are substantial limitations; do not claim universal classical/LLM equivalence.

## Interface and source work

src/escalation/legal_proposals_v66.py builds a finite GBNF grammar containing only
currently legal full configuration vectors. It removes acquired and earlier
proposed rows, charges before requests, prevents concurrent pending calls, and
fails closed with no repair/retry. Classical controls can see the same eligible
set. Ten model selections require ten requests. **Synthetic tests only**: the
local llama.cpp grammar sampler and model choice quality remain untested here.
No old V65 response was repaired/re-scored, and no fake LLM output was measured.

Owner/registry downloads23,947,108bytes. DuckDB official PyPI wheel hash checked,
no dependencies installed, isolated project runtime. OpenJPEG owner commit
210a8a5690d0da66f02d49420d7176a21ef409dc, optional PNG/TIFF/LCMS disabled. GNU release
archive/source/binary hashes retained; downloaded signature not key-verified.
Licenses MIT/GPL3+/BSD2 recorded in THIRD_PARTY.md. No application algorithm patches.
Initial platform-tag, SDK-path and generated-header build issues fixed; failed logs
preserved. Build commands total100.555497s including failures; no system install.

Identifier exposure audit:7,725saved JSON/JSONL/manifests,84,099,466bytes,zero matches.
Not a certificate of untouched data: deleted/external/unidentified/unstructured
records remain blind spots. MongoDB/Storm reservations remain semantically unadmitted.

## Evidence and reproducibility

- Report/figure: reports/candidates_v66_v67.md;
  results/v67_candidates_screen/headroom.png and.svg, visually checked.
- Raw admission: results/v66_candidate_feasibility/; full raw outputs/receipts:
  results/v67_candidates_physical/ (SQL answers, complete sorted files, lossless
  encoded/decoded images, commands, timings, process-memory supervision).
- Tables, prefixes, arms, acquisition ledgers andCSV:
  results/v67_candidates_screen/. Data manifest:data/live_manifest_v67.json.
- Runtime pins:configs/runtime_v66.lock.json. Sources:artifacts/sources/v66/.
  Workloads:data/generated_v66/. Builds/exposure:artifacts/study_v66/.
- Frozen protocol/source hashes:reports/protocol_v66_admission.md/.freeze.json,
  reports/protocol_v67_screen.md/.freeze.json. Collection one-shot; do not delete
  result directories to rerun. New inference allowance was not included.

**448 Python tests passed.** Independent replay verified all441configuration
trials/588application invocations including decoder validation, full SQL answers,
exact sorted outputs, every decoded pixel,600label charges and540classical choices.
An additional verifier check for DuckDB's human-readable memory setting initially
used too-tight half-unit rounding tolerance; it correctly exposed the display
truncation assumption. Fixed to one displayed unit and reran successfully; no
experiment/setting/analysis changed. See verification_notes.json and final receipt.

Safe read-only replay, no model/solver/server or benchmark launches:
```
.venv/bin/python scripts/verify_candidates_v66.py
.venv/bin/python scripts/verify_candidates_v67.py
.venv/bin/python scripts/seal_evidence_v67.py --verify-only
.venv/bin/python -m pytest -q tests
```
Both verifiers require the pinned local runtime/source files. Latest clean-machine
portability has not been executed; older standalone bundles remain historical.
Report generation can change figure metadata bytes; preserve the seal by rerendering
in a copy. Source freezes and integrity checks do not establish external validity.

## Actual costs and historical preservation

V66/V67:441configuration trials,588application invocations including147decoder
validations,600recorded aggregate accesses,0new model requests,USD0external spend.
Python supervisors/workers, builds/tests/audits are extra overhead. Full-grid
collection149.650159s; admission3.547014s; optimizer replay4.350587s. A deployment
20-outcome median-of-three recipe needs60configuration trials; OpenJPEG additionally
needs60decoder validations. This is a recipe estimate, not measured deployment cost.
Hardware/electricity/researcher cost unknown. Full ledger:
artifacts/study_v67/resource_ledger.json; post-collection hardware metadata beside it.

Cumulative recorded acquisitions26,358; actual model requests1,981 unchanged.
Persistent downloads4,795,409,680bytes; remaining573,299,440bytes under5GiB.
Model access works locally; V65's5/5allowance is exhausted and V67 permitted zero.
No paid/cloud calls, credentials, remote push, publication or author contact.

V65's sealed mutable docs were copied before edits to
artifacts/study_v66/previous_snapshot/. V58/V59/V65 raw evidence preserved.
Current seal:artifacts/study_v67/evidence_manifest.json, verification receipt beside
it. Future edits must preserve matching snapshots; use the current seal verifier
for the historical redirect chain. Older seal tools see historical mutable files
as changed and must not be treated as verification of current entry documents.

Historical last real-model result remains V65: five native SmolLM3-3B calls,
0contract-valid outputs,5RF fallbacks,zero LLM-attributable gain. Code-fence removal
alone fixes none: all five reuse observed rows, four repeat proposals. V64 SAT's
single admitted task had opportunity, but the model failed the proposal contract.
See reports/sat_llm_v65.md and archived previous STATUS for exact earlier counters.

## Single next action

Audit a larger, externally defined configuration benchmark with a verifiable
utility/correctness contract **before reading its objective values**. This is more
informative than another small invented grid or tuning these failed cases until a
gain appears. See reports/next_experiment.md for admission/precision/split requirements.

Untested: real constrained grammar/model sampling, larger irregular search spaces,
stronger/reasoning models, independent-machine replication and held-out benefit-aware
routing. More seeds or generated instances do not create independent systems. These
negative development findings are credible within scope, not proof of Q2 readiness.
No background process or automatic continuation is scheduled.
