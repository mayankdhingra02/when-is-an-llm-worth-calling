"""Feature/incumbent manifest fixed before fresh validation outcomes."""
import sys,json,random
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'src'))
from escalation.numerical_v94 import candidates
from collect_smollm_v47 import sha,read,write,now
ARMS=['llm','batch_3nn','full_sequential_3nn'];SEEDS=[11,23,37,53,71]
def expected_jobs():
 jobs=[]
 for family in ['superlu','highs']:
  for seed in SEEDS:
   for arm in ARMS:
    path=f'results/v94_native/branches/{family}_{seed}_{arm}.json';s=read(ROOT/path)['state'];assert len(s['ids'])==len(set(s['ids']))==len(s['labels'])==20
    j=min(range(20),key=lambda i:s['labels'][i][0]);row=s['ids'][j]
    jobs.append(dict(key=f'{family}_{seed}_{arm}',family=family,seed=seed,arm=arm,row=row,configuration=list(candidates(family).x[row]),historical_label=s['labels'][j][0],historical_branch=path,historical_branch_sha256=sha(ROOT/path)))
 return jobs

def schedule(jobs):
 cases=[(f,s) for f in ['superlu','highs'] for s in SEEDS];result=[]
 for rep in range(3):
  order=list(range(10));random.Random(113000+rep).shuffle(order)
  for j in order:
   arms=ARMS.copy();random.Random(113100+10*rep+j).shuffle(arms)
   for a in arms:
    job=next(x for x in jobs if (x['family'],x['seed'],x['arm'])==(*cases[j],a))
    result.append(dict(**job,repeat=rep,request_key=job['key']+f'_validation_{rep}'))
 return result

def main():
 out=ROOT/'configs/validation_v113.json';assert not out.exists()
 jobs=expected_jobs();write(out,dict(jobs=jobs,schedule=schedule(jobs),intended_acquisitions=90,intended_physical_solves=270,stage_seconds=1800,worker_seconds=30,max_worker_rss_bytes=2*1024**3,penalty_seconds=30))
 print('Fixed30incumbents;90validationacquisitions;zero new LLM requests')
if __name__=='__main__':main()
