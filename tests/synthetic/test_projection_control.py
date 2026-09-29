import itertools
import pytest
from escalation.core import Candidates, initial_state
from escalation.data import Oracle
from escalation.projection_control import UniformProjection, continue_projection, proposal_seed


def fixture(reverse=False):
    x=tuple(itertools.product([0.,1.],repeat=5))
    c=Candidates(tuple('abcde'),x,('Cost-',),('-',),tuple(range(32)))
    labels=tuple((float(31-i if reverse else i),) for i in range(32))
    s=initial_state(c,11)
    o=Oracle(labels)
    for i in s.order[:10]:s.observe(i,o.acquire(i),c.directions)
    return c,labels,s,o


def test_real_projection_control_budget_and_replay():
    c,labels,s,_=fixture()
    prefix=s.record();seed=proposal_seed('dataset-hash',11)
    o=Oracle(labels,prefix=prefix)
    events=continue_projection(c,s,o,seed)
    assert len(events)==10 and o.new_accesses==10
    assert len(set(s.ids))==20
    for event in events:
        assert set(event['proposal']) <= {0,1}
        assert event['proposal_source']=='uniform_domains_projection_v1'
    with pytest.raises(RuntimeError):o.acquire(next(i for i in range(32) if i not in s.ids))


def test_projection_control_cannot_use_outcomes():
    c,y,s,_=fixture();c2,y2,s2,_=fixture(reverse=True)
    o=Oracle(y,prefix=s.record());o2=Oracle(y2,prefix=s2.record())
    e=continue_projection(c,s,o,123);e2=continue_projection(c2,s2,o2,123)
    assert e==e2 and s.ids==s2.ids
    assert s.labels!=s2.labels


def test_seed_and_rng_isolation():
    c,_,s,_=fixture()
    a=UniformProjection(c,44);b=UniformProjection(c,44)
    assert a.propose_batch()==b.propose_batch()
    UniformProjection(c,13).propose_batch()
    assert a.propose_batch()==b.propose_batch()
    assert proposal_seed('a',1)!=proposal_seed('a',2)
    assert proposal_seed('a',1)!=proposal_seed('b',1)
    with pytest.raises(ValueError):a.propose_batch(0)
