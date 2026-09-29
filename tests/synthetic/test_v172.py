"""Synthetic/feature-only checks for V172; no model start, no recorded target read, nothing enters research aggregates."""
import hashlib, json, random, sys
from pathlib import Path
import pytest
ROOT = Path(__file__).resolve().parents[2]; sys.path.insert(0, str(ROOT/'scripts')); sys.path.insert(0, str(ROOT/'src'))
from common_v172 import decision
from runtime_v172 import server_command
from prepare_v172 import build_jobs
from evaluate_v172 import Ledger, SparkOracle, HadoopOracle
from analyze_v172 import specific
from verify_v172 import my_parse, my_project
import proposal_v128, spark_v144, hadoop_v148
CFG = json.loads((ROOT/'configs/study_v172.json').read_text())

def test_server_command_is_historical_command():
    hist = json.loads((ROOT/'results/v148_models/qwen3_8b/runtime.json').read_text())
    assert server_command(ROOT/hist['model']['path'], hist['config']['ports']['qwen3_8b']) == hist['command']

@pytest.mark.parametrize('a,b,expected', [(0, 0, 'close_router_question'), (1, 5, 'close_router_question'), (2, 0, 'scale_consistent_headroom_router_question_testable'),
                                          (2, 1, 'scale_consistent_headroom_router_question_testable'), (2, 2, 'headroom_also_under_8b_resampling_scale_not_supported'), (7, 3, 'headroom_also_under_8b_resampling_scale_not_supported')])
def test_decision_rule(a, b, expected): assert decision(a, b) == expected

def test_jobs_cover_v151_cases_with_fixed_split_and_redraw_seeds():
    jobs = build_jobs(CFG); v151 = {r['key'] for r in json.loads((ROOT/'artifacts/study_v151/inputs.json').read_text())['rows']}
    assert {j['qualified_key'] for j in jobs} == v151 and len(jobs) == 70
    assert sum(j['split'] == 1 for j in jobs) == sum(j['split'] == 2 for j in jobs) == 35
    assert all(j['redraw_seed'] == j['sampling_seed']+172000 for j in jobs) and build_jobs(CFG) == jobs
    saved = ROOT/'artifacts/study_v172/jobs.json'
    if saved.exists(): assert json.loads(saved.read_text()) == jobs

def test_ledger_charges_before_reads_and_enforces_caps(tmp_path):
    led = Ledger(tmp_path/'l.json', tmp_path/'j.jsonl', 2, 60); led.charge('k', 1); led.charge('k', 2)
    with pytest.raises(PermissionError): led.charge('k', 3)
    assert json.loads((tmp_path/'l.json').read_text())['acquisitions'] == 2
    with pytest.raises(TimeoutError): Ledger(tmp_path/'m.json', tmp_path/'n.jsonl', 5, 0).charge('k', 1)

def _csv(tmp_path, values):
    rows = ['h'*1+','*33]+[','.join(['0']*30+[v, 'a', 'b', 'c']) for v in values]; p = tmp_path/'s.csv'; p.write_text('\n'.join(rows)+'\n'); return p

def test_spark_oracle_keeps_missing_target_charged(tmp_path):
    p = _csv(tmp_path, ['5.0', '', '7.5']); led = Ledger(tmp_path/'l.json', tmp_path/'j.jsonl', 10, 60)
    c = {'source_path': str(p), 'source_sha256': hashlib.sha256(p.read_bytes()).hexdigest(), 'x': [[0], [1], [2]], 'source_lines': [2, 3, 4]}
    o = SparkOracle(c, 'k', {'ids': [0]}, led); assert o.acquire(1) == [None] and o.acquire(2) == [7.5] and led.state['acquisitions'] == 2
    with pytest.raises(ValueError): o.acquire(2)

def test_hadoop_oracle_applies_declared_penalty(tmp_path):
    recs = [{'framework': 'hadoop', 'workload': 'wordcount', 'datasize': 'bigdata', 'completed': True, 'elapsed_time': 100.0},
            {'framework': 'hadoop', 'workload': 'wordcount', 'datasize': 'bigdata', 'completed': False, 'elapsed_time': 5.0}]
    paths = []
    for n, r in enumerate(recs): q = tmp_path/f'r{n}.json'; q.write_text(json.dumps(r)); paths.append(str(q))
    c = {'app': 'wordcount', 'x': [[0, 0], [1, 1]], 'sources': paths, 'source_hashes': [hashlib.sha256(Path(q).read_bytes()).hexdigest() for q in paths]}
    led = Ledger(tmp_path/'l.json', tmp_path/'j.jsonl', 10, 60); o = HadoopOracle(c, 'k', {'ids': []}, led)
    assert o.acquire(0) == [100.0] and o.acquire(1) == [7200.0] and led.state['acquisitions'] == 2

