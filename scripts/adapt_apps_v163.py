"""Generate a versioned adaptation of the already tested V159 collector before freeze."""
from pathlib import Path
import json
R=Path(__file__).resolve().parents[1]
s=(R/'scripts/native_solvers_v159.py').read_text().replace('study_v159','study_v163').replace('v159_native','v163_native').replace('v159_models','v163_models').replace('159000','163000').replace('159002','163002').replace('159200','163200').replace('159700','163700').replace('159701','163701').replace('159900','163900').replace('Random(159)','Random(163)')
s=s.replace('from solver_worker_v157 import valid_queens','')
s=s.replace("ENGINES=['cvc5','ortools']","ENGINES=['ripgrep','hnswlib']")
a=s.index('def candidates(engine):');b=s.index('\ndef choose(',a)
s=s[:a]+"""def candidates(engine):
 cs=read(ROOT/'artifacts/study_v162/candidates.json')[engine];names=list(cs[0]);ds=[list(dict.fromkeys(c[n] for c in cs)) for n in names]
 ix=[[d.index(c[n]) for n,d in zip(names,ds)] for c in cs]
 return {'names':names,'domains':ds,'grid_domains':[list(range(len(d))) for d in ds],'raw_features':[[c[n] for n in names] for c in cs],'indices':ix,'x':[[v/(len(d)-1) for v,d in zip(row,ds)] for row in ix],'configs':cs}
""" +s[b:]
a=s.index('def messages(engine,c,s):');b=s.index('\ndef guard(',a)
s=s[:a]+"""def messages(engine,c,s):
 width=len(c['names'])
 task={'ripgrep':'Complete five fixed keyword-count queries over a fixed 3407-file CPython source tree. All file counts must be exact. Minimize total elapsed time for all five queries, including native process launch and count emission. Every setting does the same work.','hnswlib':'Build an approximate nearest-neighbor index over 3823 real 64-dimensional Optdigits vectors, then query 1797 vectors for ten neighbors each, squared L2 distance. Fixed seed100 and single-thread index construction. Minimize build plus query elapsed time, subject to mean tie-aware recall at least95%. Quality-infeasible results receive a fixed20second utility penalty; this is not a measured successful runtime.'}[engine]
 return [{'role':'system','content':f'Optimize {engine} configuration from ten acquired outcomes. Return a JSON array of ten {width}-digit strings ordered most promising first. Each digit indexes the listed values for its feature. Avoid duplicate proposals and propose diverse promising settings. Only the first seven projected unseen settings will be measured; three remaining evaluations are reserved for fresh validation of the best observed setting.'},{'role':'user','content':json.dumps({'feature_order':c['names'],'indexed_values':c['domains'],'observed_examples':[{'settings':c['raw_features'][i],'loss_seconds':v[0]} for i,v in zip(s['ids'],s['labels'])],'objective':task,'direction':'minimize','projection':'Normalized ordinal-coordinate L1 nearest unseen setting; seeded order breaks ties.'},separators=(',',':'))}]
""" +s[b:]
s=s.replace("read(ROOT/'results/v158_solvers/summary.json')","read(ROOT/'results/v162_apps/summary.json')")
s=s.replace("'scripts/native_solvers_v159.py','scripts/run_solvers_v159.py','scripts/collect_models_v159.py','scripts/runtime_models_v159.py','scripts/solver_worker_v157.py'","'scripts/native_apps_v163.py','scripts/run_apps_v163.py','scripts/collect_models_v163.py','scripts/runtime_models_v163.py','scripts/app_worker_v162.py','scripts/app_worker_v161.py','scripts/app_feasibility_v162.py'")
s=s.replace("'reports/protocol_v159.md','configs/study_v163.json'","'reports/protocol_v163.md','configs/study_v163.json'")
s=s.replace("'tests/synthetic/test_solvers_v159.py'","'tests/synthetic/test_apps_v163.py'")
s=s.replace("'artifacts/study_v163/candidates/cvc5.json','artifacts/study_v163/candidates/ortools.json','artifacts/study_v158/freeze.json','results/v158_solvers/summary.json','configs/solvers_v156.lock.txt'","'artifacts/study_v163/candidates/ripgrep.json','artifacts/study_v163/candidates/hnswlib.json','artifacts/study_v162/freeze.json','results/v162_apps/summary.json','artifacts/study_v162/query_references.json','artifacts/study_v160/ann_train.f32','artifacts/study_v160/ann_query.f32','artifacts/study_v160/ann_kth_squared.npy','artifacts/study_v160/corpus_files.json','.native-v160/bin/hnsw_worker_v161','.native-v160/ripgrep-15.2.0-aarch64-apple-darwin/rg','.local-runtime/llama-b11146/llama-server'")
s=s.replace("['total_collection_seconds_cap']-20","['total_collection_seconds_cap']-60")
a=s.index(" cmd=[str(ROOT/'.venv-solvers156/bin/python')");b=s.index(" except Exception as e:r.update",a)
s=s[:a]+""" cmd=[str(ROOT/'.venv/bin/python'),str(ROOT/'scripts/app_worker_v162.py'),'--engine',j['engine'],'--config',json.dumps(c['configs'][i])]
 try:
  p=subprocess.run(cmd,cwd=ROOT,capture_output=True,text=True,timeout=60);r.update(command=cmd,returncode=p.returncode,stderr=p.stderr)
  if p.returncode:raise RuntimeError('Worker failed')
  v=json.loads(p.stdout);r['measurement']=v
  if v['engine']!=j['engine'] or v['config']!=c['configs'][i]:raise ValueError('Wrong measurement identity')
  if v['correct'] and v['quality']>=.95 and v['value']==v['objective_seconds']:r.update(status='correct',value=v['value'])
  elif j['engine']=='hnswlib' and v['correct'] and v['quality']<.95 and v['value']==20.:r.update(status='quality_penalty',value=20.)
  else:raise ValueError('Incorrect/unsupported application result')
""" +s[b:]
s=s.replace("guard();O.mkdir(exist_ok=False)","guard();\\n for f in read(ROOT/'artifacts/study_v160/corpus_files.json'):assert sha(ROOT/'.native-v160/search_corpus'/f['path'])==f['sha256']\\n O.mkdir(exist_ok=False)".replace('\\n','\n'))
(R/'scripts/native_apps_v163.py').write_text(s)
s=(R/'scripts/runtime_models_v159.py').read_text().replace('V159 bounded native solver inference','V163 bounded native application inference').replace('study_v159','study_v163');(R/'scripts/runtime_models_v163.py').write_text(s)
s=(R/'scripts/collect_models_v159.py').read_text().replace('runtime_models_v159','runtime_models_v163').replace('study_v159','study_v163').replace('v159_models','v163_models').replace('v159_native','v163_native').replace('native_solvers_v159','native_apps_v163').replace("'total_seconds_cap':3600","'total_seconds_cap':1800").replace('>2200','>1000');(R/'scripts/collect_models_v163.py').write_text(s)
s=(R/'scripts/run_solvers_v159.py').read_text().replace('study_v159','study_v163').replace('native_solvers_v159','native_apps_v163').replace('collect_models_v159','collect_models_v163').replace('3580','1740').replace('3600','1800');(R/'scripts/run_apps_v163.py').write_text(s)
c=json.loads((R/'configs/study_v159.json').read_text());c.update(total_collection_seconds_cap=1800,ports={'smollm3_3b':18635,'qwen3_8b':18636},total_native_workload_invocations=2400)
(R/'configs/study_v163.json').write_text(json.dumps(c,indent=2)+'\n')
s=(R/'tests/synthetic/test_solvers_v159.py').read_text().replace('native_solvers_v159','native_apps_v163').replace('runtime_models_v159','runtime_models_v163').replace("'cvc5'","'hnswlib'").replace("'ortools'","'ripgrep'").replace("'feature_order'])==6","'feature_order'])==4").replace("[[9]*5]*10","[[9]*4]*10")
(R/'tests/synthetic/test_apps_v163.py').write_text(s)
