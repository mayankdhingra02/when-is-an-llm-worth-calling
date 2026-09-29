"""Independent scalar covariance/GP solve and policy/aggregate replay."""
import copy,hashlib,json,math
from pathlib import Path
import numpy as np
ROOT=Path(__file__).resolve().parents[1];A=ROOT/'artifacts/study_v154';O=ROOT/'results/v154_controllers'
def read(p):return json.loads(p.read_text())
def close(a,b):assert math.isclose(a,b,rel_tol=1e-7,abs_tol=1e-9),(a,b)
def matrix(raw):
 cols=[];cat=[]
 for values in zip(*raw):
  if len(set(values))<2:continue
  iscat=any(isinstance(x,str) for x in values);cat.append(iscat)
  if iscat:cols.append(list(values))
  else:
   lo,hi=min(values),max(values);cols.append([(x-lo)/(hi-lo) for x in values])
 return list(zip(*cols)),cat

def cov(a,b,cat,length):
 numeric=[(x-y)**2 for x,y,c in zip(a,b,cat) if not c];categorical=[int(x!=y) for x,y,c in zip(a,b,cat) if c]
 t=math.sqrt(5*sum(numeric)/len(numeric))/length if numeric else 0
 return (1+t+t*t/3)*math.exp(-t)*math.exp(-sum(categorical)/len(categorical) if categorical else 0)
def posterior(x,y,q,cat,length):
 k=np.array([[cov(a,b,cat,length) for b in x] for a in x])+1e-6*np.eye(len(x));cross=np.array([[cov(a,b,cat,length) for b in q] for a in x]);center=np.mean(y)
 pred=center+cross.T@np.linalg.lstsq(k,np.asarray(y)-center,rcond=None)[0]
 sd=np.sqrt(np.maximum(0,1-np.sum(cross*np.linalg.lstsq(k,cross,rcond=None)[0],axis=0)))
 return pred,sd

def verify_signals(cases,saved):
 for c in cases:
  x,cat=matrix(c['raw_features']);ids=c['ids'];y=c['labels'];assert len(set(ids))==len(y)==10
  best=[]
  for i in range(10):best.append((min if c['direction']=='minimize' else max)(y[:i+1]))
  imp=[abs(best[i]-best[i-1])/abs(best[i-1]) for i in range(4,10)];m=math.ceil(2*math.sqrt(len(cat)))
  for length in [1.,.2]:
   s=saved[c['key']][str(length)];monitor=sorted(np.random.default_rng(154000+c['seed']).choice(len(x),min(64,len(x)),replace=False).tolist());assert s['monitor_ids']==monitor and s['dimensions']==len(cat) and s['plateau_length']==m
   maximum=0
   for n,t in zip(range(4,11),s['uncertainty_trace']):
    _,sd=posterior([x[i] for i in ids[:n]],y[:n],[x[i] for i in monitor],cat,length);maximum=max(maximum,max(sd));close(t['mean_sd'],np.mean(sd));close(t['max_sd'],max(sd));close(t['running_max_sd'],maximum)
   ratio=np.mean(sd)/maximum;close(s['uncertainty_ratio'],ratio)
   for capped in [False,True]:
    mm=min(m,6) if capped else m;plateau=mm<=6 and all(v<.05 for v in imp[-mm:]);assert s['plateau_capped' if capped else 'plateau']==plateau
    action='a1' if not plateau or ratio<.3 else ('a2' if ratio>.5 else 'a3');assert s['bora_capped_action' if capped else 'bora_action']==action
   permutation=np.random.default_rng(154100+c['seed']).permutation(10);taus=[]
   for held,f in zip(np.array_split(permutation,5),s['rank_folds']):
    train=[i for i in range(10) if i not in held];assert f['train_positions']==train and f['held_positions']==held.tolist()
    pred,_=posterior([x[ids[i]] for i in train],[y[i] for i in train],[x[ids[i]] for i in held],cat,length)
    for a,b in zip(pred,f['predictions']):close(a,b)
    # Use authenticated stored prediction at exact floating-point ties.
    dy=y[held[1]]-y[held[0]];dp=f['predictions'][1]-f['predictions'][0];tau=None if dy==0 or dp==0 else (1. if dy*dp>0 else -1.)
    assert tau==f['tau'];taus.append(tau)
   tau=sum(t or 0 for t in taus)/5;p=1-max(.05,(tau+1)/2);close(p,s['p_llm']);close(tau,s['mean_tau']);assert s['undefined_folds']==sum(t is None for t in taus)
   u=int(hashlib.sha256(('154|'+c['key']).encode()).hexdigest()[:13],16)/16**13;assert s['uniform_draw']==u and s['rank_draw_call']==(u<p)

