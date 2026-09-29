# V37: the unchanged V34 archive reconstructs on Linux

**The existing V34 reproduction archive passes under Linux/Python3.11.12 and produces exactly the same scientific output as the earlier macOS/Python3.10.13 and3.12.14 checks.** Both Linux corruption controls reject altered evidence, and clean reconstruction passes after restoration. This adds a different operating system and Python version on the same physical host, not an independent-machine or third-party reproduction.

The archive is unchanged: [download the V35.1/V34 snapshot](../output/llm_escalation_v34_reproduction_v35_1.zip),3,690,811bytes. SHA256:

`75333386b2ab80ac5a49ec554050fc1f4ba92e708a2c1908c1cdfcccecb663f9`

## Actual environment and execution

Docker used an already available local image tagged`python:3.11.12-slim-bookworm`, pinned to image ID:

`sha256:dbf1de478a55d6763afaa39c2f3d7b54b25230614980276de5cacdde79529d0c`

The local engine reports Linux/arm64 image metadata and a repository digest. Its origin was **not independently authenticated against a remote registry**; no pull or network lookup was needed. Actual process environment was **Linux-6.12.76-linuxkit-aarch64-with-glibc2.36**, Python**3.11.12**, UID**65534**. This is Docker Desktop's local Linux VM on the original macOS machine and ARM architecture.

Execution disabled networking and image pulls, used a read-only container filesystem and two read-only individual mounts(archive and harness), dropped capabilities, enabled no-new-privileges, limited memory to256MiB/one CPU/64processes and used64MiB temporary extraction storage. The process confirmed UID65534,zero effective capabilities and NoNewPrivs=1. The host imposed a90-second deadline and each verifier process a30-second deadline. Only the task's UUID-named container could be cleaned up; automatic removal was verified.

The host run took **9.773409s**, including container startup and teardown. The in-container harness took **6.968893s**. Initial clean reconstruction took **2.493014s**; restored reconstruction took **2.104306s**. These are validation/maintenance times, not model latency or fresh experiment runtime.

## What matched

The same standard-library-only verifier ran with`-I -S`, with third-party site loading disabled. Every scientific output field was compared with both earlier macOS receipts; only the interpreter-version string was excluded.

| Verification item | macOS3.10 / macOS3.12 / Linux3.11 |
|---|---:|
| Archive content files checked | 418 / 418 / 418 |
| Included frozen references checked | 422 / 422 / 422 |
| Source tables reconstructed | 2 / 2 / 2 |
| Prefixes and candidate shortlists | 10each / 10each / 10each |
| Adaptive classical decisions | 300 / 300 / 300 |
| Original model outputs decoded and grammar checked | 60 / 60 / 60 |
| Relevant real cached LLM selections | 30 / 30 / 30 |
| V34 arms replayed | 70 / 70 / 70 |
| Charged source-vector records | 800 / 800 / 800 |
| Paired comparisons / Decimal scores | 120 / 240 in each environment |

Family means, wins/ties/harms and size-constraint diagnostics match exactly. The fixed assigned-ID LLM gain remains−0.3015% against size-aware shortlist3NN and−1.6470% against full-domain joint3NN. This does not add independent optimization cases or evidence of routing benefit. V36's later exact-arithmetic arms are not in this archive and were not replayed in Linux here.

## Negative controls and tests

Both negative controls ran only inside the temporary extraction. Appending an extra byte to the summary was rejected by the manifest hash check. Altering an aggregate gain and updating that file's index hash was rejected by independent semantic reconstruction. Original bytes were restored and verification passed again with identical outputs. Repository source/results and archive bytes were never modified. Hashes and these tests do not protect against coordinated malicious replacement of the verifier and all evidence.

**251 project tests passed in1.61s**, including separately named synthetic tests for hash validation,extraction path/symlink rejection and scientific-output comparison. All **3,158historical/current frozen references** passed. Nine stage inputs were frozen before container execution.

The initial Docker socket read was blocked by the filesystem sandbox and then explicitly approved. One metadata-format attempt failed because an optional image Entrypoint field was absent; an index-based format succeeded. These pre-execution events are recorded in image_selection.json. The actual container validation completed without an execution failure. No container remains.

## Commands and evidence

Actual bounded host command:

```sh
.venv/bin/python scripts/run_linux_v37.py
```

The runner refuses to overwrite its completed receipt and never pulls an image. It verifies frozen input hashes and the pinned local image before execution. The exact Docker invocation and raw stdout/stderr are retained in [execution.json](../artifacts/study_v37/execution.json). For a new host without this already cached image, image acquisition is a separate action; these instructions do not silently authorize a pull or cloud resource.

The portable archive itself remains usable after extraction via:

```sh
python3 -I -S scripts/verify_reproduction_v35_1.py
```

Evidence: [container receipt](../artifacts/study_v37/linux_receipt.json), [cross-OS comparison](../artifacts/study_v37/validation.json), [cleanup](../artifacts/study_v37/cleanup.json), [tests](../artifacts/study_v37/tests.log), [history audit](../artifacts/study_v37/history_audit.json), [protocol](protocol_v37_linux.md). The standalone archive retains its own README and source/license attribution; this validation does not repackage it or publish anything.

## Limits, costs and next action

This checks OS/Python-version portability of saved outcomes. It does not rerun model generation, authenticate model weights or image origin against publishers, measure production performance, validate application-specific quality, test unseen-system routing, or provide independent-machine confirmation. The source prompts remain runtime-only and their size filtering retrospective. No new figure is needed: the scientific numbers and existing V34 figure are unchanged.

New model calls,objective acquisitions,physical trials,downloads and external spend: **zero**. Resource and download ledgers remain byte-identical to pre-V37. Cumulative experiment runtime2286.489703/3600s,remaining1313.510297s; follow-up requests200/200(300includinginitial); recorded accesses9,308; physical trials1,274. No cloud,push,publication,contact or background job.

**Single next action:** have an independent reviewer run the unchanged archive on another physical machine. The packet now has same-host macOS/Linux and three-version evidence. A scientifically new collection campaign remains a separate prospective study requiring application quality/gain requirements,untouched software groups,strong controls and a new explicitly bounded inference allowance or genuinely compatible cache.
