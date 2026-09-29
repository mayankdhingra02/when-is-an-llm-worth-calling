"""Outcome-blind new-family decisions from historical development groups only."""
import json,math,random
import numpy as np
from collect_smollm_v47 import ROOT,read,write,sha,now
A=ROOT/'artifacts/study_v132'
FEATURES=['log_candidate_count','variable_feature_count','mean_domain_cardinality','label_cv','prefix_relative_progress','plateau_fraction','bootstrap_best_dispersion']
def features(s,ds,direction):
 y=np.asarray([v[0] for v in s['labels']],float)
 if len(y)!=10 or len(s['ids'])!=10 or not np.isfinite(y).all() or np.min(y)<=0:raise ValueError('Invalid prefix')
 best=np.minimum.accumulate(y) if direction=='minimize' else np.maximum.accumulate(y)
 progress=(best[0]-best[-1])/best[0] if direction=='minimize' else (best[-1]-best[0])/best[0]
 last=max(i for i in range(10) if i==0 or best[i]!=best[i-1]);rng=random.Random(132000)
 samples=[[y[rng.randrange(10)] for _ in range(10)] for _ in range(64)];extrema=[min(v) if direction=='minimize' else max(v) for v in samples]
 return [math.log1p(len(s['order'])),sum(len(d)>1 for d in ds),float(np.mean([len(d) for d in ds])),float(np.std(y)/np.mean(y)),float(progress),(9-last)/9,float(np.std(extrema)/np.mean(y))]
def fit(rows):
 x=np.array([r['features'] for r in rows]);y=np.array([r['gain'] for r in rows]);groups=[r['group'] for r in rows]
 w=np.array([1/groups.count(g) for g in groups]);w/=w.sum();mean=np.sum(w[:,None]*x,axis=0);scale=np.sqrt(np.sum(w[:,None]*(x-mean)**2,axis=0));scale[scale<1e-12]=1
 z=(x-mean)/scale;intercept=float(w@y);coef=np.linalg.solve(z.T@(w[:,None]*z)+np.eye(x.shape[1]),z.T@(w*(y-intercept)))
 return {'mean':mean.tolist(),'scale':scale.tolist(),'coef':coef.tolist(),'intercept':intercept,'ridge_alpha':1.0}
def predict(model,features):return float(((np.asarray(features)-model['mean'])/model['scale'])@model['coef']+model['intercept'])
def select_threshold(scores,rows):
 # Group means first; all thresholds derive from development scores only.
 thresholds=sorted(set([0.0]+[float(np.quantile(scores,q)) for q in [0,.25,.5,.75,1]]))+[None]
 groups=sorted({r['group'] for r in rows});out=[]
 for threshold in thresholds:
  decisions=[threshold is not None and s>=threshold for s in scores]
  gain=float(np.mean([np.mean([r['gain']*d for r,d in zip(rows,decisions) if r['group']==g]) for g in groups]));rate=float(np.mean(decisions))
  out.append({'threshold':threshold,'development_gain':gain,'development_rate':rate})
 maximum=max(o['development_gain'] for o in out);best=min([o for o in out if o['development_gain']>=maximum-1e-12],key=lambda o:o['development_rate'])
 return {'selected':best,'grid':out}
