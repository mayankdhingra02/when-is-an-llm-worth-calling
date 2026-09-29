# V87: DuckDB workload runner ready; generator terms awaiting user approval

This follows the completed V86 exact analysis; it is not a new optimization result. The user asked to keep working toward concrete paper evidence. Routine setup/source inspection and a bounded classical feasibility stage were prepared under the existing local/no-spend limits. The separate generator EULA is the only user decision pending.

## Verified and installed

DuckDB1.4.4 CPython3.10 macOSARM64 wheel from [owner-linked PyPI](https://pypi.org/project/duckdb/1.4.4/), SHA256`5e1933fac5293fea5926b0ee75a55b8cfe7f516d867310a5b251831ab61fe62b`. Installed without dependencies/network into `.local-runtime/duckdb-v87`, leaving the existing environment unchanged. Core runtime metadata reportedv1.4.4/osx_arm64; TPC-H extension **not installed and not loaded**. The two initial core metadata attempts failed before generator/objective use: disabled external access prevented default-home access, then home_directory was rejected as a global option. Corrected by using the project-local extension directory and SQL SET home_directory. All automatic extension installation/loading remains disabled.

[DuckDB core license](https://github.com/duckdb/duckdb/blob/v1.4.4/LICENSE) is MIT. The separately inspected [bundled DBGEN license](https://github.com/duckdb/duckdb/blob/v1.4.4/extension/tpch/dbgen/LICENSE) is TPC EULAv2.2, with use-as-acceptance language. No generator binary has been downloaded/installed/loaded and no data generated. Project instructions prohibit accepting new service terms without explicit authorization; this separate EULA is conservatively treated as requiring user approval. An asynchronous question was submitted. Do not infer approval from its preselected option or elapsed time. The source-license files are retained; no legal-advice claim or redistribution permission is inferred from the core MIT license.

[Owner extension documentation](https://duckdb.org/docs/lts/core_extensions/tpch) supplies generator/SQL/expected-answer APIs for scale0.1. It also documents fixed query parameters, so this proposed scaled subset is not an official TPC-H benchmark result. Queries4/12/13 were chosen before performance inspection for exact count outputs and multi-table operators. The exposed workload would be development data, not held-out confirmation. A bounded text search of earlier admission/registry/studyconfigs found no DuckDB case; broader historical alias/exposure certification remains unperformed.

## Implemented concrete stage

`reports/protocol_v87_admission.md`: at most64MiB source/runtime/extension download bodies, within the global remaining allowance. One setup process at most180seconds, then at most9physical trials/900seconds,60seconds per trial. SampledRSS2GiB, scratch/database1GiB, DuckDB buffer memory512MiB. No model calls, cloud, payment, Docker or system-wide settings.

Three configurations:1thread/defaultoptimizer,4threads/defaultoptimizer,1thread/join-order optimizer disabled. Three Latin-ordered repetitions,3warmup plus16timed three-query suites each. Every objective-query invocation belongs to a charged configuration trial. Execution+fetch is timed; exact answer checking/serialization is separate. Worker validates the owner-released answer table, preserves every response and verifies actual settings. Parent counts before launch and retains failed/unattempted trials. Frozen native-code/query/data/runtime pins are created only after successful preparation and before timing. No broad optimizer or model-benefit claim follows from this9-trial screen.

Files: `src/escalation/duckdb_v87.py`, `scripts/worker_duckdb_v87.py`, `scripts/run_duckdb_v87.py`, `scripts/analyze_duckdb_v87.py`. Nine synthetic validation/permission tests are separate from research data. The actual `prepare` command without a grant was executed and rejected before generator/output startup; receipt `artifacts/study_v87/permission_gate.json`. Native preparation, extension compatibility, actual expected-answer formatting, timings and residual headroom are still untested.

## Resume command sequence after explicit EULA approval

Record the actual user message and EULA SHA256 in `artifacts/study_v87/eula_approval.json` with `granted:true`, `license_sha256`, `user_message` and UTC timestamp. A matching explicit record is checked before every stage; synthetic tests are not grants. Then execute:

```
.venv/bin/python scripts/run_duckdb_v87.py install-extension
.venv/bin/python scripts/run_duckdb_v87.py prepare
.venv/bin/python scripts/run_duckdb_v87.py freeze
.venv/bin/python scripts/run_duckdb_v87.py run
.venv/bin/python scripts/analyze_duckdb_v87.py
```

Network/process-inspection sandbox escalation may be needed; it is distinct from approval of the terms. Stop on a real compatibility/correctness/resource failure and retain it; do not automatically retry scientific trials or change frozen queries based on outcomes. No new inference allowance is requested by these commands.

## Actual costs

13,742,761 new download bytes, including metadata, licenses and the verified core wheel; cumulative4,831,230,643bytes, remaining537,478,477under5GiB. Source fetch ledger retains the initial sandboxDNSfailure, zero bytes, followed by the allowed fetch. No generator/extension download occurred. New objective trials0, model calls0, spendingUSD0. Historical model calls remain2,191. No benchmark/server process is running. See `artifacts/study_v87/resource_ledger.json`.

The scientific result currently ready to review remains V86, not this unexecuted feasibility stage. Its concrete empirical contribution candidate does not certify Q2 readiness.
