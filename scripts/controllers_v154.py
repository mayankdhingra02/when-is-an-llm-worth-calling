"""Exploratory source-mapped checkpoint adaptations; feature stage has no outcomes."""
import argparse,copy,hashlib,math,time
from pathlib import Path
import numpy as np
from router_v147 import ROOT,read,write,sha,select,MODELS
A=ROOT/'artifacts/study_v154';O=ROOT/'results/v154_controllers'

def encode(raw):
    a=np.asarray(raw,dtype=object)
    if a.ndim!=2 or len(a)<10:raise ValueError('Invalid candidates')
    cols=[];cat=[]
    for j in range(a.shape[1]):
        v=a[:,j].tolist()
        if len(set(v))<2:continue
        categorical=any(isinstance(x,str) for x in v)
        if categorical:
            levels=sorted(set(v),key=str);z=np.array([levels.index(x) for x in v],float)
        else:
            z=np.asarray(v,float)
            if not np.isfinite(z).all():raise ValueError('Nonfinite features')
            z=(z-z.min())/(z.max()-z.min())
        cols.append(z);cat.append(categorical)
    if not cols:raise ValueError('No variable features')
    return np.array(cols).T,np.array(cat,bool)

def kernel(a,b,cat,length):
    if length<=0:raise ValueError('Invalid lengthscale')
    k=np.ones((len(a),len(b)))
    if (~cat).any():
        d=np.sqrt(np.mean((a[:,None,~cat]-b[None,:,~cat])**2,axis=2))/length;t=np.sqrt(5)*d
        k*=(1+t+t*t/3)*np.exp(-t)
    if cat.any():k*=np.exp(-np.mean(a[:,None,cat]!=b[None,:,cat],axis=2))
    return k

def gp(train,y,test,cat,length):
    y=np.asarray(y,float);scale=float(np.std(y));scale=scale if scale>1e-12 else 1.;mean=float(np.mean(y))
    k=kernel(train,train,cat,length)+1e-6*np.eye(len(train));cross=kernel(train,test,cat,length)
    l=np.linalg.cholesky(k);z=np.linalg.solve(l,cross)
    pred=mean+scale*cross.T@np.linalg.solve(l.T,np.linalg.solve(l,(y-mean)/scale))
    sd=np.sqrt(np.maximum(0,1-np.sum(z*z,axis=0)))
    return pred,sd

def tau_pair(a,b):
    da=float(a[1]-a[0]);db=float(b[1]-b[0])
    return None if da==0 or db==0 else float(np.sign(da)*np.sign(db))

def plateau(y,direction,m):
    y=np.asarray(y,float)
    if direction not in ['minimize','maximize']:raise ValueError('Unknown direction')
    best=np.minimum.accumulate(y) if direction=='minimize' else np.maximum.accumulate(y)
    sign=1 if direction=='minimize' else -1
    improvements=sign*(best[3:-1]-best[4:])/np.abs(best[3:-1])
    return len(improvements)>=m and bool(np.all(improvements[-m:]<.05)),improvements.tolist()

def signals(case,length):
    x,cat=encode(case['raw_features']);ids=case['ids'];y=np.asarray(case['labels'],float)
    if len(ids)!=10 or len(set(ids))!=10 or y.shape!=(10,) or not np.isfinite(y).all() or min(y)<=0:raise ValueError('Ten unique positive acquired labels required')
    if min(ids)<0 or max(ids)>=len(x):raise ValueError('Invalid row IDs')
    monitor=np.sort(np.random.default_rng(154000+case['seed']).choice(len(x),min(64,len(x)),replace=False));trace=[];maximum=0.
    for n in range(4,11):
        _,sd=gp(x[ids[:n]],y[:n],x[monitor],cat,length);maximum=max(maximum,float(max(sd)))
        trace.append({'n':n,'mean_sd':float(np.mean(sd)),'max_sd':float(max(sd)),'running_max_sd':maximum})
    ratio=trace[-1]['mean_sd']/maximum if maximum else 0.;m=math.ceil(2*math.sqrt(x.shape[1]));p,improvements=plateau(y,case['direction'],m);pc,_=plateau(y,case['direction'],min(m,6))
    def action(stalled):return 'a1' if not stalled or ratio<.3 else ('a2' if ratio>.5 else 'a3')
    permutation=np.random.default_rng(154100+case['seed']).permutation(10);folds=[]
    for held in np.array_split(permutation,5):
        train=np.array([i for i in range(10) if i not in held]);pred,_=gp(x[np.array(ids)[train]],y[train],x[np.array(ids)[held]],cat,length);tau=tau_pair(pred,y[held])
        folds.append({'train_positions':train.tolist(),'held_positions':held.tolist(),'predictions':pred.tolist(),'tau':tau})
    tau=sum(f['tau'] if f['tau'] is not None else 0. for f in folds)/5;p_llm=1-max(.05,(tau+1)/2)
    draw=int(hashlib.sha256(('154|'+case['key']).encode()).hexdigest()[:13],16)/16**13
    return {'lengthscale':length,'dimensions':x.shape[1],'categorical':cat.tolist(),'monitor_ids':monitor.tolist(),'uncertainty_trace':trace,'uncertainty_ratio':ratio,'plateau_length':m,'history_updates':6,'relative_improvements':improvements,'plateau':p,'plateau_capped':pc,'bora_action':action(p),'bora_capped_action':action(pc),'rank_folds':folds,'mean_tau':tau,'undefined_folds':sum(f['tau'] is None for f in folds),'p_llm':p_llm,'uniform_draw':draw,'rank_draw_call':draw<p_llm}

