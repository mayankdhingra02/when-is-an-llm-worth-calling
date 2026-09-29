"""Standard-library replay of saved real responses; never invokes an LLM.

Works inside the portable bundle, or the project. Checks complete intended
condition coverage and reconstructs both models' diagnostic contrasts directly
from raw outputs and source ID-to-configuration mappings.
"""
import hashlib
import itertools
import json
import math
import statistics
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

def read(name):
    return json.loads((ROOT / name).read_text())

def lines(name):
    return [json.loads(line) for line in (ROOT / name).read_text().splitlines()]

def sha(path):
    h = hashlib.sha256()
    with path.open('rb') as f:
        for block in iter(lambda: f.read(1024 * 1024), b''):
            h.update(block)
    return h.hexdigest()

def check(condition, explanation):
    if not condition:
        raise ValueError(explanation)

def audit(stage, raw, analysis):
    jobs = read('artifacts/study_v48/jobs.json')
    check(len(jobs) == 108 and len({j['key'] for j in jobs}) == 108, 'Intended denominator')
    starts = lines(raw + '/request_starts.jsonl')
    responses = lines(raw + '/responses.jsonl')
    check(len(starts) == len(responses) == 1080, 'Response denominator')
    index = {r['request_id']: r for r in responses}
    check(len(index) == 1080, 'Duplicate request IDs')
    for request in starts:
        response = index[request['request_id']]
        check(request['payload'] == response['payload'], 'Payload changed')
        check(response['response']['tokens_predicted'] == 1 and not response['response']['truncated'], 'Invalid token count/truncation')
    configs = {}
    for job in jobs:
        prompt = read(job['prefix'])
        choice = read(raw + '/choices/' + job['key'] + '.json')
        check(choice['status'] == 'completed', 'Incomplete intended condition')
        ids = choice['selected_ids']
        check(len(ids) == len(set(ids)) == 10, 'Bad selected IDs')
        check(choice['prefix_hash'] == prompt['prefix_hash'], 'Different measured prefix')
        pre = read(raw + '/preflight/' + job['key'] + '.json')
        check(pre['messages'] == prompt['messages'], 'Wrong messages')
        check(len(choice['request_ids']) == 10, 'Choice request count')
        for step, identity in enumerate(choice['request_ids']):
            response = index[identity]
            check(response['case'] == job['key'] and response['step'] == step, 'Response alignment')
            check(response['response']['content'] == ids[step], 'Choice differs from model response')
            expected = pre['rendered']['prompt'] + ''.join(c + '\n' for c in ids[:step])
            check(response['payload']['prompt'] == expected, 'Changed selection history')
        key = (job['base_case'], job['representation'], job['loss_mode'], job['presentation_mode'])
        configs[key] = (job['system_group'], {prompt['mapping'][c] for c in ids})
    pairs = []
    bases = sorted({j['base_case'] for j in jobs})
    for base, representation in itertools.product(bases, ['symbols', 'values']):
        for presentation in ['base', 'reverse', 'relabel']:
            a = configs[base, representation, 'observed', presentation]
            b = configs[base, representation, 'withheld', presentation]
            pairs.append((representation, 'loss_removal', presentation, a[0], len(a[1] & b[1]) / 10))
        for labels, presentation in itertools.product(['observed', 'withheld'], ['reverse', 'relabel']):
            a = configs[base, representation, labels, 'base']
            b = configs[base, representation, labels, presentation]
            pairs.append((representation, presentation, labels, a[0], len(a[1] & b[1]) / 10))
    expected_summary = read(analysis + '/summary.json')
    comparison = []
    for summary in expected_summary['paired_sensitivities']:
        key = (summary['representation'], summary['intervention'], summary['context'])
        rows = [r for r in pairs if r[:3] == key]
        check(len(rows) == 9, 'Unbalanced pair coverage')
        groups = {g: [r[4] for r in rows if r[3] == g] for g in sorted({r[3] for r in rows})}
        check(len(groups) == 3 and all(len(v) == 3 for v in groups.values()), 'Family/seed split')
        mean = statistics.mean(statistics.mean(v) for v in groups.values())
        changed = sum(r[4] < 1 for r in rows)
        check(math.isclose(mean, summary['family_mean_overlap'], abs_tol=1e-12), 'Aggregate mismatch')
        check(changed == summary['set_changes'], 'Change-count mismatch')
        comparison.append({'model_stage': stage, 'representation': key[0], 'intervention': key[1], 'context': key[2], 'family_mean_overlap': mean, 'changed_sets': changed, 'pairs': 9})
    for rep, reported in expected_summary['screens'].items():
        loss = [r for r in pairs if r[:3] == (rep, 'loss_removal', 'base')]
        responsive = sum(sum(r[4] < 1 for r in loss if r[3] == g) >= 2 for g in {r[3] for r in loss}) >= 2
        stable = all(next(r['family_mean_overlap'] for r in comparison if (r['representation'], r['intervention'], r['context']) == (rep, mode, 'observed')) >= .8 for mode in ['reverse', 'relabel'])
        check(reported['loss_responsiveness_pass'] == responsive and reported['row_stability_pass'] == stable and reported['screen_pass'] == (responsive and stable), 'Screen mismatch')
    return {'stage': stage, 'conditions': 108, 'requests': 1080, 'comparisons': comparison, 'screens': expected_summary['screens']}

def main():
    manifest = ROOT / 'BUNDLE_MANIFEST.json'
    if manifest.exists():
        for name, meta in read('BUNDLE_MANIFEST.json')['files'].items():
            check((ROOT / name).stat().st_size == meta['bytes'] and sha(ROOT / name) == meta['sha256'], 'Changed bundle file: ' + name)
    records = [audit('SmolLM3-3B V48', 'results/v48_sensitivity', 'results/v48_analysis'), audit('Qwen3-8B V92b', 'results/v92b_sensitivity', 'results/v92b_analysis')]
    print(json.dumps({'verified': True, 'scope': 'Saved-response replay only; no new inference, optimization outcomes or model reproducibility claim', 'records': records}, indent=2))

if __name__ == '__main__':
    main()
