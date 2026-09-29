"""Independent algebra, membership, threshold and aggregate audit; no fitting changes."""
import copy,json,math,statistics
import numpy as np
from router_v149 import ROOT,ART,OUT,read,sha,write,KINDS,MODELS

def close(a,b):assert math.isclose(float(a),float(b),rel_tol=1e-8,abs_tol=1e-10),(a,b)
def wts(rs):
 counts={g:sum(r['group']==g for r in rs) for g in {r['group'] for r in rs}}
 return np.array([1/(len(counts)*counts[r['group']]) for r in rs])
def score_model(m,rs,held):
 assert m['training_keys']==[r['key'] for r in rs]
 assert m['training_groups']==sorted({r['group'] for r in rs})
 d=len(m['mean']);x=np.array([r['features'][:d] for r in rs]);y=np.array([r['gain'] for r in rs]);w=wts(rs);mu=np.average(x,axis=0,weights=w);sd=np.sqrt(np.average((x-mu)**2,axis=0,weights=w));sd[sd<1e-12]=1
 np.testing.assert_allclose(m['mean'],mu,atol=1e-10);np.testing.assert_allclose(m['scale'],sd,atol=1e-10)
 z=(x-mu)/sd;b=float(w@y);close(m['intercept'],b);zz=np.array([r['features'][:d] for r in held]);zz=(zz-mu)/sd
 if m['kind'].startswith('ridge'):
  coef=np.linalg.lstsq(np.vstack([np.sqrt(w)[:,None]*z,np.eye(d)]),np.r_[np.sqrt(w)*(y-b),np.zeros(d)],rcond=None)[0]
  np.testing.assert_allclose(m['coef'],coef,atol=1e-9);return zz@coef+b
 if m['kind']=='rbf_extended':
  k=np.array([[math.exp(-float(np.mean((a-c)**2))/2) for c in z] for a in z]);sw=np.sqrt(w)
  dual=sw*np.linalg.lstsq(sw[:,None]*k*sw[None,:]+.1*np.eye(len(rs)),sw*(y-b),rcond=None)[0]
  np.testing.assert_allclose(m['dual'],dual,atol=1e-9);np.testing.assert_allclose(m['training_z'],z,atol=1e-10)
  return np.array([sum(math.exp(-float(np.mean((a-c)**2))/2)*v for c,v in zip(z,dual))+b for a in zz])
 def check(node,ids,depth):
  value=float(np.average(y[ids],weights=w[ids]));close(node['value'],value);assert node['n']==len(ids);assert node['groups']==sorted({rs[i]['group'] for i in ids})
  parent=float(np.sum(w[ids]*(y[ids]-value)**2));options=[]
  if depth<2:
   for j in range(d):
    for t in sorted(set(np.quantile(z[ids,j],[.25,.5,.75]))):
     aa=[ids[z[ids,j]<=t],ids[z[ids,j]>t]]
     if min(map(len,aa))<5 or min(len({rs[i]['group'] for i in a}) for a in aa)<2:continue
     loss=sum(float(np.sum(w[a]*(y[a]-np.average(y[a],weights=w[a]))**2)) for a in aa)
     if loss<parent-1e-12:options.append((loss,j,t,aa))
  if 'feature' not in node:assert not options;return
  assert options
  best=options[0]
  for option in options[1:]:
   if option[0]<best[0]-1e-12:best=option
  _,j,t,aa=best;assert node['feature']==j;close(node['threshold'],t);check(node['left'],aa[0],depth+1);check(node['right'],aa[1],depth+1)
 check(m['tree'],np.arange(len(rs)),0)
 values=[]
 for x in zz:
  node=m['tree']
  while 'feature' in node:node=node['left'] if x[node['feature']]<=node['threshold'] else node['right']
  values.append(node['value'])
 return np.array(values)

def quant(scores,rs,q):
 pairs=sorted(zip(scores,wts(rs)),key=lambda p:p[0]);total=0
 for s,w in pairs:
  total+=w
  if total>=q:return float(s)
 return float(pairs[-1][0])
def calibration(scores,rs,saved):
 ts=sorted(set([0.]+[quant(scores,rs,q) for q in [0,.25,.5,.75,1]]))+[None];grid=[];w=wts(rs);y=np.array([r['gain'] for r in rs])
 for t in ts:
  ds=np.array([t is not None and s>=t for s in scores]);grid.append({'threshold':t,'gain':float(w@(y*ds)),'rate':float(w@ds)})
 assert len(grid)==len(saved['grid'])
 for a,b in zip(grid,saved['grid']):
  for k in ['threshold','gain','rate']:
   if a[k] is None:assert b[k] is None
   else:close(a[k],b[k])
 top=max(s['gain'] for s in grid);selected=min((s for s in grid if s['gain']>=top-1e-12),key=lambda s:(s['rate'],-math.inf if s['threshold'] is None else -s['threshold']))
 assert selected['threshold']==saved['selected']['threshold'];return selected

