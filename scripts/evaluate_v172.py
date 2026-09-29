"""V172 stage E: seal all 140 selections, then charge recorded acquisitions through V172-owned oracles.

Reuses each origin stage's projection, fallback and target-scoring code; never writes to historical result directories.
"""
import copy, csv, json, math, time
from collect_smollm_v47 import ROOT, read, write, append, sha, now
from common_v172 import A, M, E, STAGES, ORDER, config, verify_freeze
from proposal_v127 import project as project_v141
from analyze_pointwise_v123 import candidates as candidates_v141
from escalation.core import State
from escalation.transfer_v41 import IndexedOracle, rank, best
import spark_v144, spark_v145, hadoop_v148
ARMS = ['qwen3_14b', 'qwen3_8b_redraw']

class Ledger:
    """One global V172 acquisition ledger; every attempt is charged before its target is read."""
    def __init__(self, path, journal, cap, seconds):
        self.path, self.journal, self.cap, self.seconds = path, journal, cap, seconds; self.started = time.time()
        self.state = {'started_unix': self.started, 'acquisitions': 0, 'cap': cap, 'seconds_cap': seconds}; write(path, self.state)
    def charge(self, key, row_id):
        if self.state['acquisitions'] >= self.cap: raise PermissionError('V172 acquisition cap')
        if time.time()-self.started >= self.seconds: raise TimeoutError('V172 evaluation time cap')
        self.state['acquisitions'] += 1; write(self.path, self.state)
    def record(self, event): append(self.journal, {'at_unix': time.time(), **event})

class SparkOracle:
    """Same semantics as spark_v145.Oracle: exec_time column 30; empty cell stays charged as None."""
    def __init__(self, c, key, prefix, ledger):
        if sha(ROOT/c['source_path']) != c['source_sha256']: raise ValueError('Changed source')
        self.c, self.key, self.ledger = c, key, ledger; self.seen = set(prefix['ids']); self.lines = (ROOT/c['source_path']).read_text().splitlines()
    def acquire(self, i):
        if type(i) != int or not 0 <= i < len(self.c['x']) or i in self.seen or len(self.seen) >= 20: raise ValueError('Invalid/duplicate/over-budget')
        self.ledger.charge(self.key, i); self.seen.add(i)
        raw = next(csv.reader([self.lines[self.c['source_lines'][i]-1]]))[30]; event = {'key': self.key, 'row_id': i, 'source_line': self.c['source_lines'][i], 'raw_target': raw}
        if not raw.strip(): self.ledger.record({**event, 'value': None, 'error': 'missing_source_target'}); return [None]
        try:
            value = float(raw)
            if not math.isfinite(value) or value <= 0: raise ValueError('Nonpositive/nonfinite target')
        except Exception as e: self.ledger.record({**event, 'error': repr(e)}); raise
        self.ledger.record({**event, 'value': value}); return [value]

class HadoopOracle:
    """Same semantics as hadoop_v148.Oracle, including its declared incomplete-run penalty."""
    def __init__(self, c, key, prefix, ledger): self.c, self.key, self.ledger = c, key, ledger; self.seen = set(prefix['ids'])
    def acquire(self, i):
        if type(i) != int or not 0 <= i < len(self.c['x']) or i in self.seen or len(self.seen) >= 20: raise ValueError('Duplicate/over-budget acquisition')
        self.ledger.charge(self.key, i); self.seen.add(i); n = self.c['sources'][i]; event = {'key': self.key, 'row_id': i, 'source': n, 'source_sha256': self.c['source_hashes'][i]}
        try:
            if sha(ROOT/n) != event['source_sha256']: raise ValueError('Changed source')
            value, status = hadoop_v148.score_record(read(ROOT/n), self.c['app']); event.update(value=value, status=status)
        except Exception as e: self.ledger.record({**event, 'value': None, 'status': 'invalid_source', 'error': repr(e)}); raise
        self.ledger.record(event); return [value]

def load_score(arm, j):
    stage = [s for s, (a, split) in STAGES.items() if a == arm and split == j['split']][0]
    p = M/stage/'scores'/f"{j['qualified_key'].replace('::', '__')}.json"
    return stage, (read(p) if p.exists() else {'status': 'unattempted', 'score': None})

