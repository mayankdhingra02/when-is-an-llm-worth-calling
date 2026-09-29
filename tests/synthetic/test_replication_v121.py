import sys,json,copy
from pathlib import Path
import pytest
sys.path.insert(0,str(Path(__file__).resolve().parents[2]/'scripts'))
from fit_router_v121 import fit,KEYS,predict,train
from prepare_model_v121 import blinded

def rows():return [{'system_group':g,'features':{k:float(i+j) for j,k in enumerate(KEYS)},'y':(-1)**i*.1} for i,g in enumerate(['a','b','c','d'])]
def test_test_family_rejected():
    rs=rows();rs[0]['system_group']='mongodb'
    with pytest.raises(ValueError):fit(rs,'y')
def test_fold_does_not_contain_own_family():
    s=train(rows(),'y')
    assert all(f['held_development_family'] not in f['training_families'] for f in s['oof']['folds'])
def test_blinding_only_losses_and_no_input_mutation():
    m=[{'role':'system','content':'test'},{'role':'user','content':'lead\n'+json.dumps({'observations':[{'x':'001','loss':.7},{'x':'102','loss':.2}],'candidates':[{'id':'A','x':'002'}]})}];old=copy.deepcopy(m);b=blinded(m)
    assert m==old and b[0]==m[0];body=json.loads(b[1]['content'].split('\n',1)[1]);assert [v['loss'] for v in body['observations']]==[.5,.5]
    assert body['candidates']==json.loads(m[1]['content'].split('\n',1)[1])['candidates']
def test_fitting_ignores_nonfeature_future_fields():
    rs=rows();a=fit(rs,'y')
    for r in rs:r['post_decision_rank']=10000
    assert fit(rs,'y')==a
