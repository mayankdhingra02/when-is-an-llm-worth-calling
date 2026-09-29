"""Evaluator-side correctness checks of one acquired result; no hidden timing table."""
import math
import numpy as np
from collect_smollm_v47 import ROOT,read
def check(raw,engine,config):
    assert raw['engine']==engine and raw['config']==config
    seconds=raw['seconds'];assert isinstance(seconds,(int,float)) and math.isfinite(seconds) and 0<seconds<60
    if engine=='polars':
        assert raw['version']=='1.35.2' and raw['thread_pool_size']==config['threads'] and raw['query_executions']==3
        assert raw['answers']==read(ROOT/'data/flights_v88/query_contract.json')['expected']['answers']
        for rows in raw['answers'].values():assert all(type(v) in [str,int] for row in rows for v in row)
        quality=1.
    elif engine=='xgboost':
        assert raw['version']=='3.1.1' and raw['query_executions']==1
        pred=raw['predictions'];assert len(pred)==8192 and all(type(v)==int and 0<=v<7 for v in pred)
        quality=float(np.mean(np.asarray(pred)==np.load(ROOT/'artifacts/study_v166/covertype.npz')['valid_y']));assert raw['accuracy']==quality
        l=raw['booster_config']['learner'];g=l['gradient_booster'];tp=g['tree_train_param']
        assert int(l['generic_param']['nthread'])==config['threads'] and l['generic_param']['device']=='cpu'
        assert int(l['generic_param']['seed'])==16601 and g['gbtree_train_param']['tree_method']=='hist'
        assert int(tp['max_depth'])==config['max_depth'] and int(tp['max_bin'])==config['max_bin']
        assert abs(float(tp['eta'])-.3)<1e-6 and int(g['gbtree_model_param']['num_trees'])==config['rounds']*7
        assert l['objective']['name']=='multi:softmax' and int(l['learner_model_param']['num_class'])==7
    else:raise ValueError('Unknown application')
    feasible=quality>=.75
    return {**raw,'correct':True,'quality':quality,'value':seconds if feasible else 60.,'objective_seconds':seconds,'native_invocations':raw['query_executions']},'correct' if feasible else 'quality_penalty'
