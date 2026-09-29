"""Synthetic full-domain projection and charged runtime boundaries."""
import json,sys,copy,random
from pathlib import Path
import pytest
sys.path.insert(0,str(Path(__file__).resolve().parents[2]/'scripts'))
from proposal_v127 import domains,encode,messages,grammar,payload,check_payload,parse,project,random_proposals
from runtime_proposal_v127 import Runtime
XS=[tuple((i>>k)&1 for k in range(5)) for i in range(32)]
P={'ids':list(range(10)),'labels':[[float(i+1)] for i in range(10)],'order':list(range(32))}

def test_messages_only_read_acquired_values_and_features():
 p=copy.deepcopy(P);p['hidden_targets']=object();p['pool']=object();ds=domains(XS)
 normal=messages(['a','b','c','d','e'],XS,p,'runtime','-');body=json.loads(normal[1]['content'])
 assert 'hidden_targets' not in body and 'pool' not in body and len(body['observed_examples'])==10
 assert body['observed_examples'][0]=={'settings':encode(XS[0],ds),'performance':'1.000000'}
 rotated=json.loads(messages(['a','b','c','d','e'],XS,p,'runtime','-','rotated_labels')[1]['content'])
 assert [x['settings'] for x in body['observed_examples']]==[x['settings'] for x in rotated['observed_examples']]
 assert [x['performance'] for x in rotated['observed_examples']]==[x['performance'] for x in body['observed_examples']][1:]+['1.000000']
 assert P=={k:p[k] for k in P}

def test_projection_excludes_seen_and_previous_projections_without_labels():
 p=copy.deepcopy(P);p['labels']=object();proposals=[XS[0]]*10
 ids,d=project(proposals,XS,p)
 assert len(ids)==len(set(ids))==10 and not set(ids)&set(P['ids'])
 assert ids[0]==16 # one bit from0, ahead of other eligible rows at that distance
 assert all(x['matches_initial_observation'] for x in d)
 assert [x['repeated_proposal'] for x in d]==[False]+[True]*9
 assert d[0]['hamming_distance']==1

def test_projection_can_escape_old_pool_and_ties_follow_order():
 p=copy.deepcopy(P);p['pool']={'mapping':dict(zip('abcdefghij',range(10,20)))}
 ids,d=project([XS[31]]*10,XS,p)
 assert ids[0]==31 and ids[0] not in p['pool']['mapping'].values()
 rev=copy.deepcopy(p);rev['order']=list(reversed(p['order']));a,_=project([XS[0]]*10,XS,p);b,_=project([XS[0]]*10,XS,rev)
 assert a[0]==b[0]==16 and a!=b

def test_random_projection_is_reproducible_without_global_rng_change():
 before=random.getstate();ds=domains(XS);a=random_proposals(ds,127911);assert a==random_proposals(ds,127911);assert before==random.getstate()
 assert all(len(x)==5 and set(x)<={0,1} for x in a)

def response(content):return {'content':content,'tokens_predicted':100,'truncated':False,'stop_type':'eos'}
def test_strict_valid_proposal_decode_and_duplicates_preserved():
 r=response(json.dumps(['00000']*10));assert parse(r,domains(XS))==[(0,0,0,0,0)]*10

@pytest.mark.parametrize('content',['["00000"]','["22222"]'*10,json.dumps(['000000']*10),json.dumps([1]*10),'prefix'+json.dumps(['00000']*10)])
def test_invalid_proposals_rejected(content):
 with pytest.raises(ValueError):parse(response(content),domains(XS))

@pytest.mark.parametrize('changes',[{'truncated':True},{'truncated':None},{'stop_type':'limit'},{'tokens_predicted':513},{'tokens_predicted':None}])
def test_incomplete_response_rejected(changes):
 r=response(json.dumps(['00000']*10));r.update(changes)
 with pytest.raises(ValueError):parse(r,domains(XS))

def cfg():return {'allow_paid_api':False,'allow_cloud':False,'max_external_spend_usd':0,'retries':0,'max_generation_stage_seconds':1800,'scientific_request_cap':1,'compatibility_request_cap':0,'new_generation_request_cap':1,'max_allocated_output_tokens':512}
def test_cap_checked_before_request_and_transport_failure_charged(tmp_path):
 rt=Runtime(tmp_path,cfg());calls=[]
 def fail(*a):calls.append(a);raise OSError('synthetic transport failure')
 rt._send=fail
 with pytest.raises(OSError):rt.generate(payload('synthetic',127011,domains(XS)),'scientific','fixture')
 assert rt.ledger['generation_requests']==1 and rt.ledger['allocated_output_tokens']==512
 with pytest.raises(PermissionError):rt.generate(payload('synthetic',127011,domains(XS)),'scientific','fixture')
 assert len(calls)==1

@pytest.mark.parametrize('field,value',[('allow_paid_api',True),('allow_cloud',True),('max_external_spend_usd',1),('retries',1)])
def test_disallowed_provider_configuration(tmp_path,field,value):
 c=cfg();c[field]=value
 with pytest.raises(AssertionError):Runtime(tmp_path,c)

def test_payload_and_metadata_route_restrictions(tmp_path):
 p=payload('synthetic',127011,domains(XS));check_payload(p);p['n_predict']=513
 with pytest.raises(ValueError):check_payload(p)
 rt=Runtime(tmp_path,cfg())
 with pytest.raises(ValueError):rt.api('https://external.invalid/')
 assert grammar(domains(XS)).count('ws row')==10
