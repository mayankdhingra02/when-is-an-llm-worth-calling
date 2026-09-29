# V20: order dependence is observed; the selection mechanism is not unique

**Two simple rules exactly reproduce every saved V8/V19 response:** taking the first ten displayed IDs, and continuing an ascending/descending canonical ID sequence from the first displayed ID. This does not undo V19's controlled display-order effect. It narrows what that experiment identifies, because every tested ID order was monotone.

| Behavioral rule | Exact V8 sequence matches | Exact V19 sequence matches |
|---|---:|---:|
| First ten displayed |15/15|9/9|
| Lowest IDs0–9 |15/15|3/9|
| Highest IDsJ–A |0/15|6/9|
| Continue ID sequence from displayed endpoint |15/15|9/9|

Selected-set matches equal sequence matches here. V8 used one display-ID order; V19 used two, ascending and descending. All24 responses were included, with four comparisons each; repeated cases/conditions are not24 independent systems. The rules are post-hoc behavioral alternatives, not inferred model source code or an exhaustive list of explanations. No statistical test or quality score was computed.

The endpoint rule starts at the first displayed ID and steps in canonical ID rank by the sign of the second-minus-first rank. It is undefined if ten steps leave the20-ID domain; undefined predictions remain in the denominator (none occurred in these measured inputs). Both rules coincide on the tested monotone lists. Thus the result supports sensitivity to the display intervention, while an exclusive claim that the model literally copies a list prefix would be too strong.

An interleaved assignment0,J,1,I,…,9,A separates their predictions: displayed prefix0,J,1,I,2,H,3,G,4,F versus sequence0,1,2,3,4,5,6,7,8,9. Those are **rule predictions, not model responses**. Three feature-preserving prompt designs were saved under artifacts/study_v20/unexecuted_designs.json and then prepared as the separately frozen [V21 proposal](nonmonotone_probe_v21.md). Actual responses remain unknown.

## Actual execution and evidence

The fixed post-hoc audit was frozen before computing all96 comparisons. The initial run and --verify-only replay agreed exactly on all24 saved responses.139 tests passed for the audit; the subsequent preparation suite has140 passing tests. No model calls, objective acquisitions, physical measurements, downloads or spending occurred. Full-table targets were not read.

[Protocol](protocol_v20_rules.md), [10-file freeze](protocol_v20_rules.freeze.json), [machine summary/all comparisons](../results/v20_rule_audit/summary.json), [rule table](../results/v20_rule_audit/rule_matches.csv), [execution log](../artifacts/study_v20/analysis.log), [replay](../artifacts/study_v20/replay.log).

Executed commands: `.venv/bin/python scripts/audit_rules_v20.py` and the same command with `--verify-only`. The first refuses overwrite; the latter recomputes saved-source comparisons and charges runtime without inference. Source inputs and prior scientific freezes are unchanged. The audit charged0.0087seconds. No new empirical mechanism response is asserted here.
