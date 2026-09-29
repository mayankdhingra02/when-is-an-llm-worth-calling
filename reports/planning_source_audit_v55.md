# V55 — compact Fast Downward source admission audit

Audited 2026-09-25; retrieved payload identities/timestamps/bytes are in
`artifacts/sources/v55/manifest.json`. Statuses below distinguish inspection from
execution. Full original target tables were not read by this continuation.

| Source | Verified support | Status / limits |
|---|---|---|
| [PerformanceEvolution owner artifact](https://github.com/ChristianKaltenecker/PerformanceEvolution_Website/tree/4ee53dad6b81543c444d44282053def0d82d97b3/PerformanceEvolution_Data/FastDownward) | README names data-network-opt-strips problem05, nine2016–2020 versions, five-repeat rule, Xeon/Debian hardware | README/XML/header inspected. Table-only `disjunctiveLMs`; XML outputString mapping mostly empty; plan validity/equal-cost/failed-run accounting unestablished. Do not admit historical timings from this metadata. V52 registry hash retained. |
| [Fast Downward pinned owner source](https://github.com/aibasel/downward/tree/1eef26b2cbf599a1894606aa898d9d49e1034cb9) | Tag release-24.06.1; local release_no_lp; README GPL3-or-later; BUILD macOS/CMake support | Inspected and compiled. Pin is not current latest26.6.0. Initial SDK/linker mismatch and local SDK15.5 fix both logged; no source patch or system-wide install. |
| [Pinned planner README](https://github.com/aibasel/downward/blob/1eef26b2cbf599a1894606aa898d9d49e1034cb9/README.md) | Primary project reference: Malte Helmert, *The Fast Downward Planning System*, JAIR26:191–246,2006 | Metadata verified from owner project; not a replication of paper timing results. |
| [Pinned benchmark](https://github.com/aibasel/downward-benchmarks/tree/e21d49c2cb61d147a46c5966f2581bf6fd422b9f/data-network-opt18-strips) | domain.pddl/p05.pddl, internal problem p9-3-15-tiny-network-4;9data,15scripts,3servers; three saved-data goals; cost minimization | Owner calls collection unofficial. Domain credits Manuel Heusner, Florian Pommerening, Alvaro Torralba. Exact byte equivalence to old experiment unproven; dataset redistribution license unresolved. Fresh adaptation label required. |
| [Pinned A* plugin](https://github.com/aibasel/downward/blob/1eef26b2cbf599a1894606aa898d9d49e1034cb9/src/search/search_algorithms/plugin_astar.cc) | g+h priority, heuristic tie break, reopening; documents equivalent general eager configuration | Source inspected. V56 varies tie rule but keeps g+h first and reopening, real costs, safe pruning. |
| [Landmark-cut plugin](https://github.com/aibasel/downward/blob/1eef26b2cbf599a1894606aa898d9d49e1034cb9/src/search/heuristics/lm_cut_heuristic.cc), [hmax plugin](https://github.com/aibasel/downward/blob/1eef26b2cbf599a1894606aa898d9d49e1034cb9/src/search/heuristics/max_heuristic.cc) | Admissible, action-cost support; hmax admissibility requires no axioms; lmcut rejects conditional effects/axioms | Actual task uses none of those unsupported constructs. Independent validator handles inspected subset only. Source comments are algorithm contracts, not an independently checked proof of compiled implementation. |
| [Pruning implementations](https://github.com/aibasel/downward/tree/1eef26b2cbf599a1894606aa898d9d49e1034cb9/src/search/pruning) | simple, EC and atom-centric stubborn sets document preservation of completeness/optimality and cite underlying publications | Inspected as configuration mappings, no new pruning invention. Defaults retained. |
| [Build/VAL warning](https://github.com/aibasel/downward/blob/1eef26b2cbf599a1894606aa898d9d49e1034cb9/BUILD.md#optional-plan-validator) | Flags VAL issue48 for IPC18 data-network; suggests older revision | Did not assume current VAL valid. Implemented separate project STRIPS/cost simulator; mature-validator cross-check still untested. |
| [macOS memory implementation](https://github.com/aibasel/downward/blob/1eef26b2cbf599a1894606aa898d9d49e1034cb9/src/search/utils/system_unix.cc) | get_peak_memory_in_kb returns task_info.virtual_size/1024 on macOS | Planner's huge reported memory is virtual address size, not RSS. Wrapper records sampled process-group RSS; driver does not support macOS address-space hard caps. |

V55 real execution: three validity-checked plans, all cost104; source/task/runner
inputs frozen first. V56 grid is a separately frozen development screen. Prior
SNAP2/EZR/MOOT audit and adaptation labels stand; this continuation does not claim
a new exact SNAP2 artifact or change older citations. MongoDB/Redis/Storm remain
reserved; no new timings from those groups were acquired.
