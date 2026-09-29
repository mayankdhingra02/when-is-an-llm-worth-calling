"""Prepared V59 four-workload screen; authorization gate precedes workload execution."""
import hashlib,itertools,json,os,random,re,shutil,sys,time
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'src'))
from escalation.bounded_process_v57 import run
from escalation.planning_v55 import Task
from escalation.classical_planning_v56 import grid as planning_grid, options as planning_options
from run_planning_v55 import SRC,DATA,rss
from run_java_feasibility_v53 import JAVA,JAR,parse_status,digest
OUT=ROOT/'results/v59_workload_physical'
SCRATCH=ROOT/'artifacts/sources/live_v59'

def write(path,obj):path.write_text(json.dumps(obj,indent=2)+'\n')
def main():
    from escalation.authorization_v59 import require_authorization
    require_authorization(ROOT)
    seal=json.loads((ROOT/'reports/protocol_v59_workload_screen.freeze.json').read_text())
    for name,h in seal['sha256'].items():assert digest(ROOT/name)==h,name
    rss(-1)
    metadata=json.loads((ROOT/'artifacts/study_v57/workload_metadata.json').read_text())
    java_meta={w['id']:w for w in metadata['workloads'] if w['family']=='javagc'}
    domain=(DATA/'domain.pddl').read_text()
    tasks={n:Task(domain,(ROOT/f'artifacts/sources/v57/{n}.pddl').read_text()) for n in ['p01','p10']}
    workload_order=[('javagc','small'),('fastdownward','p01'),('javagc','large'),('fastdownward','p10')]
    java_grid=list(itertools.product([1,2,4,8],[1,2,4,8],[2,4,8]))
    schedule=[]
    for rep in range(3):
        for j,(f,n) in enumerate(workload_order):
            ids=list(range(48));random.Random(59000+rep*10+j).shuffle(ids)
            for cid in ids: schedule.append({'trial':len(schedule),'round':rep,'family':f,'workload':n,'config_id':cid})
    OUT.mkdir(exist_ok=False);SCRATCH.mkdir(exist_ok=False);write(OUT/'schedule.json',schedule)
    rows=[];retained=set();stage=time.monotonic();stopped=None
    def monitor(pgid):
        memory=rss(pgid)
        scratch=sum(p.stat().st_size for p in SCRATCH.rglob('*') if p.is_file())
        return {'rss_bytes':memory,'scratch_bytes':scratch},('rss_watchdog' if memory>2*1024**3 else 'scratch_watchdog' if scratch>2*1024**3 else None)
    for intended in schedule:
        row=dict(intended);java=row['family']=='javagc';cap=60 if java else 30
        if stopped or time.monotonic()-stage>7200-cap-5:
            row.update(status='unattempted',reason=stopped or 'stage_limit');rows.append(row);continue
        trial=OUT/f"trial_{row['trial']:02d}";trial.mkdir();scratch=SCRATCH/f"trial_{row['trial']:02d}";scratch.mkdir()
        n=row['workload'];rep=row['round'];env=os.environ.copy()
        if java:
            config=java_grid[row['config_id']]
            command=[str(JAVA),'-Xms512m','-Xmx512m','-XX:+UseParallelGC','-XX:-UseAdaptiveSizePolicy',
                     f'-XX:ParallelGCThreads={config[0]}',f'-XX:NewRatio={config[1]}',f'-XX:SurvivorRatio={config[2]}',
                     '-jar',str(JAR),'xalan','-s',n,'-t','1','-n','2','--preserve','--scratch-directory',str(scratch),
                     '--validation-report',str(trial/'validation.txt')]
            for key in ['JAVA_TOOL_OPTIONS','_JAVA_OPTIONS','JDK_JAVA_OPTIONS','CLASSPATH']:env.pop(key,None)
        else:
            config=planning_grid()[row['config_id']]
            command=[sys.executable,str(SRC/'fast-downward.py'),'--build','release_no_lp','--overall-time-limit','27s',
                     '--keep-sas-file','--plan-file',str(trial/'sas_plan'),str(DATA/'domain.pddl'),
                     str(ROOT/f'artifacts/sources/v57/{n}.pddl'),*planning_options(config)]
        row.update(configuration=config,command=command,started_at_unix=time.time());write(trial/'start.json',row)
        if not java:
            # Put planner files in monitored scratch; retain/copy after completion.
            command=list(command);command[command.index('--plan-file')+1]=str(scratch/'sas_plan')
            row['command']=command;write(trial/'start.json',row)
        result=run(command,cwd=ROOT if java else scratch,log_path=trial/'process.log',wall_cap=cap,monitor=monitor,env=env)
        row.update(result);row['status']='failed';row['objective_ms']=120000. if java else 60000.;log=(trial/'process.log').read_text(errors='replace')
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
                row['status']='valid';row['objective_ms']=row['final_ms']
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
                    if check['cost']!='105':raise ValueError('Utility contract cost105 mismatch')
                    if re.findall(r'; cost = (\d+) \(',plan)!=[check['cost']] or re.findall(r'Plan cost: (\d+)',log)!=[check['cost']]:raise ValueError('Cost disagreement')
                    row.update(status='valid',validation=check,plan_sha256=digest(plans[0]),objective_ms=row['wall_seconds']*1000)
                except ValueError as exc:row.update(status='invalid_plan',validation_error=str(exc))
        resource_failure=row['termination_reason'] in ['wall_timeout','rss_watchdog','scratch_watchdog'] or (not java and row['exit_code'] in [20,21,22,23,24])
        if row['status']!='valid' and not resource_failure:stopped='unexpected_or_invalid_output'
        write(trial/'result.json',row);rows.append(row)
        with (OUT/'trials.jsonl').open('a') as f:f.write(json.dumps(row)+'\n')
        print(row['trial'],row['family'],n,row['status'],round(row['wall_seconds'],3),flush=True)
    write(OUT/'all_cases.json',rows)
    workloads=[]
    for f,n in workload_order:
        cases=[r for r in rows if r['family']==f and r['workload']==n]
        costs=sorted({r['validation']['cost'] for r in cases if 'validation' in r})
        workloads.append({'family':f,'workload':n,'intended':144,'attempted':sum('exit_code' in r for r in cases),'valid':sum(r['status']=='valid' for r in cases),
                          'costs':costs,'all_trials_valid':all(r['status']=='valid' for r in cases) and (f=='javagc' or len(costs)==1)})
    summary={'study':'v59','scope':'fixed physical grids, development only','independent_families':2,'workloads':workloads,
             'intended':576,'attempted':sum('exit_code' in r for r in rows),'valid':sum(r['status']=='valid' for r in rows),
             'complete_table':stopped is None and all('exit_code' in r for r in rows),'stopped_reason':stopped,'unattempted':sum(r['status']=='unattempted' for r in rows),'stage_seconds':time.monotonic()-stage,'model_requests':0,'recorded_objective_accesses':0,'external_spend_usd':0}
    write(OUT/'summary.json',summary);print(json.dumps(summary,indent=2),flush=True)
if __name__=='__main__':main()
