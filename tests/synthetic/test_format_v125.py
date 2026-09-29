"""Synthetic format intervention isolation; never experimental responses."""
import json,sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[2]/'scripts'))
from surrogate_v124 import messages as original
from format_probe_v125 import messages

def prefix():
 b={'feature_order':['switch','size'],'symbol_to_value':[[0,1],[1,2]],'observations':[{'x':'00','loss':i/9} for i in range(10)],'candidates':[{'id':i,'x':'11'} for i in '0123456789ABCDEFGHIJ']}
 return {'messages':[{}, {'content':'preamble\n'+json.dumps(b)}],'state':{'labels':[[20.+i] for i in range(10)]}}

def test_markers_are_only_json_change():
 p=prefix();a=original(p,'0','runtime');b=messages(p,'0','runtime','marked_json');assert a[0]==b[0];user=json.loads(a[1]['content'])
 for o in user['observed_examples']:o['performance']='## '+o['performance']+' ##'
 assert json.loads(b[1]['content'])==user

def test_reference_text_has_demonstrations_and_exact_query():
 p=prefix();p['unacquired_targets']=object();m=messages(p,'0','runtime','reference_text');s=m[1]['content']
 assert s.count('Performance: ## ')==10 and 'Performance: ## 22.000000 ##' in s
 assert s.endswith('Hyperparameter configuration: switch is 1, size is 2\nPerformance: ')
 assert 'normalized' not in s and 'candidate' not in s
