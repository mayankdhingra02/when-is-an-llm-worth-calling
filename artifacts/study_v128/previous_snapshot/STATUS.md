# STATUS — V127 full-domain proposal experiment complete

Resume here, then `reports/research_assessment_v127.md`, `reports/proposals_v127.md`, `reports/capacity_correction_v127.md` and `reports/next_experiment.md`. All collectors/evaluators have exited; the local model server exited0. V124–V127are complete at their declared limits. Do not restart create-once collectors or enlarge a closed cap. The research has a reproducible negative development result, not demonstrated useful unseen-system routing or a Q2-readiness claim. No paid/cloud access or external permission is currently missing.

## Latest concrete result

Implemented and executed a new intervention that escapes the old shortlist: Qwen3-8B proposes ten feature-setting strings from the prefix's ten acquired measurements and admitted feature domains. A fixed feature-only Hamming projection maps each to a valid unobserved row, excluding already acquired/projected rows and breaking ties by frozen candidate order. Model prompts contain no candidate IDs, hidden outcomes or V126hindsight extrema. All six exposed families and all five seeds were retained.

**36real local requests;900new recorded accesses across90pairedB20arms.** Thirty normal requests plus six label-rotation probes; each normal case has model, matched random-feature-proposal and full-domain batch3NN continuations. Each arm clones prefix10and acquires10labels independently. Historical full-domain sequential3NN and other controls keep their original costs.

| Comparator | Cases | Equal-family mean model gain | Wins/ties/losses |
|---|---:|---:|---:|
| Full-domain sequential3NN |30|−4.918%|1/17/12|
| Matched random proposals + identical projection |30|−0.855%|5/21/4|
| Full-domain batch3NN |30|−0.566%|2/18/10|
| Original-pool batch3NN |30|−2.889%|2/16/12|
| Random full domain |30|−0.910%|6/18/6|
| Free first-ten |30|+0.374%|8/18/4|
| Single classical portfolio |12|−6.034%|2/4/6|

The favorable first-ten mean does not survive the stronger controls. Every one of the five families with valid normal outputs has a negative family mean against sequential3NN. Model-arm selections outside the old shortlist:261/300, including declared fallbacks. Among250decoded normal proposals,167had nonzero projection distance,12repeated a prior proposal and20matched an acquired configuration. Keep those details and the matched random control visible.

## Capacity defect and qualified interpretation

All36requests returned.30were valid:25normal and5rotation probes. Six SACresponses hit512tokens, comprising all five normal SACcases and its one probe. Normal failures used the frozen full-domain batch3NN fallback; the raw failures and model cost were not removed.

**The SACfailures were guaranteed by a design error:** its59-field representation requires52binary/constant symbols per setting. Ten settings therefore need at least520binary digits. The actual pinned GGUFvocabulary contains at most one such digit per token compatible with the output character set, so≥520tokens are necessary even before other fields/delimiters/EOS. The frozen512-token cap cannot complete the format. Its original all30-valid screen was thus unattainable; I should have checked output capacity before freezing. This is not evidence against model reasoning on SAC. The exact vocabulary proof is `artifacts/study_v127/output_capacity.json` with model-hash verification receipt. A separate synthetic all-zero legal JSON fixture actually tokenized to601tokens using the existing offline tokenizer; it is not a generated response or optimization result.

The original protocol, raw completions, criteria, fallback branches and outcomes remain unchanged. The original report is preserved before a clearly marked capacity correction was attached. No cap was increased and no response repaired. All30cases remain in the main table.

Using only already charged V126outcomes, an ideal SAC-only repair replacing its five fallbacks by admitted-domain optima still gives−4.718%against sequential,−0.656%against matched random projection and−0.366%against full batch. Only1/6family means could then be positive against sequential. This is a nondeployable hindsight upper reference with the other25actual outcomes fixed. It shows a SAC-only repair cannot rescue these means; it does not rule out a different intervention elsewhere. No new LLM call or outcome acquisition was made for this diagnostic.

All five valid label-rotation pairs changed selection (overlap5,0,2,6,0of10; SACunavailable). That demonstrates limited dependence on target assignment, not useful optimization or a trained benefit predictor.

