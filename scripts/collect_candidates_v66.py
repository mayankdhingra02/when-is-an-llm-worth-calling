"""Nine bounded utility-admission trials; zero optimizer or LLM calls."""
import hashlib,json,sys,time
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'src'))
from escalation.bounded_process_v57 import run
from run_planning_v55 import rss
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
if __name__=='__main__':
    for name,digest in json.loads((ROOT/'reports/protocol_v66_admission.freeze.json').read_text())['sha256'].items():assert sha(ROOT/name)==digest,name
    rss(-1) # Permission preflight before any measured work or output directory.
    out=ROOT/'results/v66_candidate_feasibility';out.mkdir(exist_ok=False)
    schedule=json.loads((ROOT/'artifacts/study_v66/schedule.json').read_text());assert len(schedule)==9
    rows=[];started=time.monotonic();stopped=set()
    for item in schedule:
        if item['family'] in stopped or time.monotonic()-started>550:
            rows.append({**item,'status':'unattempted','reason':'family_failure_or_stage_cap'});continue
        folder=out/f"trial_{item['trial']:02d}";folder.mkdir();spec=folder/'spec.json';spec.write_text(json.dumps(item,indent=2)+'\n')
        def monitor(pgid):
            value=rss(pgid)
            return {'rss_bytes':value},('rss_watchdog' if value>1024**3 else None)
        receipt=run([str(ROOT/'.venv/bin/python'),str(ROOT/'scripts/worker_candidates_v66.py'),str(spec)],cwd=ROOT,log_path=folder/'worker.log',wall_cap=45,monitor=monitor)
        (folder/'supervision.json').write_text(json.dumps(receipt,indent=2)+'\n')
        row={**item,**(json.loads((folder/'result.json').read_text()) if (folder/'result.json').exists() else {'status':'resource_noncompletion'})}
        row['supervision']=receipt
        if receipt['exit_code'] or receipt['termination_reason']:row['status']='resource_noncompletion'
        if row['status']!='valid':stopped.add(item['family'])
        rows.append(row)
        with (out/'trials.jsonl').open('a') as f:f.write(json.dumps(row)+'\n')
        print(item['trial'],item['family'],row['status'],flush=True)
    (out/'all_cases.json').write_text(json.dumps(rows,indent=2)+'\n')
    summary={'intended_trials':9,'attempted_trials':sum('supervision' in r for r in rows),'valid_trials':sum(r['status']=='valid' for r in rows),'unattempted_trials':sum(r['status']=='unattempted' for r in rows),'stage_seconds':time.monotonic()-started,'model_requests':0,'recorded_optimizer_accesses':0,'admitted_groups':[f for f in ['duckdb','gnu_sort','openjpeg'] if sum(r['family']==f and r['status']=='valid' for r in rows)==3]}
    (out/'summary.json').write_text(json.dumps(summary,indent=2)+'\n');print(json.dumps(summary,indent=2))
