"""Bounded decode verification followed by charged, acquired-only classical arms."""
import copy,hashlib,json,os,subprocess,sys,time,zlib
from datetime import datetime,timezone
from pathlib import Path
from types import SimpleNamespace
from utility_v50 import eligible,frame_fields
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'src'))
from escalation.offline_live_v16 import FEATURES,REFERENCES,RecordedOracle,make_prefix,continuation
OUT=ROOT/'results/v50_utility'
def read(p):return json.loads(Path(p).read_text())
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def write(p,data):
 p=Path(p);p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(data,indent=2)+'\n')
def append(p,data):
 with Path(p).open('a') as f:f.write(json.dumps(data)+'\n');f.flush();os.fsync(f.fileno())
def now():return datetime.now(timezone.utc).isoformat()
def main():
 cfg=read(ROOT/'configs/study_v50.json')
 assert cfg['max_stage_seconds']==180 and cfg['max_decode_verifications']==846 and cfg['max_recorded_vector_acquisitions']==450
 assert cfg['max_model_requests']==cfg['max_new_compression_trials']==cfg['max_external_spend_usd']==0
 assert not OUT.exists(),'Preserve one-shot collection'
 for p,h in read(ROOT/'reports/protocol_v50_utility.freeze.json')['sha256'].items():assert sha(ROOT/p)==h,p
 env=read(ROOT/'artifacts/study_v15/environment.json')
 for p,h in env['sha256'].items():assert sha(p)==h,p
 work=read(ROOT/'artifacts/study_v15/workload_manifest.json');payload=(ROOT/work['workload_path']).read_bytes();assert hashlib.sha256(payload).hexdigest()==work['workload_sha256']
 trials=[json.loads(s) for s in (ROOT/'results/v17_measurements/trials.jsonl').read_text().splitlines()];assert len(trials)==846
 manifest=read(ROOT/'data/live_manifest_v17.json');OUT.mkdir()
 ledger={'started_at':now(),'decode_verifications':0,'decode_passes':0,'recorded_vector_acquisitions':0,'completed_cases':0,'model_requests':0,'new_physical_compression_trials':0,'external_spend_usd':0}
 start=time.monotonic()
 def check():
  if time.monotonic()-start>cfg['max_stage_seconds']-3:raise TimeoutError('V50 stage cap')
 try:
  datasets=[]
  for d in manifest['datasets']:
   ss=[r for r in d['configurations'] if eligible(r)]
   assert len(ss)=={'zstd':48,'lz4':48,'zlib':90}[d['system_group']]
   datasets.append({**d,'configurations':ss,'split':'development_exposed','v50_contract':'checksum_and_independent_block_contract'})
  write(OUT/'feature_manifest.json',{'datasets':datasets,'feature_only_admission':True})
  for trial in trials:
   check();assert ledger['decode_verifications']<846
   setting=trial['setting'];family=setting['family'];compressed=(ROOT/trial['compressed_path']).read_bytes()
   assert hashlib.sha256(compressed).hexdigest()==trial['compressed_sha256'] and len(compressed)==trial['compressed_bytes']
   identity={'trial_id':trial['trial_id'],'config_id':setting['config_id'],'family':family,'at':now()}
   ledger['decode_verifications']+=1;append(OUT/'decode_starts.jsonl',identity);write(OUT/'ledger.json',ledger)
   fields=frame_fields(family,compressed);error=None
   if family=='zlib':decoded=zlib.decompress(compressed)
   else:decoded=subprocess.run([env['binary_paths'][family],'-q','-d','-c'],input=compressed,stdout=subprocess.PIPE,stderr=subprocess.PIPE,timeout=min(2,180-(time.monotonic()-start)-1),check=True).stdout
   equal=decoded==payload
   assert equal,'Saved output failed exact decode'
   if family=='zstd':assert fields['content_checksum']==setting['checksum']
   if family=='lz4' and eligible(setting):assert fields['content_checksum'] and fields['independent_blocks']
   if family=='zlib':assert not fields['preset_dictionary'] and fields['window_log']==15
   result={**identity,'sha256':trial['compressed_sha256'],'decoded_sha256':hashlib.sha256(decoded).hexdigest(),'exact_bytes_equal':equal,'frame':fields,'eligible':eligible(setting)}
   append(OUT/'decode_results.jsonl',result);ledger['decode_passes']+=1
  for d in datasets:
   family=d['system_group'];ss=d['configurations'];ids=[r['config_id'] for r in ss]
   c=SimpleNamespace(x=tuple(tuple(float(r[n]) for n in FEATURES[family]) for r in ss))
   reference=next(i for i,r in enumerate(ss) if all(r[k]==v for k,v in REFERENCES[family].items()))
   for seed in cfg['seeds']:
    check();key=f'{family}_{seed}'
    def journal(arm):
     def event(row):
      check();assert ledger['recorded_vector_acquisitions']<450
      ledger['recorded_vector_acquisitions']+=1
      append(OUT/'acquisitions.jsonl',{**row,'family':family,'seed':seed,'arm':arm,'at':now()});write(OUT/'ledger.json',ledger)
     return event
    source=ROOT/'results/v17_measurements/configuration_summary.csv'
    prefix=make_prefix(c,ids,reference,seed,RecordedOracle(source,family,ids,journal('prefix'),budget=10))
    write(OUT/'prefixes'/f'{key}.json',prefix)
    write(OUT/'prefix_seals'/f'{key}.json',{'sha256':sha(OUT/'prefixes'/f'{key}.json'),'at':now()})
    for method in ('joint_3nn','random'):
     oracle=RecordedOracle(source,family,ids,journal(method),budget=20,prefix=dict(zip(prefix['ids'],copy.deepcopy(prefix['labels']))))
     branch=continuation(c,prefix,oracle,method);write(OUT/method/f'{key}.json',branch)
    ledger['completed_cases']+=1;write(OUT/'ledger.json',ledger);print(key,'two completed arms',flush=True)
 except Exception as e:
  ledger['failure']=f'{type(e).__name__}: {e}';raise
 finally:
  ledger.update(finished_at=now(),stage_seconds=time.monotonic()-start);write(OUT/'ledger.json',ledger)
if __name__=='__main__':main()
