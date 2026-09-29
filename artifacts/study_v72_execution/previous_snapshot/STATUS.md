# STATUS — blocked pending V72 local-call allowance

## Resume here

Blocked audit: the same unapproved V72 allowance has persisted across three
consecutive goal turns. Independent implementation, tests, and verification are
finished. The previous turn made progress through synthetic failure testing;
this turn revalidated the unchanged blocker. No V72 collection directory or
authorization receipt exists. This is not a live process wait. The goal is being
marked blocked, not complete; no claim of journal readiness is made.

Single next action: user approval of the already requested 35 local generation
calls and 150 physical measurements, bounded to 30 minutes and zero spending.
The exact frozen command below remains unchanged. Automatic goal continuation
is not approval. After approval, resume that experiment once; retain all outcomes.

Historical STATUS was preserved at artifacts/study_v72_blocked/previous_STATUS.md.
Read-only seal verification now uses scripts/verify_blocked_v72.py.


Latest continuation: all524 tests passed in3.59s, including eight new synthetic
end-to-end orchestration checks
against the frozen V72 runner. Complete flow, no-overwrite behavior, malformed and
truncated output fallbacks, transport/startup/context/token/physical failures were
exercised without a real server, model, network or DB. No production code/protocol
changed. Evidence: artifacts/study_v72_failure_checks/. Current seal verification:
`.venv/bin/python scripts/verify_blocked_v72.py` (includes the preserved STATUS).
These are test outcomes,
not new research results. The concrete35-call allowance question is still pending;
this automatic goal continuation does not constitute user approval.


The active journal-quality research goal remains incomplete. No experiment or
model server is running. V72 has been implemented and frozen; it has NOT run.
Do not confuse its synthetic tests with measured model results.

Next action: obtain approval for the concrete V72 envelope requested in the task,
then execute the one-shot runner below. Existing V65 allowance is exhausted.
The requested scope is35 new LOCAL SmolLM3 calls, at most2240 generated tokens,
150 new physical RocksDB evaluations,30 minutes, no retries/downloads/spend.
This is not an external-model-access problem: the pinned model is already local.

```
.venv/bin/python scripts/run_rocksdb_v72.py --approved-envelope-sha256 34044827e05860507cab9706ddca0755ea58e50e8b9abc56d966373765eb58b4
.venv/bin/python scripts/verify_rocksdb_v72.py
.venv/bin/python scripts/analyze_rocksdb_v72.py
```

Only invoke collection after scope approval. Its process/memory watchdog and local
server may require normal execution-environment escalation. Do not bypass it.
Commands are one-shot; inspect an existing output/failure before any next attempt.

V72 compares ALL five saved prefixes: fresh RF, a cheap feature-only cache/block
prior, and grammar-constrained real LLM proposals under model-resident conditions.
Each arm:10 historical prefix +7 new search +3 charged confirmations =20. New
physical acquisitions150; logical charges300; historical shared prefix50.
Model invalidity switches that arm to counted RF fallbacks; transport/resource
failure stops and preserves every intended denominator. No held-out/router claim.

Files: reports/protocol_v72.md, configs/study_v72.json, reports/preflight_v72.md.
Freeze pins105 files; analysis/replay have an additional pre-collection freeze.
All516 tests passed in2.66s; authorization refusal was executed and verified before
any collection. Read-only replay again verified203 V70/V71 physical trials.
Evidence/artifacts: artifacts/study_v72/. No new research calls/downloads/spend.
Cumulative model requests1981 and remaining download allowance568438763 bytes
are unchanged. Small native test fixtures are synthetic and excluded from results.

V71 sealed entry documents were copied byte-for-byte to
artifacts/study_v72/previous_snapshot/ before editing. The V72 seal verifies this
historical redirect chain; older standalone seals require their entry snapshots.

Real grammar/runtime integration, LLM benefit, multiple independent families,
a development-trained router and untouched system-level evaluation remain untested.
See reports/readiness_v71.md. V71's classical result below is still the latest
measured research evidence. Positive results and Q2 acceptance are not guaranteed.

## Previous measured result (V70/V71)


V70 corrected the V69 binding mistake. Both DB creation and reopening pass explicit
column-family options. Active engine logs and attached-cache usage match requests.
All three fixed feasibility trials passed without changing workload/settings.
V69's invalid contrast and serialization failure remain preserved and excluded.

