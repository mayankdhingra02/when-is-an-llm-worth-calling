"""Synthetic/feature-only checks for V173; no network request, no recorded target read, nothing enters research aggregates."""
import json, os, random, sys
from pathlib import Path
import pytest
ROOT = Path(__file__).resolve().parents[2]; sys.path.insert(0, str(ROOT/'scripts')); sys.path.insert(0, str(ROOT/'src'))
from interface_v173 import schema, parse, project_any, b_messages
from openrouter_v173 import Client, Refused, load_key, check_authorization, content_of, NoRedirect
from analyze_v173 import decision
import collect_v173, spark_v144, hadoop_v148
CFG = json.loads((ROOT/'configs/study_v173.json').read_text())

def test_schema_pattern_and_parser_agree():
    ds = [list(range(12)), [0, 1]]; s = schema(ds, 2); pat = s['properties']['proposals']['items']['pattern']
    assert pat == '^[0123456789AB][01]$' and s['properties']['proposals']['minItems'] == s['properties']['proposals']['maxItems'] == 2
    assert parse('{"proposals": ["B1", "00"]}', ds, 2) == [[11, 1], [0, 0]] == parse('["B1","00"]', ds, 2)
    for bad in ['{"proposals": ["B1"]}', '{"proposals": ["C1", "00"]}', '{"proposals": ["B1", "00"], "x": 1}', 'not json', '["B1", "002"]']:
        with pytest.raises(ValueError): parse(bad, ds, 2)

def test_content_of_rejects_truncation_and_empty():
    ok = {'choices': [{'message': {'content': '{"proposals":[]}'}, 'finish_reason': 'stop'}]}; assert content_of(ok)[0] == '{"proposals":[]}'
    for bad in [{'choices': [{'message': {'content': 'x'}, 'finish_reason': 'length'}]}, {'choices': [{'message': {'content': ''}, 'finish_reason': 'stop'}]}, {'choices': []}, None]:
        with pytest.raises(ValueError): content_of(bad)

@pytest.mark.parametrize('origin,cand,module,prefix', [('v148', 'artifacts/study_v148/candidates/wordcount.json', hadoop_v148, 'artifacts/study_v148/prefixes/wordcount_37.json'),
                                                       ('v144', 'artifacts/study_v144/candidates/terasort.json', spark_v144, 'artifacts/study_v144/prefixes/terasort_23.json')])
def test_generic_projection_matches_origin_projection(origin, cand, module, prefix):
    c = json.loads((ROOT/cand).read_text()); p = json.loads((ROOT/prefix).read_text()); rng = random.Random(3)
    props = [[rng.choice(d) for d in c['grid_domains']] for _ in range(10)]
    assert project_any(origin, c, p['order'], p['ids'], props)[0] == module.project(c, p, props)[0]

def test_generic_projection_matches_v141_and_flags_collisions():
    from analyze_pointwise_v123 import candidates
    from proposal_v127 import project, domains
    j = json.loads((ROOT/'artifacts/study_v141/jobs.json').read_text())[3]; spec, c = candidates(j['dataset']); p = json.loads((ROOT/j['prefix']).read_text())['state']
    assert domains(c.x) == j['domains']
    rng = random.Random(5); props = [tuple(rng.choice(d) for d in j['domains']) for _ in range(10)]
    assert project_any('v141', c, p['order'], p['ids'], props)[0] == project(props, c.x, p)[0]
    measured = list(c.x[p['ids'][0]]); rows, diag = project_any('v141', c, p['order'], p['ids'], [measured, measured])
    assert diag[0]['collision'] and diag[1]['collision'] and rows[0] not in p['ids'] and rows[0] != rows[1]

def test_arm_b_prompt_shows_only_acquired_labels_worst_first():
    c = {'x': [[0.0, 0], [0.5, 1], [1.0, 0], [0.25, 2]]}; original = [{'role': 'system', 'content': 'SYS'}, {'role': 'user', 'content': 'DATA'}]
    m = b_messages(original, 'v148', c, [list(range(10)), list(range(9))], [0, 1, 2], [[5.0], [9.0], [None]], 'minimize', 2, 5, ['00'], None)
    block = json.loads(m[2]['content']); traj = block['trajectory_worst_to_best']
    assert [t['performance'] for t in traj] == [None, 9.0, 5.0] and traj[0]['note'].startswith('missing') and 'retry' not in block
    assert block['diversification_collisions'] == ['00'] and 'SYS' in m[1]['content'] and 'exactly two' in m[1]['content']
    m2 = b_messages(original, 'v148', c, [list(range(10)), list(range(9))], [0, 1], [[5.0], [9.0]], 'maximize', 1, 5, [], 'Malformed JSON')
    b2 = json.loads(m2[2]['content']); assert [t['performance'] for t in b2['trajectory_worst_to_best']] == [5.0, 9.0] and 'Malformed JSON' in b2['retry'] and b2['diversification_collisions'] == 'none'

def _key(tmp_path, text='sk-or-v1-'+'a'*64, mode=0o600):
    p = tmp_path/'key'; p.write_text(text); os.chmod(p, mode); return p

def test_key_file_must_be_private_and_well_formed(tmp_path):
    cfg = dict(CFG, key_file=str(_key(tmp_path))); assert load_key(cfg).startswith('sk-or-v1-')
    with pytest.raises(Refused): load_key(dict(CFG, key_file=str(_key(tmp_path, mode=0o644))))
    with pytest.raises(Refused): load_key(dict(CFG, key_file=str(_key(tmp_path, text='not-a-key'))))

