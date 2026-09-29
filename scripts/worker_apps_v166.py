"""One native configuration outcome. No optimizers, LLMs or hidden timing tables."""
import argparse, hashlib, json, os, sys, time
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'.local-runtime/apps-v166'))
sys.path.insert(0,str(ROOT/'src'))
def polars_work(config):
    os.environ['POLARS_MAX_THREADS']=str(config['threads'])
    import polars as pl
    from escalation.flights_v88 import SCHEMAS,COLUMNS
    tables={k:pl.scan_csv(ROOT/f'data/flights_v88/normalized/{k}.csv',schema={n:pl.Int64 if typ=='INTEGER' else pl.String for n,typ in schema},null_values='') for k,schema in SCHEMAS.items()}
    f=tables['flights'];a=tables['airlines'];d=tables['airports'];p=tables['planes']
    q1=f.join(a,on='carrier').group_by(['month','name']).agg(pl.len().alias('flights'),pl.col('arr_delay').is_null().sum().alias('missing_arrival_delay'),pl.when(pl.col('arr_delay')>0).then(pl.col('arr_delay')).otherwise(0).sum().alias('positive_delay_minutes'))
    q2=f.join(d,left_on='dest',right_on='faa').filter(pl.col('alt')>500).group_by(['origin','dest','name']).agg(pl.len().alias('flights'),pl.col('distance').sum().alias('distance_miles'))
    q3=f.join(p,on='tailnum').join(a,on='carrier').join(d.select(['faa','tzone']),left_on='dest',right_on='faa').filter(pl.col('month').is_between(6,8)&(pl.col('arr_delay')>0)&(pl.col('plane_year')<2000)&pl.col('tzone').str.starts_with('America/')).group_by(['manufacturer','name']).agg(pl.len().alias('flights'),pl.col('arr_delay').sum().alias('delay_minutes'))
    frames=[q.select(COLUMNS[name]).sort(COLUMNS[name][:len(COLUMNS[name])-n]) for (name,q,n) in [('monthly_carriers',q1,3),('high_airport_routes',q2,2),('summer_aircraft',q3,2)]]
    opts=pl.QueryOptFlags(**{k:config[k] for k in ['predicate_pushdown','projection_pushdown','comm_subplan_elim']})
    t=time.perf_counter(); outputs=pl.collect_all(frames,engine=config['engine'],optimizations=opts);elapsed=time.perf_counter()-t
    return {'seconds':elapsed,'version':pl.__version__,'thread_pool_size':pl.thread_pool_size(),'answers':{n:out.rows() for n,out in zip(COLUMNS,outputs)},'query_executions':3}
def xgboost_work(config):
    import numpy as np
    import xgboost as xgb
    data=np.load(ROOT/'artifacts/study_v166/covertype.npz')
    params={'nthread':config['threads'],'max_bin':config['max_bin'],'max_depth':config['max_depth'],'tree_method':'hist','device':'cpu','objective':'multi:softmax','num_class':7,'eta':0.3,'seed':16601,'verbosity':0}
    t=time.perf_counter()
    train=xgb.DMatrix(data['train_x'],label=data['train_y'],nthread=config['threads']);valid=xgb.DMatrix(data['valid_x'],nthread=config['threads'])
    booster=xgb.train(params,train,num_boost_round=config['rounds']);pred=booster.predict(valid);elapsed=time.perf_counter()-t
    assert pred.shape==(8192,) and np.isin(pred,range(7)).all()
    return {'seconds':elapsed,'version':xgb.__version__,'accuracy':float(np.mean(pred==data['valid_y'])),'predictions':pred.astype(int).tolist(),'booster_config':json.loads(booster.save_config()),'booster_sha256':hashlib.sha256(booster.save_raw()).hexdigest(),'query_executions':1}
def main():
    ap=argparse.ArgumentParser();ap.add_argument('--engine',choices=['polars','xgboost'],required=True);ap.add_argument('--candidate',type=int,required=True);args=ap.parse_args()
    candidates=json.loads((ROOT/'artifacts/study_v166/candidates.json').read_text());config=candidates[args.engine][args.candidate]
    out=(polars_work if args.engine=='polars' else xgboost_work)(config)
    print(json.dumps({'engine':args.engine,'candidate':args.candidate,'config':config,**out}))
if __name__=='__main__':main()
