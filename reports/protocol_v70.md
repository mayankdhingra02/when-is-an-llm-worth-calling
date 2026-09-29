# V70: corrected full-workload configuration feasibility

New stage under the resumed research goal; not an overwrite or extension of V69
receipts. All four old physical attempts and validity corrections remain separate.
Run exactly three reference/contrast/reference trials using the unchanged V69
inputs, request sequence, settings, runtime and timing semantics. No outcome-led
workload or parameter adjustment. Development family RocksDB/LevelDB only.

Use the tested explicit-default-column-family opener at both creation and reopen.
Read active LOG only; require engine version, cache capacity, block size and restart
interval to match. Require positive usage of the supplied cache after warmup.
Keep exact payload checking and initial/final full scans. Atomic phase receipts
preserve load, validation, warmup and timed-read evidence even if final optional
metadata fails. Serialize bytes explicitly. Failure-injection tests must pass.

Same three settings: (cache MiB, block bytes, restart interval) =
(8,4096,16), (1,65536,1), (8,4096,16). Same 65536 records, 10000 warmup reads,
100000 timed reads. No inference or optimizer accesses. Three attempts, no retry,
120 seconds per trial, 600 seconds per stage, sampled 2 GiB worker RSS, sequential.
Stop on any failed settings, correctness or resource check; retain unattempted slots.

Admit only to a further development feasibility study if all three receipts and
active settings checks pass. Two repeats are not a reliable noise estimate, and
512 nominal vectors are not 512 proven performance-distinct configurations. A
new classical protocol must specify actual acquisition costs, sampled-search
metrics without a fictitious global optimum, and development-only interpretation.