V71 ran five seeds (11,23,37,53,71), with shared 10-evaluation prefixes and random,
3NN and RF-LCB continuations. Each arm uses 7 additional search evaluations, then
3 fresh confirmations of its frozen selected incumbent: 20 evaluations inclusive.
Actual physical collection is 200; logical per-arm charges are 300 because 50
prefix evaluations are shared. Confirmation outcomes never influence selection.
This is an explicit reliability allocation, not the earlier 20-unique-row design.

Mean confirmed median times: random 238.3288002 ms, 3NN 236.8633582 ms,
RF-LCB 227.8048998 ms. RF is substantially better on seeds 37 and 53, worse than
random on seed 71. All three methods select configuration 3 on seed 23; tiny
same-setting differences are noise, not better policy decisions. Median within-
incumbent confirmation CV is 1.064% (only three repeats each). No significance,
global optimum, LLM benefit or cross-system claim follows. One development family.

129 unique nominal vectors were physically measured out of 512. The stronger
400-distinct-effective-configuration admission criterion remains unmet. Workload
is a scaled YCSB-C-inspired adaptation, not Java benchmark replication/production:
65536 deterministic records, 10000 warmup reads, 100000 timed reads, Python RNG,
fixed scrambled-Zipfian trace, raw 10x100-byte fields, OS cache not cleared.

## Evidence and reproduction

- Feasibility: results/v70_rocksdb_feasibility/ (full DB snapshots and receipts).
- Classical: results/v71_rocksdb_classical/ (all charges, saved prefixes, arms,
  confirmations, phase receipts, engine LOG/OPTIONS/MANIFEST and file inventories).
- Analysis: results/v71_rocksdb_analysis/ (JSON, CSV, visually checked PNG/SVG).
  interpretation.json identifies the same-setting comparison limitation.
- Protocols: reports/protocol_v70.md and protocol_v71.md with SHA256 freezes.
- Inputs/runtime unchanged: data/generated_v69/, configs/runtime_v69.lock.json.
- Logs, verification and costs: artifacts/study_v70/ and artifacts/study_v71/.

```
.venv/bin/python scripts/verify_rocksdb_v71.py
.venv/bin/python scripts/seal_evidence_v71.py --verify-only
.venv/bin/python -m pytest -q tests
```

First two commands are read-only with no DB opens. Tests run tiny native synthetic
fixtures if the optional pinned runtime exists; three explicitly skip otherwise.
V71 temporary SST/data files were hashed then removed after archiving receipts and
engine metadata; these are NOT full physical snapshots. Owned scratch is empty.
Fixed inputs, trace, response digests and scan digests remain. Do not delete output
directories to rerun one-shot collection. Rerender figures in a copy to retain seals.

V69 mutable entry documents were preserved before edits under
artifacts/study_v70/previous_snapshot/. Current evidence manifest and verified
historical redirect chain: artifacts/study_v71/evidence_manifest.json and
seal_verification.json. Preserve matching snapshots before future entry-doc edits.

## Costs and current limits

203 new physical trials: 3 feasibility + 200 classical (155 search, 45 confirmation).
20.3 million checked timed reads, 2.03 million warmup reads, 26,607,616 scan records
and 13,303,808 load writes. V70 collection 3.145 s; V71 180.110 s; combined worker
process time 181.471 s. Peak sampled worker RSS 342,458,368 bytes, not a hard cap.
Archive hashing/cleanup, setup and validation are actual collection overhead.
Timed objective includes Python, timer instrumentation, exact bytes and hashing.
Full suite 505 passed in 2.73 s; native synthetic fixtures are separate from results.

No new downloads or LLM calls. Historical recorded-table acquisitions remain
26358; 200 new LIVE physical objective charges are recorded separately. Cumulative
model requests remain 1981. Persistent downloads 4800270357 bytes; remaining
568438763 bytes under 5 GiB. External spend USD0; electricity, hardware and human/
agent time unknown. No production deployment cost or controller/model latency claim.
Full ledger: artifacts/study_v71/resource_ledger.json.

V65's five-call allowance remains exhausted; V70/V71 grant zero new inference.
V67 DuckDB/GNU-sort/OpenJPEG failed grids remain closed. V69 invalid timings must
not be repaired or silently pooled. No paid service, remote publication or contact.

