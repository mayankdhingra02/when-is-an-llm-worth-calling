# STATUS — V116–V118 source recovery and routing-headroom analysis complete

Resume here, then `reports/research_readiness_v117.md`, `reports/influence_v117.md`, `reports/admission_v116.md` and `reports/archive_v118.md`. Do not reread the full initial discovery report, repeat the owner-archive search, or recollect exposed outcomes. All work in this continuation is source/feature auditing or analysis of saved real traces. No new model calls, objective acquisitions or native workloads occurred.

## Latest concrete result: qualify the negative finding

V117 reanalyzed all 36 V114 real Qwen3-8B continuations, nested within 12 fixed prefixes and six exposed software families, against the V115 single B20 classical portfolio and both original controls. No family was removed from the primary analysis.

| Comparator | Full group-first mean gain | Mean range after omitting one family | Non-deployable observed routing headroom |
|---|---:|---:|---:|
| Batch 3NN | -2.672% | -3.368% to +0.096% | 0.168% |
| Full-domain sequential 3NN | -6.446% | -8.248% to -3.384% | 0.653% |
| Single alternating classical portfolio | -2.252% | -3.112% to +0.557% | 0.568% |

OpenVPN drives the negative mean against the portfolio: excluding it changes -2.252% to +0.557%. This is an influence diagnostic, not permission to select the favorable subset, a confidence interval or learned-router cross-validation. A general statement that LLMs hurt on average is not robust here. The narrower practical-margin finding remains: zero of 36 observed continuations beats the single portfolio by 5%; nine small wins, 15 ties and 12 losses, maximum gain 3.34%. No joint 5% win over both original controls occurred either.

The hindsight headroom clips each observed gain at zero and retains the same prefix/family weighting. It selects between classical and that one sampled continuation after both outcomes are known. It is explicitly non-deployable, not a best-of-three LLM policy, not a population upper bound and not cost-free. There is still no established useful learned benefit-aware router on unseen software systems. Q2 readiness is not established.

## Independent-data route actually investigated

V116 pinned original BO4CO code at `c94d9ad23e1cc4e9009a70cee23cbb42f122b5be`, checked its complete 876-entry inventory and 11 Git blobs. The located summarizer can substitute summed bolt process latency when complete latency is zero, and averages transferred-message counts as throughput without explicit elapsed-time division. These are source-level facts; they do not prove the archived rows used those paths. The wrapper returns -1 on some deployment/summary failures. Exact per-table metric and failure/validation linkage remains unresolved.

The feature-only audit checked six tables. Largest illustrative fixed-contract partitions: MongoDB 270; named Storm 256; RollingSort 64; WordCount variants 2,880 and 1,080; Redis 3,155. All pass the audit's necessary 40-setting coverage gate, which does not certify legal/equal-utility settings or supersede later native400-setting requirements. No objective cell was converted, ranked or exported.

The exposure scan covered 27,460 structured result/manifest files / 327,895,803 bytes, finding 1,474 matching files. All were admission/manifest context or prior V60/V61 Redis work. Redis is exposed despite its old V52 reservation. No non-admission MongoDB/Storm measured file was found in this scope, but absent aliases are not proof of no external, deleted or unnamed exposure.

V118 followed the owner README to DOI10.5281/zenodo.56238, downloaded its metadata and 139,425-byte original archive, and matched the published MD5. API metadata explicitly declares BSD-3-Clause. All ten CSV headers/feature sets were audited without converting throughput/latency. The archive contains ten tables plus OS metadata, with no per-attempt validation/failure log or executed-code manifest. Three distinct multi-tenant workloads share identical feature spaces, so feature matching alone cannot uniquely establish task identity. Source location, licensing and schemas are now resolved; measurement/validation linkage is not. Existing V52 admission gates remain closed and zero independent groups were admitted.

## Evidence and commands

- Frozen rules: `reports/protocol_v116.md`, `protocol_v117.md`, `protocol_v118.md` and their `.freeze.json` files; executable audit freezes under study_v116/study_v118.
- Source bodies/URLs/hashes and retained attempts: `artifacts/sources/v116/` and `artifacts/sources/v118/`.
- Source/feature/exposure results: `results/v116_admission/summary.json`, `results/v118_archive/summary.json`.
- All control-specific group means, omission diagnostics and hindsight headroom: `results/v117_influence/summary.json`; reproducible `influence.png` and `.svg`, visually inspected.
- Execution/replay/test/reproducibility/seal receipts: `artifacts/study_v116/`, `artifacts/study_v117/`, `artifacts/study_v118/`.

