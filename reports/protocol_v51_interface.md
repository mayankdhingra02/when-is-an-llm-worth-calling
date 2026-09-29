# V51 — prospective paired codec-interface measurement check

Motivated by V50's small headroom and CLI timing scope. Same exposed development
archive, same installed versions, same restricted configuration grid; no grid or
workload expansion and no LLM prompt change. This is not an independent-system
validation or an experiment conditioned on obtaining a positive result.

Take all 48 checksum-enabled Zstandard settings and all 48 independent-block LZ4
settings from the feature-only V50 manifest. zlib already uses its API and has no
CLI comparator in this study, so it is outside this mechanism comparison.
Five rounds. Within each round shuffle all 96 configurations; for each, shuffle
API/CLI ordering and run adjacent observations. Random(51000), 960 total attempts.
All measurements are fresh; do not mix V17 timings into the new paired estimates.
No free warmups or retries; each mode runs in a fresh Python worker/process group.

CLI uses unchanged V17 commands, input on stdin and single-thread options. API
uses pinned native shared libraries through explicit ctypes signatures, based on
installed owner headers. Zstandard compression level/window/checksum on/workers0;
content-size field off. LZ4 frame preferences set block size/independence/content
checksum/compression level, remaining defaults zero. Library loading is before
API timing, while context/buffer allocation and output copy are timed. CLI launch
and pipes are timed. Both modes decode with the pinned CLI after timing and
require exact original bytes, content checksums and LZ4 independence. Decode
latency is not a target. Hash/store every output; retain all failures/denominators.

This compares execution interfaces, not a pure measurement of startup overhead:
API one-shot compression can choose different blocks/parameters than stdin
streaming CLI. Report byte/size agreement before interpretation; do not attribute
all speed differences to startup if outputs differ. Different stream-size knowledge,
FFI overhead, cache behavior and resource management remain possible causes.
No production speedup or zero-overhead-API claim follows.

Bound: 960 new physical-vector attempts, 180 seconds total collection, 3 seconds
per process group, zero downloads/model requests/spend. Charge before launch and
stop at bounds, no automatic retry/resume. Do not silently expand repetitions.
Compile/test wrappers and freeze implementation, manifest, workload, runtime hashes,
analysis before collection. Synthetic smoke fixtures stay outside measured results.

Analysis: all intended failures, exact roundtrip counts, paired compression ratio
(time CLI / time API) per setting median over five pairs, equally weighted
configuration summary separately by family; size and byte agreement, mode-specific
within-setting CV. Do not pool raw times across families, or call pairs independent
software systems. Any instability or incomplete collection blocks optimizer replay.

When complete, form separate median tables by family/mode; all five repetitions
must have stable size per setting. Do not filter timing outliers. Derive size cap
from each mode's same reference setting; note any cap discrepancy. A separate
predeclared acquired-only classical replay uses identical feature order, five
fixed seeds, ten-label prefixes and paired joint3NN/random continuations,20
inclusive labels per arm. Four family/mode cells ×5×30 =600 charged recorded
vectors; modes remain in the same software-family split. This replay has its own
30-second ceiling and is blocked by incomplete/unstable physical evidence.

Report all quality/headroom results by mode. Full-table bounds are evaluator-only.
No automatic LLM follow-up even if headroom changes: establish whether the native
interface is the relevant application first. This experiment's question is whether
measurement interface materially affects interpretation of a small-workload
optimizer benchmark; its answer may be negative. Preserve earlier results.
