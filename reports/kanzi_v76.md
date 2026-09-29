# V76: controlled evidence for the buffer repair

Three prospectively fixed trials completed in 2.987991 seconds. The unchanged
Kanzi1.9 executable reproduced V75's exact exit13/block49 invalid-length error.
The isolated buffer-reference patch compressed the same input/configuration to
7,199,115 bytes; the ORIGINAL owner decoder recovered the full16MiB input exactly.
The patched reference trial compressed to6,502,417bytes with the same SHA256 as
V74, and also decompressed exactly. Retained binary products were replay-verified.

This supports the stale-buffer diagnosis for the observed failure: after entropy
output grows ByteArrayOutputStream.buf, final emission must read its current
buffer, not the stale data.array. The only source change exposes the current buf
through getBuffer() and uses it for the final write. The owner source, original
JAR, V75 failure, and logs remain intact. The corrected JAR is a clearly labelled
Apache-2.0 adaptation, not an upstream release or a claim of a novel upstream bug.

Evidence: artifacts/study_v76/buffer_fix.patch, build.json, verification.json;
configs/runtime_v76.lock.json; reports/protocol_v76.md and .freeze.json;
results/v76_kanzi_diagnosis/ (all outputs, commands, logs, charge journal).
Patched JAR SHA256:
740a8d550f5f07a6a3eec00f2d424e9f599d5d394fcd6ad45cfd54a01b459a23.

Three physical charges include ONE failed application control and TWO successful
trials. Do not report all three as successful compression. Five application
processes executed; no retry, download, model request or external spend. The
sandbox process-monitor preflight failed before collection and the frozen command
then ran with process-monitoring permission; that was not an application retry.

Offline verification: `.venv/bin/python scripts/verify_kanzi_v76.py`.
The result is narrow: no new corpus, broad codec proof, exhaustive compatibility,
held-out system, LLM benefit or journal-readiness evidence. A fresh budgeted
classical study on the adaptation is V77; it collects all prefixes anew and keeps
the same candidate set, objective, workload, seed list and policies as V75.
