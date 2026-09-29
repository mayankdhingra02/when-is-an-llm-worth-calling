# Status — 2026-09-24, v5 registry expansion and finite-domain preparation

## Current state

Continued the requested source/identity audit beyond MOOT. **81 CSV tables audited; 22 broader-schema candidate software families identified; 37 tests pass.** No new-system objective values were inspected and no new model calls or objective acquisitions occurred. This advances the data route to a larger evaluation; it does not admit 22 tasks or complete the larger study.

Read [reports/registry_v5.md](reports/registry_v5.md), data/registry_v5.json, artifacts/registry_v5/admission_review.json, then relevant new code. The last measured optimizer results remain [reports/pilot_report_v4.md](reports/pilot_report_v4.md) and [reports/pilot_report_v3.md](reports/pilot_report_v3.md). The v4 design/freeze is unchanged. Its full prior status is saved at artifacts/history/STATUS_v4_before_expansion.md. Do not reread the supplied literature synthesis without a specific need.

## What actually ran this continuation

- Pinned owner metadata and downloaded 34 additional source CSVs: 11 DeepPerf, 11 VEER, 12 Performance Evolution, plus feature models, README/workload notes and four primary papers. Original MOOT 47 tables remain pinned. No upstream code, installers or model was executed.
- Ran the outcome-blind registry builder. It parses explicit feature cells, objective headers and declared revision/workload metadata, never objective payloads. All data/document payload hashes and Git blob IDs verified.
- Established **14 exact feature correspondences** between MOOT and named-source tables, using normalized names plus complete distinct feature matrices. These do not assert equality of objective payloads or transformations. Additional family mappings are explicitly based on primary paper metadata.
- Resolved rs/sol/wc workload families to **Apache Storm**, so they cannot count as independent systems. MOOT SS-B/H map to hardware design cases and are excluded. HSMGP is a multigrid program, not the later “Hazardous Software Management” description. HSMGP/DUNE, BDB-C/J, VP8/VP9 and MySQL/MariaDB are conservatively grouped as related families.
- Kept all Apache HTTP Server, SQLite and x264 variants excluded from new evaluation, including MOOT SS-N/U. Storm is distinct from Apache HTTP Server.
- Feature-model verification initially failed on **Fast Downward**: CSV option `disjunctiveLMs` is absent from its supplied feature model. Preserved failure, quarantined case, did not delete the column. Eleven other Performance Evolution model/header checks pass. Preliminary 23 broader candidates became **22** after this check.
- Implemented a separate **finite-domain nominal optimizer core** with explicit domains, modal centroids, deterministic acquisition/ties, uniform proposals and checked index encoding. Numeric-looking levels are treated categorically; ordinal distance is ignored. This is tested preparation, not a completed numeric study or local-model adapter.
- **37 synthetic tests passed**, including objective invariance, alias grouping, schema mismatch rejection, finite codecs, inclusive budgets and binary compatibility. Independent registry verification passes. New finite optimizer tests remain synthetic and do not enter measured aggregates.

## Candidate breadth and remaining admission issues

Only **five** families satisfy unchanged v4 schema rules: BerkeleyDB, DeepArch, HSQLDB, LLVM, OpenVPN. With explicit primary-target selection, eleven families have compatible binary feature/size schemas. Under a proposed amended limit of 64 finite features and 200,000 rows, **22 candidate families** remain:

7zip, BerkeleyDB, Brotli, DConvert, DeepArch, DUNE/HSMGP, ExaStencils, HIPAcc, HSQLDB, JavaGC, libvpx, LLVM, lrzip, MongoDB, MySQL/MariaDB, OpenVPN, Opus, PostgreSQL, Redis, SaC, Storm, Z3.

These are schema/identity candidates, **not admitted evaluation groups**. Each requires a semantic target/direction, valid workload/revision and original transformation/provenance review. No final development/test split exists. Specific hazards:

