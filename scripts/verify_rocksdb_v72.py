"""Independent receipt replay; no inference or database execution."""
import json
import random
import sys
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT/'src'))
from run_rocksdb_v72 import sha, read
from escalation.rocksdb_v69 import grid
from escalation.rocksdb_policy_v72 import SEEDS, METHODS, features, vectors, messages, prior_choice
from escalation.classical_java_v54 import choose
from escalation.legal_proposals_v66 import LegalProposals
from escalation.rocksdb_binding_v69 import active_readback


def verify():
    for n, h in read(ROOT/'reports/protocol_v72.freeze.json')['sha256'].items():
        assert sha(ROOT/n) == h, n
    out = ROOT/'results/v72_rocksdb_paired'
    summary = read(out/'summary.json'); assert summary['complete'], 'Incomplete intended study'
    ledger = read(out/'ledger.json')
    assert ledger['seconds'] <= 1800 and ledger['stop_reason'] is None
    assert ledger['generation_requests'] <= 35 and ledger['retries'] == 0
    assert ledger['resource_guard']['reason'] is None
    assert ledger['resource_guard']['peak_server_rss_bytes'] <= 8*1024**3
    assert ledger['server_exit_code'] is not None
    charges = [json.loads(line) for line in (out/'charges.jsonl').read_text().splitlines()]
    rows = read(out/'acquisitions.json'); assert len(charges) == len(rows) == 150
    configs = grid(); x = features(configs); position = 0; requests = 0; fallbacks = 0
    request_order = []
    costs = [json.loads(line) for line in (out/'selection_costs.jsonl').read_text().splitlines()]
    # Verified V71 uses exactly the same fixed trace/data and response oracle.
    reference = read(ROOT/'results/v71_rocksdb_classical/eval_000/result.json')
    def take(seed, method, ordinal, cid, purpose):
        nonlocal position
        charge, row = charges[position], rows[position]
        folder = ROOT/row['path']; result = read(folder/'result.json'); supervision = read(folder/'supervision.json')
        spec = read(folder/'spec.json')
        expected = dict(seed=seed, arm=method, ordinal=ordinal, config_id=cid, config=configs[cid], purpose=purpose)
        assert spec == expected
        for key, value in expected.items(): assert charge[key] == row[key] == value
        assert result['status'] == row['status'] == 'valid'
        assert supervision['exit_code'] == 0 and supervision['termination_reason'] is None
        assert supervision['wall_seconds'] <= 120 and supervision['sampled_maxima']['rss_bytes'] <= 2*1024**3
        active_readback(folder/'db', configs[cid])
        assert read(folder/'warmup.json')['cache_usage_bytes'] > 0
        for key in ['timed_response_sha256', 'successful_timed_reads', 'verified_timed_reads', 'initial_validation', 'final_validation']:
            assert result[key] == reference[key], (str(folder), key)
        assert read(folder/'timed.json')['objective_verified_loop_seconds'] == result['objective_verified_loop_seconds']
        assert row['value_ms'] == result['objective_verified_loop_seconds']*1000
        inventory = read(folder/'database_file_inventory.json')
        for p in (folder/'db').iterdir(): assert sha(p) == inventory[p.name]['sha256']
        position += 1
        return {'config_id': cid, 'value_ms': row['value_ms'], 'physical_receipt': row['path']}
    cost_pos = 0
    for seed in SEEDS:
        prefixpath = ROOT/f'results/v71_rocksdb_classical/prefix_{seed}.json'
        prefix = read(prefixpath); case = read(out/f'case_{seed}.json')
        assert case['prefix_sha256'] == sha(prefixpath)
        arms = {m: [dict(o) for o in prefix] for m in METHODS}
        legal = LegalProposals(vectors(configs), [o['config_id'] for o in prefix], count=7)
        rng = random.Random(seed+72000); fallback_steps = []
        for step in range(7):
            order = list(METHODS); rng.shuffle(order)
            for method in order:
                obs = arms[method]
                if method == 'domain_prior': cid = prior_choice(configs, obs)
                elif method == 'rf_lcb': cid = int(choose(x, obs, method, seed))
                else:
                    cid = None
                    if not legal.failure:
                        rid = f'v72_seed{seed}_step{step+1}'; folder = out/rid
                        assert read(folder/'messages.json') == messages(configs, obs)
                        request = read(folder/'request.json'); response = read(folder/'response.json'); decision = read(folder/'decision.json')
                        allowed = legal.begin_request(); requests += 1; request_order.append(rid)
                        assert request['eligible_ids'] == allowed['eligible_ids']
                        assert request['payload']['grammar'] == allowed['grammar']
                        rendered = read(folder/'rendered.json')
                        assert request['payload']['prompt'] == rendered['rendered']['prompt']
                        assert len(rendered['tokens'])+64 <= 4096
                        assert request['payload']['n_predict'] == 64 and request['payload']['temperature'] == 0
                        parsed = legal.finish_request(response.get('content'), truncated=bool(response.get('truncated') or response.get('stopped_limit') or response.get('stop_type') == 'limit'))
                        for key, value in parsed.items(): assert decision[key] == value
                        assert decision['usage']['tokens_predicted'] == response.get('tokens_predicted')
                        assert response.get('tokens_predicted', 0) <= 64
                        cid = parsed['selected_id']
                    if cid is None:
                        cid = int(choose(x, obs, 'rf_lcb', seed)); fallback_steps.append(step+1); fallbacks += 1
                cost = costs[cost_pos]; cost_pos += 1
                assert (cost['seed'], cost['arm'], cost['step'], cost['config_id']) == (seed, method, step+1, cid)
                assert cost['seconds'] >= 0
                obs.append(take(seed, method, len(obs)+1, cid, 'search'))
        assert case['arms'] == arms and case['fallback_steps'] == fallback_steps
        selected = {m: min(obs, key=lambda o: o['value_ms'])['config_id'] for m, obs in arms.items()}
        assert selected == case['selected_config_ids']
        confirmed = {m: [] for m in METHODS}
        for rep in range(3):
            order = list(METHODS); rng.shuffle(order)
            for method in order: confirmed[method].append(take(seed, method, 18+rep, selected[method], 'confirmation'))
        assert confirmed == case['confirmation']
        for method in METHODS:
            assert len({o['config_id'] for o in arms[method]}) == 17
            assert len(arms[method])+len(confirmed[method]) == 20
    assert position == 150 and cost_pos == len(costs) == 105
    assert requests == ledger['generation_requests'] and fallbacks == ledger['fallback_search_evaluations']
    starts = [json.loads(line)['request_id'] for line in (out/'request_starts.jsonl').read_text().splitlines()]
    assert starts == request_order
    assert not list((ROOT/'.scratch-v71').iterdir())
    return {'verified': True, 'physical_trials': 150, 'search_decisions_replayed': 105,
            'confirmation_charges': 45, 'requests_replayed': requests, 'fallback_steps': fallbacks,
            'logical_arm_evaluations': 300, 'new_requests_or_queries': 0, 'independent_families': 1}


if __name__ == '__main__': print(json.dumps(verify(), indent=2))
