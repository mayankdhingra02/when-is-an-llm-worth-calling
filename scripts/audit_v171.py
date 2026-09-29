"""V171 independent post-hoc audit: is the escalation target learnable, and is the headroom LLM-specific?

Exploratory re-analysis of already sealed, already exposed records. It makes no objective
acquisition, model request, download, native execution or network access. The auditor inspected
these outcomes before writing this script, so nothing here is confirmatory. Recorded-table and
native cohorts are analysed separately and never pooled. Repeated seeds stay inside their system.
"""
import argparse, hashlib, json, math
from pathlib import Path
import numpy as np
from scipy.stats import beta

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT/'results/v171_audit'
MARGIN = .01          # recorded cohort's historical per-case practical margin
ROBUST = .10          # native cohort's historical robust margin
MODELS = ['smollm3_3b', 'qwen3_8b']
INPUTS = {
    'recorded_rows': 'artifacts/study_v151/inputs.json',
    'recorded_v141': 'results/v141_analysis/comparison.json',
    'recorded_spark': 'results/v145_spark/comparison.json',
    'recorded_hadoop': 'results/v148_hadoop/comparison.json',
    'recorded_gp': 'results/v155_gp/comparison.json',
    'native_v169': 'results/v169_ezr/comparison.json',
    'native_v170': 'results/v170_ezr/comparison.json',
}
# Deployable cheap continuations available for every case of each cohort.
RECORDED_SWITCHES = ['random_full', 'adaptive_neighbor', 'gp_ei']
NATIVE_SWITCHES = ['random_full', 'adaptive_neighbor', 'gp_ei']
NATIVE_SOURCE_SWITCHES = ['ezr_upstream_centroid', 'ezr_upstream_bayes']

def sha(p): return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def load(n): return json.loads((ROOT/n).read_text())

def relative_gain(reference, candidate, direction):
    """Positive when candidate beats reference; relative to the reference value."""
    if direction not in ('minimize', 'maximize'): raise ValueError('Unknown direction')
    if not (math.isfinite(reference) and math.isfinite(candidate)) or reference <= 0: raise ValueError('Positive finite values required')
    return (reference-candidate)/reference if direction == 'minimize' else (candidate-reference)/reference

def log_gain(reference, candidate, direction):
    """Symmetric sensitivity: log ratio, positive when candidate is better."""
    if reference <= 0 or candidate <= 0: raise ValueError('Positive values required')
    r = math.log(reference/candidate)
    return r if direction == 'minimize' else -r

def equal_group_mean(values, groups):
    keys = sorted(set(groups))
    return float(np.mean([np.mean([v for v, g in zip(values, groups) if g == k]) for k in keys]))

def learnability(cases, positive, group_key):
    """Leave-one-group-out structure of the positive class; independent of any predictor."""
    groups = sorted({c[group_key] for c in cases}); folds = []
    for held in groups:
        test = [c for c in cases if c[group_key] == held]; train = [c for c in cases if c[group_key] != held]
        tp = sum(positive(c) for c in test); trp = sum(positive(c) for c in train)
        folds.append({'held_group': held, 'test_cases': len(test), 'test_positives': tp, 'training_positives': trp,
                      'training_groups_with_positives': len({c[group_key] for c in train if positive(c)})})
    informative = [f for f in folds if f['test_positives'] > 0 and f['training_positives'] > 0]
    return {'folds': folds, 'groups': len(groups), 'groups_with_positives': sum(f['test_positives'] > 0 for f in folds),
            'positives': sum(positive(c) for c in cases), 'informative_folds': len(informative)}

def upper_bound(k, n, alpha=.05):
    """One-sided Clopper-Pearson upper bound on a per-group rate."""
    if not 0 <= k <= n or n < 1: raise ValueError('Invalid count')
    return 1. if k == n else float(beta.ppf(1-alpha, k+1, n-k))

