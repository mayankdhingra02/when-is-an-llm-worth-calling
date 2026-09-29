"""Synthetic fixtures: never native measurements or EULA approval."""
import hashlib
import pytest
from escalation.duckdb_v87 import authorize,validate_answer

def test_no_implicit_eula_grant():
    for grant in [None,{}, {'granted':True}, {'granted':True,'license_sha256':'bad','user_message':'SYNTHETIC'}]:
        with pytest.raises(PermissionError):authorize(grant,b'SYNTHETIC LICENSE')

def test_grant_bound_to_exact_license():
    b=b'SYNTHETIC LICENSE';g={'granted':True,'license_sha256':hashlib.sha256(b).hexdigest(),'user_message':'SYNTHETIC ONLY'};authorize(g,b)
    with pytest.raises(PermissionError):authorize(g,b+'changed'.encode())

def test_exact_answers_accept_integers():
    assert validate_answer('kind|count\nA|2\nB|3\n',['kind','count'],[('A',2),('B',3)])==[['A','2'],['B','3']]

@pytest.mark.parametrize('rows',[[('A',1)],[('A',2),('A',2)],[('A',2.0)],[],[('B',2)]])
def test_missing_wrong_duplicate_or_float_results_rejected(rows):
    with pytest.raises(ValueError):validate_answer('kind|count\nA|2\n',['kind','count'],rows)

def test_wrong_header_rejected():
    with pytest.raises(ValueError):validate_answer('kind|amount\nA|2\n',['kind','count'],[('A',2)])
