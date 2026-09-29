"""Serial fresh measurements; explicit attempt journal and bounded process groups."""
import hashlib,json,os,random,subprocess,sys,time
from pathlib import Path
from datetime import datetime,timezone
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'src'))
from escalation.live_compression_v17 import isolated_trial
OUT=ROOT/'results/v51_interfaces'
def read(p):return json.loads(Path(p).read_text())
def write(p,d):Path(p).parent.mkdir(parents=True,exist_ok=True);Path(p).write_text(json.dumps(d,indent=2)+'\n')
def append(p,d):
 with Path(p).open('a') as f:f.write(json.dumps(d)+'\n');f.flush();os.fsync(f.fileno())
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def schedule(datasets):
 settings=[s for d in datasets if d['system_group'] in ('zstd','lz4') for s in d['configurations']];rng=random.Random(51000);jobs=[]
 for repetition in range(5):
  block=settings.copy();rng.shuffle(block)
  for setting in block:
   modes=['api','cli'];rng.shuffle(modes)
   for mode in modes:jobs.append({'trial_id':len(jobs),'repetition':repetition,'setting':setting,'mode':mode})
 return jobs
def main():
 cfg=read(ROOT/'configs/study_v51.json');assert cfg['max_physical_attempts']==960 and cfg['max_stage_seconds']==180 and cfg['repetitions']==5
 assert cfg['max_model_requests']==cfg['max_external_spend_usd']==cfg['max_new_download_bytes']==0
 assert not OUT.exists(),'No implicit restart'
 for p,h in read(ROOT/'reports/protocol_v51_interface.freeze.json')['sha256'].items():assert sha(ROOT/p)==h,p
 env=read(ROOT/'artifacts/study_v15/environment.json')
 for p,h in env['sha256'].items():assert sha(p)==h,p
 libs={f:next(p for p in env['sha256'] if p.endswith('.dylib') and f'lib{f}.' in p) for f in ('zstd','lz4')}
 jobs=schedule(read(ROOT/'results/v50_utility/feature_manifest.json')['datasets']);assert len(jobs)==960
 work=read(ROOT/'artifacts/study_v15/workload_manifest.json');assert sha(ROOT/work['workload_path'])==work['workload_sha256']
 OUT.mkdir();write(OUT/'schedule.json',jobs);write(OUT/'environment.json',env)
 start=time.monotonic();ledger={'started_at':datetime.now(timezone.utc).isoformat(),'physical_attempts':0,'ok':0,'failed':0,'intended':960,'model_requests':0,'external_spend_usd':0}
 try:
  for job in jobs:
   left=180-(time.monotonic()-start)-2
   if left<=.1:raise TimeoutError('Stage limit')
   assert ledger['physical_attempts']<960
   f=job['setting']['family'];spec={**job,'workload_path':work['workload_path'],'workload_sha256':work['workload_sha256'],'binary':env['binary_paths'][f],'library':libs[f]}
   ledger['physical_attempts']+=1;append(OUT/'acquisitions.jsonl',{**job,'charged_physical_vector':1});write(OUT/'ledger.json',ledger)
   t=time.monotonic();actual=isolated_trial([sys.executable,str(ROOT/'scripts/worker_interface_v51.py')],json.dumps(spec).encode(),min(3,left),str(ROOT),{'PATH':'/usr/bin:/bin','LC_ALL':'C'})
   row={**job,'worker_seconds':time.monotonic()-t,'worker_returncode':actual['returncode'],'stderr':actual['stderr'],'status':'failure'}
   if actual['returncode']==0 and not actual['timed_out']:
    response=json.loads(actual['stdout']);assert response['roundtrip_equal'] and response['decoded_sha256']==work['workload_sha256']
    assert sha(ROOT/response['compressed_path'])==response['compressed_sha256'];row.update(response);row['status']='ok';ledger['ok']+=1
   else:ledger['failed']+=1
   append(OUT/'trials.jsonl',row);write(OUT/'ledger.json',ledger)
   if ledger['physical_attempts']%96==0:print(ledger['physical_attempts'],'/',960,'attempts;',ledger['failed'],'failures',flush=True)
 except Exception as e:
  ledger['stop_reason']=f'{type(e).__name__}: {e}';raise
 finally:
  ledger.update(stage_seconds=time.monotonic()-start,finished_at=datetime.now(timezone.utc).isoformat(),unattempted=960-ledger['physical_attempts']);write(OUT/'ledger.json',ledger)
if __name__=='__main__':main()
