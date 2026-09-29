"""V172 frozen analysis: LLM-specific headroom for Qwen3-14B and a Qwen3-8B re-draw versus historical draws.

Reads historical classical arms through the V171 audit loader (which asserts agreement with V151/V155) and
V172 arms from results/v172_eval. Cohorts are never pooled; seeds stay within their system group.
"""
import argparse, json, math
from pathlib import Path
import numpy as np
from collect_smollm_v47 import ROOT, read, sha
from common_v172 import A, M, E, STAGES, FAILED_STAGES, config, decision
import audit_v171 as audit
OUT = ROOT/'results/v172_analysis'
ARMS = ['smollm3_3b', 'qwen3_8b', 'qwen3_8b_redraw', 'qwen3_14b']
SWITCHES = ['random_full', 'adaptive_neighbor', 'gp_ei']

def cases_for(arm, base, new):
    """Clone classical raw values per case and insert this arm's B20 target as 'llm'."""
    out = []
    for key, c in base.items():
        if arm in ('smollm3_3b', 'qwen3_8b'): target = c['historical'][arm]
        else: target = new[arm].get(key)
        cc = {**c, 'raw': {**c['raw'], 'llm': target}}; out.append(cc)
    return out

def specific(c, margin):
    if c['raw']['llm'] is None: return False
    g = lambda ref: audit.relative_gain(c['raw'][ref], c['raw']['llm'], c['direction'])
    return g('sequential_3nn') > margin and all(g(a) > margin for a in SWITCHES)

def summarize(cases, margin):
    scored = [c for c in cases if c['raw']['llm'] is not None]; eco = sorted({c['ecosystem'] for c in cases})
    wins = [c for c in scored if specific(c, margin)]
    gains = lambda cs: [audit.relative_gain(c['raw']['sequential_3nn'], c['raw']['llm'], c['direction']) for c in cs]
    def eq(vals, cs, key='ecosystem'): return audit.equal_group_mean(vals, [c[key] for c in cs]) if cs else None
    return {'cases': len(cases), 'scored': len(scored), 'unscorable': len(cases)-len(scored),
            'ecosystems_with_llm_specific_win': len({c['ecosystem'] for c in wins}), 'engines_with_llm_specific_win': len({c['engine'] for c in wins}),
            'llm_specific_win_cases': len(wins), 'llm_specific_win_keys': sorted(c['key'] for c in wins), 'ecosystems': len(eco),
            'useful_over_sequential': sum(g > margin for g in gains(scored)),
            'equal_ecosystem_mean_gain_vs_sequential': eq(gains(scored), scored),
            'equal_ecosystem_mean_log_gain_vs_sequential': eq([audit.log_gain(c['raw']['sequential_3nn'], c['raw']['llm'], c['direction']) for c in scored], scored),
            'equal_ecosystem_hindsight_headroom': eq([max(0., g) for g in gains(scored)], scored),
            'better_than_single_switch_by_margin': {a: sum(audit.relative_gain(c['raw'][a], c['raw']['llm'], c['direction']) > margin for c in scored) for a in SWITCHES}}

def paired(base, new, a, b, margin):
    rows = []
    for key, c in base.items():
        x = c['historical'][a] if a in c['historical'] else new[a].get(key); y = c['historical'][b] if b in c['historical'] else new[b].get(key)
        if x is None or y is None: continue
        rows.append(audit.relative_gain(x, y, c['direction']))  # positive: b beats a
    r = np.array(rows)
    return {'reference': a, 'treatment': b, 'pairs': len(rows), 'treatment_better_by_margin': int((r > margin).sum()), 'treatment_worse_by_margin': int((r < -margin).sum()),
            'identical': int((np.abs(r) < 1e-12).sum()), 'mean_relative_gain': float(r.mean()) if len(r) else None}

def reliability():
    out = {}
    for stage in STAGES:
        s = read(M/stage/'summary.json'); resp = [json.loads(l) for l in (M/stage/'responses.jsonl').read_text().splitlines()]
        pred = [r['response'].get('tokens_predicted') for r in resp]; ev = [r['response'].get('tokens_evaluated') for r in resp]
        out[stage] = {'arm': s['arm'], 'intended': s['intended'], 'responses': s['responses'], 'valid': s['valid'], 'invalid': s['invalid'], 'unattempted': len(s['unattempted']),
                      'error': s['error'], 'generated_tokens_observed': sum(p for p in pred if isinstance(p, int)), 'prefill_tokens_observed': sum(e for e in ev if isinstance(e, int)),
                      'unknown_usage_responses': sum(not isinstance(p, int) or not isinstance(e, int) for p, e in zip(pred, ev)),
                      'request_seconds': sum(r['wall_seconds'] for r in resp), 'startup_seconds': s['ledger'].get('startup_seconds'), 'peak_server_rss_bytes': s['ledger']['peak_server_rss_bytes'],
                      'stage_seconds': s['ledger'].get('stage_seconds'), 'server_exit_code': s['ledger'].get('server_exit_code')}
    out['failed_stages'] = {s: {'reason': why, 'summary_error': read(M/s/'summary.json')['error'], 'ledger': read(M/s/'ledger.json')} for s, why in FAILED_STAGES.items()}
    choices = read(E/'choices.json')
    for arm in ['qwen3_14b', 'qwen3_8b_redraw']:
        ch = [c for c in choices if c['arm'] == arm]; diag = [d for c in ch for d in c['projection']]
        dist = [d.get('hamming_distance', d.get('distance')) for d in diag]
        out[arm+'_selection'] = {'arms': len(ch), 'fallbacks': sum(c['fallback'] for c in ch), 'projected_proposals': len(diag), 'nonzero_projection_distance': sum(x > 0 for x in dist),
                                 'repeated_proposals': sum(d['repeated_proposal'] for d in diag), 'matches_prefix': sum(d.get('matches_prefix', d.get('matches_initial_observation', False)) for d in diag)}
    return out

