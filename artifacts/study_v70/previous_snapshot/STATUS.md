# STATUS — V69/V69.1 physical feasibility and validity correction complete

## Resume here

**Actual native RocksDB work executed.** Four physical configuration attempts:
one failed final-result serialization; three complete receipts with100000checked
reads each. Subsequent active-engine audit validates onlythetwo reference receipts.
The contrast requested1MiBcache but ran with8MiBafter database reopening. Its timing
is invalid for the requested configuration; do not report a speedup/headroom result.

Report:reports/rocksdb_v69.md. Corrected authority:
results/v69_validity_audit/summary.json supersedes raw `valid` flags in V69.1.
Raw evidence remains untouched. Corrected binding passes native tiny synthetic
fixture tests at1,2,8MiB. Full-workload rerun has NOT happened. **502tests pass.**
No new optimization arm or LLM call. This is an integration finding, not Q2readiness.

## What ran and what failed

Owner rocksdict0.3.27 CPython3.10ARM64wheel, installed --no-index --no-deps into
.local-runtime/rocksdb-v69. WheelSHAverified againstPyPI; owner/source/runtimepins
in configs/runtime_v69.lock.json. EngineLOG/sourceheader agreeRocksDB9.8.4.
Prebuiltbinary used; no source compilation/clean-machine reproduction claimed.

YCSB-C-inspired adaptation:65536records,10x100-byte deterministic fields,10000warmup
reads,100000timedreads, fixed saved scrambledZipfiantrace(seed69001),PythonRNG and
raw concatenated fields. Same trace/expectedvalues everycase. EveryGet exact-byte
checked; full initial/finalscans verifyallkeys/content/count. OS cache not cleared.
512nominalfeaturevectors, but onlytworequestedvectors physicallyattempted;400distinct
legal/effectiveconfigurations not established. Development RocksDB/LevelDBfamily.

V69firstreference completed execute thenfailedserializing SSTmetadata bytes; objective
timing/digest missing, not imputed. Twooriginalschedule slots unattempted. Frozen
V69.1serialization-onlyrepair reranreference/contrast/reference. Timings ascollected:
0.317655334s,0.854398500s(INVALIDcontrast),0.297620083s. IncludesPythondriver,
instrumentation,bytechecking,responsehash; notpureengine time. Too fewshortrepeats
for noise inference. Sourcecodecomparison verifies serialization-only V69.1repair.

Binding reopens with loadedcolumnfamilyoptions/default8MiBcache whenonlyDBoptions
arepassed. Originalreadback searchedoldLOGaswellasactiveLOG andmissedthemismatch.
New src/escalation/rocksdb_binding_v69.py passes explicitdefaultcolumnfamilyoptions
andchecksactiveLOGonly. RegressionrejectsstaleLOG. Nativetinyfixturetests verify
requestedcachecapacity and actualattachedcacheusage. These are synthetic tests,
notadditionalperformance trials. V69.1retrylimit reached; nofurtherphysicalretries.

## Evidence and safe replay

- Rawattempts:results/v69_rocksdb_feasibility/ andresults/v69_1_rocksdb_feasibility/
  preserveengineDBs/SSTs/OPTIONS/LOG,workers,supervisors,schedules andfailures.
- Validityaudit/CSV/PNG/SVG:results/v69_validity_audit/. Figurevisuallychecked;
  depictsrequestedvsappliedcache,notoptimizationperformance.
- Inputs/trace/nominalgrid:data/generated_v69/. Ownerbytes/manifests:
  artifacts/sources/v69/ andartifacts/sources/v69_repair/.
- Protocols:reports/protocol_v69.md,protocol_v69_1.md and.freeze.jsonfiles.
- Logs/ledger/verification:artifacts/study_v69/. Currentseal:evidence_manifest.json.

```
.venv/bin/python scripts/verify_rocksdb_v69.py
.venv/bin/python scripts/seal_evidence_v69.py --verify-only
.venv/bin/python -m pytest -q tests
```
Firsttwoarestrictlyreadonly,nodatabaseopens. Testsaddtinysyntheticnativefixtures
whentheoptionalpinnedruntimeexists(3testsotherwiseexplicitlyskip). Do notdelete
outputdirectories to rerunone-shotcollection. Figure regenerationchangesmetadata;
rerenderinacopy. V68entrydocs preservedbeforeedits under
artifacts/study_v69/previous_snapshot/. NewsealverifierresolvesV68andearlierhistory.

## Costs and limits

V69:4physicalattempts;2validrequestedsettingreceipts,1invalidcontrast,1serialization
failure. 3complete receiptsrecord196608loadwrites,300000timedverifiedreads,
30000warmupreads,393216scanrecords. Failedreceiptadditionalcountsareinferredfrom
completedcodepath andseparateinledger; objective timeunknown. Workerprocesswalltime
4.282466501s includingfailure; parentstages4.291545625s; inputprep6.951852500s.
Peak sampledRSS221822976bytes, nothardmemorylimit. Newnativesyntheticfixturesran
6times acrossfocused/fulltests(12DBopens),excludedfromperformanceresults.

Newdownloads3943560bytes; cumulative4800270357bytes;568438763bytesremainunder5GiB.
Newmodelrequests0,optimizeracquisitions0,externalspendUSD0. Cumulative1981model
requests and26358recordedacquisitions unchanged. Hardware/electricity/human/agent
costunknown; nodeploymentcostestimated. Ledger:artifacts/study_v69/resource_ledger.json.
InitialDNS/quoting/pspermissionsfailuresrecoveredbeforephysicalcollection; saved
source/workerlogsandreportidentifyfailures. Nojobsleftbackgrounded.

## Single next action

Freezea NEWthree-casefeasibilitystage usingcorrectedexplicit-column-familybinding,
sameworkload/settings,active-onlyreadback,attachedcacheusageassertions,andatomic
progress/resultreceipts. OldV69retryallowanceexhausted;preserveallfailures. Onlythen
freezea20-evaluation/10-checkpointclassicalstudy. Do notreuseinvalidcontrasttimings
or resizeworkloadafterlookingatscores. See reports/next_experiment.md.

No newinferenceallowance. V65real-model5/5allowance remains exhausted; V67DuckDB/
GNU-sort/OpenJPEGfailedopportunitygridsstayclosed. Latestreal-modelV65remains0/5
contractvalidresponses,5RFfallbacks. Untested:correctedfullworkload,largereffective
configurationdomain,classicalheadroom,realconstrainedgrammar,pairedLLMbenefit,
held-outcontrollerandindependentmachine. Journalreadinessunestablished.
