"""Independent V173 replay: request settings, provider pinning, parsing, projections, fallbacks, prompt leakage, targets, spend and primary estimand."""
import copy, json
from collect_smollm_v47 import ROOT, read
from verify_v172 import my_project, my_target, ALPHABET
from analyze_pointwise_v123 import candidates as candidates_v141
from escalation.core import State
from escalation.transfer_v41 import rank
import spark_v145, hadoop_v148, audit_v171
M = ROOT/'results/v173_models'; E = ROOT/'results/v173_eval'
CFG = read(ROOT/'configs/study_v173.json'); JOBS = {j['qualified_key']: j for j in read(ROOT/'artifacts/study_v172/jobs.json')}

def lines(p): return [json.loads(x) for x in p.read_text().splitlines()] if p.exists() else []
def my_parse(content, ds, n):
    obj = json.loads(content); rows = obj['proposals'] if isinstance(obj, dict) else obj
    assert isinstance(rows, list) and len(rows) == n and all(isinstance(r, str) and len(r) == len(ds) for r in rows)
    return [[d[ALPHABET.index(ch)] for ch, d in zip(r, ds)] for r in rows]
def content(resp):
    ch = resp['choices']; assert len(ch) == 1 and ch[0]['finish_reason'] == 'stop'; return ch[0]['message']['content']
def load_case(j):
    if j['origin'] == 'v141': spec, c = candidates_v141(j['dataset']); return spec, c, read(ROOT/j['prefix'])['state'], 'minimize' if spec['direction'] == '-' else 'maximize'
    c = read(ROOT/('artifacts/study_v144' if j['origin'] == 'v144' else 'artifacts/study_v148')/'candidates'/f"{j['app']}.json"); return None, c, read(ROOT/j['prefix']), 'minimize'
def fallback_next(j, c, ids, labels, order, k):
    if j['origin'] == 'v141': return rank(c, State(order=order, ids=list(ids), labels=[list(y) for y in labels]), order)[:k]
    t = {'ids': list(ids), 'labels': [list(y) for y in labels], 'order': order}; return [(spark_v145.choose if j['origin'] == 'v144' else hadoop_v148.choose)(c, t, 'sequential_3nn')]

def check_request(body, provider, top_p, count, j, seed=None, messages=None, arm='A'):
    s = body['response_format']['json_schema']['schema']; items = s['properties']['proposals']
    ok = (body['model'] == CFG['model'] and body['provider'] == {'order': [provider], 'allow_fallbacks': False, 'require_parameters': True} and body['temperature'] == CFG['temperature']
          and body['top_p'] == top_p and body['max_tokens'] == CFG['max_tokens'][arm] and body['reasoning'] == {'effort': CFG['reasoning_effort']} and items['minItems'] == items['maxItems'] == count
          and items['items']['pattern'] == '^'+''.join('['+ALPHABET[:len(d)]+']' for d in j['domains'])+'$' and body['stream'] is False)
    if seed is not None: ok = ok and body['seed'] == seed
    if messages is not None: ok = ok and body['messages'] == messages
    return ok

