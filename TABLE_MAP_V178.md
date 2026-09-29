# Map from manuscript tables to scripts, inputs and output fields (V178)

Table numbers follow their order in `paper/overleaf_v173/main.tex`. `scripts/check_tables_v176.py` checks every row of Tables 1 and 3–12 (80 rows) and 12 in-text headline numbers against the fields named below, or against a recomputation from the case records. Its function for each table is given in the last column.

**Case records.** `revision_v174.load_cases()` (through `audit_v171.recorded_cases()`) assembles the 70 task–seed cases from these files:

- `artifacts/study_v151/inputs.json`: controller features and the SmolLM3-3B / Qwen3-8B outcomes;
- `results/v141_analysis/comparison.json`, `results/v145_spark/comparison.json` and `results/v148_hadoop/comparison.json`: classical arms;
- `results/v155_gp/comparison.json`: GP-EI;
- `results/v41_transfer/arms/*_full_classical.json`: the prefix optimizer;
- `results/v172_eval/arms/*.json`: Qwen3-14B;
- `results/v173_eval/arms/*.json` and `results/v173_models/B*/arms/*.json`: gpt-oss-120b;
- `artifacts/study_v172/jobs.json`: case identifiers, ecosystem assignments and saved prefixes.

Raw inputs behind these files are replayed by the `verify_*` scripts in `BUNDLE_V178_README.md`. They include the per-configuration tables in `data/` and `artifacts/sources/`, the prefixes, prompts, raw responses (`results/v1xx_models/*/responses.jsonl`) and acquisition logs.

| Table | Label | Content | Produced by | Output fields | Checker |
|---|---|---|---|---|---|
| 1 | `tab:cohort` | Engines, workloads and cases | Case records | Recomputed: engine and workload counts | `rows_cohort` |
| 2 | `tab:snap2` | Design comparison with SNAP2 | Descriptive. SNAP2 facts from arXiv:2607.02583; this study's from `configs/study_v173.json`, `reports/protocol_v173.md` | — | not numeric |
| 3 | `tab:rq1` | Mean gain, log-ratio, better/worse, headroom vs sequential 3NN | `audit_v171.py`, `analyze_v172.py`, `analyze_v173.py` | `results/v171_audit/audit.json` → `recorded_cohort.<model>.arms.<arm>.{equal_group_mean_gain, equal_group_mean_log_gain, equal_group_hindsight_headroom, useful_over_sequential}`; `results/v172_analysis/analysis.json` and `results/v173_analysis/analysis.json` → `summaries.<arm>.{equal_ecosystem_mean_gain_vs_sequential, equal_ecosystem_mean_log_gain_vs_sequential, equal_ecosystem_hindsight_headroom, useful_over_sequential}` | `rows_rq1` (recomputes every cell, including "worse") |
| 4 | `tab:eco` | Mean gain by ecosystem | Case records | Recomputed per ecosystem | `rows_eco` |
| 5 | `tab:weights` | Weighting sensitivity | `revision_v174.py` | `results/v174_revision/analysis.json` → `weighting.<arm>.{equal_ecosystem, equal_engine, case_weighted, equal_ecosystem_excluding_dune, leave_one_ecosystem_out_range}`; log-ratio in `case_weighted_log` | `rows_weights` |
| 6 | `tab:native` | Native cohort vs sequential 3NN | `report_ezr_v170.py` → `synthesis_ezr_v170.py` from `results/v170_ezr/acquisitions/`, `artifacts/study_v170/` | `artifacts/study_v170/synthesis.json` → `per_application_model[engine, model].mean_gains.sequential_3nn`, `.robust_wins.sequential_3nn`; `results/v171_audit/audit.json` → `native_cohort.<model>.arms.<arm>.robust_over_sequential` | `rows_native` |
| 7 | `tab:deployable` | LLM arms vs leave-one-ecosystem-out classical policy, and the policy vs the reference | `revision_v174.py`, `revision_v175.py` | `results/v175_revision/analysis.json` → `selector_vs_reference.{ecosystem_weighted, case_weighted, better_by_margin, worse_by_margin, selected_by_fold}`; `results/v174_revision/analysis.json` → `deployable_classical_policy.llm_vs_policy.<arm>.{equal_ecosystem, case_weighted, better_by_margin, worse_by_margin}` and `.folds` | `rows_deployable` |
| 8 | `tab:match` | Useful LLM cases vs the best prespecified alternative | `revision_v175.py` | `useful_case_matching.<arm>.{useful_cases, ecosystems_with_useful_case, classical_better_or_equal, within_margin, llm_ahead_by_more_than_margin, cases}`; extended set in `useful_case_matching_extended` | `rows_match` |
| 9 | `tab:rq2` | Baseline-set wins | `revision_v174.py` | `prespecified_baseline_wins.<arm>.{per_ecosystem.<eco>.{wins, cases, keys}, ecosystems_with_win}`; `extended_baseline_wins.<arm>.{ecosystems_with_win, win_cases}` | `rows_rq2` |
| 10 | `tab:rq4` | Controllers, SmolLM3-3B and Qwen3-8B | `router_v151.py` (unchanged, rerun by `revision_v174.py`); `controllers_v154.py` | `results/v174_revision/analysis.json` → `routers_all_arms.{smollm3_3b, qwen3_8b}.policies.<policy>.{calls, equal_ecosystem_gain}`, `.oracle_equal_ecosystem` (identical to V151: `results/v151_router/`, `artifacts/study_v151/`); `results/v154_controllers/comparison.json` → `models.ecosystem.<model>.{bora_1.0, rank_expected_1.0}.{calls, family_mean_gain}`. Folds, predictions and decisions: `results/v151_router/folds.json`, `results/v154_controllers/{decisions,folds}.json` | `rows_rq4` |
| 11 | `tab:routers-strong` | Controllers rerun on the stronger arms | `revision_v174.py` | `routers_all_arms.<arm>.{groups_with_useful_gt_1pct, policies.<policy>.{calls, equal_ecosystem_gain}, oracle_equal_ecosystem}` | `rows_routers_strong` |
| 12 | `tab:ops` | Calls, retries, 429s, invalid responses, fallbacks, latency, cost | `revision_v174.py`, `revision_v175.py` from `results/v172_models/*/responses.jsonl`, `results/v173_models/*/responses.jsonl`, `results/v173_models/B*/rounds.jsonl`, `results/v173_models/spend_ledger.json` | `operations.<arm>.{logical_requests, fallback_cases, mean_request_seconds, mean_seconds_per_200, reported_cost_usd}`; `accounting.rows.<arm>.{planned_calls, retry_calls, rate_limited_attempts, invalid_responses, fallbacks}` | `rows_ops` |

