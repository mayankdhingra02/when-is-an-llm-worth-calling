"""Synthetic orchestration only: no model, HTTP, or database execution.

Real runner main() is exercised with an isolated temporary root and stubbed I/O.
These cases validate failure accounting, not model quality or engine integration.
"""
import importlib.util
import io
import json
import sys
from pathlib import Path
from urllib.parse import urlparse

import pytest

ROOT = Path(__file__).resolve().parents[2]


@pytest.fixture
def harness(tmp_path, monkeypatch):
    monkeypatch.syspath_prepend(str(ROOT/'scripts'))
    spec = importlib.util.spec_from_file_location('synthetic_v72_runner', ROOT/'scripts/run_rocksdb_v72.py')
    module = importlib.util.module_from_spec(spec); spec.loader.exec_module(module)
    monkeypatch.setattr(module, 'ROOT', tmp_path)
    out = tmp_path/'results/v72_rocksdb_paired'
    monkeypatch.setattr(module, 'OUT', out)
    def write(name, value):
        p = tmp_path/name; p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(json.dumps(value))
    write('reports/protocol_v72.freeze.json', {'sha256': {}})
    write('configs/study_v72.json', json.loads((ROOT/'configs/study_v72.json').read_text()))
    for seed in module.SEEDS:
        write(f'results/v71_rocksdb_classical/prefix_{seed}.json',
              [{'config_id': i, 'value_ms': float(i+100), 'synthetic': True} for i in range(10)])
    # Hashable fixtures, never executed and never a model artifact.
    (tmp_path/'synthetic-server').write_text('not executable')
    (tmp_path/'synthetic-model').write_text('not model weights')
    write('artifacts/study_v72/runtime_plan.json', {'command': [str(tmp_path/'synthetic-server'), '-m', str(tmp_path/'synthetic-model')]})
    monkeypatch.setattr(sys, 'argv', ['runner', '--approved-envelope-sha256', module.sha(tmp_path/'reports/protocol_v72.freeze.json')])
    monkeypatch.setattr(module, 'rss', lambda _: 0)
    monkeypatch.setattr(module, 'choose', lambda x, obs, method, seed: next(i for i in range(512) if i not in {o['config_id'] for o in obs}))
    state = {'mode': 'valid', 'generation_calls': 0, 'physical_calls': 0, 'killed': [], 'urls': []}
    class Proc:
        pid = 99999999
        returncode = None
        def poll(self): return self.returncode
        def wait(self, timeout=None): self.returncode = -15; return self.returncode
    proc = Proc()
    def popen(*args, **kwargs):
        if state['mode'] == 'startup': raise OSError('synthetic startup failure')
        return proc
    monkeypatch.setattr(module.subprocess, 'Popen', popen)
    monkeypatch.setattr(module.os, 'killpg', lambda pid, sig: state['killed'].append((pid, int(sig))))
    class Socket:
        def __enter__(self): return self
        def __exit__(self, *args): pass
        def bind(self, address): assert address == ('127.0.0.1', 18492)
    monkeypatch.setattr(module.socket, 'socket', Socket)
    class Opener:
        def open(self, request, timeout):
            state['urls'].append(request.full_url)
            parsed = urlparse(request.full_url)
            assert parsed.hostname == '127.0.0.1' and parsed.port == 18492
            payload = json.loads(request.data) if request.data else None
            if parsed.path == '/health': reply = {'status': 'ok'}
            elif parsed.path == '/apply-template': reply = {'prompt': json.dumps(payload['messages'])}
            elif parsed.path == '/tokenize': reply = {'tokens': [1]*(4096 if state['mode']=='context' else 10)}
            elif parsed.path == '/completion':
                state['generation_calls'] += 1
                # Prove durable charging and full request receipt precede transport.
                ledger = json.loads((out/'ledger.json').read_text())
                assert ledger['generation_requests'] == state['generation_calls']
                starts = (out/'request_starts.jsonl').read_text().splitlines()
                assert len(starts) == state['generation_calls']
                rid = json.loads(starts[-1])['request_id']
                assert (out/rid/'request.json').exists()
                if state['mode'] == 'transport': raise TimeoutError('synthetic transport timeout')
                literal = payload['grammar'].removeprefix('root ::= ').split(' | ')[0]
                content = json.loads(literal)
                if state['mode'] == 'invalid': content = 'not a legal vector'
                reply = {'content': content, 'tokens_predicted': 65 if state['mode']=='token_cap' else 9,
                         'tokens_evaluated': 10, 'stopped_limit': state['mode']=='truncated'}
            else: raise AssertionError('unexpected route')
            return io.BytesIO(json.dumps(reply).encode())
    monkeypatch.setattr(module.urllib.request, 'build_opener', lambda *args: Opener())
    def worker(command, **kwargs):
        state['physical_calls'] += 1
        path = Path(command[-1]); spec = json.loads(path.read_text())
        charges = (out/'charges.jsonl').read_text().splitlines()
        assert len(charges) == state['physical_calls']  # charge before worker starts
        assert json.loads(charges[-1])['config_id'] == spec['config_id']
        bad = state['mode']=='physical'
        (path.parent/'result.json').write_text(json.dumps({'status': 'failed' if bad else 'valid', 'objective_verified_loop_seconds': .123}))
        return {'exit_code': 1 if bad else 0, 'termination_reason': None, 'wall_seconds': .01, 'sampled_maxima': {}}
    monkeypatch.setattr(module, 'run', worker)
    return module, out, state, proc


