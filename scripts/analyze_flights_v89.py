"""Frozen all-setting analysis, revalidating every answer and acquisition."""
import hashlib,json,math,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'src'))
from escalation.flights_v89 import CONFIGS,BASELINE,LIMIT,SCORED,WARMUP,CHECKED,schedule,comparison
from escalation.flights_v88 import QUERIES,validate_answer
RAW=ROOT/'results/v89_flights_grid';OUT=ROOT/'results/v89_flights_analysis'
def read(p):return json.loads(p.read_text())
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
    f=read(ROOT/'reports/protocol_v89.freeze.json')
    for n,d in f['sha256'].items():assert sha(ROOT/n)==d,n
    summary=read(RAW/'summary.json');rows=read(RAW/'acquisitions.json');assert summary['complete'] and summary['valid_trials']==summary['charged_trials']==len(rows)==LIMIT and summary['failed_trials']==summary['unattempted_trials']==summary['new_model_calls']==0 and summary['seconds']<900
    contract=read(ROOT/'data/flights_v88/query_contract.json');values={i:[] for i in range(16)};plans={i:set() for i in range(16)};perquery=[]
    for idx,(row,item) in enumerate(zip(rows,schedule())):
        folder=RAW/f'trial_{idx:02d}';i=item['configuration_index'];cfg=CONFIGS[i]
        assert all(row[k]==v for k,v in item.items()) and row['trial']==idx and row['configuration']==cfg and row['status']=='valid' and row['at_unix']>=f['at_unix']
        charge=read(folder/'charge.json');assert charge['status']=='charged' and all(row[k]==v for k,v in charge.items() if k!='status')
        assert row['command']==[row['command'][0],str(ROOT/'scripts/worker_flights_v89.py'),'--config',str(i),'--out',str(folder)]
        process=read(folder/'process_receipt.json');assert process==row['process'] and process['exit_code']==0 and process['termination_reason'] is None and process['wall_seconds']<60 and process['sampled_maxima']['rss_bytes']<=2*1024**3 and process['sampled_maxima']['scratch_bytes']<=1024**3
        result=read(folder/'result.json');assert result==row['result'] and result['configuration']==cfg and result['scored_queries']==SCORED*3 and result['checked_queries']==CHECKED
        settings=read(folder/'settings.json');assert settings['threads']==str(cfg['threads']) and set(filter(None,settings['disabled_optimizers'].split(',')))==set(filter(None,cfg['disabled_optimizers'].split(','))) and settings['memory_limit']=='512.0 MiB'
        assert all(settings[k]=='false' for k in ['enable_external_access','autoinstall_known_extensions','autoload_known_extensions'])
        answers=read(folder/'answers.json');assert len(answers)==CHECKED and sha(folder/'answers.json')==result['answers_sha256']
        for j,a in enumerate(answers):
            assert a['repetition']==j//3 and a['query']==list(QUERIES)[j%3] and a['scored']==(j//3>=WARMUP) and math.isfinite(a['seconds']) and a['seconds']>0
            validate_answer(a['query'],a['columns'],a['rows'],contract['expected']['answers'][a['query']])
        assert sum(a['seconds'] for a in answers if a['scored'])==result['query_seconds'];values[i].append(result['query_seconds'])
        plan=read(folder/'plans.json');plans[i].add(hashlib.sha256(json.dumps(plan,sort_keys=True).encode()).hexdigest())
        for q in QUERIES:perquery.append({'trial':idx,'block':item['block'],'config':cfg['name'],'query':q,'seconds':sum(a['seconds'] for a in answers if a['scored'] and a['query']==q)})
    results=[{'configuration':c,**comparison(values[i],values[BASELINE]),'plan_fingerprints':sorted(plans[i])} for i,c in enumerate(CONFIGS)]
    report={'scope':'Exploratory exposed-workload classical grid; no model, held-out or optimizer comparison','physical_trials':LIMIT,'checked_queries':LIMIT*CHECKED,'scored_queries':LIMIT*SCORED*3,'native_seconds':summary['seconds'],'new_model_calls':0,'baseline':CONFIGS[BASELINE],'results':results,'qualified_configurations':[r['configuration']['name'] for r in results if r['qualified_descriptive_opportunity']],'distinct_observed_plan_fingerprints':len(set.union(*plans.values())),'max_sampled_rss_bytes':max(r['process']['sampled_maxima']['rss_bytes'] for r in rows)}
    OUT.mkdir(exist_ok=False);(OUT/'summary.json').write_text(json.dumps(report,indent=2)+'\n');(OUT/'per_query.json').write_text(json.dumps(perquery,indent=2)+'\n');print(json.dumps({k:v for k,v in report.items() if k!='results'},indent=2))
if __name__=='__main__':main()