def check(arms_a, arms_b, stages):
    errors = []; provider = read(M/'P2'/'summary.json')['provider']
    for s in [x for x in stages if x.partition('.')[0] in ('A1R', 'A2')]:
        req = {r['identity']: r for r in stages[s]['requests']}; field = CFG['arm_a_draws'][s.partition('.')[0]]
        final = {r['identity']: r for r in stages[s]['responses']}  # last attempt per logical request (earlier ones are HTTP 429)
        if any(r['http_status'] != 429 for r in stages[s]['responses'] if r is not final[r['identity']]): errors.append(f'{s} non-429 superseded attempt')
        for r in final.values():
            j = JOBS[r['identity']]
            if not check_request(req[r['identity']]['body'], provider, CFG['top_p']['A'], 10, j, j[field], read(ROOT/j['messages_path'])): errors.append(f'{s} request {r["identity"]}')
            if r['response'] is not None and str(r['response'].get('provider')).lower().replace(' ', '') != provider.split('/')[0]: errors.append(f'{s} provider {r["identity"]}')
            try: parsed = my_parse(content(r['response']), j['domains'], 10)
            except Exception: parsed = None
            sc = read(M/s/'scores'/f"{r['identity'].replace('::', '__')}.json")
            if (parsed is None) != (sc['status'] != 'valid') or (parsed is not None and parsed != sc['score']): errors.append(f'{s} parse {r["identity"]}')
    for name, a in arms_a.items():
        j = JOBS[a['qualified_key']]; spec, c, prefix, d = load_case(j); s = a.get('state')
        if s is None: errors.append('unscorable '+name); continue
        ids, labels = s['ids'], s['labels']
        if ids[:10] != prefix['ids'] or labels[:10] != prefix['labels'] or len(set(ids)) != 20: errors.append('budget '+name)
        sc = read(M/a['inference_stage']/'scores'/f"{a['qualified_key'].replace('::', '__')}.json") if (M/a['inference_stage']/'scores'/f"{a['qualified_key'].replace('::', '__')}.json").exists() else {'status': 'unattempted'}
        if sc['status'] == 'valid': expect = my_project(j['origin'], c, prefix, sc['score'])
        elif j['origin'] == 'v141': expect = fallback_next(j, c, prefix['ids'], prefix['labels'], prefix['order'], 10)
        else:
            expect = []
            for k in range(10): expect += fallback_next(j, c, ids[:10+k], labels[:10+k], prefix['order'], 1)
        if ids[10:] != expect: errors.append('selection '+name)
        if [y[0] for y in labels[10:]] != [my_target(j, c, spec, i) for i in ids[10:]]: errors.append('targets '+name)
    bst = [x for x in stages if x.startswith('B')]
    breq = {r['identity']: r for s in bst for r in stages[s]['requests']}; bresp = {r['identity']: r for s in bst for r in stages[s]['responses']}
    rounds = {}; pending = {}
    for s in bst:
        for r in lines(M/s/'rounds.jsonl'):
            rounds.setdefault(r['case'], []).append(r)
            if r['kind'] == 'fallback_pending': pending[(r['case'], r['round'])] = r['attempts']
    for name, a in arms_b.items():
        j = JOBS[a['qualified_key']]; spec, c, prefix, d = load_case(j); ids, labels = a['state']['ids'], a['state']['labels']
        if ids[:10] != prefix['ids'] or labels[:10] != prefix['labels'] or len(set(ids)) != 20: errors.append('B budget '+name); continue
        if [y[0] for y in labels[10:]] != [my_target(j, c, spec, i) for i in ids[10:]]: errors.append('B targets '+name)
        pos = 10; done = [r for r in rounds.get(j['qualified_key'], []) if r['kind'] in ('model', 'fallback')] if a['stage'] != 'EB' else []
        for r in done:
            for att in (r['attempts'] if r['kind'] == 'model' else pending.get((j['qualified_key'], r['round']), [])):
                ident = f"{j['qualified_key']}::r{r['round']}::a{att['attempt']}"; body = breq[ident]['body']
                if not check_request(body, provider, CFG['top_p']['B'], 2, j, j['sampling_seed']+CFG['arm_b']['seed_offset']+10*r['round']+att['attempt'], arm='B'): errors.append('B request '+ident)
                block = json.loads(body['messages'][2]['content']); shown = sorted(str(x['performance']) for x in block['trajectory_worst_to_best'] if x['performance'] is not None)
                have = sorted((f'{y[0]:.6f}' if j['origin'] == 'v141' else str(y[0])) for y in labels[:pos] if y[0] is not None)
                if shown != have or len(block['trajectory_worst_to_best']) != pos: errors.append('B leakage/trajectory '+ident)
            if r['kind'] == 'model':
                last = r['attempts'][-1]; ident = f"{j['qualified_key']}::r{r['round']}::a{last['attempt']}"
                expect = my_project(j['origin'], c, {'ids': ids[:pos], 'order': prefix['order']}, my_parse(content(bresp[ident]['response']), j['domains'], 2))
            elif j['origin'] == 'v141': expect = fallback_next(j, c, ids[:pos], labels[:pos], prefix['order'], 2)
            else: expect = fallback_next(j, c, ids[:pos], labels[:pos], prefix['order'], 1)+fallback_next(j, c, ids[:pos+1], labels[:pos+1], prefix['order'], 1)
            if ids[pos:pos+2] != expect or r['selected_rows'] != expect: errors.append(f"B selection {name} r{r['round']}")
            pos += 2
        if a['stage'] == 'EB':
            for k in range(5):
                expect = fallback_next(j, c, ids[:10+2*k], labels[:10+2*k], prefix['order'], 2) if j['origin'] == 'v141' else fallback_next(j, c, ids[:10+2*k], labels[:10+2*k], prefix['order'], 1)+fallback_next(j, c, ids[:11+2*k], labels[:11+2*k], prefix['order'], 1)
                if ids[10+2*k:12+2*k] != expect: errors.append('EB selection '+name)
        elif pos != 20: errors.append('B rounds incomplete '+name)
    return errors

