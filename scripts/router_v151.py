"""Fixed exploratory predictors on genuine saved prefixes; no oracle or inference."""
import argparse, copy, hashlib, json, math, time
from pathlib import Path
import numpy as np
from router_v147 import ROOT, read, write, sha, weights, quantile, select, MODELS
from router_v132 import FEATURES, features as original_features
ART=ROOT/'artifacts/study_v151'; OUT=ROOT/'results/v151_router'
EXTRA=['log_spread','relative_iqr','best_median_log_gap','early_log_progress','late_log_progress','best_second_log_gap','unique_label_fraction','time_label_correlation','last_first_log_mean','early_label_cv','high_tail_fraction']
NAMES=FEATURES+EXTRA
KINDS=['ridge_original','ridge_extended','tree_extended','rbf_extended']

def trajectory(state,direction):
    y=np.asarray(state['labels'],float)
    if y.shape!=(10,1) or len(state['ids'])!=10 or len(set(state['ids']))!=10 or not np.isfinite(y).all() or (y<=0).any():raise ValueError('Exactly ten unique positive acquired labels required')
    if direction not in ['minimize','maximize']:raise ValueError('Unknown objective direction')
    y=y[:,0]; sign=-1 if direction=='minimize' else 1
    # Normalize before logs, so changing objective units leaves the vector unchanged.
    v=np.log(y/np.median(y)); z=sign*v; best=np.maximum.accumulate(z); q1,q3=np.quantile(y,[.25,.75]); ordered=np.sort(z)
    corr=0. if np.std(z)<1e-12 else float(np.corrcoef(np.arange(10),z)[0,1])
    return [float(np.std(v)),float((q3-q1)/np.median(y)),float(max(z)),float(best[3]-best[0]),float(best[9]-best[3]),float(ordered[-1]-ordered[-2]),len(set(y.tolist()))/10,corr,float(np.mean(z[5:])-np.mean(z[:5])),float(np.std(y[:4])/np.mean(y[:4])),float(np.mean(y>q3+1.5*(q3-q1)))]

def fit(rows,kind):
    if kind not in KINDS or len({r['group'] for r in rows})<2:raise ValueError('Invalid predictor/training groups')
    d=7 if kind=='ridge_original' else len(NAMES)
    x=np.array([r['features'][:d] for r in rows]);y=np.array([r['gain'] for r in rows]);w=weights(rows)
    if not np.isfinite(x).all() or not np.isfinite(y).all():raise ValueError('Nonfinite training data')
    mean=w@x;scale=np.sqrt(w@((x-mean)**2));scale[scale<1e-12]=1;z=(x-mean)/scale;intercept=float(w@y)
    model={'kind':kind,'mean':mean.tolist(),'scale':scale.tolist(),'intercept':intercept,'training_keys':[r['key'] for r in rows],'training_groups':sorted({r['group'] for r in rows})}
    if kind.startswith('ridge'):
        coef=np.linalg.solve(z.T@(w[:,None]*z)+np.eye(d),z.T@(w*(y-intercept)));model['coef']=coef.tolist()
    elif kind=='rbf_extended':
        kernel=np.exp(-np.mean((z[:,None,:]-z[None,:,:])**2,axis=2)/2);sw=np.sqrt(w)
        model['dual']=(sw*np.linalg.solve(sw[:,None]*kernel*sw[None,:]+.1*np.eye(len(rows)),sw*(y-intercept))).tolist();model['training_z']=z.tolist()
    else:
        groups=np.array([r['group'] for r in rows])
        def build(ids,depth):
            value=float(np.average(y[ids],weights=w[ids])); node={'value':value,'n':len(ids),'groups':sorted(set(groups[ids]))}
            loss=float(np.sum(w[ids]*(y[ids]-value)**2));best=None
            if depth<2:
                for j in range(d):
                    for t in sorted(set(np.quantile(z[ids,j],[.25,.5,.75]).tolist())):
                        left=ids[z[ids,j]<=t];right=ids[z[ids,j]>t]
                        if min(len(left),len(right))<5 or min(len(set(groups[left])),len(set(groups[right])))<2:continue
                        new=sum(float(np.sum(w[a]*(y[a]-np.average(y[a],weights=w[a]))**2)) for a in [left,right])
                        if new<loss-1e-12 and (best is None or new<best[0]-1e-12):best=(new,j,t,left,right)
            if best is not None:
                _,j,t,left,right=best;node.update(feature=j,threshold=t,left=build(left,depth+1),right=build(right,depth+1))
            return node
        model['tree']=build(np.arange(len(rows)),0)
    return model

