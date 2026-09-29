import pytest
from escalation.kanzi_v75 import grid
from escalation.kanzi_policy_v80 import messages,validate_acquisition,METHODS

def test_allowlist_hidden_fields_and_metadata():
    obs=[{'config_id':439,'compressed_bytes':123,'secret_future_best':-999}]
    w={'kind':'plain text','bytes':10192446,'hidden_minimum':'LEAK','name':'LEAK'}
    result=str(messages(grid(),obs,w))
    assert 'LEAK' not in result and 'secret_future_best' not in result and '-999' not in result
    assert '10192446' in result and '123' in result and 'generated16MiB' not in result
    assert METHODS==['rf_lcb','preset','llm']

@pytest.mark.parametrize('count',[450,451])
def test_physical_cap(count):
    with pytest.raises(ValueError):validate_acquisition(1,[],'search',count)

def test_logical_cap_and_duplicates():
    with pytest.raises(ValueError):validate_acquisition(2,[{'config_id':1}]*20,'confirmation',0)
    with pytest.raises(ValueError):validate_acquisition(1,[{'config_id':1}],'search',0)
    validate_acquisition(1,[{'config_id':1}]*19,'confirmation',449)
