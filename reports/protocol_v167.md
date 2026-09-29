# V167: Polars null-schema repair, preserving failed admission

V166 completed all40 intended charged attempts. All20 Polars attempts failed parsing the documented `NA` plane_year marker. XGBoost completed20 native outcomes: candidates42/85/127 passed the fixed quality/timing rule, candidate0 failed the .75 accuracy constraint. V166 remains unchanged.

The only worker-code change is `null_values=['','NA']` instead of `null_values=''`. Reuse the identical data, query semantics, four configurations, five repetitions and admission rule. New20 charged Polars outcomes/60 intended query executions,600-second stage cap,60seconds/process,zero model calls/retries/downloads. Schedule seed16702. Retain all40 prior attempts;20 failed query bundles may not have completed every constituent query, so their60query charges represent intended executions, not successful completions. No optimization threshold or workload is changed based on benefit. This is a versioned implementation repair, not silent readmission.

Regression tests use separate toy CSV fixtures containing integer, empty and NA fields; they are not included in measured result aggregates. Freeze before new real-data collection. XGBoost is not rerun. No correctness/performance guarantee follows from passing the parser fixture alone; all real query outputs must also match the preexisting independent reference.
