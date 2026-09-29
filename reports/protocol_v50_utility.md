# V50 — utility-contract audit and restricted classical experiment

Freeze before V50 execution. Follow-up to V49's failed decoder diagnostic,
not an extension of its model-call allowance. No LLM calls, downloads or new
compression measurements. All families/workloads here were exposed in V15/V17;
no new held-out or model-generalization claim. This is a correctness/control
study, not an attempt to select a favorable prompt or another larger grid.

Audit all 846 retained V17 compressed files: verify saved hashes and lengths,
inspect format flags, and actually decode each retained file to exact original
workload bytes. Record each operation before execution; cap 846 and 180 seconds
for the combined stage. CLI decoding timeout 2 seconds, no retry. These are new
decode verification operations, not new compression runtime measurements or
new objective vectors. Do not reuse their timings as an optimization target.
If any file fails, preserve the denominator and stop the subsequent comparison.

Compare the actual frame to source settings, using the owner specifications:
Zstandard v1.5.7 magic 28 b5 2f fd, frame descriptor bit 2 content checksum;
LZ4 v1.10.0 magic 04 22 4d 18, FLG bit 5 block independence, bit 2 content
checksum, BD bits 6..4 block maximum-size ID. zlib requires its standard wrapper
and successful native decompression. Header inspection is not a cryptographic
security or corruption-resistance test. Exact original equality is checked
separately. Preserve any CLI normalization of flags rather than assuming commands
always force identical headers. Admission mask is based on requested settings;
require admitted LZ4 frames to be independent and contain content checksums.

Restricted research contract, held constant within each codec family:
- Identical original payload and version; exact lossless decoding of every trial.
- Zstandard content checksum ON; exclude checksum-OFF settings.
- LZ4 block independence ON; exclude dependent-block settings; verify content
  checksum present. Block maximum size can vary within its original <=4 MiB
  domain. Independent blocks do not by themselves supply an index/random access API.
- zlib wrapper and checksum unchanged, all original settings eligible.
- Compressed size no larger than the same predeclared V17 reference's acquired
  size: zstd level3/window19/checksum, lz4 level1/block7/independent, zlib
  level6/memory8/default strategy. Not a customer-approved SLA.

This yields 48 zstd, 48 lz4, 90 zlib requested configurations before target access.
Do not deduplicate behavior using outcomes or adjust masks after scores.
The contract does not fix total RAM, decompression latency, power, or all possible
workloads. No equivalence across codecs, semantic safety guarantee, or claim
that the old contract was invalid for purely sequential lossless use.

Run 15 cases, all five original fixed seeds in each family. Reuse the unchanged
V16 nominal joint-3NN selector: acquire reference + three seeded random settings,
then six adaptive steps for a ten-vector prefix. Save/hash prefix before branching.
Two continuations, joint-3NN and random, each ten new vectors, cloned prefix/RNG.
Every arm has 20 inclusive evaluations; actual collection 30 per case = 450
recorded-vector acquisitions. Charge before reading a target; full-table objectives
remain evaluator-only. No new physical compression trials, no LLM responses.

Independent evaluator reconstructs all decisions/source rows/budgets and computes
full restricted-table feasible headroom only after optimizer collection. Report
all cases, family means, W/T/L against random, feasibility and timing CV for chosen
incumbents. Headroom is a nondeployable bound. No inference that a model attains it.
A descriptive 5% headroom screen in at least two families, in >=2/5 cases per
family, is NECESSARY to motivate a future LLM proposal, not statistical evidence
or automatic authorization. Failures/partial runs prohibit complete-case claims.
If it fails, do not spend LLM calls or widen this grid again. If it passes, any
future real-model quality experiment needs its own frozen design and budget.

Also inventory the nine external V8/V41 family manifests without reading new
raw targets. Distinguish recorded objective meaning from verified task utility;
unknown correctness remains unknown. No retroactive relabeling of prior results.
Source schemas alone cannot establish that each flag changes user-visible output.

Pin inputs, implementation and raw-byte hashes before execution; compile and test
successfully before freeze. Keep separate actual decode-verification/recorded-
vector/inference/physical-compression counts. Same 901120-byte CPython source
archive is one small workload, not three independent workload domains. Three
codec families and repeated seeds remain development-only evidence.
