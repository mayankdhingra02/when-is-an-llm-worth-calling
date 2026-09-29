# Attribution

The independently implemented centroid optimizer is adapted from Srinivasan & Menzies, Better Together, in the Right Order (arXiv:2607.02583v1), Algorithm 1, and informed by inspection of Tim Menzies's EZR v0.9.4 (MIT). It is not a verbatim vendored EZR release. See reports/source_audit.md for differences.

MOOT CSVs: Tim Menzies and contributors, github.com/timm/moot, commit recorded in data/manifest.json; repository MIT license. License text is fetched to artifacts/sources/moot_LICENSE.md. Original dataset provenance is described by MOOT; exact machine/workload versions are unresolved.

Qwen2.5-0.5B-Instruct: Qwen Team, official Hugging Face owner Qwen, Apache-2.0. Model license and metadata are stored with local weights and hashes in artifacts/model_manifest.json. Weights, downloaded papers and original CSVs are ignored by Git. No upstream execution scripts or remote model code were run.

Python dependency versions are in requirements.lock.txt; their licenses remain with the installed distributions. No assertion of ownership of third-party data or weights.

## V4 registry extension

47 MOOT tables from the same pinned commit were retrieved for outcome-blind schema/identity auditing. Per-file URLs, SHA-256 and Git blob IDs are in artifacts/registry_v4/sources.json and data/registry_v4.json. Raw tables in data/registry_raw are Git ignored. Repository MIT licensing is recorded; original workload/row lineage is not assumed verified.

PromiseTune owner README at commit f614bc482e8cdd7b266ffefbf9989748f8a06e7e was inspected only for system identity/lineage. Source URL and hash are in artifacts/registry_v4/lineage.json. No code was reused or executed and no dependency was installed. Its downloaded README is excluded from Git; this project does not assert a reuse license for that repository. The independent uniform projection control is original project code.

## V5 primary-source expansion

Pinned repositories and downloaded file hashes are in artifacts/registry_v5/metadata.json and sources.json; author-hosted paper hashes are in papers.json. DeepPerf and VEER contribute original source tables; Performance Evolution contributes tables, variability models and workload notes. SPLConqueror metadata was inspected but its algorithms were not executed or reused. VEER declares MIT, Performance Evolution and SPLConqueror declare GPL version 2, and no top-level DeepPerf license was found in the pinned inventory. These are repository declarations, not a claim that all original data-specific rights/lineage are established. Raw data, papers and source documentation remain Git ignored. New registry/finite-domain code is independent project code. No publication or distribution occurred.

## V46–V48 local model/runtime extension

SmolLM3-3B: HuggingFaceTB, Apache-2.0. The downloaded Q4_K_M conversion is
published by ggml-org and linked from the original owner's SmolLM3 collection.
Exact conversion revision: 4965cb60b150737b68a0408c36aeefb65078f894;
GGUF SHA256: 8334b850b7bd46238c16b0c550df2138f0889bf433809008cc17a8b05761863e.
The conversion's model card does not identify an exact original-weight revision;
byte-level reproduction of the downloaded conversion is pinned, while that
upstream conversion lineage remains incomplete. Model card and publisher API
metadata are in artifacts/study_v46. Weights remain excluded from Git.

llama.cpp: ggml authors, MIT; official macOS ARM64 build b11146, commit prefix
7fe450e19. Runtime archive SHA256:
1ad3f9eff80edb9dbef4259ad564d1720612ef7eea48fa4afed0e54f5f3d5711.
License retained at artifacts/study_v46/runtime_LICENSE. Project-local runtime
is in .local-runtime (Git ignored). No system-wide installer was executed.

Primary publisher links: https://huggingface.co/HuggingFaceTB/SmolLM3-3B,
https://huggingface.co/collections/HuggingFaceTB/smollm3,
https://huggingface.co/ggml-org/SmolLM3-3B-GGUF,
https://github.com/ggml-org/llama.cpp/releases/tag/b11146.

## V55–V56 planning source and task

Fast Downward, owner aibasel/downward, release-24.06.1, commit
1eef26b2cbf599a1894606aa898d9d49e1034cb9: GNU GPL version3 or later, as declared
in pinned README.md. Owner C++/Python files were compiled/executed unchanged;
source-tree-to-archive check and local binary hashes are in artifacts/study_v55.
Planner reference: Malte Helmert, The Fast Downward Planning System, JAIR26,
191–246 (2006). This is a modern-version adaptation, not reproduction of old
PerformanceEvolution timings. Runtime/source archive remains Git ignored.

Benchmark owner aibasel/downward-benchmarks, commit
e21d49c2cb61d147a46c5966f2581bf6fd422b9f: data-network-opt18-strips/domain.pddl
and p05.pddl. Domain credits Manuel Heusner, Florian Pommerening and Alvaro
Torralba. Owner labels repository an unofficial IPC collection. Dataset-specific
redistribution license is unresolved; local PDDL payloads remain ignored, and
no publication/distribution is authorized. Per-payload URLs and hashes are in
artifacts/sources/v55/manifest.json. The new limited STRIPS/cost validator and
experiment wrappers are independent project implementations, not copied VAL code.

## V57 workload expansion

Additional data-network-opt18-strips p01/p10/p20 PDDL files from the same pinned
aibasel/downward-benchmarks e21d49c2cb61d147a46c5966f2581bf6fd422b9f owner tree.
Exact URLs/hashes in artifacts/sources/v57/manifest.json. Dataset redistribution
rights remain unresolved; local-only payloads. Xalan small/large are declared
sizes in the already pinned DaCapo9.12-MR1 jar's cnf/xalan.cnf, not newly sourced
benchmarks. No new third-party code was copied for the exit-waiter or ID-order
sensitivity tools; previous runtime/harness/algorithm attributions remain.


## V60/V61 Redis source and benchmark adaptation

Redis owner source release7.2.11, commit d4c381df7a729c06a5207c4f18d804febe956dc4;
BSD-3-Clause COPYING retained in the project-local source tree. Archive and binary
hashes: artifacts/sources/v60/manifest.json and artifacts/study_v60/build*.json.
The benchmark client adds expected-reply type/length/byte checks and a count receipt;
original C source and exact patch are in artifacts/study_v60/. Server code unchanged.
Redis/hiredis and other bundled source licenses remain in the downloaded tree;
no third-party archive or binary is being published. Workload inputs are generated
by project code. External benchmark guidance: https://redis.io/docs/latest/operate/oss_and_stack/management/optimization/benchmarks/ .

## V62–V64 MiniSat compatibility adaptation

Owner https://github.com/niklasso/minisat , commit37dc6c67e2af26379d88ce349eb9c4c6160e8543.
MIT LICENSE attributes Niklas Een and Niklas Sorensson. Original source archive,
license, source manifest and generated binary hash retained under local runtime /
artifacts/sources/v62/ and artifacts/study_v62/. Two compiler-compatibility declaration
fixes are preserved with original files and a patch; solver search code unchanged.
Uses installed system zlib and macOS SDK. Generated planted-CNF workloads and
independent solution validator are project code, not a downloaded competition dataset.
No redistribution, remote publication or author contact has occurred.
