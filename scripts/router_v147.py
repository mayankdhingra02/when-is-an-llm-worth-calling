"""Exploratory nested group evaluation, confined to previously collected real traces."""
import argparse
import hashlib
import json
import math
import time
from fractions import Fraction
from pathlib import Path
import numpy as np
from router_v132 import FEATURES, features

ROOT = Path(__file__).resolve().parents[1]
ART = ROOT/'artifacts/study_v147'
OUT = ROOT/'results/v147_router'
MODELS = ['smollm3_3b', 'qwen3_8b']
SETS = {'all': list(range(7)), 'no_cardinality': [0,1,3,4,5,6], 'trajectory': [3,4,5,6]}

def read(path):
    return json.loads(Path(path).read_text())

def write(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2, sort_keys=True, allow_nan=False)+'\n')

def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()

def weights(rows):
    groups = [r['group'] for r in rows]
    return np.array([1/(len(set(groups))*groups.count(g)) for g in groups])

def fit(rows, indices):
    x = np.array([[r['features'][i] for i in indices] for r in rows], float)
    y = np.array([r['gain'] for r in rows]); w = weights(rows)
    assert np.isfinite(x).all() and np.isfinite(y).all()
    mean = w@x; scale = np.sqrt(w@((x-mean)**2)); scale[scale<1e-12] = 1
    z = (x-mean)/scale; intercept = float(w@y)
    coef = np.linalg.solve(z.T@(w[:,None]*z)+np.eye(len(indices)), z.T@(w*(y-intercept)))
    return {'indices':indices,'mean':mean.tolist(),'scale':scale.tolist(),'coef':coef.tolist(),
            'intercept':intercept,'alpha':1.,'min':x.min(axis=0).tolist(),'max':x.max(axis=0).tolist()}

def predict(model, row):
    x = np.array([row['features'][i] for i in model['indices']])
    return float(((x-model['mean'])/model['scale'])@model['coef']+model['intercept'])

def quantile(scores, rows, q):
    order = np.argsort(scores, kind='stable'); w = weights(rows)[order]
    return float(np.asarray(scores)[order[min(int(np.searchsorted(np.cumsum(w),q,side='left')),len(order)-1)]])

def select(scores, rows):
    candidates = sorted(set([0.] + [quantile(scores,rows,q) for q in [0,.25,.5,.75,1]]))+[None]
    w = weights(rows); y = np.array([r['gain'] for r in rows]); grid = []
    for t in candidates:
        d = np.zeros(len(rows),bool) if t is None else np.array(scores)>=t
        grid.append({'threshold':t,'gain':float(w@(y*d)),'rate':float(w@d)})
    top = max(r['gain'] for r in grid)
    chosen = min((r for r in grid if r['gain']>=top-1e-12),
                 key=lambda r:(r['rate'], -math.inf if r['threshold'] is None else -r['threshold']))
    return {'selected':chosen,'grid':grid}

def outer_fold(rows, held):
    train = [r for r in rows if r['group'] != held]
    test = [r for r in rows if r['group'] == held]
    assert train and test and held not in {r['group'] for r in train}
    groups = sorted({r['group'] for r in train})
    result = {'held_group':held,'training_keys':[r['key'] for r in train], 'training_groups':groups,
              'held_keys':[r['key'] for r in test], 'variants':{}}
    decisions = {r['key']:{'never':False,'always':True} for r in test}
    for name, indices in SETS.items():
        inner = []; scores_by_key = {}
        for g in groups:
            dev = [r for r in train if r['group'] != g]; val = [r for r in train if r['group'] == g]
            model = fit(dev,indices); scores = [predict(model,r) for r in val]
            inner.append({'held_group':g,'training_keys':[r['key'] for r in dev], 'validation_keys':[r['key'] for r in val], 'model':model, 'scores':scores})
            scores_by_key.update({r['key']:s for r,s in zip(val,scores)})
        scores = [scores_by_key[r['key']] for r in train]
        calibration = select(scores,train); threshold = calibration['selected']['threshold']
        model = fit(train,indices); test_scores = {r['key']:predict(model,r) for r in test}
        support = {r['key']:[FEATURES[i] for j,i in enumerate(indices) if r['features'][i]<model['min'][j] or r['features'][i]>model['max'][j]] for r in test}
        result['variants'][name] = {'model':model,'inner_folds':inner,'calibration':calibration,'outer_scores':test_scores,'outside_training_range':support}
        for r in test:
            decisions[r['key']]['benefit_'+name] = threshold is not None and test_scores[r['key']]>=threshold
        if name == 'all':
            t = quantile(scores,train,.8); result['benefit_80pct_threshold'] = t
            for r in test: decisions[r['key']]['benefit_80pct'] = test_scores[r['key']]>=t
    scores = [r['features'][-1] for r in train]; cal = select(scores,train); t = cal['selected']['threshold']
    result['uncertainty_calibration'] = cal
    u80 = quantile(scores,train,.8); result['uncertainty_80pct_threshold'] = u80
    for r in test:
        decisions[r['key']]['uncertainty'] = t is not None and r['features'][-1]>=t
        decisions[r['key']]['uncertainty_80pct'] = r['features'][-1]>=u80
    result['decisions'] = decisions
    return result

