"""Replay completed OR stopped classical stages without dropping intended runs."""
import json,random,statistics,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'src'))
from escalation.core import State
from escalation.finite_domain import FiniteCandidates,recommend
from escalation.transfer_v41 import rank
from nginx_domain_v108 import domain
from native_nginx_v105 import sha
class Stopped(Exception):pass

def verify(root=ROOT):
 for n,h in json.loads((root/'reports/protocol_v111.freeze.json').read_text())['sha256'].items():assert sha(root/n)==h,n
 out=root/'results/v111_classical';d=json.loads((out/'summary.json').read_text());rows=domain();names=tuple(sorted(rows[0]));c=FiniteCandidates(names,tuple(tuple(r[k] for k in names) for r in rows),('seconds',),('-',),tuple(range(len(rows))))
 starts=[json.loads(s) for s in (out/'starts.jsonl').read_text().splitlines()];completed=[json.loads(s) for s in (out/'completed.jsonl').read_text().splitlines()]
 assert len(starts)==len(d['cases'])==d['charged_native_configuration_attempts']<=40 and d['cases']==completed
 assert starts==[{k:v for k,v in e.items() if k!='result'} for e in completed]
 valid=[];all_counts=0
 for e in completed:
  folder=out/'trials'/e['id'];r=e['result'];m=r.get('measurement',{})
  assert r==json.loads((folder/'result.json').read_text()) and r['configuration']==rows[e['row_id']]
  assert sha(folder/'nginx.conf')==r['config_sha256'] and sha(folder/'www/payload.bin')==r['payload_sha256']
  assert r['server_returncode']==0 and r['owned_process_group_absent']
  receipts=json.loads((folder/'clients.json').read_text());assert receipts['clients']==m['clients'] and receipts['workload_seconds']==m['workload_seconds']
  assert len(m['clients'])==4;cpu=sent=count=0
  for j,ch in enumerate(m['clients']):
   a=ch['measurement'];assert ch['index']==j and ch['owned_process_group_absent'] and a==json.loads((folder/f'client_{j}.stdout').read_text())
   assert len(a['per_connection_valid'])==4 and all(0<=n<=65536 for n in a['per_connection_valid'])
   assert sum(a['per_connection_valid'])==a['responses_byte_valid']<=a['requests_sent']<=262144
   assert abs(a['client_cpu_to_wall']-a['client_cpu_seconds']/a['workload_seconds'])<1e-7
   assert 0<=ch['launch_offset_seconds']<m['workload_seconds'];cpu+=a['client_cpu_seconds'];sent+=a['requests_sent'];count+=a['responses_byte_valid']
   if r['status']=='valid':assert ch['returncode']==0 and a['valid'] and a['requests_sent']==a['responses_byte_valid']==262144
   else:assert ch['returncode']!=0 and not a['valid'] and a['error']=='timeout' and a['workload_seconds']>=60
  assert abs(m['client_cpu_seconds']-cpu)<1e-8 and abs(m['client_cpu_to_wall']-cpu/m['workload_seconds'])<1e-8
  assert m['requests_sent']==sent and m['responses_byte_valid']==count;all_counts+=count
  assert m['valid']==(r['status']=='valid')
  if r['status']=='valid':valid.append(e)
 order=list(range(768));random.Random(11).shuffle(order);prefix=State(order);cursor=0;states={};confirm={};best={}
 def take(row,arm,phase):
  nonlocal cursor
  assert cursor<len(completed)
  e=completed[cursor];assert (e['row_id'],e['arm'],e['phase'])==(row,arm,phase);cursor+=1
  if e['result']['status']!='valid':raise Stopped()
  return [e['result']['measurement']['workload_seconds']]
 try:
  for _ in range(10):
   row=recommend(c,prefix);prefix.observe(row,take(row,'prefix','search'),('-',))
  assert prefix.record()==json.loads((out/'prefix.json').read_text())['state']
  available=[i for i in order if i not in prefix.ids]
  batches={'batch_3nn':rank(c,prefix,available)[:7],'random':random.Random(10911).sample(available,7)}
  states={a:prefix.clone() for a in ['sequential_3nn','batch_3nn','random']};schedule=list(states);random.Random(109000).shuffle(schedule)
  assert json.loads((out/'schedule.json').read_text())==dict(arm_order=schedule,batches=batches)
  for step in range(7):
   for a in schedule:
    s=states[a];row=rank(c,s,[i for i in s.order if i not in s.ids])[0] if a=='sequential_3nn' else batches[a][step]
    s.observe(row,take(row,a,'search'),('-',))
  best={a:s.ids[min(range(17),key=lambda j:s.labels[j][0])] for a,s in states.items()};confirm={a:[] for a in states}
  for _ in range(3):
   for a in schedule:confirm[a].append(take(best[a],a,'confirmation')[0])
  assert d['status']=='complete' and cursor==40
 except Stopped:
  assert d['status']=='stopped' and completed[-1]['result']['status']=='failed'
 assert cursor==len(completed) and d['prefix']==prefix.record() and d['partial_states']=={a:s.record() for a,s in states.items()}
 arms={}
 if d['status']=='complete':
  for a,s in states.items():
   saved=json.loads((out/f'{a}.json').read_text());assert saved['state']==s.record() and saved['confirmation_seconds']==confirm[a]
   assert saved['logical_evaluations']==len(s.ids)+len(confirm[a])==20 and saved['incumbent_row_id']==best[a]
   assert saved['primary_seconds']==statistics.median(confirm[a])
   arms[a]={'confirmation_median_seconds':saved['primary_seconds'],'confirmation_relative_range':(max(confirm[a])-min(confirm[a]))/statistics.mean(confirm[a]),'logical_evaluations':20}
 quality={'valid_attempts_shorter_than_two_seconds':sum(e['result']['measurement']['workload_seconds']<2 for e in valid),'individual_clients_cpu_wall_above_0_8':sum(ch['measurement']['client_cpu_to_wall']>.8 for e in completed for ch in e['result']['measurement']['clients'])}
 gates={'correctness_completion':len(valid)==40,'duration':len(valid)==40 and quality['valid_attempts_shorter_than_two_seconds']==0,'client_headroom':len(valid)==40 and quality['individual_clients_cpu_wall_above_0_8']==0,'confirmation_repeatability':len(arms)==3 and all(a['confirmation_relative_range']<=.1 for a in arms.values())}
 return dict(verified=True,status=d['status'],intended_attempts=40,native_attempts=len(completed),valid_attempts=len(valid),failed_attempts=len(completed)-len(valid),unattempted=40-len(completed),validated_responses=all_counts,arms=arms,timing_diagnostics=quality,gates=gates,all_gates_passed=all(gates.values()),new_objectives_on_replay=0,new_model_requests=0,lifecycle_seconds=d['stage_seconds'],failure_cases=[{'id':e['id'],'row_id':e['row_id'],'error':e['result'].get('error')} for e in completed if e['result']['status']!='valid'])
def main():
 result=verify();(ROOT/'artifacts/study_v111/verification.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result))
if __name__=='__main__':main()
