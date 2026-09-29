# V161–V162: native application feasibility

Both stages remain in the evidence. V161 failed; V162 was frozen before a repaired workload/domain ran. No model outputs were used to select either design. Configuration outcomes and underlying native invocations are distinct counters.

| Stage | Application / setting | Valid quality / 5 | Minimum observed quality | Median raw seconds | Relative MAD of valid timings | Admitted cell |
|---|---|---:|---:|---:|---:|---|
| 161 | ripgrep / 0 | 5/5 | 100.000% | 0.165708 | 4.231% | pass |
| 161 | ripgrep / 21 | 5/5 | 100.000% | 0.126218 | 5.582% | fail |
| 161 | ripgrep / 42 | 5/5 | 100.000% | 0.059532 | 2.161% | pass |
| 161 | ripgrep / 63 | 5/5 | 100.000% | 0.075641 | 5.413% | fail |
| 161 | hnswlib / 0 | 0/5 | 89.416% | 0.056515 | undefined (no quality-feasible results) | fail |
| 161 | hnswlib / 21 | 5/5 | 99.894% | 0.056037 | 0.580% | pass |
| 161 | hnswlib / 42 | 5/5 | 99.800% | 0.107704 | 1.126% | pass |
| 161 | hnswlib / 63 | 5/5 | 100.000% | 0.104621 | 0.444% | pass |
| 162 | ripgrep / 0 | 5/5 | 100.000% | 0.721872 | 0.564% | pass |
| 162 | ripgrep / 21 | 5/5 | 100.000% | 0.530493 | 1.475% | pass |
| 162 | ripgrep / 42 | 5/5 | 100.000% | 0.309926 | 1.031% | pass |
| 162 | ripgrep / 63 | 5/5 | 100.000% | 0.361608 | 1.003% | pass |
| 162 | hnswlib / 0 | 5/5 | 98.169% | 0.098380 | 0.547% | pass |
| 162 | hnswlib / 21 | 5/5 | 99.978% | 0.097961 | 1.291% | pass |
| 162 | hnswlib / 42 | 5/5 | 99.872% | 0.188255 | 0.467% | pass |
| 162 | hnswlib / 63 | 5/5 | 100.000% | 0.185371 | 0.981% | pass |

V161 ripgrep failed the fixed 5% MAD gate in two cells. Its hnswlib smallest graph/search cell returned valid neighbor IDs but only89.416% recall, below95%. These five infeasible outcomes used the declared20s utility penalty; their measured raw execution time is still retained. No missing value or penalty is represented as a successful constrained runtime.

V162 uses five distinct fixed code-analytics queries, one aggregate timer per setting and five separately counted native invocations. It does not measure individual query timings or repeat the same query to acquire uncharged reliability labels. Hnswlib increases minimum M/construction ef, with the same recall and timing thresholds. All40outcomes passed; two implementations are admitted. This is feasibility-based design exposure, not untouched production evidence.

Independent checks reconstructed search counts and ANN distances using a separate norm/dot formula. All80configuration outcomes and160native workload invocations are accounted for. Collection caps600s/stage and full intended denominators are preserved. No model request, retry or native warmup occurred. The initial reference timing is unknown because its receipt failed after a linker error; V162 reference preparation has its own receipt.

Raw artifacts: results/v161_apps and results/v162_apps; plans/code hashes: artifacts/study_v161 and study_v162. Safe report replay: .venv/bin/python scripts/report_apps_feasibility_v163.py.
