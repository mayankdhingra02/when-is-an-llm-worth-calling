# V96 source audit: SuperLU panel statistics

This audit uses the exact SciPy v1.13.1 sources and the installed binary already
pinned by V94. No claim about newer SciPy versions is made.

1. [`SRC/sp_ienv.c`](https://github.com/scipy/scipy/blob/v1.13.1/scipy/sparse/linalg/_dsolve/SuperLU/SRC/sp_ienv.c)
   returns20 for panel size and10 for relaxation (lines75–76 in saved file).
2. [`SRC/util.c`](https://github.com/scipy/scipy/blob/v1.13.1/scipy/sparse/linalg/_dsolve/SuperLU/SRC/util.c)
   `StatInit`, lines316–323, allocates `max(default_panel,default_relax)+1`
   histogram integers. Thus legal array indices are0 through20.
3. [`_superluobject.c`](https://github.com/scipy/scipy/blob/v1.13.1/scipy/sparse/linalg/_dsolve/_superluobject.c)
   accepts user-specified panel/relax values, initializes statistics through
   `StatInit`, then invokes factorization with those user values (saved
   `superlu_wrapper.c`, lines697,725,763). The histogram size is not adjusted there.
4. [`SRC/dgstrf.c`](https://github.com/scipy/scipy/blob/v1.13.1/scipy/sparse/linalg/_dsolve/SuperLU/SRC/dgstrf.c)
   uses `stat->panel_histo` (line240), resets panel size from the user width
   (line349), shortens it at structural boundaries, and increments its histogram
   at the resulting size (line356). Sizes above20 can therefore index past the
   allocation. Not every matrix/order necessarily visits the full requested size.

This is a direct source-level bounds inconsistency, not merely a correlation.
Whether it caused each recorded signal still needs instruction-level tracing
or an instrumented build. A worker can exit normally despite an out-of-bounds
write; numerical residual checks are not memory-safety checks.

The two newly downloaded sources total16,060bytes. Their Git blob SHA1 values
match the previously saved version-specific repository tree:
util.c `8da9fd1a9913bfebf7b80f5e2de97dea9f7c48b2`;
sp_ienv.c `804207c273bf2d936bf00985c5b8dc1140016ead`.
SHA256/URL/time/byte receipts are in `artifacts/sources/v96/fetch.jsonl`.
The initial sandbox DNS attempt failed before receiving source content;
authorized network retrieval succeeded. Process-monitoring preflight similarly
failed under the sandbox before acquisition and then succeeded with execution
permission. Neither attempt produced experimental outcomes.

These files declare the SuperLU BSD license and Regents/Lawrence Berkeley
copyright; see the V94 SuperLU/SciPy attribution. They are inspected upstream
source, not newly authored implementation. No external disclosure, publication,
repository push or author contact has occurred.
