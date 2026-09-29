"""Synthetic authorization guard tests, not model measurements."""
import pytest
from escalation.nonmonotone_v21 import authorization_config

def test_denied_and_wrong_caps_fail_closed():
    base={'inference':{},'resources':{'max_experiment_runtime_minutes':30}}
    with pytest.raises(PermissionError):authorization_config(base,{'granted':False})
    auth={'granted':True,'request_cap':140,'additional_requests':3,'runtime_cap_seconds':1800,'external_spend_usd':0,'user_authorization':'synthetic approval fixture'}
    assert authorization_config(base,auth)['inference']['max_new_model_requests']==140
    assert base['inference']=={}
    for key,value in [('request_cap',141),('additional_requests',4),('runtime_cap_seconds',1801),('external_spend_usd',1)]:
        with pytest.raises(ValueError):authorization_config(base,dict(auth,**{key:value}))
