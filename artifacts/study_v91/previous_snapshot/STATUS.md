# STATUS — V90 complete classical screen; larger-model resource decision pending

## Resume here

User challenged stopping before paper readiness. Continued through actual V89/V90 native experiments rather than stopping after a plan. **V90:60/60valid trials,12,060exact independently checked answers; no setting passed the frozen10%all-block improvement and precision screen versus four-thread default.** Best median block gain1.64%, with losses in some blocks. Control repeat spread25.24% fails20%screen. This is exploratory screening, not equivalence, LLM evidence or Q2 readiness. Report `reports/flights_v90.md`; plot/table `results/v90_flights_analysis/`.

**Scientific decision: close this12-setting DuckDB domain for escalation research.** The20-evaluationbudget can enumerate it; do not add settings/repetitions merely to seek a win. Next priority: larger-model robustness on saved paired cases. Concrete owner-pinned candidate, limits and scope: `reports/resources_v91.md`, `configs/resource_proposal_v91.json`. No request for renewed permission on routine coding. The actual next resource barrier is a5.03GBmodel file against528,758,755remainingdownloadbytes plus exhausted historical inference allowances. Proposed new cumulative caps:10GiBtotal,9GiBmodel; up to303local generationrequests including3compatibilityprobes plus30cases×10choices; USD0,8GiBsampledmodelRSS,30minutes inference. Approval not recorded. `scripts/check_resources_v91.py` correctly rejects absent approval. Do not treat broad historical approval as a change to these numeric caps.

## Actual V89/V90 execution

- V89 froze16settings×5blocks. Stopped on ninthtrial: joint join_order/filter_pushdown disabling at1thread hit60-secondtimeout.9charged,8valid,1failed,71unattempted. Failed summer-query staticplan containsCROSS_PRODUCT; exact cause not proven. Failed trial partial answer count unknown (buffered until completion).
- V89 test-suite overlap was a mistake. Timestamp audit identifies trial08as potentially overlapping; preserve confound and full denominator. No completed-grid claim.1,608persisted answers revalidated in `results/v89_flights_failure_audit/`.
- V90 new frozen exploratory protocol excludes joint disabling, after inspectingV89failure.12settings×5blocks,all60correct; no concurrent managed tests or other collection. Same independent V88reference/data/runtime,3warmup+64scored querysuites,201checkedqueries/trial.
- V90 collection68.035seconds; V89collection70.302seconds. Combined69physicalcharges and138.337seconds fit original80/900ceiling.11unusedslots are not authorization to chase a result. V89's71unattempted denominator stays unchanged; follow-up kept separate.
- No newLLM/native hiddenprobes/downloadedpayloads/spending. Peak sampledV90RSS106,151,936bytes. Readbacks/networkdisabled/watchdogs/charge-before-launch and freezehashes independently validated.
- Raw evidence `results/v89_flights_grid/`, `results/v90_flights_grid/`; frozen protocols `reports/protocol_v89*`, `reports/protocol_v90*`; source metadata `artifacts/study_v89/runtime_metadata.json`.
- Commands: `.venv/bin/python scripts/run_flights_v89.py freeze` and `run`(retainedfailure), `scripts/audit_flights_v89_failure.py`, `scripts/run_flights_v90.py freeze` and `run`, `scripts/analyze_flights_v90.py`, `scripts/report_flights_v90.py`. Tests used explicit `-m pytest -q tests`; see `artifacts/study_v90/tests_final.log`. Native/model processes finished.

## Totals, prior result and integrity

Cumulative recorded downloads4,839,950,365bytes,528,758,755remainingunder5GiB; legacy modelledger4,098,574,535bytes. Modelrequests2,191unchanged. DuckDB cumulative78physicalcharges(V88:9,V89:9,V90:60),77valid/1timeout; keepV89's71unattemptedstageentries separate. Historical H2physical299(298valid,1failure;8unattempted),Kanzi1,265,RocksDB350,recorded-tableacquisitions26,358 unchanged. USD0; electricity/hardwareunknown. Browser metadata inspection is not a retained model/data-file transfer.

V86 remains primary scoped papercandidate:65,664hindsightchoices across25cases/3exposednativefamilies, no original-margin improvement beyond cheapcomparators; residualH2hindsightmeanheadroom0.262%,adverserepeatscenario0%. No universal failure/generalization claim. `reports/frontier_v86.md`; saved-summary replay `output/frontier_v86_1_reproduction.zip` remains intact.

Still missing: larger-model evidence, independent untouchedsystems, clean-machine native replication and meaningful held-out controller evaluation. Q2 readiness cannot be asserted from these screening results. Do not mark researchgoalcomplete.

Current integrity command `.venv/bin/python scripts/seal_flights_v90.py --verify-only`. Exact oldrootdocs preserved in `artifacts/study_v89/previous_snapshot/`; V88andoldermanifests remainimmutable. No cloud/credentials/systemsettings/publish/push/contact authorized. TPCgenerator remainsunused; its terms are unnecessary for this path.

Full final suite: **672 passed in 20.71s**. NewV89/V90grid and V91permission fixtures remain synthetic; no model approval is created by a passing fixture.
