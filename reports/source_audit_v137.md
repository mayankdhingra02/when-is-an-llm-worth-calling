# V137: outcome-blind independent-cohort admission audit

No new independent cohort is admitted. This is a source/feature audit, not an LLM experiment or a reason to call old systems held out. V138 separately completed the unblocked cheap-control experiment on exposed systems.

## Primary artifacts and identity

Owner [llesoil/input_sensitivity](https://github.com/llesoil/input_sensitivity/tree/aec6b95bb0587a9fb8584fb0a290099d28c5e393), revision `aec6b95bb0587a9fb8584fb0a290099d28c5e393`. The included owner paper is **Input Sensitivity on the Performance of Configurable Systems: An Empirical Study**, Luc Lesoil, Mathieu Acher, Arnaud Blouin and Jean-Marc Jézéquel. This is not the different paper *Learning input-aware performance models...* that initially led to the search. Title/authors verified in the owner's `JSS_Input_Sensitivity.pdf`; Table 1, measurement scripts and actual feature schemas checked. MIT license, copyright 2023 Luc Lesoil, retained verbatim in the source directory. The repository contains third-party input datasets; its root code license alone is not a blanket copyright grant for those inputs. No upstream code was executed.

Also inspected owner [ideas-labo/SeMPL](https://github.com/ideas-labo/SeMPL/tree/24eb83219ef78b5382cec88490e9de7ea000263b), revision `24eb83219ef78b5382cec88490e9de7ea000263b`, and [owner paper on arXiv](https://arxiv.org/html/2402.03183v1), Jingzhi Gong and Tao Chen, DOI 10.1145/3643743. Most listed software families overlap prior development families. Root tree did not supply a license file; do not infer repository rights from the paper. Its SPEAR table description needs reconciliation before task admission. No SeMPL outcome table was downloaded or measured.

## Pre-outcome screening contract

The explicit feature plan selected the first nonempty primary file in owner tree order for GCC, ImageMagick, Node.js, Poppler and XZ, without inspecting target values. Fixed minimum 40 distinct configurations follows the V116 coverage criterion and leaves at least half the domain unacquired at B20. Lingeling was excluded from this runtime-task search on metric semantics; SQLite and x264 remain previously exposed families.

`scripts/audit_features_v137.py` uses a named feature allowlist, exact schema checking and no objective conversions. Configuration IDs do not count as options. Poisoned objective fixtures verify that target contents cannot affect its output. Raw table bytes were downloaded for provenance, but numeric objectives were not inspected, summarized, ranked or supplied to any optimizer. These five downloads are not new measured evaluation acquisitions.

| System | Actual feature-only coverage | Admission decision |
|---|---|---|
| GCC | 80 distinct configurations; 32 after excluding `-Ofast` and fixing `-ffloat-store` absent | Conservative fixed-utility partition misses 40. Native correctness is also unverified. |
| ImageMagick | 100 distinct; 34 partitions when posterization, blur and quality are fixed; largest partition 6 | Options change requested output. No adequate fixed-output partition in inspected table. |
| Node.js | 50 distinct six-flag configurations | Coverage passes; numbered table-to-workload mapping unresolved. Not admitted. |
| Poppler | 16 distinct | Cannot support B20 unique acquisitions. |
| XZ | 30 distinct | Below the declared 40 threshold. Additionally `depth` header differs from generator's thread option; do not guess its meaning. |
| Lingeling | Not fetched | Conflict/reduction counts within ten seconds, not demonstrated solve-time or solved-instance utility. Wrong metric for this cohort. |
| SQLite / x264 | Not fetched | Related versions/workloads remain the same already exposed software groups. |

Coverage is measured only for the preselected representative file, not certified across every table in a family. GCC's notebook encodes boolean 0 as flag present and 1 as absent. Excluding the two named floating-point changes is conservative screening, not a proof that every retained configuration preserves utility. ImageMagick's measured size/time varies alongside blur/posterization/quality; faster or smaller can mean a different product. XZ's small sample is not enlarged by treating inputs as independent systems.

The owner paper's threats section explicitly says the entire measurement process was not repeated because of cost. Do not claim these stored values establish per-configuration noise or correctness. Reported revisions in Table 1 include GCC ccb4e07, ImageMagick 5ee49d6, Node.js 78343bb and XZ e7da44d; these are paper metadata, not independently rebuilt binaries.

## Node.js contract follow-up

The owner notebook launches Node.js 15.14.0 with six runtime flags and `benchmark/run.js all`. Retrieved owner's `listInputs.csv` and `listInputs.txt` list named selections, not a verified mapping from the 1,939 numbered primary CSV tables. Neither explicitly identifies `data/nodejs/0.csv`. They cannot justify choosing a target workload by inference from file ordering.

Retrieved original Node.js v15.14.0 `benchmark/run.js` and `benchmark/common.js` from nodejs/node. The former forks benchmark scripts; the latter explicitly forwards `this.flags.concat(process.execArgv)` when creating configuration children. This supports the intended flag-propagation path, but does not authenticate the historical collection or recover the missing index mapping. No downloaded JavaScript was run. These source excerpts are retained for private provenance review, not incorporated in experiment software or publicly redistributed.

Checked the owner `src/main/Clean_data.ipynb` code cells as a final mapping follow-up, without displaying saved outputs or executing it. Its Node.js section loops over already numbered CSV files and checks shapes; it does not construct an index-to-benchmark map. Its expected input count is 1,932 versus the paper's 1,939, another version mismatch to reconcile. A first-row missing-value check is not evidence of complete failure handling.

Precise missing evidence: the original preprocessing/index-to-benchmark map (or raw log with traceable mapping) connecting `data/nodejs/0.csv` to a named benchmark and its fixed workload parameters, plus clarification of recorded failure handling. More than one new family would still be needed for meaningful grouped held-out controller evaluation. There is no pending paid service or permission request.

## Exposure, cost and reproducibility

Scanned the pre-extension manifest of 34,112 result JSON/JSONL/Markdown/text files, 1,757,721,567 bytes, without converting objective values. Name-based matches identify no GCC, ImageMagick, Lingeling, Node.js, Poppler or SPEAR entries. XZ's two hits are prior admission metadata and a library path, not a found XZ optimization run; DeepArch has three admission-only hits. This is a limited name-based check, not a proof about deleted, external or unnamed history. Variants would still be grouped by software lineage. The explicit-regex recheck reproduces all hit counts; use `exposure_recheck.json` as the authoritative pattern representation (the initial manifest serializes escaped pattern text ambiguously).

Actual saved source bytes: **7,059,029**, within the 20,000,000-byte stage cap. Six bounded owner retrieval stages retain URLs, sizes, SHA256s and timings in `artifacts/sources/v137/`. Owner repository blobs also match their pinned Git tree hashes. Node.js files are pinned by tag URL plus downloaded SHA256. No model requests, native executions, target acquisitions, paid/cloud spend, contacts or publishing occurred in V137.

Plans: `artifacts/study_v137/{source_plan,docs_plan,source_code_plan,feature_plan,node_contract_plan,cleaning_plan}.json`. Evidence: owner identities/trees/docs under `artifacts/sources/v137/`; code-only notebook extractions, paper text, `coverage.json`, `exposure_scan.json` and `exposure_recheck.json` under `artifacts/study_v137/`. Recheck coverage with `.venv/bin/python scripts/audit_features_v137.py`; no network or target acquisition. Fetch commands are create-once and should not be rerun on resume.

The admission bottleneck is usable task semantics and independent groups, not RAM or an inference outage. Do not relax coverage, silently optimize output quality away, or treat the same system's workloads as independent families to obtain a favorable result.
