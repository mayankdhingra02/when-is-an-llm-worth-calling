# V41 policy-transfer precommit: actual prefix evidence

The unchanged V6 benefit router selects **1 of30cases per model**, OpenVPN seed11. The uncertainty router selects **0 of30**. Exact matched-random masks are saved before any new model output; they select1 and0cases respectively. Development-rate random policies select0 because both development rates were zero. Never/always remain0/30. These counts are actual decisions from acquired ten-label prefixes, not model performance results.

**29 of30cases have at least one feature outside its development range.** Feature counts account for25 cases, plateau14, progress9, separation5 and uncertainty1; counts overlap. The sole escalated case has prefix progress0.607, compared with a development maximum0.037. Its score0.076647 is in the old normalized-loss-difference scale, not a calibrated7.66% improvement or probability. Range diagnostics do not alter the frozen masks, and being outside a marginal range does not itself establish failure.

This changes the interpretation of the planned study: it is a demanding controller transfer test, and an isolated success would still provide little evidence of reliable routing across systems. No post-decision labels, threshold refitting or new LLM responses were used to choose these masks. The feature/threshold/model shift must remain visible even if a later result is favorable.

## Executed work and safeguards

- `scripts/seal_policies_v41.py` executed and saved all30 cases, coefficients' source binding, masks, scores and range diagnostics in `results/v41_policy_precommit/decisions.json`.
- `results/v41_policy_precommit/analysis_seal.json` binds code/tests/decisions to the unchanged original protocol. Implementation followed classical inspection and precedes new-model inference; no claim otherwise.
-300tests passed, including15 new synthetic tests for no-outcome policy inputs, strict thresholds, exact random matching, family weighting, family-level permutation denominators, missing token usage, error inclusion and cost-aware diagnostic oracles. Synthetic fixtures never enter measured directories.
- Independent standard-library source audit ran under Python3.10 and3.12 with identical results:2,400 acquisition events,240 blocks,1,225 distinct acquired source rows. It imports no optimizer code and parses no unacquired numeric target. Receipt: `artifacts/study_v41/independent_source_audit.json`.
- `scripts/analyze_models_v41.py` is implemented for both models, all seven controls, transferred policies and hypothetical call penalties. It rejects absent/incomplete intended results rather than reporting a complete-case mean. Its no-data guard was executed and failed as expected before creating model-analysis results. This is not a real-model run.
- Full future analysis must also run `scripts/verify_source_events_v41.py --kind model` to independently match acquired targets against the pinned source tables. This check remains unexecuted because no V41 model journal exists.

This turn added zero model requests, new objective acquisitions or downloads. Precommit computation charged0.016608s; independent source checks charged1.899435s. Cumulative experiment runtime is2562.330002/3600s, with1037.669998s remaining. Requests remain230/230. The exact60-call extension is still not granted.

## Reproduction

```sh
.venv/bin/python -m pytest -q tests/synthetic tests/test_transfer_v41.py
.venv/bin/python -I -S scripts/verify_source_events_v41.py
```

Do not rerun the one-shot policy-sealing script into the existing directory. Future model analysis needs actual collection, full provenance, all intended cases and the unchanged precommit seal. Until then the central new LLM benefit and deployment reliability remain untested. Nothing here establishes Q2 readiness or guarantees a positive finding.