Safe replay with no new inference or optimizer acquisitions:

```sh
.venv/bin/python scripts/audit_reserved_v116.py --verify-only
.venv/bin/python scripts/audit_archive_v118.py --verify-only
.venv/bin/python scripts/analyze_influence_v117.py
.venv/bin/python -m pytest tests -q
.venv/bin/python scripts/seal_reserved_influence_v118.py --verify-only
```

Final full suite: **893 tests passed**, with 14 third-party deprecation warnings. New synthetic tests exercise poisoned targets, feature deduplication/normalization, nonfinite values, retrieval/ZIP boundaries, nested weighting and per-replica oracle clipping. They are excluded from research aggregates. Model/native jobs were not run during these checks. Every source/audit output is preserved; fetchers refuse overwrite and implicit retries.

One initial sandbox DNS failure was retained in V116 and explicitly retried using normal execution permission; the retry and subsequent source fetches succeeded. Web-tool Zenodo opening returned429, but subsequent bounded API/archive retrieval succeeded. No auto-review rejection remains. Initial source inventory output was overly broad/truncated; subsequent inspection used projected metadata only, not target scores. All ten CSV members of the original ZIP were read in memory for feature projection, without filesystem extraction or upstream execution.

## Next action and exact external gaps

**Obtain an independently validated measurement source.** For the original WordCount data, the missing evidence is a measurement contract or linked original run records establishing latency type, fixed workload/version, successful output validation and failure handling. Re-downloading the already audited archive will not provide absent records. No author contact is authorized or performed. Another owner dataset with those facts could serve instead; it must be admitted without looking for favorable outcomes.

For native claims, `output/v113_replication/README.md` remains a ready private second-host packet: 90 charged acquisitions / 270 solves, Python3.10 with pinned NumPy/SciPy/HiGHS, no GPU or LLM, 30s/2GiB per worker and 1,800s overall. Only this Mac is available; independent-host/Linux execution remains untested. Do not bypass its source-host guard and call another local run independent. HB dataset redistribution terms remain unresolved. A second host tests measurement portability, not cross-system routing generalization.

No new bounded experiment is queued and no background work is promised. The scoped low-headroom/negative-result contribution is ready for technical discussion, not a guarantee of journal acceptance. Preserve the practical-margin claim and small wins; avoid positive-outcome seeking on this exposed cohort.

## Prior actual collection and unchanged limits

Latest real inference/optimization collection remains V114–V115: 36 successful real Qwen3-8B requests, 360 recorded continuation acquisitions plus 120 classical-portfolio acquisitions, all B20. V114 runtime293.705s, peak sampled RSS6,808,207,360 bytes under8GiB, 720 generated tokens of4,608 allocated, 59,286 reported prefill tokens; zero missing usage in that batch. V115 stage3.458s; mean ten-turn loop0.025289s includes recorded-table accesses, not fresh target-software execution.

Cumulative real model requests **3,974**; recorded-table acquisitions **28,458**. Numerical native880 acquisitions; NGINX81 charged attempts /35,853,130 byte-valid responses including partial timeout outputs. Older DuckDB78 physical, H2299, Kanzi1,265, RocksDB350 units unchanged. Never mix these units or treat historical unknown usage as zero.

New saved source downloads: V116290,909 bytes + V118145,893 bytes = **436,802 bytes**. Cumulative **9,876,339,919 /10GiB**, leaving **861,078,321 bytes**. Model payload remains9,126,358,023 /9GiB. Zero new external spending, installs, system-setting changes, cloud resources, messages, publications or remote pushes. Agent/electricity costs remain unpriced; source audit/research collection is not deployment cost.

V113 native measurement limitation remains: five of eight identical-configuration contrasts appeared different by at least5%, maximum23.68%; median repeated-incumbent relative range35.92%. NGINX V111 remains stopped under its frozen failure rule; V112 is a prepared synthetic-tested adapter, never a measured model study.

## Integrity checkpoint

Combined V118 seal covers V116–V118 source evidence, code, tests, reports and results, following immutable V115 manifest SHA256 `d9d7589c2436c872b509b0445b4c2152abe078e3b229716cf538e438832389c3`. Prior root documents are preserved under `artifacts/study_v116/previous_snapshot/`. Historical manifests/raw traces are unchanged. See `artifacts/study_v118/seal_verification.json` for current hash and verification counts. The V115 checkpoint and previous 45 checkpoints remain in the resolved historical chain.
