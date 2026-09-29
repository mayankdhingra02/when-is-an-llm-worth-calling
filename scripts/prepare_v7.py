"""Freeze development-only protocol and validate real-tokenizer exclusions."""
import sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'src'))
from escalation.io import read,write,lines,digest,now
from escalation.data import sha
from escalation.finite_v6 import load_candidates,messages,symbols
from escalation.core import State
from escalation.grammar_v7 import PrefixExcludingGrammar
from escalation.study_v6 import verify_freeze
from transformers import AutoTokenizer

def main():
    freeze=Path('reports/protocol_v7.freeze.json')
    if freeze.exists():raise RuntimeError('refuse overwrite')
    verify_freeze();old=read('data/manifest_v6.json');ds=[d for d in old['datasets'] if d['selected'] and d['split']=='development']
    req={ (r['dataset'],r['seed']):r for r in lines('results/v6/requests.jsonl') if r.get('split')=='development'}
    tokenizer=AutoTokenizer.from_pretrained('models/Qwen2.5-0.5B-Instruct',local_files_only=True,trust_remote_code=False)
    cases=[];checks=[];inputs={}
    for d in ds:
        c=load_candidates(d)
        for seed in old['seeds']:
            k=d['id']+'_'+str(seed);p=read(f'results/v6/prefixes/{k}.json');s=State(**p['state']).clone();r=req[(d['id'],seed)]
            assert messages(c,s)==r['messages'] and r['device']=='cpu' and r['dtype']=='torch.float32'
            forbidden=[symbols(c,c.x[i]) for i in s.ids];g=PrefixExcludingGrammar(tokenizer,c.domains,forbidden)
            # Synthetic token traversal only, never called an LLM response.
            tokens=[]
            while len(tokens)<len(g.schedule):tokens.append(g.allowed_after(tokens)[0])
            raw=tokenizer.decode(tokens,skip_special_tokens=True);assert len(raw.splitlines())==10 and not set(raw.splitlines())&set(forbidden)
            g.replay(tokens)
            cases.append({'dataset':d['id'],'seed':seed,'prefix_hash':p['prefix_hash'],'original_request_id':r['request_id'],'original_prompt_sha256':digest(r['messages'])})
            checks.append({'dataset':d['id'],'seed':seed,'namespace':'synthetic_token_traversal_no_inference','grammar_tokens':len(g.schedule),'valid':True})
            for part in ['prefixes','classical','paired']:
                path=f'results/v6/{part}/{k}.json';inputs[path]=sha(path)
    write('data/manifest_v7.json',{'version':7,'scope':'development-only post-v6 ablation','datasets':ds,'seeds':old['seeds'],'cases':cases,'reused_inputs':inputs})
    write('artifacts/study_v7/tokenizer_preflight.json',{'passed':True,'checks':checks,'real_model_calls':0})
    paths=list(Path('src/escalation').glob('*.py'))+list(Path('tests/synthetic').glob('*.py'))+[Path(p) for p in [
      'scripts/prepare_v7.py','reports/protocol_v7.md','data/manifest_v7.json','data/manifest_v6.json','results/v6/requests.jsonl',
      'configs/followup_v3.yaml','requirements.lock.txt','artifacts/study_v7/tokenizer_preflight.json']]+[Path(p) for p in inputs]
    write(freeze,{'at':now(),'scope':'fixed scientific treatment; authorization separately recorded, default denied','sha256':{str(p):sha(p) for p in sorted(set(paths))}})
    print('Frozen',len(set(paths)),'files; 15 real-tokenizer exclusion checks passed; zero inference')
if __name__=='__main__':main()