- OpenVPN `performance` is throughput: maximize it, rather than infer minimization from the column name.
- Some throughput/obj1/obj2 descriptions differ between source papers, MOOT and VEER. Do not guess transformations or let unselected objectives become features.
- MariaDB's lexicographically first CSV revision 10.0.17 overlaps the README's reported crashing-release gap; resolve or select a documented valid representative before outcomes.
- Z3 is filtered to LRA before schema inspection; workload is not tunable.
- VEER SS-C has eleven anonymous features, inconsistent with the paper's five-option description. It and MOOT SS-L/P remain unresolved.
- Source license evidence varies: VEER MIT, Performance Evolution GPLv2 repository license, DeepPerf no top-level license found. No third-party code reused, no publication; original data-specific provenance remains explicit review work.

The broader feature limits/nominal treatment are proposed preparation and **do not silently alter v4**. A real finite-domain LLM adapter, final admitted manifest, amended protocol and full larger collector remain unimplemented/unexecuted. Current 20-group resource plan still needs 203 calls versus 34 remaining; no additional allowance has been authorized or applied.

## Evidence and reproduction

| Evidence | Location |
|---|---|
| Current source audit / findings | reports/registry_v5.md |
| Versioned registry / per-case fields | data/registry_v5.json |
| Per-family admission review, no split | artifacts/registry_v5/admission_review.json |
| Owner commits and source/paper hashes | artifacts/registry_v5/metadata.json, sources.json, papers.json |
| Actual audit logs | artifacts/registry_v5/metadata_fetch.log, data_fetch.log, paper_fetch.log, build.log |
| Schema verification / preserved failure | artifacts/registry_v5/verification.json, verification.log, verification_initial_failure.log |
| Tests / repeatability | artifacts/registry_v5/tests_final.log, reproducibility.log |
| Feature audit and preparation code | src/escalation/registry_v5.py, finite_domain.py; tests/synthetic/test_registry_v5.py |
| Previous actual measurements | results/v3/, results/v4_projection_diagnostic/ |
| Frozen v4 design, unchanged | reports/protocol_v4.md, protocol_v4.freeze.json |

```sh
.venv/bin/python scripts/fetch_registry_v5_metadata.py
.venv/bin/python scripts/fetch_registry_v5_data.py
.venv/bin/python scripts/fetch_registry_v5_papers.py
.venv/bin/python scripts/build_registry_v5.py
PYTHONPATH=src .venv/bin/python -m pytest -q
.venv/bin/python scripts/verify_registry_v5.py
```

Fetchers reuse pinned cached commits, verify payloads and preserve the persistent download guard. Data in data/registry_raw_v5 and original source/paper downloads are Git ignored. Registry building/tests acquire no outcomes. The v5 snapshot is an audit/prototype freeze, not a claim of full-study readiness.

## Unchanged measured findings and costs

The v3 pilot completed 30 classical arms and 15 real local-LLM continuations. LLM materially helped versus centroid in 2/15 and hurt in 3/15; the benefit router selected no x264 calls. The v4 projection-only diagnostic completed 15 continuations and had lower mean loss than the LLM on Apache/x264, while the LLM was better on SQLite. x264's projection advantage is dominated by one seed. No generalization advantage has been established and no controller was refitted after that diagnostic.

- **1,658 historical charged label accesses**, unchanged.
- **66/100 follow-up request attempts**, 34 remaining; **166 historical attempts** including v1, unchanged. Zero new requests this session. Unknown historical timeout/interruption usage remains unknown.
- Experiment/analysis runtime **1,157.2992/1,800 seconds**, about **642.7008 seconds remaining**, unchanged. Ledger artifacts/resource_ledger_v2.json is inactive. This source audit/download/test overhead is separate from measured experiment time.
- Accounted downloads **1,412,812,979 bytes**, within 5 GiB; model bytes remain **999,602,607**, within 4 GiB. Download ledger is authoritative.
- **USD 0 external spending**. No new installation, model, paid endpoint, cloud, credentials, push, publication or author contact. No background experiment/model worker. Original locked environment unchanged; local Git files remain uncommitted, no remote.

## Single most important next action

**Complete semantic objective and valid-revision admission for the 22 candidate families, then freeze a finite-domain model interface and final grouped manifest.** The count is now plausible, but spending the remaining model calls before these validity checks would not produce a credible larger evaluation. Finalize the full collector and a concrete explicit larger resource allowance only after data admission. No work is scheduled outside this session.
