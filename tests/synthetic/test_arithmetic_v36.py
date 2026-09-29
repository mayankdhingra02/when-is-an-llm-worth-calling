from types import SimpleNamespace
from copy import deepcopy
import pytest
from escalation.arithmetic_v36 import choose,Oracle,continuation

def test_exact_arithmetic_resolves_mathematical_tie_by_order():
    c=SimpleNamespace(x=[(0,0),(0,1),(1,1),(0,0),(1,1)])
    selected,trace=choose(c,[4,3],[0,1,2],[['9007199254740992','1'],['1','1'],['1','1']],'1')
    assert selected==4 and trace['runtime_sum_fraction']=='9007199254740994' and trace['predicted_feasible']

def test_cap_equality_and_fallback_use_exact_acquired_size():
    c=SimpleNamespace(x=[(i,) for i in range(5)])
    _,trace=choose(c,[4,3],[0,1,2],[['1','0.1'],['2','0.2'],['3','0.3']],'0.2')
    assert trace['size_sum_fraction']=='3/5' and trace['predicted_feasible']
    assert not choose(c,[4,3],[0,1,2],[['1','0.1'],['2','0.2'],['3','0.3']],'0.199')[1]['predicted_feasible']

def test_bad_value_charged_and_duplicate_rejected(tmp_path):
    p=tmp_path/'synthetic.csv';p.write_text('x;performance;size\n0;1;bad\n')
    events=[];o=Oracle({'path':str(p),'delimiter':';'},SimpleNamespace(source_ids=[2]),{'ids':[]},events.append)
    with pytest.raises(ValueError):o.acquire(0)
    assert o.new_accesses==1 and events[0]['vector_charge']==1
    with pytest.raises(ValueError):o.acquire(0)

@pytest.mark.parametrize('mode',['joint_shortlist','joint_full'])
def test_shared_prefix_and_budget_include_infeasible_rows(mode):
    p={'ids':list(range(10)),'labels':[['10','2'] for _ in range(10)],'order':list(range(40)),'size_cap':'2'};old=deepcopy(p)
    c=SimpleNamespace(x=[(i,) for i in range(40)]);charged=[]
    def acquire(i):charged.append(i);return ['1','3']
    r=continuation(c,p,list(range(10,30)),mode,acquire)
    assert p==old and len(charged)==len(set(charged))==10 and len(set(r['ids']))==20
    assert r['best_runtime']=='10' and r['infeasible_new_acquisitions']==10
