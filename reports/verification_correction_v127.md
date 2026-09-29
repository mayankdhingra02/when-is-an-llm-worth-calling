# V127 independent replay correction

The original frozen verifier stopped on a mismatch reconstructing full-domain batch3NN. Production ranking sorts by predicted target only and preserves frozen candidate order on tied predictions. The independent verifier mistakenly sorted full `(score,rowID)` tuples, giving numeric row IDs an extra tie-break. The protocol explicitly reused the existing stable project ranking; the acquisition implementation followed it. All model/random-projection choices already matched the independent projection.

The original verifier and failure record are preserved under the precollection freeze. `scripts/verify_proposal_v127_fixed.py` changes only the independent sort to stable score-only ordering. Two synthetic regression cases cover both objective directions with all prediction scores tied and reversed candidate order. The compact replay is generated from that corrected verifier. No protocol, raw completion, selected configuration, source acquisition, outcome, metric or endpoint changed.

Use the corrected verifier for execution. All original frozen file hashes remain checked. This is a disclosed post-result verification-code defect, not a rerun or repair of measured data.
