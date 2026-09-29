# V69: native RocksDB / YCSB-C feasibility adaptation

Frozen before physical trials. Development only, RocksDB/LevelDB treated as one
related family. Identifier audit found no matches in saved result JSON/JSONL and
top-level manifests; this is not a certificate against all historical exposure.

Use rocksdict0.3.27 CPython3.10 macOSARM64 wheel, PyPI SHA256 verified, installed
without dependencies in .local-runtime/rocksdb-v69. Owner release350884b4e8f30df1f155261994f97f8768b64167,
rust-rocksdb66ff53024bb6291800aa313ec5780fc1e23c9ce7, embedded RocksDB source
44e95d8af5d7ec503b3f1d5754c3379ab6c29a9d (9.8.4). Registry binary provenance is
verified; reproducible source-to-binary build is not established. No Java runtime,
compiler installation, model download or systemwide modification.

YCSB-C inspiration: read-only scrambled-Zipfian requests (theta.99, owner formula
and constants), ten100-byte deterministic ASCII fields per record. Differences:
Python seeded RNG, saved trace, ordered userN keys, fixed concatenated-field raw
encoding, Python binding, single client, scaled65536records and100000timedreads.
This is an adaptation, NOT an execution or numerical replication of YCSB Java.
Seed69001; same110000request IDs for every configuration, first10000warmup.
The Java constructor's extra draw and inclusive Zipfian range are documented.

Nominal512configuration domain: cacheMiB[1,2,4,8,16,32,64,128] x
blockbytes[512,1024,2048,4096,8192,16384,32768,65536] x
blockrestartinterval[1,2,4,8,16,32,64,128]. Source-exposed options; geometric levels
are study defaults, not an upstream benchmark configuration catalogue. Distinct
feature vectors do not prove distinct physical effects or all combinations valid.
Only the sampled settings are physically validated here; do not claim400validated
configurations or successful admission to a learned-router study from this stage.

Three intended trials in order: reference(8MiB,4096,16), contrast(1MiB,65536,1),
reference again. No outcome-led resizing, extra seeds, alternative settings or
optimization. Stop remaining trials on failure; preserve intended denominator.
No automatic retry. New instrumentation repair must be separately versioned and
must not change settings/workload; original failed attempt remains in costs.

Each trial uses a fresh DB, compressionnone,8MiBwritebuffer,2backgroundjobs,
unchanged WAL semantics. Insert every record, flush/WALsync, full exact scan,
close/reopen with a new application cache,10000warmupGet calls,100000timedGet
calls, full exact final scan. No OS page-cache clearing; OS-warm application-cache
recipe, not cold-disk production. No assertion of update or crash durability.

Every Get payload must exactly equal the independent saved1000-byte expected
record, including length. Engine-generated OPTIONS/LOG must confirm block size,
restart interval and cache capacity. Full scans check every key/content/count and
matching initial/final digest. Save engine OPTIONS/LOG/SSTs, input manifests,
request trace, result/supervisor records and aggregate timed-response digest.

Primary descriptive timing is full verified read-loop wall time: Python binding,
per-read timer instrumentation, exact-byte validation and response hashing included.
Sum of timed Get calls is diagnostic, NOT pure native engine time. Load, warmup,
full scans and total worker/parent wall time are separate actual collection costs.
No comparison to old generated-system timings, no optimizer regret/global optimum,
and no deployment extrapolation from this feasibility stage.

Caps:10MiBsource bodies inside remaining572382323bytes; preparation180s;
600scollection stage,120s/trial,oneworker,2GiBsampledRSSwatchdog; no indefinitejobs.
Fixed data/trace sizes and at most3DBs bound expected scratch; disk headroom checked
before collection. Zero LLM requests or optimizer acquisitions; all physical
attempts/validation accesses recorded. No new inference allowance is granted.