def test_authorization_host_and_cap_guards():
    check_authorization(CFG)
    with pytest.raises(Refused): check_authorization(dict(CFG, api_url='https://example.com/v1/chat/completions'))
    with pytest.raises(Refused): check_authorization(dict(CFG, spend_cap_usd=10.0))
    with pytest.raises(Refused): check_authorization(dict(CFG, allow_paid_api=False))
    with pytest.raises(Refused): NoRedirect().redirect_request(None, None, 302, 'x', {}, 'https://evil.example')

def _client(tmp_path, spent=0.0, cap=5):
    cfg = dict(CFG, key_file=str(_key(tmp_path))); c = Client(cfg, tmp_path, 'T', 'coreweave/fp4', cap, tmp_path/'spend.json')
    s = c.spend.state(); s['spent_usd'] = spent; (tmp_path/'spend.json').write_text(json.dumps(s))
    c.opener.open = lambda *a, **k: (_ for _ in ()).throw(AssertionError('network must not be reached'))
    return c

def test_spend_cap_refuses_before_any_network_call(tmp_path):
    c = _client(tmp_path, spent=2.9999); body = c.body([{'role': 'user', 'content': 'x'*3000}], schema([[0, 1]], 2), 1.0, 1, 16000)
    with pytest.raises(Refused): c.send(body, 'id', 1e18)
    assert not (tmp_path/'requests.jsonl').exists()

def test_request_cap_and_wall_cap_refuse_before_network(tmp_path):
    c = _client(tmp_path, cap=0); body = c.body([{'role': 'user', 'content': 'x'}], schema([[0, 1]], 2), 1.0, 1, 8000)
    with pytest.raises(Refused): c.send(body, 'id', 1e18)
    c2 = _client(tmp_path, cap=5)
    with pytest.raises(Refused): c2.send(body, 'id', -1.0)

def test_request_body_pins_provider_and_settings(tmp_path):
    c = _client(tmp_path); b = c.body([{'role': 'user', 'content': 'x'}], schema([[0, 1]], 2), 0.95, 7, CFG['max_tokens']['A'])
    assert b['provider'] == {'order': ['coreweave/fp4'], 'allow_fallbacks': False, 'require_parameters': True} and b['model'] == 'openai/gpt-oss-120b'
    assert b['max_tokens'] == 16000 and CFG['max_tokens']['B'] == 8000 and b['reasoning'] == {'effort': 'medium'} and b['temperature'] == .7 and b['top_p'] == .95 and b['seed'] == 7 and b['usage'] == {'include': True}
    assert 'Authorization' not in json.dumps(b) and 'sk-or' not in json.dumps(b)

def test_arm_b_stages_partition_all_cases():
    got = [j['qualified_key'] for s in [f'B{i}' for i in range(1, 9)] for j in collect_v173.b_cases(CFG, s)]
    assert max(len(collect_v173.b_cases(CFG, f'B{i}')) for i in range(1, 9)) <= 9
    assert len(got) == len(set(got)) == 70

def test_v173_decision_rule():
    assert decision(0, 1) == decision(1, 1) == 'boundary_extends_to_snap2_model_on_this_cohort'
    assert decision(2, 0) == decision(0, 3) == 'headroom_at_snap2_model_router_question_needs_fresh_cohort'

def test_rate_limit_backoff_retries_429_then_records_every_attempt(tmp_path, monkeypatch):
    import io, urllib.error, openrouter_v173
    c = _client(tmp_path); calls = {'n': 0}; slept = []
    monkeypatch.setattr(openrouter_v173.time, 'sleep', lambda s: slept.append(s))
    class R:
        status = 200
        def __enter__(self): return self
        def __exit__(self, *a): return False
        def read(self): return json.dumps({'provider': 'CoreWeave', 'choices': [{'message': {'content': '{"proposals":["0","1"]}'}, 'finish_reason': 'stop'}], 'usage': {'prompt_tokens': 10, 'completion_tokens': 5, 'cost': 1e-6}}).encode()
    def fake(req, timeout=None):
        calls['n'] += 1
        if calls['n'] < 3: raise urllib.error.HTTPError('u', 429, 'rate', {}, io.BytesIO(b'{"error":"rate limited"}'))
        return R()
    c.opener.open = fake; body = c.body([{'role': 'user', 'content': 'x'}], schema([[0, 1]], 2), 1.0, 1, 8000)
    status, resp, err = c.send(body, 'id', 1e18)
    assert status == 200 and calls['n'] == 3 and slept == CFG['rate_limit_backoff_seconds'][:2] and c.requests == 1
    rows = [json.loads(l) for l in (tmp_path/'responses.jsonl').read_text().splitlines()]
    assert [r['http_status'] for r in rows] == [429, 429, 200] and [r['rate_limit_retry'] for r in rows] == [0, 1, 2]
    assert json.loads((tmp_path/'spend.json').read_text())['requests'] == 3

def test_rate_limit_backoff_is_bounded(tmp_path, monkeypatch):
    import io, urllib.error, openrouter_v173
    c = _client(tmp_path); monkeypatch.setattr(openrouter_v173.time, 'sleep', lambda s: None)
    def always(req, timeout=None): raise urllib.error.HTTPError('u', 429, 'rate', {}, io.BytesIO(b'{}'))
    c.opener.open = always; status, resp, err = c.send(c.body([{'role': 'user', 'content': 'x'}], schema([[0, 1]], 2), 1.0, 1, 8000), 'id', 1e18)
    assert status == 429 and resp is None and len((tmp_path/'responses.jsonl').read_text().splitlines()) == 1+len(CFG['rate_limit_backoff_seconds'])

def test_continuation_chain_names_and_order():
    assert collect_v173.chain('A2') == ['A2', 'A2.c1', 'A2.c2', 'A2.c3'] and collect_v173.BASE.index('A2') < collect_v173.BASE.index('E') < collect_v173.BASE.index('B1')