def recorded_cases():
    rows = load(INPUTS['recorded_rows'])['rows']; v141 = load(INPUTS['recorded_v141'])['rows']
    spark = load(INPUTS['recorded_spark'])['cases']; hadoop = load(INPUTS['recorded_hadoop'])['cases']
    gp = {(c['key'], c['model']): c for c in load(INPUTS['recorded_gp'])['cases'] if c['kernel_length'] == '1.0'}
    out = []
    for r in rows:
        m, sk, d = r['model'], r['source_key'], r['direction']
        if r['stage'] == 141:
            src, = [x for x in v141 if x['case_key'] == sk and x['model'] == m]; v = src['references']
            raw = {'sequential_3nn': v['sequential_3nn'], 'random_full': v['random_full'], 'fixed_neighbor': v['fixed_prefix_neighbor'], 'adaptive_neighbor': v['adaptive_incumbent_neighbor']}
            assert math.isclose(src['target'], r['target'], rel_tol=1e-12)
        elif r['stage'] == 145:
            src, = [x for x in spark if x['key'] == sk and x['model'] == m]; raw = dict(src['control_best_observed'])
            assert math.isclose(src['model_best_observed'], r['target'], rel_tol=1e-12)
        elif r['stage'] == 148:
            src, = [x for x in hadoop if x['key'] == sk and x['model'] == m]; raw = dict(src['references'])
            assert math.isclose(src['target'], r['target'], rel_tol=1e-12)
        else: raise ValueError('Unexpected stage')
        assert math.isclose(raw['sequential_3nn'], r['sequential'], rel_tol=1e-12) and math.isclose(raw['adaptive_neighbor'], r['adaptive'], rel_tol=1e-12)
        ecosystem = 'spark_hadoop' if r['group'] in ('spark', 'hadoop_mapreduce') else r['group']
        g = gp[(r['key'], m)]
        assert g['gp_status'] == 'complete' and g['group'] == ('spark_hadoop_ecosystem' if ecosystem == 'spark_hadoop' else ecosystem)
        assert math.isclose(g['llm_target'], r['target'], rel_tol=1e-12)
        raw['gp_ei'] = g['gp_target']; raw['llm'] = r['target']
        assert math.isclose(relative_gain(raw['sequential_3nn'], raw['gp_ei'], d), g['gp_gain_vs_sequential'], abs_tol=1e-12)
        assert math.isclose(relative_gain(raw['sequential_3nn'], raw['llm'], d), r['gain'], abs_tol=1e-12)
        out.append({'key': r['key'], 'model': m, 'engine': r['group'], 'ecosystem': ecosystem,
                    'direction': d, 'fallback': r['fallback'], 'raw': raw})
    assert len(out) == 140 and len({(c['model'], c['key']) for c in out}) == 140
    return out

def native_cases():
    arms = {}
    for n in ['native_v169', 'native_v170']:
        for a in load(INPUTS[n])['arms']: assert (a['case'], a['arm']) not in arms; arms[(a['case'], a['arm'])] = a
    out = []
    for case in sorted({c for c, _ in arms}):
        engine = case.rsplit('_', 1)[0]
        for m in MODELS:
            raw = {k: arms[(case, k)] for k in ['sequential_3nn', 'random_full', 'random_proposal', 'adaptive_neighbor', 'gp_ei'] + NATIVE_SOURCE_SWITCHES}
            raw['llm'] = arms[(case, m)]
            out.append({'key': case, 'model': m, 'engine': engine, 'task_family': 'n_queens' if engine in ('cvc5', 'ortools') else engine,
                        'direction': 'minimize', 'raw': raw})
    assert len(out) == 60
    return out

def value(c, arm): return c['raw'][arm]['median'] if isinstance(c['raw'][arm], dict) else c['raw'][arm]
def gain(c, arm, ref='sequential_3nn'): return relative_gain(value(c, ref), value(c, arm), c['direction'])
def distinct(c, arm, ref='sequential_3nn'): return not isinstance(c['raw'][arm], dict) or c['raw'][arm]['row_id'] != c['raw'][ref]['row_id']
def robust(c, arm, ref='sequential_3nn'):
    a, b = c['raw'][arm], c['raw'][ref]
    return gain(c, arm, ref) > ROBUST and distinct(c, arm, ref) and all(x['quality_valid'] and x['stable'] and x['above_floor'] for x in (a, b))
def useful(c, arm, ref='sequential_3nn'): return gain(c, arm, ref) > MARGIN and distinct(c, arm, ref)

def arm_summary(cases, arm, group_key):
    have = [c for c in cases if c['raw'].get(arm) is not None]
    if not have: return None
    gs = [gain(c, arm) for c in have]; groups = [c[group_key] for c in have]
    s = {'cases': len(have), 'groups': len(set(groups)), 'equal_group_mean_gain': equal_group_mean(gs, groups),
         'equal_group_mean_log_gain': equal_group_mean([log_gain(value(c, 'sequential_3nn'), value(c, arm), c['direction']) for c in have], groups),
         'equal_group_hindsight_headroom': equal_group_mean([max(0., g) for g in gs], groups),
         'useful_over_sequential': sum(useful(c, arm) for c in have),
         'groups_with_useful': sorted({c[group_key] for c in have if useful(c, arm)}),
         'same_setting_as_sequential': sum(not distinct(c, arm) for c in have)}
    if isinstance(have[0]['raw'][arm], dict): s['robust_over_sequential'] = sum(robust(c, arm) for c in have)
    return s

