# V71: live classical search with in-budget endpoint confirmation

Frozen after V70 passed all three corrected feasibility trials, before any new
search measurements. Development-only exploration on one RocksDB/LevelDB family.
Same pinned workload, saved request trace, expected values, corrected V70 worker
and geometric 512-vector nominal domain. No fabricated global optimum or regret.
This domain has not established 400 performance-distinct settings; V71 does not
claim to satisfy the stronger external-benchmark/held-out admission criterion.

Five fixed seeds11,23,37,53,71. Each prefix uses four seeded random unique
configurations, then six deterministic acquired-only 3NN choices. Physically
collect each 10-evaluation prefix once and preserve it for all continuations.
Use declared-domain log2 feature scaling only. No full-table labels exist.

Three continuations: random, 3NN, and RF-LCB (64 trees, mean minus standard
deviation, same pinned classical_java_v54 implementation). Seven distinct search
choices per arm, then freeze the configuration with lowest observed verified-loop
time among its17 search observations. Spend the remaining THREE objective
evaluations repeating that selected configuration. Confirmation outcomes never
change the selected configuration or any search decision. Thus each arm uses
10prefix +7search +3confirmation =20physical objective evaluations inclusive.
This explicit reliability allocation is an adaptation of the earlier20unique-row
screen; do not pretend the designs are identical.

Seeded step-wise shuffled arm order (Random(seed+71000)) interleaves continuations
and each confirmation round. Random-search RNG is isolated (Random(seed+1000)).
Every call starts a fresh DB and identical load/scan/reopen/warmup sequence.
No observed data or RNG is shared across branches after prefix. No extra label
probes, outcome-based retry or measurement cache. All failures charged before launch.

Primary descriptive endpoint: median of the three confirmation times for the
preselected incumbent, lower is better. Report all three values, their CV, selected
configurations, search minima, per-seed RF-vs-random/3NN differences and actual
cost. No statistical significance, generalization, LLM-benefit or global-headroom
claim from five seeds of one exposed system. No headroom threshold fitted here.
Reference/repeated measurements from V69/V70 are not optimizer inputs.

Actual collection cap200physical evaluations: five times[10sharedprefix+
3arms*(7search+3confirmation)]. Logical per-arm count300, with50prefixevaluations
shared. Stop and preserve all200intendedslots on any error, timeout or incorrect
settings/data. Each call120s, stage1800s with150sreserve before launchinganother,
sampled2GiBRSS, one worker. No retry or LLM call; no download or external spending.

DB data files are owned temporary scratch, bounded to one trial at a time, removed
only after process-level results/phase receipts, file names/sizes/SHA256 and engine
LOG/OPTIONS/MANIFEST metadata are archived. Keep fixed raw inputs, traces, every
response digest and full-scan digests. Archive hashing/cleanup is actual collection
overhead but outside the timed objective. This avoids keeping ~13GiB of redundant
databases. Do not call metadata-only archives full physical DB snapshots.
