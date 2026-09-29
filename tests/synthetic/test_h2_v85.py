import json
import pytest
from escalation.h2_v85 import messages,vectors,authorize,check_cfg
from escalation.legal_proposals_v66 import LegalProposals

def test_prompt_allowlist():
    obs=[dict(config_id=i,query_seconds=.4+i) for i in range(10)]
    enriched=[dict(o,other_branch=99999999,hidden_objective=-55555555,postdecision='LEAK') for o in obs]
    assert messages(obs)==messages(enriched)
    assert 'LEAK' not in json.dumps(messages(enriched))

def test_grammar_domain():
    session=LegalProposals(vectors(),list(range(10)),count=7);req=session.begin_request()
    assert len(req['eligible_ids'])==326
    result=session.finish_request('[0,0,0]');assert not result['valid']
    with pytest.raises(RuntimeError):session.begin_request()

@pytest.mark.parametrize('bad',['absent','digest','count','source'])
def test_no_unapproved_inference(bad):
    record={'granted':True,'frozen_scope_sha256':'abc','max_generation_requests':35,'max_physical_trials':115,'max_stage_seconds':1800,'max_new_download_bytes':0,'max_external_spend_usd':0,'user_message':'synthetic approval fixture'}
    if bad=='absent':record=None
    elif bad=='digest':record['frozen_scope_sha256']='other'
    elif bad=='count':record['max_generation_requests']=36
    else:record['user_message']=''
    with pytest.raises(PermissionError):authorize(record,'abc','abc')

def test_reject_paid_endpoint():
    cfg=dict(max_generation_requests=35,max_physical_evaluations=115,max_stage_seconds=1800,max_output_tokens=64,context_tokens=4096,host='remote.invalid',port=18492,retries=0,max_external_spend_usd=0,max_new_download_bytes=0,allow_paid_api=False)
    with pytest.raises(ValueError):check_cfg(cfg)

def test_zero_generation_preflight_cannot_send(tmp_path):
    import sys
    from pathlib import Path
    sys.path.insert(0,str(Path(__file__).resolve().parents[2]/'scripts'))
    from runtime_h2_v85 import Runtime
    rt=Runtime(tmp_path,tmp_path,{})
    with pytest.raises(PermissionError):rt.generate({'n_predict':64,'temperature':0,'stream':False},tmp_path)
    assert rt.ledger['generation_requests']==rt.ledger['http_requests']==0

def test_transport_attempt_is_charged(tmp_path,monkeypatch):
    import sys
    from pathlib import Path
    sys.path.insert(0,str(Path(__file__).resolve().parents[2]/'scripts'))
    from runtime_h2_v85 import Runtime
    rt=Runtime(tmp_path,tmp_path,{},generation_limit=1)
    def fail(*args,**kwargs):raise OSError('synthetic transport failure')
    monkeypatch.setattr(rt,'_send',fail)
    with pytest.raises(OSError):rt.generate({'n_predict':64,'temperature':0,'stream':False},tmp_path)
    assert rt.ledger['generation_requests']==1 and (tmp_path/'attempt_started.json').exists()
    with pytest.raises(PermissionError):rt.generate({'n_predict':64,'temperature':0,'stream':False},tmp_path)

@pytest.mark.parametrize('malformed',[False,True])
def test_collector_budgets_with_synthetic_transport(tmp_path,monkeypatch,malformed):
    """Entirely synthetic fixtures under pytest tmp_path; no model/native process."""
    import sys,hashlib
    from pathlib import Path
    from types import SimpleNamespace
    repo=Path(__file__).resolve().parents[2];sys.path.insert(0,str(repo/'scripts'))
    import run_h2_v85 as runner
    from escalation.h2_v85 import CONFIGS,PRIOR,SEEDS
    def write(p,x):p.parent.mkdir(exist_ok=True,parents=True);p.write_text(json.dumps(x))
    freeze=tmp_path/'reports/protocol_v85.freeze.json';write(freeze,{'sha256':{}});digest=hashlib.sha256(freeze.read_bytes()).hexdigest()
    write(tmp_path/'configs/study_v85.json',json.loads((repo/'configs/study_v85.json').read_text()))
    write(tmp_path/'configs/runtime_v83.lock.json',{'java':'fixture-java','jar':'fixture.jar','classes':'fixture-classes'})
    write(tmp_path/'artifacts/study_v85_execution/user_approval.json',{'granted':True,'frozen_scope_sha256':digest,'max_generation_requests':35,'max_physical_trials':115,'max_stage_seconds':1800,'max_new_download_bytes':0,'max_external_spend_usd':0,'user_message':'SYNTHETIC TEST ONLY'})
    for seed in SEEDS:write(tmp_path/f'results/v84_h2_classical/prefix_{seed}.json',{'observations':[{'config_id':cid,'query_seconds':1.+i,'physical_trial':i} for i,cid in enumerate([PRIOR]+list(range(9)))]})
    class FakeRuntime:
        def __init__(self,root,out,cfg,**kw):self.out=out;self.reason=None;self.proc=SimpleNamespace(poll=lambda:None);self.ledger={'generation_requests':0}
        def start(self):pass
        def close(self):self.ledger['seconds']=1.
        def check(self):pass
        def api(self,route,payload):
            if route=='/apply-template':return {'prompt':json.dumps(payload['messages'])}
            assert route=='/tokenize';return {'tokens':[1]*100}
        def generate(self,payload,folder):
            self.ledger['generation_requests']+=1
            raw='SYNTHETIC MALFORMED' if malformed else json.loads(payload['grammar'].removeprefix('root ::= ').split(' | ')[0])
            return {'content':raw,'tokens_predicted':10,'tokens_evaluated':100}
    def native(command,**kw):
        p=Path(kw['log_path']).parent;(p/'answers.csv').write_text('SYNTHETIC NOT MEASURED\n');return {'exit_code':0,'termination_reason':None,'wall_seconds':.01}
    monkeypatch.setattr(runner,'ROOT',tmp_path);monkeypatch.setattr(runner,'OUT',tmp_path/'results/v85_h2_paired');monkeypatch.setattr(runner,'Runtime',FakeRuntime);monkeypatch.setattr(runner,'rss',lambda _:0);monkeypatch.setattr(runner,'expected',lambda:{});monkeypatch.setattr(runner,'run',native);monkeypatch.setattr(runner,'validate',lambda p,c,t:{'query_seconds':.5+CONFIGS.index(c)/100})
    monkeypatch.setattr(sys,'argv',['synthetic','--approved-envelope-sha256',digest])
    if malformed:
        with pytest.raises(RuntimeError):runner.main()
    else:runner.main()
    summary=json.loads((runner.OUT/'summary.json').read_text())
    if malformed:
        assert not summary['complete'] and summary['ledger']['generation_requests']==1 and summary['unattempted_generation_requests']==34
    else:
        assert summary['complete'] and summary['charged_trials']==summary['valid_trials']==115 and summary['ledger']['generation_requests']==35
        cases=json.loads((runner.OUT/'cases.json').read_text())
        assert all(c['branches']['rf_lcb'][:10]==c['branches']['llm'][:10] for c in cases)
        assert all([len(c['branches'][a]) for a in ['rf_lcb','llm','prior']]==[20,20,3] for c in cases)
