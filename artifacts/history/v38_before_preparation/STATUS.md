# STATUS — V37 Linux reconstruction complete

Updated2026-09-25. Resume here and from [Linux report](reports/linux_reproduction_v37.md), [frozen protocol](reports/protocol_v37_linux.md), and relevant code. Previous root documents/ledgers are preserved in`artifacts/history/v37_before_execution/`.

**Concrete result:** the unchanged V35.1/V34 archive reconstructs under **Linux/Python3.11.12**, with every scientific output identical to the earlier macOS3.10.13 and3.12.14 receipts. Two Linux corruption controls correctly fail; restored clean replay passes. The temporary container was automatically removed. This is a different OS/Python version on the same physical host,not independent-machine reproduction.

## Actual execution and evidence

- Existing Linux arm64 image ID`sha256:dbf1de478a55d6763afaa39c2f3d7b54b25230614980276de5cacdde79529d0c`; local tagpython:3.11.12-slim-bookworm. No pull. Registry origin not independently authenticated.
- Network disabled,read-only filesystem/inputs,non-rootUID65534,zero effective capabilities,no-new-privileges,256MiB/oneCPU/64process limit,64MiBtemporary extraction,90-second host deadline.
- Replayed418files/422included frozen references,2tables,10prefixes/shortlists,300adaptive decisions,60decoded model outputs,30relevant LLM selections,70V34arms,800journal records,120pairs/240Decimal scores. All numerical summaries match prior receipts exactly.
- Actual host validation9.773409s; in-container6.968893s. Maintenance time only.
- 251tests passed in1.61s;3,158historical/current frozen references verified;9stage inputs frozen before execution.
- Command:`.venv/bin/python scripts/run_linux_v37.py`(refuses overwrite; no pulls). Exact Docker args/raw output:`artifacts/study_v37/execution.json`.
- Receipts:`artifacts/study_v37/linux_receipt.json`,`validation.json`,`cleanup.json`,`history_audit.json`,`tests.log`,`final_checks.json`.
- Report:`reports/linux_reproduction_v37.md`; protocols:`reports/protocol_v37_linux.md`and`.freeze.json`.

Archive:`output/llm_escalation_v34_reproduction_v35_1.zip`,SHA256`75333386b2ab80ac5a49ec554050fc1f4ba92e708a2c1908c1cdfcccecb663f9`. Extract then run`python3 -I -S scripts/verify_reproduction_v35_1.py`. No dependency install or inference required. This is still a V34snapshot; later V36arms are not included.

## Failures and limits

Sandbox initially denied Docker socket access; explicit approval allowed the local engine check/run. One image-metadata template failed on an absent optional field; index-based metadata access succeeded. Container execution,negative controls,restoration and cleanup passed. No background container/job remains. Existing measured records and archives are unchanged.

V37 is saved-result portability,not fresh inference,authenticated publisher/model-weight verification,independent-machine validation,unseen-system routing or application/production evidence. Same ARMphysical machine. No model benefit claim added.

Latest scientific result remains V36: exact arithmetic changed5of20paths and3acquired sets,but0final runtimes; all60LLM comparisons unchanged. V34primary fixed-presentation gains remain−0.3015%vsjointshortlist and−1.6470%vsfulljoint3NN. Source prompts are runtime-only and constrained scoring retrospective. Both software families are exposed.

## Remaining allowance and next action

Experiment/download ledgers byte-identical to pre-V37. Runtime2286.489703/3600s;remaining1313.510297s. Requests200/200follow-up(300includinginitial); recorded accesses9,308; physical trials1,274. No new model calls,labels,physical runs,downloads or external spend. No cloud,push,publication or contact.

**Single next action:** have an independent reviewer run the unchanged archive on another physical machine. Local cross-OS/three-version checks are complete. New scientific collection remains`reports/next_experiment_v34.md`: application-defined quality/practical gain,strong controls,untouched groups,and an explicit bounded inference extension or truly compatible cache. Generic continuation does not expand the exhausted model-call allowance.
