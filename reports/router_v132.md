# V132: frozen historical controller, two new families

All ten decisions were frozen before V131model-continuation or fresh timing-validation outcomes were acquired. Eight historical training groups/40cases; two new groups/10cases. Features use only B10observations and feature-domain metadata. No new model or native trials beyond charged V131collection.

| Policy | Calls /10 | WavPack gain | FFTW fresh gain | Missed >1% | Harmful >1% |
|---|---:|---:|---:|---:|---:|
|never|0|+0.0000%|+0.0000%|1|0|
|always|10|+0.0058%|-1.5160%|0|2|
|benefit|0|+0.0000%|+0.0000%|1|0|
|uncertainty|0|+0.0000%|+0.0000%|1|0|
|random_development_rate|0|+0.0000%|+0.0000%|1|0|
|random_matched_realized_rate|0|+0.0000%|+0.0000%|1|0|
|hindsight_oracle_diagnostic|3|+0.0117%|+0.2204%|0|0|

The hindsight row is non-deployable: it uses observed outcomes to pick the branch and cannot be assigned an ordinary model-call cost. Matched-realized random uses only the saved pre-decision escalation count but is a batch diagnostic. Practical1%benefit/harm counts use raw paired outcomes; FFTWsame-configuration differences are timing variability, not evidence of distinct configuration benefit.

Benefit controller selected 0/10 escalations. Uncertainty selected 0/10. When both collapse to never, neither establishes learned selective advantage or H1/H2; their identical scores/call counts must not be presented as superiority over a classical baseline. Actual V131research still used10model calls to observe both branches; counterfactual deployment counts do not erase those costs.

Development-only calibration used leave-one-group-out ridge predictions (training-only scaling, group weights) for benefit and fixed acquired-label bootstrap-best dispersion for uncertainty. Thresholds maximize development paired gain, breaking ties toward fewer calls. The resulting zero development rate is retained without forcing a favorable nonzero rate. Heterogeneous historical treatment/output contracts, selection metrics and task domains limit transfer interpretation. SACstructural failures were excluded from model fitting only and remain in historical reliability/cost denominators.

Two test families cannot establish population generalization, confidence bounds, superiority, novelty or Q2readiness. No re-fitting, test threshold selection, rerouting after outcomes or deletion of failures occurred. Every family retains all five seeds.

Reproduce `.venv/bin/python scripts/analyze_router_v132.py`; decisions/model/development folds: `artifacts/study_v132/`; paired source: `results/v131_native/`; protocol/freeze: `reports/protocol_v132.md` and `.freeze.json`.

Post-hoc action-equivalence diagnostic: 1 raw >1%benefit cases, but 0 involved different selected configurations. 2 >1%harm cases involved different settings. Thus the raw missed-benefit counter includes same-configuration timing variability. Do not advertise it as a demonstrated missed better configuration, or reinterpret this diagnostic as a population guarantee. The original raw primary and oracle rows are preserved.

Original controller fitting/decision wall time was not recorded and is unknown, not zero. Saved coefficients/predictions can be replayed, but replay timing would be a separate measurement.
