# Resume checkpoint: V171 independent audit complete

Start with `reports/audit_v171.md`, then `reports/proposal_v172.md`. The V170 status this replaces is preserved byte for byte in `artifacts/study_v171/previous_snapshot/STATUS.md`; read it for V169–V170 collection details. Do not reread the deep-research report.

## What V171 did

A new reviewer independently audited code, protocols, raw records and provenance across the recorded-table controller cohort (V141–V155) and the native cohorts (V153, V159, V163, V168, V169–V170). The work was **post-hoc exploratory re-analysis of sealed, exposed records**:
- zero objective acquisitions, model requests, downloads and native executions;
- no paid, cloud, credential, contact, publishing or remote-push activity.

Checks run before any edit:
- The V170 seal verified: 1,558 files, 69 historical checkpoints, manifest `2eb6a885f3cf0af98c0149230c7619b6a795e1f0f6e63810c69b528617d32517`. The log is in `artifacts/study_v171/v170_seal_verification_before_edits.log`.
- The full suite passed: 1,325 tests, 14 dependency warnings.

## Main findings (details and caveats in `reports/audit_v171.md`)

1. **Always escalating loses robustly.** The equal-group mean against sequential 3NN is −4.96% and −5.24% on 70 recorded cases per model, and −9.05% and −7.50% on 30 native same-session cases (SmolLM3-3B and Qwen3-8B respectively). My independent recomputation reproduces the published V151 and V155 aggregates.
2. **No LLM-specific headroom.**
   - 0 of 140 recorded and 0 of 60 native model-cases beat sequential, random-full, adaptive neighbor and GP-EI each by >1%.
   - A random-search continuation yields as many "useful" cases as the LLM arms (recorded: 11 vs 10 and 5; native: 1 vs 1 and 1); GP-EI yields 22.
   - In Spark/Hadoop, random prototypes pushed through the LLM's own projection beat sequential while the models did not.
   - In the native cohort no arm, classical or LLM, has any robust >10% win.
3. **The router hypotheses are untested, not refuted.**
   - All 10 SmolLM positives lie in one ecosystem, leaving 0 informative leave-one-group-out folds of 7; Qwen has 2 of 7, and the native cohort 0.
   - Zero-call router outcomes (V132–V168) are correct abstention, not evidence about predictive skill.
4. **No new implementation bugs were found** in the audited paths: EZR bridge, V147/V151 fitting and threshold selection, V170 aggregates, recorded gains. The problems are inferential and design-level:
   - a non-identifiable router test;
   - a benefit target measured against sequential rather than the best cheap switch;
   - native domains without headroom;
   - transport target shift;
   - forking paths on exposed families.

## New evidence files

- `scripts/audit_v171.py` computes `results/v171_audit/audit.json` (deterministic; `--check` byte-compares).
- `tests/synthetic/test_audit_v171.py`: 8 synthetic tests, outside research aggregates.
- `reports/audit_v171.md`: the independent assessment.
- `reports/proposal_v172.md` and `configs/proposal_v172.json`: the next experiment, hash-frozen in `artifacts/study_v171/freeze.json` and **not authorized for collection**.
- `artifacts/study_v171/`: snapshots, mapping, test logs, evidence manifest and seal receipt.

## Replay

    .venv/bin/python scripts/audit_v171.py --check
    .venv/bin/pytest -q -p no:cacheprovider tests
    .venv/bin/python scripts/seal_research_v171.py --verify-only
    MPLCONFIGDIR=/tmp/mpl-v169 .venv/bin/python scripts/reproduce_ezr_v169.py
    MPLCONFIGDIR=/tmp/mpl-v170 .venv/bin/python scripts/reproduce_ezr_v170.py

`scripts/seal_research_v170.py --verify-only` will now report STATUS.md and `reports/next_experiment.md` as changed. That is expected: the V171 sealer verifies the V170 manifest through `artifacts/study_v171/previous_snapshot/mapping.json`. Collectors remain create-once; do not rerun them into completed directories.

## Counters and limits (unchanged by V171)

- Cumulative model starts: 4,855.
- Recorded-table charges: 41,613, plus two historical incidental exposures. Native counters are separate.
- Retained downloads: 10,380,159,186 of 10 GiB, leaving 357,259,054 bytes.
- Model payload: 9,126,358,023 bytes of 9 GiB.
- Disk: about 12 GiB free (98% full) on 2026-09-28.
- Hardware: Apple M3 Pro, 11 CPU cores, 18 GB unified memory.
- Second-host access has not been established.

## Single most important next action (requires an owner decision)

**Decide whether to authorize V172, the model-scale headroom test.** It uses Qwen3-14B Q4_K_M from the owner repository `Qwen/Qwen3-14B-GGUF`, about 9 GB, on the recorded 70-case cohort, with the same prompts, grammar and seeds, 70 requests and 700 recorded acquisitions. Authorizing it means:
- raising the retained-download and model-payload caps;
- freeing at least 25 GiB of disk.

The decision rule is fixed in the proposal. If you decline, the evidence does not justify more collection with the current models; write up the bounded boundary result in `reports/audit_v171.md` §4 instead.

In the audit's assessment a second host matters least:
- it cannot affect the recorded half;
- for the native half, no arm wins robustly on either conclusion.

Fresh systems matter only after some LLM arm shows LLM-specific headroom. Even then a router test needs roughly 15–100 of them, while the admissible unexposed recorded-table pool holds about two families (Opus and Z3, both classically exposed).

No work continues outside this session.
