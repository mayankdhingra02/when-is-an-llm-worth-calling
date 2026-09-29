"""V172 runtime: the unchanged V148 watchdog/ledger/generation class with V172 model pins and ports."""
import hashlib, json, os, socket, subprocess, threading, time
from runtime_models_v148 import ROOT, Runtime as RuntimeV148, rss
from escalation.receipts_v70 import atomic_json
def server_command(model_path, port):
    """Exactly the historical V141-V148 llama-server command; only model path and port vary."""
    return [str(ROOT/'.local-runtime/llama-b11146/llama-server'), '-m', str(model_path), '--load-mode', 'none', '--offline', '--host', '127.0.0.1', '--port', str(port),
            '--no-webui', '-ngl', '99', '-c', '4096', '-np', '1', '-t', '6', '-b', '512', '-ub', '128', '--reasoning', 'off', '--jinja', '--no-warmup', '--perf']

def wait_for_port(port, limit=120., interval=1.):
    """Amendment 1: poll the unchanged pre-start bind probe until TIME_WAIT clears; fail closed after limit."""
    t = time.monotonic()
    while True:
        try:
            with socket.socket() as sock: sock.bind(('127.0.0.1', port))
            return time.monotonic()-t
        except OSError:
            if time.monotonic()-t >= limit: raise
            time.sleep(interval)

class Runtime(RuntimeV148):
    def start(self):
        rss(-1)
        model = json.loads((ROOT/'artifacts/study_v172/models.json').read_text())[self.cfg['model_key']]
        h = hashlib.sha256()
        with (ROOT/model['path']).open('rb') as f:
            for b in iter(lambda: f.read(1 << 20), b''): h.update(b)
        if h.hexdigest() != model['sha256']: raise ValueError('Model pin mismatch')
        port = self.cfg['ports'][self.cfg['model_key']]
        self.ledger['port_wait_seconds'] = wait_for_port(port)
        command = server_command(ROOT/model['path'], port)
        atomic_json(self.out/'runtime.json', {'command': command, 'config': self.cfg, 'model': model, 'seed_support': 'Per-case sampling seed; no cross-device determinism guarantee'})
        with (self.out/'server.log').open('xb') as f:
            self.proc = subprocess.Popen(command, cwd=ROOT, stdout=f, stderr=f, start_new_session=True, env={k: v for k, v in os.environ.items() if not k.startswith(('LLAMA_', 'HF_', 'HUGGING_FACE_'))})
        self.thread = threading.Thread(target=self.watch, daemon=True); self.thread.start(); t = time.monotonic()
        while True:
            if time.monotonic()-t > 180: raise TimeoutError('Startup timeout')
            try:
                if self.api('/health').get('status') == 'ok': break
            except OSError: time.sleep(.25)
        self.ledger['startup_seconds'] = time.monotonic()-self.started

def runtime_config(cfg, model_key, requests, compatibility, seconds):
    return {'allow_paid_api': cfg['allow_paid_api'], 'allow_cloud': cfg['allow_cloud'], 'max_external_spend_usd': cfg['max_external_spend_usd'], 'retries': cfg['retries'],
            'model_key': model_key, 'ports': cfg['ports'], 'max_server_rss_bytes': cfg['server_rss_cap_bytes'][model_key], 'max_generation_stage_seconds': seconds,
            'scientific_request_cap': requests, 'compatibility_request_cap': compatibility, 'new_generation_request_cap': requests+compatibility,
            'max_allocated_output_tokens': 1024*(requests+compatibility)}
