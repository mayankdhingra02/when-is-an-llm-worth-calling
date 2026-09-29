# Registry expansion v5 — source audit and tested preparation

**The data search progressed from four to 22 broader-schema candidate software families.** This is a candidate registry, not 22 admitted tasks or a completed larger experiment. Five families fit the unchanged v4 binary/single-objective/size rules. Broadening to finite domains and larger feature tables requires a versioned treatment and final objective/schema admission before collection.

The audit covers 81 CSV tables: the existing 47 MOOT files plus 11 DeepPerf, 11 VEER and 12 Performance Evolution tables. New objective payloads were not parsed or scored; only feature cells, objective headers and declared revision/workload metadata were inspected. Pinned source bytes, owner commits and hashes are retained. No new optimizer objective acquisitions or model calls occurred. The previous measured v3/v4 results and v4 freeze remain unchanged.

## Primary sources and concrete identity findings

- [VEER, original v3 paper](https://www.se.cs.uni-saarland.de/publications/docs/PKS%2B23.pdf), Kewen Peng, Christian Kaltenecker, Norbert Siegmund, Sven Apel and Tim Menzies: Table 2 names systems, while §6 links [the actual artifact](https://github.com/anonymous12138/multiobj/tree/fc4b4e099c0bcc4f6958c11762c64944b637b9d8). MOOT uses different SS letters. Comparing normalized feature names and entire distinct feature matrices resolves MOOT SS-M to HSQLDB, SS-O to MariaDB, SS-Q/R to VP8/VP9, SS-T to lrzip, SS-U to x264, SS-V to MongoDB, SS-W to LLVM and SS-X to ExaStencils. SS-J/S and both rs objective variants match the artifact's rolling-sort table. These are feature correspondences, not assertions that objective values or transformations are identical.
- [FLASH, original author-hosted paper](https://www.se.cs.uni-saarland.de/publications/docs/NYM%2B18tse.pdf), Table 1, identifies the rs/sol/wc cases as workloads/configurations of Apache Storm. It also identifies the small SS-B and SS-H cases as hardware-design tasks, so they are excluded from this software study. The [MoConfig author-hosted paper](https://gu-youngfeng.github.io/paper/2019_APSEC_MultiObjective.pdf), Table I and dataset description, independently corroborates the shared Storm platform. Workloads/cluster variants do not increase the independent-system count.
- [DeepPerf owner artifact](https://github.com/DeepPerf/DeepPerf/tree/86b9b400de60075061452d2ed1eb0b82fe7def0f) names eleven systems and points back to the original SPLConqueror measurements. Its data adds candidate DUNE, HIPAcc, HSMGP, SaC and BerkeleyDB Java variants. BDB-C/J are conservatively grouped. The [original multigrid study](https://www.infosun.fim.uni-passau.de/cl/publications/docs/KSK%2B18.pdf) supports HSMGP's multigrid identity; the later “Hazardous Software Management” description is not adopted. HSMGP and DUNE are conservatively kept in one related numerical-software family. This grouping reduces sample size rather than assuming independence.
- [Performance Evolution owner artifact](https://github.com/ChristianKaltenecker/PerformanceEvolution_Website/tree/4ee53dad6b81543c444d44282053def0d82d97b3) supplies twelve named case folders, feature models and workload/revision notes. VP8/VP9 share the libvpx family; MySQL/MariaDB share a family. A single lexicographically first revision is used for schema feasibility, never counted as a separate system. Z3 is conditioned on the LRA workload before inspecting configurations; workload choice cannot become an optimization shortcut.

The detailed machine-readable correspondences are in data/registry_v5.json and artifacts/registry_v5/summary.json. Fourteen exact feature correspondences were established, including MOOT SS-N to its named x264 table. Additional Storm/HSMGP mappings are explicitly family-level primary-metadata correspondences, not byte-level table equivalence. All x264/Apache HTTP Server/SQLite variants remain excluded from fresh evaluation. Apache Storm is a distinct product from Apache HTTP Server.

## Checks that stopped unsafe admission

The first independent feature-model check failed for Fast Downward: its CSV has `disjunctiveLMs`, absent from the supplied feature model. The case is now quarantined; the original failed verification log is preserved. No column was deleted to make the check pass. Eleven other Performance Evolution feature schemas match their feature models exactly. The preliminary 23 broader candidate families therefore became **22** after this check.

VEER's SS-C artifact has eleven anonymized feature columns, inconsistent with its paper's five-option workload description. It remains unresolved, as do MOOT SS-L/P with anonymous columns. Their matrix similarity cannot identify the software without a trustworthy mapping. Hardware SS-B/H are outside scope, not extra software systems.

Objective directions require semantic review. OpenVPN's owner README describes throughput, so higher is better despite the generic `performance` header. Some MOOT/VEER throughput suffixes and obj1/obj2 descriptions disagree across sources; no reversal or transformation has been guessed. Other unselected outcome columns must remain excluded from features when a primary target is chosen.

Revision/workload notes also matter: the first MariaDB revision in the CSV, 10.0.17, overlaps a README-reported crashing-release gap. Resolve the discrepancy or predeclare a documented valid family representative before collection. Several documents describe differing workloads for the same family; do not treat these as interchangeable or infer exact original environment details from a file name.

## Candidate sets and implementation

Unchanged v4 schema-compatible candidates: **BerkeleyDB, DeepArch, HSQLDB, LLVM, OpenVPN**. They are schema candidates, not automatic admission of full provenance.

With a proposed 64-feature / 200,000-row finite-domain limit and explicit semantic target selection, the 22 candidate families are: **7zip, BerkeleyDB, Brotli, DConvert, DeepArch, DUNE/HSMGP, ExaStencils, HIPAcc, HSQLDB, JavaGC, libvpx, LLVM, lrzip, MongoDB, MySQL/MariaDB, OpenVPN, Opus, PostgreSQL, Redis, SaC, Storm and Z3**. One family remains one statistical group regardless of datasets, versions, languages or seeds. No final development/test assignments have been made.

Implemented `src/escalation/finite_domain.py` as a separate optimizer core, without modifying v3/v4. It provides explicit finite feature domains, modal centroids with deterministic ties, nearest-mode acquisition, uniform proposals and checked index encoding/decoding. Numeric-looking levels are treated as nominal categories; ordinal distances are deliberately ignored. This is a proposed adaptation, not a validated numeric optimizer. It does not include an LLM adapter or full larger-study collector.

**37 tests passed.** New tests cover objective-payload invariance, metadata filters, exact feature correspondences, family aliases, missing feature-model options, finite-domain codec rejection, inclusive budgets and agreement with the old algorithm on binary fixtures. These finite-domain runs are synthetic tests only; no measured software-quality aggregate includes them.

Independent verification checks all new data/document payload hashes and Git blob IDs, the eleven feature-model matches and quarantined mismatch, exposed-family exclusions, objective/metadata separation and preservation of the v4 freeze. Registry building was actually executed; it is not a hand-written inventory.

## Remaining work and resources

The 22 candidate families provide a plausible data route to the 20-group design. They do not remove the need to resolve semantic objectives, license/lineage evidence, valid workload/revision selection, final representative tables and the changed model interface. The per-family review is artifacts/registry_v5/admission_review.json. Only after those checks should a v5 treatment/final manifest and full collector be frozen.

No model request, objective acquisition, installation, cloud resource, paid endpoint, push or contact occurred this session. The existing allowance remains 34 calls and about 642.7 seconds; the full planned study needs 203 calls and its proposed larger runtime allowance is still unapproved. Source-audit/download/test time is separate from measured experimental runtime. Historical costs remain 1,658 charged labels and 166 request attempts.

Next action: **complete semantic target and valid-revision admission for the 22 candidate families, then freeze the finite-domain model interface and final group manifest.** More model calls before that would consume the remaining budget without resolving validity.

## Reproduce

```sh
.venv/bin/python scripts/fetch_registry_v5_metadata.py
.venv/bin/python scripts/fetch_registry_v5_data.py
.venv/bin/python scripts/fetch_registry_v5_papers.py
.venv/bin/python scripts/build_registry_v5.py
PYTHONPATH=src .venv/bin/python -m pytest -q
.venv/bin/python scripts/verify_registry_v5.py
```

Fetchers use pinned cached commits and the persistent download guard; owner files remain Git ignored. No upstream installation or executable code is run. The v5 snapshot freezes audit/preparation artifacts, not a falsely completed full-study protocol.
