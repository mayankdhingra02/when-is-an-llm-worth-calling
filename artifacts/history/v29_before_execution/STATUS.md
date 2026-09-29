# Status — 2026-09-25: V28 cached-response voting completed

## Resume here

**New concrete result:** executed fifteen fixed three-response voting continuations, charging150 new labels. Relative to the fixed assigned-ID single call, voting improves normalized loss by+0.0001779404 but worsens mean relative objective value by0.1326471%. It has2 wins,12 ties,1 loss. A future voting scenario uses45 calls versus15,with318.4311 versus104.4697 historical request-seconds. This is mixed evidence,not a cost-justified robustness fix.

Read [V28 report](reports/consensus_v28.md) and [frozen protocol](reports/protocol_v28_consensus.md). All15 prefixes,three exposed development families,five seeds retained. No new inference:45 real V22 responses were provenance-checked and combined. Each batch selects ten rows by vote count,ties by acquired-only classical shortlist rank. Plans frozen before acquisition;no branch target used to select rows. The exact repeat response is excluded from voting but retained in historical cost.

## Actual execution and checks

- Prepared15 plans from45 real outputs; raw token decoding, exact prompts/mappings/model revision and prefix identities checked.
- Froze153 references before acquisition. All15 arms completed,each10-prefix plus10 new labels.150 new journal entries;no failures,retries or omitted cases.
- 197 tests passed in1.24seconds.
- Independent evaluator replayed15 selections/final states and150 source labels. Decimal verifier checked150 paired metric values,10 aggregate gains and9 usage totals from original sources/raw responses.
- Read-only replay passed. All1823 historical/current frozen references passed integrity checks.
- Initial figure labels crowded; separate presentation script saved inspected readable figure without altering frozen analyzer.

Commands actually executed:

```sh
PYTHONPATH=src .venv/bin/python -m pytest -q
.venv/bin/python scripts/prepare_consensus_v28.py
.venv/bin/python scripts/run_consensus_v28.py
.venv/bin/python scripts/analyze_consensus_v28.py
.venv/bin/python scripts/analyze_consensus_v28.py --verify-only
.venv/bin/python scripts/verify_consensus_v28.py
.venv/bin/python scripts/render_consensus_v28.py
.venv/bin/python scripts/audit_goal_completion.py
```

Preparation was wrapped in the resource ledger. Collection refuses an existing result directory;no restart queued. Read-only verification commands do not acquire labels or invoke inference.

## Evidence

- results/v28_consensus/:15 raw arms,checkpoints,acquisitions.jsonl,progress.json,summary.json,cases.csv,comparison_readable.png/svg and original figure.
- data/consensus_v28.json:all frozen vote plans,source request IDs,usage,vote counts and boundary ties.
- artifacts/study_v28/:actual logs,197-test receipt,Decimal check,all cost receipts,historical audit.
- reports/consensus_v28.md:full comparison,limitations and exact commands.
- Prior docs/ledger:artifacts/history/v28_before_execution/.
- V26 standalone ZIP unchanged;it reconstructs V25 and does not include V27/V28.

## Findings and limits

Mean voting loss0.0096586743. Gains versus original classical+0.0059217131,static rank+0.0016787900,adaptive shortlist+0.0034837975,three-presentation one-call mean+0.0016602832. Relative gains respectively+2.4003%,−0.1695%,+1.0219%,+0.1398%. These are different quality metrics,not interchangeable runtime savings.

Voting exactly repeats a component's selected set in12/15 cases;classical rank resolves a boundary tie in2/15. No vote can beat the best component outcome because its rows are a subset of their union;that is a structural check,not an independent negative finding. Novel prompts/presentations,fresh inference,new-host execution,held-out routing and application utility remain untested. No generalization or significance claim.

New recorded-label acquisitions150;historical total7208. Physical trials unchanged1134. New model requests0;follow-up cap remains200/200 (300 total including initial stage). New downloads and spend0. All four stage costs total3.139294210seconds. Ledger2256.214322631/3600seconds;1343.785677369 remaining;active_since:null. No workers,scheduled campaigns,publication,push or contact.

**Single next action:** define a prospective application quality/latency tradeoff and untouched evaluation families before new inference;retain static shortlist and a fixed single-call control. Do not adopt three-call voting from these mixed exposed-data results or tune its weights post hoc.
