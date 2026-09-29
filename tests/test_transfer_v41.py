"""Synthetic boundary/direction fixtures, never included in measured aggregates."""
import csv
import random
import pytest
from escalation.core import initial_state
from escalation.finite_domain import FiniteCandidates, recommend
from escalation.selection_v8 import shortlist, messages as legacy_messages
from escalation.transfer_v41 import restrict, rank, branch, messages, IndexedOracle, MODES, relative_gain, current_config

def candidate(direction='-'):
    return FiniteCandidates(('a','b','c','d','e','f'), tuple(tuple((i>>j)&1 for j in range(6)) for i in range(64)), ('target',), (direction,), tuple(range(2,66)))

def prefix(c):
    state = initial_state(c,11)
    for _ in range(10):
        row = recommend(c,state); state.observe(row,[float(row+1)],c.directions)
    return state

@pytest.mark.parametrize('direction', ['-', '+'])
@pytest.mark.parametrize('mode', MODES)
def test_branches_budget_determinism_and_prefix_isolation(direction,mode):
    c = candidate(direction); p = prefix(c); before = p.record(); pool = shortlist(c,p,11)['ranked']; journal=[]
    def acquire(i): journal.append(i); return [float(i+1)]
    a = branch(c,p,pool,11,mode,acquire)
    b = branch(c,p,pool,11,mode,lambda i:[float(i+1)])
    assert a.record()==b.record() and p.record()==before
    assert len(journal)==len(set(journal))==10 and not set(journal)&set(p.ids)
    assert a.ids[:10]==p.ids and a.labels[:10]==p.labels and len(a.ids)==20

def test_maximization_reverses_neighbor_prediction_not_distance():
    c = candidate(); p=prefix(c); pool=shortlist(c,p,11)['ranked']
    low=rank(c,p,pool); high=rank(candidate('+'),p,pool)
    def score(i):
        ns=sorted(range(10),key=lambda j:sum(a!=b for a,b in zip(c.x[i],c.x[p.ids[j]])))[:3]
        return sum(p.labels[j][0] for j in ns)
    assert list(map(score,low))==sorted(map(score,pool))
    assert list(map(score,high))==sorted(map(score,pool),reverse=True)

def test_prompt_equivalent_and_contains_only_acquired_losses():
    c=candidate(); p=prefix(c); pool=shortlist(c,p,11)
    assert messages(c,p,pool)==legacy_messages(c,p,pool)
    with pytest.raises(ValueError): messages(c,initial_state(c,1),pool)

def test_subset_is_feature_only_deterministic():
    c=candidate(); a,ma=restrict(c,{'f':0.0},maximum=30); b,mb=restrict(c,{'f':0.0},maximum=30)
    assert a==b and ma==mb and len(a.x)==30 and all(x[-1]==0 for x in a.x)

def test_hidden_invalid_target_is_unparsed_until_charged(tmp_path):
    c=candidate(); p=tmp_path/'synthetic.csv'
    with p.open('w') as f:
        w=csv.writer(f); w.writerow([*c.names,'target'])
        for i,x in enumerate(c.x):w.writerow([*x,'HIDDEN_INVALID' if i==63 else i+1])
    spec={'path':str(p),'delimiter':',','primary_objective':'target'}; events=[]
    o=IndexedOracle(spec,c,journal=events.append)
    assert o.acquire(0)==[1.0] and len(events)==1
    with pytest.raises(ValueError):o.acquire(63)
    assert o.new_accesses==2 and len(o.acquired)==2 and len(events)==2
    with pytest.raises(ValueError):o.acquire(0)
    assert len(events)==2

def test_oracle_budget_and_restored_prefix(tmp_path):
    c=candidate(); p=tmp_path/'synthetic.csv'
    with p.open('w') as f:
        w=csv.writer(f);w.writerow([*c.names,'target']);w.writerows([*x,i+1] for i,x in enumerate(c.x))
    s=prefix(c);o=IndexedOracle({'path':str(p),'delimiter':',','primary_objective':'target'},c,s.record())
    for i in [i for i in s.order if i not in s.ids][:10]:o.acquire(i)
    with pytest.raises(RuntimeError):o.acquire(next(i for i in s.order if i not in o.acquired))
    assert o.new_accesses==10

def test_gain_direction_and_authorization_unchanged():
    assert relative_gain(100,90,'-')==pytest.approx(.1)
    assert relative_gain(100,110,'+')==pytest.approx(.1)
    cfg=current_config()
    assert cfg['inference']['max_new_model_requests']==230
    assert cfg['inference']['allow_paid_api'] is False
    assert cfg['resources']['max_experiment_runtime_minutes']==60

def test_new_model_phase_rejects_implicit_or_overbroad_authorization(monkeypatch):
    monkeypatch.syspath_prepend('scripts')
    from run_models_v41 import authorized_config
    with pytest.raises(PermissionError): authorized_config({'granted':True},'fixture-freeze')
    fixture={'granted':True,'additional_requests':60,'request_cap':290,'runtime_cap_seconds':3600,
             'stage_seconds':700,'max_new_vectors':600,'external_spend_usd':0,'new_downloads':0,
             'protocol_freeze_sha256':'fixture-freeze','user_authorization':'SYNTHETIC TEST ONLY'}
    assert authorized_config(fixture,'fixture-freeze')['inference']['max_new_model_requests']==290
    with pytest.raises(PermissionError): authorized_config({**fixture,'request_cap':291},'fixture-freeze')
    with pytest.raises(PermissionError): authorized_config(fixture,'wrong-freeze')
