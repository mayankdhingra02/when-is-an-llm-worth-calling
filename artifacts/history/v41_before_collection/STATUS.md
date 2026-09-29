# STATUS — V40 analysis executed; exploratory paper draft complete

Updated2026-09-25. Resume from this file, [V40 results](reports/frontier_v40.md), [paper draft](paper/manuscript.md), [readiness assessment](paper/readiness.md), and the frozen protocol. Prior mutable docs/ledgers are in `artifacts/history/v40_before_analysis/`.

## New concrete research result

Executed all30,720allocation comparisons across30comparator/presentation scenarios and330call-budget points. Against runtime3NN, even hindsight escalation plus best-tested-presentation selection cannot improve recorded feasible runtime. Assigned-ID oracle opportunity versus joint3NNshortlist is1.9745%(2calls),but only0.3238%(1call) under worst-tested presentation. The V38positive primary comparison remains1.7534%;dropping one influential Brotli case reduces its equal-family mean to0.0475%. All cases remain reported.

264tests pass in1.34s. Independent integer/combinations enumeration agrees with fractional/sorted/bitmask calculations on Python3.10/3.12. All results are descriptive finite-case bounds on two exposed systems; hindsight policies are not deployable. No learned-router success or new independent groups were added.

## Paper work completed

- `paper/manuscript.md`: complete exploratory short-paper candidate,including methods,prior work,results,formal finite-case implication,costs,reproducibility,threats and limitations.
- `paper/references.bib`,`paper/claim_evidence.md`,`paper/readiness.md`.
- `reports/literature_update_v40.md`: original sources verified. Close prior HPO paper overlaps with strong-baseline caution; order sensitivity is established prior art. Neither generic observation nor the elementary dominance bound is claimed novel.
- `results/v40_frontier/`: fullJSON,330-rowCSV,PNG/SVGfigure.
- `artifacts/study_v40/`:actual analysis/test/replay/independent-interpreter/claim-check receipts.

The evidence supports writing/discussing a narrow exploratory negative-results paper. Novelty,submission readiness and acceptance are not established. A broadly useful benefit-router paper still needs new data. No authorship,venue,contact or submission has been assumed.

## Commands actually run

```
.venv/bin/python -m pytest -q
.venv/bin/python scripts/analyze_frontier_v40.py
.venv/bin/python scripts/analyze_frontier_v40.py --verify-only
.venv/bin/python -I -S scripts/verify_frontier_v40.py
/Users/mayankdhingra/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3 -I -S scripts/verify_frontier_v40.py
.venv/bin/python -I -S scripts/verify_paper_v40.py
```

Collection code and prior data were untouched. New computation/rendering charged0.731785s;total2531.528508/3600s,remaining1068.471492s. Requests230/230(330includinginitial),recordedvectors9608,physicaltrials1274. No new model call,objective acquisition,physicaltrial,downloadedmodel/data file or externalspend. Primary pages inspected through web tools. No background task,no remote publication/push/contact.

## Reproduction and remaining work

V39.1archive `output/llm_escalation_v38_reproduction_v39_1.zip` still reconstructs V38; it does not contain V40. Its existing hash and rawV38outputs are unchanged. V40replay and independent checker use savedV38summary and frozen source bindings; portable input retokenization/model logits,independent physical machine,physical uncertainty/correctness and unseen-system routing remain untested.

**Single most important next action:** have the narrow paper's contribution reviewed against the close prior work before authorizing new collection. Any broader study needs independently admitted untouched groups and application utility,not further tuning of the exposed cases. All230model calls remain exhausted; do not silently expand the cap or present this draft as a proven novel/generalizable method.
