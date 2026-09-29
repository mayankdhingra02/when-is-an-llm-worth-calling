"""Six fixed SAT feasibility probes; no optimizer/model and no implicit retry."""
import hashlib,json,sys,time
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'src'))
from escalation.bounded_process_v57 import run
from escalation.sat_v62 import parse,validate_model
from run_planning_v55 import rss
OUT=ROOT/'results/v62_sat_feasibility'
def digest(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def write(p,o):p.write_text(json.dumps(o,indent=2)+'\n')
def main():
    for name,h in json.loads((ROOT/'reports/protocol_v62_sat_feasibility.freeze.json').read_text())['sha256'].items():assert digest(ROOT/name)==h,name
    rss(-1)
    binary=ROOT/json.loads((ROOT/'artifacts/study_v62/binary.json').read_text())['path']
    tasks=json.loads((ROOT/'data/generated_v62/manifest.json').read_text())
    configs={'reference':[.95,.999,100,2,2],'contrast':[.8,.9,25,1.2,0]}
    schedule=[{'trial':i,'task':task,'condition':c,'configuration':configs[c]} for i,(task,c) in enumerate((task,c) for task in tasks for c in ['reference','contrast','reference'])]
    OUT.mkdir(exist_ok=False);write(OUT/'schedule.json',schedule);rows=[];start=time.monotonic();stopped=None
    for item in schedule:
        row=dict(item)
        if stopped or time.monotonic()-start>155:row.update(status='unattempted',reason=stopped or 'stage_cap');rows.append(row);continue
        folder=OUT/f"trial_{row['trial']:02d}";folder.mkdir();cnf=ROOT/row['task']['path'];n,clauses=parse(cnf.read_text())
        args=[str(binary),'-verb=1','-cpu-lim=18',*[f'-{k}={v}' for k,v in zip(['var-decay','cla-decay','rfirst','rinc','phase-saving'],row['configuration'])],str(cnf),str(folder/'model.txt')]
        row['command']=args;write(folder/'start.json',row)
        def monitor(pgid):
            r=rss(pgid);return {'rss_bytes':r},('rss_watchdog' if r>512*1024**2 else None)
        row.update(run(args,cwd=ROOT,log_path=folder/'solver.log',wall_cap=20,monitor=monitor));row['log_sha256']=digest(folder/'solver.log');log=(folder/'solver.log').read_text()
        if row['exit_code']==10 and row['termination_reason'] is None:
            try:
                row['validation']=validate_model(n,clauses,(folder/'model.txt').read_text());row['model_sha256']=digest(folder/'model.txt');row.update(status='valid',objective_ms=row['wall_seconds']*1000)
            except (ValueError,FileNotFoundError) as exc:row.update(status='invalid_model',error=str(exc));stopped='invalid_model'
        elif row['termination_reason'] in ['wall_timeout','rss_watchdog'] or row['exit_code']==-24 or 'INDETERMINATE' in log or 'INTERRUPTED' in log:
            row.update(status='resource_noncompletion')
        else:row.update(status='unexpected_failure');stopped='unexpected_failure'
        write(folder/'result.json',row);rows.append(row)
        with (OUT/'trials.jsonl').open('a') as f:f.write(json.dumps(row)+'\n')
        print(row['trial'],row['status'],flush=True)
    write(OUT/'all_cases.json',rows)
    summary={'study':'v62','intended':6,'attempted':sum('exit_code' in r for r in rows),'valid':sum(r['status']=='valid' for r in rows),'unattempted':sum(r['status']=='unattempted' for r in rows),'stopped_reason':stopped,'stage_seconds':time.monotonic()-start,'stage_cap_seconds':180,'model_requests':0,'optimization_arms':0,'new_independent_family_claim':False}
    write(OUT/'summary.json',summary);print(json.dumps(summary,indent=2))
if __name__=='__main__':main()
