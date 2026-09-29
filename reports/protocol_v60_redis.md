# V60 — Redis correctness and local feasibility

Frozen before application execution. This is a new development-only feasibility
stage under the user's renewed request to continue local research. Its 180-second
cap is below the existing 30-minute per-experiment default; no old runtime/call
allowance is reset. No inference, new model allowance, paid/cloud use, or reserved
MongoDB/Storm outcome access. Redis is now designated development; related old
tables, versions, workloads and seeds cannot later be called independent test groups.

Use Redis owner release 7.2.11, commit d4c381df7a729c06a5207c4f18d804febe956dc4,
built project-locally using libc and the installed macOS 15.5 SDK. Archive BSD-3
COPYING, source tar hash, commands and binary hashes. Existing user Redis 8.2.3 is
not used: its build provenance was not established. No service or system install.

Six physical invocations: field 0 and field 127, each reference/contrast/reference.
Each trial starts an empty isolated Redis server, TCP disabled, private Unix socket,
save/AOF disabled, no replication, no eviction, maxmemory256MiB, dynamic-hz off.
This utility contract is a volatile local cache, NOT a durable database service.
Populate 256 hashes ×128 fields ×64-byte deterministic field-specific values.
All keys/fields/values are checked before and after the measured read workload.
Inputs are generated application workloads; actual server timings are measurements,
not mock LLM results. They do not represent production workload sampling.

Fixed C benchmark client: 50 connections, pipeline16, one client thread, random
keys in [0,255], seed60000. Commands HGET field f000 or f127. Fixed warmup10000
requests and measured100000 requests. The pinned owner's C client is adapted to
reject every non-prefix reply unless its type/length/bytes equal the declared
expected value. Save the exact source patch, original source, adapted binary hash,
all benchmark logs and actual counted replies. No repair or failed-query exclusion.
Up to800 pipeline-overhang completions are allowed, recorded and not hidden.

Reference: hash-max-listpack-entries512, value64, io-threads1, reads=no, hz10,
activerehashing=yes. Contrast: entries64, value32, threads4, reads=yes, hz100,
activerehashing=no. These intentionally bundled contrasts are implementation
feasibility probes, NOT isolated factor-effect experiments or optimizer outcomes.
Neither config is selected based on timing. Include all six results/failures.

Objective receipt: measured benchmark-process wall milliseconds, including client
startup and reply checks, not pure server execution. Retain owner throughput and
latency output separately. Every full invocation and warmup is research cost;
no comparison of three-repeat optimizer medians is made in this stage. No p-values,
LLM benefit, held-out generalization or journal-readiness claim.

Hard parent watchdog40s/trial; stage180s, no launch after135s. Monitor process-group
RSS1GiB; server memory cap is additional. Unexpected failure stops remaining trials;
retain intended and unattempted denominator. No automatic retries or parameter
changes. Parent kills its worker/server/client process group on breach. Each normal
trial terminates its own server; no indefinite service remains.

Archive V59 mutable docs before updates; verify original V59 seal using snapshots.
Before any larger collection, audit repeatability and the real deployable baseline,
freeze the candidate grid/workload/group split/selection protocol and limits. This
feasibility design has zero optimizer arms and zero model requests. It is not a
SNAP2 reproduction or a reinterpretation of the unresolved legacy Redis table.
