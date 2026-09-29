"""V173 frozen analysis: LLM-specific headroom for gpt-oss-120b (arm A draws, arm B loop) beside historical and V172 arms."""
import argparse, json
from collect_smollm_v47 import ROOT, read, sha
from analyze_v172 import summarize
import audit_v171 as audit
M = ROOT/'results/v173_models'; E = ROOT/'results/v173_eval'; OUT = ROOT/'results/v173_analysis'
ARMS = ['smollm3_3b', 'qwen3_8b', 'qwen3_8b_redraw', 'qwen3_14b', 'gptoss_a1', 'gptoss_a2', 'gptoss_b']

def decision(a1, b, threshold=2):
    return 'headroom_at_snap2_model_router_question_needs_fresh_cohort' if max(a1, b) >= threshold else 'boundary_extends_to_snap2_model_on_this_cohort'

def targets():
    t = {a: {} for a in ARMS[2:]}
    for p in (ROOT/'results/v172_eval/arms').glob('*.json'): r = read(p); t[r['arm']][r['qualified_key']] = r['target']
    for p in (E/'arms').glob('*.json'): r = read(p); t[r['arm']][r['qualified_key']] = r['target']
    for p in sorted(M.glob('B*/arms/*.json'))+sorted((M/'EB').glob('arms/*.json')): r = read(p); t['gptoss_b'][r['qualified_key']] = r['target']
    return t

def stage_dirs():
    base = ['P', 'A1', 'P2', 'A1R', 'A2']+[f'B{i}' for i in range(1, 9)]
    return [x for b in base for x in [b]+[f'{b}.c{i}' for i in range(1, 4)] if (M/x).is_dir()]

def usage_rows(stage):
    p = M/stage/'responses.jsonl'
    return [json.loads(l) for l in p.read_text().splitlines()] if p.exists() else []

def reliability():
    out = {}
    for s in stage_dirs():
        rows = usage_rows(s); us = [(r.get('response') or {}).get('usage') or {} for r in rows]
        rt = [((u.get('completion_tokens_details') or {}).get('reasoning_tokens')) for u in us]
        out[s] = {'requests': len(rows), 'http_errors': sum(r['http_status'] != 200 for r in rows), 'rate_limited_429': sum(r['http_status'] == 429 for r in rows), 'served_by': sorted({str((r.get('response') or {}).get('provider')) for r in rows}),
                  'prompt_tokens': sum(u.get('prompt_tokens') or 0 for u in us), 'completion_tokens': sum(u.get('completion_tokens') or 0 for u in us),
                  'reasoning_tokens': sum(x or 0 for x in rt), 'responses_without_usage': sum(not u for u in us),
                  'reported_cost_usd': sum(r['reported_cost_usd'] or 0 for r in rows), 'request_seconds': sum(r['seconds'] for r in rows)}
        if (M/s/'summary.json').exists(): out[s]['summary'] = {k: v for k, v in read(M/s/'summary.json').items() if k not in ['spend', 'attempts']}
    b = [read(p) for p in sorted(M.glob('B*/arms/*.json'))+sorted((M/'EB').glob('arms/*.json'))]
    out['arm_b'] = {'cases': len(b), 'model_rounds': sum(sum(x['kind'] == 'model' for x in r['rounds']) for r in b), 'fallback_rounds': sum(r['fallback_rounds'] for r in b),
                    'rounds_needing_retry': sum(sum(x['attempts'] > 1 for x in r['rounds']) for r in b), 'collisions': sum(len(r['collisions']) for r in b),
                    'cases_rebuilt_in_EB': sum(r['stage'] == 'EB' for r in b), 'missing_acquisitions': sum(r['missing_acquisitions'] for r in b)}
    ch = read(E/'choices.json')
    for arm in ['gptoss_a1', 'gptoss_a2']:
        c = [x for x in ch if x['arm'] == arm]; dg = [d for x in c for d in x['projection']]
        out[arm+'_selection'] = {'arms': len(c), 'fallbacks': sum(x['fallback'] for x in c), 'projected': len(dg),
                                 'nonzero_projection': sum((d.get('hamming_distance', d.get('distance')) or 0) > 0 for d in dg), 'repeated': sum(d['repeated_proposal'] for d in dg)}
    out['spend_ledger'] = read(M/'spend_ledger.json')
    return out

def run():
    cfg = read(ROOT/'configs/study_v173.json'); margin = cfg['margin']; base = {}
    for c in audit.recorded_cases():
        b = base.setdefault(c['key'], {k: c[k] for k in ['key', 'engine', 'ecosystem', 'direction']} | {'raw': {k: v for k, v in c['raw'].items() if k != 'llm'}, 'historical': {}})
        b['historical'][c['model']] = c['raw']['llm']
    t = targets(); assert len(base) == 70
    def cases(arm): return [{**c, 'raw': {**c['raw'], 'llm': c['historical'][arm] if arm in c['historical'] else t[arm].get(k)}} for k, c in base.items()]
    summaries = {a: summarize(cases(a), margin) for a in ARMS}
    def paired(a, b):
        r = []
        for k, c in base.items():
            x = c['historical'].get(a, t.get(a, {}).get(k)); y = c['historical'].get(b, t.get(b, {}).get(k))
            if x is not None and y is not None: r.append(audit.relative_gain(x, y, c['direction']))
        return {'reference': a, 'treatment': b, 'pairs': len(r), 'treatment_better_by_margin': sum(v > margin for v in r), 'treatment_worse_by_margin': sum(v < -margin for v in r),
                'identical': sum(abs(v) < 1e-12 for v in r), 'mean_relative_gain': sum(r)/len(r) if r else None}
    return {'status': 'V173 frozen analysis; exposed recorded tasks, new hosted gpt-oss-120b draws', 'margin': margin, 'summaries': summaries,
            'decision': decision(summaries['gptoss_a1']['ecosystems_with_llm_specific_win'], summaries['gptoss_b']['ecosystems_with_llm_specific_win'], cfg['decision_threshold_ecosystems']),
            'paired': [paired(a, b) for a, b in [('qwen3_8b', 'gptoss_a1'), ('qwen3_14b', 'gptoss_a1'), ('gptoss_a1', 'gptoss_a2'), ('gptoss_a1', 'gptoss_b'), ('qwen3_14b', 'gptoss_b')]],
            'reliability': reliability(), 'evaluation_a': read(E/'completion.json')}

def main():
    ap = argparse.ArgumentParser(); ap.add_argument('--check', action='store_true'); a = ap.parse_args(); text = json.dumps(run(), indent=1, sort_keys=True)+'\n'; dest = OUT/'analysis.json'
    if a.check: assert dest.read_text() == text; print(json.dumps({'reproduced': True, 'sha256': sha(dest)})); return
    OUT.mkdir(parents=True, exist_ok=True); assert not dest.exists(); dest.write_text(text); print(json.dumps({'written': str(dest.relative_to(ROOT)), 'sha256': sha(dest)}))

if __name__ == '__main__': main()
