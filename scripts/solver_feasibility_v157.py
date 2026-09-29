"""Create-once feasibility collection; writes a charged intent before every child."""
import argparse,hashlib,itertools,json,random,subprocess,time,datetime,statistics
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];ART=ROOT/'artifacts/study_v157';OUT=ROOT/'results/v157_solvers';PYTHON=ROOT/'.venv-solvers156/bin/python'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def write(p,v):p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(v,indent=2,allow_nan=False)+'\n')
def candidates():
 domains={'cvc5':{'decision':['internal','justification'],'simplification':['batch','none'],'arith-prop':['both','bi','unate','none'],'arith-static-learning':[True,False],'arith-rewrite-equalities':[False,True]},'ortools':{'search_branching':[0,2],'cp_model_presolve':[True,False],'linearization_level':[0,2],'symmetry_level':[0,2],'cp_model_probing_level':[0,2],'use_sat_inprocessing':[True,False]}}
 return {e:[dict(zip(d,v)) for v in itertools.product(*d.values())] for e,d in domains.items()}
def prepare():
 assert not (ART/'freeze.json').exists();cs=candidates();write(ART/'candidates.json',cs)
 jobs=[{'engine':e,'candidate_id':i,'repeat':r,'config':cs[e][i],'n':32,'limit':10} for r in range(5) for e in cs for i in [0,21,42,63]];random.Random(157).shuffle(jobs);write(ART/'jobs.json',jobs)
 files=['reports/protocol_v157.md','scripts/solver_worker_v157.py','scripts/solver_feasibility_v157.py','tests/synthetic/test_solver_v157.py','configs/solvers_v156.lock.txt','artifacts/study_v157/jobs.json','artifacts/study_v157/candidates.json','artifacts/study_v156/runtime_options.json']
 write(ART/'freeze.json',{'at':datetime.datetime.now(datetime.timezone.utc).isoformat(),'sha256':{f:sha(ROOT/f) for f in files},'jobs':40,'max_stage_seconds':600,'max_child_seconds':15,'native_evaluation_cap':40})
def collect():
 f=json.loads((ART/'freeze.json').read_text())
 for n,h in f['sha256'].items():assert sha(ROOT/n)==h,n
 assert not OUT.exists();OUT.mkdir(parents=True);start=time.monotonic();done=[];error=None
 try:
  for k,j in enumerate(json.loads((ART/'jobs.json').read_text())):
   if time.monotonic()-start>585:raise TimeoutError('stage cap; remaining jobs unattempted')
   with (OUT/'intents.jsonl').open('a') as o:o.write(json.dumps({'charge':k+1,'job':j,'at':datetime.datetime.now(datetime.timezone.utc).isoformat()})+'\n')
   cmd=[str(PYTHON),str(ROOT/'scripts/solver_worker_v157.py'),'--engine',j['engine'],'--config',json.dumps(j['config']),'--n',str(j['n']),'--limit',str(j['limit'])];t=time.monotonic();row={'charge':k+1,'job':j,'result':None,'error':None}
   try:
    p=subprocess.run(cmd,cwd=ROOT,capture_output=True,text=True,timeout=15);row.update(returncode=p.returncode,stdout=p.stdout,stderr=p.stderr)
    if p.returncode:row['error']='worker failed'
    else:row['result']=json.loads(p.stdout)
   except subprocess.TimeoutExpired as e:row['error']='external timeout';row['stdout']=str(e.stdout);row['stderr']=str(e.stderr)
   row['collection_seconds']=time.monotonic()-t;done.append(row);write(OUT/f'{k+1:03d}.json',row);print(k+1,j['engine'],j['candidate_id'],row['result']['status'] if row['result'] else row['error'],flush=True)
 except Exception as e:error=repr(e)
 finally:write(OUT/'completion.json',{'intended':40,'charged':len(done),'unattempted':40-len(done),'seconds':time.monotonic()-start,'error':error})
 if error:raise RuntimeError(error)
def summarize():
 rows=[json.loads(p.read_text()) for p in sorted(OUT.glob('[0-9][0-9][0-9].json'))];s={}
 for e in candidates():
  cells=[]
  for i in [0,21,42,63]:
   rr=[r for r in rows if r['job']['engine']==e and r['job']['candidate_id']==i];v=[r['result']['solve_seconds'] for r in rr if r['result'] and r['result']['correct']];med=statistics.median(v) if v else None;mad=statistics.median([abs(x-med) for x in v])/med if v else None
   cells.append({'candidate_id':i,'charged':len(rr),'correct':len(v),'median_solve_seconds':med,'relative_mad':mad,'pass':len(v)==5 and med>=.01 and mad<=.05})
  s[e]={'cells':cells,'admitted':all(x['pass'] for x in cells)}
 write(OUT/'summary.json',s);print(json.dumps(s,indent=2))
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('mode',choices=['prepare','collect','summarize']);a=p.parse_args();{'prepare':prepare,'collect':collect,'summarize':summarize}[a.mode]()
