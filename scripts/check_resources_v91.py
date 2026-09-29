"""Reviewable resource-change gate. Does not fetch files or start inference."""
import hashlib,json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def validate(proposal,approval,digest):
    assert proposal['stage_download_cap_bytes']>=proposal['model_file_bytes']
    assert proposal['previous_total_download_bytes']+proposal['stage_download_cap_bytes']<=proposal['proposed_total_download_cap_bytes']
    assert proposal['previous_model_download_bytes']+proposal['model_file_bytes']<=proposal['proposed_model_download_cap_bytes']
    assert proposal['new_generation_request_cap']==proposal['compatibility_request_cap']+proposal['scientific_request_cap']==303
    assert proposal['cases']*proposal['requests_per_case']==proposal['scientific_request_cap']
    assert proposal['retries']==proposal['max_external_spend_usd']==0 and not proposal['allow_paid_api'] and not proposal['allow_cloud'] and proposal['host']=='127.0.0.1'
    if not approval or approval.get('proposal_sha256')!=digest or approval.get('explicit_resource_change_approved') is not True or not approval.get('user_message') or not approval.get('at_utc'):
        raise PermissionError('Explicit increased download/model/request limits approval missing; current caps remain in force')
    return True

def main():
    p=ROOT/'configs/resource_proposal_v91.json';a=ROOT/'artifacts/study_v91/approval.json';proposal=json.loads(p.read_text());approval=json.loads(a.read_text()) if a.exists() else None
    validate(proposal,approval,hashlib.sha256(p.read_bytes()).hexdigest());print('Resource change approved; this check performs no download/inference')
if __name__=='__main__':main()