def predict(model,row):
    z=(np.asarray(row['features'][:len(model['mean'])])-model['mean'])/model['scale'];kind=model['kind']
    if kind.startswith('ridge'):return float(z@model['coef']+model['intercept'])
    if kind=='rbf_extended':return float(np.exp(-np.mean((np.asarray(model['training_z'])-z)**2,axis=1)/2)@model['dual']+model['intercept'])
    node=model['tree']
    while 'feature' in node:node=node['left'] if z[node['feature']]<=node['threshold'] else node['right']
    return node['value']

def outer(rows,held):
    if len({r['key'] for r in rows})!=len(rows):raise ValueError('Duplicate analysis case keys; qualify by engine family')
    train=[r for r in rows if r['group']!=held];test=[r for r in rows if r['group']==held]
    if not train or not test:raise ValueError('Missing outer split')
    groups=sorted({r['group'] for r in train});result={'held_group':held,'training_groups':groups,'training_keys':[r['key'] for r in train],'held_keys':[r['key'] for r in test],'variants':{}}
    decisions={r['key']:{'never':False,'always':True} for r in test}
    for kind in KINDS:
        inner=[];scores={}
        for g in groups:
            dev=[r for r in train if r['group']!=g];val=[r for r in train if r['group']==g];model=fit(dev,kind)
            sv={r['key']:predict(model,r) for r in val};scores.update(sv)
            inner.append({'held_group':g,'model':model,'validation_keys':[r['key'] for r in val],'scores':sv})
        ss=[scores[r['key']] for r in train];cal=select(ss,train);t=cal['selected']['threshold'];t80=quantile(ss,train,.8)
        model=fit(train,kind);test_scores={r['key']:predict(model,r) for r in test}
        result['variants'][kind]={'inner':inner,'calibration':cal,'quantile80':t80,'model':model,'scores':test_scores}
        for r in test:
            score=test_scores[r['key']];decisions[r['key']][kind]=t is not None and score>=t;decisions[r['key']][kind+'_q80']=score>=t80
    chosen=min(KINDS,key=lambda k:(-result['variants'][k]['calibration']['selected']['gain'],result['variants'][k]['calibration']['selected']['rate'],KINDS.index(k)))
    result['selected_kind']=chosen
    us=[r['features'][6] for r in train];cal=select(us,train);u=cal['selected']['threshold'];u80=quantile(us,train,.8)
    result['uncertainty_calibration']=cal;result['uncertainty_quantile80']=u80
    for r in test:
        ds=decisions[r['key']];ds['selected_predictor']=ds[chosen];ds['uncertainty']=u is not None and r['features'][6]>=u;ds['uncertainty_q80']=r['features'][6]>=u80
    result['decisions']=decisions;return result

def auc(scores,labels):
    pos=[s for s,y in zip(scores,labels) if y];neg=[s for s,y in zip(scores,labels) if not y]
    return None if not pos or not neg else sum((a>b)+.5*(a==b) for a in pos for b in neg)/(len(pos)*len(neg))

