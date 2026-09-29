"""Schema/dispatch checks only; never executes native objective workers."""
import json,sys
from pathlib import Path
import pytest
ROOT=Path(__file__).resolve().parents[2];sys.path.insert(0,str(ROOT/'scripts'))
from native_evaluator_v170 import ENGINES,candidate,command,validate
@pytest.mark.parametrize('engine',ENGINES)
def test_native_domain_and_command(engine):
    c=candidate(engine);assert len(c['configs'])==64
    cmd=command(engine,0,c);assert cmd[cmd.index('--engine')+1]==engine
    assert json.loads(cmd[cmd.index('--config')+1])==c['configs'][0]
@pytest.mark.parametrize('engine',['cvc5','ortools'])
def test_solver_invalid_output_rejected(engine):
    c=candidate(engine);raw={'engine':engine,'config':c['configs'][0],'n':c['n'],'limit':10,'solve_seconds':.1,'rows':[0]*c['n'],'correct':True,'status':'sat'}
    with pytest.raises(AssertionError):validate(raw,engine,c,0)
def test_solver_timeout_retained_as_penalty():
    c=candidate('ortools');raw={'engine':'ortools','config':c['configs'][0],'n':c['n'],'limit':10,'solve_seconds':10.,'rows':[],'correct':False,'status':'UNKNOWN'}
    out,status=validate(raw,'ortools',c,0);assert out['value']==20 and out['objective_seconds']==10 and status=='quality_penalty'
