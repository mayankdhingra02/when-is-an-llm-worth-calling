"""Sequential V173 stage driver (orchestration only; scientific logic lives in collect_v173). One stage at a time.

Runs remaining arm-A chain stages, E, then (after the amendment-2 cost check) arm-B chains and EB. Each stage is a
separate create-once collector process; the driver never retries a stage and stops on any collector error.
"""
import json, subprocess, sys
from collect_smollm_v47 import ROOT, read, write, now
from collect_v173 import M, E, BASE, chain, chain_done
PY = str(ROOT/'.venv/bin/python'); LOG = ROOT/'artifacts/study_v173/driver.jsonl'

def log(ev):
    with LOG.open('a') as f: f.write(json.dumps({'at': now(), **ev})+'\n')
    print(ev, flush=True)

def run(stage):
    with (ROOT/f'artifacts/study_v173/driver_stage_{stage}.log').open('a') as f: rc = subprocess.run([PY, 'scripts/collect_v173.py', stage], cwd=ROOT, stdout=f, stderr=subprocess.STDOUT).returncode
    log({'stage': stage, 'exit': rc})
    if rc != 0: sys.exit(f'Stage {stage} exited {rc}; driver stops')

def run_chain(base):
    for s in chain(base):
        if (M/s/'summary.json').exists(): continue
        if chain_done(base): return
        run(s)

def b_projection():
    cfg = read(ROOT/'configs/study_v173.json'); rows = [json.loads(l) for s in ['A1R', 'A2'] for x in chain(s) if (M/x/'responses.jsonl').exists() for l in (M/x/'responses.jsonl').read_text().splitlines()]
    ok = [r for r in rows if r['http_status'] == 200 and r['reported_cost_usd']]; per = sum(r['reported_cost_usd'] for r in ok)/len(ok); spent = read(M/'spend_ledger.json')['spent_usd']
    expected_b = 70*cfg['arm_b']['rounds']*1.1  # five rounds per case plus ~10% in-round retries
    projected = spent+per*expected_b*cfg['cost_safety_factor']
    return {'spent_usd': spent, 'mean_cost_per_valid_arm_a_request': per, 'expected_b_requests': expected_b, 'projected_total_usd': projected, 'cap_usd': cfg['spend_cap_usd'], 'ok': projected <= cfg['spend_cap_usd']}

def main():
    phase = sys.argv[1] if len(sys.argv) > 1 else 'A'
    if phase == 'A':
        run_chain('A1R'); run_chain('A2')
        if not (E/'completion.json').exists(): run('E')
        pr = b_projection(); write(ROOT/'artifacts/study_v173/b_cost_projection.json', pr); log({'b_cost_projection': pr})
        if not pr['ok']: sys.exit('Projected spend exceeds the cap; arm B needs an owner decision')
        phase = 'B'
    if phase == 'B':
        for b in [x for x in BASE if x.startswith('B') and len(x) == 2]: run_chain(b)
        if not (M/'EB'/'summary.json').exists(): run('EB')
        log({'done': True, 'spend': read(M/'spend_ledger.json')})

if __name__ == '__main__': main()
