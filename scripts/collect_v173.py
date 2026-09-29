"""V173 create-once stages: P (preflight), A1/A2 (arm A draws), E (arm A evaluation), B1-B4 (arm B loop), EB (arm B fallback completion)."""
import argparse, copy, json, math, time, urllib.request
from collect_smollm_v47 import ROOT, read, write, append, sha, now
from openrouter_v173 import Client, Refused, content_of, load_key, check_authorization, NoRedirect
from interface_v173 import schema, parse, project_any, b_messages
from proposal_v127 import ALPHABET
from analyze_pointwise_v123 import candidates as candidates_v141
from escalation.core import State
from escalation.transfer_v41 import IndexedOracle, rank
import evaluate_v172 as ev172, spark_v145, hadoop_v148
A = ROOT/'artifacts/study_v173'; M = ROOT/'results/v173_models'; E = ROOT/'results/v173_eval'
JOBS = ROOT/'artifacts/study_v172/jobs.json'; SPEND = M/'spend_ledger.json'
BASE = ['P', 'A1', 'P2', 'A1R', 'A2', 'E', 'B1', 'B2', 'B3', 'B4', 'B5', 'B6', 'B7', 'B8', 'EB']  # amendment 1: A1 failed (kept), P2 probe, A1R; amendment 2: B1-B8
MAX_CONT = 3  # amendment 2: continuation stages X.c1..X.c3 run only a wall-capped stage's not-yet-started cases
ORDER = BASE
def chain(base): return [base]+[f'{base}.c{i}' for i in range(1, MAX_CONT+1)]
def chain_done(base):
    ended = [x for x in chain(base) if (M/x/'summary.json').exists()]
    if not ended: return False
    last = read(M/ended[-1]/'summary.json'); left = last.get('unattempted', last.get('not_started_cases', []))
    return not left or ended[-1] == chain(base)[-1]

def config(): return read(ROOT/'configs/study_v173.json')
def freeze_names(): return ['freeze.json']+sorted((p.name for p in A.glob('freeze_amendment*.json')), key=lambda n: int(n[16:-5]))
def verify_freeze():
    merged = {}
    for n in freeze_names(): merged.update(read(A/n)['sha256'])
    for n, h in merged.items():
        if sha(ROOT/n) != h: raise ValueError('Changed frozen input: '+n)
    return merged
def require_previous(stage):
    base, _, c = stage.partition('.')
    if c:
        prev = base if c == 'c1' else f'{base}.c{int(c[1:])-1}'
        if not (M/prev/'summary.json').exists(): raise RuntimeError('Previous chain stage not ended: '+prev)
        return
    for s in BASE[:BASE.index(base)]:
        if s == 'E':
            if not (E/'completion.json').exists(): raise RuntimeError('Previous stage not ended: E')
        elif s in ('A1R', 'A2') or s.startswith('B') and s != 'B':
            if not chain_done(s): raise RuntimeError('Previous stage chain not ended: '+s)
        elif not (M/s/'summary.json').exists(): raise RuntimeError('Previous stage not ended: '+s)
def provider():
    s = read(M/('P2' if (M/'P2'/'summary.json').exists() else 'P')/'summary.json')
    if not s.get('passed'): raise RuntimeError('Preflight did not pass')
    return s['provider']
def key_name(j): return j['qualified_key'].replace('::', '__')

def b_cases(cfg, stage):
    base, _, c = stage.partition('.')
    if c:
        prev = base if c == 'c1' else f'{base}.c{int(c[1:])-1}'; left = set(read(M/prev/'summary.json')['not_started_cases'])
        return [j for j in b_cases(cfg, base) if j['qualified_key'] in left]
    split, part = cfg['arm_b']['stages'][base]; n = cfg['arm_b']['parts_per_split']; js = [j for j in read(JOBS) if j['split'] == split]; k = math.ceil(len(js)/n)
    return js[part*k:(part+1)*k]

