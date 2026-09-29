import pytest
from escalation.sat_v62 import generate,dimacs,parse,validate_model

def test_generated_known_answer_roundtrip():
    clauses,w=generate(20,62001);assert (clauses,w)==generate(20,62001)
    assert parse(dimacs(20,clauses))==(20,clauses)
    model='SAT\n'+' '.join(str(v if b else -v) for v,b in w.items())+' 0\n'
    assert validate_model(20,clauses,model)['clauses_verified']==86

@pytest.mark.parametrize('model',['UNSAT','SAT 1 1 0','SAT 2 0','SAT -1 0','SAT 1'])
def test_bad_model_rejected(model):
    with pytest.raises(ValueError):validate_model(1,[(1,)],model)

@pytest.mark.parametrize('text',['1 0','p cnf 1 2\n1 0','p cnf 1 1\n2 0','p cnf 1 1\n1','p cnf 1 0\np cnf 1 0'])
def test_invalid_dimacs_rejected(text):
    with pytest.raises(ValueError):parse(text)
