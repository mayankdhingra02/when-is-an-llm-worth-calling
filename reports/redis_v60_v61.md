# V60/V61 — correctness-checked Redis development result

**The preselected RF-LCB continuation reaches the recorded minimum in 9/10 cases;
its largest remaining gap is 0.068%. Neither workload passes the frozen opportunity
gate. No LLM calls are justified on this grid under this protocol.** This extends
the classical evidence to a new software family; it is not a new model experiment,
independent-family router validation, equivalence proof, or journal-readiness claim.

## What actually ran

Six feasibility invocations passed, followed by all 480 intended grid invocations,
all valid with no retries, resource failures or unattempted cases. Physical grid
collection took 157.102360 seconds under its 900-second cap. Two generated
read workloads, 80 configurations each, three repetitions; all belong to Redis.
Thirty classical arms ran with five fixed seeds, saved shared prefixes of 10,
20 inclusive outcomes per arm, and 400 charged recorded aggregate accesses.
Offline selection took 2.803851 seconds. Primary RF-LCB was specified
before grid timings; random and 3NN are reported controls. Full-table scoring came
only after all decisions. The portfolio is diagnostic only and not the primary gate.

| Workload | Best median ms | Median CV | Threshold | RF exact minimum | Max RF headroom | Gate cases |
|---|---:|---:|---:|---:|---:|---:|
| hget_0 | 39.483 | 2.942% | 5.883% | 5/5 | 0.000% | 0/5 |
| hget_127 | 39.663 | 1.755% | 5.000% | 4/5 | 0.068% | 0/5 |

![Preselected comparator](../results/v61_redis_screen/headroom.png)

## Correctness, provenance and costs

Redis 7.2.11 was compiled from owner commit
`d4c381df7a729c06a5207c4f18d804febe956dc4`, with project-local binaries, libc,
and the installed macOS 15.5 SDK. The source tarball and all binary hashes are
saved. The existing user Redis 8.2.3 was queried for its version only, not used.
[Owner release README](https://github.com/redis/redis/blob/d4c381df7a729c06a5207c4f18d804febe956dc4/README.md)
and [COPYING](https://github.com/redis/redis/blob/d4c381df7a729c06a5207c4f18d804febe956dc4/COPYING)
provide build and BSD-3 source-license evidence. No system service was installed.

The volatile-cache contract fixes persistence off, no replication, no eviction,
private Unix sockets, and a 256 MiB server memory ceiling. It does not represent
a durable database service. Each trial loads 256 hashes with 128 field-specific
64-byte values; complete contents are checked before and after execution. The
owner C benchmark is adapted to validate every non-prefix reply before counting it.
All 53,460,000 benchmark replies (including warmups) passed.
Original C source, exact patch, adapted binary, request counts and logs are retained.
Four separate synthetic native-client fixtures accept correct bytes and reject
wrong bytes, nil and wrong types with exit42; none enters research aggregates.

The client uses 50 connections and pipeline16, avoiding the simple synchronous
single-client measurement problem described in [Redis benchmark guidance](https://redis.io/docs/latest/operate/oss_and_stack/management/optimization/benchmarks/).
Nevertheless results describe this client/server/Unix-socket setup. They are not
production throughput or server-only time. Fixed warmup10000 and measured100000
requests per trial; V61 times process exit with a dedicated waiter, including client
startup and reply validation. V60 used Python timeout waiting, which can quantize
short runtimes; its feasibility timings are not pooled into V61 medians.

Actual new research cost is 486 physical server invocations, 400 recorded accesses,
all warmups, data loading and correctness checks. Full-grid table collection is
research overhead. A hypothetical deployed 20-outcome arm would require 60 physical
trials under the median-of-three recipe, plus setup/admission cost. No new model
requests or external spend; hardware, electricity and agent/user costs are unknown.
Peak sampled worker/server/client RSS was 44,482,560 bytes.
The RSS watchdog is sampled, not a hard OS bound; Redis's memory option does not
cap all process overhead. All dedicated servers were shut down with exit0.

## Verification and limits

Independent replay checked all frozen hashes, 486 physical receipts, known-answer
data hashes, every recorded benchmark count, configurations, timing derivation,
400 source labels, 30 arm budgets/prefixes, and 360 reconstructed classical choices.
All 393 Python tests pass. The figure was visually reviewed. Native-client synthetic
controls are stored separately under artifacts/synthetic_v61_reply_guard/.

One new software family, two generated HGET workloads, one host, tiny in-memory
working set, client overhead, three repetitions and noisy recorded minima limit
external validity. Parameter settings may share execution mechanisms; the 80 rows
are not 80 independent mechanisms. No formal significance or equivalence claim.
These short read workloads do not establish results for durable writes, large
working sets, other request mixes, networks or models. Redis is now development;
all related versions/tasks/seeds must remain grouped in future splits.

An identifier audit scanned 5,556 saved research JSON/JSONL/manifests (78,536,465
bytes). Matches were confined to admission/manifests and new Redis feasibility;
no unexplained historical matches. This is not proof of untouched outcomes: deleted,
external, unidentified-alias and unstructured records remain blind spots. Original
MongoDB/Storm tables remain reserved and semantically unadmitted.

## Reproduction and next decision

Raw logs and full denominators: results/v60_redis_feasibility/ and
results/v61_redis_physical/. Tables/prefixes/arms/journals/CSV/figures:
results/v61_redis_screen/. Build/source/verification receipts: artifacts/study_v60/
and artifacts/study_v61/. Frozen protocols and executable source are retained.

```sh
.venv/bin/python scripts/verify_redis_v61.py
.venv/bin/python scripts/report_redis_v61.py
.venv/bin/python -m pytest -q tests
```

Collectors and primary analysis are one-shot; do not delete to rerun or retune this
exposed grid. The next independent-family design should target application decisions
with materially expensive outcomes and a fixed correctness contract. Passing that
screen would still not prove model benefit. Any fresh LLM allowance requires a
concrete bounded protocol; existing cumulative request count remains 1,976.
