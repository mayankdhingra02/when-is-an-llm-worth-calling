"""One-shot 40-acquisition diagnostic; 300s stage/10s worker/2GiB RSS guards."""
import json, os, signal, subprocess, sys, time
from collect_smollm_v47 import ROOT, read, write, append, sha, now
from run_planning_v55 import rss
from superlu_v96_common import jobs, classify
OUT = ROOT / 'results/v96_superlu'

def main():
    for name, digest in read(ROOT / 'reports/protocol_v96.freeze.json')['sha256'].items():
        if sha(ROOT / name) != digest:
            raise ValueError('Frozen input changed: ' + name)
    rss(-1)  # fail before collection if process monitoring is unavailable
    OUT.mkdir(exist_ok=False)
    for folder in ['requests', 'evaluations', 'stderr']:
        (OUT / folder).mkdir()
    intended = jobs(); write(OUT / 'intended.json', intended)
    start = time.monotonic(); charged = 0; stopped = None
    env = {**os.environ, **{k:'1' for k in ['OPENBLAS_NUM_THREADS', 'OMP_NUM_THREADS',
           'VECLIB_MAXIMUM_THREADS', 'MKL_NUM_THREADS']}}
    try:
        for job in intended:
            if stopped or time.monotonic() - start >= 285:
                stopped = stopped or 'stage_time_reserve'
                append(OUT / 'outcomes.jsonl', {**job, 'status':'unattempted', 'reason':stopped})
                continue
            assert charged < 40
            key = job['key']; req = OUT / 'requests' / (key + '.json')
            result = OUT / 'evaluations' / (key + '.json')
            write(req, {**job, 'at':now()}); charged += 1
            append(OUT / 'charges.jsonl', {'key':key, 'acquisition':charged, 'at':now()})
            guard = None; peak = 0; worker_start = time.monotonic()
            with (OUT / 'stderr' / (key + '.txt')).open('x') as log:
                proc = subprocess.Popen([sys.executable, str(ROOT/'scripts/worker_superlu_v96.py'), str(req), str(result)],
                    cwd=ROOT, env=env, stdout=log, stderr=subprocess.STDOUT, start_new_session=True)
                try:
                    while proc.poll() is None:
                        peak = max(peak, rss(proc.pid))
                        if peak > 2 * 1024**3: guard = 'rss_guard'
                        if time.monotonic() - worker_start > 10: guard = 'worker_time_guard'
                        if guard:
                            os.killpg(proc.pid, signal.SIGKILL); break
                        time.sleep(.05)
                    proc.wait(timeout=3)
                finally:
                    if proc.poll() is None:
                        os.killpg(proc.pid, signal.SIGKILL); proc.wait(timeout=3)
            record = read(result) if result.exists() else None
            if record and record['peak_worker_rss_bytes'] > 2 * 1024**3: guard = 'rss_guard'
            status = classify(proc.returncode, guard, record)
            append(OUT / 'outcomes.jsonl', {**job, 'status':status, 'exit_code':proc.returncode,
                'guard':guard, 'peak_sampled_rss_bytes':peak, 'wall_seconds':time.monotonic()-worker_start})
            print(key, status, proc.returncode, flush=True)
            # Native crashes are the outcome under investigation. Only resource
            # guards stop the stage; no crashed condition is retried/replaced.
            if guard: stopped = guard
    finally:
        write(OUT / 'lifecycle.json', {'charged_acquisitions':charged,
            'seconds':time.monotonic()-start, 'stop_reason':stopped, 'at':now()})

if __name__ == '__main__':
    main()
