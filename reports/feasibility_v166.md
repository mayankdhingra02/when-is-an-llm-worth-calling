# V166 additional-application feasibility

Forty intended native outcomes, no LLM calls. Admission is based on the frozen correctness/quality and timing rule, not model benefit.

| Application | Candidate | Quality-valid / 5 | Median seconds | Relative MAD | Eligible |
|---|---:|---:|---:|---:|---|
| polars | 0 | 0 | None | None | False |
| polars | 21 | 0 | None | None | False |
| polars | 42 | 0 | None | None | False |
| polars | 63 | 0 | None | None | False |
| xgboost | 0 | 0 | 0.3614710840047337 | 0.011233612300128466 | False |
| xgboost | 42 | 5 | 0.2875301669992041 | 0.018490087693000937 | True |
| xgboost | 85 | 5 | 0.5012411250063451 | 0.012532890237253522 | True |
| xgboost | 127 | 5 | 0.778213333003805 | 0.005406774502107541 | True |

Admission: {"polars": {"admitted": false, "eligible_cells": 0, "required_eligible": 2, "all_native_valid": false}, "xgboost": {"admitted": true, "eligible_cells": 3, "required_eligible": 2, "all_native_valid": true}}

Actual charges: 40 configuration outcomes; 80 query/training executions; 26.078 seconds collector wall time. No model requests or retries.

Polars reuses a previously exposed flight workload and adds CSV scan/parsing to the timed objective. XGBoost validation accuracy is an optimization constraint; it is not an untouched test result. Both tasks are now exposed development applications. Five repeats estimate local noise, not five independent systems. Failed admissions and quality-failing settings remain in the denominator. No generalized router or journal-readiness conclusion follows from admission.
