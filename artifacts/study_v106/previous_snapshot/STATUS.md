# STATUS — V105 native NGINX ran; timing harness needs replacement

Resume here. V104 finished a source/admission audit. V105 built official NGINX locally and executed six predeclared native feasibility attempts. All responses were correct, but the timing harness failed two frozen feasibility gates. No job remains running. No LLM call or optimization stage is queued.

## Latest concrete result

NGINX1.28.3 on this arm64 Mac; fixed32768-byte public payload served only on127.0.0.1:18595. Six charged configuration attempts, reference/contrast/reference/reference/contrast/reference;16asyncio clients and8192requests per attempt. **All49,152responses were byte-exact**, including correct status, length and encoding. All six owned server process groups exited with returncode0. The generated payload is a benchmark input; these are real software executions, not fabricated outputs or unit-test results.

Workloads lasted0.163–0.171s, below the frozen2sminimum. ClientCPU/wall was0.981–0.998, above the0.8ceiling. Four-reference relative range3.15% passed the10%screen, and correctness passed6/6. These observations are consistent with substantial Python-client overhead; they do not isolate every bottleneck. **Do not run optimization/LLM comparisons on this unqualified harness or claim a bundle speedup.** Six feasibility attempts do not establish400effective tuning configurations. NGINX is now an exposed development group; future versions/seeds are not fresh independent systems.

Read reports/nginx_v105.md. Raw configurations, payloads, request counts, timing, syntax/server logs and lifecycle/cleanup receipts: results/v105_nginx/. Verified CSV/JSON/figure: results/v105_analysis/. Protocol and pre-execution hashes: reports/protocol_v105.md and its source_freeze/execution_freeze JSON files. Source/build/test receipts: artifacts/study_v105/ and artifacts/sources/v105/. The figure was inspected, then given a bundle legend. Four derived outputs reproduce byte-for-byte. Full suite: **802passed,14warnings in21.16s**. Synthetic corruption tests reject changed counts, source blobs and equal-length wrong payloads.

## Build and source integrity

Official owner source archive SHA2562c96a946bfb0882a21744ed429770a2123ae1828c7c48665092993ddee91a918; successful binary SHA2563861521068a3c36bb5a0e6f4d114123a2844fa6db29bf2d4aa56dee1fddec8ae. Initial configure failed in1.95s because installed Xcodeclang17 could not link against selected macOS27SDK. Repair selected installed CommandLineToolsclang21 and matching SDK only in that build process:13.26s success, max2compilejobs. Both attempts preserved. No system setting or installation changed. No compiler/dependency download. BSD-like owner license preserved.

V104 inventoried28,078 historical result/report/configuration/top-level manifest files: NGINX/OpenResty and TriMesh/triangular had zero identity matches; GEMM/Polly/LLVM had311. Original paper places GEMM under exposed LLVM. TriMesh has unresolved solution-quality and implementation-lineage issues. NGINX's archived dataset remains unadmitted: high-variation exclusions, differing prose/XML constraints and unresolved mapping to later four-version tables. See reports/admission_v104.md, results/v104_admission/summary.json. Metadata absence alone is not proof of code independence.

## Preserved model result and cost

V103 remains latest model-quality comparison: six exposed groups, seeds11/37, two Qwen3-8B modes,24conditions/36realrequests/240charged recorded acquisitions.22validfinals; two thinking fallbacks; no retries/timeouts/unattempted. Both modes had **zero valid>=5%wins over BOTH batch/sequential3NN**. Group-first mean gains vssequential:−7.64%thinking/−6.52%nonthinking; versusbatch−3.97%/−2.74%. Dune contributes much of mean loss. This is exposed-development evidence, not a universal harm claim. Prior failed feasibility attempts are preserved. See reports/reasoning_v103.md and reports/research_readiness_v103.md.

Cumulative realmodelrequests3,938; recorded-table acquisitions27,978. New NGINXnativeconfigurationattempts6/49,152HTTPresponses. Numerical native acquisitions790 unchanged; older native countsDuckDB78physical,H2299,Kanzi1265,RocksDB350 unchanged. V104 downloads4,361,631bytes; V1051,320,382bytes; cumulative9,875,903,117/10GiB, remaining861,515,123bytes. Modelpayload9,126,358,023/9GiB unchanged. Externalspend0. Native local body transfer1,610,612,736bytes is NOT internet download. Collection costs are separate from hypothetical deployment cost, which is not estimated for this failed feasibility screen. Missing historical tokens/electricity costs remain unknown.

## Next action

**Replace the single-process Python load generator with a bounded native or multiprocess byte-validating client, then freeze a new NGINX feasibility protocol.** Establish enough runtime, low client overhead and reference repeatability before optimization. Increasing requests alone may retain the client bottleneck. No paid service, new model or restart is needed for this next engineering step. Current six-attempt allowance is consumed; new native collection needs its own bounded protocol/output. No silent repeat of V105.

Still untested/unestablished: qualified NGINX tuning domain, any new NGINX LLM gain, enough untouched independent-system groups for learned-router evaluation, useful benefit-aware routing, and independent-machine replication. Q2 readiness is not established. Scientific honesty overrides finding positive results.

Safe saved-evidence replay:
```
.venv/bin/python scripts/report_nginx_v105.py
.venv/bin/python -m pytest tests -q
.venv/bin/python scripts/seal_nginx_v105.py --verify-only
```
Latest snapshot-aware seal: artifacts/study_v105/evidence_manifest.json. Prior root documents preserved under artifacts/study_v105/previous_snapshot/. V104 seal SHA8944f7372b6cdc02ba45d46370f771a852644a3ab1086d9db6322c2eb1f80568 verified43files/42historical checkpoints before V105. Rebuilding instructions: artifacts/study_v105/REPRODUCE.md. Do not overwrite old collection outputs or frozen binaries.
