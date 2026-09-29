> Latest checkpoint: **V129complete**. See [research assessment](reports/research_assessment_v129.md), [paired results](reports/proposals_v129.md), [post-hoc routing ceiling](reports/policy_envelope_v129.md), and [STATUS](STATUS.md). Two exposed families/all ten paired cases:−7.583%versus sequential3NN,0wins. All1,024decision masks have nonpositive gain on these pairs.13actual requests including one interrupted/recovered attempt;390experimental accesses. This is a limited negative result, not Q2readiness or validated unseen-system routing. Private replay: `python3 -I -S output/v129_replay/replay.py`.

# When Is an LLM Worth Calling?

A bounded research repository on cost- and reliability-aware escalation from a cheap software-configuration optimizer to a local LLM. The core question is whether information available after ten objective evaluations predicts that an LLM is worth using for the remaining ten.

**Latest result (V127):**the full-domain proposal experiment is complete:36real local Qwen3-8B requests and900charged recorded outcomes across90pairedB20continuations. Mean model gain was−4.918%against sequential3NN,−0.855%against matched random proposals and−0.566%against full-domain batch3NN. All five families with valid normal outputs had negative mean gains versus sequential.

**Design corrections remain explicit:** V42had already shown the old V123/V124shortlist screen was unattainable. V127escaped that shortlist, but SAC's required output exceeds its frozen512-token cap; its six failures are design-caused. Even an ideal SAC-only repair cannot make the overall primary means positive. Raw outputs, failures and old criteria are preserved. This is development evidence, not a Q2-readiness or generalizing-router claim.

Read the [current research assessment](reports/research_assessment_v127.md), [paired result](reports/proposals_v127.md), [capacity correction](reports/capacity_correction_v127.md), [prior shortlist correction](reports/attainability_v125.md), [domain audit](reports/domain_audit_v126.md) and [STATUS](STATUS.md).1,005tests pass. Independent replay checks all36new requests,900source events,90budgets and strong paired controls. Corrected reports, comparisons and the scientific figure reproduce byte-identically.

Private [V127replay ZIP](output/v127_replay.zip), [instructions](output/v127_replay/README.md): Python standard library only, no model/network/new acquisitions. The [corrected V126domain ZIP](output/v126_replay_corrected.zip) includes the full frozen dependency set, including runtime binaries for hashes; its replay never executes them. No weights are bundled. [V124corrected ZIP](output/v124_replay_corrected.zip) and [V125format ZIP](output/v125_replay.zip) retain earlier evidence. Local private verification only; source redistribution qualifications remain and no uploads occurred.

## Current evidence

| Evidence | Location |
|---|---|
| Original corrected three-system, five-seed smoke | [V3 report](reports/pilot_report_v3.md) |
| Earlier grouped routing evaluation and its limits | [V6 report](reports/pilot_report_v6.md) |
| Broader Qwen robustness comparison | [V91 report](reports/qwen_v91.md) |
| Latest completed native workload comparison | [V97 report](reports/numerical_v97.md) |
| Post-restart feasibility, including the retained failure | [V101](reports/feasibility_v101.md), [V102](reports/feasibility_v102.md) |
| V103 raw prompts, requests, responses, usage and failures | [Raw records](results/v103_reasoning/) |
| V103 charged acquisitions, metrics and figures | [Analysis](results/v103_analysis/) |
| Tests, independent replay and historical integrity chain | [Receipts](artifacts/study_v103/) |
| Prior detailed README and historical evidence map | [Preserved snapshot](artifacts/study_v103/previous_snapshot/README.md) |

The initial schema error is retained in the [erratum](reports/schema_erratum.md); affected initial runs are not silently pooled with corrected results. Earlier checkpoints and failed attempts remain preserved. Seeds are not independent software systems.

## Replay saved evidence without new inference

The current local environment uses Python 3.10.13 and [pinned dependencies](requirements.lock.txt). With the retained input/model/runtime files:

```sh
.venv/bin/python -m pytest tests -q
.venv/bin/python scripts/verify_proposal_v127_fixed.py
.venv/bin/python scripts/audit_output_capacity_v127.py --verify-only
.venv/bin/python scripts/reproduce_proposal_v127.py
.venv/bin/python -I -S output/v127_replay/replay.py
.venv/bin/python scripts/seal_proposal_v127.py --verify-only
```

Collectors and acquisition evaluators are create-once; do not rerun them into existing output directories. Use the corrected verifier: the frozen original had a disclosed tie-break error in its independent batch reconstruction. Synthetic tests/fixtures never enter model-performance aggregates. Reproduction verifies saved evidence; fresh inference on another machine and original source correctness remain unverified. Historical restoration is documented in [REPRODUCE.md](REPRODUCE.md); some source/model inputs are ignored by Git.

## Provenance and interpretation

[Primary source audit](reports/source_audit.md), [reasoning-method audit](reports/source_audit_v98.md), [current model manifest](artifacts/study_v91/model_manifest.json), and [third-party attribution](THIRD_PARTY.md) document the sources. Exact SNAP2 code was not located in the bounded source search; paper-based methods are labeled adaptations rather than numerical replications.

Model inputs contain only acquired labels and candidate features. The evaluator separately acquires outcomes and enforces each arm's budget. Shared prefixes, complete failure denominators, system grouping, actual research collection cost and modeled deployment cost remain explicit. No paid/cloud inference, publishing, remote push or author contact is authorized.

The [next experiment](reports/next_experiment.md) prioritizes demonstrating incremental value over free controls on development data before another independent-system evaluation. This repository does not guarantee positive findings or acceptance by a journal.

