"""Frozen complete-grid physical measurements, with reference-output equality."""
import itertools
import json
import os
import random
import shutil
import signal
import subprocess
import time
from pathlib import Path
from run_java_feasibility_v53 import ROOT, JAVA, JAR, digest, parse_status
OUT = ROOT / 'results/v54_java_physical'


def main():
    for seal in ('reports/protocol_v53_java_feasibility.freeze.json',
                 'reports/protocol_v54_java_screen.freeze.json'):
        for p, expected in json.loads((ROOT / seal).read_text())['files'].items():
            assert digest(ROOT / p) == expected, p
    ref = ROOT / 'artifacts/sources/live_v53/trial_0/xalan.out.0'
    reference = (ref.stat().st_size, digest(ref))
    assert reference == (23901000, '4c72b92f00eca08f8bda35e2734124f92fbfd01884c3bf259f2f5d005e98bddb')
    OUT.mkdir(exist_ok=False)
    scratch_root = ROOT / 'artifacts/sources/live_v54'
    scratch_root.mkdir(exist_ok=False)
    grid = list(itertools.product([1, 2, 4, 8], [1, 2, 4, 8], [2, 4, 8]))
    schedule = []
    for r in range(3):
        order = list(range(48))
        random.Random(54000 + r).shuffle(order)
        offset = len(schedule)
        schedule.extend({'trial': offset + j, 'round': r, 'config_id': cid,
                         'configuration': grid[cid]} for j, cid in enumerate(order))
    (OUT / 'schedule.json').write_text(json.dumps(schedule, indent=2) + '\n')
    start = time.monotonic()
    records = []
    for item in schedule:
        if time.monotonic() - start > 1140:
            break
        i = item['trial']; config = item['configuration']
        scratch = scratch_root / f'trial_{i}'
        scratch.mkdir()
        cmd = [str(JAVA), '-Xms512m', '-Xmx512m', '-XX:+UseParallelGC',
               '-XX:-UseAdaptiveSizePolicy', f'-XX:ParallelGCThreads={config[0]}',
               f'-XX:NewRatio={config[1]}', f'-XX:SurvivorRatio={config[2]}',
               '-jar', str(JAR), 'xalan', '-s', 'default', '-t', '1', '-n', '2',
               '--preserve', '--scratch-directory', str(scratch),
               '--validation-report', str(OUT / f'validation_{i}.txt')]
        rec = dict(item, command=cmd, started_at_unix=time.time(), status='started')
        with (OUT / 'starts.jsonl').open('a') as f: f.write(json.dumps(rec) + '\n')
        log = OUT / f'trial_{i}.log'; reason = None; t = time.monotonic()
        env = os.environ.copy()
        for key in ('JAVA_TOOL_OPTIONS', '_JAVA_OPTIONS', 'JDK_JAVA_OPTIONS', 'CLASSPATH'):
            env.pop(key, None)
        with log.open('wb') as f:
            p = subprocess.Popen(cmd, cwd=ROOT, stdout=f, stderr=subprocess.STDOUT,
                                 start_new_session=True, env=env)
            while p.poll() is None:
                if time.monotonic() - t > 60: reason = 'timeout'
                if sum(x.stat().st_size for x in scratch_root.rglob('*') if x.is_file()) > 2 * 1024**3:
                    reason = 'scratch_cap'
                if reason:
                    os.killpg(p.pid, signal.SIGKILL); p.wait(); break
                time.sleep(0.25)
        rec.update(parse_status(log.read_text(errors='replace')))
        outputs = list(scratch.glob('xalan.out.*'))
        pair = None
        if len(outputs) == 1 and outputs[0].name == 'xalan.out.0':
            pair = (outputs[0].stat().st_size, digest(outputs[0]))
        rec.update(exit_code=p.returncode, termination_reason=reason,
                   outer_wall_seconds=time.monotonic() - t, log_sha256=digest(log),
                   output_bytes=pair[0] if pair else None, output_sha256=pair[1] if pair else None,
                   reference_output_equal=pair == reference)
        rec['status'] = 'passed' if p.returncode == 0 and rec['success_markers'] and pair == reference and reason is None else 'failed'
        records.append(rec)
        with (OUT / 'trials.jsonl').open('a') as f: f.write(json.dumps(rec) + '\n')
        if rec['status'] != 'passed': break
        shutil.rmtree(scratch)
        if (i + 1) % 12 == 0: print(f'{i+1}/144 validated JVM trials', flush=True)
    summary = {'intended': 144, 'attempted': len(records), 'unattempted': 144 - len(records),
               'passed': sum(r['status'] == 'passed' for r in records),
               'runtime_seconds': time.monotonic() - start,
               'physical_jvm_invocations': len(records),
               'completed_timed_iterations': sum(r['final_ms'] is not None for r in records),
               'completed_warmup_iterations': sum(r['warmup_ms'] is not None for r in records),
               'model_requests': 0, 'external_spend_usd': 0}
    (OUT / 'summary.json').write_text(json.dumps(summary, indent=2) + '\n')
    print(json.dumps(summary, indent=2), flush=True)


if __name__ == '__main__': main()
