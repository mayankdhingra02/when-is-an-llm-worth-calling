"""Independent JSON/domain, provenance, paired-budget and effect verification."""
import hashlib
import itertools
import json
import math
import statistics
import time
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
def read(p): return json.loads(p.read_text())
def lines(p): return [json.loads(line) for line in p.read_text().splitlines()] if p.exists() else []
def sha(p):
    h = hashlib.sha256()
    with p.open('rb') as f:
        for b in iter(lambda: f.read(1024 * 1024), b''): h.update(b)
    return h.hexdigest()
def eq(a, b): assert math.isclose(a, b, abs_tol=1e-9, rel_tol=1e-12), (a, b)


def main():
    start = time.monotonic()
    raw = ROOT / 'results/v65_sat_llm'
    out = ROOT / 'results/v65_sat_llm_analysis'
    source = ROOT / 'results/v64_sat_screen/minisat_planted_512'
    art = ROOT / 'artifacts/study_v65'
    freeze = ROOT / 'reports/protocol_v65_sat_llm.freeze.json'
    for name, digest in read(freeze)['sha256'].items(): assert sha(ROOT / name) == digest, name
    approval = read(art / 'approval_receipt.json')
    assert approval['authorized_scope_invocation'] and approval['protocol_freeze_sha256'] == sha(freeze)
    cfg = read(ROOT / 'configs/study_v65.json')
    assert approval['scope'] == cfg
    ledger = read(raw / 'ledger.json')
    runtime = read(raw / 'runtime.json')
    assert runtime['config'] == cfg and runtime['command'] == read(art / 'runtime_plan.json')['command']
    assert runtime['model_sha256'] == cfg['model_sha256'] and sha(Path(runtime['command'][0])) == runtime['runtime_binary_sha256']
    assert ledger['stage_seconds'] <= 900 and ledger['retries'] == ledger['objective_accesses'] == ledger['external_spend_usd'] == 0
    assert ledger['server_exit_code'] is not None
    requests = lines(raw / 'request_starts.jsonl')
    responses = lines(raw / 'responses.jsonl')
    assert len(requests) == ledger['generation_requests'] <= 5
    assert len({r['request_id'] for r in requests}) == len(requests)
    assert len({r['seed'] for r in requests}) == len(requests)
    for r in responses:
        req = next(q for q in requests if q['request_id'] == r['request_id'])
        assert all(r[k] == v for k, v in req.items())
    for name, digest in read(raw / 'preflight_seal.json')['sha256'].items(): assert sha(ROOT / name) == digest
    jobs = read(art / 'jobs.json')
    choices = read(raw / 'all_cases.json')
    paired = read(out / 'paired.json')
    table = read(source / 'table.json')
    events = lines(out / 'acquisitions.jsonl')
    summary = read(out / 'summary.json')
    grid = list(itertools.product([.8, .95], [.9, .999], [25, 100, 400], [1.2, 2], [0, 2]))
    assert len(jobs) == len(choices) == len(paired) == 5
    seen_events = []
    valid = 0
    for seed, job, c, p in zip([11, 23, 37, 53, 71], jobs, choices, paired):
        assert seed == job['seed'] == c['seed'] == p['seed']
        prefix = read(source / f'prefix_{seed}.json')
        assert prefix == job['prefix'] and sha(source / f'prefix_{seed}.json') == job['prefix_sha256']
        preflight = read(raw / 'preflight' / f'seed_{seed}.json')
        assert preflight['messages'] == job['messages'] and preflight['prefix'] == prefix
        assert len(preflight['prompt_tokens']) + 1024 <= 4096
        matched = [q for q in requests if q['seed'] == seed]
        if matched:
            payload = matched[0]['payload']
            assert payload == {'prompt': preflight['rendered']['prompt'], 'n_predict': 1024, 'temperature': 0, 'seed': 11, 'cache_prompt': False, 'return_tokens': True, 'stream': False, 'repeat_penalty': 1.0}
        actual = [r for r in responses if r['seed'] == seed]
        selected = []
        is_valid = False
        if actual:
            assert len(actual) == 1
            response = actual[0]['response']
            try:
                proposal = json.loads(response['content'])
                assert isinstance(proposal, list) and len(proposal) == 10
                assert all(isinstance(row, list) and len(row) == 5 and all(type(x) in (int, float) and math.isfinite(x) for x in row) for row in proposal)
                selected = [grid.index(tuple(row)) for row in proposal]
                assert len(set(selected)) == 10 and not set(selected) & {o['config_id'] for o in prefix}
                assert not (response.get('truncated') or response.get('stopped_limit') or response.get('stop_type') == 'limit')
                is_valid = True
            except (ValueError, TypeError, AssertionError): selected = []
            assert response.get('tokens_predicted', 0) <= 1024
            assert c['usage'] == {key: response.get(key) for key in ['tokens_predicted', 'tokens_evaluated']}
            eq(c['wall_seconds'], actual[0]['wall_seconds'])
        assert c['valid'] == is_valid and c['selected_ids'] == selected
        valid += int(is_valid)
        controls = {m: read(source / f'arm_{seed}_{m}.json')['observations'] for m in ['rf_lcb', 'nn', 'random']}
        arm = read(out / f'arm_{seed}.json')
        obs = arm['observations']
        assert arm['prefix_sha256'] == sha(source / f'prefix_{seed}.json')
        assert len(obs) == len({o['config_id'] for o in obs}) == 20 and obs[:10] == prefix
        if is_valid:
            assert arm['branch'] == p['branch'] == 'real_llm_proposals'
            assert [o['config_id'] for o in obs[10:]] == selected
            for step, o in enumerate(obs[10:], 11):
                event = events[o['source_event_id']]
                assert event['event_id'] == o['source_event_id'] and event['case'] == seed and event['arm'] == 'llm_native' and event['inclusive_step'] == step
                assert event['config_id'] == o['config_id'] and event['value_ms'] == o['value_ms'] == table[o['config_id']]['median_ms']
                seen_events.append(event['event_id'])
        else:
            assert arm['branch'] == p['branch'] == 'reused_rf_fallback' and obs == controls['rf_lcb']
        best = min(obs, key=lambda o: (o['value_ms'], o['config_id']))
        ctrl = {m: min(v, key=lambda o: (o['value_ms'], o['config_id'])) for m, v in controls.items()}
        assert p['best'] == best and p['control_best'] == ctrl
        assert p['best_valid_repetitions'] == table[best['config_id']]['valid_repetitions']
        for method, control in ctrl.items():
            delta = control['value_ms'] - best['value_ms']
            eq(p['effects'][method]['absolute_improvement_ms'], delta)
            eq(p['effects'][method]['relative_improvement_percent'], 100 * delta / control['value_ms'])
        delta = ctrl['rf_lcb']['value_ms'] - best['value_ms']
        finite = is_valid and delta > 0 and table[best['config_id']]['valid_repetitions'] == table[ctrl['rf_lcb']['config_id']]['valid_repetitions'] == 3
        assert p['inference_only_break_even_executions'] == (math.ceil(c['wall_seconds'] * 1000 / delta) if finite else None)
        eq(p['hindsight_best_of_two_ms'], min(best['value_ms'], ctrl['rf_lcb']['value_ms']))
    assert sorted(seen_events) == list(range(len(events))) and len(events) == valid * 10 <= 50
    assert ledger['valid_cases'] == summary['valid_cases'] == valid
    assert summary['operational_fallbacks'] == 5 - valid and summary['intended_cases'] == 5
    assert summary['new_recorded_accesses'] == len(events) and summary['generation_requests'] == len(requests)
    for method, effect in summary['effects'].items():
        values = [p['effects'][method]['relative_improvement_percent'] for p in paired]
        eq(effect['mean_relative_improvement_percent'], statistics.mean(values))
        eq(effect['median_relative_improvement_percent'], statistics.median(values))
        assert [effect[k] for k in ['wins', 'ties', 'losses']] == [sum(v > 0 for v in values), sum(v == 0 for v in values), sum(v < 0 for v in values)]
    for key, usage in summary['usage'].items():
        vals = [r['response'].get(key) for r in responses]
        assert usage == {'observed_total': sum(v for v in vals if v is not None), 'known_responses': sum(v is not None for v in vals), 'unknown_attempted_requests': len(requests) - sum(v is not None for v in vals)}
    print(json.dumps({'verified': True, 'intended_cases': 5, 'requests': len(requests), 'valid_native_outputs': valid, 'fallbacks': 5 - valid, 'charged_acquisitions': len(events), 'runtime_seconds': time.monotonic() - start}, indent=2))


if __name__ == '__main__': main()
