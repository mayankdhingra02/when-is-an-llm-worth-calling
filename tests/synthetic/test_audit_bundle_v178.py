"""Checks for the V178 guard bootstrap and runner. Synthetic fixtures only; nothing enters research aggregates."""
import json, os, subprocess, sys
from pathlib import Path
ROOT = Path(__file__).resolve().parents[2]; sys.path.insert(0, str(ROOT/'scripts'))
import reproduce_bundle_v178 as rb
BOOT = str(ROOT/'scripts/guarded_run_v178.py')
PROBE = "import socket\ntry:\n    socket.create_connection(('127.0.0.1', 9), timeout=1); print('connected')\nexcept RuntimeError as e:\n    print('blocked' if 'offline guard' in str(e) else 'other')\nexcept Exception as e:\n    print('unguarded', type(e).__name__)\n"

def run(args, tmp_path, extra_path=None):
    env = dict(os.environ, PYTHONPATH=os.pathsep.join([p for p in [extra_path] if p]))
    return subprocess.run([sys.executable, BOOT, *args], cwd=tmp_path, env=env, capture_output=True, text=True, timeout=60)

def test_selftest_passes():
    p = subprocess.run([sys.executable, BOOT, '--selftest'], capture_output=True, text=True, timeout=60)
    assert p.returncode == 0 and json.loads(p.stdout)['guard_active'] is True

def test_guard_holds_when_a_host_sitecustomize_shadows_startup(tmp_path):
    host = tmp_path/'host'; host.mkdir(); (host/'sitecustomize.py').write_text('HOST = True\n')
    probe = tmp_path/'probe.py'; probe.write_text(PROBE)
    assert run([str(probe)], tmp_path, str(host)).stdout.strip() == 'blocked'

def test_script_runs_as_main_with_its_own_directory_first(tmp_path):
    d = tmp_path/'pkg'; d.mkdir(); (d/'helper.py').write_text('X = 7\n')
    (d/'main.py').write_text("import sys, helper\nprint(__name__, sys.argv[1:], helper.X)\n")
    p = run([str(d/'main.py'), 'a', 'b'], tmp_path)
    assert p.returncode == 0 and p.stdout.strip() == "__main__ ['a', 'b'] 7", p.stderr

def test_child_launches_are_logged(tmp_path):
    log = tmp_path/'children.jsonl'; s = tmp_path/'spawn.py'
    s.write_text("import subprocess, sys\nsubprocess.run([sys.executable, '-c', 'pass'])\n")
    env = dict(os.environ, GUARD_CHILD_LOG=str(log))
    subprocess.run([sys.executable, BOOT, str(s)], env=env, check=True, timeout=60)
    assert json.loads(log.read_text().splitlines()[0])[1:] == ['-c', 'pass']

def test_every_command_goes_through_the_bootstrap(monkeypatch, tmp_path):
    seen = []
    class P: returncode = 0; stdout = 'ok\n'; stderr = ''
    monkeypatch.setattr(rb.subprocess, 'run', lambda argv, **k: seen.append(argv) or P())
    with open(tmp_path/'log', 'w') as log: rb.run('x', ['scripts/a.py'], {}, log)
    assert seen[0][1:] == ['scripts/guarded_run_v178.py', 'scripts/a.py']

def test_non_reference_environment_is_labelled(monkeypatch, tmp_path):
    (tmp_path/'requirements-bundle-v178.txt').write_text('# pins\nnumpy==0.0.1\n')
    monkeypatch.setattr(rb, 'ROOT', tmp_path)
    e = rb.environment()
    assert e['reference_environment'] is False and 'numpy' in e['package_mismatches'] and 'Non-reference' in e['note']

def test_superseded_guard_test_is_deselected_not_counted():
    pytest_argv = next(a for n, a, _ in rb.CORE if n == 'pytest')
    assert rb.SUPERSEDED_GUARD_TEST in pytest_argv and rb.NOT_IN_BUNDLE[rb.SUPERSEDED_GUARD_TEST]['status'] == 'deselected'
