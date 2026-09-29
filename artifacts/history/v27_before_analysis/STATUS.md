# Status — 2026-09-24 America/New_York: V26 standalone reconstruction delivered

## Resume here

**Concrete deliverable:** [3.6MB reconstruction ZIP](output/llm_escalation_v25_reproduction.zip), [report](reports/reproduction_v26.md), [instructions](BUNDLE_V26_README.md). Actual isolated extraction/replay succeeded on Python3.10.13 and3.12.14 with third-party packages disabled. The archive reconstructs the V25 numerical result from original source tables and raw saved traces using an independent standard-library verifier. It is a focused saved-result reconstruction,not new inference or an independent new-machine experiment.

Final ZIP:3,626,184bytes;295 checksummed files;SHA256747d21658e3ef143f7e1388e2a3677153143a2676a2cfa2ad2e7481dd4e11e1e. A second deterministic build is byte-identical. The older V21 PDF/ZIP remain historical; this new bundle contains the latest V25 result and necessary source inputs.

## Actual execution

After extraction,one standalone command suffices:

```sh
python3 -I -S scripts/verify_reproduction_v26.py
```

Both interpreter runs used a new temporary directory outside the repository and imported no experimental package. Actual checks:3 source tables,15 seeded ten-evaluation prefixes,15 original classical arms,15 static-rank arms,15 adaptive-shortlist arms,150 new-branch journal labels,60 saved output-token decodings/grammar traces and60 LLM outcome-state replays. Recomputed all15 case losses and three family means,matching the saved scientific result.

Full suite: **181 tests passed in1.34seconds**. Two corruption tests on the temporary extraction were correctly rejected:raw byte alteration;altered acquired label even after refreshing its manifest checksum. Restoring original bytes restored a passing replay. No original measured record was changed. All final archive bytes/outputs verified again after final packaging.

Build actually executed:

```sh
.venv/bin/python scripts/build_reproduction_v26.py --output output/llm_escalation_v25_reproduction.zip
```

Builder refuses existing output. Verification reads only and prints JSON. Root workspace lacks the archive manifest by design; run the standalone verifier from the extracted copy. Experimental-stage replay commands remain documented in reports/shortlist_v25.md.

## Evidence and preservation

- Final deliverable: output/llm_escalation_v25_reproduction.zip.
- Final build/replay/determinism receipts: artifacts/reproduction_v26/final_build.json,final_replay.json,determinism_verification.json.
- Staging two-interpreter replay,synthetic corruption checks,test log: artifacts/reproduction_v26/staging_replay.json,second_runtime_replay.json,tamper_checks.json,tests.log.
- Independent verifier: scripts/verify_reproduction_v26.py; builder: scripts/build_reproduction_v26.py.
- Report/instructions: reports/reproduction_v26.md;BUNDLE_V26_README.md. Source table/tokenizer owner licenses retained inside the bundle;no new distribution license granted to the whole project.
- Prior mutable docs: artifacts/history/v26_before_delivery/. No scientific protocol,raw outcome or experimental ledger changed during packaging.

## Scientific result remains unchanged

V25 actually collected15 adaptive-shortlist classical arms/150 charged labels. Equal-family mean loss:original classical0.01558039;static shortlist0.01133746;adaptive shortlist0.01314247;LLM mean0.01131896. The adaptive arm improves original classical on average but trails the LLM. Static rank is only0.00001851 behind the LLM mean;this is not equivalence or practical cost justification. Three exposed development families and repeated seeds do not establish held-out routing success. [Scientific report](reports/shortlist_v25.md).

V22's60 real-model calls,V23 formatting checks,V24 hindsight bounds and original smoke/group-held-out routing remain preserved. Hindsight is non-deployable. The exact SNAP2 artifact was not located in the bounded source search;implementations remain adaptations.

## Limits and cost

New inference,objective acquisitions,physical trials,downloads and external spending for V26:all0. Packaging and independent reconstruction are maintenance/verification time,recorded separately. Experiment ledger remains2252.612712/3600seconds;requests200/200 follow-up (300 historical including initial stage);7058 recorded-label accesses plus1134 separate physical trials. No active workers or scheduled campaign. No email,upload,push,publication or submission.

Staging replays took1.1553seconds on3.10 and1.2241seconds on3.12;final replay timings are in its receipt. This does not benchmark deployment performance. Model weights and experimental packages are omitted. Input tokenization,logits,fresh model generation,new-host/OS execution,earlier physical workload reproduction,practical utility thresholds and successful held-out/live routing remain untested. Output decoding and result reconstruction do not prove independent LLM regeneration. Checksums are not authenticity signatures.

**Single next action:** use the executable reconstruction bundle for review with Tim before authorizing a new application-grounded model/router campaign. Scientific thresholds/tasks still need agreement;no campaign is queued.
