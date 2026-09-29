# V107: bounded native-client feasibility

**Frozen gates passed.** Six intended attempts; 6 charged native configuration attempts; 6,291,456 byte-valid responses. No LLM request or new recorded-table outcome. These are real local NGINX executions on an exposed development group; no optimization benefit, independent-group generalization or journal-readiness claim.

|Attempt|Bundle|Status|Workload seconds|Client CPU/wall|
|---|---|---|---:|---:|
|1|reference|valid|22.624346|0.6961|
|2|contrast|valid|22.367504|0.7700|
|3|reference|valid|23.866047|0.6760|
|4|reference|valid|22.629467|0.6901|
|5|contrast|valid|22.993840|0.7571|
|6|reference|valid|23.082597|0.6901|

Gate outcomes: `{"all_six_valid": true, "duration_at_least_two_seconds": true, "reference_relative_range_at_most_10_percent": true, "client_cpu_wall_at_most_0_8": true}`. Reference relative range: 0.05386845602173049. This is a screening statistic, not a confidence interval. Native client elapsed includes connection setup and every response check; CPU includes user and system time. Local client/server share this host; CPU/wall alone does not identify every bottleneck. Two bundled settings are not a validated400-configuration tuning domain. All failures and unattempted conditions remain visible.

![Feasibility](../results/v107_analysis/feasibility.png)

Collection lifecycle: 137.975s. Intended per-attempt fixed workload:16connections×65536requests×32768bodybytes. Body bytes flow over loopback, not the internet. Download0; paid/cloud spend0. No deployment-cost estimate. Client source/binary, NGINX binary, harness and protocol were hashed before outcomes. Synthetic protocol fixtures are excluded from this report. Owned processes were checked absent per attempt.

Raw logs: `results/v107_nginx/`; verifier/CSV/figure: `results/v107_analysis/`; freeze: `reports/protocol_v107.freeze.json`. Replay `.venv/bin/python scripts/report_nginx_native_v106.py --stage 107` performs no workload/model call. Do not rerun the once-only collector into its old output directory. Gates must be met before any optimizer study, using a new prospective protocol for any harness revision.