## Numbers in the text

| Text | Source |
|---|---|
| Controller reweighting (0.019 and 0.011 points; always-call loop +0.40%; checkpoint rules negative) | `results/v175_revision/analysis.json` → `router_reaggregation`, `controller_vs_better_trivial_policy`, `checkpoint_rules_reaggregation_v154`; asserted by `tests/synthetic/test_revision_v175.py` |
| Cost breakdown ($1.38 total, $1.374 arms, $0.003 probes and stopped attempt) | `accounting.cost_usd`; ledger `results/v173_models/spend_ledger.json`; replayed by `verify_v173` |
| Native exhaustive headroom (ripgrep 5.3%, up to 12.7%; hnswlib none) | `results/v174_revision/analysis.json` → `native_exhaustive_headroom_v165` ← `results/v165_headroom/comparison.json` |
| Draw disagreement (26 of 70), pairwise model comparisons, the Spark Bayes case (+8.3%, +31.5%, 27% over GP-EI), abstract ranges, 61 of 72 | Recomputed by `check_tables_v176.text_phrases` |
| Frozen V132 controllers made no calls on WavPack and FFTW; the V147 controllers none on Hadoop; masked vs. measured feedback ended with the same incumbent in all ten cases | `results/v132_router/comparison.json` (replayed by `verify_router_v132`); `reports/hadoop_v148.md` from `results/v148_hadoop/` (replayed by `verify_hadoop_v148`); `results/v136_feedback/comparison.json` (replayed by `verify_feedback_v136`) |
| Frozen V173 decision and post-hoc 2% / recurrence sensitivities | `results/v173_analysis/analysis.json` → `decision`; `results/v173_analysis/posthoc_sensitivity.json` |
