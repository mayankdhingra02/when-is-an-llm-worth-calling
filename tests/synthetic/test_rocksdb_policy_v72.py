"""Synthetic policy/guard fixtures; never research measurements."""
import json
import pytest
from escalation.rocksdb_v69 import grid
from escalation.rocksdb_policy_v72 import messages, prior_choice, validate_acquisition, vectors, features
from escalation.legal_proposals_v66 import LegalProposals


def test_prompt_allowlist_and_no_input_mutation():
    configs = grid()
    observed = [{'config_id': 3, 'value_ms': 123.0, 'hidden_labels': 'SECRET', 'physical_receipt': 'PRIVATE'}]
    text = json.dumps(messages(configs, observed))
    assert 'SECRET' not in text and 'PRIVATE' not in text and '123.0' in text
    assert observed[0]['hidden_labels'] == 'SECRET'
    assert 'measured_ms' in text


def test_prior_ignores_labels_and_excludes_acquired():
    configs = grid()
    obs = []
    picked = []
    for _ in range(7):
        cid = prior_choice(configs, obs)
        assert configs[cid]['cache_mib'] == 128
        assert configs[cid]['block_size'] == 512
        assert configs[cid]['restart_interval'] == 2**len(picked)
        picked.append(cid); obs.append({'config_id': cid, 'value_ms': -999999})
        changed = [{**o, 'value_ms': 999999} for o in obs]
        assert prior_choice(configs, obs) == prior_choice(configs, changed)


@pytest.mark.parametrize('cid,obs,purpose,count', [
    (0, [], 'search', 150), (0, [{}]*20, 'confirmation', 0),
    (512, [], 'search', 0), (True, [], 'search', 0),
    (0, [{'config_id': 0}], 'search', 0), (0, [], 'other', 0)])
def test_budget_invalid_inputs(cid, obs, purpose, count):
    with pytest.raises(ValueError): validate_acquisition(cid, obs, purpose, count)


def test_confirmation_is_charged_not_free():
    obs = [{'config_id': i} for i in range(17)]
    for _ in range(3):
        validate_acquisition(0, obs, 'confirmation', 149)
        obs.append({'config_id': 0})
    with pytest.raises(ValueError): validate_acquisition(0, obs, 'confirmation', 149)


def test_seven_legal_proposals_and_failure_no_retry():
    configs = grid()
    session = LegalProposals(vectors(configs), list(range(10)), count=7)
    for _ in range(7):
        request = session.begin_request()
        raw = json.dumps(request['eligible_configurations'][0], separators=(',', ':'))
        assert session.finish_request(raw)['valid']
    assert session.complete and session.requests == 7
    with pytest.raises(RuntimeError): session.begin_request()
    bad = LegalProposals(vectors(configs), list(range(10)), count=7)
    bad.begin_request(); assert not bad.finish_request('[1,512,1]')['valid']
    with pytest.raises(RuntimeError): bad.begin_request()


def test_declared_feature_scaling():
    x = features(grid())
    assert x.shape == (512, 3)
    assert (x.min(axis=0) == 0).all() and (x.max(axis=0) == 1).all()
