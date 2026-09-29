# Resume checkpoint: V170 complete

Start here, reports/research_assessment_v170.md, reports/protocol_v169.md, reports/protocol_v170.md and relevant code. Do not reread the deep-research report. **New result:** source-executed EZR controls across six native implementations do not reveal a robust local-model advantage over sequential 3NN or EZR Bayes. This strengthens bounded negative evidence; a useful general learned router and Q2 readiness remain unestablished.

## What actually ran

V169 executed 20 new centroid/Bayes continuation arms on Polars/XGBoost and revalidated 70 historical selections. V170 executed 40 new arms on all earlier cvc5, OR-Tools, ripgrep and hnswlib implementations and revalidated 140 historical selections. Every case uses one of the original seeds 11,23,37,53,71. Protocols, source/runtime, prefixes and inputs were frozen before new collection; these exposed-task control extensions remain secondary/exploratory.

Across both stages: **1,230 new objective outcomes, 2,460 native workload executions, 420 search labels and 810 validation labels**. All 60 new source arms use ten cached prefix labels + seven new search outcomes + three fresh validations (B20). All 270 selections were fixed before randomized three-block validation. The 630 extra validations of 210 historical selections are research costs outside the old closed policy budgets. Three hundred unique historical prefix outcomes were reused through 600 logical cached callbacks; none was reacquired. Sixty historical real responses underpin the model selections; **zero new model calls or downloads** occurred.

V169 completed 410/410 intended outcomes in 213.014/1,800 seconds. V170 completed 820/820 in 247.603/1,800 seconds. No retry, worker or bridge failure; all 60 optimizer subprocesses exited 0 and native children were waited. Both finite collectors, replay commands and test sessions completed. No model server, automation or indefinite job was started. Cleanup uses child wait/exit receipts, not an asserted successful system-wide process scan.

## Result and interpretation

The synthesis in reports/ezr_synthesis_v170.md reports each implementation/model separately. Across 60 model cases there were zero robust >10% gains over sequential or EZR Bayes and zero joint wins over sequential, adaptive, GP-EI, EZR centroid and EZR Bayes. Seeds are not independent software systems; no pooled significance inference is made.

The favorable exception is preserved: Qwen/XGBoost seed 37 beat GP-EI by 22.683% and EZR centroid by 20.893%, but lost to sequential by 1.550% and EZR Bayes by 1.187%. Mean XGBoost gains vs sequential were -26.111%/-19.525% for SmolLM3/Qwen3. Tiny favorable means on some other comparisons are not robust gains.

All 270 final validation cells met their quality constraints. Fourteen search outcomes received the fixed quality penalty and remain charged. Four Polars cells were unstable; 40/45 OR-Tools cells were below the 10 ms floor. All remain in unfiltered summaries. The robust rule requires >10% gain, distinct settings, valid quality, relative MAD <=5% and medians >=10 ms. This secondary floor does not replace the older solver cohort's primary rule. Failure to pass is not equivalence or proof of no opportunity.

Six implementations do not equal six independently sampled production tasks: cvc5 and OR-Tools use constructed N-queens problems; Polars reuses an earlier DuckDB flight contract. All collection uses one host. New EZR searches happened later than historical searches; joint fresh validation cannot remove search-selection timing effects. No model/router was improved or newly evaluated on held-out systems in this extension.

## Source integrity and adaptation

Original timm/ezr 0.9.4 commit bfda80b3b797d142378f7fb8746c3485610fb17e executes unchanged through scripts/ezr_bridge_v169.py. Source SHA256 d0fdb7ac6242cc7d8eec8ced3abec1c1e89d405326dfe384525c63f0ad92b2ad; original MIT notice retained. Existing Python 3.13.3 supports its syntax; binary and source hashes are frozen. No system installation. Retained primary provenance verified; live blob/raw web-viewer rechecks returned Cache miss, so current HEAD was not claimed verified.

