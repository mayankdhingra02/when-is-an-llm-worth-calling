"""Frozen design and explicit authorization for a larger-model development probe."""
import copy
import hashlib
import json
import random

MODEL_ID = 'Qwen/Qwen2.5-1.5B-Instruct'
REVISION = '989aa7980e4cf806f80c7fef2b1adb7bc71aa306'
IDS = list('0123456789ABCDEFGHIJ')
CONDITIONS = ('assigned_ids', 'reverse_display', 'reassigned_ids', 'assigned_ids_repeat')


def require(ok, message):
    if not ok:
        raise ValueError(message)


def authorization_config(base, auth):
    if auth.get('granted') is not True:
        raise PermissionError('V22 requires explicit approval:60 additional local calls,cap140->200,runtime1800->3600seconds')
    expected = {'request_cap': 200, 'additional_requests': 60, 'runtime_cap_seconds': 3600,
                'external_spend_usd': 0, 'max_model_download_gib': 4, 'max_total_new_download_gib': 5,
                'model_id': MODEL_ID, 'revision': REVISION}
    require(all(auth.get(k) == v for k, v in expected.items()) and bool(auth.get('user_authorization')),
            'Exact bounded V22 authorization required')
    cfg = copy.deepcopy(base)
    require(cfg['inference']['allow_paid_api'] is False and cfg['inference']['max_external_spend_usd'] == 0,
            'Paid inference prohibited')
    cfg['inference'].update(max_new_model_requests=200, max_output_tokens_per_request=20,
                            request_timeout_seconds=30, max_retries_per_request=0, model_id=MODEL_ID)
    cfg['resources'].update(max_experiment_runtime_minutes=60)
    require(cfg['resources']['max_model_download_gib'] == 4 and cfg['resources']['max_total_new_download_gib'] == 5,
            'Download limits must stay unchanged')
    return cfg


def permuted_ids(dataset, seed, tag):
    identity = f'v22|{dataset}|{seed}|{tag}'.encode()
    rng = random.Random(int.from_bytes(hashlib.sha256(identity).digest(), 'big'))
    ids = list(IDS)
    while ids in (IDS, IDS[::-1]):
        rng.shuffle(ids)
    return ids


def transform(messages, pool, dataset, seed, condition):
    require(condition in CONDITIONS, 'Unknown treatment')
    result = copy.deepcopy(messages)
    intro, raw = result[-1]['content'].split('\n', 1)
    body = json.loads(raw)
    original = body['candidates']
    require([r['id'] for r in original] == IDS, 'Canonical source IDs required')
    new_ids = permuted_ids(dataset, seed, 'A' if condition != 'reassigned_ids' else 'C')
    mapping = {new: pool['mapping'][old['id']] for old, new in zip(original, new_ids)}
    for row, new in zip(original, new_ids):
        row['id'] = new
    if condition == 'reverse_display':
        body['candidates'].reverse()
    result[-1]['content'] = intro + '\n' + json.dumps(body, separators=(',', ':'))
    return {'messages': result, 'mapping': mapping, 'display_ids': [r['id'] for r in body['candidates']]}


def controls(job):
    return {'first_display': [job['mapping'][i] for i in job['display_ids'][:10]],
            'lowest_ids': [job['mapping'][i] for i in IDS[:10]]}
