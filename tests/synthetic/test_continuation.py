"""Fabricated provider ONLY for logic tests, under pytest temporary directories."""
import json
from types import SimpleNamespace
from escalation.core import initial_state
from escalation.data import Oracle
from escalation.runner import acquire
from escalation.llm import continue_llm
from test_integrity import fixture

class FakeProvider:
    def __init__(self,path,valid):
        self.resources=SimpleNamespace(check=lambda:None);self.cfg={'inference':{'max_retries_per_request':1}};self.log=path/'synthetic_requests.jsonl';self.valid=valid;self.calls=0
    def request(self,messages,context):
        self.calls+=1
        return {'request_id':self.calls,'status':'response','raw_output':json.dumps({'candidates':[[0]*5,[1]*5]}) if self.valid else 'invalid fixture'}

def test_all_malformed_falls_back_without_free_labels(tmp_path):
    c,y=fixture();s=initial_state(c,11);o=Oracle(y);acquire(c,s,o,'ezr_centroid_adapted',10)
    p=FakeProvider(tmp_path,False);e=continue_llm(c,s,o,p,{},tmp_path/'synthetic_checkpoint.json')
    assert p.calls==10 and len(e)==10 and all(x['fallback'] for x in e) and o.new_accesses==20

def test_duplicate_proposals_still_charge_distinct_projected_rows(tmp_path):
    c,y=fixture();s=initial_state(c,11);o=Oracle(y);acquire(c,s,o,'ezr_centroid_adapted',10)
    p=FakeProvider(tmp_path,True);e=continue_llm(c,s,o,p,{},tmp_path/'synthetic_checkpoint.json')
    assert p.calls==5 and o.new_accesses==20 and len(set(s.ids))==20 and any(x['duplicate'] for x in e)
