"""V174 revision analysis (post-hoc, exploratory): responds to an external review of the V173 manuscript.

Uses only sealed V141-V173 records. No objective acquisition, model request, download or native execution.
Computed after all outcomes were known; nothing here is confirmatory.
"""
import argparse, copy, glob, json, math
from pathlib import Path
import numpy as np
from collect_smollm_v47 import ROOT, read, sha
import audit_v171 as audit
import router_v151 as r151

OUT = ROOT/'results/v174_revision'
LLM = ['smollm3_3b', 'qwen3_8b', 'qwen3_14b', 'gptoss_a1', 'gptoss_a2', 'gptoss_b']
PRESPEC = ['random_full', 'adaptive_neighbor', 'gp_ei']
CLASSICAL = ['sequential_3nn', 'random_full', 'adaptive_neighbor', 'fixed_neighbor', 'gp_ei', 'prefix_optimizer']
M = .01

def gain(ref, x, d): return audit.relative_gain(ref, x, d)
def logg(ref, x, d): return audit.log_gain(ref, x, d)

def load_cases():
    base = {}; hist = {}
    for c in audit.recorded_cases():
        hist[(c['model'], c['key'])] = c['raw']['llm']
        if c['key'] not in base: base[c['key']] = {k: c[k] for k in ['key', 'engine', 'ecosystem', 'direction']} | {'raw': {k: v for k, v in c['raw'].items() if k != 'llm'}}
    jobs = {j['qualified_key']: j for j in read(ROOT/'artifacts/study_v172/jobs.json')}
    for k, c in base.items():  # continuation of the optimizer that built the prefix
        j = jobs[k]
        if j['origin'] == 'v141':
            s = read(ROOT/f"results/v41_transfer/arms/{j['dataset']}_{j['seed']}_full_classical.json")['state']
            vals = [y[0] for y in s['labels']]; c['raw']['prefix_optimizer'] = min(vals) if c['direction'] == 'minimize' else max(vals)
        else: c['raw']['prefix_optimizer'] = c['raw']['sequential_3nn']
    t = {}
    for p in glob.glob(str(ROOT/'results/v172_eval/arms/*.json'))+glob.glob(str(ROOT/'results/v173_eval/arms/*.json'))+glob.glob(str(ROOT/'results/v173_models/B*/arms/*.json')):
        r = read(p); t[(r['arm'], r['qualified_key'])] = r['target']
    for k, c in base.items():
        for a in LLM: c['raw'][a] = hist[(a, k)] if (a, k) in hist else t[(a, k)]
    assert len(base) == 70 and all(c['raw'][a] is not None for c in base.values() for a in LLM)
    return base

def group_mean(vals, groups):
    ks = sorted(set(groups)); return float(np.mean([np.mean([v for v, g in zip(vals, groups) if g == k]) for k in ks]))

def weighting(base):
    cs = list(base.values()); out = {}
    for a in LLM+CLASSICAL[1:]:
        g = [gain(c['raw']['sequential_3nn'], c['raw'][a], c['direction']) for c in cs]; lg = [logg(c['raw']['sequential_3nn'], c['raw'][a], c['direction']) for c in cs]
        eco = [c['ecosystem'] for c in cs]; eng = [c['engine'] for c in cs]; ecos = sorted(set(eco))
        per = {e: float(np.mean([x for x, y in zip(g, eco) if y == e])) for e in ecos}
        loeo = [float(np.mean([per[x] for x in ecos if x != e])) for e in ecos]
        out[a] = {'equal_ecosystem': group_mean(g, eco), 'equal_engine': group_mean(g, eng), 'case_weighted': float(np.mean(g)),
                  'equal_ecosystem_excluding_dune': float(np.mean([per[e] for e in ecos if e != 'dune_hsmgp'])),
                  'leave_one_ecosystem_out_range': [min(loeo), max(loeo)], 'case_weighted_log': float(np.mean(lg)), 'equal_ecosystem_log': group_mean(lg, eco)}
    return out

def wins(base, extended):
    out = {}
    for a in LLM:
        per = {}
        for c in base.values():
            sw = ['sequential_3nn']+PRESPEC+(['fixed_neighbor', 'prefix_optimizer']+(['random_proposal'] if c['raw'].get('random_proposal') is not None else []) if extended else [])
            w = all(gain(c['raw'][s], c['raw'][a], c['direction']) > M for s in sw)
            e = per.setdefault(c['ecosystem'], {'cases': 0, 'wins': 0, 'keys': []}); e['cases'] += 1; e['wins'] += w
            if w: e['keys'].append(c['key'])
        out[a] = {'ecosystems_with_win': sum(v['wins'] > 0 for v in per.values()), 'win_cases': sum(v['wins'] for v in per.values()), 'per_ecosystem': per}
    return out

