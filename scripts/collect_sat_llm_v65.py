"""Five real native local completions; no objective tables read by this collector."""
import argparse
import hashlib
import json
import os
import signal
import socket
import subprocess
import sys
import time
import urllib.request
from datetime import datetime, timezone
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'src'))
from escalation.sat_llm_v65 import parse_response
OUT = ROOT / 'results/v65_sat_llm'
ART = ROOT / 'artifacts/study_v65'


def read(p): return json.loads(p.read_text())
def write(p, obj):
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(obj, indent=2) + '\n')
def append(p, obj):
    with p.open('a') as f: f.write(json.dumps(obj) + '\n')
def now(): return datetime.now(timezone.utc).isoformat()
def sha(p):
    h = hashlib.sha256()
    with p.open('rb') as f:
        for b in iter(lambda: f.read(1024 * 1024), b''): h.update(b)
    return h.hexdigest()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--approved-envelope-sha256')
    args = parser.parse_args()
    freeze = ROOT / 'reports/protocol_v65_sat_llm.freeze.json'
    if args.approved_envelope_sha256 != sha(freeze):
        raise PermissionError('Explicit approval of exact five-request envelope required')
    cfg = read(ROOT / 'configs/study_v65.json')
    assert cfg['max_generation_requests'] == 5 and cfg['max_stage_seconds'] == 900
    assert cfg['max_output_tokens'] == 1024 and cfg['context_tokens'] == 4096
    assert cfg['host'] == '127.0.0.1' and cfg['port'] == 18485
    assert all(cfg[k] == 0 for k in ['retries', 'max_external_spend_usd', 'max_new_download_bytes'])
    for name, digest in read(freeze)['sha256'].items():
        assert sha(ROOT / name) == digest, name
    if OUT.exists(): raise ValueError('No implicit restart')
    OUT.mkdir()
    jobs = read(ART / 'jobs.json')
    assert [j['seed'] for j in jobs] == cfg['seeds'] and len(jobs) == 5
    command = read(ART / 'runtime_plan.json')['command']
    assert sha(Path(command[command.index('-m') + 1])) == cfg['model_sha256']
    write(ART / 'approval_receipt.json', {'authorized_scope_invocation': True, 'at': now(), 'protocol_freeze_sha256': args.approved_envelope_sha256, 'scope': cfg})
    ledger = {'started_at': now(), 'generation_requests': 0, 'http_requests': 0, 'completed_cases': 0, 'valid_cases': 0, 'retries': 0, 'objective_accesses': 0, 'external_spend_usd': 0}
    write(OUT / 'runtime.json', {'command': command, 'config': cfg, 'runtime_binary_sha256': sha(Path(command[0])), 'model_sha256': cfg['model_sha256'], 'seed_support': 'Requested seed11; cross-device deterministic output is not guaranteed'})
    started = time.monotonic()
    proc = None
    stop = None
    cases = []
    opener = urllib.request.build_opener(urllib.request.ProxyHandler({}))

    def api(route, payload=None):
        assert route in ['/health', '/apply-template', '/tokenize', '/completion']
        left = cfg['max_stage_seconds'] - (time.monotonic() - started) - 5
        if left <= 0: raise TimeoutError('Stage cap')
        ledger['http_requests'] += 1
        req = urllib.request.Request(f"http://127.0.0.1:{cfg['port']}" + route, data=None if payload is None else json.dumps(payload).encode(), headers={'Content-Type': 'application/json'})
        with opener.open(req, timeout=min(cfg['request_timeout_seconds'], left)) as response:
            return json.load(response)
    try:
        with socket.socket() as sock: sock.bind((cfg['host'], cfg['port']))
        with (ART / 'server.log').open('w') as log:
            proc = subprocess.Popen(command, stdout=log, stderr=log, cwd=ROOT, start_new_session=True, env={k: v for k, v in os.environ.items() if not k.startswith(('LLAMA_', 'HF_', 'HUGGING_FACE_'))})
        for _ in range(100):
            if proc.poll() is not None: raise RuntimeError('Server startup failed')
            try:
                if api('/health').get('status') == 'ok': break
            except (OSError, ValueError): time.sleep(.2)
        else: raise TimeoutError('Health timeout')
        ledger['startup_seconds'] = time.monotonic() - started
        prepared = []
        for job in jobs:
            rendered = api('/apply-template', {'messages': job['messages'], 'add_generation_prompt': True, 'chat_template_kwargs': {'enable_thinking': False}})
            ids = api('/tokenize', {'content': rendered['prompt'], 'add_special': False, 'parse_special': True})['tokens']
            assert len(ids) + cfg['max_output_tokens'] <= cfg['context_tokens']
            write(OUT / 'preflight' / f"seed_{job['seed']}.json", {**job, 'rendered': rendered, 'prompt_tokens': ids})
            prepared.append((job, rendered['prompt']))
        write(OUT / 'preflight_seal.json', {'at': now(), 'sha256': {str(p.relative_to(ROOT)): sha(p) for p in sorted((OUT / 'preflight').glob('*.json'))}})
        for job, prompt in prepared:
            if time.monotonic() - started > cfg['max_stage_seconds'] - 155: raise TimeoutError('Insufficient remaining request allowance')
            assert ledger['generation_requests'] < 5
            payload = {'prompt': prompt, 'n_predict': 1024, 'temperature': 0, 'seed': 11, 'cache_prompt': False, 'return_tokens': True, 'stream': False, 'repeat_penalty': 1.0}
            request = {'request_id': f"v65_seed_{job['seed']}", 'seed': job['seed'], 'at': now(), 'payload': payload}
            ledger['generation_requests'] += 1
            write(OUT / 'ledger.json', ledger)
            append(OUT / 'request_starts.jsonl', request)
            t = time.monotonic()
            try:
                response = api('/completion', payload)
            except Exception as error:
                cases.append({'seed': job['seed'], 'status': 'transport_failure', 'valid': False, 'selected_ids': [], 'request_id': request['request_id'], 'wall_seconds': time.monotonic() - t, 'reason': f'{type(error).__name__}: {error}', 'usage': None})
                raise
            elapsed = time.monotonic() - t
            append(OUT / 'responses.jsonl', {**request, 'response': response, 'wall_seconds': elapsed})
            assert response.get('tokens_predicted', 0) <= 1024
            parsed = parse_response(response['content'], job['prefix'], bool(response.get('truncated') or response.get('stopped_limit') or response.get('stop_type') == 'limit'))
            case = {**parsed, 'seed': job['seed'], 'status': 'valid' if parsed['valid'] else 'invalid', 'request_id': request['request_id'], 'wall_seconds': elapsed, 'usage': {'tokens_predicted': response.get('tokens_predicted'), 'tokens_evaluated': response.get('tokens_evaluated')}}
            cases.append(case)
            write(OUT / 'choices' / f"seed_{job['seed']}.json", case)
            ledger['completed_cases'] += 1
            ledger['valid_cases'] += int(parsed['valid'])
            write(OUT / 'ledger.json', ledger)
            print(job['seed'], case['status'], case['reason'], flush=True)
    except Exception as error:
        stop = f'{type(error).__name__}: {error}'
        ledger['stop_reason'] = stop
    finally:
        if proc is not None and proc.poll() is None:
            os.killpg(proc.pid, signal.SIGTERM)
            try: proc.wait(timeout=3)
            except subprocess.TimeoutExpired:
                os.killpg(proc.pid, signal.SIGKILL)
                proc.wait()
        seen = {c['seed'] for c in cases}
        cases += [{'seed': j['seed'], 'status': 'unattempted', 'valid': False, 'selected_ids': [], 'reason': stop, 'usage': None} for j in jobs if j['seed'] not in seen]
        write(OUT / 'all_cases.json', sorted(cases, key=lambda c: cfg['seeds'].index(c['seed'])))
        ledger.update(finished_at=now(), stage_seconds=time.monotonic() - started, server_exit_code=None if proc is None else proc.returncode, intended_cases=5, unattempted=sum(c['status'] == 'unattempted' for c in cases))
        write(OUT / 'ledger.json', ledger)
    print(json.dumps(ledger, indent=2))
    if stop: raise RuntimeError(stop)


if __name__ == '__main__': main()
