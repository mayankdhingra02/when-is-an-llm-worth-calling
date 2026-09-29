"""Execute frozen, capped classical collection; never invoke an LLM."""
import hashlib, os, sys, time
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]; sys.path.insert(0, str(ROOT/'src')); os.chdir(ROOT)
from escalation.io import read, write, append, lines, digest, now
from escalation.core import initial_state
from escalation.finite_domain import recommend
from escalation.finite_v6 import load_candidates, features
from escalation.selection_v8 import shortlist
from escalation.transfer_v41 import restrict, IndexedOracle, branch, messages, MODES, current_config
from escalation.resources import Resources

OUT = Path('results/v41_transfer')

def verify_freeze():
    for p, h in read('reports/protocol_v41_transfer.freeze.json')['sha256'].items():
        if hashlib.sha256(Path(p).read_bytes()).hexdigest() != h: raise ValueError('Frozen input changed: '+p)

def main():
    if OUT.exists(): raise ValueError('Preserve prior attempt; no implicit restart')
    verify_freeze(); manifest = read('data/manifest_v41.json')
    before = read('artifacts/resource_ledger_v2.json'); acquired = 0; stop = None
    with Resources(current_config(), 'artifacts/resource_ledger_v2.json') as resource:
        if resource.remaining() < 310: raise RuntimeError('Need 300-second stage plus cleanup reserve')
        deadline = time.monotonic()+300
        write(OUT/'started.json', {'at': now(), 'prefixes': 30, 'arms': 210, 'maximum_acquisitions': 2400, 'baseline_ledger': before})
        try:
            for spec in manifest['datasets']:
                c, subset = restrict(load_candidates(spec), spec['fixed_features'])
                if subset != spec['subset']: raise ValueError('Changed admitted feature domain')
                for seed in manifest['seeds']:
                    key = f"{spec['id']}_{seed}"
                    context = {'dataset': spec['id'], 'system_group': spec['system_group'], 'seed': seed,
                               'namespace': 'measured_v41', 'split': 'prospective_test', 'arm': 'prefix'}
                    def oracle_for(prefix=None):
                        return IndexedOracle(spec, c, prefix, lambda e: append(OUT/'acquisitions.jsonl', {**context, **e, 'at': now()}))
                    oracle = oracle_for()
                    def acquire(i):
                        nonlocal acquired
                        resource.check()
                        if time.monotonic() >= deadline or acquired >= 2400: raise RuntimeError('Stage time/acquisition limit')
                        acquired += 1
                        return oracle.acquire(i)
                    start = time.perf_counter(); prefix = initial_state(c, seed)
                    for _ in range(10):
                        row = recommend(c, prefix); prefix.observe(row, acquire(row), c.directions)
                        write(OUT/'prefix_checkpoints'/f'{key}.json', prefix.record())
                    pool = shortlist(c, prefix, seed); f, feature_seconds = features(c, prefix, seed)
                    prompt = messages(c, prefix, pool)
                    record = {**context, 'state': prefix.record(), 'prefix_hash': digest(prefix.record()), 'pool': pool,
                              'features': f, 'messages': prompt, 'prompt_hash': digest(prompt), 'at': now(),
                              'actual_new_accesses': oracle.new_accesses, 'prefix_seconds': time.perf_counter()-start,
                              'feature_seconds': feature_seconds}
                    write(OUT/'prefixes'/f'{key}.json', record)
                    for mode in MODES:
                        context.update(arm=mode, prefix_hash=record['prefix_hash'])
                        oracle = oracle_for(prefix.record()); start = time.perf_counter()
                        state = branch(c, prefix, pool['ranked'], seed, mode, acquire)
                        write(OUT/'arms'/f'{key}_{mode}.json', {**context, 'status': 'completed', 'state': state.record(),
                              'logical_evaluations': 20, 'actual_new_accesses': oracle.new_accesses,
                              'branch_seconds': time.perf_counter()-start})
                    print(key, 'seven arms completed', flush=True)
            # Tokenization is real; no synthetic labels/model inference. Saved prompts
            # already preceded all continuation outcomes and cannot be edited here.
            os.environ.update(HF_HUB_OFFLINE='1', TRANSFORMERS_OFFLINE='1', TOKENIZERS_PARALLELISM='false')
            from transformers import AutoTokenizer
            preflight = []
            for size in ('0.5', '1.5'):
                tokenizer = AutoTokenizer.from_pretrained(f'models/Qwen2.5-{size}B-Instruct', local_files_only=True, trust_remote_code=False)
                for path in sorted((OUT/'prefixes').glob('*.json')):
                    r = read(path); ids = tokenizer.apply_chat_template(r['messages'], tokenize=True, add_generation_prompt=True)
                    preflight.append({'case': path.stem, 'model_size': size, 'input_tokens': len(ids),
                                      'within_4096': len(ids) <= 4096, 'prompt_hash': r['prompt_hash']})
            write(OUT/'model_preflight.json', {'inference_executed': False, 'rows': preflight, 'all_fit': all(r['within_4096'] for r in preflight)})
        except Exception as e:
            stop = f'{type(e).__name__}: {e}'
        finally:
            statuses = [{'dataset': d['id'], 'seed': seed, 'arm': mode,
                         'status': 'completed' if (OUT/'arms'/f"{d['id']}_{seed}_{mode}.json").exists() else 'incomplete_or_unattempted'}
                        for d in manifest['datasets'] for seed in manifest['seeds'] for mode in MODES]
            write(OUT/'progress.json', {'complete': all(r['status'] == 'completed' for r in statuses) and stop is None,
                'arms': statuses, 'stop_reason': stop, 'actual_new_accesses': len(lines(OUT/'acquisitions.jsonl'))})
    after = read('artifacts/resource_ledger_v2.json')
    if after['requests'] != before['requests']: raise AssertionError('Classical run issued a model request')
    write('artifacts/study_v41/collection_accounting.json', {'charged_seconds': after['experiment_seconds']-before['experiment_seconds'],
        'cumulative_seconds': after['experiment_seconds'], 'new_objective_acquisitions': len(lines(OUT/'acquisitions.jsonl')),
        'new_model_calls': 0, 'external_spend_usd': 0, 'active_since': after['active_since']})
    if stop: raise RuntimeError(stop)
    paths = sorted((OUT/'prefixes').glob('*.json')) + sorted((OUT/'arms').glob('*.json')) + [OUT/'model_preflight.json', OUT/'acquisitions.jsonl']
    write(OUT/'collection_seal.json', {'at': now(), 'sha256': {str(p): hashlib.sha256(p.read_bytes()).hexdigest() for p in paths}})

if __name__ == '__main__': main()