def deployable_classical(base):
    """Leave-one-ecosystem-out: pick the classical continuation with the best equal-ecosystem mean gain on the other ecosystems."""
    cs = list(base.values()); ecos = sorted({c['ecosystem'] for c in cs}); folds = []; chosen = {}
    for e in ecos:
        train = [c for c in cs if c['ecosystem'] != e]
        score = {a: group_mean([gain(c['raw']['sequential_3nn'], c['raw'][a], c['direction']) for c in train], [c['ecosystem'] for c in train]) for a in CLASSICAL}
        pick = max(CLASSICAL, key=lambda a: (round(score[a], 12), -CLASSICAL.index(a))); folds.append({'held_out': e, 'selected': pick, 'training_scores': score})
        for c in cs:
            if c['ecosystem'] == e: chosen[c['key']] = pick
    pol = {k: base[k]['raw'][chosen[k]] for k in base}
    g = [gain(base[k]['raw']['sequential_3nn'], pol[k], base[k]['direction']) for k in base]; eco = [base[k]['ecosystem'] for k in base]
    out = {'folds': folds, 'policy_gain_vs_sequential_equal_ecosystem': group_mean(g, eco), 'policy_gain_vs_sequential_case_weighted': float(np.mean(g)), 'llm_vs_policy': {}}
    for a in LLM:
        gl = [gain(pol[k], base[k]['raw'][a], base[k]['direction']) for k in base]
        out['llm_vs_policy'][a] = {'equal_ecosystem': group_mean(gl, eco), 'case_weighted': float(np.mean(gl)), 'better_by_margin': sum(x > M for x in gl), 'worse_by_margin': sum(x < -M for x in gl)}
    return out

def routers(base):
    """Exploratory: rerun the frozen V151 predictors and threshold rule unchanged on stronger arms' continuous gains."""
    feats = {}
    for r in read(ROOT/'artifacts/study_v151/inputs.json')['rows']:
        if r['key'] in feats: assert feats[r['key']] == r['features']
        feats[r['key']] = r['features']
    out = {}
    for a in LLM:
        rows = [{'key': k, 'group': c['ecosystem'], 'features': feats[k], 'gain': gain(c['raw']['sequential_3nn'], c['raw'][a], c['direction']),
                 'adaptive_gain': gain(c['raw']['adaptive_neighbor'], c['raw'][a], c['direction']), 'fallback': False,
                 'usage': {'generated_tokens': None, 'request_seconds': None}} for k, c in sorted(base.items())]
        folds = [r151.outer(rows, g) for g in sorted({r['group'] for r in rows})]; s = r151.summarize(rows, folds)
        pol = s['policies']
        out[a] = {'policies': {p: {'calls': v['calls'], 'equal_ecosystem_gain': v['family_mean_gain'], 'gain_above_matched_random': v['gain_above_random'], 'useful': v['useful'], 'harmful': v['harmful']}
                               for p, v in pol.items() if p in ['never', 'always', 'selected_predictor', 'ridge_original', 'ridge_extended', 'tree_extended', 'rbf_extended', 'ridge_extended_q80', 'tree_extended_q80', 'rbf_extended_q80', 'uncertainty', 'uncertainty_q80']},
                  'oracle_equal_ecosystem': s['oracle_family_gain'], 'groups_with_useful_gt_1pct': s['opportunity_groups'],
                  'groups_with_positive_gain': sorted({r['group'] for r in rows if r['gain'] > 0}), 'ranking_auc_by_group': s['ranking']['ridge_extended']}
    return out

