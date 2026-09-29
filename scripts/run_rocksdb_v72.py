"""One-shot local paired experiment. Requires exact frozen-scope authorization."""
import argparse
import hashlib
import json
import os
import random
import signal
import socket
import subprocess
import sys
import threading
import time
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT/'src'))
from escalation.rocksdb_v69 import grid
from escalation.rocksdb_policy_v72 import SEEDS, METHODS, features, vectors, messages, prior_choice, validate_acquisition
from escalation.classical_java_v54 import choose
from escalation.legal_proposals_v66 import LegalProposals
from escalation.receipts_v70 import atomic_json
from escalation.bounded_process_v57 import run
from run_planning_v55 import rss

OUT = ROOT/'results/v72_rocksdb_paired'
def read(p): return json.loads(p.read_text())
def sha(p):
    h = hashlib.sha256()
    with p.open('rb') as f:
        for b in iter(lambda: f.read(1024*1024), b''): h.update(b)
    return h.hexdigest()
def now(): return datetime.now(timezone.utc).isoformat()
def append(p, obj):
    with p.open('a') as f:
        f.write(json.dumps(obj)+'\n'); f.flush(); os.fsync(f.fileno())


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--approved-envelope-sha256', required=True)
    args = parser.parse_args()
    freeze = ROOT/'reports/protocol_v72.freeze.json'
    if args.approved_envelope_sha256 != sha(freeze):
        raise PermissionError('Exact prospective 35-request scope approval required')
    for name, digest in read(freeze)['sha256'].items():
        if sha(ROOT/name) != digest: raise ValueError('Changed frozen input: '+name)
    cfg = read(ROOT/'configs/study_v72.json')
    assert cfg['max_generation_requests'] == 35 and cfg['max_physical_evaluations'] == 150
    assert cfg['max_output_tokens'] == 64 and cfg['max_stage_seconds'] == 1800
    assert cfg['host'] == '127.0.0.1' and cfg['port'] == 18492
    assert all(cfg[k] == 0 for k in ['retries', 'max_external_spend_usd', 'max_new_download_bytes'])
    rss(-1)  # permission check before any collection
    with socket.socket() as sock: sock.bind((cfg['host'], cfg['port']))
    OUT.mkdir(exist_ok=False)
    command = read(ROOT/'artifacts/study_v72/runtime_plan.json')['command']
    atomic_json(OUT/'authorization.json', {'at': now(), 'approved_envelope_sha256': args.approved_envelope_sha256, 'scope': cfg})
    atomic_json(OUT/'runtime.json', {'command': command, 'config': cfg, 'binary_sha256': sha(Path(command[0])), 'model_sha256': sha(Path(command[command.index('-m')+1])), 'seed_support': 'Requested fixed seed per prefix; cross-device determinism not guaranteed'})
    configs = grid(); x = features(configs); rows = []; cases = []; proc = None
    started = time.monotonic(); finished = threading.Event(); guard = {'reason': None, 'peak_server_rss_bytes': 0}
    ledger = {'generation_requests': 0, 'http_requests': 0, 'retries': 0, 'fallback_search_evaluations': 0, 'external_spend_usd': 0, 'started_at': now()}
    opener = urllib.request.build_opener(urllib.request.ProxyHandler({}))

    def check():
        if guard['reason']: raise RuntimeError(guard['reason'])
        if time.monotonic()-started > 1640: raise TimeoutError('Stage reserve reached')
        if proc is not None and proc.poll() is not None: raise RuntimeError('Model server exited')

    def watchdog():
        while not finished.wait(.5):
            try:
                if proc is not None and proc.poll() is None:
                    guard['peak_server_rss_bytes'] = max(guard['peak_server_rss_bytes'], rss(proc.pid))
                if time.monotonic()-started >= 1790: guard['reason'] = 'stage_timeout'
                if guard['peak_server_rss_bytes'] > 8*1024**3: guard['reason'] = 'server_rss_cap'
            except Exception as error: guard['reason'] = 'watchdog_error: '+repr(error)
            if guard['reason']:
                if proc is not None and proc.poll() is None:
                    try: os.killpg(proc.pid, signal.SIGKILL)
                    except ProcessLookupError: pass
                return

    def api(route, payload=None):
        if route not in ('/health', '/apply-template', '/tokenize', '/completion'): raise ValueError('Disallowed endpoint')
        check(); ledger['http_requests'] += 1
        req = urllib.request.Request(f"http://127.0.0.1:{cfg['port']}"+route,
            data=None if payload is None else json.dumps(payload).encode(), headers={'Content-Type': 'application/json'})
        with opener.open(req, timeout=120) as response: return json.load(response)

    def acquire(cid, obs, seed, arm, purpose='search'):
        check(); validate_acquisition(cid, obs, purpose, len(rows))
        folder = OUT/f'eval_{len(rows):03d}'; folder.mkdir()
        spec = {'seed': seed, 'arm': arm, 'ordinal': len(obs)+1, 'config_id': cid, 'config': configs[cid], 'purpose': purpose}
        atomic_json(folder/'spec.json', spec)
        row = {**spec, 'status': 'intended', 'path': str(folder.relative_to(ROOT)), 'at': now()}
        rows.append(row); append(OUT/'charges.jsonl', row)
        def monitor(pid):
            value = rss(pid)
            return {'rss_bytes': value}, guard['reason'] or ('rss_cap' if value > 2*1024**3 else None)
        receipt = run([sys.executable, str(ROOT/'scripts/worker_rocksdb_v71.py'), str(folder/'spec.json')],
                      cwd=ROOT, log_path=folder/'worker.log', wall_cap=120, monitor=monitor)
        atomic_json(folder/'supervision.json', receipt)
        result = read(folder/'result.json') if (folder/'result.json').exists() else {'status': 'missing_result'}
        row.update(status=result['status'], supervision=receipt)
        if receipt['exit_code'] or receipt['termination_reason'] or result['status'] != 'valid':
            row['status'] = 'failed'; atomic_json(OUT/'acquisitions.json', rows)
            raise RuntimeError('Physical acquisition failed; no retry')
        row['value_ms'] = result['objective_verified_loop_seconds']*1000
        atomic_json(OUT/'acquisitions.json', rows)
        return {'config_id': cid, 'value_ms': row['value_ms'], 'physical_receipt': row['path']}

    def llm_choice(session, obs, seed):
        check()
        if ledger['generation_requests'] >= 35: raise ValueError('Request cap')
        request_id = f'v72_seed{seed}_step{len(obs)-9}'
        folder = OUT/request_id; folder.mkdir()
        msgs = messages(configs, obs)
        atomic_json(folder/'messages.json', msgs)
        rendered = api('/apply-template', {'messages': msgs, 'add_generation_prompt': True, 'chat_template_kwargs': {'enable_thinking': False}})
        tokens = api('/tokenize', {'content': rendered['prompt'], 'add_special': False, 'parse_special': True})['tokens']
        atomic_json(folder/'rendered.json', {'rendered': rendered, 'tokens': tokens})
        if len(tokens)+64 > 4096: raise ValueError('Context overflow; stop before generation')
        proposal = session.begin_request()
        payload = {'prompt': rendered['prompt'], 'grammar': proposal['grammar'], 'n_predict': 64,
                   'temperature': 0, 'seed': seed, 'cache_prompt': False, 'return_tokens': True,
                   'stream': False, 'repeat_penalty': 1.0}
        request = {'request_id': request_id, 'at': now(), 'payload': payload, 'eligible_ids': proposal['eligible_ids'], 'prompt_sha256': hashlib.sha256(rendered['prompt'].encode()).hexdigest()}
        ledger['generation_requests'] += 1
        atomic_json(OUT/'ledger.json', ledger); atomic_json(folder/'request.json', request)
        append(OUT/'request_starts.jsonl', {'request_id': request_id, 'at': request['at']})
        t = time.monotonic()
        try:
            response = api('/completion', payload)
            atomic_json(folder/'response.json', response)
        except Exception as error:
            parsed = session.finish_request(transport_error=repr(error))
            atomic_json(folder/'decision.json', {**parsed, 'error': repr(error), 'wall_seconds': time.monotonic()-t, 'usage': None})
            raise  # transport/grammar engine errors stop the entire run, retaining denominator
        parsed = session.finish_request(response.get('content'), truncated=bool(response.get('truncated') or response.get('stopped_limit') or response.get('stop_type') == 'limit'))
        decision = {**parsed, 'wall_seconds': time.monotonic()-t, 'usage': {'tokens_predicted': response.get('tokens_predicted'), 'tokens_evaluated': response.get('tokens_evaluated')}}
        atomic_json(folder/'decision.json', decision)
        if response.get('tokens_predicted') is not None and response['tokens_predicted'] > 64: raise ValueError('Server violated token cap')
        return parsed['selected_id']

    thread = threading.Thread(target=watchdog, daemon=True); stop = None
    try:
        with (OUT/'server.log').open('xb') as log:
            proc = subprocess.Popen(command, cwd=ROOT, stdout=log, stderr=log, start_new_session=True,
                env={k: v for k, v in os.environ.items() if not k.startswith(('LLAMA_', 'HF_', 'HUGGING_FACE_'))})
        thread.start()
        health_start = time.monotonic()
        while True:
            if time.monotonic()-health_start > 120: raise TimeoutError('Model startup timeout')
            try:
                if api('/health').get('status') == 'ok': break
            except (OSError, ValueError): time.sleep(.25)
        ledger['startup_seconds'] = time.monotonic()-started
        for seed in SEEDS:
            path = ROOT/f'results/v71_rocksdb_classical/prefix_{seed}.json'
            prefix = read(path); assert len(prefix) == 10
            arms = {m: [dict(o) for o in prefix] for m in METHODS}
            case = {'seed': seed, 'prefix_sha256': sha(path), 'arms': arms, 'confirmation': {m: [] for m in METHODS}, 'fallback_steps': []}
            cases.append(case); atomic_json(OUT/f'case_{seed}.json', case)
            session = LegalProposals(vectors(configs), [o['config_id'] for o in prefix], count=7)
            rng = random.Random(seed+72000)
            for step in range(7):
                order = list(METHODS); rng.shuffle(order)
                for method in order:
                    obs = arms[method]; t = time.monotonic()
                    if method == 'domain_prior': cid = prior_choice(configs, obs)
                    elif method == 'rf_lcb': cid = int(choose(x, obs, method, seed))
                    else:
                        cid = None if session.failure else llm_choice(session, obs, seed)
                        if cid is None:
                            cid = int(choose(x, obs, 'rf_lcb', seed))
                            ledger['fallback_search_evaluations'] += 1
                            case['fallback_steps'].append(step+1)
                    append(OUT/'selection_costs.jsonl', {'seed': seed, 'arm': method, 'step': step+1, 'seconds': time.monotonic()-t, 'config_id': cid})
                    obs.append(acquire(cid, obs, seed, method))
                    atomic_json(OUT/f'case_{seed}.json', case)
            case['selected_config_ids'] = {m: min(obs, key=lambda o: o['value_ms'])['config_id'] for m, obs in arms.items()}
            atomic_json(OUT/f'case_{seed}.json', case)
            for rep in range(3):
                order = list(METHODS); rng.shuffle(order)
                for method in order:
                    conf = case['confirmation'][method]
                    conf.append(acquire(case['selected_config_ids'][method], arms[method]+conf, seed, method, 'confirmation'))
                    atomic_json(OUT/f'case_{seed}.json', case)
            print('completed seed', seed, 'physical', len(rows), 'requests', ledger['generation_requests'], flush=True)
    except Exception as error:
        stop = repr(error); atomic_json(OUT/'failure.json', {'error': stop})
    finally:
        finished.set()
        if thread.ident is not None: thread.join(timeout=3)
        if proc is not None and proc.poll() is None:
            os.killpg(proc.pid, signal.SIGTERM)
            try: proc.wait(timeout=3)
            except subprocess.TimeoutExpired: os.killpg(proc.pid, signal.SIGKILL); proc.wait(timeout=3)
        ledger.update(finished_at=now(), seconds=time.monotonic()-started, stop_reason=stop,
                      resource_guard=guard, server_exit_code=None if proc is None else proc.returncode,
                      intended_generation_requests=35, unattempted_generation_requests=35-ledger['generation_requests'])
        atomic_json(OUT/'ledger.json', ledger)
        atomic_json(OUT/'summary.json', {'complete': stop is None and len(rows)==150,
            'intended_physical_evaluations': 150, 'charged_evaluations': len(rows),
            'successful_evaluations': sum(r['status']=='valid' for r in rows), 'unattempted': 150-len(rows),
            'planned_logical_evaluations': 300, 'actual_new_physical_charges': len(rows),
            'historical_shared_prefix_physical_evaluations': 50,
            'independent_system_families': 1, 'cases': cases, 'ledger': ledger})
    if stop: raise RuntimeError(stop)


if __name__ == '__main__': main()
