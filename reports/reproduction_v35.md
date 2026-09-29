# V35.1: latest result reconstructed in an isolated portable archive

**The complete V34 constrained result now reconstructs from an extracted archive under Python3.10.13 and3.12.14, using only the standard library.** Both interpreters produce identical scientific outputs. Nine corruption tests are rejected, including eight after updating the bundle index, and a second build is byte-identical. This is a reproducibility result, not new evidence that an LLM router improves optimization.

Download the [verified archive](../output/llm_escalation_v34_reproduction_v35_1.zip): **3,690,811 bytes**, **418 content files** plus its manifest. SHA256:

`75333386b2ab80ac5a49ec554050fc1f4ba92e708a2c1908c1cdfcccecb663f9`

Extract and run from the extracted directory:

```sh
python3 -I -S scripts/verify_reproduction_v35_1.py
```

No dependency installation, network, weights, GPU or credentials are needed. The verifier reads only bundle files and prints JSON. Both tests ran in temporary extractions outside the checkout with site packages disabled, on the same host. The older V26/V25 ZIP is unchanged. The initial V35 archive is retained as failed cross-version evidence; use the V35.1 filename above.

## What was independently reproduced

The standalone verifier imports no study optimizer, evaluator or provider. Its own standard-library arithmetic and selection routines replay:

- Two filtered/deduplicated source tables, ten seeded classical prefixes, and ten acquired-label-derived shortlists.
- Three hundred adaptive decisions: constrained shortlist/full-domain3NN and runtime-only3NN. Recommendations receive features and acquired labels only.
- Sixty original V22 output-token sequences, grammar traces and prompt/cache/model/request bindings. Thirty relevant LLM selections are mapped to their unchanged original actions. Input tokenization and model weights are not re-executed.
- Seventy completed V34 branches, identical shared prefixes, inclusive20 budgets, acquired-prefix size caps and eight hundred ordered source-bound acquisition charges.
- One hundred twenty pairwise comparisons,240 Decimal score strings, family means and all constraint-diagnostic summaries.

The reconstructed primary result remains **−0.3015% mean feasible-runtime gain for assigned-ID model selections versus size-aware shortlist3NN**, with1win,6ties,3harms. The positive+1.3495% comparison against static ranking does not survive stronger controls. All three presentations have0wins,19ties,11harms versus runtime3NN. Scientific values and measured records were not changed.

## A real portability defect was found and corrected

The initial V35 verifier passed on3.10 but failed on3.12 before corruption tests. A separate diagnostic compared every saved joint-control decision state: **five of200 states disagreed on3.12, zero on3.10**. This did not run new alternate trajectories or measure their terminal outcomes.

| Case | Arm | Continuation step (zero based) | Saved selection | Initial 3.12 verifier selection |
|---|---|---:|---:|---:|
| lrzip_11 | joint_full | 6 | 678 | 750 |
| lrzip_37 | joint_shortlist | 2 | 281 | 245 |
| lrzip_53 | joint_full | 2 | 687 | 850 |
| brotli_37 | joint_shortlist | 8 | 53 | 62 |
| brotli_53 | joint_shortlist | 3 | 97 | 120 |

At lrzip/seed11/full-domain step6, the candidate predictions use the same three runtimes in different neighbor order. The recorded arithmetic gives15630.066666666666 versus15630.066666666668; the initial3.12 verifier gives15630.066666666666 for both and invokes the candidate-order tie break. Python's official3.12 release notes document the change to more accurate compensated float summation. [Primary Python documentation](https://docs.python.org/3.12/whatsnew/3.12.html#other-language-changes).

V35.1 uses an explicit left-to-right binary64 reduction for the three-term neighbor means, matching the frozen source experiment. It changes only the new verifier, not the original NumPy implementation or historical outputs. The diagnosis does **not** show that the original NumPy optimizer changes on3.12; that experiment was not rerun there. Mathematical ties can still be broken by rounding in the historical algorithm. Future algorithm changes should specify exact/Decimal or tolerance semantics prospectively and be labeled as adaptations, not silently applied to old results.

The first code, frozen protocol, failed archive and receipts are preserved under `artifacts/reproduction_v35/`. The corrected code/protocol and successful receipts use `v35_1`. A subsequent packaging attempt failed before ZIP creation because of a dotted/underscore README filename mismatch; a byte-identical compatibility README resolved it without altering frozen code. This failure is recorded in `artifacts/reproduction_v35_1/build_attempt.json`.

## Corruption and integrity checks

One ordinary changed-byte test is rejected by the file hash. Eight tests update the bundle index after corruption, then must fail at the intended semantic invariant: altered acquired label,19-evaluation budget,duplicate acquired row,changed prefix size cap,wrong cached request identity,zero acquisition charge,missing completed-arm entry,or falsified aggregate score. Each corruption is isolated to a temporary extraction and restored. Clean verification passes again afterwards. These checks are not protection against coordinated replacement of all evidence and verifier code; file hashes are not signatures.

The full project suite passes **241 tests**. Isolated clean replay took **3.0009s** on3.10 and **2.1173s** on3.12. The successful extraction,dual replay,nine negative checks,restoration and deterministic rebuild harness took **30.1533s**. These maintenance timings exclude development and the earlier failed/diagnostic runs. **422 included frozen references** pass inside the archive; **2,758 references** pass in the full historical audit.

Receipts: [3.10](../artifacts/reproduction_v35_1/python310.json), [3.12](../artifacts/reproduction_v35_1/python312.json), [nine corruption checks](../artifacts/reproduction_v35_1/corruption_checks.json), [final validation](../artifacts/reproduction_v35_1/validation.json), [historical audit](../artifacts/reproduction_v35_1/history_audit.json), [tests](../artifacts/reproduction_v35_1/tests.log). The freeze and builder make the ZIP reconstructible without changing its timestamps or order. Validation receipts live outside the delivered archive so it does not depend on its own final hash.

## Cost, scope and next action

New inference,objective acquisitions,physical trials,downloads and external spend: **zero**. The resource and download ledgers are byte-identical to their pre-V35 snapshots. Experiment runtime remains2281.347753/3600s, model calls200/200 follow-up (300 total including initial stage), recorded accesses9,108 and physical trials1,274. No active job,upload,push,email or publication.

This is same-host cross-interpreter saved-result reconstruction. It is not an independent-machine test,fresh model generation,proof of source authenticity,application validation or held-out routing result. The archive reproduces V34 and needed dependencies; it does not independently reconstruct every intervening stage. Owner data/tokenizer licenses and attribution are included. The original runtime-only prompts still do not test a size-aware model response.

**Single next action:** run this exact archive on a second machine as an independent reproduction check before extending the study. For new scientific collection,the unchanged [prospective plan](next_experiment_v34.md) still requires an application-grounded quality bound,strong controls,untouched groups and a new explicitly bounded inference allowance or compatible cache.
