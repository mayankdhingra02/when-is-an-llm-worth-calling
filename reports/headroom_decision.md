# Headroom decision: stop the same-design stronger-model rerun

**I do not recommend spending more model calls on the current fifteen cases with the same twenty-row shortlist and .02 material-improvement criterion.** Even a perfect selector could materially beat the cheap static-ranking control in only **1/15 cases**, from **one software family**. That offers too little breadth for the proposed cross-system benefit-router experiment. This is a decision about this design, not proof that stronger LLMs or software optimization cannot help.

## Actual no-call check

All three development systems and all five fixed seeds were included. No cases were chosen after inspecting which looked promising. The analysis used saved prefixes, feature-only shortlists, baseline states and recorded outcomes. It made **zero new model calls and zero optimizer acquisitions**. Full-table values were read only for retrospective scoring, not supplied to a model, optimizer or router. Earlier protocols, outcomes and the .02 margin remain unchanged.

A perfect ten-row selection can include the best recorded candidate in its allowed pool. This gives an upper bound on improvement, assuming hindsight access to labels. It is not a deployable selector, a learned policy or a measured arm. Source values, normalization, saved V8 hindsight minima and V9 distribution minima were cross-checked; **84 tests passed** and independent replay verified all120 comparison/bound records.

| Comparator | Perfect selector's allowed pool | Cases with possible gain >.02 | Families with such cases | Maximum mean normalized-loss gain |
|---|---|---:|---:|---:|
| Cheap static ranking | Same20-row shortlist | **1/15** | **1/3** | **.002487** |
| Adaptive classical | Same20-row shortlist | 2/15 | 1/3 | .006729 |
| Observed LLM | Same20-row shortlist | **0/15** | 0/3 | .001381 |
| Cheap static ranking | Entire recorded table | 3/15 | 1/3 | .011337 |

The primary comparator is fixed static ranking, an implementable measured baseline. It is not a hindsight selection of whichever cheap algorithm happened to win each case. Uniform expectation and other comparators are also retained in the machine results. The one primary material opportunity is MySQL seed23. Descriptive margin sensitivity at .005 and .01 still gives only one same-shortlist opportunity over static ranking; no new margin was selected.

The zero above the observed LLM means no material improvement at the existing threshold—not that perfect selection could never make a smaller improvement. Its previously observed choices remain exactly the first half of the randomized display; the oracle bound does not rehabilitate those choices as learned ranking.

## Two design problems revealed

**The shortlist already captures most of what the cheap ranking can exploit.** Static ranking attains the shortlist's best terminal loss in every Brotli case. There are small additional lrzip opportunities, but only one MySQL case exceeds the frozen material threshold. A stronger model cannot create better candidates outside the list it is allowed to choose from.

**The normalized threshold can obscure meaningful raw changes.** A .02 reduction in this one-target min–max loss equals .02 times the full recorded target range:

| System | Recorded target minimum | Maximum | .02 margin in original units |
|---|---:|---:|---:|
| MySQL | 50.99952 | 143.22396 | 1.844489; runtime unit unspecified by source |
| lrzip | 15373.6 | 458834.0 | 8869.208; runtime unit unspecified by source |
| Brotli | 1.46 seconds | 394.158 seconds | **7.85396 seconds** |

Brotli's static-control best runtimes are only1.526–1.900 seconds. Even an impossible zero-runtime result could not improve them by7.85 seconds. Yet the recorded full-table minimum1.46 seconds would represent relative reductions of4.3–23.2%. Those rows lie outside the useful shortlist for the relevant prefixes. Thus a failure to clear .02 is not evidence of no possible application-level value.

For lrzip seed37, perfect same-shortlist selection reduces the primary target from16727.8 to15373.6, about8.1%, but its normalized gain is only.003054. These raw comparisons are descriptive bounds. Compression quality/output size is not matched by this single-target pilot, so a faster row is not automatically a practically preferable configuration. The historical metric is not changed retroactively to claim success.

## Decision and next action

**Stop this exact rerun. Do not authorize a stronger-model run merely by swapping the model into the existing setup.** The headroom is concentrated in one family, and the current threshold is not a consistent application-level benefit criterion across systems. Repeated seeds would not fix either issue.

The next research action is to agree on an application-grounded minimum useful improvement and required quality constraints, then design a candidate-pool/task selection protocol with enough independently grouped opportunity before requesting more inference. Preserve the current results as negative/exploratory evidence; any changed metric or candidate formulation needs a new protocol and fresh evaluation groups. A subsequent order-permutation test remains relevant once that opportunity exists, but it is not the immediate compute priority.

This does not establish that a positive routing result is impossible. It does show why another stronger-model run under the present rules is a poor next bet. No new model experiment has been started or implied by this analysis.

## Evidence and reproduction

- Specification and frozen inputs: `reports/protocol_v10_headroom.md` and `.freeze.json`.
- Per-case raw and normalized bounds: `results/v10_headroom/cases.csv` and `summary.json`.
- Executed analysis: `scripts/analyze_headroom_v10.py`; output `artifacts/study_v10/analysis.log`.
- Independent replay: `scripts/verify_headroom_v10.py`; `artifacts/study_v10/verification.json` and `.log`.
- Tests: `tests/synthetic/test_headroom_v10.py`; complete84-test output in `artifacts/study_v10/tests.log`.

```sh
PYTHONPATH=src .venv/bin/python -m pytest -q
.venv/bin/python scripts/verify_headroom_v10.py
```

The analysis refuses overwrite of completed outputs. No hidden-label-derived number in this report was used to change a measured treatment. No dollar spending, download, publication, external contact or background job occurred.
