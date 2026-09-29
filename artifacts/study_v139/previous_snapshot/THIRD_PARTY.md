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


## V66/V67 additional project-local runtimes

- DuckDB1.3.2 official PyPI CPython3.10 macOS ARM64 wheel, SHA pinned in
  artifacts/sources/v66/manifest.json and configs/runtime_v66.lock.json. MIT,
  Copyright2018–2025 Stichting DuckDB Foundation; owner LICENSE/README retained.
  Binary reports source identifier0b83e5d2f6. Installed without dependencies into
  .local-runtime/candidates-v66/duckdb, leaving prior environment locks unchanged.
- GNU coreutils9.7 sort, https://ftp.gnu.org/gnu/coreutils/coreutils-9.7.tar.xz.
  GPL version3 or later, source COPYING and per-file headers retained in owner
  archive. Source/compiled binary hashes recorded; detached signature downloaded
  but not independently key-verified. Generated build prerequisites built before
  src/sort, no algorithm-source patch or system installation.
- OpenJPEG2.5.3, owner commit210a8a5690d0da66f02d49420d7176a21ef409dc,
  https://github.com/uclouvain/openjpeg/tree/210a8a5690d0da66f02d49420d7176a21ef409dc.
  BSD2 with owner/contributor notices preserved. PGM/J2K codec built locally;
  optional PNG/TIFF/LCMS support disabled. No algorithm-source patch. Generated
  grayscale workloads and validators are project code, not upstream benchmark data.

No publication or redistribution was performed. Downloaded owner code/binaries
remain project-local and are not assumed to share this project's code license.


## V68 source inspection and YCSB value-recipe adaptation

- YCSB0.17.0, owner brianfrankcooper/YCSB, commit
  4b19340e3bab5e4c88eda75ad56e83dc4d5cc503. Apache-2.0 LICENSE.txt and
  per-file notices retained under artifacts/sources/v68/ycsb/source/.
  src/escalation/ycsb_contract_v68.py reimplements the deterministic value recipe
  in CoreWorkload: Copyright(c)2010 Yahoo! Inc.,(c)2016–2017 YCSB contributors.
  The Python adaptation adds strict field/key completeness and status validation;
  no owner Java code was compiled or executed. Source attribution retained.
- CMU BenchBase, commit33c00473807ebd49304d114a6d769d2d2b2bbb34, Apache-2.0,
  OLTPBenchmark Project notices retained. Source inspection only.
- PKU-DAIR/KnobsTuningEA, commit13290f8dcef965a62820c41b74af097b93dd54a5.
  No LICENSE/COPYING or reuse license found in complete pinned tree/inspected setup.
  Read-only provenance inspection; no downloaded code executed or incorporated,
  no training data fetched or redistributed, no license presumed.

Owner source URLs/bytes/SHA256 are recorded in artifacts/sources/v68/manifest.json.
No publication, remote push or author contact occurred.


## V69 native RocksDB binding and YCSB request-generator adaptation

RocksDict0.3.27, owner rocksdict/RocksDict commit
350884b4e8f30df1f155261994f97f8768b64167, MIT Copyright(c)2021Congyu.
Official PyPI CPython3.10macOSARM64 wheel installed project-locally without deps;
registry SHA/binary hashes in configs/runtime_v69.lock.json. Source build not reproduced.
Rust binding commit66ff53024bb6291800aa313ec5780fc1e23c9ce7, Apache2 license retained.
RocksDB source44e95d8af5d7ec503b3f1d5754c3379ab6c29a9d/version9.8.4, owner Apache2
license retained; native LOG agrees with source version, not proof of bitwise build.
Sources/licenses:artifacts/sources/v69/ and artifacts/sources/v69_repair/.

The request generator in src/escalation/rocksdb_v69.py adapts YCSB0.17.0's
ScrambledZipfianGenerator/ZipfianGenerator/FNV recipe, Apache2, Copyright2010–2016
Yahoo! Inc. and2017YCSBcontributors. Pinned upstream source and V68LICENSE preserved.
Python RNG, record layout, scale and binding differ; no Java benchmark replication
is claimed. No third-party code/model/artifact was published or remotely pushed.


