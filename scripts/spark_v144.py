"""Fixed-domain Spark adaptation. Feature loader never converts objective cells."""
import csv,json,math,random,time
from pathlib import Path
from collect_smollm_v47 import ROOT,read,write,sha,now,append
A=ROOT/'artifacts/study_v144'; O=ROOT/'results/v144_spark'
CAT={4,9,16,19,25,26,27,28,29}
TASKS=[('bayes','bayes_samples_30params.csv','bigdata'),('pagerank','pagerank_samples_30params.csv','huge'),('terasort','terasort_samples_30params.csv','ds1'),('tpch','tpch_30params_samples.csv','20'),('wordcount','wc_samples_30params.csv','bigdata')]
SEEDS=[11,23,37,53,71]
CONTROLS=['sequential_3nn','adaptive_neighbor','fixed_neighbor','random_full','random_proposal']
def load_features(path,app,size):
 names=None;xs=[];lines=[];excluded=[];ignored_trailing_cells=0
 with Path(path).open() as f:
  r=csv.reader(f);header=next(r)
  if len(header)<34 or header[30:34]!=['exec_time','App','App_id','input_size']:raise ValueError('Unknown source schema')
  names=header[:30]
  for line,row in enumerate(r,2):
   if len(row)<34:raise ValueError('Short row')
   if (row[31],row[33])!=(app,size):excluded.append(line);continue
   x=tuple(v.strip() if j in CAT else float(v) for j,v in enumerate(row[:30]))
   if not all(math.isfinite(v) for j,v in enumerate(x) if j not in CAT):raise ValueError('Invalid numeric feature')
   ignored_trailing_cells+=sum(bool(v) for v in row[34:])
   xs.append(x);lines.append(line)
 if len(xs)<40 or len(set(xs))!=len(xs):raise ValueError('Insufficient distinct fixed-workload settings')
 domains=[sorted({x[j] for x in xs}) for j in range(30)]
 normalized=[[domains[j].index(v) if j in CAT else (v-domains[j][0])/(domains[j][-1]-domains[j][0]) if len(domains[j])>1 else 0 for j,v in enumerate(x)] for x in xs]
 grid=[list(range(len(d))) if j in CAT else list(range(10)) if len(d)>1 else [0] for j,d in enumerate(domains)]
 return {'ignored_unlabelled_trailing_nonempty_cells':ignored_trailing_cells,'names':names,'raw_features':xs,'x':normalized,'source_lines':lines,'domains':domains,'grid_domains':grid,'excluded_other_context_lines':excluded,'source_path':str(Path(path).relative_to(ROOT)),'source_sha256':sha(path),'app':app,'input_size':size,'system_group':'spark'}
def distance(a,b):return sum(float(x!=y) if j in CAT else abs(x-y) for j,(x,y) in enumerate(zip(a,b)))/30

def choose(c,s,mode,anchor=None):
 if len(s['ids'])!=len(s['labels']) or len(set(s['ids']))!=len(s['ids']) or not 0<=len(s['ids'])<20:raise ValueError('Invalid state/budget')
 available=[i for i in s['order'] if i not in s['ids']]
 if len(s['ids'])<4 or mode=='random_full':return available[0]
 if mode in ['adaptive_neighbor','fixed_neighbor']:
  best=anchor if mode=='fixed_neighbor' else s['ids'][min(range(len(s['ids'])),key=lambda k:s['labels'][k][0])]
  return min(available,key=lambda i:distance(c['x'][i],c['x'][best]))
 if mode!='sequential_3nn':raise ValueError('Unknown control')
 def estimate(i):
  k=sorted(range(len(s['ids'])),key=lambda k:(distance(c['x'][i],c['x'][s['ids'][k]]),k))[:3]
  return sum(s['labels'][j][0] for j in k)/len(k)
 return min(available,key=estimate)

def project(c,s,proposals):
 if len(proposals)!=10:raise ValueError('Expected ten proposals')
 seen=set(s['ids']);ids=[];diag=[];prior=[]
 for p in proposals:
  if len(p)!=30 or any(v not in d for v,d in zip(p,c['grid_domains'])):raise ValueError('Bad prototype')
  x=[v if j in CAT else v/9 for j,v in enumerate(p)]
  i=min((i for i in s['order'] if i not in seen),key=lambda i:distance(x,c['x'][i]));ids.append(i);seen.add(i)
  diag.append({'row_id':i,'distance':distance(x,c['x'][i]),'repeated_proposal':list(p) in prior,'matches_prefix':any(distance(x,c['x'][k])==0 for k in s['ids'])});prior.append(list(p))
 return ids,diag

