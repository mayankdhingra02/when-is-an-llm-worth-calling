# STATUS — V70/V71 corrected live classical study completed

## Resume here

The active goal remains credible research on cost/reliability-aware LLM escalation
suitable for journal review. It is NOT achieved; Q2 readiness remains unproven.
The previous goal turn made progress: 203 valid physical trials and a new confirmed
classical result. No experiment, model server or background task is currently running.

Report: reports/rocksdb_v70_v71.md. Readiness gaps: reports/readiness_v71.md.
All 505 tests passed. Read-only verification reproduced every setting check,
response/full-scan digest, 155 search decisions, 45 confirmation charges and budgets.

## Latest actual results

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

## Single next action

Implement and freeze a bounded exploratory paired LOCAL-MODEL experiment from ALL
five saved V71 prefixes, with legal-vector generation, 7 search + 3 confirmation
continuation, newly measured RF and cheap domain-prior controls under the same
model-resident hardware conditions. Do not select only weak RF seeds, retune on
these results or call this held-out. A cache-size prior may explain an apparent
LLM gain; include that control prospectively. Prepare the concrete code/protocol
and request count before any required inference-scope approval. Existing inference
allowance is not silently renewed. No new model download should be necessary.

Still untested: real constrained grammar/model selection, paired LLM gain here,
multiple independently admitted families, development-trained benefit-aware router,
untouched system-level evaluation and latest clean-machine reproduction. Keep the
full goal active; test counts and classical gains do not prove completion.
