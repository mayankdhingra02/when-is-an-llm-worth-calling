"""Independent V172 replay: separately coded parsing, projection, target re-reads, budgets and primary estimand."""
import copy, csv, json, math
from collect_smollm_v47 import ROOT, read, sha
from common_v172 import A, M, E, STAGES, FAILED_STAGES, config
from runtime_v172 import server_command
from analyze_pointwise_v123 import candidates as candidates_v141
from escalation.core import State
from escalation.transfer_v41 import rank
import spark_v145, hadoop_v148, audit_v171
ALPHABET = '0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz'  # grammar order: digits, uppercase, lowercase
SPARK_CAT = {4, 9, 16, 19, 25, 26, 27, 28, 29}
EXPECTED = {'n_predict': 1024, 'temperature': .7, 'top_p': .95, 'top_k': 0, 'min_p': 0.0, 'repeat_penalty': 1.0, 'stream': False, 'cache_prompt': False, 'return_tokens': True}

def my_parse(content, ds):
    rows = json.loads(content); assert isinstance(rows, list) and len(rows) == 10
    out = []
    for r in rows:
        assert isinstance(r, str) and len(r) == len(ds)
        out.append([d[ALPHABET.index(ch)] for ch, d in zip(r, ds)])
    return out

def my_project(origin, c, prefix, proposals):
    seen = set(prefix['ids']); ids = []
    for p in proposals:
        avail = [i for i in prefix['order'] if i not in seen]
        if origin == 'v141': dist = lambda i: sum(a != b for a, b in zip(p, c.x[i]))
        elif origin == 'v144':
            x = [v if j in SPARK_CAT else v/9 for j, v in enumerate(p)]
            dist = lambda i: sum(float(a != b) if j in SPARK_CAT else abs(a-b) for j, (a, b) in enumerate(zip(x, c['x'][i])))/30
        else:
            x = [p[0]/9, p[1]]; dist = lambda i: (abs(x[0]-c['x'][i][0])+float(x[1] != c['x'][i][1]))/2
        i = min(avail, key=dist); ids.append(i); seen.add(i)
    return ids

def my_target(j, c, spec, i):
    if j['origin'] == 'v141':
        lines = (ROOT/spec['path']).read_text().splitlines(); header = next(csv.reader([lines[0]], delimiter=spec['delimiter']))
        row = dict(zip(header, next(csv.reader([lines[c.source_ids[i]-1]], delimiter=spec['delimiter'])))); return float(row[spec['primary_objective']])
    if j['origin'] == 'v144':
        raw = next(csv.reader([(ROOT/c['source_path']).read_text().splitlines()[c['source_lines'][i]-1]]))[30]; return float(raw) if raw.strip() else None
    r = read(ROOT/c['sources'][i]); assert (r['framework'], r['workload'], r['datasize']) == ('hadoop', c['app'], 'bigdata')
    return min(float(r['elapsed_time']), 7200.) if r['completed'] is True else 7200.

def check(stages, choices, arms, models):
    errors = []; jobs = {j['qualified_key']: j for j in read(A/'jobs.json')}; scores = {}
    for stage, (arm, split) in STAGES.items():
        st = stages[stage]; runtime = st['runtime']; mk = runtime['config']['model_key']
        if runtime['model']['sha256'] != models[mk]['sha256'] or runtime['command'] != server_command(ROOT/models[mk]['path'], runtime['config']['ports'][mk]): errors.append(stage+': runtime pin/command')
        seed_field = config()['arms'][arm]['seed_field']
        for g in st['starts']:
            j = jobs[g['identity']]; p = g['payload']; pre = st['preflight'][g['identity']]
            if any(p[k] != v for k, v in EXPECTED.items()) or p['seed'] != j[seed_field] or p['prompt'] != pre['rendered']['prompt'] or j['split'] != split: errors.append(stage+': payload '+g['identity'])
        for r in st['responses']:
            j = jobs[r['qualified_key']]
            try: parsed = my_parse(r['response']['content'], j['domains']); ok = r['response'].get('stop_type') == 'eos' and r['response'].get('truncated') is False
            except Exception: parsed, ok = None, False
            scores[(arm, r['qualified_key'])] = parsed if ok else None
    for ch in choices:
        j = jobs[ch['qualified_key']]; parsed = scores.get((ch['arm'], ch['qualified_key']))
        if (parsed is not None) == ch['fallback'] or (parsed is not None and [list(x) for x in parsed] != [list(x) for x in read(M/ch['inference_stage']/'scores'/f"{ch['qualified_key'].replace('::','__')}.json")['score']]):
            errors.append('parse/fallback '+ch['arm']+' '+ch['qualified_key'])
    for name, arm in arms.items():
        j = jobs[arm['qualified_key']]; spec = None
        if j['origin'] == 'v141': spec, c = candidates_v141(j['dataset']); prefix = read(ROOT/j['prefix'])['state']
        else: c = read(ROOT/('artifacts/study_v144' if j['origin'] == 'v144' else 'artifacts/study_v148')/'candidates'/f"{j['app']}.json"); prefix = read(ROOT/j['prefix'])
        s = arm.get('state')
        if s is None: errors.append('unscorable '+name); continue
        ids, labels = s['ids'], s['labels']
        if ids[:10] != prefix['ids'] or labels[:10] != prefix['labels'] or len(ids) != 20 or len(set(ids)) != 20: errors.append('budget/prefix '+name)
        parsed = scores.get((arm['arm'], arm['qualified_key']))
        if parsed is not None: expect = my_project(j['origin'], c, prefix, parsed)
        elif j['origin'] == 'v141': expect = rank(c, State(**prefix), prefix['order'])[:10]
        else:
            t = copy.deepcopy(prefix); expect = []
            for k in range(10):
                i = (spark_v145.choose if j['origin'] == 'v144' else hadoop_v148.choose)(c, t, 'sequential_3nn'); t['ids'].append(i); t['labels'].append(labels[10+k]); expect.append(i)
        if ids[10:] != expect or arm['selected_rows'] != (expect if (parsed is not None or j['origin'] == 'v141') else []): errors.append('selection '+name)
        values = [my_target(j, c, spec, i) for i in ids[10:]]
        if [y[0] for y in labels[10:]] != values: errors.append('targets '+name)
        valid = [y[0] for y in labels if y[0] is not None]; d = arm['direction']
        if arm['target'] != (min(valid) if d == 'minimize' else max(valid)): errors.append('incumbent '+name)
    return errors

