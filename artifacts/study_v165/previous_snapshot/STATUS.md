# Resume checkpoint: V164 complete

Start here, reports/research_assessment_v164.md, reports/protocol_v164.md and relevant code. Do not reread the full deep-research report. **New concrete result:** an explicit candidate catalog removed duplicate/projection events among evaluated proposals, but did not recover a robust optimization benefit and increased inference cost. This is development evidence on the two already exposed V163 applications, not a successful general router or Q2-readiness certification.

Completed40 fresh local-model starts,900 new configuration outcomes/2,700 native invocations,90 logical B20arms and270 fresh validations. Historical100 prefix outcomes/300 invocations were explicitly reused. All40responses parsed and900outcomes met correctness/quality. All1,282tests passed. Both model servers exited0; a process check found none active. No background experiment, new download, paid/cloud inference, external contact, publication or push.

## Decision and frozen design

V163 showed repeated/projected proposals and little observed ANN continuation headroom. V164 tested the representation explanation under a new finite protocol before observing new outcomes. Exact V163 application inputs/configuration domains/workers/models are reused, with no source or license change. This does not add new independent system groups.

The original numeric prompt messages are byte-identical to V163. The new catalog prompt lists all54 eligible IDs with feature values and the same ten acquired labels, asks for ten two-digit IDs, and constrains grammar to eligible IDs. Neither prompt contains hidden objectives. First seven proposals are measured; three evaluations remain for fresh incumbent validation. Duplicate IDs resolve by the same normalized feature-space nearest-unseen projection as numeric proposals. Invalid/missing completions fall back to sequential3NN and remain in the intended denominator.

This is a compound intervention: enumeration, eligible-ID grammar and output representation change together. It does not isolate encoding or grammar as the cause. Grammar enforces eligible membership but does not enforce uniqueness. No router is refitted or newly validated for the changed interface.

Ten identical saved B10prefixes, five seeds11,23,37,53,71 per application. Models: pinned SmolLM3-3B and Qwen3-8B Q4_K_M, llama.cpp b11146. New samplingseed164000+case seed, matched across interfaces; no shared-random-number/cross-device determinism guarantee. Twenty interface jobs are shuffled/interleaved in the same fixed order within each model. Models run serially, with no overlap between inference and native measurements.

Five fresh classical controls are retained: sequential3NN, adaptive neighbor, GP-EI(length1), randomfull, randomproposal. Four fresh model/interface arms are added. All90 branches clone the prefix, acquire seven new search outcomes, and freeze the incumbent before three shuffled validation blocks. Historical continuation outcomes are not used as the fresh numeric comparator. Prefix historical timing/cache drift remains a limitation common to all arms.

New accounting:350classicalsearch+280modelsearch+270validation=900outcomes. Of these450text outcomes execute five fixed distinct queries each, and450ANN outcomes execute one build/query workload each:2,700native invocations. Reused100prefix outcomes/300invocations remain separately charged in V163. All repeats and failures charge before execution.

## Results

Positive gain means catalog has lower fresh-validation utility than numeric. A practical interface win/loss requires >10%, different configurations, quality-valid outputs, MAD<=5%, and both medians>=10ms.

| Application | Model | Mean catalog gain vs numeric | Same setting / 5 | Robust wins / losses |
|---|---|---:|---:|---:|
| ripgrep | SmolLM3-3B | -1.187% | 3 | 0 / 0 |
| hnswlib | SmolLM3-3B | -0.521% | 5 | 0 / 0 |
| ripgrep | Qwen3-8B | +1.096% | 4 | 0 / 0 |
| hnswlib | Qwen3-8B | +0.577% | 5 | 0 / 0 |

Seventeen of20interface pairs selected the same configuration. No model/interface achieved a robust joint win against sequential/adaptive/GP (0/40secondary model-interface cases). One of90validation cells hadMAD>5%; none fell below10ms. All outcomes remain in descriptive means. Small signed means and same-setting differences do not establish equivalence, reliable sub-percent gains, or generalization. Repeated seeds do not create independent systems.

The mechanism improved substantially. Among140 evaluated proposals per interface, numeric needed77projections and had68duplicate proposals; catalog had0/140 for both. Amongall200 returned proposals per interface, numeric had128projections/117duplicates; catalog had2/200 for both, outside the first seven evaluated proposals. Thus do not claim every catalog output was unique or that grammar guarantees uniqueness. Both interfaces/models kept a prefix incumbent in all five ANNcases; limited observed continuation headroom remains relevant.

Catalog input tokens were2.324×numeric forSmol and2.433×forQwen. Observed request time was1.432× and1.528×, respectively. These descriptive within-batch costs are not latency guarantees or dollar/energy claims. Repairing this observed proposal problem was insufficient under the tested intervention; no claim that representation never matters or another model/workload cannot succeed.

## Evidence and checks

