"""V172 real local inference only (no oracle/optimizer imports); create-once stages P, A1, A2, B1, B2."""
import argparse, time
from collect_smollm_v47 import ROOT, read, write, append, sha, now
from common_v172 import A, M, STAGES, config, verify_freeze, stage_info, require_previous
from runtime_v172 import Runtime, runtime_config
from proposal_v128 import payload, parse
from audit_output_capacity_v127 import vocab

SYNTHETIC_DOMAINS = [[0, 1, 2], [0, 1]]
SYNTHETIC_MESSAGES = [{'role': 'system', 'content': 'Synthetic compatibility check; not a research case. Output only a JSON array of ten two-character strings.'},
                      {'role': 'user', 'content': 'First character is 0, 1 or 2; second character is 0 or 1. Return ten strings.'}]

def render(rt, messages):
    rendered = rt.api('/apply-template', {'messages': messages, 'add_generation_prompt': True, 'chat_template_kwargs': {'enable_thinking': False}})
    tokens = rt.api('/tokenize', {'content': rendered['prompt'], 'add_special': False, 'parse_special': True})['tokens']
    return rendered, tokens

def preflight(cfg):
    out = M/'P'; out.mkdir(parents=True, exist_ok=False); model_key = 'qwen3_14b'; models = read(A/'models.json')
    rt = Runtime(out, runtime_config(cfg, model_key, 0, cfg['compatibility_requests_total'], cfg['preflight_stage_seconds'])); vocabulary = vocab(ROOT/models[model_key]['path'])
    rows = []; error = None; t = time.monotonic()
    try:
        rt.start()
        for j in read(A/'jobs.json'):
            rendered, tokens = render(rt, read(ROOT/j['messages_path'])); hist = read(ROOT/j['historical_qwen3_8b_preflight'])
            proof = rt.authorize(payload(rendered['prompt'], j['sampling_seed'], j['domains']), j['domains'], vocabulary, len(tokens))
            rows.append({'qualified_key': j['qualified_key'], 'prompt_tokens': len(tokens), 'historical_qwen3_8b_prompt_tokens': len(hist['prompt_tokens']),
                         'rendered_equals_historical_qwen3_8b': rendered['prompt'] == hist['rendered']['prompt'], 'tokens_equal_historical_qwen3_8b': tokens == hist['prompt_tokens'], 'capacity': proof})
        rendered, tokens = render(rt, SYNTHETIC_MESSAGES); p = payload(rendered['prompt'], 172999, SYNTHETIC_DOMAINS); rt.authorize(p, SYNTHETIC_DOMAINS, vocabulary, len(tokens))
        start = time.monotonic(); response = rt.generate(p, 'compatibility', 'synthetic_compatibility'); seconds = time.monotonic()-start
        try: parsed = parse(response, SYNTHETIC_DOMAINS); status = 'valid'
        except ValueError as e: parsed = None; status = 'invalid:'+str(e)
        write(out/'compatibility.json', {'synthetic_not_research': True, 'response': response, 'wall_seconds': seconds, 'parsed': parsed, 'status': status})
    except Exception as e: error = repr(e)
    finally: rt.close()
    ledger = read(out/'ledger.json'); cap = cfg['server_rss_cap_bytes'][model_key]
    gate = {'at': now(), 'error': error, 'jobs_checked': len(rows), 'all_capacity_ok': len(rows) == 70, 'rendered_equal_count': sum(r['rendered_equals_historical_qwen3_8b'] for r in rows),
            'token_equal_count': sum(r['tokens_equal_historical_qwen3_8b'] for r in rows), 'peak_server_rss_bytes': ledger['peak_server_rss_bytes'], 'rss_cap_bytes': cap,
            'rss_ok': 0 < ledger['peak_server_rss_bytes'] <= cap, 'seconds': time.monotonic()-t, 'rows': rows}
    gate['passed'] = error is None and gate['all_capacity_ok'] and gate['rss_ok'] and (out/'compatibility.json').exists()
    write(out/'summary.json', gate); print({k: v for k, v in gate.items() if k != 'rows'})
    if not gate['passed']: raise SystemExit('Preflight gate failed; no scientific stage may start')

