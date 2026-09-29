# V74: Kanzi local feasibility passed

All three prospectively fixed trials completed with applied-setting receipts,
checksum enabled and exact byte equality after decompression. No failures,
retries, model calls or external spending. This admits local correctness/resource
feasibility only; it does not admit a full optimization domain or show LLM benefit.

| Trial | Compression seconds | Decompression seconds | Compressed bytes | Input ratio |
| --- | ---: | ---: | ---: | ---: |
| Reference 1 | 0.252776 | 0.142730 | 6,502,417 | 0.387574 |
| Contrast | 0.597935 | 0.272547 | 7,052,949 | 0.420389 |
| Reference 2 | 0.230801 | 0.142168 | 6,502,417 | 0.387574 |

These are single process observations, not stable performance estimates. Reference
compression outputs have identical SHA256 hashes. The contrast was slower and
larger on this generated workload; it changes several settings simultaneously,
so no individual-setting causal effect is identifiable. Do not select a new
workload or contrast to reverse this outcome. Peak sampled process-group RSS was
225,656,832 bytes (~215.2 MiB); sampling can miss instantaneous peaks.
The three-trial stage took 1.721417 seconds, including checks and monitoring.
Cold JVM startup/JIT/logging are included in process times; filesystem caches
were not cleared. No warmup, precision test or independent machine repeat ran.

## Provenance and scope

Owner [Kanzi 1.9.0](https://github.com/flanglet/kanzi/releases/tag/1.9.0), pinned
commit `9828b05815b754f1ae40acd83552605885ba515b`, was built locally from 88 Java
sources. All 113 extracted Git blobs match the owner's tree. Apache-2.0 owner
license is preserved in source and JAR. Eclipse ECJ 3.32.0 from Maven Central is
EPL-2.0; registry SHA1 and local SHA256 are recorded. Java 11 compilation target
follows owner Ant settings; the existing local Temurin 17 ARM64 runtime executes
the build. This is an adaptation, not the original ICSE benchmark artifact.

Initial build: 1.060934 seconds, exit zero with 24 warnings. A separate local
rebuild took 0.839324 seconds and produced the identical JAR SHA256
`b1585d7dd7fe118bcdf27844ce6bad37c808d28177a35eb7de98379f50aa397c`.
This verifies same-host rebuild determinism, not clean-machine reproducibility.

Input is deterministic generated 16 MiB data, including repetitive and
high-entropy sections, SHA256
`0e7fb683728be3849a18aae111f0649d589395575b5acddb8bbab46ecaf60ed4`.
Timings are actual executions; the input is artificial and cannot establish
production performance. It is not a synthetic test fixture or a model response.
No archived objective rows were read. Searching 28 top-level project data
manifests found no Kanzi string matches, but aliases and pretraining remain
unresolved. All Kanzi workloads/versions are one development family, never
independent held-out systems.

## Evidence and validation

- Protocol and prospective hashes: `reports/protocol_v74.md` and `.freeze.json`.
- Raw commands, charges, logs, all compressed/decoded files and receipts:
  `results/v74_kanzi_feasibility/` (three trials, six processes).
- Replayed JSON/CSV and inspected PNG/SVG: `results/v74_kanzi_analysis/`.
- Source provenance, runtime pins, generated input manifest: `artifacts/sources/v74/`,
  `configs/runtime_v74.lock.json`, `data/generated_v74/manifest.json`.
- Builds, exposure audit, costs and test output: `artifacts/study_v74/`.

Before collection, 510 synthetic tests passed in 3.45 seconds. After collection,
explicit `pytest -q tests` also included existing integration/other directories:
537 passed in 3.70 seconds. The default pytest testpaths excludes those 27 tests;
use the explicit command. Synthetic/test outputs are excluded from research data.
The sandbox initially denied process monitoring before any application launched;
the identical frozen command then ran with permission. This was not a trial retry.
The offline replay rechecks hashes, regeneration, exact byte equality, headers,
receipts, caps, three charges and all successful outputs; it launches no Kanzi.

```
.venv/bin/python -m pytest -q tests
.venv/bin/python scripts/analyze_kanzi_v74.py
.venv/bin/python scripts/seal_evidence_v74.py --verify-only
```

Rebuild into an unused project-local directory:
`.venv/bin/python scripts/rebuild_kanzi_v74.py --output-dir artifacts/kanzi_rebuild_new`
Saved verified sources/compiler/runtime are prerequisites. Do not rerun the
one-shot measurement collector over existing outputs; use a separate prepared
copy and preserve any new measurements as separate evidence.

## Cost and next action

New persisted downloads: 3,429,761 bytes, including compiler and source bodies;
cumulative 4,806,613,863, leaving 562,095,257 under 5 GiB. Network headers/error
traffic are not included. Six native application processes / three feasibility
trials are additional collection cost, not paired optimizer evaluations. Builds,
tests and offline replay are recorded separately. Cumulative model requests stay
2016; recorded-table acquisitions stay 26358. No deployment estimate is inferred;
electricity/hardware/human/agent cost is unknown. External experiment spend is $0.

Next: freeze a source-supported, sufficiently large effective configuration
domain and a meaningful workload utility before classical search. Two tested
settings do not prove the earlier >=400-effective-settings requirement. Keep
time/size tradeoffs explicit, include charged confirmation and exact correctness
checks, and prevent outcome-dependent workload selection. No new model allowance
is established by this stage. The prior V72 five-seed negative result stands.
Cross-system held-out routing, a practical benefit margin and paper-level
evidence remain unestablished; this feasibility result does not imply Q2 readiness.