def select(j, score):
    """Feature/prefix-only selection before any new target is read; mirrors each origin evaluator."""
    valid = score['status'] == 'valid'
    if j['origin'] == 'v141':
        spec, c = candidates_v141(j['dataset']); p = read(ROOT/j['prefix'])['state']
        if valid: ids, diag = project_v141(score['score'], c.x, p)
        else: ids, diag = rank(c, State(**p), p['order'])[:10], []
        return ids, diag, 'batch_3nn' if not valid else None
    c = read(ROOT/('artifacts/study_v144' if j['origin'] == 'v144' else 'artifacts/study_v148')/'candidates'/f"{j['app']}.json"); p = read(ROOT/j['prefix'])
    if valid: ids, diag = (spark_v144 if j['origin'] == 'v144' else hadoop_v148).project(c, p, score['score']); return ids, diag, None
    return [], [], 'stepwise_sequential_3nn'

def acquire(choice, ledger):
    j = choice; key = j['arm']+'::'+j['qualified_key']
    if j['origin'] == 'v141':
        spec, c = candidates_v141(j['dataset']); p = read(ROOT/j['prefix'])['state']; s = State(**p).clone()
        def journal(e): ledger.record({'key': key, **e})
        oracle = IndexedOracle(spec, c, p, journal)
        for i in j['selected_rows']: ledger.charge(key, i); s.observe(i, oracle.acquire(i), c.directions)
        rec = s.record(); return {'state': rec, 'direction': 'minimize' if spec['direction'] == '-' else 'maximize', 'target': best(s, spec['direction']), 'missing_acquisitions': 0}
    spark = j['origin'] == 'v144'; mod = spark_v144 if spark else hadoop_v148
    c = read(ROOT/('artifacts/study_v144' if spark else 'artifacts/study_v148')/'candidates'/f"{j['app']}.json"); p = read(ROOT/j['prefix']); s = copy.deepcopy(p)
    oracle = (SparkOracle if spark else HadoopOracle)(c, key, p, ledger)
    for step in range(10):
        if j['fallback']: i = (spark_v145.choose if spark else hadoop_v148.choose)(c, s, 'sequential_3nn')
        else: i = j['selected_rows'][step]
        s['ids'].append(i); s['labels'].append(oracle.acquire(i))
    return {'state': s, 'direction': 'minimize', 'target': min(y[0] for y in s['labels'] if y[0] is not None), 'missing_acquisitions': sum(y[0] is None for y in s['labels'])}

def main():
    cfg = config(); verify_freeze()
    for s in ORDER:
        if not (M/s/'summary.json').exists(): raise RuntimeError('Inference stage not ended: '+s)
    E.mkdir(parents=True, exist_ok=False); choices = []
    for arm in ARMS:
        for j in read(A/'jobs.json'):
            stage, score = load_score(arm, j); ids, diag, fallback = select(j, score)
            choices.append({**j, 'arm': arm, 'inference_stage': stage, 'model_status': score['status'], 'fallback': fallback is not None, 'fallback_kind': fallback, 'selected_rows': ids, 'projection': diag})
    write(E/'choices.json', choices); write(E/'selection_seal.json', {'at': now(), 'at_unix': time.time(), 'choices_sha256': sha(E/'choices.json'), 'scores_sha256': {str(p.relative_to(ROOT)): sha(p) for p in sorted(M.glob('*/scores/*.json'))}})
    ledger = Ledger(E/'ledger.json', E/'acquisitions.jsonl', cfg['new_recorded_acquisitions_cap'], cfg['evaluation_seconds_cap']); (E/'acquisitions.jsonl').touch(); arms = []; failures = []
    for ch in choices:
        name = ch['arm']+'__'+ch['qualified_key'].replace('::', '__')
        try: r = acquire(ch, ledger); write(E/'arms'/f'{name}.json', {**ch, **r}); arms.append(name)
        except (PermissionError, TimeoutError) as e: failures.append({'arm': name, 'error': repr(e)}); break
        except Exception as e: failures.append({'arm': name, 'error': repr(e)}); write(E/'arms'/f'{name}.json', {**ch, 'target': None, 'status': 'unscorable', 'error': repr(e)})
    write(E/'completion.json', {'at': now(), 'intended_arms': len(choices), 'scored_arms': len(arms), 'failures': failures, 'acquisitions': ledger.state['acquisitions'],
                               'seconds': time.time()-ledger.started, 'complete': len(arms) == len(choices) and not failures})
    print(read(E/'completion.json'))

if __name__ == '__main__': main()
