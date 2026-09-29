"""Independent replay of choices, branch isolation, budget and native receipts."""
import json,random,statistics,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'src'))
from escalation.core import State
from escalation.finite_domain import FiniteCandidates,recommend
from escalation.transfer_v41 import rank
from nginx_domain_v108 import domain
from native_nginx_v105 import sha
OUT=ROOT/'results/v109_classical'
def main():
 for n,h in json.loads((ROOT/'reports/protocol_v109.freeze.json').read_text())['sha256'].items():assert sha(ROOT/n)==h,n
 d=json.loads((OUT/'summary.json').read_text());rows=domain();names=tuple(sorted(rows[0]));c=FiniteCandidates(names,tuple(tuple(r[k] for k in names) for r in rows),('seconds',),('-',),tuple(range(len(rows))))
 starts=[json.loads(s) for s in (OUT/'starts.jsonl').read_text().splitlines()]
 completed=[json.loads(s) for s in (OUT/'completed.jsonl').read_text().splitlines()]
 assert len(starts)==len(d['cases'])==d['charged_native_configuration_attempts']<=40
 for e in completed:
  folder=OUT/'trials'/e['id'];r=e['result'];m=r.get('measurement',{})
  assert r==json.loads((folder/'result.json').read_text())
  assert r['configuration']==rows[e['row_id']]
  assert sha(folder/'nginx.conf')==r['config_sha256']
  assert sha(folder/'www/payload.bin')==r['payload_sha256']
  if r['status']=='valid':
   assert json.loads((folder/'client.stdout').read_text())==m
   assert m['valid'] and m['responses_byte_valid']==m['requests_sent']==131072 and m['per_connection_valid']==[8192]*16
   assert r['server_returncode']==r['client_returncode']==0 and r['owned_process_group_absent']
 order=list(range(len(rows)));random.Random(11).shuffle(order);prefix=State(order);cursor=0
 def take(row,arm,phase):
  nonlocal cursor
  e=completed[cursor];assert e['row_id']==row and e['arm']==arm and e['phase']==phase;cursor+=1
  return [e['result']['measurement']['workload_seconds']]
 assert d['status']=='complete','Partial trial preserved; complete replay not applicable'
 for _ in range(10):
  row=recommend(c,prefix);prefix.observe(row,take(row,'prefix','search'),('-',))
 assert prefix.record()==json.loads((OUT/'prefix.json').read_text())['state']
 available=[i for i in order if i not in prefix.ids]
 batches={'batch_3nn':rank(c,prefix,available)[:7],'random':random.Random(10911).sample(available,7)}
 states={a:prefix.clone() for a in ['sequential_3nn','batch_3nn','random']};schedule=list(states);random.Random(109000).shuffle(schedule)
 for step in range(7):
  for a in schedule:
   state=states[a];row=rank(c,state,[i for i in state.order if i not in state.ids])[0] if a=='sequential_3nn' else batches[a][step]
   state.observe(row,take(row,a,'search'),('-',))
 best={a:s.ids[min(range(17),key=lambda j:s.labels[j][0])] for a,s in states.items()};confirm={a:[] for a in states}
 for _ in range(3):
  for a in schedule:confirm[a].append(take(best[a],a,'confirmation')[0])
 assert cursor==40 and len(completed)==40
 arms={}
 for a,s in states.items():
  saved=json.loads((OUT/f'{a}.json').read_text());assert saved['state']==s.record() and saved['confirmation_seconds']==confirm[a]
  assert saved['logical_evaluations']==len(s.ids)+len(confirm[a])==20 and saved['incumbent_row_id']==best[a]
  assert saved['primary_seconds']==statistics.median(confirm[a])
  arms[a]={'confirmation_median_seconds':saved['primary_seconds'],'confirmation_relative_range':(max(confirm[a])-min(confirm[a]))/statistics.mean(confirm[a]),'logical_evaluations':20}
 quality={'shorter_than_two_seconds':sum(e['result']['measurement']['workload_seconds']<2 for e in completed),'client_cpu_wall_above_0_8':sum(e['result']['measurement']['client_cpu_to_wall']>.8 for e in completed)}
 result={'verified':True,'native_attempts':40,'validated_responses':40*131072,'arms':arms,'timing_diagnostics':quality,'new_objectives_on_replay':0,'new_model_requests':0}
 (ROOT/'artifacts/study_v109/verification.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result))
if __name__=='__main__':main()
