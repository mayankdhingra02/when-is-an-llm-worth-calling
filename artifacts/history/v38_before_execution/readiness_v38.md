# V38: size-aware prompt preflight complete; inference awaiting approval

**All30new size-aware prompts pass preflight.** They contain1,765–1,918input tokens each (55,302total), below the frozen4,096-token input limit. The same candidate IDs,display orders,feature encodings and acquired runtime observations from the matched V22 requests are preserved. Output-size observations and the fixed cap come exclusively from previously charged ten-evaluation prefixes. An independent check verifies300acquired-only runtime normalizations and300size observations; no candidate has an outcome field.

This is a completed implementation/readiness result, **not a new LLM-performance result**. No V38 model request,objective acquisition or response exists. The old runtime-only responses have zero compatible cache keys for the changed prompts and cannot stand in for this experiment.

## Concrete experiment awaiting approval

Use the already installed Qwen/Qwen2.5-1.5B-Instruct at revision989aa7980e4cf806f80c7fef2b1adb7bc71aa306. Prepare three matched ID/display presentations for each of ten prefixes: Brotli0.3.0 and lrzip530 with five fixed seeds each. The new prompts explicitly ask for low runtime subject to the unchanged prefix-size research cap and show only acquired sizes. This tests a missing treatment from V34,which evaluated runtime-only model selections retrospectively.

The requested extension is exactly30local attempts,follow-up cap200->230,at most300new joint-vector acquisitions,zero retries,a600-second collection limit and unchanged3,600-second total experiment ceiling. At preparation time1,313.510297seconds remain; execution requires700seconds of reserve. No download,paid API,cloud resource,new model or spending is involved. The permission question was presented in this task; no answer has been recorded as of this readiness report.

The full frozen protocol is[protocol_v38_size_prompt.md](protocol_v38_size_prompt.md). Primary comparison is fixed assigned-ID size-aware LLM versus exact-arithmetic shortlist3NN. All three presentations are compared with the matching old runtime-only LLM,exact joint3NN(shortlist/full domain),runtime3NN and static rank. Final selection retains the fastest acquired feasible incumbent. The planned independent evaluator checks raw tokens,prompts,cache identity,source row labels,budgets and150paired comparisons,then emits CSV/JSON and a figure.

This is an exploratory two-family prompt experiment on exposed data. It does not establish application utility,unseen-system learned routing or a clean contemporaneous causal comparison: the old model calls happened in an earlier session. The cap remains a research default. No hypothesis or parameter will be selected from new outcomes.

## What actually ran

- `.venv/bin/python scripts/prepare_size_prompt_v38.py`: generated30new prompt records and ran the existing local tokenizer without loading model weights for inference.
- `.venv/bin/python -m pytest -q`: **258tests passed in1.15s**; synthetic authorization/prompt fixtures are separate from measured evidence.
- Independent preflight reconstructed prompt structure and acquired-only normalization, and rehashed **9model files /3,098,971,928bytes**, checking owner Git/LFS digests. This verifies existing files,not a download or model request.
- Both `scripts/run_size_prompt_v38.py --preflight` and the actual command without approval exited2. The sole blocker is the missing explicit30-call extension. Neither created a results directory,loaded an inference worker or changed the resource ledger.
- The evaluator and runner compiled successfully. The evaluator has not been validated against real V38 outputs because none exist; its source/token algorithms follow prior executed verifiers. End-to-end provider/collection/scoring behavior remains untested for the new prompts.
- **428inputs frozen**,and **3,586historical/current frozen references passed**. The authorization record is deliberately absent; a future grant must bind to the exact protocol-freeze hash before any request.

## Evidence and resumption

Prepared prompt bytes,IDs/mappings and expected cache/token hashes:[data/size_prompt_v38.json](../data/size_prompt_v38.json).
Token counts and isolation checks:[prompt_preflight.json](../artifacts/study_v38/prompt_preflight.json).
Independent model/prompt check and actual gate rejection:[independent_preflight.json](../artifacts/study_v38/independent_preflight.json).
Current blocker:[execution_preflight.json](../artifacts/study_v38/execution_preflight.json).
Tests:[tests.log](../artifacts/study_v38/tests.log).
Frozen inputs:[protocol_v38_size_prompt.freeze.json](protocol_v38_size_prompt.freeze.json).

After an explicit user grant,create `configs/authorization_v38.json` with granted=true,request_cap=230,additional_requests=30,runtime_cap_seconds=3600,stage_seconds=600,max_new_vectors=300,external_spend_usd=0,new_downloads=0,pinned model/revision,the current protocol-freeze SHA256,verbatim user authorization and recorded_at timestamp. Do not create this from a generic continuation request. Then run:

```sh
.venv/bin/python scripts/run_size_prompt_v38.py --preflight
.venv/bin/python scripts/run_size_prompt_v38.py
.venv/bin/python scripts/analyze_size_prompt_v38.py
.venv/bin/python scripts/analyze_size_prompt_v38.py --verify-only
```

Run only after approval. The runner preserves failed/completed transactions and does not restart or retry automatically. At any failure preserve all30intended statuses and report partial collection honestly. No model responses may be fabricated to fill missing cases. Token and runtime forecasts remain forecasts until requests occur.

## Current costs and next action

Resource/download ledgers and earlier measured results are unchanged. No new inference,labels,physical trials,downloads or external spend. Runtime2,286.489703/3,600seconds; follow-up calls200/200; recorded accesses9,308;physical trials1,274. No background work remains.

**Single next action:** explicitly approve or decline the bounded30-call extension. `AGENTS.md` says “Do not silently increase limits.” The exhausted allowance is the sole execution blocker; the prepared protocol,code,prompts and preflight are reviewable now.
