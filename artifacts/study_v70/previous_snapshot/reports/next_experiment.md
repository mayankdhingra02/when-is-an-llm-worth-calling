# Next experiment after V69

Freeze a new three-case feasibility stage with the corrected RocksDB binding.
Use the SAME65536-record/10000-warmup/100000-read workload and the SAME reference,
contrast, reference settings; this repairs configuration application, not a search
for a favorable case. V69.1's no-further-performance-retries limit has been reached.

The corrected open helper in src/escalation/rocksdb_binding_v69.py explicitly sets
the default column family's options. Native tiny synthetic tests confirm1,2,8MiB
caches survive reopening and are attached. Full measurement workload remains unrun
with this helper. The original contrast ran with8MiB instead of1MiB. Its raw valid
flag is superseded by results/v69_validity_audit/summary.json; never pool it as valid.

Before new physical collection:
1. Freeze source/runtime/input hashes, three intended trials,120s/trial,2GiBsampled
   RSS and600s stagecap. Keep failures/unattempted denominator and previous costs.
2. Replace broad historical LOG matching with active-only cache/option readback,
   verify actual supplied-cache usage after warmup, and stop before timing if any
   setting fails. Supply explicit column-family options on creation AND reopen.
3. Serialize byte metadata safely. Write atomic progress/phase receipts before and
   after load, full scans, warmup and timed reads; preserve timing even if optional
   file metadata serialization fails. Test failure injection before execution.
4. Preserve exact payload checking, input/response hashes and full before/after
   scans. Record validation and setup costs separately; do not call Get timings
   pure native engine time or claim cold-disk behavior.

Only after corrected feasibility passes, freeze a20-label/checkpoint10 classical
study and an appropriate metric.512nominal option vectors do not establish400
physicallyvalid,semanticallydistinct effective configurations; check before stronger
admission. Avoid an exhaustive huge grid merely to learn the hidden global minimum.
Group RocksDB/LevelDB together, development only, no cross-system claims from seeds.

Remainingsource allowance568438763bytes under5GiB. Zero newmodelcalls inV69; all
oldinferenceallowances unchanged/exhausted. A latermodelstudy needs concrete scope,
realconstrainedgrammarvalidation,matchedclassicalcontrols,frozengroupsplit and
thresholdtraining rules, then an exact newinferenceallowance. No paid/cloud services,
credentials,systemwideinstalls,newterms,push/publication/contact orindefinitejobs.

Completed evidence:reports/rocksdb_v69.md,502passedtests and sealedrawlogs/validity
correction. No actual benefit-aware routing result orQ2readiness established here.
