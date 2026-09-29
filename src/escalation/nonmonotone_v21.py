"""Exact, separately approved three-call extension; V19 code stays immutable."""
import copy

def authorization_config(base,auth):
    if auth.get('granted') is not True:raise PermissionError('Three additional local calls require approval:137 to140')
    if (auth.get('request_cap'),auth.get('additional_requests'),auth.get('runtime_cap_seconds'),auth.get('external_spend_usd'))!=(140,3,1800,0) or not auth.get('user_authorization'):
        raise ValueError('Exact three-call authorization required; runtime/spend unchanged')
    c=copy.deepcopy(base)
    if c['resources']['max_experiment_runtime_minutes']!=30:raise ValueError('Original runtime cap required')
    c['inference'].update(max_new_model_requests=140,max_output_tokens_per_request=20,request_timeout_seconds=6)
    return c
