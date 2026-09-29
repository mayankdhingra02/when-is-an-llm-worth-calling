"""Synthetic fixtures only. Excluded from measured research aggregates."""
import csv,itertools,json
from pathlib import Path
import pytest
from escalation.finite_domain import FiniteCandidates
from escalation.finite_v6 import load_candidates,LazyOracle,parse_symbols,symbols,messages,features
from escalation.grammar_v6 import FiniteSymbolsGrammar
from escalation.core import State,initial_state
from escalation.finite_domain import recommend
from escalation.data import sha
from escalation.provider_v6 import FiniteProvider
from escalation.io import digest

class Tokenizer:
    eos_token_id=1000
    def encode(self,s,**kwargs):return [ord(c) for c in s]
    def decode(self,ids):return ''.join(chr(v) for v in ids)

def fixture(tmp_path,other='unread-invalid',direction='-'):
    p=tmp_path/'table.csv';rows=list(itertools.product(range(3),repeat=3))
    with p.open('w',newline='') as f:
        w=csv.writer(f);w.writerow(['a','b','c','target','other','revision'])
        for i,row in enumerate(rows):w.writerow([*row,i+1,other,'v1'])
    return {'path':str(p),'sha256':sha(p),'delimiter':',','feature_names':['a','b','c'],'objective_columns':['target','other'],
      'metadata_columns':['revision'],'primary_objective':'target','direction':direction,'filters':{'revision':'v1'},'rows':27,'duplicates':0}

def test_lazy_boundary_and_inclusive_budget(tmp_path):
    spec=fixture(tmp_path);c=load_candidates(spec);events=[];o=LazyOracle(spec,c,journal=events.append)
    for i in range(20):assert o.acquire(i)==[i+1]
    assert len(events)==o.new_accesses==20
    with pytest.raises(RuntimeError):o.acquire(20)
    with pytest.raises(ValueError):o.acquire(0)
    assert o.new_accesses==20

def test_unacquired_target_never_parsed(tmp_path):
    spec=fixture(tmp_path);p=Path(spec['path']);rows=list(csv.reader(p.open()));rows[-1][3]='hidden bad target'
    with p.open('w',newline='') as f:csv.writer(f).writerows(rows)
    spec['sha256']=sha(p);c=load_candidates(spec);events=[];o=LazyOracle(spec,c,journal=events.append)
    assert o.acquire(0)==[1]
    with pytest.raises(ValueError):o.acquire(26)
    assert o.new_accesses==len(events)==2
    with pytest.raises(ValueError):o.acquire(26)

def test_finite_prompt_invariant_to_hidden_outcomes(tmp_path):
    spec=fixture(tmp_path);c=load_candidates(spec);s=initial_state(c,11);o=LazyOracle(spec,c)
    for _ in range(10):
        i=recommend(c,s);s.observe(i,o.acquire(i),c.directions)
    before=messages(c,s);f=features(c,s,11)[0];p=Path(spec['path']);rows=list(csv.reader(p.open()))
    for i,row in enumerate(rows[1:]):
        if i not in s.ids:row[3]='999999'
        row[4]='another hidden target'
    with p.open('w',newline='') as file:csv.writer(file).writerows(rows)
    spec['sha256']=sha(p);other=load_candidates(spec)
    assert messages(other,s)==before and features(other,s,11)[0]==f
    assert '999999' not in str(before) and 'another hidden' not in str(before)

def test_pairs_restore_prefix_and_isolate(tmp_path):
    spec=fixture(tmp_path);c=load_candidates(spec);s=initial_state(c,11);o=LazyOracle(spec,c)
    for _ in range(10):
        i=recommend(c,s);s.observe(i,o.acquire(i),c.directions)
    frozen=digest(s.record());a=s.clone();b=s.clone();ao=LazyOracle(spec,c,prefix=s.record());bo=LazyOracle(spec,c,prefix=s.record())
    for state,oracle in [(a,ao),(b,bo)]:
        for _ in range(10):
            i=recommend(c,state);state.observe(i,oracle.acquire(i),c.directions)
    assert ao.new_accesses==bo.new_accesses==10 and a.record()==b.record()
    assert digest(s.record())==frozen

def test_symbols_and_grammar(tmp_path):
    c=load_candidates(fixture(tmp_path));raw='\n'.join(symbols(c,x) for x in c.x[:10]);assert parse_symbols(raw,c)==[list(x) for x in c.x[:10]]
    grammar=FiniteSymbolsGrammar(Tokenizer(),c.domains)
    assert len(grammar.choice_positions)==30
    for bad in [raw+'\nextra',raw.replace('2','3'),raw.replace('0',' '),raw.upper()+' ']:
        with pytest.raises(ValueError):parse_symbols(bad,c)
    # Mixed-size domains and forced constants stay within their exact token sets.
    g=FiniteSymbolsGrammar(Tokenizer(),[[0],[0,1,2],list(range(12))])
    assert len(g.choice_positions)==20 and g.schedule[0]==[ord('0')]
    with pytest.raises(ValueError):FiniteSymbolsGrammar(Tokenizer(),[list(range(63))])

def test_maximize_and_minimize(tmp_path):
    from escalation.evaluator import evaluate
    assert evaluate([[1],[2],[3]],('+',),[2])['loss']==0
    assert evaluate([[1],[2],[3]],('-',),[0])['loss']==0
    assert evaluate([[5],[5]],('+',),[0])['loss']==0

def test_semantic_manifest_groups_and_exposure():
    m=json.loads(Path('data/manifest_v6.json').read_text());ds=[d for d in m['datasets'] if d['selected']]
    assert len(ds)==len({d['system_group'] for d in ds})==6
    assert {d['system_group'] for d in ds}.isdisjoint({'apache','sqlite','x264'})
    assert sum(d['split']=='development' for d in ds)==sum(d['split']=='test' for d in ds)==3
    assert all(d['primary_objective'] not in d['feature_names'] for d in ds)
    assert all('revision' not in d['feature_names'] for d in ds)
    for d in m['datasets']:
        for path,h in d['evidence'].items():assert sha(path)==h
    assert next(d for d in m['datasets'] if d['id']=='OpenVPN')['direction']=='+'

def test_seal_fit_rejects_test_rows():
    from escalation.router import GainRouter
    with pytest.raises(ValueError):GainRouter().fit([{'split':'test'}])

def test_paid_guard():
    from escalation.config import load_config
    cfg=load_config('configs/followup_v3.yaml');cfg['inference']['allow_paid_api']=True
    with pytest.raises(ValueError):FiniteProvider(cfg,None,'unused')
