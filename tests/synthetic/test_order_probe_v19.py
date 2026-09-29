"""Synthetic intervention and permission guards; no fake measured responses."""
import copy,importlib.util,json
from pathlib import Path
import pytest
from escalation.order_probe_v19 import IDS,transform,inspect_response,authorization_config,StageResources
from escalation.resources import LimitReached

def fixture():
    candidates=[{'id':i,'x':f'feature-{i}'} for i in IDS]
    messages=[{'role':'system','content':'synthetic fixture'},{'role':'user','content':'intro\n'+json.dumps({'observations':[{'x':'seen','loss':.5}],'candidates':candidates},separators=(',',':'))}]
    return messages,{'mapping':dict(zip(IDS,range(20)))}

def test_original_is_byte_identical_and_interventions_do_not_mutate_input():
    messages,pool=fixture();before=copy.deepcopy(messages)
    assert transform(messages,pool,'original')['messages']==messages
    for mode in ['reverse_display','reverse_ids']:
        changed=transform(messages,pool,mode)
        body=json.loads(changed['messages'][-1]['content'].split('\n',1)[1])
        assert body['observations']==[{'x':'seen','loss':.5}]
        assert set(changed['mapping'].values())==set(range(20))
    assert messages==before

def test_display_reversal_keeps_feature_to_id_binding():
    messages,pool=fixture();changed=transform(messages,pool,'reverse_display')
    assert changed['mapping']==pool['mapping'] and changed['display_ids']==list(reversed(IDS))
    body=json.loads(changed['messages'][-1]['content'].split('\n',1)[1])
    assert [r['x'] for r in body['candidates']]==[f'feature-{i}' for i in reversed(IDS)]

def test_relabeling_keeps_feature_order_and_changes_binding():
    messages,pool=fixture();changed=transform(messages,pool,'reverse_ids')
    body=json.loads(changed['messages'][-1]['content'].split('\n',1)[1])
    assert [r['x'] for r in body['candidates']]==[f'feature-{i}' for i in IDS]
    assert changed['mapping']['J']==0 and changed['mapping']['0']==19
    synthetic=inspect_response('\n'.join(IDS[:10]),changed)
    assert synthetic['low_ids_set'] and not synthetic['first_display_half_set']
    assert synthetic['selected_rows']==list(range(19,9,-1))

def test_bad_selection_is_rejected_not_filled_with_fake_output():
    job=transform(*fixture(),'original')
    with pytest.raises(ValueError):inspect_response('0\n'*10,job)
    with pytest.raises(ValueError):inspect_response('invalid',job)

def test_only_exact_explicit_request_increase_is_accepted():
    base={'inference':{},'resources':{'max_experiment_runtime_minutes':30}}
    auth={'granted':False,'request_cap':128}
    with pytest.raises(PermissionError):authorization_config(base,auth)
    auth={'granted':True,'request_cap':137,'additional_requests':9,'user_authorization':'synthetic authorization fixture','runtime_cap_seconds':1800,'external_spend_usd':0}
    assert authorization_config(base,auth)['inference']['max_new_model_requests']==137
    for key,value in [('request_cap',138),('additional_requests',10),('runtime_cap_seconds',1900),('external_spend_usd',1),('user_authorization','')]:
        wrong=dict(auth,**{key:value})
        with pytest.raises(ValueError):authorization_config(base,wrong)

def test_expired_stage_stops_before_reserving_request():
    class FakeResources:
        def remaining(self):return 50
        def request(self):raise AssertionError('Must not reserve request')
    stage=StageResources(FakeResources(),-1)
    with pytest.raises(LimitReached):stage.request()

def test_unapproved_runner_never_creates_model_or_measured_directory(monkeypatch):
    spec=importlib.util.spec_from_file_location('test_runner_v19',Path('scripts/run_order_v19.py'));module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
    written=[]
    monkeypatch.setattr(module,'read',lambda p:{'granted':False} if 'authorization' in str(p) else {'requests':128,'active_since':None,'experiment_seconds':1745})
    monkeypatch.setattr(module,'load_config',lambda p:{})
    monkeypatch.setattr(module,'write',lambda p,d:written.append(str(p)))
    assert module.run()==2
    assert written==['artifacts/study_v19/preflight.json']
