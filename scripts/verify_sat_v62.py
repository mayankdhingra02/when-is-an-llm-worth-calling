"""Independent saved DIMACS/model replay, including planted witness checks."""
import hashlib,json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def h(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def read(p):return json.loads(p.read_text())
def check(cnf,model):
    lines=cnf.splitlines();header=lines[0].split();assert header[:2]==['p','cnf'];n,m=map(int,header[2:])
    clauses=[]
    for line in lines[1:]:
        lits=list(map(int,line.split()));assert len(lits)==4 and lits[-1]==0 and len({abs(x) for x in lits[:-1]})==3
        assert all(0<abs(x)<=n for x in lits[:-1]);clauses.append(lits[:-1])
    assert len(clauses)==m
    words=model.split();assert words[0]=='SAT' and words[-1]=='0';assignment={}
    for word in words[1:-1]:
        x=int(word);assert 0<abs(x)<=n and abs(x) not in assignment;assignment[abs(x)]=x>0
    assert all(any(assignment.get(abs(x))==(x>0) for x in c if abs(x) in assignment) for c in clauses)
    return {'variables_assigned':len(assignment),'clauses_verified':m,'satisfies_every_clause':True}
def main():
    for n,d in read(ROOT/'reports/protocol_v62_sat_feasibility.freeze.json')['sha256'].items():assert h(ROOT/n)==d,n
    meta=read(ROOT/'data/generated_v62/manifest.json')
    for t in meta:
        assert h(ROOT/t['path'])==t['sha256'] and h(ROOT/t['witness_path'])==t['witness_sha256']
        check((ROOT/t['path']).read_text(),(ROOT/t['witness_path']).read_text())
    out=ROOT/'results/v62_sat_feasibility';rows=read(out/'all_cases.json');schedule=read(out/'schedule.json');summary=read(out/'summary.json');assert len(rows)==len(schedule)==6
    journal=[json.loads(s) for s in (out/'trials.jsonl').read_text().splitlines()];assert journal==[r for r in rows if 'exit_code' in r]
    valid=0
    for r,s in zip(rows,schedule):
        assert all(r[k]==v for k,v in s.items())
        if r['status']=='unattempted':continue
        d=out/f"trial_{r['trial']:02d}";assert read(d/'result.json')==r and h(d/'solver.log')==r['log_sha256']
        start=read(d/'start.json');assert all(r[k]==v for k,v in start.items())
        if r['status']=='valid':
            assert r['exit_code']==10 and r['termination_reason'] is None and h(d/'model.txt')==r['model_sha256']
            assert check((ROOT/r['task']['path']).read_text(),(d/'model.txt').read_text())==r['validation']
            assert r['objective_ms']==1000*r['wall_seconds'];valid+=1
    assert valid==summary['valid'] and summary['stage_seconds']<=180
    print(json.dumps({'verified':True,'intended':6,'attempted':len(journal),'valid_models':valid,'witnesses_checked':2,'new_model_requests':0},indent=2))
if __name__=='__main__':main()
