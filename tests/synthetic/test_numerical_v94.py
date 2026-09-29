from types import SimpleNamespace
import numpy as np
import pytest
from scipy.sparse import csc_matrix
from escalation.numerical_v94 import candidates, options, linear_certificate, lp_certificate
from escalation.core import initial_state
from escalation.finite_domain import recommend
from escalation.selection_v8 import shortlist
from escalation.transfer_v41 import messages, rank

def test_domains_and_illegal_options():
    assert len(candidates('superlu').x)==400
    assert len(candidates('highs').x)==240
    assert options('superlu',(3,.1,4,16))['permc_spec']=='COLAMD'
    with pytest.raises(ValueError):options('highs',(1,0,0,99,0))

def test_linear_certificate_rejects_wrong_solution():
    a=csc_matrix([[2.,1.],[0.,3.]]);truth=np.array([1.,2.]);b=a@truth
    assert linear_certificate(a,b,truth,truth)['valid']
    assert not linear_certificate(a,b,truth+1.,truth)['valid']
    assert not linear_certificate(a,b,truth*np.nan,truth)['valid']

def lp():
    # min x, x >= 2, x >= 0; primal=dual=2 with row dual=1.
    return SimpleNamespace(num_row_=1,num_col_=1,offset_=0.,col_cost_=[1.],col_lower_=[0.],col_upper_=[np.inf],
        row_lower_=[2.],row_upper_=[np.inf],a_matrix_=SimpleNamespace(value_=[1.],index_=[0],start_=[0,1]))

@pytest.mark.parametrize('x,y,z,valid', [([2.],[1.],[0.],True),([1.],[1.],[0.],False),
    ([3.],[1.],[0.],False),([2.],[0.],[0.],False),([2.],[-1.],[2.],False)])
def test_lp_independent_certificate(x,y,z,valid):
    assert lp_certificate(lp(),x,y,z)['valid']==valid

def test_prefix_and_branch_isolation():
    c=candidates('highs');s=initial_state(c,11)
    for j in range(10):
        row=recommend(c,s);s.observe(row,[float(10-j)],c.directions)
    p=shortlist(c,s,11);clone=s.clone();row=rank(c,clone,p['ranked'])[0]
    clone.observe(row,[.01],c.directions)
    assert len(s.ids)==10 and row not in s.ids
    assert not set(p['ranked']) & set(s.ids)
    assert len(messages(c,s,p))==2
