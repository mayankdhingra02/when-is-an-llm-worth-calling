# STATUS — V68 external benchmark admission completed

## Resume here

V68 audited larger published database-tuning artifacts before reading objectives.
**No new measured dataset was admitted.** It implemented a strict YCSB-C validation
component and executed all **484 tests**, including36new synthetic tests.
This is source/infrastructure progress, not a new optimization-performance result.
Report: reports/admission_v68.md. Decisions:results/v68_admission/summary.json.

The latest physical result remains V66/V67:441validconfiguration trials on DuckDB,
GNU sort and OpenJPEG;45classicalarms/600recordedaccesses. RF and3NN both reached
the recorded minimum15/15. All frozen opportunity gates failed; do not tune or
spend LLM calls on those grids. Report:reports/candidates_v66_v67.md.
Latest real-model result remains V65:five SmolLM3-3B calls,0contract-valid outputs,
5RF fallbacks,zero LLM-attributable gain. Its5/5allowance is exhausted.

## V68 concrete findings

- KnobsTuningEA owner commit13290f8dcef965a62820c41b74af097b93dd54a5:
  197declaredknobs;15training-data paths inventoried by name/size only. No license
  found in complete205-filetree/inspectedsetup. Durability-sensitive settings vary;
  Sysbench parser omits matched error/reconnect rates from returned metrics;
  raw-attempt/failure-denominator mapping unresolved. Surrogate execution calls
  model.predict and must not become physical measurements. No outcome tables fetched.
- YCSB0.17.0 commit4b19340e3bab5e4c88eda75ad56e83dc4d5cc503, Apache2:
  usable workload source. Integrity disabled by default; enabled verifier checks
  returned fields but not completeness of requested field set. New Python validator
  rejects missing/extra/corrupt fields, missing/duplicate/out-of-range records and
  failed/incomplete READ/VERIFY status counts. Only synthetic tests; no database run.
- BenchBase commit33c00473807ebd49304d114a6d769d2d2b2bbb34, Apache2:
  inspected ReadRecord copies fields without expected-value comparison; POM targets
  Java23. Existing local Java17 artifact is a JRE, not compiler/JDK. Audit JSON's
  initial JDK terminology is corrected in artifacts/study_v68/clarifications.json.
- Three complete trees205/461/978files;38sourcebodies verified. Workload names and
  benchmark frameworks are not independent systems or measured datasets.

The prospective400-configuration/5%-budget-fraction gate was not evaluated because
prerequisites failed. No claim all197-knob combinations are legal. Findings do not
invalidate the original paper or prove missing artifacts cannot exist elsewhere.

## Reproduce and inspect

```
.venv/bin/python scripts/verify_admission_v68.py
.venv/bin/python -m pytest -q tests
.venv/bin/python scripts/seal_evidence_v68.py --verify-only
```

Protocol frozen before source/data audit:reports/protocol_v68_admission.md and
.freeze.json. Executable audit is one-shot; use verifier to replay. Owner metadata
and source bytes:artifacts/sources/v68/. Source manifests include retrieval failure.
New code:src/escalation/ycsb_contract_v68.py;tests/synthetic/test_ycsb_contract_v68.py.
Audit/verification/test logs and resource ledger:artifacts/study_v68/.
No new scientific plot:eligibility findings are categorical. V67figures unchanged.

One initial DNS failure recovered through approved network execution. One synthetic
fixture initially had wrong hand-computed hash arithmetic; corrected and retested.
Later linear-time hash implementation checked against independent polynomial hash
reference. Final484tests passed. All synthetic outputs stay outside measured results.
No downloaded scripts, Java classes, database, model or surrogate were executed.

## Costs and preservation

V68:0physicaltrials,0objectiveaccesses,0modelrequests,USD0externalspend.
917,117newpersistedsourcebytes; cumulative4,796,326,797;572,382,323bytesremaining
under5GiB. Counts unchanged:26,358recordedacquisitions and1,981modelrequests.
Network accounting covers persisted bodies, not web-tool traffic/TLS overhead.
Hardware/electricity/human/agent cost unknown. No deployment cost measured here.
Full ledger:artifacts/study_v68/resource_ledger.json.

V67entry documents preserved byte-for-byte before edits under
artifacts/study_v68/previous_snapshot/. Current seal:
artifacts/study_v68/evidence_manifest.json; verification receipt beside it.
This verifier resolves V67/V65/V59/V58 historical snapshots; old seal tools alone
cannot verify current mutable entry documents. Preserve matching snapshots before
future edits. Old raw evidence remains untouched. No commit/push/publication/contact.

## Single next action

Pin and build a bounded native-ARM64 **YCSB-C/RocksDB feasibility adaptation**.
First check RocksDB/LevelDB family exposure, then choose a configurable binding and
runtime:the inspected old YCSB binding exposes a directory and hard-codes options,
so it is NOT ready to tune. Preserve the owner read-only Zipfian workload; freeze
scale, at least400legalconfigurations, applied-setting readback, exact complete-field
checks, and memory/time limits before timings. Use development classification.
A final snapshot alone does not validate every timed response. Count validation
queries and startup/load separately in actual collection. Do not enumerate a giant
full grid simply to obtain an optimum. See reports/next_experiment.md.

No inference allowance renewed. New model study requires a concrete frozen scope
and new numerical allowance after eligible tasks, within resource permissions.
Untested:real database binding/validator integration, real grammar sampling, larger
irregular-domain optimization, independent-machine replication, held-out router
benefit. Q2-readiness remains unestablished. No background job or automatic task.
