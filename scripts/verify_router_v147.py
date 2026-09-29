"""Separate algebraic replay: raw paired targets, prefix features, nested folds and scores."""
import collections
import copy
import hashlib
import json
import math
import random
from pathlib import Path
import numpy as np
ROOT=Path(__file__).resolve().parents[1]
ART=ROOT/'artifacts/study_v147';OUT=ROOT/'results/v147_router'

def read(p):return json.loads(Path(p).read_text())
def close(a,b):assert np.allclose(a,b,rtol=1e-10,atol=1e-12),(a,b)
def w(rs):
    c=collections.Counter(x['group'] for x in rs)
    return np.array([1/(len(c)*c[x['group']]) for x in rs])
def ref_fit(rs,cols):
    x=np.array([[r['features'][i] for i in cols] for r in rs]);y=np.array([r['gain'] for r in rs]);weights=w(rs)
    avg=np.average(x,axis=0,weights=weights);scale=np.sqrt(np.average((x-avg)**2,axis=0,weights=weights));scale[scale<1e-12]=1
    z=(x-avg)/scale;inter=float(weights@y)
    # Independent augmented least-squares formulation of fixed-alpha ridge.
    coef=np.linalg.lstsq(np.vstack([z*np.sqrt(weights[:,None]),np.eye(len(cols))]),np.r_[(y-inter)*np.sqrt(weights),np.zeros(len(cols))],rcond=None)[0]
    return avg,scale,coef,inter

def ref_scores(rs,cols,other):
    a,s,b,i=ref_fit(rs,cols)
    return [float((np.array([r['features'][c] for c in cols])-a)/s@b+i) for r in other]
def q(scores,rs,v):
    pairs=sorted(zip(scores,w(rs)),key=lambda x:x[0]);acc=0
    for score,weight in pairs:
        acc+=weight
        if acc>=v:return float(score)
    return float(pairs[-1][0])
def threshold(scores,rs):
    candidates=sorted(set([0.]+[q(scores,rs,v) for v in [0,.25,.5,.75,1]]))+[None];options=[]
    for t in candidates:
        calls=[t is not None and x>=t for x in scores]
        options.append((t,sum(a*r['gain']*d for a,r,d in zip(w(rs),rs,calls)),sum(a*d for a,d in zip(w(rs),calls))))
    top=max(x[1] for x in options)
    return min([x for x in options if x[1]>=top-1e-12],key=lambda x:(x[2],-math.inf if x[0] is None else -x[0]))

