# V106: bounded native-client feasibility

**Frozen gates failed.** Six intended attempts; 6 charged native configuration attempts; 6,291,456 byte-valid responses. No LLM request or new recorded-table outcome. These are real local NGINX executions on an exposed development group; no optimization benefit, independent-group generalization or journal-readiness claim.

|Attempt|Bundle|Status|Workload seconds|Client CPU/wall|
|---|---|---|---:|---:|
|1|reference|valid|22.296778|0.9708|
|2|contrast|valid|21.688294|0.9773|
|3|reference|valid|21.880782|0.9771|
|4|reference|valid|21.941509|0.9822|
|5|contrast|valid|21.769836|0.9847|
|6|reference|valid|22.483349|0.9707|

Gate outcomes: `{"all_six_valid": true, "duration_at_least_two_seconds": true, "reference_relative_range_at_most_10_percent": true, "client_cpu_wall_at_most_0_8": false}`. Reference relative range: 0.02720318535776306. This is a screening statistic, not a confidence interval. Native client elapsed includes connection setup and every response check; CPU includes user and system time. Local client/server share this host; CPU/wall alone does not identify every bottleneck. Two bundled settings are not a validated400-configuration tuning domain. All failures and unattempted conditions remain visible.

![Feasibility](../results/v106_analysis/feasibility.png)

Collection lifecycle: 132.404s. Intended per-attempt fixed workload:16connections×65536requests×32768bodybytes. Body bytes flow over loopback, not the internet. Download0; paid/cloud spend0. No deployment-cost estimate. Client source/binary, NGINX binary, harness and protocol were hashed before outcomes. Synthetic protocol fixtures are excluded from this report. Owned processes were checked absent per attempt.

Raw logs: `results/v106_nginx/`; verifier/CSV/figure: `results/v106_analysis/`; freeze: `reports/protocol_v106.freeze.json`. Replay `.venv/bin/python scripts/report_nginx_native_v106.py --stage 106` performs no workload/model call. Do not rerun the once-only collector into its old output directory. Gates must be met before any optimizer study, using a new prospective protocol for any harness revision.
