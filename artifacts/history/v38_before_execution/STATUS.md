# STATUS — V38 ready; awaiting explicit 30-call extension

Updated2026-09-25. Resume here and from [readiness report](reports/readiness_v38.md),[frozen protocol](reports/protocol_v38_size_prompt.md),and relevant code. Prior root docs/ledgers are preserved in`artifacts/history/v38_before_preparation/`.

**Next concrete implementation result:**30size-aware prompts validated,1,765–1,918input tokens each(55,302total),candidate mappings/order/runtime observations preserved,and only previously acquired sizes/cap added. All9local model files(3,098,971,928bytes) reverified against pinned owner digests. **258tests passed in1.15s**.428inputs frozen;3,586historical/current references pass.

**Not an LLM-performance result:** zero V38requests,responses or objective acquisitions. No`results/v38_size_prompt/`directory exists. End-to-end inference/scoring of new prompts remains untested. All old responses have incompatible new prompt/cache keys.

## Exact blocker and pending question

The user was asked to approve exactly30additional local attempts(cap200->230),up to300new recorded-vector acquisitions,600-second collection stage,existing3,600-second total runtime cap,USD0,no downloads/retries/cloud. No answer has been recorded. Generic “continue” does not extend the exhausted200/200request allowance. `AGENTS.md`:“Do not silently increase limits.”

Both preflight and the actual run command without approval exited2 before loading the model or writing a study result. The sole blocker is missing authorization. A grant must bind to the frozen protocol hash; no `configs/authorization_v38.json` has been created.

## Prepared design and code

Two exposed families(Brotli0.3.0/lrzip530),five fixed seeds,three original V22ID/display presentations each. Same local Qwen2.5-1.5B-Instruct revision989aa7980e4cf806f80c7fef2b1adb7bc71aa306,CPUfloat32,greedy20-token candidate grammar. Existing ten-row prefix and size cap; new prompts now explicitly include acquired output sizes and require the cap. Twenty inclusive evaluations per branch,ten new unique candidates,charge infeasible evaluations.

Primary comparator: exact joint3NN shortlist(V36). Report every presentation against matched old runtime-only LLM,exact joint3NNshortlist/full-domain,runtime3NN/static controls. No outcome-based presentation selection,no new router fit or held-out claim. The old calls are historical rather than contemporaneously randomized; research cap is not application-approved quality.

- Protocol/freeze:`reports/protocol_v38_size_prompt.*`.
- Actual prepared prompts:`data/size_prompt_v38.json`.
- Code:`src/escalation/size_prompt_v38.py`;`scripts/prepare_size_prompt_v38.py`,`run_size_prompt_v38.py`,`analyze_size_prompt_v38.py`.
- Evidence:`artifacts/study_v38/prompt_preflight.json`,`independent_preflight.json`,`execution_preflight.json`,`tests.log`,`history_audit.json`,`final_checks.json`.
- Gate tests are synthetic; never counted as model results. Analyzer compiled but has no real V38outputs to validate yet.

## Resumption after explicit approval

Create a grant record only from a direct approval of this exact extension. Required fields:granted=true,request_cap=230,additional_requests=30,runtime_cap_seconds=3600,stage_seconds=600,max_new_vectors=300,external_spend_usd=0,new_downloads=0,model_id/revision above,protocol_freeze_sha256,verbatim user_authorization,recorded_at. Then run:

```
.venv/bin/python scripts/run_size_prompt_v38.py --preflight
.venv/bin/python scripts/run_size_prompt_v38.py
.venv/bin/python scripts/analyze_size_prompt_v38.py
.venv/bin/python scripts/analyze_size_prompt_v38.py --verify-only
```

Require700seconds global reserve; stop/preserve denominator at failure or600seconds. No retries or overwrite. Afterwards independently verify alltokens/rows/budgets,inspect figure,report actual costs and update STATUS. Do not alter earlier frozen code to fit new ledgers; use versioned historical-audit wrappers if needed.

## Retained evidence and remaining limits

Latest scientific result remainsV36:5paths/3sets change under exact arithmetic,0terminal changes,all60LLM comparisons unchanged. V34assigned-ID model trails jointshortlist by0.3015%andfulljoint3NNby1.6470%. V37validated the V34archive on Linux/Python3.11 matching macOS3.10/3.12,but on the same physical machine. No unseen-system routing success established.

Resource/download ledgers byte-identical to pre-V38. Runtime2,286.489703/3,600s;remaining1,313.510297s. Follow-upcalls200/200(300includinginitial); recordedaccesses9,308;physicaltrials1,274. No new inference,labels,physicalruns,downloads,spend,cloud,push,publishing or contact. No ongoing job.

**Single next action:** approve or decline the concrete30-call local extension. All independent preparation is complete; actual V38inference awaits that resource decision.