Injected prefix/order, learn.start=10, learn.budget=7, typed features, scalar loss and raw-loss incumbent choice are explicit adaptations. Source normalization, smoothing and cached-rest-centroid behavior are retained literally. This is not full from-scratch EZR or SNAP2 replication. Optimizer stdin has raw features and only acquired prefix labels; later labels arrive one at a time from the isolated native evaluator. Unknown objectives are question marks. Historical model outputs are never synthesized or replaced.

## Evidence and verification

- Protocols/configs: reports/protocol_v169.md, reports/protocol_v170.md, configs/study_v169.json, configs/study_v170.json.
- Source/runtime/dependency and prefix freezes: artifacts/study_v169 and artifacts/study_v170. Existing solver runtime checked against all 187 prior binary hashes after collection; solver_binary_verification.json is labeled post-collection.
- Raw optimizer inputs/events, native outputs, selections, validations, ledgers and completion receipts: results/v169_ezr and results/v170_ezr.
- Reports: reports/ezr_v169.md, reports/ezr_v170.md, reports/ezr_synthesis_v170.md. Figures: results/v169_ezr/baseline_gains.png/svg and results/v170_ezr/baseline_gains.png/svg; visually inspected.
- Replay verifies all 1,230 charges, saved prefixes, selection barriers, literal source choices and separate native-output/quality checks. Three semantic corruptions rejected per stage. Same-source replay is not an independent optimizer implementation or second-host experiment.
- **1,325 tests passed**, 14 dependency deprecation warnings, 32.97 seconds; artifacts/study_v170/all_tests.log. Synthetic fixtures stay in tests/synthetic and outside research aggregates.
- Five V169 and seven V170 analysis artifacts reproduce byte-identically without new objective/model calls; reproduction.json in each stage. Safe commands in reports/reproduction_v170.md.
- Critical interpretation: reports/research_assessment_v170.md. Accounting/exit and timing exceptions: artifacts/study_v170/closeout.json.

## Cost and remaining limits

New collection wall time 460.617 seconds across two independent 1,800-second caps. Source/bridge CPU 0.176132 seconds excludes native children and is not directly comparable to model end-to-end wall time. Historical source/model acquisition remains additional research cost. Extra diagnostics do not become a deployment policy; no new deployment/energy/dollar result is claimed.

Cumulative model starts remain 4,855; recorded-table charges remain 41,613 plus two historical incidental exposures. Native-stage counters are separate. Retained downloads 10,380,159,186/10 GiB, remaining 357,259,054 bytes. Model payload 9,126,358,023/9 GiB unchanged. No paid/cloud requests, credentials, new weights, global settings/installations, external contact, publication or remote push. No automatic approval rejection blocks this completed stage.

## Preserve history and resume

V168 manifest SHA256 067ba9fe1c3e80744a72241b28a9dd7f7eb3e30522236d26a4cfc14c74adffdb verified before editing. Previous roots are in artifacts/study_v169/previous_snapshot. Current sealer scripts/seal_research_v170.py preserves 69 historical checkpoints and redirects changed roots to verified snapshots. Latest evidence manifest and verification receipt are in artifacts/study_v170; that receipt records its hash.

Safe replay:

    MPLCONFIGDIR=/tmp/mpl-v169 .venv/bin/python scripts/reproduce_ezr_v169.py
    MPLCONFIGDIR=/tmp/mpl-v170 .venv/bin/python scripts/reproduce_ezr_v170.py
    .venv/bin/python scripts/seal_research_v170.py --verify-only

Collectors and preparation/adapter generation are create-once. Do not rerun them into completed directories. New collection requires a new frozen bounded protocol. Earlier failed attempts, differing cohort budgets and negative results remain preserved and cannot be pooled into one held-out study.

## Single most important next action

**Obtain access to a second physical host and replicate the paired application comparison with all search arms collected in the same campaign.** Access remains unestablished; the earlier question is still unanswered. No credentials or remote connection are assumed. Independent-host replication, adequate unseen-system controller evaluation, full original-method replication and broader model generalization remain untested. Local source-baseline work is now complete; more exposed seeds would not resolve those gaps. See reports/next_experiment.md.
