# V68: externally defined database benchmark admission

Prospective metadata-only audit, after V67 and before fetching candidate data.
Discovery has read owner README/search metadata, not candidate performance rows.
Primary candidate: PKU-DAIR/KnobsTuningEA, because its owners publish a tuning
benchmark, measurement code, and training data for up to 197 database knobs.
Secondary harness checks: owner YCSB 0.17.0 and CMU BenchBase. These are workload
frameworks, not presumed measured configuration datasets. This is a bounded
admission audit, not a comparison of their performance or an exhaustive search.

Freeze these rules before retrieving rows. Admit measured replay only if source
version/workload/units, configuration-to-objective mapping, utility contract,
failure denominator and reuse license can be established. Require at least 400
distinct legal configurations per fixed utility contract (20/400 <= 5% coverage),
chosen to address V67's 41.7% coverage, not as a guarantee of LLM opportunity.
Separate measured training records from surrogate predictions. Never deserialize
or execute fetched pickles/models/code. Do not use published knob importance or
surrogate predictions as pre-decision information. MySQL workloads are ONE family;
PostgreSQL variants ONE family; shared harnesses do not create independent groups.
Any admitted candidate is development only until a separate exposure/split audit.

First inspect pinned owner trees, README/license, configuration domains and
measurement/parser code. Fetch data only if this establishes its schema and a
plausible admission path. A metadata projection may parse configuration fields,
row identifiers and validation/failure fields, but must neither convert nor emit
performance cells. Keep raw downloaded records private to the evidence archive.
If a prerequisite fails, report its precise source-level cause and do not acquire
objectives or run optimizers on that artifact. Preserve negative admission results.

Caps: 10 MiB total persisted response bodies, 60 s per request, 600 s per retrieval
invocation, 120 s per local audit, no retries except explicit network recovery,
zero model requests, zero application performance trials, zero paid services.
This allowance is inside the existing 573,299,440-byte remaining download cap.
No dependency installations, database startup, credentials, cloud services or
owner scripts will be executed. Write source hashes, exact executable audit
results, synthetic parser tests, decision reasons and next action. This stage
does not renew any prior inference allowance and cannot establish Q2 readiness.
