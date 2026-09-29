"""Three bounded real DaCapo runs with preserved reference-output validation."""
import hashlib
import json
import os
import re
import shutil
import signal
import subprocess
import time
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'results/v53_java_feasibility'
JAVA = ROOT / '.local-runtime/java-v53/jdk-17.0.20.1+1-jre/Contents/Home/bin/java'
JAR = ROOT / 'artifacts/sources/v53/dacapo-9.12-MR1-bach.jar'


def digest(path):
    h = hashlib.sha256()
    with path.open('rb') as f:
        for b in iter(lambda: f.read(1024 * 1024), b''):
            h.update(b)
    return h.hexdigest()


def parse_status(text):
    passed = re.findall(r'===== DaCapo 9\.12-MR1 xalan PASSED in ([0-9]+) msec =====', text)
    warmups = re.findall(r'completed warmup 1 in ([0-9]+) msec', text)
    failed = bool(re.search(r'FAILED|Exception|ERROR|VALIDATION FAILED', text))
    return {'final_ms': int(passed[0]) if len(passed) == 1 else None,
            'warmup_ms': int(warmups[0]) if len(warmups) == 1 else None,
            'success_markers': len(passed) == len(warmups) == 1 and not failed}


def main():
    seal = json.loads((ROOT / 'reports/protocol_v53_java_feasibility.freeze.json').read_text())
    for p, expected in seal['files'].items():
        assert digest(ROOT / p) == expected, p
    OUT.mkdir(exist_ok=False)
    scratch_root = ROOT / 'artifacts/sources/live_v53'
    scratch_root.mkdir(exist_ok=False)
    started = time.monotonic()
    records = []
    reference = None
    for i, config in enumerate([(1, 2, 8), (4, 4, 4), (1, 2, 8)]):
        scratch = scratch_root / f'trial_{i}'
        scratch.mkdir()
        command = [str(JAVA), '-Xms512m', '-Xmx512m', '-XX:+UseParallelGC',
                   '-XX:-UseAdaptiveSizePolicy', f'-XX:ParallelGCThreads={config[0]}',
                   f'-XX:NewRatio={config[1]}', f'-XX:SurvivorRatio={config[2]}',
                   '-jar', str(JAR), 'xalan', '-s', 'default', '-t', '1', '-n', '2',
                   '--preserve', '--scratch-directory', str(scratch),
                   '--validation-report', str(OUT / f'validation_{i}.txt')]
        rec = {'trial': i, 'configuration': config, 'command': command,
               'started_at_unix': time.time(), 'status': 'started'}
        with (OUT / 'starts.jsonl').open('a') as f:
            f.write(json.dumps(rec) + '\n')
        t = time.monotonic()
        reason = None
        log = OUT / f'trial_{i}.log'
        with log.open('wb') as f:
            env = os.environ.copy()
            for key in ('JAVA_TOOL_OPTIONS', '_JAVA_OPTIONS', 'JDK_JAVA_OPTIONS', 'CLASSPATH'):
                env.pop(key, None)
            process = subprocess.Popen(command, cwd=ROOT, stdout=f, stderr=subprocess.STDOUT,
                                       start_new_session=True, env=env)
            while process.poll() is None:
                if time.monotonic() - t > 60 or time.monotonic() - started > 210:
                    reason = 'timeout'
                size = sum(p.stat().st_size for p in scratch_root.rglob('*') if p.is_file())
                if size > 2 * 1024**3:
                    reason = 'scratch_cap'
                if reason:
                    os.killpg(process.pid, signal.SIGKILL)
                    process.wait()
                    break
                time.sleep(0.25)
        rec.update(parse_status(log.read_text(errors='replace')))
        outputs = sorted(scratch.glob('xalan.out.*'))
        rec.update({'exit_code': process.returncode, 'outer_wall_seconds': time.monotonic() - t,
                    'termination_reason': reason, 'log_sha256': digest(log),
                    'output_names': [p.name for p in outputs]})
        if len(outputs) == 1 and outputs[0].name == 'xalan.out.0':
            rec['output_bytes'] = outputs[0].stat().st_size
            rec['output_sha256'] = digest(outputs[0])
        owner_ok = process.returncode == 0 and rec['success_markers'] and reason is None
        if owner_ok and i == 0 and rec.get('output_bytes', 0) > 0:
            reference = (rec['output_bytes'], rec['output_sha256'])
        rec['reference_output_equal'] = reference is not None and (
            rec.get('output_bytes'), rec.get('output_sha256')) == reference
        rec['status'] = 'passed' if owner_ok and rec['reference_output_equal'] else 'failed'
        records.append(rec)
        with (OUT / 'trials.jsonl').open('a') as f:
            f.write(json.dumps(rec) + '\n')
        print(json.dumps({k: v for k, v in rec.items() if k != 'command'}), flush=True)
        if rec['status'] != 'passed':
            break
        if i > 0:
            shutil.rmtree(scratch)  # Only this invocation's disposable, verified outputs.
    summary = {'intended_jvm_trials': 3, 'attempted_jvm_trials': len(records),
               'unattempted_trials': 3 - len(records),
               'passed_trials': sum(r['status'] == 'passed' for r in records),
               'runtime_seconds': time.monotonic() - started,
               'model_requests': 0, 'external_spend_usd': 0,
               'stage': 'real application feasibility; not an optimization result',
               'all_passed': len(records) == 3 and all(r['status'] == 'passed' for r in records)}
    (OUT / 'summary.json').write_text(json.dumps(summary, indent=2) + '\n')
    print(json.dumps(summary, indent=2))


if __name__ == '__main__':
    main()
