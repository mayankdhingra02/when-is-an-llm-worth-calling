# Status — 2026-09-24, v8 controls complete; bounded inference approval pending

## Resume here

The prior v7 negative result is complete and preserved. This session implemented and froze **v8 direct candidate selection**, then actually ran **30 classical controls, 300 new target acquisitions, zero new model calls**. All **64 tests passed**, and independent replay checked all30 branch states, source labels, prefixes, shortlist choices and budgets. All earlier scientific freezes remain intact.

Start with reports/pilot_report_v8.md and reports/protocol_v8.md, then relevant v8 code. For the overall evidence and discussion, read reports/review_note.md. The latest held-out routing result remains reports/pilot_report_v6.md; v7 and v8 use development groups only. Do not reread the original deep-research report. Previous root documentation is preserved in artifacts/history/v7_before_v8/.

## What changed and ran

Same three development systems (MySQL, lrzip, Brotli), all five seeds [11,23,37,53,71], exact saved v6 prefixes, checkpoint10 and logical budget20. Use acquired-label centroid scores to shortlist20 unevaluated recorded rows. Shuffle ID assignment with seed+70000. The prepared real-model adapter selects ten distinct IDs by greedy local-model logits; it does not project feature strings. No v8 model output has been generated.

Both new controls share the same shortlist: static classical top10 and uniform sampling without replacement (seed+40000). Each arm acquired ten new labels per case. Source snapshots and raw acquisition journal are saved. The120-file freeze includes scientific code, tests, protocol, data/prefix/comparator hashes, frozen pools and prompt digests. Fifteen real-tokenizer synthetic traversals passed without inference; fixtures are not measured outputs.

Executed commands:

```sh
PYTHONPATH=src .venv/bin/python -m pytest -q
.venv/bin/python scripts/prepare_v8.py
PYTHONPATH=src .venv/bin/python -u -m escalation.study_v8 controls
PYTHONPATH=src .venv/bin/python -m escalation.analyze_v8
PYTHONPATH=src .venv/bin/python -m escalation.study_v8 preflight
.venv/bin/python scripts/verify_v8.py
.venv/bin/python scripts/report_v8.py
```

Preflight returned exit2 intentionally: zero authorized model requests remain. All30 controls completed; all15 LLM cases remain blocked in the full45-branch denominator. No failures were omitted. No worker/background inference is running.

## Actual control results

Per-family mean normalized loss (lower is better), five seeds per family:

| Family | Existing adaptive classical | New uniform shortlist | New static shortlist | Shortlist hindsight diagnostic |
|---|---:|---:|---:|---:|
| Brotli | .000690 | .000507 | .000415 | .000415 |
| lrzip | .001392 | .001038 | .001392 | .000763 |
| MySQL | .044660 | .039642 | .032206 | .025375 |

Hindsight reads hidden labels only in retrospective evaluation and is not a deployable policy or free optimizer acquisition. These controls show potential headroom but do not show that an LLM can exploit it. No treatment changed after examining results. Per-seed outcomes: results/v8/outcomes.csv. Figure results/v8/comparison.png was visually inspected; editable/reproducible SVG and generator retained.

## Evidence

- Protocol, freeze, manifest: reports/protocol_v8.md, protocol_v8.freeze.json; data/manifest_v8.json.
- Raw collection: results/v8/acquisitions.jsonl; uniform_selection/; static_rank/; checkpoints/; starts/.
- Complete intended denominator: results/v8/progress.json.
- Machine analysis: results/v8/summary.json and outcomes.csv; figures comparison.png/svg.
- Source snapshot: results/v8/source_snapshot/.
- Actual logs: artifacts/study_v8/control_collection.log, control_analysis.log, control_verification.log, tests.log.
- Verified machine evidence: artifacts/study_v8/verification.json; preflight.json; tokenizer_preflight.json.
- Human report: reports/pilot_report_v8.md; overall review note: reports/review_note.md.

## Limits, permission and exact next action

Shared follow-up requests **113/113**; historical total including v1 **213**. Historical charged objective accesses **4058** (3758 before v8 +300 controls). Experiment runtime **1633.426451/1800 seconds**, **166.573549 seconds left**, inactive ledger. No new model weights/packages/downloads. Downloads remain1412812979bytes, model999602607bytes; external spend USD0. Coding, unit tests and forensic verification are not mislabeled experiment-collection time.

A concrete async question asks to raise only the cumulative follow-up cap **113→128** for fifteen real local Qwen calls. configs/authorization_v8.json remains granted:false/current113 until explicit approval. The existing cumulative1800-second runtime cap, USD0 spending, model/download limits and historical ledger stay unchanged. The user's generic instruction to continue until a good-enough result is not recorded as approval for a silent cap increase (AGENTS.md forbids that). No extra permission is needed for the already completed controls.

**Single next action:** resolve that bounded fifteen-call approval; if approved, record the exact response/timestamp, run `PYTHONPATH=src .venv/bin/python -u -m escalation.study_v8 llm`, then analyze, independently verify, regenerate report/figures and update this status. Preserve this preapproval state first. If approval is declined or runtime exhausts, finalize existing evidence with the LLM arm explicitly incomplete. Do not reset ledger or reuse exposed test groups as untouched data.

After this one frozen comparison, synthesize the negative or positive finding for review rather than keep tuning until success. A learned router's generalization, a stronger model, empirical nonbinary tasks, wider independent system groups and a fresh held-out evaluation remain untested. Existing v6 had no observed router advantage and only three held-out groups; v7 prevented copies without material improvement. Nothing is scheduled outside the active session.
