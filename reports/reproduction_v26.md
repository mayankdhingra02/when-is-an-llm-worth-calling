# V26: independent reconstruction succeeds in an extracted copy

**The latest result now has a standalone reconstruction package.** A new verifier independently reproduced the V25 result table from the original source tables and raw saved traces using only Python's standard library. It passed in an extraction outside the repository under **Python3.10.13 and Python3.12.14**, both with `-I -S` isolation and third-party package loading disabled. Both produced the same family means and aggregate values.

This is a concrete reproducibility result, not a new claim of LLM usefulness. It improves on the earlier V21 review archive, which omitted original tables and could only verify selected saved summaries. This focused package includes the three source tables, every input named by the216-reference V25 freeze, owner evidence/license, raw model traces, tokenizer vocabulary/license, relevant experimental source and the independent verifier. Model weights and installed dependencies are omitted.

## What was actually reconstructed

The verifier imports no experimental optimizer, evaluator, provider or resource-ledger module. Its own standard-library implementation:

- Filters and deduplicates the three source tables according to pinned schemas and source row identities.
- Recreates all15 seeded ten-evaluation prefixes and their acquired best/rest states.
- Replays15 original full-space classical arms,15 static-shortlist arms and15 new adaptive-shortlist arms, including150 charged journal entries against original targets.
- Independently decodes60 saved LLM output-token sequences using the owner tokenizer vocabulary, checks distinct-ID grammar traces, request identities and exact prepared messages, and replays all60 LLM outcome states.
- Recomputes terminal losses and the15 case rows, three family rows and final mean comparison.

| Method | Independently reconstructed equal-family mean loss |
|---|---:|
| Original full-space classical | 0.015580387366212076 |
| Static shortlist rank | 0.01133746429893384 |
| Adaptive shortlist | 0.01314247175809989 |
| LLM presentation mean | 0.011318957448751192 |

The result remains mixed: the adaptive-shortlist method improves the original classical average but trails the LLM mean. Static rank differs from the LLM mean by only0.00001851 normalized loss. No equivalence, unseen-system benefit or successful learned routing is established. [Scientific report and figure](shortlist_v25.md).

## Actual checks

**181 tests passed in1.34seconds** in the project environment. New synthetic tests check independent state updates, feature-only ranking and byte-level decoding. The archive was extracted to a newly created temporary directory outside the checkout; its verifier was launched there in a separate isolated process. Python3.10 replay took1.1553seconds and Python3.12 replay1.2241seconds for the staging archive. Timing is descriptive and includes no fresh inference.

Two corruption checks ran only on the temporary extraction. An added byte was rejected by the manifest check. An altered acquired objective, accompanied by an updated manifest checksum, was rejected by independent final-state reconstruction. The original bytes were restored and verification passed again. No measured workspace record was modified by these tests. Checksums are not a signature or protection against coordinated replacement of code and evidence.

Receipts: [3.10 replay](../artifacts/reproduction_v26/staging_replay.json), [3.12 replay](../artifacts/reproduction_v26/second_runtime_replay.json), [corruption tests](../artifacts/reproduction_v26/tamper_checks.json), [test log](../artifacts/reproduction_v26/tests.log). Final delivery/extraction receipts are retained separately in artifacts/reproduction_v26/ to avoid making the archive depend on its own hash.

## Run it

Extract the V26 ZIP and run inside its root directory:

```sh
python3 -I -S scripts/verify_reproduction_v26.py
```

No pip install, network, GPU, model weights or credentials are required. The command writes nothing; it prints counts and reconstructed means as JSON. The archive's README explains its contents and licensing. The source builder refuses an existing output and uses deterministic ordering/timestamps.

## Limits and costs

This is independent **saved-result reconstruction on the same host**, including a second Python version. It is not fresh model generation, a new OS/machine measurement, independently collected data, a full reproduction of all earlier stages or confirmation of the research hypothesis. Input prompt tokenization is not rerun; raw output decoding and grammar checks are. Without model weights the bundle cannot verify their bytes or reproduce logits. Owner identity/manifests and prior provenance checks are retained.

The three data files retain owner repository GPL-2.0 attribution; the Qwen tokenizer retains Apache-2.0 attribution. This is a local archive, not publication or a new grant of distribution rights for all project material. No email, upload, remote push or paper submission occurred.

New inference, objective acquisition, physical trials, downloads and external spend: **zero**. Packaging, independent reconstruction and test runtime are maintenance/verification costs, recorded separately from the experiment ledger. Historical counts remain200/200 follow-up calls,7058 recorded-label accesses and1134 physical trials; experiment runtime2252.612712/3600seconds. No background work remains.

**Single next action:** use this executable bundle for review with Tim, alongside the limits of the scientific result, before committing to another collection campaign.
