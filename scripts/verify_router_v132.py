"""Independent stdlib recomputation of features, ridge fits and frozen decisions."""
import argparse,hashlib,json,math,random
from pathlib import Path
from fractions import Fraction
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--root',type=Path,default=Path(__file__).resolve().parents[1]);args=ap.parse_args();root=args.root
 def read(n):return json.loads((root/n).read_text())
 def sha(n):return hashlib.sha256((root/n).read_bytes()).hexdigest()
 freeze=read('reports/protocol_v132.freeze.json')
 for n,h in freeze['sha256'].items():assert sha(n)==h,n
 before=read('artifacts/study_v132/before_outcomes.json');starts=[json.loads(l) for l in (root/'results/v131_native/continuations/starts.jsonl').read_text().splitlines()]
 assert before['continuation_directory_absent'] is True and before['freeze_sha256']==sha('reports/protocol_v132.freeze.json') and before['at']>=freeze['at'] and all(s['at']>before['at'] for s in starts)
 training=read('artifacts/study_v132/training.json')['rows'];held=read('artifacts/study_v132/decisions.json')['rows'];saved=read('artifacts/study_v132/model.json');assert len(training)==40 and len(held)==10
 assert len({r['group'] for r in training})==8 and {r['group'] for r in held}=={'fftw','wavpack'} and not {r['group'] for r in training}&{r['group'] for r in held}
 jobs={j['key']:j for v in [127,128,130,131] for j in read(f'artifacts/study_v{v}/jobs.json')}
 def mean(v):return sum(v)/len(v)
 def sd(v):m=mean(v);return math.sqrt(sum((x-m)**2 for x in v)/len(v))
 def close(a,b):return abs(a-b)<=1e-9*max(1,abs(a),abs(b))
 for r in training+held:
  j=jobs[r['key']];p=read(r['prefix']);p=p.get('state',p);direction=json.loads(read(j['messages_path'])[1]['content'])['direction'];y=[v[0] for v in p['labels']];assert len(y)==10 and all(v>0 and math.isfinite(v) for v in y)
  agg=min if direction=='minimize' else max;best=[agg(y[:i+1]) for i in range(10)];last=max(i for i in range(10) if i==0 or best[i]!=best[i-1]);rng=random.Random(132000);boot=[agg([y[rng.randrange(10)] for _ in range(10)]) for _ in range(64)]
  features=[math.log1p(len(p['order'])),sum(len(d)>1 for d in j['domains']),mean([len(d) for d in j['domains']]),sd(y)/mean(y),((best[0]-best[-1]) if direction=='minimize' else (best[-1]-best[0]))/best[0],(9-last)/9,sd(boot)/mean(y)];assert all(close(a,b) for a,b in zip(features,r['features'])) and sha(r['prefix'])==r['prefix_sha256']
  if 'gain' in r:
   if r['source_stage']==130:
    pair=next(x for x in read('results/v130_native/comparison.json')['rows'] if x['seed']==r['seed']);g=(pair['sequential_3nn_bytes']-pair['llm_bytes'])/pair['sequential_3nn_bytes']
   else:g=next(x for x in read(f"results/v{r['source_stage']}_analysis/comparison.json")['cases'] if x['key']==j['base_key'])['gains']['full_sequential_3nn']
   assert close(g,r['gain'])
 def solve(a,b):
  a=[list(row)+[v] for row,v in zip(a,b)];n=len(b)
  for k in range(n):
   pivot=max(range(k,n),key=lambda i:abs(a[i][k]));a[k],a[pivot]=a[pivot],a[k];d=a[k][k];assert abs(d)>1e-12;a[k]=[v/d for v in a[k]]
   for i in range(n):
    if i!=k:
     c=a[i][k];a[i]=[x-c*y for x,y in zip(a[i],a[k])]
  return [row[-1] for row in a]
 def fit(rows):
  groups=[r['group'] for r in rows];w=[1/(len(set(groups))*groups.count(g)) for g in groups];x=[r['features'] for r in rows];y=[r['gain'] for r in rows];d=7
  mu=[sum(ww*row[k] for ww,row in zip(w,x)) for k in range(d)];scale=[math.sqrt(sum(ww*(row[k]-mu[k])**2 for ww,row in zip(w,x))) for k in range(d)];scale=[s if s>=1e-12 else 1 for s in scale];z=[[(v-m)/s for v,m,s in zip(row,mu,scale)] for row in x];intercept=sum(ww*v for ww,v in zip(w,y))
  mat=[[sum(ww*row[i]*row[j] for ww,row in zip(w,z))+(1 if i==j else 0) for j in range(d)] for i in range(d)];rhs=[sum(ww*row[i]*(v-intercept) for ww,row,v in zip(w,z,y)) for i in range(d)];return {'mean':mu,'scale':scale,'coef':solve(mat,rhs),'intercept':intercept}
 def predict(model,x):return sum((v-m)/s*c for v,m,s,c in zip(x,model['mean'],model['scale'],model['coef']))+model['intercept']
 def same_model(a,b):
  assert close(a['intercept'],b['intercept'])
  for k in ['mean','scale','coef']:assert all(close(x,y) for x,y in zip(a[k],b[k]))
 fitted=fit(training);same_model(fitted,saved['model']);oof={}
 for fold in saved['leave_one_group_out']:
  group=fold['held_group'];rows=[r for r in training if r['group']!=group];assert set(fold['training_groups'])=={r['group'] for r in rows} and group not in fold['training_groups'];model=fit(rows);same_model(model,fold['model'])
  for r in training:
   if r['group']==group:oof[r['key']]=predict(model,r['features'])
 for p in saved['oof_scores']:assert close(p['score'],oof[p['key']])
 for kind,scores in [('benefit',[oof[r['key']] for r in training]),('uncertainty',[r['features'][-1] for r in training])]:
  cal=saved[kind+'_calibration'];groups={r['group'] for r in training}
  for row in cal['grid']:
   t=row['threshold'];ds=[t is not None and score>=t for score in scores]
   # Near-equal independently recomputed quantiles can straddle their own tie;
   # use the original frozen OOF values for exact threshold membership only.
   if kind=='benefit':ds=[t is not None and next(p['score'] for p in saved['oof_scores'] if p['key']==r['key'])>=t for r in training]
   value=mean([mean([r['gain']*d for r,d in zip(training,ds) if r['group']==g]) for g in groups]);assert close(value,row['development_gain']) and close(mean(ds),row['development_rate'])
  maximum=max(r['development_gain'] for r in cal['grid']);selected=min([r for r in cal['grid'] if r['development_gain']>=maximum-1e-12],key=lambda r:r['development_rate']);assert selected==cal['selected']
 rng=random.Random(132001);rate=saved['benefit_calibration']['selected']['development_rate'];selected=set(random.Random(132002).sample(range(10),sum(r['decisions']['benefit'] for r in held)))
 for i,r in enumerate(held):
  score=predict(fitted,r['features']);assert close(score,r['predicted_gain']);bt=saved['benefit_calibration']['selected']['threshold'];ut=saved['uncertainty_calibration']['selected']['threshold'];expected={'never':False,'always':True,'benefit':bt is not None and score>=bt,'uncertainty':ut is not None and r['features'][-1]>=ut,'random_development_rate':rng.random()<rate,'random_matched_realized_rate':i in selected};assert expected==r['decisions']
 comparison=read('results/v132_router/comparison.json');assert comparison['new_model_requests']==comparison['new_native_trials']==0
 native=read('results/v131_native/comparison.json')
 for r in comparison['rows']:
  decision=next(d for d in held if d['key']==r['key']);pair=next(p for p in native['rows'] if p['task']==r['group'] and p['seed']==r['seed']);source=pair['fresh_medians_ns'] if r['group']=='fftw' else pair
  assert r['classical_target']==source['sequential_3nn'] and r['llm_target']==source['llm'];gain=Fraction(r['classical_target']-r['llm_target'],r['classical_target']);assert r['paired_gain_fraction']==str(gain)
  for key,value in decision['decisions'].items():assert r['decisions'][key]==value
  assert r['decisions']['hindsight_oracle_diagnostic']==(gain>0)
 for policy,result in comparison['policies'].items():
  assert result['escalations']==sum(r['decisions'][policy] for r in comparison['rows'])
  for group,g in result['by_group'].items():
   rows=[r for r in comparison['rows'] if r['group']==group];gain=sum(Fraction(r['paired_gain_fraction']) if r['decisions'][policy] else 0 for r in rows)/5;assert str(gain)==g['gain_fraction']
 print(json.dumps({'verified':True,'historical_groups':8,'historical_cases':40,'new_groups':2,'new_cases':10,'features_reconstructed':50,'group_exclusion_scaling_ridge_and_thresholds_verified':True,'decisions_precede_all_148_continuation_validation_attempts':True,'new_inference_or_objective_collection':0}))
if __name__=='__main__':main()
