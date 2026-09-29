"""Read-only verification of real V46 hardware traces; never performs inference."""
import hashlib
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT/'artifacts/study_v46'

def verify():
    run = OUT/'feasibility'
    summary = json.loads((run/'summary.json').read_text())
    manifest = json.loads((run/'manifest.json').read_text())
    assert summary['requests_attempted'] == summary['completed'] == 2
    assert summary['retries'] == summary['objective_acquisitions'] == summary['external_spend_usd'] == 0
    assert summary['stage_wall_seconds'] <= manifest['config']['inference_stage_timeout_seconds']
    measurements = []
    for i, rec in enumerate(summary['records']):
        prompt = (run/f'prompt_{i}.txt').read_text()
        # Original manifest hashes the logical prompt; file adds a final newline.
        assert hashlib.sha256(prompt.removesuffix('\n').encode()).hexdigest() == manifest['prompt_sha256'][i]
        stderr = (run/f'stderr_{i}.txt').read_text()
        stdout = (run/f'output_{i}.txt').read_text()
        assert rec['status'] == 'completed' and rec['exit_code'] == 0
        rss = int(re.search(r'(\d+)\s+maximum resident set size', stderr).group(1))
        assert rss == rec['peak_resident_bytes']
        rates = re.search(r'\[ Prompt: ([\d.]+) t/s \| Generation: ([\d.]+) t/s \]', stdout)
        assert rates and 'Exiting...' in stdout
        assert 'b11146-7fe450e19' in stdout
        cmd = manifest['commands'][i]
        assert '--offline' in cmd and '--single-turn' in cmd
        assert cmd[cmd.index('-n')+1] == '128'
        assert cmd[cmd.index('-c')+1] == '4096'
        assert cmd[cmd.index('--reasoning')+1] == 'off'
        measurements.append({'request': i, 'wall_seconds_including_load': rec['wall_seconds'],
            'peak_resident_bytes': rss, 'peak_resident_gib': rss/(1024**3),
            'prompt_tokens_per_second_cli_rounded': float(rates[1]),
            'generation_tokens_per_second_cli_rounded': float(rates[2]),
            'input_tokens': None, 'output_tokens': None,
            'usage_note': 'CLI reported rates but no exact token totals; unknown, not zero.',
            'load_seconds': None, 'load_note': 'Not separately exposed by this CLI output.'})
    assert 'MTL0: Apple M3 Pro' in (OUT/'devices_host.txt').read_text()
    downloads = json.loads((OUT/'downloads.json').read_text())
    assert downloads['transferred_bytes'] + downloads['metadata_reserve_bytes'] <= manifest['config']['max_additional_download_bytes']
    assert all(x['verified'] and x['sha256']==x['expected_sha256'] for x in downloads['files'])
    result = {'verified': True, 'measurements': measurements,
        'gpu': 'Metal Apple M3 Pro available; both commands request full offload; CLI does not expose actual layer-placement logs',
        'warmup': 'Disabled. Both requests load separate processes. Second may benefit from OS file cache.',
        'download_bytes': downloads['transferred_bytes'],
        'research_outcomes': 0,
        'scope': 'Local feasibility only; synthetic fixture is excluded from all research aggregates.'}
    (OUT/'verified_measurements.json').write_text(json.dumps(result, indent=2)+'\n')
    print(json.dumps(result, indent=2))

if __name__ == '__main__': verify()
