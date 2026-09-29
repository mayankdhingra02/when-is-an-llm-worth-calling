"""Deterministic pre-freeze adaptation of the retained paired collector."""
from pathlib import Path
import json
R=Path(__file__).resolve().parents[1]
def main():
    s=(R/'scripts/native_apps_v163.py').read_text().replace('v163','v168').replace('163000','168000').replace('163002','168002').replace('163200','168200').replace('163700','168700').replace('163701','168701').replace('163900','168900').replace('Random(163)','Random(168)').replace("'159|'","'168|'")
    s=s.replace("ENGINES=['ripgrep','hnswlib']","ENGINES=['polars','xgboost']").replace('artifacts/study_v162/candidates.json','artifacts/study_v166/candidates.json')
    start=s.index(' task=');end=s.index('\n return',start)
    s=s[:start]+" task={'polars':'Minimize elapsed time for the three fixed nycflights13 queries (monthly carrier delay totals, high-altitude routes, delayed summer flights with older aircraft), including CSV scanning/parsing of336776flights and joins to airline/airport/plane tables. All integer/string results must be exact.','xgboost':'Train seven-class CPU histogram XGBoost on65536real Covertype rows and predict8192quality-validation rows. Minimize DMatrix construction plus training and prediction time. Accuracy must be at least75%; infeasible configurations have fixed60second utility penalty, not successful measured runtime. eta0.3, seed16601 and all other settings fixed.'}[engine]"+s[end:]
    start=s.index('def prepare():');end=s.index('\ndef measure',start)
    s=s[:start]+'''def prepare():
 assert not (A/'freeze.json').exists()
 assert read(ROOT/'artifacts/study_v166/analysis.json')['admissions']['xgboost']['admitted']
 assert read(ROOT/'artifacts/study_v167/analysis.json')['admissions']['polars']['admitted']
 for e in ENGINES:write(A/'candidates'/f'{e}.json',candidates(e))
 write(A/'models.json',read(ROOT/'artifacts/study_v153/models.json'));write(A/'routers.json',read(ROOT/'artifacts/study_v153/routers.json'))
 jobs=[{'key':e+'_'+str(seed),'engine':e,'system_group':e,'seed':seed,'prefix':f'artifacts/study_v168/prefixes/{e}_{seed}.json','messages_path':f'artifacts/study_v168/prompts/{e}_{seed}.json','sampling_seed':168000+seed,'domains':candidates(e)['grid_domains']} for e in ENGINES for seed in SEEDS]
 random.Random(168).shuffle(jobs);write(A/'plan.json',jobs)
 paths=['reports/protocol_v168.md','configs/study_v168.json','scripts/native_apps_v168.py','scripts/run_apps_v168.py','scripts/collect_models_v168.py','scripts/runtime_models_v168.py','scripts/check_apps_v168.py','scripts/worker_apps_v167.py','scripts/native_study_v153.py','scripts/router_v132.py','scripts/router_v151.py','scripts/controllers_v154.py','scripts/gp_continuations_v155.py','scripts/proposal_v128.py','scripts/proposal_v127.py','scripts/audit_output_capacity_v127.py','scripts/process_rss_v129.py','src/escalation/receipts_v70.py','tests/synthetic/test_apps_v168.py','artifacts/study_v168/plan.json','artifacts/study_v168/models.json','artifacts/study_v168/routers.json','artifacts/study_v168/candidates/polars.json','artifacts/study_v168/candidates/xgboost.json','artifacts/study_v167/analysis.json','artifacts/study_v166/analysis.json','.local-runtime/llama-b11146/llama-server']
 hashes=read(ROOT/'artifacts/study_v167/freeze.json')['sha256'].copy();hashes.update({n:sha(ROOT/n) for n in paths})
 write(A/'freeze.json',{'at_unix':time.time(),'sha256':hashes})
''' + s[end:]
    s=s.replace('0<=i<64',"0<=i<len(c['configs'])").replace('order=list(range(64))',"order=list(range(len(c['configs'])))")
    s=s.replace(" for f in read(ROOT/'artifacts/study_v160/corpus_files.json'):assert sha(ROOT/'.native-v160/search_corpus'/f['path'])==f['sha256']\n",'')
    start=s.index(" cmd=[str(ROOT/'.venv/bin/python')");end=s.index(' except Exception as e:r.update',start)
    s=s[:start]+''' cmd=[str(ROOT/'.venv/bin/python'),str(ROOT/'scripts/worker_apps_v167.py'),'--engine',j['engine'],'--candidate',str(i)]
 try:
  import os
  from check_apps_v168 import check
  env={k:v for k,v in os.environ.items() if not k.startswith(('POLARS_','XGBOOST_','OMP_'))};env['PYTHONHASHSEED']='16801'
  p=subprocess.run(cmd,cwd=ROOT,env=env,capture_output=True,text=True,timeout=60);r.update(command=cmd,returncode=p.returncode,stderr=p.stderr,raw_stdout=p.stdout)
  if p.returncode:raise RuntimeError('Worker failed')
  raw=json.loads(p.stdout);assert raw['candidate']==i
  v,status=check(raw,j['engine'],c['configs'][i]);r.update(measurement=v,status=status,value=v['value'])
''' + s[end:]
    (R/'scripts/native_apps_v168.py').write_text(s)
    for stem in ['runtime_models','collect_models','run_apps']:
        s=(R/f'scripts/{stem}_v163.py').read_text().replace('V163','V168').replace('v163','v168');(R/f'scripts/{stem}_v168.py').write_text(s)
    c=json.loads((R/'configs/study_v163.json').read_text());c.update(ports={'smollm3_3b':18645,'qwen3_8b':18646},total_native_workload_invocations=1600)
    (R/'configs/study_v168.json').write_text(json.dumps(c,indent=2)+'\n')
if __name__=='__main__':main()
