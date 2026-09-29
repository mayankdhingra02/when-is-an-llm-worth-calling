# STATUS — V129 complete: two-family extension and explicit monitor recovery

Resume here, then `reports/research_assessment_v129.md`, `reports/proposals_v129.md`, `reports/policy_envelope_v129.md` and `reports/next_experiment.md`. Both model processes and all collectors have exited. V128/V129collection allowances are closed; do not restart create-once collectors or silently extend them. There is a concrete negative result, not demonstrated useful unseen-system routing or a Q2-readiness claim. No paid endpoint, external permission or background job is pending.

## Latest concrete result

Full-domain Qwen3-8B proposals executed on both subsequently source-linked recorded-label families, Storm and MongoDB, with all five original seeds11,23,37,53,71. These are exposed families, not fresh holdouts; historical split labels do not apply to this new stage. Ten normal cases and two label-rotation probes returned valid. Every optimization arm shares its original prefix10and ends atB20.

| Comparator | Equal-family mean model gain | Wins/ties/losses |
|---|---:|---:|
| Full-domain sequential3NN |−7.583%|0/3/7|
| Matched random feature proposals + same projection |−4.269%|0/7/3|
| Full-domain batch3NN |−6.039%|1/3/6|
| Original shortlist batch3NN |−7.408%|1/3/6|
| Random full-domain search |−4.847%|0/6/4|
| Single classical portfolio |−7.404%|0/3/7|
| Presentation-first10 |−13.067%|0/3/7|

MongoDB's mean versus sequential3NN is−2.399%; Storm's−12.766%. Among100decoded normal proposals,34needed nonzero-distance projection,16repeated another proposal and8matched acquired settings. Both rotation probes changed selected sets (overlap2/10and1/10). Label responsiveness is not useful optimization.

A **post-hoc, evaluator-only routing envelope** enumerated all1,024binary decision masks from these ten actual paired outcomes. None improves quality over never-escalate; eight tie, including never-escalate. The seven nonempty tied masks make extra model calls. Hindsight oracle gain is0%. Never dominates all nonempty masks in quality and call count on these observed cases. Random mixtures cannot create a positive expectation from these nonpositive gains. This is not a population guarantee, risk bound or trained-router result. No extra request or objective acquisition was needed. Do not silently pool V127'sdifferent-output-contract results or erase its positive exception.

## Structural reliability and the interrupted first attempt

Implemented mandatory pre-call output construction and input-context checks using the pinned model vocabulary. Strict ten-string grammar has no whitespace loop; conservative ASCII singleton construction bounds, including EOS, are82tokens for Storm and202for MongoDB. Both fit the declared1024cap; exact rendered input plus1024fits4096context. The provider binds preflight authorization to the exact payload and refuses changed/unpreflighted requests before charging/sending. Synthetic tests reject V127's59-feature SACrepresentation at512tokens. This is a feasibility guard, not guaranteed validity/quality.

V128originally charged two requests. MongoDB seed11returned valid; seed23was interrupted when the watchdog's external `ps` command exceeded its2-second timeout. The watchdog killed its owned server (exit−9). Ten jobs were unattempted. Original30paired arms still executed with nine declared normal fallbacks and300charged accesses; this partial-policy result is labeled as such. It does not establish model quality on either family.

V129was separately frozen **before** those300outcome acquisitions. It reads process-group RSS via installed macOS libproc APIs, sums the group, and rejects missing/truncated/partial readings; seven monitor tests passed. SDK headers and ABI hashes are retained. Its prospectively declared transport timeout is180seconds rather than120. It reused exactly the one valid original response and made11real calls: one explicit repeat of the interrupted request and ten previously unattempted jobs. Prompts, model, sampling seeds, grammar and all scientific choices stayed unchanged. Recovery completed with serverexit0 and no resource stop. Do not claim the monitor caused the observed speedup; there was no controlled performance comparison.

Recovery reused20cheap arms and one exact-input valid model arm only after prefix/selection/source-hash checks, then acquired90new outcomes for the other nine model arms. No output was fabricated and no interrupted attempt removed. Raw stage receipts and a provenance-linked merged view remain separate.

## Costs and limits

Across V128/V129: **13charged real requests,12returns,one explicit recovery repeat**, zero automatic retries. Returned receipts account for1,471generated and7,281prefill tokens; interrupted usage is unknown. Its server log additionally shows≥512prompt tokens processed, so the combined observable prefill lower bound is7,793, not an exact total.13,312output tokens allocated. Combined model lifecycle315.167s, startup10.758s; peak sampled RSS6,618,546,176bytes. Actual experimental recorded accesses390(300original+90recovery); historical prefix/control costs remain historical.

V128limits:12requests/12,288allocated tokens/900s/8GiB/120s transport;300accesses/180s. It stopped after2attempts and156.729s due the monitor error, not a silently raised limit. Freeze: `reports/protocol_v128.freeze.json`, SHA25696c677b52a27554aed3d3814cc18589a48e23b08212253e95245ee528ac6e4ef,1,304inputs.

V129recovery limits:11requests/11,264allocated tokens/1,200s/8GiB/180s transport;90new accesses/180s. Actual model lifecycle158.438s. Freeze: `reports/protocol_v129.freeze.json`, SHA256b8b2641e4ca848b545fe39c7c283d4ac77f994a95bd2a50bbc5497aabce5c3c0,1,345inputs. Both stages prohibit paid/cloud inference/downloads/spending. Existing owner Qwen3-8B Q4_K_M and llama.cppb11146identities remain hash-checked.