def preflight(cfg):
    out = M/'P'; out.mkdir(parents=True, exist_ok=False); check_authorization(cfg); key = load_key(cfg); info = {}
    try:
        op = urllib.request.build_opener(urllib.request.ProxyHandler({}), NoRedirect())
        with op.open(urllib.request.Request('https://openrouter.ai/api/v1/key', headers={'Authorization': 'Bearer '+key}), timeout=30) as r: d = json.loads(r.read()).get('data', {})
        info = {k: d.get(k) for k in ['limit', 'limit_remaining', 'usage', 'is_free_tier']}
    except Exception as e: info = {'error': repr(e)}
    listing = {e['tag']: e for e in read(A/'openrouter_endpoints_snapshot.json')['data']['endpoints']}
    ds = [[0, 1, 2], [0, 1]]; msgs = [{'role': 'system', 'content': 'Synthetic compatibility check; not a research case. Respond only with a JSON object {"proposals": [...]}.'},
                                      {'role': 'user', 'content': 'Return exactly two strings of two symbols: first symbol 0, 1 or 2; second symbol 0 or 1.'}]
    attempts = []; chosen = None; deadline = time.monotonic()+cfg['stage_seconds']['P']
    for tag in cfg['provider_preference']:
        if len(attempts) >= cfg['request_caps']['P']: break
        sp = set(listing.get(tag, {}).get('supported_parameters', []))
        if not {'structured_outputs', 'response_format', 'seed', 'reasoning', 'top_p', 'max_tokens'} <= sp: attempts.append({'provider': tag, 'skipped': 'listing lacks required parameters'}); continue
        client = Client(cfg, out, 'P', tag, cfg['request_caps']['P']-len([a for a in attempts if 'http_status' in a]), SPEND)
        try:
            status, resp, err = client.send(client.body(msgs, schema(ds, 2), 1.0, 173999, cfg['max_tokens']['B']), 'synthetic_compatibility::'+tag, deadline)
            try: content, _ = content_of(resp); parsed = parse(content, ds, 2); ok = True; why = None
            except ValueError as e: parsed = None; ok = False; why = str(e) or err
        except Refused as e: status, resp, parsed, ok, why = None, None, None, False, 'refused: '+str(e)
        attempts.append({'provider': tag, 'http_status': status, 'ok': ok, 'reason': why or err, 'served_by': (resp or {}).get('provider'), 'usage': (resp or {}).get('usage'), 'parsed': parsed})
        if ok: chosen = tag; break
    s = {'at': now(), 'key_info': info, 'attempts': attempts, 'provider': chosen, 'passed': chosen is not None, 'spend': read(SPEND) if SPEND.exists() else None, 'synthetic_not_research': True}
    write(out/'summary.json', s); print(json.dumps({k: v for k, v in s.items() if k != 'attempts'}, indent=1)); print(attempts)
    if not s['passed']: raise SystemExit('Preflight failed; no scientific stage may start')

