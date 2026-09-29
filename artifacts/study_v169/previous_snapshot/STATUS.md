# Resume checkpoint: V168 complete

Start here, reports/research_assessment_v168.md, reports/protocol_v168.md and relevant code. Do not reread the full deep-research report. **New result:** two additional real-input applications still show no robust >10% benefit from either local model over sequential 3NN. XGBoost model-arm selected runtimes were worse on average. The evidence supports a bounded negative result; it does not establish a useful general learned router or guarantee Q2 readiness.

## What actually ran

V166 retrieved official pinned Polars1.35.2/runtime1.35.2 and XGBoost3.1.1 ARM wheels plus official UCI Covertype data. Hash-checked offline installation into .local-runtime/apps-v166 reused project NumPy/SciPy and existing libomp; no system installation. Source audit and locks: reports/source_audit_v166.md, configs/apps_v166.lock.txt. The predecessor V165 manifest verified unchanged before any root edits.

V166 charged40 feasibility attempts. All20 Polars attempts failed on an NA null marker; XGBoost completed20, with three of four cells passing the fixed quality/timing criteria. V167 separately froze the null-parser repair and charged20 more Polars outcomes. All20 exact outputs passed and all four cells met admission. Original failures remain raw, charged and visible. Feasibility totals:60 attempted outcomes,40 native completions,140 intended query/training charges;80 known successful query/training completions. Constituent-query completion inside the20failed Polars bundles is unknown, not zero.

V168 completed **800 new paired configuration outcomes,1,600 query/training executions,20 real model calls and70 logical B20 arms**. Each of ten cases (five fixed seeds per application) shares the same saved10-label prefix across five classical and two model arms, each with7 new settings and3 fresh validations. All70 incumbents were fixed before three randomized validation blocks. Classical checks passed before real inference. Stage544.017/1800seconds; foreground driver exited0, all workers waited. Both model servers exited0. No experiment remains scheduled or running through this task.

Polars runs three exact aggregate/join queries over336,776nycflights13 records plus three dimension tables, including CSV scan/parsing. This workload/data contract was previously exposed with DuckDB; it is a new implementation, not independent workload evidence. XGBoost trains on65,536real Covertype rows and predicts8,192quality-validation rows under a75%accuracy constraint. Remaining507,284rows are unused. This is runtime tuning under a quality constraint, not a held-out classifier-generalization result. Domains:64Polars/128XGBoost settings. Both applications are now development-exposed.

## Measured findings

Positive gain means lower median fresh-validation utility.

| Application | Model | Mean gain vs sequential | vs adaptive | vs GP-EI | Joint robust wins |
|---|---|---:|---:|---:|---:|
| Polars | SmolLM3-3B | +0.071% | -5.087% | -1.266% | 0/5 |
| Polars | Qwen3-8B | -0.816% | -5.958% | -2.064% | 0/5 |
| XGBoost | SmolLM3-3B | -25.538% | -25.185% | +0.263% | 0/5 |
| XGBoost | Qwen3-8B | -19.402% | -19.096% | +4.973% | 0/5 |

No model had a robust >10% gain against sequential in any case. The joint rule additionally requires beating adaptive and GP-EI, different configuration IDs, quality-valid validations, relative MAD<=5% and medians>=10ms. All70 final selections met quality; one validation cell was unstable, none below10ms. All754quality-valid and46quality-penalty acquisitions remain included. Penalties affected search/prefix outcomes, not final validation selections. Six model/sequential pairs chose the same setting.

Historical benefit and uncertainty controllers chose zero calls, matching never and matched-rate random; this is not evidence of useful learned discrimination. Always-escalate equal-family mean gains were -12.734%/-10.109%; hindsight diagnostic upper references +1.343%/+1.897%. All other controls/adaptations and raw cases remain in comparison.json. Models retained a prefix setting in18/20cases. Post-outcome proposal audit records34duplicates and48projections among140evaluated proposal positions; no protocol was changed in response.

## Evidence and verification