## Actual cost and limits

V127generation:36attempts/36returns,0retries,18,432allocated output tokens,9,361observed generated tokens and33,571observed prefill tokens;0missing new usage receipts.504.052s model lifecycle,2.590s startup,6,993,985,536byte peak sampled serverRSS, resource-stopreasonnull, serverexit0. Collection of900recorded outcomes took4.752s after choices were sealed. No native trials or external downloads.

Frozen limits:36requests/18,432allocated tokens/1,800s/8GiBserverRSS;900new recorded accesses/180s evaluation;zero retries/downloads/paid/cloud/spend. The496-input pre-generation freeze SHA256is63a63bd8ab9886ea24c4fd97052bf8686d60e94fe5efeaa3083773c8ce99b154. Model/runtime identities are unchanged from V124: Qwen3-8B Q4_K_M at the retained owner revision, llama.cppb11146, full weights/runtime hashes checked. This symbolic batch/Hamming method is a source-mapped adaptation, not exact SNAP2or LLAMBO replication.

Deployment would use one≤512-token request plus ten new objective evaluations per escalation under this tested contract; six probes and extra paired arms are research overhead. Projection, startup and objective latency are not a measured end-to-end deployment trace. No dollar, electricity or native-time saving is inferred. Historical prefix/control collection cost remains historical, not retrospectively free.

A post-hoc six-request loopback tokenizer check found the model server already closed: all six connection failures are preserved separately, with0generation and0processed responses. The existing offline tokenizer then completed six synthetic-format checks; these are metadata/fixture computations, not LLM completions. No server restart or model/download spending occurred.

## Verification and reproducibility

Full final suite: **1,005passed**,14dependency warnings,51.34s. Synthetic fixtures remain outside research aggregates. Independent replay validates36new requests, backend settings/prompts, strict failures, independently reconstructed projection/batch ranking,900source events,90paired budgets and30case comparisons. The full-project verifier checks the frozen dependency closure; the compact standard-library replay checks its saved-evidence subset.

The original frozen verifier failed because its independent batch sorter used(score,rowID)tuple ordering instead of the production algorithm's stable score-only ties over candidate order. A separate corrected verifier changes only that rule; two synthetic direction tests cover it. Original frozen code/failure are preserved. No collection, selection or reported result changed. Details: `reports/verification_correction_v127.md`.

Corrected report, comparisonJSON, PNG, capacity report and repair-boundJSON reproduce byte-identically. Figure visually inspected. The compact replay executes in isolated standard-library Python; private ZIPCRCchecks pass. No fresh inference on another host was performed.

## Evidence and execution

- Protocol/config: `reports/protocol_v127.md`, `.freeze.json`, `configs/study_v127.json`.
- Prefix-only prompts,36jobs,freezes,tests and receipts: `artifacts/study_v127/`.
- Raw requests/responses,actual prompts,backend settings,tokens,server log,ledger: `results/v127_proposals/`.
- Sealed90choices,raw900-event acquisition journal,paired states,all comparisons,projection/probe diagnostics and figure: `results/v127_analysis/`.
- Capacity proof and separate synthetic tokenizer receipts: `artifacts/study_v127/output_capacity.json`, `synthetic_offline_tokenizer.json`, `synthetic_tokenizer_diagnostic.json`.
- Post-hoc ideal SAC-only bound: `results/v127_analysis/repair_bound.json` and `reports/capacity_correction_v127.md`.
- Private executed replay: `output/v127_replay.zip`,1,933,271bytes,486hashed files; `output/v127_replay/README.md`. No runtime binaries/weights; no installation or network.

Create-once commands already executed; do not repeat:

```sh
.venv/bin/python scripts/prepare_proposal_v127.py
.venv/bin/python scripts/freeze_proposal_v127.py
.venv/bin/python scripts/collect_proposal_v127.py
.venv/bin/python scripts/analyze_proposal_v127.py
.venv/bin/python scripts/package_proposal_v127.py
```

Safe saved-evidence replay:

