# V74 — fresh Kanzi correctness/resource feasibility

Prospective development admission, frozen before the first application trial.
This is a locally compiled owner-source adaptation, not reproduction of ICSE
archived timings. Kanzi 1.9.0 commit 9828b05815b754f1ae40acd83552605885ba515b
is Apache-2.0. All 113 extracted Git blobs match the owner's tree. The compiler
is Eclipse ECJ 3.32.0 (EPL-2.0), Maven artifact and SHA1 verified, SHA256 pinned.
Java 11 target follows owner Ant build; existing Temurin 17 ARM64 runs it.
No upstream install/build scripts are executed. Source/archive details are in
artifacts/sources/v74/manifest.json; build warnings and command are preserved.

## Fixed input and scope

One deterministic 16 MiB input contains four equal sections: generated records,
repeated text, structured binary records, and SHA256-derived high-entropy bytes.
The generator and exact input hash are frozen. This artificial feasibility
workload is not a production corpus, but all collected timings are real native
executions. It is separate from synthetic unit-test outputs. No task/setting was
selected using archived hidden timings. Manifest exposure search is limited to
28 top-level data manifests (no Kanzi text matches); this does not establish
untouched status. Kanzi and all future variants belong to ONE development family.

Run exactly reference / contrast / reference, sequentially:

| Setting | Transform | Entropy | Block bytes | Jobs |
| --- | --- | --- | ---: | ---: |
| Reference | LZ+RLT | HUFFMAN | 1048576 | 1 |
| Contrast | BWT+RANK+ZRLT | ANS0 | 65536 | 4 |

Enable stream checksum in all compressions. Do not use level presets, skip
incompressible blocks, or overwrite flags. Charge each trial before launching.
Each trial includes compression, decompression, and full byte-exact equality.
The denominator is three intended trials, even after failure or stage exhaustion.
There are no retries, repairs, optimizer calls, warmups, or LLM requests in scope.

## Validation and bounds

Before decompression, parse the output stream's first 128 bits independently to
verify magic, version, checksum flag, entropy, transform order and block size.
Verify verbose applied-option receipts including jobs (not encoded in header).
Require exit zero, no watchdog termination, no ignored-option warning and exact
decompressed bytes. Preserve inputs, compressed and decompressed output hashes,
logs, commands, settings, charges, process exit codes and failures.

Each JVM: heap 768 MiB, ActiveProcessorCount 4; 120 s process wall limit, sampled
2 GiB process-group RSS limit, sampled 128 MiB trial-directory files limit.
Watchdog polling 0.1 s is not a hard memory/filesystem quota. Stage cap 600 s;
start a new trial only within 330 s, reserving 240 s process time and 30 s checks.
Environment removes Java option/classpath injection. One active experiment.
Permission preflight runs before creating outputs or charging any trial.

Record compression/decompression process wall time, compressed bytes, ratio,
sampled resource maxima, byte-verification time and total stage wall time.
Cold JVM startup, JIT and logging overhead are included. Filesystem caches are
not cleared. Reference repetition is descriptive only: three trials cannot
estimate stable performance distributions or prove a useful optimization domain.
No hypothesis test, learned router, practical benefit margin or utility function
is fitted here. Do not infer an LLM advantage from native feasibility.

## Costs and continuation

Zero new model requests and external spending. At most three physical trials /
six application processes; no per-arm optimization budget yet. Count source and
compiler downloads within V74's 32 MiB stage and global remaining allowance.
Keep collection cost separate from deployment estimates (none produced here).
Stop on failure, preserve the failure, and require a versioned repair protocol.
If valid, next freeze a source-supported domain and workload utility before any
classical search. At least 400 effective settings must be justified, not inferred
from an unvalidated Cartesian count. This stage does not authorize a model batch.

Execution: `.venv/bin/python scripts/run_kanzi_v74.py` once, in a prepared copy.
Freeze includes runtime, workload, collector, validation, imported helpers and
this protocol. Unit tests run before measurements; fixture data are excluded.