def verify(folds,comparison,rows):
 total=0
 for grouping in ['engine','ecosystem']:
  data=copy.deepcopy(rows)
  if grouping=='ecosystem':
   for r in data:
    if r['group'] in ['spark','hadoop_mapreduce']:r['group']='spark_hadoop_ecosystem'
  for model in MODELS:
   rs=[r for r in data if r['model']==model];fs=folds[grouping][model];assert {f['held_group'] for f in fs}=={r['group'] for r in rs};all_decisions={}
   for f in fs:
    total+=1;g=f['held_group'];train=[r for r in rs if r['group']!=g];held=[r for r in rs if r['group']==g];assert f['training_keys']==[r['key'] for r in train];assert f['held_keys']==[r['key'] for r in held];cals={}
    decisions={r['key']:{'never':False,'always':True} for r in held}
    for kind,v in f['variants'].items():
     oof={};assert {i['held_group'] for i in v['inner']}=={r['group'] for r in train}
     for inner in v['inner']:
      dev=[r for r in train if r['group']!=inner['held_group']];val=[r for r in train if r['group']==inner['held_group']];assert inner['validation_keys']==[r['key'] for r in val]
      scores=score_model(inner['model'],dev,val)
      for r,s in zip(val,scores):close(s,inner['scores'][r['key']]);oof[r['key']]=float(s)
     # Saved prediction values remove roundoff ambiguity at exact threshold ties.
     ss=[next(i['scores'][r['key']] for i in v['inner'] if r['key'] in i['scores']) for r in train]
     cals[kind]=calibration(ss,train,v['calibration']);close(v['quantile80'],quant(ss,train,.8))
     scores=score_model(v['model'],train,held);t=cals[kind]['threshold']
     for r,s in zip(held,scores):
      close(s,v['scores'][r['key']]);s=v['scores'][r['key']];decisions[r['key']][kind]=t is not None and s>=t;decisions[r['key']][kind+'_q80']=s>=v['quantile80']
    selected=min(KINDS,key=lambda k:(-cals[k]['gain'],cals[k]['rate'],KINDS.index(k)));assert f['selected_kind']==selected
    us=[r['features'][6] for r in train];cal=calibration(us,train,f['uncertainty_calibration']);close(f['uncertainty_quantile80'],quant(us,train,.8));t=cal['threshold']
    for r in held:
     d=decisions[r['key']];d['selected_predictor']=d[selected];d['uncertainty']=t is not None and r['features'][6]>=t;d['uncertainty_q80']=r['features'][6]>=f['uncertainty_quantile80']
    assert decisions==f['decisions'];all_decisions.update(decisions)
   summ=comparison['models'][grouping][model]
   for policy,s in summ['policies'].items():
    gs=[];rg=[];calls=harm=useful=joint=miss=0
    for g in sorted({r['group'] for r in rs}):
     vals=[r for r in rs if r['group']==g];chosen=[r for r in vals if all_decisions[r['key']][policy]];k=len(chosen);n=len(vals);gain=sum(r['gain'] for r in chosen)/n;random=k/n*statistics.mean(r['gain'] for r in vals);gs.append(gain);rg.append(random)
     saved=next(x for x in s['groups'] if x['group']==g);assert saved['calls']==k and saved['n']==n;close(saved['gain'],gain);close(saved['random_expected_gain'],random)
     calls+=k;harm+=sum(r['gain']<-.01 for r in chosen);useful+=sum(r['gain']>.01 for r in chosen);joint+=sum(r['gain']>.01 and r['adaptive_gain']>.01 for r in chosen);miss+=sum(r['gain']>.01 for r in vals)-sum(r['gain']>.01 for r in chosen)
    assert (s['calls'],s['harmful'],s['useful'],s['joint_useful'],s['missed'])==(calls,harm,useful,joint,miss);close(s['family_mean_gain'],statistics.mean(gs));close(s['gain_above_random'],statistics.mean(gs)-statistics.mean(rg))
 return total

def main():
 for n,h in read(ART/'freeze.json')['sha256'].items():assert sha(ROOT/n)==h,n
 rows=read(ART/'inputs.json')['rows'];base=read(ROOT/'artifacts/study_v147/inputs.json')['rows'];hadoop=read(ROOT/'results/v148_hadoop/comparison.json')['cases']
 for r in rows:
  if r['stage']!=148:
   b=next(b for b in base if (b['key'],b['model'])==(r['key'],r['model']))
   for k in ['gain','adaptive_gain','target','sequential','adaptive','prefix_sha256','usage']:assert r[k]==b[k]
   assert r['features'][:7]==b['features']
  else:
   b=next(b for b in hadoop if (b['key'],b['model'])==(r['key'],r['model']));assert r['gain']==b['gains']['sequential_3nn'] and r['target']==b['target']
  sign=1 if r['direction']=='minimize' else -1;close(r['gain'],sign*(r['sequential']-r['target'])/r['sequential']);assert sha(ROOT/r['prefix'])==r['prefix_sha256']
 folds=read(OUT/'folds.json');c=read(OUT/'comparison.json');count=verify(folds,c,rows);mut=[]
 for name in ['reported_gain','held_target','membership','decision']:
  ff=copy.deepcopy(folds);cc=copy.deepcopy(c);rr=copy.deepcopy(rows);f=ff['engine'][MODELS[0]][0]
  if name=='reported_gain':cc['models']['engine'][MODELS[0]]['policies']['never']['family_mean_gain']=.1
  elif name=='held_target':next(r for r in rr if r['model']==MODELS[0] and r['key']==f['held_keys'][0])['gain']+=123
  elif name=='membership':f['variants'][KINDS[0]]['model']['training_keys'].append(f['held_keys'][0])
  else:f['decisions'][f['held_keys'][0]]['never']=True
  try:verify(ff,cc,rr)
  except (AssertionError,ValueError):mut.append({'name':name,'rejected':True})
  else:raise AssertionError('Mutation accepted: '+name)
 write(ART/'replay.json',{'verified':True,'cases':len(rows),'outer_folds':count,'mutations':mut,'scope':'independent ridge/RBF algebra, tree split optimality, inner/outer memberships, calibration, decisions and primary aggregates; hashes authenticate original prefix/source lineage'})
 print('Verified140cases,30outerfolds,allfixedpredictors;4semanticmutationsrejected')
if __name__=='__main__':main()
