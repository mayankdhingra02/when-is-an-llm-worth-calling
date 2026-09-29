"""Reject expansion of the prospectively bounded V92 diagnostic."""
def validate(cfg):
    expected = {
        'stage': 'v92b', 'new_generation_request_cap': 1080,
        'scientific_request_cap': 1080, 'compatibility_request_cap': 0,
        'cases': 108, 'max_new_recorded_objective_acquisitions': 0,
        'max_generation_stage_seconds': 1799,
        'max_server_rss_bytes': 8589934592, 'context_tokens': 8192,
        'retries': 0, 'max_external_spend_usd': 0,
        'allow_paid_api': False, 'allow_cloud': False,
        'host': '127.0.0.1', 'stage_download_cap_bytes': 0,
        'scientific_case_source': 'artifacts/study_v48/jobs.json',
    }
    for key, value in expected.items():
        if type(cfg.get(key)) is not type(value) or cfg[key] != value:
            raise ValueError('Changed V92 bound: ' + key)

