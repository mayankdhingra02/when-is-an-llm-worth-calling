"""Six bounded, predeclared multiprocess load feasibility attempts."""
import json,signal,socket,time
from pathlib import Path
from nginx_trial_v110 import run_trial
from native_nginx_v105 import sha
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'results/v110_nginx'
def main():
 for n,h in json.loads((ROOT/'reports/protocol_v110.freeze.json').read_text())['sha256'].items():assert sha(ROOT/n)==h,n
 cfg=json.loads((ROOT/'configs/nginx_feasibility_v110.json').read_text());domain=json.loads((ROOT/'configs/nginx_domain_v108.json').read_text())['rows']
 assert not OUT.exists();OUT.mkdir()
 with socket.socket() as s:s.bind(('127.0.0.1',18596))
 cases=[dict(index=i,row_id=r,status='unattempted') for i,r in enumerate(cfg['cases'])]
 started=time.monotonic()
 def alarm(_s,_f):raise TimeoutError('stage limit')
 signal.signal(signal.SIGALRM,alarm);signal.alarm(cfg['stage_seconds'])
 try:
  for i,row in enumerate(cfg['cases']):
   if i and cases[i-1]['status']!='valid':break
   with (OUT/'starts.jsonl').open('a') as f:f.write(json.dumps({'index':i,'row_id':row,'charged_native_configuration_attempt':True})+'\n')
   result=run_trial(OUT/f'{i:02d}',domain[row]);cases[i]=dict(index=i,row_id=row,**result)
   print(json.dumps({'index':i,'row':row,'status':result['status'],'seconds':result.get('measurement',{}).get('workload_seconds')}),flush=True)
 finally:
  signal.alarm(0)
  attempts=len((OUT/'starts.jsonl').read_text().splitlines()) if (OUT/'starts.jsonl').exists() else 0
  (OUT/'summary.json').write_text(json.dumps(dict(cases=cases,charged_native_configuration_attempts=attempts,lifecycle_seconds=time.monotonic()-started,new_model_requests=0),indent=2)+'\n')
if __name__=='__main__':main()
