"""Create-once finite feasibility; charge before launch and preserve failures."""
import os, signal, subprocess, sys, time
from collect_smollm_v47 import ROOT,read,write,sha,now
A=ROOT/'artifacts/study_v167'; OUT=ROOT/'results/v167_feasibility'
def main():
    cfg=read(ROOT/'configs/feasibility_v167.json')
    assert not OUT.exists()
    for n,h in read(A/'freeze.json')['sha256'].items():assert sha(ROOT/n)==h,n
    OUT.mkdir();start=time.monotonic();ledger={'at':now(),'outcomes':0,'query_executions':0,'model_requests':0,'retries':0,'status':'running'};write(OUT/'ledger.json',ledger)
    try:
        for job in read(A/'plan.json'):
            if time.monotonic()-start>cfg['stage_seconds_cap']-cfg['worker_seconds_cap']-5:raise TimeoutError('Stage cap')
            assert ledger['outcomes']<cfg['outcome_cap']
            q=3 if job['engine']=='polars' else 1
            assert ledger['query_executions']+q<=cfg['query_execution_cap']
            ledger['outcomes']+=1;ledger['query_executions']+=q;write(OUT/'ledger.json',ledger)
            path=OUT/f"{job['order']:03d}";path.mkdir();write(path/'start.json',{**job,'at':now()})
            cmd=[str(ROOT/'.venv/bin/python'),str(ROOT/'scripts/worker_apps_v167.py'),'--engine',job['engine'],'--candidate',str(job['candidate'])]
            env={k:v for k,v in os.environ.items() if not k.startswith(('POLARS_','XGBOOST_','OMP_'))};env['PYTHONHASHSEED']='16601'
            t=time.monotonic();proc=None;err=None
            with (path/'stdout.json').open('w') as stdout,(path/'stderr.txt').open('w') as stderr:
                proc=subprocess.Popen(cmd,cwd=ROOT,env=env,stdout=stdout,stderr=stderr,start_new_session=True)
                try:proc.wait(timeout=cfg['worker_seconds_cap'])
                except subprocess.TimeoutExpired:
                    err='worker_timeout';os.killpg(proc.pid,signal.SIGKILL);proc.wait()
                finally:
                    if proc.poll() is None:os.killpg(proc.pid,signal.SIGKILL);proc.wait()
            write(path/'end.json',{'at':now(),'wall_seconds':time.monotonic()-t,'return_code':proc.returncode,'error':err,'command':cmd})
            print(job['order'],job['engine'],job['candidate'],proc.returncode,flush=True)
        ledger['status']='completed'
    except Exception as exc:ledger['status']='failed';ledger['error']=repr(exc);raise
    finally:
        ledger.update(finished_at=now(),seconds=time.monotonic()-start);write(OUT/'ledger.json',ledger)
if __name__=='__main__':main()
