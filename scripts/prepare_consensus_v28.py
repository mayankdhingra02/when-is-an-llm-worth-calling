"""Prepare compatible cached real-response selections, without branch labels."""
import os
from pathlib import Path
import sys
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT/'src')); os.chdir(ROOT)
from escalation.io import read, lines, write, digest
from escalation.core import State
from escalation.finite_v6 import load_candidates
from escalation.selection_v8 import shortlist
from escalation.consensus_v28 import select
from escalation.larger_v22 import MODEL_ID, REVISION, require
from verify_reproduction_v26 import decode_tokens


def prepare():
    manifest = read('data/manifest_v8.json')
    jobs = read('data/larger_probe_v22.json')['jobs']
    requests = lines('results/v22_larger/requests.jsonl')
    tokenizer = read('models/Qwen2.5-1.5B-Instruct/tokenizer.json')
    require(len(requests) == len(jobs) == 60, 'Complete source cache')
    cases = []
    for case in manifest['cases']:
        key = f"{case['dataset']}_{case['seed']}"
        prefix = read(f'results/v6/prefixes/{key}.json')['state']
        spec = next(d for d in manifest['datasets'] if d['id'] == case['dataset'])
        require(digest(prefix) == case['prefix_hash'], 'Prefix identity')
        pool = shortlist(load_candidates(spec), State(**prefix), case['seed'])
        require(pool == case['pool'], 'Feature/acquired-only shortlist identity')
        ballots = []; sources = []
        for condition in ('assigned_ids', 'reverse_display', 'reassigned_ids'):
            matching = [j for j in jobs if j['dataset'] == case['dataset'] and j['seed'] == case['seed'] and j['condition'] == condition]
            require(len(matching) == 1, 'Unique job identity'); job = matching[0]
            matching = [r for r in requests if r['job_id'] == job['job_id']]
            require(len(matching) == 1, 'Unique response identity'); r = matching[0]
            require(r['model_id'] == MODEL_ID and r['revision'] == REVISION, 'Model provenance')
            require(r['status'] == 'response' and r['retry'] == 0 and r['parameters'] == {'do_sample': False, 'max_new_tokens': 20}, 'Cache parameters/status')
            require(r['messages'] == job['messages'] and digest(r['messages']) == job['prompt_hash'] == r['prompt_hash'], 'Exact prompt provenance')
            require(r['prefix_hash'] == job['prefix_hash'] == case['prefix_hash'], 'Prefix provenance')
            require(r['mapping'] == job['mapping'] and set(r['mapping'].values()) == set(pool['ranked']), 'Candidate provenance')
            require(decode_tokens(r['generated_token_ids'], tokenizer) == r['raw_output'], 'Raw token decoding')
            ids = r['raw_output'].splitlines()
            require(len(ids) == len(set(ids)) == 10 and set(ids) <= set(job['mapping']), 'Real output grammar')
            ballots.append([job['mapping'][i] for i in ids])
            require(all(r[k] is not None for k in ('input_tokens', 'output_tokens', 'wall_seconds')), 'Known usage')
            sources.append({k: r[k] for k in ('job_id', 'condition', 'request_id', 'prompt_hash', 'cache_key', 'input_tokens', 'output_tokens', 'wall_seconds')})
        cases.append({'dataset': case['dataset'], 'seed': case['seed'], 'system_group': spec['system_group'],
                      'prefix_hash': case['prefix_hash'], 'pool': pool['ranked'], 'ballots': ballots,
                      'sources': sources, **select(pool['ranked'], ballots)})
    require(len(cases) == 15, 'Fifteen intended cases')
    return {'scope': 'Fixed consensus plan from 45 compatible real cached responses; no outcome-based selection', 'cases': cases}


if __name__ == '__main__':
    require(not Path('data/consensus_v28.json').exists(), 'Preserve prepared plan')
    write('data/consensus_v28.json', prepare())
    print('Prepared all15 plans using45 real responses; no branch labels acquired.')
