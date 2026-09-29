import pytest
from escalation.core import State
from escalation.finite_domain import FiniteCandidates
from escalation.shortlist_v25 import restrict,continue_branch

def fixture():
    c=FiniteCandidates(tuple('abcdef'),tuple(tuple(float((i>>j)&1) for j in range(6)) for i in range(64)),('y',),('-',),tuple(range(64)))
    s=State(list(range(64)))
    for i in range(10):s.observe(i,[float(64-i)],['-'])
    return c,s,list(range(10,30))

def test_restriction_preserves_prefix_and_ignores_display_order():
    c,s,pool=fixture();saved=s.record();acquisitions=[]
    def oracle(i):acquisitions.append(i);return [float(64-i)]
    a=continue_branch(c,s,pool,oracle);b=continue_branch(c,s,list(reversed(pool)),lambda i:[float(64-i)])
    assert a.record()==b.record() and s.record()==saved
    assert len(acquisitions)==10 and len(set(a.ids))==20 and set(acquisitions)<=set(pool)
    assert a.labels[:10]==s.labels and a.ids[:10]==s.ids

@pytest.mark.parametrize('pool',[list(range(9,29)),list(range(10,29)),[10]*20,list(range(60,80))])
def test_invalid_pool_fails_before_acquisition(pool):
    c,s,_=fixture()
    with pytest.raises(ValueError):continue_branch(c,s,pool,lambda i:pytest.fail('Unexpected label access'))

def test_outside_pool_targets_cannot_affect_run():
    c,s,pool=fixture();targets={i:float(64-i) for i in range(64)}
    a=continue_branch(c,s,pool,lambda i:[targets[i]])
    for i in set(range(64))-set(pool):targets[i]=-1e9
    b=continue_branch(c,s,pool,lambda i:[targets[i]])
    assert a.record()==b.record()
