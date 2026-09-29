# V150/V152: actual native Memcached correctness and noise screening

**These are native feasibility measurements, not LLM outcomes or a B10/B20 optimization experiment.** All four configurations and all intended probes appear in each workload. Synthetic tests are excluded. Longer-workload V152 was frozen after observing V150 noise; it is a declared exploratory amendment, with both costs/results retained.

Memcached1.6.45 came from the [official release page](https://www.memcached.org/downloads), archive SHA256d362c64e6d8d5287153501eabf7c85b4a761432fbf53f5d7b085d0bb1653c1dd and matching owner SHA1. Static libevent2.1.13-stable came from the [owner release linked by libevent.org](https://libevent.org/), SHA256f7e9383b8c0baa81b687e5b5eecc01beefaf1b19b64151d95ed61647fe7a315c. Both BSD3-clause licenses, additional libevent notices, build instructions and receipts were inspected/preserved. No system-wide install. Initial defaultSDK build failed; process-local matching Xcode15.5SDK repaired it without system changes.

Four local C clients alternate GET/SET in32request pipelines, with exact response-byte validation.1024keys have1024-byte deterministic values, no expiry;64MiB cache. Final independent server stats require no misses/evictions and exact command/item counts. Each probe starts a fresh loopback-only server with UDPoff, and reaps it. Same client/server host means measured elapsed time includes client work, validation, socket I/O and scheduling. It is not isolated server speed.

| Version / operations per probe | Threads | Requests/event | Correct /5 | Median seconds | MAD/median | Pass1%noise gate |
|---|---:|---:|---:|---:|---:|---|
| V150 / 128000 | 1 | 1 | 5 | 0.301774 | 2.870% | False |
| V150 / 128000 | 1 | 20 | 5 | 0.063894 | 3.248% | False |
| V150 / 128000 | 4 | 1 | 5 | 0.236052 | 2.987% | False |
| V150 / 128000 | 4 | 20 | 5 | 0.057588 | 1.285% | False |
| V152 / 2048000 | 1 | 1 | 5 | 4.711674 | 0.188% | True |
| V152 / 2048000 | 1 | 20 | 5 | 0.946351 | 0.042% | True |
| V152 / 2048000 | 4 | 1 | 5 | 3.564113 | 0.282% | True |
| V152 / 2048000 | 4 | 20 | 5 | 0.882666 | 0.410% | True |

The unchanged screening rule requires all20correct probes, every configurationMAD/median<=1%, and median configuration contrast>=5%. Five repetitions are a screen, not a population confidence interval. Settings with larger true effects can still be distinguishable when this conservative1%gate fails; failure does not mean Memcached is unoptimizable.

V150: **gate FAIL**; 20/20correct, 20charged probes, 20.783seconds/300secondstagecap, mediancontrast80.92%. All lifecycle/correctness/reaping conditions met: True.
V152: **gate PASS**; 20/20correct, 20charged probes, 57.755seconds/300secondstagecap, mediancontrast81.27%. All lifecycle/correctness/reaping conditions met: True.

New collection is40native feasibility probes total, with no LLM requests and no recorded-table acquisitions. Each includes prefilling and every checked timed operation; do not count these as40independent systems or free reliability probes within a future20evaluation budget. Source retrieval2,436,165bytes; builds3.046seconds failed +20.045seconds repaired, plus client compilation. CPU/wall estimates are local and no dollar/energy saving is inferred.

If either gate fails, preserve the failure. No immediate optimization run follows under the failed protocol. Any later noisy-objective study must predeclare its target (single-run time vs repeated-run estimate), charge repetitions, choose a noise-appropriate practical margin and validate the selected configurations with held-out repetitions. Changing a threshold after seeing these probes cannot create a confirmatory success. This family is now explored; later work must disclose that exposure. No remote/cloud/native production deployment or independent-host replication has occurred.

Raw commands, stdout/stderr, checked-operation counts, server statistics, lifecycle/reaping records, randomized plans and charged ledgers are in results/v150_native and results/v152_native. Protocols and preprobe hash freezes are in reports/protocol_v150.md, reports/protocol_v152.md and artifacts/study_v{150,152}. No inference or service remains running after completion.
