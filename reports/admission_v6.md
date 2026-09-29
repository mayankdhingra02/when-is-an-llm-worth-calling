# Semantic admission completed for the bounded v6 follow-up

This review narrows the 22 v5 schema candidates to seven families with explicit target semantics in already pinned primary case READMEs. Six enter the bounded experiment under an outcome-blind hash allocation. The rest remain unadmitted for a larger study. No paper/repository output is treated as executable instruction, and no upstream algorithm code is reused.

Source owner: [PerformanceEvolution_Website, pinned commit 4ee53dad6b81543c444d44282053def0d82d97b3](https://github.com/ChristianKaltenecker/PerformanceEvolution_Website/tree/4ee53dad6b81543c444d44282053def0d82d97b3). `data/manifest_v6.json` binds each original file, feature model and case README by SHA-256; v5 retains source Git blob IDs. Repository license evidence is GPL-2.0; source measurements remain Git ignored. Admission permits this local recorded-data adaptation, not a claim of resolved redistribution rights for every upstream artifact.

| Representative | Recorded revision | Target / direction | Case-document evidence and caveat |
|---|---|---|---|
| Brotli | 0.3.0 | compression runtime / minimize | README explicitly specifies seconds; uiq compression workload; source global/case payload-size descriptions differ |
| HSQLDB | 2.1.0 | runtime / minimize | PolePosition 0.6.0; explicit runtime property; unit not restated in case README |
| MySQL | 5.6.10 | runtime / minimize | case README specifies sysbench 1.0.17, 10000 oltp_read_write events; more specific than conflicting global PolePosition description |
| OpenVPN | 2.1.0 | throughput / maximize | iperf 3.6 client-to-server TCP; Mbit/s; admitted but allocation leaves it unused |
| PostgreSQL | 10.0 | runtime / minimize | PolePosition 0.6.0; revision is lexicographically first, not chronologically earliest |
| VP8 | v0.9.1 | encoding runtime / minimize | lossless Sintel trailer 480p; selected revision predates documented >=v1.4.0 option-alias behavior |
| lrzip | 530 | compression runtime / minimize | case README specifies 621 MB uiq2 payload; global summary says about 100 MB, discrepancy preserved |

The original selected revision strings, row counts and feature matrices are unchanged from v5. No alternative revision is chosen for better observed optimizer performance. All objectives other than `performance` are excluded from feature inputs. Output size/energy/quality are not optimization targets in this adaptation. This can favor different quality settings, so runtime gains cannot be interpreted as equal-quality throughput improvements.

MariaDB remains in the MySQL family, with its 10.0.17 crash-gap inconsistency unresolved. Selecting the documented MySQL representative avoids claiming that inconsistency is fixed. VP9 shares libvpx with VP8. Fast Downward stays quarantined for its missing feature-model option. Opus and z3 case documents identify workloads but do not explicitly identify the generic performance column's direction/unit, so no direction is guessed.

The remaining broader candidates (7zip, BerkeleyDB, dconvert, deeparch, DUNE/HSMGP, ExaStencils, HIPAcc, JavaGC, LLVM, MongoDB, Redis, SaC, Storm, plus Opus/z3) need target-transformation and/or workload/revision provenance review before admission. DeepPerf's original [Ha and Zhang paper](https://hongyujohn.github.io/DeepPerf.pdf) was located and read as a source lead; its general runtime-prediction framing is not sufficient by itself to prove each reused table's orientation/transformation. No additional DeepPerf data are admitted on that basis.

The code supporting broader finite domains is exercised on synthetic fixtures. All selected empirical cases are binary. The new experiment therefore tests six additional system families and a changed one-batch model interface; it does not establish performance on numeric configuration domains.