def primary(arms):
    base = {}
    for c in audit_v171.recorded_cases(): base[c['key']] = c
    out = {}
    for arm in ['qwen3_14b', 'qwen3_8b_redraw']:
        wins = set()
        for a in arms.values():
            if a['arm'] != arm or a.get('target') is None: continue
            c = base[a['qualified_key']]; sgn = 1 if c['direction'] == 'minimize' else -1
            rel = lambda ref: sgn*(ref-a['target'])/ref
            if all(rel(c['raw'][k]) > .01 for k in ['sequential_3nn', 'random_full', 'adaptive_neighbor', 'gp_ei']): wins.add(c['ecosystem'])
        out[arm] = len(wins)
    return out

def load():
    stages = {}
    for s in STAGES:
        d = M/s; lines = lambda n: [json.loads(x) for x in (d/n).read_text().splitlines()] if (d/n).exists() else []
        stages[s] = {'runtime': read(d/'runtime.json'), 'starts': [g for g in lines('generation_starts.jsonl') if g['kind'] == 'scientific'], 'responses': lines('responses.jsonl'),
                     'preflight': {read(p)['qualified_key']: read(p) for p in (d/'preflight').glob('*.json')}}
    return stages, read(E/'choices.json'), {p.stem: read(p) for p in (E/'arms').glob('*.json')}, read(A/'models.json')

def main():
    stages, choices, arms, models = load(); errors = check(stages, choices, arms, models); counts = primary(arms); analysis = read(ROOT/'results/v172_analysis/analysis.json')
    for arm, n in counts.items():
        if analysis['summaries'][arm]['ecosystems_with_llm_specific_win'] != n: errors.append('primary estimand '+arm)
    for s in FAILED_STAGES:
        led = read(M/s/'ledger.json'); resp = (M/s/'responses.jsonl').read_text()
        if led['generation_requests'] or led['allocated_output_tokens'] or resp.strip() or (M/s/'scores').exists(): errors.append('failed stage has outputs '+s)
    charged = sum(10 for a in arms.values() if a.get('state')); ledger = read(E/'ledger.json')['acquisitions']
    if charged != ledger: errors.append(f'charges {charged} vs ledger {ledger}')
    mutations = {}
    for name, mutate in [('target_value', lambda a: a['state']['labels'].__setitem__(12, [a['state']['labels'][12][0]*1.5])),
                         ('selected_row', lambda a: a['state']['ids'].__setitem__(11, a['state']['ids'][12])),
                         ('incumbent', lambda a: a.__setitem__('target', a['target']*.5))]:
        key = sorted(k for k, a in arms.items() if a.get('state'))[0]; bad = copy.deepcopy(arms); mutate(bad[key])
        mutations[name] = bool(check(stages, choices, {key: bad[key]}, models))
    bad = copy.deepcopy(stages); r = next(x for s in bad.values() for x in s['responses'] if x['response'].get('content')); r['response']['content'] = r['response']['content'][::-1]
    mutations['response_content'] = bool(check(bad, choices, {}, models))
    result = {'errors': errors, 'primary_recomputed': counts, 'charges': charged, 'arms_checked': len(arms), 'mutations_rejected': mutations, 'passed': not errors and all(mutations.values())}
    (ROOT/'artifacts/study_v172/replay.json').write_text(json.dumps(result, indent=1)+'\n'); print(json.dumps(result, indent=1))
    if not result['passed']: raise SystemExit(1)

if __name__ == '__main__': main()
