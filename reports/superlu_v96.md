# V96: solver reliability diagnosis

**Result:** 37/40 worker acquisitions passed; 3/40 failed.
All failures were at panel size32 in the COLAMD base. Panels16,20,21 had30/30
valid workers. Panel21's successful exits do not establish memory safety.
The original V94 dataset and results are unchanged.

| Base | Panel size | Valid / intended | Failed | Unattempted |
|---|---:|---:|---:|---:|
| 0 | 16 | 5/5 | 0 | 0 |
| 0 | 20 | 5/5 | 0 | 0 |
| 0 | 21 | 5/5 | 0 | 0 |
| 0 | 32 | 5/5 | 0 | 0 |
| 1 | 16 | 5/5 | 0 | 0 |
| 1 | 20 | 5/5 | 0 | 0 |
| 1 | 21 | 5/5 | 0 | 0 |
| 1 | 32 | 2/5 | 3 | 0 |

Base0: MMD_AT_PLUS_A, pivot.1, relax4. Base1: COLAMD, pivot.01, relax1.
Both were chosen from prior failures before this diagnostic. All other settings,
matrix and RHS were held fixed; five separate processes per condition.
The 40-condition order was frozen with seed96000. Crashed processes were not retried.

The source mechanism is documented in `reports/source_audit_v96.md`:
StatInit allocates21 histogram entries using default panel20/relax10;
the factorization can index this array using a larger supplied panel size.
All40 workers independently read the same defaults from the installed native
binary. The three observed bus errors occurred inside `splu`, as recorded by
faulthandler. This supports the setting-dependent reliability concern, but does
not trace the offending native instruction or prove that every V94 failure has
the same cause. Allocator layout and added diagnostic writes can affect crashes.

The V94 configuration domain therefore includes a source-identified memory-unsafe
path. Its SuperLU timing and failure results must be interpreted as observations
of that exact wrapper/domain, not as a clean solver comparison or a general LLM
reliability estimate. A correct returned numerical solution does not exclude
memory corruption. Do not delete failed or panel32 acquisitions retrospectively:
that changes the optimizer trajectory and cannot reconstruct a safe-domain run.
HiGHS is a separate implementation and is not implicated by this finding.

## Collection and verification

New charged diagnostic configuration acquisitions:40, separate from V94's500.
Physical solves:114 starts, 111 returns; 3 started without
return, 6 planned but not started. Independently recertified
111 saved solution vectors, including any returned before a later worker
failure. Stage wall time:9.726967s. New inference requests0,
recorded-table reads0, external spendUSD0. Downloaded16,060 source bytes.

Raw evidence: `results/v96_superlu/` (intended conditions, pre-launch charges,
requests, per-solve journals, vectors, stderr, exits and lifecycle).
Derived evidence: `results/v96_analysis/summary.json`, `solution_checks.json`.
Protocol: `reports/protocol_v96.md` and immutable SHA256 freeze.

Replay with `.venv/bin/python scripts/analyze_superlu_v96.py`; this reads saved
vectors only and performs no new solver or LLM calls. The collection runner
refuses an existing output directory. For a fresh replication use a separately
declared output workspace and count every acquisition.

## Research consequence

This is useful threat-to-validity evidence, not a positive router finding or
evidence of journal acceptance. The previous negative findings remain saved,
but broad claims based on the affected SuperLU domain should be narrowed.
Next: freeze a new optimization study with a source-justified restricted
SuperLU domain and retain the original study as a sensitivity case; label the
repeat exploratory because the system is now exposed. Independently reproduce
the unaffected HiGHS result on a second machine when available. More independent
systems and useful LLM benefit variation are still needed for the original
benefit-prediction hypothesis.
