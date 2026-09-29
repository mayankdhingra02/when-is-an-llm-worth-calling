# STATUS — V103 complete: delivery restored, no useful escalation gain

Resume here. The user's Mac restart was confirmed. V101 repeated the old512-token-thought feasibility test: nonthinking returned, but thinking still timed out. V102 separately reduced only the thought ceiling to128tokens and passed both final-answer checks. V103 then ran a fresh, frozen24-condition development comparison. No new experiment is queued.

## Latest concrete result

Six exposed software-system groups, seeds11/37 chosen before outcomes, two modes,12sharedprefixes. All36 real local Qwen3-8B requests returned;22/24 final answers were valid. Thinking10/12valid; nonthinking12/12valid. The two thinking failures were OpenVPN11 (nine IDs) and SAC11 (final-output limit/invalid format). They received the predeclared classical fallback without repair. No retries, missing responses, transport failures or unattempted conditions in V103.

Group-first mean gains versus sequential3NN: thinking **-7.64%**, nonthinking **-6.52%**. Versus batch3NN: **-3.97%** and **-2.74%**. Both modes had **zero valid >=5% wins over BOTH strong controls**. BerkeleyDB37 improved about5% against sequential alone, but thinking tied batch and nonthinking was slightly worse than batch. Do not present that as a gain requiring an LLM. Dune contributes substantially to the mean loss; no claim of uniform harm or population significance.

All24 intended continuations acquired ten new recorded outcomes after the same saved ten-evaluation checkpoint:240chargedtableacquisitions, logicalB20 per arm. Historical prefix/reference cost remains separately counted. These are recorded-data outcomes, not new native software timings. No controller or threshold was fit to these results.

## Runtime, validation and files

V103 lifecycle936.011s (15.60min); peak sampled modelRSS8,356,478,976bytes below8GiB; serverexit0.36requests,4608allocatedoutputtokens,2122actualgeneratedtokens and60,806actualprefilltokens. Thinking used24requests/1882generatedtokens, mean55.64s per case; nonthinking12requests/240tokens, mean22.16s. These are measured research-collection costs, not modeled deployment savings. No new downloads, paid/cloud use, credentials, publication or app/system-setting changes. Owned model processes exited.

Independent replay verified all24conditions/240savedacquisitions, prefix lineage, states and metrics with zero new labels/calls. Full suite777passed in23.45s; three added synthetic corruption tests also passed, for780currenttests. Synthetic altered copies are excluded from research data. Five report/derived-table/figure outputs reproduced byte-for-byte and the figure was inspected. Test logs and integrity receipts live in artifacts/study_v103/.

Read **reports/research_readiness_v103.md** for interpretation, **reports/reasoning_v103.md** for the full comparison and **reports/protocol_v103.md** for the pre-outcome design. Raw journals: results/v103_reasoning/. Acquired cells/metrics/figures: results/v103_analysis/. Freeze SHA1d816bfd9fea621dd6d1f293a56affe8ab3c0bb72524a04251c9033d7ec066c6 pins97files. Current snapshot-aware seal: artifacts/study_v103/evidence_manifest.json; final verification: artifacts/study_v103/seal_verification.json. Prior root documents are preserved under artifacts/study_v103/previous_snapshot/; earlier records were not overwritten. README is now a concise current entrypoint and links the preserved historical version.

Safe replay with no inference or new objective acquisitions:
```
.venv/bin/python -m pytest tests -q
.venv/bin/python scripts/verify_reasoning_v103.py
.venv/bin/python scripts/audit_usage_v103.py
.venv/bin/python scripts/report_reasoning_v103.py
.venv/bin/python scripts/seal_reasoning_v103.py --verify-only
```
Do not rerun collect_reasoning_v103.py or analyze_reasoning_v103.py into existing output: those are once-only collection/acquisition steps. Historical standalone seals require their preserved root-document versions; use the latest snapshot-aware sealer.

## Preceding attempts and cumulative accounting

V101:2realrequests/1response,137.293s,peakRSS5,954,420,736bytes,exit0; thought timeout at120s, missing usage unknown. V102:3requests/3responses,2validfinals,211.675s,peakRSS5,958,451,200bytes,exit0;168generated/10,035prefilltokens. Both acquired zero new objectives. They are feasibility stages, not independent-system quality evidence. Their41combined-with-V103 requests are all counted. The restart and reduced thought budget are distinct interventions; exact cause of the earlier slowdown is not established. All V98–V101 failures remain preserved.

Cumulative real-model requests **3,938**; recorded-table acquisitions **27,978**. Native numerical acquisitions790 acrossV94/V96/V97, physical solves counted separately. Older native counts unchanged (DuckDB78physical,H2299,Kanzi1265,RocksDB350). Downloads9,870,221,104bytes/10GiB, remaining867,197,136; modelpayload9,126,358,023bytes/9GiB unchanged. External spend0; electricity/hardware cost unknown. Cumulative token usage is not fully known because older requests lost responses.

V97 remains the latest completed native workload comparison:250validnativeacquisitions/50validmodelcalls, no >=5% LLM win over either strong control in five exposed SuperLU seeds. V103 is the latest completed recorded-data model comparison.

## Next action and remaining uncertainty

**Single highest-priority next action: freeze an independent-system replication before inspecting new continuation outcomes.** See reports/next_experiment.md. Local short-budget inference now works; another unchanged restart/feasibility loop is not the next step. The V10336-request allowance is consumed; fresh collection requires its own bounded protocol and output namespace.

The128-token reasoning allowance is very short; mode-specific sampling differs too. All six groups are exposed development data, with only two seeds each. Stronger models/larger reasoning budgets, independent-machine replication, broader untouched-system performance and a useful benefit-aware controller remain untested or unestablished. No second host is connected. Q2 readiness is not established. Do not tune the exposed cohort until a positive result appears or treat fallback quality as an LLM achievement.