def test_complete_orchestration_has_all_charges_and_is_one_shot(harness):
    module, out, state, proc = harness
    module.main()
    summary = json.loads((out/'summary.json').read_text())
    assert summary['complete'] and summary['charged_evaluations'] == 150
    assert state['generation_calls'] == 35 and state['physical_calls'] == 150
    assert summary['ledger']['fallback_search_evaluations'] == 0
    for case in summary['cases']:
        for method, obs in case['arms'].items():
            assert len(obs) == len({o['config_id'] for o in obs}) == 17
            assert len(case['confirmation'][method]) == 3
            assert all(o['config_id'] == case['selected_config_ids'][method] for o in case['confirmation'][method])
    assert state['killed'] and proc.returncode is not None
    with pytest.raises(FileExistsError): module.main()
    assert state['generation_calls'] == 35 and state['physical_calls'] == 150


@pytest.mark.parametrize('mode', ['invalid', 'truncated'])
def test_invalidity_switches_each_arm_to_counted_rf_without_retry(harness, mode):
    module, out, state, proc = harness; state['mode'] = mode
    module.main(); summary = json.loads((out/'summary.json').read_text())
    assert summary['complete'] and summary['charged_evaluations'] == 150
    assert state['generation_calls'] == 5
    assert summary['ledger']['fallback_search_evaluations'] == 35
    assert summary['ledger']['unattempted_generation_requests'] == 30
    assert all(case['fallback_steps'] == list(range(1, 8)) for case in summary['cases'])
    assert state['killed'] and proc.returncode is not None


@pytest.mark.parametrize('mode', ['transport', 'physical', 'context', 'startup', 'token_cap'])
def test_failure_preserves_intended_denominators_and_stops(harness, mode):
    module, out, state, proc = harness; state['mode'] = mode
    with pytest.raises(RuntimeError): module.main()
    summary = json.loads((out/'summary.json').read_text()); ledger = summary['ledger']
    assert not summary['complete'] and ledger['stop_reason'] is not None
    assert summary['charged_evaluations'] == state['physical_calls']
    assert summary['unattempted']+summary['charged_evaluations'] == 150
    assert ledger['generation_requests'] == state['generation_calls']
    assert ledger['unattempted_generation_requests']+ledger['generation_requests'] == 35
    assert ledger['retries'] == 0 and len(summary['cases']) <= 1
    if mode in ('transport', 'token_cap'): assert state['generation_calls'] == 1
    if mode in ('context', 'startup', 'physical'): assert state['generation_calls'] == 0
    if mode == 'physical':
        assert state['physical_calls'] == 1
        assert json.loads((out/'acquisitions.json').read_text())[0]['status'] == 'failed'
    if mode != 'startup': assert state['killed'] and proc.returncode is not None
