import pytest
from escalation.qwen_v91 import validate_response,check_payload
@pytest.mark.parametrize('r',[{'content':'A'},{'content':'A','tokens_predicted':2,'truncated':False},{'content':'A','tokens_predicted':1,'truncated':True},{'content':' A','tokens_predicted':1,'truncated':False},{'content':'Z','tokens_predicted':1,'truncated':False}])
def test_bad_real_response_shape(r):
    with pytest.raises(ValueError):validate_response(r,[])
def test_duplicate_rejected():
    with pytest.raises(ValueError):validate_response({'content':'A','tokens_predicted':1,'truncated':False},['A'])
def test_valid_token():assert validate_response({'content':'A','tokens_predicted':1,'truncated':False},[])=='A'
@pytest.mark.parametrize('payload',[{}, {'n_predict':2,'temperature':0,'stream':False},{'n_predict':1,'temperature':1,'stream':False}])
def test_changed_decoding_rejected(payload):
    with pytest.raises(ValueError):check_payload(payload)

def runtime_class():
    import importlib.util,sys
    from pathlib import Path
    scripts=Path(__file__).resolve().parents[2]/'scripts';sys.path.insert(0,str(scripts))
    spec=importlib.util.spec_from_file_location('v91_runtime_test',scripts/'runtime_qwen_v91.py');mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(mod);return mod.Runtime

def test_generation_cap_precedes_io(tmp_path):
    cls=runtime_class();r=cls(tmp_path,{'scientific_request_cap':300,'compatibility_request_cap':3,'new_generation_request_cap':303});r.check=lambda:None;r.ledger['scientific_requests']=300
    r._send=lambda *a:pytest.fail('Network must not be called')
    with pytest.raises(PermissionError):r.generate({'n_predict':1,'temperature':0,'stream':False},'scientific','fixture')

def test_failed_request_is_charged_before_io(tmp_path):
    import json
    cls=runtime_class();r=cls(tmp_path,{'scientific_request_cap':300,'compatibility_request_cap':3,'new_generation_request_cap':303});r.check=lambda:None
    def fail(*args):
        assert json.loads((tmp_path/'ledger.json').read_text())['generation_requests']==1
        raise OSError('Synthetic offline failure')
    r._send=fail
    with pytest.raises(OSError):r.generate({'n_predict':1,'temperature':0,'stream':False},'scientific','fixture')
    assert r.ledger['generation_requests']==r.ledger['scientific_requests']==1

def test_metadata_cannot_generate(tmp_path):
    r=runtime_class()(tmp_path,{})
    r._send=lambda *a:pytest.fail('Must reject before I/O')
    with pytest.raises(ValueError):r.api('/completion',{})
