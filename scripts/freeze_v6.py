import sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'src'))
from escalation.io import read,write,now
from escalation.data import sha
from escalation.finite_v6 import load_candidates
from escalation.grammar_v6 import FiniteSymbolsGrammar
from transformers import AutoTokenizer

def main():
    path=ROOT/'reports/protocol_v6.freeze.json'
    if path.exists():raise RuntimeError('refuse overwrite')
    for old in ['reports/protocol_v4.freeze.json','reports/registry_v5.freeze.json']:
        for p,h in read(old)['sha256'].items():assert sha(p)==h,p
    m=read('data/manifest_v6.json');ledger=read('artifacts/resource_ledger_v2.json')
    assert ledger['requests']+32<=100 and ledger['experiment_seconds']<1800 and not ledger.get('active_since')
    tokenizer=AutoTokenizer.from_pretrained('models/Qwen2.5-0.5B-Instruct',local_files_only=True,trust_remote_code=False)
    checks=[]
    for d in m['datasets']:
        c=load_candidates(d);grammar=FiniteSymbolsGrammar(tokenizer,c.domains)
        checks.append({'dataset':d['id'],'selected':d['selected'],'rows':len(c.x),'features':len(c.names),'grammar_tokens':len(grammar.schedule),'free_choices':len(grammar.choice_positions)})
    for domains in [[[0,1,2]]*4,[[0,1]]*30]:FiniteSymbolsGrammar(tokenizer,domains)
    write('artifacts/study_v6/preflight.json',{'passed':True,'objective_values_inspected':False,'checks':checks,'request_plan':32,'remaining_requests':100-ledger['requests'],'remaining_runtime_seconds':1800-ledger['experiment_seconds']})
    paths=list(Path('src/escalation').glob('*.py'))+list(Path('tests/synthetic').glob('*.py'))+[Path(p) for p in ['data/manifest_v6.json','scripts/admit_v6.py','scripts/freeze_v6.py','reports/protocol_v6.md','configs/followup_v3.yaml','requirements.lock.txt','artifacts/study_v6/preflight.json']]
    write(path,{'frozen_at':now(),'scope':'six-family exploratory paired smoke; insufficient generalization evidence','sha256':{str(p):sha(p) for p in paths}})
    print('Frozen',len(paths),'files; preflight passed without objective reads')
if __name__=='__main__':main()
