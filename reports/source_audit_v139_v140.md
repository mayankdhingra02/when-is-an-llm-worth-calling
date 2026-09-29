# V139–V140: source recovery and a fresh XZ task

The source audit partially recovered the Node.js mapping, but did not certify that recorded task. It also led to a fresh native XZ task with exact output validation; the new experiment does not reuse the unresolved old measurements.

## Node.js mapping recovery

The original Input Sensitivity paper links [Zenodo 5067851](https://zenodo.org/records/5067851), *nodejs performance on its test suite*. The record explicitly maps `0.csv` to `assert/deepequal-buffer.js`. Its separate `0.csv` MD5 equals the existing owner GitHub file, and its 1,677,564-byte `nodejs.zip` matches the record MD5. The archive inventory has 1,939 CSV files and two directory entries. No objective cells were inspected or converted. The deposit lists creator X (anonymous); provenance is the link in the verified original paper, not an invented named depositor. Record license: CC BY4.0.

This resolves a file-to-script association that V137 lacked. It does not resolve workload parameters: original Node.js15.14.0 `benchmark/assert/deepequal-buffer.js` crosses two buffer lengths, two strictness choices and two equality methods (eight cases, fixed n=20,000). Its source tests buffer assertions and reports iterations through the benchmark harness. The deposit links a test directory while the generation notebook invokes the benchmark directory. The preprocessing mapping from each parameterized output to numbered CSVs was not recovered. The cleaning notebook's 1,932 count still differs from the archive/paper's 1,939. Thus no old Node.js table is newly admitted for optimization.

Original Node.js `lib/child_process.js` defaults fork's execArgv to process.execArgv; the already retrieved benchmark common module explicitly forwards those flags in configuration children. This source chain supports intended flag propagation, not proof of historic execution/correctness. Owner files and LICENSE are retained; no downloaded Node.js code was run.

## Workload archive and XZ decision

[Zenodo 7504284](https://zenodo.org/records/7504284) identifies Mühlbauer, Sattler, Kaltenecker, Dorn, Apel and Siegmund's ICSE2023 workload artifact. Retrieved only metadata, README, license and accepted paper; no 390MB archive or performance table downloaded. This source overlaps the V73 audit: prior partial directory metadata already lists an XZ sample and measurements. The README says unsuccessful configurations can be omitted; it does not supply complete correctness/failure evidence for our intended contract. The record says CC BY4.0 whereas its license heading says CC BY-SA4.0 and links/describes BY terms. Preserve this unresolved discrepancy; do not claim clear new redistribution rights.

XZ was chosen for a fresh task because lossless file reconstruction gives an explicit, testable common utility. This decision precedes all V140 outcomes. It is not admission of the old XZ30-row table or an attempt to reinterpret its depth column. Workloads and versions remain one XZ/LZMA group; the source history scan also includes 7zip/p7zip aliases. Matching old results are admission metadata and a liblzma dependency path. This is a bounded name-based audit, not a universal non-exposure guarantee.

## Fresh implementation provenance

[XZ owner's release page](https://tukaani.org/xz/) listed 5.8.4 when checked. Downloaded official `tukaani-project/xz` release archive, 2,799,797 bytes; local SHA256 in artifacts/study_v140/downloads.json. HTTPS provenance and a local hash are verified; detached signature verification was not performed. Read CMake instructions and the included xz(1) parameter documentation before building. Project-local static liblzma/CLI, CMake Release, Xcode clang/SDK15.5, two build workers, translations/tests disabled, no installation. Successful build took 11.467026541 seconds; exact command/binary hash recorded. System-installed XZ5.8.3 was only queried for version and is not the experimental executable.

XZ5.8.4 liblzma and command-line tools are 0BSD, with a conditional LGPL getopt component and separate licensing for auxiliary scripts. Complete COPYING and notices retained. No auxiliary scripts were used or incorporated into project code. We wrote the experiment wrapper independently.

Three existing V133 PPM photographs are reused unchanged: astronaut (NASA/public-domain attribution), coffee (Rachel Michetti/CC0), rocket (SpaceX/public-domain attribution), pinned through scikit-image v0.20.0 owner hashes. Every PPM byte, including its header, is part of the reconstruction contract. Inputs are already exposed across earlier codec experiments; novelty lies in the newly studied software family, not unseen photos. Same-library decoder is an explicit limitation. No new photo/model/package download.

V139 saved 2,486,913 source bytes in nine files (two metadata records, four archive/documents, three Node.js source/license files). V140 saved 2,799,797 source bytes. Combined 5,286,710 bytes, bringing cumulative saved downloads to 10,250,376,799 bytes, within the approved10GiB cumulative ceiling. V139 cap20MB; V140 source cap4MB/build300seconds. V139 acquired zero objective values and made zero model calls. V140 collection is separately frozen in reports/protocol_v140.md; its measured counts belong to the result report, not this source audit.

Raw receipts/plans: artifacts/sources/v139, artifacts/study_v139, artifacts/sources/v140 and artifacts/study_v140. No upstream notebook, benchmark harness or archive installer was executed. Only the inspected owner XZ CMake build was run locally. No paid service, cloud, credentials, system settings, author contact, publication or push.
