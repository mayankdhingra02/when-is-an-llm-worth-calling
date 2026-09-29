"""One-shot frozen grid, with charge-before-launch and bounded process group."""
import argparse,time
from run_flights_v88 import ROOT,DATA,read,write,sha,rss,run
from escalation.flights_v90 import CONFIGS,LIMIT,CHECKED,SCORED,schedule
ART=ROOT/'artifacts/study_v90';RAW=ROOT/'results/v90_flights_grid';FREEZE=ROOT/'reports/protocol_v90.freeze.json'
def monitor(pid):
    memory=rss(pid);disk=sum(p.stat().st_size for d in [DATA,RAW] if d.exists() for p in d.rglob('*') if p.is_file())
    return {'rss_bytes':memory,'scratch_bytes':disk},'rss_cap' if memory>2*1024**3 else 'scratch_cap' if disk>1024**3 else None

def main():
    p=argparse.ArgumentParser();p.add_argument('stage',choices=['freeze','run']);a=p.parse_args()
    if a.stage=='freeze':
        assert not FREEZE.exists();pins=read(ROOT/'reports/protocol_v88.freeze.json')['sha256']
        for n,d in pins.items():assert sha(ROOT/n)==d,n
        names=['reports/protocol_v89.md','reports/protocol_v90.md','src/escalation/flights_v90.py','scripts/worker_flights_v90.py','scripts/run_flights_v90.py','scripts/analyze_flights_v90.py','tests/synthetic/test_flights_v90.py','artifacts/study_v89/runtime_metadata.json','reports/protocol_v89.freeze.json','results/v89_flights_grid/summary.json','reports/protocol_v88.freeze.json']
        pins.update({n:sha(ROOT/n) for n in names});write(FREEZE,{'at_unix':time.time(),'sha256':pins,'schedule':schedule(),'intended_physical_trials':LIMIT,'new_model_calls':0});return
    rss(-1);freeze=read(FREEZE)
    for n,d in freeze['sha256'].items():assert sha(ROOT/n)==d,n
    assert freeze['schedule']==schedule();RAW.mkdir(exist_ok=False);start=time.monotonic();rows=[];stop=None
    try:
        for item in freeze['schedule']:
            assert len(rows)<LIMIT and time.monotonic()-start<730
            i=item['configuration_index'];folder=RAW/f'trial_{len(rows):02d}';folder.mkdir();cmd=[__import__('sys').executable,str(ROOT/'scripts/worker_flights_v90.py'),'--config',str(i),'--out',str(folder)]
            row={**item,'trial':len(rows),'configuration':CONFIGS[i],'status':'charged','command':cmd,'at_unix':time.time()};rows.append(row);write(folder/'charge.json',row);write(RAW/'acquisitions.json',rows)
            receipt=run(cmd,cwd=ROOT,log_path=folder/'process.log',wall_cap=60,monitor=monitor);row['process']=receipt;write(folder/'process_receipt.json',receipt)
            assert receipt['exit_code']==0 and receipt['termination_reason'] is None
            row['result']=read(folder/'result.json');assert row['result']['configuration']==CONFIGS[i] and row['result']['checked_queries']==CHECKED and row['result']['scored_queries']==SCORED*3
            row['status']='valid';write(RAW/'acquisitions.json',rows);print('validated',row['trial'],CONFIGS[i]['name'],flush=True)
    except Exception as e:
        stop=repr(e)
        if rows and rows[-1]['status']=='charged':rows[-1].update(status='failed',error=stop)
        write(RAW/'failure.json',{'error':stop})
    finally:
        write(RAW/'acquisitions.json',rows);write(RAW/'summary.json',{'intended_trials':LIMIT,'charged_trials':len(rows),'valid_trials':sum(r['status']=='valid' for r in rows),'failed_trials':sum(r['status']=='failed' for r in rows),'unattempted_trials':LIMIT-len(rows),'seconds':time.monotonic()-start,'stop_reason':stop,'complete':stop is None and len(rows)==LIMIT,'new_model_calls':0})
    if stop:raise RuntimeError(stop)
if __name__=='__main__':main()