def decide(score,threshold):return threshold is not None and score>=threshold
def main():
 A.mkdir(exist_ok=False)
 assert not (ROOT/'results/v131_native/continuations').exists(),'Must freeze before any V131 LLM continuation/validation outcome'
 inputs=set();
 def load(n):inputs.add(n);return read(ROOT/n)
 def row(job,gain=None):
  path=job.get('prefix_path',job.get('prefix'));p=load(path);s=p.get('state',p);body=json.loads(load(job['messages_path'])[1]['content']);assert sha(ROOT/path)==job['prefix_sha256']
  out={'key':job['key'],'group':job['system_group'],'seed':job.get('seed',int(job['key'].split('_')[-2])) if 'seed' not in job else job['seed'],'features':features(s,job['domains'],body['direction']),'prefix':path,'prefix_sha256':sha(ROOT/path)}
  if gain is not None:out['gain']=gain
  return out
 training=[]
 for version,jobs_version in [(127,127),(129,128)]:
  comparisons=load(f'results/v{version}_analysis/comparison.json')['cases'];targets={c['key']:c for c in comparisons}
  for j in load(f'artifacts/study_v{jobs_version}/jobs.json'):
   if j['condition']!='normal' or j['system_group']=='sac':continue
   if j['base_key'] not in targets:raise ValueError('Missing historical paired outcome')
   r=row(j,targets[j['base_key']]['gains']['full_sequential_3nn']);r['source_stage']=version;training.append(r)
 old=load('results/v130_native/comparison.json')
 for j in load('artifacts/study_v130/jobs.json'):
  paired=next(r for r in old['rows'] if r['seed']==j['seed']);r=row(j,(paired['sequential_3nn_bytes']-paired['llm_bytes'])/paired['sequential_3nn_bytes']);r['source_stage']=130;training.append(r)
 assert len(training)==40 and len({r['group'] for r in training})==8
 predictions=[];folds=[]
 for group in sorted({r['group'] for r in training}):
  train=[r for r in training if r['group']!=group];model=fit(train);held=[r for r in training if r['group']==group];assert not {r['group'] for r in train}&{group}
  folds.append({'held_group':group,'training_groups':sorted({r['group'] for r in train}),'model':model})
  predictions.extend({'key':r['key'],'score':predict(model,r['features'])} for r in held)
 scores=[next(p['score'] for p in predictions if p['key']==r['key']) for r in training]
 calibration=select_threshold(scores,training);uncertainty=select_threshold([r['features'][-1] for r in training],training);model=fit(training)
 test=[row(j) for j in load('artifacts/study_v131/jobs.json')];assert len(test)==10 and {r['group'] for r in test}=={'wavpack','fftw'} and not {r['group'] for r in test}&{r['group'] for r in training}
 # Decisions use only prefix-derived features and the saved development model.
 rate=calibration['selected']['development_rate'];rng=random.Random(132001)
 for r in test:
  score=predict(model,r['features']);r.update(predicted_gain=score,decisions={'never':False,'always':True,'benefit':decide(score,calibration['selected']['threshold']),'uncertainty':decide(r['features'][-1],uncertainty['selected']['threshold']),'random_development_rate':rng.random()<rate})
 chosen=set(random.Random(132002).sample(range(len(test)),sum(r['decisions']['benefit'] for r in test)))
 for i,r in enumerate(test):r['decisions']['random_matched_realized_rate']=i in chosen
 write(A/'training.json',{'feature_names':FEATURES,'rows':training,'groups':8,'excluded':'V127 SAC output contract structurally incompatible with current guard; five failures excluded from fitting only, historical denominator/cost preserved; no V131 outcomes read'})
 write(A/'model.json',{'model':model,'leave_one_group_out':folds,'oof_scores':predictions,'benefit_calibration':calibration,'uncertainty_calibration':uncertainty})
 write(A/'decisions.json',{'at':now(),'outcome_blind_guard':'V131continuations directory absent at decision creation','rows':test})
 inputs.update(['scripts/router_v132.py','reports/protocol_v132.md','tests/synthetic/test_router_v132.py','scripts/collect_smollm_v47.py','artifacts/study_v132/training.json','artifacts/study_v132/model.json','artifacts/study_v132/decisions.json'])
 write(ROOT/'reports/protocol_v132.freeze.json',{'at':now(),'scope':'Historical groups only; decisions frozen before new LLM continuation/fresh validation acquisition','sha256':{n:sha(ROOT/n) for n in sorted(inputs)}})
 print(json.dumps({'training_groups':8,'training_cases':40,'test_groups':2,'test_cases':10,'benefit_calibration':calibration['selected'],'uncertainty_calibration':uncertainty['selected'],'test_calls':{p:sum(r['decisions'][p] for r in test) for p in test[0]['decisions']},'freeze_sha256':sha(ROOT/'reports/protocol_v132.freeze.json')}))
if __name__=='__main__':main()
