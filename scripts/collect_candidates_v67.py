"""All432 fixed grid trials; original correctness worker and retained failures."""
import hashlib,json,random,sys,time
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'src'))
from escalation.bounded_process_v57 import run
from run_planning_v55 import rss
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def write(p,x):p.write_text(json.dumps(x,indent=2)+'\n')
if __name__=='__main__':
    for name,digest in json.loads((ROOT/'reports/protocol_v67_screen.freeze.json').read_text())['sha256'].items():assert sha(ROOT/name)==digest,name
    assert json.loads((ROOT/'results/v66_candidate_feasibility/summary.json').read_text())['valid_trials']==9
    rss(-1)
    grids=json.loads((ROOT/'data/generated_v66/grids.json').read_text());schedule=[]
    for rep in range(3):
        for fi,family in enumerate(['duckdb','gnu_sort','openjpeg']):
            ids=list(range(48));random.Random(67000+1000*rep+fi).shuffle(ids)
            for cid in ids:schedule.append({'trial':len(schedule),'family':family,'workload':'fixed','round':rep,'config_id':cid,'configuration':grids[family][cid]})
    out=ROOT/'results/v67_candidates_physical';out.mkdir(exist_ok=False);write(out/'schedule.json',schedule)
    rows=[];started=time.monotonic();stopped=None
    for item in schedule:
        if stopped or time.monotonic()-started>1750:
            rows.append({**item,'status':'unattempted','reason':stopped or 'stage_cap'});continue
        folder=out/f"trial_{item['trial']:03d}";folder.mkdir();spec=folder/'spec.json';write(spec,item)
        def monitor(pgid):
            value=rss(pgid)
            return {'rss_bytes':value},('rss_watchdog' if value>1024**3 else None)
        receipt=run([str(ROOT/'.venv/bin/python'),str(ROOT/'scripts/worker_candidates_v66.py'),str(spec)],cwd=ROOT,log_path=folder/'worker.log',wall_cap=45,monitor=monitor)
        write(folder/'supervision.json',receipt)
        result_path=folder/'result.json';result=json.loads(result_path.read_text()) if result_path.exists() else {'status':'missing_result'}
        row={**item,**result,'supervision':receipt}
        resource=receipt['termination_reason'] in ['wall_timeout','rss_watchdog'] or result.get('error','').startswith(('OutOfMemoryException:','TimeoutError:'))
        if resource:row.update(status='resource_noncompletion',objective_ms=90000.)
        elif receipt['exit_code'] or receipt['termination_reason'] or result['status']!='valid':
            row['status']='unexpected_or_correctness_failure';stopped=row['status']
        rows.append(row)
        with (out/'trials.jsonl').open('a') as f:f.write(json.dumps(row)+'\n')
        print(item['trial'],item['family'],row['status'],flush=True)
    write(out/'all_cases.json',rows)
    summary={'intended':432,'attempted':sum('supervision' in r for r in rows),'valid':sum(r['status']=='valid' for r in rows),'resource_noncompletion':sum(r['status']=='resource_noncompletion' for r in rows),'unattempted':sum(r['status']=='unattempted' for r in rows),'complete_table':stopped is None and all('objective_ms' in r for r in rows),'stop_reason':stopped,'stage_seconds':time.monotonic()-started,'model_requests':0,'external_spend_usd':0}
    write(out/'summary.json',summary);print(json.dumps(summary,indent=2))