def cohort(cases, arms, switches, group_keys, extra_switch_sets):
    result = {}
    for m in MODELS:
        cs = [c for c in cases if c['model'] == m]; primary = group_keys[0]
        res = {'arms': {a: arm_summary(cs, a, primary) for a in arms}, 'llm_vs_single_switch': {}, 'learnability': {}}
        for a in [x for x in arms if x != 'llm']:
            have = [c for c in cs if c['raw'].get(a) is not None]
            res['llm_vs_single_switch'][a] = {'cases': len(have), 'llm_better_by_margin': sum(useful(c, 'llm', a) for c in have)}
        def specific(c, sw): return useful(c, 'llm') and all(useful(c, 'llm', a) for a in sw)
        res['llm_specific_wins'] = {}
        for name, sw in [('sequential_plus_' + '_'.join(switches), switches)] + extra_switch_sets:
            wins = [c for c in cs if specific(c, sw)]
            res['llm_specific_wins'][name] = {'switches': ['sequential_3nn'] + sw, 'cases': len(wins), 'keys': [c['key'] for c in wins],
                                              'groups': sorted({c[primary] for c in wins}), 'groups_total': len({c[primary] for c in cs})}
        llm_useful = [c for c in cs if useful(c, 'llm')]
        res['llm_useful_cooccurrence'] = {'llm_useful_cases': len(llm_useful),
            'with_some_switch_also_useful': sum(any(c['raw'].get(a) is not None and useful(c, a) for a in switches) for c in llm_useful),
            'cases': [{'key': c['key'], 'llm_gain': gain(c, 'llm'), **{a + '_gain': gain(c, a) for a in switches}} for c in llm_useful]}
        for gk in group_keys:
            res['learnability'][gk] = learnability(cs, lambda c: useful(c, 'llm'), gk)
        result[m] = res
    return result

def design(results):
    """Per-cohort, per-model arithmetic for sizing a prospective cohort; never pooled across cohorts."""
    out = {}
    for name, (res, key) in results.items():
        for m in MODELS:
            w = res[m]['llm_specific_wins'][key]; k, n = len(w['groups']), w['groups_total']; ub = upper_bound(k, n)
            out[f'{name}/{m}'] = {'positive_groups': k, 'groups': n, 'one_sided_95_upper_rate': ub,
                                  'fresh_groups_for_expected_positive_groups': {str(G): {'at_upper_bound': math.ceil(G/ub) if ub > 0 else None,
                                                                                         'at_rate_0.10': math.ceil(G/.10), 'at_rate_0.05': math.ceil(G/.05)} for G in (3, 5, 8)},
                                  'upper_rate_after_additional_all_negative_groups': {str(a): upper_bound(k, n+a) for a in (6, 12, 20, 30)}}
    return out

def run():
    hashes = {k: sha(ROOT/v) for k, v in INPUTS.items()}
    rec = recorded_cases(); nat = native_cases()
    recorded = cohort(rec, ['llm', 'random_full', 'random_proposal', 'fixed_neighbor', 'adaptive_neighbor', 'gp_ei'], RECORDED_SWITCHES, ['ecosystem', 'engine'], [])
    native = cohort(nat, ['llm', 'random_full', 'random_proposal', 'adaptive_neighbor', 'gp_ei'] + NATIVE_SOURCE_SWITCHES, NATIVE_SWITCHES, ['engine', 'task_family'],
                    [('sequential_plus_all_six_classical', NATIVE_SWITCHES + ['random_proposal'] + NATIVE_SOURCE_SWITCHES)])
    key = 'sequential_plus_' + '_'.join(RECORDED_SWITCHES)
    return {'status': 'post-hoc exploratory audit of exposed sealed records; not confirmatory', 'inputs': INPUTS, 'input_sha256': hashes,
            'new_acquisitions': 0, 'new_model_requests': 0, 'new_downloads': 0, 'margin': MARGIN, 'native_robust_margin': ROBUST,
            'definitions': {'useful': 'relative gain over reference > margin and, for native arms, a different selected setting',
                            'llm_specific_win': 'LLM useful over sequential_3nn and over every listed cheap switch',
                            'hindsight_headroom': 'equal-group mean of max(0, gain over sequential); non-deployable diagnostic',
                            'informative_fold': 'held-out group has >=1 LLM-useful case and training groups have >=1'},
            'recorded_cohort': recorded, 'native_cohort': native,
            'design_arithmetic': design({'recorded': (recorded, key), 'native': (native, key)})}

def main():
    ap = argparse.ArgumentParser(); ap.add_argument('--check', action='store_true', help='recompute and compare with saved audit.json'); args = ap.parse_args()
    text = json.dumps(run(), indent=1, sort_keys=True) + '\n'; dest = OUT/'audit.json'
    if args.check:
        assert dest.read_text() == text, 'audit.json differs from recomputation'; print(json.dumps({'reproduced': True, 'sha256': sha(dest)})); return
    OUT.mkdir(parents=True, exist_ok=True); dest.write_text(text); print(json.dumps({'written': str(dest.relative_to(ROOT)), 'sha256': sha(dest)}))

if __name__ == '__main__': main()
