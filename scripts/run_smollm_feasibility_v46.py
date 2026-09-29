"""Two real offline generations over non-research prompts, with bounded lifetime."""
import hashlib
import json
import os
import re
import signal
import subprocess
import time
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'artifacts/study_v46'
RUN = OUT / 'feasibility'

def stamp():
    return datetime.now(timezone.utc).isoformat()

def write(path, data):
    path.write_text(json.dumps(data, indent=2)+'\n')

def main():
    cfg = json.loads((ROOT/'configs/local_feasibility_v46.json').read_text())
    if cfg['max_requests'] != 2 or cfg['max_external_spend_usd'] != 0 or cfg['retries'] != 0:
        raise ValueError('Unexpected feasibility allowance')
    if RUN.exists(): raise RuntimeError('Preserve previous run; no implicit retry')
    downloads = json.loads((OUT/'downloads.json').read_text())
    for rec in downloads['files']:
        h = hashlib.sha256()
        with (ROOT/rec['path']).open('rb') as f:
            for chunk in iter(lambda: f.read(1024*1024), b''): h.update(chunk)
        if h.hexdigest() != rec['expected_sha256']: raise ValueError('Changed artifact')
    RUN.mkdir()
    prompts = [
        'In two short sentences, explain why measuring runtime matters when comparing two software optimizers.',
        'This is synthetic hardware-test input, not measured research data. '
        'The following are candidate settings with no measured objective values. '
        'Explain in at most three sentences why you cannot know which candidate is fastest without measurements.\n'
        + '\n'.join(f'candidate {i:02}: workers={1+i%8}, cache_mb={64*(1+i%16)}, batch={8*(1+i%4)}, compression={i%3}, logging={i%2}' for i in range(40)),
    ]
    commands = []
    for i,prompt in enumerate(prompts):
        pf = RUN/f'prompt_{i}.txt'; pf.write_text(prompt+'\n')
        commands.append(['/usr/bin/time', '-l', str(ROOT/'.local-runtime/llama-b11146/llama-cli'),
            '-m', str(ROOT/'models/SmolLM3-3B-Q4_K_M/SmolLM3-Q4_K_M.gguf'),
            '--offline', '-ngl', '99', '-c', '4096', '-n', str(cfg['max_new_tokens_per_request']),
            '-t', '6', '-b', '512', '-ub', '128', '--seed', '11', '--temp', '0',
            '--jinja', '--reasoning', 'off', '-sys', '/no_think', '--single-turn',
            '--no-warmup', '--simple-io', '--color', 'off', '--perf', '--no-display-prompt', '-f', str(pf)])
    write(RUN/'manifest.json', {'created_at': stamp(), 'config': cfg, 'commands': commands,
        'prompt_sha256': [hashlib.sha256(p.encode()).hexdigest() for p in prompts],
        'model_revision': '4965cb60b150737b68a0408c36aeefb65078f894',
        'quantization': 'Q4_K_M', 'runtime_build': 'b11146', 'sampling': 'greedy; seed11; no deterministic cross-hardware guarantee',
        'classification': 'real inference on synthetic/non-research prompts; NOT research optimization results'})
    start = time.monotonic(); records = []
    summary = {'started_at': stamp(), 'requests_attempted': 0, 'records': records, 'external_spend_usd': 0, 'objective_acquisitions': 0}
    try:
        for i, cmd in enumerate(commands):
            remaining = cfg['inference_stage_timeout_seconds']-(time.monotonic()-start)
            if remaining <= 5: break
            rec = {'request_index': i, 'started_at': stamp(), 'status': 'started'}
            records.append(rec); summary['requests_attempted'] += 1
            write(RUN/'summary.json', summary)
            t = time.monotonic()
            with (RUN/f'output_{i}.txt').open('w') as out, (RUN/f'stderr_{i}.txt').open('w') as err:
                proc = subprocess.Popen(cmd, stdout=out, stderr=err, stdin=subprocess.DEVNULL,
                    cwd=ROOT, start_new_session=True,
                    env={k:v for k,v in os.environ.items() if not k.startswith(('LLAMA_', 'HF_', 'HUGGING_FACE_'))})
                try:
                    proc.wait(timeout=min(80, remaining-3))
                    rec.update(status='completed' if proc.returncode == 0 else 'failed', exit_code=proc.returncode)
                except subprocess.TimeoutExpired:
                    os.killpg(proc.pid, signal.SIGTERM)
                    try: proc.wait(timeout=2)
                    except subprocess.TimeoutExpired:
                        os.killpg(proc.pid, signal.SIGKILL); proc.wait()
                    rec['status'] = 'timeout'
                finally:
                    if proc.poll() is None:
                        os.killpg(proc.pid, signal.SIGKILL); proc.wait()
            rec['wall_seconds'] = time.monotonic()-t
            stderr = (RUN/f'stderr_{i}.txt').read_text()
            rec['peak_resident_bytes'] = int(m.group(1)) if (m:=re.search(r'(\d+)\s+maximum resident set size', stderr)) else None
            rec['performance_lines'] = [s for s in stderr.splitlines() if 'perf' in s or 'buffer size' in s or 'offload' in s]
            write(RUN/'summary.json', summary)
            if rec['status'] != 'completed': break
    finally:
        summary.update(finished_at=stamp(), stage_wall_seconds=time.monotonic()-start,
            completed=sum(r['status']=='completed' for r in records), retries=0)
        write(RUN/'summary.json', summary)
    print(json.dumps(summary, indent=2))

if __name__ == '__main__': main()