def collect(stage, cfg):
    info = stage_info(stage, cfg); require_previous(stage, cfg)
    if not read(M/'P'/'summary.json')['passed']: raise RuntimeError('Preflight gate did not pass')
    jobs = [j for j in read(A/'jobs.json') if j['split'] == info['split']]; assert len(jobs) == cfg['requests_per_stage']
    out = M/stage; out.mkdir(parents=True, exist_ok=False); (out/'responses.jsonl').touch(); models = read(A/'models.json'); model = models[info['model_key']]
    rt = Runtime(out, runtime_config(cfg, info['model_key'], cfg['requests_per_stage'], 0, cfg['max_generation_stage_seconds'])); vocabulary = vocab(ROOT/model['path'])
    attempted = []; error = None; t = time.monotonic()
    try:
        rt.start(); prepared = []
        for j in jobs:
            msgs = read(ROOT/j['messages_path']); rendered, tokens = render(rt, msgs); seed = j[info['seed_field']]
            proof = rt.authorize(payload(rendered['prompt'], seed, j['domains']), j['domains'], vocabulary, len(tokens))
            write(out/'preflight'/f"{j['qualified_key'].replace('::', '__')}.json", {**j, 'stage': stage, 'arm': info['arm'], 'model_key': info['model_key'], 'seed_used': seed,
                  'messages': msgs, 'rendered': rendered, 'prompt_tokens': tokens, 'output_capacity': proof})
            prepared.append((j, rendered['prompt'], seed))
        write(out/'preflight_seal.json', {'at': now(), 'sha256': {str(p.relative_to(ROOT)): sha(p) for p in sorted((out/'preflight').glob('*.json'))}})
        for j, prompt, seed in prepared:
            start = time.monotonic(); attempted.append(j['qualified_key'])
            response = rt.generate(payload(prompt, seed, j['domains']), 'scientific', j['qualified_key'])
            append(out/'responses.jsonl', {'qualified_key': j['qualified_key'], 'at': now(), 'response': response, 'wall_seconds': time.monotonic()-start})
            try: score = parse(response, j['domains']); status = 'valid'; err = None
            except ValueError as e: score = None; status = 'invalid'; err = str(e)
            write(out/'scores'/f"{j['qualified_key'].replace('::', '__')}.json", {**j, 'stage': stage, 'arm': info['arm'], 'model_key': info['model_key'], 'seed_used': seed, 'score': score, 'status': status, 'error': err})
            print(stage, j['qualified_key'], status, round(time.monotonic()-start, 1), flush=True)
    except Exception as e: error = repr(e); append(out/'errors.jsonl', {'at': now(), 'error': error})
    finally: rt.close()
    scores = [read(p) for p in (out/'scores').glob('*.json')] if (out/'scores').exists() else []
    write(out/'summary.json', {'at': now(), 'stage': stage, 'arm': info['arm'], 'model_key': info['model_key'], 'intended': len(jobs), 'attempted': len(attempted),
          'responses': len(scores), 'valid': sum(s['status'] == 'valid' for s in scores), 'invalid': sum(s['status'] == 'invalid' for s in scores),
          'unattempted': [j['qualified_key'] for j in jobs if j['qualified_key'] not in attempted], 'error': error, 'seconds': time.monotonic()-t, 'ledger': read(out/'ledger.json')})
    print(read(out/'summary.json'))

def main():
    ap = argparse.ArgumentParser(); ap.add_argument('stage', choices=['P']+list(STAGES)); args = ap.parse_args(); cfg = config(); verify_freeze()
    preflight(cfg) if args.stage == 'P' else collect(args.stage, cfg)

if __name__ == '__main__': main()
