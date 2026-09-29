"""V175 second revision analysis (post-hoc, exploratory): responds to a second review of the manuscript.

Reuses V174's case loader and V151's unchanged controller code. No acquisition, model request or download.
1. Controller decisions (held-out, unchanged) reaggregated under ecosystem, engine and case weighting.
2. For every useful LLM case (>1% over the reference): does a prespecified classical continuation beat or equal it,
   come within the 1% margin, or trail it by more than 1% (a baseline-set win)?
3. Operational and cost accounting with explicit column definitions.
"""
import argparse, json
from pathlib import Path
import numpy as np
from collect_smollm_v47 import ROOT, read, sha
import revision_v174 as r174
import router_v151 as r151

OUT = ROOT/'results/v175_revision'
ALTS = ['random_full', 'adaptive_neighbor', 'gp_ei']

def router_reaggregation(base):
    feats = {}
    for r in read(ROOT/'artifacts/study_v151/inputs.json')['rows']: feats[r['key']] = r['features']
    out = {}
    for a in r174.LLM:
        rows = [{'key': k, 'group': c['ecosystem'], 'engine': c['engine'], 'features': feats[k], 'gain': r174.gain(c['raw']['sequential_3nn'], c['raw'][a], c['direction']),
                 'adaptive_gain': r174.gain(c['raw']['adaptive_neighbor'], c['raw'][a], c['direction']), 'fallback': False, 'usage': {'generated_tokens': None, 'request_seconds': None}}
                for k, c in sorted(base.items())]
        folds = [r151.outer(rows, g) for g in sorted({r['group'] for r in rows})]
        dec = {k: v for f in folds for k, v in f['decisions'].items()}
        pol = {}
        for p in dec[rows[0]['key']]:
            g = [r['gain']*dec[r['key']][p] for r in rows]
            pol[p] = {'calls': int(sum(dec[r['key']][p] for r in rows)),
                      'ecosystem_weighted': r174.group_mean(g, [r['group'] for r in rows]),
                      'engine_weighted': r174.group_mean(g, [r['engine'] for r in rows]),
                      'case_weighted': float(np.mean(g))}
        out[a] = {'policies': pol, 'decisions': {k: {p: bool(v) for p, v in d.items()} for k, d in dec.items()},
                  'fold_training_groups': {f['held_group']: f['training_groups'] for f in folds}}
    return out

def selector_counts(base, dep):
    pick = {f['held_out']: f['selected'] for f in dep['folds']}
    g = [r174.gain(c['raw']['sequential_3nn'], c['raw'][pick[c['ecosystem']]], c['direction']) for c in base.values()]
    return {'better_by_margin': sum(x > r174.M for x in g), 'worse_by_margin': sum(x < -r174.M for x in g), 'worst_case_gain': min(g)}

def checkpoint_reaggregation(base):
    """V154 BORA-inspired / rank-reliability decisions (call probabilities; utility is linear in them), reweighted per case.
    Ecosystem-grouping decisions give the ecosystem and case weightings; engine-grouping decisions the engine weighting."""
    dec = read(ROOT/'results/v154_controllers/decisions.json'); ref = read(ROOT/'results/v154_controllers/comparison.json')['models']; out = {}
    for m in ['smollm3_3b', 'qwen3_8b']:
        g = {k: r174.gain(c['raw']['sequential_3nn'], c['raw'][m], c['direction']) for k, c in base.items()}; pol = {}
        for p in dec['ecosystem'][m][next(iter(base))]:
            E, N = dec['ecosystem'][m], dec['engine'][m]; ks = sorted(base)
            pol[p] = {'expected_calls': float(sum(E[k][p] for k in ks)),
                      'ecosystem_weighted': r174.group_mean([g[k]*E[k][p] for k in ks], [base[k]['ecosystem'] for k in ks]),
                      'engine_weighted': r174.group_mean([g[k]*N[k][p] for k in ks], [base[k]['engine'] for k in ks]),
                      'case_weighted': float(np.mean([g[k]*E[k][p] for k in ks]))}
            for w, grp in [('ecosystem_weighted', 'ecosystem'), ('engine_weighted', 'engine')]:
                assert abs(pol[p][w]-ref[grp][m][p]['family_mean_gain']) < 1e-12, (m, p, w)
        out[m] = pol
    return out

def trivial_gap(reag):
    """Best non-trivial controller minus the better of always/never calling, per arm and weighting."""
    W = ['ecosystem_weighted', 'engine_weighted', 'case_weighted']; out = {}
    for a, v in reag.items():
        P = v['policies']; ctl = [p for p in P if p not in ('always', 'never')]
        out[a] = {w: {'best_controller': max(ctl, key=lambda p: (P[p][w], p)), 'best_controller_gain': max(P[p][w] for p in ctl),
                      'better_trivial': 'always' if P['always'][w] > P['never'][w] else 'never', 'better_trivial_gain': max(P['always'][w], P['never'][w]),
                      'controller_minus_better_trivial': max(P[p][w] for p in ctl)-max(P['always'][w], P['never'][w])} for w in W}
    return out

