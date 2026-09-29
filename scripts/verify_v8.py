"""Independent retrospective v8 source/label/state/token/budget replay."""
import sys,collections,hashlib
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'src'))
from escalation.io import read,lines,write,digest
from escalation.data import sha
from escalation.core import State,distances
from escalation.finite_domain import recommend,modal_centroid
from escalation.finite_v6 import load_candidates
from escalation.selection_v8 import shortlist,messages,parse_ids,control_rows
from escalation.grammar_v8 import CandidateIDGrammar
from escalation.study_v6 import retrospective_labels
from escalation.study_v8 import OUT,manifest,verify,run_config

def main():
    verify()
    for f in ['reports/protocol_v4.freeze.json','reports/registry_v5.freeze.json','reports/protocol_v6.freeze.json','reports/protocol_v7.freeze.json']:
        for p,h in read(f)['sha256'].items():assert sha(p)==h,p
    m=manifest();raw=lines(OUT/'acquisitions.jsonl');req=lines(OUT/'requests.jsonl');starts=lines(OUT/'request_starts.jsonl');progress=read(OUT/'progress.json')
    expected={(d['id'],seed,arm) for d in m['datasets'] for seed in m['seeds'] for arm in ['uniform_selection','static_rank','llm']}
    assert len(progress['intended'])==45 and {(r['dataset'],r['seed'],r['arm']) for r in progress['intended']}==expected
    ledger=read('artifacts/resource_ledger_v2.json');baseline=read(OUT/'manifest.json')['baseline_ledger']
    assert ledger['active_since'] is None and ledger['requests']<=run_config()['inference']['max_new_model_requests'] and ledger['experiment_seconds']<=1800
    assert ledger['requests']-baseline['requests']==len(starts)==len(req)<=15
    assert len(raw)==progress['actual_new_accesses']
    assert all(r['split']=='development' and r['namespace']=='measured_v8' for r in raw)
    tok=None
    if req:
        approval=read(OUT/'authorization_at_inference_start.json')
        assert approval['authorization']['granted'] and approval['authorization']['request_cap']==128 and approval['authorization']['user_authorization']
        assert all(r['started']>=approval['at'] for r in req)
        from transformers import AutoTokenizer
        tok=AutoTokenizer.from_pretrained('models/Qwen2.5-0.5B-Instruct',local_files_only=True,trust_remote_code=False)
    completed=collections.Counter();choices=0
    for d in m['datasets']:
        c=load_candidates(d);ys=retrospective_labels(d,c)
        for seed in m['seeds']:
            k=d['id']+'_'+str(seed);p=read(f'results/v6/prefixes/{k}.json');s0=State(**p['state']).clone();pool=shortlist(c,s0,seed)
            # Independent check of static score/tie ordering, before any branch state is replayed.
            available=[i for i in s0.order if i not in set(s0.ids)]
            b=modal_centroid(c,s0.best);rest=modal_centroid(c,s0.rest)
            scores={i:float(distances([c.x[i]],b)[0]-distances([c.x[i]],rest)[0]) for i in available}
            assert pool['ranked']==sorted(available,key=lambda i:scores[i])[:20]
            for arm in ['uniform_selection','static_rank','llm']:
                path=OUT/arm/(k+'.json')
                if not path.exists():continue
                r=read(path);s=s0.clone();assert r['prefix_hash']==p['prefix_hash']==digest(p['state']) and r['pool']==pool
                assert r['state']['ids'][:10]==s.ids and r['actual_new_accesses']==10
                assert r['state']['labels']==[ys[i] for i in r['state']['ids']]
                if arm!='llm':assert r['proposals']==control_rows(pool,seed,arm)
                else:
                    response=next(q for q in req if q['request_id']==r['request_id'])
                    assert response['messages']==messages(c,s,pool) and response['device']=='cpu' and response['dtype']=='torch.float32'
                    assert response['revision']=='7ae557604adf67be50417f59c2c2f167def9a775' and response['retry']==0
                    if r['status']=='completed':
                        grammar=CandidateIDGrammar(tok);trace=grammar.replay(response['generated_token_ids'])
                        assert trace==response['selection_trace'] and grammar.sha256==response['grammar_sha256']
                        assert grammar.schedule==response['grammar_schedule'] and grammar.choice_positions==response['model_choice_positions']
                        assert tok.decode(response['generated_token_ids'],skip_special_tokens=True)==response['raw_output']
                        assert r['proposals']==parse_ids(response['raw_output'],pool)
                        assert response['output_tokens']==len(response['generated_token_ids'])
                        rendered=tok.apply_chat_template(response['messages'],tokenize=False,add_generation_prompt=True)
                        assert hashlib.sha256(rendered.encode()).hexdigest()==response['rendered_prompt_sha256']
                        assert len(tok(rendered)['input_ids'])==response['input_tokens'];choices+=len(trace)
                if r['proposals'] is not None:
                    assert len(set(r['proposals']))==10 and set(r['proposals'])<=set(pool['ranked'])
                    assert not set(r['proposals'])&set(s.ids)
                for j in range(10):
                    i=recommend(c,s) if r['proposals'] is None else r['proposals'][j]
                    assert i==r['state']['ids'][10+j]==r['events'][j]['row_id'];s.observe(i,r['state']['labels'][10+j],c.directions)
                assert s.record()==r['state'] and len(set(s.ids))==20
                events=[e for e in raw if e['dataset']==d['id'] and e['seed']==seed and e['arm']==arm]
                assert len(events)==10 and [e['row_id'] for e in events]==s.ids[10:]
                assert all(float(e['raw_target'])==ys[e['row_id']][0] and e['source_line']==c.source_ids[e['row_id']] for e in events)
                completed[arm]+=1
    assert len(raw)==sum(completed.values())*10
    assert progress['complete']==(sum(completed.values())==45)
    report={'verified':True,'completed_branches':dict(completed),'intended_per_arm':15,'new_acquisitions':len(raw),'new_model_requests':len(starts),
      'model_choice_positions_verified':choices,'raw_states_replayed':True,'prior_freezes_intact':True,'only_development_groups':True,
      'request_cap':run_config()['inference']['max_new_model_requests'],'requests_used':ledger['requests'],'runtime_seconds':ledger['experiment_seconds'],'full_comparison_complete':progress['complete']}
    write('artifacts/study_v8/verification.json',report);print(__import__('json').dumps(report,indent=2))
if __name__=='__main__':main()
