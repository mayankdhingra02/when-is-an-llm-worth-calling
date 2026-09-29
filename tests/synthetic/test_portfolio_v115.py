"""Synthetic acquired-label budget/isolation fixtures, excluded from measurements."""
import sys
from pathlib import Path
import pytest
ROOT=Path(__file__).resolve().parents[2];sys.path.insert(0,str(ROOT/'scripts'))
from portfolio_v115 import portfolio
from escalation.core import State
from escalation.finite_domain import FiniteCandidates

def test_single_arm_budget_and_prefix_isolation():
 c=FiniteCandidates(('a','b'),tuple((i//10,i%10) for i in range(100)),('cost',),('-',),tuple(range(100)))
 prefix=State(list(range(100)))
 for i in range(10):prefix.observe(i,[float(11-i)],c.directions)
 saved=prefix.record();calls=[]
 def acquire(row):
  assert row not in saved['ids'] and row not in calls;calls.append(row);assert len(calls)<=10
  return [float(100-row)]
 s,trace=portfolio(c,prefix,list(range(10,30)),acquire)
 assert prefix.record()==saved and len(calls)==10 and len(s.ids)==20
 assert [t['mode'] for t in trace]==['batch','sequential']*5
 assert all(t['row'] in range(10,30) for t in trace if t['mode']=='batch')
 assert s.ids[:10]==saved['ids'] and s.labels[:10]==saved['labels']

@pytest.mark.parametrize('n',[0,9,11])
def test_bad_prefix_fails_before_any_acquisition(n):
 c=FiniteCandidates(('a',),tuple((i,) for i in range(100)),('cost',),('-',),tuple(range(100)));p=State(list(range(100)))
 for i in range(n):p.observe(i,[1.],c.directions)
 with pytest.raises(ValueError):portfolio(c,p,list(range(20,40)),lambda _:pytest.fail('must not acquire'))
