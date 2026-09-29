"""Feature-only GP-EI chooser with separate charged source oracle."""
import argparse,copy,csv,json,math,time,random
import numpy as np
from controllers_v154 import ROOT,read,write,sha,encode,gp
from hadoop_v148 import score_record
A=ROOT/'artifacts/study_v155';O=ROOT/'results/v155_gp'

def choose(raw,ids,labels,order,direction,length):
 if len(ids)!=len(labels) or len(set(ids))!=len(ids) or not 10<=len(ids)<20:raise ValueError('Invalid state/budget')
 if direction not in ['minimize','maximize']:raise ValueError('Invalid direction')
 x,cat=encode(raw);y=np.asarray(labels,float)
 if not np.isfinite(y).all() or min(y)<=0:raise ValueError('Invalid acquired outcomes')
 y=(y-y.mean())/(float(y.std()) if y.std()>1e-12 else 1.)
 available=[i for i in order if i not in ids]
 mean,sd=gp(x[ids],y,x[available],cat,length)
 delta=min(y)-mean if direction=='minimize' else mean-max(y);ei=[]
 for d,s in zip(delta,sd):
  z=d/s if s>1e-12 else 0.;ei.append(float(d*.5*math.erfc(-z/math.sqrt(2))+s*math.exp(-z*z/2)/math.sqrt(2*math.pi)) if s>1e-12 else max(float(d),0.))
 k=max(range(len(available)),key=lambda k:ei[k]);return int(available[k]),{'mean':float(mean[k]),'sd':float(sd[k]),'ei':ei[k],'acquired_count':len(ids)}

def append(path,event):
 with path.open('a') as f:f.write(json.dumps(event,allow_nan=False)+'\n')

def target(candidate,i):
 if 'spec' in candidate:
  spec=candidate['spec'];p=ROOT/spec['path'];assert sha(p)==spec['sha256'];lines=p.read_text().splitlines();header=next(csv.reader([lines[0]],delimiter=spec['delimiter']));line=candidate['source_ids'][i];row=dict(zip(header,next(csv.reader([lines[line-1]],delimiter=spec['delimiter']))));assert [float(row[k]) for k in candidate['names']]==candidate['x'][i];raw=row[spec['primary_objective']];value=float(raw);event={'source':spec['path'],'source_line':line,'raw_target':raw,'status':'completed'}
 elif 'source_lines' in candidate:
  p=ROOT/candidate['source_path'];assert sha(p)==candidate['source_sha256'];line=candidate['source_lines'][i];raw=next(csv.reader([p.read_text().splitlines()[line-1]]))[30];value=float(raw);event={'source':candidate['source_path'],'source_line':line,'raw_target':raw,'status':'completed'}
 else:
  path=candidate['sources'][i];assert sha(ROOT/path)==candidate['source_hashes'][i];r=read(ROOT/path);value,status=score_record(r,candidate['app']);event={'source':path,'source_sha256':candidate['source_hashes'][i],'raw_record':r,'status':status}
 if not math.isfinite(value) or value<=0:raise ValueError('Missing/nonpositive/nonfinite target')
 return value,event

class Oracle:
 def __init__(self,candidate,prefix_ids,key,ledger):self.c=candidate;self.seen=set(prefix_ids);self.key=key;self.ledger=ledger
 def acquire(self,i):
  if type(i)!=int or i in self.seen or not 0<=i<len(self.c['x']) or len(self.seen)>=20:raise ValueError('Duplicate/invalid/B20 acquisition')
  if self.ledger['attempts']>=1400:raise PermissionError('1400attemptcap')
  if time.monotonic()-self.ledger['started_monotonic']>=600:raise TimeoutError('600second cap')
  self.ledger['attempts']+=1;self.seen.add(i);write(O/'ledger.json',self.ledger);event={'key':self.key,'row_id':i,'at_unix':time.time(),'ordinal':self.ledger['attempts']}
  try:value,record=target(self.c,i);event.update(record,value=value)
  except Exception as e:event.update(status='invalid_source',error=repr(e),value=None);append(O/'acquisitions.jsonl',event);raise
  append(O/'acquisitions.jsonl',event);return value

