"""Generate explicit evaluator/version adaptation; source optimizer remains unchanged."""
import json
from pathlib import Path
R=Path(__file__).resolve().parents[1]
def main():
    s=(R/'scripts/collect_ezr_v169.py').read_text().replace('v169','v170')
    s=s.replace('from check_apps_v168 import check','from native_evaluator_v170 import ENGINES,stage,candidate,command,validate').replace(";OLD=ROOT/'artifacts/study_v168'",'')
    s=s.replace("jobs=read(OLD/'jobs.json')","jobs=[j for v in [159,163] for j in read(ROOT/f'artifacts/study_v{v}/jobs.json')]")
    s=s.replace("prior=read(ROOT/'results/v168_native/selections.json');assert len(prior)==70","prior=[s for v in [159,163] for s in read(ROOT/f'results/v{v}_native/selections.json')];assert len(prior)==140")
    a=s.index('    files=');b=s.index("    write(A/'freeze.json'",a)
    s=s[:a]+'''    files=['reports/protocol_v170.md','configs/study_v170.json','scripts/ezr_bridge_v169.py','scripts/native_evaluator_v170.py','scripts/collect_ezr_v170.py','scripts/prepare_ezr_v170.py','scripts/app_validation_v163.py','scripts/solver_worker_v157.py','scripts/app_worker_v162.py','tests/synthetic/test_ezr_v170.py','artifacts/study_v170/runtime.json','artifacts/study_v170/plan.json','artifacts/study_v170/prior_selections.json','artifacts/study_v170/preflight_tests.log','artifacts/sources/ezr_ezr.py','artifacts/sources/ezr_LICENSE.md','artifacts/source_manifest.json','results/v159_native/selections.json','results/v163_native/selections.json']
    hashes=read(ROOT/'artifacts/study_v169/freeze.json')['sha256'].copy()
    for v in [159,163]:
        for name in ['freeze.json','inputs.freeze.json']:hashes.update(read(ROOT/f'artifacts/study_v{v}/{name}')['sha256'])
    for f in read(ROOT/'artifacts/study_v160/corpus_files.json'):hashes['.native-v160/search_corpus/'+f['path']]=f['sha256']
    hashes.update({n:sha(ROOT/n) for n in files});rt=read(A/'runtime.json');hashes[rt['path']]=rt['sha256']
''' +s[b:]
    s=s.replace("cs={e:read(OLD/'candidates'/f'{e}.json') for e in cfg['engines']}","cs={e:candidate(e) for e in cfg['engines']}")
    s=s.replace("q=3 if task['engine']=='polars' else 1","q=5 if task['engine']=='ripgrep' else 1")
    s=s.replace("cmd=[str(ROOT/'.venv/bin/python'),str(ROOT/'scripts/worker_apps_v167.py'),'--engine',task['engine'],'--candidate',str(i)]","cmd=command(task['engine'],i,cs[task['engine']])")
    s=s.replace("raw=json.loads(p.stdout);assert raw['candidate']==i","raw=json.loads(p.stdout)").replace("v,status=check(raw,task['engine'],cs[task['engine']]['configs'][i])","v,status=validate(raw,task['engine'],cs[task['engine']],i)")
    s=s.replace("'scripts/ezr_bridge_v170.py'","'scripts/ezr_bridge_v169.py'")
    s=s.replace("'intended':410","'intended':820").replace("==140\n","==280\n").replace('len(selections)==90','len(selections)==180').replace('range(90)','range(180)').replace('16910+block','17010+block').replace("ledger['acquisitions']==410 and ledger['query_training_executions']==820","ledger['acquisitions']==820 and ledger['query_training_executions']==1640").replace('410 new outcomes /820','820 new outcomes /1640')
    s=s.replace("p=subprocess.run(cmd,cwd=ROOT,env=env,capture_output=True,text=True,timeout=cfg['worker_seconds_cap']);record.update","worker=subprocess.Popen(cmd,cwd=ROOT,env=env,stdout=subprocess.PIPE,stderr=subprocess.PIPE,text=True,start_new_session=True)\n            try:stdout,stderr=worker.communicate(timeout=cfg['worker_seconds_cap'])\n            finally:\n                if worker.poll() is None:os.killpg(worker.pid,signal.SIGKILL);worker.wait()\n            p=subprocess.CompletedProcess(cmd,worker.returncode,stdout,stderr);record.update")
    (R/'scripts/collect_ezr_v170.py').write_text(s)
    (R/'scripts/prepare_ezr_v170.py').write_text('from collect_ezr_v170 import prepare\nif __name__=="__main__":prepare()\n')
    cfg=json.loads((R/'configs/study_v169.json').read_text());cfg.update(engines=['cvc5','ortools','ripgrep','hnswlib'],new_outcome_cap=820,query_training_execution_cap=1640,schedule_seed=17001,accuracy_floor=None,quality_penalty_seconds=20,scope='fixed source controls on all four earlier native implementations')
    (R/'configs/study_v170.json').write_text(json.dumps(cfg,indent=2)+'\n')
if __name__=='__main__':main()
