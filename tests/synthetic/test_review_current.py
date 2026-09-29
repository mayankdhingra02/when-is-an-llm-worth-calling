"""Synthetic corrupt-record fixtures; never research measurements."""
import importlib.util
import json
from pathlib import Path

import pytest

spec = importlib.util.spec_from_file_location(
    'review_current', Path(__file__).resolve().parents[2] / 'scripts/verify_review_current.py')
review = importlib.util.module_from_spec(spec)
spec.loader.exec_module(review)


def fixture_records():
    ids = list('0123456789ABCDEFGHIJ')
    messages = [{'content': 'synthetic fixture\n' + json.dumps({'candidates': [{'id': i} for i in ids]})}]
    mapping = dict(zip(ids, range(20)))
    job = {'job_id': 0, 'dataset': 'synthetic_only', 'condition': 'fixture',
           'messages': messages, 'mapping': mapping}
    request = dict(job, request_id=1, status='response', retry=0,
                   raw_output='\n'.join(ids[:10]), revision='7ae557604adf67be50417f59c2c2f167def9a775',
                   provider='local_transformers', parameters={'do_sample': False, 'max_new_tokens': 20},
                   input_tokens=1, output_tokens=20)
    start = dict(job, request_id=1)
    outcome = {'request_id': 1, 'status': 'completed', 'selected_ids': ids[:10], 'selected_rows': list(range(10))}
    return [job], [request], [start], [outcome]


@pytest.mark.parametrize('corruption', ['missing_response', 'duplicate_response', 'wrong_raw_id', 'changed_mapping', 'changed_prompt', 'missing_usage'])
def test_corrupt_evidence_fails_closed(corruption):
    jobs, requests, starts, outcomes = fixture_records()
    if corruption == 'missing_response':
        requests.clear()
    elif corruption == 'duplicate_response':
        requests.append(dict(requests[0]))
    elif corruption == 'wrong_raw_id':
        requests[0]['raw_output'] = requests[0]['raw_output'].replace('9', 'A')
    elif corruption == 'changed_mapping':
        requests[0]['mapping'] = dict(requests[0]['mapping'], **{'0': 999})
    elif corruption == 'changed_prompt':
        requests[0]['messages'] = [{'content': 'tampered synthetic prompt'}]
    elif corruption == 'missing_usage':
        requests[0]['input_tokens'] = None
    with pytest.raises(ValueError):
        review.checked_selections(jobs, requests, starts, outcomes)


def test_valid_synthetic_mapping():
    result = review.checked_selections(*fixture_records())
    assert result[0]['selected_rows'] == list(range(10))
    assert result[0]['display_prefix_match']
