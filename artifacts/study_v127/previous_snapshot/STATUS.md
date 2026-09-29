# STATUS — V124–V126 complete; feasibility correction verified

Resume here, then `reports/research_assessment_v126.md`, `reports/attainability_v125.md`, `reports/domain_audit_v126.md` and `reports/next_experiment.md`. No current collector or local model server remains active. The next step is a scientific redesign, not a missing API permission. Do not rerun create-once collectors, extend closed limits or treat a favorable format diagnostic as optimization success. Scientific honesty overrides obtaining a positive or Q2-ready claim.

## Main finding and essential correction

V42 already established that the original fixed shortlist cannot meet a5%gain over batch3NN in any of30cases. The later V123/V124joint5%quality screen therefore had no possible passing case. I should have carried the prior bound into those designs. The new audit checks that the current prefixes/pools exactly match that old evidence. This is a rediscovered design limitation, not a new scientific discovery. Old raw outputs, criteria and cost records are unchanged. See `reports/attainability_v125.md`; it acquires no new labels.

The new V126 exhaustive admitted-domain audit covers4,992rows across six exposed software families and all30original prefixes. Only4/30could gain≥5%against both batch and full-domain sequential3NN even with perfect selection over the wider admitted domain: one BerkeleyDB prefix and three Dune/HSMGP prefixes. Five could beat sequential alone by≥5%. Other families have zero such5%opportunities. Mean maximum gain versus sequential, by family: BerkeleyDB6.362%, Dune20.762%, HIPAcc1.618%, LLVM0.455%, OpenVPN0.121%, SAC1.067%. Equal-family mean5.064%is a hindsight ceiling, never an achieved model gain or deployable router result.

The admitted domains are feature-restricted and sometimes subsampled, not the entire real configuration space. All families are now exposed development data despite historical prospective-test labels in old manifests. Seeds are not independent systems. Keep the outcome map/extrema/ranks outside optimizer/model/controller inputs. Do not choose future test cases by observed optimum.

## What actually ran

- **V124:**180real local Qwen3-8B Q4_K_M requests, three stochastic predictions for each of20candidates in three exposed seed11prefixes.143valid,37malformed, zero missing responses/retries. HIPAccfailed the per-candidate validity requirement and both branches fell back to recorded batch3NN. EIprimary and mean ablation acquired10outcomes separately per branch,60new recorded accesses total, each logical armB20. Both modes reached identical final targets. Mean gain:−0.038%batch3NN,−16.264%full sequential3NN,−0.771%random-full,−0.336%first-ten,−0.174%singleportfolio. Search-space restriction must accompany interpretation of the sequential comparison. No new router fit.
- **V125:**18real formatting-probe requests on the first three HIPAcccandidate IDs with the same three sampling seeds. Demonstrated marked-JSON and owner-style-text conditions each had9/9valid versus4/9for the same original nine responses. Zero new objective acquisitions. This supports narrow format feasibility only; useful prediction, optimization and generalization remain untested for the revised format.
- **V126:**4,932charged recorded outcome accesses in497coverage-only branches,3.234s. Each clones a seed11prefix10and acquires≤10additional labels. Together with60historical prefix values they cover all4,992admitted rows. These are diagnostic branches, not497competitive optimizers or new native trials. Zero model calls. All30prefixes and102existing control states were checked against that domain; no favorable cases removed.

V124 used944.372s lifecycle,2.336s startup,6,303,105,024byte peak sampled serverRSS,2,240observed generated tokens and5,760allocated. V125 used221.516s lifecycle,2.573s startup,6,448,201,728byte peakRSS,234observed generated tokens and576allocated. Both servers exited0. No missing new output-token receipts; older unknown usage remains unknown. Source capture retrieved3pinned owner LLAMBO files totaling19,537bytes, MIT; never imported/executed the owner provider code. Source-to-method differences are in `reports/source_mapping_v124.md`. This is a local compact/batch adaptation, not a full LLAMBO or SNAP2 reproduction.

Separate research collection from deployment: the198requests include18format-probe calls; V124deployment would require60requests and10new objective evaluations per escalation, plus startup/rendering. The4,932-access retrospective coverage is never a deployableB20policy. Reused prefixes/control arms retain historical collection cost. No cloud-dollar, native-runtime or electricity break-even claim. Source fetch, testing, analysis and agent time are separate from model lifecycle measurements.

## Frozen limits and verification

V124closed:180requests/5,760allocated tokens/1,500s/8GiBserverRSS/60new objective accesses. Freeze255inputs,SHA256a33ef07549a1e8ce088c52df2d9c0f8f844a0032ef3518346675c31d7a3e7efd.

V125closed:18requests/576allocated tokens/500s/8GiB/zero new objectives. Freeze289inputs,SHA256cbe3872490873acc0846207a2f10e9a22e3dd50442eee721565f721279e49503.

V126closed:4,932recorded accesses/180s/zero requests/downloads/spend. Freeze418inputs,SHA256597ca87660b1b01f546597bb4d5889f01d1910c2f4115f72ea49e1ae877711e6. Objective directions were checked before freeze: OpenVPNthroughput maximized, other five targets minimized. No frozen acquisition/evaluation code was changed after collection.

Final full suite: **980passed**,14dependency deprecation warnings,29.66s. Synthetic tests are excluded from research aggregates. Saved-evidence replay validates198new model requests,60optimization events,4,932coverage events,497coverage budgets and102control states. All30V42pool ceilings exactly match. Corrected V124 and V126 reports/comparisonJSONs/PNGs reproduce byte-identically; both figures visually inspected.