def useful_case_matching(base, extended):
    out = {}
    for a in r174.LLM:
        rows = []
        for k, c in base.items():
            g = r174.gain(c['raw']['sequential_3nn'], c['raw'][a], c['direction'])
            if g <= r174.M: continue
            alts = ALTS+(['fixed_neighbor', 'prefix_optimizer']+(['random_proposal'] if c['raw'].get('random_proposal') is not None else []) if extended else [])
            lead = {s: r174.gain(c['raw'][s], c['raw'][a], c['direction']) for s in alts}  # LLM relative to each alternative
            best_alt = min(lead, key=lambda s: (lead[s], s)); m = lead[best_alt]
            kind = 'classical_better_or_equal' if m <= 1e-12 else ('within_margin' if m <= r174.M else 'llm_ahead_by_more_than_margin')
            rows.append({'key': k, 'ecosystem': c['ecosystem'], 'llm_gain_vs_reference': g, 'best_alternative': best_alt, 'llm_lead_over_best_alternative': m, 'kind': kind})
        out[a] = {'useful_cases': len(rows), **{kind: sum(r['kind'] == kind for r in rows) for kind in ['classical_better_or_equal', 'within_margin', 'llm_ahead_by_more_than_margin']},
                  'ecosystems_with_useful_case': len({r['ecosystem'] for r in rows}), 'cases': sorted(rows, key=lambda r: r['key'])}
    return out

def cross_check(res, v174):
    """The reaggregation and matching must reproduce V174 where they overlap."""
    for a, v in res['router_reaggregation'].items():
        for p, x in v174['routers_all_arms'][a]['policies'].items():
            assert abs(v['policies'][p]['ecosystem_weighted']-x['equal_ecosystem_gain']) < 1e-12 and v['policies'][p]['calls'] == x['calls'], (a, p)
    for key, wk in [('useful_case_matching', 'prespecified_baseline_wins'), ('useful_case_matching_extended', 'extended_baseline_wins')]:
        for a, v in res[key].items(): assert v['llm_ahead_by_more_than_margin'] == v174[wk][a]['win_cases'], (key, a)
    return {'router_ecosystem_values_match_v174': True, 'llm_ahead_counts_match_v174_baseline_set_wins': True}

def accounting():
    a = read(ROOT/'results/v174_revision/analysis.json')['operations']; M = ROOT/'results/v173_models'
    def resp(stages): return [json.loads(l) for s in stages for l in (M/s/'responses.jsonl').read_text().splitlines()]
    probe = resp(['P', 'P2']); pilot = resp(['A1'])
    arms = {'gptoss_a1': a['gptoss_a1']['reported_cost_usd'], 'gptoss_a2': a['gptoss_a2']['reported_cost_usd'], 'gptoss_b': a['gptoss_b']['reported_cost_usd']}
    return {'definitions': {'planned_calls': 'one per case (one-shot) or one per round (loop, 5 per case)', 'retry_calls': 'loop only: a second call in a round after an invalid response',
                            'rate_limited_attempts': 'HTTP 429 rejections before generation, retried after backoff; not counted as calls', 'invalid_responses': 'responses that failed validation (all were truncations)',
                            'fallbacks': 'cases (one-shot) or rounds (loop) resolved by the classical fallback'},
            'rows': {'gptoss_a1': {'planned_calls': 70, 'retry_calls': 0, 'rate_limited_attempts': a['gptoss_a1']['rate_limited_429'], 'invalid_responses': 0, 'valid_responses': a['gptoss_a1']['valid'], 'fallbacks': 0},
                     'gptoss_a2': {'planned_calls': 70, 'retry_calls': 0, 'rate_limited_attempts': a['gptoss_a2']['rate_limited_429'], 'invalid_responses': 0, 'valid_responses': a['gptoss_a2']['valid'], 'fallbacks': 0},
                     'gptoss_b': {'planned_calls': 350, 'retry_calls': a['gptoss_b']['retries'], 'rate_limited_attempts': a['gptoss_b']['rate_limited_429'], 'invalid_responses': sum(a['gptoss_b']['invalid_attempt_reasons'].values()),
                                  'valid_responses': a['gptoss_b']['http_attempts']-sum(a['gptoss_b']['invalid_attempt_reasons'].values()), 'fallbacks': a['gptoss_b']['fallback_rounds']}},
            'cost_usd': {'reported_arms': arms, 'reported_arms_total': sum(arms.values()), 'preflight_and_provider_probes': sum(r['reported_cost_usd'] or 0 for r in probe),
                         'aborted_first_attempt_recorded': sum(r['reported_cost_usd'] or 0 for r in pilot), 'aborted_first_attempt_unknown_requests': 1,
                         'ledger_total': read(M/'spend_ledger.json')['spent_usd']}}

def run():
    base = r174.load_cases(); v174 = read(ROOT/'results/v174_revision/analysis.json'); dep = v174['deployable_classical_policy']
    reag = router_reaggregation(base)
    res = {'status': 'V175 post-hoc exploratory second-revision analysis of sealed V141-V174 records; not confirmatory', 'margin': r174.M,
           'selector_vs_reference': {'ecosystem_weighted': dep['policy_gain_vs_sequential_equal_ecosystem'], 'case_weighted': dep['policy_gain_vs_sequential_case_weighted'],
                                     'selected_by_fold': {f['held_out']: f['selected'] for f in dep['folds']}, **selector_counts(base, dep)},
           'router_reaggregation': reag, 'controller_vs_better_trivial_policy': trivial_gap(reag), 'checkpoint_rules_reaggregation_v154': checkpoint_reaggregation(base),
           'useful_case_matching': useful_case_matching(base, False), 'useful_case_matching_extended': useful_case_matching(base, True), 'accounting': accounting()}
    res['cross_check'] = cross_check(res, v174)
    return res

def main():
    ap = argparse.ArgumentParser(); ap.add_argument('--check', action='store_true'); a = ap.parse_args()
    text = json.dumps(run(), indent=1, sort_keys=True, default=float)+'\n'; dest = OUT/'analysis.json'
    if a.check: assert dest.read_text() == text; print(json.dumps({'reproduced': True, 'sha256': sha(dest)})); return
    OUT.mkdir(parents=True, exist_ok=True); dest.write_text(text); print(json.dumps({'written': str(dest.relative_to(ROOT)), 'sha256': sha(dest)}))

if __name__ == '__main__': main()
