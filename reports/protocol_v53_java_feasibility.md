# V53 — fresh Java/Xalan correctness feasibility

2026-09-25, frozen before application execution. Development-only adaptation,
not a numerical replication of JavaGC2015 and not a held-out router experiment.

Use official Temurin17.0.20.1+1 macOS ARM JRE (owner SHA256
190480874ccceb358cbc840393207f77ac3e63a4c5f8129d0e23e9518b96ad05), unpacked
inside the project. DaCapo9.12-MR1-bach owner release asset, SHA256 computed at
retrieval be3db084adcb2867760e1197b3ccf541c3213d918daa19386d8e236648d24be8.
GitHub did not supply a digest for this older jar; record that limitation, official
asset identity, size and metadata. Do not change system Java/settings. Runtime
GPL2 with Classpath Exception; harness and Xalan Apache2; bundled programs have
their own licenses. Owner README, configuration and Xalan source were inspected.

Exact workload: DaCapo Xalan2.7.1, default100 repetitions of17 fixed XML documents,
one application worker thread. Fixed512MiB initial/max heap, ParallelGC, adaptive
size policy disabled. Keep default pre-iteration System.gc and output validation.
Use two iterations per fresh JVM: one warmup and one reported timing. Capture both
logs, exit status, outer wall time, final harness milliseconds and validation report.
No --no-validation, --ignore-validation or --no-digest-output permitted.

Important discovered limitation: the owner's Xalan config validates completion
stdout/empty stderr, not actual transformation output. Add a stricter independent
wrapper: preserve output, require exactly xalan.out.0, nonempty bytes and SHA256
identity to the first successful reference output. Fixed single worker preserves
job order. This establishes equivalence to the released reference execution,
not a proof of XSLT standards conformance. Retain reference output and hash/size
receipts for all runs. Delete only runner-created later scratch directories after
verification to bound disk use. Full warmup payload is not independently hashed;
the final iteration payload is. No in-process harness modification.

Predeclared three executions, no retries or selecting alternatives by runtime:
reference (ParallelGCThreads1, NewRatio2, SurvivorRatio8), contrast (4,4,4), repeat
reference (1,2,8). At most3 JVM invocations,6 benchmark iterations including3
warmups; timeout60s per JVM, whole execution stage210s. On first failure, mark
remaining intended trials unattempted and retain failures. Max scratch/output2GiB
(poll runner-created scratch each second; terminate on exceedance). All processes
foreground/bounded, no service. Zero model calls, external spending or API use.
Download512MiB stage cap inside existing5GiB persistent allowance, no enlargement.

Pass requires all3 successful, owner validation passes and every final output is
identical. Timing differences are feasibility/noise diagnostics only; no selection,
gain, optimal configuration or learned-controller claim. If passed, a separate
frozen grid/classical protocol is still required before optimization. If failed,
report failure, do not silently disable checks or replace outputs. All observed
work and failures stay in cost/provenance records. Hardware noise, ancient workload,
single worker and limited JVM modes restrict external validity.