def verify_results(rows,sig,dec,folds,comparison,old):
 for grouping in ['ecosystem','engine']:
  rs=copy.deepcopy(rows)
  if grouping=='ecosystem':
   for r in rs:
    if r['group'] in ['spark','hadoop_mapreduce']:r['group']='spark_hadoop_ecosystem'
  for model in ['smollm3_3b','qwen3_8b']:
   data=[r for r in rs if r['model']==model];groups=sorted({r['group'] for r in data});by={r['key']:r for r in data}
   for fold in folds[grouping][model]:
    g=fold['held_group'];train=[r for r in data if r['group']!=g];test=[r for r in data if r['group']==g];assert fold['training_keys']==[r['key'] for r in train] and fold['held_keys']==[r['key'] for r in test];prior=next(f for f in old[grouping][model] if f['held_group']==g)
    for name,field in [('gp_uncertainty_calibrated','uncertainty_ratio'),('rank_calibrated','p_llm')]:
     cal=fold['calibrations'][name];grid=cal['grid'];tg=sorted({r['group'] for r in train})
     for entry in grid:
      t=entry['threshold'];chosen=[r for r in train if t is not None and sig[r['key']]['1.0'][field]>=t]
      gain=sum(sum(r['gain'] for r in chosen if r['group']==h)/sum(r['group']==h for r in train) for h in tg)/len(tg);rate=sum(sum(r['group']==h for r in chosen)/sum(r['group']==h for r in train) for h in tg)/len(tg);close(gain,entry['gain']);close(rate,entry['rate'])
     top=max(x['gain'] for x in grid);expected=min((x for x in grid if x['gain']>=top-1e-12),key=lambda x:(x['rate'],-math.inf if x['threshold'] is None else -x['threshold']));assert expected==cal['selected']
    for r in test:
     ds=dec[grouping][model][r['key']];assert ds['never']==0 and ds['always']==1
     for p,oldp in [('benefit_v151','selected_predictor'),('uncertainty_v151','uncertainty')]:assert ds[p]==float(prior['decisions'][r['key']][oldp])
     for length in ['1.0','0.2']:
      s=sig[r['key']][length];assert ds['bora_'+length]==float(s['bora_action']!='a1') and ds['bora_capped_'+length]==float(s['bora_capped_action']!='a1');assert ds['rank_expected_'+length]==s['p_llm'] and ds['rank_draw_'+length]==float(s['uniform_draw']<s['p_llm'])
     for p,field in [('gp_uncertainty_calibrated','uncertainty_ratio'),('rank_calibrated','p_llm')]:
      t=fold['calibrations'][p]['selected']['threshold'];assert ds[p]==float(t is not None and sig[r['key']]['1.0'][field]>=t)
   for p,out in comparison['models'][grouping][model].items():
    gains=[];random=[];adaptive=[];calls=useful=harm=joint=miss=0.
    for g in groups:
     group=[r for r in data if r['group']==g];prob=[dec[grouping][model][r['key']][p] for r in group];gains.append(sum(v*r['gain'] for v,r in zip(prob,group))/len(group));random.append(sum(prob)/len(group)*sum(r['gain'] for r in group)/len(group));ad=[]
     for v,r in zip(prob,group):
      sign=1 if r['direction']=='minimize' else -1;ad.append(v*r['adaptive_gain']+(1-v)*sign*(r['adaptive']-r['sequential'])/r['adaptive']);calls+=v;useful+=v*(r['gain']>.01);harm+=v*(r['gain']<-.01);joint+=v*(r['gain']>.01 and r['adaptive_gain']>.01);miss+=(1-v)*(r['gain']>.01)
     adaptive.append(sum(ad)/len(ad))
    for key,value in [('family_mean_gain',np.mean(gains)),('family_mean_gain_vs_adaptive',np.mean(adaptive)),('above_matched_random',np.mean(np.array(gains)-random)),('calls',calls),('useful',useful),('harmful',harm),('joint_useful',joint),('missed',miss)]:close(value,out[key])

def main():
 for n,h in read(A/'freeze.json')['sha256'].items():assert hashlib.sha256((ROOT/n).read_bytes()).hexdigest()==h,n
 cases=read(A/'prefix_inputs.json')['cases'];sig=read(A/'signals.json');rows=read(ROOT/'artifacts/study_v151/inputs.json')['rows'];dec=read(O/'decisions.json');folds=read(O/'folds.json');comp=read(O/'comparison.json');old=read(ROOT/'results/v151_router/folds.json')
 verify_signals(cases,sig);verify_results(rows,sig,dec,folds,comp,old);mutations=[]
 for name in ['probability','decision','gain']:
  ss=copy.deepcopy(sig);dd=copy.deepcopy(dec);cc=copy.deepcopy(comp)
  if name=='probability':ss[cases[0]['key']]['1.0']['p_llm']+=.1
  elif name=='decision':dd['ecosystem']['smollm3_3b'][rows[-1]['key']]['always']=0
  else:cc['models']['ecosystem']['smollm3_3b']['always']['family_mean_gain']+=.1
  try:
   if name=='probability':verify_signals(cases[:1],ss)
   else:verify_results(rows,ss,dd,folds,cc,old)
  except AssertionError:mutations.append({'name':name,'rejected':True})
  else:raise AssertionError('Undetected '+name)
 receipt={'verified':True,'prefixes':70,'kernel_variants':2,'real_historical_model_cases':140,'mutations':mutations,'scope':'independent scalar mixed covariance, least-squares posterior, probabilities, memberships, threshold utility/selection, decisions and aggregate quality; no new acquisitions/inference'}
 (A/'replay.json').write_text(json.dumps(receipt,indent=2)+'\n');print(json.dumps(receipt))
if __name__=='__main__':main()
