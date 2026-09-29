# V105: real NGINX feasibility, timing harness not admitted

Six frozen native configuration attempts ran. All49,152 HTTP responses were byte-exact and all six owned server process groups exited. The experiment validates the response-checking pipeline but **fails the predeclared optimization-feasibility screen**. No LLM called, no optimizer/controller trained, no archived target inspected, and no positive escalation claim.

|Attempt|Bundle|Status|Elapsed seconds|Client CPU/wall|
|---|---|---|---:|---:|
|1|reference|valid|0.170208|0.996|
|2|contrast|valid|0.170308|0.988|
|3|reference|valid|0.165369|0.998|
|4|reference|valid|0.168994|0.992|
|5|contrast|valid|0.163117|0.981|
|6|reference|valid|0.170683|0.984|

Four-reference relative range: **3.15%**, against the10%ceiling. Gate outcomes: `{"all_six_valid": true, "every_client_cpu_wall_at_most_0_8": false, "every_workload_at_least_two_seconds": false, "reference_relative_range_at_most_10_percent": true}`. The short timings and near-full clientCPU utilization are consistent with substantial client overhead; this does not isolate or quantify every bottleneck. No speedup/causal bundle attribution, significance or native-server population claim is justified. Enlarging the request count alone may lengthen a client-limited benchmark without fixing it.

![Predeclared timing screens](../results/v105_analysis/feasibility.png)

## What actually ran

Pinned official NGINX1.28.3 owner archive SHA2562c96a946bfb0882a21744ed429770a2123ae1828c7c48665092993ddee91a918, built locally on arm64 macOS. The first configure attempt failed because installed Xcodeclang17 could not link against the selected macOS27SDK. The successful repair selected installed CommandLineToolsclang21 and its matching SDK only in the build process environment. No system settings/installations changed; both attempt logs remain. Two build jobs maximum, no third-party build dependencies downloaded. Owner license is preserved. [Official build documentation](https://nginx.org/en/docs/configure.html).

Each fresh foreground server listened only on127.0.0.1:18595.16asyncio clients made512requests each,8192requests per configuration; every200status, contentlength/encoding and32768-byte payload was checked inside the measured interval. No HTTP warm-up or reliability probe acquired uncharged outcomes. The six attempts transfer/validate1,610,612,736bodybytes locally; these are local workload bytes, not internet-download cost. Two bundles, sequenceR/C/R/R/C/R, are described in the frozen protocol. The payload is a generated benchmark input, not fabricated model output or a synthetic substitute for measured execution. Unit-test fixtures remain separate.

Actual collection: **6nativeconfigurationattempts,49,152validatedresponses**, lifecycle1.419415s including startup/cleanup. Build time and first failure are separately logged. No new model requests, recorded-table acquisitions, paid/cloud use or external service. Deployment cost is not estimated from this unqualified harness. Successful correctness checks do not establish runtime representativeness or>=400effective tuning settings.

Source/docs download1,320,382bytes in V105; combined with V104, cumulative9,875,903,117/10GiB, remaining861,515,123bytes. Modelpayload and3,938historical requests unchanged. Raw per-attempt counts, times/configurations, stderr, syntax checks and process cleanup: `results/v105_nginx/`. Verified derivatives/figure: `results/v105_analysis/`. Source/build/freeze/test logs: `artifacts/study_v105/` and `artifacts/sources/v105/`.

## Next action

Replace the single-process Python load generator with a bounded native or multi-process byte-validating client, then freeze a new feasibility protocol. Establish sufficient workload duration, tolerable client overhead and reference repeatability before any optimization/LLM run. Keep NGINX as one exposed development group now that native outcomes have been inspected. Do not label future NGINX seeds/versions untouched held-out systems. Archived NGINX admission is still unresolved, and this result does not establish Q2 readiness.

Replay `.venv/bin/python scripts/report_nginx_v105.py` uses only saved evidence and does not reacquire outcomes. Do not rerun the once-only native collector into its existing directory.