def prepare():
    assert not (ART/'inputs.json').exists()
    used = set()
    def load(n):
        used.add(n); return read(ROOT/n)
    a = load('results/v141_analysis/comparison.json'); b = load('results/v145_spark/comparison.json')
    oldjobs = load('artifacts/study_v141/jobs.json'); sparkjobs = load('artifacts/study_v144/jobs.json')
    rows = []
    paths = load('artifacts/study_v142/model_paths.json')
    raw = {}
    for m in MODELS:
        raw[m] = {}
        for folder in [paths[m]] + (['results/v144_models/'+m] if m=='smollm3_3b' else []) + ['results/v145_models/'+m]:
            n=folder+'/responses.jsonl'; used.add(n)
            for line in (ROOT/n).read_text().splitlines():
                r=json.loads(line); assert r['key'] not in raw[m]; raw[m][r['key']]=r
    for stage,jobs in [(141,oldjobs),(145,sparkjobs)]:
        for j in jobs:
            p=load(j['prefix']); assert sha(ROOT/j['prefix'])==j['prefix_sha256']; state=p.get('state',p)
            assert len(state['ids'])==len(set(state['ids']))==len(state['labels'])==10
            if stage==141:
                matching=[r for r in a['rows'] if r['case_key']==j['key']]; assert len(matching)==2
                direction='minimize' if matching[0]['direction']=='-' else 'maximize'; domains=j['domains']
            else:
                matching=[r for r in b['cases'] if r['key']==j['key']]; assert len(matching)==2
                direction='minimize'; domains=load('artifacts/study_v144/candidates/'+j['app']+'.json')['domains']
            f=features(state,domains,direction)
            for m in MODELS:
                r=next(r for r in matching if r['model']==m)
                if stage==141:
                    gain=float(Fraction(r['gains']['sequential_3nn'])); adaptive=float(Fraction(r['gains']['adaptive_incumbent_neighbor']))
                    prefix_best=min(v[0] for v in state['labels']) if direction=='minimize' else max(v[0] for v in state['labels'])
                    actual=r['target']; baseline=r['references']['sequential_3nn']; adapt=r['references']['adaptive_incumbent_neighbor']
                else:
                    assert all(r['contrasts'][k]['scorable'] for k in ['sequential_3nn','adaptive_neighbor'])
                    gain=r['contrasts']['sequential_3nn']['gain'];adaptive=r['contrasts']['adaptive_neighbor']['gain']
                    actual=r['model_best_observed'];baseline=r['control_best_observed']['sequential_3nn'];adapt=r['control_best_observed']['adaptive_neighbor'];prefix_best=r['prefix_best']
                sign=1 if direction=='minimize' else -1
                assert math.isclose(gain,sign*(baseline-actual)/baseline,abs_tol=1e-14)
                response=raw[m].get(j['key']); usage=response['response'] if response else {}
                rows.append({'key':j['key'],'model':m,'stage':stage,'group':j['system_group'],'seed':j['seed'],
                             'features':f,'gain':gain,'adaptive_gain':adaptive,'fallback':r['fallback'],
                             'target':actual,'sequential':baseline,'adaptive':adapt,'prefix_best':prefix_best,'direction':direction,
                             'prefix':j['prefix'],'prefix_sha256':j['prefix_sha256'],
                             'usage':{'generated_tokens':usage.get('tokens_predicted'),'prefill_tokens':usage.get('tokens_evaluated'),
                                      'request_seconds':response['wall_seconds'] if response else None}})
    rows.sort(key=lambda r:(r['model'],r['group'],r['key']))
    assert len(rows)==110 and len({(r['model'],r['key']) for r in rows})==110
    assert len({r['group'] for r in rows})==7 and sum(r['fallback'] for r in rows)==1
    for m in MODELS:
        assert len([r for r in rows if r['model']==m])==55
    write(ART/'inputs.json',{'scope':'exploratory reuse of sealed measured outputs; zero new acquisitions or inference', 'feature_names':FEATURES,'rows':rows})
    used.update(['scripts/router_v147.py','scripts/report_router_v147.py','scripts/verify_router_v147.py',
                 'scripts/router_v132.py','reports/protocol_v147.md','tests/synthetic/test_router_v147.py','artifacts/study_v147/inputs.json'])
    write(ART/'freeze.json',{'frozen_unix':time.time(),'sha256':{n:sha(ROOT/n) for n in sorted(used)}})
    print('Frozen 110 paired model-cases across seven families; no new collection.')

