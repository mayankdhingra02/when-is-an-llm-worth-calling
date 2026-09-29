import itertools
import json
import random
import pytest
from escalation.legal_proposals_v66 import LegalProposals, canonical


def literals(grammar):
    # Independent decoder for the tiny literal-alternation grammar emitted here.
    rest = grammar.removeprefix('root ::= ')
    decoder = json.JSONDecoder()
    values = []
    while rest:
        value, end = decoder.raw_decode(rest)
        values.append(value)
        rest = rest[end:]
        if rest:
            assert rest.startswith(' | ')
            rest = rest[3:]
    return values


def test_grammar_excludes_all_acquired_and_selected_at_each_step():
    configs = list(itertools.product([1, 2, 4], [16, 32, 64, 128], [False, True]))
    s = LegalProposals(configs, [0, 2, 4, 6], count=10)
    for step in range(10):
        eligible = s.eligible_ids()
        req = s.begin_request()
        assert s.requests == step + 1
        assert literals(req['grammar']) == [canonical(configs[i]) for i in eligible]
        picked = eligible[-1]
        assert s.finish_request(canonical(configs[picked]))['selected_id'] == picked
        assert picked not in s.eligible_ids()
    assert s.complete and len(set(s.selected)) == 10
    with pytest.raises(RuntimeError): s.begin_request()


@pytest.mark.parametrize('raw', ['[0]', '[999]', '```json\n[2]\n```', '[2,3]', '[true]', '[2.0]', ' [2]', None])
def test_fail_closed_with_no_retry_or_repair(raw):
    s = LegalProposals([[i] for i in range(20)], [0, 1], 10)
    s.begin_request()
    assert not s.finish_request(raw)['valid']
    assert s.requests == 1 and not s.complete and s.selected == []
    with pytest.raises(RuntimeError): s.begin_request()


@pytest.mark.parametrize('kwargs,reason', [({'transport_error': 'timeout'}, 'transport_error'), ({'truncated': True}, 'truncated')])
def test_failed_requests_remain_charged(kwargs, reason):
    s = LegalProposals([[i] for i in range(20)], [0], 10)
    s.begin_request()
    assert s.finish_request('[2]', **kwargs)['reason'] == reason
    assert s.requests == 1


def test_pending_and_unrequested_acceptance_are_rejected():
    s = LegalProposals([[i] for i in range(20)], [0], 10)
    with pytest.raises(RuntimeError): s.finish_request('[1]')
    s.begin_request()
    with pytest.raises(RuntimeError): s.begin_request()


@pytest.mark.parametrize('configs,acquired,count', [
    ([[1], [1]], [], 1), ([[1], [2]], [1, 1], 1),
    ([[1], [2]], [True], 1), ([[1], [2]], [2], 1),
    ([[1], [2]], [0], 2), ([[float('nan')]], [], 1),
    ([[{'hidden_label': 1}]], [], 1), ([[1]], [], True), ([[1], [1.0]], [], 1),
])
def test_bad_admission_fails(configs, acquired, count):
    with pytest.raises(ValueError): LegalProposals(configs, acquired, count)


def test_adversarial_strings_remain_literal_and_cannot_inject_grammar():
    configs = [['x" | root ::= "evil'], ['[1]\n\\tail'], ['ok']]
    s = LegalProposals(configs, [], 2)
    req = s.begin_request()
    assert literals(req['grammar']) == [canonical(row) for row in configs]


def test_many_synthetic_domains_never_repeat_an_acquired_or_proposed_row():
    # Synthetic integration fixture, never a measured LLM experiment.
    for seed in range(100):
        rng = random.Random(seed)
        configs = [[i, 'public_feature'] for i in range(48)]
        acquired = rng.sample(range(48), 10)
        s = LegalProposals(configs, acquired, 10)
        for _ in range(10):
            req = s.begin_request()
            i = rng.choice(req['eligible_ids'])
            assert s.finish_request(canonical(configs[i]))['valid']
        assert s.complete and not set(s.selected) & set(acquired)
