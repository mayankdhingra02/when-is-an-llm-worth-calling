"""Read-only independent Decimal outcome and request-cost checks."""
import csv, json
from decimal import Decimal, getcontext
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
getcontext().prec = 40


def read(name): return json.loads((ROOT/name).read_text(), parse_float=Decimal)
def avg(xs): return sum(xs, Decimal(0))/len(xs)
def check(a, b):
    if abs(a-b) > Decimal('1e-12'): raise ValueError(f'Mismatch: {a} vs {b}')


def main():
    summary = read('results/v28_consensus/summary.json'); plans = read('data/consensus_v28.json')['cases']
    requests = [json.loads(s, parse_float=Decimal) for s in (ROOT/'results/v22_larger/requests.jsonl').read_text().splitlines()]
    specs = read('data/manifest_v8.json')['datasets']; metrics = {}; checked = 0
    for plan in plans:
        key = f"{plan['dataset']}_{plan['seed']}"
        row = next(r for r in summary['cases'] if r['dataset'] == plan['dataset'] and r['seed'] == plan['seed'])
        actual = [next(r for r in requests if r['request_id'] == s['request_id']) for s in plan['sources']]
        ballots = [[r['mapping'][symbol] for symbol in r['raw_output'].splitlines()] for r in actual]
        assert ballots == plan['ballots']
        # Deliberately enumerate count classes rather than sorting with production key.
        chosen = [i for n in (3, 2, 1, 0) for i in plan['pool'] if sum(i in b for b in ballots) == n][:10]
        assert chosen == plan['selected'] and set(chosen) <= set().union(*map(set, ballots))
        spec = next(d for d in specs if d['id'] == plan['dataset']); targets = []; seen = set()
        with (ROOT/spec['path']).open(newline='') as f:
            for r in csv.DictReader(f, delimiter=spec['delimiter']):
                if any(r[k] != str(v) for k, v in spec['filters'].items()): continue
                x = tuple(Decimal(r[k]) for k in spec['feature_names'])
                if x in seen: continue
                seen.add(x); targets.append(Decimal(r[spec['primary_objective']]))
        lo, hi = min(targets), max(targets)
        def values(state):
            assert state['labels'] == [[targets[i]] for i in state['ids']]
            target = min(targets[i] for i in state['ids'])
            return target, (target-lo)/(hi-lo)
        target, loss = values(read(f'results/v28_consensus/arms/{key}.json')['state'])
        check(target, row['ensemble_target']); check(loss, row['ensemble_loss'])
        singles = [values(read(f"results/v22_larger/arms/{r['job_id']:02d}_llm.json")['state']) for r in actual]
        bases = {'full_classical': [values(read(f'results/v6/classical/{key}.json')['arms']['centroid_nominal']['state'])],
                 'static_rank': [values(read(f'results/v8/static_rank/{key}.json')['state'])],
                 'adaptive_shortlist': [values(read(f'results/v25_shortlist/arms/{key}.json')['state'])],
                 'single_assigned': [singles[0]], 'single_presentation_mean': singles}
        for b, vs in bases.items():
            normal = avg([v[1]-loss for v in vs]); relative = avg([(v[0]-target)/v[0] for v in vs])
            check(normal, row[b+'_normalized_gain']); check(relative, row[b+'_relative_gain'])
            metrics.setdefault(b, {}).setdefault(plan['system_group'], []).append((normal, relative)); checked += 2
    for b, families in metrics.items():
        normal = avg([avg([v[0] for v in vs]) for vs in families.values()])
        relative = avg([avg([v[1] for v in vs]) for vs in families.values()])
        check(normal, summary['comparisons'][b]['mean_normalized_gain']); check(relative, summary['comparisons'][b]['mean_relative_gain'])
    costs = 0
    for scenario in ('ensemble', 'single_assigned', 'single_presentation_mean'):
        for field in ('input_tokens', 'output_tokens', 'wall_seconds'):
            terms = []
            for plan in plans:
                rs = [next(r for r in requests if r['request_id'] == s['request_id']) for s in plan['sources']]
                v = [r[field] for r in rs]
                terms.append(sum(v) if scenario == 'ensemble' else v[0] if scenario == 'single_assigned' else avg(v))
            check(sum(terms), summary['deployment_usage_scenarios'][scenario][field]); costs += 1
    print(json.dumps({'verified': True, 'independent_raw_response_vote_plans': len(plans),
        'decimal_paired_metric_checks': checked, 'aggregate_metric_checks': 10, 'request_usage_checks': costs,
        'source_labels_checked': True, 'new_model_calls': 0, 'new_objective_acquisitions': 0}, indent=2))


if __name__ == '__main__': main()
