# Next action after V75: controlled Kanzi failure diagnosis

The200-trial classical collection stopped on trial9 with an application exit13.
Eight trials passed;191were unattempted. No optimizer comparison completed.
The failing configuration/input and raw log are retained in
results/v75_kanzi_classical/eval_008/. Read reports/kanzi_v75.md first.

1. Freeze a small, bounded unmodified-control / isolated-patch diagnosis on the
   exact input and failing configuration. Record source diffs, compiler/runtime
   hashes and all charges before launching. Preserve the original owner JAR.
2. Test the source-supported stale-buffer hypothesis: ByteArrayOutputStream can
   grow its inherited buf, while CompressedOutputStream emits from data.array.
   A patch should emit the actual accumulated buffer, with exact byte validation.
   Do not assume the fix works; preserve failures and avoid repeated tuning.
3. If confirmed, freeze the subsequent choice: a clearly labelled patched
   adaptation, or an explicit failure-aware optimization objective. Define
   failure handling before another classical batch. Do not silently drop ANS1
   or remove configurations based on favorable performance.
4. Reassess domain validity. V75's448canonical configurations are not a certified
   >=400effective domain. Source support and header identity do not prove distinct
   outcomes. A diagnostic repair alone does not resolve this readiness limitation.
5. Only after a complete budgeted classical experiment consider a separately
   bounded model comparison with fixed prefixes, strong controls and inclusive
   confirmations. V72's35calls are consumed; no new inference scope is defined.

Keep Kanzi versions/workloads in one development group. Artificial input limits
production claims. Need independent families, frozen held-out groups, practical
benefit and cost margins, meaningful router evaluation and independent reproduction
before a journal-readiness claim. Preserve all negative/failure evidence. No paid
inference, cloud, credentials, publication, remote push or author contact.

Remaining download allowance562095257bytes; local diagnosis needs no downloads
or new external access. No process remains running. Do not rerun the V75collector.
