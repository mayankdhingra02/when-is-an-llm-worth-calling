# V39: V38 now has a verified portable reconstruction archive

The corrected [V39.1 archive](../output/llm_escalation_v38_reproduction_v39_1.zip) reconstructs the latest V38 result from a temporary extraction outside the working checkout, using only Python's standard library. **Python3.10.13 and3.12.14 produce identical scientific outputs. All ten corruption controls are rejected, a restored extraction passes, and rebuilding produces byte-identical ZIP bytes.**

This is a concrete reproducibility result, not new optimization evidence. The V38 conclusion is unchanged: assigned-ID size-aware prompts gain1.7534% versus the prespecified exact joint3NN shortlist (2wins,7ties,1harm), while runtime3NN matches or beats all30LLMbranches (0wins,24ties,6harms). Two exposed families cannot establish generalizable routing success.

## Artifact and command

The archive contains **553 content files** plus its checksum manifest and is **4,041,210 bytes**. SHA-256:

`79d622f175347a098629bdaeb8b05faac1b885fea1b99be23e3a4eccec686b0a`

Extract it, enter `llm-escalation-v38-reproduction`, and run:

```sh
python3 -I -S scripts/verify_reproduction_v39.py
```

No pip installation, network, credentials, model weights or model call is required. [Included instructions](../BUNDLE_V39_README.md) explain scope and licenses. Source tables and owner licenses are included; weights, environments and unrelated files are excluded by an allowlist. This is a local archive only; nothing was uploaded, published or sent.

The portable verifier checks30new response decodings against the pinned owner tokenizer, generated-token grammar traces, prepared prompts, cache identities, model/revision and approval chronology. It matches300charged acquisition entries and thirty twenty-evaluation branch states to source-table strings. It recomputes150paired gains and15aggregates with exact fractions, including separate family means, then reconstructs200exact joint3NN decision steps from acquired labels. The prior independent V35.1 checker reconstructs original prefixes/shortlists and historical comparison branches, including runtime3NN and static rank. Neither checker imports the experiment's optimizer or model provider.

## Executed validation

- Two clean isolated replays: Python3.10.13 and3.12.14, same physical host, temporary directories outside the checkout, `-I -S` mode.
- Identical scientific JSON across both versions; runtime/environment metadata excluded from equality.
- Ten negative controls on temporary copies: checksum, raw output, cache key, acquired label, duplicate row, inclusive budget, missing completed arm, free acquisition, aggregate mean and family mean. The nine semantic controls rebind affected bundle/freeze checksums before verification; all still fail the intended semantic guard.
- After restoring original bytes, the clean replay passes again. Independent archive rebuild is byte-identical.
- The full project suite also passed: **258 tests in1.30seconds**. The ten executed artifact-corruption checks are separate from that test count and are never pooled as measured optimization outcomes.

The final validation harness took **43.693493 seconds** of maintenance wall time, including subprocesses and rebuilding. The earlier failed attempts have their own retained timings; this final duration is not presented as total development time. Maintenance/read-only reconstruction does not acquire labels or run the model and leaves experiment/resource ledgers byte-identical.

## Failures retained and corrections

1. The initial V39 ZIP omitted the historical V22 request-start log. Its first isolated run correctly failed with `FileNotFoundError`. The V39.1 builder adds that provenance dependency, model-runtime record and historical V34 result directory. The failed ZIP and logs remain in `output/llm_escalation_v38_reproduction_v39.zip` and `artifacts/reproduction_v39/`; use the corrected archive linked above.
2. V39.1 passed both clean interpreter replays. Its checksum corruption was rejected by the earlier frozen-source checksum guard, while the harness expected the later bundle-checksum message. V39.2 changes only that expected test message and reruns the complete validation. **The V39.1 ZIP and verifier remain byte-identical**; no second archive correction was necessary.

All experiment source, prompts, responses, outcomes and earlier archives remain unchanged. Protocol/freeze versions preserve the corrections: `protocol_v39_reproduction.*`, `protocol_v39_1_reproduction.*`, `protocol_v39_2_validation.*`.

## Evidence and limitations

Final receipts: [validation.json](../artifacts/reproduction_v39_2/validation.json), [Python3.10 replay](../artifacts/reproduction_v39_2/python310.json), [Python3.12 replay](../artifacts/reproduction_v39_2/python312.json), [negative controls](../artifacts/reproduction_v39_2/corruption_checks.json), [deterministic rebuild](../artifacts/reproduction_v39_2/deterministic_rebuild.json). Builder receipt: [build.json](../artifacts/reproduction_v39_1/build.json). Full suite log: `artifacts/reproduction_v39_1/tests.log`.

The portable checker independently decodes output tokens; it binds input token counts/rendered hashes to frozen records without redoing input tokenization. It does not regenerate model logits, verify omitted weight bytes, test physical correctness/noise, or prove trace authenticity against coordinated fabrication; hashes are not signatures. Both interpreters ran on one Mac. No separate physical-machine or V38 Linux reproduction is claimed. The earlier Linux check applies only to the V34 snapshot. No new untouched systems or learned-router evidence were added.

New cost: **zero model calls, objective acquisitions, physical trials, downloads or external spending**. Follow-up requests remain230/230, experiment time2530.796723/3600seconds, recorded acquisitions9608 and physical trials1274. No experimental limit increased and no background job was left running.

**Single most important next action:** have an independent reviewer run this archive on another machine and review the complete V38 comparison with Tim. The package is ready for that check; no contact was made. Further scientific collection should require an application-defined objective and untouched families with opportunity beyond strong cheap controls, rather than additional tuning on these exposed results.
