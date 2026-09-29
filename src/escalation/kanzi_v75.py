"""Exploratory compression-size search: features and acquired bytes only."""
import itertools,math
import numpy as np
from sklearn.ensemble import RandomForestRegressor
TRANSFORMS=['LZ','LZX','LZP','LZ+RLT','BWT+RANK+ZRLT','TEXT+BWT+RANK+ZRLT','TEXT+BWT+SRT+ZRLT','LZP+TEXT+BWT+LZP']
CODECS=['HUFFMAN','ANS0','ANS1','RANGE','FPAQ','CM','TPAQ']
BLOCKS=[2**i for i in range(14,22)]
SEEDS=[11,23,37,53,71]
METHODS=['random','nn','rf_lcb']
def grid():
    return [dict(transform=t,entropy=e,block_bytes=b,jobs=1) for t,e,b in itertools.product(TRANSFORMS,CODECS,BLOCKS)]
def features(configs):
    return np.array([[float(c['transform']==t) for t in TRANSFORMS]+[float(c['entropy']==e) for e in CODECS]+[(math.log2(c['block_bytes'])-14)/7] for c in configs])
def choose(x,observations,method,seed,rng=None):
    ids=[o['config_id'] for o in observations];remaining=[i for i in range(len(x)) if i not in ids]
    if not remaining:raise ValueError('No remaining candidate')
    if method=='random':return rng.choice(remaining)
    y=np.array([o['compressed_bytes'] for o in observations])
    if method=='nn':
        distance=np.abs(x[remaining,None,:]-x[ids][None,:,:]).mean(axis=2)
        near=np.argsort(distance,axis=1,kind='stable')[:,:3];scores=y[near].mean(axis=1)
    elif method=='rf_lcb':
        forest=RandomForestRegressor(n_estimators=64,min_samples_leaf=1,max_features=1.0,bootstrap=True,n_jobs=1,random_state=seed*100+len(ids))
        forest.fit(x[ids],y);p=np.array([t.predict(x[remaining]) for t in forest.estimators_]);scores=p.mean(axis=0)-p.std(axis=0)
    else:raise ValueError('Unknown policy')
    return remaining[int(np.argmin(scores))]
def guard(cid,observations,purpose,count):
    if type(cid) is not int or not 0<=cid<448:raise ValueError('Invalid configuration')
    if len(observations)>=20 or count>=200:raise ValueError('Budget exhausted')
    if purpose not in ['search','confirmation']:raise ValueError('Invalid purpose')
    if purpose=='search' and cid in {o['config_id'] for o in observations}:raise ValueError('Duplicate search')
