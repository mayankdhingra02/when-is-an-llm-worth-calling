# V172 proposal: model-scale test of LLM-specific escalation headroom

**Status: design frozen by hash in `artifacts/study_v171/freeze.json`. NOT AUTHORIZED FOR COLLECTION.** It needs the owner's explicit approval to raise the retained-download and model-payload caps, and freed disk space. No download, request or acquisition for this proposal has occurred. Motivation and evidence: `reports/audit_v171.md`.

## Question and estimand

The question: does a larger model from the same family create *LLM-specific* headroom where SmolLM3-3B and Qwen3-8B created none? Without such headroom, no escalation router has anything to select.

Primary estimand: the **number of the seven V151 ecosystems containing at least one LLM-specific win.** A win is a case where the model's B20 arm beats each of sequential 3NN, random-full, adaptive neighbor and GP-EI (ℓ=1, V155) by more than 1%, with objective direction handled explicitly.

Secondary measures:
- the case count of LLM-specific wins;
- equal-ecosystem mean relative and log-ratio gain versus sequential;
- equal-ecosystem hindsight headroom versus each cheap switch;
- the eight-engine grouping sensitivity;
- parse, projection, duplicate and fallback counts;
- tokens and latency.

For reference, the SmolLM3-3B and Qwen3-8B values in `results/v171_audit/audit.json` are 0 of 7 ecosystems and 0 of 70 cases each.

## Decision rule, fixed before any collection

- **≥2 ecosystems with an LLM-specific win:** the router question becomes testable at this scale. The next step would be a separately frozen, fresh, headroom-gated large-domain cohort, sized using the V171 design arithmetic. This result would *not* itself be router evidence.
- **0–1 ecosystems:** the no-LLM-specific-headroom finding extends from 3B to 14B within this interface. Close the router question for local models on this hardware and write up the boundary result.

No prompt, grammar, sampling or threshold may be changed after any V172 response is read. A second run on these cases would be exploratory and could not change the decision above.

## Treatment: the model factor only

- **Model.** `Qwen/Qwen3-14B-GGUF`, file `Qwen3-14B-Q4_K_M.gguf`, Apache-2.0, owner-published. The owner page on 2026-09-28 showed about 9 GB at commit `530227a`. Pin the full revision hash, exact bytes and SHA256 at download and store the license and README hashes. Qwen3-8B Q4_K_M from `Qwen/Qwen3-8B-GGUF` is the within-family comparator.
- **Runtime.** The existing llama.cpp b11146 runtime already used by V141–V168. No new runtime download.
- **Inputs.** Replay the exact model-independent message lists saved for all 70 cases in `artifacts/study_v141/prompts` (30), `artifacts/study_v144/prompts` (25) and `artifacts/study_v148/prompts` (15). Also replay each stage's grammar, sampling seed, temperature 0.7, top_p 0.95, top_k 0, min_p 0, repeat_penalty 1, thinking disabled, context 4096 and 1,024 output tokens. Before the first request, verify that the 14B model's rendered prompts equal the retained Qwen3-8B rendered prompts byte for byte; record any template difference instead of editing the messages.
- **Evaluation path.** Use the stage's own projection and tie-break code and the same saved B10 prefixes, charging all ten new recorded acquisitions per arm. Seal all 70 row selections before parsing any new target.
- **Classical arms.** Reuse the historical sequential, random-full, adaptive, fixed and GP-EI arms; do not rerun them. Recorded tables are deterministic lookups, so there is no host or timing confound.

## Finite limits

| Item | Limit |
|---|---|
| Model requests | 70 (one per case), 0 retries; under the 100-request ceiling in `configs/pilot.yaml` |
| Allocated output tokens | 71,680 (70 × 1,024) |
| New recorded acquisitions | 700 |
| Stage wall time | two stages of at most 1,800 s each (cases split by a fixed seed-17200 permutation), or one explicitly approved cap |
| Per request | 180 s; a timeout becomes a charged fallback to batch 3NN, reported as a failure |
| Server | sampled RSS at most 12 GiB, one server, no concurrent tests or native workloads |
| Download | one GGUF of about 9 GB plus license and README; nothing else |
| Money, cloud, credentials | none |

## Gates that must pass before the first request

1. Written owner authorization is recorded in `artifacts/study_v172/authorization.json`, raising:
   - the retained-download cap from 10 GiB, with 357,259,054 bytes remaining at V171;
   - the model-payload cap from 9 GiB, with 9,126,358,023 bytes used.
2. At least 25 GiB of free disk before the download. On 2026-09-28 only 12 GiB was free.
3. The downloaded file's SHA256 matches the owner LFS pointer at the pinned revision.
4. A preflight on one synthetic prompt (outside research aggregates) confirms that the server starts, the grammar applies and RSS stays within the cap. This is a charged model start, recorded separately.
5. Tokenized prompt plus 1,024 output tokens fits within 4,096 for all 70 prompts.
6. The V171 seal verifies. This protocol, the config and the implementation are hash-frozen in a new `artifacts/study_v172/freeze.json` before collection.

## Accounting and reporting

- **Research cost:** all requests, including fallbacks, the model load and preflight, all 700 acquisitions and the download bytes. The historical classical and 3B/8B costs remain in their original ledgers.
- **Deployment estimate:** one call plus ten evaluations after B10 per escalated case, with load time amortized separately.
- **Reporting:** all 70 cases with every comparator, even where the 14B model looks favorable. No pooling with native cohorts, no significance test across dependent seeds, and no journal-readiness claim.
- **Scope of the conclusion:** scale within one family and one interface. Qwen3-14B differs from 8B in more than parameter count, and neither is SNAP2's gpt-oss-120b.
