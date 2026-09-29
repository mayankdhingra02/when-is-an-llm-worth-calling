from types import SimpleNamespace
import pytest
from escalation.constrained_v34 import JointOracle,terminal,continuation,MODES

def test_joint_oracle_charges_bad_size_and_rejects_repeated_probe(tmp_path):
    path=tmp_path/'synthetic.csv';path.write_text('x;performance;size\n0;1;bad\n1;2;3\n')
    journal=[];o=JointOracle({'path':str(path),'delimiter':';'},SimpleNamespace(source_ids=[2,3]),journal.append)
    with pytest.raises(ValueError):o.acquire(0)
    assert o.new_accesses==len(journal)==1 and journal[0]['vector_charge']==1
    with pytest.raises(ValueError):o.acquire(0)
    assert o.acquire(1)==[2,3]

def test_terminal_retains_feasible_incumbent_and_cap_equality():
    r=terminal([0,1,2],[[5,10],[1,11],[4,10]],10)
    assert r['best_row']==2 and r['best_runtime']==4 and r['runtime_only_best_violates_cap']

@pytest.mark.parametrize('mode',MODES)
def test_shared_prefix_vector_budget_and_no_hidden_feasibility_filter(mode):
    c=SimpleNamespace(x=[(i%2,i//2) for i in range(40)])
    prefix={'ids':list(range(10)),'labels':[[40-i,10] for i in range(10)],'order':list(range(40)),'size_cap':10}
    import copy
    saved=copy.deepcopy(prefix);charged=[]
    def acquire(i):charged.append(i);return [1,20]
    arm=continuation(c,prefix,list(range(10,30)),mode,list(range(10,20)),acquire)
    assert len(charged)==len(set(charged))==10 and prefix==saved
    assert arm['ids'][:10]==prefix['ids'] and arm['labels'][:10]==prefix['labels'] and arm['best_runtime']==31
    assert arm['infeasible_new_acquisitions']==10 and arm['runtime_only_best_violates_cap']
    if mode!='joint_full':assert set(charged)<=set(range(10,30))
