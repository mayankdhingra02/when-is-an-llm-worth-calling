"""Synthetic isolation checks, never research measurements."""
import copy,sys
from pathlib import Path
import numpy as np
import pytest
sys.path.insert(0,str(Path(__file__).resolve().parents[2]/'scripts'))
import router_v151 as r

def rows():
 rng=np.random.default_rng(149)
 return [{'key':f'g{g}_{i}','group':f'g{g}','features':rng.normal(size=18).tolist(),'gain':float(rng.normal(.01,.05))} for g in range(5) for i in range(6)]

def state(values):return {'ids':list(range(10)),'labels':[[x] for x in values],'order':list(range(60))}

@pytest.mark.parametrize('direction',['minimize','maximize'])
def test_units_and_valid_prefix(direction):
 s=state([1.,2,3,4,5,6,7,8,9,10]);expected=r.trajectory(s,direction);s['labels']=[[x[0]*12345.67] for x in s['labels']]
 np.testing.assert_allclose(r.trajectory(s,direction),expected,atol=1e-14)
 with pytest.raises(ValueError):r.trajectory(state([1]*9),direction)
 bad=state([1]*10);bad['ids'][-1]=0
 with pytest.raises(ValueError):r.trajectory(bad,direction)

@pytest.mark.parametrize('bad',[0.,-1.,float('nan'),float('inf')])
def test_invalid_labels(bad):
 with pytest.raises(ValueError):r.trajectory(state([1]*9+[bad]),'minimize')

def test_constant_prefix():
 f=r.trajectory(state([7]*10),'minimize');assert f[6]==.1;assert all(x==0 for i,x in enumerate(f) if i!=6)

def test_outer_targets_cannot_change_models_thresholds_or_choices():
 rs=rows();a=r.outer(rs,'g4');changed=copy.deepcopy(rs)
 for row in changed:
  if row['group']=='g4':row['gain']=99999.
 b=r.outer(changed,'g4');assert a==b
 for v in a['variants'].values():
  assert 'g4' not in v['model']['training_groups']
  for f in v['inner']:
   assert not {'g4',f['held_group']}&set(f['model']['training_groups'])
   assert not set(f['validation_keys'])&set(f['model']['training_keys'])

@pytest.mark.parametrize('kind',r.KINDS)
def test_reproducible_finite_models(kind):
 rs=rows();a=r.fit(rs,kind);b=r.fit(rs,kind);assert a==b
 assert all(np.isfinite(r.predict(a,x)) for x in rs)

def test_group_weighted_ridge_ignores_within_group_replication():
 rs=rows();fit=r.fit(rs,'ridge_extended');replicated=rs+[copy.deepcopy(x) for x in rs if x['group']=='g0'];other=r.fit(replicated,'ridge_extended')
 for row in rs:assert r.predict(fit,row)==pytest.approx(r.predict(other,row),abs=1e-12)

def test_all_negative_calibration_has_never_available():
 rs=rows()
 for row in rs:row['gain']=-.5
 f=r.outer(rs,'g4')
 assert all(not ds['selected_predictor'] for ds in f['decisions'].values())
 for kind in r.KINDS:assert f['variants'][kind]['calibration']['selected']['threshold'] is None

def test_auc_and_ties():
 assert r.auc([1,0],[True,False])==1
 assert r.auc([0,1],[True,False])==0
 assert r.auc([1,1],[True,False])==.5
 assert r.auc([1,1],[True,True]) is None

def test_predict_ignores_nonfeature_fields():
 rs=rows()
 for kind in r.KINDS:
  m=r.fit(rs,kind);q=copy.deepcopy(rs[0]);expected=r.predict(m,q);q.update(gain=1e9,group='secret',key='new',target=-99)
  assert r.predict(m,q)==expected


def test_reject_cross_system_short_key_collision():
 rs=rows();rs[-1]['key']=rs[0]['key']
 with pytest.raises(ValueError,match='Duplicate analysis case keys'):r.outer(rs,'g4')
 for row in rs:row['key']=row['group']+'::'+row['key']
 f=r.outer(rs,'g4');assert len(f['decisions'])==6
