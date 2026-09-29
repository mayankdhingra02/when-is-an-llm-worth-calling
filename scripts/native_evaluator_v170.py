"""Evaluator-only dispatch to frozen workers; owner optimizer cannot read this state."""
import json,math
from collect_smollm_v47 import ROOT,read
from solver_worker_v157 import valid_queens
from app_validation_v163 import Reference
ENGINES=['cvc5','ortools','ripgrep','hnswlib']
REFERENCE=None
def stage(engine):return 159 if engine in ['cvc5','ortools'] else 163
def candidate(engine):return read(ROOT/f'artifacts/study_v{stage(engine)}/candidates/{engine}.json')
def command(engine,i,c):
    if engine in ['cvc5','ortools']:
        return [str(ROOT/'.venv-solvers156/bin/python'),str(ROOT/'scripts/solver_worker_v157.py'),'--engine',engine,'--config',json.dumps(c['configs'][i]),'--n',str(c['n']),'--limit','10']
    return [str(ROOT/'.venv/bin/python'),str(ROOT/'scripts/app_worker_v162.py'),'--engine',engine,'--config',json.dumps(c['configs'][i])]
def validate(raw,engine,c,i):
    global REFERENCE
    assert raw['engine']==engine and raw['config']==c['configs'][i]
    if engine in ['cvc5','ortools']:
        assert raw['n']==c['n'] and raw['limit']==10 and math.isfinite(raw['solve_seconds']) and 0<raw['solve_seconds']<60
        valid=valid_queens(raw['rows'],c['n']);assert valid==raw['correct']
        if valid:
            assert raw['status'] in ['sat','OPTIMAL','FEASIBLE'];value=raw['solve_seconds'];status='correct'
        else:
            assert not raw['rows'] and raw['status'] in ['unknown (TIMEOUT)','UNKNOWN'];value=20.;status='quality_penalty'
        return {**raw,'quality':float(valid),'value':value,'objective_seconds':raw['solve_seconds'],'native_invocations':1},status
    if REFERENCE is None:REFERENCE=Reference(recompute=False)
    value=REFERENCE.validate(raw);assert math.isfinite(value)
    return raw,'correct' if raw['quality']>=.95 else 'quality_penalty'
