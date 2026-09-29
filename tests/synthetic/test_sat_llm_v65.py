import json
import pytest
from escalation.sat_v64 import grid
from escalation.sat_llm_v65 import messages, parse_response


def prefix():
    return [{'config_id': i, 'value_ms': i + 1.} for i in range(10)]


def test_valid_exact_native_response():
    assert parse_response(json.dumps(grid()[10:20]), prefix()) == {'valid': True, 'selected_ids': list(range(10, 20)), 'reason': None}


@pytest.mark.parametrize('raw,reason', [
    ('```json\n[]\n```', 'invalid_json'),
    ('[]', 'count_or_shape'),
    (json.dumps(grid()[0:10]), 'observed_proposal'),
    (json.dumps([grid()[10]] * 10), 'duplicate_proposal'),
    (json.dumps([[True, .9, 25, 1.2, 0]] * 10), 'outside_domain'),
    (json.dumps([[.8, .9, 26, 1.2, 0]] * 10), 'outside_domain'),
])
def test_bad_proposals_never_become_measured_llm_choices(raw, reason):
    result = parse_response(raw, prefix())
    assert not result['valid'] and result['selected_ids'] == [] and result['reason'] == reason


def test_truncation_rejects_even_parseable_payload():
    assert parse_response(json.dumps(grid()[10:20]), prefix(), True)['reason'] == 'truncated'


def test_prompt_only_uses_acquired_values():
    p = prefix()
    p[0]['hidden_objectives'] = 'SECRET_SENTINEL'
    text = json.dumps(messages(p))
    assert 'SECRET_SENTINEL' not in text
    assert '2201 clauses' in text and 'penalized_ms' in text


def test_duplicate_prefix_rejected():
    with pytest.raises(ValueError):
        messages([prefix()[0]] * 10)
