# V15: bounded live compression measurement feasibility

Purpose: establish whether this machine can collect correctly attributed, repeated, correctness-checked configuration measurements. This is development-only measurement feasibility, not another LLM experiment, learned-router evaluation or positive-result search. The three families become exposed development families; no fresh held-out claim follows.

Use already installed zstd1.5.7, lz4 1.10.0, and Python3.10.13's zlib1.2.12. Record binary/extension/library hashes and OS identity; OS shared-cache libraries are not fully archived. Do not install dependencies or change system settings. Treat these libraries as distinct implementation families for this smoke, without claiming independence from all shared infrastructure.

Workload: a901120-byte deterministic USTAR containing three unmodified CPythonv3.10.13 source files: Objects/unicodeobject.c, Python/ceval.c, Modules/_ssl.c. Owner tag resolves to49965601d6afedafe47cc85556d99b7a24981051. Preserve original hashes, license and exact archive construction. This is real source-code data; it is neither a generated synthetic fixture nor a representative production corpus.

Freeze32 settings per family before any physical trial:

- zstd: levels1,3,6,9 × windowLog17,18,19,20 × checksum off/on; single-thread mode.
- lz4: levels1,3,6,9 × block IDs4,5,6,7 × independent/dependent blocks; one compression thread. Larger blocks may be equivalent on this small input; report observed output equivalence, do not remove settings after seeing results.
- zlib: levels1,3,6,9 × memory levels5,6,8,9 × default/filtered strategy; fixed zlib wrapper/window15.

Three randomized rounds, each containing all96 settings once, order fixed by seed20260924. All288 intended trials remain in the denominator. **Each attempted physical repetition is one charged runtime/size/correctness vector**, including failures/timeouts. No uncharged warmups, retries or preflight compression trials. These are dataset-collection costs, not20-label optimizer arms. Do not pool physical runs with earlier table accesses without labeling cost types.

Every trial launches a fresh Python worker. Input read precedes timing. For zstd/lz4, compression time includes CLI startup, pipes and codec processing; zlib times the Python API. Decompression is separately timed; exact decoded bytes must equal input for the actual output from that trial. Preserve each compressed payload and digests. Do not compare raw timing across measurement stacks as if they were identical; no cross-codec ranking is the objective.

A parent owns the worker process group and kills/reaps the group at timeout, including spawned codecs. Serial trials, at most2seconds per whole worker. Inner codec operations have0.8second timeouts. The stage stops at90seconds, with cleanup reserve, within the existing cumulative1800seconds. No model requests; request count128 unchanged. Preflight refuses if remaining allowance cannot fit90seconds plus5seconds reserve. Journal each charge before launch; refuse silent reruns of started/complete outputs.

Report completion/failure denominator, exact roundtrip counts, configurations with all three observations, within-setting sample CV, and repeated-output stability. A CV above0.10 is a predeclared descriptive noise flag, not a rejection threshold or an application success margin. Preserve noisy/failing settings; three observations cannot establish reliable uncertainty or generalization. Report per-family output-digest equivalence without interpreting it as proof of identical internal behavior. Do not compute optimizer improvement, hindsight best configurations, routing policies or LLM gains in this stage.

Post-collection analysis/verification also uses the existing runtime ledger. It reads saved physical observations and payload hashes without rerunning compression; no new objective acquisition. Preserve prior freezes and all synthetic fixtures separately. Freeze code/configuration/tests/workload/environment before collection.