def summaries(rows, folds):
    groups=sorted({r['group'] for r in rows}); bykey={k:v for f in folds for k,v in f['decisions'].items()}
    policies=list(next(iter(bykey.values()))); summary={}
    for policy in policies:
        pergroup=[]; random_draws=np.zeros(10000)
        for g in groups:
            cases=[r for r in rows if r['group']==g]; d=np.array([bykey[r['key']][policy] for r in cases]); y=np.array([r['gain'] for r in cases]); z=np.array([r['adaptive_gain'] for r in cases]); n=len(cases); k=int(d.sum())
            # If not escalating, the reference action is sequential3NN. Assess that action against adaptive too.
            seq_vs_adapt=np.array([(r['adaptive']-r['sequential'])/r['adaptive']*(1 if r['direction']=='minimize' else -1) for r in cases])
            seed=int(hashlib.sha256((policy+'|'+g).encode()).hexdigest()[:12],16)+147000
            rng=np.random.default_rng(seed)
            draws=np.array([float(y[rng.choice(n,k,replace=False)].sum()/n) for _ in range(10000)])
            random_draws += draws/len(groups)
            selected = rng.choice(n,k,replace=False).tolist()
            chosen=[r for r,v in zip(cases,d) if v]
            pergroup.append({'group':g,'n':n,'calls':k,'gain':float(np.mean(y*d)),
                             'gain_vs_adaptive':float(np.mean(np.where(d,z,seq_vs_adapt))),
                             'random_expected_gain':float(k/n*y.mean()), 'random_one_gain':float(y[selected].sum()/n),
                             'random_selected_keys':[cases[i]['key'] for i in selected],
                             'harmful_calls':int(sum(d & (y<-.01))), 'missed_useful_calls':int(sum(~d & (y>.01))),
                             'useful_calls':int(sum(d & (y>.01))), 'joint_useful_calls':int(sum(d & (y>.01) & (z>.01))),
                             'selected_fallbacks':sum(r['fallback'] for r in chosen),
                             'replayed_observed_request_seconds':sum(r['usage']['request_seconds'] or 0 for r in chosen),
                             'replayed_generated_tokens_lower_bound':sum(r['usage']['generated_tokens'] or 0 for r in chosen),
                             'selected_unknown_usage':sum(r['usage']['generated_tokens'] is None for r in chosen)})
        means=[r['gain'] for r in pergroup]; expected=float(np.mean([r['random_expected_gain'] for r in pergroup]))
        summary[policy]={'family_mean_gain':float(np.mean(means)), 'pooled_mean_gain':float(sum(r['gain']*r['n'] for r in pergroup)/len(rows)),
                         'family_mean_gain_vs_adaptive':float(np.mean([r['gain_vs_adaptive'] for r in pergroup])),
                         'family_mean_call_rate':float(np.mean([r['calls']/r['n'] for r in pergroup])),
                         'calls':sum(r['calls'] for r in pergroup),'intended':len(rows),
                         'random_matched_expected_gain':expected,'gain_above_matched_random':float(np.mean(means))-expected,
                         'random_reference_95pct':np.quantile(random_draws,[.025,.975]).tolist(),
                         'leave_one_family_mean_range':[float(min((sum(means)-v)/(len(means)-1) for v in means)),float(max((sum(means)-v)/(len(means)-1) for v in means))],
                         'harmful_calls':sum(r['harmful_calls'] for r in pergroup),'missed_useful_calls':sum(r['missed_useful_calls'] for r in pergroup),
                         'joint_useful_calls':sum(r['joint_useful_calls'] for r in pergroup),'groups':pergroup}
    return summary

def run():
    start=time.monotonic(); cpu=time.process_time(); freeze=read(ART/'freeze.json')
    for n,h in freeze['sha256'].items():assert sha(ROOT/n)==h,n
    assert not OUT.exists(); OUT.mkdir(parents=True)
    rows=read(ART/'inputs.json')['rows']; results={}; allfolds={}
    for m in MODELS:
        rs=[r for r in rows if r['model']==m]; groups=sorted({r['group'] for r in rs})
        folds=[outer_fold(rs,g) for g in groups]; allfolds[m]=folds
        results[m]={'policies':summaries(rs,folds),'hindsight_oracle_family_mean_gain':float(np.mean([np.mean([max(0,r['gain']) for r in rs if r['group']==g]) for g in groups])),
                    'practical_opportunities':sum(r['gain']>.01 for r in rs),'joint_practical_opportunities':sum(r['gain']>.01 and r['adaptive_gain']>.01 for r in rs),
                    'groups_with_practical_opportunity':sorted({r['group'] for r in rs if r['gain']>.01})}
        assert time.monotonic()-start<600
    write(OUT/'folds.json',allfolds);write(OUT/'comparison.json',{'models':results,'families':7,'cases_per_model':55,'new_model_requests':0,'new_acquisitions':0,'exploratory':True})
    write(ART/'runtime.json',{'wall_seconds':time.monotonic()-start,'cpu_seconds':time.process_time()-cpu,'limit_seconds':600,'freeze_sha256':sha(ART/'freeze.json')})
    print(json.dumps({m:{p:{k:d[k] for k in ['calls','family_mean_gain','gain_above_matched_random']} for p,d in r['policies'].items()} for m,r in results.items()},indent=2))

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('command',choices=['prepare','run']);a=p.parse_args()
    prepare() if a.command=='prepare' else run()
