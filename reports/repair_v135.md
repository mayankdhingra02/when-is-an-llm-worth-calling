# V135: does a valid SAC response repair the optimization result?

Five exposed-development cases, identical historical B10 prefixes and prompt bytes, same original sampling seeds. The model/runtime identity is unchanged. This repair changes the output allowance from512 to1024 and uses the V128 canonical grammar; it does not isolate token count from whitespace grammar. The59-feature format has a constructive622-token upper bound including EOS. Original V127 failures and V134 denominator remain intact.

Actual new responses: 5/5 valid, 0 fallbacks; 0/5 improve the saved prefix.

| Comparator | Available cases | Mean new model gain | Wins/ties/losses |
|---|---:|---:|---:|
|batch_3nn|5|-0.1333%|0/4/1|
|full_sequential_3nn|5|-0.4036%|0/3/2|
|presentation_first10|5|+0.0000%|0/5/0|
|random_full|5|-0.1342%|0/4/1|
|single_portfolio|2|+0.0000%|0/2/0|

| Seed | Prefix | Old fallback | New model | Sequential |
|---:|---:|---:|---:|---:|
|11|1.5|1.5|1.5|1.5|
|23|1.5|1.5|1.5|1.5|
|37|1.5|1.5|1.5|1.5|
|53|1.51|1.5|1.51|1.5|
|71|1.5|1.49|1.5|1.48|

Actual costs: 5 real requests, 0 retries, 5120 allocated output tokens; 3013 generated / 9500 prefill observed, 0 missing-usage attempts. Model lifecycle 160.239s, startup 2.571s; peak sampled server RSS 6679609344bytes, exit 0. Exactly 50 newly charged table accesses in 0.069s; five B20 arms each preserve ten acquired prefix labels. All choices sealed before targets were parsed. No new native run, download or spending.

Every primary comparison retains all five cases. The optional historical single-portfolio control exists for only a subset of seeds; its actual denominator is explicit and cannot support a five-seed contrast. Historical classical/random controls are reused with identical prefix state and hashes; their original collection cost is not zero or charged again as new native execution. Deployment estimate is one request and ten new outcomes per escalation, total B20, plus startup/projection overhead. This table is recorded n-body execution-time data: original equal-utility, measurement-noise and dataset-redistribution limitations remain unresolved; no new functional correctness validation is implied. Historical source metadata may retain its original split label; this stage is explicitly exposed development.

This is a reliability repair, not a new independent family, a fitted router or journal-ready result. Valid output need not create incremental optimization benefit. Do not overwrite failed-contract evidence or add these five repeats as five new systems. Reproduce with `scripts/report_repair_v135.py`; full source/acquisition/response replay uses `scripts/verify_repair_v135.py`.
