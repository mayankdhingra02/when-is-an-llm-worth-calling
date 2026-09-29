# V96: controlled SuperLU crash diagnosis (exploratory)

Source inspection found that SciPy v1.13.1's bundled SuperLU StatInit allocates
21 histogram integers from default panel=20/relax=10, while its factorization
can index the histogram with the user-selected panel size. V94 allowed 32.
This is an identified out-of-bounds source path, not yet a native trace proving
which write caused each V94 failure. Successful solves cannot certify memory safety.

Select the first two V94 failures in the saved collection ledger:
`superlu_11_prefix_00` ([MMD_AT_PLUS_A, .1, 4, 32]) and
`superlu_23_prefix_00` ([COLAMD, .01, 1, 32]). Fix permutation, threshold and
relax. Compare panel sizes 16,20,21,32, five process-isolated repetitions each.
All 40 condition/repetition pairs are shuffled once with seed96000. Each
acquisition attempts three solves of the same V94 matrix/RHS with the same
independent residual/forward-error certificate. Record native sp_ienv defaults,
all starts/returns, returned solution vectors, signals, stderr, sampled RSS and
wall time. Enable Python faulthandler; disable worker core files. No native
library or optimization-policy code is patched.

Caps:40 newly charged configuration acquisitions,120 planned physical solves,
300s stage wall time,10s worker deadline,2GiB per-worker sampled RSS. Stop on
resource guard; leave remaining conditions explicitly unattempted. Native
crashes are expected diagnostic outcomes and do not trigger replacements.
There are no retries, LLM requests, optimizer/router evaluations or new groups.
This is a separately charged reliability experiment, not added budget in V94.

Primary descriptive outcome: valid/failed/unattempted process counts by panel
size and base configuration. Also report starts/returns and numerical
certificate checks. No p-value, timing-winner selection, population confidence
interval or panel threshold learned for the finished held-out study. Compare
V94 and V96 only qualitatively: the worker adds diagnostics and immediate vector
saving, which can change allocator behavior. A non-crash does not mean no corruption.
Do not amend V94 scores, remove its failures or reuse these outcomes to tune its
controller. Future optimization runs need a newly frozen memory-safe domain
or verified library fix. A sanitizer/debugger trace remains stronger causal
evidence than this unpatched reproduction.

Source files, installed binary, matrix, runner, worker, dependencies, this
protocol and synthetic guard tests are hashed before the first acquisition.
The source audit downloaded16,060bytes, below its65,536-byte cap; source bytes
match the git blob identifiers in the already saved SciPy v1.13.1 tree.
