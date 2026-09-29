"""Read-only verification of V57 measured logs, outputs and denominators."""
import hashlib,json,re,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'src'))
from escalation.planning_v55 import Task
from run_java_feasibility_v53 import digest,parse_status

def read(p):return json.loads(p.read_text())
def main():
    seal=read(ROOT/'reports/protocol_v57_workload_matrix.freeze.json')
    for name,h in seal['sha256'].items():assert digest(ROOT/name)==h,name
    out=ROOT/'results/v57_workload_matrix';rows=read(out/'all_cases.json');summary=read(out/'summary.json')
    schedule=read(out/'schedule.json');assert len(rows)==len(schedule)==15
    journal=[json.loads(x) for x in (out/'trials.jsonl').read_text().splitlines()]
    assert journal==[r for r in rows if 'exit_code' in r]
    metadata=read(ROOT/'artifacts/study_v57/workload_metadata.json')
    ref=(ROOT/'artifacts/sources/live_v53/trial_0/xalan.out.0').read_bytes();block=ref[:239010]
    assert block*100==ref and digest(ROOT/'artifacts/sources/live_v53/trial_0/xalan.out.0')==metadata['java_reference']['source_sha256']
    expected={}
    for size,n in [('small',10),('large',1000)]:
        h=hashlib.sha256()
        for _ in range(n):h.update(block)
        expected[size]=(len(block)*n,h.hexdigest())
    tasks={w:Task((ROOT/'artifacts/sources/v55/domain.pddl').read_text(),(ROOT/f'artifacts/sources/v57/{w}.pddl').read_text()) for w in ['p01','p10','p20']}
    valid=0;plans=0;jvms=0
    for row,intended in zip(rows,schedule):
        assert all(row[k]==v for k,v in intended.items())
        if row['status']=='unattempted':continue
        trial=out/f"trial_{row['trial']:02d}"
        assert row==read(trial/'result.json')
        start=read(trial/'start.json');assert all(row[k]==v for k,v in start.items())
        log=(trial/'process.log').read_text(errors='replace');assert digest(trial/'process.log')==row['log_sha256']
        assert 0 < row['wall_seconds'] <= row['watchdog_elapsed_seconds']
        if row['family']=='javagc':
            jvms+=1
            parsed=parse_status(log);assert all(row[k]==v for k,v in parsed.items())
            cap=60
            if row['status']=='valid':
                assert row['reference_output_equal'] and row['success_markers']
                assert (row['output_bytes'],row['output_sha256'])==expected[row['workload']]
                if row['output_retained']:
                    p=ROOT/row['retained_output_path'];assert p.stat().st_size==row['output_bytes'] and digest(p)==row['output_sha256']
        else:
            cap=30
            if row['status']=='valid':
                plans+=1;p=trial/'sas_plan';v=tasks[row['workload']].validate(p.read_text())
                assert v==row['validation'] and digest(p)==row['plan_sha256']
                assert re.findall(r'Plan cost: (\d+)',log)==[v['cost']]
                assert (trial/'output.sas').exists()
        if row['status']=='valid':
            valid+=1;assert row['exit_code']==0 and row['termination_reason'] is None and row['wall_seconds']<=cap
    assert valid==summary['valid'] and len(journal)==summary['attempted']
    admitted=0
    for w in summary['workloads']:
        group=[r for r in rows if r['family']==w['family'] and r['workload']==w['workload']]
        costs=sorted({r['validation']['cost'] for r in group if 'validation' in r})
        assert w['costs']==costs and len(group)==w['intended']==3
        assert w['valid']==sum(r['status']=='valid' for r in group)
        passed=all(r['status']=='valid' for r in group) and (w['family']=='javagc' or len(costs)==1)
        assert w['admitted']==passed;admitted+=passed
    print(json.dumps({'verified':True,'frozen_inputs':len(seal['sha256']),'intended':15,'attempted':len(journal),'valid_trials':valid,'valid_plans':plans,'java_invocations':jvms,'admitted_workloads':admitted,'independent_families':2},indent=2))
if __name__=='__main__':main()
