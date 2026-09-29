# Focused source follow-up, 2026-09-26

Read-only primary-source checks alongside the V86 existing-data analysis. No external code, paper PDF, weights or dataset was downloaded into the project or executed. Browsing is not a pinned artifact admission; links can change. No new benchmark was admitted merely from these pages.

## Realistic workload lead

[BenchBase owner repository](https://github.com/cmu-db/benchbase) describes variable-rate/mixture JDBC workloads, including TPC-C, SmallBank, Wikipedia and YCSB. Its current README lists postgres/mysql/mariadb/sqlite/cockroachdb/phoenix/spanner build profiles, and a Java21 modernization note; the inspected POM actually requires Java23. The retained local H2 study used Java17; H2 is not among those documented profiles. Therefore it is not a verified drop-in workload for our installed H2 runner. [Owner license](https://github.com/cmu-db/benchbase/blob/main/LICENSE) identifies Apache2.0; [build definition](https://github.com/cmu-db/benchbase/blob/main/pom.xml) was inspected for compiler requirements; dependencies have not been completely audited/pinned in this follow-up. V68 already pinned and inspected this lead; see `reports/source_followup_v86_addendum.md`.

Decision: credible workload-source lead, not yet runnable/admitted here. A future bounded admission must pin a commit, inspect dialect/config/dependency support and account for bytes before building. Do not silently restart Docker or install a DB/Java globally. Reusing H2 with a different workload still produces the same software-family group. SQLite is already exposed in earlier work; it would not automatically be untouched either. This lead addresses workload realism, not independent held-out model validation by itself.

## Contribution boundaries

[Jai Kannan, Can LLMs Configure Software Tools, arXiv2312.06121v1](https://arxiv.org/abs/2312.06121v1): verified title/author/version and abstract. It discusses LLM-assisted initialization/narrowing and observed variability/domain-keyword behavior. Full methods and artifacts not inspected in this follow-up. Do not claim configuration help or prompt sensitivity are new ideas.

The existing [V84 primary-source audit](novelty_boundary_v84.md) covers LLINBO, LLAMBO reproduction and a staged database-tuning lead. V86 adds exact comparator-sensitive feasibility analysis in this pilot; neither hindsight bounds nor strong controls are claimed as algorithmic novelty.

Search also returned a recent article titled “Prompt Escalation for Lightweight Large Language Models: An Empirical Evaluation of Cost–Performance Trade-Offs”, Applied Sciences16(18)9190. The [publisher page](https://www.mdpi.com/2076-3417/16/18/9190) failed to open in this tool. Its search snippet is a discovery lead only: authors, full methods, artifact and claims remain unverified. It is not used to support a research conclusion or a journal-tier claim.

## Next admission criterion

Select a modest realistic workload using provenance/domain criteria before outcome inspection, measure classical controls on development data under a frozen cap, then decide whether there is informative residual opportunity. Reserve independent families untouched. Additional inference/model capacity requires its own bounded allowance, since the prior batch is exhausted; source inspection and saved-data analysis do not supply that allowance. No positive result or publication is promised.