def probe(cfg):
    """Amendment 1 P2: choose the provider by the pre-declared cost-ordered probe rule (synthetic task, not research data)."""
    import random
    out = M/'P2'; out.mkdir(parents=True, exist_ok=False); pr = cfg['probe']; rng = random.Random(pr['seed']); ds = [list(range(10)) for _ in range(pr['features'])]
    obs = [{'settings': ''.join(str(rng.randrange(10)) for _ in ds), 'performance': round(rng.uniform(10, 100), 3)} for _ in range(10)]
    msgs = [{'role': 'system', 'content': 'Synthetic provider probe; not a research case. Propose ten diverse promising settings as JSON {"proposals": [...]} of 30-digit strings; lower performance is better.'},
            {'role': 'user', 'content': json.dumps({'feature_count': pr['features'], 'observed_examples': obs}, separators=(',', ':'))}]
    listing = {e['tag']: e for e in read(A/'openrouter_endpoints_snapshot.json')['data']['endpoints']}; attempts = []; chosen = None; deadline = time.monotonic()+cfg['stage_seconds']['P2']
    for tag in pr['order'][:pr['max_probes']]:
        sp = set(listing.get(tag, {}).get('supported_parameters', []))
        if not {'structured_outputs', 'response_format', 'seed', 'reasoning', 'top_p', 'max_tokens'} <= sp: attempts.append({'provider': tag, 'skipped': 'listing lacks required parameters'}); continue
        client = Client(cfg, out, 'P2', tag, 1, SPEND); t = time.monotonic()
        try:
            status, resp, err = client.send(client.body(msgs, schema(ds, pr['proposals']), 1.0, pr['seed'], cfg['max_tokens']['A']), 'provider_probe::'+tag, deadline)
            secs = time.monotonic()-t; u = (resp or {}).get('usage') or {}
            try: content, _ = content_of(resp); parse(content, ds, pr['proposals']); ok = True; why = None
            except ValueError as e: ok = False; why = str(e) if resp is not None else (err or str(e))
            last = [json.loads(l) for l in (out/'responses.jsonl').read_text().splitlines()][-1]
            tps = (u.get('completion_tokens') or 0)/last['seconds'] if last['seconds'] > 0 else 0.
        except Refused as e: status, ok, why, tps, u = None, False, 'refused: '+str(e), 0., {}
        attempts.append({'provider': tag, 'http_status': status, 'ok': ok, 'reason': why, 'completion_tokens': u.get('completion_tokens'), 'completion_tokens_per_second': tps, 'cost': u.get('cost')})
        print(attempts[-1], flush=True)
        if ok and tps >= pr['min_completion_tokens_per_second']: chosen = tag; break
    s = {'at': now(), 'rule': pr['rule'], 'attempts': attempts, 'provider': chosen, 'passed': chosen is not None, 'spend': read(SPEND), 'synthetic_not_research': True}
    write(out/'summary.json', s); print({k: v for k, v in s.items() if k != 'attempts'})
    if not s['passed']: raise SystemExit('No provider met the pre-declared probe rule; no scientific stage may start')

def close_failed_a1():
    """Amendment 1: reconstruct the summary of the A1 stage stopped by the operator (truncation and HTTP 429 at the 4,000-token cap)."""
    out = M/'A1'; assert not (out/'summary.json').exists(); rs = [json.loads(l) for l in (out/'responses.jsonl').read_text().splitlines()]; rq = [json.loads(l) for l in (out/'requests.jsonl').read_text().splitlines()]
    write(out/'summary.json', {'at': now(), 'stage': 'A1', 'reconstructed_after_operator_stop': True, 'requests_sent': len(rq), 'responses_recorded': len(rs),
          'http_status_counts': {str(k): sum(r['http_status'] == k for r in rs) for k in sorted({r['http_status'] for r in rs}, key=str)},
          'finish_reasons_200': [(((r.get('response') or {}).get('choices') or [{}])[0]).get('finish_reason') for r in rs if r['http_status'] == 200],
          'in_flight_without_response': [x['identity'] for x in rq[len(rs):]], 'superseded_by': 'A1R (amendment 1)', 'targets_read': 0, 'spend': read(SPEND)})
    print(read(out/'summary.json'))

def arm_a(cfg, stage):
    base, _, c = stage.partition('.'); tag = provider(); out = M/stage; out.mkdir(parents=True, exist_ok=False); jobs = read(JOBS); field = cfg['arm_a_draws'][base]
    if c:
        prev = base if c == 'c1' else f'{base}.c{int(c[1:])-1}'; left = set(read(M/prev/'summary.json')['unattempted']); jobs = [j for j in jobs if j['qualified_key'] in left]
    client = Client(cfg, out, stage, tag, len(jobs) if c else cfg['request_caps'][base], SPEND); deadline = time.monotonic()+cfg['stage_seconds'][base]; error = None; t = time.monotonic()
    try:
        for j in jobs:
            msgs = read(ROOT/j['messages_path'])
            status, resp, err = client.send(client.body(msgs, schema(j['domains'], 10), cfg['top_p']['A'], j[field], cfg['max_tokens']['A']), j['qualified_key'], deadline)
            try: content, _ = content_of(resp); sc = parse(content, j['domains'], 10); st = 'valid'; why = None
            except ValueError as e: sc = None; st = 'invalid'; why = str(e) if resp is not None else (err or str(e))
            write(out/'scores'/f'{key_name(j)}.json', {**j, 'stage': stage, 'seed_used': j[field], 'status': st, 'score': sc, 'error': why, 'served_by': (resp or {}).get('provider'), 'usage': (resp or {}).get('usage')})
            print(stage, j['qualified_key'], st, flush=True)
    except Refused as e: error = 'refused: '+str(e)
    except Exception as e: error = repr(e)
    sc = [read(p) for p in (out/'scores').glob('*.json')] if (out/'scores').exists() else []
    write(out/'summary.json', {'at': now(), 'stage': stage, 'provider': tag, 'intended': len(jobs), 'requests': client.requests, 'responses_scored': len(sc), 'valid': sum(x['status'] == 'valid' for x in sc),
          'invalid': sum(x['status'] == 'invalid' for x in sc), 'unattempted': [j['qualified_key'] for j in jobs if j['qualified_key'] not in {x['qualified_key'] for x in sc}], 'error': error,
          'seconds': time.monotonic()-t, 'spend': read(SPEND)})
    print(read(out/'summary.json'))

