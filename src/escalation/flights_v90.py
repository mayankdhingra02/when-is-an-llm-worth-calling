"""Prospective development grid; no optimizer or router sees these outcomes."""
import random,statistics
CONFIGS=[{'name':f't{t}_j{j}_f{f}','threads':t,'disabled_optimizers':','.join(x for x,off in [('join_order',j),('filter_pushdown',f)] if off)} for t in [1,2,4,8] for j in [0,1] for f in [0,1] if not (j and f)]
BASELINE=6
SEEDS=[11,23,37,53,71]
WARMUP=3
SCORED=64
CHECKED=(WARMUP+SCORED)*3
LIMIT=60

def schedule():
    rows=[]
    for block,seed in enumerate(SEEDS):
        order=list(range(len(CONFIGS)));random.Random(seed).shuffle(order)
        rows.extend({'block':block,'seed':seed,'configuration_index':i} for i in order)
    return rows

def comparison(values,baseline):
    if len(values)!=5 or len(baseline)!=5 or any(v<=0 for v in values+baseline):raise ValueError('Five positive paired block measurements required')
    gains=[1-v/b for v,b in zip(values,baseline)];med=statistics.median(values);spread=(max(values)-min(values))/med
    return {'seconds':values,'median_seconds':med,'range_over_median':spread,'block_relative_gains':gains,'median_block_gain':statistics.median(gains),'precision_screen_pass':med>=.1 and spread<=.2,'material_all_blocks':all(g>=.1 for g in gains),'qualified_descriptive_opportunity':all(g>=.1 for g in gains) and med>=.1 and spread<=.2}
