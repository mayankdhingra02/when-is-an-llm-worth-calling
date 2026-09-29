# V69.1 serialization-only recovery

V69trial0 completed execute(), including timed reads, full validation and close,
then failed serializing live_files() metadata containing bytes. Its worker log
records the failure and supervisor walltime1.101149459s. No objective timing or
result digest survived; do not invent or impute one. Trials1/2were unattempted.
Retain the original directory and frozen source unchanged.

Permit one versioned repair: serialize bytes as explicit bytes_hex objects.
New worker/collector are separate files; all DB operations, settings, request
trace, workload, timing code, validation and schedule remain identical to V69.
Regression tests verify lossless binary metadata and rejection of other types.

Execute the same reference/contrast/reference sequence once into a new directory.
Three new attempts, maximum four total physical attempts including the failed
original; zero LLM calls. Combined600s collection cap, same120s/trial and2GiB
sampledRSS. No further retries. Failed trial's actual process time and inferred
completed-operation counts stay in the collection ledger, with missing objective
timing explicitly unknown. Never count failed receipt as a successful measurement.