An incidental source-inspection command displayed two ExaStencils rows including objectives, outside any experimental arm. They were not used for design/selection or scored. Record two additional outcome-vector exposures separately; that family remains unadmitted and must not be certified untouched. Receipt: `artifacts/study_v128/incidental_exposure.json`. Do not hide this access in the experimental budgets.

Estimated ordinary deployment uses one model request plus ten new objective evaluations per escalation;1024is reserved output capacity, not expected usage. The rotation probes, paired controls, interrupted call and recovery are actual collection overhead. No native latency, energy or dollar savings are inferred.

## Verification and evidence

**Final full suite:1,024passed,14dependency warnings,30.75s.** Earlier full tests had one2-second launch timeout in the old native V107parser; unchanged focused tests and subsequent full runs passed. Both failed and passing logs are retained. All synthetic fixtures remain excluded from measured aggregates.

Independent replay validates13charged attempts,12actual returns, exact prompts/settings, cache links, strict parsing, independently reconstructed projection and stable3NNties, source cells, all390actual acquisition events across both stages and30recovered paired arms. The original V129verifier failed due a template-substitution arithmetic typo13288instead of13×1024=13312. The separate fixed verifier changes only that comparison constant; no collection limit, outcome or selection changed. Original frozen code/failure remain. Use the fixed verifier.

Nine reports/data/figures reproduce byte-identically. Both scientific figures were visually inspected. Private standard-library replay runs both interrupted and recovered analyses and independently recomputes the1,024mask envelope. ZIPCRCchecks pass; a deliberately corrupted copied comparison file is rejected. This is saved-evidence portability, not new inference on another host.

- Latest assessment: `reports/research_assessment_v129.md`.
- Main result and post-hoc diagnostic: `reports/proposals_v129.md`, `reports/policy_envelope_v129.md`.
- Original interrupted analysis: `reports/proposals_v128.md` with explicit notice.
- Original/recovery raw model evidence: `results/v128_proposals/`, `results/v129_proposals/`.
- Provenance-linked response view: `results/v129_merged/`.
- Choices, journals, arms, comparisons and figures: `results/v128_analysis/`, `results/v129_analysis/`.
- Freeze/test/verification/cost receipts: `artifacts/study_v128/`, `artifacts/study_v129/`.
- Private standalone bundle: `output/v129_replay.zip`,924,622bytes,296hashed files; interrupted-only bundle `output/v128_replay.zip`,526,178bytes,175files. No runtime binaries or model weights. Local review only; no public redistribution grant.

Safe replay commands (no new inference/acquisitions):

```sh
.venv/bin/python scripts/verify_proposal_v128_interrupted.py
.venv/bin/python scripts/verify_proposal_v129_fixed.py
.venv/bin/python scripts/reproduce_proposals_v129.py
.venv/bin/python scripts/cost_detail_v129.py
.venv/bin/python -I -S output/v129_replay/replay.py
.venv/bin/python scripts/seal_proposal_v129.py --verify-only
```

Do not use the original frozen V129verifier or the unqualified original V128report generator. Use `report_original_v129.py` to preserve its interruption notice. Do not rerun create-once preparation/collection/acquisition/merge/package scripts. Some large dependencies/raw sources are Git-ignored; full-project replay requires this local workspace. The compact bundle verifies its saved-evidence subset without dependencies/network/model.

## Most important next action and remaining limits

**Admit and prospectively collect a genuinely new, correctness-validated benchmark cohort before another learned-router fit.** Source/workload admission, not favorable-outcome screening, comes first. FLAC is an owner-documented unexecuted lead requiring pinned build/license, a fixed licensed PCM corpus and exact decode validation. No FLAC download/build/trial occurred. A single extra family will not establish generalization; variants/workloads/seeds must stay grouped. See `reports/next_experiment.md`.

The original useful benefit-prediction hypotheses, independent held-out groups, native correctness/equal-utility/noise, cross-host inference and a distinct contribution versus close source methods remain unestablished. Additional runtime on these exposed families cannot certify Q2readiness. Existing local authorization is enough for admission work; no external permission is currently missing. Nothing continues outside the active session.

## Cumulative ledger and preservation

Real model requests: **4,475** (4,462+13). Experimental recorded-table acquisitions: **35,570** (35,180+390), plus **2incidental ExaStencils exposures**, totaling35,572recorded outcome-vector exposures with categories retained. Native optimization counters unchanged: numerical880; NGINX81attempts/35,853,130byte-valid responses; DuckDB78;H2299;Kanzi1,265;RocksDB350. Synthetic monitor tests are not native optimization measurements.

Instrumented saved downloads remain9,881,186,771/10GiB; remaining856,231,469bytes. Model payload9,126,358,023/9GiBunchanged. Newly read web-provider metadata transfer sizes remain unknown, not zero. No new installation, paid/cloud inference, credential access, system-setting change, publication, remote push or message.

Combined V128/V129seal: `artifacts/study_v129/evidence_manifest.json`; final receipt `seal_verification.json`. It anchors V127manifest SHA256e305fe4bc337cba86428f2cff926cb1b0f178c96217dfb499f4d967137639405 and preserves52historical checkpoints. Prior mutable root documents are in `artifacts/study_v128/previous_snapshot/` with mapping.json. All older protocols/raw evidence remain unchanged; prior detailed V127status is in that snapshot. Preserve this checkpoint before future mutable-document edits.
