"""Parser and pre-decision input checks only; no model responses fabricated as evidence."""
import sys,json
from pathlib import Path
import pytest
ROOT=Path(__file__).resolve().parents[2];sys.path.insert(0,str(ROOT/'scripts'))
from nginx_model_v112 import parse,prepare
from search_nginx_v111 import C,ROWS
from escalation.core import State
@pytest.mark.parametrize('text,valid',[
 ('[0,1,2,3,4,5,39]',True),('[0,1,2,3,4,5,5]',False),('[0,1,2,3,4,5,40]',False),
 ('[0,1,2,3,4,5]',False),('[true,1,2,3,4,5,6]',False),('Answer: [0,1,2,3,4,5,6]',False),
 ('[0.0,1,2,3,4,5,6]',False),('null',False)])
def test_parser(text,valid):
 assert (parse(dict(content=text,truncated=False,stop_type='eos',tokens_predicted=20)) is not None)==valid
@pytest.mark.parametrize('change',[{'truncated':True},{'stop_type':'limit'},{'tokens_predicted':129}])
def test_metadata(change):
 assert parse(dict(content='[0,1,2,3,4,5,6]',truncated=False,stop_type='eos',tokens_predicted=20)|change) is None

def test_prefix_only_and_deterministic():
 s=State(list(range(768)))
 for i in range(10):s.observe(i,[float(i+1)],('-',))
 a=prepare(C,s,ROWS,23);b=prepare(C,s,ROWS,23)
 assert a==b and a['observed_row_ids']==list(range(10)) and a['observed_labels']==[[float(i+1)] for i in range(10)]
 assert len(set(a['shortlist_row_ids']))==40 and not set(a['shortlist_row_ids'])&set(s.ids)
 assert set(a)=={'messages','shortlist_row_ids','observed_row_ids','observed_labels','seed'}
 assert len(s.ids)==10
