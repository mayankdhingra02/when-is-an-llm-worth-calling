# V126 verification correction

The frozen verifier stopped on a mistaken order equality check after collection and analysis. V42 stores candidate IDs in shortlist acquisition order; the saved prefix maps displayed IDs to candidates in shuffled presentation order. A bound over the whole pool depends on membership, not presentation order. All 30 pool sets and exact ceiling values match.

The original `scripts/verify_domain_v126.py` remains unchanged under its precollection freeze and its failure is recorded in `artifacts/study_v126/verification_original_failure.log`. Use `scripts/verify_domain_v126_fixed.py`: the only calculation change replaces ordered-list equality with set equality and verifies both lists have length20. The subsequent per-candidate check still pairs each V42 target with its original candidate ID and compares with the acquired source value. Original source-cell, coverage, direction, budget, control and aggregate checks remain intact.

No protocol endpoint, pool, source value, acquisition, model response, selection or analysis result changed. No extra objective acquisition or inference occurred during repair. This is a verification implementation defect, disclosed after results; it does not change the bounds. A temporary corrupted pool is rejected by replay before bound calculation. The original protocol was not refrozen after outcomes.