def evaluate_a(cfg):
    for s in ['A1R', 'A2']:
        if not chain_done(s): raise RuntimeError('Arm A stage chain not ended: '+s)
    E.mkdir(parents=True, exist_ok=False); choices = []
    for s in ['A1R', 'A2']:
        for j in read(JOBS):
            found = [x for x in chain(s) if (M/x/'scores'/f'{key_name(j)}.json').exists()]; st = found[0] if found else s
            score = read(M/st/'scores'/f'{key_name(j)}.json') if found else {'status': 'unattempted', 'score': None}
            ids, diag, fb = ev172.select(j, score); choices.append({**j, 'arm': {'A1R': 'gptoss_a1', 'A2': 'gptoss_a2'}[s], 'inference_stage': st, 'model_status': score['status'], 'fallback': fb is not None, 'fallback_kind': fb, 'selected_rows': ids, 'projection': diag})
    write(E/'choices.json', choices); write(E/'selection_seal.json', {'at': now(), 'choices_sha256': sha(E/'choices.json')})
    ledger = ev172.Ledger(E/'ledger.json', E/'acquisitions.jsonl', cfg['acquisition_caps']['E'], cfg['stage_seconds']['E']); (E/'acquisitions.jsonl').touch(); done = []; failures = []
    for ch in choices:
        name = ch['arm']+'__'+key_name(ch)
        try: write(E/'arms'/f'{name}.json', {**ch, **ev172.acquire(ch, ledger)}); done.append(name)
        except (PermissionError, TimeoutError) as e: failures.append({'arm': name, 'error': repr(e)}); break
        except Exception as e: failures.append({'arm': name, 'error': repr(e)}); write(E/'arms'/f'{name}.json', {**ch, 'target': None, 'status': 'unscorable', 'error': repr(e)})
    write(E/'completion.json', {'at': now(), 'intended_arms': len(choices), 'scored_arms': len(done), 'failures': failures, 'acquisitions': ledger.state['acquisitions'], 'complete': len(done) == len(choices) and not failures})
    print(read(E/'completion.json'))

class Case:
    """Per-case arm-B state with the origin stage's oracle and fallback; only acquired labels are exposed."""
    def __init__(self, j, ledger):
        self.j, self.origin, self.ds, self.key = j, j['origin'], j['domains'], 'gptoss_b::'+j['qualified_key']
        if self.origin == 'v141':
            self.spec, self.c = candidates_v141(j['dataset']); p = read(ROOT/j['prefix'])['state']; self.st = State(**p).clone()
            self.oracle = IndexedOracle(self.spec, self.c, p, lambda e: ledger.record({'key': self.key, **e})); self.direction = 'minimize' if self.spec['direction'] == '-' else 'maximize'
        else:
            self.c = read(ROOT/('artifacts/study_v144' if self.origin == 'v144' else 'artifacts/study_v148')/'candidates'/f"{j['app']}.json"); p = read(ROOT/j['prefix'])
            self.st = copy.deepcopy(p); self.oracle = (ev172.SparkOracle if self.origin == 'v144' else ev172.HadoopOracle)(self.c, self.key, p, ledger); self.direction = 'minimize'
        self.ledger = ledger
    @property
    def ids(self): return self.st.ids if self.origin == 'v141' else self.st['ids']
    @property
    def labels(self): return self.st.labels if self.origin == 'v141' else self.st['labels']
    @property
    def order(self): return self.st.order if self.origin == 'v141' else self.st['order']
    def observe(self, i):
        if self.origin == 'v141': self.ledger.charge(self.key, i); self.st.observe(i, self.oracle.acquire(i), self.c.directions)
        else: y = self.oracle.acquire(i); self.st['ids'].append(i); self.st['labels'].append(y)
    def fallback_round(self):
        rows = []
        if self.origin == 'v141':
            for i in rank(self.c, self.st, self.st.order)[:2]: self.observe(i); rows.append(i)
        else:
            for _ in range(2): i = (spark_v145.choose if self.origin == 'v144' else hadoop_v148.choose)(self.c, self.st, 'sequential_3nn'); self.observe(i); rows.append(i)
        return rows
    def target(self):
        v = [y[0] for y in self.labels if y[0] is not None]; return min(v) if self.direction == 'minimize' else max(v)
    def record(self): return self.st.record() if self.origin == 'v141' else self.st
    def string(self, p): return ''.join(ALPHABET[d.index(v)] for v, d in zip(p, self.ds))

