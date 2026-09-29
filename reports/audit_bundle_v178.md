# V178: guard bootstrap, environment labelling, repeat-plan correction

This responds to an independent audit of the V177 package. No objective acquisition, model request, dataset or model download, paid call or publication was made. The only network use was installing the bundle's pinned Python packages from PyPI into a throwaway test environment.

## What the audit reported

These points are as reported in the audit's text; its evidence files were not available to this project.

- **Integrity.** All 17,428 manifest-listed files matched, and the 76-checkpoint chain was intact.
- **Independent recomputation.** Its own standard-library code recomputed the headline results from the saved case-level observations. Examples:
  - loop −3.138179% ecosystem-balanced and +0.398139% case-weighted;
  - the 61/3/8 matching;
  - the selector's −2.58% / −1.29%;
  - the maximum controller gain of 0.022189 points;
  - the four rounding corrections;
  - $1.377572832 across 539 response records.

  It found no new numerical error.
- **Environment.** On Python 3.13 with newer NumPy/SciPy, 12 of 32 commands failed.
  - Four outputs differed only in 27 numeric fields, by at most 7.1e-15.
  - Several replays chose different configurations among near-ties. With left-to-right summation, the Spark, Hadoop, V172 and one native-app replay passed.
  - Two native verifiers still failed exact comparisons, but their 40 controller decisions were unchanged.
- **Two problems:**
  1. The network guard did not load on that host, because a host `sitecustomize` was imported first.
  2. The draft repeat plan said all targets would be acquired after all responses, which contradicts the iterative loop.

## Changes

1. **Guard bootstrap** (`scripts/guarded_run_v178.py`).
   - **How commands run.** Every command now runs inside a bootstrap. It installs the network guard in that process, then requires a loopback connection and a host lookup to fail with the guard's own error before the command starts, exiting with status 3 otherwise.
   - **Runner self-test.** The runner performs this self-test first and stops if it fails.
   - **Child processes.** They are not guarded. Every launch is recorded and reported.
   - **Confirmed locally.** With a shadowing `sitecustomize` placed first on the path:
     - the old V176 guard did not load, and a connection reached the network stack (`ConnectionRefusedError`), reproducing the audit's finding;
     - the bootstrap blocked the connection and still ran the analysis check.
   - **Tests.** `tests/synthetic/test_audit_bundle_v178.py` covers this. The V176 test of the old start-up route is deselected and listed, not counted.
2. **Environment labelling.**
   - **In the runner.** It records the Python version and every package that differs from its pin, and labels the run *reference* or *non-reference*. A non-reference run carries a note: exact-match checks can fail from floating-point differences and near-tie flips while the observations are unchanged. Pass/fail logic is unchanged.
   - **In the README.** It explains the distinction between numerical agreement and exact-environment reproduction.
   - **In the manuscript.** *Data Availability* now has one sentence saying the same. The V177 version is kept at `previous/main_before_environment_note.tex`; no results section changed.
3. **Repeat plan** (`reports/proposal_v178_matched_repeat.md`, revision 3; earlier drafts kept).
   - **Loop arms** acquire their own charged labels round by round as feedback, as the V173 collector did, and never see other arms' outcomes.
   - **One-shot arms** have their targets acquired after their proposals.
   - **Scoring.** No comparative scoring or result-dependent decision happens before collection ends or an operational stop.
   - **Status:** still not frozen, not authorized, not run.

## Not changed

- **Numerical tolerance.** No tolerance mode was added to the exact-match checks. They remain exact by design, and the environment label says when exactness should be expected.
- **Pinned interpreter.** Supplying Python 3.10 itself is outside the package. The README states the reference environment.