```sh
.venv/bin/python scripts/verify_proposal_v127_fixed.py
.venv/bin/python scripts/audit_output_capacity_v127.py --verify-only
.venv/bin/python scripts/reproduce_proposal_v127.py
.venv/bin/python -I -S output/v127_replay/replay.py
.venv/bin/python -m pytest tests -q
.venv/bin/python scripts/seal_proposal_v127.py --verify-only
```

Use the corrected report wrapper, not plain frozen analyzer --report, to retain its interpretation notice. The frozen original verifier is retained as a known failed implementation; use the fixed file above. Some large inputs are Git-ignored and required for full-project replay; compact replay contains its own source subset. Private packages are not public redistribution grants.

## Prior completed work and corrections

V124:180real stochastic numeric requests,143valid/37malformed,60charged outcomes; EIandmean same final targets, HIPAccfallback. V125:18real format probes,9/9valid in each condition versus4/9same original responses; no quality claim. V126:4,932charged accesses covered4,992admitted rows, six families/all30prefixes; only4cases could theoretically gain≥5%over batch and sequential, concentrated in two families. These are not learned-router outcomes.

V42had already proved that the old fixed pool cannot meet the later V123/V124joint5%screen. This was overlooked in those designs and is explicitly corrected in `reports/attainability_v125.md`. Original source records and failed criteria were not changed. V43/V44already tested uniform/diverse pools and a real1.5Bmodel; do not present them as untried next steps. Earlier V91genuine exceptions, V120/V121first-ten equivalence, V122projection failures and V123ties remain in the record.

V126packaging correction: its full-dependency ZIP includes36runtime files despite an original no-runtime-binaries sentence. The new `output/v126_replay_corrected.zip` (24,619,419bytes) changes only README/manifest wording, preserving all scientific bytes and the original sealed archive. Its standard-library replay never executes those binaries; no weights are bundled. `reports/package_correction_v127.md` and its receipt document both hashes. V124/V125/V127compact bundles do omit runtime binaries.

## Most important next action / what remains untested

**Freeze an independent replication of this negative mechanism result on newly reserved software families, with output-capacity preflight and the same strong cheap controls.** Do not spend another batch solely on SACor retune these exposed groups until favorable means appear. Existing local authorization covers preparation; no paid endpoint or cloud account is requested. `reports/next_experiment.md` records the prioritized design and stop conditions.

Useful benefit-aware routing on untouched systems, independent-host inference, original benchmark correctness/equal-utility/noise and a distinct contribution against close prior work remain unestablished. All current six groups are exposed; seeds are not independent software systems. The extensive adaptive history must be disclosed. Original V113second-host need, V111NGINXfailure and V52admission restrictions remain unchanged. Negative results can be research, but Q2novelty/acceptance cannot be guaranteed by additional runtime. No work is promised outside the active session.

## Cumulative ledger and sealed history

Real model requests **4,462**; recorded-table acquisitions **35,180**. Across V124–V127this continuation added234requests and5,892recorded accesses (60optimization+4,932coverage+900paired optimization/control). Tokenizer metadata/fixtures add no generations or objectives. Native totals unchanged: numerical880; NGINX81attempts/35,853,130byte-valid responses; DuckDB78; H2299; Kanzi1,265; RocksDB350. Keep units distinct.

Instrumented artifact downloads remain9,881,186,771/10GiB; remaining856,231,469bytes. Model payload9,126,358,023/9GiBunchanged. Older/web-provider unknown usage is unknown, not zero. No paid/cloud inference, new model/dependency install, credentials, system-setting changes, publication, remote push or messages.

V127seal: `artifacts/study_v127/evidence_manifest.json`; final receipt `seal_verification.json`. It anchors the combined V124–V126manifest SHA25682dcce43d9f937d7eb0f5b65c789d6a73f0dad4855cc29de458a26a6883e54a7 and checks51historical checkpoints. Prior mutable root documents are preserved in `artifacts/study_v127/previous_snapshot/`; earlier raw outputs/protocols/manifests remain immutable. Consult the final receipt for current file count/hash. Future edits require preserving this checkpoint and creating a new one.
