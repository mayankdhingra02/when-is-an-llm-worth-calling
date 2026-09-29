"""Post-collection V22 audit/presentation; no inference or optimizer acquisitions.

Independent scalar-loss arithmetic, raw-token replay, saved-state/journal checks.
The frozen collection/analyzer sources remain unchanged.
"""
import argparse
import csv
from contextlib import nullcontext
import hashlib
import json
import math
import os
import sys
from pathlib import Path
from statistics import mean

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'src')); os.chdir(ROOT)
os.environ['MPLCONFIGDIR'] = str(ROOT / '.cache/matplotlib')
os.environ['XDG_CACHE_HOME'] = str(ROOT / '.cache')
from escalation.config import load_config
from escalation.io import read, write, lines, digest
from escalation.larger_v22 import authorization_config, require, MODEL_ID, REVISION, controls
from escalation.resources import Resources

OUT = Path('results/v22_larger')


def scalar_loss(values, direction, ids):
    lo, hi = min(values), max(values)
    if lo == hi: return 0.0
    normalized = [(x - lo) / (hi - lo) if direction == '-' else (hi - x) / (hi - lo) for x in values]
    return min(normalized[i] for i in ids)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--verify-only', action='store_true', help='Read-only replay; no figures, ledger updates, inference or acquisitions')
    args = parser.parse_args()
    cfg = authorization_config(load_config('configs/followup_v3.yaml'), read('configs/authorization_v22.json'))
    require(args.verify_only or not (OUT / 'verified_comparison.png').exists(), 'Preserve completed presentation')
    before = read('artifacts/resource_ledger_v2.json')
    with (nullcontext(None) if args.verify_only else Resources(cfg, 'artifacts/resource_ledger_v2.json')) as resource:
        if resource is not None: resource.check()
        summary = read(OUT / 'summary.json'); progress = read(OUT / 'progress.json')
        require(summary['complete'] and progress['complete'], 'Complete-case audit only; retain/report incomplete denominator separately')
        for name, expected in read('reports/protocol_v22_larger.freeze.json')['sha256'].items():
            require(hashlib.sha256(Path(name).read_bytes()).hexdigest() == expected, 'Frozen input changed:' + name)
        jobs = read('data/larger_probe_v22.json')['jobs']; manifest = read('data/manifest_v8.json')
        requests = lines(OUT / 'requests.jsonl'); starts = lines(OUT / 'request_starts.jsonl')
        journal = lines(OUT / 'acquisitions.jsonl'); began = read(OUT / 'started.json')
        require(len(requests) == len(starts) == 60 and len(journal) == 1500, 'Intended request/acquisition denominator')
        require([r['request_id'] for r in requests] == [r['request_id'] for r in starts] == list(range(141, 201)), 'Request identity sequence')
        require(began['authorization']['recorded_at'] < began['at'] < min(r['started'] for r in requests), 'Approval timing')
        from transformers import AutoTokenizer
        from escalation.grammar_v8 import CandidateIDGrammar
        from escalation.core import State
        tokenizer = AutoTokenizer.from_pretrained('models/Qwen2.5-1.5B-Instruct', local_files_only=True, trust_remote_code=False)
        grammar = CandidateIDGrammar(tokenizer)
        labels = {}
        for spec in manifest['datasets']:
            with Path(spec['path']).open() as f:
                rows = list(csv.DictReader(f, delimiter=spec['delimiter']))
            seen = set(); values = []; source_lines = []
            for line, row in enumerate(rows, 2):
                if any(row[k] != str(v) for k, v in spec['filters'].items()): continue
                features = tuple(float(row[k]) for k in spec['feature_names'])
                if features in seen: continue
                seen.add(features); source_lines.append(line); values.append(float(row[spec['primary_objective']]))
            require(len(values) == spec['rows'], 'Independent table schema/count')
            labels[spec['id']] = (values, source_lines, spec['direction'])
        metric_checks = 0
        for job, request in zip(jobs, requests):
            if resource is not None: resource.check()
            require(request['job_id'] == job['job_id'] and request['messages'] == job['messages'], 'Exact prepared messages')
            require(request['status'] == 'response' and request['retry'] == 0, 'Unexpected request failure/retry')
            require((request['model_id'], request['revision'], request['provider']) == (MODEL_ID, REVISION, 'local_transformers'), 'Model provenance')
            require(request['device'] == 'cpu' and request['dtype'] == 'torch.float32', 'Device/dtype')
            require(request['parameters'] == {'do_sample': False, 'max_new_tokens': 20}, 'Sampling parameters')
            rendered = tokenizer.apply_chat_template(job['messages'], tokenize=False, add_generation_prompt=True)
            require(hashlib.sha256(rendered.encode()).hexdigest() == request['rendered_prompt_sha256'], 'Rendered prompt digest')
            require(len(tokenizer(rendered)['input_ids']) == request['input_tokens'], 'Input usage')
            tokens = request['generated_token_ids']
            require(len(tokens) == request['output_tokens'] == 20, 'Output usage')
            require(tokenizer.decode(tokens, skip_special_tokens=True) == request['raw_output'], 'Actual token decoding')
            require(grammar.replay(tokens) == request['selection_trace'], 'Grammar/choice replay')
            require(request['grammar_sha256'] == grammar.sha256 and request['grammar_schedule'] == grammar.schedule, 'Grammar identity')
            context = {k: v for k, v in job.items() if k != 'messages'}
            context.update(namespace='measured_v22', prompt_version='larger_v22', grammar_mode='candidate_order_v19', retry=0)
            expected_key = digest({'messages': job['messages'], 'model': MODEL_ID, 'revision': REVISION,
                'parameters': request['parameters'], 'context': context, 'parser_projection': 'larger_v22',
                'grammar_domains': None, 'grammar_mode': 'candidate_order_v19'})
            require(request['cache_key'] == expected_key, 'Actual model cache binding')
            prefix = read(f"results/v6/prefixes/{job['dataset']}_{job['seed']}.json")['state']
            values, source_lines, direction = labels[job['dataset']]
            selected = [job['mapping'][i] for i in request['raw_output'].strip().splitlines()]
            row = next(r for r in summary['records'] if r['job_id'] == job['job_id'])
            arms = ['llm'] if job['condition'] == 'assigned_ids_repeat' else ['llm', 'first_display', 'lowest_ids']
            for arm in arms:
                outcome = read(OUT / 'arms' / f"{job['job_id']:02d}_{arm}.json"); state = outcome['state']
                require(len(state['ids']) == len(set(state['ids'])) == 20, 'Inclusive unique budget')
                require(state['ids'][:10] == prefix['ids'] and state['labels'][:10] == prefix['labels'], 'Shared prefix')
                proposals = selected if arm == 'llm' else controls(job)[arm]
                require(state['ids'][10:] == proposals == outcome['selected_rows'], 'Response/control-to-arm mapping')
                entries = [e for e in journal if e['job_id'] == job['job_id'] and e['arm'] == arm]
                require(len(entries) == outcome['actual_new_accesses'] == 10, 'Charged arm journal')
                replay = State(**prefix).clone()
                for entry, index in zip(entries, proposals):
                    require(entry['row_id'] == index and entry['source_line'] == source_lines[index], 'Journal row/source mapping')
                    require(float(entry['raw_target']) == values[index], 'Recorded acquisition label')
                    replay.observe(index, [values[index]], [direction])
                require(replay.record() == state, 'Acquired-state deterministic replay')
                expected_loss = scalar_loss(values, direction, state['ids'])
                field = 'llm_loss' if arm == 'llm' else arm + '_loss'
                require(math.isclose(expected_loss, row[field], abs_tol=1e-12), 'Independent scalar metric')
                metric_checks += 1
            classic = read(f"results/v6/classical/{job['dataset']}_{job['seed']}.json")['arms']['centroid_nominal']['state']
            require(math.isclose(scalar_loss(values, direction, classic['ids']), row['classical_loss'], abs_tol=1e-12), 'Classical baseline metric')
        # Recheck repeat equality and calculate descriptive overlaps without assuming stability.
        repeat_details = []
        intervention_details = []
        for original in [j for j in jobs if j['condition'] == 'assigned_ids']:
            a = requests[original['job_id']]
            ids_a = [original['mapping'][i] for i in a['raw_output'].strip().splitlines()]
            for condition in ['reverse_display', 'reassigned_ids', 'assigned_ids_repeat']:
                other = next(j for j in jobs if j['dataset'] == original['dataset'] and j['seed'] == original['seed'] and j['condition'] == condition)
                b = requests[other['job_id']]
                ids_b = [other['mapping'][i] for i in b['raw_output'].strip().splitlines()]
                item = {'dataset': original['dataset'], 'seed': original['seed'], 'condition': condition,
                        'configuration_overlap_out_of_ten': len(set(ids_a) & set(ids_b)), 'exact_output_match': a['raw_output'] == b['raw_output']}
                intervention_details.append(item)
                if condition == 'assigned_ids_repeat':
                    require(a['messages'] == b['messages'], 'Repeated prompt equality')
                    saved = next(r for r in summary['repeated_conditions'] if r['dataset'] == original['dataset'] and r['seed'] == original['seed'])
                    require(saved['exact_output_match'] == item['exact_output_match'], 'Repeat summary')
                    repeat_details.append(item)
        complete_unique = [r for r in summary['records'] if r['condition'] != 'assigned_ids_repeat']
        fields = ['classical_loss', 'uniform_expected_loss', 'first_display_loss', 'lowest_ids_loss', 'llm_loss']
        families = []
        for group in sorted({r['system_group'] for r in complete_unique}):
            records = [r for r in complete_unique if r['system_group'] == group]
            families.append({'system_group': group, **{field: mean(r[field] for r in records) for field in fields}})
        for field in fields[:-1]:
            require(math.isclose(mean(g[field] - g['llm_loss'] for g in families),
                                summary['primary_family_equal_mean_gain_excluding_repeat'][field], abs_tol=1e-12), 'Primary family aggregation')
        checks = {'verified': True, 'request_token_and_provenance_replays': 60, 'paired_arm_replays': 150,
                  'journal_acquisitions': 1500, 'independent_scalar_metric_checks': metric_checks,
                  'exact_repeats_matching': sum(r['exact_output_match'] for r in repeat_details),
                  'intended_repeats': 15, 'family_means': families,
                  'rule_matches_unique45': {k: sum(r[k + '_exact_set_match'] for r in complete_unique) for k in ['first_display', 'lowest_ids']},
                  'new_model_calls': 0, 'new_objective_acquisitions': 0}
        if args.verify_only:
            require(checks == read('artifacts/study_v22/execution_verification.json'), 'Saved verification receipt differs')
            print(json.dumps(checks, indent=2))
            return
        with (OUT / 'verified_family_means.csv').open('w', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=list(families[0])); writer.writeheader(); writer.writerows(families)
        with (OUT / 'presentation_overlaps.csv').open('w', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=list(intervention_details[0])); writer.writeheader(); writer.writerows(intervention_details)
        import matplotlib
        matplotlib.use('Agg')
        import matplotlib.pyplot as plt
        fig, axes = plt.subplots(1, 3, figsize=(11, 3.8))
        for ax, family in zip(axes, families):
            ax.bar(range(5), [family[f] for f in fields], color=['#9BA9B2', '#BAC7CE', '#7D909C', '#627581', '#176B93'])
            ax.set_xticks(range(5), ['Classical', 'Uniform\nexpectation', 'First\ndisplayed', 'Lowest\nIDs', 'LLM'], fontsize=7)
            ax.set_title(family['system_group']); ax.set_ylabel('Mean normalized loss (lower is better)')
        fig.suptitle('V22: larger local model with presentation controls')
        fig.text(.5, .01, 'Development only: 3 families, 5 seeds, 3 presentations; exact repeat excluded from quality means.', ha='center', fontsize=8)
        fig.tight_layout(rect=[0, .045, 1, .96])
        for ext in ['png', 'svg']: fig.savefig(OUT / ('verified_comparison.' + ext), dpi=180)
        plt.close(fig)
        write('artifacts/study_v22/execution_verification.json', checks)
        if resource is not None: resource.check()
    after = read('artifacts/resource_ledger_v2.json')
    write('artifacts/study_v22/verification_presentation_accounting.json',
          {'before_seconds': before['experiment_seconds'], 'after_seconds': after['experiment_seconds'],
           'charged_seconds': after['experiment_seconds'] - before['experiment_seconds'], 'requests_unchanged': before['requests'] == after['requests']})
    print(json.dumps(checks, indent=2))


if __name__ == '__main__': main()
