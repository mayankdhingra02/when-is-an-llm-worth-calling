# V76: prospectively fixed buffer-defect diagnosis

After V75 failed, build an isolated Kanzi 1.9 adaptation changing only the final
entropy output buffer reference to the current ByteArrayOutputStream.buf, exposed
through a getter. Preserve original sources/JAR/results. The diff, source hashes,
compiler and runtime are pinned. No downloads, model calls, spending or publication.

Run exactly three charged trials on unchanged V74 16 MiB input:
1. Original owner JAR, exact V75 failing configuration. Expect exit13 and the same
   block49 invalid-length error. Keep this a failed application trial even if it
   supports the diagnosis. Stop if this control does not reproduce.
2. Patched JAR, same configuration. Require compression success, checksum/header
   settings, then full byte-exact decompression using the ORIGINAL owner decoder.
3. Patched JAR, V74 reference. Require the same checks and compressed SHA256 equal
   to V74's reference. Stop on any unexpected failure; no retries/patch tuning.

Configuration1/2: LZP+TEXT+BWT+LZP, ANS1,262144-byte block,jobs1. Reference3:
LZ+RLT,HUFFMAN,1048576-byte block,jobs1. All checksum enabled. No level preset.

Each phase <=40s; heap768MiB,4active processors,jobs1; sampled process-group
RSS<=2GiB, trial files<=128MiB,0.1s monitoring. Stage<=400s; no new trial after300s.
Retain full outputs/logs, charges, commands and hashes. At most3trials/5processes
if expected control fails; an unexpectedly successful control stops the stage.
No optimization or inference. Timings are descriptive, not a performance claim.

A reproduced control error plus successful patched recovery supports the narrow
buffer diagnosis for this input/configuration. It does not establish universal
correctness, a certified domain, LLM advantage or a journal contribution. Any
subsequent optimization batch needs a new prospective protocol and fresh prefixes;
V75 remains failed and never pooled as a completed comparison. Apache-2.0 owner
attribution and the local change remain attached to the adaptation.
