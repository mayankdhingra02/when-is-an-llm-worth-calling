# V167 Polars schema repair feasibility

Twenty intended Polars native outcomes after correcting the NA null marker; V166 failures remain charged, no LLM calls. Admission is based on the frozen correctness/quality and timing rule, not model benefit.

| Application | Candidate | Quality-valid / 5 | Median seconds | Relative MAD | Eligible |
|---|---:|---:|---:|---:|---|
| polars | 0 | 5 | 0.24432658300793264 | 0.006646497418178465 | True |
| polars | 21 | 5 | 0.058001166995381936 | 0.0008462418254561159 | True |
| polars | 42 | 5 | 0.044758082993212156 | 0.002834705749393206 | True |
| polars | 63 | 5 | 0.022103625000454485 | 0.03000263516323884 | True |

Admission: {"polars": {"admitted": true, "eligible_cells": 4, "required_eligible": 2, "all_native_valid": true}}

Actual charges: 20 configuration outcomes; 60 query/training executions; 4.341 seconds collector wall time. No model requests or retries.

Polars reuses a previously exposed flight workload and adds CSV scan/parsing to the timed objective. XGBoost validation accuracy is an optimization constraint; it is not an untouched test result. Both tasks are now exposed development applications. Five repeats estimate local noise, not five independent systems. Failed admissions and quality-failing settings remain in the denominator. No generalized router or journal-readiness conclusion follows from admission.