- Frozen protocol/config: reports/protocol_v164.md; configs/study_v164.json. Main freeze includes code, copied source dependency hashes, binary/runtime hashes, prefixes, prompts, exact model pins and original historical prefix receipts.
- Preparation and provenance: artifacts/study_v164/{jobs.json,model_jobs.json,models.json,prefix_reuse.json,freeze.json}; candidates, prefixes and prompts subdirectories. Earlier sources/licenses: reports/source_audit_v160.md and artifacts/sources/v160.
- All900 new raw acquisitions,90branch states, fixed selections,270validations and aggregates: results/v164_native. Human report: reports/apps_v164.md. Mechanism/cost data: mechanism.json; figures interface_gains.png/svg and mechanism.png/svg.
- All40 real starts/responses, rendered prompts/tokenization/capacity proofs, parser scores, limits/RSS/usage/server exits: results/v164_models/{smollm3_3b,qwen3_8b}.
- 15new adapter preflight tests passed before freezing. Full1,282tests passed,14existing dependency warnings,43.66s: artifacts/study_v164/all_tests.log. Synthetic tests are not scientific outcomes.
- Independent replay validates900new+100historical raw outcomes against independently reconstructed text/ANN correctness references, exact prefix reuse,90branches,70GPchoices(maxEIgap0),270validations,40requestprovenances, prompt field isolation, mechanism and cost aggregates. Four objective/quality/identity/hidden-prompt-field mutations rejected: replay.json/log. This is internal verification, not independent-host replication.
- Eight report/data/figure artifacts regenerate byte-identically with no new inference or native measurement: reproduction.json/log. Figures visually inspected. Only report/verifier additions occurred after collection; no frozen collector, prompt, policy or raw outcome was repaired.
- Research interpretation: reports/research_assessment_v164.md; follow-up: reports/next_experiment.md. Cost/cleanup receipts and foreground driver logs are in study_v164.

A sandbox metadata query for physical memory was denied; prior hardware evidence and the live RSS guard were retained. It did not block collection. A premature read of the not-yet-written driver receipt returned file-not-found; completed receipt now exists with error:null. No scientific result was changed because of either inspection issue.

## Costs, limits and cleanup

The closed finite protocol allowed40starts,20/model, no retries,1024outputtokens/request (40,960allocated),600s/model,8GiBserverRSS and1800s total. New900outcomes/2,700nativeinvocations; totalstage465.352s, driver465.403s. Native subprocess301.984s including231.394objective-seconds. All stages completed normally. Model server peakRSS3,768,467,456bytesSmol and8,370,880,512Qwen, below8,589,934,592bytecap; serverexits0. Both stopped before model-search native timing.

Observed34,067input and1,580outputtokens; no unknown response usage. Numeric/catalog requestseconds:Smol16.975/24.303; Qwen42.445/64.852. Whole-modelstage43.333/111.761s; startup1.757/4.068s separately recorded. No retries, fallbacks or external spending. Full research collection includes both interfaces and all controls. Estimated ten-case deployment selects oneB20branch per case:200logicaloutcomes/600nativeinvocations plus selected requests. That is not an actual deployment or a monetary estimate.

Cumulative modelstarts4,835, not one homogeneous evaluation cohort. Recorded-table acquisitioncharges41,613 plus2historical incidentalexposures unchanged. Newdownloadbytes0; retainedtotal10,328,817,415/10GiB;408,600,825bytesremain. Modelpayload9,126,358,023/9GiB unchanged. Earlier limits were not silently enlarged. Any further collection needs a new prospective finite protocol under standing authorization.

## History and safe continuation

Predecessor V163manifest SHA256:2cdc943e0440d63dd7e093a55c37b865d4cac30470e65333a4681839182ed017. RootSTATUS/README/THIRD_PARTY/next_experiment were snapshotted before edits under artifacts/study_v164/previous_snapshot. V164sealer preserves66historical checkpoints using root-file redirects. Use artifacts/study_v164/evidence_manifest.json and seal_verification.json for the latest check.

V149invalid case collision remains excluded. Earlier historical seven-ecosystem/70-case-per-model studies, V153Memcached, V159solvers and V163applications remain separate, not pooled across differing designs or practical margins. Older root documents and raw failures are preserved in the evidence chain.

Safe analysis-only commands:

    .venv/bin/pytest -q tests
    MPLCONFIGDIR=/tmp/mpl-v164 .venv/bin/python scripts/report_apps_v164.py
    MPLCONFIGDIR=/tmp/mpl-v164 .venv/bin/python scripts/mechanism_apps_v164.py
    .venv/bin/python scripts/verify_apps_v164.py
    .venv/bin/python scripts/reproduce_apps_v164.py
    .venv/bin/python scripts/seal_research_v164.py --verify-only

Collectors are create-once; do not rerun into completed directories. The saved-data replay requires retained project-local inputs/binaries for hash/reference verification. No fresh second-host collection has run.

## Single most important next action

**Independent replication on a second host.** The chat asks whether another computer is available; no answer/access is established at this checkpoint. Do not treat silence as authorization or provision cloud. Larger realistic prospective workloads, full original-method comparisons and broader model/checkpoint generalization also remain untested. Local implementation, execution, tests and replay are complete for this batch. The new mechanism result is useful for discussing a bounded negative paper, but does not certify Q2 readiness. Nothing continues outside the active session.
