from pathlib import Path
import yaml

def load_config(path='configs/pilot.yaml'):
    c=yaml.safe_load(Path(path).read_text());i=c['inference'];r=c['resources'];o=c['optimization']
    if i['allow_paid_api'] or i['max_external_spend_usd']!=0 or not i['local_endpoint_only']: raise ValueError('paid/remote inference prohibited')
    if i['backend'] not in ('local_or_verified_cache','local_transformers'): raise ValueError('unapproved backend')
    checks=[i['max_new_model_requests']<=100,i['max_retries_per_request']<=1,i['max_output_tokens_per_request']<=1024,i['request_timeout_seconds']<=180,i['max_concurrent_requests']==1,r['max_experiment_runtime_minutes']<=30,r['max_model_download_gib']<=4,r['max_total_new_download_gib']<=5,r['max_parallel_experiments']==1,not r['allow_cloud_provisioning'],not r['allow_system_wide_installs'],o['total_evaluations_per_arm']==20,o['decision_after_evaluations']==10,len(c['seed_list'])==5,len(set(c['seed_list']))==5]
    checks.extend([i['max_new_model_requests']>=0, 0<=i['max_retries_per_request']<=1, 0<i['max_output_tokens_per_request']<=1024, 0<i['request_timeout_seconds']<=180, 0<r['max_experiment_runtime_minutes']<=30])
    if not all(checks): raise ValueError('pilot bounds changed or invalid')
    return c
