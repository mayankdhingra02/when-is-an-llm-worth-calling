"""Missing-label amendment; preserve V144 originals and consume unused allowance."""
import json,time,random,sys
from pathlib import Path
from collect_smollm_v47 import ROOT,read,write,append,sha,now
from spark_v144 import A,TASKS,SEEDS,CONTROLS,CAT,distance,project,messages,load_features
O=ROOT/'results/v145_spark'

def choose(c,s,mode,anchor=None):
 from spark_v144 import choose as original
 if len(s['ids'])>=20:raise ValueError('Budget exhausted')
 valid=[k for k,y in enumerate(s['labels']) if y[0] is not None]
 # Failed/missing acquisitions remain spent and excluded from candidates, but
 # never become invented training values. A valid B10 prefix always exists.
 filtered={'ids':[s['ids'][k] for k in valid],'labels':[s['labels'][k] for k in valid],'order':[i for i in s['order'] if i not in s['ids'] or i in [s['ids'][k] for k in valid]]}
 return original(c,filtered,mode,anchor)

def check_freeze():
 for n,h in read(ROOT/'reports/protocol_v145.freeze.json')['sha256'].items():
  if sha(ROOT/n)!=h:raise ValueError('Changed frozen input: '+n)

class Oracle:
 def __init__(self,c,key,state):
  self.c=c;self.key=key;self.seen=set(state['ids']);self.lines=(ROOT/c['source_path']).read_text().splitlines()
  if sha(ROOT/c['source_path'])!=c['source_sha256']:raise ValueError('Changed source')
 def acquire(self,i):
  import csv,math
  if type(i)!=int or not 0<=i<len(self.c['x']) or i in self.seen or len(self.seen)>=20:raise ValueError('Invalid/duplicate/over-budget')
  ledger=read(O/'ledger.json');cfg=read(ROOT/'configs/study_v145.json')
  if ledger['acquisitions']>=2000 or time.time()-ledger['collection_started_unix']>=1800:raise PermissionError('Original allowance exhausted')
  ledger['acquisitions']+=1;write(O/'ledger.json',ledger);self.seen.add(i);raw=next(csv.reader([self.lines[self.c['source_lines'][i]-1]]))[30];event={'at_unix':time.time(),'key':self.key,'row_id':i,'source_line':self.c['source_lines'][i],'raw_target':raw}
  if not raw.strip():event.update(value=None,error='missing_source_target');append(O/'acquisitions.jsonl',event);return [None]
  try:
   value=float(raw)
   if not math.isfinite(value) or value<=0:raise ValueError('Nonpositive/nonfinite target')
  except Exception as e:event['error']=repr(e);append(O/'acquisitions.jsonl',event);raise
  event['value']=value;append(O/'acquisitions.jsonl',event);return [value]

def best(s):return min(y[0] for y in s['labels'] if y[0] is not None)
def initialize():
 import shutil
 check_freeze();O.mkdir(exist_ok=False)
 for n in ['ledger.json','acquisitions.jsonl']:shutil.copyfile(ROOT/'results/v144_spark'/n,O/n)
 shutil.copytree(ROOT/'results/v144_spark/classical',O/'classical')
 write(O/'import.json',{'at':now(),'history_only_not_new_collection':True,'sha256':{str(p.relative_to(ROOT)):sha(p) for p in [ROOT/'results/v144_spark/ledger.json',ROOT/'results/v144_spark/acquisitions.jsonl']+list((ROOT/'results/v144_spark/classical').glob('*.json'))}})

def classical():
 check_freeze();events=[json.loads(line) for line in (O/'acquisitions.jsonl').read_text().splitlines()];t=time.monotonic()
 for job in read(A/'jobs.json'):
  c=read(A/'candidates'/f"{job['app']}.json");p=read(ROOT/job['prefix']);anchor=p['ids'][min(range(10),key=lambda k:p['labels'][k][0])]
  for mode in CONTROLS:
   key=job['key']+'_'+mode;dest=O/'classical'/(key+'.json')
   if dest.exists():continue
   start=time.monotonic();s=json.loads(json.dumps(p));previous=[e for e in events if e['key']==key]
   for e in previous:s['ids'].append(e['row_id']);s['labels'].append([e.get('value')])
   o=Oracle(c,key,s);diag=[]
   if mode=='random_proposal':
    rng=random.Random(144200+job['seed']);ids,diag=project(c,p,[[rng.choice(d) for d in c['grid_domains']] for _ in range(10)])
   for step in range(len(previous),10):
    i=ids[step] if mode=='random_proposal' else choose(c,s,mode,anchor);s['ids'].append(i);s['labels'].append(o.acquire(i))
   write(dest,{'key':key,'case':job['key'],'mode':mode,'state':s,'target':best(s),'projection':diag,'seconds':time.monotonic()-start,'missing_acquisitions':sum(y[0] is None for y in s['labels']),'imported_partial_acquisitions':len(previous)})
 write(O/'classical_summary.json',{'at_unix':time.time(),'arms':125,'total_classical_acquisitions':1250,'new_in_amendment':read(O/'ledger.json')['acquisitions']-1036,'seconds_amendment':time.monotonic()-t,'complete':True});print('All125 intended classical arms complete; missing labels retained')

def evaluate():
 check_freeze();dest=O/'models';dest.mkdir(exist_ok=False);choices=[];started={r['identity'] for r in map(json.loads,(ROOT/'results/v144_models/smollm3_3b/generation_starts.jsonl').read_text().splitlines())}
 for model in read(ROOT/'configs/study_v145.json')['model_order']:
  for j in read(A/'jobs.json'):
   c=read(A/'candidates'/f"{j['app']}.json");p=read(ROOT/j['prefix']);v='v144' if model=='smollm3_3b' and j['key'] in started else 'v145';scorepath=ROOT/'results'/f'{v}_models'/model/'scores'/f"{j['key']}.json";score=read(scorepath) if scorepath.exists() else {'status':'interrupted' if v=='v144' else 'unattempted'}
   ids,diag=project(c,p,score['score']) if score['status']=='valid' else ([],[]);choices.append({**j,'model':model,'status':score['status'],'score_path':str(scorepath.relative_to(ROOT)),'selected_rows':ids,'projection':diag})
 write(O/'choices.json',choices);write(O/'selection_seal.json',{'at_unix':time.time(),'choices_sha256':sha(O/'choices.json')})
 for j in choices:
  c=read(A/'candidates'/f"{j['app']}.json");p=read(ROOT/j['prefix']);s=json.loads(json.dumps(p));key=j['model']+'_'+j['key'];o=Oracle(c,key,p)
  for step in range(10):
   i=j['selected_rows'][step] if j['status']=='valid' else choose(c,s,'sequential_3nn');s['ids'].append(i);s['labels'].append(o.acquire(i))
  write(dest/(key+'.json'),{**j,'key':key,'case':j['key'],'state':s,'target':best(s),'missing_acquisitions':sum(y[0] is None for y in s['labels']),'fallback':j['status']!='valid'})
 write(O/'completion.json',{'at_unix':time.time(),'model_arms':50,'total_acquisitions':read(O/'ledger.json')['acquisitions'],'total_collection_seconds':time.time()-read(O/'ledger.json')['collection_started_unix']});print('All50 model/fallback B20arms;2000charged outcomes including missing')
if __name__=='__main__':
 import argparse
 p=argparse.ArgumentParser();p.add_argument('stage',choices=['initialize','classical','evaluate']);a=p.parse_args();globals()[a.stage]()
