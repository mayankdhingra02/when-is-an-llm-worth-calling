"""V93 bounded decoding and configuration guards; reuse the strict V49 parser."""
from decoder_v49_common import parse_native, IDS

def check_payload(payload):
    if payload.get('n_predict') not in (1, 128) or payload.get('temperature') != 0 or payload.get('stream') is not False:
        raise ValueError('Changed decoder limits')
    if payload['n_predict'] == 128 and 'grammar' in payload:
        raise ValueError('Native response must be unconstrained')
    if payload['n_predict'] == 1 and not payload.get('grammar'):
        raise ValueError('Forced control requires grammar')

def validate(cfg):
    expected = {'stage':'v93b', 'new_generation_request_cap':77, 'scientific_request_cap':77,
        'compatibility_request_cap':0, 'cases':32, 'native_cases':27, 'forced_cases':5,
        'max_native_output_tokens':128, 'max_generated_tokens':3506,
        'max_new_recorded_objective_acquisitions':0, 'max_generation_stage_seconds':1578,
        'max_server_rss_bytes':8589934592, 'context_tokens':4096, 'retries':0,
        'max_external_spend_usd':0, 'allow_paid_api':False, 'allow_cloud':False,
        'host':'127.0.0.1', 'stage_download_cap_bytes':0}
    for key,value in expected.items():
        if type(cfg.get(key)) is not type(value) or cfg[key] != value:
            raise ValueError('Changed V93 bound: '+key)