def open_b_ledger(cfg):
    path = M/'B_acquisitions'; path.mkdir(parents=True, exist_ok=True); lp = path/'ledger.json'
    led = ev172.Ledger.__new__(ev172.Ledger); led.path, led.journal, led.cap, led.seconds = lp, path/'acquisitions.jsonl', cfg['acquisition_caps']['B'], 10**9; led.started = time.time()
    led.state = read(lp) if lp.exists() else {'started_unix': led.started, 'acquisitions': 0, 'cap': led.cap}
    if not lp.exists(): write(lp, led.state); led.journal.touch()
    return led

def arm_b(cfg, stage):
    tag = provider(); out = M/stage; out.mkdir(parents=True, exist_ok=False); cases = b_cases(cfg, stage); ledger = open_b_ledger(cfg)
    client = Client(cfg, out, stage, tag, 10*len(cases), SPEND); deadline = time.monotonic()+cfg['stage_seconds']['B']; error = None; finished = []; t = time.monotonic()
    rounds_n = cfg['arm_b']['rounds']; current = None
    try:
        for j in cases:
            current = j['qualified_key']; case = Case(j, ledger); original = read(ROOT/j['messages_path']); collisions = []; log = []
            for r in range(1, rounds_n+1):
                parsed = None; reason = None; attempts = []
                for attempt in range(cfg['arm_b']['retries_per_round']+1):
                    msgs = b_messages(original, case.origin, case.c, case.ds, case.ids, case.labels, case.direction, r, rounds_n, collisions, reason)
                    seed = j['sampling_seed']+cfg['arm_b']['seed_offset']+10*r+attempt
                    status, resp, err = client.send(client.body(msgs, schema(case.ds, 2), cfg['top_p']['B'], seed, cfg['max_tokens']['B']), f"{j['qualified_key']}::r{r}::a{attempt}", deadline)
                    try: content, _ = content_of(resp); parsed = parse(content, case.ds, 2); attempts.append({'attempt': attempt, 'seed': seed, 'status': 'valid'}); break
                    except ValueError as e: reason = str(e) if resp is not None else (err or str(e)); attempts.append({'attempt': attempt, 'seed': seed, 'status': 'invalid', 'reason': reason})
                if parsed is not None:
                    rows, diag = project_any(case.origin, case.c, case.order, case.ids, parsed)
                    append(out/'rounds.jsonl', {'case': j['qualified_key'], 'round': r, 'kind': 'model', 'attempts': attempts, 'selected_rows': rows, 'projection': diag, 'at_unix': time.time()})
                    for i in rows: case.observe(i)
                    collisions += [case.string(d['proposal']) for d in diag if d['collision']]
                else:
                    append(out/'rounds.jsonl', {'case': j['qualified_key'], 'round': r, 'kind': 'fallback_pending', 'attempts': attempts, 'at_unix': time.time()})
                    rows = case.fallback_round(); append(out/'rounds.jsonl', {'case': j['qualified_key'], 'round': r, 'kind': 'fallback', 'selected_rows': rows, 'at_unix': time.time()})
                log.append({'round': r, 'kind': 'model' if parsed is not None else 'fallback', 'attempts': len(attempts), 'rows': rows})
            write(out/'arms'/f'{key_name(j)}.json', {**j, 'arm': 'gptoss_b', 'stage': stage, 'state': case.record(), 'direction': case.direction, 'target': case.target(),
                  'rounds': log, 'fallback_rounds': sum(x['kind'] == 'fallback' for x in log), 'requests': sum(x['attempts'] for x in log), 'collisions': collisions,
                  'missing_acquisitions': sum(y[0] is None for y in case.labels)})
            finished.append(j['qualified_key']); current = None; print(stage, j['qualified_key'], 'fallback_rounds', sum(x['kind'] == 'fallback' for x in log), 'target', case.target(), flush=True)
    except Refused as e: error = 'refused: '+str(e)
    except Exception as e: error = repr(e)
    unfinished = [j['qualified_key'] for j in cases if j['qualified_key'] not in finished]
    write(out/'summary.json', {'at': now(), 'stage': stage, 'provider': tag, 'intended_cases': len(cases), 'finished_cases': finished, 'unfinished_cases': unfinished,
          'interrupted_case': current, 'not_started_cases': [k for k in unfinished if k != current],
          'requests': client.requests, 'error': error, 'seconds': time.monotonic()-t, 'spend': read(SPEND), 'acquisitions_so_far': read(M/'B_acquisitions'/'ledger.json')['acquisitions']})
    print(read(out/'summary.json'))

