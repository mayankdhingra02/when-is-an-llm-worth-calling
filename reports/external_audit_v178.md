# External audit of the V178 package: outcome (recorded, not reproduced here)

This records what an independent reviewer reported after auditing `output/llm_escalation_audit_v178.zip`. The reviewer's evidence files stayed in its own environment and are not in this project, so the points below are as reported. No file in the package or manuscript was changed as a result.

## Reported results

- **Guard.** It blocked direct connections, `connect_ex` and host lookups, including with an unrelated `sitecustomize` already loaded. A deliberately failed guard install made the launcher exit with status 3 without running the target. The limit is as documented: child processes are logged but not guarded, so this is an in-process guard, not an operating-system sandbox.
- **Unchanged results:**
  - 17,422 files common to V177 and V178 were byte-identical; only `STATUS.md` and `main.tex` changed, the latter only in *Data Availability*.
  - The reviewer's own independent recalculation on V178 matched its V177 output exactly.
  - All 17,451 manifest files were verified, and the 77-checkpoint chain was intact.
  - The table checker found 0 mismatches over 80 rows and 12 statements.
  - The bundled tests gave 150 passed and 2 deliberately deselected.
- **Environment.** The reviewer could not obtain Python 3.10, so ran on 3.13.5, which the runner labelled NON-REFERENCE.
  - 19 commands passed, 13 failed and 1 was skipped; the runner correctly returned failure.
  - Causes: 27 numeric fields differed by at most 7.1e-15; near-tie replay differences; and two plotting scripts whose host-modified plotting hooks tried a localhost request, which the guard blocked.
  - The clean Python 3.10 run reported by this project was therefore not independently confirmed.
- **Repeat plan.** Revision 3 correctly separates within-arm feedback from cross-arm analysis. There are no further requests; the plan remains an unapproved draft.
- **Manuscript.** The bundled V178 source compiles to 23 pages without overfull boxes.

## Reviewer's recommendation

Stop the manuscript revision loop at V178. Keep the exact reference-environment checks strict. A tolerance-based diagnostic mode is optional, and must never count a changed selection or controller action as an exact replay. Treat the matched repeat as a separate experimental decision.

## Decision here

The revision loop stops at V178, and no tolerance mode is added. The reference-environment reproduction remains confirmed only by this project's own clean-environment run (`artifacts/study_v178/bundle_reproduction_*`).