def verify(rows,folds,report):
    assert len(rows)==110 and len({(r['model'],r['key']) for r in rows})==110
    assert report['families']==7 and report['cases_per_model']==55 and report['new_model_requests']==report['new_acquisitions']==0
    for r in rows:
        p=read(ROOT/r['prefix']);s=p.get('state',p);y=[v[0] for v in s['labels']];assert len(y)==len(set(s['ids']))==10
        best=[]
        for i in range(10):best.append((min if r['direction']=='minimize' else max)(y[:i+1]))
        rng=random.Random(132000);extrema=[]
        for _ in range(64):extrema.append((min if r['direction']=='minimize' else max)([y[rng.randrange(10)] for _ in range(10)]))
        sign=1 if r['direction']=='minimize' else -1
        expected=[np.std(y)/np.mean(y),sign*(best[0]-best[-1])/best[0],(9-max(i for i in range(10) if i==0 or best[i]!=best[i-1]))/9,np.std(extrema)/np.mean(y)]
        close(r['features'][3:],expected);close(r['features'][0],math.log1p(len(s['order'])))
        close(r['gain'],sign*(r['sequential']-r['target'])/r['sequential'])
        close(r['adaptive_gain'],sign*(r['adaptive']-r['target'])/r['adaptive'])
    for model in sorted({r['model'] for r in rows}):
        rs=[r for r in rows if r['model']==model];groups=sorted({r['group'] for r in rs});assert len(groups)==7 and len(rs)==55
        assert {f['held_group'] for f in folds[model]}==set(groups)
        decisions={}
        for f in folds[model]:
            held=f['held_group'];train=[r for r in rs if r['group']!=held];test=[r for r in rs if r['group']==held]
            assert f['training_keys']==[r['key'] for r in train] and f['held_keys']==[r['key'] for r in test]
            assert f['training_groups']==sorted(set(groups)-{held})
            ds={r['key']:{'never':False,'always':True} for r in test}
            for variant,v in f['variants'].items():
                cols=v['model']['indices'];a,s,b,i=ref_fit(train,cols)
                for x,y in zip([a,s,b,i],[v['model'][k] for k in ['mean','scale','coef','intercept']]):close(x,y)
                predictions={}
                for inf in v['inner_folds']:
                    g=inf['held_group'];tr=[r for r in train if r['group']!=g];va=[r for r in train if r['group']==g]
                    assert inf['training_keys']==[r['key'] for r in tr] and inf['validation_keys']==[r['key'] for r in va]
                    expected=ref_scores(tr,cols,va);close(inf['scores'],expected)
                    predictions.update(zip([r['key'] for r in va],inf['scores']))
                scores=[predictions[r['key']] for r in train];t,gain,rate=threshold(scores,train);sel=v['calibration']['selected']
                assert sel['threshold']==t;close([sel['gain'],sel['rate']],[gain,rate])
                actual=ref_scores(train,cols,test);close(list(v['outer_scores'][r['key']] for r in test),actual)
                for r in test:ds[r['key']]['benefit_'+variant]=t is not None and v['outer_scores'][r['key']]>=t
                if variant=='all':
                    t80=q(scores,train,.8);close(t80,f['benefit_80pct_threshold'])
                    for r in test:ds[r['key']]['benefit_80pct']=v['outer_scores'][r['key']]>=t80
            us=[r['features'][-1] for r in train];ut,ug,ur=threshold(us,train);assert f['uncertainty_calibration']['selected']['threshold']==ut
            u80=q(us,train,.8);close(u80,f['uncertainty_80pct_threshold'])
            for r in test:
                ds[r['key']]['uncertainty']=ut is not None and r['features'][-1]>=ut
                ds[r['key']]['uncertainty_80pct']=r['features'][-1]>=u80
            assert ds==f['decisions'];decisions.update(ds)
        summary=report['models'][model]
        close(summary['hindsight_oracle_family_mean_gain'],np.mean([np.mean([max(r['gain'],0) for r in rs if r['group']==g]) for g in groups]))
        for policy,p in summary['policies'].items():
            ys=np.array([r['gain'] for r in rs]);calls=np.array([decisions[r['key']][policy] for r in rs]);weights=w(rs)
            assert p['calls']==int(calls.sum()) and p['intended']==55
            close(p['family_mean_gain'],weights@(ys*calls));close(p['pooled_mean_gain'],np.mean(ys*calls));close(p['family_mean_call_rate'],weights@calls)
            assert p['harmful_calls']==sum(calls & (ys<-.01));assert p['missed_useful_calls']==sum(~calls & (ys>.01))
            expected=[]
            for g in groups:
                inds=[j for j,r in enumerate(rs) if r['group']==g];e=float(calls[inds].mean()*ys[inds].mean());expected.append(e)
                item=next(x for x in p['groups'] if x['group']==g);close(item['gain'],float(np.mean(ys[inds]*calls[inds])));close(item['random_expected_gain'],e)
                assert item['calls']==sum(calls[inds]) and item['n']==len(inds)
                assert len(item['random_selected_keys'])==len(set(item['random_selected_keys']))==item['calls']
                assert set(item['random_selected_keys'])<=set(rs[j]['key'] for j in inds)
            close(p['random_matched_expected_gain'],np.mean(expected));close(p['gain_above_matched_random'],p['family_mean_gain']-np.mean(expected))
    return {'verified':True,'model_cases':110,'outer_folds':14,'independent_ridge_fits':'augmented least squares','new_collection':0}

def main():
    freeze=read(ART/'freeze.json')
    for n,h in freeze['sha256'].items():assert hashlib.sha256((ROOT/n).read_bytes()).hexdigest()==h,n
    rows=read(ART/'inputs.json')['rows']; source_old=read(ROOT/'results/v141_analysis/comparison.json'); source_spark=read(ROOT/'results/v145_spark/comparison.json')
    for r in rows:
        if r['stage']==141:
            source=next(x for x in source_old['rows'] if x['case_key']==r['key'] and x['model']==r['model']);assert r['target']==source['target'] and r['fallback']==source['fallback']
            jobs=read(ROOT/'artifacts/study_v141/jobs.json');job=next(j for j in jobs if j['key']==r['key']);domains=job['domains']
        else:
            source=next(x for x in source_spark['cases'] if x['key']==r['key'] and x['model']==r['model']);assert r['target']==source['model_best_observed'] and r['fallback']==source['fallback']
            domains=read(ROOT/('artifacts/study_v144/candidates/'+source['app']+'.json'))['domains']
        close(r['features'][1:3],[sum(len(d)>1 for d in domains),np.mean([len(d) for d in domains])])
    folds=read(OUT/'folds.json');report=read(OUT/'comparison.json');receipt=verify(rows,folds,report)
    mutations=[]
    for name in ['reported_gain','call_undercount','held_family_in_training','changed_target']:
        rr,ff,cc=copy.deepcopy(rows),copy.deepcopy(folds),copy.deepcopy(report)
        m=next(iter(ff))
        if name=='reported_gain':cc['models'][m]['policies']['always']['family_mean_gain']+=.1
        elif name=='call_undercount':cc['models'][m]['policies']['always']['calls']-=1
        elif name=='held_family_in_training':ff[m][0]['training_keys'].append(ff[m][0]['held_keys'][0])
        else:rr[0]['target']*=1.1
        try:verify(rr,ff,cc)
        except AssertionError:mutations.append({'mutation':name,'rejected':True})
        else:raise AssertionError('Mutation not rejected: '+name)
    receipt['semantic_mutations']=mutations
    (ART/'replay.json').write_text(json.dumps(receipt,indent=2)+'\n');print(json.dumps(receipt))
if __name__=='__main__':main()