def operations():
    def lines(p): return [json.loads(l) for l in Path(p).read_text().splitlines()] if Path(p).exists() else []
    v151 = {(r['model']): [] for r in read(ROOT/'artifacts/study_v151/inputs.json')['rows']}
    for r in read(ROOT/'artifacts/study_v151/inputs.json')['rows']: v151[r['model']].append(r)
    out = {}
    for m in ['smollm3_3b', 'qwen3_8b']:
        rs = v151[m]; secs = [r['usage']['request_seconds'] for r in rs if r['usage']['request_seconds'] is not None]
        out[m] = {'logical_requests': len(rs), 'fallback_cases': sum(r['fallback'] for r in rs), 'unknown_usage': sum(r['usage']['generated_tokens'] is None for r in rs),
                  'mean_request_seconds': float(np.mean(secs)), 'cost_usd': 0.0, 'where': 'local llama.cpp, recorded cohort V141/V145/V148'}
    s172 = {s: read(ROOT/f'results/v172_models/{s}/summary.json') for s in ['A1R', 'A2']}
    out['qwen3_14b'] = {'logical_requests': sum(v['attempted'] for v in s172.values()), 'valid': sum(v['valid'] for v in s172.values()), 'fallback_cases': 70-sum(v['valid'] for v in s172.values()),
                        'mean_request_seconds': float(np.mean([r['wall_seconds'] for s in ['A1R', 'A2'] for r in lines(ROOT/f'results/v172_models/{s}/responses.jsonl')])), 'cost_usd': 0.0, 'failed_stage_attempts': 'A1 (port probe, 0 requests)'}
    M173 = ROOT/'results/v173_models'
    def hosted(stages):
        rs = [r for s in stages for r in lines(M173/s/'responses.jsonl')]; ok = [r for r in rs if r['http_status'] == 200]
        return {'http_attempts': len(rs), 'rate_limited_429': sum(r['http_status'] == 429 for r in rs), 'responses_200': len(ok),
                'mean_seconds_per_200': float(np.mean([r['seconds'] for r in ok])), 'reported_cost_usd': sum(r['reported_cost_usd'] or 0 for r in rs),
                'completion_tokens': sum(((r['response'] or {}).get('usage') or {}).get('completion_tokens') or 0 for r in ok),
                'reasoning_tokens': sum((((r['response'] or {}).get('usage') or {}).get('completion_tokens_details') or {}).get('reasoning_tokens') or 0 for r in ok)}
    ch = read(ROOT/'results/v173_eval/choices.json')
    for arm, stages in [('gptoss_a1', ['A1R', 'A1R.c1']), ('gptoss_a2', ['A2', 'A2.c1'])]:
        c = [x for x in ch if x['arm'] == arm]; out[arm] = {**hosted(stages), 'logical_requests': 70, 'valid': sum(x['model_status'] == 'valid' for x in c), 'fallback_cases': sum(x['fallback'] for x in c)}
    bst = sorted(p.parent.name for p in M173.glob('B*/summary.json')); arms = [read(p) for p in M173.glob('B*/arms/*.json')]
    rounds = [json.loads(l) for s in bst for l in (M173/s/'rounds.jsonl').read_text().splitlines()]
    reasons = [a.get('reason', '') for r in rounds for a in (r.get('attempts') or []) if a.get('status') == 'invalid']
    out['gptoss_b'] = {**hosted(bst), 'cases': len(arms), 'model_rounds': sum(sum(x['kind'] == 'model' for x in r['rounds']) for r in arms), 'fallback_rounds': sum(r['fallback_rounds'] for r in arms),
                       'retries': sum(sum(x['attempts'] > 1 for x in r['rounds']) for r in arms), 'invalid_attempt_reasons': {k: sum(k in x for x in reasons) for k in ['finish_reason', 'Malformed', 'Expected exactly', 'Bad proposal', 'HTTP', 'Empty']},
                       'collisions': sum(len(r['collisions']) for r in arms)}
    out['gptoss_failed_first_attempt'] = {**hosted(['A1']), 'note': 'operator-stopped A1 at the 4,000-token cap; 1 request in flight with unknown cost'}
    out['hosted_total_reported_usd'] = read(M173/'spend_ledger.json')['spent_usd']
    return out

def run():
    base = load_cases()
    res = {'status': 'V174 post-hoc exploratory revision analysis of sealed V141-V173 records; not confirmatory', 'margin': M,
           'weighting': weighting(base), 'prespecified_baseline_wins': wins(base, False), 'extended_baseline_wins': wins(base, True),
           'deployable_classical_policy': deployable_classical(base), 'routers_all_arms': routers(base), 'operations': operations(),
           'native_exhaustive_headroom_v165': [x for x in read(ROOT/'results/v165_headroom/comparison.json')['prefix_summary'] if x['checkpoint'] == 10]}
    return res

def main():
    ap = argparse.ArgumentParser(); ap.add_argument('--check', action='store_true'); a = ap.parse_args()
    text = json.dumps(run(), indent=1, sort_keys=True, default=float)+'\n'; dest = OUT/'analysis.json'
    if a.check: assert dest.read_text() == text; print(json.dumps({'reproduced': True, 'sha256': sha(dest)})); return
    OUT.mkdir(parents=True, exist_ok=True); dest.write_text(text); print(json.dumps({'written': str(dest.relative_to(ROOT)), 'sha256': sha(dest)}))

if __name__ == '__main__': main()
