"""Synthetic design/permission tests; no model inference or measured fixtures."""
import copy
import json
import pytest
from escalation.larger_v22 import IDS, MODEL_ID, REVISION, transform, controls, authorization_config


def fixture():
    body = {'observations': [{'x': 'observed', 'loss': 0.2}],
            'candidates': [{'id': i, 'x': f'feature{n}'} for n, i in enumerate(IDS)]}
    return [{'role': 'system', 'content': 'synthetic'}, {'role': 'user', 'content': 'fixture\n' + json.dumps(body)}], {'mapping': dict(zip(IDS, range(20)))}


def test_interventions_preserve_features_observations_and_row_identity():
    messages, pool = fixture(); saved = copy.deepcopy(messages)
    treatments = {name: transform(messages, pool, 'synthetic', 11, name) for name in
                  ['assigned_ids', 'reverse_display', 'reassigned_ids', 'assigned_ids_repeat']}
    assert messages == saved and treatments['assigned_ids'] == treatments['assigned_ids_repeat']
    bodies = {k: json.loads(v['messages'][-1]['content'].split('\n', 1)[1]) for k, v in treatments.items()}
    assert all(b['observations'] == bodies['assigned_ids']['observations'] for b in bodies.values())
    assert bodies['reverse_display']['candidates'] == bodies['assigned_ids']['candidates'][::-1]
    assert treatments['assigned_ids']['mapping'] == treatments['reverse_display']['mapping']
    for name in ['assigned_ids', 'reassigned_ids']:
        assert [r['x'] for r in bodies[name]['candidates']] == [f'feature{n}' for n in range(20)]
        assert [treatments[name]['mapping'][r['id']] for r in bodies[name]['candidates']] == list(range(20))
    assert treatments['assigned_ids']['display_ids'] not in [IDS, IDS[::-1]]
    assert treatments['assigned_ids']['display_ids'] != treatments['reassigned_ids']['display_ids']
    assert controls(treatments['assigned_ids'])['first_display'] == list(range(10))
    assert controls(treatments['reverse_display'])['first_display'] == list(range(19, 9, -1))


def base_and_auth():
    base = {'inference': {'allow_paid_api': False, 'max_external_spend_usd': 0},
            'resources': {'max_model_download_gib': 4, 'max_total_new_download_gib': 5, 'max_experiment_runtime_minutes': 30}}
    auth = {'granted': True, 'request_cap': 200, 'additional_requests': 60, 'runtime_cap_seconds': 3600,
            'external_spend_usd': 0, 'max_model_download_gib': 4, 'max_total_new_download_gib': 5,
            'model_id': MODEL_ID, 'revision': REVISION, 'user_authorization': 'synthetic only'}
    return base, auth


def test_no_implicit_approval_or_mutation():
    base, auth = base_and_auth(); original = copy.deepcopy(base)
    with pytest.raises(PermissionError): authorization_config(base, dict(auth, granted=False))
    cfg = authorization_config(base, auth)
    assert base == original and cfg['inference']['max_new_model_requests'] == 200
    assert cfg['resources']['max_experiment_runtime_minutes'] == 60


@pytest.mark.parametrize('key,value', [('request_cap', 201), ('additional_requests', 61),
    ('runtime_cap_seconds', 3601), ('external_spend_usd', 1), ('revision', 'main'), ('user_authorization', None)])
def test_changed_permission_bounds_are_rejected(key, value):
    base, auth = base_and_auth(); auth[key] = value
    with pytest.raises(ValueError): authorization_config(base, auth)


def test_new_provider_cache_binds_actual_model_identity(tmp_path):
    from escalation.provider_v22 import LargerProvider
    from escalation.io import digest, lines
    class Process:
        def is_alive(self): return True
    class Pipe:
        def send(self, value): pass
        def poll(self, timeout): return True
        def recv(self): return {'raw_output': 'synthetic output only', 'input_tokens': 1, 'output_tokens': 1}
    class Resources:
        def request(self): return 1
        def remaining(self): return 20
        def checkpoint(self): pass
    cfg = {'inference': {'allow_paid_api': False, 'max_external_spend_usd': 0, 'local_endpoint_only': True,
                        'backend': 'local_transformers', 'max_output_tokens_per_request': 20, 'request_timeout_seconds': 30}}
    provider = LargerProvider(cfg, Resources(), tmp_path / 'synthetic_requests.jsonl')
    provider.process = Process(); provider.pipe = Pipe()
    provider.identity = {'model_id': MODEL_ID, 'revision': REVISION}
    messages = [{'role': 'user', 'content': 'synthetic fixture'}]
    context = {'namespace': 'synthetic_only', 'prompt_version': 'synthetic', 'grammar_mode': 'candidate_order_v19'}
    result = provider.request(messages, context)
    expected = digest({'messages': messages, 'model': MODEL_ID, 'revision': REVISION,
                       'parameters': {'do_sample': False, 'max_new_tokens': 20}, 'context': context,
                       'parser_projection': 'synthetic', 'grammar_domains': None, 'grammar_mode': 'candidate_order_v19'})
    assert result['cache_key'] == expected
    assert lines(tmp_path / 'request_starts.jsonl')[0]['model_id'] == MODEL_ID