## V73 ICSE2023 workload artifact: source-only inspection

Owner https://zenodo.org/records/7658046 (version1.2), Mühlbauer et al., Analyzing
the Impact of Workloads on Modeling the Performance of Configurable Software
Systems. Metadata, paper, documentation, selected configuration-only samples,
feature model and two shell-script bodies were retrieved. No upstream code ran
or was incorporated into the experimental runtime. Raw source artifacts remain
outside shareable history under the existing artifact policy. Zenodo specifies
CC BY4.0; the included license heading says CC BY-SA4.0 but links to CC BY4.0.
Terms are recorded as discrepant, not resolved. Program licenses are separate.
Partial ranges/member CRCs/SHA256 hashes are saved; full archive MD5 is unchecked.
See reports/admission_v73.md.

## V74 Kanzi owner-source runtime and compiler

Kanzi1.9.0, flanglet/kanzi commit9828b05815b754f1ae40acd83552605885ba515b,
Apache-2.0, owner LICENSE retained in extracted source and built JAR. All113Git
blobs checked against owner tree. Header layout/constants adapted with attribution
in src/escalation/kanzi_v74.py. This fresh owner build does not resolve the V73
archived dataset's license discrepancy or imply reuse of its measurements.
Eclipse ECJ3.32.0 from Maven Central, Eclipse Foundation, EPL-2.0 per preserved
POM and compiler archive. SHA1registry check plus SHA256 pin. Existing local
Temurin17runtime reused; no system install. Source archive/compiler/JAR retained
locally only; no publishing or remote push. See reports/kanzi_v74.md.

## V76/V77 isolated Kanzi buffer repair

Apache-2.0 Kanzi1.9 owner source is retained unchanged under kanzi-v74.
The separate kanzi-v76 copy changes final compressed-block emission to read
ByteArrayOutputStream's current backing buffer through an added accessor.
Full diff: artifacts/study_v76/buffer_fix.patch. Patch/adaptation identity and
source/JAR hashes: configs/runtime_v76.lock.json. Original owner LICENSE remains
in the patched JAR. This is not an upstream release or a claimed novel reported
bug; no author contact or redistribution occurred. Original decoder recovered
the patched diagnostic output byte-exactly. V77 uses this adaptation explicitly.

## V87 DuckDB runtime and pending generator

DuckDB1.4.4 CPython3.10 macOSARM64 wheel, owner-linked PyPI, SHA2565e1933fac5293fea5926b0ee75a55b8cfe7f516d867310a5b251831ab61fe62b. Core MIT license retained at `artifacts/sources/v87/DUCKDB_LICENSE`; installed only under `.local-runtime/duckdb-v87`. No wheel/binary redistribution in the V86 analysis bundle.

The owner’s `extension/tpch/dbgen/LICENSE` at v1.4.4 is a separate TPC EULAv2.2; exact text retained at `artifacts/sources/v87/DBGEN_LICENSE`. User approval requested before generator installation/use. TPC-H extension remains not installed/not loaded; no generated data or native benchmark trials. Core MIT attribution does not establish generator redistribution rights. Protocol labels any future scaled query subset an adaptation, not officialTPC-H results. No upstream code source was modified or executed as an installer. See `reports/duckdb_readiness_v87.md`.

## V88 real-flight workload