def summarize(rows,folds):
    decisions={k:v for f in folds for k,v in f['decisions'].items()};groups=sorted({r['group'] for r in rows});out={}
    for p in next(iter(decisions.values())):
        summaries=[]
        for g in groups:
            rs=[r for r in rows if r['group']==g];chosen=[r for r in rs if decisions[r['key']][p]];k=len(chosen);n=len(rs)
            rng=np.random.default_rng(int(hashlib.sha256((p+'|'+g).encode()).hexdigest()[:12],16)+151000);idx=rng.choice(n,k,replace=False)
            summaries.append({'group':g,'n':n,'calls':k,'gain':sum(r['gain'] for r in chosen)/n,'random_expected_gain':k/n*np.mean([r['gain'] for r in rs]),'random_one_gain':sum(rs[i]['gain'] for i in idx)/n,'random_keys':[rs[i]['key'] for i in idx],'harmful':sum(r['gain']<-.01 for r in chosen),'useful':sum(r['gain']>.01 for r in chosen),'joint_useful':sum(r['gain']>.01 and r['adaptive_gain']>.01 for r in chosen),'missed':sum(r['gain']>.01 for r in rs)-sum(r['gain']>.01 for r in chosen),'observed_generated_tokens_lower_bound':sum(r['usage']['generated_tokens'] or 0 for r in chosen),'observed_request_seconds_lower_bound':sum(r['usage']['request_seconds'] or 0 for r in chosen),'unknown_usage':sum(r['usage']['generated_tokens'] is None for r in chosen),'selected_fallbacks':sum(r['fallback'] for r in chosen)})
        gains=[s['gain'] for s in summaries];random_gain=float(np.mean([s['random_expected_gain'] for s in summaries]))
        out[p]={'family_mean_gain':float(np.mean(gains)),'pooled_mean_gain':sum(s['gain']*s['n'] for s in summaries)/len(rows),'family_mean_rate':float(np.mean([s['calls']/s['n'] for s in summaries])),'random_expected_gain':random_gain,'gain_above_random':float(np.mean(gains))-random_gain,'leave_one_group_mean_range':[min((sum(gains)-x)/(len(gains)-1) for x in gains),max((sum(gains)-x)/(len(gains)-1) for x in gains)],**{k:sum(s[k] for s in summaries) for k in ['calls','harmful','useful','joint_useful','missed','observed_generated_tokens_lower_bound','observed_request_seconds_lower_bound','unknown_usage','selected_fallbacks']},'groups':summaries}
    ranking={}
    for kind in KINDS:
        ranking[kind]=[]
        for f in folds:
            rs=[r for r in rows if r['group']==f['held_group']];scores=[f['variants'][kind]['scores'][r['key']] for r in rs]
            ranking[kind].append({'group':f['held_group'],'auc':auc(scores,[r['gain']>.01 for r in rs]),'useful':sum(r['gain']>.01 for r in rs),'n':len(rs)})
    return {'policies':out,'ranking':ranking,'oracle_family_gain':float(np.mean([np.mean([max(0,r['gain']) for r in rows if r['group']==g]) for g in groups])),'opportunity_groups':sorted({r['group'] for r in rows if r['gain']>.01}),'joint_opportunity_groups':sorted({r['group'] for r in rows if r['gain']>.01 and r['adaptive_gain']>.01})}

