"""Render complete SAT admission denominator; no new software executions."""
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def main():
    rows=[];stage=[]
    for v,path in [(62,'v62_sat_feasibility'),(63,'v63_sat_midpoint')]:
        assert json.loads((ROOT/f'artifacts/study_v{v}/verification.json').read_text())['verified']
        rows+=json.loads((ROOT/'results'/path/'all_cases.json').read_text());stage.append(json.loads((ROOT/'results'/path/'summary.json').read_text()))
    table='\n'.join(f"| V{62 if r['task']['variables']!=512 else 63} | {r['task']['id']} | {r['condition']} | {r['status']} | {r.get('wall_seconds',float('nan')):.6f} | {r.get('exit_code')} |" for r in rows)
    report=f'''# V62/V63 — SAT feasibility, with failed admission retained

Nine actual invocations ran: six valid models, three CPU-limit noncompletions,
zero retries or unattempted cases. All valid models independently satisfy every
original clause. The n512 midpoint is feasible with reference wall times5.665/5.432s
and bundled contrast12.107s. These are implementation probes, not optimizer arms,
an isolated-factor effect, a stable speedup estimate or any LLM result.

| Stage | Generated task | Condition | Status | Wall seconds | Exit |
|---|---|---|---|---:|---:|
{table}

V62 stage {stage[0]['stage_seconds']:.6f}s /180s; V63 stage {stage[1]['stage_seconds']:.6f}s /90s.
Per-run18s CPU,20s wall, sampled512MiB RSS. n1024 remains failed admission0/3;
it is not evidence no configuration or LLM can solve it. The n256 first reference
has a startup/host outlier relative to its repeat; no speedup is inferred there.
No failures were replaced. No new model requests, recorded-table optimizer accesses,
paid spending, system service, cloud provision or publication.

The source is [owner MiniSat](https://github.com/niklasso/minisat/tree/37dc6c67e2af26379d88ce349eb9c4c6160e8543),
commit37dc6c67e2af26379d88ce349eb9c4c6160e8543. The original MIT LICENSE, README,
CMake file and option declarations were inspected. Project-local Release build
uses installed macOS15.5 SDK and system zlib. The first build failed on an old
memory-report declaration; inspection also found a default-argument placement
incompatible with modern C++. Both declaration fixes are saved in an exact patch;
solver search code unchanged. This is a compatibility-patched adaptation, not
an untouched binary or a replication of historical benchmark timings.

Tasks are deterministic generated planted3-CNF: n256/seed62001, n1024/seed62002,
then n512/seed62003; floor(4.3*n) unique clauses. They are application workloads
executed by real software, separate from synthetic unit-test fixtures. A separately
stored known satisfying assignment validates generation; it must never enter
future optimizer/model features. Every returned model is checked clause by clause.
Original CNF, witnesses, solver models/logs, hashes, schedule and source/runtime
pins are retained. Generated planted instances have selection bias and are not
production/competition workload samples.

V63 is an explicitly adaptive feasibility calibration: n256 completed, n1024 timed
out, so one midpoint was frozen and run. No further size calibration is allowed
in this series. This is not a held-out confirmation. Conservatively group MiniSat
with previously exposed Z3 for future evaluation; do not claim an extra independent
software family from this implementation alone. Redis remains development and
MongoDB/Storm reservations are unchanged. A complete solver-code lineage assessment
has not been established; this conservative grouping avoids assuming independence.

Safe replay: scripts/verify_sat_v62.py and scripts/verify_sat_v63.py independently
check source/protocol hashes, both and then one generation witness, all six valid
models, raw receipts, timings and complete denominators. They do not run a solver
or an LLM. Both verifiers passed. SAT parser/generator tests use separate synthetic
fixtures and reject malformed CNF, duplicate/out-of-range assignments and false models.

The concrete next stage is [V64](protocol_v64_sat_screen.md): both admitted tasks,
48 predeclared configurations, three fresh repetitions,288 physical invocations,
primary RF-LCB versus random/3NN,30 arms/400 recorded accesses. No optimizer has
run on these tasks yet. Its requested7200s local cap exceeds the30-minute default;
exact resource approval is required before launch. Zero inference is included.
Passing its primary gate would only justify preparing a real-model test, not
prove a positive result or Q2 readiness. No task or outcome will be silently dropped.
'''
    (ROOT/'reports/sat_admission_v62_v63.md').write_text(report)
    print('SAT admission report generated')
if __name__=='__main__':main()