def prepare():
    assert not (A/'freeze.json').exists();used=set()
    def load(n):used.add(n);return read(ROOT/n)
    rows=load('artifacts/study_v151/inputs.json')['rows'];cases={}
    for r in rows:
        if r['key'] in cases:continue
        p=load(r['prefix']);assert sha(ROOT/r['prefix'])==r['prefix_sha256'];s=p.get('state',p)
        if r['stage']==141:n=f"artifacts/study_v141/candidates/{r['engine_group']}.json"
        else:n=f"artifacts/study_v{144 if r['stage']==145 else 148}/candidates/{r['source_key'].rsplit('_',1)[0]}.json"
        c=load(n);raw=c.get('raw_features',c['x']);assert len(raw)==len(s['order'])
        cases[r['key']]={'key':r['key'],'seed':r['seed'],'engine_group':r['engine_group'],'direction':r['direction'],'ids':s['ids'],'labels':[v[0] for v in s['labels']],'raw_features':raw,'prefix':r['prefix'],'candidate_path':n}
    assert len(cases)==70
    write(A/'prefix_inputs.json',{'cases':list(cases.values()),'scope':'only candidate features and ten acquired labels; no continuation outcomes'})
    used.update(['artifacts/study_v154/prefix_inputs.json','scripts/controllers_v154.py','tests/synthetic/test_controllers_v154.py','reports/protocol_v154.md','scripts/router_v147.py','results/v151_router/folds.json'])
    write(A/'freeze.json',{'at_unix':time.time(),'sha256':{n:sha(ROOT/n) for n in sorted(used)}});print('Frozen70unique prefixes;140historical model outcomes for later scoring')

def guard():
    for n,h in read(A/'freeze.json')['sha256'].items():assert sha(ROOT/n)==h,n

def compute():
    guard();assert not (A/'signals.json').exists();start=time.monotonic();out={}
    for c in read(A/'prefix_inputs.json')['cases']:
        if time.monotonic()-start>600:raise TimeoutError('600second cap')
        out[c['key']]={str(l):signals(c,l) for l in [1.,.2]}
    write(A/'signals.json',out);write(A/'signals_runtime.json',{'wall_seconds':time.monotonic()-start,'cap_seconds':600,'new_requests':0,'new_acquisitions':0});print('Computed70prefixes×2fixed kernels; no continuation outcomes read')

def policies(rows,grouping,sig,old):
    folds=[];dec={}
    for g in sorted({r['group'] for r in rows}):
        train=[r for r in rows if r['group']!=g];test=[r for r in rows if r['group']==g];cal={}
        for name,field in [('gp_uncertainty_calibrated','uncertainty_ratio'),('rank_calibrated','p_llm')]:cal[name]=select([sig[r['key']]['1.0'][field] for r in train],train)
        prior=next(f for f in old if f['held_group']==g)
        for r in test:
            ds={'never':0.,'always':1.,'benefit_v151':float(prior['decisions'][r['key']]['selected_predictor']),'uncertainty_v151':float(prior['decisions'][r['key']]['uncertainty'])}
            for length in ['1.0','0.2']:
                s=sig[r['key']][length]
                ds.update({f'bora_{length}':float(s['bora_action']!='a1'),f'bora_capped_{length}':float(s['bora_capped_action']!='a1'),f'rank_expected_{length}':s['p_llm'],f'rank_draw_{length}':float(s['rank_draw_call'])})
            for name,field in [('gp_uncertainty_calibrated','uncertainty_ratio'),('rank_calibrated','p_llm')]:
                t=cal[name]['selected']['threshold'];ds[name]=float(t is not None and sig[r['key']]['1.0'][field]>=t)
            dec[r['key']]=ds
        folds.append({'held_group':g,'training_keys':[r['key'] for r in train],'held_keys':[r['key'] for r in test],'calibrations':cal})
    return dec,folds

