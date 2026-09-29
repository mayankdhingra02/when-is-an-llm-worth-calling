# V53 — a fresh application workload passed correctness feasibility

The project-local Temurin 17 ARM runtime successfully ran the released DaCapo
Xalan workload three times. Every run passed the owner's validation, and every
final 23,901,000-byte transformation output matched the retained reference SHA256
`4c72b92f00eca08f8bda35e2734124f92fbfd01884c3bf259f2f5d005e98bddb`.
There were no failed or unattempted runs. This establishes local feasibility of
a new development benchmark; it is not an optimization or LLM-benefit result.

| Run | GC threads / NewRatio / SurvivorRatio | Warmup ms | Timed iteration ms | Outer seconds |
|---|---|---:|---:|---:|
| Reference | 1 / 2 / 8 | 1965 | 1389 | 3.612 |
| Contrast | 4 / 4 / 4 | 1791 | 1328 | 3.374 |
| Repeated reference | 1 / 2 / 8 | 1746 | 1299 | 3.361 |

The same reference setting's two reported times differ, so we do not present the
contrast as a measured configuration advantage. All V53 timings are excluded
from the later V54 optimization table. Physical accounting is three JVM
invocations, three warmup and three timed iterations; elapsed stage 10.391 s of
210 s allowed. No model calls, APIs, external spending or system installation.

## Correctness evidence and scope

Inspecting the pinned owner source revealed that its Xalan configuration checks
completion stdout and empty stderr, not the transformed output itself. Our wrapper
therefore fixes one application worker (deterministic job order), preserves the
output and checks bytes against the first successful released-code execution.
All final outputs agree. The first canonical output is retained under
`artifacts/sources/live_v53/trial_0/xalan.out.0`; later disposable scratch directories
were removed after hashing. Raw process logs, validation reports, commands and
output receipts remain under `results/v53_java_feasibility/`.

Reference equivalence is not independent proof of XSLT standards conformance.
We do not independently hash warmup output; owner validation covers warmups and
timed iterations. The benchmark is historical, uses a single application worker,
and a fixed two-iteration scheme does not establish JIT convergence or steady-state
performance. It simulates repeated XML transformation and is more application-like
than the retired tiny compression workload, but is not a representative production
deployment or multiple independent software systems.

## Exact artifacts

- Runtime: Temurin 17.0.20.1+1, macOS aarch64 JRE, official release SHA256 verified.
  Unpacked only in `.local-runtime/java-v53/`; no system-wide changes.
- Benchmark: DaCapo 9.12-MR1-bach, Xalan 2.7.1, default workload of 100 repetitions
  of 17 XML inputs, `-t 1 -n 2`, 512 MiB fixed heap, ParallelGC, adaptive sizing off.
- [Owner release](https://github.com/dacapobench/dacapobench/releases/tag/v9.12-MR1-bach)
  and [pinned workload source](https://github.com/dacapobench/dacapobench/blob/4d4c995c19c3fde69c2a8d677fc5bdf22a7d7d5f/benchmarks/bms/xalan/src/org/dacapo/xalan/XSLTBench.java).
  Jar SHA256 is computed/pinned locally; this old GitHub asset supplies no
  independent digest. Owner release metadata and byte size are retained.
- DaCapo harness/Xalan: Apache 2.0; other bundled components have their own licenses.
  Temurin: GPL 2 with Classpath Exception. License material remains in artifacts.
  No upstream source modification or arbitrary installation script was executed.

The protocol and 272 input files were sealed before execution. Raw trial receipts
and exact commands are retained, with synthetic parser tests kept separate. The
Adoptium metadata endpoint returned403; the owner's GitHub release endpoint worked.
An initial README path returned404; the actual README was read from the jar.
No special credentials or terms were used. Persistent download accounting includes
all successful payloads; subsequent source metadata is also charged.

Next: V54 tests a predeclared grid using fresh repetitions and classical baselines.
Do not use this three-run feasibility test as evidence that the LLM or a router wins.

Follow-up: V54 subsequently completed all 144 trials and the classical screen; see [result](java_screen_v54.md).
