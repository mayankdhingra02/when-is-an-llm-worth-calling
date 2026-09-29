"""Fresh bounded native confirmations, no optimizer/model calls or cached scores."""
import json,os,signal,subprocess,sys,time
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'src'))
from collect_smollm_v47 import read,write,append,sha,now
from run_planning_v55 import rss
OUT=ROOT/'results/v113_validation'
def main():
 for n,h in read(ROOT/'reports/protocol_v113.freeze.json')['sha256'].items():assert sha(ROOT/n)==h,n
 import numpy,scipy,highspy
 assert (numpy.__version__,scipy.__version__,highspy.Highs().version())==('2.2.6','1.13.1','1.7.2')
 cfg=read(ROOT/'configs/validation_v113.json');assert len(cfg['schedule'])==cfg['intended_acquisitions']==90
 rss(-1);assert not OUT.exists()
 for folder in ['requests','evaluations','stdout','stderr']:(OUT/folder).mkdir(parents=True)
 started=time.monotonic();records=[];stop=None
 env={**os.environ,'OPENBLAS_NUM_THREADS':'1','OMP_NUM_THREADS':'1','VECLIB_MAXIMUM_THREADS':'1','MKL_NUM_THREADS':'1'}
 for job in cfg['schedule']:
  if time.monotonic()-started>cfg['stage_seconds']-35:stop='stage_reserve';break
  key=job['request_key'];request=OUT/'requests'/f'{key}.json';result=OUT/'evaluations'/f'{key}.json';write(request,dict(job,at=now()))
  record=dict(key=key,family=job['family'],seed=job['seed'],arm=job['arm'],repeat=job['repeat'],row=job['row'],charged_acquisition=True,at=now())
  append(OUT/'starts.jsonl',record);records.append(record);p=None;peak=0;reason=None;t=time.monotonic()
  try:
   with (OUT/'stdout'/f'{key}.txt').open('x') as log,(OUT/'stderr'/f'{key}.txt').open('x') as err:
    p=subprocess.Popen([sys.executable,str(ROOT/'scripts/worker_numerical_v94.py'),str(request),str(result)],cwd=ROOT,env=env,stdout=log,stderr=err,start_new_session=True)
    try:
     while p.poll() is None:
      peak=max(peak,rss(p.pid))
      if peak>cfg['max_worker_rss_bytes']:reason='rss_cap'
      if time.monotonic()-t>cfg['worker_seconds']:reason='worker_timeout'
      if time.monotonic()-started>cfg['stage_seconds']-5:reason='stage_cap'
      if reason:os.killpg(p.pid,signal.SIGKILL);break
      time.sleep(.05)
     p.wait(timeout=3)
    finally:
     if p.poll() is None:os.killpg(p.pid,signal.SIGKILL);p.wait(timeout=3)
   if reason or p.returncode or not result.exists():raise RuntimeError(f'worker failed:{reason},exit:{p.returncode}')
   value=read(result);assert len(value['measurements'])==3
   if value['peak_worker_rss_bytes']>cfg['max_worker_rss_bytes']:raise RuntimeError('worker maxRSS')
   record.update(status='valid' if value['valid'] else 'failed_certificate',label=value['objective_seconds'])
  except Exception as exc:record.update(status='failed',label=cfg['penalty_seconds'],error=repr(exc))
  finally:
   if p is not None and p.poll() is None:
    os.killpg(p.pid,signal.SIGKILL);p.wait(timeout=3)
   absent=True
   if p is not None:
    try:os.killpg(p.pid,0);absent=False
    except ProcessLookupError:pass
   record.update(worker_wall_seconds=time.monotonic()-t,returncode=None if p is None else p.returncode,peak_sampled_rss_bytes=peak,stop_reason=reason,owned_process_group_absent=absent)
   append(OUT/'completed.jsonl',record)
   write(OUT/'ledger.json',dict(acquisitions=len(records),intended=90,stage_seconds=time.monotonic()-started,new_model_requests=0,external_spend_usd=0,records=records))
  if not absent:stop='cleanup_failed';break
  if len(records)%10==0:print(f'{len(records)}/90 confirmations completed',flush=True)
 write(OUT/'summary.json',dict(intended=90,acquisitions=len(records),unattempted=90-len(records),status='complete' if len(records)==90 else 'stopped',stop_reason=stop,stage_seconds=time.monotonic()-started,new_model_requests=0,records=records))
 print(json.dumps(dict(acquisitions=len(records),failures=sum(r['status']!='valid' for r in records),stop_reason=stop)))
if __name__=='__main__':main()
