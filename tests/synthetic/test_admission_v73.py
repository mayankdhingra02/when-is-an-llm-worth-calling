import pytest
from escalation.admission_v73 import BOOLS, original_vector, released_vector

def fixture():
    row={k:'False' for k in BOOLS};row.update(jobs='4',blocksize='1000000',config_id='7')
    old={k:row[k] for k in BOOLS};old.update({'':'99','entropy':'True', 'jobs_1':'False','jobs_4':'True','jobs_8':'False','blocksize_1KB':'False','blocksize_1MB':'True','blocksize_1GB':'False'})
    return old,row

def test_features_reconcile_despite_different_ids():
    old,row=fixture();assert original_vector(old)==released_vector(row)

def test_objective_injection_rejected():
    _,row=fixture();row['runtime']='POISON'
    with pytest.raises(ValueError):released_vector(row)

@pytest.mark.parametrize('field,value',[('jobs_8','True'),('blocksize_1MB','False'),('LZ','maybe')])
def test_invalid_original_encoding(field,value):
    old,_=fixture();old[field]=value
    with pytest.raises(ValueError):original_vector(old)
