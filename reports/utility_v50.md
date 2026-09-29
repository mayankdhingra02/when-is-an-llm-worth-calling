# V50 — verified utility contract, still little selection headroom

Executed 2026-09-25: all 846 retained V17 compressed files were actually decoded
again and matched the original 901,120-byte source archive exactly. No hash-only
check was presented as a decode execution. All 450 newly charged recorded-vector
acquisitions and 30 classical arms completed across three exposed development
families and five fixed seeds. Full source/decision replay passed; 357 tests passed
before collection. Stage runtime 4.059 seconds. Zero new model calls or physical
compression measurements; 846 new decode verification operations are separate.

The audit distinguishes exact lossless output from extra functionality. Of 288
Zstandard files, 144 have no content checksum. LZ4 has content checksums in all
288, but 72 encode dependent blocks. Requested dependent mode generated independent
frames for some settings; command options are not sufficient evidence of frame
behavior. All 270 zlib files use the expected wrapper and decode correctly.

The new research contract fixes checksums ON for Zstandard and independent blocks
for LZ4, retains the existing zlib wrapper, and constrains compressed size to the
same predeclared reference's acquired size. The feature-only masks leave 48/48/90
configurations respectively; there is no outcome-based filtering or deduplication.
All eligible LZ4 outputs passed both independence and content-checksum checks.
This is a stated storage/format contract, not a universal quality certificate,
application-approved SLA, fixed RAM budget or verified random-access API.

| Family | Mean classical gain over random | W / T / H | Mean hindsight headroom after classical | Cases with >=5% headroom |
|---|---:|---:|---:|---:|
| Zstandard | -0.0847% | 0 / 4 / 1 | 0.6702% | 0 / 5 |
| LZ4 | 0% | 0 / 5 / 0 | 0% | 0 / 5 |
| zlib | 0% | 0 / 5 / 0 | 0% | 0 / 5 |

The headroom screen FAILED. The oracle is an evaluator-only bound on recorded
medians, not a deployable optimizer. Small timing differences do not establish
significance with three source repetitions. Every arm uses 20 inclusive labels,
with the same saved ten-label prefix within each pair. Actual collection is
30 vectors per pair, totaling 450, not 20. These families and the single small
workload are development/exposed; no evidence of unseen-system routing follows.

Source semantics were checked against the owner [Zstandard v1.5.7 format](https://github.com/facebook/zstd/blob/v1.5.7/doc/zstd_compression_format.md)
and [LZ4 v1.10.0 format](https://github.com/lz4/lz4/blob/v1.10.0/doc/lz4_Frame_format.md).
Checksum presence and block independence differ from exact decompression equality.
LZ4 block independence permits separate block decoding but does not create an
index or guarantee an application-level random-access interface. The
[Python zlib API](https://docs.python.org/3.10/library/zlib.html) documents wrapped
versus raw output; the installed stack remains pinned to Python 3.10.13/zlib 1.2.12,
while the online 3.10 documentation currently displays 3.10.21.

The nine V8/V41 external manifests were inventoried without new raw-target reads.
They identify objective columns but do not certify per-row task-equivalent output.
MySQL includes log-flush/doublewrite features, OpenVPN includes authentication and
cipher features, and numerical/compiler tasks require original output/workload
checks. These names flag questions, not verified claims that each option changes
application utility. The old MySQL manual URL redirected to 9.7, OpenVPN's old
manual URL to its article index, and owner raw-XML fetches failed in web retrieval;
no modern manual was silently substituted for the measured old versions.

Evidence: `results/v50_utility/` contains feature admission, 846 decode starts/results,
450 acquisition events, 15 saved prefixes and 30 branches. `results/v50_analysis/`
contains all per-case scores, family results, frame flags and external inventory.
Protocol/code/source freeze: `reports/protocol_v50_utility.freeze.json` (862 files).
Collection and independent analysis receipts: `artifacts/study_v50/`.
The optimizer uses the unchanged acquired-only V16 nominal joint-3NN selector.
The separate evaluator independently reconstructs its 390 adaptive decisions.

Cumulative recorded accesses: 15,158. Historical physical compression trials:
1,274, unchanged. Model requests including initial stage: 1,976, unchanged.
No spending, download, push or contact. The current grid should not be widened
again to find favorable outcomes. A distinct measurement concern remains: CLI
process startup is included in small-input timing. A paired API/CLI measurement
check is justified to examine the interface effect, without implying it will
rescue LLM selection. Any API/CLI output differences must be reported; such a
comparison cannot automatically isolate startup as the sole cause.
