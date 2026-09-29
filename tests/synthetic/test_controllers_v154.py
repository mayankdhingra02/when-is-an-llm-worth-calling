"""Synthetic-only fixtures; never included in measured research aggregates."""
import copy,sys
from pathlib import Path
import numpy as np
import pytest
sys.path.insert(0,str(Path(__file__).resolve().parents[2]/'scripts'))
import controllers_v154 as c

def case():
 return {'key':'synthetic::fixture','seed':11,'ids':list(range(10)),'labels':[10.,9,8,7,7,7,7,7,7,7],'raw_features':[[float(i),str(i%2),1] for i in range(20)],'direction':'minimize'}

def test_encoding_constant_and_nominal():
 x,cat=c.encode(case()['raw_features']);assert x.shape==(20,2);assert cat.tolist()==[False,True];assert x[0,0]==0 and x[-1,0]==1

def test_kernel_psd_and_category_renaming():
 a=case();x,t=c.encode(a['raw_features']);k=c.kernel(x,x,t,.2);assert np.min(np.linalg.eigvalsh(k))>0;assert np.allclose(k,k.T)
 for r in a['raw_features']:r[1]={'0':'z','1':'a'}[r[1]]
 z,ct=c.encode(a['raw_features']);assert np.allclose(k,c.kernel(z,z,ct,.2))

def test_gp_matches_direct_conditioning():
 x,t=c.encode(case()['raw_features']);y=np.arange(8.)**2;test=x[8:]
 pred,sd=c.gp(x[:8],y,test,t,1.);k=c.kernel(x[:8],x[:8],t,1.)+np.eye(8)*1e-6;cross=c.kernel(x[:8],test,t,1.)
 assert np.allclose(pred,y.mean()+cross.T@np.linalg.solve(k,y-y.mean()))
 assert np.allclose(sd**2,1-np.einsum('ij,ij->j',cross,np.linalg.solve(k,cross)))

def test_unit_scaling():
 a=case();b=copy.deepcopy(a);b['labels']=[1000*v for v in a['labels']];x=c.signals(a,1.);y=c.signals(b,1.)
 for k in ['p_llm','bora_action','bora_capped_action','rank_draw_call','uncertainty_ratio']:assert x[k]==y[k]

def test_no_targets_or_unacquired_labels_accessed():
 a=case();first=c.signals(a,1.);a.update(hidden_objectives=[-1e12]*20,gain=999,continuation={'labels':[1e20]});assert c.signals(a,1.)==first

def test_six_post_initialization_improvements():
 yes,changes=c.plateau(case()['labels'],'minimize',6);assert yes and changes==[0.]*6
 assert not c.plateau(case()['labels'],'minimize',7)[0]
 assert not c.plateau([10,9,8,7,7,7,7,7,7,6],'minimize',6)[0]
 assert c.plateau([1,2,3,4,4,4,4,4,4,4],'maximize',6)[0]

def test_rank_ties_preserved_neutral():
 assert c.tau_pair(np.array([1,2]),np.array([2,1]))==-1
 assert c.tau_pair(np.array([1,2]),np.array([1,2]))==1
 assert c.tau_pair(np.array([1,1]),np.array([1,2])) is None
 a=case();a['labels']=[7.]*10;s=c.signals(a,1.);assert s['undefined_folds']==5 and s['p_llm']==.5

def test_cv_disjoint_coverage_and_monitor_fixed():
 s=c.signals(case(),1.);assert sorted(i for f in s['rank_folds'] for i in f['held_positions'])==list(range(10))
 for f in s['rank_folds']:assert not set(f['train_positions'])&set(f['held_positions']);assert len(f['train_positions'])==8
 assert len(s['uncertainty_trace'])==7 and len(s['monitor_ids'])==20

@pytest.mark.parametrize('error',['duplicate','short','negative','nan','row','direction'])
def test_bad_prefix_rejected(error):
 a=case()
 if error=='duplicate':a['ids'][1]=a['ids'][0]
 if error=='short':a['labels'].pop()
 if error=='negative':a['labels'][0]=-1
 if error=='nan':a['labels'][0]=float('nan')
 if error=='row':a['ids'][0]=100
 if error=='direction':a['direction']='unknown'
 with pytest.raises(ValueError):c.signals(a,1.)

def test_held_outcome_changes_cannot_change_calibration():
 rows=[{'key':str(i),'group':str(i//2),'gain':.1*(i%2)} for i in range(6)];sig={r['key']:{'1.0':{'uncertainty_ratio':.5,'p_llm':.3,'bora_action':'a1','bora_capped_action':'a2','rank_draw_call':False},'0.2':{'bora_action':'a1','bora_capped_action':'a2','p_llm':.3,'rank_draw_call':False}} for r in rows}
 old=[{'held_group':g,'decisions':{r['key']:{'selected_predictor':False,'uncertainty':False} for r in rows if r['group']==g}} for g in ['0','1','2']]
 d,f=c.policies(rows,'engine',sig,old);changed=copy.deepcopy(rows)
 for r in changed:
  if r['group']=='0':r['gain']=-100
 dd,ff=c.policies(changed,'engine',sig,old)
 assert f[0]==ff[0] and d['0']==dd['0'] and d['1']==dd['1']

def test_expected_aggregate_and_no_call_adaptive_reference():
 rows=[{'key':str(i),'group':'a','gain':g,'adaptive_gain':g/2,'sequential':10,'adaptive':20,'direction':'minimize','usage':{'generated_tokens':10,'request_seconds':1},'fallback':False} for i,g in enumerate([.2,-.1])]
 d={'0':{'rank_expected_1.0':.5,'never':0},'1':{'rank_expected_1.0':.25,'never':0}};out=c.aggregate(rows,d)
 assert out['rank_expected_1.0']['calls']==.75
 assert out['rank_expected_1.0']['family_mean_gain']==pytest.approx(.0375)
 assert out['never']['family_mean_gain_vs_adaptive']==.5
