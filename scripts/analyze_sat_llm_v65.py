"""Frozen five-case analysis; acquire only valid native proposals through oracle."""
import hashlib
import json
import math
import statistics
import sys
import time
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'src'))
from escalation.classical_java_v54 import RecordedOracle
from escalation.sat_llm_v65 import parse_response
def read(p): return json.loads(p.read_text())
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def write(p, obj): p.write_text(json.dumps(obj, indent=2) + '\n')


def main():
    start = time.monotonic()
    out = ROOT / 'results/v65_sat_llm_analysis'
    raw = ROOT / 'results/v65_sat_llm'
    source = ROOT / 'results/v64_sat_screen/minisat_planted_512'
    freeze = ROOT / 'reports/protocol_v65_sat_llm.freeze.json'
    for name, digest in read(freeze)['sha256'].items():
        # Weight/binary provenance already checked by live collector; avoid a large in-memory read.
        if name.startswith(('models/', '.local-runtime/')): continue
        assert sha(ROOT / name) == digest, name
    approval = read(ROOT / 'artifacts/study_v65/approval_receipt.json')
    assert approval['protocol_freeze_sha256'] == sha(freeze)
    ledger = read(raw / 'ledger.json')
    assert ledger['generation_requests'] <= 5 and ledger['retries'] == ledger['objective_accesses'] == ledger['external_spend_usd'] == 0
    jobs = read(ROOT / 'artifacts/study_v65/jobs.json')
    choices = read(raw / 'all_cases.json')
    assert [c['seed'] for c in choices] == [11, 23, 37, 53, 71]
    response_path = raw / 'responses.jsonl'
    responses = {r['seed']: r for r in map(json.loads, response_path.read_text().splitlines())} if response_path.exists() else {}
    table = read(source / 'table.json')
    oracle = RecordedOracle([r['median_ms'] for r in table])
    out.mkdir(exist_ok=False)
    paired = []
    for job, choice in zip(jobs, choices):
        assert time.monotonic() - start < 180
        seed = job['seed']
        assert seed == choice['seed']
        prefix = read(source / f'prefix_{seed}.json')
        assert prefix == job['prefix']
        controls = {m: read(source / f'arm_{seed}_{m}.json')['observations'] for m in ['rf_lcb', 'nn', 'random']}
        assert all(c[:10] == prefix and len(c) == 20 for c in controls.values())
        if choice['status'] in ['valid', 'invalid']:
            response = responses[seed]['response']
            parsed = parse_response(response['content'], prefix, bool(response.get('truncated') or response.get('stopped_limit') or response.get('stop_type') == 'limit'))
            assert all(choice[k] == v for k, v in parsed.items())
        if choice['valid']:
            obs = [dict(p) for p in prefix]
            for cid in choice['selected_ids']:
                assert len(oracle.events) < 50
                obs.append(oracle.acquire(cid, obs, seed, 'llm_native'))
            branch = 'real_llm_proposals'
        else:
            obs = controls['rf_lcb']
            branch = 'reused_rf_fallback'
        assert len(obs) == len({o['config_id'] for o in obs}) == 20 and obs[:10] == prefix
        write(out / f'arm_{seed}.json', {'branch': branch, 'prefix_sha256': sha(source / f'prefix_{seed}.json'), 'observations': obs})
        best = min(obs, key=lambda o: (o['value_ms'], o['config_id']))
        ctrl = {m: min(v, key=lambda o: (o['value_ms'], o['config_id'])) for m, v in controls.items()}
        effects = {m: {'absolute_improvement_ms': o['value_ms'] - best['value_ms'], 'relative_improvement_percent': 100 * (o['value_ms'] - best['value_ms']) / o['value_ms']} for m, o in ctrl.items()}
        delta = effects['rf_lcb']['absolute_improvement_ms']
        fully_valid = table[best['config_id']]['valid_repetitions'] == table[ctrl['rf_lcb']['config_id']]['valid_repetitions'] == 3
        break_even = math.ceil(choice['wall_seconds'] * 1000 / delta) if delta > 0 and choice['valid'] and fully_valid else None
        paired.append({'seed': seed, 'status': choice['status'], 'branch': branch, 'best': best, 'best_valid_repetitions': table[best['config_id']]['valid_repetitions'], 'control_best': ctrl, 'effects': effects, 'inference_only_break_even_executions': break_even, 'request_seconds': choice.get('wall_seconds'), 'hindsight_best_of_two_ms': min(best['value_ms'], ctrl['rf_lcb']['value_ms'])})
    (out / 'acquisitions.jsonl').write_text(''.join(json.dumps(e) + '\n' for e in oracle.events))
    write(out / 'paired.json', paired)
    effects = {}
    for method in ['rf_lcb', 'nn', 'random']:
        values = [p['effects'][method]['relative_improvement_percent'] for p in paired]
        effects[method] = {'mean_relative_improvement_percent': statistics.mean(values), 'median_relative_improvement_percent': statistics.median(values), 'wins': sum(v > 0 for v in values), 'ties': sum(v == 0 for v in values), 'losses': sum(v < 0 for v in values)}
    usage = {}
    for key in ['tokens_predicted', 'tokens_evaluated']:
        values = [r['response'].get(key) for r in responses.values()]
        usage[key] = {'observed_total': sum(v for v in values if v is not None), 'known_responses': sum(v is not None for v in values), 'unknown_attempted_requests': ledger['generation_requests'] - sum(v is not None for v in values)}
    write(out / 'summary.json', {'intended_cases': 5, 'valid_cases': sum(c['valid'] for c in choices), 'operational_fallbacks': sum(not c['valid'] for c in choices), 'generation_requests': ledger['generation_requests'], 'new_recorded_accesses': len(oracle.events), 'effects': effects, 'usage': usage, 'independent_system_groups': 1, 'router_evidence': 'insufficient; no fitted router or independent-group confirmation', 'runtime_seconds': time.monotonic() - start, 'collection_seconds': ledger['stage_seconds'], 'startup_seconds': ledger.get('startup_seconds'), 'external_spend_usd': 0})


if __name__ == '__main__': main()
