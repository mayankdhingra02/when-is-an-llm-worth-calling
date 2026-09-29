"""Freeze candidate-selection inputs before new label collection; no inference."""
import sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'src'))
from escalation.io import read,write,digest,now
from escalation.data import sha
from escalation.core import State
from escalation.finite_v6 import load_candidates
from escalation.selection_v8 import shortlist,messages,parse_ids
from escalation.grammar_v8 import CandidateIDGrammar
from escalation.study_v7 import verify
from transformers import AutoTokenizer

def main():
    freeze=Path('reports/protocol_v8.freeze.json')
    if freeze.exists():raise RuntimeError('refuse freeze overwrite')
    verify();old=read('data/manifest_v7.json')
    tok=AutoTokenizer.from_pretrained('models/Qwen2.5-0.5B-Instruct',local_files_only=True,trust_remote_code=False)
    cases=[];checks=[];inputs={}
    for d in old['datasets']:
        c=load_candidates(d);inputs[d['path']]=sha(d['path'])
        for seed in old['seeds']:
            k=d['id']+'_'+str(seed);p=read(f'results/v6/prefixes/{k}.json');s=State(**p['state']).clone()
            pool=shortlist(c,s,seed);msg=messages(c,s,pool);g=CandidateIDGrammar(tok);tokens=[]
            while len(tokens)<len(g.schedule):tokens.append(g.allowed_after(tokens)[0])
            g.replay(tokens);assert len(set(parse_ids(tok.decode(tokens,skip_special_tokens=True),pool)))==10
            text=tok.apply_chat_template(msg,tokenize=False,add_generation_prompt=True);n=len(tok.encode(text,add_special_tokens=False))
            assert n+len(g.schedule)<=32768 and len(g.schedule)<=1024
            cases.append({'dataset':d['id'],'seed':seed,'prefix_hash':p['prefix_hash'],'pool':pool,'prompt_sha256':digest(msg)})
            checks.append({'dataset':d['id'],'seed':seed,'namespace':'synthetic_token_traversal_no_inference','input_tokens':n,'grammar_tokens':len(g.schedule),'choice_positions':len(g.choice_positions),'valid':True})
            for part in ['prefixes','classical','paired']:
                path=f'results/v6/{part}/{k}.json';inputs[path]=sha(path)
            path=f'results/v7/llm/{k}.json';inputs[path]=sha(path)
    write('data/manifest_v8.json',{'version':8,'scope':'development only; fixed candidate selection','datasets':old['datasets'],'seeds':old['seeds'],'cases':cases,'reused_inputs':inputs})
    write('artifacts/study_v8/tokenizer_preflight.json',{'passed':True,'checks':checks,'real_model_calls':0})
    paths=list(Path('src/escalation').glob('*.py'))+list(Path('tests/synthetic').glob('*.py'))+[Path(p) for p in ['scripts/prepare_v8.py','reports/protocol_v8.md','data/manifest_v8.json','data/manifest_v7.json','configs/followup_v3.yaml','requirements.lock.txt','artifacts/study_v8/tokenizer_preflight.json']]+[Path(p) for p in inputs]
    write(freeze,{'at':now(),'scope':'fixed scientific treatment; authorization separately recorded default denied','sha256':{str(p):sha(p) for p in sorted(set(paths))}})
    print('Frozen',len(set(paths)),'files; fifteen real-tokenizer checks passed; zero inference')
if __name__=='__main__':main()
