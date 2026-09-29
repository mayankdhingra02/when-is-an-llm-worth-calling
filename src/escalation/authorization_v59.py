"""Explicit authorization boundary for the proposed two-hour local collection."""
import hashlib,json

def require_authorization(root):
    cfg=json.loads((root/'configs/authorization_v59.json').read_text())
    if cfg.get('authorized') is not True:
        raise PermissionError('V59 requires explicit approval of a7200-second local collection cap; current default is1800seconds.')
    if cfg.get('max_stage_seconds')!=7200 or cfg.get('max_physical_trials')!=576 or cfg.get('max_model_requests')!=0 or cfg.get('max_external_spend_usd')!=0:
        raise PermissionError('V59 authorization scope mismatch')
    if not cfg.get('user_approval_text'):
        raise PermissionError('Missing explicit user approval record')
    seal=root/'reports/protocol_v59_workload_screen.freeze.json'
    if cfg.get('protocol_freeze_sha256')!=hashlib.sha256(seal.read_bytes()).hexdigest():
        raise PermissionError('Protocol authorization hash mismatch')