def complete_b(cfg):
    """EB: an unfinished case restarts from its saved prefix and spends its whole 10-label budget on the origin fallback (no model request)."""
    out = M/'EB'; out.mkdir(parents=True, exist_ok=False); ledger = open_b_ledger(cfg); completed = []
    done = {read(p)['qualified_key'] for p in M.glob('B*/arms/*.json')}; todo = []
    for stage in [x for b in BASE if b.startswith('B') for x in chain(b)]:
        if (M/stage/'summary.json').exists(): todo += [(stage, k) for k in read(M/stage/'summary.json')['unfinished_cases'] if k not in done and k not in [t[1] for t in todo]]
    for stage, k in todo:
            j = next(x for x in read(JOBS) if x['qualified_key'] == k)
            # A case interrupted mid-loop already charged acquisitions in the shared journal; those stay charged. Its B20 arm is rebuilt fallback-only from the prefix.
            case = Case(j, ledger); rows = [case.fallback_round() for _ in range(cfg['arm_b']['rounds'])]
            write(out/'arms'/f'{key_name(j)}.json', {**j, 'arm': 'gptoss_b', 'stage': 'EB', 'state': case.record(), 'direction': case.direction, 'target': case.target(),
                  'rounds': [{'round': r+1, 'kind': 'fallback_unfinished', 'attempts': 0, 'rows': x} for r, x in enumerate(rows)], 'fallback_rounds': 5, 'requests': 0, 'collisions': [],
                  'missing_acquisitions': sum(y[0] is None for y in case.labels), 'interrupted_in_stage': stage}); completed.append(k)
    write(out/'summary.json', {'at': now(), 'completed_fallback_cases': completed, 'acquisitions_total_B': read(M/'B_acquisitions'/'ledger.json')['acquisitions']}); print(read(out/'summary.json'))

def main():
    stages = ['P2', 'E', 'EB', 'close_A1']+chain('A1R')+chain('A2')+[x for b in BASE if b.startswith('B') and len(b) == 2 for x in chain(b)]
    ap = argparse.ArgumentParser(); ap.add_argument('stage', choices=stages); a = ap.parse_args(); cfg = config(); verify_freeze()
    if a.stage == 'close_A1': return close_failed_a1()
    require_previous(a.stage); base = a.stage.partition('.')[0]
    if a.stage == 'P2': probe(cfg)
    elif a.stage == 'E': evaluate_a(cfg)
    elif a.stage == 'EB': complete_b(cfg)
    elif base in ('A1R', 'A2'): arm_a(cfg, a.stage)
    else: arm_b(cfg, a.stage)

if __name__ == '__main__': main()