def prepare():
 assert not (A/'freeze.json').exists();cases=read(ROOT/'artifacts/study_v154/prefix_inputs.json')['cases'];used={'scripts/gp_continuations_v155.py','scripts/controllers_v154.py','scripts/router_v147.py','scripts/hadoop_v148.py','tests/synthetic/test_gp_continuations_v155.py','reports/protocol_v155.md','artifacts/study_v154/prefix_inputs.json','artifacts/study_v151/inputs.json'};jobs=[]
 for c in cases:
  used.update([c['prefix'],c['candidate_path']]);candidate=read(ROOT/c['candidate_path']);p=read(ROOT/c['prefix']);state=p.get('state',p);assert c['ids']==state['ids'] and c['labels']==[y[0] for y in state['labels']]
  if 'spec' in candidate:used.add(candidate['spec']['path'])
  elif 'source_path' in candidate:used.add(candidate['source_path'])
  else:used.update(candidate['sources'])
  for length in [1.,.2]:jobs.append({'key':c['key']+'::gp_'+str(length),'case':c['key'],'lengthscale':length,'candidate_path':c['candidate_path'],'prefix':c['prefix']})
 random.Random(155000).shuffle(jobs);write(A/'jobs.json',jobs);used.add('artifacts/study_v155/jobs.json');write(A/'freeze.json',{'at_unix':time.time(),'sha256':{n:sha(ROOT/n) for n in sorted(used)}});print('Frozen140GPcontinuations/1400newattempts/600seconds; zeroLLMrequests')

def run():
 for n,h in read(A/'freeze.json')['sha256'].items():assert sha(ROOT/n)==h,n
 assert not O.exists();O.mkdir();(O/'arms').mkdir();cases={c['key']:c for c in read(ROOT/'artifacts/study_v154/prefix_inputs.json')['cases']};jobs=read(A/'jobs.json');start=time.monotonic();ledger={'attempts':0,'started_monotonic':start,'started_unix':time.time(),'cap':1400};write(O/'ledger.json',ledger);complete=failed=0;errors=[]
 try:
  for j in jobs:
   if time.monotonic()-start>=600:raise TimeoutError('Global600secondcap')
   c=cases[j['case']];p=read(ROOT/j['prefix']);s=copy.deepcopy(p.get('state',p));ids=s['ids'];labels=[v[0] for v in s['labels']];oracle=Oracle(read(ROOT/j['candidate_path']),ids,j['key'],ledger);status='complete';failure=None
   try:
    for step in range(10):
     i,diag=choose(c['raw_features'],ids,labels,s['order'],c['direction'],j['lengthscale']);append(O/'choices.jsonl',{'at_unix':time.time(),'key':j['key'],'step':step,'row_id':i,**diag});value=oracle.acquire(i);ids.append(i);labels.append(value)
   except (PermissionError,TimeoutError):raise
   except Exception as e:status='unscorable';failure=repr(e);failed+=1;errors.append({'key':j['key'],'error':failure})
   if status=='complete':complete+=1
   write(O/'arms'/(j['key']+'.json'),{**j,'status':status,'error':failure,'ids':ids,'labels':labels,'target':(min(labels) if c['direction']=='minimize' else max(labels)) if status=='complete' else None,'observed_incumbent':min(labels) if c['direction']=='minimize' else max(labels),'direction':c['direction'],'remaining_unattempted':20-len(oracle.seen)})
 except Exception as e:errors.append({'global_error':repr(e)})
 finally:write(O/'completion.json',{'intended_arms':140,'complete_arms':complete,'unscorable_arms':failed,'unstarted_or_interrupted_arms':140-complete-failed,'acquisition_attempts':ledger['attempts'],'wall_seconds':time.monotonic()-start,'errors':errors,'new_model_requests':0})
 print(json.dumps(read(O/'completion.json')))
if __name__=='__main__':
 ap=argparse.ArgumentParser();ap.add_argument('stage',choices=['prepare','run']);args=ap.parse_args();globals()[args.stage]()
