# V78 proposed local paired batch — requires a new35-call allowance

Freeze before execution. This is an exploratory development comparison following
V77 classical results, not a new held-out family or a trained router evaluation.
Kanzi1.9 with the labelled V76 buffer repair; same fixed16MiB generated input,
448 canonical candidates, compressed output bytes minimized. All prior data and
failed trials stay intact. Do not alter the candidate domain or choose favorable
seeds after inspecting V77. All5seeds11,23,37,53,71 are mandatory.

## Exact scope

Reuse V77's5saved ten-evaluation prefixes (50historical physical trials). Run
fresh RF-LCB,3NN and LLM continuations under the SAME resident local model and
randomized round order (seed+78000). Each arm:7new search choices then3charged
confirmation trials of the smallest observed compressed size (tie smallerID).
20logical evaluations per arm;150new physical trials /300logical arm charges,
plus the50historical shared-prefix costs. No new prefix collection or warmups.

Use existing pinned SmolLM3-3B-Q4_K_M, revision/model hash and llama.cpp runtime
as V72. Loopback127.0.0.1 only; offline/no-webui; no downloads, cloud, credentials
or external spend. Maximum35generation requests,64output tokens/request,4096
context, temperature0, seed requested per case, no retries,1concurrent request.
No preliminary format calls. Count transport/parse failures and missing tokens as
unknown. Raw prompts/templates/tokenIDs/grammar/parameters/output/usage/timestamps
and request IDs retained. Pretraining contamination remains unknown.

Model returns [transform_index,entropy_index,block_bytes] under finite-domain
GBNF restricted to unacquired vectors. Prompt gives explicit name mappings and
only acquired compressed sizes, never receipt IDs, other-arm outcomes or hidden
candidate labels. Every model-selected vector requires actual objective collection.
No guessing/cached synthetic response may substitute for generation.

On malformed/truncated output, that case permanently falls back to RF-LCB for its
remaining search slots, with no new model calls for that case; retain intended35
request denominator and fallback counts. Transport/server errors stop the stage.
Application failure stops the stage; no repair or candidate removal mid-batch.
Do not call fallback outcomes valid LLM proposals. Proposed prompt/interface is
fixed in src/escalation/kanzi_policy_v78.py, parser reused fromV66/V72.

## Limits and measurement

Stage<=1800s, stop starting work after1640s; server startup<=120s and each HTTP
request<=120s, server sampled RSS<=8GiB. JVM each phase<=40s, heap768MiB,jobs1,
4active processors, process-group sampled RSS<=2GiB,trial files<=128MiB. A
watchdog failure terminates work; child JVMs are supervised directly and killed
on model resource-guard failure. No indefinite background server remains on exit.
Retain commands/logs/checksum/header/full-byte-check receipts and output hashes;
remove only validated bulky trial products after durable results, retain failed
ones. Input correctness is checked after every compressed output, including
confirmations. Fresh JVM startup/JIT/monitoring included in runtime.

## Predeclared descriptive analysis

Report every seed and every arm, confirmed median compressed bytes and all3
confirmation values, selected ID, whether LLM incumbent came from an actual
proposal or the prefix/fallback, paired size difference against RF and3NN, and
mean of seed medians. No selection of a preferred comparator after seeing results.
Practical descriptive flag: >=1% fewer/more bytes versus each comparator (chosen
before any Kanzi LLM outcomes, not a learned router threshold). Also report raw
byte differences so the margin does not hide small effects.

Report intended/actual requests, legal/invalid/truncated outcomes, fallbacks,
unknown tokens, transport/selection/startup/physical runtimes and resource peaks.
Distinguish actual collection (all arms+historical prefixes+diagnosis costs) from
hypothetical deployment of only one branch; do not price local tokens as dollars.
No dollar-value-per-byte or storage-cost assumption is made. If bytes are saved,
report bytes saved per added decision second as a descriptive tradeoff; it is
not a universal justification for inference or a deployable future-cost feature.

A hindsight RF/LLM oracle may be shown as a nondeployable observed upper reference,
not a fitted controller. Five seeds are one family. Stronger evidence still needs
independent families, development-only routing thresholds, a frozen held-out split
and clean reproduction. This batch alone cannot establish Q2 readiness.