- Sources, raw metadata, archive/wheels and license receipts: artifacts/sources/v166; hashes, runtime, split/schema and exposure audit: artifacts/study_v166.
- Frozen admission protocols/configs: reports/protocol_v166.md, reports/feasibility_protocol_v166.md, reports/protocol_v167.md and configs/*v166*/feasibility_v167.json. Failed and repaired logs: results/v166_feasibility and results/v167_feasibility.
- Paired prospective protocol/config: reports/protocol_v168.md and configs/study_v168.json. Main freeze, candidate grids, model/router pins, prompts, saved prefixes and pre-decision features: artifacts/study_v168.
- All800 raw acquisitions,70 branch states, fixed selections and210 fresh validations: results/v168_native. Real prompts/templates/requests/responses, usage and runtime receipts: results/v168_models.
- Main report/figure: reports/apps_v168.md and results/v168_native/paired_gains.png/svg. Hollow markers identify same-setting comparisons; black cross flags timing instability. Figure visually inspected.
- Independent replay verifies raw objectives/configurations,800 charges, prefix isolation,70 GP-EI decisions by a separate linear-solve calculation, response provenance and20 prefix-policy decisions. Three semantic mutations rejected; artifacts/study_v168/replay.json. It is internal replay, not independent-host collection.
- **1,311 tests passed**,14existing dependency warnings in43.00seconds; all_tests.log. New tests use synthetic namespaces and are excluded from research results. Twelve report/data/figure artifacts regenerate byte-identically with zero new model/native calls; reproduction.json.
- Source download/source schema/protocol/code were fixed before their respective measurements. A cost supplement's attempted pre-response freeze correctly failed because model responses already existed; it was explicitly relabeled exploratory. No primary collection or policy changed. Post-hoc specification: cost.freeze.json; report: reports/cost_v168.md.

## Costs and limits

Actual paired native collection470.697subprocess-seconds including187.919objective-seconds. SmolLM3 requests16.373seconds with4,833/411observable input/output tokens; Qwen3 requests43.791seconds with5,714/581tokens. Ten valid responses each; zero retries, missing usage, malformed responses or fallback. Whole model stages18.315/48.863seconds, peak server RSS3,031,203,840/6,778,339,328bytes, below8GiB. Cold startup separately1.786/4.806seconds. Earlier60feasibility attempts and source/setup costs are additional research costs.

Deployment proxy selects one branch per case:200outcomes/400query-trainingexecutions across ten cases plus policy-selected model calls. It is not measured deployment or energy/dollar cost. Exploratory break-even estimates exist for only two different-setting positive median pairs (neither robust>10%):1,674Polars or1,594XGBoost repeated bundles warm;3,351/2,927cold. Do not present these as observed savings.

New download51,341,771bytes/100MBcap in6.551/600seconds. Cumulative retained downloads10,380,159,186/10GiB;357,259,054bytes remain. Model payload9,126,358,023/9GiB unchanged. Cumulative modelstarts4,855. Recorded-table charges41,613plus2historical incidental exposures unchanged; native-study counters are separate. Disk14GiB free at cleanup. Zero paid/cloud requests, credentials, new model weights, system changes, remote push, publication or external contact.

Hardware sysctl and pgrep inspection were sandbox-restricted; errors are retained. Prior M3Pro/18GiB identity remains historical, current platform/binary linkage/free disk recorded. Cleanup is supported by finite driver and child wait/exit receipts, not a successful system-wide process scan. Minor read-only inspections of not-yet-written or guessed paths failed without changing experiments; Matplotlib used a temporary writable cache. No automatic approval-review rejection blocked this batch.

## Preserve history and resume

Root STATUS/README/THIRD_PARTY/next_experiment snapshots are in artifacts/study_v166/previous_snapshot. V165 manifest SHA256:f03c45727f6a2a002ed2037c869417d462e6eaa6882e9af790c98c4da34c88ac. Latest sealer: scripts/seal_research_v168.py; preserves68historical checkpoints and redirects changed roots to their snapshots. Current manifest and verification receipt are in artifacts/study_v168. All prior exclusions, differing cohort budgets/margins and negative results remain unchanged. Do not pool them into one held-out significance claim.

Safe replay (no measurements):

    MPLCONFIGDIR=/tmp/mpl-v168 .venv/bin/python scripts/reproduce_apps_v168.py
    .venv/bin/pytest -q tests
    .venv/bin/python scripts/seal_research_v168.py --verify-only

Collectors are create-once; do not restart into completed directories. Reproduction requirements are in reports/reproduction_v168.md. This finite batch is closed. New acquisition requires a new prospectively frozen bounded protocol, not silently increased counters.

## Single most important next action

**Replicate the frozen paired application comparison on a second physical host.** Access remains unestablished and no account/connection is assumed. The earlier second-host question is still unanswered; no new permission is needed for already completed local work. Independent-host replication, useful unseen-system router evaluation, full original-method comparisons, broader models and production generalization remain untested. Repeating local prompts or seeds until a positive result appears would not resolve these gaps. The current negative result is concrete and reviewable, but journal acceptance/readiness is not guaranteed.
