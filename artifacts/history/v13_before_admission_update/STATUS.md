# Status — 2026-09-24, bounded pilot closed for review

## Resume here

Read **reports/decision_brief.md** first, then this file and the relevant frozen protocol/code. No need to reread the original deep-research report. The original implemented pilot and independent unblocked follow-ups are complete. There is **no demonstrated useful LLM selection or benefit-router advantage**. Do not continue until positive by changing thresholds, selecting favorable cases or consuming unspecified resources.

The latest user instruction, “Do what you think is right,” prompted a review consolidation rather than more inference. The decision is to review the application task/utility and evidence of opportunity before scaling. No experiment, source freeze or outcome was changed in this documentation pass.

## Results that matter

- Corrected V3: three systems × five fixed seeds, budget 20/checkpoint 10; classical and real local-model paired smoke completed.
- V6: three development and three held-out families. On 15 held-out cases, never-escalate mean loss 0.06150 versus always 0.07458. Benefit and uncertainty policies both select zero escalations; no selective advantage. Only three independent test groups.
- V8: all 15 real candidate-selection outputs choose the first ten displayed IDs. A trivial order rule exactly reproduces the observed row sequences.
- V9: exact uniform-subset references independently enumerated all 184,756 subsets per case. Random selection matches/beats each observed LLM result with probability at least 0.5. Conditional finite-pool diagnostic, not a p-value or unseen-system result.
- V10–V11: documented metric sensitivity and runtime/size hindsight opportunity; no achieved LLM improvement.
- V12: all 20 constrained classical branches completed, adding 300 charged runtime/size configuration vectors on two development families. Nearest-neighbor versus random relative gain: lrzip +4.82%, Brotli −2.79%, equal-family +1.01%. Mixed point estimates, not statistically established. Ideal remaining headroom after the cheap method is 0.37% lrzip and 9.09% Brotli; two cases above 10%, both Brotli.

All recorded evaluations are table acquisitions, not new live benchmarks. V12 charges both outcomes as one vector; earlier stages mostly acquired one target. Preserve differences between treatments and metrics. Hindsight is never a deployable policy.

## Current evidence and verification

- Review entry: reports/decision_brief.md; README.md; REPRODUCE.md.
- Source/provenance: reports/source_audit.md; THIRD_PARTY.md; artifacts/source_manifest.json; artifacts/model_manifest.json.
- Held-out routing: results/v6/ (raw prompts/responses, prefixes, acquisitions, fitted controller, policy CSV and figures); reports/pilot_report_v6.md.
- Direct-selection evidence and exact reference: results/v8/; results/v9_analysis/; reports/concrete_result.md.
- Latest actual controls: results/v12_controls/acquisitions.jsonl, prefixes/, joint_3nn/, random/, progress.json, summary.json, outcomes.csv and source_snapshot/.
- Latest experiment validation: artifacts/study_v12/collection.log, analysis_verification.log, verification.json and tests.log (95 tests passed). Replay reproduced every choice using only acquired labels, source values, 20-label arm budgets, shared prefixes and all 300 charged accesses.
- Historical V10/V11 analyses/replays: results/v10_headroom/, results/v11_quality/, artifacts/study_v10/, artifacts/study_v11/.
- This review pass: scripts/verify_review_packet.py; artifacts/review_packet/verification.json and verification.log. Passed: nine scientific freeze maps (925 file references), headline arithmetic, 300 journal entries, 30 local document links and unchanged accounting. This is not fresh experimental replication.
- Previous mutable documents: artifacts/history/v12_before_review_cleanup/. Historical evidence indexes remain unchanged; mutable documentation snapshots are preserved there. New review index: artifacts/review_packet/evidence.json.

Commands for this review pass:

```sh
.venv/bin/python scripts/verify_review_packet.py
```

Earlier collection/test commands, with their exact roles and replay limitations, are in REPRODUCE.md. No historical result was overwritten to update a summary.

## Costs and authorization

This review pass adds **0 model calls and 0 configuration acquisitions**. Historical totals: **228 request attempts** (100 initial + 128 follow-up), **4,508 charged configuration accesses**, cumulative recorded experiment/analysis time **1,671.4778/1,800 seconds**, leaving **128.5222 seconds**. Tests/documentation/forensic inspection are not charged collection time. Follow-up allowance is **128/128 exhausted**; ledger inactive. Downloads remain 1,412,812,979 bytes including 999,602,607 model bytes; external spend USD 0.

No new model, download, paid service, cloud resource, external contact, push or publication. Nothing is scheduled outside this session. The exhausted allowance blocks new inference, but the scientific recommendation is also to redesign the task before spending more.

## Single next action and remaining uncertainty

**Review and specify an application-grounded runtime/size/correctness task before authorizing further inference.** If justified, prospectively define admission, margins and cheap-control headroom checks on development systems; then freeze a bounded model/order test and genuinely untouched evaluation families. See reports/next_experiment.md.

Still untested: stronger local models, fresh order-permutation responses, live correctness and repeated benchmark noise, application-approved utility, other budgets and broad router generalization. Current evidence cannot assign a credible numerical probability of eventual positive LLM results. The packet is ready for the user's discussion with Tim; no message was sent.
