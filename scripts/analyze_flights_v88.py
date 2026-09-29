"""Recheck all retained DuckDB answers, settings, charges and timing sums."""
import hashlib,json,math,statistics,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'src'))
from escalation.flights_v88 import CONFIGS,QUERIES,validate_answer

def read(p):return json.loads(p.read_text())
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
    raw=ROOT/'results/v88_flights_feasibility';summary=read(raw/'summary.json');rows=read(raw/'acquisitions.json');freeze=read(ROOT/'reports/protocol_v88.freeze.json')
    for n,d in freeze['sha256'].items():assert sha(ROOT/n)==d,n
    assert summary['complete'] and summary['valid_trials']==summary['charged_trials']==len(rows)==9 and summary['failed_trials']==summary['unattempted_trials']==summary['new_model_calls']==0 and summary['seconds']<900
    contract=read(ROOT/'data/flights_v88/query_contract.json');results=[]
    for idx,row in enumerate(rows):
        folder=raw/f'trial_{idx:02d}';rep=idx//3;i=(rep+idx%3)%3;assert row['trial']==idx and row['repetition']==rep and row['configuration_index']==i and row['configuration']==CONFIGS[i] and row['status']=='valid'
        charge=read(folder/'charge.json');assert charge['status']=='charged' and all(row[k]==v for k,v in charge.items() if k!='status')
        expected=[row['command'][0],str(ROOT/'scripts/worker_flights_v88.py'),'--config',str(i),'--out',str(folder)];assert row['command']==expected
        process=read(folder/'process_receipt.json');assert process==row['process'] and process['exit_code']==0 and process['termination_reason'] is None and process['wall_seconds']<60 and process['sampled_maxima']['rss_bytes']<=2*1024**3 and process['sampled_maxima']['scratch_bytes']<=1024**3
        result=read(folder/'result.json');assert result==row['result'] and result['configuration']==CONFIGS[i] and result['scored_suites']==16 and result['warmup_suites']==3
        settings=read(folder/'settings.json');assert settings['threads']==str(CONFIGS[i]['threads']) and settings['disabled_optimizers']==CONFIGS[i]['disabled_optimizers'] and settings['memory_limit']=='512.0 MiB'
        assert all(settings[k]=='false' for k in ['enable_external_access','autoinstall_known_extensions','autoload_known_extensions'])
        answers=read(folder/'answers.json');assert len(answers)==57 and sha(folder/'answers.json')==result['answers_sha256']
        for j,a in enumerate(answers):
            assert a['repetition']==j//3 and a['query']==list(QUERIES)[j%3] and a['scored']==(j//3>=3) and math.isfinite(a['seconds']) and a['seconds']>0
            validate_answer(a['query'],a['columns'],a['rows'],contract['expected']['answers'][a['query']])
        assert sum(a['seconds'] for a in answers if a['scored'])==result['query_seconds']
    for i,c in enumerate(CONFIGS):
        r=[row['result']['query_seconds'] for row in rows if row['configuration_index']==i];med=statistics.median(r);spread=(max(r)-min(r))/med
        results.append({'configuration':c,'seconds':r,'median_seconds':med,'range_over_median':spread,'precision_screen_pass':med>=.1 and spread<=.2})
    out=ROOT/'results/v88_flights_analysis';out.mkdir(exist_ok=False);report={'scope':'CC0 real-flight custom-query classical feasibility; no optimization, held-out or LLM claim','valid_physical_trials':9,'checked_queries':513,'scored_queries':432,'objective':'execute+fetch seconds summed over16 three-query suites; checking/serialization excluded','results':results,'native_stage_seconds':summary['seconds'],'new_model_calls':0}
    (out/'summary.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report,indent=2))
if __name__=='__main__':main()
