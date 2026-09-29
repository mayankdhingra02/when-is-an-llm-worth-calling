# V96 source inspection and posthoc reliability diagnosis

V94 and V95 are complete and frozen. This new stage investigates the observed
association between SuperLU panel size 32 and V94 worker crashes. It is a
posthoc engineering diagnosis on an exposed system, not a new independent
optimization evaluation or a basis for editing V94 failures away.

Before any new native measurements, inspect original SciPy v1.13.1 bundled
SuperLU `SRC/util.c` and `SRC/sp_ienv.c`. Download at most 65,536 bytes total
from the SciPy owner repository; retain URL, SHA256, byte count and time.
Existing wrapper/factorization sources and installed binary are already pinned
by V94. This fits within the remaining 867,213,196-byte project allowance.
No model requests, paid services, new packages, remote writes or system changes.

After this source inspection, freeze the exact controlled diagnostic design,
runner and worker before execution. Diagnostic measurements must be charged
separately, bounded and kept out of optimization/router aggregates. Preserve
all attempted conditions and raw worker failures. No retries, selective deletion
or posthoc replacement of configurations. Existing root documents are saved
under `artifacts/study_v96/previous_snapshot/` before any update.
