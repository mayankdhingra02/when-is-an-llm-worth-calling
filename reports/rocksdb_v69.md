# V69/V69.1: native RocksDB feasibility and an applied-setting failure

**Actual result:** local RocksDB executed four physical configuration attempts.
Three produced complete receipts with 100,000 checked timed reads each. Two
reference receipts match the requested settings; the contrast is invalid because
the reopened database used an 8 MiB cache instead of the requested 1 MiB. The
fourth attempt completed its worker but failed serializing the result. Its objective
timing is unknown. **No optimization comparison, headroom finding or LLM benefit
is established.** The corrected binding passes real-engine tests on tiny synthetic
fixtures, and the complete Python suite passes 502 tests.

## What ran

RocksDict 0.3.27, using the owner-published CPython3.10 macOSARM64 wheel, installed
with `pip --no-index --no-deps --no-compile --target .local-runtime/rocksdb-v69`.
Wheel SHA256 `9641e13b06cacffe1ac562874bcfa2d2fd7ae0b21751b6f64fabe60b5da9a13c`
matches PyPI. No source compilation or clean-machine reproduction was performed.
Pinned package source commit `350884b4e8f30df1f155261994f97f8768b64167` identifies
rust-rocksdb `66ff53024bb6291800aa313ec5780fc1e23c9ce7` and RocksDB source
`44e95d8af5d7ec503b3f1d5754c3379ab6c29a9d`. Source version header, Cargo.lock and
the running engine LOG agree on **9.8.4**. Registry hashes and matching version
metadata do not establish a reproducible source-to-binary build.
[Owner binding](https://github.com/rocksdict/RocksDict/tree/350884b4e8f30df1f155261994f97f8768b64167),
[PyPI release](https://pypi.org/project/rocksdict/0.3.27/).

This is an explicitly scaled **YCSB-C-inspired adaptation**, not Java YCSB
replication. It uses 65,536 records, ten deterministic 100-byte fields per record,
100,000 timed read-only requests and 10,000 warmup requests. The saved trace uses
the pinned scrambled-Zipfian formula (theta0.99), but Python's seeded RNG, ordered
keys and a concatenated raw-field layout. Every returned 1,000-byte payload must
exactly match the saved expected record; missing fields, extra bytes and corruption
fail. Initial and final scans check every key, record count and content. The same
trace and expected values are used by every trial.

The declared domain has 512 distinct **nominal** vectors over cache capacity,
block size and restart interval. These are geometric study-chosen levels of real
source-exposed options, not an externally released measured configuration table.
Only two distinct requested vectors were attempted; neither all combinations'
physical validity nor 400 distinct effective configurations has been established.
The family is development-only, grouping RocksDB/LevelDB conservatively. Identifier
scan found no matches in saved result JSON/JSONL/top-level manifests; broader
exposure and pretraining contamination are not excluded.

## Preserved failures and corrected validity

V69's first reference attempt completed `execute()` but failed JSON serialization
of byte-valued SST boundary metadata. The original result was not reconstructed or
imputed. Its worker traceback and 1.101149459-second supervisor record remain.
The remaining two original schedule slots were unattempted. A separately frozen
V69.1 repair encoded byte metadata explicitly and reran the unchanged three-case
schedule. Independent source comparison verifies that worker repair changed only
serialization/imports, not workload, settings or measurement code.

| V69.1 case | Requested cache | Active cache | Verified-loop time | Audited status |
|---|---:|---:|---:|---|
| Reference 1 | 8 MiB | 8 MiB | 0.317655334 s | Settings match; data checks pass |
| Contrast | 1 MiB | 8 MiB | 0.854398500 s | **Invalid requested configuration** |
| Reference 2 | 8 MiB | 8 MiB | 0.297620083 s | Settings match; data checks pass |

These times include Python calls, timer instrumentation, exact-byte comparison and
response hashing. They are not pure native RocksDB timings. Each process loads a
new database, flushes and checks it, closes/reopens, then warms the application
cache; the OS page cache is not cleared. All jobs are short and host activity is
uncontrolled. Two reference repetitions cannot characterize noise reliably.
The apparent contrast/reference timing difference must not be advertised as
optimization opportunity for the requested settings.

The initial readback incorrectly searched both active and historical logs. It
found the requested 1 MiB capacity in the creation log, while the reopen log showed
8 MiB. The contrast therefore incorrectly received a raw `valid` flag. The separate
`results/v69_validity_audit/summary.json` **supersedes those raw flags**, preserving
the original evidence. All three response digests and full-scan digests match
independently recomputed expected hashes. Data correctness does not establish
configuration correctness.

The pinned owner constructor explains the behavior: with explicit DB options but
no column-family map, reopening retains loaded column-family options created with
its default 8 MiB cache. Passing the `default` column-family options explicitly
avoids that path. [Pinned constructor, lines189–215](https://github.com/rocksdict/RocksDict/blob/350884b4e8f30df1f155261994f97f8768b64167/src/rdict.rs#L189).

`src/escalation/rocksdb_binding_v69.py` now supplies that map and reads only the
active `LOG`. The stale-log regression test rejects the recorded failure pattern.
Native integration tests load and reopen tiny **synthetic** databases at 1, 2 and
8 MiB, check the active settings, returned data, and positive usage of the supplied
cache. Those fixtures ran in the focused test and full suite: six fixture executions,
twelve engine opens. They do not replace or repair measured performance trials.
No further performance retries were made after the V69.1 frozen limit.

## Evidence and costs

- Raw attempts: `results/v69_rocksdb_feasibility/` and
  `results/v69_1_rocksdb_feasibility/`; complete engine databases/logs/options,
  worker/supervisor receipts and schedules retained.
- Corrected audit and reproducible CSV/PNG/SVG diagnostic:
  `results/v69_validity_audit/`. The figure shows requested versus applied cache,
  not an optimization score, and was visually checked.
- Fixed inputs/trace/nominal grid: `data/generated_v69/`; runtime/binary pins:
  `configs/runtime_v69.lock.json`; owner sources: `artifacts/sources/v69/` and
  `artifacts/sources/v69_repair/`.
- Frozen protocols: `reports/protocol_v69.md` and `protocol_v69_1.md`, each with
  its source/hash freeze. Test, verification and collection ledger:
  `artifacts/study_v69/`.

Four physical attempts consumed 4.282466501 seconds of worker process time; parent
collection stages total 4.291545625 seconds. Fixed-input preparation took
6.951852500 seconds, separate from collection. Peak sampled worker RSS was
221,822,976 bytes. Three complete receipts record 196,608 load writes, 300,000
verified timed reads, 30,000 warmup reads and 393,216 full-scan records. The failed
serialization attempt's additional operation counts are inferred from its completed
code path and explicitly separated in the ledger; its objective timing remains null.
Watchdog RSS is sampled, not a hard allocation limit. Initial sandbox `ps` access
failed before any physical trial and was retried with execution permission.

Zero new model requests, optimizer acquisitions or external spend. Previous totals
remain 1,981 model requests and 26,358 recorded acquisitions. Do not confuse native
database reads or physical configuration attempts with recorded-table oracle
acquisitions. Source-download totals and remaining allowance are machine-recorded
in `resource_ledger.json`; no hardware/electricity/human cost estimate or deployment
cost claim is made. No cloud resources, remote push, publication or author contact.

Read-only replay (does not open databases or issue queries):

```
.venv/bin/python scripts/verify_rocksdb_v69.py
.venv/bin/python scripts/seal_evidence_v69.py --verify-only
```

`python -m pytest -q tests` additionally runs tiny synthetic native integration
fixtures when the optional pinned local wheel is present; otherwise those three
tests explicitly skip. Figures can be regenerated with `scripts/figure_rocksdb_v69.py`
in a copy, since image metadata may change. The original collection scripts are
one-shot and must not be rerun by deleting existing output directories.

## Next action and limits

Freeze a **new three-case feasibility stage using the corrected binding**, with
the same workload and settings, stage-scoped active log readback, attached-cache
usage assertions and atomic progress/result receipts. This is a configuration
repair, not permission to search for a favorable workload or reuse invalid timings.
Only after it passes should a budget20/checkpoint10 classical study be frozen.

Untested: corrected binding on the full measurement workload, broader effective
configuration domain, classical headroom, paired LLM continuations, held-out routing
and independent-machine replication. No new inference allowance exists. This
result prevents a misleading measurement; it does not establish Q2 readiness.
