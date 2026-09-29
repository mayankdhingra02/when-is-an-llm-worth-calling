# V75: classical collection stopped on a real Kanzi failure

The frozen200-trial run acquired8 valid outcomes and then failed on its ninth
configuration. It stopped without retry:191trials were unattempted. No10-trial
prefix or continuation arm completed. **No classical-policy comparison, LLM
benefit or journal-readiness conclusion is supported.** This is a validity result.

Failure: Kanzi1.9 exited13 on `LZP+TEXT+BWT+LZP`, ANS1,262144-byte blocks,
jobs1, checksum enabled. Raw log reports block49:
`Invalid length: 2479880 (must be in [1..2163456])`.
These are bits:309985bytes requested versus270432available. This was an
application error, not a timeout, RSS kill, model error or fabricated response.
The failed compressed partial output is retained; decompression never launched.

The eight successful trials each passed exact-byte decompression, checksum and
applied-setting receipts. Their individual observations are retained but are
not analyzed as a completed optimization comparison or independent systems.
No failure rate for the whole448-candidate domain can be inferred from this
adaptive nine-acquisition prefix. The first observed failure stopped collection.

## Source diagnosis: plausible, not experimentally confirmed

Pinned owner `CompressedOutputStream.java` creates a
`CustomByteArrayOutputStream` using `this.data.array`, then emits the completed
entropy-coded block from `this.data.array`. The nested stream extends Java's
ByteArrayOutputStream and assigns inherited `buf` to that array; it does not
expose or propagate a grown buffer. If entropy output expands enough to grow
the inherited buffer, the final emission can still read the original smaller
array. `DefaultOutputBitStream.writeBits(byte[],...)` contains the exact invalid
length guard observed in the log. This supports a stale-buffer hypothesis.
No instrumented stack trace, minimal controlled reproduction or patch comparison
has yet confirmed the mechanism. Do not report this as a verified upstream bug
fix, or silently alter the pinned owner artifact.

Block49 at256KiB begins at12MiB, the start of the fixed input's high-entropy
section. This is an explanatory observation after failure; the input was fixed
beforehand and must not be replaced to hide the failure. No new corpus or hidden
timing table was inspected.

## Protocol and evidence

The objective was compressed size, with runtime recorded separately. The frozen
domain had448 canonical vectors, jobs fixed1. Owner source permits transform
skips, so the protocol explicitly revised the earlier400-effective-settings
gate to exploratory canonical-domain evaluation. It did not certify448 distinct
behaviors or pass the stronger readiness gate. All variants remain one Kanzi
development family. See reports/protocol_v75.md and its prospective hash freeze.

- Raw9 charges,17process logs, receipts and failed partial output:
  `results/v75_kanzi_classical/`.
- Offline replay of all acquired prefix decisions and failure denominator:
  `results/v75_failure_audit/summary.json`.
- Tests, source hashes, cost ledger, execution notes, snapshots and seal:
  `artifacts/study_v75/`.
- Exact candidate grid: `data/kanzi_domain_v75.json`.

548tests passed in3.61s before collection. The actual-record replay validates
all nine acquisition choices against only their prior acquired observations;
checks successful receipts/header/equality hashes; verifies one failed and191
unattempted cases; and verifies that no saved10-prefix or comparison exists.
Validated bulky outputs were removed as prospectively declared; later byte
equality is supported by contemporaneous receipts, not replay of deleted files.
V74 retains its full three-trial compressed/decompressed outputs.

```
.venv/bin/python scripts/audit_kanzi_v75_failure.py
.venv/bin/python scripts/seal_evidence_v75.py --verify-only
.venv/bin/python -m pytest -q tests
```

`analyze_kanzi_v75.py` implements the prospectively described complete-run
comparison but was not executed; it rejects incomplete data. No V75 comparison
figure has been generated. Do not retry the one-shot collector or overwrite this
failure with a successful future version.

## Cost and next action

18.357126seconds collection wall time;9charged trials,8successful,1failed,
17application processes. No new downloads, LLM calls or external spend. Cumulative
model requests2016, recorded-table acquisitions26358 unchanged;562095257download
bytes remain. Monetary hardware/electricity/human/agent cost is unknown; no
deployment cost estimate is presented. See the ledger for summed process time.

Next concrete action: freeze a bounded diagnosis using this exact failing
configuration and input. Verify the suspected buffer mechanism with an isolated,
clearly labelled owner-source patch and an unmodified control; charge all runs
and preserve original artifacts. If confirmed, decide prospectively between a
patched adaptation and an explicit failure-aware objective before any fresh
classical batch. Do not remove ANS1 or the failing case simply to produce a win.
The previous V72 negative LLM result and V74 feasibility result remain unchanged.
