"""Synthetic boundary checks, not native or model research observations."""
import copy,sys
from pathlib import Path
import numpy as np
import pytest
sys.path.insert(0,str(Path(__file__).resolve().parents[2]/'scripts'))
import native_v131 as n
@pytest.mark.parametrize('task,count',[('wavpack',80),('fftw',36)])
def test_domain(task,count):
 s=n.TASKS[task];assert len(s['xs'])==len(set(s['xs']))==count
 assert s['expert'] in s['xs'] and s['default'] in s['xs'] and s['expert']!=s['default']
def prefix(task):
 p=n.fresh(task,11)
 for i in p['order'][:10]:n.observe(task,p,i,1000000+i)
 return p
@pytest.mark.parametrize('task',['wavpack','fftw'])
def test_prefix_isolation_and_budget(task):
 p=prefix(task);old=copy.deepcopy(p)
 class Fake:
  def acquire(self,t,key,i):assert t==task;return 2000000+i
 r=n.arm(Fake(),task,p,'sequential_3nn',11);assert p==old
 assert len(r['state']['ids'])==len(set(r['state']['ids']))==20
 with pytest.raises(ValueError):n.observe(task,r['state'],next(i for i in p['order'] if i not in r['state']['ids']),1)
 assert n.arm(Fake(),task,p,'sequential_3nn',11)==r
@pytest.mark.parametrize('task',['wavpack','fftw'])
def test_projection_no_extra_targets(task):
 p=prefix(task);x=n.TASKS[task]['xs'][p['ids'][0]]
 ids,diag=n.choices(task,p,'llm',11,[x]*10)
 assert len(set(ids))==10 and not set(ids)&set(p['ids']) and sum(d['repeated_proposal'] for d in diag)==9
def test_numeric_validator_rejects_wrong_finite_and_shape_outputs():
 ref=np.array([1+2j,3-4j]);assert n.numerical_check(ref,ref)['max_absolute_error']==0
 for bad in [ref+1e-3,np.array([complex('nan'),0]),np.array([1])]:
  with pytest.raises(ValueError):n.numerical_check(bad,ref)
def test_zero_invalid_duplicate_labels_rejected():
 p=prefix('fftw')
 for value in [False,0,-1,float('nan'),1.2]:
  with pytest.raises(ValueError):n.observe('fftw',p,next(i for i in p['order'] if i not in p['ids']),value)
 with pytest.raises(ValueError):n.observe('fftw',p,p['ids'][0],2)
