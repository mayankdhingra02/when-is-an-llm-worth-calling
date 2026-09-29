# V75: exploratory Kanzi classical compression-size search

Prospective freeze before any V75 acquisitions. V74 feasibility outcomes were
already inspected; this is an exploratory development adaptation, not a held-out
test or replication of archived timings. Preserve the V74 workload byte-for-byte.
No new LLM calls, downloads, paid inference, external spending or model loading.

## Objective and domain decision

Minimize compressed output bytes for byte-exact lossless storage of the fixed
16 MiB input. Record compression/decompression process time, decision time,
verification cost and resource use separately. No weighted time/size utility or
post-hoc size constraint is selected. This is a size optimization workload, unlike
RocksDB's latency objective; do not pool their raw units. Future LLM escalation
would require a declared value-of-byte/cost scenario, not assumed runtime savings.

448 source-distinct candidate vectors = 8 transform pipelines × 7 entropy codecs
× 8 block sizes (powers of two from16KiB through2MiB). Exact enumeration and
ordering in src/escalation/kanzi_v75.py and data/kanzi_domain_v75.json. Jobs fixed1,
checksum enabled, skip-incompressible switch absent, no level presets or NONE
aliases. These choices vary actual pipeline constructors, codec classes and
block partitioning, not spelling or ignored/oversized threads.

Owner-source basis: TransformFactory.java getType packs up to8 non-NONE tokens,
newFunction selects LZ/LZX/LZP contexts, BWT, rank/text/SRT/zero-run stages;
EntropyCodecFactory.java maps each chosen name to a distinct codec constructor.
CompressedOutputStream.java constructs transforms/codecs per block. Block sizes
are supported powers of two smaller than input and divisible by16. Pipelines
include direct owner transforms, the V74 pipelines, and owner preset pipelines.
This deliberately restricted crossed domain is not all possible Kanzi settings.

**Admission criterion revision, before V75 outcomes:** earlier plans required
>=400 effective settings. Source inspection shows transforms can decline/skip
blocks (CompressedOutputStream.java calls forward and records skipFlags), so
canonical/header identity alone cannot certify behaviorally distinct settings.
Exhaustively timing all448 to certify separation would expose the search surface.
V75 therefore tests a *448-candidate exploratory search domain*, not a certified
400-effective-setting task. Report sampled objective/hash collisions; do not
claim this passes the stronger paper-readiness gate. Jobs are fixed specifically
to avoid inflating a size objective with scheduling-only variants. Further
independent domain evidence may be needed before a confirmatory study.

## Fixed policies, seeds and budget

Seeds11,23,37,53,71. Each seed:4 uniformly sampled unique initial configurations,
then6 sequential3NN choices, producing10 saved shared outcomes. No V74 timing or
size observation enters a prefix or policy. Candidate features are one-hot
pipeline/codec and block log2 scaled14..21, entirely source-derived.

Copy the same prefix into random,3NN and RF-LCB continuations. Each makes7 new
unique within-arm acquisitions, then selects the smallest observed byte count
(tie by smaller configuration ID) and charges3 independent confirmation trials.
Budget20 per arm =10prefix+7search+3confirmations. Prefix is physically collected
once:50prefix+105search+45confirmation=200 physical trials;300 logical arm charges.
Do not share continuation labels across arms/seeds. Same candidate chosen by two
arms is physically rerun and charged twice. No uncharged warmups or reliability
probes. Failures stop the stage and remain in the intended200 denominator.

3NN predicts mean acquired bytes of3 nearest observations, stable ties in
acquisition order and smallest candidate ID on score ties; mean absolute feature
distance. RF uses64 bootstrap trees, min leaf1, all features, n_jobs1,
random_state=seed*100+acquired_count; score=mean tree prediction minus tree SD.
Random continuation RNG seed+1000, independent per arm. Per-round arm order is
shuffled by seed+75000, including confirmation rounds. No hyperparameter fitting
or threshold fitting. Only acquired size outcomes are passed to choose().

## Physical measurement and stop rules

Reuse frozen Kanzi1.9 source build/runtime/input. Fresh JVM each phase, heap768MiB,
ActiveProcessorCount4, jobs1. Compression and decompression each <=40s, sampled
process-group RSS<=2GiB, trial files<=128MiB; watchdog0.1s is not a hard quota.
Stage<=1800s; no trial starts after1700s, reserving80s process+20s validation.
Before launching, record a physical charge and full spec. Require both exits0,
checksum enabled, independently parsed header matching codec/transform/block,
job receipt and no ignored-option warning, full decompressed byte equality.
Save commands, logs, receipts, header bytes, input/compressed/decoded hashes and
compressed byte count. Delete only that trial's validated compressed/decoded
products after durable result receipt; retain failed products for diagnosis.
This limits disk use but prevents later direct byte replay of deleted outputs;
independent re-execution would be a new measurement. No retries or adaptive repair.

## Analysis committed before collection

Replay prefix/arm decisions from acquired-only records; verify physical/logical
budgets, selected incumbents and confirmation identity. Report all five seeds,
three confirmation byte counts, medians and per-arm mean of seed medians; percent
size reduction versus each seed's shared-prefix best. Compare RF/3NN to random,
without declaring seeds independent families. Report per-seed win/tie/loss counts,
sampled unique configuration IDs, byte-count collisions and compressed hashes.
Confirmations check observed determinism, not statistical precision of a size
metric. Runtime remains descriptive with startup/JIT/logging/monitor overhead;
no timing ranking or significance claim. Do not inspect unseen candidates.

One family, one artificial workload, development-only. No held-out evaluation,
learned router or LLM benefit is established by this classical experiment. The
earlier V72 negative finding remains unchanged. Synthetic tests stay separate.
Preserve failed/missing cases; a partial run must not be analyzed as complete.
Record collection time/processes/decisions separately from hypothetical deployment
cost (not computed). Any model batch requires a separate concrete bounded scope.
