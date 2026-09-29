"""Independent retrospective replay of v7 controls and available LLM branches."""
import sys,collections
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'src'))
from escalation.io import read,lines,write,digest
from escalation.data import sha
from escalation.core import State,project
from escalation.finite_domain import recommend
from escalation.finite_v6 import load_candidates,symbols,parse_symbols,messages
from escalation.grammar_v7 import PrefixExcludingGrammar,uniform_without_prefix
from escalation.study_v6 import retrospective_labels
from escalation.study_v7 import OUT,manifest,verify,run_config

def main():
    verify()
    for path in ['reports/protocol_v4.freeze.json','reports/registry_v5.freeze.json','reports/protocol_v6.freeze.json']:
        for p,h in read(path)['sha256'].items():assert sha(p)==h,p
    m=manifest();raw=lines(OUT/'acquisitions.jsonl');req=lines(OUT/'requests.jsonl');starts=lines(OUT/'request_starts.jsonl');progress=read(OUT/'progress.json')
    assert len(progress['intended'])==30 and all(r['dataset'] in {d['id'] for d in m['datasets']} for r in progress['intended'])
    ledger=read('artifacts/resource_ledger_v2.json');baseline=read(OUT/'manifest.json')['baseline_ledger']
    assert ledger['active_since'] is None and ledger['requests']<=run_config()['inference']['max_new_model_requests'] and ledger['experiment_seconds']<=1800
    assert ledger['requests']-baseline['requests']==len(starts)==len(req)<=15
    assert len(raw)==progress['actual_new_accesses']
    for r in raw:assert r['split']=='development' and r['namespace']=='measured_v7'
    tokens=None
    if req:
        approval=read(OUT/'authorization_at_inference_start.json')
        assert approval['authorization']['granted'] and approval['authorization']['request_cap']==113
        assert approval['authorization']['user_authorization']=='approve'
        assert all(r['started']>=approval['at'] for r in req)
        from transformers import AutoTokenizer
        tokens=AutoTokenizer.from_pretrained('models/Qwen2.5-0.5B-Instruct',local_files_only=True,trust_remote_code=False)
    completed=collections.Counter();copy_count=0;dynamic_removed=0
    for d in m['datasets']:
        c=load_candidates(d);ys=retrospective_labels(d,c)
        for seed in m['seeds']:
            k=d['id']+'_'+str(seed);p=read(f'results/v6/prefixes/{k}.json');forbidden=[symbols(c,c.x[i]) for i in p['state']['ids']]
            for arm in ['uniform_excluded','llm']:
                path=OUT/arm/f'{k}.json'
                if not path.exists():continue
                r=read(path);s=State(**p['state']).clone();assert r['prefix_hash']==p['prefix_hash']==digest(p['state'])
                assert r['state']['ids'][:10]==p['state']['ids'] and r['actual_new_accesses']==10
                assert r['state']['labels']==[ys[i] for i in r['state']['ids']]
                if arm=='uniform_excluded':assert r['proposals']==uniform_without_prefix(c.domains,forbidden,seed+40000,10)
                else:
                    response=next(q for q in req if q['request_id']==r['request_id'])
                    assert response['messages']==messages(c,s) and response['device']=='cpu' and response['dtype']=='torch.float32'
                    assert response['revision']=='7ae557604adf67be50417f59c2c2f167def9a775' and response['retry']==0
                    if r['status']=='completed':
                        grammar=PrefixExcludingGrammar(tokens,c.domains,forbidden)
                        assert response['forbidden_prefix_strings']==forbidden
                        assert len(response['generated_token_ids'])==len(grammar.schedule)<=1024
                        trace=grammar.replay(response['generated_token_ids'])
                        assert trace==response['exclusion_trace'] and grammar.sha256==response['grammar_sha256']
                        assert tokens.decode(response['generated_token_ids'],skip_special_tokens=True)==response['raw_output']
                        assert r['proposals']==parse_symbols(response['raw_output'],c)
                        assert response['output_tokens']==len(response['generated_token_ids']) and response['input_tokens']>0
                        rendered=tokens.apply_chat_template(response['messages'],tokenize=False,add_generation_prompt=True)
                        assert __import__('hashlib').sha256(rendered.encode()).hexdigest()==response['rendered_prompt_sha256']
                        assert len(tokens(rendered)['input_ids'])==response['input_tokens']
                        dynamic_removed+=len(trace)
                if r['proposals'] is not None:
                    copy_count+=sum(symbols(c,x) in forbidden for x in r['proposals'])
                    assert not any(symbols(c,x) in forbidden for x in r['proposals'])
                for j in range(10):
                    if r['proposals'] is None:i=recommend(c,s)
                    else:
                        i,event=project(c,s,r['proposals'][j]);assert all(r['events'][j][k]==v for k,v in event.items())
                    assert i==r['state']['ids'][10+j];s.observe(i,r['state']['labels'][10+j],c.directions)
                assert s.record()==r['state'] and len(set(s.ids))==20
                events=[e for e in raw if e['dataset']==d['id'] and e['seed']==seed and e['arm']==arm]
                assert len(events)==10 and [e['row_id'] for e in events]==s.ids[10:]
                completed[arm]+=1
    report={'verified':True,'completed_branches':dict(completed),'intended_per_arm':15,'new_acquisitions':len(raw),'new_model_requests':len(starts),
      'original_prefix_copies':copy_count,'dynamic_mask_positions_observed':dynamic_removed,'raw_states_replayed':True,'prior_freezes_intact':True,
      'only_development_groups':True,'request_cap':run_config()['inference']['max_new_model_requests'],'requests_used':ledger['requests'],
      'runtime_seconds':ledger['experiment_seconds'],'full_ablation_complete':progress['complete']}
    write('artifacts/study_v7/verification.json',report);print(__import__('json').dumps(report,indent=2))
if __name__=='__main__':main()