def run():
    cfg = config(); margin = cfg['margin']; hist = audit.recorded_cases(); base = {}
    for c in hist:
        b = base.setdefault(c['key'], {k: c[k] for k in ['key', 'engine', 'ecosystem', 'direction']} | {'raw': {k: v for k, v in c['raw'].items() if k != 'llm'}, 'historical': {}})
        b['historical'][c['model']] = c['raw']['llm']
    assert len(base) == 70
    new = {a: {} for a in ['qwen3_14b', 'qwen3_8b_redraw']}; status = {}
    for p in sorted((E/'arms').glob('*.json')):
        r = read(p); new[r['arm']][r['qualified_key']] = r['target']; status[(r['arm'], r['qualified_key'])] = r.get('status', 'scored')
        if r['target'] is not None: assert r['direction'] == base[r['qualified_key']]['direction']
    summaries = {a: summarize(cases_for(a, base, new), margin) for a in ARMS}
    # Amendment 2 (pre-outcome, descriptive): restrict each new arm to cases where it returned a valid response.
    choices = read(E/'choices.json'); sensitivity = {}
    for a in ['qwen3_14b', 'qwen3_8b_redraw']:
        valid = {c['qualified_key'] for c in choices if c['arm'] == a and c['model_status'] == 'valid'}
        sub = [c for c in cases_for(a, base, new) if c['key'] in valid]
        sensitivity[a] = {'valid_response_cases': len(valid), 'fallback_cases': 70-len(valid), 'ecosystems_covered': len({c['ecosystem'] for c in sub}),
                          **{k: v for k, v in summarize(sub, margin).items() if k in ['ecosystems_with_llm_specific_win', 'llm_specific_win_cases', 'llm_specific_win_keys', 'equal_ecosystem_mean_gain_vs_sequential', 'equal_ecosystem_hindsight_headroom']}}
    result = {'status': 'V172 frozen analysis; exposed recorded tasks, new model draws; exploratory beyond the pre-registered decision rule', 'margin': margin, 'switch_set': ['sequential_3nn']+SWITCHES,
              'summaries': summaries,
              'sensitivity_valid_responses_only': {'label': 'Amendment 2 descriptive sensitivity; does not replace the primary estimand or the frozen decision rule', **sensitivity},
              'redraw_count_is_lower_bound': sensitivity['qwen3_8b_redraw']['fallback_cases'] > 0,
              'paired': [paired(base, new, a, b, margin) for a, b in [('qwen3_8b', 'qwen3_14b'), ('qwen3_8b', 'qwen3_8b_redraw'), ('qwen3_8b_redraw', 'qwen3_14b'), ('smollm3_3b', 'qwen3_8b')]],
              'reliability': reliability(), 'evaluation': read(E/'completion.json'),
              'decision': decision(summaries['qwen3_14b']['ecosystems_with_llm_specific_win'], summaries['qwen3_8b_redraw']['ecosystems_with_llm_specific_win'], cfg['decision_threshold_ecosystems']),
              'inputs_sha256': {'choices': sha(E/'choices.json'), 'completion': sha(E/'completion.json'), **{k: sha(ROOT/v) for k, v in audit.INPUTS.items()}}}
    return result

def main():
    ap = argparse.ArgumentParser(); ap.add_argument('--check', action='store_true'); args = ap.parse_args()
    text = json.dumps(run(), indent=1, sort_keys=True)+'\n'; dest = OUT/'analysis.json'
    if args.check: assert dest.read_text() == text; print(json.dumps({'reproduced': True, 'sha256': sha(dest)})); return
    OUT.mkdir(parents=True, exist_ok=True); assert not dest.exists(); dest.write_text(text); print(json.dumps({'written': str(dest.relative_to(ROOT)), 'sha256': sha(dest)}))

if __name__ == '__main__': main()
