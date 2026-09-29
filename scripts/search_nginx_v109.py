"""One-seed B20 classical smoke with charged confirmation and paired prefixes."""
import sys,json,random,time,signal,statistics,socket
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'src'))
from nginx_domain_v108 import domain
from nginx_trial_v109 import run_trial
from escalation.core import State
from escalation.finite_domain import FiniteCandidates,recommend
from escalation.transfer_v41 import rank
from native_nginx_v105 import sha
ROWS=domain();NAMES=tuple(sorted(ROWS[0]))
C=FiniteCandidates(NAMES,tuple(tuple(r[k] for k in NAMES) for r in ROWS),('validated_http_batch_seconds',),('-',),tuple(range(len(ROWS))))
OUT=ROOT/'results/v109_classical'

def choose(c,state,mode,seed):
 available=[i for i in state.order if i not in state.ids]
 if mode=='sequential_3nn':return rank(c,state,available)[0]
 if mode=='prefix':return recommend(c,state)
 raise ValueError(mode)

def main():
 for n,h in json.loads((ROOT/'reports/protocol_v109.freeze.json').read_text())['sha256'].items():assert sha(ROOT/n)==h,n
 assert json.loads((ROOT/'results/v108_analysis/verification.json').read_text())['all_gates_pass']
 assert not OUT.exists();OUT.mkdir()
 with socket.socket() as s:s.bind(('127.0.0.1',18596))
 started=time.monotonic();records=[];states={};status='started';error=None
 order=list(range(len(ROWS)));random.Random(11).shuffle(order);prefix=State(order)
 def acquire(row,arm,phase,state):
  if len(records)>=40 or len(state.ids)+(0 if phase=='search' else 0)>20:raise RuntimeError('acquisition cap')
  if time.monotonic()-started>1700:raise TimeoutError('stage reserve')
  ident=f'{len(records):03d}_{arm}_{phase}'
  e={'id':ident,'row_id':row,'arm':arm,'phase':phase,'charged_native_configuration_attempt':True}
  with (OUT/'starts.jsonl').open('a') as f:f.write(json.dumps(e)+'\n')
  # Charge before work, including startup/transport/correctness failures.
  records.append(e);r=run_trial(OUT/'trials'/ident,ROWS[row]);e['result']=r
  with (OUT/'completed.jsonl').open('a') as f:f.write(json.dumps(e)+'\n')
  if r['status']!='valid':raise RuntimeError('native attempt invalid')
  return [r['measurement']['workload_seconds']]
 def alarm(_s,_f):raise TimeoutError('1800s stage cap')
 signal.signal(signal.SIGALRM,alarm);signal.alarm(1800)
 try:
  for _ in range(10):
   row=choose(C,prefix,'prefix',11);prefix.observe(row,acquire(row,'prefix','search',prefix),('-',))
  (OUT/'prefix.json').write_text(json.dumps({'seed':11,'system_group':'nginx','state':prefix.record(),'feature_names':NAMES},indent=2)+'\n')
  available=[i for i in order if i not in prefix.ids]
  batches={'batch_3nn':rank(C,prefix,available)[:7],'random':random.Random(10911).sample(available,7)}
  states={m:prefix.clone() for m in ['sequential_3nn','batch_3nn','random']}
  schedule=list(states);random.Random(109000).shuffle(schedule)
  (OUT/'schedule.json').write_text(json.dumps({'arm_order':schedule,'batches':batches},indent=2)+'\n')
  for step in range(7):
   for arm in schedule:
    state=states[arm];row=choose(C,state,arm,11) if arm=='sequential_3nn' else batches[arm][step]
    state.observe(row,acquire(row,arm,'search',state),('-',))
  incumbents={arm:state.ids[min(range(len(state.ids)),key=lambda j:state.labels[j][0])] for arm,state in states.items()}
  confirmations={arm:[] for arm in states}
  for repeat in range(3):
   for arm in schedule:confirmations[arm].append(acquire(incumbents[arm],arm,'confirmation',states[arm])[0])
  for arm,state in states.items():
   (OUT/f'{arm}.json').write_text(json.dumps({'state':state.record(),'incumbent_row_id':incumbents[arm],'confirmation_seconds':confirmations[arm],'primary_seconds':statistics.median(confirmations[arm]),'logical_evaluations':20,'unique_search_evaluations':17,'charged_confirmation_evaluations':3},indent=2)+'\n')
  status='complete'
 except Exception as exc:status='stopped';error=repr(exc)
 finally:
  signal.alarm(0)
  (OUT/'summary.json').write_text(json.dumps({'status':status,'error':error,'charged_native_configuration_attempts':len(records),'cases':records,'prefix':prefix.record(),'partial_states':{k:v.record() for k,v in states.items()},'stage_seconds':time.monotonic()-started,'new_model_requests':0},indent=2)+'\n')
 print(json.dumps({'status':status,'error':error,'attempts':len(records)}))
if __name__=='__main__':main()
