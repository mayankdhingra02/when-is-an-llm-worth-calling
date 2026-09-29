# STATUS — V104 admission complete; NGINX next

Resume here. V103's completed model experiment remains the latest optimization result. V104 executed an objective-blind independent-system admission audit, with zero new model requests, objective acquisitions or native workloads. No job remains running and no inference is queued.

## Latest concrete result

28,078 historical result/report/configuration and top-level manifest files inventoried and hashed. NGINX/OpenResty:0identitymatches; TriMesh/triangular:0; GEMM/Polly/LLVM:311. GEMM belongs to the already-exposed LLVM group. TriMesh's iteration timing under varying solver/geometry settings does not establish equal final solution quality, and its implementation lineage is unresolved. NGINX is a plausible unused group but its recorded outcomes are not admitted: the original author artifact excludes high-variation cases, has conflicting prose/XML constraints, and its mapping to DHDA's four purported versions is unresolved. Four versions would still be one group.

Read reports/admission_v104.md and configs/admission_v104.json. The raw metadata, license, paper and source-inventory evidence is in artifacts/sources/v104/; executable audit result in results/v104_admission/summary.json. Frozen protocol: reports/protocol_v104.md and .freeze.json. No hidden candidate objective table was downloaded or inspected. Selection used identities/source availability, not LLM benefit.

Eight retained owner blobs match pinned Git object IDs. One arXiv v1 PDF request failed406 and is recorded; the original paper was read through the web tool, with no successful local download claimed. No upstream code executed. Ten new synthetic integrity tests passed; they are not measurements. Full suite790passed in20.99s; deterministic audit replay matched. Logs in artifacts/study_v104/. Historical root documents are preserved under artifacts/study_v104/previous_snapshot/. Latest snapshot-aware seal: artifacts/study_v104/evidence_manifest.json.

## Preserved V103 result

Six exposed groups; seeds11/37; two modes;12sharedprefixes/24conditions. Qwen3-8B Q4_K_M at128thought+128finaltokens versus128nonthinking tokens.36requests/36responses,22validfinals,2thinking fallbacks,0retries/timeouts/unattempted. Thinking10/12valid; nonthinking12/12valid. Zero valid>=5%wins over BOTH batch/sequential3NN for either mode. Group-first mean gains against sequential:−7.64%thinking/−6.52%nonthinking; versusbatch−3.97%/−2.74%. Dune dominates much of mean loss; no population claim.

240charged recorded-table acquisitions, logicalB20 per arm withshared10prefix.936.011s lifecycle, peakRSS8,356,478,976bytes,exit0.2,122generated/60,806prefilltokens. No new native workload. Full result and figure: reports/reasoning_v103.md and results/v103_analysis/. Prior seal SHA2aa01c226e4aceeaea71d8d6224848628d7ad12bfcf8d7c9abe1af966c77f351 verified136files and41historical checkpoints before V104. Original failure attempts V98–V102 preserved.

## Cumulative accounting

Real model requests3,938; recorded-table acquisitions27,978; numerical native acquisitions790(V94/V96/V97). Older native counts unchanged: DuckDB78physical,H2299,Kanzi1265,RocksDB350. V104 downloaded4,361,631persistedHTTPbodybytes, making cumulative9,874,582,735/10GiB and remaining862,835,505bytes. Modelpayload9,126,358,023/9GiB unchanged. Externalspend0; electricity/hardware costs unknown. Historical missing token usage remains unknown. No new request or objective allowance consumed.

## Next action and replay

**Pin official NGINX source and implement a fixed-response local validator, then freeze a bounded native reference/contrast/reference feasibility run before timing.** See reports/next_experiment.md. This requires no new external service or paid model. All NGINX variants/seeds must remain one development group. Archived-data admission and broad independent-group evaluation remain unresolved; no Q2-readiness assertion. Do not chase a positive result on exposed data.

Safe replay with no inference/new objective access:
```
.venv/bin/python scripts/audit_admission_v104.py --verify-only
.venv/bin/python -m pytest tests -q
.venv/bin/python scripts/seal_admission_v104.py --verify-only
```
Do not overwrite historical collection outputs. Use the latest snapshot-aware seal after root-document updates. Native NGINX, new independent model comparisons, a useful benefit-aware controller, and independent-machine replication remain untested.
