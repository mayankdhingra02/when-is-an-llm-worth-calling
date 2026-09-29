"""Read-only checks using real saved feasibility plans; mutated plans are test fixtures."""
from pathlib import Path
import pytest
from escalation.planning_v55 import Task
ROOT=Path(__file__).resolve().parents[1]
DATA=ROOT/'artifacts/sources/v55'
PLAN=ROOT/'results/v55_planning_feasibility/trial_0/sas_plan'
pytestmark=pytest.mark.skipif(not PLAN.exists() or not DATA.exists(),reason='Local source/real-plan payload absent')

def test_real_plan_cost_and_invalid_mutations():
    task=Task((DATA/'domain.pddl').read_text(),(DATA/'p05.pddl').read_text())
    plan=PLAN.read_text();lines=plan.splitlines()
    assert task.validate(plan)['cost']=='104'
    # Re-loading an already cached item violates the negative precondition.
    with pytest.raises(ValueError,match='precondition'):
        task.validate(lines[0]+'\n'+plan)
    with pytest.raises(ValueError,match='Goal'):
        task.validate('\n'.join(lines[:-2]))
    assert task.validate(plan.replace('; cost = 104','; cost = 999'))['cost']=='104'