V126's original frozen verifier stopped on a wrong ordered-list equality between shuffled presentation mapping and V42shortlist acquisition order. A separate corrected verifier checks membership and cardinality, retaining each target's original candidate identity. All30sets and bound values already matched. The frozen original, failure log and correction report remain. Two deliberate copied-data pool/target corruptions were rejected. Use the corrected verifier below; do not rerun the superseded one and misreport its known failure as a changed result.

## Evidence and commands

- Reports/protocols: `reports/surrogate_v124.md`, `format_probe_v125.md`, `attainability_v125.md`, `domain_audit_v126.md`, `research_assessment_v126.md`, `verification_correction_v126.md`, `protocol_v124/125/126.md` and corresponding freezeJSONs.
- Real raw prompts/requests/responses/backend settings/tokens/runtime: `results/v124_surrogate/`, `results/v125_format/`; templates/preflights and input freezes under `artifacts/study_v124/` and `study_v125/`.
- Sealed choices/paired arms/source journals: `results/v124_analysis/`; format comparisons `results/v125_analysis/`; old-bound rebind `results/v125_design_audit/`.
- New coverage plan `artifacts/study_v126/plans.json`; raw journal,497states,collection receipt,30case bounds and scientificPNG: `results/v126_domain_audit/`.
- Verification, correction, tests, reproduction and packaging receipts: `artifacts/study_v124/`, `study_v125/`, `study_v126/`.

Executed create-once collectors/evaluators; do not repeat:

```sh
.venv/bin/python scripts/collect_surrogate_v124.py
.venv/bin/python scripts/analyze_surrogate_v124.py
.venv/bin/python scripts/collect_format_v125.py
.venv/bin/python scripts/analyze_format_v125.py
.venv/bin/python scripts/domain_audit_v126.py --prepare
.venv/bin/python scripts/freeze_domain_v126.py
.venv/bin/python scripts/domain_audit_v126.py
```

Safe saved-evidence replay:

```sh
.venv/bin/python scripts/verify_surrogate_v124.py
.venv/bin/python scripts/audit_attainability_v125.py
.venv/bin/python -I -S scripts/verify_domain_v126_fixed.py
.venv/bin/python scripts/reproduce_reports_v126.py
.venv/bin/python -I output/v124_replay_corrected/replay.py
.venv/bin/python -I output/v125_replay/replay.py
.venv/bin/python -I -S output/v126_replay/replay.py
.venv/bin/python -m pytest tests -q
.venv/bin/python scripts/seal_research_v126.py --verify-only
```

Private executed bundles: `output/v124_replay_corrected.zip`891,600bytes/483hashedfiles; `output/v125_replay.zip`159,456bytes/68files; `output/v126_replay.zip`24,619,244bytes/928files. The V126bundle includes its full frozen input file set; corrected V124/V125are compact evidence subsets. No weights/runtime binaries or installation required. Source redistribution qualifications remain; no upload occurred. The original V124ZIP and original pre-correction report/reproduction receipts are retained, but use the corrected bundle/report for interpretation. Saved replay is not fresh model inference on another machine.

## Most important next action and remaining research gap

**Freeze and test a full-domain proposal intervention with matched cheap controls before fitting another router.** The existing user authorization covers bounded local work; no new paid endpoint or model download is needed merely to develop that adapter. Its feature-only projection must escape the old shortlist without using this audit's hidden-label map. Keep all six development families; do not cherry-pick the four feasible cases. V43already tested uniform/diverse pools and V44ran the1.5Bmodel on them; those are not untested alternatives. Details and stopping conditions: `reports/next_experiment.md`.

No current result establishes a useful unseen-system benefit-aware controller or Q2readiness. Future full-domain model effectiveness, untouched family evaluation, calibrated pre-call cost/reliability routing, original measurement correctness/equal-utility, independent-host inference and native-noise portability remain unresolved. Original V113second-host requirement, V111NGINXfailure and stronger V52admission restrictions are unchanged. No new external machine was provisioned. No work is promised outside the active session.

Prior genuine gains and negative findings remain visible: V91exceptions; V120WordCount/V121MongoDBapparent gains matched free first-ten; V122projection failed; V123pointwise ties; V43/V44expanded-pool failures. Changing interpretation of the impossible screen does not erase real model failures or prove a better unrestricted method exists.

## Cumulative ledger and immutable evidence chain

Real model requests **4,426**; recorded-table acquisitions **34,280**. This session added198requests and4,992recorded accesses (60optimization+4,932diagnosticcoverage). Native counts unchanged: numerical880; NGINX81charged attempts/35,853,130byte-valid responses; DuckDB78; H2299; Kanzi1,265; RocksDB350. These units are not interchangeable.

Instrumented artifact-download bodies9,881,186,771/10GiB; remaining856,231,469bytes. Model payload unchanged9,126,358,023/9GiB. Web-provider metadata/code transfer sizes remain unknown rather than zero. No paid/cloud inference, new model/dependency install, credentials, system settings, publication, remote push or external message.

Combined V124–V126seal: `artifacts/study_v126/evidence_manifest.json`, with final receipt `seal_verification.json`. It anchors V123manifest SHA25632c743e514350905691277dfbc173abce95b9949b2cd3e2b131ad476d4f0f09b and verifies50historical checkpoints. Original mutable root documents are preserved in `artifacts/study_v124/previous_snapshot/`; older protocols/raw outputs/manifests were not rewritten. Consult the final seal receipt for exact current file count/hash. Do not edit covered files after sealing without creating a new checkpoint and preserving the previous versions.