def test_specific_win_requires_every_switch_and_direction():
    raw = {'sequential_3nn': 10., 'random_full': 10., 'adaptive_neighbor': 10., 'gp_ei': 10., 'llm': 9.}
    assert specific({'direction': 'minimize', 'raw': raw}, .01)
    assert not specific({'direction': 'minimize', 'raw': {**raw, 'gp_ei': 9.05}}, .01)
    assert specific({'direction': 'maximize', 'raw': {**raw, 'llm': 11.}}, .01) and not specific({'direction': 'minimize', 'raw': {**raw, 'llm': None}}, .01)

def test_independent_parser_matches_frozen_parser():
    ds = [[1, 2, 3], [0, 1]]; content = json.dumps(['01', '20', '11', '00', '21', '10', '01', '20', '11', '00'], separators=(',', ':'))
    resp = {'content': content, 'truncated': False, 'stop_type': 'eos', 'tokens_predicted': 30}
    assert [list(x) for x in proposal_v128.parse(resp, ds)] == my_parse(content, ds)

def test_independent_projection_matches_origin_projection():
    rng = random.Random(0)
    for origin, cand, module, prefix in [('v148', 'artifacts/study_v148/candidates/pagerank.json', hadoop_v148, 'artifacts/study_v148/prefixes/pagerank_11.json'),
                                         ('v144', 'artifacts/study_v144/candidates/bayes.json', spark_v144, 'artifacts/study_v144/prefixes/bayes_11.json')]:
        c = json.loads((ROOT/cand).read_text()); p = json.loads((ROOT/prefix).read_text())
        props = [[rng.choice(d) for d in c['grid_domains']] for _ in range(10)]
        assert my_project(origin, c, p, props) == module.project(c, p, props)[0]

def test_independent_hamming_projection_matches_v141_projection():
    from analyze_pointwise_v123 import candidates
    from proposal_v127 import project
    j = json.loads((ROOT/'artifacts/study_v141/jobs.json').read_text())[0]; spec, c = candidates(j['dataset'])
    p = json.loads((ROOT/j['prefix']).read_text())['state']; rng = random.Random(1)
    props = [tuple(rng.choice(d) for d in j['domains']) for _ in range(10)]
    assert my_project('v141', c, p, props) == project(props, c.x, p)[0]

def test_port_wait_returns_on_free_port_and_fails_closed_when_held():
    import socket
    from runtime_v172 import wait_for_port
    with socket.socket() as s:
        s.bind(('127.0.0.1', 0)); port = s.getsockname()[1]
        with pytest.raises(OSError): wait_for_port(port, limit=.3, interval=.1)
    assert wait_for_port(port, limit=2, interval=.1) < 2

def test_stage_map_replaces_failed_a1_with_a1r():
    from common_v172 import STAGES, FAILED_STAGES, ORDER
    assert sorted(STAGES.values()) == [('qwen3_14b', 1), ('qwen3_14b', 2), ('qwen3_8b_redraw', 1), ('qwen3_8b_redraw', 2)]
    assert 'A1' in FAILED_STAGES and 'A1' not in STAGES and ORDER.index('A1') < ORDER.index('A1R') < ORDER.index('A2')

def test_freeze_overlay_order_lets_later_amendments_supersede():
    from common_v172 import FREEZES, frozen_hashes
    assert FREEZES[0] == 'freeze.json' and FREEZES[1:] == [f'freeze_amendment{i}.json' for i in range(1, len(FREEZES))]
    merged = frozen_hashes(); original = json.loads((ROOT/'artifacts/study_v172/freeze.json').read_text())['sha256']
    assert set(original) <= set(merged)

def test_verifier_parser_handles_wide_domains_like_frozen_parser():
    import proposal_v127, verify_v172
    assert verify_v172.ALPHABET == proposal_v127.ALPHABET
    ds = [list(range(19)), [0, 1]]; rows = ['I1', 'A0', '90', 'H1', '00', 'B1', 'C0', 'D1', 'E0', 'F1']
    content = json.dumps(rows, separators=(',', ':')); resp = {'content': content, 'truncated': False, 'stop_type': 'eos', 'tokens_predicted': 30}
    assert [list(x) for x in proposal_v128.parse(resp, ds)] == my_parse(content, ds)
