import importlib.util,json
from pathlib import Path
P=Path(__file__).resolve().parents[2]/'scripts/prepare_sensitivity_v48.py'
spec=importlib.util.spec_from_file_location('v48',P);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
def fixture():
    body={'feature_order':['x'],'symbol_to_value':[[10,20]],'observations':[{'x':'0','loss':0.12345}],
        'candidates':[{'id':c,'x':str(i%2)} for i,c in enumerate(m.IDS)]}
    return [{'role':'system','content':'select'},{'role':'user','content':'header\n'+json.dumps(body)}],{'mapping':{c:i for i,c in enumerate(m.IDS)}}
def test_reversal_preserves_ID_to_row_mapping():
    messages,pool=fixture();out,mapping,display,_=m.transform(messages,pool,'symbols','observed','reverse')
    assert mapping==pool['mapping'] and display==list(reversed(m.IDS))
    assert json.loads(out[1]['content'].split('\n')[1])['candidates'][0]['id']=='J'
def test_relabel_preserves_feature_display_order_but_changes_mapping():
    messages,pool=fixture();out,mapping,display,_=m.transform(messages,pool,'symbols','observed','relabel')
    assert mapping['A']==0 and mapping['0']==10
    assert [mapping[c] for c in display]==list(range(20))
def test_loss_removal_does_not_leave_numeric_loss_in_model_input():
    messages,pool=fixture()
    for representation in ('symbols','values'):
        out,_,_,_=m.transform(messages,pool,representation,'withheld','base')
        assert '0.12345' not in out[1]['content']
def test_values_decode_original_settings():
    messages,pool=fixture();out,_,_,_=m.transform(messages,pool,'values','observed','base')
    assert '0 settings=[10]' in out[1]['content'] and '1 settings=[20]' in out[1]['content']
    assert 'loss=0.12345' in out[1]['content']
