# H2 admission audit

Chosen candidate: H2, separate from Kanzi/RocksDB and from HSQLDB. Historical V73 inspected H2 metadata, so the family is exposed development data. DuckDB and other older candidates have their own earlier admission histories; none is relabeled held out here.

[Owner release2.3.232](https://github.com/h2database/h2database/releases/tag/version-2.3.232) identifies the2024-08-11 release. Pinned [owner DbSettings](https://raw.githubusercontent.com/h2database/h2database/version-2.3.232/h2/src/main/org/h2/engine/DbSettings.java) documents default query cache8, recompilefalse and analyze sample10000. The stored tagged source and [owner license](https://h2database.com/html/license.html) identify the dual MPL2.0/EPL1.0 terms. No upstream application source was modified or copied into the own JDBC harness.

The [official commands documentation](https://h2database.github.io/html/commands.html) says CACHE_SIZE and MAX_MEMORY_ROWS do not affect in-memory databases. They are excluded. Automatic analyze and result reuse are explicitly disabled; query caching fixed. Tunability comes from physical indexes, recompilation, and explicit statistics collection. Index configurations preserve logical query answers but incur creation cost. The domain baseline follows query predicates; it is not fitted to acquired timing outcomes.

Recognized registry retrieval: Maven Central com.h2database:h2:2.3.232. Published registrySHA1 checked; SHA256 of downloaded JAR/source/license and Java/compiled harness pins retained. This is provenance/integrity evidence, not a signed authenticity proof. No installer or downloaded shell script executed. Actual measured stage remains native feasibility until the prospective protocol runs and correctness/timing checks pass.

Downloads and URLs: artifacts/study_v81/download_ledger.json. Dependency/harness: configs/runtime_v81.lock.json. Application license is retained in ignored artifacts/sources/v81/LICENSE.txt; the repository does not publish or redistribute the dependency. Source audit opens no recorded H2 objective table.