def prepare():
    assert not (ART/'freeze.json').exists();used=set()
    def load(n):used.add(n);return read(ROOT/n)
    rows=copy.deepcopy(load('artifacts/study_v147/inputs.json')['rows']);jobs=load('artifacts/study_v148/jobs.json');comparison=load('results/v148_hadoop/comparison.json')
    raw={}
    for m in MODELS:
        n=f'results/v148_models/{m}/responses.jsonl';used.add(n);raw[m]={r['key']:r for r in map(json.loads,(ROOT/n).read_text().splitlines())}
    for r in comparison['cases']:
        j=next(j for j in jobs if j['key']==r['key']);s=load(j['prefix']);c=load(f"artifacts/study_v148/candidates/{j['app']}.json");response=raw[r['model']][r['key']];u=response['response']
        rows.append({'key':r['key'],'model':r['model'],'stage':148,'group':'hadoop_mapreduce','seed':r['seed'],'features':original_features(s,c['domains'],'minimize'),'gain':r['gains']['sequential_3nn'],'adaptive_gain':r['gains']['adaptive_neighbor'],'fallback':r['fallback'],'target':r['target'],'sequential':r['references']['sequential_3nn'],'adaptive':r['references']['adaptive_neighbor'],'prefix_best':r['prefix_best'],'direction':'minimize','prefix':j['prefix'],'prefix_sha256':j['prefix_sha256'],'usage':{'generated_tokens':u.get('tokens_predicted'),'prefill_tokens':u.get('tokens_evaluated'),'request_seconds':response['wall_seconds']}})
    for r in rows:
        p=load(r['prefix']);assert sha(ROOT/r['prefix'])==r['prefix_sha256'];r['features']+=trajectory(p.get('state',p),r['direction']);r['engine_group']=r['group']
    for r in rows:
        r['source_key']=r['key'];r['key']=r['engine_group']+'::'+r['source_key']
    assert len({(r['model'],r['key']) for r in rows})==len(rows)
    rows.sort(key=lambda r:(r['model'],r['group'],r['key']))
    assert len(rows)==140 and len({r['group'] for r in rows})==8 and sum(r['fallback'] for r in rows)==1
    assert all(len(r['features'])==18 for r in rows)
    write(ART/'inputs.json',{'feature_names':NAMES,'rows':rows,'exploratory':True,'new_acquisitions':0,'new_requests':0})
    used.update(['artifacts/study_v151/inputs.json','scripts/router_v151.py','reports/protocol_v151.md','tests/synthetic/test_router_v151.py','scripts/router_v147.py','scripts/router_v132.py'])
    write(ART/'freeze.json',{'at_unix':time.time(),'sha256':{n:sha(ROOT/n) for n in sorted(used)}})
    print('Frozen140existing real model-cases; no new acquisition or inference')

def run():
    start=time.monotonic();cpu=time.process_time()
    for n,h in read(ART/'freeze.json')['sha256'].items():
        if sha(ROOT/n)!=h:raise ValueError('Changed frozen input: '+n)
    assert not OUT.exists();OUT.mkdir();rows=read(ART/'inputs.json')['rows'];results={};saved={}
    for grouping in ['engine','ecosystem']:
        data=copy.deepcopy(rows)
        if grouping=='ecosystem':
            for r in data:
                if r['group'] in ['spark','hadoop_mapreduce']:r['group']='spark_hadoop_ecosystem'
        groups=sorted({r['group'] for r in data});assert len(groups)==(8 if grouping=='engine' else 7),(grouping,groups)
        results[grouping]={};saved[grouping]={}
        for m in MODELS:
            rs=[r for r in data if r['model']==m];folds=[]
            for g in groups:
                if time.monotonic()-start>600:raise TimeoutError('600second analysis cap')
                folds.append(outer(rs,g))
            saved[grouping][m]=folds;results[grouping][m]=summarize(rs,folds)
            print(json.dumps({'grouping':grouping,'model':m,'policies':{p:{k:v[k] for k in ['calls','family_mean_gain','gain_above_random','useful','harmful']} for p,v in results[grouping][m]['policies'].items()}}),flush=True)
    write(OUT/'folds.json',saved);write(OUT/'comparison.json',{'exploratory':True,'models':results,'cases_per_model':70,'new_requests':0,'new_acquisitions':0})
    write(ART/'runtime.json',{'wall_seconds':time.monotonic()-start,'cpu_seconds':time.process_time()-cpu,'cap_seconds':600,'freeze_sha256':sha(ART/'freeze.json')})
if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('stage',choices=['prepare','run']);args=ap.parse_args();globals()[args.stage]()
