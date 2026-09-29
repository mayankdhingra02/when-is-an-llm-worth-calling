"""Synthetic transport guard tests; never research outputs or live requests."""
import sys,json
from pathlib import Path
import pytest
sys.path.insert(0,str(Path(__file__).resolve().parents[2]/'scripts'))
from runtime_models_v144 import Runtime
from proposal_v128 import payload,payload_key
def config():
 return json.loads((Path(__file__).resolve().parents[2]/'configs/study_v144.json').read_text())
@pytest.mark.parametrize('flag',['allow_paid_api','allow_cloud'])
def test_paid_and_cloud_rejected_before_request(tmp_path,flag):
 c=config();c[flag]=True
 with pytest.raises(AssertionError):Runtime(tmp_path,c)
def test_exhausted_request_or_token_cap_never_sends(tmp_path,monkeypatch):
 r=Runtime(tmp_path,config());p=payload('synthetic',11,[[0,1]])
 r.authorized[payload_key(p)]={'synthetic_only':True}
 monkeypatch.setattr(r,'_send',lambda *a:pytest.fail('Must reject before transport'))
 r.ledger['generation_requests']=30
 with pytest.raises(PermissionError,match='Generation cap'):r.generate(p,'scientific','synthetic')
 r.ledger['generation_requests']=0;r.ledger['allocated_output_tokens']=30720
 with pytest.raises(PermissionError,match='Output allocation cap'):r.generate(p,'scientific','synthetic')
 assert r.ledger['scientific_requests']==0
def test_unbound_payload_never_sends(tmp_path,monkeypatch):
 r=Runtime(tmp_path,config());p=payload('synthetic',11,[[0,1]])
 monkeypatch.setattr(r,'_send',lambda *a:pytest.fail('Unapproved payload sent'))
 with pytest.raises(PermissionError,match='Missing bound preflight'):r.generate(p,'scientific','synthetic')
