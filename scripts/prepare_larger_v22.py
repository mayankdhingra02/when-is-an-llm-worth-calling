"""Prepare only predecision inputs. No tokenizer/model or hidden-label reads."""
import sys
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'src'))
from escalation.io import read, write, lines, digest
from escalation.larger_v22 import transform, CONDITIONS, MODEL_ID, REVISION, require
from escalation.resources import Resources


def main():
    destination = ROOT / 'data/larger_probe_v22.json'
    require(not destination.exists(), 'Preserve prepared inputs')
    ledger = ROOT / 'artifacts/resource_ledger_v2.json'
    before = read(ledger)
    require(before['requests'] == 140 and before['active_since'] is None, 'Inactive exhausted ledger required')
    with Resources({'resources': {'max_experiment_runtime_minutes': 30}, 'inference': {'max_new_model_requests': 140}}, ledger) as resource:
        resource.check()
        manifest = read(ROOT / 'data/manifest_v8.json')
        requests = lines(ROOT / 'results/v8/requests.jsonl')
        require(len(manifest['datasets']) == 3 and all(d['split'] == 'development' for d in manifest['datasets']), 'Development only')
        require(manifest['seeds'] == [11, 23, 37, 53, 71], 'Fixed seeds')
        cases = manifest['cases']; require(len(cases) == 15, 'All15 cases required')
        jobs = []
        for round_id in range(4):
            for index, case in enumerate(cases):
                original = next(r for r in requests if r['dataset'] == case['dataset'] and r['seed'] == case['seed'])
                require(digest(original['messages']) == case['prompt_sha256'], 'Source prompt provenance')
                condition = CONDITIONS[(round_id + index) % 3] if round_id < 3 else CONDITIONS[3]
                treatment = transform(original['messages'], case['pool'], case['dataset'], case['seed'], condition)
                jobs.append(dict(job_id=len(jobs), dataset=case['dataset'], seed=case['seed'],
                    system_group=original['system_group'], split='development', condition=condition,
                    prefix_hash=case['prefix_hash'], source_request_id=original['request_id'],
                    prompt_hash=digest(treatment['messages']), **treatment))
        write(destination, {'scope': 'prepared inputs only; no V22 model responses or results', 'model_id': MODEL_ID,
                           'revision': REVISION, 'jobs': jobs, 'intended_requests': 60, 'new_objective_acquisitions_in_preparation': 0})
        resource.check()
    after = read(ledger)
    write(ROOT / 'artifacts/study_v22/preparation_accounting.json', {'before_seconds': before['experiment_seconds'],
          'after_seconds': after['experiment_seconds'], 'charged_seconds': after['experiment_seconds'] - before['experiment_seconds'],
          'requests_before': before['requests'], 'requests_after': after['requests'], 'new_objective_acquisitions': 0})
    print('Prepared60 prompts from15 saved development prefixes; no inference or new labels.')


if __name__ == '__main__':
    main()