def primary(arms):
    base = {c['key']: c for c in audit_v171.recorded_cases()}; wins = set()
    for a in arms.values():
        c = base[a['qualified_key']]; sgn = 1 if c['direction'] == 'minimize' else -1
        if a.get('target') is not None and all(sgn*(c['raw'][k]-a['target'])/c['raw'][k] > .01 for k in ['sequential_3nn', 'random_full', 'adaptive_neighbor', 'gp_ei']): wins.add(c['ecosystem'])
    return len(wins)

def main():
    from analyze_v173 import stage_dirs
    stages = {s: {'requests': lines(M/s/'requests.jsonl'), 'responses': lines(M/s/'responses.jsonl')} for s in stage_dirs()}
    arms_a = {p.stem: read(p) for p in (E/'arms').glob('*.json')}; arms_b = {p.stem: read(p) for p in sorted(M.glob('B*/arms/*.json'))+sorted((M/'EB').glob('arms/*.json'))}
    errors = check(arms_a, arms_b, stages); analysis = read(ROOT/'results/v173_analysis/analysis.json')
    counts = {'gptoss_a1': primary({k: v for k, v in arms_a.items() if v['arm'] == 'gptoss_a1'}), 'gptoss_a2': primary({k: v for k, v in arms_a.items() if v['arm'] == 'gptoss_a2'}), 'gptoss_b': primary(arms_b)}
    for k, n in counts.items():
        if analysis['summaries'][k]['ecosystems_with_llm_specific_win'] != n: errors.append('primary '+k)
    spend = read(M/'spend_ledger.json'); nreq = sum(len(s['responses']) for s in stages.values())  # the one A1 request killed in flight has no response and unknown cost; reported separately
    if spend['requests'] != nreq or spend['spent_usd'] > CFG['spend_cap_usd']: errors.append('spend ledger')
    mut = {}
    if arms_b:
        k = sorted(arms_b)[0]; bad = copy.deepcopy(arms_b[k]); bad['state']['labels'][11] = [bad['state']['labels'][11][0]*1.5]; mut['B_target'] = bool(check({}, {k: bad}, stages))
        bs = copy.deepcopy(stages); tgt = next((r for s in bs if s.startswith('B') for r in bs[s]['requests'] if r['identity'].endswith('::r2::a0')), None)
        if tgt is not None:
            blk = json.loads(tgt['body']['messages'][2]['content']); blk['trajectory_worst_to_best'].append({'settings': 'x', 'performance': 0.123456}); tgt['body']['messages'][2]['content'] = json.dumps(blk)
            case = tgt['identity'].split('::r2::')[0]; mut['B_leakage'] = bool(check({}, {n: a for n, a in arms_b.items() if a['qualified_key'] == case}, bs))
    if arms_a:
        k = sorted(arms_a)[0]; bad = copy.deepcopy(arms_a[k]); bad['state']['ids'][11] = bad['state']['ids'][12]; mut['A_selection'] = bool(check({k: bad}, {}, stages))
    res = {'errors': errors, 'primary_recomputed': counts, 'requests': nreq, 'spent_usd': spend['spent_usd'], 'arms_a': len(arms_a), 'arms_b': len(arms_b), 'mutations_rejected': mut,
           'passed': not errors and all(mut.values()) and len(mut) == 3}
    (ROOT/'artifacts/study_v173/replay.json').write_text(json.dumps(res, indent=1)+'\n'); print(json.dumps(res, indent=1))
    if not res['passed']: raise SystemExit(1)

if __name__ == '__main__': main()
