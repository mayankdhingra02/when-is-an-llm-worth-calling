"""Acquired-only classical selection for the frozen native H2 domain."""
import random
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from escalation.h2_v83 import grid, PROFILES
SEEDS=[11,23,37,53,71]
ARMS=['rf_lcb','random','prior']
CONFIGS=grid()
PRIOR=CONFIGS.index(PROFILES['prior'])

def features():
    return np.array([[float(bool(c['mask'] & (1<<i))) for i in range(6)]+[float(c['recompile'])]+[float(c['analyze_sample']==a) for a in [0,100,2000,10000]] for c in CONFIGS])

def choose(observations,method,seed):
    ids=[o['config_id'] for o in observations]
    remaining=[i for i in range(len(CONFIGS)) if i not in ids]
    if not remaining:raise ValueError('Domain exhausted')
    if method=='random':return random.Random(seed*1000+len(ids)).choice(remaining)
    if method!='rf_lcb' or not ids:raise ValueError('Unsupported method or empty history')
    y=np.log([o['query_seconds'] for o in observations])
    if not np.all(np.isfinite(y)):raise ValueError('Invalid acquired durations')
    x=features();forest=RandomForestRegressor(n_estimators=64,min_samples_leaf=1,max_features=1.,bootstrap=True,n_jobs=1,random_state=seed*100+len(ids))
    forest.fit(x[ids],y);p=np.array([tree.predict(x[remaining]) for tree in forest.estimators_])
    return remaining[int(np.argmin(p.mean(axis=0)-p.std(axis=0)))]

def prefix_choice(observations,seed):
    if not observations:return PRIOR
    return choose(observations,'random' if len(observations)<5 else 'rf_lcb',seed)

def incumbent(observations):
    if not observations:raise ValueError('Empty history')
    return min(observations,key=lambda o:(o['query_seconds'],o['config_id']))['config_id']

def guard(cid,observations,purpose):
    if type(cid) is not int or not 0<=cid<len(CONFIGS):raise ValueError('Invalid candidate')
    if len(observations)>=20:raise ValueError('Per-arm budget exhausted')
    if purpose not in ['search','confirmation','fixed_prior']:raise ValueError('Invalid purpose')
    if purpose=='search' and cid in {o['config_id'] for o in observations}:raise ValueError('Duplicate search')
    if purpose=='confirmation' and len(observations)<17:raise ValueError('Premature confirmation')
