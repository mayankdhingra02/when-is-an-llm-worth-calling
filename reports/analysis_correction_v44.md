# V44 analysis correction: isolate mutable prefix state

The original, frozen analyzer stopped with `Paired state/budget mismatch` after
real collection completed. All60requests and600acquired outcomes remain intact.
No primary summary was produced. Failure log and partial cost output are in
`artifacts/study_v44/analysis_attempt1/`; failed analysis time remains charged
in the cumulative runtime ledger.

Diagnosis: `State(**old['state'])` shares mutable list objects with the in-memory
saved-prefix dictionary. Replaying the first pool changed that dictionary from
ten to twenty observations. The second pool then inherited the mutated prefix
and failed the paired-state check. The on-disk prefix remained ten observations.
The same alias would also have contaminated first-pool prefix-only statistics
had the analyzer completed. No numerical summary from that attempt is used.

Correction: preserve `scripts/analyze_pool_models_v44.py` unchanged; execute
`scripts/analyze_pool_models_v44_fixed.py` with `fresh_state(record)`, which
deep-clones the state before replay. A synthetic two-arm regression test verifies
that independent replay leaves the original prefix unchanged in both directions.
The fixed script additionally verifies this correction seal; original scientific
protocol, pre-response analysis definitions, model outputs, prompts, case list,
comparators, scoring and all source artifacts are unchanged.

This correction is recorded after responses existed and after the failed
postprocessor ran, before any complete quality summary. It is a computation
bug fix, not a new experiment or a hidden protocol change. All results remain
exploratory. An independent stdlib verifier will check source targets and
arithmetic directly without importing this postprocessor.