def messages(c,s):
 body={'feature_order':c['names'],'encoding':'Numeric coordinates in [0,1] use feature-table min/max. Propose digits 0..9 meaning 0/9..9/9; categorical digits are indices in categorical_values. Observations use normalized numeric coordinates and categorical indices. Projection uses mean absolute numeric distance plus categorical mismatch.','categorical_values':{str(j):c['domains'][j] for j in sorted(CAT)},'numeric_bounds':{str(j):[d[0],d[-1]] for j,d in enumerate(c['domains']) if j not in CAT},'observed_examples':[{'settings':[round(v,5) for v in c['x'][i]],'performance':y[0]} for i,y in zip(s['ids'],s['labels'])],'direction':'minimize','performance_meaning':'Recorded Spark workload execution duration in original source units; same application, input and cluster within this task.'}
 return [{'role':'system','content':'Optimize software configurations from ten acquired measurements. Propose ten diverse promising settings. Output only a JSON array of ten 30-digit strings in feature_order. Numeric digits specify equally spaced positions between feature minimum and maximum. Categorical digits specify their value index. Proposals project to unobserved recorded configurations. Infer settings from performance; avoid duplicate proposals.'},{'role':'user','content':json.dumps(body,separators=(',',':'))}]

class Oracle:
 def __init__(self,c,key,prefix=None):
  self.c=c;self.key=key;self.seen=set(prefix['ids'] if prefix else []);self.lines=(ROOT/c['source_path']).read_text().splitlines()
  if sha(ROOT/c['source_path'])!=c['source_sha256']:raise ValueError('Source changed')
 def acquire(self,i):
  if type(i)!=int or not 0<=i<len(self.c['x']) or i in self.seen or len(self.seen)>=20:raise ValueError('Duplicate/over-budget acquisition')
  ledger=read(O/'ledger.json');cfg=read(ROOT/'configs/study_v144.json')
  if ledger['acquisitions']>=cfg['total_new_recorded_acquisitions']:raise PermissionError('Global acquisition cap')
  if time.time()-ledger['collection_started_unix']>=cfg['total_collection_seconds_cap']:raise TimeoutError('Global collection cap')
  ledger['acquisitions']+=1;write(O/'ledger.json',ledger);self.seen.add(i)
  raw=next(csv.reader([self.lines[self.c['source_lines'][i]-1]]))[30]
  try:
   value=float(raw)
   if not math.isfinite(value) or value<=0:raise ValueError('Nonpositive/nonfinite duration')
  except Exception as e:
   append(O/'acquisitions.jsonl',{'at_unix':time.time(),'key':self.key,'row_id':i,'source_line':self.c['source_lines'][i],'raw_target':raw,'error':repr(e)});raise
  append(O/'acquisitions.jsonl',{'at_unix':time.time(),'key':self.key,'row_id':i,'source_line':self.c['source_lines'][i],'raw_target':raw,'value':value});return [value]

def check_freeze():
 for n,h in read(ROOT/'reports/protocol_v144.freeze.json')['sha256'].items():
  if sha(ROOT/n)!=h:raise ValueError('Changed frozen input: '+n)

def prepare():
 if (ROOT/'reports/protocol_v144.freeze.json').exists():raise FileExistsError('Frozen candidates')
 for app,file,size in TASKS:
  c=load_features(ROOT/'artifacts/sources/v143/tuneful/experiment/aws-4nodes'/file,app,size);write(A/'candidates'/f'{app}.json',c)
 print('Prepared five feature-only pools;',sum(len(read(p)['x']) for p in (A/'candidates').glob('*.json')),'rows; zero target values parsed')

