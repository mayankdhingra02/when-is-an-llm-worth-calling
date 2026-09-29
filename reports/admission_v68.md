# V68: larger external benchmark audit and strict YCSB validation

**Executed result:** one published tuning-data artifact and two owner workload
harnesses audited at pinned commits; no new measured dataset admitted. A strict
validator for a future read-only YCSB-C adaptation is implemented. All 484 Python
tests pass, including 36 new synthetic tests. This is completed infrastructure
and source verification, not a new optimization-performance result.

The admission protocol was frozen before candidate data retrieval. It requires
at least 400 distinct configurations within a fixed utility contract, so a
20-evaluation budget samples at most 5%. That criterion addresses V67's 20/48
coverage; it is not a claim that larger domains will favor an LLM. No performance
rows were downloaded, converted, ranked or used for candidate selection in V68.

## Published tuning data: not yet suitable for this study

The owner connects KnobsTuningEA to Xinyi Zhang, Zhuo Chang, Yang Li, Hong Wu,
Jian Tan, Feifei Li and Bin Cui, *Facilitating Database Tuning with Hyper-Parameter
Optimization: A Comprehensive Experimental Evaluation*, arXiv:2110.12654v4,
14 March 2022. The paper's abstract explicitly describes a surrogate benchmark.
[Paper metadata](https://arxiv.org/abs/2110.12654v4).

Pinned artifact: `PKU-DAIR/KnobsTuningEA`, commit
`13290f8dcef965a62820c41b74af097b93dd54a5`. The complete tree has 205 files;
15 training-data paths were inventoried by name and size only. Its README
identifies MySQL 5.7.19/Linux 4.9 and external Sysbench, OLTP-Bench and JOB
workloads. The unranked domain file contains 197 knobs. These are not 197
independent systems; all MySQL workloads must remain in one family.
[Owner README](https://github.com/PKU-DAIR/KnobsTuningEA/blob/13290f8dcef965a62820c41b74af097b93dd54a5/README.md).

The following source-level findings prevent admission now:

- No reuse license was found in the complete tree or inspected setup metadata.
  Public visibility is not a license for redistribution. No code from this
  artifact was imported/executed or incorporated into our runner.
- The declared domain varies `innodb_doublewrite`,
  `innodb_flush_log_at_trx_commit`, and `sync_binlog`; fixed durability/integrity
  semantics have not been established across records. We did not claim that
  all knob combinations are legal or count a Cartesian product as measured rows.
- `parse_sysbench` matches error/reconnect rates but computes its returned vector
  only from interval columns 0, 1 and 5 (TPS, QPS, latency). The Python AST audit
  confirms this. We have not linked complete raw attempts and failures to the
  released training rows. Missing denominator evidence is not evidence of zero
  failures. [Parser](https://github.com/PKU-DAIR/KnobsTuningEA/blob/13290f8dcef965a62820c41b74af097b93dd54a5/autotune/utils/parser.py).
- `step_GP` uses penalty vectors on some application failures. Those constants
  must not be reported as measured latency. Its benchmark alternative calls a
  loaded model's `predict`; those outputs are simulated objectives, not acquired
  application measurements. [Measurement path](https://github.com/PKU-DAIR/KnobsTuningEA/blob/13290f8dcef965a62820c41b74af097b93dd54a5/autotune/dbenv.py),
  [surrogate path](https://github.com/PKU-DAIR/KnobsTuningEA/blob/13290f8dcef965a62820c41b74af097b93dd54a5/autotune/dbenv_bench.py).

These are restrictions of our proposed reliability study, not findings that the
original paper is invalid. The 400-configuration gate was **not evaluated**, since
the prerequisite audit failed. The old MySQL 5.7 manual URL now redirects to a
newer version; it was not used as a version-exact provenance certificate.

## Reusable workload source and a concrete validation gap

YCSB 0.17.0 is pinned to
`4b19340e3bab5e4c88eda75ad56e83dc4d5cc503`, Apache-2.0. Workload C specifies
read-only, Zipfian requests. CoreWorkload defaults `dataintegrity` to false;
enabling it requires constant field length. Its verifier checks each returned
field against a deterministic expected value and rejects an empty result, but
does not compare the returned field set with the requested set. Consequently,
a nonempty correct subset can pass that check. This is a source-level observation,
not an observed database corruption or a claim about later YCSB versions.
[Pinned CoreWorkload](https://github.com/brianfrankcooper/YCSB/blob/4b19340e3bab5e4c88eda75ad56e83dc4d5cc503/core/src/main/java/site/ycsb/workloads/CoreWorkload.java).

`src/escalation/ycsb_contract_v68.py` now provides explicit read-only property
checks, exact field-set/value validation, complete ordered-key snapshot validation,
and an objective-blind status parser. It rejects missing/duplicate/out-of-range
records, bad field contents, unsuccessful process exits/timeouts, absent or
inconsistent READ/VERIFY denominators and positive non-OK/unexpected-operation
counters. Throughput and latency strings are never converted by the status parser.
The deterministic payload recipe is attributed to the Apache-licensed upstream.

**Limits:** only synthetic fixtures have exercised this adapter. A final database
snapshot does not certify every timed response; integrate the strict field check
at the actual read boundary too. A read-only task does not establish crash
durability or update correctness. Snapshot/export queries and validation overhead
must be recorded as actual collection cost. Backend defaults, runtime, option
domain and applied-setting readback are not yet pinned or tested. In particular,
the old RocksDB binding exposes a directory property and hard-codes options; it
is not already a ready-to-tune 400-setting benchmark.

BenchBase at `33c00473807ebd49304d114a6d769d2d2b2bbb34` is also Apache-2.0.
The inspected YCSB ReadRecord procedure reads fields without an expected-value
comparison. Its POM targets Java 23. Our existing project-local Java 17 artifact
is a **JRE**, not a JDK/compiler (the initial machine audit label says JDK; this
terminology correction is recorded in clarifications.json). No compatibility
build was attempted. Neither harness is itself a recorded tuning-response table.
[Read procedure](https://github.com/cmu-db/benchbase/blob/33c00473807ebd49304d114a6d769d2d2b2bbb34/src/main/java/com/oltpbenchmark/benchmarks/ycsb/procedures/ReadRecord.java),
[POM](https://github.com/cmu-db/benchbase/blob/33c00473807ebd49304d114a6d769d2d2b2bbb34/pom.xml).

## Execution, costs and reproducibility

The executable audit verifies 38 persisted source bodies and pins from three
complete owner trees (205, 461 and 978 files). Source bytes: 917,117, within the
10 MiB stage cap. One sandbox DNS failure was recorded and the request retried
with execution approval. No downloaded script, pickle or surrogate was run.
An initial synthetic test had an incorrect hand-calculated Java hash; the
arithmetic fixture was corrected, then all 484 tests passed. Production algorithm
and collected data were not changed by that test correction.

Raw source manifests: `artifacts/sources/v68/`; audit:
`results/v68_admission/summary.json`; logs/ledger/verifiers:
`artifacts/study_v68/`. No figure is appropriate for a three-artifact eligibility
table. V67's actual experiment figures remain available and unchanged.

```
.venv/bin/python scripts/verify_admission_v68.py
.venv/bin/python -m pytest -q tests
.venv/bin/python scripts/seal_evidence_v68.py --verify-only
```

Zero new physical trials, objective acquisitions, model requests or paid spending.
Cumulative counts stay at 26,358 recorded acquisitions and 1,981 model requests.
Downloads become 4,796,326,797 bytes, leaving 572,382,323 under 5 GiB. Electricity,
human/agent time and hardware cost remain unknown; no deployment cost was measured.
The audit's small runtime is not the time needed to run these benchmarks.

## Next action

Build a bounded **YCSB-C / RocksDB feasibility adaptation**, after checking family
exposure and pinning a native ARM64 runtime and a configurable binding. Preserve
the owner workload definition; freeze record/request scale, correctness checks,
legal option domains, memory/time limits and failure accounting before timings.
Require applied-setting readback and at least 400 legal configurations without
varying the workload or durability contract. Run correctness/resource feasibility
before a 20-evaluation classical screen; do not enumerate a huge full grid just
to obtain its hidden optimum. Treat RocksDB/LevelDB lineage as one family until
independence is justified. This is development admission, not a held-out claim.

No new LLM allowance exists, and old failed grids remain closed. The real grammar
adapter, new database runs, independent-machine replication and held-out routing
benefit are still untested. Journal readiness remains unestablished.