def aggregate(rows,dec):
    result={}
    for policy in next(iter(dec.values())):
        gs=[]
        for g in sorted({r['group'] for r in rows}):
            rs=[r for r in rows if r['group']==g];p=np.array([dec[r['key']][policy] for r in rs]);y=np.array([r['gain'] for r in rs]);z=np.array([r['adaptive_gain'] for r in rs]);no=np.array([(r['adaptive']-r['sequential'])/r['adaptive']*(1 if r['direction']=='minimize' else -1) for r in rs]);n=len(rs)
            gs.append({'group':g,'n':n,'calls':float(sum(p)),'gain':float(np.mean(p*y)),'gain_vs_adaptive':float(np.mean(p*z+(1-p)*no)),'random_expected_gain':float(np.mean(p)*np.mean(y)),'useful':float(sum(p*(y>.01))),'harmful':float(sum(p*(y<-.01))),'joint_useful':float(sum(p*((y>.01)&(z>.01)))),'missed':float(sum((1-p)*(y>.01))),'generated_tokens_lower_bound':sum(float(q)*(r['usage']['generated_tokens'] or 0) for r,q in zip(rs,p)),'request_seconds_lower_bound':sum(float(q)*(r['usage']['request_seconds'] or 0) for r,q in zip(rs,p)),'unknown_usage':sum(float(q) for r,q in zip(rs,p) if r['usage']['generated_tokens'] is None),'selected_fallbacks':sum(float(q)*r['fallback'] for r,q in zip(rs,p))})
        result[policy]={'probabilistic_expectation':policy.startswith('rank_expected'),'family_mean_gain':float(np.mean([s['gain'] for s in gs])),'family_mean_gain_vs_adaptive':float(np.mean([s['gain_vs_adaptive'] for s in gs])),'above_matched_random':float(np.mean([s['gain']-s['random_expected_gain'] for s in gs])),'family_mean_rate':float(np.mean([s['calls']/s['n'] for s in gs])),**{k:sum(s[k] for s in gs) for k in ['calls','useful','harmful','joint_useful','missed','generated_tokens_lower_bound','request_seconds_lower_bound','unknown_usage','selected_fallbacks']},'groups':gs}
    return result

def evaluate():
    guard();assert not O.exists();start=time.monotonic();O.mkdir();sig=read(A/'signals.json');original=read(A/'prefix_inputs.json');rows=read(ROOT/'artifacts/study_v151/inputs.json')['rows'];old=read(ROOT/'results/v151_router/folds.json');results={};allfolds={};decisions={}
    for grouping in ['ecosystem','engine']:
        data=copy.deepcopy(rows)
        if grouping=='ecosystem':
            for r in data:
                if r['group'] in ['spark','hadoop_mapreduce']:r['group']='spark_hadoop_ecosystem'
        results[grouping]={};allfolds[grouping]={};decisions[grouping]={}
        for m in MODELS:
            rs=[r for r in data if r['model']==m];d,f=policies(rs,grouping,sig,old[grouping][m]);decisions[grouping][m]=d;allfolds[grouping][m]=f;results[grouping][m]=aggregate(rs,d)
    write(O/'decisions.json',decisions);write(O/'folds.json',allfolds);write(O/'comparison.json',{'exploratory':True,'new_requests':0,'new_acquisitions':0,'cases_per_model':70,'models':results});write(A/'evaluation_runtime.json',{'wall_seconds':time.monotonic()-start,'signals_sha256':sha(A/'signals.json')});print('Scored all fixed policies against140real historical outcomes')
if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('stage',choices=['prepare','compute','evaluate']);args=ap.parse_args();globals()[args.stage]()
