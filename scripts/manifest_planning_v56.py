"""Seal completed V55/V56 evidence and explicit source/data lineage."""
import hashlib,json
from datetime import datetime,timezone
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]

def digest(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def read(p):return json.loads(p.read_text())
def write(p,obj):p.write_text(json.dumps(obj,indent=2)+'\n')
def main():
    physical=ROOT/'results/v56_planning_physical';screen=ROOT/'results/v56_planning_screen'
    summary=read(physical/'summary.json');assert summary['complete_admissible_table']
    verification=read(ROOT/'artifacts/study_v56/verification.json');assert verification['verified']
    source=read(ROOT/'artifacts/sources/v55/manifest.json')
    source_by_name={Path(s['path']).name:s for s in source}
    manifest={'family':'fastdownward','split':'development_only','independent_system_groups':1,
              'planner_owner':'aibasel/downward','planner_commit':'1eef26b2cbf599a1894606aa898d9d49e1034cb9',
              'planner_version':'release-24.06.1','workload_owner':'aibasel/downward-benchmarks',
              'workload_commit':'e21d49c2cb61d147a46c5966f2581bf6fd422b9f',
              'workload_path':'data-network-opt18-strips/p05.pddl','workload_identity':'p9-3-15-tiny-network-4',
              'sources':{key:source_by_name[key] for key in ['downward.tar.gz','domain.pddl','p05.pddl']},
              'outcome':'median of three penalized wall milliseconds; noncompletion penalty20000ms',
              'utility':'independently valid goal-achieving plan with total-cost104',
              'physical_intended':144,'physical_attempted':summary['attempted'],'physical_valid':summary['valid'],
              'table_sha256':digest(screen/'table.json'),'raw_trials_sha256':digest(physical/'trials.jsonl'),
              'protocol_freeze_sha256':digest(ROOT/'reports/protocol_v56_planning_screen.freeze.json'),
              'not_a_historical_timing_replication':True,'llm_calls':0,
              'dataset_redistribution_permission':'unresolved; local only'}
    write(ROOT/'data/live_manifest_v56.json',manifest)
    selected=set()
    for folder in ['results/v55_planning_feasibility','results/v56_planning_physical','results/v56_planning_screen','artifacts/study_v55','artifacts/study_v56']:
        selected.update(p for p in (ROOT/folder).rglob('*') if p.is_file() and p.name not in ['evidence_manifest.json','evidence_manifest.sha256'])
    paths=['reports/protocol_v55_planning_feasibility.md','reports/protocol_v55_planning_feasibility.freeze.json',
           'reports/protocol_v56_planning_screen.md','reports/protocol_v56_planning_screen.freeze.json',
           'reports/planning_source_audit_v55.md','reports/planning_screen_v56.md','data/live_manifest_v56.json',
           'scripts/fetch_planning_v55.py','scripts/build_planning_v55.py','scripts/build_planning_v55_retry.py',
           'scripts/run_planning_v55.py','scripts/collect_planning_v56.py','scripts/screen_planning_v56.py',
           'scripts/verify_planning_v56.py','scripts/report_planning_v56.py','scripts/manifest_planning_v56.py',
           'src/escalation/planning_v55.py','src/escalation/classical_planning_v56.py','src/escalation/classical_java_v54.py',
           'tests/synthetic/test_planning_v55.py','tests/synthetic/test_planning_v56.py','tests/test_planning_replay_v55.py',
           'requirements.lock.txt','STATUS.md','README.md','reports/next_experiment.md','THIRD_PARTY.md']
    selected.update(ROOT/p for p in paths)
    obj={'study':'v55_v56','sealed_at_utc':datetime.now(timezone.utc).isoformat(),
         'files':{str(p.relative_to(ROOT)):{'sha256':digest(p),'bytes':p.stat().st_size} for p in sorted(selected)}}
    path=ROOT/'artifacts/study_v56/evidence_manifest.json'
    if path.exists():raise FileExistsError('Do not overwrite evidence seal')
    write(path,obj)
    (path.with_suffix('.sha256')).write_text(digest(path)+'\n')
    print(json.dumps({'files':len(obj['files']),'manifest_sha256':digest(path)},indent=2))
if __name__=='__main__':main()