def prefixes():
 from router_v132 import features,predict,decide
 check_freeze();O.mkdir(exist_ok=False);write(O/'ledger.json',{'collection_started_unix':time.time(),'at':now(),'acquisitions':0});(O/'acquisitions.jsonl').touch();jobs=[];frozen=read(ROOT/'artifacts/study_v132/model.json');decisions=[]
 for app,_,_ in TASKS:
  c=read(A/'candidates'/f'{app}.json')
  for seed in SEEDS:
   key=f'{app}_{seed}';order=list(range(len(c['x'])));random.Random(seed).shuffle(order);s={'ids':[],'labels':[],'order':order};o=Oracle(c,key+'_prefix')
   for _ in range(10):
    i=choose(c,s,'sequential_3nn');s['ids'].append(i);s['labels'].append(o.acquire(i))
   p=A/'prefixes'/f'{key}.json';write(p,s);m=A/'prompts'/f'{key}.json';write(m,messages(c,s));f=features(s,c['domains'],'minimize');score=predict(frozen['model'],f);decisions.append({'key':key,'features':f,'score':score,'benefit':decide(score,frozen['benefit_calibration']['selected']['threshold']),'uncertainty':decide(f[-1],frozen['uncertainty_calibration']['selected']['threshold'])})
   jobs.append({'key':key,'app':app,'seed':seed,'system_group':'spark','domains':c['grid_domains'],'sampling_seed':144000+seed,'prefix':str(p.relative_to(ROOT)),'prefix_sha256':sha(p),'messages_path':str(m.relative_to(ROOT))})
 selected=set(random.Random(144001).sample(range(len(decisions)),sum(d['benefit'] for d in decisions)))
 for k,d in enumerate(decisions):d['random_matched_rate']=k in selected
 write(A/'decisions.json',{'at_unix':time.time(),'source_model':'artifacts/study_v132/model.json','scope':'Frozen Qwen-trained transport diagnostic, also applied unchanged to SmolLM; no calibration claim','rows':decisions});random.Random(144100).shuffle(jobs);write(A/'jobs.json',jobs)
 paths=[p for folder in ['prefixes','prompts','candidates'] for p in (A/folder).glob('*.json')]+[A/'jobs.json',A/'decisions.json',A/'models.json'];write(A/'inputs.freeze.json',{'at_unix':time.time(),'sha256':{str(p.relative_to(ROOT)):sha(p) for p in paths}})
 print('250 prefix acquisitions;25 prefixes; decisions sealed before continuations')

def classical():
 check_freeze();dest=O/'classical';dest.mkdir(exist_ok=False);t=time.monotonic()
 for job in read(A/'jobs.json'):
  c=read(A/'candidates'/f"{job['app']}.json");p=read(ROOT/job['prefix']);anchor=p['ids'][min(range(10),key=lambda k:p['labels'][k][0])]
  for mode in CONTROLS:
   start=time.monotonic();s=json.loads(json.dumps(p));key=job['key']+'_'+mode;o=Oracle(c,key,p);diag=[]
   if mode=='random_proposal':
    rng=random.Random(144200+job['seed']);proposals=[[rng.choice(d) for d in c['grid_domains']] for _ in range(10)];ids,diag=project(c,p,proposals)
   for step in range(10):
    i=ids[step] if mode=='random_proposal' else choose(c,s,mode,anchor);s['ids'].append(i);s['labels'].append(o.acquire(i))
   write(dest/(key+'.json'),{'key':key,'case':job['key'],'mode':mode,'state':s,'target':min(y[0] for y in s['labels']),'projection':diag,'seconds':time.monotonic()-start})
 write(O/'classical_summary.json',{'at_unix':time.time(),'arms':125,'new_acquisitions':1250,'seconds':time.monotonic()-t});print('125 classical B20 arms;1250 new acquisitions')

def evaluate():
 check_freeze();dest=O/'models';dest.mkdir(exist_ok=False);choices=[]
 for model in read(ROOT/'configs/study_v144.json')['model_order']:
  for j in read(A/'jobs.json'):
   c=read(A/'candidates'/f"{j['app']}.json");p=read(ROOT/j['prefix']);scorepath=ROOT/'results/v144_models'/model/'scores'/f"{j['key']}.json";score=read(scorepath) if scorepath.exists() else {'status':'unattempted'}
   ids,diag=project(c,p,score['score']) if score['status']=='valid' else ([],[])
   choice={**j,'model':model,'status':score['status'],'selected_rows':ids,'projection':diag};choices.append(choice)
 write(O/'choices.json',choices);write(O/'selection_seal.json',{'at_unix':time.time(),'choices_sha256':sha(O/'choices.json')})
 for j in choices:
  c=read(A/'candidates'/f"{j['app']}.json");p=read(ROOT/j['prefix']);s=json.loads(json.dumps(p));key=j['model']+'_'+j['key'];o=Oracle(c,key,p)
  for step in range(10):
   i=j['selected_rows'][step] if j['status']=='valid' else choose(c,s,'sequential_3nn');s['ids'].append(i);s['labels'].append(o.acquire(i))
  write(dest/(key+'.json'),{**j,'key':key,'case':j['key'],'state':s,'target':min(y[0] for y in s['labels']),'fallback':j['status']!='valid'})
 write(O/'completion.json',{'at_unix':time.time(),'model_arms':50,'total_acquisitions':read(O/'ledger.json')['acquisitions'],'total_collection_seconds':time.time()-read(O/'ledger.json')['collection_started_unix']});print('50 model continuations;500 new acquisitions')
if __name__=='__main__':
 import argparse
 p=argparse.ArgumentParser();p.add_argument('stage',choices=['prepare','prefixes','classical','evaluate']);a=p.parse_args();globals()[a.stage]()
