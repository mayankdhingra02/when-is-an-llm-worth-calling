"""New acquired-only classical runs on separately sealed API/CLI median tables."""
import copy,csv,hashlib,json,math,sys,time
from pathlib import Path
from types import SimpleNamespace
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'src'))
from escalation.offline_live_v16 import FEATURES,REFERENCES,make_prefix,continuation
from analyze_utility_v50 import choose
OUT=ROOT/'results/v51_classical'
def read(p):return json.loads(Path(p).read_text())
def write(p,v):Path(p).parent.mkdir(parents=True,exist_ok=True);Path(p).write_text(json.dumps(v,indent=2)+'\n')
class Oracle:
 def __init__(self,path,ids,journal,budget=20,prefix=None):self.path=path;self.ids=ids;self.journal=journal;self.budget=budget;self.acquired=copy.deepcopy(prefix or {})
 def acquire(self,i):
  assert type(i)==int and 0<=i<len(self.ids) and i not in self.acquired and len(self.acquired)<self.budget
  self.acquired[i]=None;self.journal({'row_id':i,'config_id':self.ids[i],'charged_recorded_vector':1})
  with self.path.open() as stream:
   for row in csv.DictReader(stream):
    if row['config_id']==self.ids[i]:
     assert row['successful_trials']=='5';label=[float(row['median_compression_ms']),float(row['compressed_bytes'])];assert all(math.isfinite(x) and x>0 for x in label)
     self.acquired[i]=label;return label.copy()
  raise ValueError('Missing acquired vector')
def main():
 assert not OUT.exists(),'Preserve replay'
 for p,h in read(ROOT/'results/v51_analysis/table_seal.json')['sha256'].items():assert hashlib.sha256((ROOT/p).read_bytes()).hexdigest()==h
 datasets=[d for d in read(ROOT/'results/v50_utility/feature_manifest.json')['datasets'] if d['system_group'] in ('zstd','lz4')]
 start=time.monotonic();OUT.mkdir();ledger={'recorded_vectors':0,'completed_cases':0,'model_requests':0,'new_physical_trials':0};cases=[]
 try:
  for mode in ('api','cli'):
   for d in datasets:
    f=d['system_group'];rows=d['configurations'];ids=[r['config_id'] for r in rows];c=SimpleNamespace(x=tuple(tuple(float(r[n]) for n in FEATURES[f]) for r in rows));ref=next(i for i,r in enumerate(rows) if all(r[k]==v for k,v in REFERENCES[f].items()));source=ROOT/f'results/v51_analysis/{mode}/configuration_summary.csv'
    for seed in (11,23,37,53,71):
     key=f'{mode}_{f}_{seed}'
     def journal(arm):
      def event(row):
       assert time.monotonic()-start<30 and ledger['recorded_vectors']<600
       ledger['recorded_vectors']+=1
       with (OUT/'acquisitions.jsonl').open('a') as stream:stream.write(json.dumps({**row,'mode':mode,'family':f,'seed':seed,'arm':arm})+'\n')
       write(OUT/'ledger.json',ledger)
      return event
     prefix=make_prefix(c,ids,ref,seed,Oracle(source,ids,journal('prefix'),10));write(OUT/'prefixes'/f'{key}.json',prefix)
     branches={}
     for method in ('joint_3nn','random'):
      arm=continuation(c,prefix,Oracle(source,ids,journal(method),20,dict(zip(prefix['ids'],prefix['labels']))),method);write(OUT/method/f'{key}.json',arm);branches[method]=arm
     ledger['completed_cases']+=1
  assert ledger['recorded_vectors']==600 and ledger['completed_cases']==20
  # Evaluator-only full tables: after ALL optimizer collection.
  for mode in ('api','cli'):
   data={r['config_id']:[float(r['median_compression_ms']),float(r['compressed_bytes'])] for r in csv.DictReader((ROOT/f'results/v51_analysis/{mode}/configuration_summary.csv').open())}
   for d in datasets:
    f=d['system_group'];rows=d['configurations'];ys=[data[r['config_id']] for r in rows];xs=[[r[n] for n in FEATURES[f]] for r in rows]
    for seed in (11,23,37,53,71):
     key=f'{mode}_{f}_{seed}';p=read(OUT/'prefixes'/f'{key}.json');ids=p['ids'][:4];labels=[ys[i] for i in ids]
     while len(ids)<10:
      i=choose(xs,p['order'],ids,labels,p['size_cap'],'joint_3nn');ids.append(i);labels.append(ys[i])
     assert ids==p['ids'] and labels==p['labels']
     arms={}
     for method in ('joint_3nn','random'):
      arm=read(OUT/method/f'{key}.json');ii=ids.copy();yy=copy.deepcopy(labels)
      while len(ii)<20:
       i=choose(xs,p['order'],ii,yy,p['size_cap'],method);ii.append(i);yy.append(ys[i])
      assert ii==arm['ids'] and yy==arm['labels'] and len(set(ii))==20
      assert arm['best_feasible_ms']==min(ys[i][0] for i in ii if ys[i][1]<=p['size_cap']);arms[method]=arm
     best=min(y[0] for y in ys if y[1]<=p['size_cap']);cheap=arms['joint_3nn']['best_feasible_ms'];rand=arms['random']['best_feasible_ms']
     cases.append({'mode':mode,'family':f,'seed':seed,'size_cap':p['size_cap'],'classical_ms':cheap,'random_ms':rand,'classical_gain_over_random':(rand-cheap)/rand,'hindsight_ms':best,'hindsight_headroom':(cheap-best)/cheap})
  write(OUT/'cases.json',cases)
 finally:
  ledger['stage_seconds']=time.monotonic()-start;write(OUT/'ledger.json',ledger)
 print(json.dumps({'ledger':ledger,'cases':cases},indent=2))
if __name__=='__main__':main()
