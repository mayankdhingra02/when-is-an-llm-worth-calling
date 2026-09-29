# V13.1: correction to the metadata-only exposure audit

V13's first metadata pass omitted x264 from its exposure list because V3 calls its test split `heldout_smoke`. V13.1 recognizes that historical label and fails closed for unknown spellings. All nine exposed families must be present. This defect did not change the zero-new-size-family result and no collection was admitted. V13 outputs/source/freeze remain preserved as a superseded first pass.

All other scope, checks and non-acquisition constraints in protocol_v13_admission.md apply. Current entry point is scripts/audit_admission_v13_1.py. It uses the corrected exposure function plus the unchanged metadata audit/split guard. The new frozen source includes the original module and the correction. Outputs are results/v13_1_admission and artifacts/study_v13_1. No numerical objective data is read or new experiment run.
