"""Run the frozen five-workload admission matrix; retains full denominator."""
import hashlib,json,os,re,shutil,sys,time
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'src'))
from escalation.bounded_process_v57 import run
from escalation.planning_v55 import Task
from run_planning_v55 import SRC,DATA,rss
from run_java_feasibility_v53 import JAVA,JAR,parse_status,digest
OUT=ROOT/'results/v57_workload_matrix'
SCRATCH=ROOT/'artifacts/sources/live_v57'

def write(path,obj):path.write_text(json.dumps(obj,indent=2)+'\n')
def main():
    seal=json.loads((ROOT/'reports/protocol_v57_workload_matrix.freeze.json').read_text())
    for name,h in seal['sha256'].items():assert digest(ROOT/name)==h,name
    rss(-1)
    metadata=json.loads((ROOT/'artifacts/study_v57/workload_metadata.json').read_text())
    java_meta={w['id']:w for w in metadata['workloads'] if w['family']=='javagc'}
    domain=(DATA/'domain.pddl').read_text()
    tasks={n:Task(domain,(ROOT/f'artifacts/sources/v57/{n}.pddl').read_text()) for n in ['p01','p10','p20']}
    workload_order=[('javagc','small'),('fastdownward','p01'),('javagc','large'),('fastdownward','p10'),('fastdownward','p20')]
    schedule=[{'trial':rep*5+j,'round':rep,'family':f,'workload':n} for rep in range(3) for j,(f,n) in enumerate(workload_order)]
    OUT.mkdir(exist_ok=False);SCRATCH.mkdir(exist_ok=False);write(OUT/'schedule.json',schedule)
    rows=[];retained=set();stage=time.monotonic();stopped=None
    def monitor(pgid):
        memory=rss(pgid)
        scratch=sum(p.stat().st_size for p in SCRATCH.rglob('*') if p.is_file())
        return {'rss_bytes':memory,'scratch_bytes':scratch},('rss_watchdog' if memory>2*1024**3 else 'scratch_watchdog' if scratch>2*1024**3 else None)
    for intended in schedule:
        row=dict(intended);java=row['family']=='javagc';cap=60 if java else 30
        if stopped or time.monotonic()-stage>750-cap-5:
            row.update(status='unattempted',reason=stopped or 'stage_limit');rows.append(row);continue
        trial=OUT/f"trial_{row['trial']:02d}";trial.mkdir();scratch=SCRATCH/f"trial_{row['trial']:02d}";scratch.mkdir()
        n=row['workload'];rep=row['round'];env=os.environ.copy()
        if java:
            config=[(1,2,8),(4,4,4),(1,2,8)][rep]
            command=[str(JAVA),'-Xms512m','-Xmx512m','-XX:+UseParallelGC','-XX:-UseAdaptiveSizePolicy',
                     f'-XX:ParallelGCThreads={config[0]}',f'-XX:NewRatio={config[1]}',f'-XX:SurvivorRatio={config[2]}',
                     '-jar',str(JAR),'xalan','-s',n,'-t','1','-n','2','--preserve','--scratch-directory',str(scratch),
                     '--validation-report',str(trial/'validation.txt')]
            for key in ['JAVA_TOOL_OPTIONS','_JAVA_OPTIONS','JDK_JAVA_OPTIONS','CLASSPATH']:env.pop(key,None)
        else:
            config=['astar(lmcut())','astar(hmax())','astar(lmcut())'][rep]
            command=[sys.executable,str(SRC/'fast-downward.py'),'--build','release_no_lp','--overall-time-limit','27s',
                     '--keep-sas-file','--plan-file',str(trial/'sas_plan'),str(DATA/'domain.pddl'),
                     str(ROOT/f'artifacts/sources/v57/{n}.pddl'),'--search',config]
        row.update(configuration=config,command=command,started_at_unix=time.time());write(trial/'start.json',row)
        if not java:
            # Put planner files in monitored scratch; retain/copy after completion.
            command=list(command);command[command.index('--plan-file')+1]=str(scratch/'sas_plan')
            row['command']=command;write(trial/'start.json',row)
        result=run(command,cwd=ROOT if java else scratch,log_path=trial/'process.log',wall_cap=cap,monitor=monitor,env=env)
        row.update(result);row['status']='failed';log=(trial/'process.log').read_text(errors='replace')
        row['log_sha256']=digest(trial/'process.log')
        if result['termination_reason']=='watchdog_error':stopped='watchdog_error'
        if java:
            row.update(parse_status(log));outputs=sorted(scratch.glob('xalan.out.*'))
            row['output_names']=[p.name for p in outputs]
            if len(outputs)==1:
                row.update(output_bytes=outputs[0].stat().st_size,output_sha256=digest(outputs[0]))
            owner_ok=result['exit_code']==0 and row['success_markers'] and result['termination_reason'] is None
            row['reference_output_equal']=row.get('output_bytes')==java_meta[n]['expected_final_bytes'] and row.get('output_sha256')==java_meta[n]['expected_final_sha256']
            if owner_ok and row['reference_output_equal']:
                row['status']='valid'
                if n in retained:
                    shutil.rmtree(scratch)
                    row['output_retained']=False
                else:
                    retained.add(n);row['output_retained']=True;row['retained_output_path']=str(outputs[0].relative_to(ROOT))
        else:
            for p in scratch.iterdir():
                if p.is_file():shutil.copyfile(p,trial/p.name)
            if result['exit_code']==0 and result['termination_reason'] is None:
                try:
                    plans=list(trial.glob('sas_plan*'))
                    if len(plans)!=1:raise ValueError('Expected exactly one plan')
                    plan=plans[0].read_text();check=tasks[n].validate(plan)
                    if re.findall(r'; cost = (\d+) \(',plan)!=[check['cost']] or re.findall(r'Plan cost: (\d+)',log)!=[check['cost']]:raise ValueError('Cost disagreement')
                    row.update(status='valid',validation=check,plan_sha256=digest(plans[0]))
                except ValueError as exc:row.update(status='invalid_plan',validation_error=str(exc))
        write(trial/'result.json',row);rows.append(row)
        with (OUT/'trials.jsonl').open('a') as f:f.write(json.dumps(row)+'\n')
        print(row['trial'],row['family'],n,row['status'],round(row['wall_seconds'],3),flush=True)
    write(OUT/'all_cases.json',rows)
    workloads=[]
    for f,n in workload_order:
        cases=[r for r in rows if r['family']==f and r['workload']==n]
        costs=sorted({r['validation']['cost'] for r in cases if 'validation' in r})
        workloads.append({'family':f,'workload':n,'intended':3,'attempted':sum('exit_code' in r for r in cases),'valid':sum(r['status']=='valid' for r in cases),
                          'costs':costs,'admitted':all(r['status']=='valid' for r in cases) and (f=='javagc' or len(costs)==1)})
    summary={'study':'v57','scope':'development workload admission, not optimization','independent_families':2,'workloads':workloads,
             'intended':15,'attempted':sum('exit_code' in r for r in rows),'valid':sum(r['status']=='valid' for r in rows),
             'unattempted':sum(r['status']=='unattempted' for r in rows),'stage_seconds':time.monotonic()-stage,'model_requests':0,'recorded_objective_accesses':0,'external_spend_usd':0}
    write(OUT/'summary.json',summary);print(json.dumps(summary,indent=2),flush=True)
if __name__=='__main__':main()