nycflights13 Python data port0.0.3 by Michael Chow, original nycflights13 by Hadley Wickham: CC0 as declared in the [registry](https://pypi.org/project/nycflights13/0.0.3/) and [owner project](https://nycflights13.tidyverse.org/). Archive SHA256d9ef2f5cf1bebca7e30b4daf69dcd7a8fd71f25b7196f5dc489879ad7e3e8a37. Only allowlisted data/metadata extracted; package code neither installed nor executed. Records at `artifacts/sources/v88/`, metadata at `data/flights_v88/PKG-INFO`. Custom queries and independent Python reference are project implementation, not an owner benchmark reproduction. Reuses MIT DuckDB1.4.4 pinned in V87; no TPC extension/generator/license acceptance.

## V91 Qwen3-8B owner GGUF

Qwen/Qwen3-8B-GGUF, revision `7c41481f57cb95916b40956ab2f0b139b296d974`, Apache License 2.0, Copyright 2025 Alibaba Cloud. File Qwen3-8B-Q4_K_M.gguf, 5,027,783,488 bytes, SHA256 `d98cdcbd03e17ce47681435b5150e34c1417f50b5c0019dd560e4882c5745785`. Exact revision LICENSE, README and pointer are retained in `artifacts/sources/v91/`; receipts and model manifest in `artifacts/study_v91/`. [Owner repository](https://huggingface.co/Qwen/Qwen3-8B-GGUF). Existing MIT llama.cpp b11146 was reused; no downloaded setup code or shell installer was executed.

## V94 numerical engines and inputs

SciPy1.13.1 / bundled SuperLU6.0.1 (BSD notice) and highspy1.7.2 / HiGHS (MIT) are used locally. The owner PyPI macOS arm64 CPython3.10 wheel is SHA-verified and installed only in `.venv`. Official HiGHS MIT text, version-pinned source, wheel metadata, and matrix fetch receipts are in `artifacts/sources/v94/`. HB/orsreg_1 is credited to R. Grimes and SuiteSparse collection editors; 25fv47 comes from owner HiGHS v1.7.2 tests. Standalone upstream data redistribution terms are not established by engine licensing; no public redistribution is authorized here. See `reports/source_audit_v94.md`. No downloaded shell installer or system-wide package change.

## V95 inference-mode source audit

Uses the existing Qwen-owned Qwen3-8B-GGUF model/revision and pinned owner README from `artifacts/sources/v91/README.md`; no new model or package download. Sampling settings follow that README's mode-specific guidance, with explicitly shorter output limits and control-prefix adaptation. llama.cpp b11146 endpoint documentation was checked for `/apply-template` and `stop_type`; see `reports/protocol_v95b.md`. The preflight failure and missing response are preserved, not reconstructed as model output.

## V96 SuperLU diagnostic sources

Fetched only SciPy v1.13.1 bundled SuperLU `SRC/util.c` and `SRC/sp_ienv.c` from the owner repository (16,060 bytes). Both carry the Regents/Lawrence Berkeley BSD notice. Saved files and SHA256 receipts are in `artifacts/sources/v96/`; Git blob hashes match the earlier pinned source tree. No native library was patched or new package installed. See `reports/source_audit_v96.md`.

## V97 restricted-domain follow-up

Reuses the pinned V94 matrix/SciPy binary and V91 owner Qwen3 GGUF with the existing llama.cpp runtime. No downloads, new dependencies or modified third-party code. Dataset/model hashes are restated in the V97 freeze; earlier source attribution and unresolved standalone dataset redistribution terms remain applicable.

## V98 bounded reasoning adaptation

Existing Qwen3 owner weights, llama.cpp b11146 and recorded datasets reused; no download or package changes. Primary verification of Muennighoff et al., s1: Simple test-time scaling, arXiv2501.19393v3, author repository, and pinned llama.cpp endpoint documentation informed the explicit two-phase procedure. No s1 code/model/data was copied or executed. Budget forcing is prior work, not claimed novelty; see `reports/source_audit_v98.md`.

## V104 source-admission metadata

DHDA (Zezhen Xiang, Jingzhi Gong, Tao Chen), owner ideas-labo/dhda revision7b1cc01246e615a4477209de72657f5786f42a43: GPL-3.0 text preserved in artifacts/sources/v104/dhda_LICENSE.txt. TwinsOrFalseFriends (Max Weber, Christian Kaltenecker, Florian Sattler, Sven Apel, Norbert Siegmund), revisiona31a1c0411f667728ee5069ae71f2927e6c146c6: GPL-2.0 text preserved in twins_LICENSE.txt. Only papers, documentation, license, file inventories and NGINX feature model were retained; no downloaded code executed or measured tables acquired. Owner Silver Bullet feature models were inspected as source metadata; no explicit redistribution license established. Scientific papers retain their own terms. See source manifest for all URLs/hashes and the failed arXiv request. No algorithm implementation copied.

## V105 native NGINX

NGINX1.28.3, official owner archive https://nginx.org/download/nginx-1.28.3.tar.gz, SHA2562c96a946bfb0882a21744ed429770a2123ae1828c7c48665092993ddee91a918. Copyright Igor Sysoev/Nginx, Inc.; complete two-clause BSD-like LICENSE retained at artifacts/study_v105/NGINX_LICENSE.txt and in the preserved source archive. Built unmodified source project-locally; no system installation. Official configure documentation archived solely as build reference. Source/docs download ledger in artifacts/sources/v105/manifest.json. The local loopback workload and validation client are this study's adaptation, not the original paper's archived hardware/workload reproduction.

## V106–V113 native validation extension

Project-authored C byte-validating clients and Python measurement wrappers reuse the unmodified pinned NGINX1.28.3 binary and V94numerical solver inputs/versions. No new download or third-party installation. Platform-option audit used the pinned NGINXDarwin/kqueue source and official ngx_core/ngx_http_core module documentation; platform-inactive knobs were excluded prospectively from V108's feature-only domain. No archived NGINXobjective labels were acquired.

The private local V113replication packet copies the fixed inputs, project certificate/worker code and HiGHSlicense. The standaloneHB/orsreg_1dataset redistribution terms remain unresolved; the packet is not represented as a license-cleared public artifact and was not uploaded. OriginalV94owner provenance and license qualifications remain applicable. No model weights are in that packet. All current confirmations are real native executions; V112parser fixtures are synthetic tests only.

## V114–V115 fixed-prefix replication

Reuses the existing owner Qwen3-8B-Q4_K_M model, llama.cpp b11146, pinned V41 recorded sources and V103 nonthinking interface. No new package, source, dataset or model download. Thirty-six new real model responses were collected; the classical portfolio is project-authored and is not an upstream SNAP2/EZR implementation. Original licenses, dataset redistribution qualifications and source/group provenance remain unchanged. Metadata-only consideration of owner Zopfli/OptiPNG documentation did not admit or execute a new workload.

## V116 original Storm provenance recovery

Read-only source audit of dice-project/DICE-Configuration-BO4CO at c94d9ad23e1cc4e9009a70cee23cbb42f122b5be. Eleven source/document blobs verified against the complete Git tree. No upstream code executed or incorporated into a benchmark. Owner LICENSE.txt calls itself FreeBSD but includes three conditions including non-endorsement; full text preserved at artifacts/sources/v116/bo_license.txt. Source license is not inferred to cover the separate Zenodo dataset DOI10.5281/zenodo.56238. That archive was not downloaded or redistributed. Existing pinned CM-CASL metadata and MOOT feature tables were reused for admission checks only. V117 only reuses our existing measured traces, with no new third-party payload.

## V118 owner archive follow-up

The separate original BO4CO dataset deposit DOI10.5281/zenodo.56238 was subsequently retrieved under a new frozen1MiB allowance. Zenodo API metadata explicitly declares BSD-3-Clause; its139425-byte ZIP matches published MD5c84ef2ba1d2e2500affa80b72ee38d98. Source metadata/archive hashes and URLs are retained under artifacts/sources/v118. CSV configuration features only were converted for lineage checks, with no target conversion/scoring, code execution or publication. This resolves the deposit-license uncertainty left by V116, not measurement/validation provenance or licenses of unrelated HB data.

## V119–V120 recorded-table selection and constrained inference

Reuses the exact original BSD-3-Clause BO4CO owner-deposit member `bo4co_dataset/wc-5d-c5.csv` (DOI10.5281/zenodo.56238; member SHA2562bc21f2ae4087b4e924c6f2f5f3744384b217b345653a4ee36526bd437bafae4). Configuration features and acquired latency labels were used under a separately declared published-label scope; upstream measurement/correctness uncertainty remains. No upstream harness was executed. Existing Qwen3-8B Q4_K_M/llama.cppb11146 model/runtime provenance and licenses are unchanged. Project-authored V91 constrained adapter was reused as an adaptation. No new third-party downloads or installations.

## V121–V122 owner MongoDB data and cached-output projection

TwinsOrFalseFriends owner AI-4-SE, pinned revisiona31a1c0411f667728ee5069ae71f2927e6c146c6: six MongoDB/ExaStencils README, FeatureModel and measurement blobs downloaded and Git-object verified. Repository GPL-2.0 text remains artifacts/sources/v104/twins_LICENSE.txt. MongoDB original performance data used locally under a disclosed fixed-contract recorded-label scope; ExaStencils target values were not converted or acquired. Owner measurement/runtime metadata does not certify original per-run correctness. The private standard-library replay includes MongoDB source and license; no public redistribution or upload occurred. Model/runtime licenses and provenance unchanged. V122 is project-authored feature projection of preserved real Qwen3 responses, not third-party code or a fabricated response.

## V123 pointwise numeric development

Reuses pinned owner Qwen3-8B Q4_K_M and llama.cpp b11146, plus the existing V41 source manifests for BerkeleyDB, Dune/HSMGP and HIPAcc. No new dependency/model/data download or source-code reuse in the experiment. Original local-only dataset redistribution qualifications remain unchanged. The private V123 replay contains source tables for local verification and is not a public redistribution grant.

After collection, the owner LLAMBO discriminative surrogate and prompt helper were inspected through commit-addressed web URLs at196fe237f60a3d3a2fa53cbf8f474ec20a01dd57; MIT, copyright2024Tennison Liu. Nothing was vendored, imported or executed. See reports/reference_surrogate_audit_v123.md. V123 is our own clipped numeric adaptation and does not replicate LLAMBO's stochastic surrogate/expected-improvement method.

## V124–V126 surrogate, format and feasibility audits

Three owner LLAMBO files were captured at revision196fe237f60a3d3a2fa53cbf8f474ec20a01dd57: discriminative_sm.py, discriminative_sm_utils.py and LICENSE, totaling19,537bytes. MIT, copyright2024Tennison Liu; exact owner URLs and SHA256s are in artifacts/sources/v124/manifest.json. Read only: no upstream import, provider access or installation. Our local compact-JSON/batch-EI implementation is a source-mapped adaptation, not a full LLAMBO replication. V125 separately tests demonstrated marked answers; the owner-style text condition changes several presentation factors.

Existing Qwen3-8B Q4_K_M, llama.cpp b11146, dependencies and V41 dataset revisions remain unchanged. V126 acquires the complete admitted six-family recorded domains locally; no new third-party dataset/model/package was downloaded or executed. Original equal-utility/noise and data-specific redistribution qualifications still apply. Private replay ZIPs include source material for local verification only; this does not authorize public redistribution. No uploads or publications occurred.

## V127 full-domain feature proposals

Reuses the pinned owner Qwen3-8B Q4_K_M/llama.cppb11146 and all six V41source datasets. No new external download or dependency installation. The original saved SNAP2paper bytes were rechecked against artifacts/source_manifest.json for its nearest-measured-row description; our symbolic JSON/batch/Hamming projection is independently implemented and differs from the source method. No exact SNAP2code was substituted or claimed. See reports/source_mapping_v127.md.

The private V126full-dependency ZIP includes36pinned runtime files, contrary to its original no-runtime-binaries sentence; a corrected archive changes only README/manifest text, preserving all scientific data and the original ZIP. No model weights are included, and its saved replay never executes the bundled runtime. The V127compact replay omits runtime binaries/weights. All recorded-data redistribution qualifications remain; no public distribution occurred. Post-hoc output-capacity analysis reads the already pinned GGUFvocabulary; synthetic tokenizer fixtures remain separate from measured LLM outputs and objective results.


## V128–V129 continuation

No new model, package or source-body download. Existing Qwen3-8B/llama.cpp, Storm owner archive and MongoDB TwinsOrFalseFriends data keep their original pinned identities and qualifications; neither table is newly admitted to V52 native-correctness gates. Private replay bundles are not publication or data-redistribution grants.

The macOS monitor uses installed libproc APIs. ABI headers from the local macOS SDK (`libproc.h`, `sys/proc_info.h`) are copied with original notices into `artifacts/study_v129/sdk_headers/` and hash-pinned. Apple's original XNU wrapper was inspected at https://github.com/apple-oss-distributions/xnu/blob/main/libsyscall/wrappers/libproc/libproc.c to confirm PID-count semantics. This moving web reference is explanatory; installed SDK byte hashes are the executed ABI pin. The project wrapper is independently written, not downloaded upstream executable code. No kernel/system setting is changed.

Optional FLAC owner documentation was read at https://www.xiph.org/flac/documentation_tools_flac.html and its release listing. No FLAC source, corpus, installation or measurement occurred. Web-provider transfer sizes remain unknown; instrumented saved-download totals are unchanged. ExaStencils source inspection accidentally displayed two raw objective rows; the incident is documented separately, not admitted as an experiment or an untouched-system certificate.


## V130 FLAC and licensed speech

FLAC1.5.0 official release from Xiph's listed OSUOSL mirror, SHA256f2c1c76592a82ffff8413ba3c4a1299b6c7ab06c734dee03fd88630485c2b920. CLI GPL-2.0-or-later; libFLAC Xiph BSD-style license; documentation GFDL notices retained under artifacts/sources/v130/flac-1.5.0. Built locally with no source changes or system installation. Existing gettext dynamic-library identity is recorded, not downloaded. Python experiment code is independently implemented.

LibriSpeech (c)2014Vassil Panayotov, OpenSLR12, CC BY4.0. Official test-clean archive and three fixed extracted utterances retained locally with LICENSE.TXT/README.TXT; full selection, hashes, commands and attribution in reports/source_audit_v130.md and artifacts/study_v130. License link: https://creativecommons.org/licenses/by/4.0/ ; owner: https://www.openslr.org/12/ . Only WAV/raw conversion for sample-identical local measurement; no resampling or trimming. No public distribution occurred. Compact replay excludes all audio/source archives/runtime binaries and weights, retaining notices and measured receipts. Qwen3-8B/llama.cpp identities and original qualifications remain unchanged.


## V131–V132 WavPack, FFTW and historical controller inputs

Owner WavPack5.9.0 source from https://www.wavpack.com/wavpack-5.9.0.tar.xz ; SHA256b5291bc4e6d69ebbd3da3800c5bf4a70f19bb92679b23e09b3b612c1e648d1ff is a local pin. Release COPYING is BSD3, copyright1998–2025David Bryant. The Git repository calls its license file license.txt; the downloaded release uses COPYING. Notices retained. Static project-local CMake build, no installation/publishing.

Owner FFTW3.3.11 from https://www.fftw.org/fftw-3.3.11.tar.gz ; owner MD540ec8d0447d03b8f01f8c90aa77bd16fverified, SHA256retained in download receipt. Library GPL2-or-later, copyrights include Matteo Frigo and MIT; authors Matteo Frigo/Steven G.Johnson per README. Public API header has a separate BSD-style exception. Original source notices/COPYING retained. Static project-local ARM NEON/pthread build, no system settings/install. Project-authored worker links FFTW locally; no binary redistribution occurred.

Reuse V130's CC BY4.0 LibriSpeech clips, Vassil Panayotov2014, and NumPy pocketfft reference under existing package licenses. WavPack preserves complete source PCM; FFTWuses fixed first8192samples scaled by32768. All input/reference hashes retained. No new corpus/model/package download. Existing Qwen3-8B/llama.cpp identities and original qualifications unchanged.

V132uses historical measured outcomes/features from eight source groups with their prior license/redistribution limitations retained. The compact private replay excludes audio, native outputs/source archives, runtime binaries and model weights; includes selected historical prefix/derived outcome records and license notices. No public upload/contact/push. reports/source_audit_v131.md maps source ownership/builds and task semantics.

## V133–V135 lossless JPEG, photographs and SAC repair

libjpeg-turbo3.1.2 owner source: https://github.com/libjpeg-turbo/libjpeg-turbo/tree/3.1.2 ; archive SHA256560f6338b547544c4f9721b18d8b87685d433ec78b3c644c70d77adad22c55e6 is a local pin. Original composite IJG/modified-BSD/zlib notices retained in LICENSE.md and README.ijg. This software is based in part on the work of the Independent JPEG Group. Local static build, no system installation or public binary redistribution. Independently written experiment code.

Three scikit-image v0.20.0 photographs verified against its owner SHA256 registry: astronaut (NASA/public domain), coffee (Rachel Michetti/CC0, courtesy of Pikolo Espresso Bar), rocket (SpaceX/public-domain attribution documented by scikit-image). Original attribution functions and registry retained under artifacts/sources/v133. Full images converted to RGB PPM using existing Pillow12.3.0; no resize/crop. Rocket is already JPEG; its decoded pixels define the task. No scikit-image package or model downloaded. The compact replay omits photographs and encoded outputs.

V134 is retrospective reuse of measured prefixes/results with all original data rights and reliability qualifications preserved. V135 reuses existing pinned DeepPerf/SAC n-body table and owner Qwen3-8B/llama.cpp; the table-specific redistribution grant remains unresolved, so source table is excluded from the private compact replay. Only already acquired row extracts/feature metadata are included for local review; this is not a public redistribution authorization. Original SAC failures are preserved. No contacts, upload or publication occurred.

## V136 matched-call feedback diagnostic

Reuses the pinned Qwen3-8B Q4_K_M owner model revision7c41481f57cb95916b40956ab2f0b139b296d974 and llama.cpp b11146 already attributed above; no new download, package or native code. Recorded LLVM/SAC sources and original provenance/limitations remain in data/manifest_v41.json and feature-only snapshots under artifacts/study_v136/candidates/. The independently implemented two-proposal feedback/masked adapter is an adaptation, not an exact SNAP2/LLAMBO artifact. Private compact replay contains only already acquired source-row extracts, original prefixes/reference arms, prompts and real response receipts, and does not assert new redistribution rights. No third-party license or source attribution was changed.


## V137–V138 admission audit and cheap controls

Input Sensitivity owner llesoil/input_sensitivity revision aec6b95bb0587a9fb8584fb0a290099d28c5e393, MIT license copyright 2023 Luc Lesoil retained at artifacts/sources/v137/input_sensitivity/LICENSE. Paper by Luc Lesoil, Mathieu Acher, Arnaud Blouin and Jean-Marc Jézéquel. Owner code/notebooks inspected only; no execution or incorporation into experiment code. Root license is not assumed to license third-party image/input datasets. Five small recorded tables retained for feature-only local admission, no objective analysis. Node.js v15.14.0 benchmark source excerpts inspected from nodejs/node, retained locally with provenance; not executed, incorporated or publicly redistributed. SeMPL owner ideas-labo/SeMPL revision 24eb83219ef78b5382cec88490e9de7ea000263b: README/tree inspected, no root license inferred and no outcome tables downloaded. See reports/source_audit_v137.md for exact source and eligibility distinctions.

V138 controls independently implemented. Existing six-family recorded sources and historical Qwen/llama.cpp provenance retain prior attribution and rights limitations. Compact private replay excludes full source tables/models/binaries and new admission tables, retaining only already acquired row extracts and prior reference states. No new public redistribution rights claimed. No upload/contact/push occurred.
