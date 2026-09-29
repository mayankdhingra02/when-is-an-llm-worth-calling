import hashlib,json
import pytest
from escalation.authorization_v59 import require_authorization

def test_exact_authorization_scope(tmp_path):
    (tmp_path/'configs').mkdir();(tmp_path/'reports').mkdir()
    seal=tmp_path/'reports/protocol_v59_workload_screen.freeze.json';seal.write_text('synthetic protocol fixture')
    cfg={'authorized':False,'max_stage_seconds':7200,'max_physical_trials':576,'max_model_requests':0,'max_external_spend_usd':0,'user_approval_text':'synthetic unit-test approval; not real authorization','protocol_freeze_sha256':hashlib.sha256(seal.read_bytes()).hexdigest()}
    p=tmp_path/'configs/authorization_v59.json'
    p.write_text(json.dumps(cfg))
    with pytest.raises(PermissionError):require_authorization(tmp_path)
    cfg['authorized']=True;p.write_text(json.dumps(cfg));require_authorization(tmp_path)
    cfg['max_model_requests']=1;p.write_text(json.dumps(cfg))
    with pytest.raises(PermissionError):require_authorization(tmp_path)
