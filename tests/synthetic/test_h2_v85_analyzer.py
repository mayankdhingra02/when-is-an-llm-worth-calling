"""Independent analyzer exercises on isolated synthetic records, never research data."""
import csv,hashlib,io,json,sys,time
from pathlib import Path
from types import SimpleNamespace
import pytest
REPO=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(REPO/'scripts'))
import run_h2_v85 as collector
import analyze_h2_v85 as analyzer
from escalation.h2_v83 import expected,COLS
from escalation.h2_v85 import CONFIGS,PRIOR,SEEDS

def write(p,data):p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(data))

@pytest.fixture(scope='module')
def synthetic(tmp_path_factory):
    root=tmp_path_factory.mktemp('SYNTHETIC_H2_ANALYZER_ONLY')
    freeze=root/'reports/protocol_v85.freeze.json';write(freeze,{'sha256':{}});digest=hashlib.sha256(freeze.read_bytes()).hexdigest()
    write(root/'configs/study_v85.json',json.loads((REPO/'configs/study_v85.json').read_text()))
    write(root/'configs/runtime_v83.lock.json',dict(java='fixture-java',jar='fixture.jar',classes='fixture-classes'))
    write(root/'artifacts/study_v78/runtime_plan.json',{'command':['SYNTHETIC-NO-MODEL']})
    write(root/'artifacts/study_v85_execution/user_approval.json',dict(granted=True,frozen_scope_sha256=digest,max_generation_requests=35,max_physical_trials=115,max_stage_seconds=1800,max_new_download_bytes=0,max_external_spend_usd=0,user_message='SYNTHETIC FIXTURE ONLY, NOT USER APPROVAL'))
    prior_rows=[]
    for seed in SEEDS:
        obs=[]
        for i,cid in enumerate([PRIOR]+list(range(9))):
            obs.append(dict(config_id=cid,query_seconds=1.+i,physical_trial=len(prior_rows)))
            prior_rows.append(dict(seed=seed,arm='prefix',config_id=cid,metrics={'query_seconds':1.+i},process={'wall_seconds':12.},decision_seconds=.001))
        write(root/f'results/v84_h2_classical/prefix_{seed}.json',{'observations':obs})
    write(root/'results/v84_h2_classical/acquisitions.json',prior_rows)
    truth=expected();buf=io.StringIO();w=csv.writer(buf);w.writerow(['round','query','parameter','count','sum'])
    for r in range(128):
        for q in range(3):
            for t in range(16):w.writerow([r,q,t,*truth[q,t]])
    answers=buf.getvalue()
    class FakeRuntime:
        def __init__(self,root,out,cfg,**kwargs):
            self.out=out;self.reason=None;self.proc=SimpleNamespace(poll=lambda:None);self.ledger=dict(generation_requests=0,http_requests=1,retries=0,external_spend_usd=0,peak_server_rss_bytes=1,startup_seconds=.01)
        def check(self):pass
        def start(self):write(self.out/'runtime.json',{'command':['SYNTHETIC-NO-MODEL']})
        def close(self):self.ledger.update(seconds=1000.,resource_stop_reason=None,server_exit_code=0);write(self.out/'ledger.json',self.ledger)
        def api(self,route,payload):
            self.ledger['http_requests']+=1
            if route=='/apply-template':return {'prompt':'\n'.join(m['content'] for m in payload['messages'])}
            assert route=='/tokenize';return {'tokens':[1]*100}
        def generate(self,payload,folder):
            self.ledger['http_requests']+=1;self.ledger['generation_requests']+=1
            write(folder/'attempt_started.json',dict(generation_number=self.ledger['generation_requests'],started_at_unix=time.time()))
            return dict(content=json.loads(payload['grammar'].removeprefix('root ::= ').split(' | ')[0]),tokens_predicted=10,tokens_evaluated=100)
    def fake_native(command,**kwargs):
        p=Path(kwargs['log_path']).parent;c=dict(mask=int(command[-4]),recompile=command[-3]=='true',analyze_sample=int(command[-2]))
        (p/'answers.csv').write_text(answers)
        (p/'settings.txt').write_text('ANALYZE_AUTO=0\nQUERY_CACHE_SIZE=8\nRECOMPILE_ALWAYS='+str(c['recompile']).lower()+'\nOPTIMIZE_REUSE_RESULTS_ENGINE=false\n')
        (p/'indexes.csv').write_text(''.join(f'IDX{i},{col},{j}\n' for i in range(6) if c['mask']&(1<<i) for j,col in enumerate(COLS[i].split(','),1)))
        metrics=dict(version='2.3.232',rows=100000,scored_queries=6144,warmup_queries=1536,query_seconds=.5+CONFIGS.index(c)/100,index_and_analyze_seconds=.01,harness_seconds=5.,**c);write(p/'metrics.json',metrics)
        return dict(exit_code=0,termination_reason=None,wall_seconds=6.,sampled_maxima={'rss_bytes':1,'scratch_bytes':1})
    with pytest.MonkeyPatch.context() as patch:
        patch.setattr(collector,'ROOT',root);patch.setattr(collector,'OUT',root/'results/v85_h2_paired');patch.setattr(collector,'Runtime',FakeRuntime);patch.setattr(collector,'rss',lambda _:0);patch.setattr(collector,'run',fake_native)
        patch.setattr(sys,'argv',['SYNTHETIC','--approved-envelope-sha256',digest]);collector.main()
    return root

def test_full_frozen_analyzer_on_synthetic_records(synthetic,monkeypatch):
    monkeypatch.setattr(analyzer,'ROOT',synthetic);result=analyzer.analyze()
    assert result['generation_requests']==35 and result['new_physical_trials']==115 and result['checked_scored_answers']==706560
    assert all([c['arms'][a]['logical_evaluations'] for a in ['rf_lcb','llm','prior']]==[20,20,3] for c in result['cases'])

@pytest.mark.parametrize('corrupt',['denominator','branch_prefix','prompt_leak','illegal_response','wrong_query_answer'])
def test_analyzer_rejects_semantic_corruption(synthetic,monkeypatch,corrupt):
    monkeypatch.setattr(analyzer,'ROOT',synthetic);raw=synthetic/'results/v85_h2_paired'
    paths={'denominator':raw/'summary.json','branch_prefix':raw/'cases.json','prompt_leak':raw/'request_11_1/messages.json','illegal_response':raw/'request_11_1/response.json','wrong_query_answer':raw/'trial_000/answers.csv'}
    path=paths[corrupt];original=path.read_bytes()
    try:
        if corrupt=='wrong_query_answer':
            lines=path.read_text().splitlines();fields=lines[1].split(',');fields[-1]=str(int(fields[-1])+1);lines[1]=','.join(fields);path.write_text('\n'.join(lines)+'\n')
        else:
            data=json.loads(original)
            if corrupt=='denominator':data['charged_trials']=114
            elif corrupt=='branch_prefix':data[0]['branches']['llm'][0]['query_seconds']+=1
            elif corrupt=='prompt_leak':data[1]['content']+=' SYNTHETIC_HIDDEN_LABEL=999'
            else:data['content']='[0,0,0]'
            write(path,data)
        with pytest.raises(AssertionError):analyzer.analyze()
    finally:path.write_bytes(original)
